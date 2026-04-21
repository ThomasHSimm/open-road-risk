# Stage 1a Geometry Transform Issue

Date observed: 20 April 2026

## Summary

Stage 1a snaps AADF count points to the nearest OS Open Roads link in British
National Grid metres. In this environment, the standard WGS84 to EPSG:27700
path returned non-finite projected coordinates, which broke the KD-tree build
used for snapping network features.

This is treated as an environment-specific geometry/projection issue, not as a
data-quality problem in AADF or Open Roads.

## Failure Mode

Observed symptoms:

- `GeoDataFrame.to_crs("EPSG:27700")` on `openroads_yorkshire.parquet`
  produced projected bounds of `[inf, inf, inf, inf]`.
- Centroids computed after that reprojection were empty/non-finite.
- Direct `pyproj.Transformer.from_crs("EPSG:4326", "EPSG:27700",
  always_xy=True).transform(-2.1, 51.8)` returned `(inf, inf)`.
- The source Open Roads geometries themselves looked valid:
  `LineString` geometries, WGS84-like bounds, no empty geometries, and
  lon/lat coordinate ranges within Great Britain.

The failure was therefore not caused by obvious out-of-domain coordinates such
as Scotland/NI records outside British National Grid coverage. The sample
failure point is in England.

Environment observed:

- Python: conda `env1`, Python 3.14.3
- pyproj: 3.7.2
- PROJ runtime/compiled: 9.5.1
- PROJ database: EPSG v11.022

The exact root cause is not established. Possible causes include local PROJ
database/grid-shift configuration, CRS axis handling, or a package/environment
compatibility issue.

## Current Workaround

`src/road_risk/model/aadt.py` now avoids using `GeoDataFrame.to_crs()` for the
Open Roads reference-point extraction when the stored bounds already look like
lon/lat coordinates. It then transforms lon/lat arrays with pyproj using
`always_xy=True`.

If the EPSG:27700 transform returns any non-finite coordinate, Stage 1a logs:

- the affected row count,
- the total row count,
- the affected percentage,
- the input lon/lat bounds,
- the transform context (`OpenRoads` or `AADF`).

It then falls back to a local British National Grid Transverse Mercator
definition:

```text
+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717
+x_0=400000 +y_0=-100000 +ellps=airy +units=m +no_defs
```

That fallback is sufficient for Stage 1a nearest-neighbour snapping distances,
but it is not a full substitute for a properly configured EPSG:27700 transform
with OSTN grid-shift support. It should remain visible in logs.

## When To Investigate Further

Investigate before trusting model outputs if any of these occur:

- The fallback triggers on one machine but not another and validation metrics
  shift materially.
- The fallback reports non-finite outputs after fallback.
- The fallback triggers for an unexpected geography or lon/lat bounds outside
  Great Britain.
- A small minority of rows fails EPSG:27700 rather than the all-or-nothing
  failure seen here; that may indicate bad source coordinates rather than an
  environment issue.
- A future PROJ/GDAL update fixes EPSG:27700 locally, in which case the fallback
  should be retained only as a guarded workaround or removed after confirming
  reproducible Stage 1a metrics.

## Follow-Up

- Compare Stage 1a snap distances and validation metrics on an environment
  where EPSG:27700 works normally.
- Record whether the fallback changes nearest-link assignments materially.
- Decide whether to keep the fallback permanently or replace it with an
  environment check in project setup.
