# Temporal Ablation Summary

## Pre-Registered Decision Rule

A new feature configuration earns adoption if BOTH:
- Pseudo-R² improvement > 0.009 over the baseline (1.5x noise floor of 0.006), AND
- Test deviance reduction > 0.6% (1.5x noise floor of ~0.4%).

Improvement must be observed on at least 4 of 5 seeds. Mixed seed outcomes (passes on 1-3 seeds) count as null result.

Anything below those thresholds counts as null result, regardless of sign of the change.

## Feature Source Note

Configuration C uses `webtris_hgv_pct` from `data/features/road_traffic_features.parquet` rather than `timezone_profiles.parquet`, because `timezone_profiles.parquet` does not contain a plain WebTRIS HGV percentage column. This is the literal WebTRIS HGV% descriptor.

## Coverage Rates

- `core_overnight_ratio` non-missing share: 1.0000

- `webtris_hgv_pct` non-missing share: 0.1425

## Config Summary

### Primary Evaluation

| config | pseudo_r2_mean | pseudo_r2_min | pseudo_r2_max | deviance_mean | deviance_min | deviance_max |
| --- | --- | --- | --- | --- | --- | --- |
| A | 0.321373 | 0.315444 | 0.325382 | 495787.341834 | 493381.566981 | 497785.782657 |
| B | 0.325502 | 0.319691 | 0.329535 | 492771.662726 | 490320.901914 | 494501.800246 |
| C | 0.327225 | 0.321424 | 0.331036 | 491512.899793 | 489072.048931 | 493189.873113 |

### Full Evaluation

| config | pseudo_r2_mean | pseudo_r2_min | pseudo_r2_max | deviance_mean | deviance_min | deviance_max |
| --- | --- | --- | --- | --- | --- | --- |
| A | 0.323498 | 0.321372 | 0.326529 | 497288.986849 | 496321.752764 | 498461.647461 |
| B | 0.327610 | 0.325532 | 0.330682 | 494266.350491 | 493576.383396 | 495170.917759 |
| C | 0.329337 | 0.327157 | 0.332182 | 492996.793767 | 492243.406732 | 493856.074178 |

## Primary Rule Check

| config | seed | pseudo_r2_improvement | deviance_reduction_pct | passes_rule |
| --- | --- | --- | --- | --- |
| B | 42 | 0.004247 | 0.006203 | False |
| B | 43 | 0.004178 | 0.006141 | False |
| B | 44 | 0.003587 | 0.005313 | False |
| B | 45 | 0.004153 | 0.006156 | False |
| B | 46 | 0.004476 | 0.006597 | False |
| C | 42 | 0.005979 | 0.008735 | False |
| C | 43 | 0.005795 | 0.008517 | False |
| C | 44 | 0.005562 | 0.008239 | False |
| C | 45 | 0.005654 | 0.008382 | False |
| C | 46 | 0.006264 | 0.009233 | False |

## Verdicts

- Config B: `null`

- Config C: `null`

## Top-1% Rank Jaccard vs Baseline

| config | mean | min | max |
| --- | --- | --- | --- |
| B | 0.764442 | 0.758407 | 0.770038 |
| C | 0.751077 | 0.748760 | 0.752294 |
