# RUC-null Link Characterisation

This diagnostic characterises network links that did not receive an ONS 2021 Rural-Urban Classification (RUC) assignment. The current integration assigns RUC through the nearest LSOA population-weighted centroid, using the same 2,000 m cap as the population-density feature, so this report checks whether the null population is a geography problem, a road-type problem, or a true outside-boundary problem. No data, model, feature, or production artefact was modified.

## 1. Count and column-level null pattern

- Total links checked: 2,167,557
- Links with no RUC assignment: 335,692 (15.49%)
- Links with RUC assignment: 1,831,865 (84.51%)
- RUC columns present in `network_features.parquet`: `ruc_class`, `ruc_urban_rural`
- Join cap identified in `src/road_risk/features/network.py`: 2,000 m (`POP_JOIN_CAP_M`)

All RUC-null rows are null in both RUC fields; there are no partial-null RUC assignments.

| null_pattern                         |     count | pct_total   |
|:-------------------------------------|----------:|:------------|
| ruc_class=SET; ruc_urban_rural=SET   | 1,831,865 | 84.51%      |
| ruc_class=NULL; ruc_urban_rural=NULL |   335,692 | 15.49%      |

## 2. Geographic Distribution

Figure: `reports/figures/ruc_null_geography.png`

The no-RUC population is geographically clustered rather than evenly scattered. The clustering follows areas where road-link centroids are more than 2 km from any LSOA population-weighted centroid, which includes large rural/coastal LSOAs and edge areas. The centroid-distance distribution confirms the mechanical failure mode: every no-RUC link is above the 2,000 m cap, with the minimum only just above the threshold.

| metric   |   distance_m |
|:---------|-------------:|
| min      |       2000   |
| p25      |       2554.3 |
| median   |       3379.4 |
| p75      |       5839.6 |
| p95      |     100075   |
| max      |     117578   |

Threshold check:

|   threshold_m |   count_at_or_above | pct_no_ruc   |
|--------------:|--------------------:|:-------------|
|         2,000 |             335,692 | 100.00%      |
|         5,000 |              97,185 | 28.95%       |
|        10,000 |              64,424 | 19.19%       |
|        25,000 |              53,435 | 15.92%       |
|        50,000 |              32,556 | 9.70%        |
|       100,000 |              16,824 | 5.01%        |

## 3. `road_function` Comparison

| road_function                |   full_count | full_pct   |   with_ruc_count | with_ruc_pct   |   no_ruc_count | no_ruc_pct   | no_ruc_share_of_function_pct   |
|:-----------------------------|-------------:|:-----------|-----------------:|:---------------|---------------:|:-------------|:-------------------------------|
| Restricted Local Access Road |      451,126 | 20.81%     |          309,039 | 16.87%         |        142,087 | 42.33%       | 31.50%                         |
| Minor Road                   |      378,407 | 17.46%     |          276,972 | 15.12%         |        101,435 | 30.22%       | 26.81%                         |
| Local Road                   |      983,644 | 45.38%     |          936,128 | 51.10%         |         47,516 | 14.15%       | 4.83%                          |
| A Road                       |      155,534 | 7.18%      |          133,687 | 7.30%          |         21,847 | 6.51%        | 14.05%                         |
| B Road                       |       89,286 | 4.12%      |           71,875 | 3.92%          |         17,411 | 5.19%        | 19.50%                         |
| Local Access Road            |       23,862 | 1.10%      |           20,778 | 1.13%          |          3,084 | 0.92%        | 12.92%                         |
| Secondary Access Road        |       81,614 | 3.77%      |           79,875 | 4.36%          |          1,739 | 0.52%        | 2.13%                          |
| Motorway                     |        4,084 | 0.19%      |            3,511 | 0.19%          |            573 | 0.17%        | 14.03%                         |

## 4. Motorway / Trunk A Breakdown

| category     |   count | pct_no_ruc   |
|:-------------|--------:|:-------------|
| Motorway     |     573 | 0.17%        |
| Trunk A-road |   4,979 | 1.48%        |
| Other        | 330,140 | 98.35%       |

Supporting road-classification counts are written to `reports/supporting/ruc_null_road_classification_counts.csv`.

## 5. Spatial-join Fallback Feasibility

No local LSOA polygon boundary file was found in the repository. For this feasibility check only, a 100-link random sample of no-RUC links was compared with the official ONS LSOA 2021 EW BSC V4 boundary service. The boundary source used here is `ONS Lower layer Super Output Areas (December 2021) Boundaries EW BSC (V4), super-generalised 200 m, clipped to coastline`; because it is super-generalised to 200 m, small edge distances should be read as approximate.

Distance-to-polygon is the relevant fallback measure: a value of 0 m means the sampled link geometry intersects an LSOA polygon and a polygon-based spatial join would likely assign it. Distance-to-polygon-edge is also reported because the task asked for nearest polygon edge distance.

| metric   |   distance_to_polygon_m |   distance_to_polygon_edge_m |
|:---------|------------------------:|-----------------------------:|
| min      |                       0 |                          0   |
| p25      |                       0 |                        314.1 |
| median   |                       0 |                        713   |
| p75      |                       0 |                       1610.9 |
| p95      |                   53663 |                      53663   |
| max      |                  109301 |                     109301   |

In the 100-link sample, 85.0% intersected an LSOA polygon, 85.0% were within 50 m of one, and 85.0% were within 200 m. For nearest polygon edge specifically, 20.0% were within 200 m.

## Interpretation

The no-RUC set is structurally weighted toward minor/rural-style links, not proportional to the full network: Restricted Local Access Road and Minor Road together account for 72.5% of no-RUC links versus 38.3% of all links. It is not exclusively minor roads, though: 573 Motorway links and 4,979 trunk A-road links are RUC-null, so the issue touches strategic-road classes even if they are a small share of the null population. Geographic clustering is present and the centroid-distance distribution refutes the idea that these are mostly arbitrary missing values; the nulls are created by the 2 km nearest-centroid cap. The polygon sample suggests most no-RUC links are not genuinely outside LSOA geography: most intersect or sit very close to an LSOA polygon, so a polygon-based fallback would likely resolve the bulk of the population. For facility-family v1, the recommended handling is a spatial fallback before modelling; if that cannot be implemented immediately, use a separate `Unknown RUC` family rather than defaulting all no-RUC links to rural, because the current null set is biased toward minor roads but still structurally mixed.

## Supporting outputs

- `reports/figures/ruc_null_geography.png`
- `reports/supporting/ruc_null_patterns.csv`
- `reports/supporting/ruc_null_road_function_comparison.csv`
- `reports/supporting/ruc_null_motorway_trunk_breakdown.csv`
- `reports/supporting/ruc_null_road_classification_counts.csv`
- `reports/supporting/ruc_null_nearest_lsoa_centroid_distance.csv`
- `reports/supporting/ruc_null_nearest_lsoa_centroid_thresholds.csv`
- `reports/supporting/ruc_null_lsoa_polygon_distance_sample.csv`
- `reports/supporting/ruc_null_lsoa_polygon_distance_sample_stats.csv`
