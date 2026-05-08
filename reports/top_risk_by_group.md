# Top-Risk Links By Comparable Road Group

## Purpose

The global top-1% table is useful, but the very top of that ranking can be dominated by high-volume motorway links. These group-specific tables help inspect high-risk links among comparable road families, OS road classes, and conservative reporting archetypes.

## Summary

| group_type | groups | top_n_per_group | rows |
| --- | --- | --- | --- |
| family | 5 | 100 | 500 |
| road_classification | 7 | 100 | 700 |
| road_archetype | 9 | 100 | 900 |

Ranking field used: `risk_percentile_eb`.

Created at: `2026-05-06T20:56:11+00:00`.

## Road-Type Schemes Used Here

- `family` is the official comparable-road-type modelling/diagnostic split: `motorway`, `trunk_a`, `other_urban`, `other_rural`, plus `other_unknown` as a fallback/reporting bucket when the family inputs do not resolve cleanly.
- `road_classification` is the broad OS Open Roads classification axis (`Motorway`, `A Road`, `B Road`, `Classified Unnumbered`, `Unclassified`, `Not Classified`, `Unknown`). It is useful for inspection but is not the same thing as the modelling family split.
- `road_function` is the OS functional category, retained as descriptive context because it is often more informative below trunk-road scale.
- `form_of_way` and derived flags (`is_dual`, `is_slip_road`, `is_roundabout`) describe physical form. They are important map/filter fields, but the repo's v1 family design explicitly did not adopt dual/single/roundabout/slip as separate families.
- `road_archetype` is a conservative reporting convenience that combines `family` with broad road class. It is not a model family and should not be read as a new production ranking surface.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores_eb.parquet | 2026-04-25T13:34:14.243889+00:00 | 215,745,466 |
| data/processed/shapefiles/openroads.parquet | 2026-04-29T00:35:29.349109+00:00 | 392,911,115 |
| data/features/network_features.parquet | 2026-05-01T17:28:10.710235+00:00 | 213,584,936 |

Project/model output version: `0.1.0`.

## Count By Road Archetype

Each archetype table contains the top 100 links within that archetype, so the count table below shows output allocation rather than population prevalence. For prevalence, use the global top-1% `Count By Road Archetype` table.

| road_archetype | count | share |
| --- | --- | --- |
| motorway | 100 | 11.1% |
| other_unknown | 100 | 11.1% |
| rural_a_road | 100 | 11.1% |
| rural_b_road | 100 | 11.1% |
| rural_minor | 100 | 11.1% |
| trunk_a | 100 | 11.1% |
| urban_a_road | 100 | 11.1% |
| urban_b_road | 100 | 11.1% |
| urban_minor | 100 | 11.1% |

## Family: motorway

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 42,232.400 | 10.633 | 136 | 13.592 | 10.987 | 100.000 | -2.397 | 53.252 |
| 2 | 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 51,462.000 | 4.910 | 129 | 12.885 | 8.860 | 100.000 | -1.686 | 53.744 |
| 3 | 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 54,576.300 | 5.066 | 123 | 12.260 | 5.505 | 100.000 | -1.826 | 52.507 |
| 4 | 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 42,870.800 | 8.245 | 119 | 11.840 | 4.156 | 100.000 | -1.611 | 52.469 |
| 5 | 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 40,764.100 | 11.595 | 110 | 10.996 | 9.730 | 100.000 | -1.333 | 52.427 |
| 6 | 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 43,138.700 | 8.304 | 107 | 10.693 | 8.736 | 100.000 | -1.205 | 53.456 |
| 7 | 7 | EEDCD4A3-3046-4C4E-8DAE-2DF46525E19F | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 40,891.400 | 7.339 | 105 | 10.482 | 6.745 | 100.000 | -2.339 | 53.104 |
| 8 | 8 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 64,451.900 | 7.765 | 104 | 10.389 | 7.822 | 100.000 | -2.752 | 53.289 |
| 9 | 9 | D4178A17-E84A-4B2E-8904-3052B12EBCED | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 45,308.500 | 8.182 | 94 | 9.381 | 5.957 | 100.000 | -1.685 | 52.573 |
| 10 | 10 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 61,144.300 | 5.266 | 93 | 9.280 | 5.728 | 100.000 | -2.366 | 53.177 |

## Family: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 30 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,207.000 | 2.097 | 64 | 6.387 | 4.607 | 99.999 | -1.237 | 53.626 |
| 2 | 43 | F92239D4-36BC-45FF-8B98-7B4FF2CF81C0 | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 14,451.600 | 0.056 | 58 | 5.704 | 1.444 | 99.998 | -2.953 | 53.493 |
| 3 | 54 | F8C83919-A991-4C0F-980E-148BFB912405 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 5,346.100 | 8.549 | 52 | 5.180 | 3.198 | 99.998 | -0.348 | 53.602 |
| 4 | 61 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 8,552.000 | 11.654 | 49 | 4.888 | 3.558 | 99.997 | -1.976 | 52.936 |
| 5 | 73 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 7,142.300 | 6.793 | 45 | 4.494 | 3.760 | 99.997 | 0.354 | 52.247 |
| 6 | 77 | 43BC8837-2592-43A6-89FF-6762DCC1611D | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 21,054.100 | 2.791 | 45 | 4.333 | 0.705 | 99.996 | 1.573 | 52.632 |
| 7 | 87 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 20,058.000 | 4.039 | 42 | 4.187 | 3.017 | 99.996 | -1.452 | 52.974 |
| 8 | 94 | A8CF56A0-06EA-4E02-82B5-8D7B18189D7F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,074.200 | 2.554 | 41 | 4.019 | 1.148 | 99.996 | 1.087 | 52.025 |
| 9 | 95 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 18,611.600 | 7.489 | 40 | 4.007 | 5.135 | 99.996 | -1.501 | 52.866 |
| 10 | 96 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,906.000 | 7.408 | 40 | 4.001 | 4.186 | 99.996 | -0.975 | 52.403 |

## Family: other_urban

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 103 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,488.700 | 3.374 | 38 | 3.786 | 2.649 | 99.995 | -0.450 | 53.703 |
| 2 | 114 | 1C5FCE8A-EB04-48CF-A2C7-79E66C780A0F | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,626.100 | 2.615 | 37 | 3.670 | 1.894 | 99.995 | -0.556 | 53.251 |
| 3 | 116 | 35598324-6978-48F4-BCB9-33DC32D6B118 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,347.600 | 0.251 | 37 | 3.621 | 1.060 | 99.995 | -0.330 | 53.768 |
| 4 | 125 | 87A56F0E-7C15-4816-8BCA-F895D218CD1F | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,763.900 | 0.087 | 36 | 3.505 | 0.893 | 99.994 | -0.376 | 53.750 |
| 5 | 128 | BFB5EAAC-3BE4-4B03-B0BF-654BB6A871F3 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 15,358.000 | 0.197 | 35 | 3.450 | 1.354 | 99.994 | -1.153 | 52.955 |
| 6 | 134 | 63B62281-35C8-4F62-B760-B6949F51ED5C | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 16,063.700 | 0.089 | 33 | 3.280 | 2.033 | 99.994 | -1.179 | 52.964 |
| 7 | 137 | 65ECF41C-0895-4918-B54F-64EB0FCFBB15 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 13,665.000 | 0.009 | 33 | 3.263 | 1.537 | 99.994 | -1.743 | 53.794 |
| 8 | 138 | 16D5C305-8230-4568-A0C5-F8146A963EA6 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 25,704.700 | 0.836 | 33 | 3.261 | 1.489 | 99.994 | -0.264 | 52.546 |
| 9 | 143 | 7E67F595-0DA0-491F-A17C-2496A75EF427 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 16,959.400 | 3.517 | 32 | 3.195 | 2.766 | 99.993 | -2.796 | 53.377 |
| 10 | 150 | 0824FEC1-4845-433E-BB69-AEDB8F1633D1 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 21,871.600 | 0.235 | 32 | 3.154 | 1.311 | 99.993 | -1.838 | 52.517 |

## Family: other_rural

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 158 | 6EA22486-59DA-4A1F-A503-6FE157C1B266 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 719.200 | 2.228 | 31 | 3.066 | 1.504 | 99.993 | -2.510 | 53.639 |
| 2 | 289 | D5833F5B-E444-4BDA-AABF-DDF4E3EE5E2F | Unknown | Local Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 639.400 | 0.037 | 23 | 2.288 | 1.668 | 99.987 | -2.948 | 53.848 |
| 3 | 313 | 4F7AA121-68AC-4F36-A483-DB2CC1A64202 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,349.000 | 4.065 | 22 | 2.202 | 2.363 | 99.986 | -0.208 | 52.621 |
| 4 | 330 | E5412A99-F27C-4D22-A253-FF9DA03A6AD1 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 16,327.400 | 1.304 | 22 | 2.145 | 0.798 | 99.985 | -0.983 | 52.772 |
| 5 | 446 | FFE927A0-D9C6-4676-9A30-B34C5CD318A0 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 4,990.100 | 0.033 | 19 | 1.873 | 1.019 | 99.979 | 1.468 | 52.192 |
| 6 | 453 | 6E9A0C83-DE15-47D7-B49A-B6E7C3390390 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,410.600 | 0.273 | 19 | 1.862 | 0.860 | 99.979 | -1.538 | 53.613 |
| 7 | 571 | F8EB83E6-E75C-47BB-86BF-6C1FAB5C1B4E | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 14,034.800 | 0.619 | 17 | 1.672 | 0.903 | 99.974 | -0.551 | 53.548 |
| 8 | 576 | BA68C73F-4D0A-42FE-9D79-8BB47C55C9B4 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 12,833.200 | 0.637 | 17 | 1.672 | 0.892 | 99.973 | -0.057 | 52.923 |
| 9 | 586 | 75075385-9C0E-4B5C-8119-957239230DFC | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 9,329.700 | 1.048 | 21 | 1.638 | 0.108 | 99.973 | -0.484 | 53.292 |
| 10 | 609 | E56501E8-3ACB-46DD-B6B1-397BF24F3499 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 9,364.300 | 4.878 | 16 | 1.592 | 1.290 | 99.972 | -1.052 | 52.239 |

## Road Classification: A Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 30 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,207.000 | 2.097 | 64 | 6.387 | 4.607 | 99.999 | -1.237 | 53.626 |
| 2 | 43 | F92239D4-36BC-45FF-8B98-7B4FF2CF81C0 | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 14,451.600 | 0.056 | 58 | 5.704 | 1.444 | 99.998 | -2.953 | 53.493 |
| 3 | 54 | F8C83919-A991-4C0F-980E-148BFB912405 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 5,346.100 | 8.549 | 52 | 5.180 | 3.198 | 99.998 | -0.348 | 53.602 |
| 4 | 61 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 8,552.000 | 11.654 | 49 | 4.888 | 3.558 | 99.997 | -1.976 | 52.936 |
| 5 | 73 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 7,142.300 | 6.793 | 45 | 4.494 | 3.760 | 99.997 | 0.354 | 52.247 |
| 6 | 77 | 43BC8837-2592-43A6-89FF-6762DCC1611D | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 21,054.100 | 2.791 | 45 | 4.333 | 0.705 | 99.996 | 1.573 | 52.632 |
| 7 | 87 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 20,058.000 | 4.039 | 42 | 4.187 | 3.017 | 99.996 | -1.452 | 52.974 |
| 8 | 94 | A8CF56A0-06EA-4E02-82B5-8D7B18189D7F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,074.200 | 2.554 | 41 | 4.019 | 1.148 | 99.996 | 1.087 | 52.025 |
| 9 | 95 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 18,611.600 | 7.489 | 40 | 4.007 | 5.135 | 99.996 | -1.501 | 52.866 |
| 10 | 96 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,906.000 | 7.408 | 40 | 4.001 | 4.186 | 99.996 | -0.975 | 52.403 |

## Road Classification: B Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 151 | 8B16D730-145F-4EB7-B6A9-5976FB696D1F | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 9,803.300 | 0.150 | 32 | 3.145 | 1.168 | 99.993 | -2.445 | 53.746 |
| 2 | 210 | 50AC7915-813B-4763-8176-4C4E5D2911C6 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 9,584.000 | 1.884 | 29 | 2.740 | 0.463 | 99.990 | -0.050 | 52.352 |
| 3 | 297 | 10675A16-3ABA-4034-8F16-9FFC0CCA0625 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 17,438.400 | 0.417 | 23 | 2.271 | 1.200 | 99.986 | -1.891 | 52.499 |
| 4 | 326 | 4DB11F0A-D996-4587-A339-26267BF1E6B2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 9,357.700 | 0.168 | 22 | 2.168 | 1.095 | 99.985 | -0.355 | 53.768 |
| 5 | 356 | C1195BA3-6D8B-46AA-99D4-0CA40DF3B9F2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 13,411.100 | 0.372 | 21 | 2.074 | 1.158 | 99.984 | -1.923 | 52.617 |
| 6 | 360 | 5DDA098F-8582-4994-BD55-C927BDA18AC2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 15,358.100 | 0.309 | 21 | 2.069 | 1.054 | 99.983 | -1.521 | 52.423 |
| 7 | 390 | 33D5E262-9BF7-4BDB-B084-4EADD9A6E365 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 7,997.100 | 0.721 | 20 | 1.974 | 1.098 | 99.982 | -0.679 | 52.293 |
| 8 | 391 | 99DAD5C8-AD6C-4D6C-9197-97F9D7C7DB36 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,206.200 | 0.110 | 20 | 1.974 | 1.092 | 99.982 | -1.888 | 52.475 |
| 9 | 433 | FF1F59CF-6C10-4052-8020-80795789C39B | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 7,984.000 | 1.024 | 19 | 1.881 | 1.180 | 99.980 | -2.156 | 53.311 |
| 10 | 436 | 6E9935DE-6967-440C-9B0F-B4A2A5E3C22B | B Road | B Road | other_urban | urban_b_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,231.400 | 0.086 | 19 | 1.880 | 1.159 | 99.980 | -1.823 | 52.480 |

## Road Classification: Unclassified

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 125 | 87A56F0E-7C15-4816-8BCA-F895D218CD1F | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,763.900 | 0.087 | 36 | 3.505 | 0.893 | 99.994 | -0.376 | 53.750 |
| 2 | 331 | AE833812-27CC-443F-8C46-8803CB5B5888 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,122.000 | 0.051 | 22 | 2.144 | 0.786 | 99.985 | -1.893 | 52.458 |
| 3 | 389 | E5864850-D299-469E-B526-862E5F0D4F9C | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,197.700 | 0.140 | 20 | 1.974 | 1.100 | 99.982 | -1.154 | 52.956 |
| 4 | 396 | 197A98EA-3CA3-4BD6-87BB-6A3E8B794DF7 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,856.300 | 0.042 | 20 | 1.973 | 1.075 | 99.982 | -0.543 | 53.230 |
| 5 | 404 | 3FB669BD-4581-4F1C-B4D3-7B09ABD166B2 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,505.500 | 0.338 | 20 | 1.947 | 0.745 | 99.981 | -1.781 | 52.483 |
| 6 | 456 | 28E34A54-86C5-4FFB-A3EE-BF2E96D5CAA5 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 785.600 | 0.080 | 19 | 1.849 | 0.721 | 99.979 | -1.889 | 52.479 |
| 7 | 502 | A628CAA7-6CEE-417A-9101-345509B01FAF | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,359.800 | 0.041 | 18 | 1.773 | 0.969 | 99.977 | -1.525 | 53.811 |
| 8 | 513 | AA5B6E1C-33E9-4C13-B36B-E9ABF73CDA1F | Unclassified | Restricted Local Access Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,293.700 | 0.109 | 18 | 1.755 | 0.733 | 99.976 | -1.548 | 53.796 |
| 9 | 585 | CE110B27-B6A9-4C1D-9277-B1731F2AA394 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,485.300 | 0.212 | 17 | 1.642 | 0.589 | 99.973 | -1.078 | 53.476 |
| 10 | 596 | 82EA9722-CEEB-4310-B0B5-5F161DA1F9DD | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,896.500 | 3.955 | 16 | 1.601 | 1.639 | 99.973 | -3.045 | 53.623 |

## Road Archetype: motorway

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 42,232.400 | 10.633 | 136 | 13.592 | 10.987 | 100.000 | -2.397 | 53.252 |
| 2 | 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 51,462.000 | 4.910 | 129 | 12.885 | 8.860 | 100.000 | -1.686 | 53.744 |
| 3 | 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 54,576.300 | 5.066 | 123 | 12.260 | 5.505 | 100.000 | -1.826 | 52.507 |
| 4 | 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 42,870.800 | 8.245 | 119 | 11.840 | 4.156 | 100.000 | -1.611 | 52.469 |
| 5 | 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 40,764.100 | 11.595 | 110 | 10.996 | 9.730 | 100.000 | -1.333 | 52.427 |
| 6 | 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 43,138.700 | 8.304 | 107 | 10.693 | 8.736 | 100.000 | -1.205 | 53.456 |
| 7 | 7 | EEDCD4A3-3046-4C4E-8DAE-2DF46525E19F | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 40,891.400 | 7.339 | 105 | 10.482 | 6.745 | 100.000 | -2.339 | 53.104 |
| 8 | 8 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 64,451.900 | 7.765 | 104 | 10.389 | 7.822 | 100.000 | -2.752 | 53.289 |
| 9 | 9 | D4178A17-E84A-4B2E-8904-3052B12EBCED | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 45,308.500 | 8.182 | 94 | 9.381 | 5.957 | 100.000 | -1.685 | 52.573 |
| 10 | 10 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 61,144.300 | 5.266 | 93 | 9.280 | 5.728 | 100.000 | -2.366 | 53.177 |

## Road Archetype: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 30 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,207.000 | 2.097 | 64 | 6.387 | 4.607 | 99.999 | -1.237 | 53.626 |
| 2 | 43 | F92239D4-36BC-45FF-8B98-7B4FF2CF81C0 | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 14,451.600 | 0.056 | 58 | 5.704 | 1.444 | 99.998 | -2.953 | 53.493 |
| 3 | 54 | F8C83919-A991-4C0F-980E-148BFB912405 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 5,346.100 | 8.549 | 52 | 5.180 | 3.198 | 99.998 | -0.348 | 53.602 |
| 4 | 61 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 8,552.000 | 11.654 | 49 | 4.888 | 3.558 | 99.997 | -1.976 | 52.936 |
| 5 | 73 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 7,142.300 | 6.793 | 45 | 4.494 | 3.760 | 99.997 | 0.354 | 52.247 |
| 6 | 77 | 43BC8837-2592-43A6-89FF-6762DCC1611D | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 21,054.100 | 2.791 | 45 | 4.333 | 0.705 | 99.996 | 1.573 | 52.632 |
| 7 | 87 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 20,058.000 | 4.039 | 42 | 4.187 | 3.017 | 99.996 | -1.452 | 52.974 |
| 8 | 94 | A8CF56A0-06EA-4E02-82B5-8D7B18189D7F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,074.200 | 2.554 | 41 | 4.019 | 1.148 | 99.996 | 1.087 | 52.025 |
| 9 | 95 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 18,611.600 | 7.489 | 40 | 4.007 | 5.135 | 99.996 | -1.501 | 52.866 |
| 10 | 96 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,906.000 | 7.408 | 40 | 4.001 | 4.186 | 99.996 | -0.975 | 52.403 |

## Road Archetype: urban_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 103 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,488.700 | 3.374 | 38 | 3.786 | 2.649 | 99.995 | -0.450 | 53.703 |
| 2 | 114 | 1C5FCE8A-EB04-48CF-A2C7-79E66C780A0F | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,626.100 | 2.615 | 37 | 3.670 | 1.894 | 99.995 | -0.556 | 53.251 |
| 3 | 116 | 35598324-6978-48F4-BCB9-33DC32D6B118 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,347.600 | 0.251 | 37 | 3.621 | 1.060 | 99.995 | -0.330 | 53.768 |
| 4 | 128 | BFB5EAAC-3BE4-4B03-B0BF-654BB6A871F3 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 15,358.000 | 0.197 | 35 | 3.450 | 1.354 | 99.994 | -1.153 | 52.955 |
| 5 | 134 | 63B62281-35C8-4F62-B760-B6949F51ED5C | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 16,063.700 | 0.089 | 33 | 3.280 | 2.033 | 99.994 | -1.179 | 52.964 |
| 6 | 137 | 65ECF41C-0895-4918-B54F-64EB0FCFBB15 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 13,665.000 | 0.009 | 33 | 3.263 | 1.537 | 99.994 | -1.743 | 53.794 |
| 7 | 138 | 16D5C305-8230-4568-A0C5-F8146A963EA6 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 25,704.700 | 0.836 | 33 | 3.261 | 1.489 | 99.994 | -0.264 | 52.546 |
| 8 | 143 | 7E67F595-0DA0-491F-A17C-2496A75EF427 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 16,959.400 | 3.517 | 32 | 3.195 | 2.766 | 99.993 | -2.796 | 53.377 |
| 9 | 150 | 0824FEC1-4845-433E-BB69-AEDB8F1633D1 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 21,871.600 | 0.235 | 32 | 3.154 | 1.311 | 99.993 | -1.838 | 52.517 |
| 10 | 156 | EEF807BC-30B7-480F-855A-3C86F95040C8 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 38,021.300 | 1.738 | 31 | 3.087 | 2.216 | 99.993 | -1.363 | 53.394 |

## Road Archetype: rural_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 313 | 4F7AA121-68AC-4F36-A483-DB2CC1A64202 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,349.000 | 4.065 | 22 | 2.202 | 2.363 | 99.986 | -0.208 | 52.621 |
| 2 | 330 | E5412A99-F27C-4D22-A253-FF9DA03A6AD1 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 16,327.400 | 1.304 | 22 | 2.145 | 0.798 | 99.985 | -0.983 | 52.772 |
| 3 | 446 | FFE927A0-D9C6-4676-9A30-B34C5CD318A0 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 4,990.100 | 0.033 | 19 | 1.873 | 1.019 | 99.979 | 1.468 | 52.192 |
| 4 | 571 | F8EB83E6-E75C-47BB-86BF-6C1FAB5C1B4E | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 14,034.800 | 0.619 | 17 | 1.672 | 0.903 | 99.974 | -0.551 | 53.548 |
| 5 | 576 | BA68C73F-4D0A-42FE-9D79-8BB47C55C9B4 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 12,833.200 | 0.637 | 17 | 1.672 | 0.892 | 99.973 | -0.057 | 52.923 |
| 6 | 586 | 75075385-9C0E-4B5C-8119-957239230DFC | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 9,329.700 | 1.048 | 21 | 1.638 | 0.108 | 99.973 | -0.484 | 53.292 |
| 7 | 609 | E56501E8-3ACB-46DD-B6B1-397BF24F3499 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 9,364.300 | 4.878 | 16 | 1.592 | 1.290 | 99.972 | -1.052 | 52.239 |
| 8 | 628 | 195A6448-2614-4A63-BA21-2271C0708C3D | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 18,100.100 | 0.861 | 16 | 1.586 | 1.121 | 99.971 | -1.566 | 53.936 |
| 9 | 679 | 1A5709E4-3788-45B2-97F1-5261B18C4562 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 6,954.900 | 0.302 | 16 | 1.570 | 0.811 | 99.969 | -0.065 | 53.467 |
| 10 | 684 | 944456FB-0DD6-4D87-9149-CF30A8EE6A2C | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 8,865.300 | 0.093 | 16 | 1.565 | 0.752 | 99.968 | -0.413 | 53.584 |

## Road Archetype: urban_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 151 | 8B16D730-145F-4EB7-B6A9-5976FB696D1F | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 9,803.300 | 0.150 | 32 | 3.145 | 1.168 | 99.993 | -2.445 | 53.746 |
| 2 | 210 | 50AC7915-813B-4763-8176-4C4E5D2911C6 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 9,584.000 | 1.884 | 29 | 2.740 | 0.463 | 99.990 | -0.050 | 52.352 |
| 3 | 297 | 10675A16-3ABA-4034-8F16-9FFC0CCA0625 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 17,438.400 | 0.417 | 23 | 2.271 | 1.200 | 99.986 | -1.891 | 52.499 |
| 4 | 326 | 4DB11F0A-D996-4587-A339-26267BF1E6B2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 9,357.700 | 0.168 | 22 | 2.168 | 1.095 | 99.985 | -0.355 | 53.768 |
| 5 | 356 | C1195BA3-6D8B-46AA-99D4-0CA40DF3B9F2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 13,411.100 | 0.372 | 21 | 2.074 | 1.158 | 99.984 | -1.923 | 52.617 |
| 6 | 360 | 5DDA098F-8582-4994-BD55-C927BDA18AC2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 15,358.100 | 0.309 | 21 | 2.069 | 1.054 | 99.983 | -1.521 | 52.423 |
| 7 | 390 | 33D5E262-9BF7-4BDB-B084-4EADD9A6E365 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 7,997.100 | 0.721 | 20 | 1.974 | 1.098 | 99.982 | -0.679 | 52.293 |
| 8 | 391 | 99DAD5C8-AD6C-4D6C-9197-97F9D7C7DB36 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,206.200 | 0.110 | 20 | 1.974 | 1.092 | 99.982 | -1.888 | 52.475 |
| 9 | 433 | FF1F59CF-6C10-4052-8020-80795789C39B | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 7,984.000 | 1.024 | 19 | 1.881 | 1.180 | 99.980 | -2.156 | 53.311 |
| 10 | 436 | 6E9935DE-6967-440C-9B0F-B4A2A5E3C22B | B Road | B Road | other_urban | urban_b_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,231.400 | 0.086 | 19 | 1.880 | 1.159 | 99.980 | -1.823 | 52.480 |

## Road Archetype: rural_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 691 | 41EBB9AE-4F03-4D4E-9D0E-51EEB3D7BCB2 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 10,783.200 | 1.291 | 16 | 1.531 | 0.492 | 99.968 | -0.634 | 53.786 |
| 2 | 782 | 0E71C679-EA65-4F2B-9977-38927BE26F6E | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 9,591.300 | 0.654 | 15 | 1.481 | 0.942 | 99.964 | -1.248 | 53.365 |
| 3 | 871 | F10D4083-55D5-4094-94CB-CACA05C2D7DF | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 13,429.600 | 1.626 | 14 | 1.394 | 1.177 | 99.960 | -1.356 | 53.596 |
| 4 | 1,123 | FC3BD23B-DB93-4146-A467-4E0AE6F28E1B | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 10,281.800 | 1.057 | 13 | 1.287 | 0.914 | 99.948 | -3.040 | 53.521 |
| 5 | 1,230 | C80EEE2B-8E19-464C-9797-B70EF1068C21 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 7,238.900 | 0.542 | 14 | 1.243 | 0.214 | 99.943 | -1.589 | 52.485 |
| 6 | 1,521 | B8D515CF-BADA-43E8-9158-07E2B2492E3B | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,709.500 | 1.053 | 12 | 1.160 | 0.518 | 99.930 | -1.625 | 52.200 |
| 7 | 1,578 | F39A956E-D089-4FF3-97E8-1BCC0AF7BE6D | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 8,617.200 | 1.017 | 11 | 1.102 | 1.158 | 99.927 | -1.350 | 53.812 |
| 8 | 1,931 | 9BEF64F7-0A98-44C5-9D04-6659BC928E58 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 9,800.400 | 1.525 | 12 | 1.047 | 0.183 | 99.911 | -1.586 | 52.605 |
| 9 | 1,933 | 4418CFB3-8A69-434C-BD96-4A146BA7910B | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 6,521.100 | 0.965 | 12 | 1.043 | 0.179 | 99.911 | 0.072 | 52.659 |
| 10 | 2,016 | DC125845-5814-4046-B548-BE8D238D0E5F | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 7,828.900 | 0.203 | 10 | 1.001 | 1.031 | 99.907 | -1.258 | 53.394 |

## Road Archetype: urban_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 125 | 87A56F0E-7C15-4816-8BCA-F895D218CD1F | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,763.900 | 0.087 | 36 | 3.505 | 0.893 | 99.994 | -0.376 | 53.750 |
| 2 | 192 | 6FA816AE-B4FD-4E1D-94AB-30501E97ADF6 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,397.100 | 0.370 | 29 | 2.853 | 1.170 | 99.991 | -0.548 | 53.219 |
| 3 | 204 | 58AF7081-C5FF-4239-8D5B-CEC477724409 | Unknown | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,932.200 | 0.009 | 28 | 2.768 | 1.393 | 99.991 | -2.933 | 53.441 |
| 4 | 208 | 4435DC95-53B2-4912-8AEC-AF330489ED11 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,827.500 | 0.124 | 28 | 2.758 | 1.206 | 99.990 | -0.543 | 53.225 |
| 5 | 275 | 6A4DC099-8541-4671-908F-64DF143273D0 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,254.500 | 0.151 | 24 | 2.340 | 0.826 | 99.987 | -1.479 | 52.910 |
| 6 | 288 | 0AFF5EE0-3267-43D0-9EC5-CA6119303BE6 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,025.100 | 3.048 | 23 | 2.292 | 1.834 | 99.987 | -3.026 | 53.793 |
| 7 | 323 | C910A5C2-7048-4751-9013-8769E14AD8BC | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,481.800 | 0.282 | 22 | 2.174 | 1.204 | 99.985 | -0.273 | 53.758 |
| 8 | 324 | FA5F7264-2B23-49EF-842F-1F6EDA2814A6 | Unknown | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,216.200 | 0.130 | 22 | 2.174 | 1.199 | 99.985 | -0.363 | 53.787 |
| 9 | 331 | AE833812-27CC-443F-8C46-8803CB5B5888 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,122.000 | 0.051 | 22 | 2.144 | 0.786 | 99.985 | -1.893 | 52.458 |
| 10 | 365 | 6D2B61E1-2C45-4F4E-B027-CB05AC2F267F | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,970.700 | 0.178 | 21 | 2.054 | 0.845 | 99.983 | -1.915 | 52.475 |

## Road Archetype: rural_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 158 | 6EA22486-59DA-4A1F-A503-6FE157C1B266 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 719.200 | 2.228 | 31 | 3.066 | 1.504 | 99.993 | -2.510 | 53.639 |
| 2 | 289 | D5833F5B-E444-4BDA-AABF-DDF4E3EE5E2F | Unknown | Local Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 639.400 | 0.037 | 23 | 2.288 | 1.668 | 99.987 | -2.948 | 53.848 |
| 3 | 453 | 6E9A0C83-DE15-47D7-B49A-B6E7C3390390 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,410.600 | 0.273 | 19 | 1.862 | 0.860 | 99.979 | -1.538 | 53.613 |
| 4 | 831 | 105AC89B-8D74-40E3-BDA4-47F76F9A5296 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,814.100 | 0.522 | 16 | 1.444 | 0.249 | 99.962 | 0.810 | 52.246 |
| 5 | 1,510 | D603CF6D-6679-4BA7-AEF7-C7E5C80BA099 | Unclassified | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 724.400 | 0.115 | 12 | 1.169 | 0.594 | 99.930 | -2.772 | 53.485 |
| 6 | 1,526 | BF3895E2-B32C-4E56-BBB3-5FD653ECE8E1 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,272.800 | 2.469 | 13 | 1.154 | 0.210 | 99.930 | -0.487 | 54.264 |
| 7 | 1,652 | F4BD04B7-082E-4553-8225-0A260234EA7F | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,095.300 | 2.266 | 15 | 1.095 | 0.081 | 99.924 | -2.731 | 54.058 |
| 8 | 2,367 | 9FD284E9-7963-485A-8F55-B80434F7E4D6 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,833.500 | 1.034 | 10 | 0.987 | 0.701 | 99.891 | -1.779 | 53.906 |
| 9 | 2,434 | EFDE7664-F824-4249-A6CD-21FC9D849CA2 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,381.000 | 0.612 | 10 | 0.982 | 0.636 | 99.888 | -1.670 | 52.574 |
| 10 | 2,498 | 74788147-D695-4EF4-BF35-248631E9F43F | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,835.200 | 0.237 | 10 | 0.977 | 0.572 | 99.885 | -1.474 | 53.865 |

## Road Archetype: other_unknown

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 211 | 4158BCEE-7926-475E-9CCF-F464B6F8E137 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 5,311.300 | 7.573 | 29 | 2.733 | 0.446 | 99.990 | -1.875 | 53.432 |
| 2 | 249 | 7BF88232-B992-4162-8A4F-691D46F186E7 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 9,636.100 | 4.288 | 25 | 2.470 | 1.293 | 99.989 | -0.360 | 52.525 |
| 3 | 293 | 1942361E-5A0E-4926-B8F2-AAC3EB2AB46A | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 5,556.500 | 2.647 | 23 | 2.279 | 1.376 | 99.987 | -2.355 | 53.071 |
| 4 | 362 | 36FB8B57-4494-4469-95CE-D46C9A54FF23 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 7,420.100 | 2.710 | 24 | 2.065 | 0.183 | 99.983 | -0.248 | 52.793 |
| 5 | 380 | D98C3D9A-C954-4A9D-AE6C-1B7A54D8495F | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 5,921.200 | 2.503 | 20 | 1.988 | 1.440 | 99.983 | 0.021 | 53.306 |
| 6 | 382 | B303D610-A520-4619-81E3-3AA9ED7BDDA9 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 8,382.700 | 3.422 | 20 | 1.985 | 1.369 | 99.982 | -0.186 | 52.653 |
| 7 | 402 | 65825479-8993-4C9B-8E0F-492D499B0870 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 9,438.800 | 0.791 | 20 | 1.962 | 0.911 | 99.981 | -0.486 | 53.126 |
| 8 | 462 | A7516B09-B4F0-4906-947F-2ED4B3CF0821 | A Road | A Road | other_unknown | other_unknown | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,227.900 | 4.445 | 18 | 1.810 | 2.633 | 99.979 | -0.450 | 53.657 |
| 9 | 517 | 82330FE2-C8E2-4C6C-8F4E-25B91126226E | Classified Unnumbered | Minor Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 920.500 | 0.731 | 18 | 1.739 | 0.602 | 99.976 | -1.299 | 52.745 |
| 10 | 587 | A5F6D895-B5CD-4F0F-AA33-4CD5D519C066 | B Road | B Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 4,143.100 | 2.137 | 18 | 1.634 | 0.268 | 99.973 | -0.457 | 54.075 |

## Caveats

- These are within-group rankings, not claims that risk is comparable across all road types.
- A top-ranked rural road may have much lower absolute risk than a top-ranked motorway.
- `road_archetype` is only a reporting convenience; it is not a model family.
- `other_unknown` is a fallback/reporting bucket, not a deliberately modelled family.
- `form_of_way` remains descriptive context unless later residual diagnostics justify separate families.
- Motorway calibration remains a known caveat.
- EB ranking still reflects observed collision history and should be treated as screening evidence.

## Next Use

Use these finalised output columns to seed map review, stakeholder examples, or class-specific portfolio triage without losing the global risk columns.

TODO: build the interactive QMD map against these finalised output columns.
