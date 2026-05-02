### Grade from OS Terrain 50 DEM

> **STATUS: COMPLETED 1–2 May 2026.**
> See `todo/feature_addition_imd_grade.md` for the writeup.
> Kept here as a record of the original specification and prompt.

**Original status before implementation:** Designed, partially set up. OS
Terrain 50 ASCII grid had been downloaded; the implementation later landed in
`src/road_risk/features/road_terrain.py` and `mean_grade` was added to Stage 2.

**Approach (from deep research):**
- OS Terrain 50 ASCII grid (NOT GeoPackage — that's the contour product)
- Build VRT via gdalbuildvrt over ~2,858 tiles in 55 folders
- Bilinear interpolation against the raster (NOT rasterio.sample() 
  nearest-neighbour, which produces edge artefacts on a 50m grid)
- Sample at same 15m point spacing as curvature features
- Compute slope over 45-60m effective baseline (3-4 sample steps), 
  not consecutive 15m pairs — the 50m DEM doesn't support 15m 
  resolution
- Features: mean_grade_pct (length-weighted absolute), 
  max_grade_pct, grade_change_m
- Use magnitudes not signed values (link direction often arbitrary)
- 4m RMSE on heights, 50m cell spacing — feature is rank-preserving, 
  amplitude-conservative

**Structure handling — open design decision:**
Bridges, tunnels, AND slip roads need special handling because the 
DTM removes supported structures and reports ground level under/over 
them. Slip roads on grade-separated junctions are particularly 
problematic — the DTM has no way to know which level a link is on.

Two paths considered:
1. OSM bridge/tunnel tags (bridge=*, tunnel=*, covered=*) joined 
   to links, endpoint-fallback grade where flagged. Requires 
   extending OSM extraction in network.py to capture these tags.
2. OS Open Roads form_of_way to identify slip roads, endpoint-
   fallback for those. Uses authoritative network metadata; doesn't 
   need OSM extension; but only catches slip roads, not bridges 
   in general.

Best path is probably both: OS form_of_way for slip roads, OSM 
tags for bridges/tunnels, endpoint-fallback for either flag. 
Approximately 2-3% of links would be affected.

**Why not now:**
- Deferred after a high-output day to avoid attention fatigue on 
  fiddly debug
- Structure handling design needs to land cleanly — running without 
  it produces visibly wrong values on bridges/tunnels/slip roads, 
  which would require explaining away in methodology
- Lower priority than the 5-seed harness (evaluation infrastructure 
  unlocks honest measurement of every future change including this)

**Next steps when picked up:**
1. Verify OS Terrain 50 unzip state and VRT build (check tile count 
   ~2,858 .asc files; build VRT if not done)
2. Extend OSM extraction in network.py to capture bridge, tunnel, 
   covered tags (separate small task)
3. Implement grade script with both structure-handling paths
4. Validation tests: flat terrain (grade ~0), linear ramp 
   (grade matches), bridge/tunnel/slip flagged correctly
5. Spot-check 20 random links per category against OSM 
6. Don't retrain Stage 2 — this is feature engineering only, retrain 
   happens after 5-seed harness lands

**Related:** Pairs with curvature features. Both attack the geometric-
risk gap in the current feature set. Likely modest individual 
contribution given the rank stability findings (top-1% Jaccard 0.951 
across the tiered imputation change), but as a paired set with 
curvature, captures geometric alignment risk that the model currently 
has no signal for.

---
