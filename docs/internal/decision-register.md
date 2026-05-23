# Open Road Risk — Decision Register

Working record of what's been investigated, what was concluded, and why.
Internal notes; not for the public site. The point is one-page readability
when reviewing project state in three months' time, not completeness.

## Conventions

- Entries chronological, newest at top.
- One investigation = one entry.
- Format: question → method → outcome → artefacts → revisit condition.
- Keep tight; link to artefacts rather than duplicating their content.
- Update when an investigation concludes, not while it is in progress.
- If an entry's conclusion is later overturned or refined, add a new entry
  rather than editing the old one; cross-reference both ways.
- Numerical claims in entries reflect the source artefacts cited; where these
  differ from informal summaries elsewhere in the repo (done.md, Quarto pages),
  the entry's number is canonical and the informal summary should be updated.

## Entry template

```
## YYYY-MM-DD: <short title> — <verdict>
**Investigated:** <one-sentence question>
**Method:** <one or two sentences; reference to design/pre-registration doc if separate>
**Outcome:** <one or two sentences with the key numerical or factual result>
**Artefacts:**
- <file path>
- <file path>
**Revisit condition:** <what would need to change for this to be re-opened,
or "none / superseded by X" if closed permanently>
```

## Entries

<!-- newest first -->

## 2026-05-22: Standalone KSI atlas — parked

**Investigated:** can a separate KSI count model produce a meaningfully
different operational ranking from the all-injury model on the Open Road
Risk study area?

**Method:** pre-registered two-part KSI diagnostic. Part A is a
severity-reporting consistency check across the 23 police forces in the
study area over 2015–2024, comparing KSI counts and KSI-to-all-injury
ratios by force-year against pre-registered ±20% year-on-year ratio-change
and ≥25 absolute count change rules. Part B is a Wang/Quddus-style
predictor-set comparison and EB-shrunk Jaccard against the all-injury
ranking. Part B was conditional on Part A clearing.

**Outcome:** Part A returned the strict pre-registered verdict
"per-force handling required before KSI modelling is defensible". 28
force/year rows flagged under the pre-registered rule; 26 of those
survived the practical sensitivity threshold, so the result is not
small-number volatility. The flag pattern is consistent with the
documented 2016–2019 CRaSH/COPA injury-based severity reporting reform
plus Staffordshire-specific anomalies, and does not collapse cleanly
under tested restricted windows (2017–2024, 2017–2023, 2019–2023). Part
B was not run.

**Artefacts:**
- `reports/preregistration/ksi_diagnostic_preregistration.md`
- `reports/ksi_reporting_consistency.md`
- `reports/figures/ksi_reporting_consistency/`
- `src/road_risk/diagnostics/ksi_reporting_consistency.py`
- `todo/parked.md` (KSI entry)

**Revisit condition:** Reopen only if (a) DfT's published severity
adjustment factors are integrated for a specific deliverable, or (b) the
study area is restricted to a single force or force-group with internally
stable severity reporting. Do not reopen at the current scope and
threshold based on this evidence.

---

## 2026-04-24: OSM tiered speed-limit imputation — adopted

**Investigated:** does a road-classification × urban/rural lookup imputation
for OSM `speed_limit_mph` fix the Stage 2 GLM base-table shrinkage caused
by raw OSM 56% coverage, without destabilising the XGBoost ranking?

**Method:** `speed_limit_mph_effective` defined by a 9-rule priority cascade
(OSM value if tagged; otherwise UK statutory defaults keyed on
`road_classification` × dual/trunk flag × `ruc_urban_rural`); Stage 2 GLM
and XGBoost retrained on the updated feature. Full rule table in
`data/provenance/speed_limit_effective_provenance.json`.

**Outcome:** network coverage rose from 56% to 91.3% (1.98M / 2.17M links),
recovering GLM `n_full` to 18.3M (pre-OSM baseline) and improving GLM
pseudo-R² 0.251 → 0.301. XGBoost unchanged at 0.858; top-1% Jaccard 0.951,
Spearman 0.996 — ranking essentially stable.

**Artefacts:**
- `data/provenance/speed_limit_effective_provenance.json`
- `reports/speed_limit_effective_verification.md`
- `todo/osm_features.md`

**Revisit condition:** Reopen if OSM tagging rate for any major road class
exceeds 80%, at which point the imputed default for that class can be retired
in favour of direct OSM values.

---

## 2026-04-25: Empirical Bayes shrinkage v1 — adopted as parallel ranking

**Investigated:** does NB2 EB shrinkage on per-link XGBoost predictions
produce a materially different and more stable ranking than the raw XGBoost
percentile?

**Method:** method-of-moments NB2 dispersion estimated across 18
predicted-risk quantile bins; positive-event weighted k used as production
value; EB-adjusted scores stored as `risk_percentile_eb`. Design and
rationale in `quarto/methodology/empirical-bayes-shrinkage.qmd`.

**Outcome:** production k = 3.45 (positive-event weighted); k_bin varies
~40× across the predicted-risk range, confirming dispersion non-constancy
makes global-k a known-imperfect summary. EB top-1% overlaps 38.85% with
the non-EB top-1% — substantially demoting high-AADT zero-collision links
and elevating observation-heavy low-prediction links. Cross-seed stability
diagnostic showed churn links move at parity with the general population;
EB does not reduce seed-induced ranking instability. Adopted as
`risk_percentile_eb` alongside, not replacing, `risk_percentile`.

**Artefacts:**
- `reports/eb_dispersion.md`
- `reports/eb_validation.md`
- `data/provenance/eb_dispersion_provenance.json`
- `data/models/risk_scores_eb.parquet`
- `quarto/methodology/empirical-bayes-shrinkage.qmd`

**Revisit condition:** Reopen for per-family or per-bin k when the
facility-family split advances to production; global-k EB carries a ~4%
top-1% membership ambiguity from aggregation choice that per-family k
removes.

---

## 2026-04-25: 5-seed XGBoost rank stability — noise floor established

**Investigated:** how stable are Stage 2 XGBoost rankings across random-seed
variation, and what is the noise floor for evaluating future feature
additions?

**Method:** XGBoost trained across seeds 42–46 with the same
GroupShuffleSplit link-level CV; pseudo-R², top-k Jaccard, and full-rank
Spearman computed pairwise. Figures reflect the post-hgv-fix rerun that
became the authoritative noise floor for the temporal ablation.

**Outcome:** pseudo-R² 0.323 ± 0.003 across five seeds; top-1% pairwise
Jaccard mean 0.904 (below the >0.93 prior — dense boundary region around
k=1000 explains the non-monotonic top-k profile); full-rank Spearman >
0.999. Noise floor for feature evaluation: a proposed addition must exceed
~0.006 pseudo-R² improvement (1.5× cross-seed std) to be distinguishable
from seed noise.

**Artefacts:**
- `reports/rank_stability.md`
- `reports/rank_stability_investigation.md`
- `data/provenance/rank_stability_provenance.json`

**Revisit condition:** Rerun after any change to model architecture, training
data grain, or feature set; the current figures are the comparative baseline
for all subsequent feature evaluations.

---

## 2026-05-04: Stage 2 exposure offset and calibration diagnostics — Model A retained; learned exposure and pooled interaction GLM rejected

**Investigated:** should the Stage 2 GLM move away from the fixed
`log(AADT × length × time)` exposure offset, or add post-hoc intercept
calibration / facility-family exposure slopes?

**Method:** compared Model A fixed offset, Model B learned exposure, global
intercept calibration, per-family intercept calibration, pooled family
interaction GLM (M4), and separate per-family GLMs (M5). Model A/B used
full-frame residual diagnostics; calibration, M4, and M5 were checked on
held-out links with train-only calibration factors.

**Outcome:** retain Model A: Model B improved downsampled-training pseudo-R²
0.3117 → 0.3266 but did not improve calibrated full-frame residuals, and
Poisson overdispersion was ~1.40, below the pre-set 1.5 Negative Binomial
gate. A + per-family intercept calibration remains a candidate v3 diagnostic
layer only; M4's held-out deviance gain over A+fcal was tiny (548,042.5 vs
549,579.0), M5 was rejected as overfit-prone on small per-family training
sets, and the motorway residual pattern, including under-prediction in some
AADT bands, remains unresolved.

**Artefacts:**
- `reports/exposure_offset_full_frame_diagnostics.md`
- `reports/family_intercept_calibration_diagnostics.md`
- `reports/family_within_aadt_diagnostics.md`
- `reports/family_exposure_slope_heldout_diagnostics.md`
- `todo/done.md` (Stage 2 GLM exposure/calibration entry)
- `todo/model.md`

**Revisit condition:** Reopen if motorway under-prediction is addressed by
other means, at which point A + per-family intercept calibration can be tested
as a production layer; also reopen if facility-family split v2 advances to
production, because family calibration and family modelling would need a
single combined decision.

---

## 2026-04-25/26: Facility-family split v1 — diagnostic only; v2 deferred

**Investigated:** does training separate XGBoost models for four facility
families (motorway, trunk A, other urban, other rural) improve held-out
ranking over the global model?

**Method:** network split by `road_classification` × `ruc_urban_rural` into
four families; per-family models trained on 80% of links (seed=42
GroupShuffleSplit) and evaluated on per-family held-out sets; stitched
ranking benchmarked against the global model. Adoption criteria in
`quarto/methodology/facility-family-split.qmd §11`.

**Outcome:** motorway per-family R² reverses on held-out links (−0.027 vs
global), indicating overfitting on the 4,084-link training set; trunk-A,
other-urban, and other-rural held-out deltas (+0.006, +0.001, +0.002) are
within seed noise. Top-1% stitched vs global intersection: 93.6%; boundary
discontinuity max gap 0.005. Adoption blocked by motorway overfitting, not
calibration quality. v1 retained diagnostically in
`data/models/risk_scores_family.parquet`.

**Artefacts:**
- `reports/family_validation.md`
- `reports/family_exposure_slope_heldout_diagnostics.md`
- `reports/family_intercept_calibration_diagnostics.md`
- `reports/family_within_aadt_diagnostics.md`
- `quarto/methodology/facility-family-split.qmd`
- `data/provenance/family_split_provenance.json`

**Revisit condition:** Reopen v2 when motorway overfitting is addressed
(hyperparameter reduction, partial pooling with trunk-A, or larger motorway
training window); pair with per-family EB k.

---

## 2026-05-03: Temporal descriptors evaluation — real but below threshold; parked

**Investigated:** do link-level temporal descriptors (`core_overnight_ratio`,
WebTRIS HGV%) improve Stage 2 XGBoost pseudo-R² enough to warrant production
adoption?

**Method:** pre-registered two-criterion rule (pseudo-R² Δ > 0.009 and test
deviance reduction > 0.6%, on ≥ 4/5 seeds); three configurations (A =
baseline, B = + overnight ratio, C = + overnight ratio + WebTRIS HGV%)
evaluated across seeds 42–46 excluding 737 WebTRIS-snapped held-out links.
Step-by-step record in `docs/internal/temporal_changes_plan.md`.

**Outcome:** Config B: pseudo-R² Δ 0.0036–0.0045, deviance reduction
0.53–0.66% — null. Config C: pseudo-R² Δ 0.0056–0.0063, deviance reduction
0.82–0.92% — null. Config C narrowly clears the deviance criterion but fails
pseudo-R² on every seed. Weekday/weekend and seasonal descriptors were parked
earlier for lack of link-specific variation in WebTRIS data.

**Artefacts:**
- `docs/internal/temporal_changes_plan.md`
- `reports/temporal_findings.md`
- `reports/supporting/temporal_ablation_summary.md`
- `todo/parked.md` (temporal entry)

**Revisit condition:** Do not reopen at the same threshold on current
evidence. Reopen only if project priorities intentionally reset the adoption
threshold or if the Stage 1b time-zone / WebTRIS HGV models improve
materially.

---

## 2026-04-19: Counted-only AADF filter for Stage 1a — adopted; weighted-Estimated alternative rejected

**Investigated:** should Stage 1a train on directly counted AADF rows only,
or keep DfT Estimated rows with a downweighting scheme?

**Method:** filtered Stage 1a training and holdout validation to count points
with at least one `estimation_method == "Counted"` observation in 2015-2024,
then compared CV, local holdout, and spatial holdout performance against the
pre-filter training target.

**Outcome:** adopted counted-only training: the filter drops 1,288 of 14,193
count points (9.1%) that are always Estimated, while CV R² improves 0.72 →
0.83, local holdout R² 0.776 → 0.832, and spatial holdout R² 0.707 → 0.788.
Dropped points skew Major vs Minor (11.2% vs 4.6%); regional loss is broadly
uniform, with Wales higher at 17% on a small sample. Weighted-Estimated
training was rejected as methodologically arbitrary.

**Artefacts:**
- `todo/done.md` (Counted-only AADF filter entry)
- `quarto/methodology/exposure-model.qmd`

**Revisit condition:** Reopen if DfT publishes methodology that makes the
Counted/Estimated distinction less load-bearing, or if a specific deliverable
requires coverage on roads where only Estimated AADF exists.

---

## 2026-04-22: MRDB vs OS Open Roads network backbone — OS Open Roads adopted as network truth; MRDB retained for SRN-specific use only

**Investigated:** what should serve as the network geometry backbone for the
Open Road Risk pipeline — MRDB (National Highways / DfT major-road data) or OS
Open Roads (Ordnance Survey)?

**Method:** reconstructed from current code, source pages, and git history
rather than a closed comparison report: compare MRDB's count-point key and
major-road scope against OS Open Roads' all-classified-road coverage, link
geometry, graph topology, AADF spatial snap, and collision snap quality.
[reconstruct from memory: whether MRDB licensing differed materially from OS
Open Roads; repo evidence only confirms OS Open Roads is Open Government
Licence].

**Outcome:** OS Open Roads supersedes MRDB as the geometry truth: AADF is joined
to OS Open Roads with `sjoin_nearest`, collisions are snapped to OS Open Roads
links, and the model scores OS Open Roads links. The early Yorkshire artefacts
show the scale reason: 705,672 OS Open Roads links versus 1,948 MRDB major-road
links (~362× coverage), while current OS Open Roads coverage is ~2.17M links
across the expanded study area; MRDB ingest still runs but its output is
orphaned.

**Artefacts:**
- `todo/mrdb_ingest.md`
- `src/road_risk/clean_join/join.py`
- `src/road_risk/ingest/legacy_ingest_mrdb.py`
- `src/road_risk/ingest/ingest_openroads.py`
- `todo/done.md`
- `quarto/methodology/data-joining.qmd`
- `quarto/data-sources/openroads.qmd`
- `quarto/data-sources/index.qmd`
- `docs/internal/sites_todo.md`
- `docs/internal/data-quality-notes.md`
- `todo/network_model_gdb.md`

**Revisit condition:** Reopen only if OS Open Roads coverage or snap quality
proves materially worse than MRDB for a named road class and deliverable; if
Network Model GDB integration proceeds, redecide MRDB's remaining SRN role
because GDB is the more authoritative SRN enrichment source.
