---
title: "Stage 2 GLM: Per-family intercept calibration diagnostic"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** Diagnostic only. No production models changed. No retraining.
**Model:** Model A (full offset). Model B excluded from per-family analysis.
**Frame:** All tables use the full ~21M-row scored population.

Comparisons: **raw** (uncalibrated) · **global-cal** (single intercept correction) · **family-cal** (per-family intercept correction).

---

## 1. What this diagnostic tests

The global intercept calibration corrects the downsampling intercept bias (factor applies
uniformly to all links). The open question is: does a *per-family* intercept — keeping all
slopes fixed — reduce the remaining family-level residual bias observed after global
calibration, and does it do so without damaging AADT decile or top-risk-band calibration?

The per-family factor is:
`factor_f = sum_obs_f / sum_pred_a_raw_f`
`pred_a_family_cal = pred_a * factor_f`

This is a multiplicative intercept correction per facility family. It cannot change
within-family AADT or link-length residual patterns; it only shifts the level.

---

## 2. Calibration factors

| Family | N rows | Obs | Raw pred | Global-cal pred | Family-cal pred | Factor | Log correction |
|---|---:|---:|---:|---:|---:|---:|---:|
| motorway | 40,840 | 16,981 | 32,092 | 7,901 | 16,981 | 0.5291 | -0.6365 |
| other | 3,301,370 | 30,205 | 154,926 | 38,141 | 30,205 | 0.1950 | -1.6349 |
| other_rural | 4,769,600 | 56,742 | 341,750 | 84,134 | 56,742 | 0.1660 | -1.7956 |
| other_urban | 13,403,650 | 328,333 | 1,244,243 | 306,316 | 328,333 | 0.2639 | -1.3323 |
| trunk_a | 160,110 | 18,731 | 58,901 | 14,501 | 18,731 | 0.3180 | -1.1457 |

The log correction is the implied intercept shift (log-scale). Family-cal pred ≈ obs by construction.

---

## 3. Residuals by road family

rel_resid = (obs − pred) / pred. Positive = under-prediction. Negative = over-prediction.
family_vs_global > 0 means family-cal is better calibrated than global-cal.

| Family | N | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|
| motorway | 40,840 | 16,981 | -0.4709 | +1.1494 | +0.0000 | +1.1494 |
| other | 3,301,370 | 30,205 | -0.8050 | -0.2081 | -0.0000 | +0.2081 |
| other_rural | 4,769,600 | 56,742 | -0.8340 | -0.3256 | -0.0000 | +0.3256 |
| other_urban | 13,403,650 | 328,333 | -0.7361 | +0.0719 | -0.0000 | +0.0719 |
| trunk_a | 160,110 | 18,731 | -0.6820 | +0.2917 | +0.0000 | +0.2917 |

---

## 4. Residuals by road classification

| Class | N | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|
| A Road | 1,555,380 | 174,615 | -0.7069 | +0.1906 | +0.1805 | +0.0101 |
| B Road | 892,860 | 56,216 | -0.8196 | -0.2673 | -0.2302 | +0.0371 |
| Classified Unnumbered | 1,909,210 | 65,399 | -0.5787 | +0.7113 | +0.8821 | -0.1707 |
| Motorway | 40,840 | 16,981 | -0.4709 | +1.1494 | +0.0000 | +1.1494 |
| Not Classified | 2,248,780 | 5,133 | -0.9386 | -0.7505 | -0.7367 | +0.0138 |
| Unclassified | 10,600,140 | 121,071 | -0.7581 | -0.0172 | -0.0231 | -0.0058 |
| Unknown | 4,428,360 | 11,577 | -0.9244 | -0.6931 | -0.6682 | +0.0249 |

---

## 5. Residuals by AADT decile

Decile 0 = lowest AADT, 9 = highest. This is the key test: does family calibration
damage within-decile calibration?

| Decile | N | Mean AADT | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2,183,050 | 227 | 1,803 | -0.9447 | -0.7754 | -0.7196 | +0.0558 |
| 1 | 2,163,967 | 344 | 4,972 | -0.8897 | -0.5520 | -0.4905 | +0.0614 |
| 2 | 2,174,124 | 424 | 6,598 | -0.8707 | -0.4747 | -0.4295 | +0.0452 |
| 3 | 2,154,994 | 499 | 8,161 | -0.8568 | -0.4182 | -0.3807 | +0.0375 |
| 4 | 2,167,000 | 593 | 10,827 | -0.8401 | -0.3504 | -0.3076 | +0.0428 |
| 5 | 2,163,503 | 750 | 16,636 | -0.8097 | -0.2271 | -0.1676 | +0.0595 |
| 6 | 2,170,525 | 1,048 | 27,354 | -0.7757 | -0.0888 | -0.0464 | +0.0424 |
| 7 | 2,165,429 | 1,564 | 46,730 | -0.7357 | +0.0735 | +0.0863 | -0.0128 |
| 8 | 2,165,585 | 2,695 | 83,766 | -0.7138 | +0.1626 | +0.1840 | -0.0214 |
| 9 | 2,167,393 | 11,808 | 244,145 | -0.7286 | +0.1023 | +0.0524 | +0.0498 |

---

## 6. Residuals by top-risk band (common Model A ranking)

Bands are fixed by raw Model A link-level predicted rate. All three variants are
evaluated on the same link groups. This tests whether family calibration shifts
risk within the top-risk population.

| Band | Links | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|
| bottom_80pct | 1,734,045 | 109,577 | -0.8204 | -0.2706 | -0.2313 | +0.0393 |
| 5_to_20pct | 325,134 | 160,386 | -0.7244 | +0.1196 | +0.1330 | -0.0134 |
| 1_to_5pct | 86,702 | 110,971 | -0.7367 | +0.0694 | +0.0550 | +0.0145 |
| top_1pct | 21,676 | 70,058 | -0.6791 | +0.3037 | +0.1357 | +0.1679 |

---

## 7. Interpretation

### Motorway calibration
Motorway: raw=-0.4709, global-cal=+1.1494, family-cal=+0.0000 (by definition ≈ 0).

Motorway family-cal rel_resid is ≈ 0 by construction (factor forces sum_pred = sum_obs
at family level). Whether the motorway issue is structural is not answered by the global
AADT decile table. It requires a within-motorway diagnostic: residuals by AADT decile
using motorway rows only, after family intercept calibration.

### Top-risk bands
Top-1% band: raw=-0.6791, global-cal=+0.3037, family-cal=+0.1357.

### Summary

Family calibration improves 8/10 global AADT deciles.
It worsens 2 decile(s) by more than 1 percentage point, but improves the
highest-AADT decile and substantially improves the lowest-to-mid deciles.

**Recommendation:** Treat per-family intercept calibration as a candidate v3 GLM calibration layer, not yet a production change. The follow-up gate is within-family AADT-decile diagnostics, especially motorway and trunk-A. If those show no major residual slope pattern, family intercept calibration is probably enough for the GLM. If they show systematic high-AADT or low-AADT bias within family, move to family-specific slopes or interactions.

### Next steps
- If motorway rel_resid at the family level is ≈ 0 (by construction) but AADT decile 9
  (highest traffic) still shows bias, the motorway problem is a slope/composition issue,
  not an intercept issue. Per-family GLM slopes are needed.
- Top-risk-band calibration improves at the bottom 80%, 1–5%, and top 1% bands, with the
  largest gain in the top 1% band. The 5–20% band worsens slightly.
- Consider applying family calibration as a post-scoring step in the EB shrinkage workflow
  rather than in the GLM itself, to keep the model unchanged.

_Machine-readable: `docs/internal/family_intercept_calibration_diagnostics.json`_
