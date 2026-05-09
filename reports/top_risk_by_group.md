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

Created at: `2026-05-08T22:17:58+00:00`.

## Road-Type Schemes Used Here

- `family` is the official comparable-road-type modelling/diagnostic split: `motorway`, `trunk_a`, `other_urban`, `other_rural`, plus `other_unknown` as a fallback/reporting bucket when the family inputs do not resolve cleanly.
- `road_classification` is the broad OS Open Roads classification axis (`Motorway`, `A Road`, `B Road`, `Classified Unnumbered`, `Unclassified`, `Not Classified`, `Unknown`). It is useful for inspection but is not the same thing as the modelling family split.
- `road_function` is the OS functional category, retained as descriptive context because it is often more informative below trunk-road scale.
- `form_of_way` and derived flags (`is_dual`, `is_slip_road`, `is_roundabout`) describe physical form. They are important map/filter fields, but the repo's v1 family design explicitly did not adopt dual/single/roundabout/slip as separate families.
- `road_archetype` is a conservative reporting convenience that combines `family` with broad road class. It is not a model family and should not be read as a new production ranking surface.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores_eb.parquet | 2026-05-08T22:13:34.224788+00:00 | 205,672,672 |
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
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 60,783.200 | 10.633 | 136 | 13.594 | 11.112 | 100.000 | -2.397 | 53.252 |
| 2 | 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 89,230.000 | 4.910 | 129 | 12.884 | 8.360 | 100.000 | -1.686 | 53.744 |
| 3 | 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 78,308.800 | 5.066 | 123 | 12.259 | 5.063 | 100.000 | -1.826 | 52.507 |
| 4 | 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 48,140.500 | 8.245 | 119 | 11.845 | 4.072 | 100.000 | -1.611 | 52.469 |
| 5 | 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 48,862.600 | 11.595 | 110 | 10.994 | 9.044 | 100.000 | -1.333 | 52.427 |
| 6 | 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 55,438.900 | 8.304 | 107 | 10.683 | 6.724 | 100.000 | -1.205 | 53.456 |
| 7 | 7 | EEDCD4A3-3046-4C4E-8DAE-2DF46525E19F | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 61,259.400 | 7.339 | 105 | 10.480 | 6.166 | 100.000 | -2.339 | 53.104 |
| 8 | 8 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 71,928.400 | 7.765 | 104 | 10.383 | 6.527 | 100.000 | -2.752 | 53.289 |
| 9 | 9 | D4178A17-E84A-4B2E-8904-3052B12EBCED | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 57,746.100 | 8.182 | 94 | 9.383 | 5.864 | 100.000 | -1.685 | 52.573 |
| 10 | 10 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 72,431.700 | 5.266 | 93 | 9.271 | 4.659 | 100.000 | -2.366 | 53.177 |

## Family: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 30 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 35,033.000 | 2.097 | 64 | 6.382 | 3.978 | 99.999 | -1.237 | 53.626 |
| 2 | 49 | F92239D4-36BC-45FF-8B98-7B4FF2CF81C0 | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 16,257.800 | 0.056 | 58 | 5.300 | 0.291 | 99.998 | -2.953 | 53.493 |
| 3 | 54 | F8C83919-A991-4C0F-980E-148BFB912405 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,865.300 | 8.549 | 52 | 5.143 | 1.726 | 99.998 | -0.348 | 53.602 |
| 4 | 61 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,767.600 | 11.654 | 49 | 4.889 | 3.580 | 99.997 | -1.976 | 52.936 |
| 5 | 74 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,917.400 | 6.793 | 45 | 4.468 | 2.109 | 99.997 | 0.354 | 52.247 |
| 6 | 75 | 43BC8837-2592-43A6-89FF-6762DCC1611D | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 26,908.600 | 2.791 | 45 | 4.446 | 1.544 | 99.997 | 1.573 | 52.632 |
| 7 | 84 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,088.900 | 4.039 | 42 | 4.189 | 3.030 | 99.996 | -1.452 | 52.974 |
| 8 | 94 | A8CF56A0-06EA-4E02-82B5-8D7B18189D7F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,047.800 | 2.554 | 41 | 4.015 | 1.016 | 99.996 | 1.087 | 52.025 |
| 9 | 95 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,033.900 | 7.489 | 40 | 3.999 | 3.841 | 99.996 | -1.501 | 52.866 |
| 10 | 96 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,475.000 | 7.408 | 40 | 3.988 | 2.811 | 99.996 | -0.975 | 52.403 |

## Family: other_urban

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 105 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 29,499.600 | 3.374 | 38 | 3.771 | 1.877 | 99.995 | -0.450 | 53.703 |
| 2 | 115 | 1C5FCE8A-EB04-48CF-A2C7-79E66C780A0F | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 27,669.100 | 2.615 | 37 | 3.649 | 1.331 | 99.995 | -0.556 | 53.251 |
| 3 | 129 | BFB5EAAC-3BE4-4B03-B0BF-654BB6A871F3 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 13,667.100 | 0.197 | 35 | 3.365 | 0.595 | 99.994 | -1.153 | 52.955 |
| 4 | 139 | 16D5C305-8230-4568-A0C5-F8146A963EA6 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,918.700 | 0.836 | 33 | 3.187 | 0.650 | 99.994 | -0.264 | 52.546 |
| 5 | 142 | 7E67F595-0DA0-491F-A17C-2496A75EF427 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 27,906.300 | 3.517 | 32 | 3.170 | 1.555 | 99.993 | -2.796 | 53.377 |
| 6 | 146 | 63B62281-35C8-4F62-B760-B6949F51ED5C | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 14,092.100 | 0.089 | 33 | 3.128 | 0.450 | 99.993 | -1.179 | 52.964 |
| 7 | 152 | 65ECF41C-0895-4918-B54F-64EB0FCFBB15 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 15,155.900 | 0.009 | 33 | 3.063 | 0.334 | 99.993 | -1.743 | 53.794 |
| 8 | 154 | EEF807BC-30B7-480F-855A-3C86F95040C8 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 29,486.000 | 1.738 | 31 | 3.060 | 1.281 | 99.993 | -1.363 | 53.394 |
| 9 | 155 | 35598324-6978-48F4-BCB9-33DC32D6B118 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,143.700 | 0.251 | 37 | 3.036 | 0.127 | 99.993 | -0.330 | 53.768 |
| 10 | 156 | 0824FEC1-4845-433E-BB69-AEDB8F1633D1 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 16,603.000 | 0.235 | 32 | 3.023 | 0.425 | 99.993 | -1.838 | 52.517 |

## Family: other_rural

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 231 | 6EA22486-59DA-4A1F-A503-6FE157C1B266 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 590.400 | 2.228 | 31 | 2.536 | 0.124 | 99.989 | -2.510 | 53.639 |
| 2 | 311 | 4F7AA121-68AC-4F36-A483-DB2CC1A64202 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,657.900 | 4.065 | 22 | 2.179 | 1.271 | 99.986 | -0.208 | 52.621 |
| 3 | 329 | E5412A99-F27C-4D22-A253-FF9DA03A6AD1 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 16,058.200 | 1.304 | 22 | 2.085 | 0.420 | 99.985 | -0.983 | 52.772 |
| 4 | 382 | 75075385-9C0E-4B5C-8119-957239230DFC | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,440.800 | 1.048 | 21 | 1.908 | 0.251 | 99.982 | -0.484 | 53.292 |
| 5 | 528 | 6E9A0C83-DE15-47D7-B49A-B6E7C3390390 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,222.200 | 0.273 | 19 | 1.636 | 0.162 | 99.976 | -1.538 | 53.613 |
| 6 | 542 | BA68C73F-4D0A-42FE-9D79-8BB47C55C9B4 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 12,405.000 | 0.637 | 17 | 1.614 | 0.408 | 99.975 | -0.057 | 52.923 |
| 7 | 554 | E56501E8-3ACB-46DD-B6B1-397BF24F3499 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 11,919.300 | 4.878 | 16 | 1.601 | 1.672 | 99.974 | -1.052 | 52.239 |
| 8 | 600 | 7029D21C-8EDD-4FB4-B958-58AF901A9EDF | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 8,215.200 | 2.589 | 16 | 1.542 | 0.513 | 99.972 | -1.594 | 53.109 |
| 9 | 607 | 195A6448-2614-4A63-BA21-2271C0708C3D | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 10,884.000 | 0.861 | 16 | 1.533 | 0.463 | 99.972 | -1.566 | 53.936 |
| 10 | 619 | F8EB83E6-E75C-47BB-86BF-6C1FAB5C1B4E | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 14,129.200 | 0.619 | 17 | 1.520 | 0.211 | 99.971 | -0.551 | 53.548 |

## Road Classification: A Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 30 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 35,033.000 | 2.097 | 64 | 6.382 | 3.978 | 99.999 | -1.237 | 53.626 |
| 2 | 49 | F92239D4-36BC-45FF-8B98-7B4FF2CF81C0 | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 16,257.800 | 0.056 | 58 | 5.300 | 0.291 | 99.998 | -2.953 | 53.493 |
| 3 | 54 | F8C83919-A991-4C0F-980E-148BFB912405 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,865.300 | 8.549 | 52 | 5.143 | 1.726 | 99.998 | -0.348 | 53.602 |
| 4 | 61 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,767.600 | 11.654 | 49 | 4.889 | 3.580 | 99.997 | -1.976 | 52.936 |
| 5 | 74 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,917.400 | 6.793 | 45 | 4.468 | 2.109 | 99.997 | 0.354 | 52.247 |
| 6 | 75 | 43BC8837-2592-43A6-89FF-6762DCC1611D | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 26,908.600 | 2.791 | 45 | 4.446 | 1.544 | 99.997 | 1.573 | 52.632 |
| 7 | 84 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,088.900 | 4.039 | 42 | 4.189 | 3.030 | 99.996 | -1.452 | 52.974 |
| 8 | 94 | A8CF56A0-06EA-4E02-82B5-8D7B18189D7F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,047.800 | 2.554 | 41 | 4.015 | 1.016 | 99.996 | 1.087 | 52.025 |
| 9 | 95 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,033.900 | 7.489 | 40 | 3.999 | 3.841 | 99.996 | -1.501 | 52.866 |
| 10 | 96 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,475.000 | 7.408 | 40 | 3.988 | 2.811 | 99.996 | -0.975 | 52.403 |

## Road Classification: B Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 158 | 8B16D730-145F-4EB7-B6A9-5976FB696D1F | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,839.200 | 0.150 | 32 | 3.014 | 0.406 | 99.993 | -2.445 | 53.746 |
| 2 | 201 | 50AC7915-813B-4763-8176-4C4E5D2911C6 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,011.400 | 1.884 | 29 | 2.739 | 0.417 | 99.991 | -0.050 | 52.352 |
| 3 | 301 | 10675A16-3ABA-4034-8F16-9FFC0CCA0625 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 15,737.200 | 0.417 | 23 | 2.198 | 0.487 | 99.986 | -1.891 | 52.499 |
| 4 | 343 | 4DB11F0A-D996-4587-A339-26267BF1E6B2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 7,764.700 | 0.168 | 22 | 2.027 | 0.290 | 99.984 | -0.355 | 53.768 |
| 5 | 362 | 5DDA098F-8582-4994-BD55-C927BDA18AC2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 16,162.500 | 0.309 | 21 | 1.980 | 0.385 | 99.983 | -1.521 | 52.423 |
| 6 | 371 | C1195BA3-6D8B-46AA-99D4-0CA40DF3B9F2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 15,018.200 | 0.372 | 21 | 1.949 | 0.315 | 99.983 | -1.923 | 52.617 |
| 7 | 413 | 99DAD5C8-AD6C-4D6C-9197-97F9D7C7DB36 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 11,905.600 | 0.110 | 20 | 1.855 | 0.308 | 99.981 | -1.888 | 52.475 |
| 8 | 425 | 33D5E262-9BF7-4BDB-B084-4EADD9A6E365 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 8,549.400 | 0.721 | 20 | 1.825 | 0.259 | 99.980 | -0.679 | 52.293 |
| 9 | 431 | C9ACE698-0977-45FB-83E5-85E673CA2EE1 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 12,016.800 | 1.075 | 19 | 1.810 | 0.442 | 99.980 | -1.158 | 53.956 |
| 10 | 452 | 6E9935DE-6967-440C-9B0F-B4A2A5E3C22B | B Road | B Road | other_urban | urban_b_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,661.500 | 0.086 | 19 | 1.769 | 0.321 | 99.979 | -1.823 | 52.480 |

## Road Classification: Unclassified

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 165 | 87A56F0E-7C15-4816-8BCA-F895D218CD1F | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,956.200 | 0.087 | 36 | 2.945 | 0.125 | 99.992 | -0.376 | 53.750 |
| 2 | 427 | 3FB669BD-4581-4F1C-B4D3-7B09ABD166B2 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,842.000 | 0.338 | 20 | 1.815 | 0.245 | 99.980 | -1.781 | 52.483 |
| 3 | 519 | E5864850-D299-469E-B526-862E5F0D4F9C | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,346.900 | 0.140 | 20 | 1.654 | 0.128 | 99.976 | -1.154 | 52.956 |
| 4 | 608 | 82EA9722-CEEB-4310-B0B5-5F161DA1F9DD | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,869.000 | 3.955 | 16 | 1.532 | 0.456 | 99.972 | -3.045 | 53.623 |
| 5 | 659 | 197A98EA-3CA3-4BD6-87BB-6A3E8B794DF7 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,936.900 | 0.042 | 20 | 1.483 | 0.079 | 99.970 | -0.543 | 53.230 |
| 6 | 684 | 65CE239A-3621-44FA-ADF6-5657AF3A5508 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 6,070.800 | 0.236 | 16 | 1.466 | 0.260 | 99.968 | -1.520 | 53.806 |
| 7 | 720 | 2AFBB011-5C0A-4265-B3AD-8CA4E1E0C272 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,887.400 | 0.223 | 16 | 1.444 | 0.226 | 99.967 | -2.980 | 53.404 |
| 8 | 728 | 51A08DFB-46BA-4A1A-B2DF-DC23C1E888DA | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,263.100 | 0.157 | 16 | 1.438 | 0.218 | 99.966 | -0.358 | 53.738 |
| 9 | 988 | 98BBC197-9873-482D-B90A-5EE7681BA1ED | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,048.600 | 0.105 | 15 | 1.263 | 0.138 | 99.954 | -1.915 | 52.474 |
| 10 | 1,005 | 00ADC461-C483-43D0-96D4-0A9D90AD959D | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,521.600 | 0.087 | 14 | 1.256 | 0.210 | 99.954 | -1.543 | 53.799 |

## Road Archetype: motorway

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 60,783.200 | 10.633 | 136 | 13.594 | 11.112 | 100.000 | -2.397 | 53.252 |
| 2 | 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 89,230.000 | 4.910 | 129 | 12.884 | 8.360 | 100.000 | -1.686 | 53.744 |
| 3 | 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 78,308.800 | 5.066 | 123 | 12.259 | 5.063 | 100.000 | -1.826 | 52.507 |
| 4 | 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 48,140.500 | 8.245 | 119 | 11.845 | 4.072 | 100.000 | -1.611 | 52.469 |
| 5 | 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 48,862.600 | 11.595 | 110 | 10.994 | 9.044 | 100.000 | -1.333 | 52.427 |
| 6 | 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 55,438.900 | 8.304 | 107 | 10.683 | 6.724 | 100.000 | -1.205 | 53.456 |
| 7 | 7 | EEDCD4A3-3046-4C4E-8DAE-2DF46525E19F | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 61,259.400 | 7.339 | 105 | 10.480 | 6.166 | 100.000 | -2.339 | 53.104 |
| 8 | 8 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 71,928.400 | 7.765 | 104 | 10.383 | 6.527 | 100.000 | -2.752 | 53.289 |
| 9 | 9 | D4178A17-E84A-4B2E-8904-3052B12EBCED | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 57,746.100 | 8.182 | 94 | 9.383 | 5.864 | 100.000 | -1.685 | 52.573 |
| 10 | 10 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 72,431.700 | 5.266 | 93 | 9.271 | 4.659 | 100.000 | -2.366 | 53.177 |

## Road Archetype: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 30 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 35,033.000 | 2.097 | 64 | 6.382 | 3.978 | 99.999 | -1.237 | 53.626 |
| 2 | 49 | F92239D4-36BC-45FF-8B98-7B4FF2CF81C0 | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 16,257.800 | 0.056 | 58 | 5.300 | 0.291 | 99.998 | -2.953 | 53.493 |
| 3 | 54 | F8C83919-A991-4C0F-980E-148BFB912405 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,865.300 | 8.549 | 52 | 5.143 | 1.726 | 99.998 | -0.348 | 53.602 |
| 4 | 61 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,767.600 | 11.654 | 49 | 4.889 | 3.580 | 99.997 | -1.976 | 52.936 |
| 5 | 74 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,917.400 | 6.793 | 45 | 4.468 | 2.109 | 99.997 | 0.354 | 52.247 |
| 6 | 75 | 43BC8837-2592-43A6-89FF-6762DCC1611D | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 26,908.600 | 2.791 | 45 | 4.446 | 1.544 | 99.997 | 1.573 | 52.632 |
| 7 | 84 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,088.900 | 4.039 | 42 | 4.189 | 3.030 | 99.996 | -1.452 | 52.974 |
| 8 | 94 | A8CF56A0-06EA-4E02-82B5-8D7B18189D7F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,047.800 | 2.554 | 41 | 4.015 | 1.016 | 99.996 | 1.087 | 52.025 |
| 9 | 95 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,033.900 | 7.489 | 40 | 3.999 | 3.841 | 99.996 | -1.501 | 52.866 |
| 10 | 96 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,475.000 | 7.408 | 40 | 3.988 | 2.811 | 99.996 | -0.975 | 52.403 |

## Road Archetype: urban_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 105 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 29,499.600 | 3.374 | 38 | 3.771 | 1.877 | 99.995 | -0.450 | 53.703 |
| 2 | 115 | 1C5FCE8A-EB04-48CF-A2C7-79E66C780A0F | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 27,669.100 | 2.615 | 37 | 3.649 | 1.331 | 99.995 | -0.556 | 53.251 |
| 3 | 129 | BFB5EAAC-3BE4-4B03-B0BF-654BB6A871F3 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 13,667.100 | 0.197 | 35 | 3.365 | 0.595 | 99.994 | -1.153 | 52.955 |
| 4 | 139 | 16D5C305-8230-4568-A0C5-F8146A963EA6 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,918.700 | 0.836 | 33 | 3.187 | 0.650 | 99.994 | -0.264 | 52.546 |
| 5 | 142 | 7E67F595-0DA0-491F-A17C-2496A75EF427 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 27,906.300 | 3.517 | 32 | 3.170 | 1.555 | 99.993 | -2.796 | 53.377 |
| 6 | 146 | 63B62281-35C8-4F62-B760-B6949F51ED5C | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 14,092.100 | 0.089 | 33 | 3.128 | 0.450 | 99.993 | -1.179 | 52.964 |
| 7 | 152 | 65ECF41C-0895-4918-B54F-64EB0FCFBB15 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 15,155.900 | 0.009 | 33 | 3.063 | 0.334 | 99.993 | -1.743 | 53.794 |
| 8 | 154 | EEF807BC-30B7-480F-855A-3C86F95040C8 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 29,486.000 | 1.738 | 31 | 3.060 | 1.281 | 99.993 | -1.363 | 53.394 |
| 9 | 155 | 35598324-6978-48F4-BCB9-33DC32D6B118 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,143.700 | 0.251 | 37 | 3.036 | 0.127 | 99.993 | -0.330 | 53.768 |
| 10 | 156 | 0824FEC1-4845-433E-BB69-AEDB8F1633D1 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 16,603.000 | 0.235 | 32 | 3.023 | 0.425 | 99.993 | -1.838 | 52.517 |

## Road Archetype: rural_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 311 | 4F7AA121-68AC-4F36-A483-DB2CC1A64202 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,657.900 | 4.065 | 22 | 2.179 | 1.271 | 99.986 | -0.208 | 52.621 |
| 2 | 329 | E5412A99-F27C-4D22-A253-FF9DA03A6AD1 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 16,058.200 | 1.304 | 22 | 2.085 | 0.420 | 99.985 | -0.983 | 52.772 |
| 3 | 382 | 75075385-9C0E-4B5C-8119-957239230DFC | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,440.800 | 1.048 | 21 | 1.908 | 0.251 | 99.982 | -0.484 | 53.292 |
| 4 | 542 | BA68C73F-4D0A-42FE-9D79-8BB47C55C9B4 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 12,405.000 | 0.637 | 17 | 1.614 | 0.408 | 99.975 | -0.057 | 52.923 |
| 5 | 554 | E56501E8-3ACB-46DD-B6B1-397BF24F3499 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 11,919.300 | 4.878 | 16 | 1.601 | 1.672 | 99.974 | -1.052 | 52.239 |
| 6 | 600 | 7029D21C-8EDD-4FB4-B958-58AF901A9EDF | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 8,215.200 | 2.589 | 16 | 1.542 | 0.513 | 99.972 | -1.594 | 53.109 |
| 7 | 607 | 195A6448-2614-4A63-BA21-2271C0708C3D | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 10,884.000 | 0.861 | 16 | 1.533 | 0.463 | 99.972 | -1.566 | 53.936 |
| 8 | 619 | F8EB83E6-E75C-47BB-86BF-6C1FAB5C1B4E | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 14,129.200 | 0.619 | 17 | 1.520 | 0.211 | 99.971 | -0.551 | 53.548 |
| 9 | 681 | 03CE9061-A22B-43A8-B558-35C2671DAB7E | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 10,537.300 | 2.687 | 15 | 1.468 | 0.693 | 99.969 | -1.623 | 53.320 |
| 10 | 740 | CF7EDF58-3627-48D3-88D7-4F4007136CF1 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 13,941.200 | 1.680 | 15 | 1.422 | 0.384 | 99.966 | -0.781 | 52.375 |

## Road Archetype: urban_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 158 | 8B16D730-145F-4EB7-B6A9-5976FB696D1F | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,839.200 | 0.150 | 32 | 3.014 | 0.406 | 99.993 | -2.445 | 53.746 |
| 2 | 201 | 50AC7915-813B-4763-8176-4C4E5D2911C6 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,011.400 | 1.884 | 29 | 2.739 | 0.417 | 99.991 | -0.050 | 52.352 |
| 3 | 301 | 10675A16-3ABA-4034-8F16-9FFC0CCA0625 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 15,737.200 | 0.417 | 23 | 2.198 | 0.487 | 99.986 | -1.891 | 52.499 |
| 4 | 343 | 4DB11F0A-D996-4587-A339-26267BF1E6B2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 7,764.700 | 0.168 | 22 | 2.027 | 0.290 | 99.984 | -0.355 | 53.768 |
| 5 | 362 | 5DDA098F-8582-4994-BD55-C927BDA18AC2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 16,162.500 | 0.309 | 21 | 1.980 | 0.385 | 99.983 | -1.521 | 52.423 |
| 6 | 371 | C1195BA3-6D8B-46AA-99D4-0CA40DF3B9F2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 15,018.200 | 0.372 | 21 | 1.949 | 0.315 | 99.983 | -1.923 | 52.617 |
| 7 | 413 | 99DAD5C8-AD6C-4D6C-9197-97F9D7C7DB36 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 11,905.600 | 0.110 | 20 | 1.855 | 0.308 | 99.981 | -1.888 | 52.475 |
| 8 | 425 | 33D5E262-9BF7-4BDB-B084-4EADD9A6E365 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 8,549.400 | 0.721 | 20 | 1.825 | 0.259 | 99.980 | -0.679 | 52.293 |
| 9 | 431 | C9ACE698-0977-45FB-83E5-85E673CA2EE1 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 12,016.800 | 1.075 | 19 | 1.810 | 0.442 | 99.980 | -1.158 | 53.956 |
| 10 | 452 | 6E9935DE-6967-440C-9B0F-B4A2A5E3C22B | B Road | B Road | other_urban | urban_b_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,661.500 | 0.086 | 19 | 1.769 | 0.321 | 99.979 | -1.823 | 52.480 |

## Road Archetype: rural_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 699 | 41EBB9AE-4F03-4D4E-9D0E-51EEB3D7BCB2 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 7,318.500 | 1.291 | 16 | 1.456 | 0.244 | 99.968 | -0.634 | 53.786 |
| 2 | 804 | 0E71C679-EA65-4F2B-9977-38927BE26F6E | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 10,578.100 | 0.654 | 15 | 1.375 | 0.258 | 99.963 | -1.248 | 53.365 |
| 3 | 831 | F10D4083-55D5-4094-94CB-CACA05C2D7DF | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 11,981.500 | 1.626 | 14 | 1.357 | 0.546 | 99.962 | -1.356 | 53.596 |
| 4 | 1,137 | FC3BD23B-DB93-4146-A467-4E0AE6F28E1B | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 7,705.100 | 1.057 | 13 | 1.189 | 0.247 | 99.948 | -3.040 | 53.521 |
| 5 | 1,290 | C80EEE2B-8E19-464C-9797-B70EF1068C21 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 5,128.300 | 0.542 | 14 | 1.137 | 0.113 | 99.941 | -1.589 | 52.485 |
| 6 | 1,304 | 9BEF64F7-0A98-44C5-9D04-6659BC928E58 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 7,397.300 | 1.525 | 12 | 1.130 | 0.332 | 99.940 | -1.586 | 52.605 |
| 7 | 1,389 | 4418CFB3-8A69-434C-BD96-4A146BA7910B | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 6,179.400 | 0.965 | 12 | 1.100 | 0.246 | 99.936 | 0.072 | 52.659 |
| 8 | 1,491 | B8D515CF-BADA-43E8-9158-07E2B2492E3B | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,294.900 | 1.053 | 12 | 1.074 | 0.201 | 99.931 | -1.625 | 52.200 |
| 9 | 1,597 | F39A956E-D089-4FF3-97E8-1BCC0AF7BE6D | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 7,159.800 | 1.017 | 11 | 1.046 | 0.365 | 99.926 | -1.350 | 53.812 |
| 10 | 1,911 | 89EE5B81-9E1D-4F24-9BF8-E35255E02865 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 6,753.200 | 1.581 | 10 | 0.971 | 0.485 | 99.912 | -2.093 | 52.939 |

## Road Archetype: urban_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 165 | 87A56F0E-7C15-4816-8BCA-F895D218CD1F | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,956.200 | 0.087 | 36 | 2.945 | 0.125 | 99.992 | -0.376 | 53.750 |
| 2 | 217 | 6FA816AE-B4FD-4E1D-94AB-30501E97ADF6 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,504.500 | 0.370 | 29 | 2.630 | 0.255 | 99.990 | -0.548 | 53.219 |
| 3 | 221 | 4435DC95-53B2-4912-8AEC-AF330489ED11 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,606.200 | 0.124 | 28 | 2.613 | 0.351 | 99.990 | -0.543 | 53.225 |
| 4 | 269 | 58AF7081-C5FF-4239-8D5B-CEC477724409 | Unknown | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,984.000 | 0.009 | 28 | 2.316 | 0.131 | 99.988 | -2.933 | 53.441 |
| 5 | 278 | 0AFF5EE0-3267-43D0-9EC5-CA6119303BE6 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 5,350.400 | 3.048 | 23 | 2.285 | 1.511 | 99.987 | -3.026 | 53.793 |
| 6 | 307 | 6A4DC099-8541-4671-908F-64DF143273D0 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,231.200 | 0.151 | 24 | 2.187 | 0.262 | 99.986 | -1.479 | 52.910 |
| 7 | 326 | C910A5C2-7048-4751-9013-8769E14AD8BC | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,428.700 | 0.282 | 22 | 2.091 | 0.437 | 99.985 | -0.273 | 53.758 |
| 8 | 363 | 6D2B61E1-2C45-4F4E-B027-CB05AC2F267F | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,006.400 | 0.178 | 21 | 1.978 | 0.380 | 99.983 | -1.915 | 52.475 |
| 9 | 427 | 3FB669BD-4581-4F1C-B4D3-7B09ABD166B2 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,842.000 | 0.338 | 20 | 1.815 | 0.245 | 99.980 | -1.781 | 52.483 |
| 10 | 503 | FA5F7264-2B23-49EF-842F-1F6EDA2814A6 | Unknown | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,246.300 | 0.130 | 22 | 1.675 | 0.088 | 99.977 | -0.363 | 53.787 |

## Road Archetype: rural_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 231 | 6EA22486-59DA-4A1F-A503-6FE157C1B266 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 590.400 | 2.228 | 31 | 2.536 | 0.124 | 99.989 | -2.510 | 53.639 |
| 2 | 528 | 6E9A0C83-DE15-47D7-B49A-B6E7C3390390 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,222.200 | 0.273 | 19 | 1.636 | 0.162 | 99.976 | -1.538 | 53.613 |
| 3 | 971 | F4BD04B7-082E-4553-8225-0A260234EA7F | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 872.700 | 2.266 | 15 | 1.271 | 0.143 | 99.955 | -2.731 | 54.058 |
| 4 | 1,116 | 105AC89B-8D74-40E3-BDA4-47F76F9A5296 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,750.900 | 0.522 | 16 | 1.199 | 0.081 | 99.949 | 0.810 | 52.246 |
| 5 | 1,574 | BF3895E2-B32C-4E56-BBB3-5FD653ECE8E1 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 633.000 | 2.469 | 13 | 1.052 | 0.110 | 99.927 | -0.487 | 54.264 |
| 6 | 2,056 | 6D7DC47C-9363-4B59-A2C4-C885C49A5F5C | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 997.700 | 1.415 | 12 | 0.948 | 0.098 | 99.905 | -1.018 | 52.962 |
| 7 | 2,240 | E8B19672-2773-42A8-98F2-8393D548685C | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,003.800 | 2.895 | 10 | 0.911 | 0.223 | 99.897 | -2.350 | 53.847 |
| 8 | 2,490 | EFDE7664-F824-4249-A6CD-21FC9D849CA2 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,141.400 | 0.612 | 10 | 0.872 | 0.161 | 99.885 | -1.670 | 52.574 |
| 9 | 2,535 | 9FD284E9-7963-485A-8F55-B80434F7E4D6 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,668.300 | 1.034 | 10 | 0.868 | 0.156 | 99.883 | -1.779 | 53.906 |
| 10 | 2,664 | 74788147-D695-4EF4-BF35-248631E9F43F | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 4,996.300 | 0.237 | 10 | 0.854 | 0.141 | 99.877 | -1.474 | 53.865 |

## Road Archetype: other_unknown

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 196 | 4158BCEE-7926-475E-9CCF-F464B6F8E137 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 3,649.200 | 7.573 | 29 | 2.783 | 0.554 | 99.991 | -1.875 | 53.432 |
| 2 | 241 | 7BF88232-B992-4162-8A4F-691D46F186E7 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 10,514.200 | 4.288 | 25 | 2.478 | 1.397 | 99.989 | -0.360 | 52.525 |
| 3 | 286 | 1942361E-5A0E-4926-B8F2-AAC3EB2AB46A | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 6,234.700 | 2.647 | 23 | 2.233 | 0.671 | 99.987 | -2.355 | 53.071 |
| 4 | 291 | 36FB8B57-4494-4469-95CE-D46C9A54FF23 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 5,587.600 | 2.710 | 24 | 2.220 | 0.308 | 99.987 | -0.248 | 52.793 |
| 5 | 364 | B303D610-A520-4619-81E3-3AA9ED7BDDA9 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 7,524.000 | 3.422 | 20 | 1.965 | 0.885 | 99.983 | -0.186 | 52.653 |
| 6 | 373 | D98C3D9A-C954-4A9D-AE6C-1B7A54D8495F | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 6,911.000 | 2.503 | 20 | 1.942 | 0.645 | 99.983 | 0.021 | 53.306 |
| 7 | 409 | 40DDE02A-7B4B-4BD4-9BBD-E8437DFF6A64 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 5,215.200 | 0.849 | 20 | 1.857 | 0.312 | 99.981 | -1.216 | 54.237 |
| 8 | 424 | 65825479-8993-4C9B-8E0F-492D499B0870 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 8,401.200 | 0.791 | 20 | 1.826 | 0.261 | 99.980 | -0.486 | 53.126 |
| 9 | 437 | A7516B09-B4F0-4906-947F-2ED4B3CF0821 | A Road | A Road | other_unknown | other_unknown | Collapsed Dual Carriageway | 1 | 0 | 0 | 19,848.000 | 4.445 | 18 | 1.796 | 1.566 | 99.980 | -0.450 | 53.657 |
| 10 | 495 | DF3B328C-54DE-44DC-BB3B-01EF9BD66434 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 5,865.300 | 2.904 | 18 | 1.690 | 0.353 | 99.977 | -1.733 | 53.377 |

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
