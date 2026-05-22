# KSI Reporting Consistency Diagnostic

**Status:** Part A diagnostic report. No KSI GLM, EB shrinkage, or production model change.

## Setup

This report checks whether fatal/serious reporting is consistent enough across force/year cells to proceed to the next pre-registered KSI diagnostic stage.

## Input Data Path

- Stage 2 collision count table: `data/features/road_link_annual.parquet`
- Collision-level STATS19-linked source used for force/year reporting: `data/processed/stats19/snapped_weighted.parquet`
- Input collision rows: 452,897
- Retained rows after Stage 2 snap-method and snap-score filters: 450,991

## Method

The diagnostic uses the same snapped collision source that feeds `road_link_annual.parquet`, then applies the Stage 2 snap filters: `snap_method in {attribute, spatial, weighted}` and, where present, `snap_score >= 0.6`.

- Collision year field: `collision_year` if present; otherwise derived from `date`.
- Police force field: `police_force`, with names mapped from `config/settings.yaml`.
- Severity field: `collision_severity`.
- All-injury count indicator: one retained STATS19 collision row counted by `collision_index`.
- KSI definition: `collision_severity in {1, 2}` where 1=fatal and 2=serious.
- Flag rule: a force/year row is flagged when the year-on-year percentage change in KSI-to-all-injury ratio exceeds ±20%.
- Sensitivity flag: a force/year row is flagged only when the same ±20% ratio rule is met and the absolute KSI count change is at least 25 collisions. This does not replace the pre-registered rule.

## Summary Tables

| metric | value |
| --- | --- |
| force/year rows | 230 |
| forces | 23 |
| years | 2015–2024 |
| all-injury collisions | 450,991 |
| KSI collisions | 99,559 |
| overall KSI/all-injury ratio | 0.2208 |
| pre-registered flagged force/year rows | 28 |
| practical-sensitivity flagged force/year rows | 26 |

### By Year

| year | all_injury_count | ksi_count | ksi_to_all_injury_ratio | pre_registered_flagged_force_years | practical_sensitivity_flagged_force_years |
| --- | --- | --- | --- | --- | --- |
| 2015 | 56022 | 9313 | 0.1662 | 0 | 0 |
| 2016 | 54330 | 9893 | 0.1821 | 6 | 6 |
| 2017 | 51018 | 10038 | 0.1968 | 3 | 3 |
| 2018 | 48030 | 10033 | 0.2089 | 1 | 1 |
| 2019 | 45318 | 10029 | 0.2213 | 5 | 4 |
| 2020 | 34540 | 8016 | 0.2321 | 1 | 1 |
| 2021 | 39345 | 9639 | 0.2450 | 3 | 3 |
| 2022 | 40995 | 10689 | 0.2607 | 3 | 2 |
| 2023 | 40531 | 10785 | 0.2661 | 3 | 3 |
| 2024 | 40862 | 11124 | 0.2722 | 3 | 3 |

### By Force

| police_force | force_name | all_injury_count | ksi_count | ksi_to_all_injury_ratio | pre_registered_flagged_years | practical_sensitivity_flagged_years |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | Cumbria | 9928 | 2480 | 0.2498 | 2 | 1 |
| 4 | Lancashire | 30198 | 8061 | 0.2669 | 1 | 1 |
| 5 | Merseyside | 21736 | 4630 | 0.2130 | 0 | 0 |
| 6 | Greater Manchester | 30954 | 6926 | 0.2238 | 1 | 1 |
| 7 | Cheshire | 18219 | 3333 | 0.1829 | 1 | 1 |
| 11 | Durham | 7910 | 2117 | 0.2676 | 1 | 1 |
| 12 | North Yorkshire | 15154 | 3357 | 0.2215 | 0 | 0 |
| 13 | West Yorkshire | 41626 | 9296 | 0.2233 | 1 | 1 |
| 14 | South Yorkshire | 24161 | 6528 | 0.2702 | 2 | 2 |
| 16 | Humberside | 21003 | 4536 | 0.2160 | 1 | 1 |
| 17 | Cleveland | 6627 | 1517 | 0.2289 | 1 | 1 |
| 20 | West Midlands | 51332 | 9013 | 0.1756 | 0 | 0 |
| 21 | Staffordshire | 14173 | 2475 | 0.1746 | 5 | 4 |
| 22 | West Mercia | 18052 | 4539 | 0.2514 | 0 | 0 |
| 23 | Warwickshire | 11299 | 2701 | 0.2390 | 1 | 1 |
| 30 | Derbyshire | 17665 | 3682 | 0.2084 | 2 | 2 |
| 31 | Nottinghamshire | 22098 | 4405 | 0.1993 | 1 | 1 |
| 32 | Lincolnshire | 17691 | 3898 | 0.2203 | 2 | 2 |
| 33 | Leicestershire | 14703 | 3103 | 0.2110 | 1 | 1 |
| 34 | Northamptonshire | 11348 | 2652 | 0.2337 | 1 | 1 |
| 35 | Cambridgeshire | 16544 | 3729 | 0.2254 | 2 | 2 |
| 36 | Norfolk | 15900 | 3932 | 0.2473 | 0 | 0 |
| 37 | Suffolk | 12670 | 2649 | 0.2091 | 2 | 2 |

## Plots

![KSI count by force and year](reports/figures/ksi_reporting_consistency/ksi_count_by_force_year.png)

![KSI-to-all-injury ratio by force and year](reports/figures/ksi_reporting_consistency/ksi_ratio_by_force_year.png)

## Flagged Force/Year Breaks

| police_force | force_name | year | all_injury_count | ksi_count | ksi_to_all_injury_ratio | ksi_count_change | ratio_yoy_pct_change | practical_sensitivity_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | Cumbria | 2016 | 1247 | 242 | 0.1941 | +44 | 24.1% | yes |
| 14 | South Yorkshire | 2016 | 3053 | 524 | 0.1716 | +165 | 46.5% | yes |
| 21 | Staffordshire | 2016 | 2535 | 319 | 0.1258 | +50 | 20.8% | yes |
| 23 | Warwickshire | 2016 | 1453 | 332 | 0.2285 | +63 | 27.3% | yes |
| 32 | Lincolnshire | 2016 | 1973 | 376 | 0.1906 | +97 | 45.4% | yes |
| 37 | Suffolk | 2016 | 1550 | 259 | 0.1671 | +73 | 33.2% | yes |
| 14 | South Yorkshire | 2017 | 2792 | 728 | 0.2607 | +204 | 51.9% | yes |
| 32 | Lincolnshire | 2017 | 1902 | 498 | 0.2618 | +122 | 37.4% | yes |
| 35 | Cambridgeshire | 2017 | 1995 | 413 | 0.2070 | +44 | 20.7% | yes |
| 33 | Leicestershire | 2018 | 1584 | 346 | 0.2184 | +79 | 32.8% | yes |
| 3 | Cumbria | 2019 | 1011 | 282 | 0.2789 | +4 | 21.0% | no |
| 4 | Lancashire | 2019 | 2929 | 908 | 0.3100 | +232 | 53.4% | yes |
| 11 | Durham | 2019 | 849 | 245 | 0.2886 | +52 | 41.6% | yes |
| 16 | Humberside | 2019 | 2308 | 441 | 0.1911 | -141 | -24.8% | yes |
| 37 | Suffolk | 2019 | 1360 | 317 | 0.2331 | +59 | 30.2% | yes |
| 35 | Cambridgeshire | 2020 | 1245 | 345 | 0.2771 | -43 | 21.0% | yes |
| 6 | Greater Manchester | 2021 | 3003 | 746 | 0.2484 | +285 | 29.2% | yes |
| 13 | West Yorkshire | 2021 | 3877 | 1032 | 0.2662 | +450 | 25.8% | yes |
| 21 | Staffordshire | 2021 | 819 | 209 | 0.2552 | +63 | 53.6% | yes |
| 17 | Cleveland | 2022 | 672 | 188 | 0.2798 | +43 | 20.0% | yes |
| 21 | Staffordshire | 2022 | 506 | 194 | 0.3834 | -15 | 50.2% | no |
| 31 | Nottinghamshire | 2022 | 1889 | 493 | 0.2610 | +113 | 27.5% | yes |
| 21 | Staffordshire | 2023 | 883 | 268 | 0.3035 | +74 | -20.8% | yes |
| 30 | Derbyshire | 2023 | 1764 | 442 | 0.2506 | +36 | 21.6% | yes |
| 34 | Northamptonshire | 2023 | 1232 | 241 | 0.1956 | -76 | -24.2% | yes |
| 7 | Cheshire | 2024 | 1463 | 358 | 0.2447 | +52 | 22.1% | yes |
| 21 | Staffordshire | 2024 | 1493 | 354 | 0.2371 | +86 | -21.9% | yes |
| 30 | Derbyshire | 2024 | 1650 | 500 | 0.3030 | +58 | 20.9% | yes |

## Interpretation

- Isolated small-number volatility: the pre-registered ±20% rule flags 28 force/year rows across 18 of 23 forces. The stricter practical sensitivity flag still retains 26 rows, so the result is not mainly an artefact of tiny absolute KSI changes.
- Systematic reporting transition: there is some evidence of an early transition because 9 flags occur in 2016–2017, including clustered changes for South Yorkshire and Lincolnshire. The 2016–2019 flag concentration is consistent with the documented staggered rollout of CRaSH (Collision Recording and Sharing) and COPA (Case Overview Preparation Application) injury-based reporting systems across UK police forces during this period, which is known to increase the share of casualties classified as serious. DfT publishes severity adjustment factors for exactly this purpose; this diagnostic does not apply them. The 2016–2019 pattern is not a clean single-year national transition, however: removing 2015–2016 reduces but does not remove the issue.
- Covid-era disruption: present but not dominant. 4 flags occur in 2020–2021. The flagged rows continue before and after the Covid period, so Covid alone is not a sufficient explanation.
- 2024 CF→RSF transition: this does not appear to be a system-wide break in this extract: 3 of 23 forces are flagged in 2024, well below the 'all or most forces' decision rule.
- Heterogeneous force-specific behaviour: this is the dominant pattern rather than a single clean national break. Forces with repeated flagged years are: 21 Staffordshire (5), 3 Cumbria (2), 14 South Yorkshire (2), 30 Derbyshire (2), 32 Lincolnshire (2), 35 Cambridgeshire (2), 37 Suffolk (2).

## Window Sensitivity

The pre-registered flag is retained exactly. The practical-sensitivity columns show the stricter flag that also requires an absolute KSI count change of at least 25 collisions.

| window | number_of_forces | number_of_force_year_rows | all_injury_count | ksi_count | overall_ksi_to_all_injury_ratio | pre_registered_flagged_force_year_rows | forces_with_any_pre_registered_flagged_years | practical_sensitivity_flagged_force_year_rows | forces_with_any_practical_sensitivity_flagged_years |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2015–2024 | 23 | 230 | 450,991 | 99,559 | 0.2208 | 28 | 3, 4, 6, 7, 11, 13, 14, 16, 17, 21, 23, 30, 31, 32, 33, 34, 35, 37 | 26 | 3, 4, 6, 7, 11, 13, 14, 16, 17, 21, 23, 30, 31, 32, 33, 34, 35, 37 |
| 2017–2024 | 23 | 184 | 340,639 | 80,353 | 0.2359 | 22 | 3, 4, 6, 7, 11, 13, 14, 16, 17, 21, 30, 31, 32, 33, 34, 35, 37 | 20 | 4, 6, 7, 11, 13, 14, 16, 17, 21, 30, 31, 32, 33, 34, 35, 37 |
| 2017–2023 | 23 | 161 | 299,777 | 69,229 | 0.2309 | 19 | 3, 4, 6, 11, 13, 14, 16, 17, 21, 30, 31, 32, 33, 34, 35, 37 | 17 | 4, 6, 11, 13, 14, 16, 17, 21, 30, 31, 32, 33, 34, 35, 37 |
| 2019–2023 | 23 | 115 | 200,729 | 49,158 | 0.2449 | 15 | 3, 4, 6, 11, 13, 16, 17, 21, 30, 31, 34, 35, 37 | 13 | 4, 6, 11, 13, 16, 17, 21, 30, 31, 34, 35, 37 |

## Practical Modelling Recommendation

A standalone national-scope KSI atlas is not recommended on the basis of this diagnostic. The KSI/all-injury reporting ratio is not stable across the study area's police forces over 2015–2024, with the instability concentrated in (a) the documented 2016–2019 CRaSH/COPA reporting reform rollout, (b) Staffordshire-specific data anomalies, and (c) residual heterogeneity in remaining forces that does not collapse under tested restricted windows. A KSI model fit on these counts would conflate severity reporting changes with genuine severity variation; the rankings would not be defensible at national scope without applying DfT's published severity adjustment factors as a methodological prerequisite.

Part B is not run on this diagnostic. The standalone KSI atlas is parked (see `todo/parked.md`) with an explicit revisit condition tied to the DfT severity adjustment factor methodology.

## Verdict

**Strict pre-registered verdict:** per-force handling required before KSI modelling is defensible.

**Operational decision:** do not proceed with Part B. Park the standalone KSI atlas. Move on to Temporal B.
