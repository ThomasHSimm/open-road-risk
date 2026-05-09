# Top 1% Highest-Risk Road Segments

## Purpose

This table lists the top 1% highest-risk road links after controlling for traffic exposure. It is intended for inspection, mapping, portfolio review, and demo use.

## Method

- Ranking field used: `risk_percentile_eb`.
- EB-adjusted ranking used: yes.
- Top 1% definition: sorted all 2,167,557 scored links by `risk_percentile_eb` descending, with `link_id` as a deterministic tie-break, then selected the first 21,676 rows (1%).
- Created at: `2026-05-08T22:17:53+00:00`.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores_eb.parquet | 2026-05-08T22:13:34.224788+00:00 | 205,672,672 |
| data/processed/shapefiles/openroads.parquet | 2026-04-29T00:35:29.349109+00:00 | 392,911,115 |
| data/features/network_features.parquet | 2026-05-01T17:28:10.710235+00:00 | 213,584,936 |

Project/model output version: `0.1.0`.

## Count By Road Family

| family | count | share |
| --- | --- | --- |
| other_urban | 15,873 | 73.2% |
| other_rural | 2,049 | 9.5% |
| trunk_a | 1,467 | 6.8% |
| other_unknown | 1,314 | 6.1% |
| motorway | 973 | 4.5% |

## Count By Road Classification

| road_classification | count | share |
| --- | --- | --- |
| A Road | 13,264 | 61.2% |
| B Road | 3,035 | 14.0% |
| Classified Unnumbered | 2,569 | 11.9% |
| Unclassified | 1,710 | 7.9% |
| Motorway | 973 | 4.5% |
| Unknown | 116 | 0.5% |
| Not Classified | 9 | 0.0% |

## Count By Urban/Rural

| ruc_urban_rural | count | share |
| --- | --- | --- |
| Urban | 17,288 | 79.8% |
| Rural | 2,672 | 12.3% |
| Unknown | 1,716 | 7.9% |

## Count By Road Archetype

| road_archetype | count | share |
| --- | --- | --- |
| urban_a_road | 9,479 | 43.7% |
| urban_minor | 4,035 | 18.6% |
| urban_b_road | 2,359 | 10.9% |
| trunk_a | 1,467 | 6.8% |
| rural_a_road | 1,398 | 6.4% |
| other_unknown | 1,314 | 6.1% |
| motorway | 973 | 4.5% |
| rural_b_road | 383 | 1.8% |
| rural_minor | 268 | 1.2% |

## Numeric Summary

| field | n | min | median | mean | p90 | max |
| --- | --- | --- | --- | --- | --- | --- |
| estimated_aadt | 21,676 | 298.200 | 12,379.200 | 13,736.866 | 22,997.450 | 122,681.700 |
| link_length_km | 21,676 | 0.001 | 0.171 | 0.427 | 1.031 | 16.221 |
| collision_count | 21,676 | 3 | 5.000 | 6.666 | 10.000 | 136 |
| fatal_count | 21,676 | 0 | 0.000 | 0.130 | 1.000 | 6 |
| serious_count | 21,676 | 0 | 1.000 | 1.289 | 3.000 | 29 |
| predicted_eb | 21,676 | 0.322 | 0.469 | 0.602 | 0.925 | 13.594 |
| predicted_xgb | 21,676 | 0.010 | 0.190 | 0.280 | 0.463 | 11.112 |
| predicted_glm | 21,676 | 0.015 | 0.572 | 0.716 | 1.335 | 7.750 |

## Top Examples

| risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | risk_percentile | is_motorway | low_exposure_flag | sparse_collision_history_flag | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 60,783.200 | 10.633 | 136 | 13.594 | 11.112 | 100.000 | 100.000 | 1 | 0 | 0 | -2.397 | 53.252 |
| 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 89,230.000 | 4.910 | 129 | 12.884 | 8.360 | 100.000 | 100.000 | 1 | 0 | 0 | -1.686 | 53.744 |
| 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 78,308.800 | 5.066 | 123 | 12.259 | 5.063 | 100.000 | 99.998 | 1 | 0 | 0 | -1.826 | 52.507 |
| 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 48,140.500 | 8.245 | 119 | 11.845 | 4.072 | 100.000 | 99.997 | 1 | 0 | 0 | -1.611 | 52.469 |
| 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 48,862.600 | 11.595 | 110 | 10.994 | 9.044 | 100.000 | 100.000 | 1 | 0 | 0 | -1.333 | 52.427 |
| 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 55,438.900 | 8.304 | 107 | 10.683 | 6.724 | 100.000 | 99.999 | 1 | 0 | 0 | -1.205 | 53.456 |
| 7 | EEDCD4A3-3046-4C4E-8DAE-2DF46525E19F | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 61,259.400 | 7.339 | 105 | 10.480 | 6.166 | 100.000 | 99.999 | 1 | 0 | 0 | -2.339 | 53.104 |
| 8 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 71,928.400 | 7.765 | 104 | 10.383 | 6.527 | 100.000 | 99.999 | 1 | 0 | 0 | -2.752 | 53.289 |
| 9 | D4178A17-E84A-4B2E-8904-3052B12EBCED | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 57,746.100 | 8.182 | 94 | 9.383 | 5.864 | 100.000 | 99.999 | 1 | 0 | 0 | -1.685 | 52.573 |
| 10 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 72,431.700 | 5.266 | 93 | 9.271 | 4.659 | 100.000 | 99.998 | 1 | 0 | 0 | -2.366 | 53.177 |
| 11 | F8DAA031-5405-495A-BF94-995E345CDC1A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 64,225.800 | 7.817 | 92 | 9.187 | 6.273 | 100.000 | 99.999 | 1 | 0 | 0 | -2.597 | 53.636 |
| 12 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 51,867.300 | 16.221 | 90 | 9.002 | 9.692 | 99.999 | 100.000 | 1 | 0 | 0 | -1.188 | 52.526 |
| 13 | 1C2CFBA6-441D-4A61-A277-DA84E8F445FF | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 93,118.300 | 5.393 | 88 | 8.793 | 7.179 | 99.999 | 100.000 | 1 | 0 | 0 | -1.792 | 53.681 |
| 14 | CD5E5752-A199-46E0-A8E6-BF680BE4D1E3 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 68,203.100 | 4.846 | 87 | 8.681 | 5.250 | 99.999 | 99.998 | 1 | 0 | 0 | -2.028 | 52.612 |
| 15 | 781B41A8-2D3E-4304-BD4E-20A334272872 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 74,690.600 | 3.124 | 87 | 8.640 | 2.816 | 99.999 | 99.993 | 1 | 0 | 0 | -1.884 | 52.524 |
| 16 | 16B613FC-2995-42B1-83E0-AC7F83065EEC | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 44,571.800 | 13.866 | 85 | 8.495 | 7.301 | 99.999 | 100.000 | 1 | 0 | 0 | -1.698 | 52.302 |
| 17 | BE3BBEEB-2ED2-4869-8421-A6836514AE3A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 57,392.100 | 9.200 | 81 | 8.063 | 3.535 | 99.999 | 99.996 | 1 | 0 | 0 | -2.753 | 53.919 |
| 18 | AAEFE2E4-F785-4CFB-B265-0424D640F2F2 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 40,420.200 | 10.957 | 78 | 7.787 | 5.418 | 99.999 | 99.999 | 1 | 0 | 0 | -1.076 | 52.262 |
| 19 | F454DAB1-296B-4FDB-8F67-2FA30FF33EBD | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 72,945.800 | 6.419 | 77 | 7.686 | 5.133 | 99.999 | 99.998 | 1 | 0 | 0 | -2.462 | 53.329 |
| 20 | BF145B8F-DF6F-4D8F-88E4-3943C5A72A44 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 70,388.000 | 7.469 | 73 | 7.294 | 6.048 | 99.999 | 99.999 | 1 | 0 | 0 | -2.101 | 52.728 |

## Caveats

- This is a triage and screening output, not causal proof.
- Motorway calibration remains a known caveat.
- Sparse collision histories should be interpreted cautiously.
- This does not replace engineering audit or iRAP-style assessment.

## Next Use

This output can feed a Streamlit map, GeoPackage export, or stakeholder demo.
