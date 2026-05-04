# Open Road Risk

Open Road Risk is an open-source road safety pipeline combining DfT STATS19
collision data, AADF traffic counts, OS Open Roads geometry, WebTRIS sensor
data, and OpenStreetMap attributes to produce **exposure-adjusted risk scores
for every road link across a Northern and Central England study area** —
including the large share of roads without direct traffic counters.

- **Current geography:** Yorkshire, NW England, North East, Midlands, and parts of East England
- **Time range:** 2015–2024
- **Network size:** 2,167,557 OS Open Roads links; model stages expand this to link × year rows

**Documentation site:** https://thomashsimm.github.io/open-road-risk/

This project was developed with substantial AI assistance under human direction and review. See the project pages for details on the [AI-assisted development methodology](https://thomashsimm.github.io/open-road-risk/project/ai-assisted-development.html).

---

## What this builds

**Stage 1a — Traffic estimation**  
Predicts AADT (annual average daily traffic) for all 2.1M road links using a gradient
boosting model trained on AADF count points. Fills coverage gaps on minor/unclassified
roads where DfT has no measured counts. The current training run uses directly Counted
AADF rows only across 2015-2024. CV R² ~0.83 with features including road class,
location, link length, HGV proportion, network position, population density, and
available OSM attributes.

**Stage 1b — Time-zone profiles**  
Uses WebTRIS National Highways sensor reports to learn within-day traffic
shape (peak / pre-peak / off-peak fractions). The cleaned WebTRIS table is
sparse by design: current local data has 15,011 site × year rows from 5,948
sensor sites for 2019, 2021, and 2023. The profile model then applies those
learned fractions to all links using estimated AADT and network features,
producing `timezone_profiles.parquet`. These profiles are currently a
separate output for temporal analysis and future exposure weighting; they are
not part of the current Stage 2 collision feature set.

**Stage 2 — Collision risk model** Poisson GLM + XGBoost predicting collision counts per link per year.
Uses `log(AADT × length_km × 365 / 1e6)` as exposure offset so the model learns
*which roads are dangerous given their traffic* — not just which are busy.
XGBoost drives the final risk percentile ranking (`risk_scores.parquet`).
The current honest post-fix baseline is pseudo-R² `0.323` out of sample,
measured as the mean across five seeds with temporal features included
(`0.321-0.327` range). Earlier repo
documentation cited `~0.86`, but that figure came from a pre-fix evaluation
surface that was later found to be contaminated by feature-table leakage and
should not be used for current project positioning.
The GLM (pseudo-R² 0.3472, in-sample on downsampled training set) provides
interpretable coefficients and diagnostic residuals. Features include a tiered
speed limit imputation (`speed_limit_mph_effective`), IMD deprivation deciles,
and `mean_grade`, with GLM optional-feature imputation keeping the training
population stable across feature additions.

*Experimental variants for Empirical Bayes (EB) shrinkage (`risk_scores_eb.parquet`) and a Facility-Family split (`risk_scores_family.parquet`) are also generated for diagnostic comparison.*

---

## Quick Start

```bash
# 1. Clone and install
git clone <repo>
cd open-road-risk
pip install -e ".[dev]"

# 2. Download raw data into data/raw/
#    Required: STATS19 CSV, AADF zip, OS Open Roads GeoPackage,
#    WebTRIS data or API access, OSM pbf files, and MRDB.

# 3. Ingest source files
python src/road_risk/ingest/ingest_stats19.py
python src/road_risk/ingest/ingest_aadf.py
python src/road_risk/ingest/ingest_webtris.py   # slow if pulling from API
python src/road_risk/ingest/ingest_mrdb.py
python src/road_risk/ingest/ingest_openroads.py

# 4. Convert OSM pbf files (download study-area county files from Geofabrik first)
sudo apt install osmium-tool
for f in data/raw/osm/*.osm.pbf; do
    osmium cat "$f" -o "${f%.osm.pbf}.osm"
done

# 5. Run pipeline in order
python src/road_risk/clean_join/clean.py
python src/road_risk/clean_join/snap.py
python src/road_risk/clean_join/join.py
python src/road_risk/features/network.py --osm   # graph + OSM features (~25 mins first run)

python -m road_risk.model --stage traffic     # Stage 1a: AADT estimator
python -m road_risk.model --stage profile     # Stage 1b: time-zone profiles
python -m road_risk.model --stage collision   # Stage 2: Poisson risk model
```

---

## Data Sources

| Source | Provider | Granularity | Coverage |
|---|---|---|---|
| STATS19 (collisions, vehicles, casualties) | DfT | Per incident | GB 1979– |
| AADF by direction | DfT | Count point / year | GB — major + some minor |
| OS Open Roads | Ordnance Survey | Road link geometry | GB |
| WebTRIS sensor reports | National Highways | Site / month, cleaned to site × year | National Highways network; current pull uses 2019, 2021, 2023 |
| OpenStreetMap | OSM contributors | Road edge | GB — speed, lanes, surface |
| LSOA population + area | ONS | LSOA 2021 | England & Wales |

Large raw files are not tracked in git.

---

## Repo Structure

```
open-road-risk/
├── src/road_risk/
│   ├── ingest/              # Source ingestion (STATS19, AADF, WebTRIS, MRDB, OS Roads)
│   ├── clean_join/          # Cleaned source tables, collision snapping, annual joins
│   │   ├── clean.py         # Coordinate validation, COVID flags, WebTRIS aggregation
│   │   ├── snap.py          # Collision -> road link snapping (weighted multi-criteria)
│   │   └── join.py          # Build road_link x year feature table
│   ├── features/            # Link-level feature builders and legacy feature helper
│   │   ├── network.py       # Graph centrality, OSM attributes, population density
│   │   ├── road_curvature.py  # Curvature features from Open Roads geometry
│   │   ├── road_terrain.py  # Grade features from OS Terrain 50
│   │   └── legacy.py        # Deprecated old model feature table builder
│   ├── model/               # Modelling package (CLI: python -m road_risk.model)
│   │   ├── main.py          # --stage traffic|profile|collision|all
│   │   ├── aadt.py          # Stage 1a: AADT estimator
│   │   ├── timezone_profile.py  # Stage 1b: time-zone fractions
│   │   ├── collision.py     # Stage 2: Poisson GLM + XGBoost
│   │   ├── eb_*.py          # Empirical Bayes shrinkage diagnostics/output
│   │   ├── family_split.py  # Facility-family model diagnostics
│   │   └── rank_stability.py # Multi-seed ranking stability harness
│   ├── app/                 # Streamlit risk map app
│   ├── diagnostics/         # Validation/report builders
│   ├── utils/               # Shared logging/helpers
│   ├── config.py            # YAML loader, paths
│   └── eda_collision_model.py
├── docs/                    # Internal notes, design rationale, research notes
├── reports/                 # Validation reports and supporting CSVs
├── quarto/                  # Documentation site (Quarto)
├── tests/                   # Fast unit/smoke tests
├── data/
│   ├── raw/                 # Source files — never modified, not in git
│   ├── processed/           # Cleaned parquets
│   ├── features/            # Model-ready feature tables
│   ├── provenance/          # Committable provenance JSONs
│   └── models/              # Saved model artefacts + risk scores
└── config/settings.yaml     # Police force codes, year ranges, paths
```

---

## Key Results (May 2026)

| Metric | Value |
|---|---|
| Collisions loaded (2015–2024) | 203,928 |
| Collisions snapped to road links | ~99.8% |
| Mean snap score | 0.860 |
| Road links scored (full network) | 2,167,557 |
| AADT estimator CV R² | ~0.83 (counted-only AADF rows) |
| Poisson GLM pseudo-R² | 0.3472 (verified post-fix; in-sample, downsampled training set; not directly comparable to XGBoost) |
| XGBoost pseudo-R² | 0.3235 mean across 5 post-fix seeds with temporal features included (range 0.3214-0.3265) |

---

## Key Data Quality Notes

- **STATS19 force-code selection bug (fixed April 2026)** — the original
  Yorkshire pilot accidentally used police-force codes 4–7
  (Lancashire, Merseyside, Greater Manchester, Cheshire) instead of the
  Yorkshire codes 12, 13, 14, and 16. The current project has since expanded
  beyond Yorkshire, and `config/settings.yaml` now intentionally lists the full
  multi-force study area.

- **Snap rate ~99.8%** — achieved in the current full-area run after the force
  code fix and weighted snap. Previous 40.6% ceiling was because NW England
  collisions were snapping to NW England roads in the 20km buffer zone.

- **AADF training signal** — AADF ingest covers 2015-2024, but Stage 1a trains
  only on directly Counted rows. This drops 1,288 count points with no Counted
  observation in the training window and avoids learning from DfT-interpolated
  targets.

- **OSM attribute coverage** — Raw speed limit is 56.4%, but a tiered imputation 
  keyed off OS road classifications provides a `speed_limit_mph_effective` coverage 
  of 91.27%. `lanes` (7.3%), `lit` (9.3%), and surface flags (16.2%) remain 
  sparse and are median-imputed where retained in the GLM.

Detailed working notes are kept in `docs/internal/data-quality-notes.md`.

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

Python dependencies are declared in `pyproject.toml`. The main groups are:

- Data/geospatial: `pandas`, `geopandas`, `pyarrow`, `shapely`, `pyproj`,
  `rasterio`, `numpy`, `scipy`
- WebTRIS/API/progress: `pytris`, `requests`, `tqdm`
- Modelling: `scikit-learn`, `statsmodels`, `xgboost`, `shap`,
  `imbalanced-learn`
- Network/OSM: `networkx`, `osmnx`
- Visualisation/app: `matplotlib`, `seaborn`, `plotly`, `folium`,
  `streamlit`, `streamlit-folium`, `contextily`

The OSM conversion step also needs the system CLI `osmium-tool`
(`sudo apt install osmium-tool` on Ubuntu/Debian).
