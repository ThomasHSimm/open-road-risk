---
title: "Stage 2 GLM: Within-family AADT decile calibration"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** Diagnostic only. No production models changed. No retraining.
**Model:** Model A (full offset). All three prediction variants compared.
**Frame:** Full ~21M-row scored population.

Comparisons: **raw** · **global-cal** (single intercept correction) · **family-cal** (per-family intercept correction).

---

## Background

After per-family intercept calibration, the family-level totals match observations by
construction. This diagnostic tests whether residual bias *within each family* varies
systematically across the AADT distribution.

If family-cal residuals are roughly flat across within-family AADT deciles → intercept
calibration is probably enough for that family.

If family-cal residuals still show a systematic AADT slope within a family → that family
needs per-family exposure slopes or AADT interactions, not just an intercept shift.

AADT deciles are computed separately within each family (decile 0 = lowest 10% of AADT
within that family, not across the full population).

`family_vs_global` > 0 means family-cal is better calibrated than global-cal at that decile.

---


## 1. motorway

Family total (family-cal): obs=16,981, pred=16,981.00, rel_resid=+0.0000 (≈ 0 by construction).

**Interpretation:** Strong within-motorway AADT slope remains after family-cal (range 0.848, negative slope: low-AADT rel=+0.5519, high-AADT rel=+0.0916). Per-family intercept calibration is not sufficient for this family. Per-family GLMs with separate exposure slopes are recommended.

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 4,084 | 3,381 | 5,260 | 6,820 | 245 | -0.1788 | +2.3356 | +0.5519 | +1.7837 |
| 1 | 4,084 | 7,480 | 8,804 | 10,205 | 351 | -0.3453 | +1.6592 | +0.2372 | +1.4220 |
| 2 | 4,085 | 10,911 | 12,660 | 14,514 | 426 | -0.4386 | +1.2802 | +0.0609 | +1.2193 |
| 3 | 4,083 | 15,561 | 18,215 | 21,032 | 576 | -0.4834 | +1.0983 | -0.0238 | +1.0745 |
| 4 | 4,084 | 22,525 | 25,420 | 28,381 | 640 | -0.6274 | +0.5136 | -0.2958 | +0.2179 |
| 5 | 4,084 | 29,892 | 32,844 | 35,861 | 988 | -0.6261 | +0.5186 | -0.2934 | +0.2252 |
| 6 | 4,085 | 37,492 | 40,646 | 43,803 | 1,658 | -0.5405 | +0.8663 | -0.1317 | +0.7346 |
| 7 | 4,083 | 45,491 | 49,204 | 53,052 | 2,443 | -0.4785 | +1.1184 | -0.0144 | +1.1041 |
| 8 | 4,084 | 55,328 | 60,488 | 66,149 | 3,703 | -0.4239 | +1.3402 | +0.0888 | +1.2514 |
| 9 | 4,084 | 69,643 | 81,640 | 97,917 | 5,951 | -0.4224 | +1.3462 | +0.0916 | +1.2546 |
---
## 2. trunk_a

Family total (family-cal): obs=18,731, pred=18,731.00, rel_resid=+0.0000 (≈ 0 by construction).

**Interpretation:** Strong within-trunk_a AADT slope remains after family-cal (range 0.885, positive slope: low-AADT rel=-0.7008, high-AADT rel=+0.1127). Per-family intercept calibration is not sufficient for this family. Per-family GLMs with separate exposure slopes are recommended.

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 16,013 | 3,121 | 3,944 | 4,631 | 199 | -0.9048 | -0.6135 | -0.7008 | -0.0873 |
| 1 | 16,013 | 4,888 | 5,357 | 5,820 | 388 | -0.8598 | -0.4305 | -0.5591 | -0.1286 |
| 2 | 16,012 | 6,059 | 6,552 | 7,058 | 747 | -0.7788 | -0.1013 | -0.3043 | -0.2030 |
| 3 | 16,008 | 7,327 | 7,905 | 8,502 | 974 | -0.7588 | -0.0204 | -0.2417 | -0.2212 |
| 4 | 16,019 | 8,811 | 9,483 | 10,176 | 1,446 | -0.6885 | +0.2655 | -0.0203 | +0.2451 |
| 5 | 16,005 | 10,544 | 11,305 | 12,088 | 1,767 | -0.6648 | +0.3615 | +0.0540 | +0.3075 |
| 6 | 16,011 | 12,499 | 13,400 | 14,327 | 2,210 | -0.6235 | +0.5294 | +0.1840 | +0.3454 |
| 7 | 16,011 | 14,820 | 15,899 | 17,024 | 2,494 | -0.6457 | +0.4390 | +0.1140 | +0.3250 |
| 8 | 16,007 | 17,669 | 19,265 | 21,035 | 3,305 | -0.6370 | +0.4745 | +0.1415 | +0.3330 |
| 9 | 16,011 | 22,161 | 26,802 | 33,382 | 5,201 | -0.6462 | +0.4373 | +0.1127 | +0.3246 |
---
## 3. other_urban

Family total (family-cal): obs=328,333, pred=328,333.00, rel_resid=-0.0000 (≈ 0 by construction).

**Interpretation:** Strong within-other_urban AADT slope remains after family-cal (range 0.614, positive slope: low-AADT rel=-0.3943, high-AADT rel=+0.0084). Per-family intercept calibration is not sufficient for this family. Per-family GLMs with separate exposure slopes are recommended.

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1,352,547 | 269 | 333 | 384 | 4,158 | -0.8402 | -0.3507 | -0.3943 | -0.0435 |
| 1 | 1,342,517 | 401 | 431 | 460 | 4,610 | -0.8444 | -0.3679 | -0.4103 | -0.0424 |
| 2 | 1,340,181 | 473 | 503 | 532 | 5,175 | -0.8422 | -0.3588 | -0.4018 | -0.0430 |
| 3 | 1,332,111 | 549 | 587 | 628 | 6,214 | -0.8341 | -0.3262 | -0.3714 | -0.0452 |
| 4 | 1,335,850 | 654 | 724 | 803 | 9,160 | -0.8063 | -0.2132 | -0.2660 | -0.0528 |
| 5 | 1,341,360 | 851 | 969 | 1,098 | 15,162 | -0.7694 | -0.0632 | -0.1260 | -0.0628 |
| 6 | 1,339,786 | 1,172 | 1,337 | 1,512 | 25,752 | -0.7190 | +0.1414 | +0.0649 | +0.0765 |
| 7 | 1,339,574 | 1,613 | 1,864 | 2,146 | 37,870 | -0.6964 | +0.2333 | +0.1506 | +0.0827 |
| 8 | 1,339,390 | 2,336 | 3,114 | 4,356 | 63,486 | -0.6824 | +0.2901 | +0.2035 | +0.0865 |
| 9 | 1,340,334 | 7,870 | 13,197 | 19,392 | 156,746 | -0.7339 | +0.0809 | +0.0084 | +0.0725 |
---
## 4. other_rural

Family total (family-cal): obs=56,742, pred=56,742.00, rel_resid=-0.0000 (≈ 0 by construction).

**Interpretation:** Strong within-other_rural AADT slope remains after family-cal (range 0.911, positive slope: low-AADT rel=-0.7127, high-AADT rel=+0.1984). Per-family intercept calibration is not sufficient for this family. Per-family GLMs with separate exposure slopes are recommended.

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 482,288 | 169 | 230 | 277 | 331 | -0.9523 | -0.8063 | -0.7127 | +0.0935 |
| 1 | 475,118 | 293 | 321 | 347 | 585 | -0.9351 | -0.7363 | -0.6090 | +0.1273 |
| 2 | 475,896 | 360 | 385 | 410 | 813 | -0.9219 | -0.6826 | -0.5293 | +0.1532 |
| 3 | 477,035 | 423 | 449 | 476 | 987 | -0.9164 | -0.6606 | -0.4967 | +0.1639 |
| 4 | 476,291 | 491 | 527 | 566 | 1,472 | -0.8957 | -0.5765 | -0.3721 | +0.2044 |
| 5 | 475,584 | 589 | 644 | 703 | 2,350 | -0.8669 | -0.4596 | -0.1986 | +0.2609 |
| 6 | 477,504 | 739 | 830 | 929 | 3,740 | -0.8393 | -0.3472 | -0.0321 | +0.3151 |
| 7 | 476,683 | 992 | 1,160 | 1,357 | 5,202 | -0.8370 | -0.3381 | -0.0185 | +0.3195 |
| 8 | 476,244 | 1,498 | 2,000 | 2,677 | 8,607 | -0.8360 | -0.3340 | -0.0125 | +0.3215 |
| 9 | 476,957 | 3,581 | 7,404 | 12,485 | 32,655 | -0.8010 | -0.1918 | +0.1984 | -0.0067 |
---
## 5. other

Family total (family-cal): obs=30,205, pred=30,205.00, rel_resid=-0.0000 (≈ 0 by construction).

**Interpretation:** Strong within-other AADT slope remains after family-cal (range 1.277, positive slope: low-AADT rel=-0.9257, high-AADT rel=+0.3509). Per-family intercept calibration is not sufficient for this family. Per-family GLMs with separate exposure slopes are recommended.

| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 334,138 | 109 | 146 | 175 | 52 | -0.9855 | -0.9411 | -0.9257 | +0.0155 |
| 1 | 334,379 | 184 | 201 | 217 | 132 | -0.9710 | -0.8821 | -0.8512 | +0.0310 |
| 2 | 321,951 | 224 | 237 | 250 | 174 | -0.9647 | -0.8566 | -0.8190 | +0.0377 |
| 3 | 333,159 | 257 | 273 | 289 | 244 | -0.9603 | -0.8388 | -0.7964 | +0.0424 |
| 4 | 327,270 | 298 | 318 | 338 | 470 | -0.9356 | -0.7384 | -0.6697 | +0.0687 |
| 5 | 332,488 | 349 | 375 | 401 | 808 | -0.9075 | -0.6242 | -0.5254 | +0.0987 |
| 6 | 328,666 | 416 | 452 | 490 | 1,421 | -0.8689 | -0.4676 | -0.3277 | +0.1399 |
| 7 | 329,348 | 513 | 566 | 623 | 2,494 | -0.8162 | -0.2533 | -0.0571 | +0.1962 |
| 8 | 329,838 | 657 | 781 | 965 | 4,377 | -0.7722 | -0.0746 | +0.1686 | -0.0940 |
| 9 | 330,133 | 1,385 | 3,913 | 7,128 | 20,033 | -0.7366 | +0.0698 | +0.3509 | -0.2811 |


---

## Overall verdict

Slope patterns persist within motorway, trunk_a, other_urban, other_rural, other after family-cal. **Per-family intercept calibration alone is not sufficient. Per-family GLMs with separate exposure slopes should be tested.**

_Machine-readable: `docs/internal/family_within_aadt_diagnostics.json`_
