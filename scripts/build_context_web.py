"""Build static family-filtered road context layers for the Quarto top-risk map."""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely

from road_risk.config import _ROOT

logger = logging.getLogger(__name__)

OPENROADS_PATH = _ROOT / "data/processed/shapefiles/openroads.parquet"
NETWORK_FEATURES_PATH = _ROOT / "data/features/network_features.parquet"
RISK_SCORES_EB_PATH = _ROOT / "data/models/risk_scores_eb.parquet"
RISK_SCORES_PATH = _ROOT / "data/models/risk_scores.parquet"
DEFAULT_OUTPUT_DIR = _ROOT / "data/outputs/web/context"
DEFAULT_QUARTO_RESOURCE_DIR = _ROOT / "quarto/data/outputs/web/context"
MANIFEST_NAME = "context_manifest.json"
SIZE_WARNING_BYTES = 30 * 1024 * 1024

OPENROADS_COLUMNS = [
    "link_id",
    "road_classification",
    "road_function",
    "is_trunk",
    "geometry",
]
NETWORK_COLUMNS = ["link_id", "ruc_urban_rural"]
RISK_COLUMNS = ["link_id", "risk_percentile_eb"]
OUTPUT_COLUMNS = ["family", "road_function", "road_classification", "geometry"]

FAMILIES = ["motorway", "trunk_a", "other_urban", "other_rural"]
FAMILY_TOLERANCE_M = {
    "motorway": 15.0,
    "trunk_a": 15.0,
    "other_urban": 30.0,
    "other_rural": 40.0,
}


def _clean_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for pattern in ("*.geojson", "*.json"):
        for stale in path.glob(pattern):
            stale.unlink()


def _choose_risk_path() -> Path:
    if RISK_SCORES_EB_PATH.exists():
        return RISK_SCORES_EB_PATH
    if RISK_SCORES_PATH.exists():
        return RISK_SCORES_PATH
    raise FileNotFoundError(
        "No risk score file found. Tried "
        f"{RISK_SCORES_EB_PATH.relative_to(_ROOT)} and "
        f"{RISK_SCORES_PATH.relative_to(_ROOT)}"
    )


def _derive_family(df: pd.DataFrame) -> pd.Series:
    road_function = df["road_function"].fillna("")
    ruc = df["ruc_urban_rural"].fillna("")
    is_trunk = df["is_trunk"].fillna(False).astype(bool)
    conditions = [
        road_function.eq("Motorway"),
        road_function.eq("A Road") & is_trunk,
        ruc.eq("Urban"),
        ruc.eq("Rural"),
    ]
    choices = ["motorway", "trunk_a", "other_urban", "other_rural"]
    return pd.Series(np.select(conditions, choices, default="other_unknown"), index=df.index)


def _tile_index(gdf: gpd.GeoDataFrame, grid_size: int) -> pd.Series:
    projected = gdf.to_crs("EPSG:3857")
    minx, miny, maxx, maxy = projected.total_bounds
    width = max(maxx - minx, 1e-9)
    height = max(maxy - miny, 1e-9)
    centroids = projected.geometry.centroid
    x_index = ((centroids.x - minx) / width * grid_size).clip(0, grid_size - 1).astype(int)
    y_index = ((centroids.y - miny) / height * grid_size).clip(0, grid_size - 1).astype(int)
    return y_index * grid_size + x_index


def _simplify_family(gdf: gpd.GeoDataFrame, tolerance_m: float) -> gpd.GeoDataFrame:
    if gdf.empty:
        return gdf
    simplified = gdf.to_crs("EPSG:3857")
    simplified["geometry"] = simplified.geometry.simplify(tolerance_m, preserve_topology=True)
    simplified = simplified[~simplified.geometry.isna()].copy()
    simplified = simplified[~simplified.geometry.is_empty].copy()
    simplified = simplified.to_crs("EPSG:4326")
    simplified["geometry"] = shapely.set_precision(simplified.geometry.array, grid_size=0.00001)
    simplified = simplified[~simplified.geometry.isna()].copy()
    simplified = simplified[~simplified.geometry.is_empty].copy()
    return simplified


def _write_geojson(gdf: gpd.GeoDataFrame, path: Path) -> dict[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    gdf[OUTPUT_COLUMNS].to_file(path, driver="GeoJSON")
    return {"row_count": int(len(gdf)), "file_size_bytes": int(path.stat().st_size)}


def _write_tiled_family(
    gdf: gpd.GeoDataFrame,
    output_dir: Path,
    family: str,
    max_file_size_bytes: int,
) -> list[dict[str, Any]]:
    last_records: list[dict[str, Any]] = []
    last_paths: list[Path] = []

    for grid_size in range(2, 5):
        for path in last_paths:
            path.unlink(missing_ok=True)
        last_records = []
        last_paths = []

        tile_values = _tile_index(gdf, grid_size)
        logger.info("Splitting %s into %sx%s context tiles", family, grid_size, grid_size)

        for tile in sorted(tile_values.unique()):
            tile_gdf = gdf.loc[tile_values == tile]
            if tile_gdf.empty:
                continue
            filename = f"context_{family}_tile_{int(tile)}.geojson"
            path = output_dir / filename
            stats = _write_geojson(tile_gdf, path)
            last_records.append(
                {
                    "filename": filename,
                    "family": family,
                    "tile": int(tile),
                    **stats,
                }
            )
            last_paths.append(path)

        oversized = [
            record
            for record in last_records
            if int(record["file_size_bytes"]) > max_file_size_bytes
        ]
        if not oversized:
            return last_records

    logger.warning(
        "%s still has %s context tile(s) over %.2f MB after 4x4 split",
        family,
        len(
            [
                record
                for record in last_records
                if int(record["file_size_bytes"]) > max_file_size_bytes
            ]
        ),
        max_file_size_bytes / 1024 / 1024,
    )
    return last_records


def _write_family_or_tiles(
    gdf: gpd.GeoDataFrame,
    output_dir: Path,
    family: str,
    max_file_size_bytes: int,
) -> list[dict[str, Any]]:
    filename = f"context_{family}.geojson"
    path = output_dir / filename
    stats = _write_geojson(gdf, path)
    logger.info(
        "Wrote %s: %s rows, %.2f MB",
        filename,
        f"{stats['row_count']:,}",
        stats["file_size_bytes"] / 1024 / 1024,
    )

    if stats["file_size_bytes"] <= max_file_size_bytes:
        return [{"filename": filename, "family": family, "tile": None, **stats}]

    logger.info(
        "%s exceeds max size %.2f MB; replacing with spatial tiles",
        filename,
        max_file_size_bytes / 1024 / 1024,
    )
    path.unlink()
    return _write_tiled_family(gdf, output_dir, family, max_file_size_bytes)


def _mirror_to_quarto(output_dir: Path, quarto_resource_dir: Path) -> None:
    _clean_dir(quarto_resource_dir)
    for path in sorted(output_dir.glob("*.geojson")):
        shutil.copy2(path, quarto_resource_dir / path.name)
    shutil.copy2(output_dir / MANIFEST_NAME, quarto_resource_dir / MANIFEST_NAME)


def _family_stats(total: int, kept: int) -> dict[str, int | float]:
    return {
        "total_links": int(total),
        "kept_links": int(kept),
        "pct_kept": round((kept / total * 100) if total else 0.0, 3),
    }


def build_context_web(
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    other_percentile: float = 15.0,
    max_file_size_mb: float = 5.0,
    quarto_resource_dir: Path | None = DEFAULT_QUARTO_RESOURCE_DIR,
) -> dict[str, Any]:
    _clean_dir(output_dir)
    max_file_size_bytes = int(max_file_size_mb * 1024 * 1024)
    other_cutoff = 100.0 - other_percentile

    logger.info("Loading Open Roads from %s", OPENROADS_PATH.relative_to(_ROOT))
    gdf = gpd.read_parquet(OPENROADS_PATH, columns=OPENROADS_COLUMNS)
    logger.info("Loaded %s Open Roads links", f"{len(gdf):,}")

    logger.info("Loading network features from %s", NETWORK_FEATURES_PATH.relative_to(_ROOT))
    network = pd.read_parquet(NETWORK_FEATURES_PATH, columns=NETWORK_COLUMNS)

    risk_path = _choose_risk_path()
    logger.info("Loading risk scores from %s", risk_path.relative_to(_ROOT))
    risk = pd.read_parquet(risk_path, columns=RISK_COLUMNS)

    gdf = gdf.merge(network, on="link_id", how="left")
    gdf = gdf.merge(risk, on="link_id", how="left")
    gdf["road_classification"] = gdf["road_classification"].fillna("Unknown").astype(str)
    gdf["road_function"] = gdf["road_function"].fillna("Unknown").astype(str)
    gdf = gdf[~gdf.geometry.isna()].copy()
    gdf = gdf[~gdf.geometry.is_empty].copy()
    gdf["family"] = _derive_family(gdf)

    family_totals = gdf["family"].value_counts().to_dict()
    keep_masks = {
        "motorway": gdf["family"].eq("motorway"),
        "trunk_a": gdf["family"].eq("trunk_a"),
        "other_urban": gdf["family"].eq("other_urban")
        & gdf["risk_percentile_eb"].notna()
        & gdf["risk_percentile_eb"].ge(other_cutoff),
        "other_rural": gdf["family"].eq("other_rural")
        & gdf["risk_percentile_eb"].notna()
        & gdf["risk_percentile_eb"].ge(other_cutoff),
    }

    files: list[dict[str, Any]] = []
    families: dict[str, dict[str, int | float]] = {}

    for family in FAMILIES:
        total = int(family_totals.get(family, 0))
        family_gdf = gdf.loc[keep_masks[family], OUTPUT_COLUMNS].copy()
        kept = len(family_gdf)
        families[family] = _family_stats(total, kept)
        logger.info(
            "%s: kept %s / %s links (%.3f%%)",
            family,
            f"{kept:,}",
            f"{total:,}",
            families[family]["pct_kept"],
        )

        if family_gdf.empty:
            continue

        tolerance = FAMILY_TOLERANCE_M[family]
        logger.info("Simplifying %s with %.1f m tolerance", family, tolerance)
        family_gdf = _simplify_family(family_gdf, tolerance)
        files.extend(_write_family_or_tiles(family_gdf, output_dir, family, max_file_size_bytes))

    total_file_size_bytes = int(sum(record["file_size_bytes"] for record in files))
    manifest = {
        "created_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "simplification_tolerance_m": FAMILY_TOLERANCE_M,
        "coordinate_precision_degrees": 0.00001,
        "other_percentile": float(other_percentile),
        "families": families,
        "total_features": int(sum(record["row_count"] for record in files)),
        "total_file_size_bytes": total_file_size_bytes,
        "files": files,
    }

    with open(output_dir / MANIFEST_NAME, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    if quarto_resource_dir is not None:
        _mirror_to_quarto(output_dir, quarto_resource_dir)

    for family in FAMILIES:
        family_files = [record for record in files if record["family"] == family]
        family_size = sum(record["file_size_bytes"] for record in family_files)
        stats = families[family]
        logger.info(
            "%s summary: kept %s / %s links, files=%s, size=%.2f MB",
            family,
            f"{stats['kept_links']:,}",
            f"{stats['total_links']:,}",
            len(family_files),
            family_size / 1024 / 1024,
        )

    logger.info(
        "Grand total: files=%s, features=%s, size=%.2f MB",
        len(files),
        f"{manifest['total_features']:,}",
        total_file_size_bytes / 1024 / 1024,
    )
    if total_file_size_bytes > SIZE_WARNING_BYTES:
        logger.warning(
            "Context output size %.2f MB exceeds 30.00 MB target",
            total_file_size_bytes / 1024 / 1024,
        )

    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--simplify-tolerance-m",
        type=float,
        default=None,
        help="Ignored; context simplification uses hardcoded per-family tolerances.",
    )
    parser.add_argument("--other-percentile", type=float, default=15.0)
    parser.add_argument("--max-file-size-mb", type=float, default=5.0)
    parser.add_argument("--no-quarto-resource-copy", action="store_true")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    args = parse_args()
    if args.simplify_tolerance_m is not None:
        logger.info("--simplify-tolerance-m is ignored; using per-family tolerances")
    build_context_web(
        output_dir=args.output_dir,
        other_percentile=args.other_percentile,
        max_file_size_mb=args.max_file_size_mb,
        quarto_resource_dir=None if args.no_quarto_resource_copy else DEFAULT_QUARTO_RESOURCE_DIR,
    )


if __name__ == "__main__":
    main()
