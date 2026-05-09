"""
Build the v0.1 top-risk road segment output.

This script consumes existing scored outputs only. It does not retrain models
or modify production scoring artefacts.
"""

from __future__ import annotations

import argparse
import logging
import math
import tomllib
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import shapely
from shapely.ops import transform

from road_risk.config import _ROOT

logger = logging.getLogger(__name__)

DEFAULT_RISK_EB_PATH = _ROOT / "data/models/risk_scores_eb.parquet"
DEFAULT_RISK_PATH = _ROOT / "data/models/risk_scores.parquet"
OPENROADS_PATH = _ROOT / "data/processed/shapefiles/openroads.parquet"
NETWORK_PATH = _ROOT / "data/features/network_features.parquet"
PARQUET_PATH = _ROOT / "data/outputs/top_1pct_risk_segments.parquet"
CSV_PATH = _ROOT / "data/outputs/top_1pct_risk_segments.csv"
REPORT_PATH = _ROOT / "reports/top_1pct_risk_segments.md"
FAMILY_PARQUET_PATH = _ROOT / "data/outputs/top_risk_by_family.parquet"
FAMILY_CSV_PATH = _ROOT / "data/outputs/top_risk_by_family.csv"
ROAD_CLASS_PARQUET_PATH = _ROOT / "data/outputs/top_risk_by_road_class.parquet"
ROAD_CLASS_CSV_PATH = _ROOT / "data/outputs/top_risk_by_road_class.csv"
ARCHETYPE_PARQUET_PATH = _ROOT / "data/outputs/top_risk_by_road_archetype.parquet"
ARCHETYPE_CSV_PATH = _ROOT / "data/outputs/top_risk_by_road_archetype.csv"
GROUP_REPORT_PATH = _ROOT / "reports/top_risk_by_group.md"
PLOT_DIR = _ROOT / "reports/figures/top_risk_context"

FAMILY_GROUPS = ["motorway", "trunk_a", "other_urban", "other_rural", "other_unknown"]
ARCHETYPE_GROUPS = [
    "motorway",
    "trunk_a",
    "urban_a_road",
    "rural_a_road",
    "urban_b_road",
    "rural_b_road",
    "urban_minor",
    "rural_minor",
    "other_unknown",
]
ROAD_CLASS_GROUPS = [
    "Motorway",
    "A Road",
    "B Road",
    "Classified Unnumbered",
    "Unclassified",
    "Not Classified",
    "Unknown",
]
MINOR_ROAD_CLASSES = {
    "Classified Unnumbered",
    "Unclassified",
    "Not Classified",
    "Unknown",
}


RISK_BASE_COLUMNS = [
    "link_id",
    "collision_count",
    "fatal_count",
    "serious_count",
    "estimated_aadt",
    "predicted_glm",
    "predicted_xgb",
    "predicted_eb",
    "risk_percentile",
    "risk_percentile_eb",
    "residual_glm",
    "hgv_proportion",
    "speed_limit_mph_effective",
    "speed_limit_mph",
    "betweenness_relative",
    "n_years",
    "eb_weight",
]

OPENROADS_COLUMNS = [
    "link_id",
    "road_classification",
    "road_function",
    "form_of_way",
    "road_number",
    "road_name",
    "link_length_m",
    "link_length_km",
    "is_trunk",
    "is_primary",
    "geometry",
]

NETWORK_COLUMNS = [
    "link_id",
    "ruc_class",
    "ruc_urban_rural",
    "imd_decile",
    "imd_crime_decile",
    "imd_living_indoor_decile",
    "mean_grade",
    "max_grade",
    "grade_change",
    "mean_curvature_deg_per_km",
    "max_curvature_deg_per_km",
    "sinuosity",
    "speed_limit_mph_effective",
    "speed_limit_mph",
    "speed_limit_source",
    "speed_limit_mph_imputed",
    "degree_mean",
    "dist_to_major_km",
    "pop_density_per_km2",
    "betweenness_relative",
]

CSV_DROP_COLUMNS = {
    "geometry",
    "link_length_m",
    "road_name",
    "hgv_proportion",
    "residual_glm",
    "speed_limit_source",
}

GROUP_OUTPUT_COLUMNS = [
    "link_id",
    "within_group_rank",
    "within_group_percentile",
    "group_name",
    "group_type",
    "global_risk_rank",
    "ranking_source",
    "risk_percentile_eb",
    "risk_percentile",
    "predicted_eb",
    "predicted_xgb",
    "predicted_glm",
    "collision_count",
    "fatal_count",
    "serious_count",
    "estimated_aadt",
    "link_length_km",
    "road_classification",
    "road_function",
    "family",
    "road_archetype",
    "form_of_way",
    "road_number",
    "road_name",
    "is_motorway",
    "is_trunk",
    "is_primary",
    "is_dual",
    "is_slip_road",
    "is_roundabout",
    "ruc_urban_rural",
    "ruc_class",
    "speed_limit_mph_effective",
    "speed_limit_mph",
    "mean_grade",
    "low_exposure_flag",
    "sparse_collision_history_flag",
    "calibration_caveat",
    "centroid_longitude",
    "centroid_latitude",
    "output_created_at_utc",
    "source_risk_scores_file",
    "model_output_version",
]


def _schema_columns(path: Path) -> list[str]:
    return pq.ParquetFile(path).schema_arrow.names


def _existing_columns(path: Path, wanted: list[str]) -> list[str]:
    available = set(_schema_columns(path))
    return [col for col in wanted if col in available]


def _read_parquet_filtered(path: Path, columns: list[str], link_ids: set[str]) -> pd.DataFrame:
    """Read only requested columns and retain matching link IDs batch-by-batch."""
    frames: list[pd.DataFrame] = []
    parquet_file = pq.ParquetFile(path)
    for batch in parquet_file.iter_batches(columns=columns, batch_size=200_000):
        df = batch.to_pandas()
        df = df[df["link_id"].isin(link_ids)]
        if not df.empty:
            frames.append(df)
    if not frames:
        return pd.DataFrame(columns=columns)
    return pd.concat(frames, ignore_index=True)


def _read_parquet_selected(
    path: Path,
    columns: list[str],
    link_ids: set[str] | None = None,
) -> pd.DataFrame:
    if link_ids is None:
        return pd.read_parquet(path, columns=columns)
    return _read_parquet_filtered(path, columns, link_ids)


def _choose_risk_path(ranking_field: str, explicit_path: Path | None) -> Path:
    if explicit_path is not None:
        return explicit_path
    candidates = [DEFAULT_RISK_EB_PATH, DEFAULT_RISK_PATH]
    for path in candidates:
        if path.exists() and ranking_field in _schema_columns(path):
            return path
    available = {
        str(path.relative_to(_ROOT)): _schema_columns(path) if path.exists() else []
        for path in candidates
    }
    raise KeyError(
        f"Ranking field '{ranking_field}' was not found in candidate risk score files: {available}"
    )


def _project_version() -> str:
    pyproject = _ROOT / "pyproject.toml"
    with open(pyproject, "rb") as f:
        return str(tomllib.load(f).get("project", {}).get("version", "unknown"))


def _source_fingerprint(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": str(path.relative_to(_ROOT)),
        "mtime_utc": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
        "size_bytes": stat.st_size,
    }


def _format_number(value: Any, digits: int = 3) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, (int, np.integer)):
        return f"{int(value):,}"
    if isinstance(value, (float, np.floating)):
        return f"{float(value):,.{digits}f}"
    return str(value)


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def _count_table(df: pd.DataFrame, column: str) -> list[list[Any]]:
    if column not in df.columns:
        return [["missing", 0, "0.0%"]]
    counts = df[column].fillna("Unknown").value_counts(dropna=False)
    return [
        [str(label), f"{int(count):,}", f"{count / len(df) * 100:.1f}%"]
        for label, count in counts.items()
    ]


def _summary_table(df: pd.DataFrame, columns: list[str]) -> list[list[Any]]:
    rows = []
    for col in columns:
        if col not in df.columns:
            continue
        series = pd.to_numeric(df[col], errors="coerce").dropna()
        if series.empty:
            continue
        rows.append(
            [
                col,
                f"{len(series):,}",
                _format_number(series.min()),
                _format_number(series.median()),
                _format_number(series.mean()),
                _format_number(series.quantile(0.9)),
                _format_number(series.max()),
            ]
        )
    return rows


def _derive_family(df: pd.DataFrame) -> pd.Series:
    road_function = df.get("road_function", pd.Series("", index=df.index)).fillna("")
    ruc = df.get("ruc_urban_rural", pd.Series("", index=df.index)).fillna("")
    is_trunk = df.get("is_trunk", pd.Series(False, index=df.index)).fillna(False).astype(bool)

    conditions = [
        road_function.eq("Motorway"),
        road_function.eq("A Road") & is_trunk,
        ruc.eq("Urban"),
        ruc.eq("Rural"),
    ]
    choices = ["motorway", "trunk_a", "other_urban", "other_rural"]
    return pd.Series(np.select(conditions, choices, default="other_unknown"), index=df.index)


def _derive_road_archetype(df: pd.DataFrame) -> pd.Series:
    family = df.get("family", pd.Series("", index=df.index)).fillna("")
    road_classification = df.get("road_classification", pd.Series("", index=df.index)).fillna("")

    conditions = [
        family.eq("motorway"),
        family.eq("trunk_a"),
        road_classification.eq("A Road") & family.eq("other_urban"),
        road_classification.eq("A Road") & family.eq("other_rural"),
        road_classification.eq("B Road") & family.eq("other_urban"),
        road_classification.eq("B Road") & family.eq("other_rural"),
        road_classification.isin(MINOR_ROAD_CLASSES) & family.eq("other_urban"),
        road_classification.isin(MINOR_ROAD_CLASSES) & family.eq("other_rural"),
    ]
    choices = [
        "motorway",
        "trunk_a",
        "urban_a_road",
        "rural_a_road",
        "urban_b_road",
        "rural_b_road",
        "urban_minor",
        "rural_minor",
    ]
    return pd.Series(np.select(conditions, choices, default="other_unknown"), index=df.index)


def _calibration_caveat(row: pd.Series) -> str:
    caveats = []
    if bool(row.get("is_motorway", False)):
        caveats.append("motorway calibration caveat")
    if bool(row.get("low_exposure_flag", False)):
        caveats.append("low exposure")
    if bool(row.get("sparse_collision_history_flag", False)):
        caveats.append("sparse collision history")
    return "; ".join(caveats)


def _load_ranked_scores(risk_path: Path, ranking_field: str) -> pd.DataFrame:
    risk_columns = _existing_columns(risk_path, RISK_BASE_COLUMNS)
    if "link_id" not in risk_columns:
        raise KeyError(f"Risk score file has no link_id column: {risk_path}")
    if ranking_field not in risk_columns:
        raise KeyError(f"Requested ranking field '{ranking_field}' missing from {risk_path}")

    logger.info("Loading risk scores from %s", risk_path.relative_to(_ROOT))
    scores = pd.read_parquet(risk_path, columns=risk_columns)
    scores[ranking_field] = pd.to_numeric(scores[ranking_field], errors="coerce")
    if scores[ranking_field].isna().any():
        missing = int(scores[ranking_field].isna().sum())
        raise ValueError(f"{missing:,} rows have missing ranking field '{ranking_field}'")

    ranked = scores.sort_values(
        [ranking_field, "link_id"],
        ascending=[False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    ranked.insert(1, "global_risk_rank", np.arange(1, len(ranked) + 1))
    return ranked


def _prepare_top_scores(
    risk_path: Path,
    ranking_field: str,
    percentile: float,
) -> tuple[pd.DataFrame, int]:
    scores = _load_ranked_scores(risk_path, ranking_field)
    top_n = math.ceil(len(scores) * percentile / 100)
    if top_n <= 0:
        raise ValueError(f"Percentile must select at least one row; got {percentile}")

    top = scores.head(top_n).copy()
    top.insert(1, "risk_rank", range(1, len(top) + 1))
    top.insert(2, "ranking_source", ranking_field)
    logger.info(
        "Selected top %.3f%%: %s / %s rows", percentile, f"{len(top):,}", f"{len(scores):,}"
    )
    return top, len(scores)


def _join_metadata(top: pd.DataFrame) -> tuple[gpd.GeoDataFrame, list[Path]]:
    source_paths = [OPENROADS_PATH, NETWORK_PATH]
    link_ids = set(top["link_id"])

    openroads_cols = _existing_columns(OPENROADS_PATH, OPENROADS_COLUMNS)
    logger.info("Joining Open Roads metadata from %s", OPENROADS_PATH.relative_to(_ROOT))
    openroads = _read_parquet_filtered(OPENROADS_PATH, openroads_cols, link_ids)

    network_cols = _existing_columns(NETWORK_PATH, NETWORK_COLUMNS)
    logger.info("Joining network features from %s", NETWORK_PATH.relative_to(_ROOT))
    network = _read_parquet_filtered(NETWORK_PATH, network_cols, link_ids)

    metadata = openroads
    if not network.empty:
        duplicate_cols = [c for c in network.columns if c != "link_id" and c in metadata.columns]
        network = network.drop(columns=duplicate_cols)
        metadata = metadata.merge(network, on="link_id", how="left", validate="one_to_one")

    duplicate_cols = [c for c in metadata.columns if c != "link_id" and c in top.columns]
    merged = top.drop(columns=duplicate_cols, errors="ignore").merge(
        metadata,
        on="link_id",
        how="left",
        validate="one_to_one",
    )
    if len(merged) != len(top):
        raise RuntimeError("Metadata join changed the top-risk row count")

    if "geometry" in merged.columns:
        geometry = shapely.from_wkb(merged["geometry"])
        gdf = gpd.GeoDataFrame(
            merged.drop(columns=["geometry"]), geometry=geometry, crs="EPSG:4326"
        )
    else:
        gdf = gpd.GeoDataFrame(merged)
    return gdf, source_paths


def _add_output_columns(
    gdf: gpd.GeoDataFrame,
    risk_path: Path,
    ranking_field: str,
    created_at: str,
) -> gpd.GeoDataFrame:
    result = gdf.copy()
    if "risk_percentile" in result.columns:
        result["risk_percentile"] = pd.to_numeric(result["risk_percentile"], errors="coerce")
    if "risk_percentile_eb" in result.columns:
        result["risk_percentile_eb"] = pd.to_numeric(result["risk_percentile_eb"], errors="coerce")

    road_classification = result.get(
        "road_classification", pd.Series("", index=result.index)
    ).fillna("")
    road_function = result.get("road_function", pd.Series("", index=result.index)).fillna("")
    result["is_motorway"] = road_classification.eq("Motorway") | road_function.eq("Motorway")
    if "is_trunk" in result.columns:
        result["is_trunk"] = result["is_trunk"].fillna(False).astype(bool)
    if "is_primary" in result.columns:
        result["is_primary"] = result["is_primary"].fillna(False).astype(bool)

    form_of_way = result.get("form_of_way", pd.Series("", index=result.index)).fillna("")
    result["is_dual"] = form_of_way.isin({"Dual Carriageway", "Collapsed Dual Carriageway"})
    result["is_slip_road"] = form_of_way.eq("Slip Road")
    result["is_roundabout"] = form_of_way.eq("Roundabout")
    result["family"] = _derive_family(result)
    result["road_archetype"] = _derive_road_archetype(result)
    result["low_exposure_flag"] = pd.to_numeric(
        result.get("estimated_aadt", np.nan), errors="coerce"
    ).lt(500)
    result["sparse_collision_history_flag"] = pd.to_numeric(
        result.get("collision_count", np.nan), errors="coerce"
    ).le(1)
    result["calibration_caveat"] = result.apply(_calibration_caveat, axis=1)
    result["output_created_at_utc"] = created_at
    result["source_risk_scores_file"] = str(risk_path.relative_to(_ROOT))
    result["model_output_version"] = _project_version()

    if "geometry" in result.columns:
        # These source geometries are already WGS84 line strings. The lon/lat
        # centroid is only a light CSV/map locator, not a measured geometry.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Geometry is in a geographic CRS")
            centroids = result.geometry.centroid
        result["centroid_longitude"] = centroids.x
        result["centroid_latitude"] = centroids.y

    ordered = [
        "link_id",
        "risk_rank",
        "global_risk_rank",
        "within_group_rank",
        "within_group_percentile",
        "group_name",
        "group_type",
        "ranking_source",
        ranking_field,
        "risk_percentile",
        "risk_percentile_eb",
        "predicted_eb",
        "predicted_xgb",
        "predicted_glm",
        "collision_count",
        "fatal_count",
        "serious_count",
        "estimated_aadt",
        "link_length_km",
        "road_classification",
        "road_function",
        "family",
        "road_archetype",
        "form_of_way",
        "road_number",
        "road_name",
        "is_motorway",
        "is_trunk",
        "is_primary",
        "is_dual",
        "is_slip_road",
        "is_roundabout",
        "ruc_urban_rural",
        "ruc_class",
        "speed_limit_mph_effective",
        "speed_limit_mph",
        "mean_grade",
        "low_exposure_flag",
        "sparse_collision_history_flag",
        "calibration_caveat",
        "centroid_longitude",
        "centroid_latitude",
        "output_created_at_utc",
        "source_risk_scores_file",
        "model_output_version",
    ]
    cols = []
    for col in ordered + list(result.columns):
        if col in result.columns and col not in cols:
            cols.append(col)
    return result[cols]


def _project_centroids(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    result = gdf.copy()
    if "geometry" in result.columns:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Geometry is in a geographic CRS")
            centroids = result.geometry.centroid
        result["centroid_longitude"] = centroids.x
        result["centroid_latitude"] = centroids.y
    return result


def _load_non_spatial_metadata() -> tuple[pd.DataFrame, list[Path]]:
    source_paths = [OPENROADS_PATH, NETWORK_PATH]
    openroads_cols = _existing_columns(
        OPENROADS_PATH,
        [col for col in OPENROADS_COLUMNS if col != "geometry"],
    )
    network_cols = _existing_columns(NETWORK_PATH, NETWORK_COLUMNS)

    logger.info(
        "Loading non-spatial Open Roads metadata from %s", OPENROADS_PATH.relative_to(_ROOT)
    )
    metadata = _read_parquet_selected(OPENROADS_PATH, openroads_cols)
    logger.info("Loading non-spatial network metadata from %s", NETWORK_PATH.relative_to(_ROOT))
    network = _read_parquet_selected(NETWORK_PATH, network_cols)

    duplicate_cols = [c for c in network.columns if c != "link_id" and c in metadata.columns]
    if duplicate_cols:
        network = network.drop(columns=duplicate_cols)
    metadata = metadata.merge(network, on="link_id", how="left", validate="one_to_one")
    return metadata, source_paths


def _select_group_top(
    full: pd.DataFrame,
    group_col: str,
    group_type: str,
    ranking_field: str,
    top_n: int,
    expected_groups: list[str],
) -> pd.DataFrame:
    if group_col not in full.columns:
        raise KeyError(f"Required group column missing: {group_col}")
    if top_n <= 0:
        raise ValueError(f"--top-n must be positive; got {top_n}")

    grouped = full.copy()
    grouped[group_col] = grouped[group_col].fillna("Unknown")
    grouped["within_group_rank"] = (
        grouped.groupby(group_col, dropna=False)[ranking_field]
        .rank(method="first", ascending=False)
        .astype(int)
    )
    grouped["within_group_percentile"] = (
        grouped.groupby(group_col, dropna=False)[ranking_field].rank(method="average", pct=True)
        * 100
    )
    selected = grouped[
        grouped[group_col].isin(expected_groups) & grouped["within_group_rank"].le(top_n)
    ].copy()
    selected["group_name"] = selected[group_col]
    selected["group_type"] = group_type
    selected["ranking_source"] = ranking_field
    selected = selected.sort_values(
        ["group_name", "within_group_rank", "link_id"],
        kind="mergesort",
    ).reset_index(drop=True)
    return selected


def _finalize_group_output(
    selected: pd.DataFrame,
    risk_path: Path,
    ranking_field: str,
    created_at: str,
) -> gpd.GeoDataFrame:
    gdf, _ = _join_metadata(selected)
    gdf = _add_output_columns(gdf, risk_path, ranking_field, created_at)
    cols = []
    for col in GROUP_OUTPUT_COLUMNS + list(gdf.columns):
        if col in gdf.columns and col not in cols:
            cols.append(col)
    return gdf[cols].sort_values(["group_name", "within_group_rank"], kind="mergesort")


def _write_group_report(
    family_gdf: gpd.GeoDataFrame,
    road_class_gdf: gpd.GeoDataFrame,
    archetype_gdf: gpd.GeoDataFrame,
    path: Path,
    source_paths: list[Path],
    risk_path: Path,
    ranking_field: str,
    top_n: int,
    created_at: str,
) -> None:
    def top_rows(df: pd.DataFrame, group_name: str, n: int = 10) -> list[list[Any]]:
        cols = [
            "within_group_rank",
            "global_risk_rank",
            "link_id",
            "road_classification",
            "road_function",
            "family",
            "road_archetype",
            "form_of_way",
            "is_dual",
            "is_slip_road",
            "is_roundabout",
            "estimated_aadt",
            "link_length_km",
            "collision_count",
            "predicted_eb",
            "predicted_xgb",
            "risk_percentile_eb",
            "centroid_longitude",
            "centroid_latitude",
        ]
        subset = df[df["group_name"] == group_name].head(n)
        if subset.empty:
            return [["No rows available"] + [""] * (len(cols) - 1)]
        return [
            [_format_number(value) for value in row]
            for row in subset[[c for c in cols if c in subset.columns]].to_numpy().tolist()
        ]

    table_cols = [
        "within_group_rank",
        "global_risk_rank",
        "link_id",
        "road_classification",
        "road_function",
        "family",
        "road_archetype",
        "form_of_way",
        "is_dual",
        "is_slip_road",
        "is_roundabout",
        "estimated_aadt",
        "link_length_km",
        "collision_count",
        "predicted_eb",
        "predicted_xgb",
        "risk_percentile_eb",
        "centroid_longitude",
        "centroid_latitude",
    ]
    source_rows = [
        [source["path"], source["mtime_utc"], f"{source['size_bytes']:,}"]
        for source in [_source_fingerprint(risk_path)]
        + [_source_fingerprint(source_path) for source_path in source_paths]
    ]
    summary_rows = [
        ["family", f"{family_gdf['group_name'].nunique():,}", f"{top_n:,}", f"{len(family_gdf):,}"],
        [
            "road_classification",
            f"{road_class_gdf['group_name'].nunique():,}",
            f"{top_n:,}",
            f"{len(road_class_gdf):,}",
        ],
        [
            "road_archetype",
            f"{archetype_gdf['group_name'].nunique():,}",
            f"{top_n:,}",
            f"{len(archetype_gdf):,}",
        ],
    ]

    sections = [
        "# Top-Risk Links By Comparable Road Group",
        (
            "## Purpose\n\n"
            "The global top-1% table is useful, but the very top of that ranking can be "
            "dominated by high-volume motorway links. These group-specific tables help "
            "inspect high-risk links among comparable road families, OS road classes, "
            "and conservative reporting archetypes."
        ),
        (
            "## Summary\n\n"
            + _markdown_table(["group_type", "groups", "top_n_per_group", "rows"], summary_rows)
            + f"\n\nRanking field used: `{ranking_field}`.\n\nCreated at: `{created_at}`."
        ),
        (
            "## Road-Type Schemes Used Here\n\n"
            "- `family` is the official comparable-road-type modelling/diagnostic split: "
            "`motorway`, `trunk_a`, `other_urban`, `other_rural`, plus `other_unknown` as "
            "a fallback/reporting bucket when the family inputs do not resolve cleanly.\n"
            "- `road_classification` is the broad OS Open Roads classification axis "
            "(`Motorway`, `A Road`, `B Road`, `Classified Unnumbered`, `Unclassified`, "
            "`Not Classified`, `Unknown`). It is useful for inspection but is not the "
            "same thing as the modelling family split.\n"
            "- `road_function` is the OS functional category, retained as descriptive "
            "context because it is often more informative below trunk-road scale.\n"
            "- `form_of_way` and derived flags (`is_dual`, `is_slip_road`, "
            "`is_roundabout`) describe physical form. They are important map/filter "
            "fields, but the repo's v1 family design explicitly did not adopt "
            "dual/single/roundabout/slip as separate families.\n"
            "- `road_archetype` is a conservative reporting convenience that combines "
            "`family` with broad road class. It is not a model family and should not be "
            "read as a new production ranking surface."
        ),
        (
            "## Provenance\n\n"
            + _markdown_table(["source", "mtime_utc", "size_bytes"], source_rows)
            + f"\n\nProject/model output version: `{_project_version()}`."
        ),
        (
            "## Count By Road Archetype\n\n"
            f"Each archetype table contains the top {top_n:,} links within that archetype, "
            "so the count table below shows output allocation rather than population "
            "prevalence. For prevalence, use the global top-1% `Count By Road Archetype` "
            "table.\n\n"
            + _markdown_table(
                ["road_archetype", "count", "share"],
                _count_table(archetype_gdf, "group_name"),
            )
        ),
    ]

    for group_name in ["motorway", "trunk_a", "other_urban", "other_rural"]:
        sections.append(
            f"## Family: {group_name}\n\n"
            + _markdown_table(
                [c for c in table_cols if c in family_gdf.columns], top_rows(family_gdf, group_name)
            )
        )
    for group_name in ["A Road", "B Road", "Unclassified"]:
        sections.append(
            f"## Road Classification: {group_name}\n\n"
            + _markdown_table(
                [c for c in table_cols if c in road_class_gdf.columns],
                top_rows(road_class_gdf, group_name),
            )
        )
    for group_name in ARCHETYPE_GROUPS:
        sections.append(
            f"## Road Archetype: {group_name}\n\n"
            + _markdown_table(
                [c for c in table_cols if c in archetype_gdf.columns],
                top_rows(archetype_gdf, group_name),
            )
        )

    sections.extend(
        [
            (
                "## Caveats\n\n"
                "- These are within-group rankings, not claims that risk is comparable across all road types.\n"
                "- A top-ranked rural road may have much lower absolute risk than a top-ranked motorway.\n"
                "- `road_archetype` is only a reporting convenience; it is not a model family.\n"
                "- `other_unknown` is a fallback/reporting bucket, not a deliberately modelled family.\n"
                "- `form_of_way` remains descriptive context unless later residual diagnostics justify separate families.\n"
                "- Motorway calibration remains a known caveat.\n"
                "- EB ranking still reflects observed collision history and should be treated as screening evidence."
            ),
            (
                "## Next Use\n\n"
                "Use these finalised output columns to seed map review, stakeholder examples, "
                "or class-specific portfolio triage without losing the global risk columns.\n\n"
                "TODO: build the interactive QMD map against these finalised output columns."
            ),
        ]
    )
    path.write_text("\n\n".join(sections) + "\n")
    logger.info("Wrote grouped report to %s", path.relative_to(_ROOT))


def build_group_outputs(
    top_n: int,
    ranking_field: str,
    risk_scores_path: Path | None,
    make_plots: bool,
    plot_top_n: int,
    buffer_motorway_m: float,
    buffer_default_m: float,
) -> dict[str, Any]:
    created_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    risk_path = _choose_risk_path(ranking_field, risk_scores_path)
    scores = _load_ranked_scores(risk_path, ranking_field)
    metadata, metadata_sources = _load_non_spatial_metadata()

    duplicate_cols = [c for c in metadata.columns if c != "link_id" and c in scores.columns]
    full = scores.drop(columns=duplicate_cols, errors="ignore").merge(
        metadata,
        on="link_id",
        how="left",
        validate="one_to_one",
    )
    if len(full) != len(scores):
        raise RuntimeError("Full metadata join changed scored row count")
    full = _add_output_columns(gpd.GeoDataFrame(full), risk_path, ranking_field, created_at)

    family_selected = _select_group_top(
        full, "family", "family", ranking_field, top_n, FAMILY_GROUPS
    )
    road_class_selected = _select_group_top(
        full,
        "road_classification",
        "road_classification",
        ranking_field,
        top_n,
        ROAD_CLASS_GROUPS,
    )
    archetype_selected = _select_group_top(
        full,
        "road_archetype",
        "road_archetype",
        ranking_field,
        top_n,
        ARCHETYPE_GROUPS,
    )

    family_gdf = _finalize_group_output(family_selected, risk_path, ranking_field, created_at)
    road_class_gdf = _finalize_group_output(
        road_class_selected, risk_path, ranking_field, created_at
    )
    archetype_gdf = _finalize_group_output(archetype_selected, risk_path, ranking_field, created_at)

    for path, gdf in [
        (FAMILY_PARQUET_PATH, family_gdf),
        (ROAD_CLASS_PARQUET_PATH, road_class_gdf),
        (ARCHETYPE_PARQUET_PATH, archetype_gdf),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        gdf.to_parquet(path, index=False)
        logger.info("Wrote grouped Parquet to %s", path.relative_to(_ROOT))
    _write_csv(family_gdf, FAMILY_CSV_PATH)
    _write_csv(road_class_gdf, ROAD_CLASS_CSV_PATH)
    _write_csv(archetype_gdf, ARCHETYPE_CSV_PATH)

    GROUP_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _write_group_report(
        family_gdf,
        road_class_gdf,
        archetype_gdf,
        GROUP_REPORT_PATH,
        metadata_sources,
        risk_path,
        ranking_field,
        top_n,
        created_at,
    )

    plot_paths: list[Path] = []
    if make_plots:
        plot_paths = make_context_plots(
            family_gdf,
            road_class_gdf,
            scores,
            ranking_field,
            plot_top_n,
            buffer_motorway_m,
            buffer_default_m,
            PLOT_DIR,
        )

    return {
        "ranking_field": ranking_field,
        "family_rows": len(family_gdf),
        "road_class_rows": len(road_class_gdf),
        "family_path": FAMILY_PARQUET_PATH,
        "family_csv_path": FAMILY_CSV_PATH,
        "road_class_path": ROAD_CLASS_PARQUET_PATH,
        "road_class_csv_path": ROAD_CLASS_CSV_PATH,
        "archetype_rows": len(archetype_gdf),
        "archetype_path": ARCHETYPE_PARQUET_PATH,
        "archetype_csv_path": ARCHETYPE_CSV_PATH,
        "report_path": GROUP_REPORT_PATH,
        "plot_count": len(plot_paths),
        "plot_dir": PLOT_DIR,
        "family_counts": family_gdf["group_name"].value_counts().to_dict(),
        "road_class_counts": road_class_gdf["group_name"].value_counts().to_dict(),
        "archetype_counts": archetype_gdf["group_name"].value_counts().to_dict(),
    }


def _write_csv(gdf: gpd.GeoDataFrame, path: Path) -> None:
    csv_df = pd.DataFrame(gdf.drop(columns=[c for c in CSV_DROP_COLUMNS if c in gdf.columns]))
    csv_df.to_csv(path, index=False)
    logger.info("Wrote CSV to %s", path.relative_to(_ROOT))


def _write_report(
    gdf: gpd.GeoDataFrame,
    path: Path,
    source_paths: list[Path],
    risk_path: Path,
    ranking_field: str,
    percentile: float,
    population_count: int,
    created_at: str,
) -> None:
    top_example_cols = [
        "risk_rank",
        "link_id",
        "road_classification",
        "road_function",
        "family",
        "road_archetype",
        "form_of_way",
        "estimated_aadt",
        "link_length_km",
        "collision_count",
        "predicted_eb",
        "predicted_xgb",
        "risk_percentile_eb",
        "risk_percentile",
        "is_motorway",
        "low_exposure_flag",
        "sparse_collision_history_flag",
        "centroid_longitude",
        "centroid_latitude",
    ]
    top_rows = []
    for _, row in gdf[[c for c in top_example_cols if c in gdf.columns]].head(20).iterrows():
        top_rows.append([_format_number(value) for value in row.to_list()])

    summary_cols = [
        "estimated_aadt",
        "link_length_km",
        "collision_count",
        "fatal_count",
        "serious_count",
        "predicted_eb",
        "predicted_xgb",
        "predicted_glm",
    ]
    summary_rows = _summary_table(gdf, summary_cols)

    sources = [_source_fingerprint(risk_path)] + [_source_fingerprint(p) for p in source_paths]
    source_rows = [
        [source["path"], source["mtime_utc"], f"{source['size_bytes']:,}"] for source in sources
    ]

    report = "\n\n".join(
        [
            "# Top 1% Highest-Risk Road Segments",
            (
                "## Purpose\n\n"
                "This table lists the top 1% highest-risk road links after controlling for "
                "traffic exposure. It is intended for inspection, mapping, portfolio review, "
                "and demo use."
            ),
            (
                "## Method\n\n"
                f"- Ranking field used: `{ranking_field}`.\n"
                f"- EB-adjusted ranking used: {'yes' if ranking_field == 'risk_percentile_eb' else 'no'}.\n"
                f"- Top 1% definition: sorted all {population_count:,} scored links by "
                f"`{ranking_field}` descending, with `link_id` as a deterministic tie-break, "
                f"then selected the first {len(gdf):,} rows ({percentile:g}%).\n"
                f"- Created at: `{created_at}`."
            ),
            (
                "## Provenance\n\n"
                + _markdown_table(["source", "mtime_utc", "size_bytes"], source_rows)
                + f"\n\nProject/model output version: `{_project_version()}`."
            ),
            (
                "## Count By Road Family\n\n"
                + _markdown_table(["family", "count", "share"], _count_table(gdf, "family"))
            ),
            (
                "## Count By Road Classification\n\n"
                + _markdown_table(
                    ["road_classification", "count", "share"],
                    _count_table(gdf, "road_classification"),
                )
            ),
            (
                "## Count By Urban/Rural\n\n"
                + _markdown_table(
                    ["ruc_urban_rural", "count", "share"],
                    _count_table(gdf, "ruc_urban_rural"),
                )
            ),
            (
                "## Count By Road Archetype\n\n"
                + _markdown_table(
                    ["road_archetype", "count", "share"],
                    _count_table(gdf, "road_archetype"),
                )
            ),
            (
                "## Numeric Summary\n\n"
                + _markdown_table(
                    ["field", "n", "min", "median", "mean", "p90", "max"],
                    summary_rows,
                )
            ),
            (
                "## Top Examples\n\n"
                + _markdown_table([c for c in top_example_cols if c in gdf.columns], top_rows)
            ),
            (
                "## Caveats\n\n"
                "- This is a triage and screening output, not causal proof.\n"
                "- Motorway calibration remains a known caveat.\n"
                "- Sparse collision histories should be interpreted cautiously.\n"
                "- This does not replace engineering audit or iRAP-style assessment."
            ),
            (
                "## Next Use\n\n"
                "This output can feed a Streamlit map, GeoPackage export, or stakeholder demo."
            ),
        ]
    )
    path.write_text(report + "\n")
    logger.info("Wrote report to %s", path.relative_to(_ROOT))


def build_outputs(
    percentile: float,
    ranking_field: str,
    parquet_path: Path | None,
    csv_path: Path | None,
    report_path: Path,
    risk_scores_path: Path | None,
) -> dict[str, Any]:
    created_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    risk_path = _choose_risk_path(ranking_field, risk_scores_path)
    top, population_count = _prepare_top_scores(risk_path, ranking_field, percentile)
    gdf, metadata_sources = _join_metadata(top)
    gdf = _add_output_columns(gdf, risk_path, ranking_field, created_at)
    gdf = gdf.sort_values(["risk_rank"], kind="mergesort").reset_index(drop=True)

    if parquet_path is not None:
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        gdf.to_parquet(parquet_path, index=False)
        logger.info("Wrote Parquet to %s", parquet_path.relative_to(_ROOT))
    if csv_path is not None:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        _write_csv(gdf, csv_path)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    _write_report(
        gdf,
        report_path,
        metadata_sources,
        risk_path,
        ranking_field,
        percentile,
        population_count,
        created_at,
    )
    return {
        "ranking_field": ranking_field,
        "row_count": len(gdf),
        "population_count": population_count,
        "risk_path": risk_path,
        "parquet_path": parquet_path,
        "csv_path": csv_path,
        "report_path": report_path,
        "family_counts": gdf["family"].value_counts().to_dict(),
        "class_counts": gdf["road_classification"].value_counts(dropna=False).to_dict()
        if "road_classification" in gdf.columns
        else {},
    }


def _safe_filename(value: Any) -> str:
    text = str(value).lower().replace(" ", "_")
    return "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in text)


def _context_degree_padding(
    bounds: tuple[float, float, float, float],
    buffer_m: float,
) -> tuple[float, float]:
    _, miny, _, maxy = bounds
    lat = (miny + maxy) / 2
    lat_pad = buffer_m / 111_320
    lon_pad = buffer_m / max(111_320 * math.cos(math.radians(lat)), 1)
    return lon_pad, lat_pad


def make_context_plots(
    family_gdf: gpd.GeoDataFrame,
    road_class_gdf: gpd.GeoDataFrame,
    ranked_scores: pd.DataFrame,
    ranking_field: str,
    plot_top_n: int,
    buffer_motorway_m: float,
    buffer_default_m: float,
    plot_dir: Path,
) -> list[Path]:
    if "geometry" not in family_gdf.columns or "geometry" not in road_class_gdf.columns:
        raise KeyError("Grouped outputs must contain geometry to make context plots")
    if ranking_field not in ranked_scores.columns:
        raise KeyError(f"Ranking field missing from scores for plotting: {ranking_field}")

    try:
        import os

        plot_cache = Path("/tmp/open-road-risk-plot-cache")
        plot_cache.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("MPLCONFIGDIR", str(plot_cache / "matplotlib"))
        os.environ.setdefault("XDG_CACHE_HOME", str(plot_cache / "xdg"))
        import matplotlib.pyplot as plt
        from pyproj import Transformer
    except ImportError as exc:
        raise ImportError("Context plots require matplotlib and pyproj") from exc

    plot_dir.mkdir(parents=True, exist_ok=True)
    family_plot = family_gdf[
        family_gdf["group_name"].isin(["motorway", "trunk_a", "other_urban", "other_rural"])
        & family_gdf["within_group_rank"].le(plot_top_n)
    ]
    class_plot = road_class_gdf[
        road_class_gdf["group_name"].isin(["B Road", "Unclassified"])
        & road_class_gdf["within_group_rank"].le(plot_top_n)
    ]
    selected = (
        pd.concat([family_plot, class_plot], ignore_index=True)
        .drop_duplicates("link_id", keep="first")
        .reset_index(drop=True)
    )

    context_cols = _existing_columns(
        OPENROADS_PATH,
        ["link_id", "road_classification", "road_function", "geometry"],
    )
    if "geometry" not in context_cols:
        raise KeyError(f"Open Roads file has no geometry column: {OPENROADS_PATH}")
    logger.info("Loading Open Roads geometry for context plots")
    context = gpd.read_parquet(OPENROADS_PATH, columns=context_cols)
    risk_cols = ["link_id", ranking_field]
    if "predicted_eb" in ranked_scores.columns:
        risk_cols.append("predicted_eb")
    context = context.merge(ranked_scores[risk_cols], on="link_id", how="left")
    context_bounds = context.bounds

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    project = transformer.transform

    plot_paths: list[Path] = []
    for _, row in selected.iterrows():
        target_geom = row.geometry
        if target_geom is None or target_geom.is_empty:
            logger.warning("Skipping plot for %s: missing geometry", row["link_id"])
            continue

        large_buffer_context = bool(row.get("is_motorway", False)) or row.get("group_name") in {
            "motorway",
            "other_rural",
        }
        buffer_m = buffer_motorway_m if large_buffer_context else buffer_default_m
        lon_pad, lat_pad = _context_degree_padding(target_geom.bounds, buffer_m)
        minx, miny, maxx, maxy = target_geom.bounds
        mask = (
            (context_bounds["maxx"] >= minx - lon_pad)
            & (context_bounds["minx"] <= maxx + lon_pad)
            & (context_bounds["maxy"] >= miny - lat_pad)
            & (context_bounds["miny"] <= maxy + lat_pad)
        )
        candidates = context.loc[mask].copy()
        if candidates.empty:
            logger.warning("Skipping plot for %s: no context links in bounding box", row["link_id"])
            continue

        target_projected = transform(project, target_geom)
        candidates["geometry"] = candidates.geometry.map(lambda geom: transform(project, geom))
        context_projected = gpd.GeoDataFrame(candidates, geometry="geometry", crs="EPSG:3857")
        context_projected = context_projected[
            context_projected.geometry.intersects(target_projected.buffer(buffer_m))
        ]
        if context_projected.empty:
            logger.warning(
                "Skipping plot for %s: no context links in metric buffer", row["link_id"]
            )
            continue

        target_projected_gdf = gpd.GeoDataFrame(
            [row.drop(labels=["geometry"], errors="ignore").to_dict()],
            geometry=[target_projected],
            crs="EPSG:3857",
        )

        fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=True)
        if (
            ranking_field in context_projected.columns
            and context_projected[ranking_field].notna().any()
        ):
            context_projected.plot(
                ax=ax,
                column=ranking_field,
                cmap="viridis",
                linewidth=1.0,
                legend=True,
                missing_kwds={"color": "#d9d9d9", "label": "missing"},
            )
        else:
            context_projected.plot(ax=ax, color="#c7c7c7", linewidth=1.0)
        target_projected_gdf.plot(ax=ax, color="#e31a1c", linewidth=5.0)
        target_projected_gdf.plot(ax=ax, color="#fff7bc", linewidth=2.0)

        title = (
            f"{row.get('group_type', '')}: {row.get('group_name', '')} | "
            f"rank {int(row.get('within_group_rank', 0))}\n"
            f"{row.get('road_classification', '')} / {row.get('road_function', '')} | "
            f"collisions {_format_number(row.get('collision_count'))} | "
            f"AADT {_format_number(row.get('estimated_aadt'))} | "
            f"{ranking_field} {_format_number(row.get(ranking_field))}"
        )
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
        ax.set_aspect("equal")

        filename = (
            f"{_safe_filename(row.get('group_type'))}_"
            f"{_safe_filename(row.get('group_name'))}_"
            f"rank_{int(row.get('within_group_rank', 0)):03d}_"
            f"{str(row.get('link_id'))[:8]}.png"
        )
        out_path = plot_dir / filename
        fig.savefig(out_path, dpi=180)
        plt.close(fig)
        plot_paths.append(out_path)
        logger.info("Wrote context plot to %s", out_path.relative_to(_ROOT))

    return plot_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--percentile", type=float, default=1.0)
    parser.add_argument("--ranking-field", default="risk_percentile_eb")
    parser.add_argument("--risk-scores", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    parser.add_argument("--csv", nargs="?", const=CSV_PATH, type=Path, default=None)
    parser.add_argument("--parquet", nargs="?", const=PARQUET_PATH, type=Path, default=None)
    parser.add_argument("--top-n", type=int, default=100)
    parser.add_argument("--make-plots", action="store_true")
    parser.add_argument("--plot-top-n", type=int, default=3)
    parser.add_argument("--buffer-motorway-m", type=float, default=2000)
    parser.add_argument("--buffer-default-m", type=float, default=750)
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    args = parse_args()
    csv_path = args.csv
    parquet_path = args.parquet
    if csv_path is None and parquet_path is None:
        csv_path = CSV_PATH
        parquet_path = PARQUET_PATH

    result = build_outputs(
        percentile=args.percentile,
        ranking_field=args.ranking_field,
        parquet_path=parquet_path,
        csv_path=csv_path,
        report_path=args.report,
        risk_scores_path=args.risk_scores,
    )
    logger.info(
        "Done: ranking=%s rows=%s parquet=%s csv=%s report=%s",
        result["ranking_field"],
        f"{result['row_count']:,}",
        result["parquet_path"],
        result["csv_path"],
        result["report_path"],
    )
    group_result = build_group_outputs(
        top_n=args.top_n,
        ranking_field=args.ranking_field,
        risk_scores_path=args.risk_scores,
        make_plots=args.make_plots,
        plot_top_n=args.plot_top_n,
        buffer_motorway_m=args.buffer_motorway_m,
        buffer_default_m=args.buffer_default_m,
    )
    logger.info(
        "Done grouped outputs: ranking=%s family_rows=%s road_class_rows=%s "
        "archetype_rows=%s plots=%s",
        group_result["ranking_field"],
        f"{group_result['family_rows']:,}",
        f"{group_result['road_class_rows']:,}",
        f"{group_result['archetype_rows']:,}",
        f"{group_result['plot_count']:,}",
    )


if __name__ == "__main__":
    main()
