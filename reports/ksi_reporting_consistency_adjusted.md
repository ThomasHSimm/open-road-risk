# Adjusted Expected KSI Reporting Consistency Diagnostic

**Status:** Part A diagnostic rerun only. No KSI modelling, EB shrinkage, decision-register edit, or production model change.

## Purpose

This report reruns the KSI Part A force/year reporting consistency check using DfT collision-level adjusted severity probabilities. It tests whether the adjusted expected KSI target clears the same pre-registered +/-20% year-on-year KSI-to-all-injury ratio threshold used in the original Part A diagnostic.

## Input Files

- Stage 2 collision count table: `data/features/road_link_annual.parquet`
- Snapped collision source: `data/processed/stats19/snapped_weighted.parquet`
- Original unadjusted Part A report: `reports/ksi_reporting_consistency.md`
- Input collision rows: 452,897
- Retained rows after Stage 2 snap-method and snap-score filters: 450,991

## Target Definition

For each retained collision:

```text
fatal_indicator = 1 if collision_severity == 1 else 0
adjusted_expected_ksi = fatal_indicator + collision_adjusted_severity_serious
```

`enhanced_severity_collision` is not used directly as the KSI target. The adjusted target is an expected-count target, not an observed integer collision count.

## Summary

| metric | value |
| --- | --- |
| force/year rows | 230 |
| forces | 23 |
| years | 2015-2024 |
| all-injury collisions | 450,991 |
| adjusted expected KSI | 114,817.3 |
| overall adjusted expected KSI/all-injury ratio | 0.2546 |
| pre-registered flagged force/year rows | 15 |
| practical-sensitivity flagged force/year rows | 13 |

## By Year

| year | all_injury_count | adjusted_expected_ksi | adjusted_expected_ksi_to_all_injury_ratio | pre_registered_flagged_force_years | practical_sensitivity_flagged_force_years |
| --- | --- | --- | --- | --- | --- |
| 2015 | 56,022 | 12,672.0 | 0.2262 | 0 | 0 |
| 2016 | 54,330 | 11,967.2 | 0.2203 | 3 | 3 |
| 2017 | 51,018 | 12,020.8 | 0.2356 | 2 | 2 |
| 2018 | 48,030 | 11,979.7 | 0.2494 | 1 | 1 |
| 2019 | 45,318 | 11,519.6 | 0.2542 | 4 | 3 |
| 2020 | 34,540 | 9,188.1 | 0.2660 | 1 | 1 |
| 2021 | 39,345 | 10,571.9 | 0.2687 | 1 | 1 |
| 2022 | 40,995 | 11,496.4 | 0.2804 | 1 | 0 |
| 2023 | 40,531 | 11,601.1 | 0.2862 | 1 | 1 |
| 2024 | 40,862 | 11,800.5 | 0.2888 | 1 | 1 |

## Force-Year Ratios

| police_force | force_name | year | all_injury_count | adjusted_expected_ksi | adjusted_expected_ksi_to_all_injury_ratio | ratio_yoy_pct_change | pre_registered_flag |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | Cumbria | 2015 | 1,266 | 308.9 | 0.2440 |  | no |
| 3 | Cumbria | 2016 | 1,247 | 242.0 | 0.1941 | -20.5% | yes |
| 3 | Cumbria | 2017 | 1,256 | 256.0 | 0.2038 | 5.0% | no |
| 3 | Cumbria | 2018 | 1,206 | 278.0 | 0.2305 | 13.1% | no |
| 3 | Cumbria | 2019 | 1,011 | 282.0 | 0.2789 | 21.0% | yes |
| 3 | Cumbria | 2020 | 746 | 238.0 | 0.3190 | 14.4% | no |
| 3 | Cumbria | 2021 | 732 | 204.0 | 0.2787 | -12.6% | no |
| 3 | Cumbria | 2022 | 835 | 274.0 | 0.3281 | 17.7% | no |
| 3 | Cumbria | 2023 | 854 | 270.0 | 0.3162 | -3.7% | no |
| 3 | Cumbria | 2024 | 775 | 238.0 | 0.3071 | -2.9% | no |
| 4 | Lancashire | 2015 | 3,670 | 1,156.3 | 0.3151 |  | no |
| 4 | Lancashire | 2016 | 3,641 | 1,139.5 | 0.3130 | -0.7% | no |
| 4 | Lancashire | 2017 | 3,319 | 1,042.6 | 0.3141 | 0.4% | no |
| 4 | Lancashire | 2018 | 3,346 | 1,056.5 | 0.3158 | 0.5% | no |
| 4 | Lancashire | 2019 | 2,929 | 908.6 | 0.3102 | -1.8% | no |
| 4 | Lancashire | 2020 | 2,344 | 703.0 | 0.2999 | -3.3% | no |
| 4 | Lancashire | 2021 | 2,708 | 867.0 | 0.3202 | 6.8% | no |
| 4 | Lancashire | 2022 | 2,755 | 961.0 | 0.3488 | 9.0% | no |
| 4 | Lancashire | 2023 | 2,756 | 903.0 | 0.3276 | -6.1% | no |
| 4 | Lancashire | 2024 | 2,730 | 876.0 | 0.3209 | -2.1% | no |
| 5 | Merseyside | 2015 | 2,689 | 720.3 | 0.2679 |  | no |
| 5 | Merseyside | 2016 | 2,483 | 717.9 | 0.2891 | 7.9% | no |
| 5 | Merseyside | 2017 | 2,227 | 677.5 | 0.3042 | 5.2% | no |
| 5 | Merseyside | 2018 | 2,276 | 614.0 | 0.2698 | -11.3% | no |
| 5 | Merseyside | 2019 | 2,133 | 567.9 | 0.2663 | -1.3% | no |
| 5 | Merseyside | 2020 | 1,700 | 460.1 | 0.2706 | 1.6% | no |
| 5 | Merseyside | 2021 | 1,981 | 563.5 | 0.2845 | 5.1% | no |
| 5 | Merseyside | 2022 | 2,241 | 608.2 | 0.2714 | -4.6% | no |
| 5 | Merseyside | 2023 | 2,115 | 644.7 | 0.3048 | 12.3% | no |
| 5 | Merseyside | 2024 | 1,891 | 570.1 | 0.3015 | -1.1% | no |
| 6 | Greater Manchester | 2015 | 3,071 | 884.6 | 0.2880 |  | no |
| 6 | Greater Manchester | 2016 | 2,906 | 878.6 | 0.3023 | 5.0% | no |
| 6 | Greater Manchester | 2017 | 4,069 | 1,097.0 | 0.2696 | -10.8% | no |
| 6 | Greater Manchester | 2018 | 3,762 | 1,042.6 | 0.2772 | 2.8% | no |
| 6 | Greater Manchester | 2019 | 3,620 | 962.7 | 0.2659 | -4.0% | no |
| 6 | Greater Manchester | 2020 | 2,398 | 691.8 | 0.2885 | 8.5% | no |
| 6 | Greater Manchester | 2021 | 3,003 | 768.3 | 0.2558 | -11.3% | no |
| 6 | Greater Manchester | 2022 | 2,803 | 778.9 | 0.2779 | 8.6% | no |
| 6 | Greater Manchester | 2023 | 2,530 | 731.2 | 0.2890 | 4.0% | no |
| 6 | Greater Manchester | 2024 | 2,792 | 926.3 | 0.3318 | 14.8% | no |
| 7 | Cheshire | 2015 | 2,314 | 574.8 | 0.2484 |  | no |
| 7 | Cheshire | 2016 | 2,354 | 549.1 | 0.2332 | -6.1% | no |
| 7 | Cheshire | 2017 | 2,200 | 482.6 | 0.2193 | -6.0% | no |
| 7 | Cheshire | 2018 | 2,025 | 502.8 | 0.2483 | 13.2% | no |
| 7 | Cheshire | 2019 | 1,721 | 379.5 | 0.2205 | -11.2% | no |
| 7 | Cheshire | 2020 | 1,355 | 333.6 | 0.2462 | 11.6% | no |
| 7 | Cheshire | 2021 | 1,586 | 387.2 | 0.2441 | -0.8% | no |
| 7 | Cheshire | 2022 | 1,674 | 401.3 | 0.2398 | -1.8% | no |
| 7 | Cheshire | 2023 | 1,527 | 407.4 | 0.2668 | 11.3% | no |
| 7 | Cheshire | 2024 | 1,463 | 415.1 | 0.2837 | 6.3% | no |
| 11 | Durham | 2015 | 1,068 | 273.8 | 0.2564 |  | no |
| 11 | Durham | 2016 | 1,010 | 210.8 | 0.2088 | -18.6% | no |
| 11 | Durham | 2017 | 1,047 | 222.0 | 0.2120 | 1.6% | no |
| 11 | Durham | 2018 | 947 | 193.0 | 0.2038 | -3.9% | no |
| 11 | Durham | 2019 | 849 | 245.0 | 0.2886 | 41.6% | yes |
| 11 | Durham | 2020 | 599 | 170.0 | 0.2838 | -1.7% | no |
| 11 | Durham | 2021 | 630 | 204.1 | 0.3239 | 14.1% | no |
| 11 | Durham | 2022 | 619 | 225.0 | 0.3635 | 12.2% | no |
| 11 | Durham | 2023 | 571 | 214.0 | 0.3748 | 3.1% | no |
| 11 | Durham | 2024 | 570 | 221.0 | 0.3877 | 3.5% | no |
| 12 | North Yorkshire | 2015 | 2,035 | 567.1 | 0.2787 |  | no |
| 12 | North Yorkshire | 2016 | 2,015 | 570.2 | 0.2830 | 1.5% | no |
| 12 | North Yorkshire | 2017 | 1,840 | 523.7 | 0.2846 | 0.6% | no |
| 12 | North Yorkshire | 2018 | 1,588 | 458.2 | 0.2885 | 1.4% | no |
| 12 | North Yorkshire | 2019 | 1,348 | 424.1 | 0.3146 | 9.0% | no |
| 12 | North Yorkshire | 2020 | 1,148 | 330.9 | 0.2882 | -8.4% | no |
| 12 | North Yorkshire | 2021 | 1,290 | 367.5 | 0.2849 | -1.2% | no |
| 12 | North Yorkshire | 2022 | 1,151 | 332.9 | 0.2892 | 1.5% | no |
| 12 | North Yorkshire | 2023 | 1,409 | 460.7 | 0.3270 | 13.0% | no |
| 12 | North Yorkshire | 2024 | 1,330 | 399.9 | 0.3007 | -8.0% | no |
| 13 | West Yorkshire | 2015 | 5,270 | 1,157.4 | 0.2196 |  | no |
| 13 | West Yorkshire | 2016 | 4,959 | 1,110.2 | 0.2239 | 1.9% | no |
| 13 | West Yorkshire | 2017 | 4,361 | 1,056.4 | 0.2422 | 8.2% | no |
| 13 | West Yorkshire | 2018 | 4,120 | 1,072.5 | 0.2603 | 7.5% | no |
| 13 | West Yorkshire | 2019 | 3,601 | 978.5 | 0.2717 | 4.4% | no |
| 13 | West Yorkshire | 2020 | 2,751 | 774.8 | 0.2816 | 3.6% | no |
| 13 | West Yorkshire | 2021 | 3,877 | 1,071.6 | 0.2764 | -1.9% | no |
| 13 | West Yorkshire | 2022 | 4,390 | 1,267.2 | 0.2887 | 4.4% | no |
| 13 | West Yorkshire | 2023 | 4,243 | 1,287.1 | 0.3033 | 5.1% | no |
| 13 | West Yorkshire | 2024 | 4,054 | 1,197.0 | 0.2953 | -2.7% | no |
| 14 | South Yorkshire | 2015 | 3,065 | 783.3 | 0.2556 |  | no |
| 14 | South Yorkshire | 2016 | 3,053 | 524.0 | 0.1716 | -32.8% | yes |
| 14 | South Yorkshire | 2017 | 2,792 | 728.0 | 0.2607 | 51.9% | yes |
| 14 | South Yorkshire | 2018 | 2,467 | 753.0 | 0.3052 | 17.1% | no |
| 14 | South Yorkshire | 2019 | 2,377 | 761.0 | 0.3202 | 4.9% | no |
| 14 | South Yorkshire | 2020 | 2,018 | 614.1 | 0.3043 | -5.0% | no |
| 14 | South Yorkshire | 2021 | 2,061 | 630.4 | 0.3059 | 0.5% | no |
| 14 | South Yorkshire | 2022 | 2,037 | 720.0 | 0.3535 | 15.6% | no |
| 14 | South Yorkshire | 2023 | 2,186 | 737.0 | 0.3371 | -4.6% | no |
| 14 | South Yorkshire | 2024 | 2,105 | 702.0 | 0.3335 | -1.1% | no |
| 16 | Humberside | 2015 | 2,389 | 522.9 | 0.2189 |  | no |
| 16 | Humberside | 2016 | 2,378 | 429.0 | 0.1804 | -17.6% | no |
| 16 | Humberside | 2017 | 2,324 | 492.0 | 0.2117 | 17.4% | no |
| 16 | Humberside | 2018 | 2,292 | 582.0 | 0.2539 | 19.9% | no |
| 16 | Humberside | 2019 | 2,308 | 441.1 | 0.1911 | -24.7% | yes |
| 16 | Humberside | 2020 | 1,708 | 360.0 | 0.2108 | 10.3% | no |
| 16 | Humberside | 2021 | 1,821 | 434.0 | 0.2383 | 13.1% | no |
| 16 | Humberside | 2022 | 1,912 | 464.2 | 0.2428 | 1.9% | no |
| 16 | Humberside | 2023 | 1,975 | 451.0 | 0.2284 | -5.9% | no |
| 16 | Humberside | 2024 | 1,896 | 496.0 | 0.2616 | 14.6% | no |
| 17 | Cleveland | 2015 | 941 | 250.1 | 0.2658 |  | no |
| 17 | Cleveland | 2016 | 775 | 196.6 | 0.2537 | -4.6% | no |
| 17 | Cleveland | 2017 | 679 | 187.6 | 0.2762 | 8.9% | no |
| 17 | Cleveland | 2018 | 606 | 169.7 | 0.2800 | 1.4% | no |
| 17 | Cleveland | 2019 | 658 | 202.7 | 0.3080 | 10.0% | no |
| 17 | Cleveland | 2020 | 568 | 160.8 | 0.2831 | -8.1% | no |
| 17 | Cleveland | 2021 | 622 | 192.2 | 0.3091 | 9.2% | no |
| 17 | Cleveland | 2022 | 672 | 234.6 | 0.3491 | 12.9% | no |
| 17 | Cleveland | 2023 | 606 | 195.6 | 0.3228 | -7.5% | no |
| 17 | Cleveland | 2024 | 500 | 152.5 | 0.3050 | -5.5% | no |
| 20 | West Midlands | 2015 | 6,082 | 908.3 | 0.1493 |  | no |
| 20 | West Midlands | 2016 | 5,861 | 972.0 | 0.1658 | 11.0% | no |
| 20 | West Midlands | 2017 | 5,639 | 912.0 | 0.1617 | -2.5% | no |
| 20 | West Midlands | 2018 | 5,475 | 928.0 | 0.1695 | 4.8% | no |
| 20 | West Midlands | 2019 | 5,415 | 888.0 | 0.1640 | -3.3% | no |
| 20 | West Midlands | 2020 | 3,930 | 732.0 | 0.1863 | 13.6% | no |
| 20 | West Midlands | 2021 | 4,679 | 821.0 | 0.1755 | -5.8% | no |
| 20 | West Midlands | 2022 | 4,943 | 915.0 | 0.1851 | 5.5% | no |
| 20 | West Midlands | 2023 | 4,687 | 976.0 | 0.2082 | 12.5% | no |
| 20 | West Midlands | 2024 | 4,621 | 986.0 | 0.2134 | 2.5% | no |
| 21 | Staffordshire | 2015 | 2,583 | 331.6 | 0.1284 |  | no |
| 21 | Staffordshire | 2016 | 2,535 | 319.1 | 0.1259 | -2.0% | no |
| 21 | Staffordshire | 2017 | 1,790 | 247.2 | 0.1381 | 9.7% | no |
| 21 | Staffordshire | 2018 | 1,376 | 225.0 | 0.1635 | 18.4% | no |
| 21 | Staffordshire | 2019 | 1,309 | 245.7 | 0.1877 | 14.8% | no |
| 21 | Staffordshire | 2020 | 879 | 146.1 | 0.1662 | -11.5% | no |
| 21 | Staffordshire | 2021 | 819 | 209.3 | 0.2555 | 53.7% | yes |
| 21 | Staffordshire | 2022 | 506 | 194.0 | 0.3834 | 50.0% | yes |
| 21 | Staffordshire | 2023 | 883 | 268.1 | 0.3037 | -20.8% | yes |
| 21 | Staffordshire | 2024 | 1,493 | 354.0 | 0.2371 | -21.9% | yes |
| 22 | West Mercia | 2015 | 2,295 | 543.4 | 0.2368 |  | no |
| 22 | West Mercia | 2016 | 2,296 | 487.0 | 0.2121 | -10.4% | no |
| 22 | West Mercia | 2017 | 2,119 | 477.0 | 0.2251 | 6.1% | no |
| 22 | West Mercia | 2018 | 1,785 | 443.0 | 0.2482 | 10.2% | no |
| 22 | West Mercia | 2019 | 1,876 | 445.0 | 0.2372 | -4.4% | no |
| 22 | West Mercia | 2020 | 1,444 | 380.0 | 0.2632 | 10.9% | no |
| 22 | West Mercia | 2021 | 1,595 | 475.2 | 0.2980 | 13.2% | no |
| 22 | West Mercia | 2022 | 1,657 | 481.1 | 0.2903 | -2.6% | no |
| 22 | West Mercia | 2023 | 1,448 | 440.0 | 0.3039 | 4.7% | no |
| 22 | West Mercia | 2024 | 1,537 | 491.0 | 0.3195 | 5.1% | no |
| 23 | Warwickshire | 2015 | 1,499 | 339.7 | 0.2266 |  | no |
| 23 | Warwickshire | 2016 | 1,453 | 332.1 | 0.2285 | 0.8% | no |
| 23 | Warwickshire | 2017 | 1,367 | 303.0 | 0.2217 | -3.0% | no |
| 23 | Warwickshire | 2018 | 1,212 | 314.0 | 0.2591 | 16.9% | no |
| 23 | Warwickshire | 2019 | 1,107 | 274.0 | 0.2475 | -4.5% | no |
| 23 | Warwickshire | 2020 | 855 | 223.0 | 0.2608 | 5.4% | no |
| 23 | Warwickshire | 2021 | 856 | 211.0 | 0.2465 | -5.5% | no |
| 23 | Warwickshire | 2022 | 865 | 234.0 | 0.2705 | 9.7% | no |
| 23 | Warwickshire | 2023 | 993 | 253.2 | 0.2550 | -5.7% | no |
| 23 | Warwickshire | 2024 | 1,092 | 288.0 | 0.2638 | 3.4% | no |
| 30 | Derbyshire | 2015 | 2,142 | 491.1 | 0.2293 |  | no |
| 30 | Derbyshire | 2016 | 1,910 | 458.0 | 0.2398 | 4.6% | no |
| 30 | Derbyshire | 2017 | 1,636 | 433.8 | 0.2651 | 10.6% | no |
| 30 | Derbyshire | 2018 | 1,653 | 455.6 | 0.2756 | 4.0% | no |
| 30 | Derbyshire | 2019 | 1,701 | 476.6 | 0.2802 | 1.7% | no |
| 30 | Derbyshire | 2020 | 1,458 | 368.2 | 0.2526 | -9.9% | no |
| 30 | Derbyshire | 2021 | 1,781 | 446.1 | 0.2505 | -0.8% | no |
| 30 | Derbyshire | 2022 | 1,970 | 546.9 | 0.2776 | 10.9% | no |
| 30 | Derbyshire | 2023 | 1,764 | 562.5 | 0.3189 | 14.9% | no |
| 30 | Derbyshire | 2024 | 1,650 | 600.9 | 0.3642 | 14.2% | no |
| 31 | Nottinghamshire | 2015 | 2,748 | 617.8 | 0.2248 |  | no |
| 31 | Nottinghamshire | 2016 | 2,581 | 614.1 | 0.2379 | 5.8% | no |
| 31 | Nottinghamshire | 2017 | 2,489 | 609.0 | 0.2447 | 2.8% | no |
| 31 | Nottinghamshire | 2018 | 2,428 | 591.2 | 0.2435 | -0.5% | no |
| 31 | Nottinghamshire | 2019 | 2,347 | 623.9 | 0.2658 | 9.2% | no |
| 31 | Nottinghamshire | 2020 | 1,673 | 476.1 | 0.2846 | 7.1% | no |
| 31 | Nottinghamshire | 2021 | 1,857 | 524.2 | 0.2823 | -0.8% | no |
| 31 | Nottinghamshire | 2022 | 1,889 | 493.0 | 0.2610 | -7.6% | no |
| 31 | Nottinghamshire | 2023 | 2,020 | 531.1 | 0.2629 | 0.7% | no |
| 31 | Nottinghamshire | 2024 | 2,066 | 518.0 | 0.2507 | -4.6% | no |
| 32 | Lincolnshire | 2015 | 2,129 | 423.1 | 0.1987 |  | no |
| 32 | Lincolnshire | 2016 | 1,973 | 502.8 | 0.2549 | 28.2% | yes |
| 32 | Lincolnshire | 2017 | 1,902 | 608.9 | 0.3201 | 25.6% | yes |
| 32 | Lincolnshire | 2018 | 1,869 | 563.3 | 0.3014 | -5.9% | no |
| 32 | Lincolnshire | 2019 | 1,880 | 578.6 | 0.3078 | 2.1% | no |
| 32 | Lincolnshire | 2020 | 1,390 | 472.3 | 0.3398 | 10.4% | no |
| 32 | Lincolnshire | 2021 | 1,520 | 511.4 | 0.3365 | -1.0% | no |
| 32 | Lincolnshire | 2022 | 1,595 | 493.2 | 0.3092 | -8.1% | no |
| 32 | Lincolnshire | 2023 | 1,713 | 511.6 | 0.2986 | -3.4% | no |
| 32 | Lincolnshire | 2024 | 1,720 | 504.2 | 0.2932 | -1.8% | no |
| 33 | Leicestershire | 2015 | 2,248 | 398.5 | 0.1773 |  | no |
| 33 | Leicestershire | 2016 | 2,172 | 362.1 | 0.1667 | -6.0% | no |
| 33 | Leicestershire | 2017 | 1,623 | 311.8 | 0.1921 | 15.2% | no |
| 33 | Leicestershire | 2018 | 1,584 | 389.8 | 0.2461 | 28.1% | yes |
| 33 | Leicestershire | 2019 | 1,315 | 315.5 | 0.2399 | -2.5% | no |
| 33 | Leicestershire | 2020 | 1,133 | 319.5 | 0.2820 | 17.5% | no |
| 33 | Leicestershire | 2021 | 1,128 | 330.5 | 0.2930 | 3.9% | no |
| 33 | Leicestershire | 2022 | 1,076 | 356.3 | 0.3311 | 13.0% | no |
| 33 | Leicestershire | 2023 | 1,221 | 360.0 | 0.2949 | -11.0% | no |
| 33 | Leicestershire | 2024 | 1,203 | 357.0 | 0.2968 | 0.6% | no |
| 34 | Northamptonshire | 2015 | 1,321 | 379.6 | 0.2874 |  | no |
| 34 | Northamptonshire | 2016 | 1,202 | 345.5 | 0.2874 | 0.0% | no |
| 34 | Northamptonshire | 2017 | 1,068 | 321.8 | 0.3013 | 4.8% | no |
| 34 | Northamptonshire | 2018 | 1,040 | 316.6 | 0.3044 | 1.0% | no |
| 34 | Northamptonshire | 2019 | 1,111 | 373.2 | 0.3359 | 10.3% | no |
| 34 | Northamptonshire | 2020 | 881 | 294.8 | 0.3346 | -0.4% | no |
| 34 | Northamptonshire | 2021 | 1,026 | 344.4 | 0.3356 | 0.3% | no |
| 34 | Northamptonshire | 2022 | 1,228 | 403.5 | 0.3286 | -2.1% | no |
| 34 | Northamptonshire | 2023 | 1,232 | 342.7 | 0.2782 | -15.3% | no |
| 34 | Northamptonshire | 2024 | 1,239 | 349.6 | 0.2821 | 1.4% | no |
| 35 | Cambridgeshire | 2015 | 1,967 | 397.8 | 0.2022 |  | no |
| 35 | Cambridgeshire | 2016 | 2,151 | 387.4 | 0.1801 | -11.0% | no |
| 35 | Cambridgeshire | 2017 | 1,995 | 413.0 | 0.2070 | 15.0% | no |
| 35 | Cambridgeshire | 2018 | 1,786 | 375.0 | 0.2100 | 1.4% | no |
| 35 | Cambridgeshire | 2019 | 1,694 | 388.0 | 0.2290 | 9.1% | no |
| 35 | Cambridgeshire | 2020 | 1,245 | 345.0 | 0.2771 | 21.0% | yes |
| 35 | Cambridgeshire | 2021 | 1,334 | 386.0 | 0.2894 | 4.4% | no |
| 35 | Cambridgeshire | 2022 | 1,484 | 413.0 | 0.2783 | -3.8% | no |
| 35 | Cambridgeshire | 2023 | 1,517 | 378.1 | 0.2493 | -10.4% | no |
| 35 | Cambridgeshire | 2024 | 1,371 | 337.0 | 0.2458 | -1.4% | no |
| 36 | Norfolk | 2015 | 1,747 | 392.1 | 0.2245 |  | no |
| 36 | Norfolk | 2016 | 1,825 | 357.2 | 0.1957 | -12.8% | no |
| 36 | Norfolk | 2017 | 1,733 | 367.0 | 0.2118 | 8.2% | no |
| 36 | Norfolk | 2018 | 1,746 | 398.0 | 0.2279 | 7.6% | no |
| 36 | Norfolk | 2019 | 1,648 | 441.0 | 0.2676 | 17.4% | no |
| 36 | Norfolk | 2020 | 1,322 | 349.0 | 0.2640 | -1.3% | no |
| 36 | Norfolk | 2021 | 1,374 | 354.0 | 0.2576 | -2.4% | no |
| 36 | Norfolk | 2022 | 1,530 | 420.0 | 0.2745 | 6.5% | no |
| 36 | Norfolk | 2023 | 1,351 | 412.0 | 0.3050 | 11.1% | no |
| 36 | Norfolk | 2024 | 1,624 | 500.0 | 0.3079 | 1.0% | no |
| 37 | Suffolk | 2015 | 1,483 | 249.4 | 0.1682 |  | no |
| 37 | Suffolk | 2016 | 1,550 | 262.2 | 0.1692 | 0.6% | no |
| 37 | Suffolk | 2017 | 1,543 | 251.0 | 0.1627 | -3.8% | no |
| 37 | Suffolk | 2018 | 1,441 | 258.0 | 0.1790 | 10.1% | no |
| 37 | Suffolk | 2019 | 1,360 | 317.0 | 0.2331 | 30.2% | yes |
| 37 | Suffolk | 2020 | 995 | 245.0 | 0.2462 | 5.6% | no |
| 37 | Suffolk | 2021 | 1,065 | 269.0 | 0.2526 | 2.6% | no |
| 37 | Suffolk | 2022 | 1,163 | 279.0 | 0.2399 | -5.0% | no |
| 37 | Suffolk | 2023 | 930 | 264.0 | 0.2839 | 18.3% | no |
| 37 | Suffolk | 2024 | 1,140 | 321.0 | 0.2816 | -0.8% | no |

## Plots

![Adjusted expected KSI by force and year](reports/figures/ksi_reporting_consistency_adjusted_expected_count.png)

![Adjusted expected KSI-to-all-injury ratio by force and year](reports/figures/ksi_reporting_consistency_adjusted_ratio.png)

## Flagged Force/Year Breaks

| police_force | force_name | year | all_injury_count | adjusted_expected_ksi | adjusted_expected_ksi_to_all_injury_ratio | adjusted_expected_ksi_change | ratio_yoy_pct_change | practical_sensitivity_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | Cumbria | 2016 | 1,247 | 242.0 | 0.1941 | -66.9 | -20.5% | yes |
| 14 | South Yorkshire | 2016 | 3,053 | 524.0 | 0.1716 | -259.3 | -32.8% | yes |
| 32 | Lincolnshire | 2016 | 1,973 | 502.8 | 0.2549 | +79.7 | 28.2% | yes |
| 14 | South Yorkshire | 2017 | 2,792 | 728.0 | 0.2607 | +204.0 | 51.9% | yes |
| 32 | Lincolnshire | 2017 | 1,902 | 608.9 | 0.3201 | +106.0 | 25.6% | yes |
| 33 | Leicestershire | 2018 | 1,584 | 389.8 | 0.2461 | +78.0 | 28.1% | yes |
| 3 | Cumbria | 2019 | 1,011 | 282.0 | 0.2789 | +4.0 | 21.0% | no |
| 11 | Durham | 2019 | 849 | 245.0 | 0.2886 | +52.0 | 41.6% | yes |
| 16 | Humberside | 2019 | 2,308 | 441.1 | 0.1911 | -140.9 | -24.7% | yes |
| 37 | Suffolk | 2019 | 1,360 | 317.0 | 0.2331 | +59.0 | 30.2% | yes |
| 35 | Cambridgeshire | 2020 | 1,245 | 345.0 | 0.2771 | -43.0 | 21.0% | yes |
| 21 | Staffordshire | 2021 | 819 | 209.3 | 0.2555 | +63.2 | 53.7% | yes |
| 21 | Staffordshire | 2022 | 506 | 194.0 | 0.3834 | -15.3 | 50.0% | no |
| 21 | Staffordshire | 2023 | 883 | 268.1 | 0.3037 | +74.1 | -20.8% | yes |
| 21 | Staffordshire | 2024 | 1,493 | 354.0 | 0.2371 | +85.9 | -21.9% | yes |

## Window Sensitivity

The pre-registered flag is the +/-20% year-on-year ratio-change rule. The practical-sensitivity flag mirrors the original extra check using an absolute adjusted expected-KSI change of at least 25.

| window | number_of_forces | number_of_force_year_rows | all_injury_count | adjusted_expected_ksi | overall_adjusted_ratio | pre_registered_flagged_force_year_rows | forces_with_any_pre_registered_flagged_years | practical_sensitivity_flagged_force_year_rows | forces_with_any_practical_sensitivity_flagged_years |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2015-2024 | 23 | 230 | 450,991 | 114,817.3 | 0.2546 | 15 | 3, 11, 14, 16, 21, 32, 33, 35, 37 | 13 | 3, 11, 14, 16, 21, 32, 33, 35, 37 |
| 2017-2024 | 23 | 184 | 340,639 | 90,178.2 | 0.2647 | 12 | 3, 11, 14, 16, 21, 32, 33, 35, 37 | 10 | 11, 14, 16, 21, 32, 33, 35, 37 |
| 2017-2023 | 23 | 161 | 299,777 | 78,377.6 | 0.2615 | 11 | 3, 11, 14, 16, 21, 32, 33, 35, 37 | 9 | 11, 14, 16, 21, 32, 33, 35, 37 |
| 2019-2023 | 23 | 115 | 200,729 | 54,377.1 | 0.2709 | 8 | 3, 11, 16, 21, 35, 37 | 6 | 11, 16, 21, 35, 37 |

## Comparison With Original Part A

| target | total_ksi_metric | overall_ratio | pre_registered_flagged_force_year_rows | practical_sensitivity_flagged_force_year_rows | least_disrupted_tested_window |
| --- | --- | --- | --- | --- | --- |
| unadjusted recorded KSI | 99,559.0 | 0.2208 | 28 | 26 | 2019-2023 |
| adjusted expected KSI | 114,817.3 | 0.2546 | 15 | 13 | 2019-2023 |

The adjusted target materially reduces the original recorded-KSI flag count, but it does not clear the pre-registered Part A consistency gate. The decision still follows the pre-registered Part A logic, not an after-the-fact threshold.

## Methodological Caveats

- Adjusted expected KSI is an expected-count target, not an observed integer count.
- The adjusted severity columns are suitable for aggregate force/year checks; they are not deterministic record-level labels.
- Passing adjusted Part A would not automatically justify full KSI modelling. It would only clear the reporting-consistency gate for a future Part B.
- EB shrinkage is not a drop-in target swap, because the current EB layer assumes observed integer counts.
- If Part B proceeds later, it must specify whether EB is re-derived for expected-count targets or deferred.

## Verdict

**Headline adjusted Part A verdict:** keep KSI parked.

**Operational decision:** adjusted Part A still shows heterogeneous force/year breaks, so Part B should not be run as a defensible national-scope KSI modelling stage.

**Parking status:** this diagnostic does not unpark the KSI atlas or modify the decision register.
