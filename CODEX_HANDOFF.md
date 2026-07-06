# Open Road Risk Codex handoff

Current branch/work:
- We are updating full-GB outputs and documentation after fixing stale STATS19 coverage.
- Do not rerun STATS19, snap, join, traffic, AADT, or collision modelling unless explicitly asked.
- Do not inspect or edit huge generated files unless necessary.
- Avoid reading full GeoJSON/HTML outputs into context.

Validated full-GB model/output state:
- Open Roads links: 3,941,299
- Link-years: 39,412,990
- Processed STATS19 collision rows: 1,148,857
- Retained collisions in road_link_annual: 1,145,198
- Positive road-link-year rows: 945,373
- Unique links with observed retained collisions: 531,442
- XGBoost zero policy: full
- XGBoost pseudo-R²: 0.360
- GLM pseudo-R²: 0.505
- Risk-score rows: 3,941,299
- Top 1% risk links: 39,413

GIS/Kaggle release state:
- Full link-level GIS export script: `src/road_risk/outputs/gis_link_export.py`.
- Local GeoPackage target: `data/exports/gis/open-road-risk-gb-link-risk-exposure.gpkg` (large, ignored by git).
- Public Kaggle Dataset: https://www.kaggle.com/datasets/thomassimm/open-road-risk-gb-link-risk-exposure-gis/
- Public demo notebook: `notebooks/open-road-risk-gis-export-for-qgis.ipynb`; keep outputs and attachments cleared so Kaggle source stays below 1 MB.

Known issues:
- Key figures now use a GB-wide reporting-area layer, but dissolve/grouping policy is still rough.
- Old partial `areas_study.geojson` should not drive final full-GB named areas.
- Named reporting areas are a display geography only.
- The 10 km grid is the primary consistent GB comparison geography.
- Raw XGBoost predicted counts are somewhat high on average; risk percentiles/deciles are the safer public output.

Working rule:
- Prefer small source/docs edits.
- Render only the single page being changed when testing.
- Do not commit raw data, logs, parquet outputs, or huge generated artefacts unless explicitly requested.
