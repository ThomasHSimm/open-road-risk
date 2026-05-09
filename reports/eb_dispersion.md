# EB Dispersion Method-of-Moments Estimate

This report estimates a global NB2 dispersion parameter k for EB-style shrinkage using method-of-moments. Link-years are binned by existing Stage 2 XGBoost predicted collision count, and each bin's observed mean and variance imply k_bin = (Var(y) - E(y)) / E(y)^2.

## k_bin Values

| bin | predicted_xgb_range | n_link_years | n_positive | E(y) | Var(y) | k_bin |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.00033272-0.00053720 | 1,083,779 | 366 | 0.00034140 | 0.00034866 | 62.335353 |
| 2 | 0.00053720-0.00078450 | 1,083,777 | 583 | 0.00054070 | 0.00054595 | 17.938059 |
| 3 | 0.00078450-0.001090 | 1,083,780 | 851 | 0.00079075 | 0.00080673 | 25.562654 |
| 4 | 0.001090-0.001466 | 1,083,777 | 1,109 | 0.001049 | 0.001129 | 72.774665 |
| 5 | 0.001466-0.001930 | 1,083,780 | 1,585 | 0.001476 | 0.001502 | 11.701183 |
| 6 | 0.001930-0.002504 | 1,083,776 | 2,091 | 0.001956 | 0.002010 | 13.951115 |
| 7 | 0.002504-0.003219 | 1,083,779 | 2,606 | 0.002437 | 0.002495 | 9.877208 |
| 8 | 0.003219-0.004118 | 1,083,779 | 3,512 | 0.003295 | 0.003406 | 10.218794 |
| 9 | 0.004118-0.005291 | 1,083,776 | 4,517 | 0.004249 | 0.004403 | 8.506124 |
| 10 | 0.005291-0.006864 | 1,083,781 | 5,948 | 0.005604 | 0.005812 | 6.640434 |
| 11 | 0.006864-0.009018 | 1,083,779 | 7,959 | 0.007522 | 0.007847 | 5.751822 |
| 12 | 0.009018-0.012058 | 1,083,779 | 10,750 | 0.010211 | 0.010725 | 4.928744 |
| 13 | 0.012058-0.016499 | 1,083,777 | 14,839 | 0.014196 | 0.015133 | 4.650221 |
| 14 | 0.016499-0.023348 | 1,083,780 | 20,472 | 0.019661 | 0.020954 | 3.344423 |
| 15 | 0.023348-0.034644 | 1,083,778 | 29,773 | 0.028980 | 0.031538 | 3.045268 |
| 16 | 0.034644-0.054709 | 1,083,779 | 44,364 | 0.043815 | 0.048332 | 2.352888 |
| 17 | 0.054709-0.097510 | 1,083,778 | 71,362 | 0.072283 | 0.081919 | 1.844292 |
| 18 | 0.097510-17.882029 | 1,083,779 | 168,303 | 0.197478 | 0.304868 | 2.753793 |

## k Aggregations

| aggregation | k |
| --- | --- |
| link-year weighted (primary) | 14.898721 |
| positive-event weighted (diagnostic) | 3.451158 |
| median of retained k_bin (diagnostic) | 7.573279 |

Divergence between the primary link-year weighted k and the diagnostic alternatives indicates non-constant dispersion and a potentially fragile global-k assumption.

## Dropped Bins

Dropped bins: 1 of 19 after merging (5.263158%).

## Bin Merges

Initial 20 quantile bins were merged into 19 retained bins before negative-k filtering.

Merge rule: start with 20 quantile bins by predicted_xgb, walk bins from low to high prediction, and accumulate adjacent bins until the candidate bin has at least 10,000 link-years and 100 positive-collision link-years; any trailing low-count bin is merged into the previous retained bin.

## Interpretation

1 bins were dropped for non-physical negative dispersion. The retained k_bin values vary by about 39.5x across the predicted-risk range. The diagnostic aggregations diverge materially from the primary k. These diagnostics describe the MoM estimate only; they do not decide whether EB shrinkage should be adopted.

Full provenance, bin definitions, and merge actions are in `data/provenance/eb_dispersion_provenance.json`.
