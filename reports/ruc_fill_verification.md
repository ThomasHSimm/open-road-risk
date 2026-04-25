# RUC Fill Verification: Rural Default Fallback

This read-only verification checks whether the `97,185` links assigned by `ruc_fill_method == "rural_default_median_density"` are structurally consistent with the rural default used in the RUC fill. The hypothesis is that the fallback subset, being the long-distance tail beyond the 5 km nearest-LSOA-centroid cap, should be weighted toward minor/rural road functions and geographically peripheral grid squares rather than major urban-adjacent roads.

## 1. Road-Function Breakdown

| road_function                |   full_no_ruc_count | full_no_ruc_pct   |   fallback_count | fallback_pct   | fallback_vs_full_no_ruc_pct_point_delta   |
|:-----------------------------|--------------------:|:------------------|-----------------:|:---------------|:------------------------------------------|
| Restricted Local Access Road |             142,087 | 42.33%            |           38,512 | 39.63%         | -2.70%                                    |
| Local Road                   |              47,516 | 14.15%            |           24,846 | 25.57%         | 11.41%                                    |
| Minor Road                   |             101,435 | 30.22%            |           19,824 | 20.40%         | -9.82%                                    |
| A Road                       |              21,847 | 6.51%             |            6,659 | 6.85%          | 0.34%                                     |
| B Road                       |              17,411 | 5.19%             |            5,452 | 5.61%          | 0.42%                                     |
| Local Access Road            |               3,084 | 0.92%             |            1,036 | 1.07%          | 0.15%                                     |
| Secondary Access Road        |               1,739 | 0.52%             |              685 | 0.70%          | 0.19%                                     |
| Motorway                     |                 573 | 0.17%             |              171 | 0.18%          | 0.01%                                     |

Strategic-road check within the fallback set:

| category         |   count | pct_fallback   |
|:-----------------|--------:|:---------------|
| Motorway         |     171 | 0.18%          |
| A Road           |   6,659 | 6.85%          |
| Trunk A-road     |   1,748 | 1.80%          |
| Non-trunk A-road |   4,911 | 5.05%          |
| B Road           |   5,452 | 5.61%          |
| Other            |  84,903 | 87.36%         |

The fallback set is similarly concentrated in Restricted Local Access Road, Minor Road, and Local Road as the full no-RUC population, though slightly less so: `85.6%` versus `86.7%`. Motorway, all A-road, trunk A-road, and B-road shares are `0.18%`, `6.85%`, `1.80%`, and `5.61%`, respectively, so major-road presence is non-zero but not substantial.

## 2. Geographic Distribution

Top fallback 100 km BNG grid squares, compared with full no-RUC counts:

| grid100km   |   full_no_ruc_count | full_no_ruc_pct   |   fallback_count | fallback_pct   | fallback_vs_full_no_ruc_pct_point_delta   |
|:------------|--------------------:|:------------------|-----------------:|:---------------|:------------------------------------------|
| 2,6         |              26,412 | 7.87%             |           26,412 | 27.18%         | 19.31%                                    |
| 3,6         |              20,483 | 6.10%             |           19,680 | 20.25%         | 14.15%                                    |
| 3,5         |              28,469 | 8.48%             |           14,127 | 14.54%         | 6.06%                                     |
| 2,5         |              11,456 | 3.41%             |           11,396 | 11.73%         | 8.31%                                     |
| 2,2         |              11,489 | 3.42%             |            5,207 | 5.36%          | 1.94%                                     |
| 3,2         |              33,043 | 9.84%             |            3,257 | 3.35%          | -6.49%                                    |
| 2,3         |               8,954 | 2.67%             |            2,732 | 2.81%          | 0.14%                                     |
| 4,4         |              24,799 | 7.39%             |            2,731 | 2.81%          | -4.58%                                    |
| 3,4         |              15,280 | 4.55%             |            2,571 | 2.65%          | -1.91%                                    |
| 5,3         |              20,242 | 6.03%             |            1,986 | 2.04%          | -3.99%                                    |
| 3,3         |              26,961 | 8.03%             |            1,945 | 2.00%          | -6.03%                                    |
| 4,5         |              11,622 | 3.46%             |            1,429 | 1.47%          | -1.99%                                    |
| 4,6         |               3,525 | 1.05%             |            1,329 | 1.37%          | 0.32%                                     |
| 4,3         |              23,910 | 7.12%             |              817 | 0.84%          | -6.28%                                    |
| 5,2         |              20,880 | 6.22%             |              711 | 0.73%          | -5.49%                                    |

The top 10 fallback grid squares overlap `6` of the top 10 full no-RUC grid squares. This means the fallback set is partly the extreme-distance tail of the same no-RUC geography, but it is also geographically more concentrated in a different subset of peripheral grid squares.

## 3. Distance Distribution

| metric   |   distance_m |
|:---------|-------------:|
| min      |       5000   |
| p25      |       7250.5 |
| median   |      29194.8 |
| p75      |      80354.4 |
| p95      |     111058   |
| max      |     117578   |

Distance-tail counts:

|   threshold_m |   count_above | pct_fallback   |
|--------------:|--------------:|:---------------|
|        25,000 |        53,435 | 54.98%         |
|        50,000 |        32,556 | 33.50%         |
|       100,000 |        16,824 | 17.31%         |

The fallback set is not mostly in the 5-10 km range. The median nearest-centroid distance is `29,194.8` m, and `55.0%` are above 25 km, `33.5%` above 50 km, and `17.3%` above 100 km. That makes the rural default a pragmatic working assumption for a substantial tail, not a close spatial inference from nearby LSOA centroids.

## 4. `road_link_annual` Coverage

| population         |   n_links |   links_in_road_link_annual | pct_in_road_link_annual   |
|:-------------------|----------:|----------------------------:|:--------------------------|
| fallback           |    97,185 |                         993 | 1.02%                     |
| full_no_ruc_filled |   335,692 |                      17,860 | 5.32%                     |
| full_network       | 2,167,557 |                     233,604 | 10.78%                    |

Only `1.02%` of fallback links appear in `road_link_annual.parquet`, lower than both the full no-RUC filled population and the full network. The fallback therefore has limited direct collision-history coverage, but the links still appear in the AADT/scoring network and can matter for complete family assignment.

## Closing Assessment

The rural default is broadly consistent with the fallback population's road structure: the subset is overwhelmingly minor/local-access and has only small Motorway, A-road, trunk A-road, and B-road shares. The geographic and distance checks are more mixed. The fallback is clearly peripheral relative to the centroid join, but a large share is tens of kilometres from any LSOA centroid, so the assignment should be described as a conservative modelling default rather than a spatially observed rural classification. Overall, the default is defensible for facility-family completeness, provided downstream documentation keeps the `ruc_imputed` and `ruc_fill_method` distinction visible.

## Supporting Outputs

- `reports/supporting/ruc_fill_verification_road_function.csv`
- `reports/supporting/ruc_fill_verification_road_classification.csv`
- `reports/supporting/ruc_fill_verification_strategic_breakdown.csv`
- `reports/supporting/ruc_fill_verification_grid100km.csv`
- `reports/supporting/ruc_fill_verification_fallback_distance_stats.csv`
- `reports/supporting/ruc_fill_verification_fallback_distance_thresholds.csv`
- `reports/supporting/ruc_fill_verification_rla_coverage.csv`
