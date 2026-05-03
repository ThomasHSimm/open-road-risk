## 🟡 Medium Priority — Model

- [ ] Build a feature-audit script that runs the coverage-by-collision-history
  check across every Stage 2 feature, not just `hgv_proportion`. The HGV
  investigation found a real source-table/grain bug and fixed it; this audit
  is open work that could surface similar issues elsewhere.

- [ ] Consider: given consistent rank stability across feature additions
  (Jaccard >0.95 on each of RUC, tiered imputation), future feature work
  has diminishing returns on ranking vs structural modelling changes (EB
  shrinkage, facility-family split). Re-evaluate priority after 5-seed
  harness quantifies seed-level noise.

- [ ] Drop raw `betweenness` from GLM — coefficient is −8 which dominates the
      coefficient chart and is a multicollinearity symptom. Keep `betweenness_relative`
      which is the cleaner feature. XGBoost handles both fine via tree splits.

- [ ] Validate AADT estimates on WebTRIS motorway corridors — compare predicted vs
  measured flow on M62/M1 as sense check. Currently evaluated only on AADF holdout.

- [ ] Stage 1c vehicle mix model — predict % HGV/LGV/car per link from road type +
  network features. Enables vehicle-type risk analysis on uncounted roads.

- [ ] Remove `smartmotorway`, `parentlinkref`, `enddate` from any feature derivation
  lists — all empty (100% null) in current Network Model GDB release.

- [ ] Test exposure-as-offset vs exposure-as-feature in Stage 2 GLM —
  current implementation uses `log(AADT × length_km × 365 / 1e6)` as
  fixed offset (forces β_AADT = β_length = 1). Re-fit GLM with
  `log(AADT)` and `log(length)` as features and compare. SPF literature
  suggests β_AADT ≈ 0.7-0.9 is typical; if confirmed, the offset
  formulation distorts predictions at AADT extremes (over-predicts at
  high AADT, under-predicts at low). XGBoost partly compensates via
  `estimated_aadt` as a feature on top of the offset, but a cleaner
  formulation is preferable. Affects ranking interpretation: motorways
  may rank higher than they should, unclassified roads lower. Document
  result on methodology page regardless of outcome.

- [ ] Test for Poisson overdispersion in Stage 2 — compute
  variance/mean ratio of `collision_count`. If > ~1.5, switch GLM to
  Negative Binomial via `sm.families.NegativeBinomial(alpha=...)`.
  Independent of the offset/feature decision: NB mostly affects
  standard errors and inference, not point estimates. Do in the same
  session as the offset experiment since the data inspection overlaps.

- [ ] Tighten Stage 1a feature selection against `network_features.parquet`
  drift. `build_aadt_features()` in `aadt.py` currently appends every
  non-`link_id` column from the parquet, so retraining silently absorbs
  whatever has been added since the last train (RUC strings, IMD deciles,
  grade columns, future additions). Inference is safe — `aadt_model.pkl`
  carries its own saved feature list — but a retrain would change feature
  membership without an explicit decision. Replace append-all with an
  explicit allowlist (mirroring `network_candidates` in `collision.py`)
  and log added/dropped columns at training time so feature drift is
  visible. Address before any deliberate Stage 1a retrain.

- [ ] Investigate the negative `mean_grade` coefficient (final May 2026
  run: −0.0202, significant). Sign is opposite to SPF-literature prior.
  Diagnostic: does sign hold within road class? Hypotheses include
  rural-minor selection, driver compensation on grades, or grade acting
  as a proxy for unmodelled features (lighting, lane width). See
  `todo/feature_addition_imd_grade.md §6.1`.

- [ ] Collapse the three identical IMD missingness flags into a single
  `imd_missing`. The Welsh-LSOA gap is identical across `imd_decile`,
  `imd_crime_decile`, and `imd_living_indoor_decile`, so the per-feature
  `_missing` columns are perfectly collinear (all reported as −1.6258 in
  the final GLM coefficient table). Cosmetic only; saves ~30MB.

- [x] Document `score_collision_models` mutation contract. After the
  May 2026 chunked-scoring rewrite, the function no longer copies its
  input. Verify no other callers depend on non-mutation; document the
  new contract in the docstring.

- [ ] Run the family-residual diagnostic against final post-grade
  `risk_scores.parquet` to test whether mean grade specifically shrinks
  the motorway under-prediction. The original justification for adding
  grade was the family-split work's ~−3.3 motorway residual. The IMD+grade
  writeup notes this test was deferred (`todo/feature_addition_imd_grade.md §6.3`).

- [ ] Decide and implement memory strategy for future feature additions.
  Current pipeline at ~85% of 32 GB ceiling after IMD+grade; chunked
  scoring already added (was load-bearing, not nice-to-have); future
  additions will hit limits. Recommended approach (see
  `todo/feature_addition_imd_grade.md §7` for full reasoning):
  **stratified XGBoost training sample** (positive cases + AADT/road-class/
  region-stratified zero sample) as the next near-term move, with the
  full chunked scoring path retained for ranking output. Compare ranking
  stability against a one-off full-data confirmation run. Cloud VM
  (64–128 GB) reserved as emergency lever for full-data inference when
  needed for a write-up. Out-of-core (Polars + sklearn `PoissonRegressor`)
  is the long-term platform shift if memory keeps biting; significant
  refactor with real interpretability tradeoffs. Region-split modelling
  rejected — no road-safety prior, lots of stitching pain. Link-grain
  collapse rejected as a memory fix — it changes the estimand, treat as
  a separate modelling experiment.
