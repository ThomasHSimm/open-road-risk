# Curvature from OS Open Roads geometry

## Overall judgement

Horizontal curvature is worth adding. The entity["organization","Federal Highway Administration","us transport agency"] reports that more than 25 percent of fatal crashes are associated with horizontal curves, that the average crash rate on curves is about three times that on tangent segments, and that roadway-departure crashes on curves are more severe; in a separate urban case-control study, run-off-crash odds fell markedly as curve radius increased. That is enough to justify a curvature proxy as a missing geometric risk signal in a link-level model. citeturn2search0turn4view0turn4view2

The source is good, but not in the exact way your context note suggests. entity["organization","Ordnance Survey","gb mapping agency"] describes OS Open Roads as an approximate centreline road-link network covering classified and unclassified roads, and as an open dataset under the Open Government Licence. But the delivered product is explicitly generalised to 1:25,000 scale with a recommended viewing range of 1:15,000 to 1:30,000; by contrast, OS MasterMap Highways Network – Roads is the more detailed road-geometry product at 1:1,250 to 1:10,000. So curvature derived from OS Open Roads should be treated as a conservative screening and ranking variable, not as engineering-grade radius. citeturn3view1turn4view4turn1search0turn7search2

I would therefore not commit yet to unconditional universal coverage. The safer design is path two with an automatic class gate: compute curvature for every road class that clears a minimum vertex-density threshold, and let the same pipeline collapse to universal coverage if every class passes. That protects you against false near-zero curvature on sparse minor-road geometry while still preserving maximum usable coverage. The threshold itself is an operational quality rule inferred from the product’s generalisation level and your intended 15 m resampling interval, not an external OS standard. citeturn3view1turn5search1

## Why the signal is worth adding

The literature signal is directionally consistent. The FHWA summary of curve safety says the vast majority of curve-related fatal crashes are roadway departures, and its roadway-departure guidance cites earlier work showing that single-vehicle run-off-road crash rates on horizontal curves are roughly four times those on tangents and that severity is higher on curves. Separately, FHWA research on horizontal curve and grade combinations found crash frequency increases as horizontal curve radius decreases and that short, sharp curves are associated with higher crash frequencies. Even though your proposed metric is not radius itself, it is monotonic with “more turning per unit distance,” which is the same behavioural signal. citeturn2search0turn4view0turn8view0

The urban run-off study is useful because it shows the same directional relationship outside the classic rural two-lane setting. In that case-control analysis, the odds of a run-off crash decreased as radius increased, with the largest-radius category showing much lower odds than the tightest-radius reference class. That matters for your use case because it suggests that conservative relative ranking from a simplified national road dataset can still be informative even when absolute curvature is damped by source generalisation. citeturn4view2

## What the source geometry can support

OS Open Roads is not just broad coverage; it is a topologically structured link-and-node road network whose links represent an approximate central alignment of road carriageways and include both classified and unclassified roads. It is also free to re-use under the Open Government Licence, which permits copying, adapting, and commercial re-use subject mainly to attribution. Those are real advantages for a universal feature-engineering pipeline. citeturn3view1turn4view4turn1search0

The main limitation is simplification. Ordnance Survey states that OS Open Roads is automatically generalised from larger-scale source data and is appropriate to 1:25,000 scale. That means curvature extracted from the polyline will be conservative in two ways: some bend detail will already have been smoothed out, and longer straight chords between preserved vertices will flatten the local turning signal when you interpolate along them. For modelling, that is acceptable if you frame the feature as rank-order geometry rather than design geometry. It is not acceptable if you silently assume the values are comparable to survey-grade radius inventories. citeturn3view1turn5search1turn7search2

The class split matters because the OS code list includes Motorway, A Road, B Road, Classified Unnumbered, Unclassified, Not Classified, and Unknown, and the same documentation notes that Unclassified roads make up the majority of roads in the UK. If Unclassified geometry is materially sparser, the degradation is not a corner case; it affects a large share of the network. citeturn3view0

A second operational caveat is versioning. OS says OS Open Roads is updated every six months, in April and October, and that feature identifiers are not persistent between product versions. So curvature must be merged back into the same network edition from which it was computed; using a later refresh as the join target is unsafe even if column names look compatible. citeturn0search2turn3view1

## Decision rule for coverage

I recommend path two as the implementation pattern, because it strictly dominates path one. If every class passes the gate, path two behaves exactly like universal coverage. If one or more classes fail, path two prevents low-information geometry from masquerading as genuinely straight roads.

A sensible starting gate for 15 m resampling is:

- class median `vertices_per_km` at least `40`
- class 25th percentile `vertices_per_km` at least `20`

That corresponds to mean original vertex spacing of about 25 m at the median and 50 m at the lower quartile. Below that, a 15 m resampler is mostly interpolating long simplified chords rather than preserved bends, which is risky given the source is already a 1:25,000 generalised product. This is an engineering convenience threshold, not a published standard, and it should be treated as a first-pass QA rule. citeturn3view1turn5search1

If a class narrowly misses the gate, the right sensitivity test is not to force universal coverage immediately. It is to rerun the same pipeline at 20 m spacing and see whether the density warning meaningfully improves. If a class still fails there, I would keep curvature as `NaN` for that class and document the result as minor-road-degraded due to source simplification. False zeros are more dangerous than explicit missingness because they look like evidence of straight geometry.

## Reference implementation

The script below does the exact pre-check and feature-engineering steps you described. It loads `openroads.parquet` if present, otherwise falls back to `current_network.parquet` or `network_features.parquet`; computes `vertices_per_km`; prints `describe()` by `road_classification`; chooses universal or gated coverage automatically from the observed distribution; resamples each eligible LineString at 15 m spacing; computes interior turning-angle density in degrees per km; writes `mean_curvature`, `max_curvature`, and `sinuosity`; and saves summary CSVs for the vertex-density and feature distributions. If `network_features.parquet` already exists, it updates that file when a stable key is available; otherwise it writes a new one. Because OS identifiers are not persistent across product versions, the join target must be from the same OS Open Roads release as the source parquet. citeturn3view1turn0search2

```python
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import wkb
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge

INPUT_CANDIDATES = [
    Path("openroads.parquet"),
    Path("current_network.parquet"),
    Path("network_features.parquet"),
]
OUTPUT_PATH = Path("network_features.parquet")
SPACING_M = 15.0

# Operational quality gate for 15 m resampling.
MEDIAN_VERTICES_PER_KM_MIN = 40.0
P25_VERTICES_PER_KM_MIN = 20.0

KEY_CANDIDATES = ["link_id", "road_link_id", "roadlink_id", "identifier", "id"]


def _load_parquet(path: Path) -> gpd.GeoDataFrame:
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
        sample = df[geom_col].dropna().iloc[0]
        if isinstance(sample, (bytes, bytearray, memoryview)):
            geom = df[geom_col].apply(lambda x: None if pd.isna(x) else wkb.loads(bytes(x)))
        else:
            geom = df[geom_col]
        gdf = gpd.GeoDataFrame(df.drop(columns=[geom_col]), geometry=geom, crs=getattr(df, "crs", None))
        return gdf


def load_input() -> tuple[Path, gpd.GeoDataFrame]:
    for path in INPUT_CANDIDATES:
        if path.exists():
            gdf = _load_parquet(path)
            return path, gdf
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
    return gdf.to_crs(27700)


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


def turning_angle_features(ls: LineString, spacing_m: float = 15.0) -> dict[str, float]:
    length_m = float(ls.length)
    start = np.array(ls.coords[0], dtype=float)
    end = np.array(ls.coords[-1], dtype=float)
    straight_m = float(np.linalg.norm(end - start))
    sinuosity = np.nan if straight_m <= 0 else length_m / straight_m

    pts = resample_linestring(ls, spacing_m=spacing_m)
    if len(pts) < 3:
        return {
            "mean_curvature": 0.0,
            "max_curvature": 0.0,
            "sinuosity": sinuosity,
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
            "mean_curvature": 0.0,
            "max_curvature": 0.0,
            "sinuosity": sinuosity,
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

    # Length-weighted mean = total turning angle per unit length.
    mean_curvature = float(np.average(curvature_deg_per_km, weights=local_spacing_m))
    max_curvature = float(np.max(curvature_deg_per_km))

    return {
        "mean_curvature": mean_curvature,
        "max_curvature": max_curvature,
        "sinuosity": float(sinuosity) if not np.isnan(sinuosity) else np.nan,
    }


def infer_key_column(df: pd.DataFrame) -> str | None:
    for col in KEY_CANDIDATES:
        if col in df.columns:
            return col
    return None


def main():
    input_path, gdf = load_input()
    gdf = ensure_metric_crs(gdf).copy()
    original_columns = list(gdf.columns)

    gdf["geometry"] = gdf.geometry.apply(normalise_linestring)
    gdf = gdf.loc[gdf["geometry"].notna()].copy()

    if "road_classification" not in gdf.columns:
        candidates = [c for c in gdf.columns if c.lower() in {"roadclassification", "road_classification"}]
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

    valid_classes = vertex_summary.index[
        (vertex_summary["50%"] >= MEDIAN_VERTICES_PER_KM_MIN) &
        (vertex_summary["25%"] >= P25_VERTICES_PER_KM_MIN)
    ].tolist()

    strategy = (
        "all_classes"
        if set(valid_classes) == set(vertex_summary.index.tolist())
        else "gated_by_road_classification"
    )

    print("\nChosen strategy:", strategy)
    print("Valid classes:", valid_classes)

    gdf["mean_curvature"] = np.nan
    gdf["max_curvature"] = np.nan
    gdf["sinuosity"] = np.nan

    mask = gdf["road_classification"].isin(valid_classes)
    feature_rows = []
    for idx, ls in gdf.loc[mask, "geometry"].items():
        feats = turning_angle_features(ls, spacing_m=SPACING_M)
        feature_rows.append((idx, feats["mean_curvature"], feats["max_curvature"], feats["sinuosity"]))

    if feature_rows:
        feature_df = pd.DataFrame(
            feature_rows,
            columns=["_row_ix", "mean_curvature", "max_curvature", "sinuosity"],
        ).set_index("_row_ix")
        gdf.loc[feature_df.index, ["mean_curvature", "max_curvature", "sinuosity"]] = feature_df[
            ["mean_curvature", "max_curvature", "sinuosity"]
        ].values

    non_null_count = int(gdf["mean_curvature"].notna().sum())
    total_count = int(len(gdf))

    print(f"\nCurvature non-null links: {non_null_count:,} / {total_count:,} ({non_null_count / total_count:.1%})")

    curv_summary = gdf[["mean_curvature", "max_curvature", "sinuosity"]].describe().round(3)
    print("\nOverall feature distribution:\n")
    print(curv_summary.to_string())

    by_class_curv = (
        gdf.groupby("road_classification")[["mean_curvature", "max_curvature", "sinuosity"]]
        .describe()
        .round(3)
    )
    print("\nFeature distribution by road_classification:\n")
    print(by_class_curv.to_string())

    save_cols = list(dict.fromkeys(original_columns + ["mean_curvature", "max_curvature", "sinuosity"]))
    gdf_save = gdf[save_cols].copy()

    if OUTPUT_PATH.exists() and OUTPUT_PATH != input_path:
        existing = _load_parquet(OUTPUT_PATH)
        left_key = infer_key_column(existing)
        right_key = infer_key_column(gdf_save)

        if left_key and right_key:
            features_only = gdf_save[[right_key, "mean_curvature", "max_curvature", "sinuosity"]].copy()
            updated = existing.drop(columns=["mean_curvature", "max_curvature", "sinuosity"], errors="ignore").merge(
                features_only,
                left_on=left_key,
                right_on=right_key,
                how="left",
                suffixes=("", "_new"),
            ).drop(columns=[right_key] if left_key != right_key else [], errors="ignore")
            updated.to_parquet(OUTPUT_PATH, index=False)
        else:
            gdf_save.to_parquet(OUTPUT_PATH, index=False)
    else:
        gdf_save.to_parquet(OUTPUT_PATH, index=False)

    vertex_summary.to_csv("openroads_vertex_density_by_class.csv")
    curv_summary.to_csv("openroads_curvature_distribution_overall.csv")
    by_class_curv.to_csv("openroads_curvature_distribution_by_class.csv")
    print(f"\nWrote updated features to {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
```

This implementation defines `mean_curvature` as the length-weighted average of local turning-angle density, so it is interpretable as total turning per kilometre of link, and `max_curvature` as the sharpest local turning-angle density observed on the resampled line. `sinuosity` is `link_length / straight_line_length`, with `NaN` for zero-chord loops such as degenerate roundabout-like links.

## Execution status in this workspace

At the time this note was written, I could not run the pre-check because neither `openroads.parquet` nor an alternative current network parquet was available in that workspace. So this note does not report the observed `vertices_per_km` distribution, the final all-classes-versus-gated decision from the data, the count of non-null curvature links, or the realised feature distributions from your network.

When you do run it, the interpretation should be straightforward. If every road class clears the density gate, keep curvature as a universal-coverage feature. If the weaker classes are mainly `Unclassified`, `Not Classified`, or `Unknown`, keep the gated result and document those links as degraded by source simplification rather than backfilling zeros. The feature distributions you want to see are strongly right-skewed `mean_curvature` and `max_curvature`, with `sinuosity` tightly clustered above 1 and a longer tail on winding links. That is the correct place to stop for now, before any model retraining.
