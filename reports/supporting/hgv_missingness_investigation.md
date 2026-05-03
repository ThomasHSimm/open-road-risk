# HGV Proportion Missingness Investigation

## Question

`hgv_proportion` is AADF-derived as `all_hgvs / all_motor_vehicles`, but in
`risk_scores.parquet` it is present for only about 10% of links and only on
links with historical collisions. This investigation checks whether that is a
legitimate coverage limit, a join bug, an imputation gap, or something else.

Supporting CSVs:

- `reports/supporting/hgv_coverage_by_road_class.csv`
- `reports/supporting/hgv_coverage_by_collision_history.csv`
- `reports/supporting/hgv_aadf_vs_webtris_correlation.csv`

## Coverage Pattern

In current `risk_scores.parquet`:

| population | links | links with `hgv_proportion` | coverage |
|---|---:|---:|---:|
| All links | 2,167,557 | 209,594 | 9.67% |
| Links with >=1 historical collision | 233,604 | 209,594 | 89.72% |
| Links with zero historical collisions | 1,933,953 | 0 | 0.00% |

This is not just a road-class coverage effect. Within each broad road class,
zero-collision links still have zero `hgv_proportion` coverage:

| road class group | collision-history coverage | zero-collision coverage |
|---|---:|---:|
| Motorway | 97.85% | 0.00% |
| A-road | 92.52% | 0.00% |
| B-road | 81.44% | 0.00% |
| Minor | 89.73% | 0.00% |
| Unknown | 92.15% | 0.00% |

The same pattern holds by estimated-AADT decile: coverage on links with
historical collisions ranges from 54.86% in D1 to 93.14% in D8, while coverage
on zero-collision links is 0.00% in every decile.

Conclusion from coverage: the missingness is collision-history dependent within
road class and traffic-volume strata. It is not explained by AADF only covering
major roads.

## Join Logic

### Source Construction

`hgv_proportion` is constructed in `src/road_risk/ingest/ingest_aadf.py` as:

```python
df["hgv_proportion"] = df["all_hgvs"] / df["all_motor_vehicles"]
```

So the field itself is AADF-derived, not WebTRIS-derived.

### AADF to Open Roads

`src/road_risk/clean_join/join.py::build_road_features()` builds a link-year
traffic feature table by spatially matching OS Open Roads link centroids to
AADF count points year-by-year.

Join properties:

- Join key: geographic nearest-neighbour, not `link_id` or `count_point_id`.
- Direction: Open Roads links -> nearest AADF count point for each year.
- Cardinality: many Open Roads links can receive features from the same AADF
  count point; this is many-to-one from links to count points.
- Unmatched handling: links beyond the AADF distance cap retain the row but
  get `NaN` for AADF-derived features. Some beyond-cap rows can be filled by
  road-name matching.
- Intended grain: all Open Roads links x AADF years.

This table is not currently persisted as the Stage 2 traffic feature source.

### Collision Aggregation to `road_link_annual`

`src/road_risk/clean_join/join.py::build_road_link_annual()` first aggregates
snapped collision records:

```python
agg = snapped.groupby(["link_id", "year"]).agg(...)
```

That aggregation only creates rows for link-years with retained snapped
collisions. It then joins traffic features onto this collision-positive table:

```python
result = agg.merge(road_feat, on=["link_id", "year"], how="left")
```

Join properties:

- Join key: `link_id`, `year`.
- Direction: collision-positive link-years -> road feature table.
- Cardinality: expected many-to-one or one-to-one per `link_id, year`,
  depending on whether the road-feature table has duplicate link-year rows.
- Unmatched handling: collision-positive rows with no AADF match get `NaN`.
- Dropped population: zero-collision link-years never enter `agg`, so they
  never receive AADF `hgv_proportion` in `road_link_annual`.

### Stage 2 Collision Dataset

`src/road_risk/model/collision.py::build_collision_dataset()` correctly starts
from all links x years, then left-joins `road_link_annual` on `link_id, year`.
However, it currently pulls `hgv_proportion` from `road_link_annual`.

That means:

- collision-positive link-years can receive AADF-derived `hgv_proportion`;
- zero-collision link-years have no `road_link_annual` row and therefore get
  `NaN`;
- after pooling, every link with non-null `hgv_proportion` has historical
  collision history.

### Downstream Imputation

There is no safe downstream imputation of `hgv_proportion` in the XGBoost path.
`train_collision_xgb()` includes `hgv_proportion` whenever the column exists and
then fills missing feature values with zero:

```python
model_df[feature_cols] = model_df[feature_cols].fillna(0)
```

This turns missing `hgv_proportion` into a value branch that is effectively
equivalent to "no retained historical collision row exists".

The GLM path is less affected because its coverage threshold excludes
`hgv_proportion` from the current GLM feature list, but the XGBoost model uses
it directly.

`src/road_risk/model/aadt.py::apply_aadt_estimator()` does internally fill
missing AADF-derived `hgv_proportion` with the AADF median for AADT inference,
but `aadt_estimates.parquet` only persists `link_id`, `year`, and
`estimated_aadt`. That median-filled HGV feature is not available to Stage 2.

## Mechanism

This is primarily **(d) something else: a source-table/grain design bug**.

It is adjacent to a join bug, but the problem is not that nearest-neighbour
AADF snapping preferentially matches collision links. The problem is that the
only table Stage 2 uses for `hgv_proportion` is `road_link_annual`, and that
table is collision-aggregate-first. AADF traffic features are joined after the
collision aggregation, so they are only carried forward for collision-positive
link-years.

It is not **(a) legitimate coverage limit**, because zero-collision links have
0% coverage even within motorways, A-roads, trunk links, and the highest AADT
decile.

It is not only **(c) imputation gap**, because imputing the current missingness
would be imputing a feature that was never joined for the zero-collision
population. Missingness itself has already become collision-history information.

## Recommended Fix Options

### Option 1: Drop `hgv_proportion` from the collision model now

This is the safest immediate unblocker.

Expected impact:

- Removes the collision-history availability leak.
- Likely reduces apparent predictive performance and changes feature
  importance because the current XGBoost model relies heavily on this feature.
- Does not preserve true HGV signal.
- Makes the temporal WebTRIS HGV ablation cleaner, because the baseline no
  longer contains a contaminated AADF HGV field.

### Option 2: Fix the Stage 2 join source

This is the correct production fix.

Persist or rebuild an all-link x year traffic feature table from
`build_road_features()` and join it into Stage 2 independently of
`road_link_annual`.

Stage 2 should join three separate sources:

- all-link x year base from Open Roads and AADT estimate years;
- collision counts from `road_link_annual`;
- pre-collision traffic features from an all-link x year AADF/WebTRIS feature
  table.

Expected impact:

- Preserves legitimate AADF HGV signal where available.
- Removes the collision-history missingness leak.
- Allows honest missingness handling for roads outside AADF coverage.
- Requires rerunning Stage 2 and rank-stability after implementation.

### Option 3: Impute missing links

If the all-link traffic table cannot be fixed immediately, a temporary
imputation could fill `hgv_proportion` by road class and possibly AADT decile.

Suggested temporary hierarchy:

1. road_classification x estimated_aadt_decile median;
2. road_classification median;
3. global median.

Expected impact:

- Removes the exact missing-as-zero collision-history branch.
- Preserves only broad HGV signal, not link-specific AADF HGV signal.
- Still relies on medians estimated from the collision-positive subset unless
  computed from the original all-AADF/road-feature source.
- Should not be treated as the final fix.

### Option 4: Keep feature and add `hgv_proportion_missing`

Do not use this with the current source table.

Expected impact:

- The missing indicator would almost directly encode zero historical collisions.
- It would make the leakage more explicit rather than safer.
- This option only becomes valid after `hgv_proportion` is joined from an
  all-link traffic source, where missingness means "no AADF coverage" rather
  than "no collision row".

## Recommendation

For the temporal ablation: drop current `hgv_proportion` from the baseline or
fix the all-link traffic feature join first. Do not run the ablation with the
current XGBoost `hgv_proportion` feature, because its missingness is tied to
historical collision presence.

For production: implement Option 2, then decide whether to impute remaining
true AADF-coverage gaps. After the join is fixed, rerun Stage 2 and the
rank-stability harness before interpreting any HGV or temporal-ablation lift.
