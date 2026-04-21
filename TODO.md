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

- [ ] Drop raw `betweenness` from GLM — coefficient is −8 which dominates the
  coefficient chart and is a multicollinearity symptom. Keep `betweenness_relative`
  which is the cleaner feature. XGBoost handles both fine via tree splits.

- [ ] Validate AADT estimates on WebTRIS motorway corridors — compare predicted vs
  measured flow on M62/M1 as sense check. Currently evaluated only on AADF holdout.

- [ ] Stage 1c vehicle mix model — predict % HGV/LGV/car per link from road type +
  network features. Enables vehicle-type risk analysis on uncounted roads.

- [ ] Remove `smartmotorway`, `parentlinkref`, `enddate` from any feature derivation
  lists — all empty (100% null) in current Network Model GDB release.

---

## 🟢 Infrastructure / Output

- [ ] `db.py` — PostGIS loader for all processed parquets + model outputs. Required
  for Streamlit app queries.

- [ ] Streamlit app skeleton — map with road links coloured by risk percentile,
  sidebar filters for road type / year / severity.

- [ ] GeoPackage export — ESRI-compatible output layer (link_id, geometry,
  estimated_aadt, risk_percentile, road_classification). Demonstrates ESRI
  integration story for DfT/DVSA conversations.

- [ ] `data/README.md` — download instructions for all large raw files not in git
  (STATS19 CSV, OS Open Roads GeoPackage, AADF zip, OSM pbf files, MRDB).

- [ ] Kaggle dataset — upload processed parquets so others can skip ingest/clean/snap.

---

## 🔵 Applications / Demonstrations

- [x] DVSA test route pipeline — `dtc/routes.py` (NetworkX routing, 174 routes,
  24 centres) + `dtc/analysis.py` (per-centre features, correlations vs Annex D).

- [ ] Risk-normalised output table — "Top 1% highest-risk road segments controlling
  for traffic" as a clean publishable output.

- [ ] Seasonal risk analysis — combine Stage 2 risk scores with Stage 1b temporal
  profiles. Do high-risk roads have worse seasonal variation?

- [ ] DVSA correlations — apply multiple-testing correction (FDR or Bonferroni)
  given ~3,000+ feature × outcome pairs on 24 centres. Currently reported without
  adjustment; results should be framed as hypothesis-generating, not confirmatory.

---

## ⚪ Parked (investigated, deprioritised — with reason)

- **OSM global retrain without class-tiered imputation** — coverage diagnostic
  (19 April 2026) showed no column × road-class combination reaches 80% coverage.
  Median imputation at 5–16% true coverage injects bias that correlates with road
  class. See `reports/osm_coverage_summary.md`. Replaced by the road-class-tiered
  imputation task below.

- **OS MasterMap Highways (RAMI)** — blocked pending OS Data Hub licensing
  clarification on development-mode use for a public portfolio site. RAMI gives
  lanes and widths on the full GB network but "live application" vs "development
  mode" boundary is not defined clearly enough to commit. Revisit if OS Support
  responds with a specific answer permitting portfolio use.

- **Common-basis pseudo-R²** — deprioritised in favour of 5-seed rank stability
  (see queued tasks). Pseudo-R² isn't the operationally relevant metric; rank
  stability of the top-1% list is.

- **DVSA test route data as collision model feature** — selection bias risk
  (routes chosen by DVSA for teachability, not randomness), coverage issue
  (<1% of network), and structural target-leakage risk. Better used as external
  validation of the risk score and as its own downstream analysis, not as an
  input feature.

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
- [x] QMD site: eda-traffic, model-results, eda-collisions, test-routes (methodology + analysis)
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
- [x] OSM coverage diagnostic (`reports/osm_coverage_summary.md`, 19 April 2026)
      — no column × road-class combination reaches 80% coverage; `lanes` at 4–7%
      on minor roads; `speed_limit_mph` highest at 56% overall but lowest on
      motorways (46%, near-constant where populated).
- [x] Model inventory (`reports/model_inventory.md`, refreshed 21 April 2026) — durable
      baseline of current Stage 2 features, hyperparameters, training rows, and
      DVSA correlation pipeline description.
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

---

## Queued tasks with prompts

---

### Empirical Bayes shrinkage for risk ranking

**Context:** Stage 2 currently ranks on `mean predicted_xgb` with no shrinkage.
For a network-screening output with rare events across millions of links, EB
adjustment (HSM/FHWA standard) combines model prediction with observed history
and controls for regression to the mean. Likely to improve stability of top-k
lists without necessarily moving headline R².

**Decisions already made:**
- Global NB fit for `k` (not per-family) for v1 simplicity. Per-family is a
  future extension that pairs with the facility-family split.
- Shrink toward `predicted_xgb`, not `predicted_glm` — GLM has biased intercept
  from zero-downsampling.
- Compute `n_years` per link; don't assume uniform (some links may only appear
  in some AADT years).
- Output `risk_percentile_eb` alongside existing `risk_percentile`, not replacing.
- Methodological compromise: HSM uses NB model predictions as the prior; we
  use XGBoost-Poisson predictions and borrow `k` from an auxiliary NB GLM.
  Flag explicitly in methodology.

**Prompt:**

Produce a markdown design doc at reports/eb_shrinkage_design.md, NOT code.
I will review before any implementation.

The doc should cover:

1. Mathematical formulation: `expected_EB = w × predicted + (1-w) × observed`,
   where `w = 1 / (1 + k × predicted × n_years)`. Confirm units — read
   `collision.py` and report shape and units of `predicted_xgb` at pooling point.
2. `k` estimation: fit a global NB GLM on the full link-year table using the
   same feature set as the current Poisson GLM; extract dispersion parameter.
   Document that this is a compromise: HSM assumes NB-derived predictions as
   prior; we use XGBoost + borrowed `k`.
3. Handling of `n_years` — per link, from AADT output row counts.
4. Implementation plan: which functions change, new diagnostic module, aim to
   keep changes in `collision.py` plus a small new module.
5. Validation plan:
   - How many links have rank change >10 percentiles.
   - Top-1% list size change.
   - Qualitative review: 5 links that drop out of top-1% under EB vs 5 that
     enter, and what they have in common.
   - Do NOT include cross-fold stability — that is separate 5-seed work.
6. Caveat section on the `k`-borrowing methodology compromise.

Stop after the doc. Do not implement. Do not modify `collision.py`.

**Expected outcomes:**
- Top-1% list likely shrinks slightly as high-predicted/low-observed links
  shrink toward observed.
- Short segments with one freak collision should drop in ranking.
- Long segments with smooth exposure should rise.
- Rank correlation old vs new likely 0.85–0.95 (meaningful change, not total
  reshuffle).

---

### 5-seed GroupShuffleSplit for rank stability

**Context:** Current XGBoost training uses a single GroupShuffleSplit seed.
Single-split pseudo-R² implies precision that isn't there. The operational
output is a ranking, so rank stability across retrains matters more than a
single R² number. Running 5 seeds is infrastructure that supports EB
shrinkage validation, facility-family split evaluation, and any future
model comparison.

**Decisions already made:**
- 5 seeds as starting point; extend to 10–20 only if results are loose.
- Report pseudo-R² mean ± std, top-k Jaccard (k = 100, 1000, 10000, 1%),
  Spearman rank correlation full list, per-decile calibration.
- XGBoost only for v1; GLM adds compute without directly supporting the
  production ranking.

**Prompt:**

Add 5-seed GroupShuffleSplit rank stability evaluation to Stage 2.

**Implementation:**

1. In `collision.py` or a new validation module, wrap the XGBoost training in a
   loop over 5 seeds passed to GroupShuffleSplit.
2. Save per-seed `risk_percentile` outputs; do not overwrite
   `risk_scores.parquet`.
3. Compute and save:
   - Pseudo-R² per seed: mean ± std.
   - Top-k Jaccard index for `k in [100, 1000, 10000, ceil(0.01 × n_links)]`.
   - Pairwise seed comparisons; report mean pairwise Jaccard per k.
   - Spearman rank correlation for the full ranked list, each pair; report mean.
   - Per-risk-decile observed collision rate per seed; report std across seeds.

Save to reports/rank_stability.md with a table and short narrative.

Do NOT change the production risk_scores.parquet — keep using seed=42 for
the canonical output. This evaluation is reported alongside, not replacing.

**Expected outcomes:**
- Pseudo-R² spread <0.02 → model is stable; single-number reporting is defensible.
- Top-1% Jaccard >0.85 → ranking is robust; stakeholder-facing use case is supported.
- Top-1% Jaccard <0.70 → ranking is unstable; flag as a concern and investigate
  before further production use.

---

### OSM features with road-class-tiered imputation

**Context:** Current OSM coverage (`speed_limit_mph` 56%, `lanes` 7%,
`is_unpaved` 16%) is too low for global inclusion as-is. Median imputation
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
- Features: `mean_curvature`, `max_curvature`, `sinuosity` (length /
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
   - `mean_curvature` (degrees per km)
   - `max_curvature`
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

**Context:** Vertical gradient correlates with crash frequency and severity,
especially for heavy-vehicle and run-off-road incidents. OS Terrain 50
(50m grid) is open data, GB-wide, free. Paired naturally with curvature
— both are full-coverage geometric features, both attack gaps the literature
supports.

**Decisions already made:**
- Use OS Terrain 50 (50m grid) — open data, consistent with rest of OS
  ecosystem. Terrain 5 is better but premium.
- Sample elevation at points along each link (same resampling as curvature).
- Per-link features: `mean_grade`, `max_grade`, `grade_change` (absolute
  total vertical change over link).
- Handle bridges and tunnels separately — DEM-sampled grade is wrong under
  a bridge. Needs either a bridge flag (OS or OSM) or outlier detection.

**Prompt:**
[Draft after curvature is done so the resampled point geometry is already
cached. Should include: OS Terrain 50 download + grid handling, sampling
elevation along each link, bridge/tunnel handling (from OSM tunnel=yes
and bridge=yes tags as a proxy since OS Open Roads lacks the flag), per-link
grade summary features. Add to network_features.parquet.]

**Expected outcomes:**
- Universal GB coverage.
- Grade correlates with road class (motorways flatter on average) but has
  meaningful within-class variance — the bit road class doesn't capture.
- Combined with curvature, attacks the geometric-risk gap in the current
  feature set.

---

### Facility-family split for Stage 2

**Context:** Current Stage 2 uses one global model with road-class indicators.
HSM/FHWA safety performance functions are explicitly site-type specific
because the exposure-to-risk curve has different shape across road families,
not just different level. Separate models by family (or partially pooled)
typically improve calibration and interpretability before they improve
headline R². Prerequisite for integrating the Network Model GDB cleanly
(lets authoritative SRN features live on the SRN model rather than needing
imputation across the full network).

**Decisions already made:**
- Candidate families: motorway, trunk A-road, urban A-road, rural A-road,
  B-road, unclassified, explicit intersection entity.
- Start with separate models then evaluate hierarchical/partial-pooling
  variants. Small families (motorways at 4k links) will fit noisily
  standalone.
- Urban/rural split depends on ONS Rural-Urban classification or
  pop_density threshold — needs a decision.
- Must be done before NHNM integration but after EB shrinkage infrastructure
  lands.

**Prompt:**
[Draft after EB shrinkage design doc is in hand. Design doc first, not
implementation. Should cover: family definition, separate vs hierarchical
modelling tradeoffs, how to handle intersections as separate entities,
how per-family EB k estimation interacts with this, evaluation strategy
against single-model baseline.]

**Expected outcomes:**
- Better calibration per family, especially on motorways where the global
  model currently under-predicts (mean residual -3.3 on motorway from
  current results).
- Enables clean NHNM integration on SRN families.
- Expected modest pseudo-R² change but meaningful rank stability improvement
  and interpretability gain.

---

### IMD (Index of Multiple Deprivation) LSOA join

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

**Context:** Cleaner urban/rural split than population density alone.
Needed for OSM imputation defaults (rural 60 mph vs urban 30 mph on
unclassified roads) and itself a useful model feature. Pairs with the
OSM tiered imputation task above — effectively a prerequisite if we
want imputation defaults to be rural/urban aware.

**Decisions already made:**
- ONS Rural-Urban Classification 2011 (or newer if released) at LSOA.
- Universal coverage, free, no licensing.
- Use as both a feature and as the urban/rural flag for OSM imputation.

**Prompt:**
[Draft as a small task. Download ONS RUC at LSOA, join via existing spatial
infrastructure, add as a categorical feature, use to drive OSM imputation
defaults in the OSM tiered imputation task.]

**Expected outcomes:**
- Small direct contribution as a feature.
- Larger indirect contribution by improving OSM imputation quality.

---

## Notes On Execution Order

The "Queued tasks with prompts" section is now long. Eleven tasks are queued.
Realistic pace is probably one per session, maybe two if things are flowing. This
list documents intent as much as plan.

Dependencies matter more than priority:

- EB shrinkage and 5-seed stability are independent of everything else — do
  those first.
- Facility-family split depends on EB shrinkage infrastructure being in place.
- NHNM depends on facility-family split.
- OSM tiered imputation benefits from ONS RUC being done first.
- Curvature/grade are independent but want the 5-seed infrastructure to evaluate
  their contribution honestly.

A rough execution sequence that respects dependencies:

1. AADF filter — small, quick win.
2. 5-seed stability — infrastructure for evaluating everything else.
3. EB shrinkage — biggest single structural improvement.
4. IMD + NaPTAN — cheap adds, independent of model structure.
5. ONS RUC.
6. OSM tiered imputation — uses ONS RUC.
7. Curvature + grade — independent; do when in the mood for geometry work.
8. Facility-family split — larger refactor, do when other improvements are in
   place.
9. NHNM integration — depends on facility-family split.


## 🔭 Future Work & Open directions (low priority, good starting points for others)

Ideas worth pursuing that aren't scoped for the immediate backlog in the
[Future Work site page](quarto/future-work.qmd). Each
entry captures enough context that someone — future me, a collaborator,
or an open-source contributor — can pick it up without reconstructing
the reasoning from scratch. Not ranked against each other; roughly equal
priority ("worth doing eventually or by someone else").
