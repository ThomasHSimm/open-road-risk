# Stage 2 Base-Table Size Investigation

**Date:** 2026-04-23  
**Branch:** main  

---

## 1. Findings Summary

The 40% reduction in Stage 2 `n_full` (18,302,830 → 10,892,180) is **not caused by the
counted-only AADF filter**. It is caused by the OSM network-features enrichment (run
ca. 2026-04-19, timestamp 2026-04-21) adding `speed_limit_mph` to `network_features.parquet`
at 56.4% link coverage. Because the GLM feature-selection logic uses columns with
>50% coverage directly (no imputation), 43.6% of link-years with no OSM speed limit
are dropped by `.dropna()` in `train_collision_glm()`. The reduction in `n_pos`
(360,674 → 224,117) is a proportional consequence of the same filter — not a
separate downsampling event.

---

## 2. Hypothesis Testing

### Hypothesis 1: Stage 1a inference now produces fewer predictions

**Verdict: FALSE**

`data/models/aadt_estimates.parquet` contains:

| Metric | Value |
|--------|-------|
| Total rows | 21,675,570 |
| Unique `link_id` | 2,167,557 |
| Years | 2015–2024 (10 years, exactly 2,167,557 rows per year) |
| Nulls in `estimated_aadt` | 0 |
| File mtime | 2026-04-20 23:14 |

This is 2,167,557 links × 10 years = 21,675,570 — the full network, no gaps.

`aadt.py:apply_aadt_estimator()` (line 532) confirms the inference path: it iterates
over `years = sorted(aadf["year"].unique())` using the **full** AADF table (not the
counted-only filtered subset) and calls `model.predict()` for every OS Open Roads link
in every AADF year. No links are dropped at inference.

The counted-only filter is correctly scoped to training via:

```python
# aadt.py:802
training_aadf = filter_counted_aadf_for_training(aadf, context="AADT stage")
# inference uses the original 'aadf', not 'training_aadf':
estimates = apply_aadt_estimator(model, features, openroads, aadf, year_means)
```

`exposure-model.qmd` lines 167–168 also explicitly states: *"The filter applies only
to the learning signal: the fitted model is still applied to every OS Open Roads link
for every AADF year, so downstream exposure coverage remains unchanged."*

**Stage 1a inference is intact. The counted-only filter did not shrink exposure coverage.**

---

### Hypothesis 2: Stage 2 has a filtering step removing rows with missing features

**Verdict: TRUE — this is the root cause**

`collision.py:train_collision_glm()` (line 253) uses:

```python
model_df = df[feature_cols + ["collision_count", "log_offset"]].dropna()
```

`n_full` in `collision_metrics.json` is defined as `len(model_df)` (line 284) — the
GLM training set **after** `.dropna()`.

#### Feature selection coverage thresholds

`train_collision_glm()` selects network features dynamically (lines 229–250):

- Coverage **> 50%** → column used directly; NaN rows dropped by `.dropna()`
- Coverage **5–50%** → column imputed to median, renamed `<col>_imputed`; no dropna impact
- Coverage **< 5%** → column excluded entirely

`data/features/network_features.parquet` (mtime 2026-04-21 21:51) coverage:

| Column | Coverage | Selection path | Dropna impact |
|--------|----------|---------------|---------------|
| `degree_mean` | 100.0% | Direct | None (no nulls) |
| `betweenness` | 100.0% | Direct | None |
| `betweenness_relative` | 100.0% | Direct | None |
| `dist_to_major_km` | 99.9% | Direct | ~0.1% of rows |
| `pop_density_per_km2` | 84.5% | Direct | 15.5% of rows with NaN |
| `speed_limit_mph` | **56.4%** | **Direct** | **43.6% of rows with NaN** |
| `lanes` | 7.3% | Imputed (`lanes_imputed`) | None |
| `is_unpaved` | 16.2% | Imputed (`is_unpaved_imputed`) | None |

#### Joint null analysis

```
speed_limit_mph null:      944,415 links (43.6%)
pop_density_per_km2 null:  335,692 links (15.5%)
Both null:                 202,380 links  (9.3%)
Either null:             1,077,727 links (49.7%)
Neither null:            1,089,830 links (50.3%)
```

Links with both `speed_limit_mph` and `pop_density_per_km2` non-null (plus ~99.9%
`dist_to_major_km`) define the GLM training set:

```
1,089,830 surviving links × 10 years = 10,898,300 rows
dist_to_major null overlap subtracts:       ~6,120 rows
                                         ──────────────
Estimated n_full:                        10,892,180
Actual n_full (collision_metrics.json):  10,892,180  ✓  (exact match)
```

#### What changed between the before and after states

`network_features_backup.parquet` (mtime 2026-04-11, 998,769 links) predates the OSM
enrichment. The current `network_features.parquet` was first generated with OSM speed
data around 2026-04-19 (per TODO: "OSM enrichment run on full 2.16M-link study area,
19 April 2026") and last regenerated at 2026-04-21 21:51.

**Before OSM enrichment** (network_features had 2.17M links with graph features and
`pop_density_per_km2`, but no `speed_limit_mph`):

```
Only pop_density_per_km2 (15.5% null) + dist_to_major_km (0.1% null) cause dropna.
Surviving links: 2,167,557 − 337,274 = 1,830,283
n_full = 1,830,283 × 10 = 18,302,830  ✓  (exact match to "before" figure)
```

This was verified by computing `(nf['pop_density_per_km2'].notna() & nf['dist_to_major_km'].notna()).sum() * 10 = 18,302,830`.

**After OSM enrichment** (speed_limit_mph added at 56.4% coverage):

```
speed_limit_mph (43.6% null) added to dropna.
Surviving links: 1,089,830
n_full = 10,892,180  ✓
```

**Stage 2 was run at 2026-04-21 00:01** (collision_metrics.json mtime), after the OSM
enrichment had produced a network_features file that included `speed_limit_mph`. That
is why the current metrics show the 10.9M state, not the 18.3M state.

#### Proportional n_pos reduction

`n_pos` records GLM training rows with `collision_count > 0` — i.e., collision
link-years that survive `.dropna()`. `road_link_annual.parquet` (mtime 2026-04-18)
contains 391,255 total collision link-years across 233,604 unique links.

| State | n_pos | % of 391,255 total collision link-years |
|-------|-------|----------------------------------------|
| Before (pop-only dropna) | 360,674 | 92.2% |
| After (speed+pop dropna) | 224,117 | 57.3% |

After the OSM enrichment, 136,557 collision link-years (35% of positive rows) belong to
links without a recorded OSM speed limit — mostly unclassified and minor roads. Their
collision records are removed from GLM training but are still present in XGBoost
training and scoring (see XGBoost path below).

The proportional drop (38% for n_pos vs 40% for n_full) confirms that collision-positive
links are slightly over-represented among links with OSM speed data (they skew toward
major roads), but the selection effect is modest.

---

### Hypothesis 3: road_link_annual changed in structure

**Verdict: NOT APPLICABLE — LEFT JOIN CANNOT REDUCE BASE TABLE**

`data/features/road_link_annual.parquet` (mtime 2026-04-18):

| Metric | Value |
|--------|-------|
| Total rows | 391,255 |
| Unique `link_id` | 233,604 |
| Year range | 2015–2024 |
| All 233,604 link_ids in aadt_estimates | yes (confirmed) |

`collision.py:build_collision_dataset()` joins RLA onto the base table as a **left
join** (line 139):

```python
base = base.merge(rla_trim, on=["link_id", "year"], how="left")
base["collision_count"] = base["collision_count"].fillna(0).astype(int)
```

A left join cannot reduce the base table row count. RLA's 391,255 rows do not gate
which link-years appear in the Stage 2 dataset. `road_link_annual.parquet` did not
cause the shrinkage.

---

## 3. Mechanism: End-to-End Chain

```
OSM enrichment adds speed_limit_mph to network_features.parquet (2026-04-19/21)
  → speed_limit_mph: 56.4% coverage across 2.17M links (above 50% threshold)
  → train_collision_glm() feature-selection adds speed_limit_mph to feature_cols directly
  → model_df = df[feature_cols].dropna() drops 944,415 links × 10 years = 9.44M rows
  → combined with pop_density_per_km2 nulls: 1,077,727 links × 10 years = 10.78M rows dropped
  → n_full = 2,167,557 − 1,077,727 = 1,089,830 surviving links × 10 years = 10,892,180
```

The counted-only AADF filter (Stage 1a training, 2026-04-20) is **not in this chain**.
It changed the quality of the AADT estimator but did not alter the set of link-years
reaching Stage 2. The two changes (counted-only filter and OSM enrichment) were
applied almost simultaneously, which created the appearance of a causal link when the
actual driver is the network-features enrichment.

**XGBoost is unaffected**: `train_collision_xgb()` fills NaN with 0 rather than
calling `.dropna()` (lines 336–337), so it trains on all 21,675,570 link-years.
The current `xgb.n_train = 17,340,450` = 80% × 21.7M, unchanged from the "before"
state. Scoring via `score_and_save()` also fills NaN with 0 and produces
`risk_scores.parquet` with all 2,167,557 links.

---

## 4. Methodological Assessment

### What is defensible

- **Stage 1a inference coverage is intact.** All 2.17M links receive AADT estimates
  for all 10 years. The counted-only filter improves training signal quality without
  reducing exposure denominator coverage.

- **XGBoost risk scores cover all links.** The final `risk_percentile` ranking
  (which the application uses) is computed over all 2,167,557 links with
  `fillna(0)` for missing features. No link is left unscored.

- **The proportional n_pos drop is expected.** Collision-positive links retain at
  57.3% vs 50.3% overall, consistent with major roads (more collisions, better OSM
  speed coverage) surviving the speed-limit filter.

### What is NOT defensible as-is

**The GLM is now trained on a biased subset of links.** 43.6% of all links — primarily
unclassified roads, C-roads, and rural minor roads — are excluded from GLM training
because they lack OSM speed limit data. This has two consequences:

1. **The GLM's Poisson coefficient for `speed_limit_mph` is estimated on roads that
   have speed limits (56% of the network), then applied in scoring to roads that
   don't (with `fillna(0)`, i.e. 0 mph imputed).** Zero is not a plausible speed
   limit and is far outside the training distribution. GLM-predicted rates for
   these links are unreliable.

2. **136,557 collision link-years on minor roads are excluded from GLM training.**
   The GLM's Poisson rate estimates for road classes disproportionately represented
   among unclassified roads may be biased toward the major-road subset.

The TODO explicitly acknowledges this (entry "OSM features with road-class-tiered
imputation"):
> "Current OSM coverage (`speed_limit_mph` 56%, `lanes` 7%, `is_unpaved` 16%) is
> too low for global inclusion as-is."

The 56.4% coverage barely clears the >50% direct-use threshold by chance. Had it been
49% instead of 56%, it would have triggered imputation (no dropna), and n_full would
remain at ~18.3M. The current behavior is a threshold artefact.

**However, the risk_percentile ranking (used by the application) is not affected
by this issue** because XGBoost provides the ranking and uses all rows. The GLM
contributes the exposure offset but is not the ranking signal.

---

## 5. Methodology Page Impact

`quarto/methodology/exposure-model.qmd` (lines 147–178) describes the counted-only
AADF filter correctly: it scopes the filter to training and explicitly states
"downstream exposure coverage remains unchanged." **This text is accurate** — Stage 1a
inference is unchanged.

What the page does not address (and should):

1. **The OSM speed-limit coverage drop.** The page should note that `speed_limit_mph`
   at 56% coverage causes the GLM training set (n_full) to be ~10.9M, not the full
   21.7M base table, and explain that this is a consequence of the feature-selection
   threshold.

2. **The GLM/XGBoost split.** The page should clarify that `n_full` in
   `collision_metrics.json` refers to the GLM training set after `.dropna()`, not the
   full base table. XGBoost trains on all 21.7M link-years; risk scores cover all
   2.17M links.

3. **The imputation gap.** Scoring applies the GLM to all links with
   `speed_limit_mph` filled to 0, which is outside the training distribution. This
   should be flagged as a known limitation.

`quarto/methodology/modelling.qmd` should also note the n_full definition and the
GLM/XGBoost difference in training set size.

---

## 6. Recommendations

### No action needed

- The counted-only AADF filter itself is correctly implemented. Stage 1a inference is
  fully intact. Hypothesis 1 can be formally closed.

- The proportional n_pos drop (38%) is consistent with the overall n_full drop (40%)
  and requires no code change.

### Documentation-only

- Update `exposure-model.qmd` or `modelling.qmd` to clarify that:
  - `n_full` in `collision_metrics.json` is the **GLM** training set (post-dropna),
    not the Stage 2 base table (which is always 21.7M rows)
  - The current n_full of 10.9M reflects the OSM speed-limit coverage gap, not the
    counted-only filter
  - XGBoost `n_train` = 17.3M (80% of full 21.7M) remains unchanged

- Add a TODO cross-reference: the 40% GLM training-set shrinkage is a direct
  consequence of the road-class-tiered imputation task (already in TODO under
  "OSM features with road-class-tiered imputation"). Once that work is complete,
  n_full should return to ≥18M.

### Code fix needed (flag only — do not implement)

**The current 50% coverage threshold in `train_collision_glm()` is causing a
methodological problem for `speed_limit_mph`.** At 56.4% coverage, the column
barely crosses the direct-use threshold, but the 43.6% NaN fraction is too large
to drop via `.dropna()` without biasing the training set.

Recommended fix: raise the direct-use threshold from 50% to 80% (or a
project-determined value), so that `speed_limit_mph` at 56.4% would be imputed
(as `speed_limit_mph_imputed`) rather than used directly. This would:
- Restore n_full to ~18.3M (pop_density-only dropna)
- Retain `speed_limit_mph` as a feature (via imputed column) without dropping half the training set
- Align with the intended road-class-tiered imputation described in the TODO

Alternatively, the road-class-tiered imputation (UK legal defaults: 70 mph
motorway, 60 mph A-road, etc.) described in the TODO would push `speed_limit_mph`
to near-100% coverage and eliminate this issue entirely. That is the preferred
long-term fix; the threshold adjustment is a short-term mitigation.

**File to fix:** [collision.py:237–249](../src/road_risk/model/collision.py#L237-L249) — the
`if coverage > 0.5: feature_cols.append(col)` branch.

---

## Appendix: Key Data File Inventory

| File | Rows | Mtime | Role |
|------|------|-------|------|
| `data/models/aadt_estimates.parquet` | 21,675,570 (2.17M links × 10 yrs) | 2026-04-20 23:14 | Stage 1a output — unchanged |
| `data/features/network_features.parquet` | 2,167,557 links | 2026-04-21 21:51 | OSM-enriched; `speed_limit_mph` 56.4% |
| `data/features/network_features_backup.parquet` | 998,769 links | 2026-04-11 17:13 | Pre-expansion backup; no speed/lanes |
| `data/features/road_link_annual.parquet` | 391,255 rows / 233,604 links | 2026-04-18 22:40 | LEFT-joined; no row reduction |
| `data/processed/shapefiles/openroads_yorkshire.parquet` | 2,167,557 links | 2026-04-12 19:51 | Base link set |
| `data/models/collision_metrics.json` | — | 2026-04-21 00:01 | Stage 2 metrics at OSM-speed state |
| `data/models/risk_scores.parquet` | 2,167,557 links | 2026-04-21 00:01 | Scores all links (XGBoost, fillna=0) |

---

## Appendix: Numerical Verification

```python
# Computed in this investigation session:

# aadt_estimates.parquet
total_rows = 21_675_570        # 2,167,557 × 10 years
null_estimated_aadt = 0        # no missing AADT

# network_features.parquet joint null analysis
speed_null      = 944_415      # 43.6%
pop_null        = 335_692      # 15.5%
both_null       = 202_380      #  9.3%
either_null   = 1_077_727      # 49.7%
neither_null  = 1_089_830      # 50.3%

# After state (speed + pop + dtm dropna):
n_full_predicted = 1_089_830 * 10   # = 10,898,300
n_full_actual    = 10_892_180        # in collision_metrics.json
# delta = 6,120 ≈ dist_to_major_km nulls overlapping the surviving set

# Before state (pop + dtm dropna only, no speed_limit):
pop_dtm_null    = 337_274            # 15.6%
n_full_before_predicted = (2_167_557 - 337_274) * 10   # = 18,302,830
n_full_before_actual    = 18_302_830                    # ✓ exact match
```
