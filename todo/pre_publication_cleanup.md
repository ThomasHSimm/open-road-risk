# Pre-publication cleanup — triage

Triage of the 15 verification items (R1–R15) ahead of the ResearchGate
methodology publication. State for each item was confirmed by reading the
referenced files on branch `walkthroughs` (commit `4745cdb`), not inferred.

Ground-truth current values (from `reports/rank_stability.md` /
`data/provenance/rank_stability_provenance.json`): XGB pseudo-R² 0.323,
top-1% Jaccard 0.904 (mean 0.90357 @ 21,675 links), Spearman 0.999,
top-1% link count **21,675**, production EB k = 3.451158.

---

## Pre-publication blockers

Items that should be closed before the methodology document is shared
externally, because they are factual errors inside the published Quarto site.

| R | Item | Cross-ref | File(s) | Effort |
|---|---|---|---|---|
| **R5** | `model-inventory.qmd:148` says 21,676 top-1% links; all provenance sources say **21,675**. This page is part of the published methodology site, so the off-by-one is reader-visible. | C4 | `quarto/methodology/model-inventory.qmd:148` | ~5 min |

That is the only genuine blocker among the 15. **R6 — the item you flagged as
the one real blocker — is not a blocker** (see below): `collision_xgb.json`
postdates the leakage fix, so the reproducibility claim holds.

---

## Concurrent with publication

Cheap corrections / notes. The methodology document discloses the underlying
open work, so none of these block it, but each removes a stale-number or
parameterisation-confusion risk and can be done in parallel.

| R | Item | State | Cross-ref | File(s) | Effort |
|---|---|---|---|---|---|
| **R2** | Add supersession note to KSI preregistration: the 0.859 pseudo-R² / 0.918 Jaccard were correct at pre-registration, superseded post-hgv-fix by 0.323 / 0.904. Annotation only — do **not** edit the pre-registered rule. | open | C1 | `reports/preregistration/ksi_diagnostic_preregistration.md:25-26` | ~15 min |
| **R3** | `sites_todo.md:33` cites Spearman 0.998 and Jaccard 0.918 as current; should be 0.999 / 0.904. Internal planning doc. | open | C2 | `docs/internal/sites_todo.md:33` | ~5 min |
| **R4** | The stale XGB pseudo-R² already carries a supersession note (lines 25–30), but the 0.918 Jaccard *noise-floor* references at lines 14, 31, 196 are still unqualified; should be annotated as superseded by 0.904. Conclusion ("ranking didn't move") unchanged under 0.904. | partially-closed | C3 | `docs/internal/feature_addition_imd_grade.md:14,31,196` (+ duplicate `todo/feature_addition_imd_grade.md`) | ~10 min |
| **R1** | EB methodology page already documents the NB2 convention `Var = E + k·E²` (§3, line 238) and derives `w = 1/(1 + k·N_pred)` (§2, line 183). What is missing is an explicit one-line note contrasting it with the alternative `k/(k+N_pred)` form, so a reader comparing literature NB2 k values is not confused. Confusion risk is already largely mitigated by §2/§3. | partially-closed | Cos4 | `quarto/methodology/empirical-bayes-shrinkage.qmd` (§2/§3) | ~20 min |
| **R8** | LIT-TODO-001 — exposure-offset support is documented across several methodology pages (`modelling.qmd`, `feature-engineering.qmd`, `model-inventory.qmd`); the published doc covers it in §6.1/§10.2. The thin part in-repo is a consolidated *limitations* note (elasticity / functional-form caveats). Register itself marks it "partly present, now". | partially-closed | LIT-TODO-001 | `quarto/methodology/modelling.qmd` (likely home) | ~30 min |
| **R13** | Khodadadi action item — **zero proportion is already reported** (0.9820, in `reports/zero_calibration.md` and the zero-calibration investigation). **Skewness is not computed anywhere.** Computing the link-year crash skewness is a single number and the precondition for the NB-2 vs NB-L decision in R10. | partially-closed | LIT-TODO-031 | new diagnostic; report alongside `reports/zero_calibration.md` | ~30 min |

---

## Post-publication

Substantive work the methodology document already acknowledges as open. Listed
for prioritisation, not as blockers.

| R | Item | State | Cross-ref | File(s) | Effort |
|---|---|---|---|---|---|
| **R10** | LIT-TODO-022 — NB GLM with exposure offset as a Stage 2 *candidate*, compared to Poisson via grouped-link CV. A global NB was already fitted in the zero-calibration diagnostic (α = 2.057, NB2), but **not** as a CV-compared Stage 2 candidate. The candidate fit + grouped-link CV comparison is the open part. | partially-closed | LIT-TODO-022 | `reports/`, `data/models/` | hours–days |
| **R12** | Refined LIT-TODO-002 — family-stratified free-AADT. The *global* version is done (Model A vs B, `exposure_offset_full_frame_intercept_diagnostics.md`); residuals are stratified by family, but `log_aadt` + `log_length` as free covariates **with road-family interactions** has not been fitted. §10 of that report names it as the recommended next step. | open (not started) | LIT-TODO-002 (refined) | `reports/exposure_offset_full_frame_intercept_diagnostics.md` (precursor) | hours |
| **R11** | LIT-TODO-023 — empirical variogram of Stage 2 Poisson residuals on a stratified subsample. No variogram/spatial-autocorrelation report found in `reports/` or `data/provenance/`. | open (not started) | LIT-TODO-023 | new report under `reports/` | hours |
| **R14** | Investigate `mean_grade` negative coefficient (−0.0202) stratified by road class. | open | `todo/model.md` (§ medium-priority, line 49) | `todo/model.md`; new diagnostic | hours |
| **R15** | Drop raw `betweenness` from GLM features (coef −8, collinear with `betweenness_relative`). Confirmed still in the feature list — `rank_stability_provenance.json` shows both `betweenness_imputed` and `betweenness_relative_imputed`. | open | `todo/model.md` (line 14) | `src/road_risk/model/collision.py`; retrain | hours (requires retrain) |
| **R7** | Yorkshire terminology in `src/`. **73 references across 12 real `.py` files** (excluding `__pycache__`/egg-info). Clusters: `ingest/ingest_webtris.py` (35), `ingest/ingest_stats19.py` (11), `ingest/legacy_ingest_mrdb.py` (7), plus a whole module `app/yorkshire.py` (9). They are a mix of module name, function names (`get_yorkshire_sites`, `pull_yorkshire`), constants (`YORKSHIRE_BBOX`, `_in_yorkshire_bbox`), comments, and docstrings — not just comments. No rename performed. | open | new (R-only) | `src/road_risk/{ingest,app,features,clean_join,diagnostics}/...` | hours (rename, low priority) |

---

## Closed (no action)

| R | Item | Evidence |
|---|---|---|
| **R6** | `data/models/collision_xgb.json` exists (3.6 MB), mtime **2026-05-04 11:04**, which is *after* the leakage-fix run (SHA `301a766b`, committed 2026-05-02 23:50; rank_stability run timestamp 2026-05-03). The artefact postdates the fix — it is **not** the pre-leakage-fix artefact. No retrain or removal needed; reproducibility claim holds. |
| **R9** | LIT-TODO-021 posterior-predictive zero check is **done thoroughly**: `reports/zero_calibration.md`, `quarto/investigations/zero-calibration.qmd`, `src/road_risk/diagnostics/zero_calibration.py`. Poisson fails (p = 0.000, ~2,900 missing zeros ≈ 16 SD); NB closes the gap (p = 0.722, α = 2.057). |

---

## What surprised me

The biggest surprise is **R6**, the one item you marked as a real
pre-publication blocker: the XGBoost artefact already postdates the leakage
fix by a day, so there is nothing to retrain or remove — the only genuine
blocker turns out to be the off-by-one in **R5**, a cosmetic-looking number
that happens to live in a published page. Several items you listed as open are
further along than expected: **R9** is fully done (and the NB fit inside it
already produced the global α = 2.057 that **R10** needs as a starting point),
and **R13**'s zero-proportion half is already reported in `zero_calibration.md`
— only the skewness number is genuinely missing. Two gaps not on your list worth
flagging without acting: the same 21,676 off-by-one (R5/C4) also appears in
`reports/exposure_offset_full_frame_intercept_diagnostics.md` §7–§8, so fixing
only `model-inventory.qmd:148` leaves a sibling inconsistency; and the
consistency review's Cos1 (`feature-engineering.qmd:561`, a 2-link union-count
discrepancy) is a published-page cosmetic error in the same family as R5,
though too minor to block.
