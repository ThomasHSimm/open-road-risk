---
title: "Stage 2 GLM: Full-frame exposure calibration diagnostics"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).  
**Scope:** GLM diagnostic only. No production models changed.  
**Models:** A (full offset) vs B (learned exposure). Model C dropped.  
**Frame:** Full scored population unless explicitly labelled as the downsampled training frame.

---

## 1. Why motorway residuals were exactly 0.0 in the training-frame report

The training-frame mean_resid is exactly 0.0 by construction. The Poisson GLM feature set includes 'is_motorway' and 'is_a_road' binary indicators. For a Poisson GLM with canonical log link, the score equations at convergence require Σ_i[x_ij*(y_i-μ_i)]=0 for every predictor j. For a binary indicator x_ij ∈ {0,1}, this becomes Σ_group(y_i-μ_i)=0 within the TRAINING FRAME — i.e. sum(obs) = sum(pred) exactly for motorway links in the training data. This is a GLM score-equation identity, not evidence of perfect calibration. Full-frame residuals are not constrained this way because the model was fitted on a downsampled subset.

### Training-frame motorway residuals

| Metric | Model A | Model B |
|---|---:|---:|
| N rows | 13,996 | — |
| sum_obs | 16981.000000 | — |
| sum_pred | 16981.000000 | 16981.000000 |
| net_resid | 0.000000 | 0.000000 |
| mean_resid | 0.000000 | 0.000000 |
| rel_resid | 0.000000 | 0.000000 |

### Full-frame motorway residuals — raw predictions

| Metric | Model A | Model B |
|---|---:|---:|
| N rows | 40,840 | — |
| sum_obs | 16981 | — |
| sum_pred | 32091.53 | 32383.62 |
| net_resid | -15110.53 | -15402.62 |
| rel_resid | -0.4709 | -0.4756 |

### Full-frame motorway residuals — intercept-calibrated predictions

| Metric | Model A | Model B |
|---|---:|---:|
| N rows | 40,840 | — |
| sum_obs | 16981 | — |
| sum_pred | 7900.50 | 7941.44 |
| net_resid | 9080.50 | 9039.56 |
| rel_resid | 1.1494 | 1.1383 |

---

## 2. Model summary

| | Model A | Model B |
|---|---:|---:|
| Exposure treatment | Full offset `log(AADT × length × 365 / 1e6)` | No offset; `log_aadt` + `log_length` as features |
| pseudo-R², training frame | 0.3117 | 0.3266 |
| coef(log_aadt) | forced = 1.0 | 0.9321 |
| coef(log_length) | -0.6564 | 0.3392 |
| effective length β | 0.3436 | 0.3392 |

Model A forces AADT and length to scale linearly through the offset, then partly offsets the length assumption through the learned `log_link_length` correction. Model B learns both terms directly. In this diagnostic GLM, AADT is only mildly sub-linear, while length is strongly sub-linear.

---

## 3. Intercept calibration

The raw full-frame predictions are affected by zero-downsampling intercept bias. The calibrated predictions apply a single multiplicative correction so that total predicted collisions match total observed collisions on the full scored frame.

| | Model A | Model B |
|---|---:|---:|
| raw sum_pred | 1,831,911 | 1,839,057 |
| calibrated sum_pred | 450,992 | 450,992 |
| sum_obs | 450,992 | 450,992 |
| calibration factor | 0.246187 | 0.245230 |
| log correction | -1.401665 | -1.405559 |

The raw tables show the downsampling calibration problem. The calibrated tables are the cleaner basis for structural residual diagnosis.

---

## 4. Calibrated residuals by AADT decile

Decile 0 = lowest AADT. Positive net residual means under-prediction. `Improvement > 0` means Model B has smaller absolute relative residual than Model A.

| Decile | N | Mean AADT | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2,183,050 | 227 | 1,803 | -6,223 | -0.7754 | -6,999 | -0.7952 | -0.0198 |
| 1 | 2,163,967 | 344 | 4,972 | -6,126 | -0.5520 | -6,962 | -0.5834 | -0.0314 |
| 2 | 2,174,124 | 424 | 6,598 | -5,963 | -0.4747 | -6,764 | -0.5062 | -0.0315 |
| 3 | 2,154,994 | 499 | 8,161 | -5,866 | -0.4182 | -6,631 | -0.4483 | -0.0301 |
| 4 | 2,167,000 | 593 | 10,827 | -5,840 | -0.3504 | -6,587 | -0.3783 | -0.0279 |
| 5 | 2,163,503 | 750 | 16,636 | -4,889 | -0.2271 | -5,579 | -0.2511 | -0.0240 |
| 6 | 2,170,525 | 1,048 | 27,354 | -2,665 | -0.0888 | -2,962 | -0.0977 | -0.0089 |
| 7 | 2,165,429 | 1,564 | 46,730 | +3,200 | +0.0735 | +3,784 | +0.0881 | -0.0146 |
| 8 | 2,165,585 | 2,695 | 83,766 | +11,717 | +0.1626 | +13,403 | +0.1905 | -0.0279 |
| 9 | 2,167,393 | 11,808 | 244,145 | +22,653 | +0.1023 | +25,298 | +0.1156 | -0.0133 |

---

## 5. Calibrated residuals by road family

| Family | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
| motorway | 40,840 | 16,981 | +9,080 | +1.1494 | +9,040 | +1.1383 | +0.0111 |
| other | 3,301,370 | 30,205 | -7,936 | -0.2081 | -10,185 | -0.2522 | -0.0441 |
| other_rural | 4,769,600 | 56,742 | -27,392 | -0.3256 | -28,877 | -0.3373 | -0.0117 |
| other_urban | 13,403,650 | 328,333 | +22,017 | +0.0719 | +25,856 | +0.0855 | -0.0136 |
| trunk_a | 160,110 | 18,731 | +4,230 | +0.2917 | +4,166 | +0.2861 | +0.0057 |

---

## 6. Calibrated residuals by road classification

| Class | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Road | 1,555,380 | 174,615 | +27,950 | +0.1906 | +27,955 | +0.1906 | -0.0000 |
| B Road | 892,860 | 56,216 | -20,507 | -0.2673 | -19,106 | -0.2537 | +0.0136 |
| Classified Unnumbered | 1,909,210 | 65,399 | +27,184 | +0.7113 | +25,552 | +0.6412 | +0.0701 |
| Motorway | 40,840 | 16,981 | +9,080 | +1.1494 | +9,040 | +1.1383 | +0.0111 |
| Not Classified | 2,248,780 | 5,133 | -15,442 | -0.7505 | -16,554 | -0.7633 | -0.0128 |
| Unclassified | 10,600,140 | 121,071 | -2,121 | -0.0172 | -1,405 | -0.0115 | +0.0058 |
| Unknown | 4,428,360 | 11,577 | -26,143 | -0.6931 | -25,482 | -0.6876 | +0.0055 |

---

## 7. Calibrated top-risk bands

Bands are defined separately for each model using that model's own link-level predicted rate. Residuals use summed link-year predictions, not `mean × global n_years`.

### Model A own-rank bands

| Band | Links | Obs | Pred | Net resid | Rel resid |
|---|---:|---:|---:|---:|---:|
| bottom_80pct | 1,734,045 | 109,577 | 150,229 | -40,652 | -0.2706 |
| 5_to_20pct | 325,134 | 160,386 | 143,256 | +17,130 | +0.1196 |
| 1_to_5pct | 86,702 | 110,971 | 103,768 | +7,203 | +0.0694 |
| top_1pct | 21,676 | 70,058 | 53,740 | +16,318 | +0.3037 |

### Model B own-rank bands

| Band | Links | Obs | Pred | Net resid | Rel resid |
|---|---:|---:|---:|---:|---:|
| bottom_80pct | 1,734,045 | 108,468 | 154,287 | -45,819 | -0.2970 |
| 5_to_20pct | 325,134 | 161,298 | 142,212 | +19,086 | +0.1342 |
| 1_to_5pct | 86,702 | 110,932 | 102,367 | +8,565 | +0.0837 |
| top_1pct | 21,676 | 70,294 | 52,127 | +18,167 | +0.3485 |

---

## 8. Calibrated top-risk bands on common Model A basis

These bands use Model A's link-level ranking as the fixed basis, then compare Model A and Model B predictions on exactly the same link groups. This is the cleaner operational comparison.

| Band | Links | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
| bottom_80pct | 1,734,045 | 109,577 | -40,652 | -0.2706 | -44,839 | -0.2904 | -0.0198 |
| 5_to_20pct | 325,134 | 160,386 | +17,130 | +0.1196 | +18,251 | +0.1284 | -0.0088 |
| 1_to_5pct | 86,702 | 110,971 | +7,203 | +0.0694 | +8,630 | +0.0843 | -0.0149 |
| top_1pct | 21,676 | 70,058 | +16,318 | +0.3037 | +17,959 | +0.3447 | -0.0411 |

---

## 9. Raw residual appendix

These tables are included to show the scale of zero-downsampling intercept bias before calibration. They should not be used as the primary structural calibration evidence.

### Raw residuals by AADT decile

| Decile | N | Mean AADT | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2,183,050 | 227 | 1,803 | -30,799 | -0.9447 | -34,091 | -0.9498 | -0.0051 |
| 1 | 2,163,967 | 344 | 4,972 | -40,106 | -0.8897 | -43,694 | -0.8978 | -0.0081 |
| 2 | 2,174,124 | 424 | 6,598 | -44,423 | -0.8707 | -47,889 | -0.8789 | -0.0082 |
| 3 | 2,154,994 | 499 | 8,161 | -48,815 | -0.8568 | -52,159 | -0.8647 | -0.0079 |
| 4 | 2,167,000 | 593 | 10,827 | -56,874 | -0.8401 | -60,186 | -0.8475 | -0.0075 |
| 5 | 2,163,503 | 750 | 16,636 | -70,797 | -0.8097 | -73,953 | -0.8164 | -0.0066 |
| 6 | 2,170,525 | 1,048 | 27,354 | -94,581 | -0.7757 | -96,267 | -0.7787 | -0.0031 |
| 7 | 2,165,429 | 1,564 | 46,730 | -130,086 | -0.7357 | -128,394 | -0.7332 | +0.0026 |
| 8 | 2,165,585 | 2,695 | 83,766 | -208,894 | -0.7138 | -203,160 | -0.7081 | +0.0057 |
| 9 | 2,167,393 | 11,808 | 244,145 | -655,545 | -0.7286 | -648,272 | -0.7264 | +0.0022 |

### Raw residuals by road family

| Family | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
| motorway | 40,840 | 16,981 | -15,111 | -0.4709 | -15,403 | -0.4756 | -0.0048 |
| other | 3,301,370 | 30,205 | -124,721 | -0.8050 | -134,498 | -0.8166 | -0.0116 |
| other_rural | 4,769,600 | 56,742 | -285,008 | -0.8340 | -292,395 | -0.8375 | -0.0035 |
| other_urban | 13,403,650 | 328,333 | -915,910 | -0.7361 | -905,109 | -0.7338 | +0.0023 |
| trunk_a | 160,110 | 18,731 | -40,170 | -0.6820 | -40,661 | -0.6846 | -0.0026 |

---

## 10. Interpretation and recommendation

Model B improves the downsampled training-frame pseudo-R², and its coefficients make the exposure assumptions more explicit. However, the production question is whether it improves full-population calibration after removing the known intercept bias.

Calibrated comparison summary:

- Model B improves 0/10 AADT deciles.
- Model B improves 2/5 road-family groups.
- On the calibrated common-basis top-1% band, Model B relative-residual improvement is -0.0411.

**Recommendation:** Model B should remain a diagnostic formulation rather than replacing Model A, because calibrated full-frame improvements are mixed rather than consistently positive.

If motorway residuals remain large after intercept calibration, the issue is not solved by global exposure treatment alone. The next modelling step should be family-specific calibration or per-family GLM diagnostics, not more global exposure tweaking.

_Machine-readable: `docs/internal/exposure_offset_full_frame_diagnostics.json`_
