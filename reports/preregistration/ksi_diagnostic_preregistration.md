# KSI Diagnostic — Pre-Registration

**Status:** Draft, pre-KSI-diagnostic results
**Date written:** [date before running any analysis]
**Author:** T. H. Simm
**Purpose:** Commit to evaluation criteria and decision rules before observing data, to prevent the analysis from being shaped by intermediate results.
**Related:** `todo/feature_addition_imd_grade.md`, `reports/family_validation.md`, `reports/rank_stability.md`, `quarto/literature/severity-modelling.qmd`, `quarto/literature/literature-pipeline-alignment.qmd`.

---

## 1. Purpose

Decide whether a separate KSI count model is worth building as the next major Open Road Risk extension, or whether KSI ranking is operationally redundant given the existing all-injury model. The diagnostic itself is a small piece of work (~1 week); the outcome determines what the next 10–15 weeks of project effort look like.

This is a *diagnostic*, not a model build. No production change is proposed regardless of outcome. The outputs are two short reports and a verdict line.

---

## 2. Context and prior evidence

Existing all-injury Stage 2 model results are treated as prior evidence for this diagnostic. This document is nevertheless written before observing the KSI diagnostic outputs described below, and the KSI-specific thresholds and decision rules are committed before those outputs are inspected.

### What is already established

- XGBoost is saturated at all-injury pseudo-R² ~0.859 across multiple feature batches. Feature additions move the headline metric by ≤0.001 (RUC, IMD, grade). See `feature_addition_imd_grade.md §6.5`.
- Top-1% Jaccard noise floor under feature changes is 0.918 (5-seed harness baseline; `reports/rank_stability.md`).
- Motorway under-prediction is unresolved. Global model residual ~−3.3 on motorway; family-split work documented but did not declare solved. See `reports/family_exposure_slope_heldout_diagnostics.md §7`.
- Grade coefficient on all-injury Stage 2 GLM is negative and significant (−0.0202), opposite to the SPF-literature prior. Mechanism uncertain. See `feature_addition_imd_grade.md §6.1`.
- 2024 STATS19 has a documented structural break (CF→RSF transition; DfT 2025 guide). Some forces also changed severity reporting practices from 2016 onwards.

### What the literature says

- Frequency and severity are different estimands (Quddus 2010, Michalaki 2015, Ma 2019, Savolainen 2011).
- Wang/Quddus/Ison 2011 (LIT-059): on M25 motorway segments, separate KSI and slight count models showed *different predictor structures* — lanes significant for slight only, gradient significant for both.
- Boulieri 2016 / Gilardi 2022: severity levels are strongly spatially correlated (ρ ~ 0.74–0.90) but distinct; joint Bayesian models substantially improve KSI estimation by borrowing strength from the more common slight pattern. Computationally infeasible at 2.17M-link scale.
- EB shrinkage extension to KSI sub-band is the lit-supported next step (`severity-modelling.qmd` lines 222–226; alignment page priority #15).
- STATS19 underreporting is severity-band-dependent: ~75% slight, ~30% serious, ~100% fatal (Elvik & Myssen 1999, cited in Savolainen 2011). KSI may therefore be a *less reporting-biased* outcome than total injury.

### What is not yet known

- Whether KSI counts at link-year grain across the Open Road Risk study area are dense enough to fit a stable GLM, especially on minor roads.
- Whether the predictor sets for KSI and all-injury differ in this network (Wang found differences on M25; whether they transfer to a mixed-class national network is open).
- Whether KSI severity classification has step-changes within 2015–2024 that would force restriction of the modelling years.
- Whether the EB-shrunk KSI ranking is operationally different from EB-shrunk all-injury ranking at top-1% / top-5% / top-10%.

---

## 3. Diagnostic components

The diagnostic has two parts. Both must produce defensible findings before any decision is made.

**Stage 2 modelling-table input path:** `data/features/road_link_annual.parquet` is the current persisted collision-count input used by the Stage 2 / link-year modelling workflow. Existing diagnostics load it via `RLA_PATH` and join it with `data/models/aadt_estimates.parquet` inside `build_collision_dataset()` to create the full in-memory link-year modelling frame.

### Part A — Severity reporting consistency check

**Question:** Is the KSI target measured consistently across the 2015–2024 study period and across the police forces in the study area?

**Method:**
1. Compute KSI count per (force, year) for forces 12/13/14/16 (Yorkshire) and any extended forces present in the modelling dataset.
2. Compute the KSI-to-all-injury ratio per (force, year). This normalises out collision-volume trends.
3. Plot both as line series, one panel per force.
4. Visually inspect for step-changes, particularly around 2016 (DfT-documented severity reporting system changes in some forces) and 2024 (CF→RSF transition).
5. Compute year-over-year ratio changes; flag any year where the change exceeds ±20% of the prior year's ratio.

**Output:** `reports/ksi_reporting_consistency.md` containing plots, flagged years/forces, and a verdict line on whether the 2015–2024 window can be used intact, restricted, or whether per-force handling is needed.

**Decision rules:**

| Finding | Action |
|---|---|
| No visible breaks across any force | Use full 2015–2024 window; standard underreporting caveat only |
| Visible break in 1 force around 2016 | Document; exclude that force from KSI work or restrict to post-2016 years |
| Visible break across all forces in 2024 | Restrict KSI modelling to 2015–2023; document loss of most recent year |
| Heterogeneous breaks across forces | Per-force calibration required; KSI atlas at national scope is not defensible without further methodology work |

### Part B — Wang/Quddus-style predictor-set comparison

**Question:** Does a KSI count model produce meaningfully different predictor relationships and operational rankings from the all-injury count model, on this network?

**Method:**

1. **Build KSI count column** at link-year grain. Use STATS19 severity field: KSI = fatal + serious. Pre-check: total KSI count, distribution per link-year, share of link-years with zero KSI.

2. **Fit two Poisson GLMs** with the *exact same* feature set, train/validation split, and offset structure as the existing Stage 2 production GLM:
   - Model A: outcome = all-injury count (replicates existing model)
   - Model B: outcome = KSI count
   - Use the post-grade feature set (`feature_addition_imd_grade.md`).
   - Same `log(AADT × length × 365 / 1e6)` offset for both.
   - Same grouped-link CV splits.

   Poisson GLM is used for comparability with the existing Stage 2 GLM and for interpretable coefficient comparison; it is not being claimed as the final best KSI model.

3. **Coefficient comparison.** For each feature in the common set:
   - Sign agreement / disagreement between Models A and B
   - Magnitude ratio (|coef_B / coef_A|)
   - Statistical significance pattern (significant in one but not the other)
   - Focus on lit-flagged features: `mean_grade`, HGV-related, `is_motorway`, family indicators

4. **EB shrinkage on KSI counts.** Re-estimate the method-of-moments dispersion parameter k on KSI counts using positive-event weighting (same procedure as the existing all-injury EB; see `reports/eb_dispersion.md`). Produce EB-shrunk KSI rankings.

5. **Operational ranking comparison.** Compute on EB-shrunk rankings only (not raw model output):
   - Spearman rank correlation, all links
   - Top-1% Jaccard
   - Top-5% Jaccard
   - Top-10% Jaccard
   - Entrants and leavers in top-1% list
   - Family composition of each top-1% list (motorway / trunk_a / other_urban / other_rural counts)

**Output:** `reports/ksi_diagnostic.md` containing all of the above, plus a verdict line against the pre-registered thresholds below.

---

## 4. Pre-registered evaluation thresholds

These thresholds are committed before any of the above analysis is run. The verdict line in `reports/ksi_diagnostic.md` reports against these specific values.

### 4.1 Primary threshold (operational distinctness)

**Top-1% Jaccard between EB-shrunk KSI ranking and EB-shrunk all-injury ranking** is the single most important metric.

| Jaccard range | Interpretation | Default next action |
|---|---|---|
| < 0.70 | Operationally distinct | KSI atlas justified as separate next project |
| 0.70 – 0.85 | Grey zone | Park; do not build KSI atlas this quarter; revisit after Temporal B v1 |
| > 0.85 | Operationally redundant | Do not build KSI atlas. Publish the diagnostic as a negative-result finding. Reroute capacity to Temporal B and LA-facing tool on all-injury model |

Below 0.70, at least 30% of the operational priority set changes, which is large enough to imply a materially different intervention shortlist.

### 4.2 Secondary threshold (methodological distinctness)

**Predictor-set difference signal.** A KSI model is considered methodologically distinct if at least *two* of the following are observed in the GLM coefficient comparison:

- `mean_grade` coefficient changes sign or doubles in absolute magnitude between A and B
- `is_motorway` or motorway-family coefficient changes in sign or doubles in magnitude
- One of the IMD decile features becomes non-significant (|t| < 1.96) in B while remaining significant in A, or vice versa
- HGV-proportion-related coefficient changes magnitude by >50%

This is a softer criterion and informs framing but does not by itself trigger the "KSI atlas justified" decision. The primary threshold (4.1) is the operational gate.

### 4.3 Feasibility threshold

If KSI counts are too sparse for a stable GLM fit, neither of the above matters. The diagnostic stops at "infeasible at this grain" and the report concludes with options for aggregation (multi-year link-grain or facility-family-only).

Stability checks before reporting coefficient comparisons:
- Coefficient standard error inflation: median SE in Model B vs Model A across the feature set. Flag if median ratio > 3.
- Convergence: does the GLM converge cleanly on Model B? Flag if not.
- Sparsity: report share of link-years with KSI = 0; share of links with zero KSI across all years.
- Sparsity flag: more than 99.5% of link-years have KSI = 0.
- Sparsity flag: more than 95% of links have zero KSI across all years.

If any flag fires, the verdict line reports "infeasible at link-year grain" rather than a Jaccard-based decision.

---

## 5. What this diagnostic does *not* answer

To prevent scope creep during execution:

- **It does not test whether KSI is a "better" target.** KSI and all-injury are different estimands. The diagnostic compares their *operational rankings*, not their predictive quality.
- **It does not test the joint Bayesian model** (Boulieri/Gilardi). Joint modelling at 2.17M-link scale is computationally infeasible and is documented as a deferred option.
- **It does not propose a production change.** Even if Jaccard < 0.70, the next step is *planning* a KSI atlas, not switching the production `risk_percentile`.
- **It does not test XGBoost-on-KSI.** GLM only, for two reasons: (a) the lit comparison is GLM-based, (b) XGBoost coefficient comparison is not interpretable in the same way. If KSI work proceeds, an XGBoost-on-KSI build is a downstream task.
- **It does not test severity-weighted composites** (e.g. DfT WTP-weighted harm scores). These are documented as a design to avoid (`severity-modelling.qmd` lines 240–248; Gao 2024 critique).

---

## 6. Confirmation-bias protections

Three explicit safeguards:

1. **Thresholds pre-committed.** The numbers in §4.1 are set before any KSI analysis is run. They will not be adjusted after observing results to make the outcome "interesting".

2. **All three outcomes have a defined narrative.**
   - Jaccard < 0.70: KSI atlas project plan drafted next.
   - Jaccard 0.70 – 0.85: park decision documented, return to Temporal B planning.
   - Jaccard > 0.85: publish as a methodological finding. *This is a legitimate and useful outcome*, not a failed diagnostic. "We rigorously tested whether KSI requires a separate model on UK open-data network screening, found it didn't, and shipped Temporal B / LA tool on the all-injury model with explicit caveats" is a defensible research story.

3. **Report structure committed in advance.** The output reports (`reports/ksi_reporting_consistency.md` and `reports/ksi_diagnostic.md`) follow a fixed structure: setup → method → results → verdict-against-thresholds → caveats. The verdict line names a specific threshold range; it does not contain hedging language designed to keep options open.

---

## 7. Effort and resource budget

- Severity reporting consistency check: 0.5 day
- KSI count column + descriptive sparsity audit: 0.5 day
- Model B GLM fit + coefficient comparison: 1 day
- EB shrinkage k re-estimation for KSI: 0.5 day
- Ranking comparison (Jaccard, Spearman, family composition): 0.5 day
- Two reports written up: 1 day
- Slippage buffer: 1 day

**Total: 5 days.** If actual elapsed time exceeds 7 days, stop and reassess scope rather than expanding.

---

## 8. Dependencies and risks

### Pre-flight dependencies
- Existing all-injury Model A GLM artefacts (coefficients, training rows, validation splits) accessible.
- STATS19 severity field reliably populated at the link-year join grain in current modelling table.
- EB shrinkage infrastructure (`src/road_risk/model/eb_dispersion.py`) reusable for KSI counts with target swap only.

### Risks
- **KSI counts too sparse to fit stable GLM at link-year grain.** Probability medium-high on minor roads specifically. Mitigation: feasibility check (§4.3) before reporting comparison metrics.
- **Severity reporting break makes 2015–2024 window unusable as-is.** Probability medium. Mitigation: Part A runs first; window restriction documented before Part B.
- **EB k for KSI is unstable due to per-bin dispersion variation (already observed at ~3,400× for all-injury; expected to be worse for KSI).** Mitigation: report bin-level dispersion explicitly; if global k is uninterpretable, retreat to family-stratified k for the ranking comparison.
- **Confirmation bias toward the "build KSI" outcome.** Mitigation: §6 above; pre-commit the negative-result narrative.

---

## 9. Decisions made at write time

These are recorded so future readers can distinguish them from decisions made during analysis:

- KSI defined as fatal + serious (combined). Fatal-only as separate target is not tested in this diagnostic — too sparse to be useful at link-year grain.
- GLM only. XGBoost-on-KSI is downstream.
- Same feature set as current all-injury Stage 2 GLM. Feature selection for KSI specifically is a downstream task if KSI proceeds.
- EB shrinkage applied to both rankings. Comparing raw model output would be dominated by KSI noise on sparse links.
- Jaccard threshold of 0.70 / 0.85 as the primary gate. These match the rank-stability noise envelope (0.918 baseline) — meaningful operational difference must be visible above seed-level noise.

---

## 10. Sign-off

This document is committed to the repository at write time. Any subsequent change to thresholds or methodology in §3 or §4 must be documented with a new section noting the change, its date, and the reason, before further analysis is run.
