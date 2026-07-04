# Top 1% Highest-Risk Road Segments

## Purpose

This table lists the top 1% highest-risk road links after controlling for traffic exposure. It is intended for inspection, mapping, portfolio review, and demo use.

## Method

- Ranking field used: `risk_percentile`.
- EB-adjusted ranking used: no.
- Top 1% definition: sorted all 3,941,299 scored links by `risk_percentile` descending, with `link_id` as a deterministic tie-break, then selected the first 39,413 rows (1%).
- Created at: `2026-07-04T12:44:54+00:00`.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores.parquet | 2026-07-04T12:18:58.712085+00:00 | 284,070,422 |
| data/processed/shapefiles/openroads.parquet | 2026-07-02T23:47:44.335016+00:00 | 853,847,157 |
| data/features/network_features.parquet | 2026-07-03T21:39:50.600900+00:00 | 275,258,014 |

Project/model output version: `0.1.0`.

## Count By Road Family

| family | count | share |
| --- | --- | --- |
| other_urban | 27,383 | 69.5% |
| other_rural | 7,352 | 18.7% |
| trunk_a | 2,675 | 6.8% |
| motorway | 2,001 | 5.1% |
| other_unknown | 2 | 0.0% |

## Count By Road Classification

| road_classification | count | share |
| --- | --- | --- |
| A Road | 28,435 | 72.1% |
| B Road | 4,234 | 10.7% |
| Classified Unnumbered | 4,168 | 10.6% |
| Motorway | 2,001 | 5.1% |
| Unclassified | 568 | 1.4% |
| Unknown | 6 | 0.0% |
| Not Classified | 1 | 0.0% |

## Count By Urban/Rural

| ruc_urban_rural | count | share |
| --- | --- | --- |
| Urban | 29,874 | 75.8% |
| Rural | 9,537 | 24.2% |
| Unknown | 2 | 0.0% |

## Count By Road Archetype

| road_archetype | count | share |
| --- | --- | --- |
| urban_a_road | 19,603 | 49.7% |
| rural_a_road | 6,155 | 15.6% |
| urban_minor | 4,343 | 11.0% |
| urban_b_road | 3,437 | 8.7% |
| trunk_a | 2,675 | 6.8% |
| motorway | 2,001 | 5.1% |
| rural_b_road | 797 | 2.0% |
| rural_minor | 400 | 1.0% |
| other_unknown | 2 | 0.0% |

## Numeric Summary

| field | n | min | median | mean | p90 | max |
| --- | --- | --- | --- | --- | --- | --- |
| estimated_aadt | 39,413 | 459.000 | 14,734.300 | 15,018.389 | 22,523.940 | 101,745.000 |
| link_length_km | 39,413 | 0.003 | 0.212 | 0.451 | 0.987 | 19.085 |
| collision_count | 39,413 | 0 | 2.000 | 3.011 | 7.000 | 137 |
| fatal_count | 39,413 | 0 | 0.000 | 0.072 | 0.000 | 6 |
| serious_count | 39,413 | 0 | 0.000 | 0.606 | 2.000 | 29 |
| predicted_xgb | 39,413 | 0.242 | 0.328 | 0.421 | 0.577 | 17.602 |
| predicted_glm | 39,413 | 0.019 | 1.523 | 1.649 | 2.553 | 11.058 |

## Top Examples

| risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | estimated_aadt | link_length_km | collision_count | predicted_xgb | risk_percentile | is_motorway | low_exposure_flag | sparse_collision_history_flag | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 39,171.800 | 10.633 | 137 | 17.602 | 100.000 | 1 | 0 | 0 | -2.397 | 53.252 |
| 2 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 31,557.000 | 16.221 | 90 | 17.405 | 100.000 | 1 | 0 | 0 | -1.188 | 52.526 |
| 3 | C88EE264-D645-4EEB-B759-332F064347E4 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 45,836.700 | 8.959 | 69 | 17.056 | 100.000 | 1 | 0 | 0 | -2.209 | 52.935 |
| 4 | BBB307EC-410E-4741-B22C-9DE761845549 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 31,522.600 | 16.045 | 57 | 15.489 | 100.000 | 1 | 0 | 0 | -1.390 | 52.130 |
| 5 | CD5E5752-A199-46E0-A8E6-BF680BE4D1E3 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 49,892.400 | 4.846 | 85 | 14.472 | 100.000 | 1 | 0 | 0 | -2.028 | 52.612 |
| 6 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 61,859.400 | 7.765 | 104 | 14.002 | 100.000 | 1 | 0 | 0 | -2.752 | 53.289 |
| 7 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 33,596.500 | 11.595 | 110 | 13.733 | 100.000 | 1 | 0 | 0 | -1.333 | 52.427 |
| 8 | 16B613FC-2995-42B1-83E0-AC7F83065EEC | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 35,733.300 | 13.866 | 85 | 13.166 | 100.000 | 1 | 0 | 0 | -1.698 | 52.302 |
| 9 | 151C3468-CD42-4DC9-9DB4-0B03FE374503 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 61,454.500 | 6.820 | 59 | 13.094 | 100.000 | 1 | 0 | 0 | -2.687 | 53.664 |
| 10 | F454DAB1-296B-4FDB-8F67-2FA30FF33EBD | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 50,646.300 | 6.419 | 77 | 13.072 | 100.000 | 1 | 0 | 0 | -2.462 | 53.329 |
| 11 | 0E4A9C14-C13E-4F70-9A16-6306AE5D3296 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 39,512.400 | 10.689 | 46 | 12.631 | 100.000 | 1 | 0 | 0 | -1.595 | 52.646 |
| 12 | BF145B8F-DF6F-4D8F-88E4-3943C5A72A44 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 44,387.600 | 7.469 | 73 | 12.444 | 100.000 | 1 | 0 | 0 | -2.101 | 52.728 |
| 13 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 42,921.300 | 8.304 | 107 | 12.427 | 100.000 | 1 | 0 | 0 | -1.205 | 53.456 |
| 14 | AAEFE2E4-F785-4CFB-B265-0424D640F2F2 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 31,437.500 | 10.957 | 78 | 12.170 | 100.000 | 1 | 0 | 0 | -1.076 | 52.262 |
| 15 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 50,210.900 | 5.266 | 93 | 11.832 | 100.000 | 1 | 0 | 0 | -2.366 | 53.177 |
| 16 | 756626D6-5192-44E6-90B9-292B3A15D742 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 47,041.700 | 8.115 | 32 | 11.502 | 100.000 | 1 | 0 | 0 | -1.259 | 52.662 |
| 17 | A0E0E728-BB7C-4FAD-93A3-30DDA7DE2974 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 47,681.400 | 8.214 | 72 | 11.406 | 100.000 | 1 | 0 | 0 | -2.135 | 52.251 |
| 18 | 41A19ED6-5441-400A-8F13-095A42A69E0B | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 54,950.200 | 7.485 | 49 | 11.357 | 100.000 | 1 | 0 | 0 | -2.430 | 53.455 |
| 19 | 218B87AC-FEC7-46FA-8088-37A0CE992738 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 26,219.200 | 12.371 | 59 | 10.866 | 100.000 | 1 | 0 | 0 | -0.775 | 53.755 |
| 20 | BAB55927-2103-4F9F-8EB8-5E16536ABC13 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 29,161.900 | 12.147 | 42 | 10.766 | 100.000 | 1 | 0 | 0 | -2.824 | 54.749 |

## Caveats

- This is a triage and screening output, not causal proof.
- Motorway calibration remains a known caveat.
- Sparse collision histories should be interpreted cautiously.
- This does not replace engineering audit or iRAP-style assessment.

## Next Use

This output can feed a Streamlit map, GeoPackage export, or stakeholder demo.
