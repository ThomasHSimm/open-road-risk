# Top-Risk Output QA

Created at: `2026-05-08T22:25:31+00:00`.



## Purpose

This report checks the refreshed top-risk outputs generated from the May 4 production scores and the refreshed EB file. It is a QA/readiness report for the v0.1 screening output, not a model retrain or ranking-method change.



## Inputs And Provenance

| path | mtime_utc | size_bytes |
| --- | --- | --- |
| data/models/risk_scores_eb.parquet | 2026-05-08T22:13:34.224788+00:00 | 205,672,672 |
| data/models/risk_scores.parquet | 2026-05-04T10:04:39.444106+00:00 | 151,573,649 |
| data/outputs/top_1pct_risk_segments.parquet | 2026-05-08T22:17:58.631116+00:00 | 8,232,205 |
| data/outputs/top_risk_by_family.parquet | 2026-05-08T22:18:38.397915+00:00 | 368,679 |
| data/outputs/top_risk_by_road_class.parquet | 2026-05-08T22:18:38.404222+00:00 | 433,306 |
| data/outputs/top_risk_by_road_archetype.parquet | 2026-05-08T22:18:38.410603+00:00 | 553,377 |
| data/provenance/eb_dispersion_provenance.json | 2026-05-08T22:13:06.483625+00:00 | 19,379 |



## EB Refresh Context

- Current EB production k, positive-event weighted: `3.451158`.

- Previous stale positive-event weighted k: `3.074322`.

- Change from stale k: `12.3%`.

- Link-year weighted k: `14.898721`.

- Median retained-bin k: `7.573279`.

- Refreshed EB provenance timestamp: `2026-05-08T22:13:06.482558+00:00`.

- MoM aggregation sensitivity remains non-trivial but bounded for top-1 membership: positive-weighted vs link-year-weighted top-1 Jaccard was `0.954375`, about `4.6%` membership churn.



## Global Top 20 EB-Ranked Links

| risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | motorway | 60,783.2 | 136 | 13.594 | 100.000 | 10.633 |
| 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | motorway | 89,230.0 | 129 | 12.884 | 100.000 | 4.910 |
| 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | motorway | 78,308.8 | 123 | 12.259 | 100.000 | 5.066 |
| 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | motorway | 48,140.5 | 119 | 11.845 | 100.000 | 8.245 |
| 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | motorway | 48,862.6 | 110 | 10.994 | 100.000 | 11.595 |
| 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | motorway | 55,438.9 | 107 | 10.683 | 100.000 | 8.304 |
| 7 | EEDCD4A3-3046-4C4E-8DAE-2DF46525E19F | Motorway | motorway | 61,259.4 | 105 | 10.480 | 100.000 | 7.339 |
| 8 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | motorway | 71,928.4 | 104 | 10.383 | 100.000 | 7.765 |
| 9 | D4178A17-E84A-4B2E-8904-3052B12EBCED | Motorway | motorway | 57,746.1 | 94 | 9.383 | 100.000 | 8.182 |
| 10 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | motorway | 72,431.7 | 93 | 9.271 | 100.000 | 5.266 |
| 11 | F8DAA031-5405-495A-BF94-995E345CDC1A | Motorway | motorway | 64,225.8 | 92 | 9.187 | 100.000 | 7.817 |
| 12 | 77BE17EE-137D-4878-9924-01726CD60C0A | Motorway | motorway | 51,867.3 | 90 | 9.002 | 99.999 | 16.221 |
| 13 | 1C2CFBA6-441D-4A61-A277-DA84E8F445FF | Motorway | motorway | 93,118.3 | 88 | 8.793 | 99.999 | 5.393 |
| 14 | CD5E5752-A199-46E0-A8E6-BF680BE4D1E3 | Motorway | motorway | 68,203.1 | 87 | 8.681 | 99.999 | 4.846 |
| 15 | 781B41A8-2D3E-4304-BD4E-20A334272872 | Motorway | motorway | 74,690.6 | 87 | 8.640 | 99.999 | 3.124 |
| 16 | 16B613FC-2995-42B1-83E0-AC7F83065EEC | Motorway | motorway | 44,571.8 | 85 | 8.495 | 99.999 | 13.866 |
| 17 | BE3BBEEB-2ED2-4869-8421-A6836514AE3A | Motorway | motorway | 57,392.1 | 81 | 8.063 | 99.999 | 9.200 |
| 18 | AAEFE2E4-F785-4CFB-B265-0424D640F2F2 | Motorway | motorway | 40,420.2 | 78 | 7.787 | 99.999 | 10.957 |
| 19 | F454DAB1-296B-4FDB-8F67-2FA30FF33EBD | Motorway | motorway | 72,945.8 | 77 | 7.686 | 99.999 | 6.419 |
| 20 | BF145B8F-DF6F-4D8F-88E4-3943C5A72A44 | Motorway | motorway | 70,388.0 | 73 | 7.294 | 99.999 | 7.469 |



## Distribution Summaries

| field | count | mean | std | min | 1% | 5% | 25% | median | 75% | 95% | 99% | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| link_length_km | 21,676 | 0.427 | 0.798 | 0.001 | 0.008 | 0.028 | 0.082 | 0.171 | 0.460 | 1.487 | 3.630 | 16.221 |
| estimated_aadt | 21,676 | 13,736.866 | 12,013.361 | 298.200 | 1,002.750 | 1,833.050 | 6,290.825 | 12,379.200 | 16,923.625 | 29,367.025 | 72,166.425 | 122,681.700 |
| collision_count | 21,676 | 6.666 | 5.343 | 3.000 | 4.000 | 4.000 | 4.000 | 5.000 | 7.000 | 13.000 | 27.000 | 136.000 |
| predicted_eb | 21,676 | 0.602 | 0.528 | 0.322 | 0.325 | 0.338 | 0.381 | 0.469 | 0.639 | 1.214 | 2.625 | 13.594 |
| risk_percentile_eb | 21,676 | 99.500 | 0.289 | 99.000 | 99.010 | 99.050 | 99.250 | 99.500 | 99.750 | 99.950 | 99.990 | 100.000 |



## Composition Checks

### Count By Family

| family | count | share |
| --- | --- | --- |
| other_urban | 15,873 | 73.2 |
| other_rural | 2,049 | 9.5 |
| trunk_a | 1,467 | 6.8 |
| other_unknown | 1,314 | 6.1 |
| motorway | 973 | 4.5 |



### Count By Road Classification

| road_classification | count | share |
| --- | --- | --- |
| A Road | 13,264 | 61.2 |
| B Road | 3,035 | 14.0 |
| Classified Unnumbered | 2,569 | 11.9 |
| Unclassified | 1,710 | 7.9 |
| Motorway | 973 | 4.5 |
| Unknown | 116 | 0.5 |
| Not Classified | 9 | 0.0 |



### Count By Road Archetype

| road_archetype | count | share |
| --- | --- | --- |
| urban_a_road | 9,479 | 43.7 |
| urban_minor | 4,035 | 18.6 |
| urban_b_road | 2,359 | 10.9 |
| trunk_a | 1,467 | 6.8 |
| rural_a_road | 1,398 | 6.4 |
| other_unknown | 1,314 | 6.1 |
| motorway | 973 | 4.5 |
| rural_b_road | 383 | 1.8 |
| rural_minor | 268 | 1.2 |



## Outlier Flag Summary

| check | count |
| --- | --- |
| link_length_km < 0.05 | 2,505 |
| estimated_aadt < 500 | 12 |
| estimated_aadt > 150,000 | 0 |
| collision_count = 0 | 0 |
| predicted_eb > 3 SD above family mean | 460 |
| abs(predicted_eb z-score) > 3 within family | 460 |



## Suspicious Links For Later Manual Review

These rows are a small stratified sample, not an exhaustive list. They are not automatic failures; they are links where a mapper or analyst should inspect geometry, exposure assignment, segmentation, or EB behaviour before using them as showcase examples.

| review_reason | risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | predicted_eb_z_within_family | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| estimated_aadt < 500 | 2,392 | 11349F9F-BDA5-4723-A9C9-AA1D215AE6C1 | Classified Unnumbered | other_unknown | 483.8 | 10 | 0.883 | 1.29 | 3.682 |
| estimated_aadt < 500 | 2,960 | C2F14111-CB21-454D-92E6-29A045EA2632 | Classified Unnumbered | other_unknown | 487.4 | 12 | 0.817 | 1.04 | 2.690 |
| estimated_aadt < 500 | 4,341 | 886284B4-1653-4DDB-907F-3D8C6BF3EAEE | Unclassified | other_urban | 485.0 | 11 | 0.693 | 0.53 | 0.140 |
| estimated_aadt < 500 | 9,838 | C5B854D0-AC80-4A80-921A-1A71F4A00DC7 | Classified Unnumbered | other_unknown | 467.6 | 6 | 0.485 | -0.22 | 2.287 |
| estimated_aadt < 500 | 11,444 | 0C5D66DE-9F22-4E14-83AB-BDEDE2DF92F0 | Unclassified | other_unknown | 384.6 | 7 | 0.460 | -0.31 | 6.034 |
| estimated_aadt < 500 | 12,464 | 18BCC635-CD0D-43FF-BB61-0AAE1C62E079 | Classified Unnumbered | other_rural | 481.6 | 6 | 0.439 | -0.35 | 0.905 |
| estimated_aadt < 500 | 15,582 | 0E5B30F4-C8BC-46F8-9364-50D88A8B8A24 | Classified Unnumbered | other_rural | 418.2 | 5 | 0.387 | -0.60 | 1.110 |
| estimated_aadt < 500 | 15,689 | 7A15AA50-9A20-4E5B-B73D-369BDB71A5E4 | Classified Unnumbered | other_unknown | 442.8 | 5 | 0.386 | -0.59 | 1.796 |
| predicted_eb > 3 SD within family | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | motorway | 60,783.2 | 136 | 13.594 | 6.66 | 10.633 |
| predicted_eb > 3 SD within family | 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | motorway | 89,230.0 | 129 | 12.884 | 6.27 | 4.910 |
| predicted_eb > 3 SD within family | 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | motorway | 78,308.8 | 123 | 12.259 | 5.92 | 5.066 |
| predicted_eb > 3 SD within family | 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | motorway | 48,140.5 | 119 | 11.845 | 5.70 | 8.245 |
| predicted_eb > 3 SD within family | 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | motorway | 48,862.6 | 110 | 10.994 | 5.23 | 11.595 |
| predicted_eb > 3 SD within family | 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | motorway | 55,438.9 | 107 | 10.683 | 5.06 | 8.304 |
| short link < 50m | 152 | 65ECF41C-0895-4918-B54F-64EB0FCFBB15 | A Road | other_urban | 15,155.9 | 33 | 3.063 | 9.17 | 0.009 |
| short link < 50m | 244 | 004CAA81-DABC-4704-8BA6-18A319BECB28 | A Road | other_urban | 14,250.8 | 28 | 2.467 | 7.00 | 0.015 |
| short link < 50m | 246 | D9D6490D-28C0-41C5-9B1F-DADDDDC1CBE0 | A Road | other_urban | 14,767.1 | 27 | 2.425 | 6.85 | 0.015 |
| short link < 50m | 269 | 58AF7081-C5FF-4239-8D5B-CEC477724409 | Unknown | other_urban | 1,984.0 | 28 | 2.316 | 6.45 | 0.009 |
| short link < 50m | 339 | DD586BC0-668B-4CC8-AA80-3A0BE2A6AD99 | A Road | other_urban | 35,374.1 | 21 | 2.044 | 5.46 | 0.026 |
| short link < 50m | 368 | BCD70817-00FF-45F7-88F1-A1C44A15BC85 | A Road | other_urban | 12,064.0 | 25 | 1.956 | 5.13 | 0.031 |
| short link < 50m | 410 | 3F39400B-5676-4A5B-9402-4A147AA9128F | A Road | other_urban | 19,078.9 | 21 | 1.857 | 4.77 | 0.023 |
| short link < 50m | 458 | 2DABCE0D-8B14-413E-ADB8-F5A0FF3301E5 | A Road | other_urban | 16,061.6 | 20 | 1.755 | 4.40 | 0.006 |

## Motorway Share Check

- Motorway-family links in the global top 1%: `973` of `21,676` (`4.5%`).

- This is not dominant in the full top-1% output, but motorways still dominate the very top examples because long, high-volume motorway links with many observed collisions remain high under EB.

- This is explainable for a screening output, but should be shown with the existing motorway calibration caveat rather than framed as final engineering prioritisation.



## Top Non-Motorway Spot Check

| risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 30 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | trunk_a | 35,033.0 | 64 | 6.382 | 99.999 | 2.097 |
| 49 | F92239D4-36BC-45FF-8B98-7B4FF2CF81C0 | A Road | trunk_a | 16,257.8 | 58 | 5.300 | 99.998 | 0.056 |
| 54 | F8C83919-A991-4C0F-980E-148BFB912405 | A Road | trunk_a | 11,865.3 | 52 | 5.143 | 99.998 | 8.549 |
| 61 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | trunk_a | 13,767.6 | 49 | 4.889 | 99.997 | 11.654 |
| 74 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | trunk_a | 15,917.4 | 45 | 4.468 | 99.997 | 6.793 |
| 75 | 43BC8837-2592-43A6-89FF-6762DCC1611D | A Road | trunk_a | 26,908.6 | 45 | 4.446 | 99.997 | 2.791 |
| 84 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | trunk_a | 34,088.9 | 42 | 4.189 | 99.996 | 4.039 |
| 94 | A8CF56A0-06EA-4E02-82B5-8D7B18189D7F | A Road | trunk_a | 11,047.8 | 41 | 4.015 | 99.996 | 2.554 |
| 95 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | trunk_a | 31,033.9 | 40 | 3.999 | 99.996 | 7.489 |
| 96 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | trunk_a | 21,475.0 | 40 | 3.988 | 99.996 | 7.408 |
| 102 | 980A4752-91AD-4B78-8D85-FC7BC10F4106 | A Road | trunk_a | 32,780.3 | 38 | 3.800 | 99.995 | 6.140 |
| 105 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | other_urban | 29,499.6 | 38 | 3.771 | 99.995 | 3.374 |



Narrative spot check: the highest non-motorway rows are mostly A-road/trunk or urban major-road examples with substantial observed collision histories. In the top 20 non-motorway rows, collision counts range from `35` to a median of `39.0`, and AADT ranges from `11,047.8` to `40,366.9`. That looks plausible for a screening layer, provided it is not read as causal proof or a substitute for site audit.



## Top 10 Per Family

### Family: motorway

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | motorway | 60,783.2 | 136 | 13.594 | 100.000 | 10.633 |
| 2 | 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | motorway | 89,230.0 | 129 | 12.884 | 100.000 | 4.910 |
| 3 | 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | motorway | 78,308.8 | 123 | 12.259 | 100.000 | 5.066 |
| 4 | 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | motorway | 48,140.5 | 119 | 11.845 | 100.000 | 8.245 |
| 5 | 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | motorway | 48,862.6 | 110 | 10.994 | 100.000 | 11.595 |
| 6 | 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | motorway | 55,438.9 | 107 | 10.683 | 100.000 | 8.304 |
| 7 | 7 | EEDCD4A3-3046-4C4E-8DAE-2DF46525E19F | Motorway | motorway | 61,259.4 | 105 | 10.480 | 100.000 | 7.339 |
| 8 | 8 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | motorway | 71,928.4 | 104 | 10.383 | 100.000 | 7.765 |
| 9 | 9 | D4178A17-E84A-4B2E-8904-3052B12EBCED | Motorway | motorway | 57,746.1 | 94 | 9.383 | 100.000 | 8.182 |
| 10 | 10 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | motorway | 72,431.7 | 93 | 9.271 | 100.000 | 5.266 |

### Family: other_rural

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 231 | 6EA22486-59DA-4A1F-A503-6FE157C1B266 | Classified Unnumbered | other_rural | 590.4 | 31 | 2.536 | 99.989 | 2.228 |
| 2 | 311 | 4F7AA121-68AC-4F36-A483-DB2CC1A64202 | A Road | other_rural | 7,657.9 | 22 | 2.179 | 99.986 | 4.065 |
| 3 | 329 | E5412A99-F27C-4D22-A253-FF9DA03A6AD1 | A Road | other_rural | 16,058.2 | 22 | 2.085 | 99.985 | 1.304 |
| 4 | 382 | 75075385-9C0E-4B5C-8119-957239230DFC | A Road | other_rural | 7,440.8 | 21 | 1.908 | 99.982 | 1.048 |
| 5 | 528 | 6E9A0C83-DE15-47D7-B49A-B6E7C3390390 | Classified Unnumbered | other_rural | 3,222.2 | 19 | 1.636 | 99.976 | 0.273 |
| 6 | 542 | BA68C73F-4D0A-42FE-9D79-8BB47C55C9B4 | A Road | other_rural | 12,405.0 | 17 | 1.614 | 99.975 | 0.637 |
| 7 | 554 | E56501E8-3ACB-46DD-B6B1-397BF24F3499 | A Road | other_rural | 11,919.3 | 16 | 1.601 | 99.974 | 4.878 |
| 8 | 600 | 7029D21C-8EDD-4FB4-B958-58AF901A9EDF | A Road | other_rural | 8,215.2 | 16 | 1.542 | 99.972 | 2.589 |
| 9 | 607 | 195A6448-2614-4A63-BA21-2271C0708C3D | A Road | other_rural | 10,884.0 | 16 | 1.533 | 99.972 | 0.861 |
| 10 | 619 | F8EB83E6-E75C-47BB-86BF-6C1FAB5C1B4E | A Road | other_rural | 14,129.2 | 17 | 1.520 | 99.971 | 0.619 |

### Family: other_unknown

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 196 | 4158BCEE-7926-475E-9CCF-F464B6F8E137 | A Road | other_unknown | 3,649.2 | 29 | 2.783 | 99.991 | 7.573 |
| 2 | 241 | 7BF88232-B992-4162-8A4F-691D46F186E7 | A Road | other_unknown | 10,514.2 | 25 | 2.478 | 99.989 | 4.288 |
| 3 | 286 | 1942361E-5A0E-4926-B8F2-AAC3EB2AB46A | A Road | other_unknown | 6,234.7 | 23 | 2.233 | 99.987 | 2.647 |
| 4 | 291 | 36FB8B57-4494-4469-95CE-D46C9A54FF23 | A Road | other_unknown | 5,587.6 | 24 | 2.220 | 99.987 | 2.710 |
| 5 | 364 | B303D610-A520-4619-81E3-3AA9ED7BDDA9 | A Road | other_unknown | 7,524.0 | 20 | 1.965 | 99.983 | 3.422 |
| 6 | 373 | D98C3D9A-C954-4A9D-AE6C-1B7A54D8495F | A Road | other_unknown | 6,911.0 | 20 | 1.942 | 99.983 | 2.503 |
| 7 | 409 | 40DDE02A-7B4B-4BD4-9BBD-E8437DFF6A64 | A Road | other_unknown | 5,215.2 | 20 | 1.857 | 99.981 | 0.849 |
| 8 | 424 | 65825479-8993-4C9B-8E0F-492D499B0870 | A Road | other_unknown | 8,401.2 | 20 | 1.826 | 99.980 | 0.791 |
| 9 | 437 | A7516B09-B4F0-4906-947F-2ED4B3CF0821 | A Road | other_unknown | 19,848.0 | 18 | 1.796 | 99.980 | 4.445 |
| 10 | 495 | DF3B328C-54DE-44DC-BB3B-01EF9BD66434 | A Road | other_unknown | 5,865.3 | 18 | 1.690 | 99.977 | 2.904 |

### Family: other_urban

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 105 | 07DE5B08-8356-4B4C-AFC4-5D54ED87B47D | A Road | other_urban | 29,499.6 | 38 | 3.771 | 99.995 | 3.374 |
| 2 | 115 | 1C5FCE8A-EB04-48CF-A2C7-79E66C780A0F | A Road | other_urban | 27,669.1 | 37 | 3.649 | 99.995 | 2.615 |
| 3 | 129 | BFB5EAAC-3BE4-4B03-B0BF-654BB6A871F3 | A Road | other_urban | 13,667.1 | 35 | 3.365 | 99.994 | 0.197 |
| 4 | 139 | 16D5C305-8230-4568-A0C5-F8146A963EA6 | A Road | other_urban | 34,918.7 | 33 | 3.187 | 99.994 | 0.836 |
| 5 | 142 | 7E67F595-0DA0-491F-A17C-2496A75EF427 | A Road | other_urban | 27,906.3 | 32 | 3.170 | 99.993 | 3.517 |
| 6 | 146 | 63B62281-35C8-4F62-B760-B6949F51ED5C | A Road | other_urban | 14,092.1 | 33 | 3.128 | 99.993 | 0.089 |
| 7 | 152 | 65ECF41C-0895-4918-B54F-64EB0FCFBB15 | A Road | other_urban | 15,155.9 | 33 | 3.063 | 99.993 | 0.009 |
| 8 | 154 | EEF807BC-30B7-480F-855A-3C86F95040C8 | A Road | other_urban | 29,486.0 | 31 | 3.060 | 99.993 | 1.738 |
| 9 | 155 | 35598324-6978-48F4-BCB9-33DC32D6B118 | A Road | other_urban | 9,143.7 | 37 | 3.036 | 99.993 | 0.251 |
| 10 | 156 | 0824FEC1-4845-433E-BB69-AEDB8F1633D1 | A Road | other_urban | 16,603.0 | 32 | 3.023 | 99.993 | 0.235 |

### Family: trunk_a

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 30 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | trunk_a | 35,033.0 | 64 | 6.382 | 99.999 | 2.097 |
| 2 | 49 | F92239D4-36BC-45FF-8B98-7B4FF2CF81C0 | A Road | trunk_a | 16,257.8 | 58 | 5.300 | 99.998 | 0.056 |
| 3 | 54 | F8C83919-A991-4C0F-980E-148BFB912405 | A Road | trunk_a | 11,865.3 | 52 | 5.143 | 99.998 | 8.549 |
| 4 | 61 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | trunk_a | 13,767.6 | 49 | 4.889 | 99.997 | 11.654 |
| 5 | 74 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | trunk_a | 15,917.4 | 45 | 4.468 | 99.997 | 6.793 |
| 6 | 75 | 43BC8837-2592-43A6-89FF-6762DCC1611D | A Road | trunk_a | 26,908.6 | 45 | 4.446 | 99.997 | 2.791 |
| 7 | 84 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | trunk_a | 34,088.9 | 42 | 4.189 | 99.996 | 4.039 |
| 8 | 94 | A8CF56A0-06EA-4E02-82B5-8D7B18189D7F | A Road | trunk_a | 11,047.8 | 41 | 4.015 | 99.996 | 2.554 |
| 9 | 95 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | trunk_a | 31,033.9 | 40 | 3.999 | 99.996 | 7.489 |
| 10 | 96 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | trunk_a | 21,475.0 | 40 | 3.988 | 99.996 | 7.408 |



## Top 10 Per Road Classification

### Road classification: A Road

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 30 | 34BADB00-8728-4B0B-B6F6-B9B345697BFB | A Road | trunk_a | 35,033.0 | 64 | 6.382 | 99.999 | 2.097 |
| 2 | 49 | F92239D4-36BC-45FF-8B98-7B4FF2CF81C0 | A Road | trunk_a | 16,257.8 | 58 | 5.300 | 99.998 | 0.056 |
| 3 | 54 | F8C83919-A991-4C0F-980E-148BFB912405 | A Road | trunk_a | 11,865.3 | 52 | 5.143 | 99.998 | 8.549 |
| 4 | 61 | 207F717C-C2B2-4F2E-B941-B630910E47E6 | A Road | trunk_a | 13,767.6 | 49 | 4.889 | 99.997 | 11.654 |
| 5 | 74 | 6EE4A050-5EED-45D1-847E-3F6CD0D237C2 | A Road | trunk_a | 15,917.4 | 45 | 4.468 | 99.997 | 6.793 |
| 6 | 75 | 43BC8837-2592-43A6-89FF-6762DCC1611D | A Road | trunk_a | 26,908.6 | 45 | 4.446 | 99.997 | 2.791 |
| 7 | 84 | FDF6363C-95EA-40F6-9DCF-87DAC74DC92F | A Road | trunk_a | 34,088.9 | 42 | 4.189 | 99.996 | 4.039 |
| 8 | 94 | A8CF56A0-06EA-4E02-82B5-8D7B18189D7F | A Road | trunk_a | 11,047.8 | 41 | 4.015 | 99.996 | 2.554 |
| 9 | 95 | 1EAC12A0-7280-42C7-84ED-993A69D02C8F | A Road | trunk_a | 31,033.9 | 40 | 3.999 | 99.996 | 7.489 |
| 10 | 96 | CE9DB154-EF72-4841-BE95-61741E93D84F | A Road | trunk_a | 21,475.0 | 40 | 3.988 | 99.996 | 7.408 |

### Road classification: B Road

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 158 | 8B16D730-145F-4EB7-B6A9-5976FB696D1F | B Road | other_urban | 10,839.2 | 32 | 3.014 | 99.993 | 0.150 |
| 2 | 201 | 50AC7915-813B-4763-8176-4C4E5D2911C6 | B Road | other_urban | 10,011.4 | 29 | 2.739 | 99.991 | 1.884 |
| 3 | 301 | 10675A16-3ABA-4034-8F16-9FFC0CCA0625 | B Road | other_urban | 15,737.2 | 23 | 2.198 | 99.986 | 0.417 |
| 4 | 343 | 4DB11F0A-D996-4587-A339-26267BF1E6B2 | B Road | other_urban | 7,764.7 | 22 | 2.027 | 99.984 | 0.168 |
| 5 | 362 | 5DDA098F-8582-4994-BD55-C927BDA18AC2 | B Road | other_urban | 16,162.5 | 21 | 1.980 | 99.983 | 0.309 |
| 6 | 371 | C1195BA3-6D8B-46AA-99D4-0CA40DF3B9F2 | B Road | other_urban | 15,018.2 | 21 | 1.949 | 99.983 | 0.372 |
| 7 | 413 | 99DAD5C8-AD6C-4D6C-9197-97F9D7C7DB36 | B Road | other_urban | 11,905.6 | 20 | 1.855 | 99.981 | 0.110 |
| 8 | 425 | 33D5E262-9BF7-4BDB-B084-4EADD9A6E365 | B Road | other_urban | 8,549.4 | 20 | 1.825 | 99.980 | 0.721 |
| 9 | 431 | C9ACE698-0977-45FB-83E5-85E673CA2EE1 | B Road | other_urban | 12,016.8 | 19 | 1.810 | 99.980 | 1.075 |
| 10 | 452 | 6E9935DE-6967-440C-9B0F-B4A2A5E3C22B | B Road | other_urban | 15,661.5 | 19 | 1.769 | 99.979 | 0.086 |

### Road classification: Classified Unnumbered

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 217 | 6FA816AE-B4FD-4E1D-94AB-30501E97ADF6 | Classified Unnumbered | other_urban | 2,504.5 | 29 | 2.630 | 99.990 | 0.370 |
| 2 | 221 | 4435DC95-53B2-4912-8AEC-AF330489ED11 | Classified Unnumbered | other_urban | 2,606.2 | 28 | 2.613 | 99.990 | 0.124 |
| 3 | 231 | 6EA22486-59DA-4A1F-A503-6FE157C1B266 | Classified Unnumbered | other_rural | 590.4 | 31 | 2.536 | 99.989 | 2.228 |
| 4 | 278 | 0AFF5EE0-3267-43D0-9EC5-CA6119303BE6 | Classified Unnumbered | other_urban | 5,350.4 | 23 | 2.285 | 99.987 | 3.048 |
| 5 | 307 | 6A4DC099-8541-4671-908F-64DF143273D0 | Classified Unnumbered | other_urban | 3,231.2 | 24 | 2.187 | 99.986 | 0.151 |
| 6 | 326 | C910A5C2-7048-4751-9013-8769E14AD8BC | Classified Unnumbered | other_urban | 4,428.7 | 22 | 2.091 | 99.985 | 0.282 |
| 7 | 363 | 6D2B61E1-2C45-4F4E-B027-CB05AC2F267F | Classified Unnumbered | other_urban | 3,006.4 | 21 | 1.978 | 99.983 | 0.178 |
| 8 | 509 | 1FF6B42F-F67B-471B-A258-D2ED8C149053 | Classified Unnumbered | other_urban | 5,024.2 | 17 | 1.665 | 99.977 | 0.144 |
| 9 | 516 | A78461B8-9991-423A-81E2-8B2AEC6D5DB8 | Classified Unnumbered | other_urban | 5,817.3 | 17 | 1.658 | 99.976 | 0.189 |
| 10 | 528 | 6E9A0C83-DE15-47D7-B49A-B6E7C3390390 | Classified Unnumbered | other_rural | 3,222.2 | 19 | 1.636 | 99.976 | 0.273 |

### Road classification: Motorway

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A57DAB69-A505-453A-86E9-6B5D8D6AF484 | Motorway | motorway | 60,783.2 | 136 | 13.594 | 100.000 | 10.633 |
| 2 | 2 | 41907D38-3A53-4D70-98FA-035837CB8F24 | Motorway | motorway | 89,230.0 | 129 | 12.884 | 100.000 | 4.910 |
| 3 | 3 | 6D5519F9-1BB1-4FF0-8C3C-08D8428420A8 | Motorway | motorway | 78,308.8 | 123 | 12.259 | 100.000 | 5.066 |
| 4 | 4 | 67A3AC19-C318-4965-93DC-C0601F5ADF64 | Motorway | motorway | 48,140.5 | 119 | 11.845 | 100.000 | 8.245 |
| 5 | 5 | C58A74B8-5ACF-4AE3-A415-F1C3EC186D70 | Motorway | motorway | 48,862.6 | 110 | 10.994 | 100.000 | 11.595 |
| 6 | 6 | 22CC6D97-4AD1-412F-A51D-5851D2B3FBD9 | Motorway | motorway | 55,438.9 | 107 | 10.683 | 100.000 | 8.304 |
| 7 | 7 | EEDCD4A3-3046-4C4E-8DAE-2DF46525E19F | Motorway | motorway | 61,259.4 | 105 | 10.480 | 100.000 | 7.339 |
| 8 | 8 | 6BD1F007-9650-4D84-88D9-40BADED164DB | Motorway | motorway | 71,928.4 | 104 | 10.383 | 100.000 | 7.765 |
| 9 | 9 | D4178A17-E84A-4B2E-8904-3052B12EBCED | Motorway | motorway | 57,746.1 | 94 | 9.383 | 100.000 | 8.182 |
| 10 | 10 | 0D020305-A2B7-49D2-B614-B4C44316D9AB | Motorway | motorway | 72,431.7 | 93 | 9.271 | 100.000 | 5.266 |

### Road classification: Not Classified

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,588 | 9D54B359-FA86-4AD3-B247-1CB815DD8DE1 | Not Classified | other_urban | 810.2 | 14 | 1.049 | 99.927 | 1.053 |
| 2 | 1,705 | 4F3590B5-A05A-43B0-ACA3-2B20E009C722 | Not Classified | other_urban | 1,248.5 | 16 | 1.010 | 99.921 | 0.602 |
| 3 | 3,741 | 1875A561-005B-48EC-A1CF-0EBBA92349F0 | Not Classified | other_urban | 969.1 | 11 | 0.748 | 99.827 | 0.849 |
| 4 | 4,917 | 89726CC1-B89A-4573-AC37-1F3A932BCBE5 | Not Classified | other_urban | 644.1 | 13 | 0.665 | 99.773 | 0.799 |
| 5 | 8,990 | 70532AFC-018B-4315-AA62-DFD720FAB18C | Not Classified | other_urban | 1,808.3 | 7 | 0.502 | 99.585 | 0.157 |
| 6 | 9,249 | F429D637-2E77-41F8-97EE-1F4DE788E23F | Not Classified | other_urban | 1,417.5 | 9 | 0.496 | 99.573 | 0.142 |
| 7 | 12,366 | CEB968B5-58FF-470D-AB2E-6D3970282853 | Not Classified | other_urban | 1,711.8 | 9 | 0.442 | 99.430 | 0.211 |
| 8 | 20,054 | 96C0CAB0-9390-49B9-A92D-AC5F4AD6CC49 | Not Classified | other_urban | 2,141.1 | 4 | 0.345 | 99.075 | 0.075 |
| 9 | 21,605 | 69A73CE3-E150-4485-83B1-C0F60842AF82 | Not Classified | other_urban | 1,596.0 | 5 | 0.323 | 99.003 | 0.087 |
| 10 | 26,182 | 32A34183-EFB8-4945-896C-FE0EEEC15DCC | Not Classified | other_urban | 2,433.2 | 4 | 0.290 | 98.792 | 0.254 |

### Road classification: Unclassified

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 165 | 87A56F0E-7C15-4816-8BCA-F895D218CD1F | Unclassified | other_urban | 4,956.2 | 36 | 2.945 | 99.992 | 0.087 |
| 2 | 427 | 3FB669BD-4581-4F1C-B4D3-7B09ABD166B2 | Unclassified | other_urban | 3,842.0 | 20 | 1.815 | 99.980 | 0.338 |
| 3 | 519 | E5864850-D299-469E-B526-862E5F0D4F9C | Unclassified | other_urban | 1,346.9 | 20 | 1.654 | 99.976 | 0.140 |
| 4 | 608 | 82EA9722-CEEB-4310-B0B5-5F161DA1F9DD | Unclassified | other_urban | 2,869.0 | 16 | 1.532 | 99.972 | 3.955 |
| 5 | 659 | 197A98EA-3CA3-4BD6-87BB-6A3E8B794DF7 | Unclassified | other_urban | 3,936.9 | 20 | 1.483 | 99.970 | 0.042 |
| 6 | 684 | 65CE239A-3621-44FA-ADF6-5657AF3A5508 | Unclassified | other_urban | 6,070.8 | 16 | 1.466 | 99.968 | 0.236 |
| 7 | 720 | 2AFBB011-5C0A-4265-B3AD-8CA4E1E0C272 | Unclassified | other_urban | 2,887.4 | 16 | 1.444 | 99.967 | 0.223 |
| 8 | 728 | 51A08DFB-46BA-4A1A-B2DF-DC23C1E888DA | Unclassified | other_urban | 2,263.1 | 16 | 1.438 | 99.966 | 0.157 |
| 9 | 988 | 98BBC197-9873-482D-B90A-5EE7681BA1ED | Unclassified | other_urban | 2,048.6 | 15 | 1.263 | 99.954 | 0.105 |
| 10 | 1,005 | 00ADC461-C483-43D0-96D4-0A9D90AD959D | Unclassified | other_urban | 2,521.6 | 14 | 1.256 | 99.954 | 0.087 |

### Road classification: Unknown

| within_group_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | risk_percentile_eb | link_length_km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 269 | 58AF7081-C5FF-4239-8D5B-CEC477724409 | Unknown | other_urban | 1,984.0 | 28 | 2.316 | 99.988 | 0.009 |
| 2 | 503 | FA5F7264-2B23-49EF-842F-1F6EDA2814A6 | Unknown | other_urban | 2,246.3 | 22 | 1.675 | 99.977 | 0.130 |
| 3 | 711 | 1AD98107-A5D4-4D13-997B-C391C3C51B08 | Unknown | other_urban | 2,248.8 | 16 | 1.448 | 99.967 | 0.142 |
| 4 | 761 | 4E99C170-2307-4436-84F7-4C64613CDB6E | Unknown | other_urban | 1,800.5 | 16 | 1.404 | 99.965 | 0.133 |
| 5 | 1,259 | 8D21D353-0B2C-4630-B72D-DE9E32E50B3C | Unknown | other_urban | 1,645.6 | 14 | 1.148 | 99.942 | 0.010 |
| 6 | 1,447 | 71FDF20B-7AB5-4BA0-BB47-49EC0FD0A5CD | Unknown | other_urban | 1,416.0 | 16 | 1.085 | 99.933 | 0.193 |
| 7 | 1,710 | E70D0CC7-60EA-407E-BC90-7A9AB745964A | Unknown | other_urban | 2,390.2 | 19 | 1.009 | 99.921 | 0.057 |
| 8 | 2,008 | 75897DA4-CD1D-4D4A-9C8F-328937F299B5 | Unknown | other_urban | 1,416.3 | 18 | 0.956 | 99.907 | 0.220 |
| 9 | 2,243 | 75A512C7-30A0-4057-AACB-AB89B5A0F406 | Unknown | other_urban | 4,886.4 | 10 | 0.911 | 99.897 | 0.198 |
| 10 | 2,435 | 4BA1E3DA-96B9-4B2C-89B8-6678CA8C4419 | Unknown | other_urban | 1,868.8 | 12 | 0.878 | 99.888 | 0.205 |



## Actionable Short-Link Review Subset

- `879` of `2,505` short links (`< 50m`) in the top 1% show `eb_z_vs_neighbours > 3`, indicating isolated risk spikes relative to graph neighbours.

- Filtering to `global_risk_rank < 2000` produces `55` links requiring manual review before use as case study examples.

- Extreme z-scores (`> 100`) reflect near-zero neighbour SD (numerical sensitivity) rather than proportionally greater suspicion.

- The two `other_rural` entries at ranks `1,382` and `1,838` are unusual; short rural links warrant specific inspection.

| risk_rank | global_risk_rank | link_id | road_classification | family | estimated_aadt | collision_count | predicted_eb | link_length_km | n_neighbours | neighbour_mean_predicted_eb | neighbour_sd_predicted_eb | eb_z_vs_neighbours |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 152 | 152 | 65ECF41C-0895-4918-B54F-64EB0FCFBB15 | A Road | other_urban | 15,155.9 | 33 | 3.063 | 0.009 | 3 | 0.138 | 0.105 | 27.895 |
| 246 | 246 | D9D6490D-28C0-41C5-9B1F-DADDDDC1CBE0 | A Road | other_urban | 14,767.1 | 27 | 2.425 | 0.015 | 3 | 0.155 | 0.121 | 18.712 |
| 269 | 269 | 58AF7081-C5FF-4239-8D5B-CEC477724409 | Unknown | other_urban | 1,984.0 | 28 | 2.316 | 0.009 | 4 | 0.373 | 0.323 | 6.011 |
| 368 | 368 | BCD70817-00FF-45F7-88F1-A1C44A15BC85 | A Road | other_urban | 12,064.0 | 25 | 1.956 | 0.031 | 5 | 0.098 | 0.125 | 14.874 |
| 410 | 410 | 3F39400B-5676-4A5B-9402-4A147AA9128F | A Road | other_urban | 19,078.9 | 21 | 1.857 | 0.023 | 6 | 0.394 | 0.437 | 3.346 |
| 458 | 458 | 2DABCE0D-8B14-413E-ADB8-F5A0FF3301E5 | A Road | other_urban | 16,061.6 | 20 | 1.755 | 0.006 | 3 | 0.269 | 0.434 | 3.423 |
| 461 | 461 | 8941431D-1913-48FE-BCC2-FD28E2CF338C | A Road | other_urban | 15,141.2 | 22 | 1.749 | 0.006 | 4 | 0.251 | 0.349 | 4.297 |
| 508 | 508 | 9904B14E-BDA4-443B-8527-39CA1EB5F30F | A Road | other_urban | 31,368.6 | 19 | 1.666 | 0.011 | 5 | 0.412 | 0.383 | 3.275 |
| 522 | 522 | E2FFCA08-836A-4E64-896C-1CF3ED5EB052 | A Road | other_urban | 16,364.5 | 19 | 1.651 | 0.034 | 5 | 0.030 | 0.017 | 92.989 |
| 551 | 551 | 75C7F5C7-8CFC-4C7C-914E-ABF71C87FCB9 | A Road | other_urban | 14,019.6 | 19 | 1.602 | 0.020 | 3 | 0.098 | 0.131 | 11.481 |
| 598 | 598 | E42EB109-97BC-470F-AA87-DFC952BD517F | A Road | other_urban | 9,838.3 | 18 | 1.543 | 0.011 | 3 | 0.121 | 0.086 | 16.585 |
| 659 | 659 | 197A98EA-3CA3-4BD6-87BB-6A3E8B794DF7 | Unclassified | other_urban | 3,936.9 | 20 | 1.483 | 0.042 | 4 | 0.085 | 0.080 | 17.401 |
| 692 | 692 | A631FEFD-EE45-457C-A9EF-652375A09B10 | A Road | other_urban | 13,672.2 | 18 | 1.458 | 0.033 | 4 | 0.018 | 0.004 | 330.906 |
| 739 | 739 | FBC181B0-3FD8-42DF-884C-9E722F6AE9F5 | A Road | other_urban | 16,632.2 | 16 | 1.423 | 0.034 | 4 | 0.177 | 0.251 | 4.970 |
| 777 | 777 | B5C28C24-E237-41A4-ADAA-09E39014D7E4 | A Road | other_urban | 11,133.9 | 16 | 1.391 | 0.038 | 6 | 0.160 | 0.163 | 7.544 |
| 827 | 827 | BB2A8E63-50B3-4488-B77A-732BCDE74110 | A Road | other_urban | 32,357.6 | 15 | 1.361 | 0.028 | 3 | 0.105 | 0.155 | 8.077 |
| 851 | 851 | 82EFEB3E-602E-42E5-B198-9E80BB43F71B | A Road | other_urban | 11,605.1 | 17 | 1.347 | 0.038 | 3 | 0.165 | 0.257 | 4.595 |
| 875 | 875 | E0D12CAD-8DD6-4383-BF96-FEC3C7455BCD | A Road | other_urban | 18,407.9 | 16 | 1.326 | 0.042 | 4 | 0.270 | 0.208 | 5.086 |
| 904 | 904 | 35A7327E-3CB1-48DF-846B-CCE70F450A81 | A Road | other_urban | 29,364.9 | 15 | 1.306 | 0.006 | 3 | 0.048 | 0.056 | 22.604 |
| 941 | 941 | 9FD53343-7A2E-4A52-8EBB-0ED395C8E934 | A Road | other_urban | 21,095.6 | 15 | 1.287 | 0.034 | 5 | 0.198 | 0.148 | 7.352 |
| 966 | 966 | D1135471-075C-43C1-8652-19A1F1906E80 | A Road | other_urban | 9,602.9 | 17 | 1.274 | 0.006 | 3 | 0.138 | 0.144 | 7.877 |
| 982 | 982 | C6BF9FF3-B8F6-49D0-819B-3047A47F2532 | A Road | other_urban | 13,616.0 | 14 | 1.265 | 0.018 | 6 | 0.251 | 0.200 | 5.079 |
| 1,012 | 1,012 | D747DE1C-A989-4AA8-9CE7-9D0EC819B731 | A Road | other_urban | 13,245.7 | 15 | 1.251 | 0.034 | 5 | 0.146 | 0.173 | 6.383 |
| 1,077 | 1,077 | A628CAA7-6CEE-417A-9101-345509B01FAF | Unclassified | other_urban | 1,992.4 | 18 | 1.218 | 0.041 | 5 | 0.263 | 0.081 | 11.758 |
| 1,089 | 1,089 | F3759A42-794F-4E79-82B0-3DC6E247AFA5 | A Road | other_urban | 21,345.8 | 14 | 1.211 | 0.032 | 5 | 0.187 | 0.277 | 3.689 |
| 1,096 | 1,096 | ECF66B8C-8090-4882-A8C4-60013EDBB521 | A Road | other_urban | 38,334.3 | 14 | 1.208 | 0.024 | 4 | 0.135 | 0.232 | 4.628 |
| 1,118 | 1,118 | 53322AC6-696F-4735-8431-F61CDC2EF65F | A Road | other_urban | 25,183.9 | 14 | 1.198 | 0.005 | 3 | 0.142 | 0.216 | 4.899 |
| 1,162 | 1,162 | FE26402C-EBF4-45A6-9DD1-DA371ACA5C7C | Classified Unnumbered | other_urban | 4,112.2 | 13 | 1.181 | 0.037 | 4 | 0.450 | 0.205 | 3.574 |
| 1,259 | 1,259 | 8D21D353-0B2C-4630-B72D-DE9E32E50B3C | Unknown | other_urban | 1,645.6 | 14 | 1.148 | 0.010 | 4 | 0.204 | 0.265 | 3.563 |
| 1,303 | 1,303 | F4006720-F28B-47B5-8777-DFCC241B9EAA | A Road | other_urban | 18,698.5 | 13 | 1.131 | 0.040 | 3 | 0.049 | 0.041 | 26.633 |
| 1,340 | 1,340 | 80B47D1B-564D-418A-8DAD-34729C93534F | B Road | other_urban | 11,250.0 | 13 | 1.117 | 0.021 | 4 | 0.190 | 0.115 | 8.046 |
| 1,344 | 1,344 | 8A85A7D6-6601-4294-8946-83E07033217F | A Road | other_urban | 18,222.2 | 13 | 1.117 | 0.006 | 3 | 0.103 | 0.074 | 13.783 |
| 1,357 | 1,357 | F2C9A129-F9AF-4AAF-A834-9DDA3FC1C33F | A Road | other_urban | 23,056.3 | 13 | 1.112 | 0.036 | 4 | 0.301 | 0.130 | 6.239 |
| 1,382 | 1,382 | 7282FBB4-9FD9-44EB-A0AC-153852F9823D | A Road | other_rural | 12,702.7 | 15 | 1.102 | 0.013 | 5 | 0.127 | 0.113 | 8.645 |
| 1,406 | 1,406 | 17CD445D-E2B8-4E6A-B542-18856410638C | A Road | other_urban | 22,961.0 | 12 | 1.095 | 0.048 | 5 | 0.305 | 0.203 | 3.895 |
| 1,415 | 1,415 | 5A007501-AA81-4A4D-8766-431181D55107 | A Road | other_urban | 7,349.0 | 15 | 1.091 | 0.006 | 3 | 0.031 | 0.032 | 33.027 |
| 1,421 | 1,421 | ADF06DF2-E7C7-48A9-BA89-3EA0D2575A86 | A Road | other_urban | 23,623.8 | 12 | 1.090 | 0.008 | 5 | 0.276 | 0.202 | 4.022 |
| 1,429 | 1,429 | AB0E4E8A-1CD0-4A2C-B7B0-61B568342B5D | A Road | other_urban | 19,153.7 | 12 | 1.088 | 0.039 | 4 | 0.232 | 0.277 | 3.096 |
| 1,436 | 1,436 | 8FBFF59A-2AB7-481C-AF34-B32E2015153F | A Road | other_urban | 13,678.2 | 15 | 1.087 | 0.035 | 4 | 0.140 | 0.164 | 5.762 |
| 1,492 | 1,492 | 8482F245-91EC-465D-9634-4CF06384342A | A Road | other_urban | 9,963.0 | 12 | 1.074 | 0.042 | 5 | 0.083 | 0.113 | 8.774 |
| 1,627 | 1,627 | 51A51F79-55CE-4423-9406-90821C0504D9 | B Road | other_urban | 7,692.2 | 13 | 1.036 | 0.018 | 3 | 0.051 | 0.050 | 19.723 |
| 1,688 | 1,688 | 549AF832-839E-41AC-859B-46F0F0834B55 | A Road | other_urban | 17,497.7 | 13 | 1.017 | 0.032 | 4 | 0.061 | 0.088 | 10.910 |
| 1,690 | 1,690 | 95A95AB2-0BFC-454B-88C5-23AB2FBB7EB2 | A Road | other_urban | 13,501.8 | 12 | 1.016 | 0.007 | 3 | 0.049 | 0.052 | 18.661 |
| 1,716 | 1,716 | 156066FE-A0B6-4002-B8FD-EF93257F0EFD | A Road | other_urban | 13,255.8 | 12 | 1.008 | 0.041 | 5 | 0.019 | 0.004 | 255.945 |
| 1,725 | 1,725 | 7872CBBE-29CF-4D55-B1A8-41A3795ACA07 | Classified Unnumbered | other_urban | 3,454.0 | 12 | 1.004 | 0.049 | 4 | 0.225 | 0.096 | 8.079 |
| 1,793 | 1,793 | 62213C4D-85A8-49AE-8F8A-81C500F4B75D | Classified Unnumbered | other_urban | 1,538.8 | 13 | 0.988 | 0.027 | 4 | 0.029 | 0.027 | 34.948 |
| 1,811 | 1,811 | 633DDA64-5D7B-4D97-B5C4-D499000E7D4F | A Road | other_urban | 14,582.1 | 13 | 0.985 | 0.018 | 4 | 0.158 | 0.092 | 8.985 |
| 1,818 | 1,818 | 1738477C-7D7A-4BD4-B271-8183057E3C64 | A Road | other_urban | 33,111.5 | 11 | 0.984 | 0.028 | 4 | 0.085 | 0.133 | 6.771 |
| 1,822 | 1,822 | BE4A009C-C2AE-4D22-ABD6-36296A298700 | A Road | other_urban | 12,047.4 | 12 | 0.984 | 0.034 | 4 | 0.289 | 0.184 | 3.766 |
| 1,838 | 1,838 | FFE927A0-D9C6-4676-9A30-B34C5CD318A0 | A Road | other_rural | 5,323.7 | 19 | 0.981 | 0.033 | 4 | 0.026 | 0.025 | 37.749 |
| 1,875 | 1,875 | 1E3CC8CF-C381-49B2-BF8A-A99C8158118F | A Road | other_urban | 25,240.0 | 12 | 0.976 | 0.027 | 4 | 0.132 | 0.164 | 5.148 |
| 1,912 | 1,912 | 35E2C7E6-1A74-4C49-BB9B-D91B5FD20815 | A Road | other_urban | 38,494.5 | 12 | 0.971 | 0.006 | 4 | 0.113 | 0.130 | 6.598 |
| 1,940 | 1,940 | 8DBC3C8E-B6B1-44CD-8B93-B46085024DE1 | B Road | other_urban | 16,032.4 | 11 | 0.967 | 0.043 | 3 | 0.042 | 0.044 | 21.054 |
| 1,945 | 1,945 | B150FDEC-3C53-4F93-8034-1FAC16B123D2 | Classified Unnumbered | other_urban | 1,499.2 | 16 | 0.966 | 0.030 | 4 | 0.035 | 0.039 | 24.141 |
| 1,947 | 1,947 | 383F9C3B-AFC8-42BD-B606-E59FBA91F375 | B Road | other_urban | 15,760.1 | 11 | 0.966 | 0.037 | 3 | 0.168 | 0.254 | 3.148 |

## Known Issues To Carry Forward

- `pct_attribute_snapped` is known broken/always zero and is intentionally excluded from all QA tables here.

- Motorway EB calibration remains unresolved; motorway examples should carry this caveat in demos and stakeholder review.

- Global EB uses a single refreshed Phase 1 MoM dispersion surface. The selected production k is `3.451158`; MoM aggregation choice still moves about `4.6%` of top-1 membership between positive-weighted and link-year-weighted k.

- EB is screening evidence that still reflects observed collision history. It should not be presented as causal proof or an iRAP-style engineering audit.



## Final Verdict

**Suitable with caveats. 55 short links (< 50m, top-2000 rank) flagged for manual review before case-study use. Full outputs remain unchanged.**



The refreshed outputs are suitable for v0.1 screening/demo use because the top-1% table is now based on the refreshed EB scores, contains no zero-collision top-1% rows, has no AADT values above 150,000, and preserves useful group-specific views. The caveats are important: short segments and family-level EB outliers need manual review before being used as exemplar case studies, and motorway calibration should remain explicit.
