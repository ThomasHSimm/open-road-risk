# Rank Stability Evaluation

This report evaluates Stage 2 XGBoost rank stability across five seeds (42-46), with seed 42 representing the production realisation. The evaluation measures pseudo-R2 variation, top-k ranking overlap, full-rank Spearman correlation, and observed per-decile calibration stability. The expected per-seed row count, taken from production risk_scores.parquet before the run, is 2,167,557 links.

## Pseudo-R2

| seed | pseudo_R2 |
| --- | --- |
| 42 | 0.321444 |
| 43 | 0.321372 |
| 44 | 0.326320 |
| 45 | 0.326529 |
| 46 | 0.321825 |
| mean | 0.323498 |
| std | 0.002678 |

## Top-k Jaccard

| k | pairwise_mean | pairwise_min |
| --- | --- | --- |
| 100 | 0.878141 | 0.851852 |
| 1000 | 0.870936 | 0.858736 |
| 10000 | 0.883074 | 0.873185 |
| 21675 | 0.903575 | 0.896574 |

## Spearman Correlation

| metric | value |
| --- | --- |
| pairwise_mean | 0.999140 |
| pairwise_min | 0.999069 |

## Calibration

| decile | seed_42 | seed_43 | seed_44 | seed_45 | seed_46 | std |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.000121 | 0.000125 | 0.000126 | 0.000127 | 0.000131 | 0.000004 |
| 2 | 0.000452 | 0.000446 | 0.000452 | 0.000451 | 0.000443 | 0.000004 |
| 3 | 0.000946 | 0.000933 | 0.000934 | 0.000935 | 0.000949 | 0.000007 |
| 4 | 0.001718 | 0.001702 | 0.001705 | 0.001706 | 0.001699 | 0.000007 |
| 5 | 0.002866 | 0.002855 | 0.002885 | 0.002894 | 0.002865 | 0.000016 |
| 6 | 0.004985 | 0.004997 | 0.004946 | 0.004956 | 0.004958 | 0.000022 |
| 7 | 0.008841 | 0.008817 | 0.008860 | 0.008816 | 0.008868 | 0.000024 |
| 8 | 0.017073 | 0.017122 | 0.017079 | 0.017069 | 0.017056 | 0.000025 |
| 9 | 0.036558 | 0.036609 | 0.036613 | 0.036564 | 0.036506 | 0.000044 |
| 10 | 0.134505 | 0.134458 | 0.134465 | 0.134547 | 0.134590 | 0.000056 |

Decile std small relative to decile mean indicates the calibrated prediction is stable across seeds; large std in any decile would indicate the calibration itself is seed-dependent in that risk band.

## Interpretation

Seed 42 pseudo-R2 is within one cross-seed standard deviation of the mean. Its mean top-1% Jaccard against the other seeds is 0.902825, compared with the all-pair mean of 0.903575; its mean Spearman rho against the other seeds is 0.999130, compared with the all-pair mean of 0.999140. On these measures, seed 42 appears representative of the five-seed set.

Full run metadata and pairwise values are in `data/provenance/rank_stability_provenance.json`.

### Flags

- Top-1% Jaccard mean is 0.903575, below the >0.93 prior.
