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
| positive_weighted (production) | 3.074322 |
| link_year_weighted | 146.440984 |
| median | 82.436850 |

### eb_weight Distribution

| percentile | eb_weight |
| --- | --- |
| p0 | 0.002942 |
| p5 | 0.215992 |
| p25 | 0.942876 |
| p50 | 0.986152 |
| p75 | 0.994727 |
| p95 | 0.997965 |
| p100 | 0.999970 |

### Percentile Movement

| metric | value |
| --- | --- |
| median_abs_delta | 0.068833 |
| p90_abs_delta | 0.303245 |
| p99_abs_delta | 2.963751 |
| >10 percentile points | 6,597 (0.30%) |
| >25 percentile points | 1,673 (0.08%) |

## 6.2 Top-1% Comparison

| metric | value |
| --- | --- |
| top_1pct_count | 21,675 |
| intersection | 18,408 |
| intersection_pct_of_top1 | 84.93% |
| entering_EB_top1 | 3,267 |
| leaving_EB_top1 | 3,267 |

### Entrants By Road Class

| road_classification | count |
| --- | --- |
| A Road | 1645 |
| B Road | 600 |
| Classified Unnumbered | 460 |
| Unclassified | 453 |
| Motorway | 51 |
| Unknown | 49 |
| Not Classified | 9 |

### Leavers By Road Class

| road_classification | count |
| --- | --- |
| A Road | 2096 |
| Classified Unnumbered | 433 |
| B Road | 391 |
| Unclassified | 181 |
| Motorway | 144 |
| Unknown | 20 |
| Not Classified | 2 |

## 6.3 Qualitative Link Review

| direction | link_id | road_classification | estimated_aadt | collision_count | n_years | predicted_xgb | predicted_eb | eb_weight | risk_percentile | risk_percentile_eb |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| entered | A030CDDF-A2FA-40B6-A449-1DB2F3684B75 | A Road | 14670.300000 | 14 | 10 | 0.024974 | 0.622174 | 0.565681 | 89.213663 | 99.692557 |
| entered | 4CF48109-02C0-4F29-89F4-4A6239BEC42F | Motorway | 25835.400000 | 11 | 10 | 0.027084 | 0.514553 | 0.545660 | 89.356866 | 99.545848 |
| entered | 6A56043C-517A-4DFD-856B-DC4759EB1A6E | A Road | 5603.300000 | 10 | 10 | 0.032061 | 0.512538 | 0.503608 | 89.614621 | 99.544833 |
| entered | C7F57C41-3F02-4FDB-8741-99553F7FBEF8 | Classified Unnumbered | 866.300000 | 9 | 10 | 0.027425 | 0.426581 | 0.542554 | 89.377442 | 99.304378 |
| entered | CCDE2762-6B32-43FD-9C91-38FFA11208CB | A Road | 15406.000000 | 10 | 10 | 0.030794 | 0.502128 | 0.513691 | 89.560136 | 99.482182 |
| left | BBEF00E6-223E-4D1E-AB1A-A9405DECEB35 | Motorway | 34357.000000 | 0 | 10 | 1.075141 | 0.031572 | 0.029366 | 99.955941 | 89.824074 |
| left | 820518D0-C224-46A4-8FB7-4EEFC724BD35 | Motorway | 27334.300000 | 0 | 10 | 0.988530 | 0.031491 | 0.031857 | 99.942839 | 89.822920 |
| left | 8C790D90-3617-40D3-A1E9-3B7E7F00E8F2 | Motorway | 28871.000000 | 0 | 10 | 0.940153 | 0.031440 | 0.033441 | 99.931997 | 89.822275 |
| left | 404C1C28-6BC0-42AA-99B3-532EF2CE70E1 | Motorway | 28871.000000 | 0 | 10 | 0.880066 | 0.031368 | 0.035643 | 99.914374 | 89.821398 |
| left | 14192A90-CB96-4B73-9A68-5AD3794CE5B2 | Motorway | 28871.000000 | 0 | 10 | 0.865161 | 0.031349 | 0.036235 | 99.908330 | 89.821213 |

## 6.4 Seed-Churn Intersection Diagnostic

EB should disproportionately affect borderline links, which should overlap with the population that seed-churns. If churning links do not show systematically larger EB movement than the general population, EB is probably not addressing the source of seed-induced ranking instability. This is a diagnostic, not a pass/fail criterion.

| population | n_links | abs_delta_gt5 | abs_delta_gt5_pct | gt5_toward_top1 | gt5_away_top1 | abs_delta_gt10 | abs_delta_gt10_pct | gt10_toward_top1 | gt10_away_top1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seed_churn_top_100 | 21 | 0 | 0.00% | 0 | 0 | 0 | 0.00% | 0 | 0 |
| seed_churn_top_1000 | 234 | 2 | 0.85% | 0 | 2 | 1 | 0.43% | 0 | 1 |
| full_scored_population | 2,167,557 | 16,114 | 0.74% | 15,445 | 669 | 6,597 | 0.30% | 6,590 | 7 |

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
| link_year_weighted vs positive_weighted | 21,263 | 22,087 | 0.962693 |
| link_year_weighted vs median | 21,667 | 21,683 | 0.999262 |
| positive_weighted vs median | 21,271 | 22,079 | 0.963404 |

### Pairwise Spearman

| pair | spearman |
| --- | --- |
| link_year_weighted vs positive_weighted | 0.999557 |
| link_year_weighted vs median | 0.999999 |
| positive_weighted vs median | 0.999560 |

### Percentile Movement Versus Production k

| comparison | abs_delta_gt1 | abs_delta_gt5 | abs_delta_gt10 |
| --- | --- | --- | --- |
| link_year_weighted vs positive_weighted | 11,645 | 7,386 | 2,647 |
| median vs positive_weighted | 11,649 | 7,309 | 2,561 |

If top-1% membership or Spearman moves materially across the three k values, the borrowed-k method is operationally fragile under non-constant dispersion. Material vs not-material is left for human review from the numbers above.

## Closing Recommendation

The diagnostics above should be read as evidence for whether EB is useful, ambiguous, or problematic. This run produces the EB-adjusted scores and single-run validation only; cross-seed EB stability is reserved for session 3.

### Observations Against Priors

- Risk percentiles remain related but not identical: median absolute change is 0.068833 percentile points and p99 is 2.963751.
- Low-exposure or limited-observation links dropping is assessed in the entrant/leaver table via AADT, collision counts, and EB weights.
- Links rising under EB are visible in the deterministic entrant sample; repeated observed collisions relative to the prior should show as lower EB weights and higher predicted_eb.
- With positive-weighted k, movement should concentrate where k * predicted_xgb * n_years is large; the weight distribution above shows how much shrinkage is applied across the scored population.
