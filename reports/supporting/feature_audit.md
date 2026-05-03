# Feature Missingness Audit

## Methodology

This audit rebuilds the current Stage 2 collision dataset with `build_collision_dataset()` and checks only NaN/non-NaN structure. Collision history is fixed per link: a link is collision-positive if it had at least one collision in 2015-2024, otherwise it is zero-collision. Coverage is compared within exact `road_classification` strata.

For each feature, the audit reports both per-link ever-non-null coverage and per-link-year coverage. Target and collision-derived columns are skipped, as are globally 0% or 100% non-null features.

## Development Subset

The configured `study_area.bbox_bng` covered more than 30% of cached OpenRoads links, so the development subset used the fallback West Yorkshire 50 km BNG square.

Selected subset bbox: `West Yorkshire 50 km BNG square: E 400000-450000, N 400000-450000`.

Configured bbox link count: 2,167,290 (100.0% of full cached OpenRoads).

Selected subset link count: 147,925 (6.8% of full cached OpenRoads).

Subset filter counts:

| frame | rows before | links before | rows after | links after |
| --- | --- | --- | --- | --- |
| openroads | 2,167,557 | 2,167,557 | 147,925 | 147,925 |
| aadt_estimates | 21,675,570 | 2,167,557 | 1,479,250 | 147,925 |
| road_link_annual | 391,255 | 233,604 | 40,260 | 24,350 |
| net_features | 2,167,557 | 2,167,557 | 147,925 | 147,925 |

Full-network counts:

| frame | rows before | links before | rows after | links after |
| --- | --- | --- | --- | --- |
| openroads | 2,167,557 | 2,167,557 | 2,167,557 | 2,167,557 |
| aadt_estimates | 21,675,570 | 2,167,557 | 21,675,570 | 2,167,557 |
| road_link_annual | 391,255 | 233,604 | 391,255 | 233,604 |
| net_features | 2,167,557 | 2,167,557 | 2,167,557 | 2,167,557 |

## Runtimes

| step | runtime |
| --- | --- |
| subset build_collision_dataset | 13.4s |
| subset audit | 5.1s |
| full build_collision_dataset | 48.2s |
| full audit | 2m 19.3s |

## Threshold Calibration

Gap distribution across auditable feature x road-class pairs before applying flags:

| metric | value |
| --- | --- |
| n_feature_road_class_pairs | 112.000000 |
| mean_gap | 0.098125 |
| std_gap | 0.073729 |
| q00_gap | 0.000012 |
| q01_gap | 0.000029 |
| q05_gap | 0.000962 |
| q10_gap | 0.002895 |
| q25_gap | 0.054778 |
| q50_gap | 0.086128 |
| q75_gap | 0.133176 |
| q90_gap | 0.224159 |
| q95_gap | 0.234771 |
| q99_gap | 0.271798 |
| q100_gap | 0.287946 |

Thresholds used: per-link gap > 5%, zero-collision non-null share < 50%, and per-link versus per-link-year gap disagreement > 10%. The 5 percentage point starting threshold was retained after printing the empirical gap distribution above and before listing flagged features.

## Flagged Features

| feature | road_class | positive | zero | gap | link-year gap | reason |
| --- | --- | --- | --- | --- | --- | --- |
| speed_limit_mph | B Road | 61.0% | 48.6% | 12.4% | 12.4% | coverage_gap_and_low_zero_collision_coverage |
| is_unpaved | Unknown | 19.6% | 9.0% | 10.5% | 10.5% | coverage_gap_and_low_zero_collision_coverage |
| is_unpaved | Classified Unnumbered | 28.3% | 18.3% | 10.0% | 10.0% | coverage_gap_and_low_zero_collision_coverage |
| lanes | A Road | 40.2% | 30.4% | 9.8% | 9.8% | coverage_gap_and_low_zero_collision_coverage |
| is_unpaved | Unclassified | 25.6% | 15.9% | 9.7% | 9.7% | coverage_gap_and_low_zero_collision_coverage |
| lanes | Classified Unnumbered | 19.7% | 11.6% | 8.1% | 8.1% | coverage_gap_and_low_zero_collision_coverage |
| lanes | B Road | 27.3% | 19.5% | 7.8% | 7.8% | coverage_gap_and_low_zero_collision_coverage |
| is_unpaved | B Road | 30.2% | 22.5% | 7.7% | 7.7% | coverage_gap_and_low_zero_collision_coverage |
| lit | Classified Unnumbered | 16.7% | 9.4% | 7.4% | 7.4% | coverage_gap_and_low_zero_collision_coverage |
| lit | Unknown | 9.4% | 2.2% | 7.3% | 7.3% | coverage_gap_and_low_zero_collision_coverage |
| lit | Unclassified | 16.5% | 9.6% | 6.9% | 6.9% | coverage_gap_and_low_zero_collision_coverage |
| lanes | Unknown | 7.4% | 1.3% | 6.1% | 6.1% | coverage_gap_and_low_zero_collision_coverage |
| lit | A Road | 28.4% | 22.4% | 6.1% | 6.1% | coverage_gap_and_low_zero_collision_coverage |
| lit | B Road | 20.4% | 14.5% | 5.9% | 5.9% | coverage_gap_and_low_zero_collision_coverage |
| lanes | Unclassified | 9.9% | 4.0% | 5.9% | 5.9% | coverage_gap_and_low_zero_collision_coverage |
| is_unpaved | A Road | 30.6% | 24.9% | 5.8% | 5.8% | coverage_gap_and_low_zero_collision_coverage |
| is_unpaved | Not Classified | 17.7% | 12.4% | 5.2% | 5.2% | coverage_gap_and_low_zero_collision_coverage |

## Expected Flags Baseline

The current expected baseline is that flags on `is_unpaved`, `lanes`, `lit`, and raw `speed_limit_mph` are known sparse-OSM/provenance patterns rather than HGV-style source-table bugs.

| check | value |
| --- | --- |
| Expected sparse-OSM/provenance features present | is_unpaved, lanes, lit, speed_limit_mph |
| Expected sparse-OSM/provenance feature-road-class pairs | 17 |
| Expected baseline features not flagged in this run | None |
| Unexpected flagged feature names | None |

Details are in `reports/supporting/flagged_feature_plan_status.md`. A future rerun that reproduces only these feature names can be triaged quickly against that note. A future rerun that flags any additional feature name should be investigated as a new candidate missingness-vs-collision-history issue.

Recommended next steps for any flags: inspect the feature source table and join grain, decide separately whether to source from an all-link table, drop the feature, or impute it. No fixes are made by this diagnostic.

## Untestable Features

| feature | reason | road classes |
| --- | --- | --- |
| dist_to_major_km | within_class_all_0_or_all_100 | 2 |
| max_curvature_deg_per_km | within_class_all_0_or_all_100 | 7 |
| mean_curvature_deg_per_km | within_class_all_0_or_all_100 | 7 |
| sinuosity | within_class_all_0_or_all_100 | 3 |
| speed_limit_mph_effective | within_class_all_0_or_all_100 | 2 |

Globally 0% or 100% non-null features skipped before within-class testing:

| feature | global non-null share |
| --- | --- |
| betweenness | 100.0% |
| betweenness_relative | 100.0% |
| degree_mean | 100.0% |
| estimated_aadt | 100.0% |
| form_of_way | 100.0% |
| form_of_way_ord | 100.0% |
| grade_low_confidence | 100.0% |
| grade_method | 100.0% |
| is_a_road | 100.0% |
| is_bridge_proxy | 100.0% |
| is_covered_proxy | 100.0% |
| is_covid | 100.0% |
| is_dual | 100.0% |
| is_motorway | 100.0% |
| is_primary | 100.0% |
| is_roundabout | 100.0% |
| is_slip_road | 100.0% |
| is_trunk | 100.0% |
| is_tunnel_proxy | 100.0% |
| link_length_km | 100.0% |
| log_link_length | 100.0% |
| log_offset | 100.0% |
| road_class_ord | 100.0% |
| speed_limit_mph_imputed | 100.0% |
| speed_limit_source | 100.0% |
| valid_elev_points | 100.0% |
| valid_grade_segments | 100.0% |
| year_norm | 100.0% |

## Passed Features

| feature | auditable road classes | untestable road classes |
| --- | --- | --- |
| dist_to_major_km | 5 | 2 |
| grade_change | 7 | 0 |
| hgv_proportion | 7 | 0 |
| imd_crime_decile | 7 | 0 |
| imd_decile | 7 | 0 |
| imd_living_indoor_decile | 7 | 0 |
| max_curvature_deg_per_km | 0 | 7 |
| max_grade | 7 | 0 |
| mean_curvature_deg_per_km | 0 | 7 |
| mean_grade | 7 | 0 |
| pop_density_per_km2 | 7 | 0 |
| ruc_class | 7 | 0 |
| ruc_urban_rural | 7 | 0 |
| sinuosity | 4 | 3 |
| speed_limit_mph_effective | 5 | 2 |

Flagged features excluded from this pass table: is_unpaved, lanes, lit, speed_limit_mph.

## Road-Class Consistency

Links with inconsistent `road_classification` across years: 0.

## Outputs

- `reports/supporting/feature_audit_full.csv`
- `reports/supporting/feature_audit_flagged.csv`
