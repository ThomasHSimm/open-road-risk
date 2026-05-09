# EB Single-Run Validation

This report applies EB-style shrinkage to the current pooled Stage 2 risk scores without modifying production `risk_scores.parquet`. The production EB run uses the positive-event weighted dispersion from `data/provenance/eb_dispersion_provenance.json`; see `quarto/methodology/empirical-bayes-shrinkage.qmd` for the design and `reports/eb_dispersion.md` for the MoM k diagnostics.

## 6.1 Single-Run Ranking Movement

### n_years Distribution

| metric | value |
| --- | --- |
| count | 2,167,557 |
| min | 10.000000 |
| median | 10.000000 |
| max | 10.000000 |
| p5 | 10.000000 |
| p25 | 10.000000 |
| p75 | 10.000000 |
| p95 | 10.000000 |

### k Values

| k | value |
| --- | --- |
| positive_weighted (production) | 3.451158 |
| link_year_weighted | 14.898721 |
| median | 7.573279 |

### eb_weight Distribution

| percentile | eb_weight |
| --- | --- |
| p0 | 0.002601 |
| p5 | 0.228888 |
| p25 | 0.634687 |
| p50 | 0.874102 |
| p75 | 0.962871 |
| p95 | 0.994311 |
| p100 | 0.999848 |

### Percentile Movement

| metric | value |
| --- | --- |
| median_abs_delta | 0.491798 |
| p90_abs_delta | 5.052647 |
| p99_abs_delta | 29.312792 |
| >10 percentile points | 83,806 (3.87%) |
| >25 percentile points | 29,725 (1.37%) |

## 6.2 Top-1% Comparison

| metric | value |
| --- | --- |
| top_1pct_count | 21,675 |
| intersection | 8,421 |
| intersection_pct_of_top1 | 38.85% |
| entering_EB_top1 | 13,254 |
| leaving_EB_top1 | 13,254 |

### Entrants By Road Class

| road_classification | count |
| --- | --- |
| A Road | 7068 |
| B Road | 2205 |
| Classified Unnumbered | 2020 |
| Unclassified | 1647 |
| Motorway | 198 |
| Unknown | 107 |
| Not Classified | 9 |

### Leavers By Road Class

| road_classification | count |
| --- | --- |
| A Road | 9835 |
| B Road | 1410 |
| Classified Unnumbered | 1219 |
| Motorway | 635 |
| Unclassified | 153 |
| Unknown | 2 |

## 6.3 Qualitative Link Review

| direction | link_id | road_classification | estimated_aadt | collision_count | n_years | predicted_xgb | predicted_eb | eb_weight | risk_percentile | risk_percentile_eb |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| entered | BE0C6A74-CA05-44BF-8261-C9FC7410AA6F | Unknown | 1544.700000 | 14 | 10 | 0.010362 | 0.376396 | 0.736598 | 67.248474 | 99.223273 |
| entered | 28E34A54-86C5-4FFB-A3EE-BF2E96D5CAA5 | Unclassified | 637.600000 | 19 | 10 | 0.013720 | 0.619873 | 0.678652 | 71.936286 | 99.735278 |
| entered | EE397B35-B9BC-4D90-95E0-CE0BC73F0C3E | B Road | 1591.300000 | 10 | 10 | 0.015557 | 0.359456 | 0.650666 | 73.924607 | 99.135524 |
| entered | 03408C6C-D7C0-485A-9396-AD12A20E9B2A | Unknown | 1056.600000 | 9 | 10 | 0.015600 | 0.325109 | 0.650035 | 73.966405 | 99.010130 |
| entered | AD0A0BDA-8D7C-4C01-A9C2-056974CBBD10 | Classified Unnumbered | 676.700000 | 14 | 10 | 0.016841 | 0.525250 | 0.632429 | 75.152487 | 99.612329 |
| left | 663D1F8B-85D6-4273-AE27-A20BC0BB5068 | A Road | 54357.900000 | 0 | 10 | 0.945679 | 0.028114 | 0.029729 | 99.971996 | 90.334556 |
| left | 5AB2D086-022B-44E4-AC3A-BCCB3C6A433A | A Road | 17194.600000 | 0 | 10 | 0.982105 | 0.028145 | 0.028658 | 99.973519 | 90.336125 |
| left | F0910578-5FAE-4F8B-8B62-020287B3621B | A Road | 13971.800000 | 0 | 10 | 0.945406 | 0.028114 | 0.029738 | 99.971904 | 90.334510 |
| left | 990A611B-3DEE-4BEF-AB26-F4C20652F69D | A Road | 27764.700000 | 0 | 10 | 0.933682 | 0.028104 | 0.030100 | 99.971073 | 90.333772 |
| left | E6689AB8-D9EF-4849-8737-FA73FA26DB5E | A Road | 33247.100000 | 0 | 10 | 0.925116 | 0.028096 | 0.030370 | 99.970566 | 90.333265 |

## 6.4 Seed-Churn Intersection Diagnostic

EB should disproportionately affect borderline links, which should overlap with the population that seed-churns. If churning links do not show systematically larger EB movement than the general population, EB is probably not addressing the source of seed-induced ranking instability. This is a diagnostic, not a pass/fail criterion.

| population | n_links | abs_delta_gt5 | abs_delta_gt5_pct | gt5_toward_top1 | gt5_away_top1 | abs_delta_gt10 | abs_delta_gt10_pct | gt10_toward_top1 | gt10_away_top1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seed_churn_top_100 (expected approx 21, observed 27) | 27 | 0 | 0.00% | 0 | 0 | 0 | 0.00% | 0 | 0 |
| seed_churn_top_1000 (expected approx 234, observed 283) | 283 | 30 | 10.60% | 0 | 30 | 0 | 0.00% | 0 | 0 |
| full_scored_population | 2,167,557 | 219,664 | 10.13% | 122,228 | 97,436 | 83,806 | 3.87% | 83,806 | 0 |

## 7 k Sensitivity

### Top-1% Membership Count

| k | top_1pct_count |
| --- | --- |
| link_year_weighted | 21,675 |
| positive_weighted | 21,675 |
| median | 21,675 |

### Pairwise Top-1% Overlap

| pair | intersection | union | jaccard |
| --- | --- | --- | --- |
| link_year_weighted vs positive_weighted | 21,169 | 22,181 | 0.954375 |
| link_year_weighted vs median | 21,476 | 21,874 | 0.981805 |
| positive_weighted vs median | 21,368 | 21,982 | 0.972068 |

### Pairwise Spearman

| pair | spearman |
| --- | --- |
| link_year_weighted vs positive_weighted | 0.998003 |
| link_year_weighted vs median | 0.999677 |
| positive_weighted vs median | 0.998892 |

### Percentile Movement Versus Production k

| comparison | abs_delta_gt1 | abs_delta_gt5 | abs_delta_gt10 |
| --- | --- | --- | --- |
| link_year_weighted vs positive_weighted | 30,684 | 14,393 | 10,146 |
| median vs positive_weighted | 26,330 | 14,357 | 10,110 |

If top-1% membership or Spearman moves materially across the three k values, the borrowed-k method is operationally fragile under non-constant dispersion. Material vs not-material is left for human review from the numbers above.

## Closing Recommendation

The diagnostics above should be read as evidence for whether EB is useful, ambiguous, or problematic. This run produces the EB-adjusted scores and single-run validation only; cross-seed EB stability is reserved for session 3.

### Observations Against Priors

- Risk percentiles remain related but not identical: median absolute change is 0.491798 percentile points and p99 is 29.312792.
- Low-exposure or limited-observation links dropping is assessed in the entrant/leaver table via AADT, collision counts, and EB weights.
- Links rising under EB are visible in the deterministic entrant sample; repeated observed collisions relative to the prior should show as lower EB weights and higher predicted_eb.
- With positive-weighted k, movement should concentrate where k * predicted_xgb * n_years is large; the weight distribution above shows how much shrinkage is applied across the scored population.
