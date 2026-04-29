"""
timezone_profile.py
-------------------
Stage 1b: Estimate time-zone traffic profile for all road links.

Trained on WebTRIS sensor sites (motorways + major A-roads with
time-resolved flow data). Predicts the *fraction* of daily traffic
in each time band — a dimensionless ratio independent of total volume.

Time bands (from differencing cumulative 12h/16h/18h/24h windows):

    | Code label | True period | Hours |
   |------------|-------------|------:|
   | `core_daytime_frac` | 07:00–18:59 | 12 |
   | `shoulder_frac` | 06–07 + 19–22 (mixed shoulder) | 4 |
   | `late_evening_frac` | 22:00–24:00 | 2 |
   | `overnight_frac` | 00:00–06:00 | 6 |

Why fractions, not absolute flows
----------------------------------
Absolute time-zone flows depend on total AADT (estimated in Stage 1a).
Predicting dimensionless fractions separates the volume question from the
shape question. Absolute flows for any link are then reconstructed as:

    flow_ph_core_daytime = estimated_aadt × core_daytime_frac / 12   (vehicles per hour)

Generalisation strategy
------------------------
WebTRIS sensors are concentrated on motorways and major A-roads (~5k
site×year rows). The daily profile shape is driven by road function,
proximity to urban centres, network position, and traffic volume — all
available network-wide from Stage 1a + network_features.parquet.
This extends time-zone profiles from ~5k training sites to all 2.1M links.

Outputs
-------
data/models/timezone_profiles.parquet
    link_id × year with columns:
        core_daytime_frac, shoulder_frac, late_evening_frac, overnight_frac
        flow_ph_core_daytime, flow_ph_shoulder, flow_ph_late_evening, flow_ph_overnight
        hgv_core_daytime_frac, hgv_ph_core_daytime
        core_overnight_ratio
"""

import logging

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold, cross_val_score

from road_risk.config import _ROOT
from road_risk.model.constants import COVID_YEARS, RANDOM_STATE

logger = logging.getLogger(__name__)

WEBTRIS_PATH = _ROOT / "data/processed/webtris/webtris_clean.parquet"
OPENROADS_PATH = _ROOT / "data/processed/shapefiles/openroads.parquet"
NET_FEATURES_PATH = _ROOT / "data/features/network_features.parquet"
AADT_ESTIMATES = _ROOT / "data/models/aadt_estimates.parquet"
PROFILES_OUT = _ROOT / "data/models/timezone_profiles.parquet"

# Fractions predicted by the model (all four — normalised to sum=1 on output)
FRACTION_TARGETS = [
    "core_daytime_frac",
    "shoulder_frac",
    "late_evening_frac",
    "overnight_frac",
]

# HGV fraction in peak (optional — predicted separately)
HGV_TARGET = "hgv_core_daytime_frac"


# ---------------------------------------------------------------------------
# Training data
# ---------------------------------------------------------------------------


def build_profile_training(webtris: pd.DataFrame) -> pd.DataFrame:
    """
    Build training DataFrame from WebTRIS sensor data.

    Computes time-zone fractions as targets, snaps each site to its nearest
    OpenRoads link, and joins network features.

    Returns
    -------
    DataFrame with feature columns + FRACTION_TARGETS + HGV_TARGET
    """
    df = webtris.copy()
    df = df[df["all_flow"] > 0].copy()

    # --- Compute fraction targets -------------------------------------------
    df["core_daytime_frac"] = (df["flow_ph_core_daytime"] * 12) / df["all_flow"]
    df["shoulder_frac"] = (df["flow_ph_shoulder"] * 4) / df["all_flow"]
    df["late_evening_frac"] = (df["flow_ph_late_evening"] * 2) / df["all_flow"]
    df["overnight_frac"] = (df["flow_ph_overnight"] * 6) / df["all_flow"]

    # HGV fraction of peak traffic relative to all HGVs on that road
    total_hgv = df["all_flow"] * df["hgv_pct"] / 100
    df["hgv_core_daytime_frac"] = np.where(
        total_hgv > 0,
        (df["hgv_ph_core_daytime"] * 12) / total_hgv,
        np.nan,
    )

    # Drop rows where fractions are implausible (data artefacts)
    frac_sum = df[FRACTION_TARGETS].sum(axis=1)
    df = df[frac_sum.between(0.98, 1.02)].copy()

    # log-transform of flow as a feature
    df["log_all_flow"] = np.log1p(df["all_flow"])

    year_min, year_max = df["year"].min(), df["year"].max()
    df["year_norm"] = (df["year"] - year_min) / max(year_max - year_min, 1)
    df["is_covid"] = df["year"].isin(COVID_YEARS).astype(int)

    # --- Snap to nearest OpenRoads link and join network features -----------
    df = _snap_to_network(df)

    n = len(df)
    logger.info(f"  Profile training set: {n:,} WebTRIS site×year rows")
    return df


def _snap_to_network(df: pd.DataFrame) -> pd.DataFrame:
    """Snap lat/lon points to nearest OpenRoads link and join network features."""
    if not (NET_FEATURES_PATH.exists() and OPENROADS_PATH.exists()):
        logger.warning("  Network features not found — training without")
        return df

    import geopandas as gpd
    import pyproj
    from scipy.spatial import cKDTree

    net = pd.read_parquet(NET_FEATURES_PATH)
    or_gdf = gpd.read_parquet(OPENROADS_PATH)
    or_bng = or_gdf.to_crs("EPSG:27700")

    link_xy = np.column_stack(
        [
            or_bng.geometry.centroid.x,
            or_bng.geometry.centroid.y,
        ]
    )
    tree = cKDTree(link_xy)

    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
    e, n_coord = transformer.transform(df["longitude"].values, df["latitude"].values)
    dists, idx = tree.query(np.column_stack([e, n_coord]), k=1, distance_upper_bound=2000)

    valid = dists < 2000
    snapped_link_ids = or_gdf["link_id"].values
    df = df.copy()
    df["_link_id"] = None
    df.loc[valid, "_link_id"] = snapped_link_ids[idx[valid]]

    net_cols = [c for c in net.columns if c != "link_id"]
    df = df.merge(
        net[["link_id"] + net_cols].rename(columns={"link_id": "_link_id"}),
        on="_link_id",
        how="left",
    ).drop(columns=["_link_id"])

    n_joined = df["degree_mean"].notna().sum()
    logger.info(
        f"  Network features joined for {n_joined:,} / {len(df):,} "
        f"WebTRIS sites ({n_joined / len(df):.1%})"
    )
    return df


def _feature_cols(df: pd.DataFrame) -> list[str]:
    """Return feature columns present in df."""
    candidates = [
        "log_all_flow",
        "latitude",
        "longitude",
        "year_norm",
        "is_covid",
        # network features (present when snap succeeded)
        "betweenness_relative",
        "betweenness",
        "dist_to_major_km",
        "pop_density_per_km2",
        "degree_mean",
    ]
    return [c for c in candidates if c in df.columns]


# ---------------------------------------------------------------------------
# Train
# ---------------------------------------------------------------------------


def train_profile_estimator(train_df: pd.DataFrame) -> tuple:
    """
    Train one HistGradientBoostingRegressor per fraction target plus one
    for hgv_core_daytime_frac.

    GroupKFold grouped by site_id so the same sensor never appears in both
    train and validation folds.

    Returns
    -------
    models   : dict target → fitted model
    metrics  : dict target → {cv_r2_mean, cv_r2_std, cv_mae_mean}
    feat_cols: list of feature column names used
    """
    feat_cols = _feature_cols(train_df)
    X = train_df[feat_cols].copy()
    groups = train_df["site_id"].values

    models = {}
    metrics = {}

    targets = FRACTION_TARGETS + [HGV_TARGET]
    for target in targets:
        if target not in train_df.columns:
            continue
        y = train_df[target].copy()
        valid = y.notna()
        if valid.sum() < 50:
            logger.warning(f"  {target}: only {valid.sum()} non-null rows — skipping")
            continue

        X_t = X[valid]
        y_t = y[valid]
        g_t = groups[valid]

        model = HistGradientBoostingRegressor(
            max_iter=300,
            max_depth=4,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
            verbose=0,
        )
        cv = GroupKFold(n_splits=5)
        cv_r2 = cross_val_score(model, X_t, y_t, groups=g_t, cv=cv, scoring="r2", n_jobs=-1)
        cv_mae = cross_val_score(
            model, X_t, y_t, groups=g_t, cv=cv, scoring="neg_mean_absolute_error", n_jobs=-1
        )
        model.fit(X_t, y_t)

        metrics[target] = {
            "cv_r2_mean": float(cv_r2.mean()),
            "cv_r2_std": float(cv_r2.std()),
            "cv_mae_mean": float(-cv_mae.mean()),
            "n_train": int(valid.sum()),
        }
        models[target] = model
        logger.info(
            f"  {target}: CV R²={cv_r2.mean():.3f} (±{cv_r2.std():.3f}) | MAE={-cv_mae.mean():.4f}"
        )

    return models, metrics, feat_cols


# ---------------------------------------------------------------------------
# Apply to all links
# ---------------------------------------------------------------------------


def apply_profile_estimator(
    models: dict,
    feat_cols: list,
    openroads,
    aadt_estimates: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply trained fraction models to all OS Open Roads links × years.

    For each link × year:
      1. Predict fraction of daily traffic in each time band.
      2. Normalise fractions to sum = 1 (corrects small model drift).
      3. Reconstruct absolute flow_ph_* from estimated_aadt × fraction.

    Returns
    -------
    DataFrame: link_id × year with fraction + flow_ph_* + core_overnight_ratio
    """
    import geopandas as gpd

    logger.info(f"Applying profile estimator to {len(openroads):,} links ...")

    or_df = openroads.copy()
    if isinstance(or_df, gpd.GeoDataFrame):
        bng = or_df.to_crs("EPSG:27700")
        centroids = bng.geometry.centroid.to_crs("EPSG:4326")
        or_df["latitude"] = centroids.y
        or_df["longitude"] = centroids.x

    # Join network features
    if NET_FEATURES_PATH.exists():
        net = pd.read_parquet(NET_FEATURES_PATH)
        net_cols = [c for c in net.columns if c != "link_id"]
        or_df = or_df.merge(net[["link_id"] + net_cols], on="link_id", how="left")

    years = sorted(aadt_estimates["year"].unique())
    year_min, year_max = years[0], years[-1]

    # Build a lookup: link_id × year → estimated_aadt
    aadt_lookup = aadt_estimates.set_index(["link_id", "year"])["estimated_aadt"]

    frames = []
    for year in years:
        pred_df = or_df.copy()
        pred_df["year"] = year
        pred_df["year_norm"] = (year - year_min) / max(year_max - year_min, 1)
        pred_df["is_covid"] = int(year in COVID_YEARS)

        # Traffic volume feature — use measured AADT where available, else estimate
        estimated = aadt_lookup.reindex(
            pd.MultiIndex.from_arrays([pred_df["link_id"], pred_df["year"]])
        ).values
        pred_df["log_all_flow"] = np.log1p(np.where(estimated > 0, estimated, 1))

        # Ensure all trained feature columns exist
        for fc in feat_cols:
            if fc not in pred_df.columns:
                pred_df[fc] = np.nan

        # HistGradientBoostingRegressor handles NaN natively. Keep missing
        # network features as NaN so inference follows the same missing-value
        # routing learned from WebTRIS training rows.
        X_pred = pred_df[feat_cols]

        # Predict each fraction
        preds = {}
        for target, model in models.items():
            if target in FRACTION_TARGETS:
                raw = model.predict(X_pred)
                preds[target] = np.clip(raw, 0.01, 0.99)

        # Normalise the four fractions to sum = 1
        if all(t in preds for t in FRACTION_TARGETS):
            frac_arr = np.column_stack([preds[t] for t in FRACTION_TARGETS])
            frac_arr = frac_arr / frac_arr.sum(axis=1, keepdims=True)
            for i, t in enumerate(FRACTION_TARGETS):
                preds[t] = frac_arr[:, i]

        # HGV peak fraction
        if HGV_TARGET in models:
            preds[HGV_TARGET] = np.clip(models[HGV_TARGET].predict(X_pred), 0.0, 1.0)

        out = pred_df[["link_id", "year"]].copy()
        for target, vals in preds.items():
            out[target] = vals

        # Reconstruct absolute per-hour flows from estimated_aadt × fraction
        aadt_vals = np.where(estimated > 0, estimated, np.expm1(pred_df["log_all_flow"].values))
        if "core_daytime_frac" in out.columns:
            out["flow_ph_core_daytime"] = aadt_vals * out["core_daytime_frac"] / 12
            out["flow_ph_shoulder"] = aadt_vals * out["shoulder_frac"] / 4
            out["flow_ph_late_evening"] = aadt_vals * out["late_evening_frac"] / 2
            out["flow_ph_overnight"] = aadt_vals * out["overnight_frac"] / 6
            out["core_overnight_ratio"] = out["flow_ph_core_daytime"] / out[
                "flow_ph_overnight"
            ].replace(0, np.nan)

        if HGV_TARGET in out.columns:
            # hgv_ph_core_daytime needs hgv proportion — use 0.05 as fallback
            hgv_prop = or_df.get("hgv_proportion", pd.Series(0.05, index=or_df.index)).values
            hgv_prop = np.where(np.isnan(hgv_prop), 0.05, hgv_prop)
            daily_hgv = aadt_vals * hgv_prop
            out["hgv_ph_core_daytime"] = daily_hgv * out[HGV_TARGET] / 12

        frames.append(out)

    result = pd.concat(frames, ignore_index=True)
    logger.info(
        f"  Profile estimates: {len(result):,} link × year rows | "
        f"median core_daytime_frac={result['core_daytime_frac'].median():.3f} | "
        f"median core_overnight_ratio={result['core_overnight_ratio'].median():.2f}"
    )
    return result


# ---------------------------------------------------------------------------
# End-to-end stage runner
# ---------------------------------------------------------------------------


def run_profile_stage(openroads) -> pd.DataFrame:
    """
    Run Stage 1b end-to-end: train profile estimator on WebTRIS data,
    apply to all OS Open Roads links, save timezone_profiles.parquet.

    Returns
    -------
    profiles DataFrame (link_id × year × fraction + flow columns)
    """
    from road_risk.config import _ROOT

    MODELS = _ROOT / "data/models"
    MODELS.mkdir(parents=True, exist_ok=True)

    if not WEBTRIS_PATH.exists():
        raise FileNotFoundError(f"WebTRIS clean parquet not found: {WEBTRIS_PATH}")
    if not AADT_ESTIMATES.exists():
        raise FileNotFoundError(
            f"AADT estimates not found: {AADT_ESTIMATES}\n"
            "Run Stage 1a first: python -m road_risk.model --stage traffic"
        )

    webtris = pd.read_parquet(WEBTRIS_PATH)
    aadt_estimates = pd.read_parquet(AADT_ESTIMATES)

    logger.info("Building profile training data ...")
    train_df = build_profile_training(webtris)

    logger.info("Training time-zone profile estimator ...")
    models, metrics, feat_cols = train_profile_estimator(train_df)

    logger.info("Applying profile estimator to all OS Open Roads links ...")
    profiles = apply_profile_estimator(models, feat_cols, openroads, aadt_estimates)

    profiles.to_parquet(MODELS / "timezone_profiles.parquet", index=False)
    logger.info(
        f"  Saved timezone_profiles to {MODELS / 'timezone_profiles.parquet'} "
        f"({len(profiles):,} rows)"
    )
    return profiles, metrics
