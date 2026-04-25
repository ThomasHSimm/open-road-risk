# EB Dispersion Method-of-Moments Estimate

This report estimates a global NB2 dispersion parameter k for EB-style shrinkage using method-of-moments. Link-years are binned by existing Stage 2 XGBoost predicted collision count, and each bin's observed mean and variance imply k_bin = (Var(y) - E(y)) / E(y)^2.

## k_bin Values

| bin | predicted_xgb_range | n_link_years | n_positive | E(y) | Var(y) | k_bin |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.00000070-0.00010749 | 3,251,331 | 153 | 0.00004737 | 0.00004798 | 273.195395 |
| 1 | 0.00010749-0.00016324 | 2,167,557 | 226 | 0.00010657 | 0.00011117 | 405.210734 |
| 2 | 0.00016324-0.00019776 | 1,083,778 | 140 | 0.00013102 | 0.00013470 | 213.999900 |
| 3 | 0.00019776-0.00023863 | 1,083,783 | 208 | 0.00019377 | 0.00019742 | 97.307165 |
| 4 | 0.00023863-0.00028782 | 1,083,778 | 245 | 0.00022791 | 0.00023155 | 70.061039 |
| 5 | 0.00028782-0.00034846 | 1,083,779 | 290 | 0.00027312 | 0.00028596 | 172.178597 |
| 6 | 0.00034847-0.00042527 | 1,083,778 | 365 | 0.00034324 | 0.00035789 | 124.309544 |
| 7 | 0.00042527-0.00052555 | 1,083,779 | 470 | 0.00044382 | 0.00046392 | 102.058168 |
| 8 | 0.00052555-0.00065953 | 1,083,776 | 602 | 0.00057392 | 0.00061788 | 133.463864 |
| 9 | 0.00065953-0.00084427 | 1,083,781 | 738 | 0.00069756 | 0.00073767 | 82.436850 |
| 10 | 0.00084427-0.001108 | 1,083,778 | 972 | 0.00093100 | 0.001002 | 82.034425 |
| 11 | 0.001108-0.001509 | 1,083,778 | 1,281 | 0.001228 | 0.001324 | 63.847839 |
| 12 | 0.001509-0.002154 | 1,083,780 | 1,732 | 0.001674 | 0.001844 | 60.919676 |
| 13 | 0.002154-0.003330 | 1,083,777 | 2,651 | 0.002595 | 0.002937 | 50.808912 |
| 14 | 0.003330-0.005868 | 1,083,779 | 4,350 | 0.004274 | 0.004811 | 29.409102 |
| 15 | 0.005868-0.014413 | 1,083,779 | 9,104 | 0.009000 | 0.010285 | 15.859316 |
| 16 | 0.014413-20.332432 | 1,083,779 | 367,728 | 0.393188 | 0.411518 | 0.118566 |

## k Aggregations

| aggregation | k |
| --- | --- |
| link-year weighted (primary) | 146.440984 |
| positive-event weighted (diagnostic) | 3.074322 |
| median of retained k_bin (diagnostic) | 82.436850 |

Divergence between the primary link-year weighted k and the diagnostic alternatives indicates non-constant dispersion and a potentially fragile global-k assumption.

## Dropped Bins

Dropped bins: 0 of 17 after merging (0.00000000%).

## Bin Merges

Initial 20 quantile bins were merged into 17 retained bins before negative-k filtering.

Merge rule: start with 20 quantile bins by predicted_xgb, walk bins from low to high prediction, and accumulate adjacent bins until the candidate bin has at least 10,000 link-years and 100 positive-collision link-years; any trailing low-count bin is merged into the previous retained bin.

## Interpretation

No bins were dropped for non-physical negative dispersion. The retained k_bin values vary by about 3417.6x across the predicted-risk range. The diagnostic aggregations diverge materially from the primary k. These diagnostics describe the MoM estimate only; they do not decide whether EB shrinkage should be adopted.

Full provenance, bin definitions, and merge actions are in `data/provenance/eb_dispersion_provenance.json`.
