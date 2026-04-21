# Grade from OS Terrain 50 DEM

## Recommendation

Use OS Terrain 50 grade features across **all** road classes, not a class-gated subset. Unlike curvature from OS Open Roads geometry, the constraint here is not class-specific vertex sparsity; it is the coarseness and semantics of the elevation surface itself. OS Terrain 50 is a Great Britain–wide 50 m digital terrain model with annual refreshes, so it gives you uniform national support for link-level vertical geometry. The safety case is also strong: FHWA work on rural two-lane roads found crash frequency increases with increasing percent grade, and downgrade-focused truck studies report worse severe-injury risk on downgrades. That makes grade a defensible companion to curvature in the feature set. citeturn4search0turn4search3turn1search9turn3search1

The two main corrections to the Gemini draft are straightforward. First, for **grade extraction** you need the **ASCII grid** supply, not the GeoPackage, because the GeoPackage is the **contours** product while the raster grid is delivered separately as ASCII grid plus companion GML metadata. Second, you should not compute grade from adjacent 15 m point pairs using `rasterio.sample()` as written there, because `sample()` returns the value of the **nearest pixel** with **no interpolation**, and Rasterio’s own guidance says nearest-neighbour is often not suitable for continuous data whereas bilinear or cubic are better suited. citeturn4search3turn4search5turn4search1turn10search5turn10search0

My preferred implementation is therefore: keep the same cached 15 m resampled points you use for curvature so the features remain geometrically aligned, sample elevation from the Terrain 50 grid using **bilinear interpolation**, but compute slope over a **45–60 m effective baseline** rather than raw 15 m step-to-step differences. That preserves consistency with the curvature cache while avoiding pseudo-detail from a 50 m terrain surface. This gives you near-universal coverage, with structure-aware handling for bridges and tunnels. citeturn4search1turn10search0turn10search5

## What to download

The product to use is OS Terrain 50 from entity["organization","Ordnance Survey","gb mapping agency"]. The official documentation is explicit that OS Terrain 50 is published as both **grid** and **contour** data. The **grid** is a 50 m raster of heighted points, supplied in **ASCII grid** and **GML**. The **contours** are 10 m interval vectors, supplied in **GML**, **Esri Shapefile**, **GeoPackage**, and **vector tiles**. So if your task is to sample elevation at road points, the correct download is the **ASCII grid** bundle; the GeoPackage is useful for visual QA in desktop GIS, but it is not the DEM you want for production sampling. citeturn4search3turn4search5turn0search4

Operationally, OS supplies the national dataset in **10 km by 10 km tiles**; for the ASCII, GML, and Shapefile formats, the full national set contains **2,858 tiles** arranged in **55 folders**. For the grid itself, each tile is **200 by 200 pixels** at **50 m** cell size, with heights given to the **nearest 0.1 m**. That makes a VRT mosaic the right engineering pattern: you keep a virtual national DEM without materialising a huge raster, while still letting GDAL index the tiles for you. citeturn4search1turn4search5turn6search0

A practical acquisition pattern is to download the ASCII grid archive from the OS Data Hub, unpack it by folder, generate a plain text file of all `.asc` paths, and build a VRT with `gdalbuildvrt`. GDAL’s VRT tooling is designed for exactly this use case: it builds a virtual mosaic over many source rasters and supports nodata handling and resampling options. citeturn4search5turn6search0turn6search1

## What the DEM can and cannot represent

OS Terrain 50 is a **DTM**, not a road-surface profile. The documentation says the product represents the **bare earth surface**, with buildings, trees, and other protruding features removed. It also states that **supported structures** are removed where an air gap exists. That point matters more than anything else for your bridge and tunnel logic: a DEM-derived elevation sampled “inside” a bridge span or through a tunnel corridor cannot simply be assumed to represent the travelled carriageway elevation. citeturn4search3turn5search0

At the same time, the product is not useless for roads. The source-data documentation says that **major communication routes** are specifically modelled so that the road carriageway or railway track bed reflects the real-world shape, with associated slopes and embankments modelled as well. That is exactly why the dataset is good enough for broad link-level grade features. But the same documentation also makes clear that the surface is smoothed and generalised for landscape-scale use, and the product overview reports **4 m RMSE** for height points. Together with the **50 m** cell spacing, that means your grade features should be interpreted as conservative, link-scale vertical geometry, not fine vertical alignment or engineering-grade crest/sag design parameters. citeturn5search0turn5search1turn4search1

There is also a subtle but important sampling implication. The ASCII grid values are defined at the **centre of each 50 m pixel**. If you sample every 15 m, those extra sample points are not new measurements; they are interpolated estimates between 50 m-supported terrain points. That is completely acceptable as long as you treat the output as a smoothed feature and avoid pretending that a 15 m profile extracted from a 50 m raster has 15 m native support. citeturn4search1turn10search0

## Feature engineering design

I would keep the curvature point cache at **15 m** spacing and compute grade from those same points, but I would **not** use consecutive-point slopes as the production feature. A 15 m differencing baseline on a 50 m grid is too short and will exaggerate cell-edge artefacts, especially if nearest-neighbour sampling is used. The better pattern is: sample bilinear elevations at all cached points, then compute slope over an effective baseline of roughly one Terrain 50 cell. With 15 m point spacing, that means comparing points about **3 to 4 steps apart**, i.e. **45–60 m**. citeturn4search1turn10search0turn10search5

That leads to a stable feature definition. `mean_grade` should be the **length-weighted mean absolute grade** in **percent** over the chosen 45–60 m baseline; `max_grade` should be the **maximum absolute grade** over that same baseline, again in **percent**; and `grade_change` should be the **sum of absolute adjacent elevation changes** along the bilinearly sampled profile, in **metres**. I would store magnitude rather than signed values in the main feature columns, because signed uphill/downhill estimates are only meaningful if the link direction is aligned with traffic movement, which is often not the case in a generic link network. For model work, magnitude is the safer default. citeturn4search1turn10search0

This is where the grade pipeline differs from the curvature pipeline. Curvature needed a pre-check for source geometry density by road class. Grade does **not** need that same gate, because the raster support is uniform regardless of road class. The quality issue is instead driven by product scale and by supported structures. So the right decision here is **universal computation with structure-aware confidence handling**, not class gating. citeturn4search3turn5search0

## Bridge and tunnel handling

Your instinct to treat bridges and tunnels separately is correct, but the exact OSM proxy should be defined a little more carefully. In entity["organization","OpenStreetMap","collaborative map project"], bridges are tagged with `bridge=*`, not only `bridge=yes`, and tunnels are tagged with `tunnel=*`, not only `tunnel=yes`. The tunnel key also covers values such as `building_passage`, `culvert`, and other tunnel-like cases, and the OSM guidance explicitly recommends `covered=*` instead of `tunnel=*` for some covered passages. So for detection, you should flag **any non-`no` `bridge=*`**, **any non-`no` `tunnel=*`**, and optionally **any non-`no` `covered=*`** if your OSM extract includes those tags. citeturn9search1turn8search0

Way tags should be your primary proxy, but they are not the whole story. OSM also documents bridge and tunnel **relations** for more complex structures, although the wiki notes that simple way-level tagging remains the simplest standard approach and the relation is mainly for grouping complex cases. In practice, if your extract preserves relation membership or already flattens relation tags onto member ways, use it; if not, way-level `bridge=*` and `tunnel=*` tags are still the right first-pass proxy. citeturn7search0turn7search2turn7search6

For flagged structure links, I would not trust raw interior DEM samples. The most robust compromise is to keep numeric coverage by replacing the raw interior-profile features with an **endpoint fallback**: sample the start and end elevations of the link, compute net rise over link length, set `mean_grade` and `max_grade` to that endpoint grade magnitude, and set `grade_change` to the absolute start-end elevation difference. This is not a perfect bridge-deck or tunnel-bore profile, but it is usually much closer to the travelled slope than letting the DTM dive to valley floor under a viaduct or climb hillside above a tunnel. I would also persist helper flags such as `is_bridge_proxy`, `is_tunnel_proxy`, and `grade_method` so you can audit the approximation later. The remaining fallback after that should be anomaly detection, not hard deletion. citeturn5search0turn9search1turn8search0

## Reference pipeline

```python
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

DEM_VRT_PATH = Path("data/dem/os_terrain_50_gb.vrt")

POINT_CACHE_CANDIDATES = [
    Path("data/processed/link_resampled_points.parquet"),
    Path("link_resampled_points.parquet"),
]

NETWORK_CANDIDATES = [
    Path("data/processed/network_features.parquet"),
    Path("network_features.parquet"),
    Path("data/processed/current_network.parquet"),
    Path("current_network.parquet"),
    Path("openroads_yorkshire.parquet"),
]

OSM_STRUCTURE_CANDIDATES = [
    Path("data/external/osm_bridges_tunnels.parquet"),
    Path("osm_bridges_tunnels.parquet"),
]

OUTPUT_PATH = Path("network_features.parquet")

# Keep the same point spacing as curvature.
POINT_SPACING_M = 15.0

# Compute grade over ~1 Terrain 50 cell, not over raw 15 m steps.
GRADE_BASELINE_M = 45.0   # 3 * 15 m, close to the 50 m DEM support

LINK_ID_CANDIDATES = ["link_id", "road_link_id", "roadlink_id", "identifier", "id"]
POINT_SEQ_CANDIDATES = ["point_sequence", "sequence", "seq", "point_idx", "sample_idx"]
POINT_DIST_CANDIDATES = ["distance_m", "distance", "chainage_m", "dist_m"]
ROAD_CLASS_CANDIDATES = ["road_classification", "roadclassification"]

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
    for c in candidates:
        if c in colset:
            return c
    return None


def ensure_bng(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.crs is None:
        raise ValueError("CRS missing. Expected a projected CRS in metres.")
    epsg = gdf.crs.to_epsg()
    if epsg == 27700:
        return gdf
    return gdf.to_crs(27700)


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


def build_points_from_network(network_gdf: gpd.GeoDataFrame, link_col: str) -> gpd.GeoDataFrame:
    rows = []

    for _, row in network_gdf[[link_col, "geometry"]].iterrows():
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

        for seq, d in enumerate(dists):
            rows.append(
                {
                    link_col: link_id,
                    "point_sequence": seq,
                    "distance_m": float(d),
                    "geometry": geom.interpolate(float(d)),
                }
            )

    points = gpd.GeoDataFrame(rows, geometry="geometry", crs=network_gdf.crs)
    return points


def load_or_build_points(network_gdf: gpd.GeoDataFrame, link_col: str) -> gpd.GeoDataFrame:
    for path in POINT_CACHE_CANDIDATES:
        if path.exists():
            points = ensure_bng(load_geodf(path))
            point_link_col = infer_column(points.columns, [link_col] + LINK_ID_CANDIDATES)
            if point_link_col is None:
                raise KeyError("Could not infer link id column in point cache.")

            if point_link_col != link_col:
                points = points.rename(columns={point_link_col: link_col})

            seq_col = infer_column(points.columns, POINT_SEQ_CANDIDATES)
            dist_col = infer_column(points.columns, POINT_DIST_CANDIDATES)

            if seq_col is None:
                points["point_sequence"] = points.groupby(link_col).cumcount()
            elif seq_col != "point_sequence":
                points = points.rename(columns={seq_col: "point_sequence"})

            if dist_col is None:
                # Approximate if cache does not already store cumulative distance.
                points = points.sort_values([link_col, "point_sequence"]).copy()
                points["distance_m"] = points.groupby(link_col).cumcount() * POINT_SPACING_M
            elif dist_col != "distance_m":
                points = points.rename(columns={dist_col: "distance_m"})

            return points

    # Fallback: build points from network geometries.
    return build_points_from_network(network_gdf, link_col)


def bilinear_sample_band(src: rasterio.io.DatasetReader, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    """
    Bilinear interpolation against a single-band raster whose values are specified
    at pixel centres. This is preferable to nearest-neighbour sampling for a
    continuous DTM.
    """
    band = src.read(1, masked=True).astype("float32")
    transform = src.transform

    # For north-up rasters:
    # transform.a > 0 (pixel width)
    # transform.e < 0 (pixel height)
    # transform.c, transform.f are the upper-left corner of the upper-left pixel
    cols_edge = (xs - transform.c) / transform.a
    rows_edge = (ys - transform.f) / transform.e

    # Convert edge-based coordinates to centre-based coordinates because
    # OS Terrain 50 heights are defined at pixel centres.
    cols = cols_edge - 0.5
    rows = rows_edge - 0.5

    col0 = np.floor(cols).astype(int)
    row0 = np.floor(rows).astype(int)
    col1 = col0 + 1
    row1 = row0 + 1

    dr = rows - row0
    dc = cols - col0

    out = np.full(xs.shape[0], np.nan, dtype="float32")

    valid = (
        (row0 >= 0)
        & (col0 >= 0)
        & (row1 < src.height)
        & (col1 < src.width)
    )

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

    m00 = np.ma.getmaskarray(z00)
    m01 = np.ma.getmaskarray(z01)
    m10 = np.ma.getmaskarray(z10)
    m11 = np.ma.getmaskarray(z11)

    interp_valid = ~(m00 | m01 | m10 | m11)
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


def load_structure_flags(network_gdf: gpd.GeoDataFrame, link_col: str) -> pd.DataFrame:
    path = None
    for candidate in OSM_STRUCTURE_CANDIDATES:
        if candidate.exists():
            path = candidate
            break

    if path is None:
        flags = pd.DataFrame(
            {
                link_col: network_gdf[link_col].values,
                "is_bridge_proxy": False,
                "is_tunnel_proxy": False,
                "is_covered_proxy": False,
            }
        ).drop_duplicates(subset=[link_col])
        return flags

    osm = ensure_bng(load_geodf(path)).copy()

    for col in ["bridge", "tunnel", "covered"]:
        if col not in osm.columns:
            osm[col] = None

    def is_trueish(series: pd.Series) -> pd.Series:
        s = series.astype("string").str.lower()
        return s.notna() & (s != "no") & (s != "none") & (s != "")

    osm["is_bridge_proxy"] = is_trueish(osm["bridge"])
    osm["is_tunnel_proxy"] = is_trueish(osm["tunnel"])
    osm["is_covered_proxy"] = is_trueish(osm["covered"])

    osm = osm.loc[
        osm["is_bridge_proxy"] | osm["is_tunnel_proxy"] | osm["is_covered_proxy"],
        ["geometry", "is_bridge_proxy", "is_tunnel_proxy", "is_covered_proxy"],
    ].copy()

    links = network_gdf[[link_col, "geometry"]].drop_duplicates(subset=[link_col]).copy()
    joined = gpd.sjoin(
        links,
        osm,
        how="left",
        predicate="intersects",
    )

    flags = (
        joined.groupby(link_col)[["is_bridge_proxy", "is_tunnel_proxy", "is_covered_proxy"]]
        .max()
        .reset_index()
        .fillna(False)
    )
    return flags


def compute_grade_features(points_gdf: gpd.GeoDataFrame, link_col: str) -> pd.DataFrame:
    points = points_gdf.sort_values([link_col, "point_sequence"]).copy()

    baseline_steps = max(1, int(round(GRADE_BASELINE_M / POINT_SPACING_M)))

    # Adjacent dz for grade_change.
    points["prev_elev"] = points.groupby(link_col)["elevation_m"].shift(1)
    points["adj_dz_abs_m"] = (points["elevation_m"] - points["prev_elev"]).abs()

    # Multi-step dz/dx for mean/max grade.
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

    features = points.groupby(link_col, as_index=False).apply(summarise).reset_index(drop=True)
    return features


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

    # If a structure was flagged but endpoints are unusable, null out grades.
    null_mask = structure_mask & ~endpoint_ok
    out.loc[null_mask, ["mean_grade", "max_grade", "grade_change"]] = np.nan
    out.loc[null_mask, "grade_method"] = "null_structure"

    return out


def main():
    network_path = find_existing_path(NETWORK_CANDIDATES)
    network = ensure_bng(load_geodf(network_path)).copy()

    link_col = infer_column(network.columns, LINK_ID_CANDIDATES)
    if link_col is None:
        raise KeyError("Could not infer link id column from the network parquet.")

    road_class_col = infer_column(network.columns, ROAD_CLASS_CANDIDATES)

    if "geometry" not in network.columns:
        raise ValueError("Network parquet must contain LineString geometry.")

    network["geometry"] = network.geometry.apply(normalise_line)
    network = network.loc[network["geometry"].notna()].copy()

    points = load_or_build_points(network, link_col)
    points = ensure_bng(points)

    with rasterio.open(DEM_VRT_PATH) as src:
        xs = points.geometry.x.to_numpy(dtype="float64")
        ys = points.geometry.y.to_numpy(dtype="float64")
        points["elevation_m"] = bilinear_sample_band(src, xs, ys)

    raw_features = compute_grade_features(points, link_col)
    flags = load_structure_flags(network, link_col)

    features = raw_features.merge(flags, on=link_col, how="left")
    features = apply_structure_fallback(features)

    # Optional anomaly flag: keep, do not delete.
    features["grade_low_confidence"] = False
    anomaly_mask = features["max_grade"].notna() & (features["max_grade"] > 25.0)
    features.loc[anomaly_mask, "grade_low_confidence"] = True

    # Merge back into network.
    feature_cols = [
        link_col,
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

    out = network.drop(
        columns=[
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
        ],
        errors="ignore",
    ).merge(features[feature_cols], on=link_col, how="left")

    out.to_parquet(OUTPUT_PATH, index=False)

    # Reporting
    non_null = out["mean_grade"].notna().sum()
    total = len(out)

    print(f"Saved: {OUTPUT_PATH}")
    print(f"Non-null mean_grade: {non_null:,} / {total:,} ({non_null / total:.1%})")
    print(out[["mean_grade", "max_grade", "grade_change"]].describe().round(3).to_string())

    if road_class_col is not None:
        by_class = (
            out.groupby(road_class_col)[["mean_grade", "max_grade", "grade_change"]]
            .describe()
            .round(3)
        )
        print("\nDistribution by road_classification:\n")
        print(by_class.to_string())

    print("\nStructure proxy counts:")
    print(out[["is_bridge_proxy", "is_tunnel_proxy", "is_covered_proxy", "grade_method"]]
          .fillna(False)
          .astype(str)
          .value_counts(dropna=False)
          .head(20)
          .to_string())


if __name__ == "__main__":
    main()
```

This implementation deliberately differs from the Gemini sketch in three places: it uses the **ASCII grid DEM** rather than the contour GeoPackage, it uses **bilinear interpolation** rather than nearest-pixel `sample()`, and it computes grade over an approximately **50 m support baseline** instead of raw 15 m adjacent pairs. Those changes are driven directly by the OS product specification and Rasterio’s own guidance on continuous-data resampling. citeturn4search3turn4search1turn10search5turn10search0

## Validation and expected outputs

The right QA pattern after running this is not road-class gating but confidence auditing. First, report overall non-null counts for `mean_grade`, `max_grade`, and `grade_change`; with endpoint fallback enabled, you should get **near-universal numeric coverage** across terrestrial links in entity["place","Great Britain","island in north atlantic"], with residual nulls concentrated in links that have too few valid points or pathological geometry. Second, inspect distributions by `road_classification`: motorways should usually sit lower on `max_grade` and `grade_change` than lower-order roads, but there should still be strong within-class variation in upland or urban-cutting areas. Third, check the flagged structure subset separately; the `grade_method` split should make it obvious how much of the network used the profile method versus endpoint fallback. citeturn4search0turn5search0

There are three failure modes worth watching closely. One is **coastal/tidal edge behaviour**; OS extends coverage at least to low water, and the foreshore is interpolated between mean high and low water heights, but you should still expect occasional nodata or edge artefacts that need masking. The second is **short links** whose length is less than the chosen baseline, for which endpoint slope may dominate. The third is **supported structures** missed by the OSM proxy, which is why I would keep `grade_low_confidence` or a similar anomaly flag rather than pretending all grades are equally reliable. citeturn5search0turn4search4

The net result should be exactly what you want from this stage of the pipeline: a GB-wide geometric feature set where curvature captures horizontal alignment risk and Terrain 50 grade captures broad vertical alignment risk, both with explicit documentation of where source generalisation and structure handling make the values conservative. That is enough to add the features to `network_features.parquet` now and defer model retraining until the geometry layer is fully audited. citeturn1search9turn3search1turn4search3turn5search0