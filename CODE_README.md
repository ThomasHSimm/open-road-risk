# src/road_risk — Module Tracker

Status of each module in the pipeline.

| Module | Status | Notes |
|---|---|---|
| `config.py` | ✅ Done | YAML loader, `_ROOT`, path helpers |
| `ingest/ingest_stats19.py` | ✅ Done | Loads 1979-latest CSVs, multi-force filter, pre-filters vehicle/casualty by collision index |
| `ingest/ingest_aadf.py` | ✅ Done | Reads from zip, bidirectional aggregation, bbox filter (replaces region filter), parquet cache |
| `ingest/ingest_webtris.py` | ✅ Done | WebTRIS API, annual reports, per-site-year chunk saves, extended bbox for NW England |
| `ingest/ingest_openroads.py` | ✅ Done | OS Open Roads GeoPackage, study area bbox, road_name_clean + street_name_clean |
| `clean.py` | ✅ Done | LSOA validation, COVID flag, target year filters. Lat/lon used for spatial work; current raw BNG fields cross-check cleanly |
| `snap.py` | ✅ Done | Weighted multi-criteria snap + quick snap, densified geometry KD-tree, ~99.8% match rate |
| `join.py` | ✅ Done | road_link × year table, AADF join, WebTRIS join, snap quality filter (score ≥ 0.6), STATS19 contextual aggregates kept as diagnostics only (excluded from Stage 2 features) |
| `network_features.py` | ✅ Done | Betweenness, degree, dist_to_major, pop_density, betweenness_relative, OSM speed/lanes/surface/lit |
| `features.py` | ✅ Done (legacy) | Deprecated — collision.py builds its own feature table. Self-deprecates on import. |
| `model/aadt.py` | ✅ Done | Stage 1a AADT estimator (counted-only CV R² ~0.83), GroupKFold by count_point_id, applied to 2.1M links |
| `model/timezone_profile.py` | ✅ Done | Stage 1b time-zone fractions (peak/pre-peak/off-peak), GroupKFold by site_id |
| `model/collision.py` | ✅ Done | Stage 2 Poisson GLM + XGBoost (R² 0.858); XGBoost drives risk_percentile; GroupShuffleSplit by link_id |
| `dtc/routes.py` | ✅ Done | GPX + Google Maps → NetworkX routing → ordered link sequences; 174 routes, 24 centres |
| `dtc/analysis.py` | ✅ Done | Per-route features (speed, turns, junctions, risk), DTC aggregation, Pearson correlations vs DVSA Annex D |
| `app/` | 🔄 In progress | Streamlit risk map — functional, performance tuning ongoing |
| `db.py` | ⬜ Not started | PostGIS loader |

---

## Pipeline Run Order

```bash
# 1. Ingest — download raw files first (see data/README.md)
python src/road_risk/ingest/ingest_stats19.py
python src/road_risk/ingest/ingest_aadf.py
python src/road_risk/ingest/ingest_webtris.py   # slow — ~60 mins
python src/road_risk/ingest/ingest_openroads.py

# 2. Convert OSM pbf files (download county files from Geofabrik first)
#    https://download.geofabrik.de/europe/great-britain/england/
for f in data/raw/osm/*.osm.pbf; do
    osmium cat "$f" -o "${f%.osm.pbf}.osm"
done

# 3. Clean
python src/road_risk/clean.py

# 4. Snap collisions to road links
python src/road_risk/snap.py

# 5. Join — build road_link × year feature table
python src/road_risk/join.py

# 6. Network features — run with --osm to include speed/lanes/lit/surface in one pass
#    Re-running with --osm on an existing non-OSM cache auto-triggers recompute
python src/road_risk/network_features.py --osm

# 7. Models
python -m road_risk.model --stage traffic     # Stage 1a: AADT estimator
python -m road_risk.model --stage profile     # Stage 1b: time-zone profiles
python -m road_risk.model --stage collision   # Stage 2: Poisson risk model

# Driving test centre analysis
python src/road_risk/dtc/routes.py            # process GPX + Google Maps routes
python src/road_risk/dtc/analysis.py          # per-centre features + correlations
```

---

## Key Data Quality Findings

See `docs/internal/data-quality-notes.md` for working detail. Summary:

- **STATS19 police force code bug (fixed April 2026)** — `config/settings.yaml`
  previously used codes 4–7 (Lancashire/Merseyside/GM/Cheshire) instead of 12–16
  (Yorkshire). All pipeline outputs before this fix used NW England data.
  Codes are now documented with a derivation snippet using the DfT data guide Excel.

- **STATS19 coordinate handling** — spatial snapping uses `latitude`/`longitude`.
  A previous notebook suspected a Yorkshire BNG grid-square error, but a direct
  check against the current raw DfT STATS19 CSV found no systematic mismatch:
  Yorkshire `location_easting_osgr` / `location_northing_osgr` agree with
  lat/lon-derived BNG positions within a few metres. The stale notebook has
  been archived under `notebooks/old/`.

- **Snap rate ~99.8%** in the current full-area run — achieved after the force
  code fix and weighted multi-criteria snap. A snap quality filter (score ≥ 0.6)
  removes ambiguous matches before annual link aggregation.

- **AADF coverage** — current DfT single-file ingest covers 2015–2024. Stage 1a
  trains on directly Counted AADF rows only, then estimates AADT for every
  Open Roads link × year.

- **OSM coverage** — current `speed_limit_mph` coverage is 56.4% overall and
  59.4% on Unclassified links; `lanes`, `lit`, and surface-derived flags remain
  sparse. Run `src/road_risk/diagnostics/osm_coverage.py` for the class-stratified
  table. Sparse features are median-imputed in the GLM where retained.

---

## Engineering Conventions

- **Post-event provenance guard** — collision-derived context columns must be
  listed explicitly and excluded by guard, not merely omitted from feature
  lists. Stage 2 uses `FORBIDDEN_POST_EVENT_COLS` in `model/collision.py` to
  block `pct_dark`, `pct_urban`, `pct_junction`, `pct_near_crossing`, and
  `mean_speed_limit` from the modelling dataframe, GLM/XGBoost feature lists,
  and `risk_scores.parquet`.

---

## Hardcoded Values — Source Reference

| Value | File | Derivable from? |
|---|---|---|
| Police force codes 12/13/14/16 | `config/settings.yaml`, `ingest_stats19.py` | DfT data guide Excel — `police_force` field |
| HGV vehicle types {19,20,21} | `join.py` | DfT data guide Excel — `vehicle_type` field |
| Road class scores (1=Motorway etc) | `snap.py` | DfT data guide Excel — `first_road_class` field |
| Junction detail codes | `snap.py` | DfT data guide Excel — `junction_detail` field |
| COVID years {2020, 2021} | `clean.py`, `model.py` | Domain knowledge — not in Excel |
| Yorkshire bbox BNG | `ingest_openroads.py` | Spatial — not in Excel |

---

## Model Results Summary

See [methodology site](https://thomashsimm.github.io/open-road-risk/) for feature lists,
performance metrics, and validation detail — kept there to avoid documentation drift in this file.

**Stage 1a — AADT Estimator**
- Counted-only AADF target CV R²: ~0.83 | Applied to 2,167,557 links × 10 years

**Stage 2 — Collision Model**
- Poisson GLM pseudo-R²: 0.251 (in-sample on downsampled training set)
- XGBoost pseudo-R²: 0.858 (out-of-sample, GroupShuffleSplit by link_id)
- **Not directly comparable** — different row subsets, different null models. See methodology site.
- XGBoost drives `risk_percentile`; GLM drives `residual_glm` residual diagnostics
- Metrics are read from `data/models/collision_metrics.json` — that file is canonical

---

## Data Sources

| Source | Location | Coverage |
|---|---|---|
| STATS19 collisions | `data/raw/stats19/` | Northern/Central England 2015–2024 |
| AADF traffic counts | `data/raw/aadf/` | Study area 2015–2024 |
| WebTRIS sensor data | `data/raw/webtris/` | Motorways/trunk 2019, 2021, 2023 |
| OS Open Roads | `data/raw/shapefiles/oproad_gb.gpkg` | Study area + 20km buffer |
| MRDB | `data/raw/shapefiles/MRDB_2024_published.shp` | Study area major roads |
| OSM pbf files | `data/raw/osm/*.osm` | County files from Geofabrik (see `data/raw/osm/`) |
| LSOA population + area | `data/raw/stats19/lsoa_*.csv` | England & Wales 2021 |
| DfT data guide Excel | `data/raw/stats19/dft-road-casualty-*-data-guide-2024.xlsx` | Code lookups |
