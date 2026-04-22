# Data Quality Notes

This document records data quality issues found during the pipeline build,
the evidence for each, and how they are handled in the code.

---

## STATS19 — Collision Coordinates

### Retired suspected BNG grid-letter issue

**Status:** Denied for the current raw DfT STATS19 CSV.

A previous investigation suspected a Yorkshire BNG grid-square error in
`location_easting_osgr` / `location_northing_osgr`. That conclusion was
rechecked against the current raw STATS19 collision CSV by transforming
`latitude` / `longitude` to BNG and comparing the result with the published
easting/northing fields for Yorkshire forces 12, 13, 14, and 16 across
2015-2024.

The fields agree within normal rounding/projection tolerance:

| Police force | Median difference | Max difference |
|---|---:|---:|
| 12 | 1.23 m | 2.43 m |
| 13 | 0.55 m | 2.19 m |
| 14 | 1.44 m | 2.38 m |
| 16 | 2.18 m | 2.97 m |

No checked Yorkshire record was more than 100 m from its lat/lon-derived BNG
position. The earlier suspected issue was likely a consequence of the
now-fixed police-force-code selection bug, where codes 4-7
(Lancashire/Merseyside/Greater Manchester/Cheshire) were mistakenly treated as
Yorkshire. The stale exploratory notebook has been moved to `notebooks/old/`.

**Handling in code:** no coordinate correction is applied. Spatial snapping and
LSOA validation use the STATS19 `latitude` / `longitude` fields directly.

---

### LSOA Coordinate Validation

**Purpose:** Catch coordinate errors and provide a principled quality flag for
use in modelling.

**Method:**
Join each collision to its recorded `lsoa_of_accident_location` using ONS 2021
LSOA population-weighted centroids. Compute haversine distance between the
collision lat/lon and the LSOA centroid. Flag collisions more than 10km from
their LSOA centroid as `coords_suspect = True`.

A collision being far from its LSOA centroid is strong evidence of a coordinate
or attribution error: the recorded LSOA and recorded coordinate should normally
refer to the same neighbourhood.

**Source file:** `data/raw/stats19/lsoa_centroids.csv`
Downloaded from ONS Open Geography Portal:
LSOA (Dec 2021) EW Population Weighted Centroids V4

**Output columns added:**
- `coords_corrected` (bool) — retained for schema compatibility; no correction
  is currently applied
- `coords_suspect` (bool) — True if >10km from LSOA centroid
- `lsoa_dist_m` (float) — distance in metres from LSOA centroid
- `coords_valid` (bool) — False if outside GB bounds OR coords_suspect

**Code location:** `src/road_risk/clean_join/clean.py` → `_validate_lsoa_coords()`

---

### Post-2015 Coordinate Quality

**Finding:** Post-2015 STATS19 data has near-100% valid coordinates in the
current study extract. Pre-2015 data has much higher rates of missing/invalid
coordinates because GPS recording was not universal.

**Decision:** Pipeline filters to 2015–2024 to avoid the pre-GPS coordinate
quality issues. This is set in `clean.py → main()`.

---

## STATS19 — Road Number Quality

### Road Numbers Are Unreliable for Spatial Joining

**Finding:**
STATS19 `first_road_number` contains systematic errors — e.g. a collision near
Burnley (West Yorkshire) recorded with road number 23, producing `road_name_clean = A23`
which is a Surrey/London road. Analysis showed 709 unique road names in Yorkshire
STATS19 but only 97 overlapping with Yorkshire OS Open Roads links.

**Root cause:**
Road numbers are manually entered by the attending officer. Errors include:
- Wrong road number (e.g. A23 in Yorkshire)
- Road numbers from adjacent force areas
- Numbers that exist in other regions but not Yorkshire

**Decision:**
Road number is used as a low-weight (10%) scoring input in `snap_weighted()`
rather than a primary join key. Weight is set to `W_NUMBER = 0.10` in
`src/road_risk/clean_join/snap.py`. The DfT themselves do not perform road network
matching in published STATS19 data — coordinates are the primary spatial
reference.

**Reference:** DfT STATS19 Review (2021) roadmap explicitly lists road network
matching as a *future* priority, confirming it has not been done in official
publications.

**Code location:** `src/road_risk/clean_join/snap.py` → `W_NUMBER = 0.10`

---

## STATS19 — Snap Rate

**Achieved snap rate:** ~99.8% of current study-area collisions successfully
snap to OS Open Roads links before the quality-score filter.

**Method:** `snap_weighted()` in `src/road_risk/clean_join/snap.py`
- KD-tree built on road geometry densified at 25m intervals (~3.9M points)
- Top K=20 candidate links within 500m search radius per collision
- Composite scoring across 4 dimensions: spatial distance (40%), road
  classification (25%), junction/form-of-way (25%), road number (10%)
- Mean snap score for matched collisions: ~0.860 / 1.0

**Remaining unmatched / low-quality snaps:**
Residual unmatched or filtered collisions are likely to have local coordinate
drift, ambiguous locations, or weak road-attribute agreement. These are retained
in the dataset with their snap status and excluded from road-link analysis where
appropriate, but included in aggregate statistics.

---

## AADF — Count Point Coverage

**Finding:** AADF count points cover ~62% of OS Open Roads links within 2km.
Major roads (motorways, A roads) have near-complete coverage. Minor roads and
unclassified roads have sparse coverage.

**Handling:** AADF features are NaN for links beyond 2km from any count point.
The 2km cap is set in `src/road_risk/clean_join/join.py → build_road_features()`.

---

## WebTRIS — Coverage

**Coverage:** National Highways network only — motorways and major trunk roads.
In Yorkshire: M1, M62, M18, M621, A1(M), A64(M) corridors.

**Finding:** Initial pull attempted all 19,518 GB sites. Filtered to 2,571
active Yorkshire sites after applying bounding box and Active status filter.

**Pull years:** 2019, 2021, 2023 (pre-COVID, COVID anomaly, recent normal).
Full 10-year pull was impractical (~25 hours). Three representative years
gives sufficient temporal coverage for the model.

---

## OS Open Roads — Yorkshire Bounding Box

**Issue:** Initial bbox clipped road links that serve collisions near the
Yorkshire boundary, particularly in the west (Lancashire border).

**Fix:** Bbox widened by 20km on all sides:
```python
# Before
YORKSHIRE_BBOX_BNG = (390000, 370000, 570000, 520000)
# After
YORKSHIRE_BBOX_BNG = (370000, 350000, 590000, 540000)
```

This increased link count from 457,884 to 705,672 and improved snap coverage
for boundary-area collisions.
