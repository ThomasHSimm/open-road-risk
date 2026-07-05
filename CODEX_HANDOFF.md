# Open Road Risk Codex handoff

## Current branch/work

We are updating full-GB outputs and documentation after fixing stale output coverage.

Do not rerun STATS19, snapping, joining, traffic, AADT, or collision modelling unless explicitly asked.

Do not inspect or edit huge generated files unless necessary. Avoid reading full GeoJSON/HTML outputs into context.

Prefer small source/docs edits. Render only the single page being changed when testing.

Do not commit raw data, logs, parquet outputs, or huge generated artefacts unless explicitly requested.

## Validated full-GB model/output state

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

## Top-risk map status

The model files were already full GB. The stale/England-biased layer was:

- `data/outputs/top_1pct_risk_segments.parquet`

It has now been regenerated from current full-GB `data/models/risk_scores.parquet`.

Current regenerated bounds:

- `top_1pct_risk_segments.parquet`: `[-6.297683, 50.023067, 1.751146, 60.323022]`
- `data/outputs/web/top_1pct_risk_segments.geojson`: `[-6.29768, 50.02307, 1.75115, 60.32302]`

Current regenerated top-risk country counts:

- England: 37,959
- Scotland: 893
- Wales: 548
- missing: 13

Context layers were also regenerated from current GB scores:

- features: 597,072
- files: 33
- bounds: `[-7.51646, 49.9119, 1.75939, 60.78527]`

Commands already run:

```bash
python -m road_risk.outputs.top_risk_web
python scripts/build_context_web.py
conda run --no-capture-output -n env1 quarto render quarto/outputs/top-risk-map.qmd