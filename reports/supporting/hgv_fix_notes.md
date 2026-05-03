# HGV Source-Table Fix Notes

## What Changed

Code changes:

- `src/road_risk/clean_join/join.py`
  - Added `save_road_traffic_features()`.
  - `main()` now persists the existing `build_road_features()` output to
    `data/features/road_traffic_features.parquet`.
  - `build_road_features()` logic itself was not changed.

- `src/road_risk/model/collision.py`
  - Added `TRAFFIC_FEATURES_PATH`.
  - `build_collision_dataset()` no longer pulls `hgv_proportion` from
    `road_link_annual`.
  - `build_collision_dataset()` now left-joins `hgv_proportion` from
    `data/features/road_traffic_features.parquet` onto the all-link x year
    base using `link_id, year`.
  - The join guards against duplicate `link_id, year` rows and checks that the
    Stage 2 row count is unchanged.

Generated artefacts:

- `data/features/road_traffic_features.parquet`
- `reports/supporting/hgv_coverage_post_fix.csv`

No modelling, rank-stability, or ablation runs were executed.

## Verification

The rebuilt Stage 2 dataset has the expected row count:

| check | value |
|---|---:|
| Stage 2 rows | 21,675,570 |
| Expected rows | 21,675,570 |
| Overall `hgv_proportion` coverage | 72.37% |
| Non-null `hgv_proportion` link-years | 15,686,626 |

Coverage by collision stratum:

| stratum | link-years | non-null HGV | coverage |
|---|---:|---:|---:|
| Collision-positive link-years | 391,255 | 351,969 | 89.96% |
| Zero-collision link-years | 21,284,315 | 15,334,657 | 72.05% |

Coverage by road class and collision stratum:

| road class | collision-positive coverage | zero-collision coverage |
|---|---:|---:|
| A Road | 92.11% | 79.11% |
| B Road | 81.41% | 63.23% |
| Classified Unnumbered | 80.13% | 53.15% |
| Motorway | 96.72% | 87.60% |
| Not Classified | 91.38% | 68.81% |
| Unclassified | 95.18% | 80.48% |
| Unknown | 93.38% | 60.90% |

The old pathological pattern is gone: zero-collision link-years now receive
AADF-derived HGV coverage where the all-link traffic table has a valid AADF
match. Before the fix, zero-collision links had 0.00% coverage in every road
class.

## Remaining Caveat

Coverage is still higher for collision-positive link-years than for
zero-collision link-years within the same road class. This means the strict
"approximately equal within road class" verification criterion is not fully
satisfied.

The remaining gap is no longer caused by sourcing `hgv_proportion` from a
collision-positive table. It appears to be a genuine AADF survey-coverage /
network-location confound: collision-positive rows tend to be busier and more
survey-covered within road class. For example, median AADT in the fixed Stage 2
dataset is 4,533 on collision-positive link-years versus 643 on zero-collision
link-years.

An extra road-class x AADT-decile check still showed a median absolute coverage
gap of about 11.7 percentage points between collision-positive and zero-collision
rows. So the source-table bug is fixed, but AADF coverage remains informative
about road importance and traffic geography.

## Decisions

- Did not alter `build_road_features()` spatial matching logic.
- Did not alter `build_road_link_annual()` collision aggregation.
- Did not add imputation.
- Did not add `hgv_proportion_missing`.
- Did not move other traffic/WebTRIS features into Stage 2. Only
  `hgv_proportion` was moved off the collision-positive source table, matching
  the requested scope.

## Recommendation

The immediate source-table/grain bug is fixed, but `hgv_proportion` should
still be treated carefully in the temporal ablation because AADF coverage is
not random. Two defensible next choices:

1. Keep the fixed `hgv_proportion` baseline and report that remaining HGV
   missingness reflects AADF survey coverage, not collision-table leakage.
2. For the cleanest temporal ablation baseline, compare against a sensitivity
   run that drops `hgv_proportion`, because coverage still carries road-importance
   information.

The production path should use the fixed all-link traffic join, then rerun
Stage 2 and rank-stability before interpreting HGV importance or temporal lift.
