---
title: "Stage 2 GLM: Exposure offset experiment"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** GLM-only diagnostic. No production models changed.
**Purpose:** Test whether fixed exposure offset (β=1 forced) is misspecified relative to
empirically learned β values, and measure impact on residual bias by road class and AADT extremes.

---

## 1. Background

The current Stage 2 GLM uses `log(AADT × length × 365/1e6)` as a fixed Poisson offset,
which forces the exposure scaling coefficient β=1. The `collision-exposure-behaviour.qmd`
diagnostic showed empirical β values of 0.46–0.81 across road classes, suggesting the offset
is misspecified. This experiment tests three formulations on the same downsampled training
data (ratio 1:10 zeros:positives) to isolate the exposure treatment effect.

Production baseline (collision_metrics.json): GLM pseudo-R²=0.351, XGBoost pseudo-R²=0.321.

---

## 2. Overdispersion check

| Statistic | Value |
|---|---:|
| Dispersion ratio (var/mean) | 1.401 |
| Threshold for NegBin | 1.5 |
| NegBin sensitivity | Not run (dispersion ratio 1.40 ≤ 1.5) |

---

## 3. Model variant summary

| Model | Exposure treatment | pseudo-R² | Deviance | AIC | Converged |
|---|---|---:|---:|---:|---|
| A (production) | Full offset: log(AADT×length×365/1e6) | 0.3117 | 1,499,899 | 2,314,204 | True |
| B (learned) | No offset; log_aadt + log_length as features | 0.3266 | 1,499,042 | 2,313,349 | True |
| C (hybrid) | Partial offset log(length×365/1e6); log_aadt learned | 0.2544 | 1,734,603 | 2,548,908 | True |

### Exposure coefficients

| Model | coef(log_aadt) | coef(log_length) | Note |
|---|---:|---:|---|
| A | — (β=1 forced) | -0.6564 | length residual adjustment |
| B | 0.9321 | 0.3392 | both freely learned |
| C | 1.1031 | — (β=1 via offset) | AADT freely learned |

### Top-1% ranking Jaccard vs production XGBoost

Computed from the downsampled GLM frame (all positive link-years + sampled zeros).
Directionally correct for diagnosis; not a full-population Jaccard.

| Comparison | Jaccard |
|---|---:|
| Model A GLM vs production XGBoost | 0.3748 |
| Model B GLM vs production XGBoost | 0.3819 |
| Model C GLM vs production XGBoost | 0.2790 |

### Motorway mean residual (observed − predicted, downsampled frame)

| Model | Mean residual |
|---|---:|
| A | 0.0000 |
| B | 0.0000 |
| C | 0.0000 |

Positive = model under-predicts (more collisions than expected).
Negative = model over-predicts.

---

## 4. Residuals by road class

### Model A (current offset)

| Road class | N | Obs | Pred | Mean resid |
|---|---:|---:|---:|---:|
| A Road | 404,175 | 174615 | 174615 | 0.0000 |
| B Road | 204,739 | 56216 | 78499 | -0.1088 |
| Classified Unnumbered | 399,428 | 65399 | 35334 | 0.0753 |
| Motorway | 13,996 | 16981 | 16981 | 0.0000 |
| Not Classified | 416,772 | 5133 | 15619 | -0.0252 |
| Unclassified | 2,043,277 | 121071 | 101163 | 0.0097 |
| Unknown | 821,418 | 11577 | 28781 | -0.0209 |

### Model B (learned exposure)

| Road class | N | Obs | Pred | Mean resid |
|---|---:|---:|---:|---:|
| A Road | 404,175 | 174615 | 174615 | 0.0000 |
| B Road | 204,739 | 56216 | 77069 | -0.1019 |
| Classified Unnumbered | 399,428 | 65399 | 36816 | 0.0716 |
| Motorway | 13,996 | 16981 | 16981 | 0.0000 |
| Not Classified | 416,772 | 5133 | 16518 | -0.0273 |
| Unclassified | 2,043,277 | 121071 | 100637 | 0.0100 |
| Unknown | 821,418 | 11577 | 28356 | -0.0204 |

### Model C (hybrid)

| Road class | N | Obs | Pred | Mean resid |
|---|---:|---:|---:|---:|
| A Road | 404,175 | 174615 | 174615 | 0.0000 |
| B Road | 204,739 | 56216 | 79501 | -0.1137 |
| Classified Unnumbered | 399,428 | 65399 | 37920 | 0.0688 |
| Motorway | 13,996 | 16981 | 16981 | 0.0000 |
| Not Classified | 416,772 | 5133 | 13430 | -0.0199 |
| Unclassified | 2,043,277 | 121071 | 93774 | 0.0134 |
| Unknown | 821,418 | 11577 | 34771 | -0.0282 |

---

## 5. Residuals by AADT decile

Decile 0 = lowest traffic, 9 = highest. Net residual = sum(observed) − sum(predicted) across all rows in decile.

### Model A

| Decile | Mean AADT | Obs | Pred | Net resid |
|---|---:|---:|---:|---:|
| 0 | 232 | 2106 | 6575 | -4469.0 |
| 1 | 354 | 5619 | 9208 | -3589.0 |
| 2 | 438 | 7270 | 10336 | -3066.5 |
| 3 | 520 | 9271 | 11861 | -2590.3 |
| 4 | 631 | 12770 | 14512 | -1742.0 |
| 5 | 835 | 20299 | 19553 | 745.9 |
| 6 | 1,214 | 34253 | 28173 | 6080.2 |
| 7 | 1,851 | 54912 | 41760 | 13152.2 |
| 8 | 3,854 | 98390 | 84563 | 13827.0 |
| 9 | 14,633 | 206102 | 224451 | -18348.5 |

### Model B

| Decile | Mean AADT | Obs | Pred | Net resid |
|---|---:|---:|---:|---:|
| 0 | 232 | 2106 | 7231 | -5125.5 |
| 1 | 354 | 5619 | 9929 | -4309.8 |
| 2 | 438 | 7270 | 11022 | -3752.0 |
| 3 | 520 | 9271 | 12533 | -3261.6 |
| 4 | 631 | 12770 | 15183 | -2412.6 |
| 5 | 835 | 20299 | 20136 | 163.2 |
| 6 | 1,214 | 34253 | 28314 | 5939.2 |
| 7 | 1,851 | 54912 | 41104 | 13808.2 |
| 8 | 3,854 | 98390 | 84044 | 14346.1 |
| 9 | 14,633 | 206102 | 221497 | -15395.2 |

### Model C

| Decile | Mean AADT | Obs | Pred | Net resid |
|---|---:|---:|---:|---:|
| 0 | 232 | 2106 | 8601 | -6494.8 |
| 1 | 354 | 5619 | 10063 | -4444.5 |
| 2 | 438 | 7270 | 10256 | -2986.2 |
| 3 | 520 | 9271 | 11741 | -2470.0 |
| 4 | 631 | 12770 | 15011 | -2241.0 |
| 5 | 835 | 20299 | 20709 | -409.6 |
| 6 | 1,214 | 34253 | 28076 | 6176.9 |
| 7 | 1,851 | 54912 | 41010 | 13902.0 |
| 8 | 3,854 | 98390 | 89576 | 8814.1 |
| 9 | 14,633 | 206102 | 215949 | -9846.9 |

---

## 6. Interpretation

The learned-exposure GLM (Model B) is the strongest formulation in this experiment. It improves pseudo-R² from 0.3117 to 0.3266 and lowers AIC relative to the current fixed-offset formulation. The hybrid model performs materially worse and should not be adopted.

The experiment does not support the strongest version of the earlier diagnostic claim that exposure scaling is globally in the 0.4–0.8 range. Once the wider Stage 2 feature set is included, learned AADT scaling is 0.9321: mildly sub-linear, but still close to linear.

The larger finding is length scaling. The current offset forces both AADT and length to scale at β=1, but Model B learns `log_length` at 0.3392. Model A already compensates for this via a negative `log_length` coefficient (-0.6564), implying an effective length coefficient of roughly 0.34. This suggests the current full-exposure offset is mainly misspecified through link length, not AADT.

Residuals by AADT decile show Model B modestly reduces over-prediction in the highest AADT decile, but worsens over-prediction in the lowest deciles. The residual pattern remains non-monotonic, so a single learned exposure coefficient does not fully solve calibration across the traffic distribution.

Motorway residuals on the downsampled training frame are not informative because the aggregate mean residual is exactly zero across all variants. The motorway under-prediction question should be tested on the full scored network using the existing family residual diagnostic.

Conclusion: adopt Model B as the preferred diagnostic GLM formulation for v3 consideration, but do not change production ranking yet. The next step is to run full-frame residual diagnostics by AADT decile and facility family, then compare whether Model B improves calibration without destabilising the top-risk list.

---

## 7. Next steps

Based on findings:
- If Model C shows materially lower residual bias at AADT extremes with comparable or better
  pseudo-R²: consider adopting hybrid offset as the v3 GLM formulation.
- If B and C show similar results: the AADT scaling is the dominant issue; length can stay fixed.
- If motorway under-prediction persists across all variants: the problem is not exposure treatment
  alone — investigate motorway-specific features or per-family GLMs.
- Per-family k values (EB shrinkage v2) remain the recommended next step regardless of outcome.

_Machine-readable results: `docs/internal/exposure_offset_experiment.json`_
