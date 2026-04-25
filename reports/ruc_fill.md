# RUC Fill Report

This report documents the characterisation, Stage 2 exclusion diagnosis, and fill applied to the `data/features/network_features.parquet` LSOA-derived feature gap. The starting issue was `335,692` links with `pop_density_per_km2`, `ruc_class`, and `ruc_urban_rural` all null. The original file was backed up to `data/features/network_features_pre_ruc_fill.parquet` before any write.

## Stage 1: Characterisation

Exact no-LSOA count: `335,692` of `2,167,557` links (`15.49%`). The null pattern is complete: the same links have null `pop_density_per_km2`, `ruc_class`, and `ruc_urban_rural`.

Road-function comparison:

| road_function                |   full_count | full_pct   |   no_lsoa_count | no_lsoa_pct   | no_lsoa_share_of_category_pct   |
|:-----------------------------|-------------:|:-----------|----------------:|:--------------|:--------------------------------|
| Restricted Local Access Road |      451,126 | 20.81%     |         142,087 | 42.33%        | 31.50%                          |
| Minor Road                   |      378,407 | 17.46%     |         101,435 | 30.22%        | 26.81%                          |
| Local Road                   |      983,644 | 45.38%     |          47,516 | 14.15%        | 4.83%                           |
| A Road                       |      155,534 | 7.18%      |          21,847 | 6.51%         | 14.05%                          |
| B Road                       |       89,286 | 4.12%      |          17,411 | 5.19%         | 19.50%                          |
| Local Access Road            |       23,862 | 1.10%      |           3,084 | 0.92%         | 12.92%                          |
| Secondary Access Road        |       81,614 | 3.77%      |           1,739 | 0.52%         | 2.13%                           |
| Motorway                     |        4,084 | 0.19%      |             573 | 0.17%         | 14.03%                          |

Form-of-way comparison:

| form_of_way                |   full_count | full_pct   |   no_lsoa_count | no_lsoa_pct   | no_lsoa_share_of_category_pct   |
|:---------------------------|-------------:|:-----------|----------------:|:--------------|:--------------------------------|
| Single Carriageway         |    2,081,815 | 96.04%     |         330,311 | 98.40%        | 15.87%                          |
| Roundabout                 |       32,903 | 1.52%      |           2,116 | 0.63%         | 6.43%                           |
| Collapsed Dual Carriageway |       32,345 | 1.49%      |           1,950 | 0.58%         | 6.03%                           |
| Slip Road                  |       12,234 | 0.56%      |             989 | 0.29%         | 8.08%                           |
| Dual Carriageway           |        6,123 | 0.28%      |             296 | 0.09%         | 4.83%                           |
| Shared Use Carriageway     |        2,001 | 0.09%      |              30 | 0.01%         | 1.50%                           |
| Guided Busway              |          136 | 0.01%      |               0 | 0.00%         | 0.00%                           |

Nearest LSOA centroid distance for no-LSOA links:

| metric   |   nearest_lsoa_centroid_distance_m |
|:---------|-----------------------------------:|
| min      |                             2000   |
| p25      |                             2554.3 |
| median   |                             3379.4 |
| p75      |                             5839.6 |
| p90      |                            47529.7 |
| p95      |                           100075   |
| p99      |                           111819   |
| max      |                           117578   |

Distance threshold coverage:

|   threshold_m |   count_within_or_equal | pct_no_lsoa   |
|--------------:|------------------------:|:--------------|
|         1,000 |                       0 | 0.00%         |
|         2,000 |                       0 | 0.00%         |
|         3,000 |                 134,607 | 40.10%        |
|         5,000 |                 238,507 | 71.05%        |
|        10,000 |                 271,268 | 80.81%        |
|        25,000 |                 282,257 | 84.08%        |
|        50,000 |                 303,136 | 90.30%        |
|       100,000 |                 318,868 | 94.99%        |
|       125,000 |                 335,692 | 100.00%       |

Top 100 km BNG grid-square counts for no-LSOA links:

| grid100km   |   no_lsoa_count | pct_no_lsoa   |
|:------------|----------------:|:--------------|
| 3,2         |          33,043 | 9.84%         |
| 3,5         |          28,469 | 8.48%         |
| 3,3         |          26,961 | 8.03%         |
| 2,6         |          26,412 | 7.87%         |
| 4,4         |          24,799 | 7.39%         |
| 4,3         |          23,910 | 7.12%         |
| 4,2         |          23,896 | 7.12%         |
| 5,2         |          20,880 | 6.22%         |
| 3,6         |          20,483 | 6.10%         |
| 5,3         |          20,242 | 6.03%         |
| 3,4         |          15,280 | 4.55%         |
| 6,2         |          12,101 | 3.60%         |

Collision comparison:

| population   |   link_years_all_aadt |   positive_rla_rows |   collision_sum |   mean_collision_count_all_link_years |   positive_link_year_rate |   mean_collision_count_positive_rows |
|:-------------|----------------------:|--------------------:|----------------:|--------------------------------------:|--------------------------:|-------------------------------------:|
| no_lsoa      |             3,356,920 |              30,570 |          36,133 |                              0.010764 |                  0.009107 |                              1.18198 |
| with_lsoa    |            18,318,650 |             360,685 |         414,859 |                              0.022647 |                  0.019689 |                              1.1502  |
| full         |            21,675,570 |             391,255 |         450,992 |                              0.020806 |                  0.018051 |                              1.15268 |

Summary: the no-LSOA links are not random missing rows. They are heavily weighted toward lower-order road functions: Restricted Local Access Road and Minor Road together make up `72.5%` of no-LSOA links versus `38.3%` of the full network. They are also overwhelmingly Single Carriageway (`98.4%`). The centroid-distance distribution confirms the original hypothesis in part: all failures are beyond the current 2 km nearest-centroid cap. It also complicates the hypothesis, because `29.0%` of the population is more than 5 km from the nearest centroid and `19.2%` is more than 10 km away, so forcing a distant centroid assignment for all links would be weak. Observationally, these links are lower-collision than the covered population: `0.010764` collisions/link-year versus `0.022647` for covered links.

## Stage 2: Training-set Exclusion Diagnosis

The Stage 2 GLM exclusion is complete-case logic, not an explicit RUC filter. In `src/road_risk/model/collision.py`, `train_collision_glm()` selects candidate features whose coverage is above 50% as raw complete-case features, median-imputes candidates with 5-50% coverage, skips lower-coverage candidates, then calls `.dropna()` on the selected feature matrix. XGBoost does not exclude these links because `train_collision_xgb()` fills missing selected features with 0 before fitting.

Feature policy at current coverage:

| feature                   |   link_year_coverage | glm_policy             |
|:--------------------------|---------------------:|:-----------------------|
| hgv_proportion            |             0.016238 | skipped_low_coverage   |
| degree_mean               |             1        | selected_complete_case |
| betweenness               |             1        | selected_complete_case |
| betweenness_relative      |             1        | selected_complete_case |
| dist_to_major_km          |             0.998719 | selected_complete_case |
| pop_density_per_km2       |             0.845129 | selected_complete_case |
| speed_limit_mph_effective |             0.912728 | selected_complete_case |
| lanes                     |             0.072979 | median_imputed         |
| is_unpaved                |             0.161737 | median_imputed         |

Binding complete-case nulls before fill:

| feature                   |   null_links_no_lsoa |   null_links_full |
|:--------------------------|---------------------:|------------------:|
| pop_density_per_km2       |              335,692 |           335,692 |
| speed_limit_mph_effective |              189,166 |           189,166 |
| dist_to_major_km          |                1,194 |             2,776 |
| degree_mean               |                    0 |                 0 |
| betweenness               |                    0 |                 0 |
| betweenness_relative      |                    0 |                 0 |

Training-row counts before fill:

|   total_links |   complete_case_links |   incomplete_case_links |   complete_case_link_years_before_downsample |   no_lsoa_complete_case_links |   no_lsoa_dropped_links |   no_lsoa_complete_case_link_years |   no_lsoa_dropped_link_years |   with_lsoa_complete_case_links |   with_lsoa_dropped_links |   with_lsoa_complete_case_link_years |   with_lsoa_dropped_link_years |
|--------------:|----------------------:|------------------------:|---------------------------------------------:|------------------------------:|------------------------:|-----------------------------------:|-----------------------------:|--------------------------------:|--------------------------:|-------------------------------------:|-------------------------------:|
|     2,167,557 |             1,830,283 |                 337,274 |                                   18,302,830 |                             0 |                 335,692 |                                  0 |                    3,356,920 |                       1,830,283 |                     1,582 |                           18,302,830 |                         15,820 |

Filling RUC and population density alone is not quite sufficient for GLM inclusion because `speed_limit_mph_effective` is also null for `189,166` of the no-LSOA links. That column is derived partly from `ruc_urban_rural`, so it was recomputed after the RUC fill using the existing speed-limit lookup rules. `dist_to_major_km` remains null for `1,194` original no-LSOA links; that is a separate network-topology gap, not an LSOA-derived feature, and was not filled in this task.

## Stage 3: Fill Method

Chosen method: hybrid nearest-centroid and fallback. Links with a nearest LSOA population-weighted centroid within `5,000` m received that LSOA's `RUC21CD`, derived urban/rural split, and population density. Links beyond `5,000` m were assigned the documented conservative fallback: `ruc_urban_rural = Rural`, `ruc_class = RURAL_DEFAULT`, and `pop_density_per_km2 = 174.256232`, the pre-fill median among Rural-classified links. All filled links have `ruc_imputed = True`, with `ruc_fill_method`, `ruc_nearest_lsoa21cd`, and `ruc_nearest_lsoa_centroid_distance_m` audit columns.

Fill coverage:

| fill_method                  |   n_links | pct_target   |
|:-----------------------------|----------:|:-------------|
| nearest_lsoa_centroid_5km    |   238,507 | 71.05%       |
| rural_default_median_density |    97,185 | 28.95%       |

Fill distance distribution:

| population    |   n_links |   min_m |   p25_m |   median_m |   p75_m |    p95_m |    max_m |
|:--------------|----------:|--------:|--------:|-----------:|--------:|---------:|---------:|
| all_filled    |   335,692 |    2000 |  2554.3 |     3379.4 |  5839.6 | 100075   | 117578   |
| spatial_5km   |   238,507 |    2000 |  2378.6 |     2850.6 |  3529.6 |   4528.4 |   4999.9 |
| fallback_tail |    97,185 |    5000 |  7250.5 |    29194.8 | 80354.4 | 111058   | 117578   |

Residual nulls after fill:

|   ruc_class |   ruc_urban_rural |   pop_density_per_km2 |   speed_limit_mph_effective |
|------------:|------------------:|----------------------:|----------------------------:|
|           0 |                 0 |                     0 |                           0 |

Stage 2 complete-case status after this fill:

|   total_links |   complete_case_links |   incomplete_case_links |   complete_case_link_years_before_downsample |   no_lsoa_original_complete_case_links_after_fill |   no_lsoa_original_remaining_incomplete_links_after_fill |   with_lsoa_original_remaining_incomplete_links_after_fill |
|--------------:|----------------------:|------------------------:|---------------------------------------------:|--------------------------------------------------:|---------------------------------------------------------:|-----------------------------------------------------------:|
|     2,167,557 |             2,164,781 |                   2,776 |                                   21,647,810 |                                           334,498 |                                                    1,194 |                                                      1,582 |

The fill resolves all LSOA-derived nulls and the RUC-derived speed-limit nulls. Practical modelling impact: of the 97,185 links filled via rural-default fallback, only 993 (1.02%) appear in `road_link_annual.parquet`, so the rural default affects about 1k active modelled links, not 97k; verification is in `reports/ruc_fill_verification.md`. The remaining original no-LSOA links not recovered into GLM complete-case training are the `1,194` links with `dist_to_major_km` still null, which should be handled separately if complete GLM inclusion is required.

## Supporting Outputs

- `reports/supporting/ruc_fill_stage1_road_function.csv`
- `reports/supporting/ruc_fill_stage1_form_of_way.csv`
- `reports/supporting/ruc_fill_stage1_road_classification.csv`
- `reports/supporting/ruc_fill_stage1_grid100km_top.csv`
- `reports/supporting/ruc_fill_stage1_grid10km_top.csv`
- `reports/supporting/ruc_fill_stage1_nearest_lsoa_distance_stats.csv`
- `reports/supporting/ruc_fill_stage1_nearest_lsoa_distance_thresholds.csv`
- `reports/supporting/ruc_fill_stage1_collision_summary.csv`
- `reports/supporting/ruc_fill_stage2_feature_policy.csv`
- `reports/supporting/ruc_fill_stage2_binding_null_counts.csv`
- `reports/supporting/ruc_fill_stage2_training_counts_pre.csv`
- `reports/supporting/ruc_fill_stage2_training_counts_post.csv`
- `reports/supporting/ruc_fill_stage3_fill_summary.csv`
- `reports/supporting/ruc_fill_stage3_fill_distance_stats.csv`

Full provenance is in `data/provenance/ruc_fill_provenance.json`.
