"""Build lightweight static web data for top-risk road segment maps."""

from __future__ import annotations

import argparse
import json
import logging
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import shapely
from pyproj import Transformer
from shapely.ops import transform

from road_risk.config import _ROOT

logger = logging.getLogger(__name__)

DEFAULT_INPUT = _ROOT / "data/outputs/top_1pct_risk_segments.parquet"
DEFAULT_OUTPUT_DIR = _ROOT / "data/outputs/web"
DEFAULT_GEOJSON = DEFAULT_OUTPUT_DIR / "top_1pct_risk_segments.geojson"
DEFAULT_METADATA = DEFAULT_OUTPUT_DIR / "top_1pct_risk_segments_web_metadata.json"
DEFAULT_QUARTO_RESOURCE_DIR = _ROOT / "quarto/data/outputs/web"

WEB_COLUMNS = [
    "global_risk_rank",
    "link_id",
    "road_classification",
    "road_function",
    "family",
    "road_archetype",
    "form_of_way",
    "collision_count",
    "fatal_count",
    "serious_count",
    "estimated_aadt",
    "link_length_km",
    "predicted_eb",
    "predicted_xgb",
    "risk_percentile_eb",
    "calibration_caveat",
    "geometry",
]

ROUNDING = {
    "estimated_aadt": 1,
    "link_length_km": 3,
    "predicted_eb": 3,
    "predicted_xgb": 3,
    "risk_percentile_eb": 3,
    "log_predicted_eb": 4,
    "eb_visual_quantile_global": 2,
}


def _existing_columns(path: Path, wanted: list[str]) -> list[str]:
    available = set(pq.ParquetFile(path).schema_arrow.names)
    missing = [col for col in wanted if col not in available]
    required_missing = [col for col in missing if col != "calibration_caveat"]
    if required_missing:
        raise KeyError(f"Missing required web export columns in {path}: {required_missing}")
    return [col for col in wanted if col in available]


def _round_properties(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    result = gdf.copy()
    for col, digits in ROUNDING.items():
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors="coerce").round(digits)
    for col in ["global_risk_rank", "collision_count", "fatal_count", "serious_count"]:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors="coerce").astype("Int64")
    for col in result.columns.difference(["geometry"]):
        if result[col].dtype == "object":
            result[col] = result[col].fillna("")
    return result


def _simplify_geometry(gdf: gpd.GeoDataFrame, tolerance_m: float) -> gpd.GeoDataFrame:
    if tolerance_m <= 0:
        return gdf
    if gdf.crs is None:
        raise ValueError("Input GeoDataFrame has no CRS; cannot simplify in metres.")
    gdf = gdf.set_crs("EPSG:4326", allow_override=True)
    to_metric = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    to_wgs84 = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    simplified = gdf.copy()
    simplified["geometry"] = simplified.geometry.apply(
        lambda geom: transform(to_metric.transform, geom)
    )
    simplified["geometry"] = simplified.geometry.simplify(tolerance_m, preserve_topology=True)
    simplified["geometry"] = simplified.geometry.apply(
        lambda geom: transform(to_wgs84.transform, geom)
    )
    simplified = simplified.set_crs("EPSG:4326", allow_override=True)
    simplified["geometry"] = shapely.set_precision(simplified.geometry.array, grid_size=0.00001)
    return simplified


def _summary_counts(gdf: gpd.GeoDataFrame, column: str) -> dict[str, int]:
    if column not in gdf.columns:
        return {}
    counts = gdf[column].fillna("Unknown").value_counts(dropna=False)
    return {str(label): int(count) for label, count in counts.items()}


def _numeric_summary(
    gdf: gpd.GeoDataFrame, columns: list[str]
) -> dict[str, dict[str, float | int]]:
    summary: dict[str, dict[str, float | int]] = {}
    for col in columns:
        if col not in gdf.columns:
            continue
        series = pd.to_numeric(gdf[col], errors="coerce").dropna()
        if series.empty:
            continue
        summary[col] = {
            "n": int(series.size),
            "min": round(float(series.min()), 3),
            "median": round(float(series.median()), 3),
            "mean": round(float(series.mean()), 3),
            "p90": round(float(series.quantile(0.9)), 3),
            "max": round(float(series.max()), 3),
        }
    return summary


def build_web_geojson(
    input_path: Path = DEFAULT_INPUT,
    geojson_path: Path = DEFAULT_GEOJSON,
    metadata_path: Path = DEFAULT_METADATA,
    simplify_tolerance_m: float = 25.0,
    quarto_resource_dir: Path | None = DEFAULT_QUARTO_RESOURCE_DIR,
) -> dict[str, Any]:
    columns = _existing_columns(input_path, WEB_COLUMNS)
    logger.info("Loading %s", input_path.relative_to(_ROOT))
    gdf = gpd.read_parquet(input_path, columns=columns)
    if gdf.crs is None:
        raise ValueError(f"{input_path} has no CRS")
    if gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(4326)
    gdf = gdf.set_crs("EPSG:4326", allow_override=True)

    gdf["log_predicted_eb"] = np.log1p(pd.to_numeric(gdf["predicted_eb"], errors="coerce"))
    gdf["eb_visual_quantile_global"] = (
        pd.to_numeric(gdf["predicted_eb"], errors="coerce").rank(pct=True, method="average") * 100
    )

    gdf = _simplify_geometry(gdf, simplify_tolerance_m)
    gdf = _round_properties(gdf)

    geojson_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(geojson_path, driver="GeoJSON")

    metadata = {
        "created_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "source": str(input_path.relative_to(_ROOT)),
        "geojson": str(geojson_path.relative_to(_ROOT)),
        "quarto_resource_copy": (
            str((quarto_resource_dir / geojson_path.name).relative_to(_ROOT))
            if quarto_resource_dir is not None
            else None
        ),
        "rows": int(len(gdf)),
        "crs": "EPSG:4326",
        "geometry_simplification_tolerance_m": simplify_tolerance_m,
        "geometry_simplification_crs": "EPSG:3857",
        "coordinate_precision_degrees": 0.00001,
        "colour_scaling": "log_predicted_eb = log1p(predicted_eb)",
        "file_size_bytes": geojson_path.stat().st_size,
        "count_by_family": _summary_counts(gdf, "family"),
        "count_by_road_classification": _summary_counts(gdf, "road_classification"),
        "count_by_road_archetype": _summary_counts(gdf, "road_archetype"),
        "numeric_summary": _numeric_summary(
            gdf, ["estimated_aadt", "collision_count", "predicted_eb"]
        ),
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        f.write("\n")

    if quarto_resource_dir is not None:
        quarto_resource_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(geojson_path, quarto_resource_dir / geojson_path.name)
        shutil.copy2(metadata_path, quarto_resource_dir / metadata_path.name)

    logger.info(
        "Wrote %s (%s bytes) and %s",
        geojson_path.relative_to(_ROOT),
        f"{geojson_path.stat().st_size:,}",
        metadata_path.relative_to(_ROOT),
    )
    return metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--geojson", type=Path, default=DEFAULT_GEOJSON)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--simplify-tolerance-m", type=float, default=25.0)
    parser.add_argument(
        "--no-quarto-resource-copy",
        action="store_true",
        help="Do not mirror web files into quarto/data/outputs/web for site publishing.",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    args = parse_args()
    build_web_geojson(
        input_path=args.input,
        geojson_path=args.geojson,
        metadata_path=args.metadata,
        simplify_tolerance_m=args.simplify_tolerance_m,
        quarto_resource_dir=None if args.no_quarto_resource_copy else DEFAULT_QUARTO_RESOURCE_DIR,
    )


if __name__ == "__main__":
    main()
