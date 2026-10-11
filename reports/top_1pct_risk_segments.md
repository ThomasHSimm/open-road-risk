# Top 1% Highest-Risk Road Segments

## Purpose

This table lists the top 1% highest-risk road links after controlling for traffic exposure. It is intended for inspection, mapping, portfolio review, and demo use.

## Method

- Ranking field used: `risk_percentile`.
- EB-adjusted ranking used: no.
- Top 1% definition: sorted all 3,941,299 scored links by `risk_percentile` descending, with `link_id` as a deterministic tie-break, then selected the first 39,413 rows (1%).
- Created at: `2026-10-06T22:15:33+00:00`.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores_eb.parquet | 2026-10-06T22:12:16.028189+00:00 | 385,058,544 |
| data/processed/shapefiles/openroads.parquet | 2026-07-02T23:47:44.335016+00:00 | 853,847,157 |
| data/features/network_features.parquet | 2026-07-03T21:39:50.600900+00:00 | 275,258,014 |

Project/model output version: `0.1.0`.

## Count By Road Family

| family | count | share |
| --- | --- | --- |
| other_urban | 29,328 | 74.4% |
| other_rural | 4,483 | 11.4% |
| trunk_a | 3,414 | 8.7% |
| motorway | 2,185 | 5.5% |
| other_unknown | 3 | 0.0% |

## Count By Road Classification

| road_classification | count | share |
| --- | --- | --- |
| A Road | 33,328 | 84.6% |
| B Road | 2,433 | 6.2% |
| Motorway | 2,185 | 5.5% |
| Classified Unnumbered | 1,447 | 3.7% |
| Unclassified | 17 | 0.0% |
| Unknown | 3 | 0.0% |

## Count By Urban/Rural

| ruc_urban_rural | count | share |
| --- | --- | --- |
| Urban | 32,122 | 81.5% |
| Rural | 7,277 | 18.5% |
| Unknown | 14 | 0.0% |

## Count By Road Archetype

| road_archetype | count | share |
| --- | --- | --- |
| urban_a_road | 25,872 | 65.6% |
| rural_a_road | 4,039 | 10.2% |
| trunk_a | 3,414 | 8.7% |
| motorway | 2,185 | 5.5% |
| urban_b_road | 2,032 | 5.2% |
| urban_minor | 1,424 | 3.6% |
| rural_b_road | 401 | 1.0% |
| rural_minor | 43 | 0.1% |
| other_unknown | 3 | 0.0% |

## Numeric Summary

| field | n | min | median | mean | p90 | max |
| --- | --- | --- | --- | --- | --- | --- |
| estimated_aadt | 39,413 | 568.400 | 18,625.800 | 19,201.960 | 26,168.820 | 110,889.800 |
| link_length_km | 39,413 | 0.002 | 0.190 | 0.507 | 1.210 | 19.085 |
| collision_count | 39,413 | 0 | 4.000 | 6.417 | 14.000 | 267 |
| fatal_count | 39,413 | 0 | 0.000 | 0.110 | 0.000 | 7 |
| serious_count | 39,413 | 0 | 1.000 | 1.105 | 3.000 | 36 |
| predicted_eb | 39,413 | 0.027 | 0.410 | 0.649 | 1.380 | 26.664 |
| predicted_xgb | 39,413 | 0.475 | 0.655 | 0.879 | 1.307 | 26.721 |
| predicted_glm | 39,413 | 0.269 | 1.643 | 1.781 | 2.551 | 181.623 |

## Top Examples

| risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | risk_percentile | is_motorway | low_exposure_flag | sparse_collision_history_flag | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DB762ED8-493D-4273-89AA-1E793BEA822C | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 56,389.300 | 15.627 | 74 | 7.421 | 26.721 | 99.998 | 100.000 | 1 | 0 | 0 | -3.430 | 50.798 |
| 2 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 45,717.100 | 16.221 | 90 | 9.018 | 23.396 | 99.999 | 100.000 | 1 | 0 | 0 | -1.188 | 52.526 |
| 3 | 62A5F5FF-7806-45F6-8E1A-A01332356323 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 38,654.900 | 19.085 | 143 | 14.311 | 23.133 | 100.000 | 100.000 | 1 | 0 | 0 | -1.986 | 51.537 |
| 4 | FF70F2F4-ABFF-4211-BCBF-D45425648018 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 38,451.400 | 16.291 | 209 | 20.899 | 20.087 | 100.000 | 100.000 | 1 | 0 | 0 | 0.774 | 51.304 |
| 5 | 7E604C90-3F9B-43EA-ADE1-416FFDB2D167 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 38,479.900 | 17.578 | 84 | 8.416 | 19.251 | 99.998 | 100.000 | 1 | 0 | 0 | -1.184 | 51.460 |
| 6 | AF0F5809-67DC-43D2-848E-E1A2E08E2628 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 37,156.700 | 17.230 | 97 | 9.714 | 18.358 | 99.999 | 100.000 | 1 | 0 | 0 | -1.124 | 51.814 |
| 7 | 12229866-3F77-4DB3-9034-1029042770E5 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 54,574.400 | 9.905 | 258 | 25.788 | 18.345 | 100.000 | 100.000 | 1 | 0 | 0 | -0.262 | 51.277 |
| 8 | 22B9F354-B2AA-4300-811B-A0DCDCFA2A7D | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 40,768.500 | 15.283 | 72 | 7.218 | 18.340 | 99.998 | 100.000 | 1 | 0 | 0 | -1.270 | 52.002 |
| 9 | D9CF0BEC-6749-44F5-8688-7F3D432DF36A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 77,077.900 | 6.192 | 53 | 5.320 | 18.082 | 99.995 | 100.000 | 1 | 0 | 0 | -0.341 | 51.492 |
| 10 | 0E4A9C14-C13E-4F70-9A16-6306AE5D3296 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 52,991.600 | 10.689 | 46 | 4.622 | 17.954 | 99.992 | 100.000 | 1 | 0 | 0 | -1.595 | 52.646 |
| 11 | 23C59E20-F791-4D88-87CE-8E8422A18973 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 56,355.600 | 9.214 | 137 | 13.707 | 17.787 | 100.000 | 100.000 | 1 | 0 | 0 | 0.206 | 51.642 |
| 12 | D42CBE2B-8CBB-4FD3-BE59-FF61D34D57D9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 57,099.500 | 7.724 | 220 | 21.993 | 17.750 | 100.000 | 100.000 | 1 | 0 | 0 | -0.110 | 51.688 |
| 13 | 3BA6561C-4542-4C91-8E7A-DE913EFBCC87 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 53,086.500 | 8.897 | 183 | 18.298 | 17.384 | 100.000 | 100.000 | 1 | 0 | 0 | -0.123 | 51.220 |
| 14 | 2C8C18E7-E809-44ED-9F00-8CFDA9100AEB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 50,867.700 | 10.665 | 113 | 11.310 | 17.203 | 99.999 | 100.000 | 1 | 0 | 0 | -0.787 | 51.465 |
| 15 | 2A413476-76D1-446A-B219-46372A2F6C2A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 52,914.600 | 11.179 | 68 | 6.817 | 17.026 | 99.997 | 100.000 | 1 | 0 | 0 | -2.440 | 51.501 |
| 16 | 2847FB9E-D79B-4BA1-8EF6-3D78185BA690 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 61,289.100 | 11.069 | 41 | 4.122 | 16.905 | 99.990 | 100.000 | 1 | 0 | 0 | -2.495 | 51.592 |
| 17 | 03C94C2B-D930-440E-ABE2-E09D86988EA3 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 64,334.300 | 8.161 | 58 | 5.819 | 16.823 | 99.995 | 100.000 | 1 | 0 | 0 | -0.473 | 51.400 |
| 18 | 348C3546-FDA1-47AA-97D0-866A94EEE8F2 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 55,343.300 | 12.566 | 41 | 4.122 | 16.584 | 99.990 | 100.000 | 1 | 0 | 0 | -2.375 | 51.709 |
| 19 | 36F42C08-799D-40E1-9810-BF0A842CE9F9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 61,282.200 | 7.759 | 117 | 11.708 | 15.914 | 99.999 | 100.000 | 1 | 0 | 0 | 0.279 | 51.535 |
| 20 | A0E0E728-BB7C-4FAD-93A3-30DDA7DE2974 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 58,882.000 | 8.214 | 72 | 7.216 | 15.707 | 99.997 | 100.000 | 1 | 0 | 0 | -2.135 | 52.251 |

## Caveats

- This is a triage and screening output, not causal proof.
- Motorway calibration remains a known caveat.
- Sparse collision histories should be interpreted cautiously.
- This does not replace engineering audit or iRAP-style assessment.

## Next Use

This output can feed a Streamlit map, GeoPackage export, or stakeholder demo.
