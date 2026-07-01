# Open Road Risk

[![DOI](https://zenodo.org/badge/1216505266.svg)](https://doi.org/10.5281/zenodo.20451731)
[![CI](https://github.com/ThomasHSimm/open-road-risk/actions/workflows/ci.yml/badge.svg)](https://github.com/ThomasHSimm/open-road-risk/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Open Road Risk is an open-source road safety pipeline combining DfT STATS19
collision data, AADF traffic counts, OS Open Roads geometry, WebTRIS sensor
data, OpenStreetMap attributes, OS Terrain 50, ONS area context, and MHCLG
deprivation data to produce **exposure-adjusted risk scores
for every road link across Great Britain (England, Scotland, and Wales; not
Northern Ireland)** —
including the large share of roads without direct traffic counters.

- **Current geography:** Great Britain (GB)
- **Time range:** 2015–2024
- **Network size:** 2,167,557 OS Open Roads links; model stages expand this to link × year rows

**Documentation site:** https://openroadrisk.org/

This project was developed with substantial AI assistance under human direction and review. See the project pages for details on the [AI-assisted development methodology](https://openroadrisk.org/project/ai-assisted-development.html).

Open Road Risk is an independent personal research and software project. It uses public/open datasets and is not produced by, endorsed by, or representative of DfT, National Highways, DVSA, Ordnance Survey, Office for National Statistics, or any other public body.

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
The clean full GB retrain completed on 2026-07-01 with XGBoost pseudo-R²
`0.325` out of sample. Earlier repo
documentation cited `~0.86`, but that figure came from a pre-fix evaluation
surface that was later found to be contaminated by feature-table leakage and
should not be used for current project positioning.
The GLM (pseudo-R² `0.566`, in-sample on a 1:3 zero-collision downsampled
training set) provides interpretable coefficients and diagnostic residuals.
Features include a tiered
speed limit imputation (`speed_limit_mph_effective`), GB within-country
deprivation deciles, GB rural/urban context, population density, and
`mean_grade`, with GLM optional-feature imputation keeping the training
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
#    GB boundary, WebTRIS data or API access, OSM pbf files,
#    OS Terrain 50 tiles, ONS population/RUC files, and IMD/WIMD/SIMD inputs.
conda run -n env1 python scripts/download_gb_boundary.py

# Full GB OSM is large (~2.0 GB as of 2026-06-30); download only when needed.
curl -L -o data/raw/osm/great-britain-latest.osm.pbf \
  https://download.geofabrik.de/europe/great-britain-latest.osm.pbf

# 3. Ingest source files
conda run -n env1 python src/road_risk/ingest/ingest_stats19.py
conda run -n env1 python src/road_risk/ingest/ingest_aadf.py
conda run -n env1 python src/road_risk/ingest/ingest_webtris.py   # slow if pulling from API
conda run -n env1 python src/road_risk/ingest/ingest_openroads.py

# 4. Convert OSM pbf files
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
| GB boundary | ONS Open Geography Portal | Country polygon | England, Scotland, Wales |
| OS Open Roads | Ordnance Survey | Road link geometry | GB |
| Network Model GDB | National Highways | Link + related tables | Strategic Road Network only; source notes and scoped structural-feature candidate |
| OS Terrain 50 | Ordnance Survey | 50 m elevation grid | GB — terrain grade features |
| WebTRIS sensor reports | National Highways | Site / month, cleaned to site × year | National Highways network; current pull uses 2019, 2021, 2023 |
| OpenStreetMap | OSM contributors | Road edge | GB — speed, lanes, surface |
| OA population density context | ONS / National Records of Scotland | OA polygon | GB — `data/processed/context/oa_population_density_gb.parquet`; assigned by road-link centroid with a short nearest fallback |
| GB rural-urban context | ONS / Scottish Government | LSOA 2021 / SGUR 2022 polygon | England/Wales ONS 2021 RUC + Scotland Urban Rural Classification 2022 |
| GB deprivation context | MHCLG / Welsh Government / Scottish Government | LSOA / Data Zone polygon | England IoD 2025, Wales WIMD 2019, Scotland SIMD 2020v2; deciles are within-country only |

Large raw files are not tracked in git.

---

## Repo Structure

```
open-road-risk/
├── src/road_risk/
│   ├── ingest/              # Source ingestion (STATS19, AADF, WebTRIS, OS Roads)
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
| Poisson GLM pseudo-R² | 0.566 (clean full GB run; in-sample on 1:3 zero-collision downsampled training set; not directly comparable to XGBoost or earlier 1:10 runs) |
| XGBoost pseudo-R² | 0.325 (clean full GB run; out-of-sample with temporal features included) |

---

## Key Data Quality Notes

- **STATS19 force-code selection bug (fixed April 2026, retired for GB runs)** — the original
  Yorkshire pilot accidentally used police-force codes 4–7
  (Lancashire, Merseyside, Greater Manchester, Cheshire) instead of the
  Yorkshire codes 12, 13, 14, and 16. The current project has since expanded
  beyond police-force geography. `ingest_stats19.py` now selects GB collisions
  by valid lat/lon plus the configured GB boundary, not by `police_force`.

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

- **Grade structure handling (not yet active)** — `mean_grade` is sampled from the
  OS Terrain 50 bare-earth DTM. Structure correction for bridges/tunnels/slip roads
  is coded but inactive in the current build (the OSM structure file is absent and
  slip roads are unwired), so `grade_method = profile` for all links. Grade on
  structure-carrying links may be wrong; the per-link `grade_method` column flags
  this for future correction.

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

## How to cite

Simm, T. H. (2026). *Open Road Risk: an open-data pipeline for exposure-adjusted
collision risk across the Great Britain road network.*
Zenodo. https://doi.org/10.5281/zenodo.20451731

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
