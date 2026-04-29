"""
aadt.py
-------
Stage 1a: Estimate Annual Average Daily Traffic (AADT) for all road links.

Trained on AADF count points and applied to all OS Open Roads links to fill
coverage gaps.

Key design decisions
--------------------
- GroupKFold CV grouped by count_point_id prevents data leakage (same station
  in multiple years must stay in one fold).
- Predictions for ALL years in AADF training data so the collision model
  always has AADT coverage — no links are dropped due to missing exposure.
- Year-de-meaned log-AADT target lets the model learn road-level differences
  while year means are added back at inference.
- WebTRIS time-zone features are intentionally excluded from Stage 1a because
  they are not available for every Open Roads link at inference time.

External validation
-------------------
Standard GroupKFold CV is optimistic for an interpolation model: nearby
count points share road class, urban context, and network structure, so
held-out stations are effectively close to training stations.

Two holdout schemes are used to probe harder extrapolation tasks:

  1. Local holdout  — withhold 20% of count_point_ids at random.
     Tests whether the model can fill realistic local gaps.

  2. Spatial block  — withhold all count points inside a geographic tile
     (default: northern quarter of the study area).
     Tests whether the model can generalise to less-supported geography.

After evaluation the production model is retrained on all available counts.
"""

import logging
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold, cross_val_score

from road_risk.config import _ROOT, cfg
from road_risk.model.constants import COVID_YEARS, RANDOM_STATE

logger = logging.getLogger(__name__)

OPENROADS_PATH = _ROOT / cfg["paths"]["processed"] / "shapefiles/openroads.parquet"
NET_FEATURES_PATH = _ROOT / cfg["paths"]["features"] / "network_features.parquet"
WEBTRIS_PATH = _ROOT / cfg["paths"]["processed"] / "webtris/webtris_clean.parquet"
AADT_ESTIMATES_PATH = _ROOT / cfg["paths"]["models"] / "aadt_estimates.parquet"

# WebTRIS features used in Stage 1a AADT training.
# Must be empty: core_overnight_ratio is produced by Stage 1b (timezone_profile),
# which runs *after* Stage 1a. At inference, no real sensor values exist for
# the full 2.1M-link network, so the column was being filled with 0 via
# fillna(0). HistGBR routes NaN and 0 through different tree branches, so
# filling NaN→0 corrupts ~80% of training rows' equivalent signal and collapses
# the full-network predictions to near-mean. Keep this list empty.
WEBTRIS_AADT_FEATURES: list[str] = []
COUNTED_ESTIMATION_METHOD = "Counted"
BNG_FALLBACK_PROJ = (
    "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 "
    "+x_0=400000 +y_0=-100000 +ellps=airy +units=m +no_defs"
)


def filter_counted_aadf_for_training(
    aadf: pd.DataFrame,
    *,
    context: str = "AADT training",
) -> pd.DataFrame:
    """
    Keep only directly counted AADF rows for model fitting/evaluation.

    DfT AADF includes direct counts and interpolated estimates. Stage 1a should
    learn from the direct-count signal only, then still apply the trained model
    to every Open Roads link/year at inference time.
    """
    if "estimation_method" not in aadf.columns:
        logger.warning(
            "  AADF estimation_method column missing for %s — using all %s rows",
            context,
            f"{len(aadf):,}",
        )
        return aadf.copy()

    method = aadf["estimation_method"].astype("string").str.strip()
    counted_mask = method.eq(COUNTED_ESTIMATION_METHOD)

    logger.info(
        "  AADF estimation_method before %s filter:\n%s",
        context,
        method.value_counts(dropna=False).to_string(),
    )

    has_counted_by_point = counted_mask.groupby(aadf["count_point_id"]).any()
    estimated_only_points = has_counted_by_point[~has_counted_by_point].index
    if len(estimated_only_points) > 0:
        examples = ", ".join(map(str, estimated_only_points[:10]))
        logger.warning(
            "  %s count_point_id values have no Counted rows in the training "
            "window and will be absent after filtering. Examples: %s",
            f"{len(estimated_only_points):,}",
            examples,
        )

    filtered = aadf.loc[counted_mask].copy()
    if filtered.empty:
        raise ValueError(
            f"No AADF rows with estimation_method == {COUNTED_ESTIMATION_METHOD!r}; "
            "cannot train AADT estimator."
        )

    missing_years = sorted(set(aadf["year"].unique()) - set(filtered["year"].unique()))
    if missing_years:
        logger.warning(
            "  Counted-only %s data is missing years: %s",
            context,
            missing_years,
        )

    n_groups = filtered["count_point_id"].nunique()
    if n_groups < 5:
        raise ValueError(
            "Counted-only AADF data has fewer than 5 count_point_id groups; "
            "GroupKFold(n_splits=5) cannot run."
        )

    logger.info(
        "  Counted-only %s filter: %s → %s rows | %s → %s count points",
        context,
        f"{len(aadf):,}",
        f"{len(filtered):,}",
        f"{aadf['count_point_id'].nunique():,}",
        f"{n_groups:,}",
    )
    return filtered


def _openroads_reference_lonlat(openroads) -> tuple[np.ndarray, np.ndarray]:
    """
    Return one lon/lat reference point per OpenRoads geometry.

    The processed OpenRoads parquet stores coordinates as lon/lat, but some
    environments read the CRS with latitude/longitude axis metadata. Calling
    GeoPandas.to_crs() can then swap axes and yield invalid projected
    coordinates. When bounds show lon/lat-like coordinates, use the stored
    coordinates directly and let pyproj handle later transforms with
    always_xy=True.
    """
    bounds = np.asarray(openroads.total_bounds, dtype=float)
    looks_lonlat = (
        np.isfinite(bounds).all()
        and -180 <= bounds[0] <= 180
        and -90 <= bounds[1] <= 90
        and -180 <= bounds[2] <= 180
        and -90 <= bounds[3] <= 90
    )
    geom_source = openroads if looks_lonlat else openroads.to_crs("EPSG:4326")

    geom_types = geom_source.geometry.geom_type
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Geometry is in a geographic CRS.*",
            category=UserWarning,
        )
        if geom_types.str.contains("LineString", na=False).all():
            points = geom_source.geometry.interpolate(0.5, normalized=True)
        else:
            points = geom_source.geometry.centroid

    return points.x.to_numpy(), points.y.to_numpy()


def _transform_wgs84_to_bng(
    lon: np.ndarray,
    lat: np.ndarray,
    *,
    context: str,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Transform WGS84 lon/lat arrays to British National Grid coordinates.

    Some PROJ/GDAL environments return non-finite coordinates for EPSG:27700.
    That failure mode is explicitly logged with affected row counts before
    falling back to a local BNG Transverse Mercator definition.
    """
    import pyproj

    lon = np.asarray(lon, dtype=float)
    lat = np.asarray(lat, dtype=float)

    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
    x, y = transformer.transform(lon, lat)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    nonfinite = ~np.isfinite(x) | ~np.isfinite(y)
    if not nonfinite.any():
        return x, y

    n_bad = int(nonfinite.sum())
    logger.warning(
        "  EPSG:27700 transform returned non-finite coordinates for %s / %s "
        "%s rows (%.1f%%). lon=[%.4f, %.4f], lat=[%.4f, %.4f]. Using local "
        "British National Grid fallback projection for this transform.",
        f"{n_bad:,}",
        f"{len(lon):,}",
        context,
        n_bad / max(len(lon), 1) * 100,
        np.nanmin(lon),
        np.nanmax(lon),
        np.nanmin(lat),
        np.nanmax(lat),
    )

    fallback = pyproj.Transformer.from_crs("EPSG:4326", BNG_FALLBACK_PROJ, always_xy=True)
    x, y = fallback.transform(lon, lat)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    fallback_nonfinite = ~np.isfinite(x) | ~np.isfinite(y)
    if fallback_nonfinite.any():
        logger.warning(
            "  BNG fallback transform still returned non-finite coordinates for "
            "%s / %s %s rows (%.1f%%). These rows will be skipped downstream.",
            f"{int(fallback_nonfinite.sum()):,}",
            f"{len(lon):,}",
            context,
            fallback_nonfinite.mean() * 100,
        )
    return x, y


def build_aadt_features(aadf: pd.DataFrame) -> tuple:
    """
    Build feature matrix and year-de-meaned log-AADT target from AADF data.

    Design: target is de-meaned by year before training so the model learns
    road-level deviation from each year's network-wide average. The year means
    are returned separately and added back at inference. This prevents year_norm
    (a feature that is CONSTANT within each year at inference) from absorbing
    51% of importance and collapsing full-network predictions to near the
    year mean for every link.

    Network features are joined by snapping each count point to its nearest
    OS Open Roads link via KD-tree (2km cap).

    Returns
    -------
    X          : feature DataFrame (no year_norm — handled via year_means)
    y          : year-de-meaned log1p(all_motor_vehicles) target Series
    df_full    : enriched aadf with all joined columns (for group CV)
    year_means : Series indexed by year — mean log1p(AADF) per year, used
                 to reconstruct absolute predictions at inference
    """
    from road_risk.model.constants import ROAD_CLASS_ORDINAL

    df = aadf.copy()

    target_raw = np.log1p(df["all_motor_vehicles"])

    # Per-year mean of log-AADT — captures temporal trend (growth + COVID dip).
    # Stored separately; subtracted from training target so the model focuses
    # on road-level differentiation rather than year trend.
    year_means = target_raw.groupby(df["year"]).mean()
    target = target_raw - df["year"].map(year_means)

    # road_class_ord from AADF road_name — M/A/B prefixes identify class
    # directly and reliably (corr=0.76 with log-AADT). Spatial snap assigns
    # wrong classes too often (M62 count point → slip road in OpenRoads).
    # Uses a 4-level encoding {1, 4, 5, 6} matching the inference-side mapping
    # in apply_aadt_estimator so train and infer see the same ordinal space.
    def _road_name_to_ord(name: str) -> int:
        if pd.isna(name):
            return 1
        n = str(name).strip()
        if n.startswith("M"):
            return ROAD_CLASS_ORDINAL["Motorway"]  # 6
        if n.startswith("A"):
            return ROAD_CLASS_ORDINAL["A Road"]  # 5
        if n.startswith("B"):
            return ROAD_CLASS_ORDINAL["B Road"]  # 4
        return 1  # Unclassified / minor

    df["road_class_ord"] = df["road_name"].apply(_road_name_to_ord)
    df["is_trunk"] = df["road_name"].str.match(r"^[MA]\d", na=False).astype(int)

    # is_covid stays as a binary indicator: captures residual within-year
    # variation (different road types may respond differently to COVID). The
    # global COVID level is already captured by year_means de-meaning.
    feature_cols = [
        "road_class_ord",
        "is_trunk",
        "latitude",
        "longitude",
        "is_covid",
        "hgv_proportion",
    ]

    if "link_length_km" in df.columns:
        df["link_length_km"] = df.groupby("road_class_ord")["link_length_km"].transform(
            lambda x: x.fillna(x.median() if x.notna().any() else 0)
        )
        feature_cols.append("link_length_km")

    # --- WebTRIS time-zone features (empty by default — see WEBTRIS_AADT_FEATURES) -
    if WEBTRIS_PATH.exists() and WEBTRIS_AADT_FEATURES:
        df = _attach_webtris_features(df)
        for col in WEBTRIS_AADT_FEATURES:
            if col in df.columns:
                feature_cols.append(col)

    # --- Network features via KD-tree snap to OpenRoads ---------------------
    if NET_FEATURES_PATH.exists() and OPENROADS_PATH.exists():
        import geopandas as gpd
        from scipy.spatial import cKDTree

        net = pd.read_parquet(NET_FEATURES_PATH)
        net_cols = [c for c in net.columns if c != "link_id"]

        or_gdf = gpd.read_parquet(OPENROADS_PATH)
        link_lon, link_lat = _openroads_reference_lonlat(or_gdf)
        link_e, link_n = _transform_wgs84_to_bng(
            link_lon,
            link_lat,
            context="OpenRoads",
        )
        link_xy = np.column_stack([link_e, link_n])
        finite_links = np.isfinite(link_xy).all(axis=1)
        if not finite_links.any():
            raise ValueError("No finite OpenRoads reference points available for AADF snapping.")
        if not finite_links.all():
            logger.warning(
                "  Skipping %s OpenRoads links with non-finite centroids for "
                "AADF network-feature snap",
                f"{(~finite_links).sum():,}",
            )
        link_xy = link_xy[finite_links]
        snapped_ids = or_gdf["link_id"].values[finite_links]
        tree = cKDTree(link_xy)

        aadf_e, aadf_n = _transform_wgs84_to_bng(
            df["longitude"].values,
            df["latitude"].values,
            context="AADF",
        )
        aadf_xy = np.column_stack([aadf_e, aadf_n])
        finite_aadf = np.isfinite(aadf_xy).all(axis=1)
        if not finite_aadf.all():
            logger.warning(
                "  Skipping %s AADF rows with non-finite coordinates for network-feature snap",
                f"{(~finite_aadf).sum():,}",
            )
        dists = np.full(len(df), np.inf)
        idx = np.full(len(df), len(snapped_ids))
        dists[finite_aadf], idx[finite_aadf] = tree.query(
            aadf_xy[finite_aadf],
            k=1,
            distance_upper_bound=2000,
        )
        valid = dists < 2000
        df["_snapped_link_id"] = None
        df.loc[valid, "_snapped_link_id"] = snapped_ids[idx[valid]]

        df = df.merge(
            net[["link_id"] + net_cols].rename(columns={"link_id": "_snapped_link_id"}),
            on="_snapped_link_id",
            how="left",
        ).drop(columns=["_snapped_link_id"])

        n_joined = df["degree_mean"].notna().sum()
        logger.info(
            f"  Network features joined for {n_joined:,} / {len(df):,} "
            f"AADF count points ({n_joined / len(df):.1%}) via direct KD-tree snap"
        )
        for col in net_cols:
            if col in df.columns:
                feature_cols.append(col)
    else:
        logger.info(
            "  Network features or OpenRoads not found — training without (CV R² will be lower)"
        )

    X = df[feature_cols].copy()
    return X, target, df, year_means


def _attach_webtris_features(aadf: pd.DataFrame) -> pd.DataFrame:
    """
    Spatial nearest-neighbour join of WebTRIS time-zone features onto AADF
    count points, per year. 5km cap — beyond this a sensor is too remote to
    represent the count point's road type.

    Only the WEBTRIS_AADT_FEATURES columns are attached. NaN where no sensor
    is within the cap.
    """
    import geopandas as gpd

    wt = pd.read_parquet(WEBTRIS_PATH)
    wt_years = set(wt["year"].unique())
    aadf_years = set(aadf["year"].unique())

    # Only join for years present in both datasets
    common_years = wt_years & aadf_years
    if not common_years:
        logger.info("  WebTRIS: no overlapping years with AADF — skipping")
        return aadf

    cols_needed = ["site_id", "year", "latitude", "longitude"] + [
        c for c in WEBTRIS_AADT_FEATURES if c in wt.columns
    ]
    wt = wt[[c for c in cols_needed if c in wt.columns]].copy()

    wt_gdf = gpd.GeoDataFrame(
        wt,
        geometry=gpd.points_from_xy(wt["longitude"], wt["latitude"]),
        crs="EPSG:4326",
    ).to_crs("EPSG:27700")

    aadf_gdf = gpd.GeoDataFrame(
        aadf,
        geometry=gpd.points_from_xy(aadf["longitude"], aadf["latitude"]),
        crs="EPSG:4326",
    ).to_crs("EPSG:27700")

    wt_feature_cols = [c for c in WEBTRIS_AADT_FEATURES if c in wt.columns]

    result_frames = []
    for year in sorted(aadf["year"].unique()):
        aadf_yr = aadf_gdf[aadf_gdf["year"] == year].copy()
        if year in wt_years:
            wt_yr = wt_gdf[wt_gdf["year"] == year][wt_feature_cols + ["geometry"]].copy()
            joined = gpd.sjoin_nearest(
                aadf_yr,
                wt_yr,
                how="left",
                max_distance=5000,
                distance_col="_wt_dist",
            )
            joined = joined[~joined.index.duplicated(keep="first")]
            far = joined["_wt_dist"].isna()
            if far.any():
                joined.loc[far, wt_feature_cols] = np.nan
            joined = joined.drop(columns=["_wt_dist", "geometry", "index_right"], errors="ignore")
            n_matched = (~far).sum()
            logger.info(
                f"  WebTRIS {year}: {n_matched:,} / {len(aadf_yr):,} AADF points matched within 5km"
            )
        else:
            joined = aadf_yr.drop(columns=["geometry"])
            for col in wt_feature_cols:
                joined[col] = np.nan
        result_frames.append(joined)

    return pd.concat(result_frames, ignore_index=True)


def train_aadt_estimator(aadf: pd.DataFrame, *, counted_only: bool = True) -> tuple:
    """
    Train gradient boosting AADT estimator with GroupKFold cross-validation.

    Returns
    -------
    model    : fitted HistGradientBoostingRegressor
    metrics  : dict with CV R², MAE
    features : list of feature column names
    """
    logger.info("Training AADT estimator ...")

    if counted_only:
        aadf = filter_counted_aadf_for_training(aadf, context="AADT training")

    X, y, df, year_means = build_aadt_features(aadf)
    groups = df["count_point_id"].values
    n_groups = df["count_point_id"].nunique()
    if n_groups < 5:
        raise ValueError(
            "AADT estimator needs at least 5 count_point_id groups for GroupKFold(n_splits=5)."
        )

    model = HistGradientBoostingRegressor(
        max_iter=300,
        max_depth=5,
        learning_rate=0.05,
        random_state=RANDOM_STATE,
        verbose=0,
    )

    cv = GroupKFold(n_splits=5)
    cv_r2 = cross_val_score(model, X, y, groups=groups, cv=cv, scoring="r2", n_jobs=-1)
    cv_mae = cross_val_score(
        model, X, y, groups=groups, cv=cv, scoring="neg_mean_absolute_error", n_jobs=-1
    )

    model.fit(X, y)

    perm = permutation_importance(model, X, y, n_repeats=5, random_state=RANDOM_STATE)
    importance = pd.Series(perm.importances_mean, index=X.columns).sort_values(ascending=False)

    metrics = {
        "cv_r2_mean": float(cv_r2.mean()),
        "cv_r2_std": float(cv_r2.std()),
        "cv_mae_mean": float(-cv_mae.mean()),
        "cv_mae_std": float(cv_mae.std()),
        "n_train": len(X),
    }

    logger.info(
        f"  AADT estimator CV R²: {metrics['cv_r2_mean']:.3f} "
        f"(±{metrics['cv_r2_std']:.3f}) | "
        f"MAE: {metrics['cv_mae_mean']:.3f} log-units"
    )
    logger.info(f"  Feature importance:\n{importance.to_string()}")

    return model, metrics, X.columns.tolist(), year_means


def apply_aadt_estimator(
    model,
    feature_cols: list,
    openroads,
    aadf: pd.DataFrame,
    year_means: pd.Series,
) -> pd.DataFrame:
    """
    Apply trained AADT estimator to ALL OS Open Roads links × AADF years.

    Produces estimated_aadt for every link × every year that appears in the
    training data. No links are dropped — this is the full exposure denominator
    for the collision model.

    Returns
    -------
    DataFrame with columns: link_id, year, estimated_aadt
    """
    import geopandas as gpd

    logger.info(f"Applying AADT estimator to {len(openroads):,} OS Open Roads links ...")

    or_df = openroads.copy()
    if isinstance(or_df, gpd.GeoDataFrame):
        lon, lat = _openroads_reference_lonlat(or_df)
        or_df["latitude"] = lat
        or_df["longitude"] = lon

    # road_class_ord: must use the same 4-level bucketing as build_aadt_features().
    # Training derives ord from AADF road_name prefix (M=6, A=5, B=4, else=1).
    # OS Open Roads has a 7-class road_classification; collapse to the same 4
    # levels so inference sees only values the model was trained on.
    # Limitation: AADF road_name is reliable (road names on count-point records
    # match the road being counted). OS Open Roads road_classification is also
    # authoritative for network links. The mismatch is that training had no
    # "Classified Unnumbered" or "Not Classified" class — those collapse to 1.
    _INFER_CLASS_MAP = {"Motorway": 6, "A Road": 5, "B Road": 4}
    or_df["road_class_ord"] = (
        or_df["road_classification"].map(_INFER_CLASS_MAP).fillna(1).astype(int)
    )
    or_df["is_trunk"] = or_df["road_classification"].isin(["Motorway", "A Road"]).astype(int)

    if NET_FEATURES_PATH.exists():
        net = pd.read_parquet(NET_FEATURES_PATH)
        net_cols = [c for c in net.columns if c != "link_id"]
        or_df = or_df.merge(net[["link_id"] + net_cols], on="link_id", how="left")
        n_joined = or_df["degree_mean"].notna().sum()
        logger.info(f"  Network features joined for {n_joined:,} / {len(or_df):,} links")

    years = sorted(aadf["year"].unique())

    # Median fallbacks for features not present on all OpenRoads links
    hgv_median = aadf["hgv_proportion"].median()
    length_median = aadf["link_length_km"].median() if "link_length_km" in aadf.columns else 1.0

    frames = []
    for year in years:
        pred_df = or_df.copy()
        pred_df["year"] = year
        pred_df["is_covid"] = int(year in COVID_YEARS)

        # Fill missing AADF-derived columns with overall medians
        if "hgv_proportion" not in pred_df.columns:
            pred_df["hgv_proportion"] = hgv_median
        else:
            pred_df["hgv_proportion"] = pred_df["hgv_proportion"].fillna(hgv_median)

        if "link_length_km" not in pred_df.columns:
            pred_df["link_length_km"] = length_median
        else:
            pred_df["link_length_km"] = pred_df["link_length_km"].fillna(length_median)

        # Ensure all trained feature columns exist. NaN is intentional: HistGBR
        # routes NaN the same way it learned during training (native missing-
        # value handling). Do NOT fillna(0) — zero and NaN take different tree
        # branches and would corrupt predictions for features that were NaN in
        # ~80% of training rows (e.g. pop_density_per_km2 for rural links).
        for fc in feature_cols:
            if fc not in pred_df.columns:
                pred_df[fc] = np.nan
        X_pred = pred_df[feature_cols]
        # Model predicts year-de-meaned log-AADT; add the training year mean back.
        # Falls back to the nearest observed year if this year is outside the
        # training range (e.g. a future prediction year).
        year_mean = year_means.get(
            year, year_means.iloc[np.argmin(np.abs(year_means.index - year))]
        )
        log_pred = model.predict(X_pred) + year_mean
        pred_df["estimated_aadt"] = np.expm1(log_pred).round().clip(1).astype(int)
        frames.append(pred_df[["link_id", "year", "estimated_aadt"]])

    result = pd.concat(frames, ignore_index=True)
    logger.info(
        f"  Estimated AADT: median={result['estimated_aadt'].median():,.0f} "
        f"vehicles/day | range {result['estimated_aadt'].min():,}–"
        f"{result['estimated_aadt'].max():,}"
    )
    return result


def validate_aadt_external(aadf: pd.DataFrame, *, counted_only: bool = True) -> dict:
    """
    External validation of the AADT estimator using two holdout schemes.

    Standard GroupKFold CV is optimistic: withheld stations are still
    surrounded by nearby training stations with similar road context.
    These schemes probe harder extrapolation tasks.

    Scheme 1 — Local holdout
        Withhold 20% of count_point_ids at random. The model has no
        measurements from those specific stations but has nearby ones.
        Tests: can the model fill realistic local gaps?

    Scheme 2 — Spatial block
        Withhold all count points in the northern quarter of the study
        area (latitude > 75th percentile of all count points). The model
        has no support in that region.
        Tests: can the model generalise to less-supported geography?

    For each scheme, reports R², MAE, RMSE overall and by road class.

    Returns
    -------
    dict with keys 'local' and 'spatial', each containing:
        r2, mae, rmse : float — overall metrics (log scale)
        by_class      : DataFrame — metrics per road_type
        n_holdout     : int — number of held-out rows
    """
    logger.info("Running external validation ...")

    if counted_only:
        aadf = filter_counted_aadf_for_training(
            aadf,
            context="AADT external validation",
        )

    rng = np.random.default_rng(RANDOM_STATE)
    results = {}

    for scheme in ("local", "spatial"):
        # --- Define holdout mask --------------------------------------------
        if scheme == "local":
            all_pts = aadf["count_point_id"].unique()
            n_hold = max(1, int(len(all_pts) * 0.20))
            held_pts = rng.choice(all_pts, size=n_hold, replace=False)
            holdout_mask = aadf["count_point_id"].isin(held_pts)
        else:
            lat_thresh = aadf["latitude"].quantile(0.75)
            holdout_mask = aadf["latitude"] > lat_thresh

        train_df = aadf[~holdout_mask].copy()
        test_df = aadf[holdout_mask].copy()

        if train_df.empty or test_df.empty:
            logger.warning(f"  {scheme}: empty train or test split — skipping")
            continue

        # --- Train on held-in, predict on held-out --------------------------
        X_train, y_train, _, train_year_means = build_aadt_features(train_df)
        X_test, _, df_test, _ = build_aadt_features(test_df)

        # y_test: raw observed log-scale (not de-meaned). Using the test set's
        # own log1p directly avoids shifting observed values by (train_mean -
        # test_mean), which would inflate R² in spatial holdout where the held-
        # out region may have a systematically different traffic level.
        y_test = np.log1p(test_df["all_motor_vehicles"].values)

        # Align columns — test may have columns train doesn't (or vice versa)
        shared = [c for c in X_train.columns if c in X_test.columns]
        X_train = X_train[shared]
        X_test = X_test[shared]

        model = HistGradientBoostingRegressor(
            max_iter=300,
            max_depth=5,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
            verbose=0,
        )
        model.fit(X_train, y_train)
        # Reconstruct raw log predictions: de-meaned model output + training year mean.
        # Using training year means (not test year means) is the correct out-of-sample
        # setup — the model has no access to the test set's year-level statistics.
        year_adj = df_test["year"].map(train_year_means).fillna(train_year_means.mean()).values
        y_pred = model.predict(X_test) + year_adj

        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred) ** 0.5

        logger.info(
            f"  {scheme} holdout: R²={r2:.3f} | MAE={mae:.3f} | "
            f"RMSE={rmse:.3f} (log scale) | n={len(y_test):,}"
        )

        # --- Metrics by road class ------------------------------------------
        test_with_pred = test_df.copy().reset_index(drop=True)
        test_with_pred["_y_true"] = y_test
        test_with_pred["_y_pred"] = y_pred

        road_class_col = next(
            (c for c in ["road_type", "road_classification"] if c in test_with_pred.columns),
            None,
        )
        if road_class_col:
            by_class = (
                test_with_pred.groupby(road_class_col)
                .apply(
                    lambda g: pd.Series(
                        {
                            "r2": r2_score(g["_y_true"], g["_y_pred"]) if len(g) > 1 else np.nan,
                            "mae": mean_absolute_error(g["_y_true"], g["_y_pred"]),
                            "rmse": mean_squared_error(g["_y_true"], g["_y_pred"]) ** 0.5,
                            "n": len(g),
                        }
                    ),
                    include_groups=False,
                )
                .reset_index()
            )
        else:
            by_class = pd.DataFrame()

        results[scheme] = {
            "r2": r2,
            "mae": mae,
            "rmse": rmse,
            "n_holdout": int(len(y_test)),
            "by_class": by_class,
        }

    # Save results as parquet for the QMD page
    MODELS = _ROOT / cfg["paths"]["models"]
    MODELS.mkdir(parents=True, exist_ok=True)
    rows = []
    for scheme, res in results.items():
        rows.append(
            {
                "scheme": scheme,
                "r2": res["r2"],
                "mae": res["mae"],
                "rmse": res["rmse"],
                "n_holdout": res["n_holdout"],
            }
        )
        if not res["by_class"].empty:
            bc = res["by_class"].copy()
            bc["scheme"] = scheme
            bc.to_parquet(MODELS / f"aadt_validation_{scheme}.parquet", index=False)

    pd.DataFrame(rows).to_parquet(MODELS / "aadt_validation_summary.parquet", index=False)
    logger.info("  External validation results saved to data/models/")

    return results


def run_traffic_stage(aadf: pd.DataFrame, openroads) -> pd.DataFrame:
    """
    Run Stage 1a end-to-end: train estimator, apply to all links, save.

    Saves aadt_estimates.parquet and returns the estimates DataFrame.
    Always regenerates — never loads from cache — so the network always
    reflects the current openroads.parquet.
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    MODELS = _ROOT / cfg["paths"]["models"]
    MODELS.mkdir(parents=True, exist_ok=True)

    # Stage 1a learns only from directly counted AADF rows. The full AADF table
    # is still passed to inference so prediction covers every link × AADF year.
    training_aadf = filter_counted_aadf_for_training(aadf, context="AADT stage")

    # External validation before fitting production model on counted data
    val_results = validate_aadt_external(training_aadf, counted_only=False)

    model, metrics, features, year_means = train_aadt_estimator(
        training_aadf,
        counted_only=False,
    )
    metrics["n_train_all_aadf_rows"] = len(aadf)
    metrics["n_train_counted_rows"] = len(training_aadf)
    metrics["external_validation"] = {
        scheme: {"r2": r["r2"], "mae": r["mae"], "rmse": r["rmse"], "n": r["n_holdout"]}
        for scheme, r in val_results.items()
    }
    estimates = apply_aadt_estimator(model, features, openroads, aadf, year_means)

    # Training residuals
    X_train, y_train, _, _ = build_aadt_features(training_aadf)
    y_pred = model.predict(X_train)
    logger.info(
        f"  Training residuals (log scale):\n"
        f"    MAE  : {mean_absolute_error(y_train, y_pred):.4f}\n"
        f"    RMSE : {mean_squared_error(y_train, y_pred) ** 0.5:.4f}\n"
        f"    R²   : {r2_score(y_train, y_pred):.4f}"
    )

    estimates.to_parquet(MODELS / "aadt_estimates.parquet", index=False)
    logger.info(
        f"  Saved AADT estimates: {len(estimates):,} rows "
        f"({estimates['link_id'].nunique():,} links × {estimates['year'].nunique()} years)"
    )

    import pickle

    with open(MODELS / "aadt_model.pkl", "wb") as fh:
        pickle.dump({"model": model, "features": features, "year_means": year_means}, fh)
    logger.info("  Saved aadt_model.pkl")

    return estimates, model, metrics, features
