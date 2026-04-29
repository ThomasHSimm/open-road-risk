"""
Grade features from OS Terrain 50.

This module samples the OS Terrain 50 ASCII-grid DTM along OS Open Roads links
and merges link-level grade features into ``data/features/network_features.parquet``.

Methodology:

- Terrain source: OS Terrain 50 grid tiles, not contour data. The local source
  is expected under ``data/raw/terr50/data/**/**_OST50GRID_*.zip``. Each zip
  contains one 10 km x 10 km ASCII grid tile at 50 m cell size.
- Sampling: road links are resampled every 15 m to align with the curvature
  pipeline. Elevation is sampled with bilinear interpolation from the 50 m DTM.
- Grade support: slope is calculated over a 45 m baseline, approximately one
  Terrain 50 cell, rather than raw 15 m adjacent differences.
- Units: ``mean_grade`` and ``max_grade`` are absolute percent grade;
  ``grade_change`` is metres of absolute sampled elevation change along the link.
- Structures: OSM bridge/tunnel/covered tags, when available, trigger an
  endpoint fallback because Terrain 50 is a bare-earth DTM and does not reliably
  represent bridge decks or tunnel carriageways.
- Confidence: grades above 25% are retained but flagged as low confidence.

The features are broad, link-scale vertical geometry signals. They should not be
read as engineering-grade crest/sag or carriageway profile measurements.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from zipfile import ZipFile

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge, transform
from tqdm import tqdm

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from road_risk.config import _ROOT  # noqa: E402

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

TERRAIN_ROOT = _ROOT / "data/raw/terr50"
TERRAIN_DATA_DIR = TERRAIN_ROOT / "data"
OUTPUT_PATH = _ROOT / "data/features/network_features.parquet"
SUMMARY_DIR = _ROOT / "data/features"

POINT_CACHE_CANDIDATES = [
    _ROOT / "data/processed/link_resampled_points.parquet",
    Path("link_resampled_points.parquet"),
]

NETWORK_CANDIDATES = [
    _ROOT / "data/processed/shapefiles/openroads.parquet",
    _ROOT / "data/processed/current_network.parquet",
    Path("openroads.parquet"),
    Path("current_network.parquet"),
]

OSM_STRUCTURE_CANDIDATES = [
    _ROOT / "data/external/osm_bridges_tunnels.parquet",
    Path("osm_bridges_tunnels.parquet"),
]

# Keep the same point spacing as curvature.
POINT_SPACING_M = 15.0

# Compute grade over ~1 Terrain 50 cell, not over raw 15 m steps.
GRADE_BASELINE_M = 45.0

LOW_CONFIDENCE_MAX_GRADE_PCT = 25.0
TERRAIN_TILE_SIZE_M = 10_000

LINK_ID_CANDIDATES = ["link_id", "road_link_id", "roadlink_id", "identifier", "id"]
POINT_SEQ_CANDIDATES = ["point_sequence", "sequence", "seq", "point_idx", "sample_idx"]
POINT_DIST_CANDIDATES = ["distance_m", "distance", "chainage_m", "dist_m"]
ROAD_CLASS_CANDIDATES = ["road_classification", "roadclassification"]

GRADE_COLUMNS = [
    "mean_grade",
    "max_grade",
    "grade_change",
    "is_bridge_proxy",
    "is_tunnel_proxy",
    "is_covered_proxy",
    "grade_method",
    "grade_low_confidence",
    "valid_elev_points",
    "valid_grade_segments",
]

WGS84_PROJ = "+proj=longlat +datum=WGS84 +no_defs"
OSGB36_TM_PROJ = (
    "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 "
    "+x_0=400000 +y_0=-100000 +ellps=airy +units=m +no_defs"
)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def load_geodf(path: Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_parquet(path)
    if not isinstance(gdf, gpd.GeoDataFrame):
        if "geometry" not in gdf.columns:
            raise ValueError(f"{path} does not contain a geometry column.")
        gdf = gpd.GeoDataFrame(gdf, geometry="geometry")
    return gdf


def find_existing_path(candidates: list[Path]) -> Path:
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"None of these files exist: {candidates}")


def infer_column(columns, candidates):
    colset = set(columns)
    for col in candidates:
        if col in colset:
            return col
    return None


def normalise_line(geom):
    if geom is None or geom.is_empty:
        return None
    if isinstance(geom, LineString):
        return geom
    if isinstance(geom, MultiLineString):
        merged = linemerge(geom)
        if isinstance(merged, LineString):
            return merged
        if hasattr(merged, "geoms") and len(merged.geoms) > 0:
            return max(merged.geoms, key=lambda g: g.length)
    return None


def ensure_bng(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.crs is None:
        raise ValueError("CRS missing. Expected a projected CRS in metres.")
    epsg = gdf.crs.to_epsg()
    if epsg == 27700:
        return gdf

    transformer = Transformer.from_crs(gdf.crs, "EPSG:27700", always_xy=True)
    minx, miny, maxx, maxy = gdf.total_bounds
    test_x, test_y = transformer.transform((minx + maxx) / 2, (miny + maxy) / 2)
    if not np.isfinite(test_x) or not np.isfinite(test_y):
        print(
            "EPSG:27700 transform returned non-finite coordinates; "
            "using explicit British National Grid projection fallback."
        )
        transformer = Transformer.from_crs(WGS84_PROJ, OSGB36_TM_PROJ, always_xy=True)

    projected = gdf.copy()
    projected["geometry"] = projected.geometry.apply(
        lambda geom: None if geom is None else transform(transformer.transform, geom)
    )
    return projected.set_crs("EPSG:27700", allow_override=True)


def terrain_zip_paths() -> list[Path]:
    if not TERRAIN_DATA_DIR.exists():
        raise FileNotFoundError(f"Terrain 50 data directory not found: {TERRAIN_DATA_DIR}")
    paths = sorted(TERRAIN_DATA_DIR.glob("*/*_OST50GRID_*.zip"))
    if not paths:
        raise FileNotFoundError(f"No Terrain 50 zip tiles found under {TERRAIN_DATA_DIR}")
    return paths


def asc_url_from_zip(zip_path: Path) -> str:
    with ZipFile(zip_path) as zf:
        asc_names = [name for name in zf.namelist() if name.lower().endswith(".asc")]
    if len(asc_names) != 1:
        raise ValueError(f"Expected exactly one .asc in {zip_path}, found {asc_names}")
    return f"/vsizip/{zip_path.resolve()}/{asc_names[0]}"


def build_terrain_tile_index(tile_paths: list[Path]) -> pd.DataFrame:
    rows = []
    for path in tqdm(tile_paths, desc="Indexing Terrain 50 tiles", unit="tile"):
        url = asc_url_from_zip(path)
        with rasterio.open(url) as src:
            rows.append(
                {
                    "zip_path": str(path),
                    "asc_url": url,
                    "left": float(src.bounds.left),
                    "bottom": float(src.bounds.bottom),
                    "right": float(src.bounds.right),
                    "top": float(src.bounds.top),
                    "width": int(src.width),
                    "height": int(src.height),
                    "crs": str(src.crs),
                }
            )
    return pd.DataFrame(rows)


def build_points_from_network(network_gdf: gpd.GeoDataFrame, link_col: str) -> gpd.GeoDataFrame:
    rows = []
    cols = [link_col, "geometry"]

    for _, row in tqdm(
        network_gdf[cols].iterrows(),
        total=len(network_gdf),
        desc="Building 15 m road sample points",
        unit="link",
    ):
        link_id = row[link_col]
        geom = normalise_line(row.geometry)
        if geom is None:
            continue

        length_m = float(geom.length)
        if length_m <= 0:
            continue

        dists = np.arange(0.0, length_m, POINT_SPACING_M, dtype=float)
        if len(dists) == 0 or dists[0] != 0.0:
            dists = np.insert(dists, 0, 0.0)
        if not np.isclose(dists[-1], length_m):
            dists = np.append(dists, length_m)

        for seq, dist_m in enumerate(dists):
            rows.append(
                {
                    link_col: link_id,
                    "point_sequence": seq,
                    "distance_m": float(dist_m),
                    "geometry": geom.interpolate(float(dist_m)),
                }
            )

    return gpd.GeoDataFrame(rows, geometry="geometry", crs=network_gdf.crs)


def load_or_build_points(network_gdf: gpd.GeoDataFrame, link_col: str) -> gpd.GeoDataFrame:
    network_ids = set(network_gdf[link_col].dropna().unique())
    for path in POINT_CACHE_CANDIDATES:
        if path.exists():
            points = ensure_bng(load_geodf(path))
            point_link_col = infer_column(points.columns, [link_col] + LINK_ID_CANDIDATES)
            if point_link_col is None:
                raise KeyError("Could not infer link id column in point cache.")

            if point_link_col != link_col:
                points = points.rename(columns={point_link_col: link_col})

            points = points.loc[points[link_col].isin(network_ids)].copy()

            seq_col = infer_column(points.columns, POINT_SEQ_CANDIDATES)
            dist_col = infer_column(points.columns, POINT_DIST_CANDIDATES)

            if seq_col is None:
                points["point_sequence"] = points.groupby(link_col).cumcount()
            elif seq_col != "point_sequence":
                points = points.rename(columns={seq_col: "point_sequence"})

            if dist_col is None:
                points = points.sort_values([link_col, "point_sequence"]).copy()
                points["distance_m"] = points.groupby(link_col).cumcount() * POINT_SPACING_M
            elif dist_col != "distance_m":
                points = points.rename(columns={dist_col: "distance_m"})

            print(f"Loaded {len(points):,} cached road sample points from {path}")
            return points

    return build_points_from_network(network_gdf, link_col)


def bilinear_sample_band(
    src: rasterio.io.DatasetReader,
    xs: np.ndarray,
    ys: np.ndarray,
) -> np.ndarray:
    """
    Bilinear interpolation against a single Terrain 50 tile.

    The ASCII grid transform is edge-based; the heights represent pixel-centre
    values, so coordinates are shifted by half a cell before interpolation.
    """
    band = src.read(1, masked=True).astype("float32")
    transform_ = src.transform

    cols_edge = (xs - transform_.c) / transform_.a
    rows_edge = (ys - transform_.f) / transform_.e
    cols = cols_edge - 0.5
    rows = rows_edge - 0.5

    col0 = np.floor(cols).astype(int)
    row0 = np.floor(rows).astype(int)
    col1 = col0 + 1
    row1 = row0 + 1

    dr = rows - row0
    dc = cols - col0

    out = np.full(xs.shape[0], np.nan, dtype="float32")
    valid = (row0 >= 0) & (col0 >= 0) & (row1 < src.height) & (col1 < src.width)
    if not np.any(valid):
        return out

    r0 = row0[valid]
    r1 = row1[valid]
    c0 = col0[valid]
    c1 = col1[valid]

    z00 = band[r0, c0]
    z01 = band[r0, c1]
    z10 = band[r1, c0]
    z11 = band[r1, c1]

    interp_valid = ~(
        np.ma.getmaskarray(z00)
        | np.ma.getmaskarray(z01)
        | np.ma.getmaskarray(z10)
        | np.ma.getmaskarray(z11)
    )
    if not np.any(interp_valid):
        return out

    zv00 = np.asarray(z00[interp_valid], dtype="float32")
    zv01 = np.asarray(z01[interp_valid], dtype="float32")
    zv10 = np.asarray(z10[interp_valid], dtype="float32")
    zv11 = np.asarray(z11[interp_valid], dtype="float32")

    drv = dr[valid][interp_valid]
    dcv = dc[valid][interp_valid]
    z = (
        zv00 * (1 - drv) * (1 - dcv)
        + zv01 * (1 - drv) * dcv
        + zv10 * drv * (1 - dcv)
        + zv11 * drv * dcv
    )

    idx = np.flatnonzero(valid)[interp_valid]
    out[idx] = z
    return out


def sample_elevation_from_tiles(
    points: gpd.GeoDataFrame,
    tile_index: pd.DataFrame,
) -> np.ndarray:
    xs = points.geometry.x.to_numpy(dtype="float64")
    ys = points.geometry.y.to_numpy(dtype="float64")
    elevations = np.full(len(points), np.nan, dtype="float32")

    x_tile = (np.floor(xs / TERRAIN_TILE_SIZE_M) * TERRAIN_TILE_SIZE_M).astype("int64")
    y_tile = (np.floor(ys / TERRAIN_TILE_SIZE_M) * TERRAIN_TILE_SIZE_M).astype("int64")

    point_groups = (
        pd.DataFrame({"point_ix": np.arange(len(points)), "left": x_tile, "bottom": y_tile})
        .groupby(["left", "bottom"])["point_ix"]
        .apply(lambda s: s.to_numpy(dtype="int64"))
        .to_dict()
    )

    tile_lookup = {
        (int(row.left), int(row.bottom)): row for row in tile_index.itertuples(index=False)
    }

    missing_tile_points = 0
    for key, point_ix in tqdm(
        point_groups.items(),
        total=len(point_groups),
        desc="Sampling Terrain 50 tiles",
        unit="tile",
    ):
        tile = tile_lookup.get(key)
        if tile is None:
            missing_tile_points += len(point_ix)
            continue
        with rasterio.open(tile.asc_url) as src:
            elevations[point_ix] = bilinear_sample_band(src, xs[point_ix], ys[point_ix])

    if missing_tile_points:
        print(f"Terrain tile missing for {missing_tile_points:,} sample points.")
    return elevations


def load_structure_flags(network_gdf: gpd.GeoDataFrame, link_col: str) -> pd.DataFrame:
    path = next((candidate for candidate in OSM_STRUCTURE_CANDIDATES if candidate.exists()), None)

    if path is None:
        return pd.DataFrame(
            {
                link_col: network_gdf[link_col].values,
                "is_bridge_proxy": False,
                "is_tunnel_proxy": False,
                "is_covered_proxy": False,
            }
        ).drop_duplicates(subset=[link_col])

    osm = ensure_bng(load_geodf(path)).copy()
    for col in ["bridge", "tunnel", "covered"]:
        if col not in osm.columns:
            osm[col] = None

    def is_trueish(series: pd.Series) -> pd.Series:
        s = series.astype("string").str.lower()
        return s.notna() & ~s.isin(["no", "none", "false", "0", ""])

    osm["is_bridge_proxy"] = is_trueish(osm["bridge"])
    osm["is_tunnel_proxy"] = is_trueish(osm["tunnel"])
    osm["is_covered_proxy"] = is_trueish(osm["covered"])

    osm = osm.loc[
        osm["is_bridge_proxy"] | osm["is_tunnel_proxy"] | osm["is_covered_proxy"],
        ["geometry", "is_bridge_proxy", "is_tunnel_proxy", "is_covered_proxy"],
    ].copy()

    if osm.empty:
        return pd.DataFrame(
            {
                link_col: network_gdf[link_col].values,
                "is_bridge_proxy": False,
                "is_tunnel_proxy": False,
                "is_covered_proxy": False,
            }
        ).drop_duplicates(subset=[link_col])

    links = network_gdf[[link_col, "geometry"]].drop_duplicates(subset=[link_col]).copy()
    joined = gpd.sjoin(links, osm, how="left", predicate="intersects")

    return (
        joined.groupby(link_col)[["is_bridge_proxy", "is_tunnel_proxy", "is_covered_proxy"]]
        .max()
        .reset_index()
        .fillna(False)
    )


def compute_grade_features(points_gdf: gpd.GeoDataFrame, link_col: str) -> pd.DataFrame:
    points = points_gdf.sort_values([link_col, "point_sequence"]).copy()
    baseline_steps = max(1, int(round(GRADE_BASELINE_M / POINT_SPACING_M)))

    points["prev_elev"] = points.groupby(link_col)["elevation_m"].shift(1)
    points["adj_dz_abs_m"] = (points["elevation_m"] - points["prev_elev"]).abs()

    points["lead_elev"] = points.groupby(link_col)["elevation_m"].shift(-baseline_steps)
    points["lead_dist"] = points.groupby(link_col)["distance_m"].shift(-baseline_steps)
    points["segment_dz_m"] = points["lead_elev"] - points["elevation_m"]
    points["segment_dx_m"] = points["lead_dist"] - points["distance_m"]

    valid_grade = (
        points["elevation_m"].notna()
        & points["lead_elev"].notna()
        & points["segment_dx_m"].notna()
        & (points["segment_dx_m"] > 0)
    )

    points.loc[valid_grade, "grade_pct_abs"] = (
        points.loc[valid_grade, "segment_dz_m"].abs() / points.loc[valid_grade, "segment_dx_m"]
    ) * 100.0

    def summarise(group: pd.DataFrame) -> pd.Series:
        grade_rows = group.loc[group["grade_pct_abs"].notna()].copy()
        elev_rows = group.loc[group["elevation_m"].notna()].copy()

        if len(grade_rows) == 0:
            mean_grade = np.nan
            max_grade = np.nan
        else:
            mean_grade = np.average(
                grade_rows["grade_pct_abs"].to_numpy(),
                weights=grade_rows["segment_dx_m"].to_numpy(),
            )
            max_grade = float(grade_rows["grade_pct_abs"].max())

        if len(elev_rows) < 2:
            grade_change = np.nan
            start_elev = np.nan
            end_elev = np.nan
            link_length = np.nan
        else:
            grade_change = float(group["adj_dz_abs_m"].sum(skipna=True))
            start_elev = float(elev_rows["elevation_m"].iloc[0])
            end_elev = float(elev_rows["elevation_m"].iloc[-1])
            link_length = float(elev_rows["distance_m"].iloc[-1] - elev_rows["distance_m"].iloc[0])

        return pd.Series(
            {
                "mean_grade": mean_grade,
                "max_grade": max_grade,
                "grade_change": grade_change,
                "start_elev_m": start_elev,
                "end_elev_m": end_elev,
                "profile_length_m": link_length,
                "valid_elev_points": int(group["elevation_m"].notna().sum()),
                "valid_grade_segments": int(group["grade_pct_abs"].notna().sum()),
            }
        )

    return points.groupby(link_col).apply(summarise, include_groups=False).reset_index()


def apply_structure_fallback(features: pd.DataFrame) -> pd.DataFrame:
    out = features.copy()
    out["grade_method"] = "profile"

    structure_mask = (
        out["is_bridge_proxy"].fillna(False)
        | out["is_tunnel_proxy"].fillna(False)
        | out["is_covered_proxy"].fillna(False)
    )

    endpoint_ok = (
        out["profile_length_m"].notna()
        & (out["profile_length_m"] > 0)
        & out["start_elev_m"].notna()
        & out["end_elev_m"].notna()
    )

    fallback_mask = structure_mask & endpoint_ok
    endpoint_grade = (
        (out.loc[fallback_mask, "end_elev_m"] - out.loc[fallback_mask, "start_elev_m"]).abs()
        / out.loc[fallback_mask, "profile_length_m"]
    ) * 100.0
    endpoint_change = (
        out.loc[fallback_mask, "end_elev_m"] - out.loc[fallback_mask, "start_elev_m"]
    ).abs()

    out.loc[fallback_mask, "mean_grade"] = endpoint_grade
    out.loc[fallback_mask, "max_grade"] = endpoint_grade
    out.loc[fallback_mask, "grade_change"] = endpoint_change
    out.loc[fallback_mask, "grade_method"] = "endpoint_fallback"

    null_mask = structure_mask & ~endpoint_ok
    out.loc[null_mask, ["mean_grade", "max_grade", "grade_change"]] = np.nan
    out.loc[null_mask, "grade_method"] = "null_structure"

    return out


def merge_into_network_features(features: pd.DataFrame, link_col: str) -> pd.DataFrame:
    feature_cols = [link_col, *GRADE_COLUMNS]
    if OUTPUT_PATH.exists():
        existing = pd.read_parquet(OUTPUT_PATH)
        existing_link_col = infer_column(existing.columns, [link_col] + LINK_ID_CANDIDATES)
        if existing_link_col is None:
            raise KeyError(f"Could not infer link id column in {OUTPUT_PATH}")
        if existing[existing_link_col].duplicated().any():
            raise ValueError(f"Existing feature table has duplicate {existing_link_col} values.")
        if features[link_col].duplicated().any():
            raise ValueError(f"Terrain features have duplicate {link_col} values.")

        merged = existing.drop(columns=GRADE_COLUMNS, errors="ignore").merge(
            features[feature_cols],
            left_on=existing_link_col,
            right_on=link_col,
            how="left",
            validate="one_to_one",
        )
        if existing_link_col != link_col:
            merged = merged.drop(columns=[link_col])
        return merged

    return features[feature_cols].copy()


def print_report(out: pd.DataFrame, road_class_col: str | None = None) -> None:
    non_null = out["mean_grade"].notna().sum()
    total = len(out)

    print(f"Non-null mean_grade: {non_null:,} / {total:,} ({non_null / total:.1%})")
    print(out[["mean_grade", "max_grade", "grade_change"]].describe().round(3).to_string())

    if road_class_col is not None and road_class_col in out.columns:
        by_class = (
            out.groupby(road_class_col)[["mean_grade", "max_grade", "grade_change"]]
            .describe()
            .round(3)
        )
        print("\nDistribution by road_classification:\n")
        print(by_class.to_string())

    print("\nStructure proxy counts:")
    print(
        out[["is_bridge_proxy", "is_tunnel_proxy", "is_covered_proxy", "grade_method"]]
        .fillna(False)
        .astype(str)
        .value_counts(dropna=False)
        .head(20)
        .to_string()
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate paths and tile metadata, then exit before sampling roads.",
    )
    parser.add_argument(
        "--limit-links",
        type=int,
        default=None,
        help="Smoke-test on the first N links. Implies --no-write.",
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="Run computation and reporting without writing network_features.parquet.",
    )
    return parser.parse_args()


def main(check_only: bool = False, limit_links: int | None = None, no_write: bool = False) -> None:
    network_path = find_existing_path(NETWORK_CANDIDATES)
    tile_paths = terrain_zip_paths()

    print(f"Network geometry source: {network_path}")
    print(f"Terrain 50 zip tiles: {len(tile_paths):,} under {TERRAIN_DATA_DIR}")
    print(f"Output feature table: {OUTPUT_PATH}")

    tile_index = build_terrain_tile_index(tile_paths)
    print(
        "Terrain tile bounds: "
        f"x {tile_index['left'].min():.0f}-{tile_index['right'].max():.0f}, "
        f"y {tile_index['bottom'].min():.0f}-{tile_index['top'].max():.0f}"
    )

    if check_only:
        print("Check-only mode: exiting before road sampling.")
        return

    network = load_geodf(network_path).copy()
    link_col = infer_column(network.columns, LINK_ID_CANDIDATES)
    if link_col is None:
        raise KeyError("Could not infer link id column from the network parquet.")
    if "geometry" not in network.columns:
        raise ValueError("Network parquet must contain LineString geometry.")

    road_class_col = infer_column(network.columns, ROAD_CLASS_CANDIDATES)
    keep_cols = [link_col, "geometry"] + ([road_class_col] if road_class_col else [])
    network = network[keep_cols].copy()
    network["geometry"] = network.geometry.apply(normalise_line)
    network = network.loc[network["geometry"].notna()].copy()
    network = ensure_bng(network)

    if limit_links is not None:
        network = network.head(limit_links).copy()
        no_write = True
        print(f"Limit mode: using first {len(network):,} links and skipping output write.")

    points = load_or_build_points(network, link_col)
    points = ensure_bng(points)
    points["elevation_m"] = sample_elevation_from_tiles(points, tile_index)

    raw_features = compute_grade_features(points, link_col)
    flags = load_structure_flags(network, link_col)

    features = raw_features.merge(flags, on=link_col, how="left")
    for col in ["is_bridge_proxy", "is_tunnel_proxy", "is_covered_proxy"]:
        features[col] = features[col].fillna(False).astype(bool)
    features = apply_structure_fallback(features)

    features["grade_low_confidence"] = False
    anomaly_mask = features["max_grade"].notna() & (
        features["max_grade"] > LOW_CONFIDENCE_MAX_GRADE_PCT
    )
    features.loc[anomaly_mask, "grade_low_confidence"] = True

    report_df = network[[link_col] + ([road_class_col] if road_class_col else [])].merge(
        features[[link_col, *GRADE_COLUMNS]],
        on=link_col,
        how="left",
    )

    if no_write:
        print("No-write mode: not updating network_features.parquet.")
        print_report(report_df, road_class_col=road_class_col)
        return

    out = merge_into_network_features(features, link_col)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUTPUT_PATH, index=False)

    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    out[["mean_grade", "max_grade", "grade_change"]].describe().round(3).to_csv(
        SUMMARY_DIR / "terrain50_grade_distribution_overall.csv"
    )
    print(f"Saved: {OUTPUT_PATH}")
    print_report(report_df, road_class_col=road_class_col)


if __name__ == "__main__":
    args = parse_args()
    main(check_only=args.check_only, limit_links=args.limit_links, no_write=args.no_write)
