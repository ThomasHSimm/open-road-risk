# Session Changelog — April 12 2026

## Study Area Extended: Yorkshire + NW England

Police force codes now include both Yorkshire (12/13/14/16) and NW England
(4=Lancashire, 5=Merseyside, 6=Greater Manchester, 7=Cheshire).

OS Open Roads bbox extended west to easting 290,000 (Liverpool coast).
203,928 collisions loaded (was 102,361). Snap rate 99.8% at mean 9.8m.

---

## clean.py — SD→SE correction removed

`_fix_sd_se_error()` deleted entirely. It was incorrectly shifting NW England
collisions 100km east (Lancashire genuinely has eastings in the 300-400k range).
LSOA coordinate validation now uses haversine distance on lat/lon fields,
which are reliable for all forces. BNG fields not used anywhere in the pipeline.

---

## model.py refactored → model/ package

1390-line model.py split into:

    src/road_risk/model/
    ├── __init__.py
    ├── main.py          ← CLI (--stage traffic|temporal|collision|all)
    ├── aadt.py          ← Stage 1a AADT estimator
    ├── collision.py     ← Stage 2 Poisson GLM + XGBoost
    ├── temporal.py      ← Stage 1b seasonal profiles
    └── constants.py     ← shared encodings

src/road_risk/model.py retained as backwards-compat shim.

Key architectural changes:
- AADT estimates always regenerated (no stale cache) — covers all 998,769 links
- Collision model trains on years with AADT estimates (2019/2021/2023) only
- risk_scores.parquet: ONE ROW PER LINK (no year dimension) — pooled totals
- All 998,769 links scored including zero-collision links
- Pooling: collision_count=sum, estimated_aadt=mean, predicted_glm=mean across years

Model results (Yorkshire + NW England, full network):
  AADT estimator CV R²: 0.720 (±0.030)
  Poisson GLM pseudo-R²: 0.097
  XGBoost pseudo-R²: 0.287
  Links scored: 998,769

---

## App updated for pooled architecture

data.py:
- build_map_gdf() signature: (road_classes_tuple, min_percentile) — no years_tuple
- Straight left join risk → openroads, no groupby aggregation
- _enrich_unscored() and has_risk_data flag removed (all links scored)
- Drops road_classification from risk before merge to avoid _x/_y collision

yorkshire.py:
- Year multiselect removed from sidebar
- Summary cards show "pooled 2019/2021/2023"

map_builder.py:
- Two-layer rendering removed — single layer (all links scored)
- Priority sampling: motorways + A roads always rendered fully,
  B roads + others fill remaining budget up to MAX_LINKS_SCORED=60,000

---

## ingest_aadf.py — region filter replaced with bbox filter

Previously filtered to "Yorkshire and the Humber" region only — zero NW England
count points. Now filters by lat/lon bbox (53.0–55.2, -3.4–0.5) covering full
northern corridor. Delete data/raw/aadf/aadf_filtered.parquet and re-run
clean.py to pick up NW England count points.

---

## ingest_webtris.py — bbox extended

YORKSHIRE_BBOX extended to cover NW England motorway sensors:
  min_lat: 53.00, max_lat: 55.20, min_lon: -3.40, max_lon: 0.50

Delete data/raw/webtris/sites.parquet before re-running to refresh site list.
Yorkshire sites load from chunk cache (fast). Only new NW England sites hit API.

---

## Known issues / next steps

PERFORMANCE: Streamlit app running slow at 60k links. Needs profiling —
likely GeoJSON serialisation bottleneck. Options: tile server, simplify
geometries, or server-side rendering.

NETWORK BOUNDARY: Manchester AADT still underestimated due to betweenness
boundary effect. Fix: expand OS Open Roads network bbox further (two separate
bboxes in settings.yaml — study_area_bbox vs network_bbox). Separate issue
from AADF coverage gap (now fixed).

AADF NW ENGLAND: Cache deleted and re-ingest pending. Re-run clean.py then
model.py --stage traffic and --stage collision after webtris ingest completes.

WEBTRIS NW ENGLAND: ingest_webtris.py running overnight for new sites.

CATCHMENT MODEL: CV R²=-0.154 with Random Forest (too few centres for RF).
Replace with simple Pearson correlation per fault category. First-attempt
pass rates computed and ready as target variable.

OSM NW ENGLAND: New pbf files added but not yet ingested. Run osmium cat
then network_features.py --osm --force after webtris completes.