"""
collision.py
------------
Stage 2: Poisson GLM + XGBoost collision risk model.

Architecture
------------
Train with model-specific zero-collision handling. The GLM keeps all positive
link-years and uses documented zero downsampling for memory. XGBoost defaults
to the full available link-year population unless an explicit sampled-zero
mode is requested.

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

import argparse
import gc
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
# design matrix at GB scale.
# Ratio of 3 gives ~1.6M rows for GB (391k positives × ~3 zeros): enough
# for a baseline coefficient check without trying to pickle a multi-GB GLM.
GLM_ZERO_SAMPLE_RATIO = 3
# XGBoost zero handling is a modelling choice, not a memory implementation
# detail. Default to full-zero training to preserve the original design; use
# --xgb-zero-policy sampled only as an explicit memory fallback.
XGB_ZERO_POLICY = "full"
XGB_ZERO_SAMPLE_RATIO = 10
XGB_ZERO_POLICIES = {"full", "sampled"}
SCORE_CHUNK_ROWS = 1_000_000
SMOKE_POSITIVE_LINKS = 800
SMOKE_LINKS_PER_COUNTRY = 300

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

GB_CONTEXT_REQUIRED_COLS = [
    "pop_density_per_km2",
    "population_nation",
    "overall_decile_within_country",
    "income_decile_within_country",
    "employment_decile_within_country",
    "deprivation_country_england",
    "deprivation_country_wales",
    "deprivation_country_scotland",
    "ruc_class",
    "ruc_urban_rural",
    "ruc_country",
]

OPTIONAL_MODEL_FEATURE_COLS = [
    "hgv_proportion",
    "degree_mean",
    "betweenness",
    "betweenness_relative",
    "dist_to_major_km",
    "pop_density_per_km2",
    "speed_limit_mph_effective",
    "lanes",
    "is_unpaved",
    "overall_decile_within_country",
    "income_decile_within_country",
    "employment_decile_within_country",
    "deprivation_country_england",
    "deprivation_country_wales",
    "deprivation_country_scotland",
    "mean_grade",
]

NETWORK_FEATURE_COLS_FOR_COLLISION = [
    "link_id",
    "speed_limit_mph",
    *[col for col in OPTIONAL_MODEL_FEATURE_COLS if col != "hgv_proportion"],
]

OPENROADS_COLS_FOR_COLLISION = [
    "link_id",
    "road_classification",
    "form_of_way",
    "link_length_km",
    "is_trunk",
    "is_primary",
]

RLA_COLS_FOR_COLLISION = [
    "link_id",
    "year",
    "collision_count",
    "fatal_count",
    "serious_count",
    "slight_count",
    "casualty_count",
]

TRAFFIC_COLS_FOR_COLLISION = ["link_id", "year", "hgv_proportion"]
AADT_COLS_FOR_COLLISION = ["link_id", "year", "estimated_aadt"]


def _assert_no_post_event_features(feature_cols: list[str], *, context: str) -> None:
    """Fail fast if collision-derived diagnostics enter a model feature list."""
    feature_roots = {c.removesuffix("_imputed") for c in feature_cols}
    forbidden = sorted(feature_roots & FORBIDDEN_POST_EVENT_COLS)
    if forbidden:
        raise ValueError(
            f"Post-event collision-derived columns cannot be used as {context} "
            f"features: {forbidden}"
        )


def _finalise_collision_features(base: pd.DataFrame) -> pd.DataFrame:
    """Add exposure, road encodings and temporal model features in place."""
    n_missing_aadt = base["estimated_aadt"].isna().sum()
    if n_missing_aadt > 0:
        logger.warning(
            f"  {n_missing_aadt:,} rows missing estimated_aadt — "
            "imputing median per road class (check Stage 1a output)"
        )
        median_aadt = base.groupby("road_classification")["estimated_aadt"].transform(
            lambda x: x.fillna(x.median() if x.notna().any() else 500)
        )
        base["estimated_aadt"] = base["estimated_aadt"].fillna(median_aadt)

    base["link_length_km"] = base["link_length_km"].fillna(
        base.groupby("road_classification")["link_length_km"].transform(
            lambda x: x.fillna(x.median() if x.notna().any() else 0.5)
        )
    )
    vehicle_km_M = base["estimated_aadt"] * base["link_length_km"] * 365 / 1e6
    base["log_offset"] = np.log(vehicle_km_M.clip(lower=1e-6)).astype("float32")

    base["road_class_ord"] = (
        base["road_classification"].map(ROAD_CLASS_ORDINAL).fillna(0).astype("int8")
    )
    base["form_of_way_ord"] = base["form_of_way"].map(FORM_OF_WAY_ORDINAL).fillna(1).astype("int8")
    base["is_motorway"] = (base["road_classification"] == "Motorway").astype("int8")
    base["is_a_road"] = (base["road_classification"] == "A Road").astype("int8")
    base["is_slip_road"] = (base["form_of_way"] == "Slip Road").astype("int8")
    base["is_roundabout"] = (base["form_of_way"] == "Roundabout").astype("int8")
    base["is_dual"] = (
        base["form_of_way"].isin(["Dual Carriageway", "Collapsed Dual Carriageway"]).astype("int8")
    )
    base["is_trunk"] = base["is_trunk"].fillna(False).astype("int8")
    base["is_primary"] = base["is_primary"].fillna(False).astype("int8")

    base["is_covid"] = base["year"].isin(COVID_YEARS).astype("int8")
    year_min, year_max = base["year"].min(), base["year"].max()
    base["year_norm"] = ((base["year"] - year_min) / max(year_max - year_min, 1)).astype("float32")
    base["log_link_length"] = np.log(base["link_length_km"].clip(lower=0.001)).astype("float32")
    return base


def _trim_rla(rla: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in RLA_COLS_FOR_COLLISION if c in rla.columns]
    excluded_post_event = sorted(FORBIDDEN_POST_EVENT_COLS & set(rla.columns))
    if excluded_post_event:
        logger.info(
            "  Excluding post-event diagnostic columns from Stage 2 model dataset: %s",
            ", ".join(excluded_post_event),
        )
    return rla[cols]


def _merge_collision_counts(base: pd.DataFrame, rla: pd.DataFrame) -> pd.DataFrame:
    base = base.merge(_trim_rla(rla), on=["link_id", "year"], how="left")
    for col in [
        "collision_count",
        "fatal_count",
        "serious_count",
        "slight_count",
        "casualty_count",
    ]:
        if col in base.columns:
            base[col] = base[col].fillna(0).astype("int32")
        elif col in {"collision_count", "fatal_count", "serious_count"}:
            base[col] = np.int32(0)
    return base


def _merge_traffic_features(
    base: pd.DataFrame,
    traffic_features: pd.DataFrame | None,
) -> pd.DataFrame:
    if traffic_features is None:
        return base
    traffic = traffic_features[
        [c for c in TRAFFIC_COLS_FOR_COLLISION if c in traffic_features.columns]
    ]
    if "hgv_proportion" not in traffic.columns:
        logger.warning("  traffic_features has no hgv_proportion column — skipping")
        return base
    if traffic.duplicated(["link_id", "year"]).any():
        raise RuntimeError("traffic_features has duplicate link_id/year rows")
    before_rows = len(base)
    base = base.merge(traffic, on=["link_id", "year"], how="left")
    if len(base) != before_rows:
        raise RuntimeError(
            "Traffic feature join changed Stage 2 row count; "
            "traffic_features must be unique by link_id/year"
        )
    return base


def _merge_network_features(
    base: pd.DataFrame,
    net_features: pd.DataFrame | None,
) -> pd.DataFrame:
    if net_features is None:
        return base
    keep_cols = [col for col in NETWORK_FEATURE_COLS_FOR_COLLISION if col in net_features.columns]
    net_trim = net_features[keep_cols]
    before_rows = len(base)
    base = base.merge(net_trim, on="link_id", how="left")
    if len(base) != before_rows:
        raise RuntimeError("Network feature join changed Stage 2 row count")
    return base


def _build_collision_frame_for_keys(
    keys: pd.DataFrame,
    links: pd.DataFrame,
    rla: pd.DataFrame,
    aadt_estimates: pd.DataFrame,
    net_features: pd.DataFrame | None = None,
    traffic_features: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build a modelling frame for an explicit link_id/year key set."""
    base = keys.merge(links, on="link_id", how="left")
    base = _merge_collision_counts(base, rla)
    base = _merge_traffic_features(base, traffic_features)
    base = base.merge(aadt_estimates[AADT_COLS_FOR_COLLISION], on=["link_id", "year"], how="left")
    base = _finalise_collision_features(base)
    base = _merge_network_features(base, net_features)
    return base


def build_collision_dataset(
    openroads,
    aadt_estimates: pd.DataFrame,
    rla: pd.DataFrame,
    net_features: pd.DataFrame | None = None,
    traffic_features: pd.DataFrame | None = None,
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
    base = _merge_collision_counts(base, rla)

    n_with = (base["collision_count"] > 0).sum()
    logger.info(
        f"  Collisions joined: {n_with:,} link-years with ≥1 collision "
        f"({n_with / len(base):.2%} of all link-years)"
    )

    # Join pre-collision traffic features from the all-link × year table.
    # These must not be sourced from road_link_annual, which is collision-
    # aggregate-first and therefore has no rows for zero-collision link-years.
    if traffic_features is not None:
        base = _merge_traffic_features(base, traffic_features)
        if "hgv_proportion" in base.columns:
            n_hgv = base["hgv_proportion"].notna().sum()
            logger.info(
                f"  Traffic features joined: hgv_proportion present on "
                f"{n_hgv:,} / {len(base):,} rows ({n_hgv / len(base):.1%})"
            )
    elif TRAFFIC_FEATURES_PATH.exists():
        traffic = pd.read_parquet(TRAFFIC_FEATURES_PATH, columns=TRAFFIC_COLS_FOR_COLLISION)
        base = _merge_traffic_features(base, traffic)
        if "hgv_proportion" in base.columns:
            n_hgv = base["hgv_proportion"].notna().sum()
            logger.info(
                f"  Traffic features joined: hgv_proportion present on "
                f"{n_hgv:,} / {len(base):,} rows ({n_hgv / len(base):.1%})"
            )
    else:
        logger.warning(
            "  road_traffic_features.parquet not found — hgv_proportion unavailable. "
            "Run road_risk.clean_join.join to persist all-link traffic features."
        )

    # Join AADT — every link should have an estimate after Stage 1a
    base = base.merge(aadt_estimates[AADT_COLS_FOR_COLLISION], on=["link_id", "year"], how="left")
    base = _finalise_collision_features(base)

    if net_features is not None:
        base = _merge_network_features(base, net_features)
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


def _sample_training_link_year_keys(
    links: pd.DataFrame,
    years: list[int],
    rla: pd.DataFrame,
    zero_ratio: int,
    *,
    label: str,
) -> pd.DataFrame:
    """Keep all positive link-years and sample zero link-years for training."""
    positives = (
        rla.loc[rla["collision_count"].gt(0), ["link_id", "year"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    positives["link_id"] = positives["link_id"].astype(str)
    positives["year"] = positives["year"].astype("int16")

    n_total = len(links) * len(years)
    n_zero_available = n_total - len(positives)
    n_zero_keep = min(n_zero_available, len(positives) * zero_ratio)

    logger.info(
        "%s zero policy: sampled | total link-years=%s positives=%s "
        "zeros_available=%s zeros_sampled=%s sample_ratio=1:%s",
        label,
        f"{n_total:,}",
        f"{len(positives):,}",
        f"{n_zero_available:,}",
        f"{n_zero_keep:,}",
        zero_ratio,
    )

    rng = np.random.default_rng(RANDOM_STATE)
    link_values = links["link_id"].astype(str).to_numpy()
    years_arr = np.asarray(years, dtype="int16")
    positive_index = pd.MultiIndex.from_frame(positives)

    zero_frames = []
    n_collected = 0
    while n_collected < n_zero_keep:
        batch_size = min(max((n_zero_keep - n_collected) * 2, 250_000), 2_000_000)
        candidates = pd.DataFrame(
            {
                "link_id": rng.choice(link_values, size=batch_size, replace=True),
                "year": rng.choice(years_arr, size=batch_size, replace=True),
            }
        ).drop_duplicates()
        candidate_index = pd.MultiIndex.from_frame(candidates)
        candidates = candidates.loc[~candidate_index.isin(positive_index)]
        if zero_frames:
            previous = pd.MultiIndex.from_frame(pd.concat(zero_frames, ignore_index=True))
            candidates = candidates.loc[~pd.MultiIndex.from_frame(candidates).isin(previous)]
        take = min(len(candidates), n_zero_keep - n_collected)
        if take:
            zero_frames.append(candidates.iloc[:take].copy())
            n_collected += take

    zeros = pd.concat(zero_frames, ignore_index=True) if zero_frames else positives.iloc[:0].copy()
    keys = pd.concat([positives, zeros], ignore_index=True)
    keys["year"] = keys["year"].astype(int)
    logger.info("  %s training key sample: %s rows", label, f"{len(keys):,}")
    return keys


def _full_training_link_year_keys(
    links: pd.DataFrame,
    years: list[int],
    rla: pd.DataFrame,
    *,
    label: str,
) -> pd.DataFrame:
    """Return the full link_id × year key set for training."""
    positives = int(rla["collision_count"].gt(0).sum())
    n_total = len(links) * len(years)
    n_zero = n_total - positives
    logger.info(
        "%s zero policy: full | total link-years=%s positives=%s zeros=%s XGBoost training rows=%s",
        label,
        f"{n_total:,}",
        f"{positives:,}",
        f"{n_zero:,}",
        f"{n_total:,}",
    )
    return pd.DataFrame(
        {
            "link_id": np.repeat(links["link_id"].values, len(years)),
            "year": np.tile(years, len(links)),
        }
    )


def _read_link_year_rows_for_keys(
    path,
    keys: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Read a link-year parquet table year-by-year and retain explicit keys."""
    frames = []
    for year in sorted(int(y) for y in keys["year"].dropna().unique()):
        keys_yr = keys.loc[keys["year"].eq(year), ["link_id", "year"]].copy()
        rows_yr = pd.read_parquet(path, columns=columns, filters=[("year", "=", year)])
        try:
            keys_yr["link_id"] = keys_yr["link_id"].astype(rows_yr["link_id"].dtype)
        except (TypeError, ValueError):
            logger.warning("Could not cast sampled keys to %s link_id dtype for %s", path, year)
        matched = keys_yr.merge(rows_yr, on=["link_id", "year"], how="left")
        if len(matched) != len(keys_yr):
            raise RuntimeError(
                f"Filtered read from {path} changed row count for {year}: "
                f"{len(keys_yr):,} -> {len(matched):,}"
            )
        frames.append(matched)
        del keys_yr, rows_yr, matched
    return pd.concat(frames, ignore_index=True)


def build_collision_training_dataset(
    links: pd.DataFrame,
    years: list[int],
    rla: pd.DataFrame,
    net_features: pd.DataFrame | None,
    *,
    zero_policy: str,
    zero_ratio: int | None = None,
    label: str,
) -> pd.DataFrame:
    """Build a Stage 2 training dataset with explicit zero handling."""
    if zero_policy not in XGB_ZERO_POLICIES:
        raise ValueError(
            f"Unknown zero_policy {zero_policy!r}; expected {sorted(XGB_ZERO_POLICIES)}"
        )
    if zero_policy == "full":
        keys = _full_training_link_year_keys(links, years, rla, label=label)
    else:
        if zero_ratio is None:
            raise ValueError("zero_ratio is required for sampled zero policy")
        keys = _sample_training_link_year_keys(
            links,
            years,
            rla,
            zero_ratio=zero_ratio,
            label=label,
        )
    aadt = _read_link_year_rows_for_keys(AADT_PATH, keys, AADT_COLS_FOR_COLLISION)
    traffic = (
        _read_link_year_rows_for_keys(TRAFFIC_FEATURES_PATH, keys, TRAFFIC_COLS_FOR_COLLISION)
        if TRAFFIC_FEATURES_PATH.exists()
        else None
    )
    train_df = _build_collision_frame_for_keys(
        keys,
        links,
        rla,
        aadt,
        net_features=net_features,
        traffic_features=traffic,
    )
    logger.info(
        "  %s training collision dataset: %s rows | positives=%s zeros=%s | zero_policy=%s%s",
        label,
        f"{len(train_df):,}",
        f"{int(train_df['collision_count'].gt(0).sum()):,}",
        f"{int(train_df['collision_count'].eq(0).sum()):,}",
        zero_policy,
        "" if zero_policy == "full" else f" ratio=1:{zero_ratio}",
    )
    return train_df


def train_collision_glm(df: pd.DataFrame, maxiter: int = 100) -> tuple:
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
    network_candidates = OPTIONAL_MODEL_FEATURE_COLS
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
    ).fit(maxiter=maxiter)

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
    try:
        result.remove_data()
        logger.info("  Removed stored GLM training data before scoring/saving")
    except Exception as e:
        logger.warning("  Could not remove stored GLM training data: %s", e)

    return result, feature_cols, summary


def train_collision_xgb(
    df: pd.DataFrame,
    seed: int = RANDOM_STATE,
    memory_efficient: bool = False,
) -> tuple:
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
    for col in OPTIONAL_MODEL_FEATURE_COLS:
        if col in df.columns:
            feature_cols.append(col)
    _assert_no_post_event_features(feature_cols, context="XGBoost")

    logger.info(f"  XGBoost training rows: {len(df):,}")

    gc.collect()
    groups = df["link_id"].to_numpy(copy=True)
    y = df["collision_count"].to_numpy(dtype=np.float32, copy=True)
    offsets = df["log_offset"].fillna(0).to_numpy(dtype=np.float32, copy=True)
    X = df[feature_cols].to_numpy(dtype=np.float32, copy=True)
    np.nan_to_num(X, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
    logger.info(
        "  XGBoost matrix: shape=%s dtype=%s | y dtype=%s | base_margin dtype=%s | features=%s",
        X.shape,
        X.dtype,
        y.dtype,
        offsets.dtype,
        len(feature_cols),
    )

    # The caller does not need the wide training dataframe after this point.
    # Dropping feature columns before train/test slicing reduces peak RSS for
    # the full-zero fit attempt.
    df.drop(columns=[c for c in feature_cols if c in df.columns], inplace=True, errors="ignore")
    gc.collect()

    # XGBoost Poisson with exposure offset via base_margin.
    # base_margin sets the initial prediction in log-space so the model
    # learns collision rate conditional on exposure (vehicle-km), matching
    # the GLM formulation. Without this, XGBoost learns absolute counts
    # and systematically overestimates risk on high-traffic links.
    model_params = {
        "objective": "count:poisson",
        "n_estimators": 500,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": seed,
        "n_jobs": 1,
        "verbosity": 0,  # pin for cross-machine reproducibility
    }
    if memory_efficient:
        model_params.update({"tree_method": "hist", "max_bin": 128})
        logger.info("  XGBoost memory mode: tree_method=hist max_bin=128")
    model = XGBRegressor(**model_params)

    # GroupShuffleSplit by link_id: all years for a given link stay in one
    # fold, preventing the same link appearing in both train and test.
    # A random row split is optimistic because repeated-year rows for the
    # same link leak network structure across the split boundary.
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    idx_train, idx_test = next(gss.split(X, y, groups=groups))
    X_train, X_test = X[idx_train], X[idx_test]
    y_train, y_test = y[idx_train], y[idx_test]
    off_train, off_test = offsets[idx_train], offsets[idx_test]
    del X, groups, offsets, idx_train, idx_test
    gc.collect()

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
        "memory_efficient": bool(memory_efficient),
        "tree_method": model_params.get("tree_method"),
        "max_bin": model_params.get("max_bin"),
    }

    logger.info(f"  XGBoost Poisson: pseudo-R²={pseudo_r2:.3f} | test deviance={deviance:,.0f}")
    logger.info(f"  Feature importance (top 10):\n{importance.head(10).to_string()}")

    return model, feature_cols, metrics


def _build_glm_design(
    chunk: pd.DataFrame,
    glm_features: list[str],
    glm_result,
) -> pd.DataFrame:
    imputed_features = getattr(glm_result, "_road_risk_imputed_features", {})
    missing_features = getattr(glm_result, "_road_risk_missing_features", {})
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


def score_collision_models(
    glm_result,
    xgb_model,
    glm_features: list,
    xgb_features: list,
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply both models to full dataset and pool across years.

    Mutates ``df`` in place by adding/replacing ``predicted_glm`` and
    ``predicted_xgb`` link-year columns before pooling. This avoids a full-frame
    copy during national-scale scoring; callers that need the input frame
    without prediction columns should pass a copy.

    Pooling logic:
    - collision_count : sum across years (total observed)
    - estimated_aadt  : mean across years
    - predicted_glm   : mean across years (expected rate at mean traffic)
    - residual_glm    : total_collisions - total_predicted (pooled excess)
    - risk_percentile : rank of mean predicted_xgb across all links (single stable rank)

    One row per link_id — no year dimension in the output.
    """
    logger.info("Applying models and pooling across years ...")

    # Avoid a full-frame defensive copy here: at national scale this can double
    # scoring memory. The caller's df is intentionally annotated with temporary
    # prediction columns before pooling. Repeated callers overwrite these two
    # columns on each run; training feature lists are explicit, so they are never
    # model inputs.
    predicted_glm = np.empty(len(df), dtype="float32")
    predicted_xgb = np.empty(len(df), dtype="float32")

    for start in range(0, len(df), SCORE_CHUNK_ROWS):
        end = min(start + SCORE_CHUNK_ROWS, len(df))
        chunk = df.iloc[start:end]
        X_glm = _build_glm_design(chunk, glm_features, glm_result)
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
    # The GLM was trained on downsampled zeros, which biases
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


def score_collision_models_streamed(
    glm_result,
    xgb_model,
    glm_features: list,
    xgb_features: list,
    links: pd.DataFrame,
    years: list[int],
    rla: pd.DataFrame,
    net_features: pd.DataFrame | None,
) -> pd.DataFrame:
    """Score all links year-by-year and pool without holding all link-years."""
    logger.info("Applying models year-by-year and pooling across years ...")
    n_links = len(links)
    n_years = len(years)

    collision_sum = np.zeros(n_links, dtype="int32")
    fatal_sum = np.zeros(n_links, dtype="int32")
    serious_sum = np.zeros(n_links, dtype="int32")
    aadt_sum = np.zeros(n_links, dtype="float64")
    glm_sum = np.zeros(n_links, dtype="float64")
    xgb_sum = np.zeros(n_links, dtype="float64")
    hgv_first = np.full(n_links, np.nan, dtype="float32")

    for year in years:
        logger.info("  Scoring year %s", year)
        keys = pd.DataFrame({"link_id": links["link_id"].values, "year": year})
        aadt = pd.read_parquet(
            AADT_PATH, columns=AADT_COLS_FOR_COLLISION, filters=[("year", "=", year)]
        )
        traffic = (
            pd.read_parquet(
                TRAFFIC_FEATURES_PATH,
                columns=TRAFFIC_COLS_FOR_COLLISION,
                filters=[("year", "=", year)],
            )
            if TRAFFIC_FEATURES_PATH.exists()
            else None
        )
        rla_year = rla.loc[rla["year"].eq(year), RLA_COLS_FOR_COLLISION]
        year_df = _build_collision_frame_for_keys(
            keys,
            links,
            rla_year,
            aadt,
            net_features=net_features,
            traffic_features=traffic,
        )

        predicted_glm = np.empty(len(year_df), dtype="float32")
        predicted_xgb = np.empty(len(year_df), dtype="float32")
        for start in range(0, len(year_df), SCORE_CHUNK_ROWS):
            end = min(start + SCORE_CHUNK_ROWS, len(year_df))
            chunk = year_df.iloc[start:end]
            X_glm = _build_glm_design(chunk, glm_features, glm_result)
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

        collision_sum += year_df["collision_count"].to_numpy(dtype="int32", copy=False)
        fatal_sum += year_df["fatal_count"].to_numpy(dtype="int32", copy=False)
        serious_sum += year_df["serious_count"].to_numpy(dtype="int32", copy=False)
        aadt_sum += year_df["estimated_aadt"].to_numpy(dtype="float64", copy=False)
        glm_sum += predicted_glm.astype("float64", copy=False)
        xgb_sum += predicted_xgb.astype("float64", copy=False)
        if "hgv_proportion" in year_df.columns:
            hgv_vals = year_df["hgv_proportion"].to_numpy(dtype="float32", copy=False)
            update = np.isnan(hgv_first) & ~np.isnan(hgv_vals)
            hgv_first[update] = hgv_vals[update]

        logger.info(
            "    %s: positives=%s hgv coverage=%.1f%%",
            year,
            f"{int(year_df['collision_count'].gt(0).sum()):,}",
            100
            * year_df.get("hgv_proportion", pd.Series(index=year_df.index, dtype=float))
            .notna()
            .mean(),
        )
        del keys, aadt, traffic, rla_year, year_df, predicted_glm, predicted_xgb

    pooled = links[["link_id", "road_classification"]].copy()
    pooled["collision_count"] = collision_sum
    pooled["fatal_count"] = fatal_sum
    pooled["serious_count"] = serious_sum
    pooled["estimated_aadt"] = aadt_sum / n_years
    pooled["predicted_glm"] = glm_sum / n_years
    pooled["predicted_xgb"] = xgb_sum / n_years
    pooled["residual_glm"] = pooled["collision_count"] - pooled["predicted_glm"] * n_years
    pooled["risk_percentile"] = pooled["predicted_xgb"].rank(pct=True) * 100
    pooled["hgv_proportion"] = hgv_first

    if net_features is not None:
        attrs = [
            c
            for c in [
                "link_id",
                "speed_limit_mph_effective",
                "speed_limit_mph",
                "betweenness_relative",
            ]
            if c in net_features.columns
        ]
        pooled = pooled.merge(net_features[attrs], on="link_id", how="left")

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
    return pooled[[c for c in save_cols if c in pooled.columns]]


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


def score_streamed_and_save(
    glm_result,
    xgb_model,
    glm_features: list,
    xgb_features: list,
    glm_summary: dict,
    xgb_metrics: dict,
    links: pd.DataFrame,
    years: list[int],
    rla: pd.DataFrame,
    net_features: pd.DataFrame | None,
) -> pd.DataFrame:
    """Stream full-GB scoring, pool to links, and save model artefacts."""
    pooled = score_collision_models_streamed(
        glm_result,
        xgb_model,
        glm_features,
        xgb_features,
        links,
        years,
        rla,
        net_features,
    )

    MODELS.mkdir(parents=True, exist_ok=True)
    glm_result.save(str(MODELS / "collision_glm.pkl"))
    xgb_model.save_model(str(MODELS / "collision_xgb.json"))
    pooled.to_parquet(MODELS / "risk_scores.parquet", index=False)
    logger.info(f"  Saved risk scores: {len(pooled):,} links")

    with open(MODELS / "collision_metrics.json", "w") as f:
        json.dump({"glm": glm_summary, "xgb": xgb_metrics}, f, indent=2)

    return pooled


def _parquet_columns(path) -> set[str]:
    import pyarrow.parquet as pq

    return set(pq.ParquetFile(path).schema_arrow.names)


def _read_parquet_for_links(path, link_ids, columns: list[str] | None = None) -> pd.DataFrame:
    link_ids = list(pd.Index(link_ids).astype(str).unique())
    try:
        return pd.read_parquet(
            path,
            columns=columns,
            filters=[("link_id", "in", link_ids)],
        )
    except Exception as e:
        logger.warning(
            "Filtered parquet read failed for %s (%s); falling back to full column read.",
            path,
            e,
        )
        df = pd.read_parquet(path, columns=columns)
        return df[df["link_id"].astype(str).isin(link_ids)].copy()


def _assert_gb_context_schema(net_path=NET_PATH) -> None:
    columns = _parquet_columns(net_path)
    missing = sorted(set(GB_CONTEXT_REQUIRED_COLS).difference(columns))
    legacy_prefix = "imd"
    retired_present = sorted(
        col
        for col in columns
        if col == f"{legacy_prefix}_decile"
        or (col.startswith(f"{legacy_prefix}_") and col.endswith("_decile"))
    )
    if missing:
        raise RuntimeError(f"network_features.parquet is missing GB context columns: {missing}")
    if retired_present:
        raise RuntimeError(
            "network_features.parquet still contains retired English-only IMD fields: "
            f"{retired_present}"
        )


def _sample_smoke_link_ids(
    positive_links: int = SMOKE_POSITIVE_LINKS,
    links_per_country: int = SMOKE_LINKS_PER_COUNTRY,
    seed: int = RANDOM_STATE,
) -> pd.Index:
    rla = pd.read_parquet(RLA_PATH, columns=["link_id", "collision_count"])
    positive = pd.Index(rla.loc[rla["collision_count"].gt(0), "link_id"].dropna().unique())
    n_positive = min(positive_links, len(positive))
    positive_sample = positive.to_series().sample(n=n_positive, random_state=seed)

    context = pd.read_parquet(NET_PATH, columns=["link_id", "ruc_country"])
    country_samples = []
    for i, country in enumerate(["England", "Wales", "Scotland"], start=1):
        candidates = context.loc[context["ruc_country"].eq(country), "link_id"].dropna()
        n_country = min(links_per_country, len(candidates))
        if n_country == 0:
            raise RuntimeError(f"No {country} links found in ruc_country for smoke sample")
        country_samples.append(candidates.sample(n=n_country, random_state=seed + i))

    link_ids = pd.Index(pd.concat([positive_sample, *country_samples]).astype(str).unique())
    logger.info(
        "Smoke sample link_ids: %s total (%s positive-link seeds + %s per country)",
        f"{len(link_ids):,}",
        f"{n_positive:,}",
        f"{links_per_country:,}",
    )
    return link_ids


def run_collision_smoke(
    positive_links: int = SMOKE_POSITIVE_LINKS,
    links_per_country: int = SMOKE_LINKS_PER_COUNTRY,
) -> dict:
    """
    Cheap Stage 2 schema/plumbing smoke test.

    Loads a small link sample from the real model inputs, asserts the GB context
    columns, builds the normal collision modelling frame for that subset, fits
    the fast GLM baseline, and exits without writing model artefacts.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    logger.info("=== Collision model smoke test ===")
    _assert_gb_context_schema(NET_PATH)

    link_ids = _sample_smoke_link_ids(
        positive_links=positive_links,
        links_per_country=links_per_country,
    )

    openroads_cols = [
        "link_id",
        "road_classification",
        "form_of_way",
        "link_length_km",
        "is_trunk",
        "is_primary",
    ]
    rla_cols = [
        "link_id",
        "year",
        "collision_count",
        "fatal_count",
        "serious_count",
        "slight_count",
        "casualty_count",
    ]
    traffic_cols = ["link_id", "year", "hgv_proportion"]

    openroads = _read_parquet_for_links(OPENROADS_PATH, link_ids, columns=openroads_cols)
    aadt_estimates = _read_parquet_for_links(
        AADT_PATH,
        link_ids,
        columns=["link_id", "year", "estimated_aadt"],
    )
    rla = _read_parquet_for_links(RLA_PATH, link_ids, columns=rla_cols)
    net_features = _read_parquet_for_links(NET_PATH, link_ids)
    context_missingness = net_features[GB_CONTEXT_REQUIRED_COLS].isna().mean().sort_index()
    traffic_features = (
        _read_parquet_for_links(TRAFFIC_FEATURES_PATH, link_ids, columns=traffic_cols)
        if TRAFFIC_FEATURES_PATH.exists()
        else None
    )

    df = build_collision_dataset(
        openroads,
        aadt_estimates,
        rla,
        net_features=net_features,
        traffic_features=traffic_features,
    )

    glm_result, glm_features, glm_summary = train_collision_glm(df, maxiter=200)

    print("\n=== Collision smoke test ===")
    print(f"Rows: {len(df):,}")
    print(f"Links: {df['link_id'].nunique():,}")
    print(f"Years: {sorted(df['year'].unique().tolist())}")
    print(f"Positive link-years: {int(df['collision_count'].gt(0).sum()):,}")
    print("\nGB context missingness:")
    print((context_missingness * 100).round(3).astype(str).add("%").to_string())
    print("\nSelected GLM features:")
    print("\n".join(f"  {col}" for col in glm_features))
    print(
        "\nGLM smoke fit: "
        f"n_obs={glm_summary['n_obs']:,}, "
        f"pseudo_r2={glm_summary['pseudo_r2']:.4f}, "
        f"converged={glm_summary['converged']}"
    )

    return {
        "rows": int(len(df)),
        "links": int(df["link_id"].nunique()),
        "positive_link_years": int(df["collision_count"].gt(0).sum()),
        "glm_features": glm_features,
        "glm_summary": glm_summary,
        "glm_converged": bool(getattr(glm_result, "converged", False)),
    }


def run_collision_stage(
    xgb_zero_policy: str = XGB_ZERO_POLICY,
    xgb_zero_sample_ratio: int = XGB_ZERO_SAMPLE_RATIO,
) -> pd.DataFrame:
    """
    Run Stage 2 end-to-end. Loads all required inputs, trains, scores, saves.
    """
    logger.info("=== Stage 2: Collision model ===")
    if xgb_zero_policy not in XGB_ZERO_POLICIES:
        raise ValueError(
            f"Unknown xgb_zero_policy {xgb_zero_policy!r}; expected {sorted(XGB_ZERO_POLICIES)}"
        )

    openroads = pd.read_parquet(OPENROADS_PATH, columns=OPENROADS_COLS_FOR_COLLISION)
    rla = pd.read_parquet(
        RLA_PATH,
        columns=[c for c in RLA_COLS_FOR_COLLISION if c in _parquet_columns(RLA_PATH)],
    )
    if NET_PATH.exists():
        _assert_gb_context_schema(NET_PATH)
        net_feature_columns = [
            col for col in NETWORK_FEATURE_COLS_FOR_COLLISION if col in _parquet_columns(NET_PATH)
        ]
        net_features = pd.read_parquet(NET_PATH, columns=net_feature_columns)
    else:
        net_features = None
    if net_features is None:
        logger.warning("Network features not found — run network_features.py first")

    if not AADT_PATH.exists():
        raise FileNotFoundError(
            f"AADT estimates not found at {AADT_PATH}. Run --stage traffic first."
        )
    years = sorted(int(y) for y in pd.read_parquet(AADT_PATH, columns=["year"])["year"].unique())

    glm_df = build_collision_training_dataset(
        openroads,
        years,
        rla,
        net_features,
        zero_policy="sampled",
        zero_ratio=GLM_ZERO_SAMPLE_RATIO,
        label="GLM",
    )

    glm_result, glm_features, glm_summary = train_collision_glm(glm_df)
    del glm_df

    xgb_df = build_collision_training_dataset(
        openroads,
        years,
        rla,
        net_features,
        zero_policy=xgb_zero_policy,
        zero_ratio=xgb_zero_sample_ratio if xgb_zero_policy == "sampled" else None,
        label="XGBoost",
    )

    try:
        xgb_model, xgb_features, xgb_metrics = train_collision_xgb(
            xgb_df,
            memory_efficient=(xgb_zero_policy == "full"),
        )
        xgb_metrics["zero_policy"] = xgb_zero_policy
        if xgb_zero_policy == "sampled":
            xgb_metrics["zero_sample_ratio"] = int(xgb_zero_sample_ratio)
    except ImportError:
        logger.warning("XGBoost not installed — skipping. pip install xgboost")
        return None
    finally:
        del xgb_df

    risk_scores = score_streamed_and_save(
        glm_result,
        xgb_model,
        glm_features,
        xgb_features,
        glm_summary,
        xgb_metrics,
        openroads,
        years,
        rla,
        net_features,
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 2 collision model")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run a cheap schema/model-plumbing smoke test instead of a full retrain",
    )
    parser.add_argument(
        "--smoke-positive-links",
        type=int,
        default=SMOKE_POSITIVE_LINKS,
        help=f"Positive-collision links to sample for --smoke (default: {SMOKE_POSITIVE_LINKS})",
    )
    parser.add_argument(
        "--smoke-links-per-country",
        type=int,
        default=SMOKE_LINKS_PER_COUNTRY,
        help=f"Links to sample per RUC country for --smoke (default: {SMOKE_LINKS_PER_COUNTRY})",
    )
    parser.add_argument(
        "--xgb-zero-policy",
        choices=sorted(XGB_ZERO_POLICIES),
        default=XGB_ZERO_POLICY,
        help=(
            "XGBoost zero-collision training population. 'full' preserves the "
            "all link-year design; 'sampled' is an explicit memory fallback."
        ),
    )
    parser.add_argument(
        "--xgb-zero-sample-ratio",
        type=int,
        default=XGB_ZERO_SAMPLE_RATIO,
        help=(
            "Zero-to-positive sample ratio when --xgb-zero-policy sampled is used "
            f"(default: {XGB_ZERO_SAMPLE_RATIO})"
        ),
    )
    args = parser.parse_args()

    if args.smoke:
        run_collision_smoke(
            positive_links=args.smoke_positive_links,
            links_per_country=args.smoke_links_per_country,
        )
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
        run_collision_stage(
            xgb_zero_policy=args.xgb_zero_policy,
            xgb_zero_sample_ratio=args.xgb_zero_sample_ratio,
        )


if __name__ == "__main__":
    main()
