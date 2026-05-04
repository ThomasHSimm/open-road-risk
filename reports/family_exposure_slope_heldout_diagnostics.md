---
title: "Stage 2 GLM: Family exposure slope held-out diagnostics"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** Held-out diagnostic only. No production models changed. No retraining.
**Split:** 80/20 by link_id (seed 42). Train: 1,734,045 links (17,340,450 link-years). Held-out: 433,512 links (4,335,120 link-years).
**Note:** Intercept calibration factors (global and per-family) are estimated on training links only and applied to held-out links. No information leakage.

---

## 1. Why this diagnostic

Within-family AADT decile diagnostics showed that per-family intercept calibration alone
is insufficient: all families retain structured residual patterns across their own AADT
deciles. This diagnostic tests whether family-specific exposure slopes (AADT × family,
length × family interactions) close that gap on held-out data.

---

## 2. Model summary

| Model | Train pseudo-R² | Held-out deviance | Notes |
|---|---:|---:|---|
| A raw | 0.3116 | 853995.9 | Global Model A, no calibration |
| A gcal | 0.3116 | 554264.4 | Model A + global intercept cal (train links) |
| A fcal | 0.3116 | 549579.0 | Model A + per-family intercept cal (train links) |
| M4 raw | 0.3183 | 847319.4 | Pooled interaction GLM, no calibration |
| M4 gcal | 0.3183 | 550232.8 | M4 + global intercept cal (train links) |
| M4 fcal | 0.3183 | 548042.5 | M4 + per-family intercept cal (train links) — primary M4 comparison |
| M5 raw | 0.2024 | 843161.2 | Per-family GLMs, no calibration. Motorway train n=32,730. |

---

## 3. Intercept calibration factors (estimated on training links)

Global factor: 0.2462 (log -1.4017).

| Family | Train obs | Train pred A raw | Cal factor | Log factor |
|---|---:|---:|---:|---:|
| motorway | 13,502 | 25,475.89 | 0.5300 | -0.6349 |
| trunk_a | 14,987 | 47,303.75 | 0.3168 | -1.1494 |
| other_urban | 262,573 | 995,109.69 | 0.2639 | -1.3323 |
| other_rural | 45,238 | 272,991.06 | 0.1657 | -1.7975 |
| other | 24,301 | 123,879.64 | 0.1962 | -1.6288 |

---

## 4. Held-out residuals by family

| Family | N | Obs | rel A raw | rel A gcal | rel A fcal | rel M4 raw | rel M5 raw |
|---|---:|---:|---:|---:|---:|---:|---:|
| motorway | 8,110 | 3,479 | -0.4374 | +1.2852 | +0.0615 | -0.4552 | -0.4174 |
| other | 661,970 | 5,904 | -0.8084 | -0.2217 | -0.0232 | -0.7956 | -0.7638 |
| other_rural | 953,620 | 11,504 | -0.8322 | -0.3183 | +0.0128 | -0.7691 | -0.7615 |
| other_urban | 2,679,880 | 65,760 | -0.7366 | +0.0698 | -0.0019 | -0.7549 | -0.7590 |
| trunk_a | 31,540 | 3,744 | -0.6788 | +0.3048 | +0.0139 | -0.6825 | -0.6797 |

---

## 5. Held-out residuals by top-risk band (common Model A raw ranking)

Bands fixed by raw Model A held-out link-level predicted rate.
All models evaluated on the same link groups.

| Band | Links | Obs | rel A raw | rel A gcal | rel A fcal | rel M4 raw | rel M5 raw |
|---|---:|---:|---:|---:|---:|---:|---:|
| bottom_80pct | 346,809 | 22,213 | -0.8185 | -0.2626 | -0.2231 | -0.8148 | -0.8085 |
| 5_to_20pct | 65,027 | 31,506 | -0.7295 | +0.0988 | +0.1115 | -0.7280 | -0.7342 |
| 1_to_5pct | 17,340 | 22,574 | -0.7322 | +0.0879 | +0.0730 | -0.7377 | -0.7345 |
| top_1pct | 4,336 | 14,098 | -0.6778 | +0.3087 | +0.1479 | -0.6746 | -0.6811 |

---

## 6. Held-out within-family AADT decile residuals

AADT deciles are within each family (decile 0 = lowest 10 % of AADT within that family).
This is the primary test of whether interaction slopes fix the residual bias seen in the
family intercept calibration diagnostics.

### motorway

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | rel A raw | rel A gcal | rel A fcal | rel M4 raw | rel M5 raw |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 811 | 3,449 | 5,549 | 7,280 | 59 | -0.0622 | +2.8094 | +0.7695 | -0.6898 | +0.1126 |
| 1 | 811 | 7,928 | 9,255 | 10,632 | 71 | -0.3571 | +1.6116 | +0.2131 | -0.7180 | -0.3039 |
| 2 | 811 | 11,378 | 13,119 | 14,965 | 89 | -0.4352 | +1.2943 | +0.0657 | -0.6790 | -0.3589 |
| 3 | 811 | 15,895 | 18,397 | 21,076 | 127 | -0.4323 | +1.3061 | +0.0712 | -0.5886 | -0.3295 |
| 4 | 811 | 22,526 | 24,963 | 27,507 | 95 | -0.7033 | +0.2050 | -0.4402 | -0.7578 | -0.6552 |
| 5 | 811 | 28,982 | 31,937 | 35,074 | 163 | -0.6753 | +0.3187 | -0.3874 | -0.7233 | -0.6503 |
| 6 | 811 | 36,654 | 39,805 | 43,025 | 316 | -0.5500 | +0.8280 | -0.1509 | -0.6048 | -0.5444 |
| 7 | 811 | 44,696 | 48,178 | 51,917 | 470 | -0.4949 | +1.0519 | -0.0469 | -0.5051 | -0.4907 |
| 8 | 811 | 54,097 | 59,171 | 64,462 | 792 | -0.3566 | +1.6134 | +0.2140 | -0.2893 | -0.3418 |
| 9 | 811 | 67,967 | 80,064 | 97,708 | 1,297 | -0.3327 | +1.7107 | +0.2592 | -0.1428 | -0.3267 |

---

### trunk_a

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | rel A raw | rel A gcal | rel A fcal | rel M4 raw | rel M5 raw |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 3,158 | 3,256 | 4,020 | 4,650 | 36 | -0.9178 | -0.6663 | -0.7407 | -0.9244 | -0.9105 |
| 1 | 3,153 | 4,895 | 5,367 | 5,817 | 61 | -0.8893 | -0.5503 | -0.6506 | -0.8971 | -0.8791 |
| 2 | 3,151 | 6,027 | 6,504 | 7,007 | 142 | -0.7894 | -0.1446 | -0.3353 | -0.8017 | -0.7729 |
| 3 | 3,154 | 7,279 | 7,868 | 8,472 | 192 | -0.7550 | -0.0047 | -0.2266 | -0.7677 | -0.7404 |
| 4 | 3,154 | 8,786 | 9,447 | 10,128 | 321 | -0.6399 | +0.4627 | +0.1366 | -0.6546 | -0.6332 |
| 5 | 3,155 | 10,489 | 11,273 | 12,061 | 355 | -0.6428 | +0.4511 | +0.1276 | -0.6545 | -0.6483 |
| 6 | 3,153 | 12,469 | 13,365 | 14,293 | 443 | -0.6149 | +0.5644 | +0.2156 | -0.6235 | -0.6304 |
| 7 | 3,154 | 14,776 | 15,863 | 16,974 | 459 | -0.6729 | +0.3288 | +0.0325 | -0.6757 | -0.6866 |
| 8 | 3,155 | 17,611 | 19,211 | 20,988 | 665 | -0.6447 | +0.4433 | +0.1215 | -0.6410 | -0.6535 |
| 9 | 3,153 | 22,104 | 26,639 | 33,330 | 1,070 | -0.6308 | +0.4998 | +0.1654 | -0.6150 | -0.6372 |

---

### other_urban

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | rel A raw | rel A gcal | rel A fcal | rel M4 raw | rel M5 raw |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 269,373 | 268 | 333 | 384 | 817 | -0.8425 | -0.3601 | -0.4029 | -0.8585 | -0.8666 |
| 1 | 267,426 | 401 | 431 | 460 | 952 | -0.8391 | -0.3466 | -0.3904 | -0.8555 | -0.8637 |
| 2 | 267,827 | 474 | 503 | 532 | 1,048 | -0.8405 | -0.3521 | -0.3956 | -0.8565 | -0.8649 |
| 3 | 268,068 | 549 | 587 | 629 | 1,253 | -0.8343 | -0.3271 | -0.3721 | -0.8505 | -0.8597 |
| 4 | 267,923 | 655 | 726 | 806 | 1,883 | -0.8024 | -0.1975 | -0.2513 | -0.8206 | -0.8325 |
| 5 | 267,538 | 854 | 973 | 1,102 | 3,102 | -0.7648 | -0.0445 | -0.1085 | -0.7844 | -0.8000 |
| 6 | 268,019 | 1,176 | 1,343 | 1,520 | 5,257 | -0.7151 | +0.1574 | +0.0798 | -0.7366 | -0.7567 |
| 7 | 267,935 | 1,621 | 1,871 | 2,152 | 7,540 | -0.6978 | +0.2274 | +0.1451 | -0.7194 | -0.7403 |
| 8 | 267,787 | 2,343 | 3,124 | 4,375 | 12,468 | -0.6887 | +0.2644 | +0.1797 | -0.7099 | -0.7242 |
| 9 | 267,984 | 7,929 | 13,228 | 19,440 | 31,440 | -0.7342 | +0.0798 | +0.0074 | -0.7495 | -0.7391 |

---

### other_rural

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | rel A raw | rel A gcal | rel A fcal | rel M4 raw | rel M5 raw |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 95,794 | 170 | 230 | 277 | 70 | -0.9492 | -0.7937 | -0.6936 | -0.9312 | -0.8974 |
| 1 | 95,876 | 293 | 321 | 348 | 132 | -0.9276 | -0.7058 | -0.5630 | -0.8998 | -0.8537 |
| 2 | 95,046 | 361 | 386 | 411 | 174 | -0.9166 | -0.6614 | -0.4969 | -0.8840 | -0.8332 |
| 3 | 95,386 | 424 | 450 | 477 | 193 | -0.9186 | -0.6695 | -0.5090 | -0.8860 | -0.8386 |
| 4 | 94,961 | 492 | 528 | 566 | 320 | -0.8866 | -0.5395 | -0.3159 | -0.8428 | -0.7813 |
| 5 | 95,591 | 589 | 644 | 703 | 472 | -0.8670 | -0.4597 | -0.1973 | -0.8173 | -0.7525 |
| 6 | 95,049 | 739 | 828 | 927 | 721 | -0.8429 | -0.3617 | -0.0518 | -0.7844 | -0.7183 |
| 7 | 95,206 | 988 | 1,158 | 1,354 | 1,046 | -0.8353 | -0.3311 | -0.0063 | -0.7708 | -0.7120 |
| 8 | 95,349 | 1,494 | 1,999 | 2,686 | 1,692 | -0.8387 | -0.3450 | -0.0269 | -0.7707 | -0.7466 |
| 9 | 95,362 | 3,590 | 7,427 | 12,540 | 6,684 | -0.7980 | -0.1793 | +0.2193 | -0.7258 | -0.7627 |

---

### other

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | rel A raw | rel A gcal | rel A fcal | rel M4 raw | rel M5 raw |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 66,270 | 109 | 146 | 175 | 13 | -0.9817 | -0.9257 | -0.9068 | -0.9784 | -0.9533 |
| 1 | 66,694 | 184 | 201 | 217 | 26 | -0.9713 | -0.8836 | -0.8539 | -0.9647 | -0.9273 |
| 2 | 66,214 | 224 | 237 | 251 | 26 | -0.9744 | -0.8962 | -0.8697 | -0.9685 | -0.9366 |
| 3 | 66,476 | 258 | 274 | 290 | 58 | -0.9531 | -0.8095 | -0.7610 | -0.9442 | -0.8897 |
| 4 | 65,765 | 299 | 319 | 339 | 93 | -0.9368 | -0.7434 | -0.6780 | -0.9274 | -0.8612 |
| 5 | 66,007 | 350 | 375 | 401 | 172 | -0.9009 | -0.5977 | -0.4951 | -0.8879 | -0.7967 |
| 6 | 66,307 | 416 | 452 | 490 | 280 | -0.8719 | -0.4797 | -0.3470 | -0.8589 | -0.7596 |
| 7 | 66,200 | 513 | 566 | 624 | 510 | -0.8139 | -0.2440 | -0.0513 | -0.7982 | -0.6860 |
| 8 | 65,844 | 658 | 782 | 965 | 889 | -0.7681 | -0.0579 | +0.1823 | -0.7559 | -0.6788 |
| 9 | 66,193 | 1,390 | 3,869 | 7,028 | 3,837 | -0.7437 | +0.0411 | +0.3065 | -0.7392 | -0.7653 |

---

## 7. Verdict

**M4+fcal does not materially improve held-out within-family AADT calibration vs A+fcal (max range: M4+fcal=1.171 vs A+fcal=1.213). Prefer A + per-family intercept calibration for simplicity.**

### Decision rules applied
- M4 improves held-out within-family AADT calibration (max range < 85 % of family-cal
  range) AND does not worsen top-1% band → **Recommend M4 as candidate v3 GLM**.
- M4 improves within-family calibration but worsens top-1% → further investigation needed.
- M4 no better than family-cal → prefer intercept-only for simplicity.
- M5 improves train/full-frame but not held-out → **Reject (overfit)**. Motorway n is
  small enough (~32,730 train link-years) that
  per-family GLM risks learning noise rather than signal.

_Machine-readable: `docs/internal/family_exposure_slope_heldout_diagnostics.json`_
