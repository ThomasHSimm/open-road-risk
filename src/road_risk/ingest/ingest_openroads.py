"""
ingest_openroads.py
-------------------
Loader for OS Open Roads GeoPackage.

Source:
  https://osdatahub.os.uk/downloads/open/OpenRoads
  File: oproad_gb.gpkg
  Layers: road_link (LineString), road_node (Point), motorway_junction (Point)

OS Open Roads covers ALL classified roads in GB — motorways, A roads, B roads,
minor roads and unclassified roads. Unlike MRDB (major roads only), this gives
full coverage for snapping STATS19 collisions regardless of road type.

Key columns in road_link layer:
  id                        : unique TOID identifier
  road_classification       : Motorway / A Road / B Road / Minor Road / Local Road
  road_function             : A Road / B Road / Minor Road / Local Street etc.
  form_of_way               : Single Carriageway / Dual Carriageway / Slip Road etc.
  road_classification_number: numeric part of road name (e.g. '62' for M62)
  name_1                    : full road name where available (e.g. 'M62', 'A64')
  length                    : link length in metres (CRS is BNG metres)
  trunk_road                : boolean — National Highways trunk road
  primary_route             : boolean — primary route network
  start_node / end_node     : node TOIDs for network analysis

Coordinate system:
  Raw: EPSG:27700 (British National Grid)
  Output: EPSG:4326 (WGS84) to match STATS19 and AADF

GB ingest strategy:
  Read source rows in small chunks and reproject each chunk. OS Open Roads is
  already a GB source, so this ingest does not apply a study-area polygon clip.
"""

import logging
import math
from pathlib import Path

import geopandas as gpd
import pandas as pd

from road_risk.config import _ROOT, cfg
from road_risk.geography import STUDY_AREA_BBOX_BNG

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_DEFAULT_RAW_FOLDER = _ROOT / cfg["paths"]["raw"]["shapefiles"]
_DEFAULT_OUTPUT_FOLDER = _ROOT / cfg["paths"]["processed"] / "shapefiles"

TARGET_CRS = "EPSG:4326"
SOURCE_CRS = "EPSG:27700"
CHUNK_SIZE = 10_000
EXPECTED_GB_ROWS = 3_941_299
ROW_TOLERANCE_FRACTION = 0.01

YORKSHIRE_BBOX_BNG = STUDY_AREA_BBOX_BNG  # backwards-compat alias

# Columns to keep
KEEP_COLS = [
    "id",
    "road_classification",
    "road_function",
    "form_of_way",
    "road_classification_number",
    "name_1",
    "length",
    "trunk_road",
    "primary_route",
    "start_node",
    "end_node",
    "geometry",
]

# Map OS road_classification → short prefix for road_name_clean
CLASSIFICATION_PREFIX = {
    "Motorway": "M",
    "A Road": "A",
    "B Road": "B",
    "Minor Road": "",
    "Local Road": "",
    "Local Street": "",
    "Unknown": "",
}

COL_RENAMES = {
    "id": "link_id",
    "road_classification": "road_classification",
    "road_function": "road_function",
    "form_of_way": "form_of_way",
    "road_classification_number": "road_number",
    "name_1": "road_name",
    "length": "link_length_m",
    "trunk_road": "is_trunk",
    "primary_route": "is_primary",
    "start_node": "start_node",
    "end_node": "end_node",
}

OUTPUT_COLUMNS = [
    "link_id",
    "road_classification",
    "road_function",
    "form_of_way",
    "road_number",
    "road_name",
    "link_length_m",
    "is_trunk",
    "is_primary",
    "start_node",
    "end_node",
    "geometry",
    "link_length_km",
    "road_name_clean",
    "street_name_clean",
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _find_gpkg(folder: Path) -> Path:
    """Find the OS Open Roads GeoPackage in the given folder."""
    # Try known filename first
    for name in ["oproad_gb.gpkg", "oproads_gb.gpkg", "OpenRoads_gpkg.gpkg"]:
        p = folder / name
        if p.exists():
            return p

    # Glob fallback
    matches = sorted(folder.glob("*.gpkg"))
    if matches:
        # Prefer one that isn't MRDB
        non_mrdb = [m for m in matches if "mrdb" not in m.name.lower()]
        if non_mrdb:
            logger.debug(f"Found GeoPackage: {non_mrdb[0].name}")
            return non_mrdb[0]
        return matches[0]

    raise FileNotFoundError(
        f"No OS Open Roads GeoPackage found in {folder}\n"
        f"Download from https://osdatahub.os.uk/downloads/open/OpenRoads "
        f"and place oproad_gb.gpkg in {folder}"
    )


def _build_road_name_clean(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Build road_name_clean for joining to STATS19 road_name_clean.

    Priority:
      1. name_1 / road_name if it looks like a road number (M62, A64, B1234)
      2. Reconstruct from road_classification + road_number
      3. Empty string for unnamed/unclassified roads
    """
    # --- road_name_clean: use road_number directly (already contains prefix) -
    # road_number contains full designation e.g. 'A64', 'M62', 'B1234'
    # road_classification prefix must NOT be prepended — it would double it.
    number = (
        gdf["road_number"]
        .fillna("")
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.strip()
        .str.upper()
    )
    number = number.replace({"0": "", "NAN": "", "NONE": ""})
    gdf["road_name_clean"] = number

    n_numbered = (gdf["road_name_clean"] != "").sum()
    logger.info(
        f"  road_name_clean (M/A/B number): {n_numbered:,} / {len(gdf):,} links "
        f"({n_numbered / len(gdf):.1%})"
    )

    # --- street_name_clean: normalised name_1 (Dale Close → DALECLOSE) ------
    # Used for AADF → OpenRoads name matching where road_name in AADF is a
    # street name rather than a road number.
    if "road_name" in gdf.columns:
        gdf["street_name_clean"] = (
            gdf["road_name"]
            .fillna("")
            .str.upper()
            .str.replace(r"[^A-Z0-9]", "", regex=True)
            .str.strip()
        )
    else:
        gdf["street_name_clean"] = ""

    n_street = (gdf["street_name_clean"] != "").sum()
    logger.info(
        f"  street_name_clean (named streets): {n_street:,} / {len(gdf):,} links "
        f"({n_street / len(gdf):.1%})"
    )
    return gdf


def _finite_bounds(bounds) -> bool:
    return len(bounds) == 4 and all(math.isfinite(float(value)) for value in bounds)


def _crs_is(gdf: gpd.GeoDataFrame, expected_crs: str) -> bool:
    if gdf.crs is None:
        return False
    expected = expected_crs.upper()
    if str(gdf.crs).upper() == expected:
        return True
    epsg = gdf.crs.to_epsg() if hasattr(gdf.crs, "to_epsg") else None
    return expected == f"EPSG:{epsg}"


def _format_bounds(gdf: gpd.GeoDataFrame) -> list[float]:
    return [round(float(value), 6) for value in gdf.total_bounds]


def _fail_chunk(chunk: gpd.GeoDataFrame, start: int, end: int, reason: str) -> None:
    message = (
        f"Open Roads chunk rows {start:,}-{end:,} failed validation: {reason}. "
        f"rows={len(chunk):,}, crs={chunk.crs}, bounds={chunk.total_bounds.tolist()}, "
        f"geom_types={chunk.geometry.geom_type.value_counts(dropna=False).to_dict()}"
    )
    if "id" in chunk.columns:
        message += f", first_ids={chunk['id'].head(10).astype(str).tolist()}"
    raise ValueError(message)


def _validate_raw_chunk(chunk: gpd.GeoDataFrame, start: int, end: int) -> None:
    if chunk.empty:
        _fail_chunk(chunk, start, end, "chunk is empty")
    if not _crs_is(chunk, SOURCE_CRS):
        _fail_chunk(chunk, start, end, f"expected CRS {SOURCE_CRS}")
    if chunk.geometry.isna().any():
        _fail_chunk(chunk, start, end, "null geometries present")
    if chunk.geometry.is_empty.any():
        _fail_chunk(chunk, start, end, "empty geometries present")
    geom_types = set(chunk.geometry.geom_type.unique())
    if geom_types != {"LineString"}:
        _fail_chunk(chunk, start, end, f"expected only LineString geometries, got {geom_types}")
    if not _finite_bounds(chunk.total_bounds):
        _fail_chunk(chunk, start, end, "raw bounds are not finite")


def _read_total_rows(gpkg_path: Path, layer: str) -> int:
    rows = gpd.read_file(gpkg_path, layer=layer, columns=["id"], ignore_geometry=True)
    return len(rows)


def _normalise_openroads_chunk(chunk: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    cols_present = [c for c in KEEP_COLS if c in chunk.columns]
    out = chunk[cols_present].copy()

    out = out.rename(columns={k: v for k, v in COL_RENAMES.items() if k in out.columns})

    if "link_length_m" in out.columns:
        out["link_length_km"] = out["link_length_m"] / 1000

    for col in ["road_name", "road_classification", "road_function", "form_of_way"]:
        if col in out.columns:
            out[col] = out[col].fillna("").astype(str).str.strip()

    if "road_number" in out.columns:
        out["road_number"] = (
            out["road_number"]
            .fillna("")
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.strip()
        )

    out = _build_road_name_clean(out)
    return out[OUTPUT_COLUMNS]


def _read_openroads_chunked(
    gpkg_path: Path,
    target_crs: str,
    layer: str,
    chunk_size: int = CHUNK_SIZE,
) -> gpd.GeoDataFrame:
    total_rows = _read_total_rows(gpkg_path, layer)
    logger.info("  Source road_link rows: %s", f"{total_rows:,}")
    logger.info("  Reading and reprojecting in %s-row chunks", f"{chunk_size:,}")

    chunks: list[gpd.GeoDataFrame] = []
    for start in range(0, total_rows, chunk_size):
        end = min(start + chunk_size, total_rows)
        if start == 0 or start % 100_000 == 0 or end == total_rows:
            logger.info("  Processing Open Roads rows %s-%s", f"{start:,}", f"{end:,}")

        chunk = gpd.read_file(gpkg_path, layer=layer, rows=slice(start, end))
        _validate_raw_chunk(chunk, start, end)

        chunk = chunk.to_crs(target_crs)
        if not _finite_bounds(chunk.total_bounds):
            _fail_chunk(chunk, start, end, "WGS84 bounds are not finite")

        chunks.append(_normalise_openroads_chunk(chunk))

    gdf = gpd.GeoDataFrame(
        pd.concat(chunks, ignore_index=True),
        geometry="geometry",
        crs=target_crs,
    )
    logger.info("  Chunked Open Roads ingest assembled %s links", f"{len(gdf):,}")
    return gdf


def validate_openroads_gb(gdf: gpd.GeoDataFrame) -> None:
    if gdf.empty:
        raise ValueError("Open Roads ingest produced zero links.")

    min_expected = int(EXPECTED_GB_ROWS * (1 - ROW_TOLERANCE_FRACTION))
    max_expected = int(EXPECTED_GB_ROWS * (1 + ROW_TOLERANCE_FRACTION))
    if not min_expected <= len(gdf) <= max_expected:
        raise ValueError(
            "Open Roads row count is outside expected GB range: "
            f"{len(gdf):,} not in [{min_expected:,}, {max_expected:,}]"
        )

    if not _crs_is(gdf, TARGET_CRS):
        raise ValueError(f"Open Roads output CRS is {gdf.crs}; expected {TARGET_CRS}.")

    if not _finite_bounds(gdf.total_bounds):
        raise ValueError(f"Open Roads output bounds are not finite: {gdf.total_bounds.tolist()}")

    min_lon, min_lat, max_lon, max_lat = [float(value) for value in gdf.total_bounds]
    if min_lat > 50.5 or max_lat < 60.0 or min_lon > -5.0 or max_lon < 1.0:
        raise ValueError(f"Open Roads output does not look GB-wide: bounds={_format_bounds(gdf)}")

    geom_counts = gdf.geometry.geom_type.value_counts(dropna=False).to_dict()
    if set(geom_counts) != {"LineString"}:
        raise ValueError(f"Open Roads output contains non-LineString geometries: {geom_counts}")

    null_count = int(gdf.geometry.isna().sum())
    empty_count = int(gdf.geometry.is_empty.sum())
    invalid_count = int((~gdf.geometry.is_valid).sum())
    if null_count or empty_count or invalid_count:
        raise ValueError(
            "Open Roads output geometry validation failed: "
            f"null={null_count}, empty={empty_count}, invalid={invalid_count}"
        )

    if "link_id" not in gdf.columns:
        raise ValueError("Open Roads output is missing link_id.")
    unique_links = int(gdf["link_id"].nunique())
    if unique_links != len(gdf):
        raise ValueError(
            f"Open Roads link_id values are not unique: {unique_links:,} unique / {len(gdf):,} rows"
        )

    logger.info(
        "  Validated Open Roads GB output: rows=%s bounds=%s unique_link_id=%s",
        f"{len(gdf):,}",
        _format_bounds(gdf),
        f"{unique_links:,}",
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_openroads(
    raw_folder: str | Path = _DEFAULT_RAW_FOLDER,
    bbox_bng: tuple = STUDY_AREA_BBOX_BNG,
    target_crs: str = TARGET_CRS,
    layer: str = "road_link",
) -> gpd.GeoDataFrame:
    """
    Load OS Open Roads road_link layer, filter to the study area, reproject to WGS84.

    Parameters
    ----------
    raw_folder : folder containing oproad_gb.gpkg
    bbox_bng   : (minx, miny, maxx, maxy) in BNG metres for spatial filter.
                 Retained for backwards-compatible function signature; GB
                 Open Roads ingest reads source row chunks instead.
    target_crs : output CRS, defaults to EPSG:4326 (WGS84)
    layer      : GeoPackage layer name, defaults to 'road_link'

    Returns
    -------
    GeoDataFrame with normalised columns and WGS84 geometry.

    Example
    -------
    >>> gdf = load_openroads()
    >>> gdf["road_classification"].value_counts()
    """
    folder = Path(raw_folder)
    gpkg_path = _find_gpkg(folder)
    logger.info(f"Loading OS Open Roads from {gpkg_path.name} (layer='{layer}') ...")

    gdf = _read_openroads_chunked(gpkg_path, target_crs, layer)
    gdf = gdf.reset_index(drop=True)
    validate_openroads_gb(gdf)

    logger.info(
        f"OS Open Roads loaded: {len(gdf):,} links | "
        f"road types:\n{gdf['road_classification'].value_counts().to_string()}"
    )
    return gdf


def save_openroads(
    gdf: gpd.GeoDataFrame,
    output_folder: str | Path = _DEFAULT_OUTPUT_FOLDER,
) -> None:
    """Save OS Open Roads GeoDataFrame to GeoParquet."""
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    out_path = output_folder / "openroads.parquet"
    tmp_path = output_folder / "openroads.tmp.parquet"

    validate_openroads_gb(gdf)
    gdf.to_parquet(tmp_path, index=False)
    readback = gpd.read_parquet(tmp_path)
    validate_openroads_gb(readback)
    tmp_path.replace(out_path)

    size_mb = out_path.stat().st_size / 1024 / 1024
    logger.info(
        "Saved OS Open Roads to %s (%s links, %.1f MB)",
        out_path,
        f"{len(gdf):,}",
        size_mb,
    )


def main(
    raw_folder: str | Path = None,
    output_folder: str | Path = None,
) -> gpd.GeoDataFrame:
    """Load, filter, and save OS Open Roads for the study area."""
    if raw_folder is None:
        raw_folder = _DEFAULT_RAW_FOLDER
    if output_folder is None:
        output_folder = _DEFAULT_OUTPUT_FOLDER

    gdf = load_openroads(raw_folder)

    print("\n=== OS Open Roads summary ===")
    print(f"  Road links : {len(gdf):,}")
    print(f"  CRS        : {gdf.crs}")
    print(f"  Columns    : {gdf.columns.tolist()}")
    print(f"\n  Road classification:\n{gdf['road_classification'].value_counts().to_string()}")
    if "form_of_way" in gdf.columns:
        print(f"\n  Form of way:\n{gdf['form_of_way'].value_counts().to_string()}")
    n_named = (gdf["road_name_clean"] != "").sum()
    print(f"\n  Named roads: {n_named:,} / {len(gdf):,} ({n_named / len(gdf):.1%})")

    save_openroads(gdf, output_folder)
    return gdf


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    main()
