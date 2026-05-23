# Consistency Review — 2026-05-23

Forensic sweep of `.md` and `.qmd` files for stale numbers, contradictions,
and wording left over from the pre-hgv-fix model era. Findings are grouped by
severity. Source of each finding is a file path and line number confirmed by
grep.

---

## Ground truth used for comparison

| Metric | Correct current value | Source |
|---|---|---|
| XGBoost pseudo-R² (post-fix) | 0.323 ± 0.003 | `reports/rank_stability.md:14-15` |
| XGBoost pseudo-R² (pre-fix, leaky) | ~0.86, 0.858, 0.859 | stale; `reports/family_validation.md:3` confirms supersession |
| Top-1% pairwise Jaccard (post-fix noise floor) | 0.904 | `reports/rank_stability.md:22` |
| Top-1% pairwise Jaccard (pre-fix run) | 0.918 | stale; `todo/done.md:167` |
| EB k (production, positive-event weighted) | 3.451158 | `data/provenance/eb_dispersion_provenance.json:489` |
| EB k (pre-fix run, stale) | ≈ 3.07 | stale; only in done.md and content-audit notes |
| EB top-1% intersection (EB vs non-EB, post-fix) | 38.85% | `reports/eb_validation.md:56` |
| EB top-1% intersection (pre-fix run, stale) | 84.93% | stale; pre-dates hgv-fix |
| GLM pseudo-R² post-tiered-imputation | 0.301 | `data/provenance/speed_limit_effective_provenance.json` |
| OSM speed_limit_mph coverage (raw) | 56.4% | `todo/osm_features.md:6` |
| OSM speed_limit_mph_effective coverage | 91.27% | `data/provenance/speed_limit_effective_provenance.json:90` |
| Top-1% link count | 21,675 | `reports/rank_stability.md:20` |
| Active speed feature in model | `speed_limit_mph_effective` | `quarto/methodology/feature-engineering.qmd:297` |

---

## Critical — wrong number in a current-context claim, no qualifier

### C1 — KSI preregistration cites superseded XGB pseudo-R² and Jaccard noise floor

**File:** `reports/preregistration/ksi_diagnostic_preregistration.md:25-26`

```
- XGBoost is saturated at all-injury pseudo-R² ~0.859 across multiple feature batches.
- Top-1% Jaccard noise floor under feature changes is 0.918 (5-seed harness baseline;
  `reports/rank_stability.md`).
```

Both values are from the pre-hgv-fix era. `reports/rank_stability.md` now reports
pseudo-R² 0.323 and top-1% Jaccard 0.904. The preregistration was written before
the hgv-fix and correctly described the state at writing — but a reader comparing
this document against the current `rank_stability.md` will see contradictory values
with no explanation.

**Implication for Part B:** if Part B of the KSI diagnostic is ever run, the
pre-registered noise floor (0.918) no longer matches the current harness baseline
(0.904). The pre-registered threshold is locked in by definition and should not be
changed retroactively, but the discrepancy should be acknowledged in a note rather
than left as a silent contradiction.

**Fix:** add a note to the preregistration (not editing the pre-registered rule
itself) stating that the 0.859 / 0.918 figures were the correct baselines at the
time of pre-registration and have since been superseded by the post-hgv-fix run
(0.323 / 0.904). Alternatively document this in the decision register if/when
Part B is scoped.

---

### C2 — `docs/internal/sites_todo.md:33` cites stale Jaccard

**File:** `docs/internal/sites_todo.md:33`

```
`reports/rank_stability.md` — Spearman 0.998 and Jaccard 0.918 across seeds.
```

Current `rank_stability.md` shows Jaccard 0.904 and Spearman 0.999. Both values
are wrong. This is a live planning document, not archival.

---

### C3 — `docs/internal/feature_addition_imd_grade.md` cites 0.918 as the
current noise floor in interpretation text

**Files:** `docs/internal/feature_addition_imd_grade.md:14, 31, 196`
and the duplicate `todo/feature_addition_imd_grade.md` (same content)

```
Reference baselines: ... top-1% 5-seed Jaccard 0.918 (`reports/rank_stability.md`).
The 5-seed baseline for the global XGBoost model is top-1% Jaccard 0.918
(`reports/rank_stability.md`); this comparison gives 0.918.
```

The interpretation on line 196 declares the IMD/grade feature additions
"within the seed-noise envelope" by comparing to 0.918 — but the envelope is
now 0.904. The conclusion (additions didn't move the ranking) is likely still
correct, but the stated justification uses the wrong reference. Any future
reader scanning for "what is the noise floor?" will find 0.918 here and 0.904
in `rank_stability.md` with no explanation.

**Fix:** note that the 0.918 figure was the baseline at the time of the IMD/grade
experiment and has since been revised to 0.904 post-hgv-fix, and that the
conclusion is unchanged under either value.

---

### C4 — `model-inventory.qmd:148` top-1% count off by one

**File:** `quarto/methodology/model-inventory.qmd:148`

```
The effective-speed retrain retained 2,167,557 scored links and 21,676 top-1% links.
```

All other sources (`reports/rank_stability.md`, `reports/eb_validation.md`,
`reports/family_validation.md`, `data/provenance/rank_stability_provenance.json`)
give **21,675**. 21,676 is inconsistent by one link; likely a rounding or
off-by-one in the script that generated this sentence.

---

## Minor — stale but clearly historical, or in archival/internal-notes context

### M1 — `done.md` carries multiple stale EB figures

**File:** `todo/done.md:121, 125, 167`

Lines 121, 125: `k ≈ 3.07`, `top-1% intersection 84.93%, ~3,267 links`.
Line 167: `Pseudo-R² highly stable (0.8590 ± 0.0014). Top-1% Jaccard averages 0.918`.

These are all from pre-hgv-fix runs. `done.md` is an archival log rather than a
live reference document, so these are not blocking — but they are the direct source
of confabulation risk for anyone (human or AI) summarising project state from
`done.md` alone. No action required unless `done.md` is used as a reference
rather than a log.

---

### M2 — Content-audit notes carry stale EB k and Jaccard

**Files:** `docs/notes/content-audit-2026-04-27-v3.md:26`,
`docs/notes/content-audit-2026-04-27-v4.md:26, 118`,
`docs/notes/content-audit-2026-04-27-v5.md:26, 121`

All cite `k ≈ 3.07`, `84.9%` intersection, Jaccard `0.918`. These are
April 2026 audit snapshots written before the hgv-fix. Archival; do not edit.

---

### M3 — `reports/preregistration/ksi_diagnostic_preregistration.md:25`
XGB `~0.859` used as the stability-saturation claim

The document says "XGBoost is saturated at all-injury pseudo-R² ~0.859 across
multiple feature batches. Feature additions move the headline metric by ≤0.001
(RUC, IMD, grade)."

The saturation claim was correct at the time of writing and is still directionally
correct post-fix (IMD/grade moves were ≤0.001 at the post-fix baseline too). The
specific figure is stale; the conclusion holds. See C1 for recommended handling.

---

### M4 — Deep-research notes (April 2026) list `speed_limit_mph` in XGBoost feature list

**Files:** `docs/notes/2026-04-19-deep-research-report.md:23`,
`docs/notes/2026-04-19-deep-research-report-followup.md:24-25`

Both were written against commit `36d26c5` from April 2026, before the tiered
imputation replaced raw `speed_limit_mph` with `speed_limit_mph_effective`.
Archival; do not edit.

---

### M5 — `todo/osm_features.md` describes tiered imputation as a queued task

**File:** `todo/osm_features.md`

The file still reads as a planning/queued document for OSM speed-limit tiered
imputation. This task was completed on 24 April 2026 and adopted into production.
The file should either be moved to `todo/done.md` (already captured there) or
have a completion header added.

---

### M6 — `future-work.qmd` prereqs reference EB and family-split as not-yet-in-place

**File:** `quarto/future-work.qmd:91, 144, 176`

Lines include:
```
5-seed stability harness (see `TODO.md` → Queued tasks) to be in place
After EB shrinkage and facility-family split are in place, add fatal_count target
```

The 5-seed harness, EB v1, and family-split v1 are all done (v1 diagnostic).
"In place" is now true for EB and partially true for family-split (diagnostic
only, not production). The prereq language is no longer accurate and may
misdirect a reader about current project state. Minor because it's the
future-work page, not the methodology.

---

### M7 — `feature_addition_imd_grade.md` table shows XGB 0.858/0.859 without clear supersession marker in the table itself

**File:** `docs/internal/feature_addition_imd_grade.md:131-133`

```
| Pre-IMD baseline | 0.301 | 0.858 (historical, superseded) | ...
| Post-IMD ...     | 0.325 | 0.859 (historical, superseded) | ...
| Post-grade ...   | 0.347 | 0.859 (historical, superseded) | ...
```

The "(historical, superseded)" qualifiers are already present. Well-handled;
no action needed.

---

## Cosmetic — wording inconsistencies and minor discrepancies

### Cos1 — `feature-engineering.qmd:561` union count arithmetic

**File:** `quarto/methodology/feature-engineering.qmd:561`

```
top-1% Jaccard overlap was 0.9512 (21,134 shared links out of 22,218 in the union)
```

This is the pre-effective-speed vs post-effective-speed comparison, not a
cross-seed comparison. The numbers are internally consistent (Jaccard =
21,134/22,218 = 0.9512). However, the union of 22,218 from two 21,675-link sets
implies 21,132 intersection, not 21,134 — one-link discrepancy in the stated
intersection count. Cosmetic; not worth investigating.

---

### Cos2 — `quarto/methodology/empirical-bayes-shrinkage.qmd §9` was updated correctly

**File:** `quarto/methodology/empirical-bayes-shrinkage.qmd:732-735`

The section now reads:
```
top-1% intersection is 38.85% (8,421 of 21,675 links); median absolute percentile
change is 0.491798 points; p99 change is 29.312792 points. These figures are from
`reports/eb_validation.md` using production k = 3.451158...
```

**No issue.** The page was updated with post-fix figures and explicitly cites the
source artefact. Note for record: the pre-fix figures (84.93%, 0.07pts, 2.96pts)
appear only in `todo/done.md` and the April 2026 content-audit notes (M1, M2).

---

### Cos3 — `docs/internal/temporal_changes_plan.md` references old band names in description of the *problem*

**File:** `docs/internal/temporal_changes_plan.md:46, 62-63`

References to `peak_offpeak_ratio`, `prepeak_frac`, `preoffpeak_frac` appear in
the section documenting the mislabelling bug that Step 0 fixed. The document
correctly marks Step 0 as complete and the names are correct in the "after" state.
No action needed; the old names appear only in the "before" context.

---

### Cos4 — EB formula in `eb_shrinkage.py` is non-standard; no documentation note

**File:** `src/road_risk/model/eb_shrinkage.py:79`

The implementation uses `eb_weight = 1 / (1 + k * n_pred)` rather than the
standard NB2 formula `k / (k + n_pred)`. At k = 3.451 these diverge significantly:
for a link with n_pred = 9.46 (predicted_xgb ≈ 0.946 over 10 years), the
implementation gives eb_weight ≈ 0.030 while standard NB2 would give ≈ 0.267.
The implementation formula is consistent with the reported eb_weight values in
`reports/eb_validation.md` (verified by back-calculation), so the code is
correct — but neither `eb_shrinkage.py` nor the Quarto methodology page
explains why the non-standard parameterisation was chosen. If the k value is
ever re-estimated or compared against literature NB2 k values, the parameterisation
difference will cause confusion.

---

## Summary table

| ID | File | Issue | Severity |
|---|---|---|---|
| C1 | `reports/preregistration/ksi_diagnostic_preregistration.md:25-26` | 0.859 pseudo-R² and 0.918 Jaccard cited as current; rank_stability.md now shows 0.323 / 0.904 | Critical |
| C2 | `docs/internal/sites_todo.md:33` | Jaccard 0.918 and Spearman 0.998 — both stale; correct values 0.904 / 0.999 | Critical |
| C3 | `docs/internal/feature_addition_imd_grade.md:14,31,196` | 0.918 cited as current noise floor in interpretation; correct is 0.904 | Critical |
| C4 | `quarto/methodology/model-inventory.qmd:148` | 21,676 top-1% links; should be 21,675 | Critical |
| M1 | `todo/done.md:121,125,167` | k≈3.07, 84.93%, 0.8590±0.0014, 0.918 — all pre-fix; archival log | Minor |
| M2 | `docs/notes/content-audit-2026-04-27-v*.md` | k≈3.07, 84.9%, 0.918 — April 2026 snapshots; archival | Minor |
| M3 | `reports/preregistration/ksi_diagnostic_preregistration.md:25` | 0.859 saturation claim stale; conclusion still holds | Minor |
| M4 | `docs/notes/2026-04-19-deep-research-report*.md` | `speed_limit_mph` in feature list; pre-tiered-imputation snapshot | Minor |
| M5 | `todo/osm_features.md` | Tiered imputation still described as queued; task is done | Minor |
| M6 | `quarto/future-work.qmd:91,144,176` | EB / family-split described as future prereqs; both done at v1 | Minor |
| M7 | `docs/internal/feature_addition_imd_grade.md:131-133` | XGB 0.858/0.859 in table — already marked (historical, superseded) | Minor (well-handled) |
| Cos1 | `quarto/methodology/feature-engineering.qmd:561` | Union intersection count 21,134 off by 2 | Cosmetic |
| Cos2 | `quarto/methodology/empirical-bayes-shrinkage.qmd:732` | §9 was updated correctly; record only | None (resolved) |
| Cos3 | `docs/internal/temporal_changes_plan.md:46,62-63` | Old band names in "before" description; context is correct | Cosmetic |
| Cos4 | `src/road_risk/model/eb_shrinkage.py:79` | Non-standard EB formula undocumented; correct but confusing | Cosmetic |
