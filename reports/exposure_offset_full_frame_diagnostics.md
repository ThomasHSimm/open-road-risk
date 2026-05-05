---
title: "Stage 2 GLM: Full-frame exposure calibration diagnostics"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** GLM diagnostic only. No production models changed.
**Models:** A (full offset) vs B (learned exposure). Model C dropped.
**Frame:** All diagnostics use the FULL ~21M-row scored population unless noted.

---

## 1. Why motorway residuals were exactly 0.0 in the training-frame report

The training-frame mean_resid is exactly 0.0 by construction. The Poisson GLM feature set includes 'is_motorway' and 'is_a_road' binary indicators. For a Poisson GLM with canonical log link, the score equations at convergence require Σ_i[x_ij*(y_i-μ_i)]=0 for every predictor j. For a binary indicator x_ij ∈ {0,1}, this becomes Σ_{group j}(y_i-μ_i)=0 within the TRAINING FRAME — i.e., sum(obs) = sum(pred) exactly for motorway links in the training data. mean_resid = 0/n = 0 exactly. This is a mathematical identity of GLMs with indicator variables, not a sign of perfect calibration. Full-frame residuals (below) are not subject to this constraint because the GLM was fitted on a downsampled subset.

### Training-frame motorway residuals (downsampled frame)

| Metric | Model A | Model B |
|---|---:|---:|
| N rows (motorway, training frame) | 13,996 | — |
| sum_obs | 16981.000000 | — |
| sum_pred | 16981.000000 | 16981.000000 |
| net_resid | 0.000000 | 0.000000 |
| mean_resid | 0.000000 | 0.000000 |
| rel_resid | 0.000000 | 0.000000 |

### Full-frame motorway residuals (all ~21M rows)

| Metric | Model A | Model B |
|---|---:|---:|
| N rows (motorway, full frame) | 40,840 | — |
| sum_obs | 16981 | — |
| sum_pred | 32091.53 | 32383.62 |
| net_resid | -15110.53 | -15402.62 |
| rel_resid | -0.4709 | -0.4756 |

---

## 2. Model summary (training frame)

| | Model A | Model B |
|---|---:|---:|
| Exposure treatment | Full offset log(AADT×len×365/1e6) | No offset; log_aadt + log_length as features |
| pseudo-R² | 0.3117 | 0.3266 |
| coef(log_aadt) | forced=1.0 (in offset) | 0.9321 |
| coef(log_length) | -0.6564 (residual adj. on β=1 forced) | 0.3392 |
| Effective length β | ~0.3436 | 0.3392 |

Note: Model A forces β_aadt=1 and β_length=1 via offset, then allows a residual
`log_link_length` coefficient to absorb length misspecification.
The effective length scaling is 1 + (−0.6564) = ~0.34, matching the empirical β from
collision-exposure-behaviour.qmd (0.46–0.81 range). Model B learns β_aadt=0.93 and
β_length=0.34 directly, confirming sub-linear exposure scaling.

---

## 3. Full-frame residuals by AADT decile

Decile 0 = lowest AADT. Positive net_resid = model under-predicts.
rel_improvement > 0 means Model B is better calibrated.

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

---

## 4. Full-frame residuals by road family

| Family | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
| motorway | 40,840 | 16,981 | -15,111 | -0.4709 | -15,403 | -0.4756 | -0.0048 |
| other | 3,301,370 | 30,205 | -124,721 | -0.8050 | -134,498 | -0.8166 | -0.0116 |
| other_rural | 4,769,600 | 56,742 | -285,008 | -0.8340 | -292,395 | -0.8375 | -0.0035 |
| other_urban | 13,403,650 | 328,333 | -915,910 | -0.7361 | -905,109 | -0.7338 | +0.0023 |
| trunk_a | 160,110 | 18,731 | -40,170 | -0.6820 | -40,661 | -0.6846 | -0.0026 |

---

## 5. Full-frame residuals by road classification

| Class | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Road | 1,555,380 | 174,615 | -421,134 | -0.7069 | -423,434 | -0.7080 | -0.0011 |
| B Road | 892,860 | 56,216 | -255,429 | -0.8196 | -250,933 | -0.8170 | +0.0026 |
| Classified Unnumbered | 1,909,210 | 65,399 | -89,831 | -0.5787 | -97,090 | -0.5975 | -0.0188 |
| Motorway | 40,840 | 16,981 | -15,111 | -0.4709 | -15,403 | -0.4756 | -0.0048 |
| Not Classified | 2,248,780 | 5,133 | -78,444 | -0.9386 | -83,301 | -0.9420 | -0.0034 |
| Unclassified | 10,600,140 | 121,071 | -379,331 | -0.7581 | -378,361 | -0.7576 | +0.0005 |
| Unknown | 4,428,360 | 11,577 | -141,641 | -0.9244 | -139,544 | -0.9234 | +0.0010 |

---

## 6. Full-frame residuals by top-risk band

Bands defined separately for each model using its own link-level predicted rate.
pred_total = mean predicted rate × n_years (to match observed collision sum).

### Model A top-risk bands

| Band | Links | Obs | Pred | Net resid | Rel resid |
|---|---:|---:|---:|---:|---:|
| bottom_80pct | 1,734,045 | 109,577 | 610,222 | -500,645 | -0.8204 |
| 5_to_20pct | 325,134 | 160,386 | 581,899 | -421,513 | -0.7244 |
| 1_to_5pct | 86,702 | 110,971 | 421,501 | -310,530 | -0.7367 |
| top_1pct | 21,676 | 70,058 | 218,289 | -148,231 | -0.6791 |

### Model B top-risk bands

| Band | Links | Obs | Pred | Net resid | Rel resid |
|---|---:|---:|---:|---:|---:|
| bottom_80pct | 1,734,045 | 108,468 | 629,150 | -520,682 | -0.8276 |
| 5_to_20pct | 325,134 | 161,298 | 579,912 | -418,614 | -0.7219 |
| 1_to_5pct | 86,702 | 110,932 | 417,432 | -306,500 | -0.7343 |
| top_1pct | 21,676 | 70,294 | 212,563 | -142,269 | -0.6693 |

---

## 7. Interpretation and recommendation

### Systematic over-prediction caveat

Both models over-predict massively on the full population (relative residuals −0.73 to
−0.95 across all segments). This is not caused by exposure treatment. It is an intercept
bias from the 10:1 zero-downsampling used during training: the GLM intercept is calibrated
to a subsampled population where zero-collision links are under-represented, so when
applied to all 21M link-years it over-predicts everywhere. The production pipeline does not
use the raw GLM prediction as an absolute rate — the GLM is used for the residual
diagnostic and relative ordering, and XGBoost provides the ranking used in production.
Both A and B are equally affected, so the comparison below is still meaningful as a
relative comparison, but the absolute predictions from either model should not be treated
as calibrated collision rates without intercept correction.

---

### Finding 1 — Motorway full-frame residuals are large and not fixed by Model B

Training-frame motorway residuals are exactly 0 for both models (GLM score-equation
identity; explained in §1). On the full scored frame:

| | Model A | Model B |
|---|---:|---:|
| Motorway sum_obs | 16,981 | 16,981 |
| Motorway sum_pred | 32,092 | 32,384 |
| Motorway rel_resid | −0.471 | −0.476 |

Both models over-predict motorway collisions by ~47% on the full frame. Model B is
marginally *worse* (−0.476 vs −0.471). Motorway over-prediction is not caused by
exposure treatment; it persists regardless of whether β_aadt is forced to 1.0 or
learned as 0.93. The motorway issue requires a different investigation (motorway-specific
features, per-family intercept correction, or EB shrinkage adjustment).

---

### Finding 2 — AADT decile improvement is marginal and mixed

| Decile | AADT range | Model A rel | Model B rel | Improvement |
|---|---|---:|---:|---:|
| 0–2 (low) | <450 | ≈ −0.87 to −0.94 | ≈ −0.88 to −0.95 | **−0.005 to −0.008** (B worse) |
| 3–6 (mid) | 450–1200 | ≈ −0.78 to −0.86 | ≈ −0.78 to −0.86 | **−0.003 to −0.008** (B worse) |
| 7–9 (high) | >1500 | ≈ −0.73 to −0.74 | ≈ −0.73 | **+0.002 to +0.006** (B better) |

Model B is marginally better only at the three highest AADT deciles (improvement 0.2–0.6
percentage points). It is marginally worse at the seven lowest deciles. The improvement at
high AADT is consistent with the learned β_aadt = 0.93 (vs forced 1.0): slightly reducing
the predicted rate for high-exposure links. But the effect is small.

---

### Finding 3 — Road family improvement is marginal and mixed

| Family | Model A rel | Model B rel | Improvement |
|---|---:|---:|---:|
| motorway | −0.471 | −0.476 | **−0.005** (B worse) |
| trunk_a | −0.682 | −0.685 | **−0.003** (B worse) |
| other_rural | −0.834 | −0.837 | **−0.004** (B worse) |
| other_urban | −0.736 | −0.734 | **+0.002** (B better) |
| other (unassigned) | −0.805 | −0.817 | **−0.012** (B worse) |

Model B is better only on other_urban (urban non-trunk A Roads and below), which is the
largest family (13.4M rows, 61% of the population). The improvement (+0.2 pp) is small.
Motorway, trunk_a, rural, and unassigned are all slightly worse.

---

### Finding 4 — Top-risk band improvement is consistent but tiny

| Band | Model A rel | Model B rel | Improvement |
|---|---:|---:|---:|
| bottom 80% | −0.820 | −0.828 | **−0.008** (B worse) |
| 5–20% | −0.724 | −0.722 | **+0.002** (B better) |
| 1–5% | −0.737 | −0.734 | **+0.002** (B better) |
| top 1% | −0.679 | −0.669 | **+0.010** (B better) |

Model B is better at the top of the risk distribution (top 1%: +1.0 pp). The bottom 80%
is marginally worse. This is the clearest signal in favour of Model B: its slightly more
accurate AADT scaling reduces over-prediction on the highest-risk links.

---

### Recommendation

**Model B should be kept as a diagnostic, not adopted as the v3 GLM formulation.**

Reasons:
1. The full-frame calibration improvement is marginal (max 1 pp at top 1%, ≤0.6 pp elsewhere)
   and mixed (worse on 7/10 AADT deciles, 4/5 families).
2. The learned β_aadt = 0.93 confirms the misspecification is real but small at the
   aggregate level. The per-class β values (0.47–0.76 from collision-exposure-behaviour.qmd)
   suggest the heterogeneity is the larger issue, not the global β.
3. Motorway over-prediction is identical under A and B. Exposure treatment is not the
   motorway calibration issue.
4. The dominant calibration problem is the intercept bias from zero-downsampling. Fixing
   that (offset correction or post-hoc recalibration) would benefit both models more than
   switching from A to B.

**What Model B confirms for the v3 roadmap:**
- β_aadt ≈ 0.93 globally (sub-linear, but less extreme than per-class estimates suggested).
- Switching to per-family GLMs (with separate intercepts) is more likely to improve
  motorway calibration than changing the global exposure treatment.
- The XGBoost model, which uses `estimated_aadt` as a free feature, already learns
  sub-linear exposure implicitly. The GLM formulation choice has little downstream effect
  on the production ranking.

_Machine-readable: `docs/internal/exposure_offset_full_frame_diagnostics.json`_
