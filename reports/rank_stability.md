# Rank Stability Evaluation

This report evaluates Stage 2 XGBoost rank stability across five seeds (42-46), with seed 42 representing the production realisation. The evaluation measures pseudo-R2 variation, top-k ranking overlap, full-rank Spearman correlation, and observed per-decile calibration stability. The expected per-seed row count, taken from production risk_scores.parquet before the run, is 3,941,299 links.

## Pseudo-R2

| seed | pseudo_R2 |
| --- | --- |
| 42 | 0.361633 |
| 43 | 0.359392 |
| 44 | 0.362738 |
| 45 | 0.359891 |
| 46 | 0.360815 |
| mean | 0.360894 |
| std | 0.001343 |

## Top-k Jaccard

| k | pairwise_mean | pairwise_min |
| --- | --- | --- |
| 100 | 0.847385 | 0.785714 |
| 1000 | 0.893263 | 0.883239 |
| 10000 | 0.910606 | 0.908033 |
| 39412 | 0.931497 | 0.927049 |

## Spearman Correlation

| metric | value |
| --- | --- |
| pairwise_mean | 0.999423 |
| pairwise_min | 0.999364 |

## Calibration

| decile | seed_42 | seed_43 | seed_44 | seed_45 | seed_46 | std |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.000250 | 0.000252 | 0.000250 | 0.000254 | 0.000252 | 0.000002 |
| 2 | 0.000742 | 0.000740 | 0.000746 | 0.000738 | 0.000740 | 0.000003 |
| 3 | 0.001466 | 0.001451 | 0.001461 | 0.001462 | 0.001469 | 0.000007 |
| 4 | 0.002511 | 0.002518 | 0.002524 | 0.002515 | 0.002506 | 0.000007 |
| 5 | 0.004280 | 0.004287 | 0.004291 | 0.004270 | 0.004283 | 0.000008 |
| 6 | 0.007322 | 0.007318 | 0.007310 | 0.007319 | 0.007324 | 0.000006 |
| 7 | 0.012842 | 0.012898 | 0.012891 | 0.012910 | 0.012870 | 0.000027 |
| 8 | 0.023977 | 0.023870 | 0.023935 | 0.023858 | 0.023932 | 0.000049 |
| 9 | 0.048366 | 0.048328 | 0.048366 | 0.048391 | 0.048390 | 0.000025 |
| 10 | 0.188808 | 0.188901 | 0.188789 | 0.188847 | 0.188798 | 0.000046 |

Decile std small relative to decile mean indicates the calibrated prediction is stable across seeds; large std in any decile would indicate the calibration itself is seed-dependent in that risk band.

## Interpretation

Seed 42 pseudo-R2 is within one cross-seed standard deviation of the mean. Its mean top-1% Jaccard against the other seeds is 0.930413, compared with the all-pair mean of 0.931497; its mean Spearman rho against the other seeds is 0.999416, compared with the all-pair mean of 0.999423. On these measures, seed 42 appears representative of the five-seed set.

Full run metadata and pairwise values are in `data/provenance/rank_stability_provenance.json`.

### Flags

- All measured stability metrics are within the prior expectations.
