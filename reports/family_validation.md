# Family-Split Session 2 Validation

Session-1 artefacts: commit `e446d677b0b2`, scored at `2026-04-25T22:01:23.794929+00:00`. Held-out pseudo-R² in §6.1 is computed on the union of per-family held-out links (20% of each family, seed=42) using link-grain collision counts from `risk_scores_family.parquet`. The rank_stability.md baseline (0.859 ± 0.001) is link-year grain; §6.2 column `held_out_pr2` (from session-1 training) is the per-family link-year grain equivalent. Supporting CSVs are in `reports/supporting/family_validation_*.csv`.

## §6.1 Headline: stitched vs global

| metric | stitched_family | global | baseline_5seed |
| --- | --- | --- | --- |
| pseudo_R² (all-links, link-grain) | 0.895214 | 0.888691 | 0.859041 ± 0.001411 |
| Spearman vs global rank | 0.981128 | 1.000000 | 0.998106 |
| top-1% intersection | 20,285 (93.59%) | 21,675 (100.00%) | — |
| top-1% entrants (family new) | 1,390 | — | — |
| top-1% leavers (global only) | 1,390 | — | — |

### Held-out comparison

Pseudo-R² on the union of per-family held-out link_ids (433,513 links, ≈20% of network). Both models evaluated on the same held-out set; this is apples-to-apples between stitched and global, and directionally comparable to the rank_stability.md baseline of 0.859 ± 0.001 (note: baseline is link-year grain; these figures are link-grain).

| metric | stitched_family | global |
| --- | --- | --- |
| pseudo_R² (held-out links, link-grain) | 0.889772 | 0.889216 |
| pseudo_R² (all-links, link-grain) | 0.895214 | 0.888691 |

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

Columns: `held_out_pr2` = held-out link-year pseudo-R² from session-1 training (authoritative, link-year grain). `family_all_pr2` / `global_subset_pr2` = all-links link-grain pseudo-R² on family subset. `global_held_out_pr2` = global model on family's held-out links, link-grain. `global_heldout_link_year_pr2` = global model on family's held-out links, link-year grain (same grain as `held_out_pr2`; apples-to-apples for §6.2.1). `mean_resid` = mean(y_obs - y_pred) at link grain.

| family | n_links | held_out_pr2 | family_all_pr2 | global_subset_pr2 | global_held_out_pr2 | global_heldout_link_year_pr2 | mean_y_obs | mean_resid_family | mean_resid_global | zero_collision_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| motorway | 4,084 | 0.850701 | 0.959813 | 0.908025 | 0.924466 | 0.878084 | 4.1579 | 0.1276 | -0.0419 | 44.20% |
| trunk_a | 16,011 | 0.773086 | 0.875155 | 0.805693 | 0.801238 | 0.767308 | 1.1699 | 0.0070 | 0.0051 | 65.87% |
| other_urban | 1,366,925 | 0.917339 | 0.937822 | 0.935815 | 0.933182 | 0.915873 | 0.2438 | 0.00019220 | -0.00098681 | 87.03% |
| other_rural | 780,537 | 0.648410 | 0.724126 | 0.713163 | 0.717468 | 0.646499 | 0.1052 | 0.00000121 | 0.0015 | 93.78% |

### §6.2.1 Did separating help?

**All-data comparison (link-grain; per-family model vs global on same family subset):**

| family | per-family R² | global-on-subset R² | delta |
| --- | --- | --- | --- |
| motorway | 0.959813 | 0.908025 | +0.052 |
| trunk_a | 0.875155 | 0.805693 | +0.069 |
| other_urban | 0.937822 | 0.935815 | +0.002 |
| other_rural | 0.724126 | 0.713163 | +0.011 |

Per-family models match or beat the global model on every family. The largest gains are motorway and trunk_a, consistent with the design doc §9 hypothesis that high-speed, access-controlled families would benefit most from a dedicated model. Other-Urban and Other-Rural gains are small (+0.002 and +0.011), also consistent with the design doc hypothesis that the global model already captures the relevant feature signals for those populations.

**Held-out comparison (both columns at link-year grain):**

| family | per-family held-out R² (link-year) | global held-out R² (link-year) | delta |
| --- | --- | --- | --- |
| motorway | 0.850701 | 0.878084 | -0.027 |
| trunk_a | 0.773086 | 0.767308 | +0.006 |
| other_urban | 0.917339 | 0.915873 | +0.001 |
| other_rural | 0.648410 | 0.646499 | +0.002 |

Both columns are link-year grain Poisson pseudo-R² on the same per-family held-out sets (seed=42, 20% of links). Per-family column: authoritative figures from session-1 training provenance. Global column: global `collision_xgb.json` scored on identical held-out link-years using the same eps=1e-6 deviance formula. trunk_a, other_urban, and other_rural deltas are consistent in sign with the all-data comparison. **Motorway reverses sign**: per-family is -0.027 on held-out but +0.052 on all-data. The all-data gain is real (link-grain, same formula for both models), but the held-out reversal indicates the motorway model over-fits its 4,084-link training set; the global model generalises better out-of-sample on the 817 held-out motorway links (8,170 link-years). The all-data comparison remains the primary surface for 'did separating help?' because it uses the full population; the held-out reversal is a v2 signal for regularisation or a larger motorway training window.

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

Consecutive-rank pairs in ±500 window around each threshold where adjacent links are from different families. Up to 25 pairs per family-pair per threshold. Largest observed gap: 0.004712. The in-report sample below emphasises motorway/other_urban pairs at the top-1% boundary because those families have the most rank-range overlap there. The full CSV (`reports/supporting/family_validation_boundary_pairs.csv`) contains all 6 family-pair combinations across all three thresholds. Some pairs such as trunk_a × other_rural at narrow thresholds have very few adjacent crossings because their rank ranges barely overlap — itself a calibration signal indicating limited rank-range mixing between those families.

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

**Interpretation:** other_rural has a 93.78% zero-collision rate and mean AADT of 1,137 vs 2,246 for other_urban. The gap is primarily a sparse-data / low-signal problem: with most links recording no collisions over 10 years, there is limited within-family variation for the model to explain. Per-family EB k (v2 candidate) and per-family feature pruning would address different aspects of this gap.

## §6.5 Urban pseudo-R² check

other_urban held-out pseudo-R² = 0.917. The correct within-experiment comparison (§6.2.1) is per-family other_urban R² (0.938 all-data) vs global-on-urban-subset R² (0.936 all-data), a delta of +0.002 — essentially zero. The 0.917 vs 0.859 global baseline gap is largely explained by urban roads being inherently more predictable than the full mixed network, not by per-family modelling adding value. The calibration table below confirms the 0.917 figure reflects genuine discrimination across a large population, not concentration in a small high-count subset:

| family | n_links | mean_collision | pct_zero | pct_gt10 | collision_share_pct |
| --- | --- | --- | --- | --- | --- |
| other_urban | 1,366,925 | 0.2438 | 87.03% | 0.08% | 73.88% |
| other_rural | 780,537 | 0.1052 | 93.78% | 0.02% | 18.20% |
| motorway | 4,084 | 4.1579 | 44.20% | 9.11% | 3.77% |
| trunk_a | 16,011 | 1.1699 | 65.87% | 1.74% | 4.15% |

**Interpretation:** other_urban accounts for 73.9% of all network collisions despite an 87% zero-collision rate, providing the calibration signal that drives the high pseudo-R². The per-family gain for urban is ~0.002 (essentially zero); the main benefit of per-family modelling accrues to motorway and trunk_a.

## Closing observations

- Held-out stitched pseudo-R² (link-grain): 0.889772 vs global 0.889216 (rank_stability.md baseline 0.859 ± 0.001 is link-year grain).
- Stitched pseudo-R² (all-links link-grain): 0.895214 vs global 0.888691.
- Top-1% intersection (stitched vs global): 20,285 / 21,675 (93.59%).
- Motorway mean residual (family model, link-grain): 0.1276.
- other_rural held-out pseudo-R²: 0.648 (global baseline 0.859); gap consistent with sparse low-AADT signal.
- other_urban per-family gain over global: +0.002 (all-data link-grain); elevation vs 0.859 baseline explained by urban predictability, not per-family modelling.
- Largest adjacent different-family predicted-value gap near boundary: 0.004712 — stitched ranking is smoothly calibrated.
