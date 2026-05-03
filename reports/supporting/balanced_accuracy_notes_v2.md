# Balanced Accuracy Notes V2

Seed file used: `data/models/rank_stability/seed_42.parquet`

Method used here:
This benchmark is computed at the correct link grain. The seed-42 rank-stability
output is already pooled to one row per link, so the observed outcome is also
pooled to one row per link:

- `observed_link_outcome = 1` if `collision_count >= 1`
- `observed_link_outcome = 0` otherwise

This supersedes the prior link-year computation in
`reports/supporting/balanced_accuracy_notes.md`, which expanded pooled
per-link predictions back across link-years and was methodologically flawed.

Best balanced accuracy:

- Threshold percentile: `75.0`
- Threshold value: `0.0166778844`
- Balanced accuracy: `0.799319`
- Sensitivity: `0.784122`
- Specificity: `0.814517`
- Predicted positive links: `541,890`

Approximate comparison to Gilardi et al. (2022) JRSSA:

- Gilardi severe benchmark: `0.675`
- Gilardi slight benchmark: `0.720`
- This pooled-all-crashes link-grain model: `0.799319`

This comparison remains approximate rather than apples-to-apples because
Gilardi reported severity-stratified models, while the present model predicts
all crashes pooled.

Caveats:

- Positive rate here is `10.7773%` (233,604 positive links
  out of 2,167,557), not Gilardi's outcome definition.
- These are point predictions from a fitted XGBoost model, not posterior
  samples.
- The network here is much larger, about 2.17 million links, roughly 600x the
  size discussed in the benchmark prompt.
- The benchmark uses pooled link-level outcomes over 2015-2024, matching the
  pooled link-level predictions, rather than year-specific outcomes.
