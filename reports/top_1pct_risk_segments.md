# Top 1% Highest-Risk Road Segments

## Purpose

This table lists the top 1% highest-risk road links after controlling for traffic exposure. It is intended for inspection, mapping, portfolio review, and demo use.

## Method

- Ranking field used: `risk_percentile`.
- EB-adjusted ranking used: no.
- Top 1% definition: sorted all 2,167,557 scored links by `risk_percentile` descending, with `link_id` as a deterministic tie-break, then selected the first 21,676 rows (1%).
- Created at: `2026-07-01T18:43:26+00:00`.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores.parquet | 2026-07-01T00:45:59.477722+00:00 | 151,405,508 |
| data/processed/shapefiles/openroads.parquet | 2026-04-29T00:35:29.349109+00:00 | 392,911,115 |
| data/features/network_features.parquet | 2026-06-30T23:35:35.810308+00:00 | 223,068,149 |

Project/model output version: `0.1.0`.

## Count By Road Family

| family | count | share |
| --- | --- | --- |
| other_urban | 14,405 | 66.5% |
| other_rural | 4,063 | 18.7% |
| trunk_a | 1,824 | 8.4% |
| motorway | 1,381 | 6.4% |
| other_unknown | 3 | 0.0% |

## Count By Road Classification

| road_classification | count | share |
| --- | --- | --- |
| A Road | 16,064 | 74.1% |
| B Road | 2,256 | 10.4% |
| Classified Unnumbered | 1,735 | 8.0% |
| Motorway | 1,381 | 6.4% |
| Unclassified | 232 | 1.1% |
| Unknown | 8 | 0.0% |

## Count By Urban/Rural

| ruc_urban_rural | count | share |
| --- | --- | --- |
| Urban | 16,138 | 74.5% |
| Rural | 5,535 | 25.5% |
| Unknown | 3 | 0.0% |

## Count By Road Archetype

| road_archetype | count | share |
| --- | --- | --- |
| urban_a_road | 10,736 | 49.5% |
| rural_a_road | 3,501 | 16.2% |
| urban_minor | 1,866 | 8.6% |
| trunk_a | 1,824 | 8.4% |
| urban_b_road | 1,803 | 8.3% |
| motorway | 1,381 | 6.4% |
| rural_b_road | 453 | 2.1% |
| rural_minor | 109 | 0.5% |
| other_unknown | 3 | 0.0% |

## Numeric Summary

| field | n | min | median | mean | p90 | max |
| --- | --- | --- | --- | --- | --- | --- |
| estimated_aadt | 21,676 | 671.700 | 15,147.300 | 17,680.904 | 27,546.200 | 122,681.700 |
| link_length_km | 21,676 | 0.003 | 0.282 | 0.572 | 1.260 | 17.230 |
| collision_count | 21,676 | 0 | 3.000 | 4.009 | 9.000 | 135 |
| fatal_count | 21,676 | 0 | 0.000 | 0.104 | 0.000 | 6 |
| serious_count | 21,676 | 0 | 0.000 | 0.808 | 2.000 | 29 |
| predicted_xgb | 21,676 | 0.230 | 0.299 | 0.391 | 0.524 | 9.823 |
| predicted_glm | 21,676 | 0.010 | 1.268 | 1.397 | 2.144 | 6.856 |

## Top Examples

| risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | estimated_aadt | link_length_km | collision_count | predicted_xgb | risk_percentile | is_motorway | low_exposure_flag | sparse_collision_history_flag | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 60,783.200 | 10.633 | 135 | 9.823 | 100.000 | 1 | 0 | 0 | -2.397 | 53.252 |
| 2 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 51,867.300 | 16.221 | 90 | 9.789 | 100.000 | 1 | 0 | 0 | -1.188 | 52.526 |
| 3 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 48,862.600 | 11.595 | 111 | 8.231 | 100.000 | 1 | 0 | 0 | -1.333 | 52.427 |
| 4 | BBB307EC-410E-4741-B22C-9DE761845549 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 44,108.600 | 16.045 | 57 | 7.986 | 100.000 | 1 | 0 | 0 | -1.390 | 52.130 |
| 5 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 89,230.000 | 4.910 | 129 | 7.944 | 100.000 | 1 | 0 | 0 | -1.686 | 53.744 |
| 6 | F5E342B6-EE33-4F30-92BD-1A5670B41BE4 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 97,711.900 | 6.021 | 30 | 7.931 | 100.000 | 1 | 0 | 0 | -1.304 | 52.884 |
| 7 | 41A19ED6-5441-400A-8F13-095A42A69E0B | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 89,308.900 | 7.485 | 49 | 7.662 | 100.000 | 1 | 0 | 0 | -2.430 | 53.455 |
| 8 | 1C2CFBA6-441D-4A61-A277-DA84E8F445FF | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 93,118.300 | 5.393 | 87 | 7.371 | 100.000 | 1 | 0 | 0 | -1.792 | 53.681 |
| 9 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 78,308.800 | 5.066 | 122 | 7.308 | 100.000 | 1 | 0 | 0 | -1.826 | 52.507 |
| 10 | C88EE264-D645-4EEB-B759-332F064347E4 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 66,244.800 | 8.959 | 69 | 7.299 | 100.000 | 1 | 0 | 0 | -2.209 | 52.935 |
| 11 | 151C3468-CD42-4DC9-9DB4-0B03FE374503 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 83,798.900 | 6.820 | 59 | 7.231 | 100.000 | 1 | 0 | 0 | -2.687 | 53.664 |
| 12 | 0E4A9C14-C13E-4F70-9A16-6306AE5D3296 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 56,597.700 | 10.689 | 46 | 7.138 | 99.999 | 1 | 0 | 0 | -1.595 | 52.646 |
| 13 | BF145B8F-DF6F-4D8F-88E4-3943C5A72A44 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 70,388.000 | 7.469 | 73 | 7.072 | 99.999 | 1 | 0 | 0 | -2.101 | 52.728 |
| 14 | 07E13017-66B1-462C-8A91-6171375AF51C | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 87,737.700 | 7.704 | 50 | 6.923 | 99.999 | 1 | 0 | 0 | -1.246 | 53.027 |
| 15 | A9B8EF1C-FC42-4E4B-9DFB-8C218F5D2FDB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 47,498.300 | 10.771 | 32 | 6.817 | 99.999 | 1 | 0 | 0 | -1.104 | 53.436 |
| 16 | 16B613FC-2995-42B1-83E0-AC7F83065EEC | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 44,571.800 | 13.866 | 84 | 6.740 | 99.999 | 1 | 0 | 0 | -1.698 | 52.302 |
| 17 | 756626D6-5192-44E6-90B9-292B3A15D742 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 61,267.000 | 8.115 | 33 | 6.727 | 99.999 | 1 | 0 | 0 | -1.259 | 52.662 |
| 18 | CD5E5752-A199-46E0-A8E6-BF680BE4D1E3 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 68,203.100 | 4.846 | 86 | 6.686 | 99.999 | 1 | 0 | 0 | -2.028 | 52.612 |
| 19 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 71,928.400 | 7.765 | 105 | 6.642 | 99.999 | 1 | 0 | 0 | -2.752 | 53.289 |
| 20 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 55,438.900 | 8.304 | 107 | 6.408 | 99.999 | 1 | 0 | 0 | -1.205 | 53.456 |

## Caveats

- This is a triage and screening output, not causal proof.
- Motorway calibration remains a known caveat.
- Sparse collision histories should be interpreted cautiously.
- This does not replace engineering audit or iRAP-style assessment.

## Next Use

This output can feed a Streamlit map, GeoPackage export, or stakeholder demo.
