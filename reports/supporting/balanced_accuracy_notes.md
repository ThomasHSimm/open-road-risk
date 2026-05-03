# Balanced Accuracy Notes

Seed file used: `data/models/rank_stability/seed_42.parquet`

Method used here:
The available rank-stability seed output is pooled to one row per link, with
`predicted_xgb` representing the pooled annual prediction. To score a
link-year 0 vs >=1 benchmark without retraining, this analysis expands the
seed-42 prediction back across link-years by joining it to
`data/models/aadt_estimates.parquet` and observed `collision_count` from
`data/features/road_link_annual.parquet`. Each link therefore carries the same
predicted score in every year.

Best balanced accuracy:

- Threshold percentile: `75.0`
- Threshold value: `0.0166778844`
- Balanced accuracy: `0.807662`
- Sensitivity: `0.854218`
- Specificity: `0.761107`
- Predicted positive link-years: `5,418,900`

Approximate comparison to Gilardi et al. (2022) JRSSA:

- Gilardi severe benchmark: `0.675`
- Gilardi slight benchmark: `0.720`
- This pooled-all-crashes model: `0.807662`

This comparison is approximate rather than apples-to-apples because Gilardi
reported severity-stratified models, while the present model predicts all
crashes pooled.

Caveats:

- Positive rate here is `1.8051%` (391,255 positive
  link-years out of 21,675,570), versus roughly 20% in the Gilardi setup
  over 8 years.
- These are point predictions from a fitted XGBoost model, not posterior
  samples.
- The network here is much larger, about 2.17 million links and 21.68 million
  link-years, roughly 600x the size discussed in the benchmark prompt.
- Because the available seed output is pooled to one row per link, the same
  annual predicted score is repeated across years for a given link in this
  benchmark.
