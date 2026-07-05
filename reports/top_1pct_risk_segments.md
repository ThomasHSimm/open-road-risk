# Top 1% Highest-Risk Road Segments

## Purpose

This table lists the top 1% highest-risk road links after controlling for traffic exposure. It is intended for inspection, mapping, portfolio review, and demo use.

## Method

- Ranking field used: `risk_percentile`.
- EB-adjusted ranking used: no.
- Top 1% definition: sorted all 3,941,299 scored links by `risk_percentile` descending, with `link_id` as a deterministic tie-break, then selected the first 39,413 rows (1%).
- Created at: `2026-07-05T21:44:29+00:00`.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores.parquet | 2026-07-04T14:34:27.740790+00:00 | 283,415,144 |
| data/processed/shapefiles/openroads.parquet | 2026-07-02T23:47:44.335016+00:00 | 853,847,157 |
| data/features/network_features.parquet | 2026-07-03T21:39:50.600900+00:00 | 275,258,014 |

Project/model output version: `0.1.0`.

## Count By Road Family

| family | count | share |
| --- | --- | --- |
| other_urban | 28,411 | 72.1% |
| other_rural | 5,140 | 13.0% |
| trunk_a | 3,428 | 8.7% |
| motorway | 2,431 | 6.2% |
| other_unknown | 3 | 0.0% |

## Count By Road Classification

| road_classification | count | share |
| --- | --- | --- |
| A Road | 31,799 | 80.7% |
| B Road | 3,305 | 8.4% |
| Motorway | 2,431 | 6.2% |
| Classified Unnumbered | 1,824 | 4.6% |
| Unclassified | 48 | 0.1% |
| Unknown | 4 | 0.0% |
| Not Classified | 2 | 0.0% |

## Count By Urban/Rural

| ruc_urban_rural | count | share |
| --- | --- | --- |
| Urban | 31,354 | 79.6% |
| Rural | 8,046 | 20.4% |
| Unknown | 13 | 0.0% |

## Count By Road Archetype

| road_archetype | count | share |
| --- | --- | --- |
| urban_a_road | 23,755 | 60.3% |
| rural_a_road | 4,613 | 11.7% |
| trunk_a | 3,428 | 8.7% |
| urban_b_road | 2,865 | 7.3% |
| motorway | 2,431 | 6.2% |
| urban_minor | 1,791 | 4.5% |
| rural_b_road | 440 | 1.1% |
| rural_minor | 87 | 0.2% |
| other_unknown | 3 | 0.0% |

## Numeric Summary

| field | n | min | median | mean | p90 | max |
| --- | --- | --- | --- | --- | --- | --- |
| estimated_aadt | 39,413 | 312.600 | 11,559.200 | 13,206.159 | 20,893.320 | 101,745.000 |
| link_length_km | 39,413 | 0.002 | 0.190 | 0.519 | 1.227 | 19.085 |
| collision_count | 39,413 | 0 | 4.000 | 6.409 | 14.000 | 267 |
| fatal_count | 39,413 | 0 | 0.000 | 0.110 | 0.000 | 7 |
| serious_count | 39,413 | 0 | 1.000 | 1.099 | 3.000 | 36 |
| predicted_xgb | 39,413 | 0.435 | 0.607 | 0.827 | 1.245 | 26.749 |
| predicted_glm | 39,413 | 0.143 | 1.646 | 1.827 | 2.845 | 210.543 |

## Top Examples

| risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | estimated_aadt | link_length_km | collision_count | predicted_xgb | risk_percentile | is_motorway | low_exposure_flag | sparse_collision_history_flag | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 62A5F5FF-7806-45F6-8E1A-A01332356323 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 27,316.500 | 19.085 | 143 | 26.749 | 100.000 | 1 | 0 | 0 | -1.986 | 51.537 |
| 2 | FF70F2F4-ABFF-4211-BCBF-D45425648018 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 28,645.200 | 16.291 | 209 | 26.338 | 100.000 | 1 | 0 | 0 | 0.774 | 51.304 |
| 3 | FE40918E-61F2-40D9-8C75-520D2EA696FD | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 35,982.500 | 12.363 | 117 | 24.332 | 100.000 | 1 | 0 | 0 | 0.215 | 51.931 |
| 4 | 22B9F354-B2AA-4300-811B-A0DCDCFA2A7D | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 28,541.100 | 15.283 | 72 | 22.078 | 100.000 | 1 | 0 | 0 | -1.270 | 52.002 |
| 5 | AF0F5809-67DC-43D2-848E-E1A2E08E2628 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 24,239.900 | 17.230 | 97 | 21.352 | 100.000 | 1 | 0 | 0 | -1.124 | 51.814 |
| 6 | EC5693F4-942F-47B9-A3D9-A146089227F2 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 43,808.400 | 9.477 | 72 | 20.943 | 100.000 | 1 | 0 | 0 | -2.322 | 53.020 |
| 7 | 7E604C90-3F9B-43EA-ADE1-416FFDB2D167 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 23,776.500 | 17.578 | 84 | 20.843 | 100.000 | 1 | 0 | 0 | -1.184 | 51.460 |
| 8 | 12229866-3F77-4DB3-9034-1029042770E5 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 32,511.800 | 9.905 | 258 | 19.960 | 100.000 | 1 | 0 | 0 | -0.262 | 51.277 |
| 9 | D42CBE2B-8CBB-4FD3-BE59-FF61D34D57D9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 35,353.100 | 7.724 | 220 | 19.940 | 100.000 | 1 | 0 | 0 | -0.110 | 51.688 |
| 10 | E32D6E17-A06D-4EB8-8C7A-94E29341B452 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 44,971.200 | 8.100 | 47 | 19.877 | 100.000 | 1 | 0 | 0 | -1.789 | 51.536 |
| 11 | E68D0DAE-2675-4014-8740-920F69B20AEA | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 25,855.800 | 11.276 | 65 | 19.364 | 100.000 | 1 | 0 | 0 | -0.844 | 51.628 |
| 12 | 348C3546-FDA1-47AA-97D0-866A94EEE8F2 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 34,919.600 | 12.566 | 41 | 19.349 | 100.000 | 1 | 0 | 0 | -2.375 | 51.709 |
| 13 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 52,955.600 | 8.245 | 119 | 18.984 | 100.000 | 1 | 0 | 0 | -1.611 | 52.469 |
| 14 | 6EAAB2A0-A274-41EA-9B5B-2B4F8E3B8540 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 30,373.600 | 12.445 | 68 | 18.811 | 100.000 | 1 | 0 | 0 | -2.254 | 51.511 |
| 15 | 3BA6561C-4542-4C91-8E7A-DE913EFBCC87 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 29,622.600 | 8.897 | 183 | 18.194 | 100.000 | 1 | 0 | 0 | -0.123 | 51.220 |
| 16 | 2A413476-76D1-446A-B219-46372A2F6C2A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 30,488.900 | 11.179 | 68 | 18.040 | 100.000 | 1 | 0 | 0 | -2.440 | 51.501 |
| 17 | 07E7F45D-5CE6-404C-9855-E197C478A262 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 36,393.000 | 10.588 | 38 | 17.372 | 100.000 | 1 | 0 | 0 | -2.219 | 52.647 |
| 18 | BE3BBEEB-2ED2-4869-8421-A6836514AE3A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 38,336.700 | 9.200 | 81 | 17.368 | 100.000 | 1 | 0 | 0 | -2.753 | 53.919 |
| 19 | 2847FB9E-D79B-4BA1-8EF6-3D78185BA690 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 36,902.700 | 11.069 | 41 | 17.243 | 100.000 | 1 | 0 | 0 | -2.495 | 51.592 |
| 20 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 31,557.000 | 16.221 | 90 | 17.212 | 100.000 | 1 | 0 | 0 | -1.188 | 52.526 |

## Caveats

- This is a triage and screening output, not causal proof.
- Motorway calibration remains a known caveat.
- Sparse collision histories should be interpreted cautiously.
- This does not replace engineering audit or iRAP-style assessment.

## Next Use

This output can feed a Streamlit map, GeoPackage export, or stakeholder demo.
