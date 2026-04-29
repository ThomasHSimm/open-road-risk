"""
Curvature features from OS Open Roads geometry.

The output columns are:

- ``mean_curvature_deg_per_km``: total absolute turning angle per kilometre.
- ``max_curvature_deg_per_km``: largest local turning-angle density, capped at
  10,000 degrees per kilometre to suppress single-vertex digitisation artefacts.
- ``sinuosity``: dimensionless link length divided by straight-line chord
  distance, clipped at 5.0 for near-closed roundabout/self-loop geometries.

Resolution floor: links shorter than ``SPACING_M`` use a three-point sample
from start to midpoint to end. For ordinary short links this produces curvature
near zero; genuine sub-15 m curvature is below this feature's resolution.

MultiLineString handling: disconnected ``MultiLineString`` geometries are
reduced to their longest component. This is conservative and avoids fabricating
turning across disconnected fragments, but it silently discards curvature on
dropped fragments and can under-report complex junction geometry.

Source limitation: OS Open Roads is generalised to 1:25,000 scale. Curvature
values should be treated as rank-preserving but amplitude-conservative relative
to survey-grade road geometry.

Identifier persistence: OS Open Roads link identifiers are not persistent
across releases, which are published in April and October. The curvature output
must be merged back to the same Open Roads release it was computed from.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import Transformer
from shapely import wkb
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge, transform
from tqdm import tqdm

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from road_risk.config import _ROOT  # noqa: E402

MEAN_CURVATURE_COL = "mean_curvature_deg_per_km"
MAX_CURVATURE_COL = "max_curvature_deg_per_km"
SINUOSITY_COL = "sinuosity"
CURVATURE_COLUMNS = [MEAN_CURVATURE_COL, MAX_CURVATURE_COL, SINUOSITY_COL]

INPUT_CANDIDATES = [
    _ROOT / "data/processed/shapefiles/openroads.parquet",
    _ROOT / "data/processed/current_network.parquet",
    _ROOT / "data/features/network_features.parquet",
    Path("openroads.parquet"),
    Path("current_network.parquet"),
    Path("network_features.parquet"),
]
OUTPUT_PATH = _ROOT / "data/features/network_features.parquet"
SUMMARY_DIR = _ROOT / "data/features"
PROVENANCE_PATH = _ROOT / "data/provenance/curvature_provenance.json"
SPACING_M = 15.0
VALIDATION_SPACING_M = 5.0
SINUOSITY_MAX = 5.0
MAX_CURVATURE_DEG_PER_KM_CAP = 10_000.0

# Operational quality gate for 15 m resampling.
MEDIAN_VERTICES_PER_KM_MIN = 40.0
P25_VERTICES_PER_KM_MIN = 20.0

KEY_CANDIDATES = ["link_id", "road_link_id", "roadlink_id", "identifier", "id"]

OS_OPEN_ROADS_RELEASE_NOTE = (
    "OS Open Roads identifiers are not persistent across releases. This curvature output "
    "must be merged back to the same release it was computed from."
)
WGS84_PROJ = "+proj=longlat +datum=WGS84 +no_defs"
OSGB36_TM_PROJ = (
    "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 "
    "+x_0=400000 +y_0=-100000 +ellps=airy +units=m +no_defs"
)


def _load_geometry_parquet(path: Path) -> gpd.GeoDataFrame:
    """
    Load a GeoParquet or a regular parquet with a geometry column containing either
    shapely objects or WKB bytes.
    """
    try:
        gdf = gpd.read_parquet(path)
        if "geometry" not in gdf.columns:
            raise ValueError("No geometry column found.")
        if not isinstance(gdf, gpd.GeoDataFrame):
            gdf = gpd.GeoDataFrame(gdf, geometry="geometry")
        return gdf
    except Exception:
        df = pd.read_parquet(path)
        geom_candidates = [c for c in df.columns if c.lower() == "geometry"]
        if not geom_candidates:
            raise
        geom_col = geom_candidates[0]
        non_null_geom = df[geom_col].dropna()
        if non_null_geom.empty:
            geom = df[geom_col]
        elif isinstance(non_null_geom.iloc[0], (bytes, bytearray, memoryview)):
            geom = df[geom_col].apply(lambda x: None if pd.isna(x) else wkb.loads(bytes(x)))
        else:
            geom = df[geom_col]
        gdf = gpd.GeoDataFrame(
            df.drop(columns=[geom_col]),
            geometry=geom,
            crs=getattr(df, "crs", None),
        )
        return gdf


def load_input() -> tuple[Path, gpd.GeoDataFrame]:
    for path in INPUT_CANDIDATES:
        if path.exists():
            try:
                gdf = _load_geometry_parquet(path)
                return path, gdf
            except Exception as exc:
                if path == INPUT_CANDIDATES[-1]:
                    raise
                print(f"Skipping {path}: could not load geometry ({exc})")
    raise FileNotFoundError(
        f"No input parquet found. Looked for: {', '.join(str(p) for p in INPUT_CANDIDATES)}"
    )


def normalise_linestring(geom):
    if geom is None:
        return None
    if hasattr(geom, "is_empty") and geom.is_empty:
        return None
    if isinstance(geom, LineString):
        return geom
    if isinstance(geom, MultiLineString):
        merged = linemerge(geom)
        if isinstance(merged, LineString):
            return merged
        if hasattr(merged, "geoms") and len(merged.geoms) > 0:
            return max(merged.geoms, key=lambda g: g.length)
        if len(geom.geoms) > 0:
            return max(geom.geoms, key=lambda g: g.length)
    return None


def ensure_metric_crs(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.crs is None:
        raise ValueError("Input CRS is missing. Set a projected CRS in metres before running.")
    units = getattr(gdf.crs.axis_info[0], "unit_name", "").lower() if gdf.crs.axis_info else ""
    if "metre" in units or "meter" in units:
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


def vertex_count(ls) -> int:
    if ls is None:
        return 0
    return len(ls.coords)


def resample_linestring(ls: LineString, spacing_m: float = 15.0) -> np.ndarray:
    length = float(ls.length)
    if length <= 0:
        return np.asarray(ls.coords, dtype=float)

    if length < spacing_m:
        distances = np.array([0.0, length / 2.0, length], dtype=float)
    else:
        distances = np.arange(0.0, length, spacing_m, dtype=float)
        if distances.size == 0 or not np.isclose(distances[0], 0.0):
            distances = np.insert(distances, 0, 0.0)
        if not np.isclose(distances[-1], length):
            distances = np.append(distances, length)

    coords = np.array([ls.interpolate(float(d)).coords[0] for d in distances], dtype=float)

    # Drop consecutive duplicates if they appear because of zero-length artefacts.
    keep = np.ones(len(coords), dtype=bool)
    keep[1:] = np.any(np.diff(coords, axis=0) != 0, axis=1)
    coords = coords[keep]
    return coords


def calculate_sinuosity(length_m: float, straight_m: float) -> float:
    """Return link sinuosity clipped at 5.0 for near-closed loop geometries."""
    if straight_m <= 0:
        return np.nan
    return float(min(length_m / straight_m, SINUOSITY_MAX))


def turning_angle_features(ls: LineString, spacing_m: float = 15.0) -> dict[str, float]:
    """
    Calculate curvature and sinuosity for a single LineString.

    Curvature features are degrees per kilometre. Sinuosity is dimensionless and
    is clipped at 5.0 so near-closed roundabout/self-loop geometries do not
    dominate summaries with pathological length/chord ratios.
    """
    length_m = float(ls.length)
    start = np.array(ls.coords[0], dtype=float)
    end = np.array(ls.coords[-1], dtype=float)
    straight_m = float(np.linalg.norm(end - start))
    sinuosity = calculate_sinuosity(length_m, straight_m)

    pts = resample_linestring(ls, spacing_m=spacing_m)
    if len(pts) < 3:
        return {
            MEAN_CURVATURE_COL: 0.0,
            MAX_CURVATURE_COL: 0.0,
            SINUOSITY_COL: sinuosity,
        }

    p_prev = pts[:-2]
    p_mid = pts[1:-1]
    p_next = pts[2:]

    v1 = p_mid - p_prev
    v2 = p_next - p_mid

    d1 = np.linalg.norm(v1, axis=1)
    d2 = np.linalg.norm(v2, axis=1)
    valid = (d1 > 0) & (d2 > 0)
    if not np.any(valid):
        return {
            MEAN_CURVATURE_COL: 0.0,
            MAX_CURVATURE_COL: 0.0,
            SINUOSITY_COL: sinuosity,
        }

    v1 = v1[valid]
    v2 = v2[valid]
    d1 = d1[valid]
    d2 = d2[valid]

    cross = v1[:, 0] * v2[:, 1] - v1[:, 1] * v2[:, 0]
    dot = np.einsum("ij,ij->i", v1, v2)
    angle_deg = np.degrees(np.abs(np.arctan2(cross, dot)))

    # Discrete curvature: turning angle per local path length.
    local_spacing_m = 0.5 * (d1 + d2)
    curvature_deg_per_km = angle_deg / (local_spacing_m / 1000.0)

    # Total absolute turning angle per kilometre of link.
    mean_curvature = float(np.sum(angle_deg) / (length_m / 1000.0))
    max_curvature = float(
        min(np.max(curvature_deg_per_km), MAX_CURVATURE_DEG_PER_KM_CAP)
    )

    return {
        MEAN_CURVATURE_COL: mean_curvature,
        MAX_CURVATURE_COL: max_curvature,
        SINUOSITY_COL: float(sinuosity) if not np.isnan(sinuosity) else np.nan,
    }


def infer_key_column(df: pd.DataFrame) -> str | None:
    for col in KEY_CANDIDATES:
        if col in df.columns:
            return col
    return None


def make_semicircle(radius_m: float = 50.0, n_points: int = 181) -> LineString:
    theta = np.linspace(0.0, np.pi, n_points)
    coords = np.column_stack((radius_m * np.cos(theta), radius_m * np.sin(theta)))
    return LineString(coords)


def assert_close_pct(
    name: str,
    actual: float,
    expected: float,
    tolerance_pct: float = 0.05,
) -> None:
    if expected == 0:
        passed = abs(actual - expected) <= tolerance_pct
    else:
        passed = abs(actual - expected) <= abs(expected) * tolerance_pct
    if not passed:
        raise AssertionError(
            f"{name}: expected {expected:.6g} within {tolerance_pct:.0%}, got {actual:.6g}"
        )


def run_validation_tests() -> None:
    print(f"\nRunning curvature validation tests at {VALIDATION_SPACING_M:g} m spacing...")

    straight = turning_angle_features(
        LineString([(0, 0), (100, 0)]),
        spacing_m=VALIDATION_SPACING_M,
    )
    semicircle = turning_angle_features(
        make_semicircle(radius_m=50),
        spacing_m=VALIDATION_SPACING_M,
    )
    right_angle = turning_angle_features(
        LineString([(0, 0), (50, 0), (50, 50)]),
        spacing_m=VALIDATION_SPACING_M,
    )

    expected_semicircle_mean = 180.0 / ((np.pi * 50.0) / 1000.0)
    expected_semicircle_sinuosity = np.pi / 2.0
    expected_right_angle_mean = 90.0 / 0.1
    expected_right_angle_sinuosity = 100.0 / (50.0 * np.sqrt(2.0))

    results = pd.DataFrame(
        [
            {
                "shape": "straight_100m",
                MEAN_CURVATURE_COL: straight[MEAN_CURVATURE_COL],
                MAX_CURVATURE_COL: straight[MAX_CURVATURE_COL],
                SINUOSITY_COL: straight[SINUOSITY_COL],
            },
            {
                "shape": "semicircle_r50m",
                MEAN_CURVATURE_COL: semicircle[MEAN_CURVATURE_COL],
                MAX_CURVATURE_COL: semicircle[MAX_CURVATURE_COL],
                SINUOSITY_COL: semicircle[SINUOSITY_COL],
            },
            {
                "shape": "right_angle_50m_legs",
                MEAN_CURVATURE_COL: right_angle[MEAN_CURVATURE_COL],
                MAX_CURVATURE_COL: right_angle[MAX_CURVATURE_COL],
                SINUOSITY_COL: right_angle[SINUOSITY_COL],
            },
        ]
    )
    print(results.round(3).to_string(index=False))

    assert_close_pct("straight mean curvature", straight[MEAN_CURVATURE_COL], 0.0)
    assert_close_pct("straight sinuosity", straight[SINUOSITY_COL], 1.0)
    assert_close_pct(
        "semicircle mean curvature",
        semicircle[MEAN_CURVATURE_COL],
        expected_semicircle_mean,
    )
    assert_close_pct(
        "semicircle sinuosity",
        semicircle[SINUOSITY_COL],
        expected_semicircle_sinuosity,
    )
    if right_angle[MEAN_CURVATURE_COL] <= 0:
        raise AssertionError("right angle mean curvature should be positive")
    assert_close_pct(
        "right angle mean curvature",
        right_angle[MEAN_CURVATURE_COL],
        expected_right_angle_mean,
    )
    assert_close_pct(
        "right angle sinuosity",
        right_angle[SINUOSITY_COL],
        expected_right_angle_sinuosity,
    )
    print("Validation tests passed.")


def choose_valid_classes(vertex_summary: pd.DataFrame) -> tuple[list, str]:
    valid_classes = vertex_summary.index[
        (vertex_summary["50%"] >= MEDIAN_VERTICES_PER_KM_MIN)
        & (vertex_summary["25%"] >= P25_VERTICES_PER_KM_MIN)
    ].tolist()

    strategy = (
        "all_classes"
        if set(valid_classes) == set(vertex_summary.index.tolist())
        else "gated_by_road_classification"
    )
    return valid_classes, strategy


def get_script_git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def write_provenance(
    *,
    input_path: Path,
    strategy: str,
    valid_classes: list,
    gated_classes: list,
    n_links_total: int,
    n_links_with_curvature: int,
) -> None:
    provenance = {
        "script_path": str(Path(__file__).resolve()),
        "script_git_sha": get_script_git_sha(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "input_parquet_path": str(input_path.resolve()),
        "spacing_m": SPACING_M,
        "median_vertices_per_km_min": MEDIAN_VERTICES_PER_KM_MIN,
        "p25_vertices_per_km_min": P25_VERTICES_PER_KM_MIN,
        "strategy_chosen": strategy,
        "valid_classes": [str(c) for c in valid_classes],
        "gated_classes": [str(c) for c in gated_classes],
        "n_links_total": n_links_total,
        "n_links_with_curvature": n_links_with_curvature,
        "coverage_pct": n_links_with_curvature / n_links_total if n_links_total else 0.0,
        "os_open_roads_release_note": OS_OPEN_ROADS_RELEASE_NOTE,
    }

    PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROVENANCE_PATH, "w") as f:
        json.dump(provenance, f, indent=2)
    print(f"Wrote provenance to {PROVENANCE_PATH.resolve()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Print vertex density summary and exit without computing curvature.",
    )
    return parser.parse_args()


def main(check_only: bool = False):
    run_validation_tests()

    input_path, gdf = load_input()
    gdf = ensure_metric_crs(gdf).copy()
    original_columns = list(gdf.columns)

    gdf["geometry"] = gdf.geometry.apply(normalise_linestring)
    gdf = gdf.loc[gdf["geometry"].notna()].copy()

    if "road_classification" not in gdf.columns:
        candidates = [
            c
            for c in gdf.columns
            if c.lower() in {"roadclassification", "road_classification"}
        ]
        if not candidates:
            raise KeyError("Expected a road_classification column.")
        gdf["road_classification"] = gdf[candidates[0]]

    gdf["link_length_m"] = gdf.geometry.length
    gdf = gdf.loc[gdf["link_length_m"] > 0].copy()

    gdf["vertex_count"] = gdf.geometry.apply(vertex_count)
    gdf["vertices_per_km"] = gdf["vertex_count"] / (gdf["link_length_m"] / 1000.0)

    vertex_summary = (
        gdf.groupby("road_classification", dropna=False)["vertices_per_km"]
        .describe()
        .sort_index()
    )

    print("\nVertices per km by road_classification:\n")
    print(vertex_summary.round(2).to_string())

    valid_classes, strategy = choose_valid_classes(vertex_summary)
    gated_classes = [c for c in vertex_summary.index.tolist() if c not in valid_classes]

    print("\nChosen strategy:", strategy)
    print("Valid classes:", valid_classes)
    print("Gated classes:", gated_classes)

    if check_only:
        print("\nCheck-only mode: exiting before curvature computation.")
        return

    gdf[CURVATURE_COLUMNS] = np.nan

    mask = gdf["road_classification"].isin(valid_classes)
    feature_rows = []
    geometry_iter = gdf.loc[mask, "geometry"].items()
    for idx, ls in tqdm(
        geometry_iter,
        total=int(mask.sum()),
        desc="Computing curvature features",
        unit="link",
    ):
        feats = turning_angle_features(ls, spacing_m=SPACING_M)
        feature_rows.append(
            (
                idx,
                feats[MEAN_CURVATURE_COL],
                feats[MAX_CURVATURE_COL],
                feats[SINUOSITY_COL],
            )
        )

    if feature_rows:
        feature_df = pd.DataFrame(feature_rows, columns=["_row_ix", *CURVATURE_COLUMNS]).set_index(
            "_row_ix"
        )
        gdf.loc[feature_df.index, CURVATURE_COLUMNS] = feature_df[CURVATURE_COLUMNS].values

    non_null_count = int(gdf[MEAN_CURVATURE_COL].notna().sum())
    total_count = int(len(gdf))

    print(
        f"\nCurvature non-null links: "
        f"{non_null_count:,} / {total_count:,} ({non_null_count / total_count:.1%})"
    )

    curv_summary = gdf[CURVATURE_COLUMNS].describe().round(3)
    print("\nOverall feature distribution:\n")
    print(curv_summary.to_string())

    by_class_curv = (
        gdf.groupby("road_classification")[CURVATURE_COLUMNS]
        .describe()
        .round(3)
    )
    print("\nFeature distribution by road_classification:\n")
    print(by_class_curv.to_string())

    save_cols = list(dict.fromkeys(original_columns + CURVATURE_COLUMNS))
    gdf_save = gdf[save_cols].copy()

    if OUTPUT_PATH.exists() and OUTPUT_PATH != input_path:
        existing = pd.read_parquet(OUTPUT_PATH)
        left_key = infer_key_column(existing)
        right_key = infer_key_column(gdf_save)

        if left_key and right_key:
            if gdf_save[right_key].duplicated().any():
                raise ValueError(f"Curvature source has duplicate {right_key} values.")
            if existing[left_key].duplicated().any():
                raise ValueError(f"Existing feature table has duplicate {left_key} values.")

            features_only = gdf_save[[right_key, *CURVATURE_COLUMNS]].copy()
            updated = existing.drop(columns=CURVATURE_COLUMNS, errors="ignore").merge(
                features_only,
                left_on=left_key,
                right_on=right_key,
                how="left",
                validate="one_to_one",
            ).drop(columns=[right_key] if left_key != right_key else [], errors="ignore")
            OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
            updated.to_parquet(OUTPUT_PATH, index=False)
        else:
            OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
            gdf_save.to_parquet(OUTPUT_PATH, index=False)
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        gdf_save.to_parquet(OUTPUT_PATH, index=False)

    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    vertex_summary.to_csv(SUMMARY_DIR / "openroads_vertex_density_by_class.csv")
    curv_summary.to_csv(SUMMARY_DIR / "openroads_curvature_distribution_overall.csv")
    by_class_curv.to_csv(SUMMARY_DIR / "openroads_curvature_distribution_by_class.csv")
    write_provenance(
        input_path=input_path,
        strategy=strategy,
        valid_classes=valid_classes,
        gated_classes=gated_classes,
        n_links_total=total_count,
        n_links_with_curvature=non_null_count,
    )
    print(f"\nWrote updated features to {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main(check_only=parse_args().check_only)
