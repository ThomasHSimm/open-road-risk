# Rank Stability Jaccard Investigation

This diagnostic investigates why the five-seed top-k Jaccard results are non-monotonic: top-1000 overlap is lower than top-100 and top-10000 overlap. It uses only the existing `data/models/rank_stability/seed_<N>.parquet` outputs, ranks links by descending `predicted_xgb`, and checks whether the 100-1000 rank region has tight predicted-risk gaps and concentrated borderline membership churn.

## Predicted-Risk Values At Rank Boundaries

| rank | seed_42 | seed_43 | seed_44 | seed_45 | seed_46 |
| --- | --- | --- | --- | --- | --- |
| 1 | 11.023898 | 10.816540 | 10.526414 | 11.188269 | 10.824545 |
| 10 | 7.778656 | 7.317611 | 7.499019 | 7.956236 | 7.849905 |
| 100 | 3.739568 | 3.654406 | 3.665484 | 3.745479 | 3.588023 |
| 500 | 1.353827 | 1.351644 | 1.353158 | 1.344723 | 1.348596 |
| 1000 | 1.062179 | 1.055831 | 1.053699 | 1.045636 | 1.052371 |
| 5000 | 0.656397 | 0.654587 | 0.653588 | 0.652990 | 0.653288 |
| 10000 | 0.514048 | 0.514068 | 0.513342 | 0.512398 | 0.512672 |
| top-1% (21675) | 0.366555 | 0.365360 | 0.365317 | 0.365356 | 0.365740 |

## Predicted-Risk Gaps By Band

| rank_band | seed | mean_gap | median_gap |
| --- | --- | --- | --- |
| 90-110 | 42 | 0.020595 | 0.015314 |
| 90-110 | 43 | 0.017927 | 0.012016 |
| 90-110 | 44 | 0.022434 | 0.018490 |
| 90-110 | 45 | 0.022207 | 0.013727 |
| 90-110 | 46 | 0.025374 | 0.026898 |
| 490-510 | 42 | 0.001353 | 0.00097471 |
| 490-510 | 43 | 0.001423 | 0.001017 |
| 490-510 | 44 | 0.001203 | 0.001100 |
| 490-510 | 45 | 0.001669 | 0.001404 |
| 490-510 | 46 | 0.001537 | 0.001203 |
| 990-1010 | 42 | 0.00041100 | 0.00039399 |
| 990-1010 | 43 | 0.00045641 | 0.00035602 |
| 990-1010 | 44 | 0.00029195 | 0.00016654 |
| 990-1010 | 45 | 0.00028335 | 0.00025749 |
| 990-1010 | 46 | 0.00030853 | 0.00025165 |
| 9990-10010 | 42 | 0.00002507 | 0.00001928 |
| 9990-10010 | 43 | 0.00001615 | 0.00001121 |
| 9990-10010 | 44 | 0.00002239 | 0.00002003 |
| 9990-10010 | 45 | 0.00001454 | 0.00001234 |
| 9990-10010 | 46 | 0.00001590 | 0.00001037 |

Across seeds, the mean consecutive-rank gap is 0.021708 for ranks 90-110, 0.001437 for ranks 490-510, 0.00035025 for ranks 990-1010, and 0.00001881 for ranks 9990-10010.

## Churning-Link Counts

| k | distinct_churning_links | union_top_k_links | stable_in_all_5 | in_1_seed | in_2_seeds | in_3_seeds | in_4_seeds | in_5_seeds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 21 | 110 | 89 | 5 | 5 | 4 | 7 | 0 |
| 1000 | 234 | 1120 | 886 | 75 | 45 | 51 | 63 | 0 |
| 10000 | 1559 | 10814 | 9255 | 498 | 354 | 309 | 398 | 0 |

For a given k, a churning link is any link that appears in at least one seed's top-k set and is absent from at least one other seed's top-k set. The `in_N_seeds` columns count how many churning links appear in exactly N of the five top-k sets.

## Interpretation

The 100-1000 band is not explained by smaller local predicted-risk gaps than the k=10000 neighbourhood: the average of the 490-510 and 990-1010 mean gaps is 0.00089353, while the 9990-10010 mean gap is 0.00001881. The boundary table instead shows a steep early risk curve followed by much flatter values by rank 10000, so the lower top-1000 Jaccard is not a simple consequence of tighter prediction spacing around rank 1000. Churn at k=1000 is spread across 234 distinct links in a union of 1,120 candidate top-1000 links, with most churn links appearing in only one or four seeds rather than being evenly split. The practical caveat is that narrow top-k cuts, especially around k=1000, should be treated as a fuzzy frontier rather than a hard deterministic ordering; adjacent links near the threshold may swap in or out across equally valid seed realisations.
