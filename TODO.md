# TODO

Tracked here so nothing gets lost. Cross off as done.

---

## 🔴 High Priority

- [ ] Fix temporal trend chart in `03_model_results.ipynb` — observed collision bars
  are invisible because the y-axis is dominated by the predicted × 1000 line. Either
  drop the ×1000 scaling or use a secondary y-axis.

- [ ] Fix middle panel in risk score distribution plot (section 5) — flat uniform
  distribution because it's plotting risk_percentile which is by construction uniform.
  Replace with collision count distribution on collision links instead.

- [ ] Stage 1a geometry fallback — EPSG:27700 transform was
  returning non-finite values in some environments, triggering a BNG coordinate
  fallback in `aadt.py`. Root cause not established. Fallback trigger counts
  are now logged and `docs/internal/aadt_geometry_issue.md` documents the
  observed failure mode; compare against an environment where EPSG:27700 works
  normally and decide whether the fallback should be a permanent path or a
  guarded workaround.

- [ ] Fix `pct_attribute_snapped` in `road_link_annual` — always 0 because snap
  method name changed to "weighted". Column is misleading, should be removed or
  recalculated as `pct_weighted_snapped`.

---

## 🟡 Medium Priority — Model

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
  future additions). Inference is safe — `aadt_model.pkl` carries its own
  saved feature list — but a retrain would change feature membership
  without an explicit decision. Replace append-all with an explicit
  allowlist (mirroring `network_candidates` in `collision.py:246`) and log
  added/dropped columns at training time so feature drift is visible.
  Address before any deliberate Stage 1a retrain.

---

## 🟢 Infrastructure / Output

- [ ] `db.py` — PostGIS loader for all processed parquets + model outputs. Required
  for Streamlit app queries.

- [ ] Streamlit app skeleton — map with road links coloured by risk percentile,
  sidebar filters for road type / year / severity.

- [ ] GeoPackage export — ESRI-compatible output layer (link_id, geometry,
  estimated_aadt, risk_percentile, road_classification). Useful.

- [ ] `data/README.md` — download instructions for all large raw files not in git
  (STATS19 CSV, OS Open Roads GeoPackage, AADF zip, OSM pbf files, MRDB).

- [ ] Add "Related work / where this fits" page — short, written from
  your perspective with verified citations. Position project relative
  to Lovelace / Leeds ITS active travel work, any UK SPF-style work
  surfaced by OS conversation, and proprietary commercial work. Wait
  until after OS contact response so the page reflects specific
  references rather than generic ecosystem framing.

- [ ] Kaggle dataset — upload processed parquets so others can skip ingest/clean/snap.

- [ ] Provenance directory restructure (small session) — move
  `curvature_provenance.json`, `ruc_provenance.json`,
  `speed_limit_effective_provenance.json` from `data/features/` to
  `data/provenance/`. Update code paths that write these. gitignore
  already allow-lists the directory.

- [ ] Minimal CI workflow — add GitHub Actions for PRs and pushes to `main`
  running `pytest -x --tb=short` and `ruff check`. Do not run the full
  pipeline in CI: it is too slow and depends on raw data not stored in git.

- [ ] `config/model.yaml` migration — split model/runtime constants out of
  `config/settings.yaml`. Create `config/model.yaml`, migrate
  `RANDOM_STATE = 42` and `COVID_YEARS = {2020, 2021}`, and update
  `config.py` to load both YAML files with consistent fail-loud errors.
  `clean.py` currently reads COVID years from `cfg["years"]["covid"]`;
  after migration, `model/constants.py` should become the canonical model-side
  source.

- [ ] Add argparse to pipeline entrypoints — `python -m road_risk.<module> --help`
  should print usage rather than running the pipeline. Cover entrypoints in
  `clean_join/`, `ingest/`, `model/`, and `features/`; support `--help`,
  `--dry-run`, and module-specific arguments.

- [ ] Fix STATS19 expected-column validation timing — `ingest_stats19.py`
  currently warns that `collision_date` is missing because `EXPECTED_COLS`
  uses post-rename names while validation runs before rename. Either validate
  pre-rename names (`date`) or move validation after rename. Low priority:
  warning only, no current breakage.

- [ ] Add smoke tests for ingest/clean/model modules — current tests mainly
  cover feature engineering. Add synthetic-fixture tests for
  `ingest_stats19.load_stats19()` and clean/model entrypoints so config/path
  refactors do not rely only on manual end-to-end runs. Keep tests fast and
  CI-compatible; avoid real raw-data dependencies.

- [ ] Force-area vs bbox coverage audit — current STATS19 filtering combines
  `police_force` membership with coordinate bbox clipping. Audit listed force
  areas against `study_area.bbox_wgs84`, identify partially clipped forces
  such as Cheshire/Lincolnshire if present, and either expand the bbox or
  document intentional partial coverage. Force boundaries are available from
  data.police.uk.

- [ ] Derive `bbox_bng` from `bbox_wgs84` — settings currently stores both
  coordinate systems by hand, creating drift risk. Keep one source of truth
  (probably WGS84) and derive BNG bounds in code via `pyproj`. Low priority:
  current values work, but this is config hygiene.

- [ ] Add YAML schema validation when config complexity justifies it — use
  Pydantic for `settings.yaml` and future `config/model.yaml` once settings
  exceeds ~100 lines or after the next config-related debugging session.
  Below that threshold, schema overhead likely outweighs benefit.

- [ ] Logger integration and print triage — `road_risk.utils.logger` now supports
  file logging under `_ROOT/logs/`, but entrypoints still mostly use local
  `logging.basicConfig()` and many run summaries use `print()`. Decide which
  prints are CLI-only versus run diagnostics, then route important summaries
  through the logger.

---

## 🔵 Applications / Demonstrations

- [ ] Risk-normalised output table — "Top 1% highest-risk road segments controlling
  for traffic" as a clean publishable output.

- [ ] Seasonal risk analysis — combine Stage 2 risk scores with Stage 1b temporal
  profiles. Do high-risk roads have worse seasonal variation?

- [ ] Stage 1b integration decision — keep `timezone_profiles.parquet` as a
  separate temporal output for now, then run an ablation before using time-zone
  fractions as Stage 2 exposure weights. This prevents the current all-day risk
  ranking and future temporal-risk ranking from being mixed accidentally.

---

## ⚪ Parked (investigated, deprioritised — with reason)

- **OSM global retrain without class-tiered imputation** — coverage diagnostic
  (19 April 2026) showed no column × road-class combination reaches 80% coverage.
  Median imputation at 5–16% true coverage injects bias that correlates with road
  class. See `quarto/analysis/osm-coverage.qmd`. Replaced by the road-class-tiered
  imputation task below.

- **OS MasterMap Highways (RAMI)** — blocked pending OS Data Hub licensing
  clarification on development-mode use for a public portfolio site. RAMI gives
  lanes and widths on the full GB network but "live application" vs "development
  mode" boundary is not defined clearly enough to commit. Revisit if OS Support
  responds with a specific answer permitting portfolio use.

- **Common-basis pseudo-R²** — deprioritised in favour of 5-seed rank stability
  (see queued tasks). Pseudo-R² isn't the operationally relevant metric; rank
  stability of the top-1% list is.

- **Strava Metro for active travel exposure** — technically free for researchers
  on application but not open data; redistribution of derivatives restricted.
  Portfolio publication friction outweighs benefit. Pedestrian/cyclist exposure
  gap remains open; potential alternative is DfT active travel statistics at
  LSOA level if needed.

- **SCRIM skid resistance** — National Highways collects pavement friction
  continuously but typically does not publish as open data due to liability
  concerns. Checked; no viable open source identified. Parked permanently unless
  a specific LA publishes their local surveys.

---

## ✅ Done

- [x] STATS19 ingestion (102,361 Yorkshire collisions 2015–2024, forces 12/13/14/16)
- [x] AADF ingestion (5,260 rows, 2019/2021/2023)
- [x] WebTRIS ingestion (6,516 site × year rows)
- [x] MRDB ingestion (1,948 Yorkshire major road links)
- [x] OS Open Roads ingestion (705,672 links, Yorkshire bbox)
- [x] **Force code bug fixed** — was loading Lancashire/NW England (codes 4–7),
      now correctly loads Yorkshire (codes 12/13/14/16). Pipeline re-run April 2026.
- [x] LSOA coordinate validation (146 flagged suspect, 0.1%)
- [x] Weighted multi-criteria snap (current full-area run ~99.8%, score 0.860)
- [x] Snap quality filter in join.py (score ≥ 0.6, retains 97% of matches)
- [x] `road_link_annual.parquet` (84,146 rows × 37 cols, 49,247 links, 2015–2024)
- [x] `network_features.py` — degree, betweenness, betweenness_relative,
      dist_to_major, pop_density, speed_limit_mph, lanes, lit, is_unpaved
- [x] `model.py` Stage 1a — AADT estimator (counted-only CV R² 0.831)
- [x] `model.py` Stage 1b — temporal profiles (WebTRIS seasonal indices)
- [x] `model.py` Stage 2 — Poisson GLM (pseudo-R² 0.251 after provenance
      hardening) + XGBoost (0.858)
- [x] `03_model_results.ipynb` — full model results notebook with maps
- [x] Retired stale STATS19 coordinate notebook — direct raw-data check found
      Yorkshire BNG fields agree with lat/lon-derived BNG positions within a
      few metres; notebook archived under `notebooks/old/`.
- [x] README.md, CODE_README.md, TODO.md — updated April 2026
- [x] Hardcoded values audit — documented in CODE_README with derivation sources
- [x] OSM features via osmnx + osmium (Geofabrik county pbf files, full study area)
- [x] Post-event column provenance guard (21 April 2026) — STATS19 contextual
      aggregates in join.py
      (`pct_urban`, `pct_dark`, `pct_junction`, `pct_near_crossing`,
      `mean_speed_limit`) are post-event diagnostics. `collision.py` excludes
      them from the Stage 2 modelling dataframe via `FORBIDDEN_POST_EVENT_COLS`
      and asserts GLM/XGBoost feature lists are clean pre-training. Columns are
      also removed from the `risk_scores.parquet` output contract and Streamlit
      app config. Synthetic smoke test verifies they are dropped even when
      present upstream; Stage 2 was rerun and the current `risk_scores.parquet`
      has no forbidden columns.
- [x] `_fix_sd_se_error()` removed from clean.py (April 2026)
- [x] Study area extended to NW England + Midlands (2,167,557 links, 203,928+ collisions)
- [x] XGBoost now drives risk_percentile (not GLM) — GroupShuffleSplit by link_id, R² 0.858
- [x] hgv_proportion added to XGBoost (not GLM — failed 50% coverage threshold)
- [x] QMD site: eda-traffic, model-results, eda-collisions
- [x] R² reconciliation (19 April 2026) — fixed stale values in model-results.qmd
      (0.22/0.31 → 0.269/0.858), README.md, CODE_README.md. Added pseudo-R²
      comparability note flagging that GLM in-sample on downsampled set vs
      XGBoost out-of-sample on true distribution. Superseded by the 21 April
      counted-only/provenance-guard run (GLM 0.251, XGBoost 0.858).
- [x] OSM cache-trap fix (19 April 2026) — `network_features.py` now detects
      missing OSM columns in existing cache and triggers recompute without
      needing `--force`. README quick-start collapsed to single `--osm` call.
- [x] OSM enrichment run on full 2.16M-link study area (19 April 2026) — with
      per-county checkpointing, gc.collect() between counties, trimmed slim
      parquets (refactor to avoid OOM after initial failure on North Yorkshire).
- [x] OSM coverage diagnostic (`quarto/analysis/osm-coverage.qmd`, 19 April 2026)
      — no column × road-class combination reaches 80% coverage; `lanes` at 4–7%
      on minor roads; `speed_limit_mph` highest at 56% overall but lowest on
      motorways (46%, near-constant where populated).
- [x] Model inventory (`quarto/methodology/model-inventory.qmd`, refreshed 21 April 2026) — durable
      baseline of current Stage 2 features, hyperparameters, and training rows.
- [x] Stage 2 base-table size investigation (23 April 2026) — 40% reduction
      in GLM n_full (18.3M → 10.9M) traced to OSM speed_limit_mph at 56.4%
      coverage crossing the 50% direct-use threshold in train_collision_glm(),
      causing dropna cascade. Not caused by counted-only AADF filter. XGBoost
      n_train unchanged (uses fillna=0), production risk_percentile ranking
      unaffected. See reports/stage2_base_table_investigation.md. Short-term
      fix: raise coverage threshold to 80%. Long-term fix: OSM tiered
      imputation (already queued).
- [x] Counted-only AADF filter for Stage 1a (19 April 2026) — CV R² 0.72→0.83,
      local holdout R² 0.776→0.832, spatial holdout R² 0.707→0.788. Dropped
      1,288 count points (9.1%) that are always Estimated across 2015-2024.
      Major/Minor skew 11.2% vs 4.6%; regional distribution approximately
      uniform, with Wales higher at 17% on a small sample. Documented in
      exposure-model.qmd. Weighted-Estimated training considered and rejected
      as methodologically arbitrary.
- [x] ~~Download additional AADF years~~ — stale; AADF ingest already loads full
      2015-2024 range. Real issue was counted-vs-estimated, now handled by the
      counted-only filter.
- [x] Empirical Bayes shrinkage for risk ranking (25 April 2026) — v1
  implemented with positive-event weighted MoM k ≈ 3.07. Session 1: dispersion
  strongly non-constant across predicted-risk range (k_bin varies ~3,400× from
  low- to high-prediction bins); global-k is a known-imperfect summary. Session 2:
  EB does regression-to-the-mean correction at prediction/observation extremes
  (top-1% intersection 84.93%, ~3,267 links each entering/leaving). Does NOT
  improve cross-seed top-k stability — seed-churn population moved at parity with
  general population under EB. Adopted as additional ranking (`risk_percentile_eb`),
  not a replacement for `risk_percentile`. 5-seed EB comparison deferred — single-run
  §6.4 already answered the relevant question. Per-family or per-bin EB recommended
  for v2, paired with planned facility-family split. Outputs:
  `src/road_risk/model/eb_{dispersion,shrinkage}.py`,
  `src/road_risk/diagnostics/eb_validation.py`,
  `data/models/risk_scores_eb.parquet`,
  `data/provenance/eb_dispersion_provenance.json`,
  `reports/eb_{dispersion,validation}.md`,
  `quarto/methodology/empirical-bayes-shrinkage.qmd`.
  Production `risk_scores.parquet` unchanged throughout. Open caveat: ~4%
  top-1% membership churn from MoM aggregation choice; production k logged in
  provenance JSON. Per-family k removes this ambiguity.
- [x] OSM tiered speed-limit imputation + Stage 2 retrain (24 April 2026) —
      `speed_limit_mph_effective` replaces raw OSM-only feature in model. Coverage
      91.27% (1.98M / 2.17M links) via `road_classification × ruc_urban_rural` lookup;
      raw `speed_limit_mph` preserved as OSM-tagged-only. GLM `n_full` recovered to
      18.3M (matches pre-OSM baseline), GLM pseudo-R² 0.251 → 0.301, XGBoost
      unchanged at 0.858. Top-1% Jaccard 0.951, Spearman 0.996 — ranking essentially
      stable. Methodology page and model inventory updated.
- [x] [DONE] Investigate and resolve 335,692 links (15.5%) with no
      LSOA-derived features — characterised as boundary/coastal/peripheral,
      biased toward minor/rural `road_function`, and 99% outside the active
      `road_link_annual` network. Filled via two-stage approach: 238,507 links
      (71%) by nearest LSOA centroid within 5 km; 97,185 links (29%) with
      rural-default fallback. `speed_limit_mph_effective` recomputed from new
      RUC values. Audit columns `ruc_imputed`, `ruc_fill_method`, and
      `ruc_nearest_lsoa21cd` added. Practical impact of rural-default fallback:
      993 active modelled links (~0.05% of network) carry the default rather
      than spatially inferred values. 1,194 links remain incomplete on
      `dist_to_major_km` (separate gap, not LSOA-derived; deferred). Reports:
      `reports/ruc_fill.md`, `reports/ruc_fill_verification.md`. Provenance:
      `data/provenance/ruc_fill_provenance.json`. Backup:
      `data/features/network_features_pre_ruc_fill.parquet`.
- [x] Methodology Feature summary table verified (24 April 2026) — Network row
      correctly references `speed_limit_mph_effective` not `speed_limit_mph`.
- [x] `.coverage` and `htmlcov/` already ignored in root `.gitignore` — no
      additional housekeeping change needed.
- [x] 5-seed GroupShuffleSplit for rank stability (25 April 2026) — XGBoost evaluated 
      across seeds 42-46. Pseudo-R² highly stable (0.8590 ± 0.0014). Top-1% Jaccard 
      averages 0.918. Narrow top-k cuts show expected fuzzy boundary churn, but full-rank 
      Spearman correlation remains >0.998. See `reports/rank_stability.md`.
- [x] Facility-family split for Stage 2 (25–26 April 2026) — Sessions 1 & 2 complete;
      sessions 3–4 deferred. Split network into Motorway (4,084 links), Trunk A, Other-Urban,
      and Other-Rural based on ONS RUC and road function. Stitched all-links pseudo-R² 0.895
      vs global 0.888; held-out link-grain 0.8898 vs 0.8892 (baseline 0.859 is link-year grain).
      Held-out link-year deltas: trunk_a +0.006, other_urban +0.001, other_rural +0.002 —
      within seed-noise of zero. Motorway delta reverses on held-out (−0.027 vs +0.052
      all-data): overfitting on ~4k-link training set; global model generalises better
      out-of-sample on motorway. Motorway mean residual +0.13 (global −3.3): calibration
      improvement is robust. Adoption decision: do not replace `risk_percentile` with
      stitched ranking; v1 outputs available diagnostically in `risk_scores_family.parquet`.
      Boundary discontinuity max gap 0.0047 — stitching is clean. v2 candidates: motorway
      hyperparameter reduction / partial pooling with trunk-A; per-family EB k; network
      topology features. See `reports/family_validation.md`,
      `quarto/methodology/facility-family-split.qmd §11`.

---

## Queued tasks with prompts

### MRDB ingest — confirm and clean up

Status: ingest pipeline runs but output is orphaned.

`ingest_mrdb.py` and `clean_mrdb()` produce `mrdb_clean.parquet` but nothing
downstream reads it. The actual AADF→link join in `join.py` uses
`sjoin_nearest` against OS Open Roads, not MRDB's `count_point_id` hard-link.
The docstring on `join.py` line 23 ("Joins AADF count point data onto MRDB
links via count_point_id") is stale — actual joins are spatial, on OS Open
Roads.

History (likely): OS Open Roads was added after MRDB and superseded it for
network geometry. MRDB-specific code path was deprecated but the ingest step
was never removed. Worth confirming via git log on `clean_join/join.py`.

Action:
- Confirm MRDB is genuinely unused (grep for any read of `mrdb_clean.parquet`
  outside of `clean.py`).
- If unused: remove `ingest_mrdb.py` from the pipeline run order in
  `README.md` and `CODE_README.md`. Delete or archive `ingest_mrdb.py` and
  the `clean_mrdb()` function in `clean.py`. Update the stale docstring
  on `join.py:23`.
- If used somewhere I missed: document the actual usage and update the
  methodology page (`data-joining.qmd`) to reflect it.

Public site has been updated separately to remove the MRDB data source page
(removed from `_quarto.yml`, page deleted). See `docs/internal/site-todo.md`.
---

### External iRAP-class benchmark (Victoria first, NZ/NSW second)

**Context:** Current validation is strong internally but still mostly within the
open-data stack. To make a stakeholder-facing claim that the model is more than
an interesting predictor, it needs an external benchmark against a recognised
road-infrastructure safety framework. The cleanest use of iRAP-class data is
not as a Stage 2 feature, but as a held-out benchmark for convergent validity.
This tests whether the open-data risk ranking agrees with accepted surveyed-road
safety ratings on the subset of roads where those ratings exist.

**Decisions already made:**
- Use iRAP / AusRAP / KiwiRAP **as benchmark only**, not as a production
  feature in Stage 2 v1. Avoids circularity and patchy-coverage bias.
- Benchmark against **vehicle Star Rating first**, not crash risk maps or FSI
  estimates. Star rating is the cleaner infrastructure-oriented label.
- Victoria is the first proving ground because the public AusRAP dataset appears
  machine-readable and pairs with open crash and traffic data.
- New South Wales is the next replication if the goal is low-friction external
  replication; New Zealand is the next replication if the goal is closest
  UK-like policy / institutional analogue.
- Compare on a **common benchmark section table** — do not join native OS Open
  Roads links directly to RAP segments and pretend they are the same unit.
- Report this as **convergent validity** / external benchmark evidence, not as
  proof the model "replaces iRAP".
- Keep internal validation work (future-years holdout, naïve `AADT × length`
  baseline, 5-seed stability, EB shrinkage) separate. External benchmark adds
  evidence; it does not rescue weak internal validity.

**Prompt:**

Draft a Quarto design doc at
`quarto/methodology/external-benchmark-irap.qmd`, NOT code.
I will review before any implementation.

The doc should cover:

1. Why iRAP-class data is a benchmark and not a training feature:
   - coverage mismatch on unsurveyed roads
   - circularity risk
   - distinction between infrastructure audit and realised-harm prediction

2. Benchmark geography choice:
   - Victoria as first benchmark
   - NSW as second benchmark for within-country replication
   - New Zealand as second benchmark for closest UK-like analogue
   - what exact public datasets are expected for each (RAP layer, crash data,
     traffic / AADT backbone)

3. Unit-of-analysis design:
   - define a common benchmark section table
   - options: provider section IDs vs fixed 100 m segmentation
   - length-weighted aggregation of link-year predictions onto benchmark sections
   - note that the benchmark must use surveyed-road geometry as reference, not
     raw OS Open Roads links as-if equivalent

4. Metrics to report:
   - Spearman or Kendall rank agreement between predicted risk and inverse star score
   - AUROC / PR-AUC for identifying 1–2 star sections
   - Quadratic-weighted kappa after binning predicted risk into 5 bands
   - share of top-x% predicted-risk length falling on 1–2 star roads
   - disagreement audit by quadrant:
     high predicted / low star,
     high predicted / high star,
     low predicted / low star,
     low predicted / high star

5. Diagnostic outputs:
   - map of true positives
   - map of informative disagreements
   - table of representative sections in each disagreement quadrant
   - note whether audited geometric fields (e.g. curvature, grade, lane width if
     present in the benchmark) broadly agree with model signal

6. Reporting and claims discipline:
   - exact wording for README / Quarto / slides
   - explicitly avoid “replacement for iRAP”
   - record RAP programme name, publication date, and model version so the
     comparison is robust to methodology drift

7. Dependency / execution note:
   - benchmark should be run alongside, not before, future-years holdout,
     naïve baseline, 5-seed stability, and EB shrinkage review
   - stop after the design doc; do not download data or implement joins yet

**Expected outcomes:**
- A credible external-validation story for surveyed roads without weakening the
  open-data positioning of the core model.
- Agreement should be meaningful but not perfect; informative disagreement is a
  feature, not necessarily a failure.
- Strongest likely public claim: the model aligns with an accepted
  infrastructure-safety framework on surveyed roads and can then be used as a
  network-wide triage layer on roads that are not routinely surveyed.
- If agreement is weak even after sensible benchmarking design, that is a real
  signal to revisit feature set / geometry / exposure assumptions before making
  stronger stakeholder claims.

---
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

**Parked decision - `lit`:** do not add OSM `lit` to Stage 2 for now.
Current `network_features.parquet` coverage is 90.7% null overall and 88.3%
null even on Urban links (`lit=True` 8.1%, `lit=False` 1.2% overall). This is
not just sparse coverage: the explicit tags appear selection-biased toward
roads where contributors bothered to tag lighting state, especially the
obviously-rural/unlit minority. A `lit_known` flag would mostly teach the
model OSM tagging behaviour, duplicating RUC/pop-density/road-class signal.
Revisit only if OSM coverage improves materially, or if there is a specific
diagnostic question about explicitly tagged-and-unlit links as their own class.

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

### Network Model GDB integration (SRN-only)

**Context:** National Highways Network Model Public download provides
authoritative lane counts and structural attributes for ~42,960 SRN links
(motorways + trunk A-roads), covering ~14,000 of the 21,676 top-1% risk
links. Open Government Licence; no friction. Speed limit removed pending
validation — not available here. SRN-only coverage means this is
facility-family-conditional by construction; integrating it well means
using it *within* a facility-family split, not as a global feature with
NaN-everywhere-else.

**Decisions already made:**
- Queue as dependency of facility-family split, not independent retrain.
  Integrating before the split means wrestling with 95%-missing features
  — the same bias problem OSM had.
- Join via TOID where available (96.45% complete); spatial-join fallback
  for the ~3.5% missing (~1,500 links).
- Useful features: `numberoflanes`, `carriageway`, `srn` flag,
  `startgradeseparation`, `endgradeseparation`, turn/access/vehicle
  restriction counts per link.
- Skip empty columns: `smartmotorway`, `parentlinkref`, `enddate`, and
  `Speed_Limit` layer (0 rows).
- Validity dates: Network Model startdates only go back to 2020 (~75 links)
  with most from 2022 onwards. Do NOT use as evidence of physical road
  presence for pre-2020 modelling years. Use OS Open Roads as truth for
  pre-2020 link existence.

**Prompt:**
[Draft when ready. Should depend on facility-family split work being done
first. Should include: join via TOID with spatial-join fallback, feature
extraction from Link layer + Lane-summary aggregation, exclusion of empty
columns, join quality diagnostics (how many of the expected ~14k top-1%
links got enriched), methodology-page update describing the authoritative
SRN feature set.]

**Expected outcomes:**
- Clean authoritative lane counts on motorway + trunk A model in the
  facility-family split.
- Modest predictive improvement on the SRN model; no impact on other classes.
- Methodology story: "authoritative lanes on SRN, imputed defaults elsewhere."

---

### Curvature from OS Open Roads geometry

**Context:** Curve geometry correlates with run-off-road crashes and
severity per the literature. OS does not publish curvature as an attribute;
neither does OSM cleanly (OSM node density is unreliable for curvature
derivation). OS Open Roads provides LineString geometry — survey-grade
accuracy, universal coverage — from which curvature can be computed by
resampling. Major win because it's universal coverage, no licensing, no
imputation.

**Decisions already made:**
- Resample geometry to fixed spacing (10–25m, TBD after vertex-density
  check), compute turning angle at each interior point, summarise per link.
- Features: `mean_curvature_deg_per_km`, `max_curvature_deg_per_km`, `sinuosity` (length /
  straight-line distance).
- Before committing: verify vertex density on OS Open Roads per road class.
  If Unclassified is sparsely vertexed, curvature feature will be near-zero
  noise on 1.06M links and should be flagged as minor-road-degraded.
- OS Open Roads simplifies at 1:25,000. Curvature values will be conservative
  relative to survey-grade. Acceptable for ranking purposes; document in
  methodology.

**Prompt:**

Pre-check step first:

1. Load `openroads_yorkshire.parquet` or current network parquet.
2. Compute `vertices_per_km` per link:
   `len(geometry.coords) / (length / 1000)`.
3. Summarise by `road_classification` using `describe()`.
4. Report the distribution.

Based on the vertex density result, propose either:

1. Compute curvature features across all road classes as a universal-coverage
   feature.
2. Compute curvature only on classes where vertex density is adequate
   (threshold TBD from the data); flag as NaN for others.

Then implement the chosen path:

1. Resample each LineString to 15m spacing (tunable).
2. Compute turning angle per interior sample point.
3. Per-link features:
   - `mean_curvature_deg_per_km`
   - `max_curvature_deg_per_km`
   - `sinuosity` (`link_length / straight_line_length`)
4. Add to `network_features.parquet` as new columns.
5. Report how many links get non-null curvature values and distribution.

Do not retrain the collision model yet. This is feature engineering only.

**Expected outcomes:**
- Universal or near-universal coverage depending on vertex density.
- Curvature features rank links sensibly even if absolute values are
  conservative (OS Open Roads simplification).
- Adds the geometric risk signal missing from current feature set.

---

### Grade from OS Terrain 50 DEM

**Status:** Designed, partially set up, not implemented. Deep research 
report at <path or location>. OS Terrain 50 ASCII grid downloaded but 
[unzip / VRT build status unknown — verify before next session]. 
road_terrain.py listed in README repo structure but [file may or may 
not exist — verify].

**Approach (from deep research):**
- OS Terrain 50 ASCII grid (NOT GeoPackage — that's the contour product)
- Build VRT via gdalbuildvrt over ~2,858 tiles in 55 folders
- Bilinear interpolation against the raster (NOT rasterio.sample() 
  nearest-neighbour, which produces edge artefacts on a 50m grid)
- Sample at same 15m point spacing as curvature features
- Compute slope over 45-60m effective baseline (3-4 sample steps), 
  not consecutive 15m pairs — the 50m DEM doesn't support 15m 
  resolution
- Features: mean_grade_pct (length-weighted absolute), 
  max_grade_pct, grade_change_m
- Use magnitudes not signed values (link direction often arbitrary)
- 4m RMSE on heights, 50m cell spacing — feature is rank-preserving, 
  amplitude-conservative

**Structure handling — open design decision:**
Bridges, tunnels, AND slip roads need special handling because the 
DTM removes supported structures and reports ground level under/over 
them. Slip roads on grade-separated junctions are particularly 
problematic — the DTM has no way to know which level a link is on.

Two paths considered:
1. OSM bridge/tunnel tags (bridge=*, tunnel=*, covered=*) joined 
   to links, endpoint-fallback grade where flagged. Requires 
   extending OSM extraction in network.py to capture these tags.
2. OS Open Roads form_of_way to identify slip roads, endpoint-
   fallback for those. Uses authoritative network metadata; doesn't 
   need OSM extension; but only catches slip roads, not bridges 
   in general.

Best path is probably both: OS form_of_way for slip roads, OSM 
tags for bridges/tunnels, endpoint-fallback for either flag. 
Approximately 2-3% of links would be affected.

**Why not now:**
- Deferred after a high-output day to avoid attention fatigue on 
  fiddly debug
- Structure handling design needs to land cleanly — running without 
  it produces visibly wrong values on bridges/tunnels/slip roads, 
  which would require explaining away in methodology
- Lower priority than the 5-seed harness (evaluation infrastructure 
  unlocks honest measurement of every future change including this)

**Next steps when picked up:**
1. Verify OS Terrain 50 unzip state and VRT build (check tile count 
   ~2,858 .asc files; build VRT if not done)
2. Extend OSM extraction in network.py to capture bridge, tunnel, 
   covered tags (separate small task)
3. Implement grade script with both structure-handling paths
4. Validation tests: flat terrain (grade ~0), linear ramp 
   (grade matches), bridge/tunnel/slip flagged correctly
5. Spot-check 20 random links per category against OSM 
6. Don't retrain Stage 2 — this is feature engineering only, retrain 
   happens after 5-seed harness lands

**Related:** Pairs with curvature features. Both attack the geometric-
risk gap in the current feature set. Likely modest individual 
contribution given the rank stability findings (top-1% Jaccard 0.951 
across the tiered imputation change), but as a paired set with 
curvature, captures geometric alignment risk that the model currently 
has no signal for.

---

### IMD (Index of Multiple Deprivation) LSOA join

- [x] IMD 2025 LSOA join added to `network_features.parquet` (1 May 2026) —
  overall IMD decile, crime decile, and living-environment indoors decile
  included. Indoors sub-domain used instead of the full Living Environment
  domain to avoid leakage from the Outdoors road traffic accidents indicator.
  See `data/provenance/imd_provenance.json`.
- [ ] Persist `lsoa21cd_assigned` to `network_features.parquet` for future
  IMD/RUC coverage diagnostics. Current IMD coverage gap is explained:
  61,313 links without English IMD ≈ the earlier 62k estimate, almost
  certainly Welsh LSOAs picked up at the western edge of the study bounding
  box (Cheshire/Shropshire border and Wirral peninsula reaching toward Wales).
  Not urgent; this would make the diagnostic one-line in future.

**Context:** Deprivation correlates with crash risk via mechanisms not
captured by population density alone — older vehicle fleets, enforcement
gaps, pedestrian exposure, on-street parking density. LSOA-grain open data
from MHCLG. Integration is near-free — same spatial join as existing LSOA
population density feature.

**Decisions already made:**
- Use domain-level scores (crime, living environment) rather than only
  the overall IMD decile; these domains are more directly road-safety-
  relevant.
- Universal England coverage (LSOA is complete).
- No licensing friction.

**Prompt:**
[Draft as a small, well-scoped task. Download IMD 2019 LSOA data, join
via existing LSOA spatial join infrastructure, add as features to Stage 2.
Include overall decile plus crime domain and living environment domain as
separate features. Report before/after CV R² on Stage 2 retrain.]

**Expected outcomes:**
- Modest pseudo-R² improvement (0.01–0.03).
- Crime domain likely carries more distinctive signal than overall decile
  (which correlates heavily with other things already in the model).

---

### NaPTAN bus stops — buffer features

**Context:** Bus stops are conflict generators — braking, overtaking,
pedestrian density. DfT NaPTAN is open, point data, GB-wide. Simple buffer-
count feature per link.

**Decisions already made:**
- Features: `n_bus_stops_50m` (count in 50m buffer), `has_bus_stop`
  (binary flag).
- Buffer distance tunable; 50m is literature-informed starting point.
- Straightforward computation; no licensing or coverage issues.

**Prompt:**
[Draft. Download NaPTAN bus stop data, compute per-link buffer counts at
50m (and optionally 100m for comparison), add features to
network_features.parquet. Retrain Stage 2 and report.]

**Expected outcomes:**
- Modest pseudo-R² improvement (0.005–0.02).
- Likely higher feature importance on urban A-roads and B-roads than on
  motorways or rural classes.

---

### ONS Rural-Urban LSOA classification

- [x] ONS Rural-Urban Classification (2021) added to `network_features.parquet`
  (23 April 2026) — 84.51% link coverage, 6-class 2021 scheme (`UN1`, `UF1`,
  `RSN1`, `RSF1`, `RLN1`, `RLF1`) preserved from source; derived binary
  `ruc_urban_rural` shows 74% urban / 26% rural across non-null links,
  consistent with the study area. `pop_density_per_km2` unchanged.
  Nearest-centroid limitation documented in methodology page. See
  `data/features/ruc_provenance.json`.

---

## Notes On Execution Order

The "Queued tasks with prompts" section is now long. Eleven tasks are queued.
Realistic pace is probably one per session, maybe two if things are flowing. This
list documents intent as much as plan.

Dependencies matter more than priority:

- ~~EB shrinkage~~ ✅ done. 5-seed stability is independent of everything else.
- Facility-family split depends on EB shrinkage infrastructure being in place ✅.
- NHNM depends on facility-family split.
- OSM tiered imputation benefits from ONS RUC being done first.
- Curvature/grade are independent but want the 5-seed infrastructure to evaluate
  their contribution honestly.

A rough execution sequence that respects dependencies:

1. ~~AADF filter~~ ✅ done.
2. 5-seed stability — infrastructure for evaluating everything else.
3. ~~EB shrinkage~~ ✅ done (25 April 2026).
4. ~~IMD~~ ✅ + NaPTAN — cheap adds, independent of model structure.
5. ~~ONS RUC~~ ✅ done.
6. ~~OSM tiered imputation~~ ✅ done.
7. Curvature + grade — independent; do when in the mood for geometry work.
8. ~~Facility-family split~~ ✅ sessions 1–2 done (26 April 2026); sessions 3–4 deferred
   pending v2 redesign (motorway overfitting, partial pooling candidate).
9. NHNM integration — depends on facility-family v2 decision.


## 🔭 Future Work & Open directions (low priority, good starting points for others)

Ideas worth pursuing that aren't scoped for the immediate backlog in the
[Future Work site page](quarto/future-work.qmd). Each
entry captures enough context that someone — future me, a collaborator,
or an open-source contributor — can pick it up without reconstructing
the reasoning from scratch. Not ranked against each other; roughly equal
priority ("worth doing eventually or by someone else").
