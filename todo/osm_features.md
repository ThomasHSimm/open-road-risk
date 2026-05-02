### OSM features with road-class-tiered imputation

**Context:** Current OSM coverage (`speed_limit_mph` 56%, `lanes` 7%,
`is_unpaved` 16%) is too low for global inclusion as-is. Median imputation

**Additional context (23 April 2026):** OSM speed_limit_mph at 56.4%
coverage is currently causing GLM training-set shrinkage to 10.9M rows
due to coverage-threshold edge case in train_collision_glm(). Tiered
imputation will restore full coverage and eliminate the issue. See
reports/stage2_base_table_investigation.md.
injects bias. Tiered imputation by road class (UK legal defaults) with
explicit `_imputed` flags may rescue these features for A-roads and B-roads
where coverage is moderate. Expectation: the feature becomes *not broken* on
minor roads, with the real signal living in the explicit-tag subset where
`_imputed=0`.

**Decisions already made:**
- Keyed off OS Open Roads `road_classification`, not OSM `highway`.
  Consistent with rest of pipeline.
- UK-specific defaults in mph: Motorway 70, A Road (dual/trunk) 70, A Road
  (single) 60, B Road 60 rural / 30 urban, Unclassified 30 (built-up
  assumption), with urban/rural proxied via `pop_density_per_km2`.
- Lanes defaults: Motorway dual 3, A dual 2, A single 1, B/Unclassified 1.
  One-way adjustment: where one-way indicated, divide by 2, clip to 1 min.
- `is_unpaved` default = False for Motorway/A/B/Unclassified.
- Three `_imputed` binary flags so the model can distinguish explicit-tag
  rows from imputed rows.
- Keep existing regex parser in `network_features.py` for explicit OSM tags.
- Check correlation between imputed `speed_limit_mph` and `road_class_ord`
  before committing; if r > 0.9, drop from GLM, keep in XGBoost.

**Prompt:**
[Draft when ready to run. Should include: specific default values keyed
off OS Open Roads road_classification, one-way adjustment for lanes,
_imputed flag per feature, UK-defaults verification step, correlation
check pre-GLM, methodology-page update documenting the imputation scheme
and its limits.]

**Expected outcomes:**
- `speed_limit_mph` becomes a usable feature with ~100% coverage (explicit
  tags + tiered defaults).
- `lanes` becomes near-constant within class after imputation. Limited
  predictive lift but no longer an imputation-artefact.
- `is_unpaved` becomes a rare-event flag; if a road IS explicitly tagged
  unpaved, that's real signal on unclassified roads.
- Modest pseudo-R² improvement (0.01–0.03) plausible but not guaranteed;
  rank stability of top-1% is the better evaluation.
- Correlation check may reveal the imputed features duplicate `road_class_ord`
  — in which case they add little to the GLM but may still help XGBoost
  via interaction with explicit-tag rows.

---

