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

Created at: `2026-10-06T22:15:46+00:00`.

## Road-Type Schemes Used Here

- `family` is the official comparable-road-type modelling/diagnostic split: `motorway`, `trunk_a`, `other_urban`, `other_rural`, plus `other_unknown` as a fallback/reporting bucket when the family inputs do not resolve cleanly.
- `road_classification` is the broad OS Open Roads classification axis (`Motorway`, `A Road`, `B Road`, `Classified Unnumbered`, `Unclassified`, `Not Classified`, `Unknown`). It is useful for inspection but is not the same thing as the modelling family split.
- `road_function` is the OS functional category, retained as descriptive context because it is often more informative below trunk-road scale.
- `form_of_way` and derived flags (`is_dual`, `is_slip_road`, `is_roundabout`) describe physical form. They are important map/filter fields, but the repo's v1 family design explicitly did not adopt dual/single/roundabout/slip as separate families.
- `road_archetype` is a conservative reporting convenience that combines `family` with broad road class. It is not a model family and should not be read as a new production ranking surface.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores_eb.parquet | 2026-10-06T22:12:16.028189+00:00 | 385,058,544 |
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

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | DB762ED8-493D-4273-89AA-1E793BEA822C | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 56,389.300 | 15.627 | 74 | 7.421 | 26.721 | 99.998 | -3.430 | 50.798 |
| 2 | 2 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 45,717.100 | 16.221 | 90 | 9.018 | 23.396 | 99.999 | -1.188 | 52.526 |
| 3 | 3 | 62A5F5FF-7806-45F6-8E1A-A01332356323 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 38,654.900 | 19.085 | 143 | 14.311 | 23.133 | 100.000 | -1.986 | 51.537 |
| 4 | 4 | FF70F2F4-ABFF-4211-BCBF-D45425648018 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 38,451.400 | 16.291 | 209 | 20.899 | 20.087 | 100.000 | 0.774 | 51.304 |
| 5 | 5 | 7E604C90-3F9B-43EA-ADE1-416FFDB2D167 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 38,479.900 | 17.578 | 84 | 8.416 | 19.251 | 99.998 | -1.184 | 51.460 |
| 6 | 6 | AF0F5809-67DC-43D2-848E-E1A2E08E2628 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 37,156.700 | 17.230 | 97 | 9.714 | 18.358 | 99.999 | -1.124 | 51.814 |
| 7 | 7 | 12229866-3F77-4DB3-9034-1029042770E5 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 54,574.400 | 9.905 | 258 | 25.788 | 18.345 | 100.000 | -0.262 | 51.277 |
| 8 | 8 | 22B9F354-B2AA-4300-811B-A0DCDCFA2A7D | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 40,768.500 | 15.283 | 72 | 7.218 | 18.340 | 99.998 | -1.270 | 52.002 |
| 9 | 9 | D9CF0BEC-6749-44F5-8688-7F3D432DF36A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 77,077.900 | 6.192 | 53 | 5.320 | 18.082 | 99.995 | -0.341 | 51.492 |
| 10 | 10 | 0E4A9C14-C13E-4F70-9A16-6306AE5D3296 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 52,991.600 | 10.689 | 46 | 4.622 | 17.954 | 99.992 | -1.595 | 52.646 |

## Family: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 102 | 7ABDD823-7CBD-4802-A732-33559BA80616 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,698.800 | 12.647 | 103 | 10.298 | 9.537 | 99.999 | -0.878 | 50.851 |
| 2 | 143 | F661CF64-7E58-4AA7-A42B-3054B4306A68 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 19,245.900 | 6.328 | 76 | 7.602 | 8.226 | 99.998 | 0.302 | 51.631 |
| 3 | 153 | 747C8806-A6D6-465B-871C-845C059C3080 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 19,508.000 | 8.694 | 32 | 3.217 | 7.941 | 99.982 | -3.788 | 50.723 |
| 4 | 166 | 223F6B05-29DF-4A08-8C8C-B8DA44DD9298 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,055.300 | 8.696 | 54 | 5.408 | 7.556 | 99.995 | -5.078 | 50.321 |
| 5 | 174 | 62EFFFFE-0DE2-438F-8F83-D1D1A71B35EA | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,071.000 | 8.264 | 32 | 3.216 | 7.366 | 99.982 | -3.901 | 50.735 |
| 6 | 201 | 59AD968E-0D5A-4432-A9E8-4B8C84451F84 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,543.900 | 7.991 | 31 | 3.116 | 6.876 | 99.981 | -4.873 | 50.414 |
| 7 | 208 | 5A1BBEEE-9B67-4AA3-9520-97FC0B311A96 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,441.400 | 5.071 | 80 | 7.994 | 6.711 | 99.998 | -0.331 | 51.357 |
| 8 | 230 | 45B942B0-9125-44B4-B7FD-69A011E03E72 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,474.100 | 3.499 | 127 | 12.671 | 6.386 | 100.000 | 0.208 | 51.430 |
| 9 | 268 | 91026D33-C723-403D-B651-1BF6C9E75E70 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,873.300 | 5.346 | 35 | 3.512 | 5.875 | 99.985 | -1.315 | 51.643 |
| 10 | 278 | 8F227E78-6E1C-4C80-9B84-32774702BBF4 | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 19,720.400 | 5.200 | 42 | 4.208 | 5.700 | 99.990 | -5.366 | 50.207 |

## Family: other_urban

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 108 | 51991592-6273-4FA0-B34A-CEACF052E777 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,885.800 | 2.935 | 105 | 10.496 | 9.350 | 99.999 | -0.001 | 51.560 |
| 2 | 165 | 595E8891-9205-445B-9296-702A22E823DA | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,267.800 | 2.098 | 47 | 4.711 | 7.609 | 99.993 | -0.203 | 51.519 |
| 3 | 193 | C39C13F4-205A-4BB8-9115-A60E97910F01 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 19,786.500 | 2.291 | 50 | 5.008 | 7.000 | 99.994 | -0.441 | 51.885 |
| 4 | 255 | A437DF2C-5344-4058-866D-6ECF773A608B | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,352.000 | 1.827 | 70 | 6.995 | 6.050 | 99.997 | 0.055 | 51.565 |
| 5 | 265 | E7D07249-6666-492E-88E1-984FC87A5A59 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 28,962.100 | 1.511 | 103 | 10.279 | 5.927 | 99.999 | 0.068 | 51.546 |
| 6 | 272 | FA4E48A8-3348-48DF-AC18-E81DD06AF88B | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 17,802.600 | 0.223 | 99 | 9.880 | 5.806 | 99.999 | -0.072 | 51.585 |
| 7 | 287 | B980D095-8D75-4365-AC28-5BCF3DF67D11 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 27,872.100 | 0.276 | 39 | 3.909 | 5.535 | 99.989 | -0.127 | 51.488 |
| 8 | 299 | ECAF9F1D-E364-4F3A-A7B6-2C744018D604 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 22,906.000 | 0.309 | 45 | 4.505 | 5.354 | 99.992 | -0.073 | 51.581 |
| 9 | 306 | 6A3D2D1E-D14A-4D89-B29D-1D4D615A5080 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 27,027.900 | 2.639 | 1 | 0.128 | 5.302 | 95.079 | -3.006 | 53.414 |
| 10 | 319 | 5EA99404-841D-411E-A631-90ED7E42A8F8 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 37,957.700 | 0.755 | 51 | 5.100 | 5.099 | 99.994 | -0.328 | 51.534 |

## Family: other_rural

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 305 | A0E6AE20-B4AA-4A3D-9329-8C7611351750 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,466.200 | 8.188 | 61 | 6.096 | 5.304 | 99.996 | 0.535 | 51.664 |
| 2 | 378 | FD31F6C4-0EC6-4397-8327-E47E46D1E5A2 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,105.100 | 4.544 | 26 | 2.612 | 4.544 | 99.971 | -1.814 | 50.805 |
| 3 | 435 | 656DFDF8-8BCC-4E61-AB70-DA334530A1F5 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 30,496.400 | 2.868 | 8 | 0.823 | 4.126 | 99.674 | -4.841 | 50.522 |
| 4 | 482 | 98B74305-10C3-4D73-835F-9287DF8C2B6C | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 12,134.300 | 6.699 | 21 | 2.113 | 3.812 | 99.953 | -0.012 | 51.856 |
| 5 | 621 | 89D775E5-B175-45FA-9009-D353F84D302F | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,900.900 | 5.057 | 8 | 0.822 | 3.267 | 99.674 | -1.945 | 53.334 |
| 6 | 710 | A7A0B915-AA50-4E9F-8B2D-3F443DBC28E8 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,751.600 | 1.863 | 12 | 1.217 | 2.999 | 99.851 | -3.546 | 50.628 |
| 7 | 717 | F0910578-5FAE-4F8B-8B62-020287B3621B | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 16,724.600 | 4.495 | 39 | 3.891 | 2.981 | 99.988 | 1.115 | 51.842 |
| 8 | 737 | 7DF328A5-D6CB-4615-984B-EC0FFDCCB8C9 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 12,811.100 | 4.714 | 15 | 1.514 | 2.941 | 99.905 | -0.716 | 51.951 |
| 9 | 775 | 9F068480-CE0B-4CCA-AA7C-DB455776A7FF | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 25,809.400 | 2.435 | 17 | 1.712 | 2.854 | 99.927 | -1.540 | 55.160 |
| 10 | 787 | C521DAB5-C86C-4810-A60B-A28974331DB1 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 24,656.100 | 1.890 | 8 | 0.821 | 2.828 | 99.674 | -3.492 | 50.682 |

## Road Classification: A Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 102 | 7ABDD823-7CBD-4802-A732-33559BA80616 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,698.800 | 12.647 | 103 | 10.298 | 9.537 | 99.999 | -0.878 | 50.851 |
| 2 | 108 | 51991592-6273-4FA0-B34A-CEACF052E777 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,885.800 | 2.935 | 105 | 10.496 | 9.350 | 99.999 | -0.001 | 51.560 |
| 3 | 143 | F661CF64-7E58-4AA7-A42B-3054B4306A68 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 19,245.900 | 6.328 | 76 | 7.602 | 8.226 | 99.998 | 0.302 | 51.631 |
| 4 | 153 | 747C8806-A6D6-465B-871C-845C059C3080 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 19,508.000 | 8.694 | 32 | 3.217 | 7.941 | 99.982 | -3.788 | 50.723 |
| 5 | 165 | 595E8891-9205-445B-9296-702A22E823DA | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,267.800 | 2.098 | 47 | 4.711 | 7.609 | 99.993 | -0.203 | 51.519 |
| 6 | 166 | 223F6B05-29DF-4A08-8C8C-B8DA44DD9298 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,055.300 | 8.696 | 54 | 5.408 | 7.556 | 99.995 | -5.078 | 50.321 |
| 7 | 174 | 62EFFFFE-0DE2-438F-8F83-D1D1A71B35EA | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,071.000 | 8.264 | 32 | 3.216 | 7.366 | 99.982 | -3.901 | 50.735 |
| 8 | 193 | C39C13F4-205A-4BB8-9115-A60E97910F01 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 19,786.500 | 2.291 | 50 | 5.008 | 7.000 | 99.994 | -0.441 | 51.885 |
| 9 | 201 | 59AD968E-0D5A-4432-A9E8-4B8C84451F84 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,543.900 | 7.991 | 31 | 3.116 | 6.876 | 99.981 | -4.873 | 50.414 |
| 10 | 208 | 5A1BBEEE-9B67-4AA3-9520-97FC0B311A96 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,441.400 | 5.071 | 80 | 7.994 | 6.711 | 99.998 | -0.331 | 51.357 |

## Road Classification: B Road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,891 | C10AB286-2FC8-446B-B9B9-3CF56FD88CD2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 11,308.800 | 0.267 | 4 | 0.422 | 1.817 | 98.927 | -1.852 | 52.488 |
| 2 | 1,971 | 08FD9A0B-E2ED-42CA-BBA7-A64A5A92C4EC | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 13,362.200 | 1.942 | 3 | 0.324 | 1.777 | 98.388 | -1.427 | 53.431 |
| 3 | 2,744 | C5DD3055-F618-410F-AD85-FEE4DB8B2549 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,640.400 | 0.551 | 18 | 1.795 | 1.534 | 99.934 | -0.184 | 51.541 |
| 4 | 2,892 | 2D1B04CB-F44A-4941-BA90-C7BDBEC82C5E | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 9,292.400 | 0.185 | 4 | 0.421 | 1.503 | 98.924 | -0.220 | 51.519 |
| 5 | 3,040 | 139B5E9C-C08F-4BCD-BCB5-B0C582BF47F2 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,214.300 | 5.274 | 23 | 2.284 | 1.469 | 99.960 | -4.021 | 50.527 |
| 6 | 3,115 | 0D030DE3-B497-44A5-ADE8-22DC54B5047A | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,107.900 | 0.180 | 8 | 0.813 | 1.452 | 99.669 | -0.207 | 51.515 |
| 7 | 3,240 | C58DE491-DC7A-4F90-97B7-A86F028C8525 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 11,071.200 | 0.143 | 4 | 0.420 | 1.423 | 98.923 | -0.219 | 51.532 |
| 8 | 3,293 | 25FBEE69-3C26-4E54-B1C8-244B02CA5EB8 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,274.500 | 0.215 | 5 | 0.518 | 1.416 | 99.241 | -0.027 | 51.535 |
| 9 | 3,715 | B2F68F81-82BB-4933-8A55-9DDA41DF1B34 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 7,692.400 | 0.184 | 9 | 0.909 | 1.346 | 99.731 | -0.188 | 51.539 |
| 10 | 3,808 | 1E7CF005-BB1D-48C8-B20B-3CD98FF0C5FD | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,578.900 | 3.681 | 16 | 1.594 | 1.329 | 99.915 | -2.140 | 50.984 |

## Road Classification: Unclassified

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 17,854 | 938D74FF-5A33-4943-A80B-77563E52F32F | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,822.000 | 0.131 | 9 | 0.891 | 0.685 | 99.715 | -1.545 | 53.799 |
| 2 | 19,406 | 52E63066-0936-42ED-B284-750EFDDEF107 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,144.600 | 1.829 | 5 | 0.507 | 0.660 | 99.198 | -1.172 | 50.827 |
| 3 | 19,726 | 45BACFBC-F2EA-4C89-8C02-DC2B5F71C30C | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,269.800 | 1.559 | 11 | 1.081 | 0.655 | 99.804 | -1.092 | 50.856 |
| 4 | 21,795 | BCA0A7CC-6C8E-4CF3-A600-CA657083F4E8 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 5,450.800 | 0.810 | 7 | 0.697 | 0.627 | 99.544 | -1.641 | 53.676 |
| 5 | 28,955 | 5DE4CD5C-E5F0-434F-92BC-260AF6A77A70 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,832.700 | 0.196 | 9 | 0.883 | 0.550 | 99.706 | -0.088 | 51.513 |
| 6 | 31,814 | 7E8351C1-D656-4E86-90DD-B3D0E95075D9 | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 4,058.100 | 0.781 | 8 | 0.786 | 0.526 | 99.632 | -0.195 | 51.643 |
| 7 | 31,889 | 6534C4C5-3483-44D6-BCD8-3BADC7E9CC60 | Unclassified | Local Road | other_urban | urban_minor | Collapsed Dual Carriageway | 1 | 0 | 0 | 1,732.200 | 0.112 | 9 | 0.880 | 0.525 | 99.704 | -1.545 | 53.800 |
| 8 | 32,727 | 5D5599EF-026D-4A0C-AC67-F13AE5618484 | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,469.800 | 0.151 | 8 | 0.785 | 0.519 | 99.631 | -1.510 | 52.410 |
| 9 | 33,386 | 00ADC461-C483-43D0-96D4-0A9D90AD959D | Unclassified | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,751.900 | 0.087 | 7 | 0.690 | 0.514 | 99.528 | -1.543 | 53.799 |
| 10 | 33,434 | F1393950-85A8-45A5-949C-3ACBF16BD61A | Unclassified | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,832.000 | 2.390 | 13 | 1.258 | 0.514 | 99.857 | -1.740 | 53.668 |

## Road Archetype: motorway

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | DB762ED8-493D-4273-89AA-1E793BEA822C | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 56,389.300 | 15.627 | 74 | 7.421 | 26.721 | 99.998 | -3.430 | 50.798 |
| 2 | 2 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 45,717.100 | 16.221 | 90 | 9.018 | 23.396 | 99.999 | -1.188 | 52.526 |
| 3 | 3 | 62A5F5FF-7806-45F6-8E1A-A01332356323 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 38,654.900 | 19.085 | 143 | 14.311 | 23.133 | 100.000 | -1.986 | 51.537 |
| 4 | 4 | FF70F2F4-ABFF-4211-BCBF-D45425648018 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 38,451.400 | 16.291 | 209 | 20.899 | 20.087 | 100.000 | 0.774 | 51.304 |
| 5 | 5 | 7E604C90-3F9B-43EA-ADE1-416FFDB2D167 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 38,479.900 | 17.578 | 84 | 8.416 | 19.251 | 99.998 | -1.184 | 51.460 |
| 6 | 6 | AF0F5809-67DC-43D2-848E-E1A2E08E2628 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 37,156.700 | 17.230 | 97 | 9.714 | 18.358 | 99.999 | -1.124 | 51.814 |
| 7 | 7 | 12229866-3F77-4DB3-9034-1029042770E5 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 54,574.400 | 9.905 | 258 | 25.788 | 18.345 | 100.000 | -0.262 | 51.277 |
| 8 | 8 | 22B9F354-B2AA-4300-811B-A0DCDCFA2A7D | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 40,768.500 | 15.283 | 72 | 7.218 | 18.340 | 99.998 | -1.270 | 52.002 |
| 9 | 9 | D9CF0BEC-6749-44F5-8688-7F3D432DF36A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 77,077.900 | 6.192 | 53 | 5.320 | 18.082 | 99.995 | -0.341 | 51.492 |
| 10 | 10 | 0E4A9C14-C13E-4F70-9A16-6306AE5D3296 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 1 | 0 | 0 | 52,991.600 | 10.689 | 46 | 4.622 | 17.954 | 99.992 | -1.595 | 52.646 |

## Road Archetype: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 102 | 7ABDD823-7CBD-4802-A732-33559BA80616 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 11,698.800 | 12.647 | 103 | 10.298 | 9.537 | 99.999 | -0.878 | 50.851 |
| 2 | 143 | F661CF64-7E58-4AA7-A42B-3054B4306A68 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 19,245.900 | 6.328 | 76 | 7.602 | 8.226 | 99.998 | 0.302 | 51.631 |
| 3 | 153 | 747C8806-A6D6-465B-871C-845C059C3080 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 19,508.000 | 8.694 | 32 | 3.217 | 7.941 | 99.982 | -3.788 | 50.723 |
| 4 | 166 | 223F6B05-29DF-4A08-8C8C-B8DA44DD9298 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,055.300 | 8.696 | 54 | 5.408 | 7.556 | 99.995 | -5.078 | 50.321 |
| 5 | 174 | 62EFFFFE-0DE2-438F-8F83-D1D1A71B35EA | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,071.000 | 8.264 | 32 | 3.216 | 7.366 | 99.982 | -3.901 | 50.735 |
| 6 | 201 | 59AD968E-0D5A-4432-A9E8-4B8C84451F84 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,543.900 | 7.991 | 31 | 3.116 | 6.876 | 99.981 | -4.873 | 50.414 |
| 7 | 208 | 5A1BBEEE-9B67-4AA3-9520-97FC0B311A96 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,441.400 | 5.071 | 80 | 7.994 | 6.711 | 99.998 | -0.331 | 51.357 |
| 8 | 230 | 45B942B0-9125-44B4-B7FD-69A011E03E72 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,474.100 | 3.499 | 127 | 12.671 | 6.386 | 100.000 | 0.208 | 51.430 |
| 9 | 268 | 91026D33-C723-403D-B651-1BF6C9E75E70 | A Road | A Road | trunk_a | trunk_a | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,873.300 | 5.346 | 35 | 3.512 | 5.875 | 99.985 | -1.315 | 51.643 |
| 10 | 278 | 8F227E78-6E1C-4C80-9B84-32774702BBF4 | A Road | A Road | trunk_a | trunk_a | Single Carriageway | 0 | 0 | 0 | 19,720.400 | 5.200 | 42 | 4.208 | 5.700 | 99.990 | -5.366 | 50.207 |

## Road Archetype: urban_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 108 | 51991592-6273-4FA0-B34A-CEACF052E777 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,885.800 | 2.935 | 105 | 10.496 | 9.350 | 99.999 | -0.001 | 51.560 |
| 2 | 165 | 595E8891-9205-445B-9296-702A22E823DA | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,267.800 | 2.098 | 47 | 4.711 | 7.609 | 99.993 | -0.203 | 51.519 |
| 3 | 193 | C39C13F4-205A-4BB8-9115-A60E97910F01 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 19,786.500 | 2.291 | 50 | 5.008 | 7.000 | 99.994 | -0.441 | 51.885 |
| 4 | 255 | A437DF2C-5344-4058-866D-6ECF773A608B | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 22,352.000 | 1.827 | 70 | 6.995 | 6.050 | 99.997 | 0.055 | 51.565 |
| 5 | 265 | E7D07249-6666-492E-88E1-984FC87A5A59 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 28,962.100 | 1.511 | 103 | 10.279 | 5.927 | 99.999 | 0.068 | 51.546 |
| 6 | 272 | FA4E48A8-3348-48DF-AC18-E81DD06AF88B | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 17,802.600 | 0.223 | 99 | 9.880 | 5.806 | 99.999 | -0.072 | 51.585 |
| 7 | 287 | B980D095-8D75-4365-AC28-5BCF3DF67D11 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 27,872.100 | 0.276 | 39 | 3.909 | 5.535 | 99.989 | -0.127 | 51.488 |
| 8 | 299 | ECAF9F1D-E364-4F3A-A7B6-2C744018D604 | A Road | A Road | other_urban | urban_a_road | Single Carriageway | 0 | 0 | 0 | 22,906.000 | 0.309 | 45 | 4.505 | 5.354 | 99.992 | -0.073 | 51.581 |
| 9 | 306 | 6A3D2D1E-D14A-4D89-B29D-1D4D615A5080 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 27,027.900 | 2.639 | 1 | 0.128 | 5.302 | 95.079 | -3.006 | 53.414 |
| 10 | 319 | 5EA99404-841D-411E-A631-90ED7E42A8F8 | A Road | A Road | other_urban | urban_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 37,957.700 | 0.755 | 51 | 5.100 | 5.099 | 99.994 | -0.328 | 51.534 |

## Road Archetype: rural_a_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 305 | A0E6AE20-B4AA-4A3D-9329-8C7611351750 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,466.200 | 8.188 | 61 | 6.096 | 5.304 | 99.996 | 0.535 | 51.664 |
| 2 | 378 | FD31F6C4-0EC6-4397-8327-E47E46D1E5A2 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 21,105.100 | 4.544 | 26 | 2.612 | 4.544 | 99.971 | -1.814 | 50.805 |
| 3 | 435 | 656DFDF8-8BCC-4E61-AB70-DA334530A1F5 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 30,496.400 | 2.868 | 8 | 0.823 | 4.126 | 99.674 | -4.841 | 50.522 |
| 4 | 482 | 98B74305-10C3-4D73-835F-9287DF8C2B6C | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 12,134.300 | 6.699 | 21 | 2.113 | 3.812 | 99.953 | -0.012 | 51.856 |
| 5 | 621 | 89D775E5-B175-45FA-9009-D353F84D302F | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 13,900.900 | 5.057 | 8 | 0.822 | 3.267 | 99.674 | -1.945 | 53.334 |
| 6 | 710 | A7A0B915-AA50-4E9F-8B2D-3F443DBC28E8 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 34,751.600 | 1.863 | 12 | 1.217 | 2.999 | 99.851 | -3.546 | 50.628 |
| 7 | 717 | F0910578-5FAE-4F8B-8B62-020287B3621B | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 16,724.600 | 4.495 | 39 | 3.891 | 2.981 | 99.988 | 1.115 | 51.842 |
| 8 | 737 | 7DF328A5-D6CB-4615-984B-EC0FFDCCB8C9 | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 12,811.100 | 4.714 | 15 | 1.514 | 2.941 | 99.905 | -0.716 | 51.951 |
| 9 | 775 | 9F068480-CE0B-4CCA-AA7C-DB455776A7FF | A Road | A Road | other_rural | rural_a_road | Collapsed Dual Carriageway | 1 | 0 | 0 | 25,809.400 | 2.435 | 17 | 1.712 | 2.854 | 99.927 | -1.540 | 55.160 |
| 10 | 787 | C521DAB5-C86C-4810-A60B-A28974331DB1 | A Road | A Road | other_rural | rural_a_road | Single Carriageway | 0 | 0 | 0 | 24,656.100 | 1.890 | 8 | 0.821 | 2.828 | 99.674 | -3.492 | 50.682 |

## Road Archetype: urban_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,891 | C10AB286-2FC8-446B-B9B9-3CF56FD88CD2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 11,308.800 | 0.267 | 4 | 0.422 | 1.817 | 98.927 | -1.852 | 52.488 |
| 2 | 1,971 | 08FD9A0B-E2ED-42CA-BBA7-A64A5A92C4EC | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 13,362.200 | 1.942 | 3 | 0.324 | 1.777 | 98.388 | -1.427 | 53.431 |
| 3 | 2,744 | C5DD3055-F618-410F-AD85-FEE4DB8B2549 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,640.400 | 0.551 | 18 | 1.795 | 1.534 | 99.934 | -0.184 | 51.541 |
| 4 | 2,892 | 2D1B04CB-F44A-4941-BA90-C7BDBEC82C5E | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 9,292.400 | 0.185 | 4 | 0.421 | 1.503 | 98.924 | -0.220 | 51.519 |
| 5 | 3,115 | 0D030DE3-B497-44A5-ADE8-22DC54B5047A | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,107.900 | 0.180 | 8 | 0.813 | 1.452 | 99.669 | -0.207 | 51.515 |
| 6 | 3,240 | C58DE491-DC7A-4F90-97B7-A86F028C8525 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 11,071.200 | 0.143 | 4 | 0.420 | 1.423 | 98.923 | -0.219 | 51.532 |
| 7 | 3,293 | 25FBEE69-3C26-4E54-B1C8-244B02CA5EB8 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 10,274.500 | 0.215 | 5 | 0.518 | 1.416 | 99.241 | -0.027 | 51.535 |
| 8 | 3,715 | B2F68F81-82BB-4933-8A55-9DDA41DF1B34 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 7,692.400 | 0.184 | 9 | 0.909 | 1.346 | 99.731 | -0.188 | 51.539 |
| 9 | 3,811 | 69D7DA01-ED2C-4F85-8E4E-D09D943B91B2 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 6,304.500 | 0.237 | 17 | 1.692 | 1.329 | 99.924 | -0.064 | 51.525 |
| 10 | 3,949 | F295DF55-9DE0-4D7D-A1E0-11D671AEF430 | B Road | B Road | other_urban | urban_b_road | Single Carriageway | 0 | 0 | 0 | 9,284.900 | 0.157 | 11 | 1.104 | 1.307 | 99.817 | -0.202 | 51.533 |

## Road Archetype: rural_b_road

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3,040 | 139B5E9C-C08F-4BCD-BCB5-B0C582BF47F2 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,214.300 | 5.274 | 23 | 2.284 | 1.469 | 99.960 | -4.021 | 50.527 |
| 2 | 3,808 | 1E7CF005-BB1D-48C8-B20B-3CD98FF0C5FD | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,578.900 | 3.681 | 16 | 1.594 | 1.329 | 99.915 | -2.140 | 50.984 |
| 3 | 5,859 | C318621A-B93A-4C03-A279-D440D7E566A9 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 3,602.100 | 4.174 | 27 | 2.660 | 1.112 | 99.972 | -2.749 | 51.284 |
| 4 | 6,546 | 20AB2E37-034B-4B3D-BC28-EECB1559AAE6 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,003.000 | 3.823 | 6 | 0.612 | 1.063 | 99.436 | -0.323 | 52.851 |
| 5 | 6,963 | FC2665C5-0AD2-4683-9A2F-CA9B985B9951 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 8,518.400 | 1.822 | 4 | 0.417 | 1.037 | 98.912 | -1.452 | 52.980 |
| 6 | 7,084 | 1EA197CF-A44C-4656-A054-ADD9D2872BD7 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 3,485.400 | 4.280 | 2 | 0.223 | 1.030 | 97.345 | -3.875 | 50.615 |
| 7 | 7,246 | EA7F0705-5592-41E6-A409-A82AE504823B | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 6,160.100 | 2.537 | 7 | 0.709 | 1.019 | 99.569 | -1.113 | 53.852 |
| 8 | 7,453 | F10D4083-55D5-4094-94CB-CACA05C2D7DF | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 9,181.000 | 1.626 | 12 | 1.195 | 1.008 | 99.843 | -1.356 | 53.596 |
| 9 | 8,183 | 13D3D399-A12C-4CDD-8D44-A0F24E325EF3 | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 5,533.300 | 2.750 | 2 | 0.222 | 0.968 | 97.341 | -1.642 | 53.308 |
| 10 | 8,446 | 7350A90C-A59A-4E33-9CB6-2C8DC36278FD | B Road | B Road | other_rural | rural_b_road | Single Carriageway | 0 | 0 | 0 | 4,648.400 | 2.547 | 3 | 0.319 | 0.954 | 98.367 | -0.294 | 53.598 |

## Road Archetype: urban_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 801 | 90900201-4148-4BDC-8F78-5FAFA847F7C7 | Unknown | Minor Road | other_urban | urban_minor | Collapsed Dual Carriageway | 1 | 0 | 0 | 1,308.300 | 0.419 | 21 | 2.107 | 2.801 | 99.952 | -3.203 | 55.951 |
| 2 | 2,076 | 0AFF5EE0-3267-43D0-9EC5-CA6119303BE6 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,736.700 | 3.048 | 23 | 2.291 | 1.737 | 99.960 | -3.026 | 53.793 |
| 3 | 2,446 | C1302B26-E9B8-4379-A75E-6E9B79BAD3A4 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,863.600 | 2.091 | 32 | 3.172 | 1.615 | 99.981 | -0.124 | 50.861 |
| 4 | 3,236 | 572E079D-C1C0-47BE-BAAD-41F4DF2D960C | Classified Unnumbered | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,254.800 | 0.318 | 72 | 7.085 | 1.425 | 99.997 | -0.064 | 51.473 |
| 5 | 3,750 | CA9B7AFE-75CA-4F44-B97C-183B71282EE8 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,161.400 | 0.291 | 8 | 0.811 | 1.340 | 99.668 | -0.002 | 51.552 |
| 6 | 4,366 | 3135435D-E5A1-4E25-B043-1F4937CCE9C7 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,065.900 | 0.254 | 3 | 0.322 | 1.252 | 98.380 | -1.481 | 53.368 |
| 7 | 4,572 | AFCA7278-962D-4A10-975D-D6A3DE91444B | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 3,471.500 | 0.320 | 9 | 0.908 | 1.230 | 99.730 | -0.237 | 51.565 |
| 8 | 4,631 | 78E35D31-3214-46C9-B09E-74F17205C6FC | Classified Unnumbered | Local Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 6,541.500 | 0.198 | 5 | 0.517 | 1.225 | 99.237 | -1.134 | 52.637 |
| 9 | 4,897 | 82C7FF83-94D8-4BDE-9218-3417389FA081 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 2,245.700 | 0.308 | 0 | 0.028 | 1.197 | 87.298 | -1.969 | 52.487 |
| 10 | 5,450 | D25E4AA7-7B03-4F04-A7D6-412B77112C52 | Classified Unnumbered | Minor Road | other_urban | urban_minor | Single Carriageway | 0 | 0 | 0 | 1,977.800 | 0.316 | 7 | 0.711 | 1.146 | 99.573 | -0.410 | 51.652 |

## Road Archetype: rural_minor

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 12,374 | D81B9DBA-4BB8-4C2B-80AF-9C6639E5FDBD | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 665.400 | 3.581 | 29 | 2.828 | 0.809 | 99.975 | -1.170 | 50.680 |
| 2 | 12,984 | 5CF5D37A-1FBF-406F-A242-82487ACF21B8 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 4,097.800 | 1.567 | 6 | 0.607 | 0.791 | 99.422 | 0.249 | 51.414 |
| 3 | 16,855 | A840D400-FB6D-4004-8716-855F2C873B6A | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,104.900 | 2.716 | 0 | 0.028 | 0.703 | 87.262 | -1.370 | 53.896 |
| 4 | 17,376 | DEA988A0-68C2-45D8-BC49-081052D8BFB3 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,981.700 | 0.187 | 1 | 0.124 | 0.693 | 95.004 | -2.548 | 51.189 |
| 5 | 18,254 | 10391DF9-E4A0-41AC-8859-058626C1D134 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,214.800 | 2.359 | 3 | 0.316 | 0.678 | 98.330 | -0.801 | 53.531 |
| 6 | 18,882 | B323765C-526C-4AB3-9DF6-299786860AF4 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 1,842.500 | 3.216 | 2 | 0.219 | 0.668 | 97.297 | -0.297 | 53.529 |
| 7 | 21,569 | E261BCBD-8D2B-4238-AE08-F358ED79FC4E | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 3,276.200 | 0.796 | 1 | 0.123 | 0.629 | 94.986 | -1.420 | 53.672 |
| 8 | 22,443 | 0C53BAC7-6BC0-44C6-B782-B0CC56EE3F41 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,233.300 | 2.193 | 2 | 0.219 | 0.619 | 97.281 | 0.981 | 51.032 |
| 9 | 22,762 | D21C78BB-43E4-4A55-89CE-B2A80D7D0B65 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 4,251.900 | 1.230 | 2 | 0.219 | 0.615 | 97.280 | -1.720 | 54.830 |
| 10 | 23,056 | 4EEA5A6C-FB37-484C-94FF-3D03265824B2 | Classified Unnumbered | Minor Road | other_rural | rural_minor | Single Carriageway | 0 | 0 | 0 | 2,983.300 | 1.221 | 1 | 0.123 | 0.611 | 94.979 | -1.155 | 53.718 |

## Road Archetype: other_unknown

| within_group_rank | global_risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | is_dual | is_slip_road | is_roundabout | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2,171 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | A Road | other_unknown | other_unknown | Collapsed Dual Carriageway | 1 | 0 | 0 | 15,382.000 | 3.374 | 17 | 1.700 | 1.704 | 99.925 | -0.450 | 53.703 |
| 2 | 3,774 | C51DA9F7-73F7-4E79-B42E-EC481E872721 | A Road | A Road | other_unknown | other_unknown | Collapsed Dual Carriageway | 1 | 0 | 0 | 17,393.700 | 2.411 | 9 | 0.909 | 1.336 | 99.731 | -2.714 | 53.353 |
| 3 | 7,174 | 3ABAEE19-657F-4356-BC1E-8C1DBEFA65F3 | A Road | A Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 18,055.500 | 2.774 | 1 | 0.125 | 1.024 | 95.045 | -3.005 | 53.400 |
| 4 | 104,712 | D0ED5E45-1727-4FDB-B864-47B42571BE7D | Classified Unnumbered | Minor Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 1,053.600 | 5.189 | 0 | 0.026 | 0.278 | 86.758 | -5.320 | 58.057 |
| 5 | 382,147 | 1F6B2F40-EB73-4319-8B20-B6A84CC06929 | Classified Unnumbered | Minor Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 351.600 | 3.267 | 0 | 0.023 | 0.103 | 83.367 | -7.442 | 57.023 |
| 6 | 1,671,868 | C3DC224D-8786-425D-BB99-94542BBAFB26 | Not Classified | Local Access Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 1,170.000 | 0.635 | 0 | 0.009 | 0.012 | 56.412 | -1.161 | 50.736 |
| 7 | 3,070,033 | D807EEF4-29A7-405E-8656-9B8EEDA9CE7B | Unknown | Restricted Local Access Road | other_unknown | other_unknown | Single Carriageway | 0 | 0 | 0 | 829.200 | 0.873 | 0 | 0.002 | 0.002 | 21.996 | -5.062 | 51.704 |

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
