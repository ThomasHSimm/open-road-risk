# Top 1% Highest-Risk Road Segments

## Purpose

This table lists the top 1% highest-risk road links after controlling for traffic exposure. It is intended for inspection, mapping, portfolio review, and demo use.

## Method

- Ranking field used: `risk_percentile_eb`.
- EB-adjusted ranking used: yes.
- Top 1% definition: sorted all 2,167,557 scored links by `risk_percentile_eb` descending, with `link_id` as a deterministic tie-break, then selected the first 21,676 rows (1%).
- Created at: `2026-05-06T20:56:05+00:00`.

## Provenance

| source | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores_eb.parquet | 2026-04-25T13:34:14.243889+00:00 | 215,745,466 |
| data/processed/shapefiles/openroads.parquet | 2026-04-29T00:35:29.349109+00:00 | 392,911,115 |
| data/features/network_features.parquet | 2026-05-01T17:28:10.710235+00:00 | 213,584,936 |

Project/model output version: `0.1.0`.

## Count By Road Family

| family | count | share |
| --- | --- | --- |
| other_urban | 16,439 | 75.8% |
| other_rural | 1,835 | 8.5% |
| trunk_a | 1,361 | 6.3% |
| other_unknown | 1,103 | 5.1% |
| motorway | 938 | 4.3% |

## Count By Road Classification

| road_classification | count | share |
| --- | --- | --- |
| A Road | 12,549 | 57.9% |
| B Road | 2,826 | 13.0% |
| Classified Unnumbered | 2,619 | 12.1% |
| Unclassified | 2,420 | 11.2% |
| Motorway | 938 | 4.3% |
| Unknown | 289 | 1.3% |
| Not Classified | 35 | 0.2% |

## Count By Urban/Rural

| ruc_urban_rural | count | share |
| --- | --- | --- |
| Urban | 17,796 | 82.1% |
| Rural | 2,400 | 11.1% |
| Unknown | 1,480 | 6.8% |

## Count By Road Archetype

| road_archetype | count | share |
| --- | --- | --- |
| urban_a_road | 9,189 | 42.4% |
| urban_minor | 4,965 | 22.9% |
| urban_b_road | 2,285 | 10.5% |
| trunk_a | 1,361 | 6.3% |
| rural_a_road | 1,233 | 5.7% |
| other_unknown | 1,103 | 5.1% |
| motorway | 938 | 4.3% |
| rural_b_road | 313 | 1.4% |
| rural_minor | 289 | 1.3% |

## Numeric Summary

| field | n | min | median | mean | p90 | max |
| --- | --- | --- | --- | --- | --- | --- |
| estimated_aadt | 21,676 | 240.300 | 12,394.750 | 12,749.278 | 21,247.200 | 100,311.500 |
| link_length_km | 21,676 | 0.001 | 0.154 | 0.399 | 0.970 | 16.221 |
| collision_count | 21,676 | 4 | 5.000 | 6.677 | 10.000 | 136 |
| fatal_count | 21,676 | 0 | 0.000 | 0.123 | 1.000 | 6 |
| serious_count | 21,676 | 0 | 1.000 | 1.282 | 3.000 | 29 |
| predicted_eb | 21,676 | 0.395 | 0.504 | 0.660 | 0.994 | 13.592 |
| predicted_xgb | 21,676 | 0.025 | 0.496 | 0.587 | 0.845 | 11.024 |
| predicted_glm | 21,676 | 0.006 | 0.478 | 0.605 | 1.167 | 7.643 |

## Top Examples

| risk_rank | link_id | road_classification | road_function | family | road_archetype | form_of_way | estimated_aadt | link_length_km | collision_count | predicted_eb | predicted_xgb | risk_percentile_eb | risk_percentile | is_motorway | low_exposure_flag | sparse_collision_history_flag | centroid_longitude | centroid_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 42,232.400 | 10.633 | 136 | 13.592 | 10.987 | 100.000 | 100.000 | 1 | 0 | 0 | -2.397 | 53.252 |
| 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 51,462.000 | 4.910 | 129 | 12.885 | 8.860 | 100.000 | 100.000 | 1 | 0 | 0 | -1.686 | 53.744 |
| 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 54,576.300 | 5.066 | 123 | 12.260 | 5.505 | 100.000 | 99.998 | 1 | 0 | 0 | -1.826 | 52.507 |
| 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 42,870.800 | 8.245 | 119 | 11.840 | 4.156 | 100.000 | 99.996 | 1 | 0 | 0 | -1.611 | 52.469 |
| 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 40,764.100 | 11.595 | 110 | 10.996 | 9.730 | 100.000 | 100.000 | 1 | 0 | 0 | -1.333 | 52.427 |
| 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 43,138.700 | 8.304 | 107 | 10.693 | 8.736 | 100.000 | 100.000 | 1 | 0 | 0 | -1.205 | 53.456 |
| 7 | EEDCD4A3-3046-4C4E-8DAE-2DF46525E19F | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 40,891.400 | 7.339 | 105 | 10.482 | 6.745 | 100.000 | 99.999 | 1 | 0 | 0 | -2.339 | 53.104 |
| 8 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 64,451.900 | 7.765 | 104 | 10.389 | 7.822 | 100.000 | 100.000 | 1 | 0 | 0 | -2.752 | 53.289 |
| 9 | D4178A17-E84A-4B2E-8904-3052B12EBCED | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 45,308.500 | 8.182 | 94 | 9.381 | 5.957 | 100.000 | 99.999 | 1 | 0 | 0 | -1.685 | 52.573 |
| 10 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 61,144.300 | 5.266 | 93 | 9.280 | 5.728 | 100.000 | 99.998 | 1 | 0 | 0 | -2.366 | 53.177 |
| 11 | F8DAA031-5405-495A-BF94-995E345CDC1A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 49,495.200 | 7.817 | 92 | 9.183 | 6.060 | 100.000 | 99.999 | 1 | 0 | 0 | -2.597 | 53.636 |
| 12 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 41,594.900 | 16.221 | 90 | 9.006 | 11.024 | 99.999 | 100.000 | 1 | 0 | 0 | -1.188 | 52.526 |
| 13 | 1C2CFBA6-441D-4A61-A277-DA84E8F445FF | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 73,567.600 | 5.393 | 88 | 8.789 | 6.581 | 99.999 | 99.999 | 1 | 0 | 0 | -1.792 | 53.681 |
| 14 | CD5E5752-A199-46E0-A8E6-BF680BE4D1E3 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 54,828.000 | 4.846 | 87 | 8.689 | 6.436 | 99.999 | 99.999 | 1 | 0 | 0 | -2.028 | 52.612 |
| 15 | 781B41A8-2D3E-4304-BD4E-20A334272872 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 62,404.800 | 3.124 | 87 | 8.625 | 2.599 | 99.999 | 99.991 | 1 | 0 | 0 | -1.884 | 52.524 |
| 16 | 16B613FC-2995-42B1-83E0-AC7F83065EEC | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 34,608.000 | 13.866 | 85 | 8.499 | 8.228 | 99.999 | 100.000 | 1 | 0 | 0 | -1.698 | 52.302 |
| 17 | BE3BBEEB-2ED2-4869-8421-A6836514AE3A | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 50,188.300 | 9.200 | 81 | 7.825 | 0.829 | 99.999 | 99.893 | 1 | 0 | 0 | -2.753 | 53.919 |
| 18 | AAEFE2E4-F785-4CFB-B265-0424D640F2F2 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 39,699.300 | 10.957 | 78 | 7.799 | 7.584 | 99.999 | 99.999 | 1 | 0 | 0 | -1.076 | 52.262 |
| 19 | F454DAB1-296B-4FDB-8F67-2FA30FF33EBD | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 61,735.700 | 6.419 | 77 | 7.695 | 6.628 | 99.999 | 99.999 | 1 | 0 | 0 | -2.462 | 53.329 |
| 20 | A0E0E728-BB7C-4FAD-93A3-30DDA7DE2974 | Motorway | Motorway | motorway | motorway | Collapsed Dual Carriageway | 49,724.900 | 8.214 | 73 | 7.302 | 7.779 | 99.999 | 100.000 | 1 | 0 | 0 | -2.135 | 52.251 |

## Caveats

- This is a triage and screening output, not causal proof.
- Motorway calibration remains a known caveat.
- Sparse collision histories should be interpreted cautiously.
- This does not replace engineering audit or iRAP-style assessment.

## Next Use

This output can feed a Streamlit map, GeoPackage export, or stakeholder demo.
