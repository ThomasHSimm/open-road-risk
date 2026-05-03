"""
collision.py
------------
Stage 2: Poisson GLM + XGBoost collision risk model.

Architecture
------------
Train on all links × AADF years (2019, 2021, 2023) using year_norm and
is_covid as temporal features. This pools collision data across years,
giving better statistical power for rare per-link-per-year events.

Score ALL links — not just those with observed collisions. A link with
zero collisions and valid exposure is a genuine low-risk observation.

Output: one row per link_id with pooled collision count, mean predicted
rate, and a single stable risk_percentile ranked across all links.

Key design decisions
--------------------
- No AADT filter: after Stage 1a every link has estimated_aadt. Rows
  with no AADT should not exist; if they do, impute median per road class.
- Pooled scoring: percentile is computed over mean(predicted_xgb) across
  years, not per-year. Removes year selector from the app entirely.
- year_norm and is_covid remain as training features to capture temporal
  trend and Covid anomaly — they just don't appear in the output grain.
"""

import json
import logging

import numpy as np
import pandas as pd

from road_risk.config import _ROOT, cfg
from road_risk.model.constants import (
    COVID_YEARS,
    FORM_OF_WAY_ORDINAL,
    RANDOM_STATE,
    ROAD_CLASS_ORDINAL,
)

logger = logging.getLogger(__name__)

# GLM zero-downsampling ratio: keep all positive link-years but sample
# zero-collision rows to this multiple. Prevents OOM on statsmodels dense
# design matrix (18M rows × 15 features × float64 ≈ 2GB+).
# XGBoost is not affected — it handles full dataset via its own chunking.
# Ratio of 10 gives ~4M rows (391k positives × ~10 zeros) — sufficient
# for stable GLM coefficient estimation on rare-event Poisson data.
GLM_ZERO_SAMPLE_RATIO = 10
SCORE_CHUNK_ROWS = 1_000_000

MODELS = _ROOT / cfg["paths"]["models"]
OPENROADS_PATH = _ROOT / cfg["paths"]["processed"] / "shapefiles/openroads.parquet"
RLA_PATH = _ROOT / cfg["paths"]["features"] / "road_link_annual.parquet"
TRAFFIC_FEATURES_PATH = _ROOT / cfg["paths"]["features"] / "road_traffic_features.parquet"
NET_PATH = _ROOT / cfg["paths"]["features"] / "network_features.parquet"
AADT_PATH = MODELS / "aadt_estimates.parquet"

# Collision-derived context columns can be useful diagnostics, but they are
# post-event aggregates from snapped STATS19 records. They must not enter the
# Stage 2 training dataframe or pooled risk output as if they were pre-collision
# road attributes.
FORBIDDEN_POST_EVENT_COLS = {
    "pct_dark",
    "pct_urban",
    "pct_junction",
    "pct_near_crossing",
    "mean_speed_limit",
}


def _assert_no_post_event_features(feature_cols: list[str], *, context: str) -> None:
    """Fail fast if collision-derived diagnostics enter a model feature list."""
    feature_roots = {c.removesuffix("_imputed") for c in feature_cols}
    forbidden = sorted(feature_roots & FORBIDDEN_POST_EVENT_COLS)
    if forbidden:
        raise ValueError(
            f"Post-event collision-derived columns cannot be used as {context} "
            f"features: {forbidden}"
        )


def build_collision_dataset(
    openroads,
    aadt_estimates: pd.DataFrame,
    rla: pd.DataFrame,
    net_features: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Build full collision dataset for Poisson modelling.

    Includes ALL links × ALL AADF years (not just collision links).
    Zero-collision links are genuine low-risk observations.

    Parameters
    ----------
    openroads      : GeoDataFrame with link geometry and attributes
    aadt_estimates : link_id × year × estimated_aadt (all links, all years)
    rla            : road_link_annual — collision counts per link × year
    net_features   : optional network features

    Returns
    -------
    DataFrame at link_id × year grain ready for GLM/XGBoost training
    """
    # Use only years that have AADT estimates
    years = sorted(aadt_estimates["year"].unique())
    logger.info(
        f"Building collision dataset: {len(openroads):,} links × {len(years)} years ({years}) ..."
    )

    links = openroads[
        [
            "link_id",
            "road_classification",
            "form_of_way",
            "link_length_km",
            "is_trunk",
            "is_primary",
        ]
    ].copy()

    # Base: all links × all AADF years
    base = pd.DataFrame(
        {
            "link_id": np.repeat(links["link_id"].values, len(years)),
            "year": np.tile(years, len(links)),
        }
    ).merge(links, on="link_id", how="left")

    logger.info(f"  Base table: {len(base):,} rows")

    # Join collision counts — NaN → 0 for links with no collisions
    rla_cols = [
        "link_id",
        "year",
        "collision_count",
        "fatal_count",
        "serious_count",
        "slight_count",
        "casualty_count",
    ]
    excluded_post_event = sorted(FORBIDDEN_POST_EVENT_COLS & set(rla.columns))
    if excluded_post_event:
        logger.info(
            "  Excluding post-event diagnostic columns from Stage 2 model dataset: %s",
            ", ".join(excluded_post_event),
        )
    rla_trim = rla[[c for c in rla_cols if c in rla.columns]].copy()
    base = base.merge(rla_trim, on=["link_id", "year"], how="left")
    base["collision_count"] = base["collision_count"].fillna(0).astype(int)
    base["fatal_count"] = base["fatal_count"].fillna(0).astype(int)
    base["serious_count"] = base["serious_count"].fillna(0).astype(int)

    n_with = (base["collision_count"] > 0).sum()
    logger.info(
        f"  Collisions joined: {n_with:,} link-years with ≥1 collision "
        f"({n_with / len(base):.2%} of all link-years)"
    )

    # Join pre-collision traffic features from the all-link × year table.
    # These must not be sourced from road_link_annual, which is collision-
    # aggregate-first and therefore has no rows for zero-collision link-years.
    if TRAFFIC_FEATURES_PATH.exists():
        traffic_cols = ["link_id", "year", "hgv_proportion"]
        traffic = pd.read_parquet(TRAFFIC_FEATURES_PATH, columns=traffic_cols)
        if "hgv_proportion" in traffic.columns:
            if traffic.duplicated(["link_id", "year"]).any():
                raise RuntimeError("road_traffic_features.parquet has duplicate link_id/year rows")
            before_rows = len(base)
            base = base.merge(traffic, on=["link_id", "year"], how="left")
            if len(base) != before_rows:
                raise RuntimeError(
                    "Traffic feature join changed Stage 2 row count; "
                    "road_traffic_features must be unique by link_id/year"
                )
            n_hgv = base["hgv_proportion"].notna().sum()
            logger.info(
                f"  Traffic features joined: hgv_proportion present on "
                f"{n_hgv:,} / {len(base):,} rows ({n_hgv / len(base):.1%})"
            )
        else:
            logger.warning(
                "  road_traffic_features.parquet has no hgv_proportion column — skipping"
            )
    else:
        logger.warning(
            "  road_traffic_features.parquet not found — hgv_proportion unavailable. "
            "Run road_risk.clean_join.join to persist all-link traffic features."
        )

    # Join AADT — every link should have an estimate after Stage 1a
    base = base.merge(aadt_estimates, on=["link_id", "year"], how="left")
    n_missing_aadt = base["estimated_aadt"].isna().sum()
    if n_missing_aadt > 0:
        # Should not happen after Stage 1a covers all links — impute as fallback
        logger.warning(
            f"  {n_missing_aadt:,} rows missing estimated_aadt — "
            "imputing median per road class (check Stage 1a output)"
        )
        median_aadt = base.groupby("road_classification")["estimated_aadt"].transform(
            lambda x: x.fillna(x.median() if x.notna().any() else 500)
        )
        base["estimated_aadt"] = base["estimated_aadt"].fillna(median_aadt)

    # Compute log exposure offset: log(AADT × length_km × 365 / 1e6)
    base["link_length_km"] = base["link_length_km"].fillna(
        base.groupby("road_classification")["link_length_km"].transform(
            lambda x: x.fillna(x.median() if x.notna().any() else 0.5)
        )
    )
    vehicle_km_M = base["estimated_aadt"] * base["link_length_km"] * 365 / 1e6
    base["log_offset"] = np.log(vehicle_km_M.clip(lower=1e-6))

    # Road feature encoding
    base["road_class_ord"] = (
        base["road_classification"].map(ROAD_CLASS_ORDINAL).fillna(0).astype(int)
    )
    base["form_of_way_ord"] = base["form_of_way"].map(FORM_OF_WAY_ORDINAL).fillna(1).astype(int)
    base["is_motorway"] = (base["road_classification"] == "Motorway").astype(int)
    base["is_a_road"] = (base["road_classification"] == "A Road").astype(int)
    base["is_slip_road"] = (base["form_of_way"] == "Slip Road").astype(int)
    base["is_roundabout"] = (base["form_of_way"] == "Roundabout").astype(int)
    base["is_dual"] = (
        base["form_of_way"].isin(["Dual Carriageway", "Collapsed Dual Carriageway"]).astype(int)
    )
    base["is_trunk"] = base["is_trunk"].fillna(False).astype(int)
    base["is_primary"] = base["is_primary"].fillna(False).astype(int)

    # Temporal features (training only — pooled away in scoring output)
    base["is_covid"] = base["year"].isin(COVID_YEARS).astype(int)
    year_min, year_max = base["year"].min(), base["year"].max()
    base["year_norm"] = (base["year"] - year_min) / max(year_max - year_min, 1)
    base["log_link_length"] = np.log(base["link_length_km"].clip(lower=0.001))

    if net_features is not None:
        base = base.merge(net_features, on="link_id", how="left")
        n_net = base["degree_mean"].notna().sum()
        logger.info(
            f"  Network features joined: {n_net:,} / {len(base):,} rows ({n_net / len(base):.1%})"
        )

    logger.info(
        f"  Collision dataset: {len(base):,} rows | "
        f"zeros={(base['collision_count'] == 0).sum():,} "
        f"({(base['collision_count'] == 0).mean():.1%})"
    )
    return base


def train_collision_glm(df: pd.DataFrame) -> tuple:
    """
    Fit Poisson GLM with AADT log-offset. Returns result, features, summary.
    """
    try:
        import statsmodels.api as sm
    except ImportError as e:
        raise ImportError("pip install statsmodels") from e

    logger.info("Fitting Poisson GLM (statsmodels) ...")

    core_cols = [
        "road_class_ord",
        "form_of_way_ord",
        "is_motorway",
        "is_a_road",
        "is_slip_road",
        "is_roundabout",
        "is_dual",
        "is_trunk",
        "is_primary",
        "log_link_length",
        "is_covid",
        "year_norm",
    ]

    # Optional contextual/network features. Policy:
    #   - any feature meeting MIN_COVERAGE_FOR_INCLUSION is included via
    #     median-imputation
    #   - features below SKIP_MISSING_FLAG_COVERAGE additionally get a
    #     missingness indicator column (lets the GLM separate "missing"
    #     from "imputed median value")
    #   - features above SKIP_MISSING_FLAG_COVERAGE get imputation only
    #     (the missing flag would be a near-zero-variance column with
    #     no estimation power, just memory cost)
    #
    # This keeps the GLM training population CONSTANT across feature
    # additions. The previous policy (raw column above 50% coverage,
    # then dropna) silently changed the estimation sample whenever a
    # partial-coverage feature was added, confounding feature-effect
    # with sample-effect.
    #
    # Materialisation policy: imputed/missing columns are computed on
    # the DOWNSAMPLED frame, not on the full 21.7M-row df, to keep
    # peak memory in budget.
    network_candidates = [
        "hgv_proportion",
        "degree_mean",
        "betweenness",
        "betweenness_relative",
        "dist_to_major_km",
        "pop_density_per_km2",
        "speed_limit_mph_effective",
        "lanes",
        "is_unpaved",
        "imd_decile",
        "imd_crime_decile",
        "imd_living_indoor_decile",
        "mean_grade",
    ]
    MIN_COVERAGE_FOR_INCLUSION = 0.05
    SKIP_MISSING_FLAG_COVERAGE = 0.99

    # Phase 1 — coverage scan only. Decide which candidates to include
    # and what their median values will be. NO column materialisation
    # on `df` here.
    feature_specs = []  # list of (raw_col, median_val, imputed_name, missing_name_or_None)
    for col in network_candidates:
        if col not in df.columns:
            logger.info(f"  {col}: not in dataset — skipping")
            continue
        coverage = df[col].notna().mean()
        if coverage < MIN_COVERAGE_FOR_INCLUSION:
            logger.info(
                f"  {col}: {coverage:.1%} coverage below "
                f"{MIN_COVERAGE_FOR_INCLUSION:.0%} threshold — skipping"
            )
            continue

        median_val = df[col].median()
        imputed_name = f"{col}_imputed"
        missing_name = f"{col}_missing" if coverage < SKIP_MISSING_FLAG_COVERAGE else None
        feature_specs.append((col, median_val, imputed_name, missing_name))
        flag_note = "" if missing_name is None else f" + {missing_name}"
        logger.info(
            f"  {col}: {coverage:.1%} coverage — imputing median={median_val:.4g}, "
            f"adding {imputed_name}{flag_note}"
        )

    # Build the feature_cols list in deterministic order: core first, then
    # imputed columns, then missing flags (grouped so the coefficient
    # table reads sensibly).
    feature_cols = list(core_cols)
    feature_cols.extend(spec[2] for spec in feature_specs)
    feature_cols.extend(spec[3] for spec in feature_specs if spec[3] is not None)
    _assert_no_post_event_features(feature_cols, context="GLM")

    # Phase 2 — downsample on raw data. Use only collision_count and
    # log_offset to decide row inclusion; no imputed columns yet.
    raw_optional_cols = [spec[0] for spec in feature_specs]
    minimal_cols = list(core_cols) + raw_optional_cols + ["collision_count", "log_offset"]
    minimal_cols = [c for c in minimal_cols if c in df.columns]

    # Drop only on core_cols + log_offset; optional cols may be NaN and
    # will be handled by imputation below. This is the methodological
    # change from the old policy.
    core_required = list(core_cols) + ["log_offset"]
    core_required = [c for c in core_required if c in df.columns]
    full_idx = df.dropna(subset=core_required).index
    n_dropped_core = len(df) - len(full_idx)
    if n_dropped_core > 0:
        logger.info(f"  Dropped {n_dropped_core:,} rows missing core features")

    pos_mask = df.loc[full_idx, "collision_count"] > 0
    pos_idx = pos_mask[pos_mask].index
    zero_idx = pos_mask[~pos_mask].index
    n_pos = len(pos_idx)
    n_zeros_keep = min(len(zero_idx), n_pos * GLM_ZERO_SAMPLE_RATIO)
    zeros_sample_idx = zero_idx.to_series().sample(n=n_zeros_keep, random_state=RANDOM_STATE).index
    selected_idx = pos_idx.union(zeros_sample_idx).sort_values()
    logger.info(
        f"  GLM downsampled: {n_pos:,} positives + {n_zeros_keep:,} zeros "
        f"= {len(selected_idx):,} rows (ratio 1:{GLM_ZERO_SAMPLE_RATIO})"
    )

    # Phase 3 — materialise the GLM frame ONLY for selected rows.
    glm_df = df.loc[selected_idx, minimal_cols].copy()
    for raw_col, median_val, imputed_name, missing_name in feature_specs:
        glm_df[imputed_name] = glm_df[raw_col].fillna(median_val)
        if missing_name is not None:
            glm_df[missing_name] = glm_df[raw_col].isna().astype("int8")
        # Drop the raw column once we've derived imputed/missing — saves memory
        # and prevents accidentally fitting on the wrong column.
        glm_df.drop(columns=[raw_col], inplace=True)

    X = sm.add_constant(glm_df[feature_cols].astype(float))
    y = glm_df["collision_count"].astype(int)
    result = sm.GLM(
        y,
        X,
        family=sm.families.Poisson(),
        offset=glm_df["log_offset"].astype(float),
    ).fit(maxiter=100)

    summary = {
        "n_obs": len(glm_df),
        "n_pos": int(n_pos),
        "n_full": len(full_idx),
        "deviance": float(result.deviance),
        "null_deviance": float(result.null_deviance),
        "pseudo_r2": float(1 - result.deviance / result.null_deviance),
        "aic": float(result.aic),
        "converged": result.converged,
        "features": feature_cols,
    }

    logger.info(
        f"  Poisson GLM: pseudo-R²={summary['pseudo_r2']:.3f} | "
        f"deviance={summary['deviance']:,.0f} | "
        f"AIC={summary['aic']:,.0f} | converged={summary['converged']}"
    )

    coef_df = pd.DataFrame(
        {
            "coef": result.params,
            "pvalue": result.pvalues,
            "ci_low": result.conf_int()[0],
            "ci_high": result.conf_int()[1],
        }
    ).round(4)
    sig = coef_df[coef_df["pvalue"] < 0.05].sort_values("coef", ascending=False)
    logger.info(f"  Significant coefficients (p<0.05):\n{sig.to_string()}")

    result._road_risk_imputed_features = {
        imputed_name: (raw_col, median_val)
        for raw_col, median_val, imputed_name, _missing_name in feature_specs
    }
    result._road_risk_missing_features = {
        missing_name: raw_col
        for raw_col, _median_val, _imputed_name, missing_name in feature_specs
        if missing_name is not None
    }

    return result, feature_cols, summary


def train_collision_xgb(df: pd.DataFrame, seed: int = RANDOM_STATE) -> tuple:
    """
    Fit XGBoost Poisson regression. Returns model, features, metrics.
    """
    try:
        from xgboost import XGBRegressor
    except ImportError as e:
        raise ImportError("pip install xgboost") from e

    from sklearn.model_selection import GroupShuffleSplit

    logger.info(f"Fitting XGBoost Poisson model (seed={seed}) ...")

    feature_cols = [
        "road_class_ord",
        "form_of_way_ord",
        "is_motorway",
        "is_a_road",
        "is_slip_road",
        "is_roundabout",
        "is_dual",
        "is_trunk",
        "is_primary",
        "log_link_length",
        "estimated_aadt",
        "is_covid",
        "year_norm",
    ]
    for col in [
        "hgv_proportion",
        "degree_mean",
        "betweenness",
        "betweenness_relative",
        "dist_to_major_km",
        "pop_density_per_km2",
        "speed_limit_mph_effective",
        "lanes",
        "is_unpaved",
        "imd_decile",
        "imd_crime_decile",
        "imd_living_indoor_decile",
        "mean_grade",
    ]:
        if col in df.columns:
            feature_cols.append(col)
    _assert_no_post_event_features(feature_cols, context="XGBoost")

    model_df = df[feature_cols + ["collision_count", "log_offset"]].copy()
    model_df[feature_cols] = model_df[feature_cols].fillna(0)
    model_df["log_offset"] = model_df["log_offset"].fillna(0)

    logger.info(f"  XGBoost training rows: {len(model_df):,}")

    # XGBoost computes in float32 internally; explicit downcast avoids
    # silent float64 copies of the 21.7M-row training matrix and resolves
    # the Int8/extension-dtype interop where pd.NA -> np.nan upcast forces
    # an additional copy.
    X = model_df[feature_cols].astype("float32")
    y = model_df["collision_count"].astype(int)
    offsets = model_df["log_offset"].values.astype("float32")

    # XGBoost Poisson with exposure offset via base_margin.
    # base_margin sets the initial prediction in log-space so the model
    # learns collision rate conditional on exposure (vehicle-km), matching
    # the GLM formulation. Without this, XGBoost learns absolute counts
    # and systematically overestimates risk on high-traffic links.
    model = XGBRegressor(
        objective="count:poisson",
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=seed,
        n_jobs=1,
        verbosity=0,  # pin for cross-machine reproducibility
    )

    # GroupShuffleSplit by link_id: all years for a given link stay in one
    # fold, preventing the same link appearing in both train and test.
    # A random row split is optimistic because repeated-year rows for the
    # same link leak network structure across the split boundary.
    groups = df["link_id"].values
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    idx_train, idx_test = next(gss.split(X, y, groups=groups))
    X_train, X_test = X.iloc[idx_train], X.iloc[idx_test]
    y_train, y_test = y.iloc[idx_train], y.iloc[idx_test]
    off_train, off_test = offsets[idx_train], offsets[idx_test]

    model.fit(
        X_train,
        y_train,
        base_margin=off_train,
        eval_set=[(X_test, y_test)],
        base_margin_eval_set=[off_test],
        verbose=False,
    )
    y_pred = model.predict(X_test, base_margin=off_test)

    eps = 1e-6
    deviance = 2 * np.sum(
        np.where(y_test > 0, y_test * np.log((y_test + eps) / (y_pred + eps)), 0)
        - (y_test - y_pred)
    )
    null_pred = np.full_like(y_pred, y_test.mean())
    null_dev = 2 * np.sum(
        np.where(y_test > 0, y_test * np.log((y_test + eps) / (null_pred + eps)), 0)
        - (y_test - null_pred)
    )
    pseudo_r2 = 1 - deviance / null_dev if null_dev > 0 else np.nan

    importance = pd.Series(model.feature_importances_, index=feature_cols).sort_values(
        ascending=False
    )

    metrics = {
        "n_train": len(X_train),
        "n_test": len(X_test),
        "pseudo_r2": float(pseudo_r2),
        "deviance": float(deviance),
        "features": feature_cols,
        "seed": int(seed),
        "n_jobs": 1,
    }

    logger.info(f"  XGBoost Poisson: pseudo-R²={pseudo_r2:.3f} | test deviance={deviance:,.0f}")
    logger.info(f"  Feature importance (top 10):\n{importance.head(10).to_string()}")

    return model, feature_cols, metrics


def score_collision_models(
    glm_result,
    xgb_model,
    glm_features: list,
    xgb_features: list,
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply both models to full dataset and pool across years.

    Pooling logic:
    - collision_count : sum across years (total observed)
    - estimated_aadt  : mean across years
    - predicted_glm   : mean across years (expected rate at mean traffic)
    - residual_glm    : total_collisions - total_predicted (pooled excess)
    - risk_percentile : rank of mean predicted_xgb across all links (single stable rank)

    One row per link_id — no year dimension in the output.
    """
    logger.info("Applying models and pooling across years ...")

    # Score per link × year. GLM imputed/missing columns are rebuilt here
    # instead of being materialised on the full modelling frame after training.
    # That keeps peak scoring memory lower and avoids retaining ~GBs of derived
    # columns that are only needed for prediction.
    imputed_features = getattr(glm_result, "_road_risk_imputed_features", {})
    missing_features = getattr(glm_result, "_road_risk_missing_features", {})
    # Avoid a full-frame defensive copy here: at national scale this can double
    # scoring memory. The caller's df is intentionally annotated with temporary
    # prediction columns before pooling.
    predicted_glm = np.empty(len(df), dtype="float32")
    predicted_xgb = np.empty(len(df), dtype="float32")

    def _build_glm_design(chunk: pd.DataFrame) -> pd.DataFrame:
        glm_feature_data = {}
        for feature in glm_features:
            if feature in chunk.columns:
                glm_feature_data[feature] = chunk[feature]
            elif feature in imputed_features:
                raw_col, median_val = imputed_features[feature]
                glm_feature_data[feature] = chunk[raw_col].fillna(median_val)
            elif feature in missing_features:
                raw_col = missing_features[feature]
                glm_feature_data[feature] = chunk[raw_col].isna().astype("int8")
            elif feature.endswith("_imputed") and feature[: -len("_imputed")] in chunk.columns:
                raw_col = feature[: -len("_imputed")]
                glm_feature_data[feature] = chunk[raw_col].fillna(chunk[raw_col].median())
            elif feature.endswith("_missing") and feature[: -len("_missing")] in chunk.columns:
                raw_col = feature[: -len("_missing")]
                glm_feature_data[feature] = chunk[raw_col].isna().astype("int8")
            else:
                raise KeyError(f"GLM feature {feature!r} cannot be built for scoring")

        X_glm = pd.DataFrame(glm_feature_data, index=chunk.index).fillna(0).astype("float32")
        if "const" not in X_glm.columns:
            X_glm.insert(0, "const", np.float32(1.0))
        return X_glm

    for start in range(0, len(df), SCORE_CHUNK_ROWS):
        end = min(start + SCORE_CHUNK_ROWS, len(df))
        chunk = df.iloc[start:end]
        X_glm = _build_glm_design(chunk)
        glm_pred = glm_result.predict(
            X_glm,
            offset=chunk["log_offset"].fillna(0).astype("float32"),
        )
        predicted_glm[start:end] = np.asarray(glm_pred, dtype="float32")
        del X_glm

        X_xgb = chunk[xgb_features].fillna(0).astype("float32")
        predicted_xgb[start:end] = xgb_model.predict(
            X_xgb,
            base_margin=chunk["log_offset"].fillna(0).astype("float32").values,
        ).astype("float32", copy=False)
        del X_xgb

    df["predicted_glm"] = predicted_glm
    df["predicted_xgb"] = predicted_xgb

    # Pool to one row per link
    pool_agg = {
        "collision_count": "sum",
        "fatal_count": "sum",
        "serious_count": "sum",
        "estimated_aadt": "mean",
        "predicted_glm": "mean",
        "predicted_xgb": "mean",
    }
    # Include optional pre-collision attributes if present.
    for col in [
        "hgv_proportion",
        "speed_limit_mph",
        "speed_limit_mph_effective",
        "betweenness_relative",
        "road_classification",
    ]:
        if col in df.columns:
            pool_agg[col] = "first"

    pooled = df.groupby("link_id").agg(pool_agg).reset_index()

    # Diagnostic residual: observed minus GLM-predicted total.
    # The GLM was trained on downsampled zeros (ratio 1:10), which biases
    # the intercept. Use residual_glm for spatial pattern diagnosis only —
    # not as a calibrated excess-collision count.
    n_years = df["year"].nunique()
    pooled["residual_glm"] = pooled["collision_count"] - pooled["predicted_glm"] * n_years

    # Single stable risk percentile — ranked on XGBoost (higher pseudo-R² than GLM)
    pooled["risk_percentile"] = pooled["predicted_xgb"].rank(pct=True) * 100

    logger.info(
        f"  Risk scores applied to {len(pooled):,} links\n"
        f"  Mean predicted collisions/year: {pooled['predicted_glm'].mean():.4f}\n"
        f"  Links in top 1% risk: {(pooled['risk_percentile'] >= 99).sum():,}"
    )

    save_cols = [
        "link_id",
        "collision_count",
        "fatal_count",
        "serious_count",
        "estimated_aadt",
        "predicted_glm",
        "predicted_xgb",
        "residual_glm",
        "risk_percentile",
        "road_classification",
        "hgv_proportion",
        "speed_limit_mph_effective",
        "speed_limit_mph",
        "betweenness_relative",
    ]
    final_cols = [c for c in save_cols if c in pooled.columns]

    return pooled[final_cols]


def score_and_save(
    glm_result,
    xgb_model,
    glm_features: list,
    xgb_features: list,
    glm_summary: dict,
    xgb_metrics: dict,
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply both models to full dataset, pool across years, save risk_scores.parquet.
    """
    pooled = score_collision_models(glm_result, xgb_model, glm_features, xgb_features, df)

    # Save
    MODELS.mkdir(parents=True, exist_ok=True)

    glm_result.save(str(MODELS / "collision_glm.pkl"))
    xgb_model.save_model(str(MODELS / "collision_xgb.json"))

    pooled.to_parquet(MODELS / "risk_scores.parquet", index=False)
    logger.info(f"  Saved risk scores: {len(pooled):,} links")

    with open(MODELS / "collision_metrics.json", "w") as f:
        json.dump({"glm": glm_summary, "xgb": xgb_metrics}, f, indent=2)

    return pooled


def run_collision_stage() -> pd.DataFrame:
    """
    Run Stage 2 end-to-end. Loads all required inputs, trains, scores, saves.
    """
    import geopandas as gpd

    logger.info("=== Stage 2: Collision model ===")

    openroads = gpd.read_parquet(OPENROADS_PATH)
    rla = pd.read_parquet(RLA_PATH)
    net_features = pd.read_parquet(NET_PATH) if NET_PATH.exists() else None
    if net_features is None:
        logger.warning("Network features not found — run network_features.py first")

    if not AADT_PATH.exists():
        raise FileNotFoundError(
            f"AADT estimates not found at {AADT_PATH}. Run --stage traffic first."
        )
    aadt_estimates = pd.read_parquet(AADT_PATH)

    df = build_collision_dataset(openroads, aadt_estimates, rla, net_features)

    glm_result, glm_features, glm_summary = train_collision_glm(df)

    try:
        xgb_model, xgb_features, xgb_metrics = train_collision_xgb(df)
    except ImportError:
        logger.warning("XGBoost not installed — skipping. pip install xgboost")
        return None

    risk_scores = score_and_save(
        glm_result,
        xgb_model,
        glm_features,
        xgb_features,
        glm_summary,
        xgb_metrics,
        df,
    )

    # Print summary
    print("\n=== Collision model results ===")
    print(f"  Poisson GLM pseudo-R²: {glm_summary['pseudo_r2']:.3f}")
    print(f"  Training rows: {glm_summary['n_obs']:,}")
    print(f"  XGBoost pseudo-R²: {xgb_metrics['pseudo_r2']:.3f}")
    print(f"  Links scored: {len(risk_scores):,} (pooled — no year dimension)")
    print(f"  Top 1% risk links: {(risk_scores['risk_percentile'] >= 99).sum():,}")
    if "road_classification" in risk_scores.columns:
        print(
            risk_scores[risk_scores["risk_percentile"] >= 99]["road_classification"]
            .value_counts()
            .head(6)
            .to_string()
        )

    return risk_scores
