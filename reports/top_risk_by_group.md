# Top-Risk Links By Comparable Road Group

## Purpose

The global top-1% table is useful, but the very top of that ranking can be dominated by high-volume motorway links. These group-specific tables help inspect high-risk links among comparable road families, OS road classes, and conservative reporting archetypes.

## Summary

| group_type | groups | top_n_per_group | rows |
| --- | --- | --- | --- |
| family | 5 | 100 | 407 |
| road_classification | 7 | 100 | 700 |
| road_archetype | 9 | 100 | 807 |

Ranking field used: `risk_percentile`.

Created at: `2026-07-04T12:45:06+00:00`.

## Road-Type Schemes Used Here

- `family` is the official comparable-road-type modelling/diagnostic split: `motorway`, `trunk_a`, `other_urban`, `other_rural`, plus `other_unknown` as a fallback/reporting bucket when the family inputs do not resolve cleanly.
- `road_classification` is the broad OS Open Roads classification axis (`Motorway`, `A Road`, `B Road`, `Classified Unnumbered`, `Unclassified`, `Not Classified`, `Unknown`). It is useful for inspection but is not the same thing as the modelling family split.
- `road_function` is the OS functional category, retained as descriptive context because it is often more informative below trunk-road scale.
- `form_of_way` and derived flags (`is_dual`, `is_slip_road`, `is_roundabout`) describe physical form. They are important map/filter fields, but the repo's v1 family design explicitly did not adopt dual/single/roundabout/slip as separate families.
- `road_archetype` is a conservative reporting convenience that combines `family` with broad road class. It is not a model family and should not be read as a new production ranking surface.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores.parquet | 2026-07-04T12:18:58.712085+00:00 | 284,070,422 |
| data/processed/shapefiles/openroads.parquet | 2026-07-02T23:47:44.335016+00:00 | 853,847,157 |
| data/features/network_features.parquet | 2026-07-03T21:39:50.600900+00:00 | 275,258,014 |

Project/model output version: `0.1.0`.

## Count By Road Archetype

Each archetype table contains the top 100 links within that archetype, so the count table below shows output allocation rather than population prevalence. For prevalence, use the global top-1% `Count By Road Archetype` table.

| road_archetype | count | share |
| --- | --- | --- |
| motorway | 100 | 12.4% |
| rural_a_road | 100 | 12.4% |
| rural_b_road | 100 | 12.4% |
| rural_minor | 100 | 12.4% |
| trunk_a | 100 | 12.4% |
| urban_b_road | 100 | 12.4% |
| urban_a_road | 100 | 12.4% |
| urban_minor | 100 | 12.4% |
| other_unknown | 7 | 0.9% |

## Family: motorway

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 39,171.800 | 10.633 | 137 | 17.602 | -2.397 | 53.252 |
| 2 | 2 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,557.000 | 16.221 | 90 | 17.405 | -1.188 | 52.526 |
| 3 | 3 | C88EE264-D645-4EEB-B759-332F064347E4 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 45,836.700 | 8.959 | 69 | 17.056 | -2.209 | 52.935 |
| 4 | 4 | BBB307EC-410E-4741-B22C-9DE761845549 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,522.600 | 16.045 | 57 | 15.489 | -1.390 | 52.130 |
| 5 | 5 | CD5E5752-A199-46E0-A8E6-BF680BE4D1E3 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 49,892.400 | 4.846 | 85 | 14.472 | -2.028 | 52.612 |
| 6 | 6 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 61,859.400 | 7.765 | 104 | 14.002 | -2.752 | 53.289 |
| 7 | 7 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 33,596.500 | 11.595 | 110 | 13.733 | -1.333 | 52.427 |
| 8 | 8 | 16B613FC-2995-42B1-83E0-AC7F83065EEC | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 35,733.300 | 13.866 | 85 | 13.166 | -1.698 | 52.302 |
| 9 | 9 | 151C3468-CD42-4DC9-9DB4-0B03FE374503 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 61,454.500 | 6.820 | 59 | 13.094 | -2.687 | 53.664 |
| 10 | 10 | F454DAB1-296B-4FDB-8F67-2FA30FF33EBD | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 50,646.300 | 6.419 | 77 | 13.072 | -2.462 | 53.329 |

## Family: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 116 | E1AC0C71-21A6-4F45-ACAD-7A3C4E0EF99F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,596.900 | 9.050 | 29 | 4.840 | -1.102 | 52.395 |
| 2 | 125 | 5A06A2A0-3648-46B2-B91E-D5F8EA000B77 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,529.300 | 7.167 | 15 | 4.656 | -1.412 | 52.781 |
| 3 | 130 | 65BA14C9-05CF-4ED8-AB6E-F76B69344D16 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,878.600 | 6.488 | 35 | 4.558 | -1.648 | 52.816 |
| 4 | 140 | AF5910F7-72AB-4D30-99E8-3FAF54587147 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,990.600 | 6.750 | 24 | 4.374 | -1.913 | 52.138 |
| 5 | 142 | 980A4752-91AD-4B78-8D85-FC7BC10F4106 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,666.800 | 6.140 | 39 | 4.367 | -1.438 | 53.027 |
| 6 | 144 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 18,922.000 | 2.097 | 62 | 4.361 | -1.237 | 53.626 |
| 7 | 160 | 3A4AC0CF-7824-4005-8DD7-B56E117DB95E | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,052.000 | 6.433 | 19 | 4.094 | -1.298 | 54.497 |
| 8 | 165 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,940.300 | 7.408 | 40 | 3.939 | -0.975 | 52.403 |
| 9 | 167 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 10,739.500 | 6.793 | 43 | 3.931 | 0.354 | 52.247 |
| 10 | 186 | 7D0B0A92-F0E3-4E6C-B54F-9B07CB98C51D | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,679.200 | 5.857 | 24 | 3.587 | 0.264 | 52.215 |

## Family: other_urban

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 233 | D4BB3DD4-0E97-4836-A859-49562A809C14 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 23,341.000 | 3.178 | 15 | 2.932 | -1.402 | 53.221 |
| 2 | 306 | 0AFF5EE0-3267-43D0-9EC5-CA6119303BE6 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,945.700 | 3.048 | 23 | 2.293 | -3.026 | 53.793 |
| 3 | 310 | 8052BE32-C298-4EBE-9DDB-BFA080ED1AE0 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,336.200 | 3.731 | 18 | 2.250 | -1.893 | 52.389 |
| 4 | 344 | 9B7133A4-1631-43EE-8CC6-6A33EC90CE9D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 12,903.500 | 3.847 | 22 | 2.108 | -1.924 | 53.889 |
| 5 | 365 | A0EF54FA-237C-4490-A04A-68A179CA4F6F | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,058.000 | 1.906 | 6 | 2.018 | -3.001 | 53.370 |
| 6 | 368 | 0C94874C-B9CE-42E2-B3D5-DFF1BD0E6358 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,700.200 | 5.522 | 24 | 2.004 | -1.472 | 53.291 |
| 7 | 378 | C599344D-4260-4D18-85E4-E5DEB1702789 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 23,901.200 | 2.317 | 12 | 1.954 | -1.374 | 53.351 |
| 8 | 385 | 6A3D2D1E-D14A-4D89-B29D-1D4D615A5080 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 25,685.100 | 2.639 | 2 | 1.927 | -3.006 | 53.414 |
| 9 | 398 | F097AA80-1A73-4DF5-8004-3AE2AE8CC16D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,414.300 | 3.609 | 17 | 1.882 | -2.463 | 53.065 |
| 10 | 405 | A7516B09-B4F0-4906-947F-2ED4B3CF0821 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 8,876.900 | 4.445 | 18 | 1.870 | -0.450 | 53.657 |

## Family: other_rural

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 284 | 59FFE4B6-01EB-478C-A8DE-17370D48427D | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,200.800 | 6.596 | 11 | 2.444 | -0.126 | 52.716 |
| 2 | 304 | E56501E8-3ACB-46DD-B6B1-397BF24F3499 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 15,008.100 | 4.878 | 16 | 2.298 | -1.052 | 52.239 |
| 3 | 308 | 89D775E5-B175-45FA-9009-D353F84D302F | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 10,842.000 | 5.057 | 8 | 2.267 | -1.945 | 53.334 |
| 4 | 312 | 7E90F309-C9E6-4DF8-B923-884C83F21BA8 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 7,935.800 | 5.875 | 7 | 2.236 | -0.703 | 52.461 |
| 5 | 390 | 8620C2C5-CC9B-465D-BEE2-A8C0131E7D12 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 14,590.800 | 3.807 | 11 | 1.904 | -2.422 | 53.822 |
| 6 | 425 | D45E8FA7-81BC-44A3-A28C-A9B7E9E179CB | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 13,495.900 | 2.950 | 3 | 1.816 | -1.215 | 54.118 |
| 7 | 458 | 4F7AA121-68AC-4F36-A483-DB2CC1A64202 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 8,509.300 | 4.065 | 22 | 1.681 | -0.208 | 52.621 |
| 8 | 476 | C3E9EA94-5905-4E01-AA00-7C0FEE6B2FCA | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 18,835.500 | 2.391 | 0 | 1.620 | -0.694 | 52.113 |
| 9 | 487 | A8C191DC-224B-41B3-B35B-B64BACF8EFA7 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 16,932.800 | 3.468 | 12 | 1.598 | -1.425 | 54.140 |
| 10 | 507 | F044802C-D97E-4681-B63D-9E424120BF63 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 10,842.100 | 3.456 | 4 | 1.552 | 1.168 | 52.377 |

## Road Classification: A Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 116 | E1AC0C71-21A6-4F45-ACAD-7A3C4E0EF99F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,596.900 | 9.050 | 29 | 4.840 | -1.102 | 52.395 |
| 2 | 125 | 5A06A2A0-3648-46B2-B91E-D5F8EA000B77 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,529.300 | 7.167 | 15 | 4.656 | -1.412 | 52.781 |
| 3 | 130 | 65BA14C9-05CF-4ED8-AB6E-F76B69344D16 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,878.600 | 6.488 | 35 | 4.558 | -1.648 | 52.816 |
| 4 | 140 | AF5910F7-72AB-4D30-99E8-3FAF54587147 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,990.600 | 6.750 | 24 | 4.374 | -1.913 | 52.138 |
| 5 | 142 | 980A4752-91AD-4B78-8D85-FC7BC10F4106 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,666.800 | 6.140 | 39 | 4.367 | -1.438 | 53.027 |
| 6 | 144 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 18,922.000 | 2.097 | 62 | 4.361 | -1.237 | 53.626 |
| 7 | 160 | 3A4AC0CF-7824-4005-8DD7-B56E117DB95E | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,052.000 | 6.433 | 19 | 4.094 | -1.298 | 54.497 |
| 8 | 165 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,940.300 | 7.408 | 40 | 3.939 | -0.975 | 52.403 |
| 9 | 167 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 10,739.500 | 6.793 | 43 | 3.931 | 0.354 | 52.247 |
| 10 | 186 | 7D0B0A92-F0E3-4E6C-B54F-9B07CB98C51D | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,679.200 | 5.857 | 24 | 3.587 | 0.264 | 52.215 |

## Road Classification: B Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 526 | 08FD9A0B-E2ED-42CA-BBA7-A64A5A92C4EC | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,710.700 | 1.942 | 3 | 1.494 | -1.427 | 53.431 |
| 2 | 833 | 903A6F71-6F14-4C5A-9C21-4FC7FE00BEF3 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 12,769.700 | 0.983 | 3 | 1.103 | -2.715 | 53.332 |
| 3 | 1,020 | C784F8EB-237F-4372-A437-594EEB8C2426 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 8,982.900 | 2.108 | 18 | 0.983 | -1.596 | 53.661 |
| 4 | 1,158 | 346B75A1-6B87-4E5B-999E-75DAD35E68A6 | B Road | B Road | other_urban | urban_b_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,215.600 | 0.785 | 4 | 0.911 | -1.978 | 52.449 |
| 5 | 1,207 | FC2665C5-0AD2-4683-9A2F-CA9B985B9951 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 11,219.900 | 1.822 | 4 | 0.894 | -1.452 | 52.980 |
| 6 | 1,298 | F10D4083-55D5-4094-94CB-CACA05C2D7DF | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 10,937.100 | 1.626 | 12 | 0.864 | -1.356 | 53.596 |
| 7 | 1,353 | C10AB286-2FC8-446B-B9B9-3CF56FD88CD2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,857.900 | 0.267 | 4 | 0.847 | -1.852 | 52.488 |
| 8 | 1,358 | 7350A90C-A59A-4E33-9CB6-2C8DC36278FD | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,812.100 | 2.547 | 3 | 0.844 | -0.294 | 53.598 |
| 9 | 1,448 | 13D3D399-A12C-4CDD-8D44-A0F24E325EF3 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 6,137.700 | 2.750 | 2 | 0.820 | -1.642 | 53.308 |
| 10 | 1,449 | B8BC385E-1068-4734-8AF8-FD237F3FC9A5 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 13,970.000 | 0.269 | 5 | 0.819 | -3.009 | 53.375 |

## Road Classification: Unclassified

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,567 | 5D5599EF-026D-4A0C-AC67-F13AE5618484 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,115.100 | 0.151 | 8 | 0.793 | -1.510 | 52.410 |
| 2 | 1,938 | 4E1A24B2-0704-42C0-87F5-D66FAFB4BD10 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,868.500 | 0.133 | 8 | 0.733 | -1.511 | 52.411 |
| 3 | 2,422 | D670CA17-1A5E-4CBB-8BFA-4DC6D0A7D3C2 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,859.000 | 0.130 | 0 | 0.681 | -1.514 | 52.411 |
| 4 | 2,597 | DDADCCB5-282A-4B56-B151-6B73B3865A1C | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,303.500 | 0.091 | 0 | 0.666 | -1.512 | 52.412 |
| 5 | 3,195 | FDFAE69E-289B-43A9-B405-A09A618DA7AF | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,003.200 | 0.108 | 4 | 0.618 | -1.511 | 52.412 |
| 6 | 3,403 | 271B6958-2000-44D6-AA5F-FD6DEF9566F2 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,083.000 | 0.144 | 12 | 0.606 | -1.538 | 53.797 |
| 7 | 4,086 | 6534C4C5-3483-44D6-BCD8-3BADC7E9CC60 | Unclassified | Local Road | other_urban | urban_minor | Collapsed Dual Carriageway | 1 | 0 | 0 | 1,727.200 | 0.112 | 9 | 0.570 | -1.545 | 53.800 |
| 8 | 4,435 | CAB2B179-F04C-48F4-89E6-57CBF162ABE4 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,415.900 | 0.178 | 2 | 0.554 | -1.136 | 52.623 |
| 9 | 4,620 | E67DF9F4-E91F-4586-B7F2-67D7EE48806D | Unclassified | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 4,114.400 | 1.093 | 0 | 0.547 | -1.264 | 53.388 |
| 10 | 4,966 | 938D74FF-5A33-4943-A80B-77563E52F32F | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,507.700 | 0.131 | 9 | 0.533 | -1.545 | 53.799 |

## Road Archetype: motorway

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 39,171.800 | 10.633 | 137 | 17.602 | -2.397 | 53.252 |
| 2 | 2 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,557.000 | 16.221 | 90 | 17.405 | -1.188 | 52.526 |
| 3 | 3 | C88EE264-D645-4EEB-B759-332F064347E4 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 45,836.700 | 8.959 | 69 | 17.056 | -2.209 | 52.935 |
| 4 | 4 | BBB307EC-410E-4741-B22C-9DE761845549 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 31,522.600 | 16.045 | 57 | 15.489 | -1.390 | 52.130 |
| 5 | 5 | CD5E5752-A199-46E0-A8E6-BF680BE4D1E3 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 49,892.400 | 4.846 | 85 | 14.472 | -2.028 | 52.612 |
| 6 | 6 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 61,859.400 | 7.765 | 104 | 14.002 | -2.752 | 53.289 |
| 7 | 7 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 33,596.500 | 11.595 | 110 | 13.733 | -1.333 | 52.427 |
| 8 | 8 | 16B613FC-2995-42B1-83E0-AC7F83065EEC | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 35,733.300 | 13.866 | 85 | 13.166 | -1.698 | 52.302 |
| 9 | 9 | 151C3468-CD42-4DC9-9DB4-0B03FE374503 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 61,454.500 | 6.820 | 59 | 13.094 | -2.687 | 53.664 |
| 10 | 10 | F454DAB1-296B-4FDB-8F67-2FA30FF33EBD | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 50,646.300 | 6.419 | 77 | 13.072 | -2.462 | 53.329 |

## Road Archetype: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 116 | E1AC0C71-21A6-4F45-ACAD-7A3C4E0EF99F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,596.900 | 9.050 | 29 | 4.840 | -1.102 | 52.395 |
| 2 | 125 | 5A06A2A0-3648-46B2-B91E-D5F8EA000B77 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,529.300 | 7.167 | 15 | 4.656 | -1.412 | 52.781 |
| 3 | 130 | 65BA14C9-05CF-4ED8-AB6E-F76B69344D16 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,878.600 | 6.488 | 35 | 4.558 | -1.648 | 52.816 |
| 4 | 140 | AF5910F7-72AB-4D30-99E8-3FAF54587147 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,990.600 | 6.750 | 24 | 4.374 | -1.913 | 52.138 |
| 5 | 142 | 980A4752-91AD-4B78-8D85-FC7BC10F4106 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,666.800 | 6.140 | 39 | 4.367 | -1.438 | 53.027 |
| 6 | 144 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 18,922.000 | 2.097 | 62 | 4.361 | -1.237 | 53.626 |
| 7 | 160 | 3A4AC0CF-7824-4005-8DD7-B56E117DB95E | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,052.000 | 6.433 | 19 | 4.094 | -1.298 | 54.497 |
| 8 | 165 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,940.300 | 7.408 | 40 | 3.939 | -0.975 | 52.403 |
| 9 | 167 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 10,739.500 | 6.793 | 43 | 3.931 | 0.354 | 52.247 |
| 10 | 186 | 7D0B0A92-F0E3-4E6C-B54F-9B07CB98C51D | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 9,679.200 | 5.857 | 24 | 3.587 | 0.264 | 52.215 |

## Road Archetype: urban_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 233 | D4BB3DD4-0E97-4836-A859-49562A809C14 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 23,341.000 | 3.178 | 15 | 2.932 | -1.402 | 53.221 |
| 2 | 310 | 8052BE32-C298-4EBE-9DDB-BFA080ED1AE0 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,336.200 | 3.731 | 18 | 2.250 | -1.893 | 52.389 |
| 3 | 344 | 9B7133A4-1631-43EE-8CC6-6A33EC90CE9D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 12,903.500 | 3.847 | 22 | 2.108 | -1.924 | 53.889 |
| 4 | 365 | A0EF54FA-237C-4490-A04A-68A179CA4F6F | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,058.000 | 1.906 | 6 | 2.018 | -3.001 | 53.370 |
| 5 | 368 | 0C94874C-B9CE-42E2-B3D5-DFF1BD0E6358 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,700.200 | 5.522 | 24 | 2.004 | -1.472 | 53.291 |
| 6 | 378 | C599344D-4260-4D18-85E4-E5DEB1702789 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 23,901.200 | 2.317 | 12 | 1.954 | -1.374 | 53.351 |
| 7 | 385 | 6A3D2D1E-D14A-4D89-B29D-1D4D615A5080 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 25,685.100 | 2.639 | 2 | 1.927 | -3.006 | 53.414 |
| 8 | 398 | F097AA80-1A73-4DF5-8004-3AE2AE8CC16D | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 14,414.300 | 3.609 | 17 | 1.882 | -2.463 | 53.065 |
| 9 | 405 | A7516B09-B4F0-4906-947F-2ED4B3CF0821 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 8,876.900 | 4.445 | 18 | 1.870 | -0.450 | 53.657 |
| 10 | 422 | F97064ED-C237-4D44-BAF3-9F3175BB3508 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 17,701.600 | 2.964 | 12 | 1.819 | -0.836 | 52.435 |

## Road Archetype: rural_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 284 | 59FFE4B6-01EB-478C-A8DE-17370D48427D | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 7,200.800 | 6.596 | 11 | 2.444 | -0.126 | 52.716 |
| 2 | 304 | E56501E8-3ACB-46DD-B6B1-397BF24F3499 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 15,008.100 | 4.878 | 16 | 2.298 | -1.052 | 52.239 |
| 3 | 308 | 89D775E5-B175-45FA-9009-D353F84D302F | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 10,842.000 | 5.057 | 8 | 2.267 | -1.945 | 53.334 |
| 4 | 312 | 7E90F309-C9E6-4DF8-B923-884C83F21BA8 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 7,935.800 | 5.875 | 7 | 2.236 | -0.703 | 52.461 |
| 5 | 390 | 8620C2C5-CC9B-465D-BEE2-A8C0131E7D12 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 14,590.800 | 3.807 | 11 | 1.904 | -2.422 | 53.822 |
| 6 | 425 | D45E8FA7-81BC-44A3-A28C-A9B7E9E179CB | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 13,495.900 | 2.950 | 3 | 1.816 | -1.215 | 54.118 |
| 7 | 458 | 4F7AA121-68AC-4F36-A483-DB2CC1A64202 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 8,509.300 | 4.065 | 22 | 1.681 | -0.208 | 52.621 |
| 8 | 476 | C3E9EA94-5905-4E01-AA00-7C0FEE6B2FCA | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 18,835.500 | 2.391 | 0 | 1.620 | -0.694 | 52.113 |
| 9 | 487 | A8C191DC-224B-41B3-B35B-B64BACF8EFA7 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 16,932.800 | 3.468 | 12 | 1.598 | -1.425 | 54.140 |
| 10 | 507 | F044802C-D97E-4681-B63D-9E424120BF63 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 10,842.100 | 3.456 | 4 | 1.552 | 1.168 | 52.377 |

## Road Archetype: urban_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 526 | 08FD9A0B-E2ED-42CA-BBA7-A64A5A92C4EC | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,710.700 | 1.942 | 3 | 1.494 | -1.427 | 53.431 |
| 2 | 833 | 903A6F71-6F14-4C5A-9C21-4FC7FE00BEF3 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 12,769.700 | 0.983 | 3 | 1.103 | -2.715 | 53.332 |
| 3 | 1,020 | C784F8EB-237F-4372-A437-594EEB8C2426 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 8,982.900 | 2.108 | 18 | 0.983 | -1.596 | 53.661 |
| 4 | 1,158 | 346B75A1-6B87-4E5B-999E-75DAD35E68A6 | B Road | B Road | other_urban | urban_b_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,215.600 | 0.785 | 4 | 0.911 | -1.978 | 52.449 |
| 5 | 1,353 | C10AB286-2FC8-446B-B9B9-3CF56FD88CD2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,857.900 | 0.267 | 4 | 0.847 | -1.852 | 52.488 |
| 6 | 1,449 | B8BC385E-1068-4734-8AF8-FD237F3FC9A5 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 13,970.000 | 0.269 | 5 | 0.819 | -3.009 | 53.375 |
| 7 | 1,458 | EBFD11B4-E4E9-4A4A-8C81-91C6E5FAC5D3 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 21,348.700 | 0.177 | 3 | 0.818 | -2.717 | 53.754 |
| 8 | 1,512 | 686018EB-5425-4D7B-A7D4-A759D1922DDB | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 11,443.600 | 1.625 | 0 | 0.806 | -2.738 | 53.772 |
| 9 | 1,580 | 17375E51-36BB-4F43-B98A-F998174BFA12 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 5,440.000 | 0.110 | 17 | 0.791 | -2.226 | 53.457 |
| 10 | 1,722 | 5F91ABF6-7218-47AC-8A74-DB47F2E43BC9 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 14,425.600 | 1.499 | 1 | 0.768 | -1.354 | 54.832 |

## Road Archetype: rural_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,207 | FC2665C5-0AD2-4683-9A2F-CA9B985B9951 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 11,219.900 | 1.822 | 4 | 0.894 | -1.452 | 52.980 |
| 2 | 1,298 | F10D4083-55D5-4094-94CB-CACA05C2D7DF | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 10,937.100 | 1.626 | 12 | 0.864 | -1.356 | 53.596 |
| 3 | 1,358 | 7350A90C-A59A-4E33-9CB6-2C8DC36278FD | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,812.100 | 2.547 | 3 | 0.844 | -0.294 | 53.598 |
| 4 | 1,448 | 13D3D399-A12C-4CDD-8D44-A0F24E325EF3 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 6,137.700 | 2.750 | 2 | 0.820 | -1.642 | 53.308 |
| 5 | 2,005 | 2554C670-2549-4A03-BDD9-BAEEA68CC19B | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 5,574.900 | 2.844 | 2 | 0.725 | 0.045 | 52.046 |
| 6 | 2,162 | A3A1FDD9-0B7A-4279-8803-79EF7817031F | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 3,156.000 | 3.565 | 2 | 0.706 | 0.063 | 52.366 |
| 7 | 2,371 | 20AB2E37-034B-4B3D-BC28-EECB1559AAE6 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 3,961.500 | 3.823 | 6 | 0.686 | -0.323 | 52.851 |
| 8 | 2,551 | 3C6D6D98-6B54-4770-9B71-5D7089B0B9FB | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 5,147.600 | 3.021 | 9 | 0.670 | -0.454 | 54.122 |
| 9 | 2,589 | 531F3B6B-1918-4F51-9A82-E2424951C767 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 6,988.900 | 1.617 | 1 | 0.668 | -1.345 | 52.432 |
| 10 | 2,798 | EA7F0705-5592-41E6-A409-A82AE504823B | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 7,120.700 | 2.537 | 7 | 0.649 | -1.113 | 53.852 |

## Road Archetype: urban_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 306 | 0AFF5EE0-3267-43D0-9EC5-CA6119303BE6 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,945.700 | 3.048 | 23 | 2.293 | -3.026 | 53.793 |
| 2 | 953 | D07D145D-DA08-46CC-B1BB-B0687BCE2F08 | Classified Unnumbered | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 982.600 | 0.113 | 0 | 1.019 | -1.468 | 53.375 |
| 3 | 961 | EAF1B83D-85E9-4640-B71B-197430F13013 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,264.000 | 0.147 | 6 | 1.015 | -1.503 | 52.407 |
| 4 | 1,098 | 7F0067FA-4223-4859-BE59-4828D208010D | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,327.100 | 1.530 | 9 | 0.942 | -1.427 | 53.434 |
| 5 | 1,141 | A8CCA6AC-F78F-49DC-853E-375412122097 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,371.300 | 0.151 | 1 | 0.919 | -2.243 | 53.476 |
| 6 | 1,208 | FB0EF761-2FA3-486A-9B60-226D92C96C15 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,073.500 | 0.195 | 4 | 0.893 | -1.156 | 52.627 |
| 7 | 1,238 | 86C51704-C549-48B0-8137-7A7220A0FBE8 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,326.500 | 0.168 | 4 | 0.882 | -2.705 | 53.762 |
| 8 | 1,243 | 3A5A31FD-45A6-44F1-B4A7-8AE293CE3B7B | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,501.000 | 0.270 | 13 | 0.881 | -1.828 | 52.470 |
| 9 | 1,321 | FCDCDED9-785C-46B3-84D2-898F5598AEA5 | Classified Unnumbered | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,566.600 | 0.095 | 1 | 0.857 | -1.480 | 53.390 |
| 10 | 1,401 | 4565C592-BF41-4AA1-B81D-91BA338DEDDE | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,854.600 | 0.404 | 0 | 0.832 | -1.626 | 54.982 |

## Road Archetype: rural_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2,081 | A840D400-FB6D-4004-8716-855F2C873B6A | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,950.300 | 2.716 | 0 | 0.717 | -1.370 | 53.896 |
| 2 | 2,193 | 16E51577-B697-43EE-AFDF-1FA670370425 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,015.000 | 3.227 | 4 | 0.703 | -0.771 | 52.706 |
| 3 | 3,933 | E261BCBD-8D2B-4238-AE08-F358ED79FC4E | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,722.500 | 0.796 | 1 | 0.577 | -1.420 | 53.672 |
| 4 | 4,620 | E67DF9F4-E91F-4586-B7F2-67D7EE48806D | Unclassified | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 4,114.400 | 1.093 | 0 | 0.547 | -1.264 | 53.388 |
| 5 | 4,797 | D21C78BB-43E4-4A55-89CE-B2A80D7D0B65 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,838.600 | 1.230 | 2 | 0.539 | -1.720 | 54.830 |
| 6 | 5,217 | C14B8C32-E135-4D81-B317-D29B96B628CC | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,516.600 | 0.710 | 1 | 0.525 | -1.242 | 53.279 |
| 7 | 5,309 | 1BCD5F92-C653-4616-8CBE-6F60EF75DBE3 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,513.000 | 1.973 | 3 | 0.522 | -1.103 | 53.571 |
| 8 | 5,350 | 66DAE859-1882-4D29-A38B-D1B242D827B6 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,918.900 | 1.743 | 2 | 0.520 | -1.405 | 53.759 |
| 9 | 5,564 | 629CFABF-2ADB-4E2A-87CF-B609A44125F8 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,899.400 | 0.189 | 0 | 0.514 | -1.357 | 53.747 |
| 10 | 6,072 | 96D41AD4-5A39-4883-8E14-9AB7D7F9361C | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,584.600 | 2.111 | 2 | 0.499 | -1.349 | 52.400 |

## Road Archetype: other_unknown

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_xgb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 257 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | A Road | other_unknown | other_unknown | Collapsed Dual Carriageway | 1 | 0 | 0 | 10,811.600 | 3.374 | 38 | 2.659 | -0.450 | 53.703 |
| 2 | 1,118 | C51DA9F7-73F7-4E79-B42E-EC481E872721 | A Road | A Road | other_unknown | other_unknown | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,058.600 | 2.411 | 18 | 0.930 | -2.714 | 53.353 |
| 3 | 63,271 | 3ABAEE19-657F-4356-BC1E-8C1DBEFA65F3 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 15,966.100 | 2.774 | 3 | 0.189 | -3.005 | 53.400 |
| 4 | 793,140 | D0ED5E45-1727-4FDB-B864-47B42571BE7D | Classified Unnumbered | Minor Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 1,010.800 | 5.189 | 0 | 0.013 | -5.320 | 58.057 |
| 5 | 1,911,073 | 1F6B2F40-EB73-4319-8B20-B6A84CC06929 | Classified Unnumbered | Minor Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 278.000 | 3.267 | 0 | 0.002 | -7.442 | 57.023 |
| 6 | 2,343,910 | C3DC224D-8786-425D-BB99-94542BBAFB26 | Not Classified | Local Access Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 607.400 | 0.635 | 0 | 0.001 | -1.161 | 50.736 |
| 7 | 3,288,251 | D807EEF4-29A7-405E-8656-9B8EEDA9CE7B | Unknown | Restricted Local Access Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 300.500 | 0.873 | 0 | 0.000 | -5.062 | 51.704 |

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
