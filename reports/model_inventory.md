# Model Inventory

**Date:** 24 April 2026  
**Status:** Refreshed after the Stage 2 effective-speed retrain.  
**Canonical metrics source:** `data/models/collision_metrics.json`

## Stage 2 - Collision Risk Model

Implementation: `src/road_risk/model/collision.py`

### Training Data

| Item | Value | Source |
|---|---:|---|
| Link-year modelling table | 21,675,570 | `xgb.n_train + xgb.n_test` |
| GLM complete-case rows before downsampling | 18,302,830 | `glm.n_full` |
| GLM training rows after downsampling | 3,967,414 | `glm.n_obs` |
| GLM positive rows | 360,674 | `glm.n_pos` |
| XGBoost training rows | 17,340,450 | `xgb.n_train` |
| XGBoost test rows | 4,335,120 | `xgb.n_test` |

The GLM keeps complete cases for its feature set, then downsamples
zero-collision rows to 10x positives. XGBoost trains on the full Stage 2 table
with missing model features filled to 0.

### GLM Features

From `collision_metrics.json -> glm.features`:

| # | Feature | Category |
|---:|---|---|
| 1 | `road_class_ord` | Road structure |
| 2 | `form_of_way_ord` | Road structure |
| 3 | `is_motorway` | Binary flag |
| 4 | `is_a_road` | Binary flag |
| 5 | `is_slip_road` | Binary flag |
| 6 | `is_roundabout` | Binary flag |
| 7 | `is_dual` | Binary flag |
| 8 | `is_trunk` | Binary flag |
| 9 | `is_primary` | Binary flag |
| 10 | `log_link_length` | Geometry |
| 11 | `is_covid` | Temporal |
| 12 | `year_norm` | Temporal |
| 13 | `degree_mean` | Network |
| 14 | `betweenness` | Network |
| 15 | `betweenness_relative` | Network |
| 16 | `dist_to_major_km` | Network |
| 17 | `pop_density_per_km2` | Network/context |
| 18 | `speed_limit_mph_effective` | Speed limit |
| 19 | `lanes_imputed` | OSM, median-imputed |
| 20 | `is_unpaved_imputed` | OSM, median-imputed |

Raw `speed_limit_mph` is retained in the Stage 2 dataframe and scored output as
provenance, but is not a model feature.

### GLM Metrics

| Metric | Value |
|---|---:|
| Pseudo-R2 | 0.3013 |
| Deviance | 1,376,539 |
| Null deviance | 1,970,118 |
| AIC | 2,126,878 |
| Converged | Yes |

### XGBoost Features

From `collision_metrics.json -> xgb.features`:

| # | Feature | Category |
|---:|---|---|
| 1 | `road_class_ord` | Road structure |
| 2 | `form_of_way_ord` | Road structure |
| 3 | `is_motorway` | Binary flag |
| 4 | `is_a_road` | Binary flag |
| 5 | `is_slip_road` | Binary flag |
| 6 | `is_roundabout` | Binary flag |
| 7 | `is_dual` | Binary flag |
| 8 | `is_trunk` | Binary flag |
| 9 | `is_primary` | Binary flag |
| 10 | `log_link_length` | Geometry |
| 11 | `estimated_aadt` | Exposure |
| 12 | `is_covid` | Temporal |
| 13 | `year_norm` | Temporal |
| 14 | `hgv_proportion` | Traffic |
| 15 | `degree_mean` | Network |
| 16 | `betweenness` | Network |
| 17 | `betweenness_relative` | Network |
| 18 | `dist_to_major_km` | Network |
| 19 | `pop_density_per_km2` | Network/context |
| 20 | `speed_limit_mph_effective` | Speed limit |
| 21 | `lanes` | OSM |
| 22 | `is_unpaved` | OSM |

Raw `speed_limit_mph` is not in the XGBoost feature list.

### XGBoost Metrics

| Metric | Value |
|---|---:|
| Pseudo-R2 | 0.3235 mean across 5 post-fix seeds with temporal features included |
| Test deviance | 104,503 |

### Output And Rank Stability

`data/models/risk_scores.parquet` contains 2,167,557 scored links. The top 1%
set contains 21,676 links.

Compared with `data/models/risk_scores_pre_effective_speed.parquet`, the
effective-speed retrain had Spearman rank correlation **0.9962** across all
links and top-1% Jaccard overlap **0.9512**. The top-1% intersection was
21,134 links.
