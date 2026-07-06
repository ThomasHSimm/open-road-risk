# Open Road Risk GB link risk and exposure GIS export

This folder contains a QGIS-ready full-GB link-level export built from existing Open Road Risk outputs.

Primary GeoPackage:

`data/exports/gis/open-road-risk-gb-link-risk-exposure.gpkg`

Layer:

`gb_link_risk_exposure`

The layer has one row per scored OS Open Roads link. It joins modelled risk scores, observed retained collision counts, estimated traffic exposure, broad road metadata, deprivation country, and line geometry. GeoPackage is preferred over GeoJSON for the full GB network because it handles millions of line features, typed columns, spatial indexing, and QGIS loading much more reliably.

Public Kaggle Dataset:

https://www.kaggle.com/datasets/thomassimm/open-road-risk-gb-link-risk-exposure-gis/

## Rebuild command

From the repository root:

```bash
PYTHONPATH=src python -m road_risk.outputs.gis_link_export
```

The script consumes existing parquet outputs only. It does not rerun STATS19 processing, snapping, joining, traffic processing, AADT modelling, collision model training, or scoring.

## Source data

- `data/models/risk_scores.parquet`
- `data/models/risk_scores_eb.parquet`, when `predicted_eb` is available
- `data/processed/shapefiles/openroads.parquet`
- `data/features/network_features.parquet`

## Fields

- `link_id`: OS Open Roads link identifier.
- `risk_percentile`: modelled risk percentile from the production risk score table; higher means higher modelled risk.
- `risk_decile`: integer decile derived from `risk_percentile`, where 10 is the highest-risk decile.
- `global_risk_rank`: full-network rank derived from `risk_percentile`, with highest modelled risk ranked 1.
- `predicted_xgb`: XGBoost model predicted collision count/risk score from the scoring artifact.
- `predicted_eb`: empirical-Bayes-smoothed prediction where available; null where the EB artifact has no row.
- `estimated_aadt`: estimated average annual daily traffic used by the model.
- `link_length_km`: OS Open Roads link length in kilometres.
- `exposure_vehicle_km_year`: annual vehicle-kilometre exposure estimate.
- `collision_count`: retained observed collision count in the model scoring window.
- `fatal_count`: retained fatal collision count in the model scoring window.
- `serious_count`: retained serious collision count in the model scoring window.
- `crude_rate_per_million_vkm`: crude observed collision count divided by annual vehicle-km exposure, multiplied by 1,000,000.
- `road_classification`: broad OS road classification.
- `road_function`: OS road function.
- `family`: broad facility family used for reporting context.
- `road_archetype`: reporting convenience combining family and broad road class.
- `form_of_way`: OS form-of-way description.
- `deprivation_country`: deprivation framework country assigned to the link.
- `calibration_caveat`: semicolon-separated screening caveats such as motorway calibration, low exposure, or sparse collision history.
- `is_top_1pct`: true where `risk_percentile >= 99`.
- `is_top_5pct`: true where `risk_percentile >= 95`.
- `is_top_decile`: true where `risk_percentile >= 90`.
- `geometry`: WGS84 line geometry for the OS Open Roads link.

## Formulas

`exposure_vehicle_km_year = estimated_aadt x link_length_km x 365`

`crude_rate_per_million_vkm = collision_count / exposure_vehicle_km_year x 1,000,000`

If exposure is zero, missing, or invalid, `crude_rate_per_million_vkm` is left null.

`risk_decile` is derived from `risk_percentile` on a 1-10 scale, with decile 10 representing `risk_percentile >= 90`.

`global_risk_rank` is derived by sorting `risk_percentile` descending and `link_id` ascending for stable tie handling.

## Interpretation cautions

This is a screening and research dataset. It is not causal proof, a road safety engineering audit, a substitute for site investigation, or a guarantee of future collisions.

Modelled risk is not the same as crude observed collisions per vehicle-km. The modelled score combines exposure, road context, and learned network patterns, while the crude rate is a simple observed-count ratio that can be unstable.

Absence from the top risk bands does not mean a road is safe. It only means the link is not in the highest modelled-risk bands under this scoring surface.

Sparse collision counts and short links require caution. Small denominators can create very large crude rates, and many links have little or no direct collision history.

`collision_count`, `fatal_count`, and `serious_count` are retained model-window counts at link grain. The requested crude exposure denominator is annual vehicle-km, so the crude rate should be read as a screening indicator rather than an audited annual collision rate.

## QGIS styles

Two lightweight QGIS style files are written beside the GeoPackage:

- `risk_decile.qml`
- `crude_collision_rate.qml`

In QGIS, load the GeoPackage layer, then use Layer Properties -> Symbology -> Style -> Load Style to apply either style.

## How to cite

Simm, T. H. (2026). *Open Road Risk: an open-data pipeline for exposure-adjusted collision risk across the Great Britain road network*. Zenodo. https://doi.org/10.5281/zenodo.20451731

## Licence and attribution

This GeoPackage is a derived export from multiple open-data sources and Open Road Risk processing/model outputs. It should not be treated as having one simple standalone licence that overrides upstream terms. Users are responsible for preserving applicable attribution, copyright, database-right, and licence requirements for the source data used in any onward use or redistribution.

Suggested attribution text:

- Contains OS data © Crown copyright and database right.
- Contains public sector information licensed under the Open Government Licence v3.0.
- Contains OpenStreetMap-derived information where OSM-derived features are used; OpenStreetMap data is available under the Open Database Licence.
- Open Road Risk processing, modelling code, and export logic: Thomas H. Simm / Open Road Risk.

When publishing maps, extracts, derivative datasets, or analysis based on this export, include source-specific attribution appropriate to the fields and geography used. If redistributing a modified or subsetted dataset, check the relevant upstream licences and preserve required notices.


