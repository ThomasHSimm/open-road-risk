# Rank Stability Evaluation

This report evaluates Stage 2 XGBoost rank stability across five seeds (42-46), with seed 42 representing the production realisation. The evaluation measures pseudo-R2 variation, top-k ranking overlap, full-rank Spearman correlation, and observed per-decile calibration stability. The expected per-seed row count, taken from production risk_scores.parquet before the run, is 2,167,557 links.

A follow-up investigation into the non-monotonic top-k Jaccard pattern is in `reports/rank_stability_investigation.md`.

## Pseudo-R2

| seed | pseudo_R2 |
| --- | --- |
| 42 | 0.857516 |
| 43 | 0.858736 |
| 44 | 0.861335 |
| 45 | 0.858514 |
| 46 | 0.859102 |
| mean | 0.859041 |
| std | 0.001411 |

## Top-k Jaccard

| k | pairwise_mean | pairwise_min |
| --- | --- | --- |
| 100 | 0.903206 | 0.869159 |
| 1000 | 0.893325 | 0.863933 |
| 10000 | 0.927142 | 0.919386 |
| 21675 | 0.918494 | 0.907843 |

## Spearman Correlation

| metric | value |
| --- | --- |
| pairwise_mean | 0.998106 |
| pairwise_min | 0.997841 |

## Calibration

| decile | seed_42 | seed_43 | seed_44 | seed_45 | seed_46 | std |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.000044 | 0.000046 | 0.000043 | 0.000045 | 0.000045 | 0.000001 |
| 2 | 0.000087 | 0.000084 | 0.000083 | 0.000080 | 0.000088 | 0.000003 |
| 3 | 0.000132 | 0.000135 | 0.000130 | 0.000134 | 0.000124 | 0.000004 |
| 4 | 0.000232 | 0.000225 | 0.000224 | 0.000233 | 0.000234 | 0.000005 |
| 5 | 0.000312 | 0.000315 | 0.000311 | 0.000300 | 0.000303 | 0.000006 |
| 6 | 0.000510 | 0.000505 | 0.000514 | 0.000507 | 0.000513 | 0.000004 |
| 7 | 0.000897 | 0.000906 | 0.000896 | 0.000899 | 0.000896 | 0.000004 |
| 8 | 0.001826 | 0.001819 | 0.001833 | 0.001820 | 0.001830 | 0.000006 |
| 9 | 0.010645 | 0.010578 | 0.010548 | 0.010611 | 0.010602 | 0.000036 |
| 10 | 0.193380 | 0.193452 | 0.193482 | 0.193437 | 0.193430 | 0.000037 |

The std column shows how much observed decile calibration varies across seeds; large std in any decile would indicate that calibration is seed-dependent in that risk band. Here, all decile stds are very small relative to their decile means: the largest relative std is around 3-4% in lower deciles, falling to about 0.34% in decile 9 and under 0.1% in the top decile, so per-decile calibration is stable across seeds.

## Interpretation

Seed 42 is nominally the lowest pseudo-R2 of the five, but the cross-seed spread is operationally negligible (std 0.001411). Its rank-overlap and Spearman correlation against the other seeds are close to the all-pair means, so the production seed is representative and does not appear to be an outlier.

The top-k Jaccard pattern is non-monotonic in k: k=1000 is the lowest (0.893 mean), k=100 and top-1% are similar at roughly 0.90-0.92, and k=10000 is the highest (0.927). The follow-up investigation in `reports/rank_stability_investigation.md` rules out the most obvious mechanistic explanation, tight predicted-risk gaps in the 100-1000 band: gaps near rank 1000 are actually larger than near rank 10000, not smaller. A consistent, but not directly proven, explanation is that the steep part of the risk curve sits in the top roughly 1000 ranks, where small tree-structure perturbations across seeds have the most leverage on which specific links land in narrow top-k cuts; below that, the model is differentiating among a large mass of moderate-risk links and any fixed number of churners gets diluted across a wider denominator.

For downstream use, narrow top-k cuts, particularly k=1000, should be treated as a fuzzy frontier rather than a deterministic ranking. The investigation found 234 distinct links that churn in or out of top-1000 across seed pairs, with 886 links stable in all five seeds. A high-confidence top-1000 defined as the intersection across seeds is one practical way to express this stability where it matters downstream. The full ranking and the calibrated probabilities themselves are stable; what varies is membership at narrow threshold cuts.

Note for future production re-runs: Stage 2 XGBoost training is now pinned to `n_jobs=1` for cross-machine reproducibility. Re-running production training from the current code may therefore produce a `risk_scores.parquet` that differs from the current canonical output in tree structure, even where fit quality and rank stability remain comparable.

Full run metadata and pairwise values are in `data/provenance/rank_stability_provenance.json`.

### Flags

- Pseudo-R2 spread (0.001411) is roughly 7x tighter than the <0.01 prior. Fit quality is highly stable across seeds.
- Calibration std is well within the 10%-of-decile-mean prior in every decile. The largest relative std is in the lower-risk deciles (around 3-4% relative); top-decile relative std is under 0.1%. Calibrated predictions are essentially seed-invariant.
- Spearman mean (0.998) and min (0.998) exceed the >0.99 prior. Full-ranking ordering is stable.
- Top-1% Jaccard mean (0.918) is below the >0.93 prior. Top-1000 Jaccard (0.893) is the lowest of the four k values measured, despite k=1000 being neither the smallest nor the largest k tested. The follow-up investigation in `reports/rank_stability_investigation.md` rules out tight predicted-risk clustering at rank 1000 as the cause and characterises the churn population.
