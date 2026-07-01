# Top-Risk Links By Comparable Road Group

## Purpose

The global top-1% table is useful, but the very top of that ranking can be dominated by high-volume motorway links. These group-specific tables help inspect high-risk links among comparable road families, OS road classes, and conservative reporting archetypes.

## Summary

| group_type | groups | top_n_per_group | rows |
| --- | --- | --- | --- |
| family | 5 | 100 | 403 |
| road_classification | 7 | 100 | 700 |
| road_archetype | 9 | 100 | 803 |

Ranking field used: `risk_percentile`.

Created at: `2026-07-01T18:43:32+00:00`.

## Road-Type Schemes Used Here

- `family` is the official comparable-road-type modelling/diagnostic split: `motorway`, `trunk_a`, `other_urban`, `other_rural`, plus `other_unknown` as a fallback/reporting bucket when the family inputs do not resolve cleanly.
- `road_classification` is the broad OS Open Roads classification axis (`Motorway`, `A Road`, `B Road`, `Classified Unnumbered`, `Unclassified`, `Not Classified`, `Unknown`). It is useful for inspection but is not the same thing as the modelling family split.
- `road_function` is the OS functional category, retained as descriptive context because it is often more informative below trunk-road scale.
- `form_of_way` and derived flags (`is_dual`, `is_slip_road`, `is_roundabout`) describe physical form. They are important map/filter fields, but the repo's v1 family design explicitly did not adopt dual/single/roundabout/slip as separate families.
- `road_archetype` is a conservative reporting convenience that combines `family` with broad road class. It is not a model family and should not be read as a new production ranking surface.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores.parquet | 2026-07-01T00:45:59.477722+00:00 | 151,405,508 |
| data/processed/shapefiles/openroads.parquet | 2026-04-29T00:35:29.349109+00:00 | 392,911,115 |
| data/features/network_features.parquet | 2026-06-30T23:35:35.810308+00:00 | 223,068,149 |

Project/model output version: `0.1.0`.

## Count By Road Archetype

Each archetype table contains the top 100 links within that archetype, so the count table below shows output allocation rather than population prevalence. For prevalence, use the global top-1% `Count By Road Archetype` table.

| road_archetype | count | share |
| --- | --- | --- |
| motorway | 100 | 12.5% |
| rural_a_road | 100 | 12.5% |
| rural_b_road | 100 | 12.5% |
| rural_minor | 100 | 12.5% |
| trunk_a | 100 | 12.5% |
| urban_b_road | 100 | 12.5% |
| urban_a_road | 100 | 12.5% |
| urban_minor | 100 | 12.5% |
| other_unknown | 3 | 0.4% |

## Family: motorway

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 60,783.200 | 10.633 | 135 | 9.823 | -2.397 | 53.252 |
| 2 | 2 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 51,867.300 | 16.221 | 90 | 9.789 | -1.188 | 52.526 |
| 3 | 3 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 48,862.600 | 11.595 | 111 | 8.231 | -1.333 | 52.427 |
| 4 | 4 | BBB307EC-410E-4741-B22C-9DE761845549 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 44,108.600 | 16.045 | 57 | 7.986 | -1.390 | 52.130 |
| 5 | 5 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 89,230.000 | 4.910 | 129 | 7.944 | -1.686 | 53.744 |
| 6 | 6 | F5E342B6-EE33-4F30-92BD-1A5670B41BE4 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 97,711.900 | 6.021 | 30 | 7.931 | -1.304 | 52.884 |
| 7 | 7 | 41A19ED6-5441-400A-8F13-095A42A69E0B | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 89,308.900 | 7.485 | 49 | 7.662 | -2.430 | 53.455 |
| 8 | 8 | 1C2CFBA6-441D-4A61-A277-DA84E8F445FF | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 93,118.300 | 5.393 | 87 | 7.371 | -1.792 | 53.681 |
| 9 | 9 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 78,308.800 | 5.066 | 122 | 7.308 | -1.826 | 52.507 |
| 10 | 10 | C88EE264-D645-4EEB-B759-332F064347E4 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 66,244.800 | 8.959 | 69 | 7.299 | -2.209 | 52.935 |

## Family: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 65 | 65BA14C9-05CF-4ED8-AB6E-F76B69344D16 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 26,425.100 | 6.488 | 37 | 4.283 | -1.648 | 52.816 |
| 2 | 72 | 980A4752-91AD-4B78-8D85-FC7BC10F4106 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 32,780.300 | 6.140 | 39 | 4.090 | -1.438 | 53.027 |
| 3 | 80 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,767.600 | 11.654 | 48 | 3.893 | -1.976 | 52.936 |
| 4 | 100 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,033.900 | 7.489 | 40 | 3.486 | -1.501 | 52.866 |
| 5 | 106 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 35,033.000 | 2.097 | 62 | 3.424 | -1.237 | 53.626 |
| 6 | 119 | 5A06A2A0-3648-46B2-B91E-D5F8EA000B77 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 27,967.400 | 7.167 | 15 | 3.203 | -1.412 | 52.781 |
| 7 | 134 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,088.900 | 4.039 | 42 | 3.027 | -1.452 | 52.974 |
| 8 | 135 | 5088ECCF-1253-4615-98B0-B86A78AE9F8A | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,240.000 | 10.608 | 33 | 3.026 | 0.602 | 52.361 |
| 9 | 141 | EED25C47-4544-4CE8-9911-4C61EB5B4C6A | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 8,378.000 | 8.117 | 26 | 2.922 | -0.851 | 53.199 |
| 10 | 156 | E1AC0C71-21A6-4F45-ACAD-7A3C4E0EF99F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,717.400 | 9.050 | 29 | 2.830 | -1.102 | 52.395 |

## Family: other_urban

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 194 | 0C94874C-B9CE-42E2-B3D5-DFF1BD0E6358 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 26,877.400 | 5.522 | 24 | 2.471 | -1.472 | 53.291 |
| 2 | 216 | D4BB3DD4-0E97-4836-A859-49562A809C14 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 37,381.200 | 3.178 | 14 | 2.302 | -1.402 | 53.221 |
| 3 | 308 | 8052BE32-C298-4EBE-9DDB-BFA080ED1AE0 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,837.800 | 3.731 | 17 | 1.698 | -1.893 | 52.389 |
| 4 | 334 | DA9D6C85-144F-4378-9982-7515E9011AF0 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 23,764.200 | 2.447 | 20 | 1.597 | -1.395 | 53.366 |
| 5 | 345 | F97064ED-C237-4D44-BAF3-9F3175BB3508 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 15,492.300 | 2.964 | 12 | 1.548 | -0.836 | 52.435 |
| 6 | 354 | 58DCCA6D-CC1F-43B2-9352-060A40A37EED | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 28,915.600 | 0.212 | 17 | 1.516 | -1.170 | 52.961 |
| 7 | 355 | 6A3D2D1E-D14A-4D89-B29D-1D4D615A5080 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,311.300 | 2.639 | 2 | 1.516 | -3.006 | 53.414 |
| 8 | 356 | EEF807BC-30B7-480F-855A-3C86F95040C8 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 29,486.000 | 1.738 | 31 | 1.510 | -1.363 | 53.394 |
| 9 | 358 | 9B7133A4-1631-43EE-8CC6-6A33EC90CE9D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,932.000 | 3.847 | 22 | 1.507 | -1.924 | 53.889 |
| 10 | 378 | A6837F2E-09F4-428D-B50D-9E03FE6B5AAB | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 24,003.700 | 0.341 | 24 | 1.429 | -1.967 | 52.510 |

## Family: other_rural

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 234 | 7E90F309-C9E6-4DF8-B923-884C83F21BA8 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,530.900 | 5.875 | 7 | 2.164 | -0.703 | 52.461 |
| 2 | 249 | 89D775E5-B175-45FA-9009-D353F84D302F | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 20,920.700 | 5.057 | 9 | 2.085 | -1.945 | 53.334 |
| 3 | 310 | E56501E8-3ACB-46DD-B6B1-397BF24F3499 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 11,919.300 | 4.878 | 16 | 1.692 | -1.052 | 52.239 |
| 4 | 326 | 59FFE4B6-01EB-478C-A8DE-17370D48427D | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 5,922.500 | 6.596 | 11 | 1.629 | -0.126 | 52.716 |
| 5 | 367 | 8620C2C5-CC9B-465D-BEE2-A8C0131E7D12 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 18,153.300 | 3.807 | 11 | 1.466 | -2.422 | 53.822 |
| 6 | 369 | 7BF88232-B992-4162-8A4F-691D46F186E7 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 10,514.200 | 4.288 | 25 | 1.458 | -0.360 | 52.525 |
| 7 | 413 | 4F7AA121-68AC-4F36-A483-DB2CC1A64202 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,657.900 | 4.065 | 22 | 1.335 | -0.208 | 52.621 |
| 8 | 422 | E997C98A-8910-4A9A-A070-0701F379C461 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 10,132.900 | 2.723 | 20 | 1.313 | -0.021 | 52.840 |
| 9 | 431 | D45E8FA7-81BC-44A3-A28C-A9B7E9E179CB | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 14,487.000 | 2.950 | 3 | 1.284 | -1.215 | 54.118 |
| 10 | 448 | F044802C-D97E-4681-B63D-9E424120BF63 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 23,938.900 | 3.456 | 6 | 1.254 | 1.168 | 52.377 |

## Road Classification: A Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 65 | 65BA14C9-05CF-4ED8-AB6E-F76B69344D16 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 26,425.100 | 6.488 | 37 | 4.283 | -1.648 | 52.816 |
| 2 | 72 | 980A4752-91AD-4B78-8D85-FC7BC10F4106 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 32,780.300 | 6.140 | 39 | 4.090 | -1.438 | 53.027 |
| 3 | 80 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,767.600 | 11.654 | 48 | 3.893 | -1.976 | 52.936 |
| 4 | 100 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,033.900 | 7.489 | 40 | 3.486 | -1.501 | 52.866 |
| 5 | 106 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 35,033.000 | 2.097 | 62 | 3.424 | -1.237 | 53.626 |
| 6 | 113 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | A Road | other_unknown | other_unknown | Collapsed Dual Carriageway | 1 | 0 | 0 | 29,499.600 | 3.374 | 38 | 3.310 | -0.450 | 53.703 |
| 7 | 119 | 5A06A2A0-3648-46B2-B91E-D5F8EA000B77 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 27,967.400 | 7.167 | 15 | 3.203 | -1.412 | 52.781 |
| 8 | 134 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,088.900 | 4.039 | 42 | 3.027 | -1.452 | 52.974 |
| 9 | 135 | 5088ECCF-1253-4615-98B0-B86A78AE9F8A | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,240.000 | 10.608 | 33 | 3.026 | 0.602 | 52.361 |
| 10 | 141 | EED25C47-4544-4CE8-9911-4C61EB5B4C6A | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 8,378.000 | 8.117 | 26 | 2.922 | -0.851 | 53.199 |

## Road Classification: B Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 530 | 08FD9A0B-E2ED-42CA-BBA7-A64A5A92C4EC | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,557.200 | 1.942 | 2 | 1.070 | -1.427 | 53.431 |
| 2 | 841 | 903A6F71-6F14-4C5A-9C21-4FC7FE00BEF3 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 15,800.800 | 0.983 | 2 | 0.798 | -2.715 | 53.332 |
| 3 | 923 | 91C22F5A-3A4A-4B2A-B1CF-22698BA28BEE | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 16,847.700 | 0.174 | 0 | 0.758 | -1.227 | 54.572 |
| 4 | 933 | C784F8EB-237F-4372-A437-594EEB8C2426 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 8,475.100 | 2.108 | 18 | 0.751 | -1.596 | 53.661 |
| 5 | 1,012 | B8BC385E-1068-4734-8AF8-FD237F3FC9A5 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,111.600 | 0.269 | 3 | 0.717 | -3.009 | 53.375 |
| 6 | 1,084 | C09D8618-925E-400C-ACC0-21429682FEE2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 19,778.900 | 0.125 | 0 | 0.697 | -1.236 | 54.573 |
| 7 | 1,098 | C10AB286-2FC8-446B-B9B9-3CF56FD88CD2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 11,244.200 | 0.267 | 3 | 0.691 | -1.852 | 52.488 |
| 8 | 1,161 | D9AE138E-3ED4-4F36-B93E-E44B27031266 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 13,644.300 | 1.992 | 9 | 0.673 | -1.522 | 52.509 |
| 9 | 1,183 | CABCBCCB-D26A-403B-B7BE-72638F3E9EAD | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,750.900 | 0.139 | 16 | 0.669 | -2.219 | 53.442 |
| 10 | 1,189 | 52FD4847-E4E3-494E-A9E6-7D8D083F38C1 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,672.100 | 0.140 | 11 | 0.668 | -1.897 | 52.499 |

## Road Classification: Unclassified

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 542 | 2F860946-7F25-41A8-96DB-377DAC95BE55 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,741.100 | 0.102 | 7 | 1.055 | -1.541 | 53.796 |
| 2 | 672 | 3544ABE8-D8FF-4830-912E-D469999D403E | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,333.200 | 0.147 | 12 | 0.924 | -1.541 | 53.799 |
| 3 | 1,248 | 1799A1DA-D84A-44A4-8ADB-5AE09ED584B1 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,764.700 | 0.130 | 7 | 0.653 | -1.540 | 53.798 |
| 4 | 1,485 | 6534C4C5-3483-44D6-BCD8-3BADC7E9CC60 | Unclassified | Local Road | other_urban | urban_minor | Collapsed Dual Carriageway | 1 | 0 | 0 | 3,507.400 | 0.112 | 8 | 0.605 | -1.545 | 53.800 |
| 5 | 1,603 | 82EA9722-CEEB-4310-B0B5-5F161DA1F9DD | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,869.000 | 3.955 | 16 | 0.587 | -3.045 | 53.623 |
| 6 | 1,696 | FDFAE69E-289B-43A9-B405-A09A618DA7AF | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,805.900 | 0.108 | 4 | 0.573 | -1.511 | 52.412 |
| 7 | 2,193 | E65741BC-51FD-4D26-928C-7B96BB93E213 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,871.600 | 0.072 | 7 | 0.522 | -1.542 | 53.796 |
| 8 | 2,263 | 9BC9ACDC-F03D-4C4A-818A-36AD74742433 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 5,194.300 | 0.220 | 6 | 0.516 | -1.775 | 52.481 |
| 9 | 2,423 | 4D221F64-3055-4F1D-97E9-EA1BC566094A | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,622.500 | 0.060 | 2 | 0.503 | -1.547 | 53.796 |
| 10 | 2,459 | 5E883A9C-2F74-43E5-B65E-65C3417825C0 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,835.300 | 0.060 | 1 | 0.501 | -1.545 | 53.799 |

## Road Archetype: motorway

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 60,783.200 | 10.633 | 135 | 9.823 | -2.397 | 53.252 |
| 2 | 2 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 51,867.300 | 16.221 | 90 | 9.789 | -1.188 | 52.526 |
| 3 | 3 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 48,862.600 | 11.595 | 111 | 8.231 | -1.333 | 52.427 |
| 4 | 4 | BBB307EC-410E-4741-B22C-9DE761845549 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 44,108.600 | 16.045 | 57 | 7.986 | -1.390 | 52.130 |
| 5 | 5 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 89,230.000 | 4.910 | 129 | 7.944 | -1.686 | 53.744 |
| 6 | 6 | F5E342B6-EE33-4F30-92BD-1A5670B41BE4 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 97,711.900 | 6.021 | 30 | 7.931 | -1.304 | 52.884 |
| 7 | 7 | 41A19ED6-5441-400A-8F13-095A42A69E0B | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 89,308.900 | 7.485 | 49 | 7.662 | -2.430 | 53.455 |
| 8 | 8 | 1C2CFBA6-441D-4A61-A277-DA84E8F445FF | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 93,118.300 | 5.393 | 87 | 7.371 | -1.792 | 53.681 |
| 9 | 9 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 78,308.800 | 5.066 | 122 | 7.308 | -1.826 | 52.507 |
| 10 | 10 | C88EE264-D645-4EEB-B759-332F064347E4 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 66,244.800 | 8.959 | 69 | 7.299 | -2.209 | 52.935 |

## Road Archetype: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 65 | 65BA14C9-05CF-4ED8-AB6E-F76B69344D16 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 26,425.100 | 6.488 | 37 | 4.283 | -1.648 | 52.816 |
| 2 | 72 | 980A4752-91AD-4B78-8D85-FC7BC10F4106 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 32,780.300 | 6.140 | 39 | 4.090 | -1.438 | 53.027 |
| 3 | 80 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,767.600 | 11.654 | 48 | 3.893 | -1.976 | 52.936 |
| 4 | 100 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,033.900 | 7.489 | 40 | 3.486 | -1.501 | 52.866 |
| 5 | 106 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 35,033.000 | 2.097 | 62 | 3.424 | -1.237 | 53.626 |
| 6 | 119 | 5A06A2A0-3648-46B2-B91E-D5F8EA000B77 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 27,967.400 | 7.167 | 15 | 3.203 | -1.412 | 52.781 |
| 7 | 134 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,088.900 | 4.039 | 42 | 3.027 | -1.452 | 52.974 |
| 8 | 135 | 5088ECCF-1253-4615-98B0-B86A78AE9F8A | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,240.000 | 10.608 | 33 | 3.026 | 0.602 | 52.361 |
| 9 | 141 | EED25C47-4544-4CE8-9911-4C61EB5B4C6A | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 8,378.000 | 8.117 | 26 | 2.922 | -0.851 | 53.199 |
| 10 | 156 | E1AC0C71-21A6-4F45-ACAD-7A3C4E0EF99F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,717.400 | 9.050 | 29 | 2.830 | -1.102 | 52.395 |

## Road Archetype: urban_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 194 | 0C94874C-B9CE-42E2-B3D5-DFF1BD0E6358 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 26,877.400 | 5.522 | 24 | 2.471 | -1.472 | 53.291 |
| 2 | 216 | D4BB3DD4-0E97-4836-A859-49562A809C14 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 37,381.200 | 3.178 | 14 | 2.302 | -1.402 | 53.221 |
| 3 | 308 | 8052BE32-C298-4EBE-9DDB-BFA080ED1AE0 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,837.800 | 3.731 | 17 | 1.698 | -1.893 | 52.389 |
| 4 | 334 | DA9D6C85-144F-4378-9982-7515E9011AF0 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 23,764.200 | 2.447 | 20 | 1.597 | -1.395 | 53.366 |
| 5 | 345 | F97064ED-C237-4D44-BAF3-9F3175BB3508 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 15,492.300 | 2.964 | 12 | 1.548 | -0.836 | 52.435 |
| 6 | 354 | 58DCCA6D-CC1F-43B2-9352-060A40A37EED | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 28,915.600 | 0.212 | 17 | 1.516 | -1.170 | 52.961 |
| 7 | 355 | 6A3D2D1E-D14A-4D89-B29D-1D4D615A5080 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,311.300 | 2.639 | 2 | 1.516 | -3.006 | 53.414 |
| 8 | 356 | EEF807BC-30B7-480F-855A-3C86F95040C8 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 29,486.000 | 1.738 | 31 | 1.510 | -1.363 | 53.394 |
| 9 | 358 | 9B7133A4-1631-43EE-8CC6-6A33EC90CE9D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,932.000 | 3.847 | 22 | 1.507 | -1.924 | 53.889 |
| 10 | 378 | A6837F2E-09F4-428D-B50D-9E03FE6B5AAB | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 24,003.700 | 0.341 | 24 | 1.429 | -1.967 | 52.510 |

## Road Archetype: rural_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 234 | 7E90F309-C9E6-4DF8-B923-884C83F21BA8 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,530.900 | 5.875 | 7 | 2.164 | -0.703 | 52.461 |
| 2 | 249 | 89D775E5-B175-45FA-9009-D353F84D302F | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 20,920.700 | 5.057 | 9 | 2.085 | -1.945 | 53.334 |
| 3 | 310 | E56501E8-3ACB-46DD-B6B1-397BF24F3499 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 11,919.300 | 4.878 | 16 | 1.692 | -1.052 | 52.239 |
| 4 | 326 | 59FFE4B6-01EB-478C-A8DE-17370D48427D | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 5,922.500 | 6.596 | 11 | 1.629 | -0.126 | 52.716 |
| 5 | 367 | 8620C2C5-CC9B-465D-BEE2-A8C0131E7D12 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 18,153.300 | 3.807 | 11 | 1.466 | -2.422 | 53.822 |
| 6 | 369 | 7BF88232-B992-4162-8A4F-691D46F186E7 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 10,514.200 | 4.288 | 25 | 1.458 | -0.360 | 52.525 |
| 7 | 413 | 4F7AA121-68AC-4F36-A483-DB2CC1A64202 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,657.900 | 4.065 | 22 | 1.335 | -0.208 | 52.621 |
| 8 | 422 | E997C98A-8910-4A9A-A070-0701F379C461 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 10,132.900 | 2.723 | 20 | 1.313 | -0.021 | 52.840 |
| 9 | 431 | D45E8FA7-81BC-44A3-A28C-A9B7E9E179CB | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 14,487.000 | 2.950 | 3 | 1.284 | -1.215 | 54.118 |
| 10 | 448 | F044802C-D97E-4681-B63D-9E424120BF63 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 23,938.900 | 3.456 | 6 | 1.254 | 1.168 | 52.377 |

## Road Archetype: urban_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 530 | 08FD9A0B-E2ED-42CA-BBA7-A64A5A92C4EC | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,557.200 | 1.942 | 2 | 1.070 | -1.427 | 53.431 |
| 2 | 841 | 903A6F71-6F14-4C5A-9C21-4FC7FE00BEF3 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 15,800.800 | 0.983 | 2 | 0.798 | -2.715 | 53.332 |
| 3 | 923 | 91C22F5A-3A4A-4B2A-B1CF-22698BA28BEE | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 16,847.700 | 0.174 | 0 | 0.758 | -1.227 | 54.572 |
| 4 | 933 | C784F8EB-237F-4372-A437-594EEB8C2426 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 8,475.100 | 2.108 | 18 | 0.751 | -1.596 | 53.661 |
| 5 | 1,012 | B8BC385E-1068-4734-8AF8-FD237F3FC9A5 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,111.600 | 0.269 | 3 | 0.717 | -3.009 | 53.375 |
| 6 | 1,084 | C09D8618-925E-400C-ACC0-21429682FEE2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 19,778.900 | 0.125 | 0 | 0.697 | -1.236 | 54.573 |
| 7 | 1,098 | C10AB286-2FC8-446B-B9B9-3CF56FD88CD2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 11,244.200 | 0.267 | 3 | 0.691 | -1.852 | 52.488 |
| 8 | 1,161 | D9AE138E-3ED4-4F36-B93E-E44B27031266 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 13,644.300 | 1.992 | 9 | 0.673 | -1.522 | 52.509 |
| 9 | 1,183 | CABCBCCB-D26A-403B-B7BE-72638F3E9EAD | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,750.900 | 0.139 | 16 | 0.669 | -2.219 | 53.442 |
| 10 | 1,189 | 52FD4847-E4E3-494E-A9E6-7D8D083F38C1 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,672.100 | 0.140 | 11 | 0.668 | -1.897 | 52.499 |

## Road Archetype: rural_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,443 | F10D4083-55D5-4094-94CB-CACA05C2D7DF | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 11,981.500 | 1.626 | 14 | 0.613 | -1.356 | 53.596 |
| 2 | 1,670 | 3ED3C2E2-4A1A-4CB0-8A4B-2FDD56124A98 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 9,882.700 | 2.191 | 7 | 0.577 | -2.309 | 52.348 |
| 3 | 1,768 | FC2665C5-0AD2-4683-9A2F-CA9B985B9951 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 7,756.100 | 1.822 | 3 | 0.564 | -1.452 | 52.980 |
| 4 | 1,793 | 20AB2E37-034B-4B3D-BC28-EECB1559AAE6 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 3,658.500 | 3.823 | 6 | 0.561 | -0.323 | 52.850 |
| 5 | 1,835 | 1F099E61-1799-4B74-A660-50EEB2E5EC15 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 9,079.000 | 1.641 | 13 | 0.557 | -0.895 | 53.487 |
| 6 | 2,052 | 275D73CD-DDB0-4E54-8361-550A9F9BD2F1 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 5,019.100 | 2.026 | 2 | 0.534 | -0.922 | 53.487 |
| 7 | 2,083 | BDEF49B0-651D-4D1F-A447-FC07DC43957E | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 5,670.400 | 3.071 | 3 | 0.531 | 0.624 | 52.750 |
| 8 | 2,266 | A3A1FDD9-0B7A-4279-8803-79EF7817031F | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 3,761.000 | 3.565 | 2 | 0.516 | 0.063 | 52.366 |
| 9 | 2,283 | 89EE5B81-9E1D-4F24-9BF8-E35255E02865 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 6,753.200 | 1.581 | 13 | 0.515 | -2.093 | 52.939 |
| 10 | 2,356 | A73F5D72-09B5-4573-9421-FC0A0F82982E | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 9,359.100 | 1.528 | 5 | 0.509 | -1.376 | 54.084 |

## Road Archetype: urban_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 385 | 0AFF5EE0-3267-43D0-9EC5-CA6119303BE6 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 5,350.400 | 3.048 | 23 | 1.418 | -3.026 | 53.793 |
| 2 | 542 | 2F860946-7F25-41A8-96DB-377DAC95BE55 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,741.100 | 0.102 | 7 | 1.055 | -1.541 | 53.796 |
| 3 | 564 | 2CAA0FA4-E20E-4595-9D7F-9E0EF862DAC0 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,662.700 | 0.177 | 7 | 1.030 | -1.885 | 52.455 |
| 4 | 664 | EF55F308-7758-4857-BE3D-6BC733D4F120 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,319.500 | 0.161 | 4 | 0.929 | -1.888 | 52.455 |
| 5 | 672 | 3544ABE8-D8FF-4830-912E-D469999D403E | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,333.200 | 0.147 | 12 | 0.924 | -1.541 | 53.799 |
| 6 | 762 | F632B24E-7811-454D-84B8-9C71B87DE04C | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,314.300 | 0.150 | 6 | 0.852 | -1.884 | 52.462 |
| 7 | 823 | 728FA45A-EAA3-4CF2-95E7-BAE6BDA8483D | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,845.800 | 0.172 | 3 | 0.808 | -1.876 | 52.460 |
| 8 | 863 | 4FF6DB02-1084-41D1-8ECD-B12EDA10B879 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 9,021.900 | 0.210 | 1 | 0.787 | -1.788 | 52.477 |
| 9 | 934 | 89CE80E0-BE9E-4D1D-9EB7-7FC5B427FC3C | Unknown | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 5,492.900 | 0.708 | 9 | 0.751 | -1.627 | 53.791 |
| 10 | 1,094 | 3135435D-E5A1-4E25-B043-1F4937CCE9C7 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 5,301.900 | 0.254 | 2 | 0.694 | -1.481 | 53.368 |

## Road Archetype: rural_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2,072 | 1BCD5F92-C653-4616-8CBE-6F60EF75DBE3 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,322.500 | 1.973 | 3 | 0.533 | -1.103 | 53.571 |
| 2 | 3,544 | DE1D187E-F119-41BE-8B51-9F46C41C5F2F | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,089.100 | 1.352 | 1 | 0.441 | -1.419 | 53.733 |
| 3 | 3,748 | A840D400-FB6D-4004-8716-855F2C873B6A | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,704.600 | 2.716 | 0 | 0.432 | -1.370 | 53.896 |
| 4 | 4,331 | 9F346345-D2F0-4376-8473-95B716AE4401 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,499.200 | 2.616 | 1 | 0.411 | -0.500 | 53.115 |
| 5 | 5,101 | D7873FEF-2A30-49C1-B312-1A21E000D462 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,871.900 | 0.155 | 0 | 0.389 | -0.983 | 54.561 |
| 6 | 5,218 | F5D4C18C-2665-4CFC-9461-AF2CFEF16788 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,695.100 | 1.381 | 4 | 0.386 | 0.252 | 52.211 |
| 7 | 5,402 | 2872CFC3-62B9-4A66-BF89-50C68F697674 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,589.500 | 1.510 | 5 | 0.382 | -1.262 | 53.377 |
| 8 | 6,762 | 3F1CE439-4C3F-42A4-9B87-F8FB4910EA04 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,962.200 | 2.351 | 1 | 0.354 | -3.011 | 53.598 |
| 9 | 7,031 | 54933025-F7C4-424E-9982-F8AB1FB39678 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,950.200 | 1.334 | 0 | 0.349 | -1.097 | 52.756 |
| 10 | 7,427 | B8F57D1E-4785-4CD0-B970-CD1C17641364 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 4,590.200 | 0.958 | 1 | 0.342 | -0.472 | 53.819 |

## Road Archetype: other_unknown

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 113 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | A Road | other_unknown | other_unknown | Collapsed Dual Carriageway | 1 | 0 | 0 | 29,499.600 | 3.374 | 38 | 3.310 | -0.450 | 53.703 |
| 2 | 343 | C51DA9F7-73F7-4E79-B42E-EC481E872721 | A Road | A Road | other_unknown | other_unknown | Collapsed Dual Carriageway | 1 | 0 | 0 | 32,817.900 | 2.411 | 18 | 1.564 | -2.714 | 53.353 |
| 3 | 1,409 | 3ABAEE19-657F-4356-BC1E-8C1DBEFA65F3 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 13,515.900 | 2.774 | 3 | 0.618 | -3.005 | 53.400 |

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
