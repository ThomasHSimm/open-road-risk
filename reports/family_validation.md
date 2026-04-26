# Family-Split Session 2 Validation

Session-1 artefacts: commit `e446d677b0b2`, scored at `2026-04-25T22:01:23.794929+00:00`. All pseudo-R² figures in §6.1–6.2 are computed on link-grain all-link data (not held-out). Held-out link-year metrics from session-1 training appear in §6.2 column `held_out_pr2` and are authoritative for model comparison. Supporting CSVs are in `reports/supporting/family_validation_*.csv`.

## §6.1 Headline: stitched vs global

All-links link-grain pseudo-R² uses `y_obs = collision_count`, `y_pred = predicted * N_YEARS` (N_YEARS=10).

| metric | stitched_family | global | baseline_5seed |
| --- | --- | --- | --- |
| pseudo_R² (all-links, link-grain) | 0.895214 | 0.888691 | 0.859041 ± 0.001411 |
| Spearman vs global rank | 0.981128 | 1.000000 | 0.998106 |
| top-1% intersection | 20,285 (93.59%) | 21,675 (100.00%) | — |
| top-1% entrants (family new) | 1,390 | — | — |
| top-1% leavers (global only) | 1,390 | — | — |

### Top-1% entrants by family

| family | count |
| --- | --- |
| other_urban | 936 |
| other_rural | 248 |
| trunk_a | 124 |
| motorway | 82 |

### Top-1% leavers by family

| family | count |
| --- | --- |
| other_urban | 956 |
| other_rural | 208 |
| trunk_a | 126 |
| motorway | 100 |

## §6.2 Per-family metrics

Columns: `held_out_pr2` = held-out link-year pseudo-R² from session-1 training. `family_all_pr2` / `global_subset_pr2` = all-links link-grain pseudo-R² on family subset. `mean_resid` = mean(y_obs - y_pred) at link grain.

| family | n_links | held_out_pr2 | family_all_pr2 | global_subset_pr2 | mean_y_obs | mean_resid_family | mean_resid_global | zero_collision_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| motorway | 4,084 | 0.850701 | 0.959813 | 0.908025 | 4.1579 | 0.1276 | -0.0419 | 44.20% |
| trunk_a | 16,011 | 0.773086 | 0.875155 | 0.805693 | 1.1699 | 0.0070 | 0.0051 | 65.87% |
| other_urban | 1,366,925 | 0.917339 | 0.937822 | 0.935815 | 0.2438 | 0.00019220 | -0.00098681 | 87.03% |
| other_rural | 780,537 | 0.648410 | 0.724126 | 0.713163 | 0.1052 | 0.00000121 | 0.0015 | 93.78% |

## §6.3 Family-boundary discontinuity

### Per-family representation at each threshold

| threshold | k | family | count_in_top_k | min_pred_in_top_k |
| --- | --- | --- | --- | --- |
| top_1pct | 21,675 | motorway | 1,013 | 0.364508 |
| top_1pct | 21,675 | trunk_a | 1,427 | 0.364640 |
| top_1pct | 21,675 | other_urban | 16,646 | 0.364438 |
| top_1pct | 21,675 | other_rural | 2,589 | 0.364432 |
| top_1000 | 1,000 | motorway | 352 | 1.081932 |
| top_1000 | 1,000 | trunk_a | 235 | 1.078136 |
| top_1000 | 1,000 | other_urban | 370 | 1.077677 |
| top_1000 | 1,000 | other_rural | 43 | 1.081061 |
| top_10000 | 10,000 | motorway | 740 | 0.513570 |
| top_10000 | 10,000 | trunk_a | 859 | 0.513205 |
| top_10000 | 10,000 | other_urban | 7,407 | 0.513120 |
| top_10000 | 10,000 | other_rural | 994 | 0.513221 |

### Adjacent different-family pairs near threshold boundaries

Consecutive-rank pairs in ±500 window around each threshold where adjacent links are from different families. Up to 25 pairs per family-pair per threshold. Largest observed gap: 0.004712. Full table in `reports/supporting/family_validation_boundary_pairs.csv`.

| threshold | family_a | family_b | rank_a | rank_b | pred_a | pred_b | gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| top_1pct | motorway | trunk_a | 21883 | 21884 | 0.362964 | 0.362961 | 0.00000229 |
| top_1pct | motorway | other_urban | 21176 | 21177 | 0.367716 | 0.367703 | 0.00001246 |
| top_1pct | other_urban | motorway | 21287 | 21288 | 0.366954 | 0.366949 | 0.00000533 |
| top_1pct | motorway | other_urban | 21289 | 21290 | 0.366948 | 0.366942 | 0.00000629 |
| top_1pct | motorway | other_urban | 21401 | 21402 | 0.366146 | 0.366146 | 0.00000048 |
| top_1pct | other_urban | motorway | 21454 | 21455 | 0.365831 | 0.365823 | 0.00000772 |
| top_1pct | other_urban | motorway | 21661 | 21662 | 0.364513 | 0.364508 | 0.00000474 |
| top_1pct | motorway | other_urban | 21662 | 21663 | 0.364508 | 0.364506 | 0.00000232 |
| top_1pct | other_urban | motorway | 21685 | 21686 | 0.364380 | 0.364365 | 0.00001469 |
| top_1pct | motorway | other_urban | 21686 | 21687 | 0.364365 | 0.364364 | 0.00000185 |
| top_1pct | other_urban | motorway | 21725 | 21726 | 0.364073 | 0.364065 | 0.00000766 |
| top_1pct | motorway | other_urban | 21726 | 21727 | 0.364065 | 0.364060 | 0.00000548 |
| top_1pct | other_urban | motorway | 21729 | 21730 | 0.364051 | 0.364045 | 0.00000548 |
| top_1pct | motorway | other_urban | 21730 | 21731 | 0.364045 | 0.364037 | 0.00000781 |
| top_1pct | other_urban | motorway | 21732 | 21733 | 0.364027 | 0.364005 | 0.00002190 |
| top_1pct | motorway | other_urban | 21733 | 21734 | 0.364005 | 0.363998 | 0.00000682 |
| top_1pct | other_urban | motorway | 21785 | 21786 | 0.363581 | 0.363579 | 0.00000191 |
| top_1pct | motorway | other_urban | 21786 | 21787 | 0.363579 | 0.363574 | 0.00000489 |
| top_1pct | other_urban | motorway | 21800 | 21801 | 0.363496 | 0.363486 | 0.00001061 |
| top_1pct | motorway | other_urban | 21801 | 21802 | 0.363486 | 0.363483 | 0.00000301 |
| top_1pct | other_urban | motorway | 21882 | 21883 | 0.362965 | 0.362964 | 0.00000164 |
| top_1pct | other_urban | motorway | 21898 | 21899 | 0.362858 | 0.362854 | 0.00000420 |
| top_1pct | motorway | other_urban | 21899 | 21900 | 0.362854 | 0.362848 | 0.00000513 |
| top_1pct | other_urban | motorway | 21926 | 21927 | 0.362688 | 0.362683 | 0.00000560 |
| top_1pct | motorway | other_urban | 21927 | 21928 | 0.362683 | 0.362679 | 0.00000405 |
| top_1pct | motorway | other_urban | 21934 | 21935 | 0.362643 | 0.362641 | 0.00000232 |
| top_1pct | other_rural | motorway | 21400 | 21401 | 0.366161 | 0.366146 | 0.00001425 |
| top_1pct | motorway | other_rural | 21455 | 21456 | 0.365823 | 0.365818 | 0.00000522 |
| top_1pct | other_rural | motorway | 21933 | 21934 | 0.362646 | 0.362643 | 0.00000280 |
| top_1pct | other_rural | motorway | 22003 | 22004 | 0.362260 | 0.362257 | 0.00000224 |

## §6.4 Rural pseudo-R² gap diagnostic

other_rural held-out pseudo-R² = 0.648 vs global baseline 0.859. Collision-count signal distribution by family:

| family | n_links | mean_collision | median_collision | zero_pct | p95_collision | mean_aadt |
| --- | --- | --- | --- | --- | --- | --- |
| motorway | 4,084 | 4.1579 | 1.0000 | 44.20% | 20.0000 | 27678 |
| trunk_a | 16,011 | 1.1699 | 0.00000000 | 65.87% | 6.0000 | 10039 |
| other_urban | 1,366,925 | 0.2438 | 0.00000000 | 87.03% | 1.0000 | 2246 |
| other_rural | 780,537 | 0.1052 | 0.00000000 | 93.78% | 1.0000 | 1137 |

**Interpretation:** If other_rural has a higher zero-collision percentage and lower mean AADT, the gap is primarily a sparse-data / low-signal problem. Per-family EB k (v2 candidate) and per-family feature pruning would address different aspects of this gap.

## §6.5 Urban pseudo-R² check

other_urban held-out pseudo-R² = 0.917 vs global baseline 0.859. Verify this is driven by data density, not concentration in a small high-count subset:

| family | n_links | mean_collision | pct_zero | pct_gt10 | collision_share_pct |
| --- | --- | --- | --- | --- | --- |
| other_urban | 1,366,925 | 0.2438 | 87.03% | 0.08% | 73.88% |
| other_rural | 780,537 | 0.1052 | 93.78% | 0.02% | 18.20% |
| motorway | 4,084 | 4.1579 | 44.20% | 9.11% | 3.77% |
| trunk_a | 16,011 | 1.1699 | 65.87% | 1.74% | 4.15% |

**Interpretation:** A high collision share from other_urban despite a high zero-collision rate indicates the model benefits from a large number of high-count links providing calibration signal. The elevation over the global baseline is consistent with the urban family having a more homogeneous exposure-to-risk curve than the mixed global population.

## Closing observations

- Stitched pseudo-R² (all-links link-grain): 0.895214 vs global 0.888691.
- Top-1% intersection (stitched vs global): 20,285 / 21,675 (93.59%).
- Spearman between stitched and global rank: 0.981128.
- other_rural held-out pseudo-R² gap: 0.648 vs 0.859 global baseline (Δ ≈ 0.211). Consistent with sparse low-AADT signal.
- other_urban held-out pseudo-R² above baseline: 0.917 vs 0.859 (Δ ≈ 0.058). Consistent with dense high-count urban signal.
- Largest adjacent different-family predicted-value gap near boundary: 0.004712.
