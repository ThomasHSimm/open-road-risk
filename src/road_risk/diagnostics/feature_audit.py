"""
Feature missingness-vs-collision-history audit for the Stage 2 dataset.

The diagnostic looks for the specific structural bug signature that previously
affected HGV percentage: a feature is much more likely to be non-null on links
with historical collisions than on zero-collision links, even within the same
road class.
"""

from __future__ import annotations

import argparse
import logging
import time
from dataclasses import dataclass
from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd
import yaml
from shapely.geometry import box

from road_risk.config import _ROOT
from road_risk.model.collision import (
    AADT_PATH,
    NET_PATH,
    OPENROADS_PATH,
    RLA_PATH,
    build_collision_dataset,
)
from road_risk.model.constants import RANDOM_STATE

logger = logging.getLogger(__name__)

SETTINGS_PATH = _ROOT / "config/settings.yaml"
SUPPORTING_DIR = _ROOT / "reports/supporting"

FULL_RAW_OUT = SUPPORTING_DIR / "feature_audit_full.csv"
FULL_FLAGGED_OUT = SUPPORTING_DIR / "feature_audit_flagged.csv"
REPORT_OUT = SUPPORTING_DIR / "feature_audit.md"
FLAGGED_PLAN_STATUS_OUT = SUPPORTING_DIR / "flagged_feature_plan_status.md"

TRAINING_YEARS = set(range(2015, 2025))
GAP_THRESHOLD = 0.05
ZERO_COVERAGE_THRESHOLD = 0.50
VIEW_DISAGREEMENT_THRESHOLD = 0.10
CONFIGURED_BBOX_MAX_SHARE = 0.30

# A compact 50 km OS grid square centred on the West Yorkshire/Leeds-Bradford
# area. Used only when the configured study-area bbox is too large to be a
# useful development subset.
FALLBACK_BBOX_BNG = {
    "name": "West Yorkshire 50 km BNG square",
    "min_easting": 400_000,
    "min_northing": 400_000,
    "max_easting": 450_000,
    "max_northing": 450_000,
}

BNG_PROJ = (
    "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 "
    "+x_0=400000 +y_0=-100000 +ellps=airy +units=m +no_defs"
)

ROAD_CLASS_ORDER = [
    "Motorway",
    "A Road",
    "B Road",
    "Classified Unnumbered",
    "Unclassified",
    "Not Classified",
    "Unknown",
]

COLLISION_POSITIVE = "one_or_more_collisions_2015_2024"
ZERO_COLLISIONS = "zero_collisions_2015_2024"
COLLISION_STRATA = [COLLISION_POSITIVE, ZERO_COLLISIONS]

TARGET_DERIVED_COLUMNS = {
    "collision_count",
    "fatal_count",
    "serious_count",
    "slight_count",
    "casualty_count",
}
NON_FEATURE_COLUMNS = {
    "link_id",
    "year",
    "road_classification",
}
EXPECTED_SPARSE_OSM_FLAG_FEATURES = {
    "is_unpaved",
    "lanes",
    "lit",
    "speed_limit_mph",
}


@dataclass(frozen=True)
class BBoxSelection:
    name: str
    bounds: dict[str, float]
    configured_n_links: int
    configured_share: float
    selected_n_links: int
    selected_share: float
    used_fallback: bool


@dataclass(frozen=True)
class InputFrames:
    openroads: pd.DataFrame
    aadt_estimates: pd.DataFrame
    rla: pd.DataFrame
    net_features: pd.DataFrame | None


@dataclass(frozen=True)
class FilterCounts:
    scope: str
    bbox_name: str
    bbox_bounds: dict[str, float] | None
    rows: list[dict[str, Any]]


@dataclass(frozen=True)
class AuditResult:
    raw: pd.DataFrame
    gap_table: pd.DataFrame
    flagged: pd.DataFrame
    untestable: pd.DataFrame
    passed: pd.DataFrame
    skipped_global: pd.DataFrame
    skipped_target: pd.DataFrame
    inconsistent_road_class_links: int
    gap_distribution: pd.DataFrame


def _timer() -> float:
    return time.perf_counter()


def _elapsed(start: float) -> float:
    return time.perf_counter() - start


def _format_seconds(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, rem = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes)}m {rem:.1f}s"
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {rem:.1f}s"


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def _load_inputs() -> InputFrames:
    logger.info("Loading Stage 2 inputs")
    openroads = gpd.read_parquet(OPENROADS_PATH)
    aadt_estimates = pd.read_parquet(AADT_PATH)
    rla = pd.read_parquet(RLA_PATH)
    net_features = pd.read_parquet(NET_PATH) if NET_PATH.exists() else None
    return InputFrames(
        openroads=openroads,
        aadt_estimates=aadt_estimates,
        rla=rla,
        net_features=net_features,
    )


def _configured_bbox() -> dict[str, float]:
    cfg = yaml.safe_load(SETTINGS_PATH.read_text())
    bbox = cfg.get("study_area", {}).get("bbox_bng", {})
    required = ["min_easting", "min_northing", "max_easting", "max_northing"]
    missing = [key for key in required if key not in bbox]
    if missing:
        raise ValueError(f"Missing bbox_bng keys in {SETTINGS_PATH}: {missing}")
    return {key: float(bbox[key]) for key in required}


def _bbox_mask(openroads: gpd.GeoDataFrame, bounds: dict[str, float]) -> pd.Series:
    geom = box(
        bounds["min_easting"],
        bounds["min_northing"],
        bounds["max_easting"],
        bounds["max_northing"],
    )
    # In the current env, EPSG:27700 transforms through PROJ return infinities
    # for this GeoParquet, while the equivalent BNG proj string is stable.
    roads_bng = openroads.to_crs(BNG_PROJ)
    return roads_bng.geometry.intersects(geom)


def _select_subset_bbox(openroads: gpd.GeoDataFrame) -> BBoxSelection:
    configured = _configured_bbox()
    configured_mask = _bbox_mask(openroads, configured)
    configured_n = int(configured_mask.sum())
    configured_share = configured_n / len(openroads)

    if configured_share <= CONFIGURED_BBOX_MAX_SHARE:
        selected = configured
        selected_mask = configured_mask
        name = "configured study_area.bbox_bng"
        used_fallback = False
    else:
        selected = {k: float(v) for k, v in FALLBACK_BBOX_BNG.items() if k != "name"}
        selected_mask = _bbox_mask(openroads, selected)
        name = str(FALLBACK_BBOX_BNG["name"])
        used_fallback = True

    selected_n = int(selected_mask.sum())
    if selected_n == 0:
        raise ValueError(f"Subset bbox {name!r} selected zero OpenRoads links")

    logger.info(
        "Configured bbox: %s links (%.1f%%); selected %s: %s links (%.1f%%)",
        f"{configured_n:,}",
        configured_share * 100,
        name,
        f"{selected_n:,}",
        selected_n / len(openroads) * 100,
    )
    return BBoxSelection(
        name=name,
        bounds=selected,
        configured_n_links=configured_n,
        configured_share=configured_share,
        selected_n_links=selected_n,
        selected_share=selected_n / len(openroads),
        used_fallback=used_fallback,
    )


def _row_counts(name: str, df: pd.DataFrame | None) -> tuple[int, int]:
    if df is None:
        return 0, 0
    n_links = int(df["link_id"].nunique()) if "link_id" in df.columns else 0
    return int(len(df)), n_links


def _filter_inputs_to_link_ids(
    frames: InputFrames,
    link_ids: set[Any],
    *,
    scope: str,
    bbox_name: str,
    bbox_bounds: dict[str, float] | None,
) -> tuple[InputFrames, FilterCounts]:
    link_index = pd.Index(link_ids)

    def filt(df: pd.DataFrame | None) -> pd.DataFrame | None:
        if df is None:
            return None
        return df[df["link_id"].isin(link_index)].copy()

    rows: list[dict[str, Any]] = []
    filtered_openroads = filt(frames.openroads)
    filtered_aadt = filt(frames.aadt_estimates)
    filtered_rla = filt(frames.rla)
    filtered_net = filt(frames.net_features)

    for label, before, after in [
        ("openroads", frames.openroads, filtered_openroads),
        ("aadt_estimates", frames.aadt_estimates, filtered_aadt),
        ("road_link_annual", frames.rla, filtered_rla),
        ("net_features", frames.net_features, filtered_net),
    ]:
        before_rows, before_links = _row_counts(label, before)
        after_rows, after_links = _row_counts(label, after)
        rows.append(
            {
                "frame": label,
                "rows_before": before_rows,
                "links_before": before_links,
                "rows_after": after_rows,
                "links_after": after_links,
            }
        )

    return (
        InputFrames(
            openroads=filtered_openroads,
            aadt_estimates=filtered_aadt,
            rla=filtered_rla,
            net_features=filtered_net,
        ),
        FilterCounts(scope=scope, bbox_name=bbox_name, bbox_bounds=bbox_bounds, rows=rows),
    )


def _subset_inputs(frames: InputFrames) -> tuple[InputFrames, BBoxSelection, FilterCounts]:
    if not isinstance(frames.openroads, gpd.GeoDataFrame):
        raise TypeError("openroads must be a GeoDataFrame for bbox filtering")
    selection = _select_subset_bbox(frames.openroads)
    selected_mask = _bbox_mask(frames.openroads, selection.bounds)
    link_ids = set(frames.openroads.loc[selected_mask, "link_id"])
    subset, counts = _filter_inputs_to_link_ids(
        frames,
        link_ids,
        scope="subset",
        bbox_name=selection.name,
        bbox_bounds=selection.bounds,
    )
    return subset, selection, counts


def _full_counts(frames: InputFrames) -> FilterCounts:
    rows = []
    for label, df in [
        ("openroads", frames.openroads),
        ("aadt_estimates", frames.aadt_estimates),
        ("road_link_annual", frames.rla),
        ("net_features", frames.net_features),
    ]:
        n_rows, n_links = _row_counts(label, df)
        rows.append(
            {
                "frame": label,
                "rows_before": n_rows,
                "links_before": n_links,
                "rows_after": n_rows,
                "links_after": n_links,
            }
        )
    return FilterCounts(scope="full", bbox_name="unfiltered", bbox_bounds=None, rows=rows)


def _build_dataset(frames: InputFrames, *, label: str) -> tuple[pd.DataFrame, float]:
    start = _timer()
    logger.info("Building %s collision dataset", label)
    df = build_collision_dataset(
        frames.openroads,
        frames.aadt_estimates,
        frames.rla,
        frames.net_features,
    )
    seconds = _elapsed(start)
    logger.info("%s collision dataset built: %s rows in %s", label, f"{len(df):,}", seconds)
    return df, seconds


def _collision_history(df: pd.DataFrame) -> pd.DataFrame:
    training = df[df["year"].isin(TRAINING_YEARS)]
    collisions_by_link = training.groupby("link_id", observed=True)["collision_count"].sum()
    out = pd.DataFrame(
        {
            "link_id": collisions_by_link.index,
            "collision_stratum": np.where(
                collisions_by_link.to_numpy() >= 1,
                COLLISION_POSITIVE,
                ZERO_COLLISIONS,
            ),
        }
    )
    return out


def _link_metadata(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    class_nunique = df.groupby("link_id", observed=True)["road_classification"].nunique(
        dropna=False
    )
    inconsistent = int((class_nunique > 1).sum())
    road_class = (
        df[["link_id", "road_classification"]]
        .drop_duplicates("link_id", keep="first")
        .reset_index(drop=True)
    )
    return road_class.merge(_collision_history(df), on="link_id", how="left"), inconsistent


def _is_target_derived(col: str) -> bool:
    if col in TARGET_DERIVED_COLUMNS:
        return True
    return "collision" in col.lower()


def _candidate_features(df: pd.DataFrame) -> tuple[list[str], pd.DataFrame, pd.DataFrame]:
    skipped_target = []
    skipped_global = []
    candidates = []

    for col in df.columns:
        if col in NON_FEATURE_COLUMNS or _is_target_derived(col):
            if col not in NON_FEATURE_COLUMNS:
                skipped_target.append({"feature": col, "reason": "target_or_collision_derived"})
            continue
        share = float(df[col].notna().mean())
        if share <= 0.0 or share >= 1.0:
            skipped_global.append({"feature": col, "global_non_null_share": share})
            continue
        candidates.append(col)

    return candidates, pd.DataFrame(skipped_global), pd.DataFrame(skipped_target)


def _audit_feature(
    df: pd.DataFrame,
    link_meta: pd.DataFrame,
    row_stratum: pd.Series,
    feature: str,
) -> pd.DataFrame:
    non_null = df[feature].notna()
    link_non_null = non_null.groupby(df["link_id"], observed=True).any()
    link_tmp = link_meta.copy()
    link_tmp["is_non_null"] = link_tmp["link_id"].map(link_non_null).fillna(False)

    link_stats = (
        link_tmp.groupby(["road_classification", "collision_stratum"], observed=True)
        .agg(n_links=("link_id", "size"), n_non_null=("is_non_null", "sum"))
        .reset_index()
        .rename(columns={"road_classification": "road_class"})
    )
    link_stats["non_null_share_per_link"] = link_stats["n_non_null"] / link_stats["n_links"]

    ly_stats = (
        non_null.groupby([df["road_classification"], row_stratum], observed=True)
        .agg(["sum", "size"])
        .reset_index()
        .rename(
            columns={
                "road_classification": "road_class",
                "collision_stratum": "collision_stratum",
                "sum": "n_non_null_link_years",
                "size": "n_link_years",
            }
        )
    )
    ly_stats["non_null_share_per_link_year"] = (
        ly_stats["n_non_null_link_years"] / ly_stats["n_link_years"]
    )

    out = link_stats.merge(
        ly_stats[
            [
                "road_class",
                "collision_stratum",
                "non_null_share_per_link_year",
                "n_link_years",
            ]
        ],
        on=["road_class", "collision_stratum"],
        how="left",
    )
    out.insert(0, "feature", feature)
    return out[
        [
            "feature",
            "road_class",
            "collision_stratum",
            "n_links",
            "n_non_null",
            "non_null_share_per_link",
            "non_null_share_per_link_year",
            "n_link_years",
        ]
    ]


def _gap_distribution(gap_table: pd.DataFrame) -> pd.DataFrame:
    gap = gap_table["gap"].dropna()
    if gap.empty:
        return pd.DataFrame(columns=["metric", "value"])
    quantiles = gap.quantile([0.0, 0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 1.0])
    rows = [
        {"metric": "n_feature_road_class_pairs", "value": int(gap.count())},
        {"metric": "mean_gap", "value": float(gap.mean())},
        {"metric": "std_gap", "value": float(gap.std(ddof=0))},
    ]
    rows.extend(
        {"metric": f"q{int(q * 100):02d}_gap", "value": float(v)} for q, v in quantiles.items()
    )
    return pd.DataFrame(rows)


def _build_gap_table(raw: pd.DataFrame) -> pd.DataFrame:
    pivot = raw.pivot_table(
        index=["feature", "road_class"],
        columns="collision_stratum",
        values=[
            "n_links",
            "non_null_share_per_link",
            "non_null_share_per_link_year",
        ],
        aggfunc="first",
    )
    rows: list[dict[str, Any]] = []
    for (feature, road_class), values in pivot.iterrows():
        try:
            pos_share = float(values[("non_null_share_per_link", COLLISION_POSITIVE)])
            zero_share = float(values[("non_null_share_per_link", ZERO_COLLISIONS)])
            pos_ly_share = float(values[("non_null_share_per_link_year", COLLISION_POSITIVE)])
            zero_ly_share = float(values[("non_null_share_per_link_year", ZERO_COLLISIONS)])
            pos_links = int(values[("n_links", COLLISION_POSITIVE)])
            zero_links = int(values[("n_links", ZERO_COLLISIONS)])
        except KeyError:
            rows.append(
                {
                    "feature": feature,
                    "road_class": road_class,
                    "status": "untestable",
                    "untestable_reason": "missing_collision_stratum",
                }
            )
            continue

        gap = pos_share - zero_share
        link_year_gap = pos_ly_share - zero_ly_share
        view_gap_diff = abs(gap - link_year_gap)
        degenerate = pos_share == zero_share and pos_share in {0.0, 1.0}
        rows.append(
            {
                "feature": feature,
                "road_class": road_class,
                "positive_n_links": pos_links,
                "zero_n_links": zero_links,
                "positive_non_null_share": pos_share,
                "zero_non_null_share": zero_share,
                "gap": gap,
                "positive_link_year_non_null_share": pos_ly_share,
                "zero_link_year_non_null_share": zero_ly_share,
                "link_year_gap": link_year_gap,
                "link_vs_link_year_gap_abs_diff": view_gap_diff,
                "status": "untestable" if degenerate else "auditable",
                "untestable_reason": "within_class_all_0_or_all_100" if degenerate else "",
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    class_rank = {value: i for i, value in enumerate(ROAD_CLASS_ORDER)}
    out["_class_rank"] = out["road_class"].map(class_rank).fillna(len(class_rank))
    out = out.sort_values(["feature", "_class_rank", "road_class"]).drop(columns="_class_rank")
    return out.reset_index(drop=True)


def _apply_flags(gap_table: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if gap_table.empty:
        empty = pd.DataFrame()
        return empty, empty, empty

    auditable = gap_table[gap_table["status"] == "auditable"].copy()
    missingness_bug = (auditable["gap"] > GAP_THRESHOLD) & (
        auditable["zero_non_null_share"] < ZERO_COVERAGE_THRESHOLD
    )
    view_disagreement = auditable["link_vs_link_year_gap_abs_diff"] > VIEW_DISAGREEMENT_THRESHOLD
    flagged = auditable[missingness_bug | view_disagreement].copy()
    flagged["flag_reason"] = np.select(
        [missingness_bug.loc[flagged.index], view_disagreement.loc[flagged.index]],
        [
            "coverage_gap_and_low_zero_collision_coverage",
            "per_link_vs_link_year_disagreement",
        ],
        default="",
    )
    flagged = flagged.sort_values(["gap", "link_vs_link_year_gap_abs_diff"], ascending=False)

    untestable = gap_table[gap_table["status"] == "untestable"].copy()
    passed = auditable.drop(index=flagged.index).copy()
    return (
        flagged.reset_index(drop=True),
        untestable.reset_index(drop=True),
        passed.reset_index(drop=True),
    )


def run_audit(df: pd.DataFrame) -> AuditResult:
    link_meta, inconsistent = _link_metadata(df)
    row_stratum = df["link_id"].map(link_meta.set_index("link_id")["collision_stratum"])
    row_stratum.name = "collision_stratum"

    candidates, skipped_global, skipped_target = _candidate_features(df)
    logger.info(
        "Auditing %s candidate features (%s globally degenerate, %s target-derived skipped)",
        len(candidates),
        len(skipped_global),
        len(skipped_target),
    )

    raw_parts = []
    for feature in candidates:
        raw_parts.append(_audit_feature(df, link_meta, row_stratum, feature))

    raw = pd.concat(raw_parts, ignore_index=True) if raw_parts else pd.DataFrame()
    gap_table = _build_gap_table(raw) if not raw.empty else pd.DataFrame()
    gap_distribution = _gap_distribution(gap_table[gap_table["status"] == "auditable"])

    print("\nGap distribution before applying flags:")
    print(gap_distribution.to_string(index=False))
    print(
        "\nCommitted thresholds before flagged-feature inspection: "
        f"gap > {GAP_THRESHOLD:.0%}, zero-collision coverage < "
        f"{ZERO_COVERAGE_THRESHOLD:.0%}, view disagreement > "
        f"{VIEW_DISAGREEMENT_THRESHOLD:.0%}."
    )

    flagged, untestable, passed = _apply_flags(gap_table)
    return AuditResult(
        raw=raw,
        gap_table=gap_table,
        flagged=flagged,
        untestable=untestable,
        passed=passed,
        skipped_global=skipped_global,
        skipped_target=skipped_target,
        inconsistent_road_class_links=inconsistent,
        gap_distribution=gap_distribution,
    )


def _choose_self_test_class(df: pd.DataFrame) -> str:
    link_meta, _ = _link_metadata(df)
    counts = (
        link_meta.groupby(["road_classification", "collision_stratum"], observed=True)
        .size()
        .unstack(fill_value=0)
    )
    counts = counts[
        (counts.get(COLLISION_POSITIVE, 0) >= 5) & (counts.get(ZERO_COLLISIONS, 0) >= 20)
    ].copy()
    if counts.empty:
        raise AssertionError(
            "No road class has enough links in both collision strata for self-test"
        )
    counts["total"] = counts.sum(axis=1)
    return str(counts.sort_values("total", ascending=False).index[0])


def _set_feature_null_for_links(df: pd.DataFrame, feature: str, link_ids: set[Any]) -> pd.DataFrame:
    out = df.copy()
    out.loc[out["link_id"].isin(link_ids), feature] = np.nan
    return out


def run_self_test(df: pd.DataFrame) -> pd.DataFrame:
    feature = "estimated_aadt" if "estimated_aadt" in df.columns else _candidate_features(df)[0][0]
    road_class = _choose_self_test_class(df)
    rng = np.random.default_rng(RANDOM_STATE)

    link_meta, _ = _link_metadata(df)
    target_zero = link_meta[
        (link_meta["road_classification"] == road_class)
        & (link_meta["collision_stratum"] == ZERO_COLLISIONS)
    ]["link_id"].to_numpy()
    target_pos = link_meta[
        (link_meta["road_classification"] == road_class)
        & (link_meta["collision_stratum"] == COLLISION_POSITIVE)
    ]["link_id"].to_numpy()

    positive_n = min(len(target_zero), max(1, len(target_zero) // 2 + 1))
    positive_null_links = set(rng.choice(target_zero, size=positive_n, replace=False))
    positive_df = _set_feature_null_for_links(df, feature, positive_null_links)
    positive_result = run_audit(positive_df)
    positive_hit = positive_result.flagged[
        (positive_result.flagged["feature"] == feature)
        & (positive_result.flagged["road_class"] == road_class)
        & (positive_result.flagged["flag_reason"] == "coverage_gap_and_low_zero_collision_coverage")
    ]
    if positive_hit.empty:
        raise AssertionError(
            f"Positive self-test failed: {feature} was not flagged for {road_class}"
        )

    negative_null_links: set[Any] = set()
    for links in [target_zero, target_pos]:
        negative_null_links.update(
            rng.choice(links, size=max(1, int(round(len(links) * 0.30))), replace=False)
        )
    negative_df = _set_feature_null_for_links(df, feature, negative_null_links)
    negative_result = run_audit(negative_df)
    negative_hit = negative_result.flagged[
        (negative_result.flagged["feature"] == feature)
        & (negative_result.flagged["road_class"] == road_class)
    ]
    if not negative_hit.empty:
        raise AssertionError(
            f"Negative self-test failed: {feature} was incorrectly flagged for {road_class}"
        )

    return pd.DataFrame(
        [
            {
                "case": "positive_structural_missingness",
                "feature": feature,
                "road_class": road_class,
                "n_zero_links_corrupted": len(positive_null_links),
                "passed": True,
            },
            {
                "case": "negative_uniform_missingness",
                "feature": feature,
                "road_class": road_class,
                "n_links_corrupted": len(negative_null_links),
                "passed": True,
            },
        ]
    )


def _write_full_outputs(result: AuditResult) -> None:
    SUPPORTING_DIR.mkdir(parents=True, exist_ok=True)
    result.raw.to_csv(FULL_RAW_OUT, index=False)
    result.flagged.to_csv(FULL_FLAGGED_OUT, index=False)
    logger.info("Wrote %s", FULL_RAW_OUT)
    logger.info("Wrote %s", FULL_FLAGGED_OUT)


def _counts_table(counts: FilterCounts) -> str:
    rows = []
    for row in counts.rows:
        rows.append(
            [
                row["frame"],
                f"{row['rows_before']:,}",
                f"{row['links_before']:,}",
                f"{row['rows_after']:,}",
                f"{row['links_after']:,}",
            ]
        )
    return _markdown_table(
        ["frame", "rows before", "links before", "rows after", "links after"],
        rows,
    )


def _gap_distribution_table(gap_distribution: pd.DataFrame) -> str:
    rows = []
    for row in gap_distribution.itertuples(index=False):
        value = row.value
        if isinstance(value, (float, np.floating)):
            formatted = f"{value:.6f}"
        else:
            formatted = str(value)
        rows.append([row.metric, formatted])
    return _markdown_table(["metric", "value"], rows)


def _feature_pattern_table(df: pd.DataFrame, limit: int = 30) -> str:
    if df.empty:
        return "No rows."
    rows = []
    for row in df.head(limit).itertuples(index=False):
        mapping = row._asdict()
        rows.append(
            [
                mapping["feature"],
                mapping["road_class"],
                f"{mapping['positive_non_null_share']:.1%}",
                f"{mapping['zero_non_null_share']:.1%}",
                f"{mapping['gap']:.1%}",
                f"{mapping['link_year_gap']:.1%}",
                mapping.get("flag_reason", ""),
            ]
        )
    table = _markdown_table(
        ["feature", "road_class", "positive", "zero", "gap", "link-year gap", "reason"],
        rows,
    )
    if len(df) > limit:
        table += f"\n\nShowing first {limit:,} of {len(df):,} rows."
    return table


def _expected_flags_baseline(full_result: AuditResult) -> str:
    if full_result.flagged.empty:
        flagged_features: set[str] = set()
    else:
        flagged_features = set(full_result.flagged["feature"])

    expected_present = sorted(flagged_features & EXPECTED_SPARSE_OSM_FLAG_FEATURES)
    unexpected = sorted(flagged_features - EXPECTED_SPARSE_OSM_FLAG_FEATURES)
    missing_expected = sorted(EXPECTED_SPARSE_OSM_FLAG_FEATURES - flagged_features)
    expected_pair_count = (
        int(full_result.flagged["feature"].isin(EXPECTED_SPARSE_OSM_FLAG_FEATURES).sum())
        if not full_result.flagged.empty
        else 0
    )

    rows = [
        ["Expected sparse-OSM/provenance features present", ", ".join(expected_present) or "None"],
        ["Expected sparse-OSM/provenance feature-road-class pairs", expected_pair_count],
        [
            "Expected baseline features not flagged in this run",
            ", ".join(missing_expected) or "None",
        ],
        ["Unexpected flagged feature names", ", ".join(unexpected) or "None"],
    ]

    return "\n".join(
        [
            "The current expected baseline is that flags on `is_unpaved`, `lanes`, "
            "`lit`, and raw `speed_limit_mph` are known sparse-OSM/provenance "
            "patterns rather than HGV-style source-table bugs.",
            "",
            _markdown_table(["check", "value"], rows),
            "",
            f"Details are in `{FLAGGED_PLAN_STATUS_OUT.relative_to(_ROOT)}`. "
            "A future rerun that reproduces only these feature names can be "
            "triaged quickly against that note. A future rerun that flags any "
            "additional feature name should be investigated as a new candidate "
            "missingness-vs-collision-history issue.",
        ]
    )


def _status_summary_table(result: AuditResult) -> str:
    summary = (
        result.gap_table.groupby(["feature", "status"], observed=True)
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    flagged_features = set(result.flagged["feature"]) if not result.flagged.empty else set()
    summary["flagged_pairs"] = (
        summary["feature"]
        .map(result.flagged["feature"].value_counts().to_dict() if not result.flagged.empty else {})
        .fillna(0)
        .astype(int)
    )
    passed = summary[summary["flagged_pairs"] == 0].sort_values("feature")
    rows = []
    for row in passed.head(40).itertuples(index=False):
        mapping = row._asdict()
        rows.append(
            [
                mapping["feature"],
                int(mapping.get("auditable", 0)),
                int(mapping.get("untestable", 0)),
            ]
        )
    text = _markdown_table(["feature", "auditable road classes", "untestable road classes"], rows)
    if len(passed) > 40:
        text += f"\n\nShowing first 40 of {len(passed):,} non-flagged features."
    if flagged_features:
        text += f"\n\nFlagged features excluded from this pass table: {', '.join(sorted(flagged_features))}."
    return text


def _write_report(
    *,
    subset_selection: BBoxSelection,
    subset_counts: FilterCounts,
    full_counts: FilterCounts,
    subset_build_seconds: float,
    subset_audit_seconds: float,
    full_build_seconds: float,
    full_audit_seconds: float,
    full_result: AuditResult,
) -> None:
    fallback_note = (
        "The configured `study_area.bbox_bng` covered more than 30% of cached OpenRoads "
        "links, so the development subset used the fallback West Yorkshire 50 km BNG square."
        if subset_selection.used_fallback
        else "The configured `study_area.bbox_bng` was small enough for development use."
    )
    bounds = subset_selection.bounds
    bbox_text = (
        f"{subset_selection.name}: "
        f"E {bounds['min_easting']:.0f}-{bounds['max_easting']:.0f}, "
        f"N {bounds['min_northing']:.0f}-{bounds['max_northing']:.0f}"
    )

    untestable_summary = (
        full_result.untestable.groupby(["feature", "untestable_reason"], observed=True)
        .size()
        .reset_index(name="n_road_classes")
        .sort_values(["feature", "untestable_reason"])
    )
    untestable_rows = [
        [row.feature, row.untestable_reason, int(row.n_road_classes)]
        for row in untestable_summary.itertuples(index=False)
    ]
    untestable_table = (
        _markdown_table(["feature", "reason", "road classes"], untestable_rows)
        if untestable_rows
        else "No within-class degenerate feature/road-class pairs."
    )

    skipped_global_rows = [
        [row.feature, f"{row.global_non_null_share:.1%}"]
        for row in full_result.skipped_global.sort_values("feature").itertuples(index=False)
    ]
    skipped_global_table = (
        _markdown_table(["feature", "global non-null share"], skipped_global_rows)
        if skipped_global_rows
        else "No globally degenerate features skipped."
    )

    lines = [
        "# Feature Missingness Audit",
        "",
        "## Methodology",
        "",
        "This audit rebuilds the current Stage 2 collision dataset with "
        "`build_collision_dataset()` and checks only NaN/non-NaN structure. "
        "Collision history is fixed per link: a link is collision-positive if it "
        "had at least one collision in 2015-2024, otherwise it is zero-collision. "
        "Coverage is compared within exact `road_classification` strata.",
        "",
        "For each feature, the audit reports both per-link ever-non-null coverage "
        "and per-link-year coverage. Target and collision-derived columns are "
        "skipped, as are globally 0% or 100% non-null features.",
        "",
        "## Development Subset",
        "",
        fallback_note,
        "",
        f"Selected subset bbox: `{bbox_text}`.",
        "",
        f"Configured bbox link count: {subset_selection.configured_n_links:,} "
        f"({subset_selection.configured_share:.1%} of full cached OpenRoads).",
        "",
        f"Selected subset link count: {subset_selection.selected_n_links:,} "
        f"({subset_selection.selected_share:.1%} of full cached OpenRoads).",
        "",
        "Subset filter counts:",
        "",
        _counts_table(subset_counts),
        "",
        "Full-network counts:",
        "",
        _counts_table(full_counts),
        "",
        "## Runtimes",
        "",
        _markdown_table(
            ["step", "runtime"],
            [
                ["subset build_collision_dataset", _format_seconds(subset_build_seconds)],
                ["subset audit", _format_seconds(subset_audit_seconds)],
                ["full build_collision_dataset", _format_seconds(full_build_seconds)],
                ["full audit", _format_seconds(full_audit_seconds)],
            ],
        ),
        "",
        "## Threshold Calibration",
        "",
        "Gap distribution across auditable feature x road-class pairs before applying flags:",
        "",
        _gap_distribution_table(full_result.gap_distribution),
        "",
        f"Thresholds used: per-link gap > {GAP_THRESHOLD:.0%}, zero-collision "
        f"non-null share < {ZERO_COVERAGE_THRESHOLD:.0%}, and per-link versus "
        f"per-link-year gap disagreement > {VIEW_DISAGREEMENT_THRESHOLD:.0%}. "
        "The 5 percentage point starting threshold was retained after printing "
        "the empirical gap distribution above and before listing flagged features.",
        "",
        "## Flagged Features",
        "",
        _feature_pattern_table(full_result.flagged),
        "",
        "## Expected Flags Baseline",
        "",
        _expected_flags_baseline(full_result),
        "",
        "Recommended next steps for any flags: inspect the feature source table and "
        "join grain, decide separately whether to source from an all-link table, "
        "drop the feature, or impute it. No fixes are made by this diagnostic.",
        "",
        "## Untestable Features",
        "",
        untestable_table,
        "",
        "Globally 0% or 100% non-null features skipped before within-class testing:",
        "",
        skipped_global_table,
        "",
        "## Passed Features",
        "",
        _status_summary_table(full_result),
        "",
        "## Road-Class Consistency",
        "",
        f"Links with inconsistent `road_classification` across years: "
        f"{full_result.inconsistent_road_class_links:,}.",
        "",
        "## Outputs",
        "",
        f"- `{FULL_RAW_OUT.relative_to(_ROOT)}`",
        f"- `{FULL_FLAGGED_OUT.relative_to(_ROOT)}`",
    ]
    REPORT_OUT.write_text("\n".join(lines) + "\n")
    logger.info("Wrote %s", REPORT_OUT)


def _run_subset_audit(
    frames: InputFrames,
) -> tuple[AuditResult, BBoxSelection, FilterCounts, float, float]:
    subset_frames, selection, counts = _subset_inputs(frames)
    subset_df, build_seconds = _build_dataset(subset_frames, label="subset")
    start = _timer()
    subset_result = run_audit(subset_df)
    audit_seconds = _elapsed(start)
    logger.info("Subset audit complete in %s", _format_seconds(audit_seconds))
    return subset_result, selection, counts, build_seconds, audit_seconds


def _run_full_audit(frames: InputFrames) -> tuple[AuditResult, FilterCounts, float, float]:
    full_counts = _full_counts(frames)
    full_df, build_seconds = _build_dataset(frames, label="full")
    start = _timer()
    full_result = run_audit(full_df)
    audit_seconds = _elapsed(start)
    logger.info("Full audit complete in %s", _format_seconds(audit_seconds))
    return full_result, full_counts, build_seconds, audit_seconds


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run synthetic positive/negative validation cases on the spatial subset and exit.",
    )
    parser.add_argument(
        "--subset-only",
        action="store_true",
        help="Run the real audit only on the development subset. Intended for validation.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    frames = _load_inputs()

    if args.self_test:
        subset_frames, selection, counts = _subset_inputs(frames)
        subset_df, build_seconds = _build_dataset(subset_frames, label="self-test subset")
        start = _timer()
        results = run_self_test(subset_df)
        audit_seconds = _elapsed(start)
        print("\nSynthetic self-test results:")
        print(results.to_string(index=False))
        print(f"\nSubset bbox: {selection.name}")
        print(_counts_table(counts))
        print(
            f"\nSelf-test subset build runtime: {_format_seconds(build_seconds)}; "
            f"self-test audit runtime: {_format_seconds(audit_seconds)}"
        )
        return

    subset_result, selection, subset_counts, subset_build_seconds, subset_audit_seconds = (
        _run_subset_audit(frames)
    )
    print("\nSubset flagged preview:")
    print(subset_result.flagged.head(20).to_string(index=False))

    if args.subset_only:
        return

    full_result, full_counts, full_build_seconds, full_audit_seconds = _run_full_audit(frames)
    _write_full_outputs(full_result)
    _write_report(
        subset_selection=selection,
        subset_counts=subset_counts,
        full_counts=full_counts,
        subset_build_seconds=subset_build_seconds,
        subset_audit_seconds=subset_audit_seconds,
        full_build_seconds=full_build_seconds,
        full_audit_seconds=full_audit_seconds,
        full_result=full_result,
    )
    print("\nFull flagged features:")
    print(full_result.flagged.to_string(index=False))
    print(f"\nWrote {FULL_RAW_OUT}")
    print(f"Wrote {FULL_FLAGGED_OUT}")
    print(f"Wrote {REPORT_OUT}")


if __name__ == "__main__":
    main()
