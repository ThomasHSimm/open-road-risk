# Road Risk Analysis

Open-source road safety pipeline combining DfT STATS19 collision data, AADF traffic counts,
OS Open Roads network geometry, and OpenStreetMap attributes to produce **exposure-adjusted
risk scores for every road link across Northern and Central England** — including the ~85%
of roads without traffic counters.

**Current geography:** Yorkshire, NW England, Midlands (expanding)  
**Time range:** 2015–2024  
**Grain:** OS Open Roads link × year (2,167,557 links)

---

## What this builds

**Stage 1a — Traffic estimation**  
Predicts AADT (annual average daily traffic) for all 2.1M road links using a gradient
boosting model trained on AADF count points. Fills coverage gaps on minor/unclassified
roads where DfT has no measured counts. The current training run uses directly Counted
AADF rows only across 2015-2024. CV R² ~0.83 with features including network
centrality, OSM speed limits, population density, HGV proportion, and betweenness.

**Stage 1b — Time-zone profiles**  
Estimates daily traffic shape (peak / pre-peak / off-peak fractions) for every road
link using WebTRIS sensor data as training. Supports per-hour flow reconstruction and
future temporal exposure weighting in the collision model.

**Stage 2 — Collision risk model**  
Poisson GLM + XGBoost predicting collision counts per link per year.
Uses `log(AADT × length_km × 365 / 1e6)` as exposure offset so the model learns
*which roads are dangerous given their traffic* — not just which are busy.
XGBoost (pseudo-R² 0.858, out-of-sample) drives the final risk percentile ranking;
the GLM (pseudo-R² 0.251, in-sample on downsampled training set) provides
interpretable coefficients and diagnostic residuals. Note: the two pseudo-R² values
are not computed on a common evaluation set and are not directly comparable.

**Driving test route analysis**  
Routes from 24 DVSA test centres (174 routes, Google Maps + GPX) are snapped to the
road network and scored. Per-centre risk and road-environment features are correlated
with DVSA Annex D fault rates to identify which road characteristics drive test outcomes.

---

## Quick Start

```bash
# 1. Clone and install
git clone <repo>
cd road-risk-analysis
pip install -e ".[dev]"

# 2. Download raw data — see data/README.md for links
#    Required: STATS19 CSV, AADF zip, OS Open Roads GeoPackage, MRDB, OSM pbf files

# 3. Convert OSM pbf files (download Yorkshire counties from Geofabrik first)
sudo apt install osmium-tool
for f in data/raw/osm/*.osm.pbf; do
    osmium cat "$f" -o "${f%.osm.pbf}.osm"
done

# 4. Run pipeline in order
python src/road_risk/clean.py
python src/road_risk/snap.py
python src/road_risk/join.py
python src/road_risk/network_features.py --osm   # graph + OSM features (~25 mins first run)

python -m road_risk.model --stage traffic     # Stage 1a: AADT estimator
python -m road_risk.model --stage profile     # Stage 1b: time-zone profiles
python -m road_risk.model --stage collision   # Stage 2: Poisson risk model

# Optional: driving test route analysis
python src/road_risk/dtc/routes.py            # snap GPX/Google Maps routes
python src/road_risk/dtc/analysis.py          # per-centre features + correlations
```

---

## Data Sources

| Source | Provider | Granularity | Coverage |
|---|---|---|---|
| STATS19 (collisions, vehicles, casualties) | DfT | Per incident | GB 1979– |
| AADF by direction | DfT | Count point / year | GB — major + some minor |
| OS Open Roads | Ordnance Survey | Road link geometry | GB |
| Major Road Database (MRDB) | DfT / OS | Road geometry | GB |
| WebTRIS / MIDAS | National Highways | Site / month | Motorways + trunk A-roads |
| OpenStreetMap | OSM contributors | Road edge | GB — speed, lanes, surface |
| LSOA population + area | ONS | LSOA 2021 | England & Wales |

See `data/README.md` for download instructions.

---

## Repo Structure

```
road-risk-analysis/
├── src/road_risk/
│   ├── ingest/              # Data ingestion (STATS19, AADF, WebTRIS, MRDB, OS Roads)
│   ├── model/               # Model package (CLI: python -m road_risk.model)
│   │   ├── main.py          # --stage traffic|profile|collision|all
│   │   ├── aadt.py          # Stage 1a: AADT estimator
│   │   ├── timezone_profile.py  # Stage 1b: time-zone fractions
│   │   └── collision.py     # Stage 2: Poisson GLM + XGBoost
│   ├── dtc/                 # Driving test centre analysis
│   │   ├── routes.py        # GPX/Google Maps → link sequences (NetworkX)
│   │   └── analysis.py      # Per-route features, DTC aggregation, correlations
│   ├── app/                 # Streamlit risk map app
│   ├── config.py            # YAML loader, paths
│   ├── clean.py             # Coordinate validation, COVID flags
│   ├── snap.py              # Collision → road link snapping (weighted multi-criteria)
│   ├── join.py              # Build road_link × year feature table
│   └── network_features.py  # Graph centrality, OSM attributes, population density
├── quarto/                  # Documentation site (Quarto)
├── data/
│   ├── raw/                 # Source files — never modified, not in git
│   ├── processed/           # Cleaned parquets
│   ├── features/            # Model-ready feature tables
│   └── models/              # Saved model artefacts + risk scores
└── config/settings.yaml     # Police force codes, year ranges, paths
```

---

## Key Results (April 2026)

| Metric | Value |
|---|---|
| Collisions loaded (2015–2024) | 203,928 |
| Collisions snapped to road links | ~99.8% |
| Mean snap score | 0.860 |
| Road links scored (full network) | 2,167,557 |
| AADT estimator CV R² | ~0.83 (counted-only AADF rows) |
| Poisson GLM pseudo-R² | 0.251 (in-sample, downsampled training set) |
| XGBoost pseudo-R² | 0.858 |
| DTC routes processed | 174 across 24 centres |

---

## Key Data Quality Notes

- **STATS19 force code bug (fixed April 2026)** — `config/settings.yaml` previously
  used police_force codes 4–7 (Lancashire, Merseyside, Greater Manchester, Cheshire)
  instead of the correct Yorkshire codes 12–16. This caused the entire pipeline to load
  NW England data. Now fixed and documented in `config/settings.yaml` with instructions
  to re-derive codes from the DfT data guide Excel.

- **Snap rate ~99.8%** — achieved in the current full-area run after the force
  code fix and weighted snap. Previous 40.6% ceiling was because NW England
  collisions were snapping to NW England roads in the 20km buffer zone.

- **AADF training signal** — AADF ingest covers 2015-2024, but Stage 1a trains
  only on directly Counted rows. This drops 1,288 count points with no Counted
  observation in the training window and avoids learning from DfT-interpolated
  targets.

- **OSM attribute coverage** — speed limit 56.4%, lanes 7.3%, lit 9.3%,
  unpaved/surface flag 16.2%. The current Stage 2 run includes OSM speed in both
  GLM and XGBoost; sparse OSM attributes are imputed or used only where present.

Detailed working notes are currently kept in
`docs/internal/data-quality-notes.md` and can be promoted back into the Quarto
site once the relevant code paths are clearer.

---

## STATS19 Coordinate Handling

The pipeline uses STATS19 `latitude` / `longitude` fields for collision
snapping and spatial validation. A previous investigation suspected a Yorkshire
BNG grid-square error in `location_easting_osgr` / `location_northing_osgr`, but
a direct check against the current raw DfT STATS19 CSV found no systematic
mismatch: Yorkshire force coordinates agree with lat/lon-derived BNG positions
within a few metres. The earlier issue was likely a consequence of the
now-fixed police-force-code selection bug.

---

## Positioning

This pipeline produces **Safety Performance Functions (SPFs)** for the full road network
using open data — extending exposure-adjusted risk analysis to the 85% of roads where
DfT currently has no traffic counts.

Compatible with ESRI/ArcGIS workflows via GeoPackage output. PostGIS backend for app queries.

---

## Requirements

```
geopandas, pandas, numpy, scikit-learn, networkx, scipy, pyproj
statsmodels    # Stage 2 Poisson GLM
xgboost        # Stage 2 XGBoost
osmnx          # OSM network features
osmium-tool    # CLI — convert pbf to osm (apt install osmium-tool)
streamlit      # App (optional)
```
