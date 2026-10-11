# EB Single-Run Validation

This report applies EB-style shrinkage to the current pooled Stage 2 risk scores without modifying production `risk_scores.parquet`. The production EB run uses the positive-event weighted dispersion from `data/provenance/eb_dispersion_provenance.json`; see `quarto/methodology/empirical-bayes-shrinkage.qmd` for the design and `reports/eb_dispersion.md` for the MoM k diagnostics.

## 6.1 Single-Run Ranking Movement

### n_years Distribution

| metric | value |
| --- | --- |
| count | 3,941,299 |
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
| p0 | 0.001083 |
| p5 | 0.138045 |
| p25 | 0.475633 |
| p50 | 0.776692 |
| p75 | 0.928032 |
| p95 | 0.987354 |
| p100 | 0.999607 |

### Percentile Movement

| metric | value |
| --- | --- |
| median_abs_delta | 0.726968 |
| p90_abs_delta | 6.819249 |
| p99_abs_delta | 32.873463 |
| >10 percentile points | 222,769 (5.65%) |
| >25 percentile points | 71,198 (1.81%) |

## 6.2 Top-1% Comparison

| metric | value |
| --- | --- |
| top_1pct_count | 39,412 |
| intersection | 17,829 |
| intersection_pct_of_top1 | 45.24% |
| entering_EB_top1 | 21,583 |
| leaving_EB_top1 | 21,583 |

### Entrants By Road Class

| road_classification | count |
| --- | --- |
| A Road | 12200 |
| B Road | 3774 |
| Classified Unnumbered | 3120 |
| Unclassified | 1900 |
| Motorway | 368 |
| Unknown | 154 |
| Not Classified | 67 |

### Leavers By Road Class

| road_classification | count |
| --- | --- |
| A Road | 18378 |
| B Road | 1430 |
| Motorway | 889 |
| Classified Unnumbered | 882 |
| Unclassified | 3 |
| Unknown | 1 |

## 6.3 Qualitative Link Review

| direction | link_id | road_classification | estimated_aadt | collision_count | n_years | predicted_xgb | predicted_eb | eb_weight | risk_percentile | risk_percentile_eb |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| entered | 62BAADBD-84D5-4426-B072-53FB9F6DC407 | Classified Unnumbered | 320.200000 | 20 | 10 | 0.008914 | 0.477327 | 0.764745 | 51.393868 | 99.052165 |
| entered | 078F352D-5F15-4405-82E3-7CD95F7BB6F9 | Not Classified | 948.100000 | 16 | 10 | 0.015165 | 0.559656 | 0.656437 | 61.875488 | 99.292137 |
| entered | BF0DB0FF-E79E-481A-96D7-EEFC5C3135CA | Unclassified | 1210.200000 | 17 | 10 | 0.019209 | 0.689254 | 0.601351 | 66.248387 | 99.526527 |
| entered | B814B09C-879A-490E-A777-8AE6E790BF54 | Unclassified | 395.500000 | 12 | 10 | 0.022575 | 0.538195 | 0.562078 | 69.134770 | 99.263872 |
| entered | 45D17E74-420F-457B-BEA8-88929B72C6C3 | Unknown | 1584.900000 | 24 | 10 | 0.023923 | 1.098470 | 0.547764 | 70.152480 | 99.813945 |
| left | 8ADEDB60-30DB-49B7-B8EF-6EFFE14C1C73 | Motorway | 49332.800000 | 0 | 10 | 2.714892 | 0.028670 | 0.010560 | 99.978408 | 87.314690 |
| left | 2F42EE5E-864C-4DFA-B32B-AE5719DE5C69 | A Road | 20754.800000 | 0 | 10 | 2.608722 | 0.028657 | 0.010985 | 99.976937 | 87.314106 |
| left | 410822CD-2365-434F-B2FF-086AB4B1E702 | Motorway | 54224.000000 | 0 | 10 | 2.463457 | 0.028639 | 0.011626 | 99.973993 | 87.313218 |
| left | 87B34109-337D-46B7-B856-C8BFE2C3E2CC | A Road | 17599.900000 | 0 | 10 | 2.410379 | 0.028632 | 0.011878 | 99.972953 | 87.313091 |
| left | 98FD9D7A-270F-4C9C-9C67-CA7D46FD1C28 | A Road | 22013.700000 | 0 | 10 | 2.274653 | 0.028611 | 0.012578 | 99.969680 | 87.312330 |

## 6.4 Seed-Churn Intersection Diagnostic

EB should disproportionately affect borderline links, which should overlap with the population that seed-churns. If churning links do not show systematically larger EB movement than the general population, EB is probably not addressing the source of seed-induced ranking instability. This is a diagnostic, not a pass/fail criterion.

| population | n_links | abs_delta_gt5 | abs_delta_gt5_pct | gt5_toward_top1 | gt5_away_top1 | abs_delta_gt10 | abs_delta_gt10_pct | gt10_toward_top1 | gt10_away_top1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seed_churn_top_100 (expected approx 21, observed 27) | 27 | 0 | 0.00% | 0 | 0 | 0 | 0.00% | 0 | 0 |
| seed_churn_top_1000 (expected approx 234, observed 283) | 283 | 11 | 3.89% | 1 | 10 | 10 | 3.53% | 0 | 10 |
| full_scored_population | 3,941,299 | 572,027 | 14.51% | 274,716 | 297,311 | 222,769 | 5.65% | 193,620 | 29,149 |

## 7 k Sensitivity

### Top-1% Membership Count

| k | top_1pct_count |
| --- | --- |
| link_year_weighted | 39,412 |
| positive_weighted | 39,412 |
| median | 39,412 |

### Pairwise Top-1% Overlap

| pair | intersection | union | jaccard |
| --- | --- | --- | --- |
| link_year_weighted vs positive_weighted | 38,577 | 40,247 | 0.958506 |
| link_year_weighted vs median | 39,153 | 39,671 | 0.986943 |
| positive_weighted vs median | 38,836 | 39,988 | 0.971191 |

### Pairwise Spearman

| pair | spearman |
| --- | --- |
| link_year_weighted vs positive_weighted | 0.997818 |
| link_year_weighted vs median | 0.999668 |
| positive_weighted vs median | 0.998658 |

### Percentile Movement Versus Production k

| comparison | abs_delta_gt1 | abs_delta_gt5 | abs_delta_gt10 |
| --- | --- | --- | --- |
| link_year_weighted vs positive_weighted | 42,663 | 23,730 | 15,913 |
| median vs positive_weighted | 40,137 | 20,800 | 15,855 |

If top-1% membership or Spearman moves materially across the three k values, the borrowed-k method is operationally fragile under non-constant dispersion. Material vs not-material is left for human review from the numbers above.

## Closing Recommendation

The diagnostics above should be read as evidence for whether EB is useful, ambiguous, or problematic. This run produces the EB-adjusted scores and single-run validation only; cross-seed EB stability is reserved for session 3.

### Observations Against Priors

- Risk percentiles remain related but not identical: median absolute change is 0.726968 percentile points and p99 is 32.873463.
- Low-exposure or limited-observation links dropping is assessed in the entrant/leaver table via AADT, collision counts, and EB weights.
- Links rising under EB are visible in the deterministic entrant sample; repeated observed collisions relative to the prior should show as lower EB weights and higher predicted_eb.
- With positive-weighted k, movement should concentrate where k * predicted_xgb * n_years is large; the weight distribution above shows how much shrinkage is applied across the scored population.
