# Speed Limit Effective Verification

- Updated parquet shape: `2,167,557 x 15`
- `speed_limit_mph_effective` coverage: `1,978,391 / 2,167,557` (91.27%)
- Raw `speed_limit_mph` unchanged: `True`
- `ruc_class` nulls before/after: `335,692` / `335,692`
- `ruc_urban_rural` nulls before/after: `335,692` / `335,692`
- `pop_density_per_km2` nulls before/after: `335,692` / `335,692`

## speed_limit_source counts

| speed_limit_source   |   n_links |
|:---------------------|----------:|
| osm                  |   1223082 |
| lookup_minor_urban   |    485384 |
| null_no_ruc          |    189166 |
| lookup_minor_rural   |    166583 |
| lookup_a_road_single |     51532 |
| lookup_b_road_urban  |     20253 |
| lookup_b_road_rural  |     11382 |
| lookup_a_road_dual   |     11360 |
| lookup_a_road_trunk  |      6612 |
| lookup_motorway      |      2203 |

## road_classification x ruc_urban_rural x speed_limit_mph_effective

| road_classification   | ruc_urban_rural   | speed_limit_mph_effective   |   n_links |
|:----------------------|:------------------|:----------------------------|----------:|
| A Road                | Rural             | 10                          |         1 |
| A Road                | Rural             | 15                          |         8 |
| A Road                | Rural             | 17                          |         6 |
| A Road                | Rural             | 19                          |        32 |
| A Road                | Rural             | 20                          |       219 |
| A Road                | Rural             | 21                          |        72 |
| A Road                | Rural             | 22                          |        95 |
| A Road                | Rural             | 23                          |        66 |
| A Road                | Rural             | 24                          |        12 |
| A Road                | Rural             | 25                          |        67 |
| A Road                | Rural             | 26                          |        42 |
| A Road                | Rural             | 27                          |        14 |
| A Road                | Rural             | 28                          |        96 |
| A Road                | Rural             | 29                          |       106 |
| A Road                | Rural             | 30                          |      5075 |
| A Road                | Rural             | 31                          |         2 |
| A Road                | Rural             | 32                          |         1 |
| A Road                | Rural             | 33                          |         3 |
| A Road                | Rural             | 34                          |        51 |
| A Road                | Rural             | 35                          |       289 |
| A Road                | Rural             | 36                          |       174 |
| A Road                | Rural             | 37                          |       117 |
| A Road                | Rural             | 38                          |        49 |
| A Road                | Rural             | 39                          |        87 |
| A Road                | Rural             | 40                          |      2358 |
| A Road                | Rural             | 41                          |       147 |
| A Road                | Rural             | 42                          |       315 |
| A Road                | Rural             | 43                          |       104 |
| A Road                | Rural             | 45                          |       342 |
| A Road                | Rural             | 46                          |        31 |
| A Road                | Rural             | 47                          |         5 |
| A Road                | Rural             | 48                          |        80 |
| A Road                | Rural             | 49                          |         1 |
| A Road                | Rural             | 50                          |      2144 |
| A Road                | Rural             | 51                          |        28 |
| A Road                | Rural             | 53                          |         3 |
| A Road                | Rural             | 54                          |         6 |
| A Road                | Rural             | 55                          |       136 |
| A Road                | Rural             | 56                          |         9 |
| A Road                | Rural             | 57                          |        10 |
| A Road                | Rural             | 58                          |        14 |
| A Road                | Rural             | 59                          |        25 |
| A Road                | Rural             | 60                          |     15317 |
| A Road                | Rural             | 62                          |         6 |
| A Road                | Rural             | 63                          |        17 |
| A Road                | Rural             | 64                          |         2 |
| A Road                | Rural             | 65                          |        19 |
| A Road                | Rural             | 67                          |         1 |
| A Road                | Rural             | 70                          |      4432 |
| A Road                | Rural             | 90                          |         2 |
| A Road                | Rural             | 110                         |         2 |
| A Road                | Urban             | 10                          |         7 |
| A Road                | Urban             | 15                          |        30 |
| A Road                | Urban             | 17                          |       116 |
| A Road                | Urban             | 18                          |         1 |
| A Road                | Urban             | 19                          |       156 |
| A Road                | Urban             | 20                          |      1072 |
| A Road                | Urban             | 21                          |       703 |
| A Road                | Urban             | 22                          |       497 |
| A Road                | Urban             | 23                          |       280 |
| A Road                | Urban             | 24                          |       502 |
| A Road                | Urban             | 25                          |       242 |
| A Road                | Urban             | 26                          |       182 |
| A Road                | Urban             | 27                          |        74 |
| A Road                | Urban             | 28                          |       519 |
| A Road                | Urban             | 29                          |       470 |
| A Road                | Urban             | 30                          |     28066 |
| A Road                | Urban             | 31                          |       900 |
| A Road                | Urban             | 32                          |        11 |
| A Road                | Urban             | 33                          |       161 |
| A Road                | Urban             | 34                          |       309 |
| A Road                | Urban             | 35                          |       940 |
| A Road                | Urban             | 36                          |       261 |
| A Road                | Urban             | 37                          |       820 |
| A Road                | Urban             | 38                          |       215 |
| A Road                | Urban             | 39                          |       188 |
| A Road                | Urban             | 40                          |     10458 |
| A Road                | Urban             | 41                          |       484 |
| A Road                | Urban             | 42                          |       427 |
| A Road                | Urban             | 43                          |       111 |
| A Road                | Urban             | 45                          |       278 |
| A Road                | Urban             | 46                          |        93 |
| A Road                | Urban             | 47                          |        18 |
| A Road                | Urban             | 48                          |       126 |
| A Road                | Urban             | 49                          |         4 |
| A Road                | Urban             | 50                          |      2977 |
| A Road                | Urban             | 51                          |       100 |
| A Road                | Urban             | 52                          |        26 |
| A Road                | Urban             | 53                          |         7 |
| A Road                | Urban             | 54                          |        20 |
| A Road                | Urban             | 55                          |       255 |
| A Road                | Urban             | 56                          |        12 |
| A Road                | Urban             | 57                          |        12 |
| A Road                | Urban             | 58                          |         6 |
| A Road                | Urban             | 59                          |         9 |
| A Road                | Urban             | 60                          |     35638 |
| A Road                | Urban             | 61                          |         6 |
| A Road                | Urban             | 62                          |         4 |
| A Road                | Urban             | 63                          |         3 |
| A Road                | Urban             | 65                          |        95 |
| A Road                | Urban             | 67                          |         7 |
| A Road                | Urban             | 69                          |         1 |
| A Road                | Urban             | 70                          |     13522 |
| A Road                | Urban             | 75                          |         8 |
| A Road                | Urban             | 77                          |         1 |
| A Road                | Urban             | 80                          |         5 |
| A Road                | Urban             | 83                          |         1 |
| A Road                | Urban             | 85                          |         1 |
| A Road                | Urban             | 87                          |         1 |
| A Road                | Urban             | 90                          |         1 |
| A Road                | Urban             | 95                          |         2 |
| A Road                | Urban             | 100                         |         6 |
| A Road                | Urban             | 110                         |         3 |
| A Road                | Urban             | 115                         |         1 |
| A Road                | <NA>              | 15                          |         2 |
| A Road                | <NA>              | 17                          |         5 |
| A Road                | <NA>              | 19                          |        20 |
| A Road                | <NA>              | 20                          |        38 |
| A Road                | <NA>              | 21                          |        18 |
| A Road                | <NA>              | 22                          |        56 |
| A Road                | <NA>              | 23                          |        13 |
| A Road                | <NA>              | 24                          |        11 |
| A Road                | <NA>              | 25                          |        31 |
| A Road                | <NA>              | 26                          |        23 |
| A Road                | <NA>              | 27                          |         8 |
| A Road                | <NA>              | 28                          |        36 |
| A Road                | <NA>              | 29                          |        42 |
| A Road                | <NA>              | 30                          |       917 |
| A Road                | <NA>              | 31                          |         2 |
| A Road                | <NA>              | 33                          |        22 |
| A Road                | <NA>              | 34                          |        18 |
| A Road                | <NA>              | 35                          |        88 |
| A Road                | <NA>              | 36                          |        62 |
| A Road                | <NA>              | 37                          |        17 |
| A Road                | <NA>              | 38                          |         1 |
| A Road                | <NA>              | 39                          |        13 |
| A Road                | <NA>              | 40                          |       570 |
| A Road                | <NA>              | 41                          |        64 |
| A Road                | <NA>              | 42                          |       131 |
| A Road                | <NA>              | 43                          |        54 |
| A Road                | <NA>              | 45                          |       148 |
| A Road                | <NA>              | 46                          |        16 |
| A Road                | <NA>              | 47                          |         5 |
| A Road                | <NA>              | 48                          |        50 |
| A Road                | <NA>              | 50                          |      1447 |
| A Road                | <NA>              | 51                          |        29 |
| A Road                | <NA>              | 52                          |         8 |
| A Road                | <NA>              | 53                          |         1 |
| A Road                | <NA>              | 54                          |         7 |
| A Road                | <NA>              | 55                          |        76 |
| A Road                | <NA>              | 56                          |         8 |
| A Road                | <NA>              | 57                          |         1 |
| A Road                | <NA>              | 58                          |         6 |
| A Road                | <NA>              | 59                          |         5 |
| A Road                | <NA>              | 60                          |     13271 |
| A Road                | <NA>              | 62                          |         4 |
| A Road                | <NA>              | 63                          |         5 |
| A Road                | <NA>              | 64                          |         2 |
| A Road                | <NA>              | 65                          |        38 |
| A Road                | <NA>              | 68                          |         3 |
| A Road                | <NA>              | 70                          |      4454 |
| A Road                | <NA>              | 110                         |         1 |
| B Road                | Rural             | 15                          |         7 |
| B Road                | Rural             | 17                          |        13 |
| B Road                | Rural             | 18                          |         1 |
| B Road                | Rural             | 19                          |        10 |
| B Road                | Rural             | 20                          |       427 |
| B Road                | Rural             | 21                          |        44 |
| B Road                | Rural             | 22                          |        74 |
| B Road                | Rural             | 23                          |        37 |
| B Road                | Rural             | 24                          |         8 |
| B Road                | Rural             | 25                          |       100 |
| B Road                | Rural             | 26                          |        21 |
| B Road                | Rural             | 27                          |         6 |
| B Road                | Rural             | 28                          |        63 |
| B Road                | Rural             | 29                          |       121 |
| B Road                | Rural             | 30                          |      5940 |
| B Road                | Rural             | 31                          |         6 |
| B Road                | Rural             | 32                          |       166 |
| B Road                | Rural             | 33                          |         3 |
| B Road                | Rural             | 34                          |       233 |
| B Road                | Rural             | 35                          |       144 |
| B Road                | Rural             | 36                          |       151 |
| B Road                | Rural             | 37                          |       238 |
| B Road                | Rural             | 38                          |       737 |
| B Road                | Rural             | 39                          |       550 |
| B Road                | Rural             | 40                          |      1226 |
| B Road                | Rural             | 41                          |        15 |
| B Road                | Rural             | 42                          |       787 |
| B Road                | Rural             | 43                          |       123 |
| B Road                | Rural             | 44                          |       134 |
| B Road                | Rural             | 45                          |       294 |
| B Road                | Rural             | 46                          |         5 |
| B Road                | Rural             | 49                          |         1 |
| B Road                | Rural             | 50                          |       565 |
| B Road                | Rural             | 51                          |         1 |
| B Road                | Rural             | 52                          |         2 |
| B Road                | Rural             | 53                          |         1 |
| B Road                | Rural             | 55                          |        27 |
| B Road                | Rural             | 59                          |         2 |
| B Road                | Rural             | 60                          |     13451 |
| B Road                | Rural             | 63                          |         1 |
| B Road                | Rural             | 65                          |         1 |
| B Road                | Rural             | 70                          |        36 |
| B Road                | Rural             | 75                          |         1 |
| B Road                | Rural             | 80                          |         1 |
| B Road                | Rural             | 82                          |         1 |
| B Road                | Rural             | 110                         |         1 |
| B Road                | Urban             | 10                          |         4 |
| B Road                | Urban             | 12                          |         3 |
| B Road                | Urban             | 15                          |        14 |
| B Road                | Urban             | 16                          |         6 |
| B Road                | Urban             | 17                          |        84 |
| B Road                | Urban             | 19                          |        56 |
| B Road                | Urban             | 20                          |      1260 |
| B Road                | Urban             | 21                          |       293 |
| B Road                | Urban             | 22                          |       152 |
| B Road                | Urban             | 23                          |        77 |
| B Road                | Urban             | 24                          |       218 |
| B Road                | Urban             | 25                          |       196 |
| B Road                | Urban             | 26                          |        86 |
| B Road                | Urban             | 27                          |        13 |
| B Road                | Urban             | 28                          |       147 |
| B Road                | Urban             | 29                          |       222 |
| B Road                | Urban             | 30                          |     34832 |
| B Road                | Urban             | 31                          |       474 |
| B Road                | Urban             | 32                          |       356 |
| B Road                | Urban             | 33                          |        17 |
| B Road                | Urban             | 34                          |       350 |
| B Road                | Urban             | 35                          |       171 |
| B Road                | Urban             | 36                          |      1217 |
| B Road                | Urban             | 37                          |       192 |
| B Road                | Urban             | 38                          |       481 |
| B Road                | Urban             | 39                          |       707 |
| B Road                | Urban             | 40                          |      2351 |
| B Road                | Urban             | 41                          |        23 |
| B Road                | Urban             | 42                          |       532 |
| B Road                | Urban             | 43                          |        83 |
| B Road                | Urban             | 44                          |       109 |
| B Road                | Urban             | 45                          |       104 |
| B Road                | Urban             | 46                          |         1 |
| B Road                | Urban             | 47                          |         5 |
| B Road                | Urban             | 50                          |       357 |
| B Road                | Urban             | 51                          |         8 |
| B Road                | Urban             | 52                          |         5 |
| B Road                | Urban             | 53                          |         8 |
| B Road                | Urban             | 54                          |         1 |
| B Road                | Urban             | 55                          |        23 |
| B Road                | Urban             | 60                          |       770 |
| B Road                | Urban             | 65                          |         4 |
| B Road                | Urban             | 70                          |        71 |
| B Road                | Urban             | 75                          |         5 |
| B Road                | Urban             | 80                          |         2 |
| B Road                | Urban             | 85                          |         3 |
| B Road                | Urban             | 92                          |         1 |
| B Road                | Urban             | 100                         |         1 |
| B Road                | Urban             | 105                         |         1 |
| B Road                | Urban             | 110                         |         2 |
| B Road                | Urban             | 125                         |         1 |
| B Road                | <NA>              | 15                          |         1 |
| B Road                | <NA>              | 17                          |         1 |
| B Road                | <NA>              | 19                          |         4 |
| B Road                | <NA>              | 20                          |        29 |
| B Road                | <NA>              | 21                          |        20 |
| B Road                | <NA>              | 22                          |        27 |
| B Road                | <NA>              | 23                          |        21 |
| B Road                | <NA>              | 24                          |         6 |
| B Road                | <NA>              | 25                          |        16 |
| B Road                | <NA>              | 26                          |         5 |
| B Road                | <NA>              | 27                          |         5 |
| B Road                | <NA>              | 28                          |        13 |
| B Road                | <NA>              | 29                          |        21 |
| B Road                | <NA>              | 30                          |      1042 |
| B Road                | <NA>              | 32                          |         1 |
| B Road                | <NA>              | 33                          |         1 |
| B Road                | <NA>              | 34                          |       163 |
| B Road                | <NA>              | 35                          |        31 |
| B Road                | <NA>              | 36                          |        28 |
| B Road                | <NA>              | 37                          |       108 |
| B Road                | <NA>              | 38                          |       483 |
| B Road                | <NA>              | 39                          |       134 |
| B Road                | <NA>              | 40                          |       466 |
| B Road                | <NA>              | 41                          |         5 |
| B Road                | <NA>              | 42                          |       657 |
| B Road                | <NA>              | 43                          |       141 |
| B Road                | <NA>              | 44                          |        81 |
| B Road                | <NA>              | 45                          |       137 |
| B Road                | <NA>              | 50                          |       393 |
| B Road                | <NA>              | 52                          |         1 |
| B Road                | <NA>              | 53                          |         1 |
| B Road                | <NA>              | 55                          |        25 |
| B Road                | <NA>              | 58                          |         1 |
| B Road                | <NA>              | 60                          |      2463 |
| B Road                | <NA>              | 64                          |         1 |
| B Road                | <NA>              | 70                          |        24 |
| B Road                | <NA>              | <NA>                        |     10855 |
| Classified Unnumbered | Rural             | 15                          |        21 |
| Classified Unnumbered | Rural             | 17                          |        48 |
| Classified Unnumbered | Rural             | 19                          |        69 |
| Classified Unnumbered | Rural             | 20                          |      1010 |
| Classified Unnumbered | Rural             | 21                          |       132 |
| Classified Unnumbered | Rural             | 22                          |       299 |
| Classified Unnumbered | Rural             | 23                          |        87 |
| Classified Unnumbered | Rural             | 24                          |        25 |
| Classified Unnumbered | Rural             | 25                          |       373 |
| Classified Unnumbered | Rural             | 26                          |       234 |
| Classified Unnumbered | Rural             | 27                          |       102 |
| Classified Unnumbered | Rural             | 28                          |       435 |
| Classified Unnumbered | Rural             | 29                          |       458 |
| Classified Unnumbered | Rural             | 30                          |     12222 |
| Classified Unnumbered | Rural             | 31                          |       741 |
| Classified Unnumbered | Rural             | 32                          |         1 |
| Classified Unnumbered | Rural             | 33                          |       711 |
| Classified Unnumbered | Rural             | 34                          |      1844 |
| Classified Unnumbered | Rural             | 35                          |      3110 |
| Classified Unnumbered | Rural             | 36                          |      1713 |
| Classified Unnumbered | Rural             | 37                          |       881 |
| Classified Unnumbered | Rural             | 38                          |        92 |
| Classified Unnumbered | Rural             | 39                          |      1056 |
| Classified Unnumbered | Rural             | 40                          |      2200 |
| Classified Unnumbered | Rural             | 41                          |      1718 |
| Classified Unnumbered | Rural             | 42                          |       526 |
| Classified Unnumbered | Rural             | 43                          |       393 |
| Classified Unnumbered | Rural             | 45                          |       819 |
| Classified Unnumbered | Rural             | 46                          |       633 |
| Classified Unnumbered | Rural             | 47                          |         5 |
| Classified Unnumbered | Rural             | 48                          |        10 |
| Classified Unnumbered | Rural             | 50                          |       412 |
| Classified Unnumbered | Rural             | 51                          |         1 |
| Classified Unnumbered | Rural             | 52                          |         5 |
| Classified Unnumbered | Rural             | 54                          |         1 |
| Classified Unnumbered | Rural             | 55                          |        34 |
| Classified Unnumbered | Rural             | 56                          |         3 |
| Classified Unnumbered | Rural             | 57                          |         1 |
| Classified Unnumbered | Rural             | 58                          |         3 |
| Classified Unnumbered | Rural             | 59                          |         2 |
| Classified Unnumbered | Rural             | 60                          |     32470 |
| Classified Unnumbered | Rural             | 62                          |         1 |
| Classified Unnumbered | Rural             | 63                          |         1 |
| Classified Unnumbered | Rural             | 65                          |         4 |
| Classified Unnumbered | Rural             | 67                          |         1 |
| Classified Unnumbered | Rural             | 70                          |        47 |
| Classified Unnumbered | Rural             | 75                          |         5 |
| Classified Unnumbered | Rural             | 80                          |         2 |
| Classified Unnumbered | Rural             | 90                          |         7 |
| Classified Unnumbered | Rural             | 95                          |         1 |
| Classified Unnumbered | Rural             | 100                         |         1 |
| Classified Unnumbered | Rural             | 105                         |         1 |
| Classified Unnumbered | Rural             | 110                         |         4 |
| Classified Unnumbered | Rural             | 125                         |         2 |
| Classified Unnumbered | Urban             | 10                          |         5 |
| Classified Unnumbered | Urban             | 15                          |        14 |
| Classified Unnumbered | Urban             | 17                          |        95 |
| Classified Unnumbered | Urban             | 18                          |         2 |
| Classified Unnumbered | Urban             | 19                          |        86 |
| Classified Unnumbered | Urban             | 20                          |      3810 |
| Classified Unnumbered | Urban             | 21                          |       412 |
| Classified Unnumbered | Urban             | 22                          |       661 |
| Classified Unnumbered | Urban             | 23                          |       109 |
| Classified Unnumbered | Urban             | 24                          |       183 |
| Classified Unnumbered | Urban             | 25                          |       697 |
| Classified Unnumbered | Urban             | 26                          |       446 |
| Classified Unnumbered | Urban             | 27                          |       169 |
| Classified Unnumbered | Urban             | 28                          |      2888 |
| Classified Unnumbered | Urban             | 29                          |       536 |
| Classified Unnumbered | Urban             | 30                          |     45763 |
| Classified Unnumbered | Urban             | 31                          |      1759 |
| Classified Unnumbered | Urban             | 32                          |        13 |
| Classified Unnumbered | Urban             | 33                          |       260 |
| Classified Unnumbered | Urban             | 34                          |      1255 |
| Classified Unnumbered | Urban             | 35                          |      1881 |
| Classified Unnumbered | Urban             | 36                          |      1283 |
| Classified Unnumbered | Urban             | 37                          |       515 |
| Classified Unnumbered | Urban             | 38                          |        43 |
| Classified Unnumbered | Urban             | 39                          |       329 |
| Classified Unnumbered | Urban             | 40                          |      2006 |
| Classified Unnumbered | Urban             | 41                          |       908 |
| Classified Unnumbered | Urban             | 42                          |        78 |
| Classified Unnumbered | Urban             | 43                          |        87 |
| Classified Unnumbered | Urban             | 44                          |         1 |
| Classified Unnumbered | Urban             | 45                          |       165 |
| Classified Unnumbered | Urban             | 46                          |       165 |
| Classified Unnumbered | Urban             | 47                          |         2 |
| Classified Unnumbered | Urban             | 48                          |         2 |
| Classified Unnumbered | Urban             | 50                          |       282 |
| Classified Unnumbered | Urban             | 51                          |        35 |
| Classified Unnumbered | Urban             | 52                          |         4 |
| Classified Unnumbered | Urban             | 54                          |        13 |
| Classified Unnumbered | Urban             | 55                          |        23 |
| Classified Unnumbered | Urban             | 57                          |         4 |
| Classified Unnumbered | Urban             | 58                          |         1 |
| Classified Unnumbered | Urban             | 60                          |      1229 |
| Classified Unnumbered | Urban             | 62                          |         3 |
| Classified Unnumbered | Urban             | 63                          |         1 |
| Classified Unnumbered | Urban             | 65                          |         1 |
| Classified Unnumbered | Urban             | 70                          |        52 |
| Classified Unnumbered | Urban             | 75                          |         1 |
| Classified Unnumbered | Urban             | 80                          |         6 |
| Classified Unnumbered | Urban             | 85                          |         1 |
| Classified Unnumbered | Urban             | 90                          |         1 |
| Classified Unnumbered | Urban             | 91                          |         1 |
| Classified Unnumbered | Urban             | 100                         |         1 |
| Classified Unnumbered | Urban             | 105                         |         2 |
| Classified Unnumbered | Urban             | 110                         |         1 |
| Classified Unnumbered | Urban             | 115                         |         1 |
| Classified Unnumbered | Urban             | 125                         |         2 |
| Classified Unnumbered | <NA>              | 15                          |        11 |
| Classified Unnumbered | <NA>              | 17                          |        16 |
| Classified Unnumbered | <NA>              | 19                          |        29 |
| Classified Unnumbered | <NA>              | 20                          |       104 |
| Classified Unnumbered | <NA>              | 21                          |        51 |
| Classified Unnumbered | <NA>              | 22                          |       155 |
| Classified Unnumbered | <NA>              | 23                          |        46 |
| Classified Unnumbered | <NA>              | 24                          |         8 |
| Classified Unnumbered | <NA>              | 25                          |       105 |
| Classified Unnumbered | <NA>              | 26                          |       152 |
| Classified Unnumbered | <NA>              | 27                          |        40 |
| Classified Unnumbered | <NA>              | 28                          |        70 |
| Classified Unnumbered | <NA>              | 29                          |       200 |
| Classified Unnumbered | <NA>              | 30                          |      3733 |
| Classified Unnumbered | <NA>              | 31                          |       246 |
| Classified Unnumbered | <NA>              | 32                          |         3 |
| Classified Unnumbered | <NA>              | 33                          |       464 |
| Classified Unnumbered | <NA>              | 34                          |      1630 |
| Classified Unnumbered | <NA>              | 35                          |      1830 |
| Classified Unnumbered | <NA>              | 36                          |      1229 |
| Classified Unnumbered | <NA>              | 37                          |       482 |
| Classified Unnumbered | <NA>              | 38                          |        79 |
| Classified Unnumbered | <NA>              | 39                          |      1170 |
| Classified Unnumbered | <NA>              | 40                          |      2105 |
| Classified Unnumbered | <NA>              | 41                          |      1554 |
| Classified Unnumbered | <NA>              | 42                          |       879 |
| Classified Unnumbered | <NA>              | 43                          |       751 |
| Classified Unnumbered | <NA>              | 45                          |       601 |
| Classified Unnumbered | <NA>              | 46                          |      1313 |
| Classified Unnumbered | <NA>              | 47                          |         2 |
| Classified Unnumbered | <NA>              | 48                          |         4 |
| Classified Unnumbered | <NA>              | 50                          |       282 |
| Classified Unnumbered | <NA>              | 52                          |         1 |
| Classified Unnumbered | <NA>              | 54                          |         1 |
| Classified Unnumbered | <NA>              | 55                          |        33 |
| Classified Unnumbered | <NA>              | 56                          |         1 |
| Classified Unnumbered | <NA>              | 57                          |         2 |
| Classified Unnumbered | <NA>              | 58                          |         4 |
| Classified Unnumbered | <NA>              | 60                          |      5751 |
| Classified Unnumbered | <NA>              | 62                          |         2 |
| Classified Unnumbered | <NA>              | 65                          |         6 |
| Classified Unnumbered | <NA>              | 70                          |        29 |
| Classified Unnumbered | <NA>              | 75                          |         3 |
| Classified Unnumbered | <NA>              | 80                          |         2 |
| Classified Unnumbered | <NA>              | 100                         |         1 |
| Classified Unnumbered | <NA>              | 110                         |         2 |
| Classified Unnumbered | <NA>              | 125                         |         3 |
| Classified Unnumbered | <NA>              | 195                         |         1 |
| Classified Unnumbered | <NA>              | <NA>                        |     32465 |
| Motorway              | Rural             | 15                          |         1 |
| Motorway              | Rural             | 19                          |         2 |
| Motorway              | Rural             | 20                          |         2 |
| Motorway              | Rural             | 21                          |         1 |
| Motorway              | Rural             | 22                          |         7 |
| Motorway              | Rural             | 25                          |         2 |
| Motorway              | Rural             | 27                          |         1 |
| Motorway              | Rural             | 29                          |         2 |
| Motorway              | Rural             | 30                          |         2 |
| Motorway              | Rural             | 31                          |         2 |
| Motorway              | Rural             | 33                          |         1 |
| Motorway              | Rural             | 34                          |         1 |
| Motorway              | Rural             | 36                          |         3 |
| Motorway              | Rural             | 40                          |         4 |
| Motorway              | Rural             | 50                          |         5 |
| Motorway              | Rural             | 55                          |         1 |
| Motorway              | Rural             | 60                          |        15 |
| Motorway              | Rural             | 68                          |        12 |
| Motorway              | Rural             | 69                          |         9 |
| Motorway              | Rural             | 70                          |       686 |
| Motorway              | Urban             | 17                          |         5 |
| Motorway              | Urban             | 18                          |         1 |
| Motorway              | Urban             | 19                          |         4 |
| Motorway              | Urban             | 20                          |         4 |
| Motorway              | Urban             | 21                          |        17 |
| Motorway              | Urban             | 22                          |        16 |
| Motorway              | Urban             | 23                          |         4 |
| Motorway              | Urban             | 24                          |         4 |
| Motorway              | Urban             | 25                          |         1 |
| Motorway              | Urban             | 27                          |         2 |
| Motorway              | Urban             | 28                          |         1 |
| Motorway              | Urban             | 29                          |         3 |
| Motorway              | Urban             | 30                          |        38 |
| Motorway              | Urban             | 31                          |         2 |
| Motorway              | Urban             | 33                          |         2 |
| Motorway              | Urban             | 34                          |         4 |
| Motorway              | Urban             | 35                          |        17 |
| Motorway              | Urban             | 37                          |         2 |
| Motorway              | Urban             | 40                          |        56 |
| Motorway              | Urban             | 45                          |         6 |
| Motorway              | Urban             | 50                          |        83 |
| Motorway              | Urban             | 53                          |         1 |
| Motorway              | Urban             | 54                          |         1 |
| Motorway              | Urban             | 55                          |         9 |
| Motorway              | Urban             | 60                          |        27 |
| Motorway              | Urban             | 61                          |         1 |
| Motorway              | Urban             | 65                          |         3 |
| Motorway              | Urban             | 68                          |        10 |
| Motorway              | Urban             | 69                          |        28 |
| Motorway              | Urban             | 70                          |      2400 |
| Motorway              | <NA>              | 22                          |         2 |
| Motorway              | <NA>              | 27                          |         2 |
| Motorway              | <NA>              | 29                          |         1 |
| Motorway              | <NA>              | 30                          |         1 |
| Motorway              | <NA>              | 34                          |         1 |
| Motorway              | <NA>              | 35                          |         1 |
| Motorway              | <NA>              | 37                          |         1 |
| Motorway              | <NA>              | 39                          |         1 |
| Motorway              | <NA>              | 40                          |         3 |
| Motorway              | <NA>              | 60                          |         1 |
| Motorway              | <NA>              | 68                          |         8 |
| Motorway              | <NA>              | 69                          |         8 |
| Motorway              | <NA>              | 70                          |       543 |
| Not Classified        | Rural             | 9                           |         8 |
| Not Classified        | Rural             | 10                          |       168 |
| Not Classified        | Rural             | 12                          |         7 |
| Not Classified        | Rural             | 15                          |       663 |
| Not Classified        | Rural             | 16                          |         3 |
| Not Classified        | Rural             | 17                          |       606 |
| Not Classified        | Rural             | 19                          |      1489 |
| Not Classified        | Rural             | 20                          |      2162 |
| Not Classified        | Rural             | 21                          |      2547 |
| Not Classified        | Rural             | 22                          |      5957 |
| Not Classified        | Rural             | 23                          |       968 |
| Not Classified        | Rural             | 24                          |       155 |
| Not Classified        | Rural             | 25                          |      4105 |
| Not Classified        | Rural             | 26                          |      2835 |
| Not Classified        | Rural             | 27                          |      2267 |
| Not Classified        | Rural             | 28                          |      2612 |
| Not Classified        | Rural             | 29                          |      4778 |
| Not Classified        | Rural             | 30                          |      3269 |
| Not Classified        | Rural             | 31                          |       107 |
| Not Classified        | Rural             | 33                          |        82 |
| Not Classified        | Rural             | 34                          |       662 |
| Not Classified        | Rural             | 35                          |       748 |
| Not Classified        | Rural             | 36                          |        78 |
| Not Classified        | Rural             | 37                          |       210 |
| Not Classified        | Rural             | 38                          |        15 |
| Not Classified        | Rural             | 39                          |        12 |
| Not Classified        | Rural             | 40                          |       211 |
| Not Classified        | Rural             | 41                          |        80 |
| Not Classified        | Rural             | 42                          |       181 |
| Not Classified        | Rural             | 43                          |       668 |
| Not Classified        | Rural             | 44                          |         1 |
| Not Classified        | Rural             | 45                          |       203 |
| Not Classified        | Rural             | 46                          |       177 |
| Not Classified        | Rural             | 48                          |        30 |
| Not Classified        | Rural             | 50                          |        11 |
| Not Classified        | Rural             | 55                          |         1 |
| Not Classified        | Rural             | 60                          |     23496 |
| Not Classified        | Rural             | 62                          |         1 |
| Not Classified        | Rural             | 65                          |         3 |
| Not Classified        | Rural             | 70                          |        13 |
| Not Classified        | Rural             | 75                          |         1 |
| Not Classified        | Rural             | 80                          |         3 |
| Not Classified        | Urban             | 6                           |         1 |
| Not Classified        | Urban             | 8                           |         1 |
| Not Classified        | Urban             | 9                           |        15 |
| Not Classified        | Urban             | 10                          |       691 |
| Not Classified        | Urban             | 12                          |         4 |
| Not Classified        | Urban             | 14                          |         3 |
| Not Classified        | Urban             | 15                          |       769 |
| Not Classified        | Urban             | 16                          |         4 |
| Not Classified        | Urban             | 17                          |      2552 |
| Not Classified        | Urban             | 18                          |        11 |
| Not Classified        | Urban             | 19                          |      4084 |
| Not Classified        | Urban             | 20                          |      9043 |
| Not Classified        | Urban             | 21                          |      4338 |
| Not Classified        | Urban             | 22                          |     12709 |
| Not Classified        | Urban             | 23                          |      1345 |
| Not Classified        | Urban             | 24                          |       523 |
| Not Classified        | Urban             | 25                          |      6582 |
| Not Classified        | Urban             | 26                          |      5674 |
| Not Classified        | Urban             | 27                          |      2860 |
| Not Classified        | Urban             | 28                          |      6461 |
| Not Classified        | Urban             | 29                          |      5554 |
| Not Classified        | Urban             | 30                          |     63548 |
| Not Classified        | Urban             | 31                          |       211 |
| Not Classified        | Urban             | 32                          |         1 |
| Not Classified        | Urban             | 33                          |       214 |
| Not Classified        | Urban             | 34                          |       741 |
| Not Classified        | Urban             | 35                          |       489 |
| Not Classified        | Urban             | 36                          |       133 |
| Not Classified        | Urban             | 37                          |       383 |
| Not Classified        | Urban             | 38                          |        12 |
| Not Classified        | Urban             | 39                          |        28 |
| Not Classified        | Urban             | 40                          |       277 |
| Not Classified        | Urban             | 41                          |       190 |
| Not Classified        | Urban             | 42                          |       245 |
| Not Classified        | Urban             | 43                          |       196 |
| Not Classified        | Urban             | 45                          |       110 |
| Not Classified        | Urban             | 46                          |       278 |
| Not Classified        | Urban             | 48                          |        53 |
| Not Classified        | Urban             | 50                          |        11 |
| Not Classified        | Urban             | 51                          |         4 |
| Not Classified        | Urban             | 52                          |         1 |
| Not Classified        | Urban             | 55                          |         2 |
| Not Classified        | Urban             | 60                          |        54 |
| Not Classified        | Urban             | 62                          |         2 |
| Not Classified        | Urban             | 65                          |         4 |
| Not Classified        | Urban             | 67                          |         3 |
| Not Classified        | Urban             | 68                          |         1 |
| Not Classified        | Urban             | 70                          |        19 |
| Not Classified        | Urban             | 72                          |         2 |
| Not Classified        | Urban             | 75                          |         5 |
| Not Classified        | Urban             | 80                          |         3 |
| Not Classified        | Urban             | 85                          |         3 |
| Not Classified        | Urban             | 90                          |         8 |
| Not Classified        | Urban             | 95                          |         1 |
| Not Classified        | Urban             | 105                         |         1 |
| Not Classified        | Urban             | 125                         |         2 |
| Not Classified        | Urban             | 224                         |         1 |
| Not Classified        | <NA>              | 9                           |         5 |
| Not Classified        | <NA>              | 10                          |       105 |
| Not Classified        | <NA>              | 15                          |       154 |
| Not Classified        | <NA>              | 16                          |         1 |
| Not Classified        | <NA>              | 17                          |       304 |
| Not Classified        | <NA>              | 19                          |       539 |
| Not Classified        | <NA>              | 20                          |       382 |
| Not Classified        | <NA>              | 21                          |      1676 |
| Not Classified        | <NA>              | 22                          |      2283 |
| Not Classified        | <NA>              | 23                          |       525 |
| Not Classified        | <NA>              | 24                          |        26 |
| Not Classified        | <NA>              | 25                          |      2558 |
| Not Classified        | <NA>              | 26                          |      1362 |
| Not Classified        | <NA>              | 27                          |       316 |
| Not Classified        | <NA>              | 28                          |       341 |
| Not Classified        | <NA>              | 29                          |       909 |
| Not Classified        | <NA>              | 30                          |       519 |
| Not Classified        | <NA>              | 31                          |        16 |
| Not Classified        | <NA>              | 33                          |        71 |
| Not Classified        | <NA>              | 34                          |       484 |
| Not Classified        | <NA>              | 35                          |      1351 |
| Not Classified        | <NA>              | 36                          |        49 |
| Not Classified        | <NA>              | 37                          |       141 |
| Not Classified        | <NA>              | 38                          |        12 |
| Not Classified        | <NA>              | 39                          |         8 |
| Not Classified        | <NA>              | 40                          |       515 |
| Not Classified        | <NA>              | 41                          |        25 |
| Not Classified        | <NA>              | 42                          |       340 |
| Not Classified        | <NA>              | 43                          |       637 |
| Not Classified        | <NA>              | 44                          |         1 |
| Not Classified        | <NA>              | 45                          |       239 |
| Not Classified        | <NA>              | 46                          |       180 |
| Not Classified        | <NA>              | 48                          |         1 |
| Not Classified        | <NA>              | 50                          |         6 |
| Not Classified        | <NA>              | 55                          |         4 |
| Not Classified        | <NA>              | 60                          |       111 |
| Not Classified        | <NA>              | 64                          |         1 |
| Not Classified        | <NA>              | 65                          |         1 |
| Not Classified        | <NA>              | 68                          |         6 |
| Not Classified        | <NA>              | 70                          |        10 |
| Not Classified        | <NA>              | 75                          |         1 |
| Not Classified        | <NA>              | 82                          |         1 |
| Not Classified        | <NA>              | 92                          |         1 |
| Not Classified        | <NA>              | 100                         |         1 |
| Not Classified        | <NA>              | 224                         |         2 |
| Not Classified        | <NA>              | <NA>                        |     16605 |
| Unclassified          | Rural             | 10                          |        24 |
| Unclassified          | Rural             | 14                          |         1 |
| Unclassified          | Rural             | 15                          |       181 |
| Unclassified          | Rural             | 16                          |         9 |
| Unclassified          | Rural             | 17                          |       421 |
| Unclassified          | Rural             | 18                          |         1 |
| Unclassified          | Rural             | 19                          |       841 |
| Unclassified          | Rural             | 20                          |      6333 |
| Unclassified          | Rural             | 21                          |      2882 |
| Unclassified          | Rural             | 22                          |     10780 |
| Unclassified          | Rural             | 23                          |      2344 |
| Unclassified          | Rural             | 24                          |       178 |
| Unclassified          | Rural             | 25                          |      5817 |
| Unclassified          | Rural             | 26                          |      8550 |
| Unclassified          | Rural             | 27                          |      6714 |
| Unclassified          | Rural             | 28                          |     10051 |
| Unclassified          | Rural             | 29                          |     13204 |
| Unclassified          | Rural             | 30                          |     24994 |
| Unclassified          | Rural             | 31                          |       655 |
| Unclassified          | Rural             | 32                          |         1 |
| Unclassified          | Rural             | 33                          |       593 |
| Unclassified          | Rural             | 34                          |      2978 |
| Unclassified          | Rural             | 35                          |      1985 |
| Unclassified          | Rural             | 36                          |      1321 |
| Unclassified          | Rural             | 37                          |      1181 |
| Unclassified          | Rural             | 38                          |       109 |
| Unclassified          | Rural             | 39                          |       402 |
| Unclassified          | Rural             | 40                          |      1556 |
| Unclassified          | Rural             | 41                          |      1435 |
| Unclassified          | Rural             | 42                          |      1598 |
| Unclassified          | Rural             | 43                          |      1426 |
| Unclassified          | Rural             | 44                          |         1 |
| Unclassified          | Rural             | 45                          |       543 |
| Unclassified          | Rural             | 46                          |      1847 |
| Unclassified          | Rural             | 48                          |         4 |
| Unclassified          | Rural             | 50                          |       175 |
| Unclassified          | Rural             | 51                          |         1 |
| Unclassified          | Rural             | 52                          |         3 |
| Unclassified          | Rural             | 54                          |         1 |
| Unclassified          | Rural             | 55                          |        27 |
| Unclassified          | Rural             | 59                          |         5 |
| Unclassified          | Rural             | 60                          |     66184 |
| Unclassified          | Rural             | 65                          |         1 |
| Unclassified          | Rural             | 68                          |         1 |
| Unclassified          | Rural             | 70                          |        41 |
| Unclassified          | Rural             | 75                          |         4 |
| Unclassified          | Rural             | 90                          |         2 |
| Unclassified          | Rural             | 92                          |         1 |
| Unclassified          | Rural             | 100                         |         1 |
| Unclassified          | Rural             | 110                         |         1 |
| Unclassified          | Rural             | 117                         |         1 |
| Unclassified          | Rural             | 220                         |         1 |
| Unclassified          | Urban             | 6                           |         1 |
| Unclassified          | Urban             | 9                           |         1 |
| Unclassified          | Urban             | 10                          |       134 |
| Unclassified          | Urban             | 12                          |        13 |
| Unclassified          | Urban             | 14                          |        28 |
| Unclassified          | Urban             | 15                          |       462 |
| Unclassified          | Urban             | 16                          |        91 |
| Unclassified          | Urban             | 17                          |      4295 |
| Unclassified          | Urban             | 18                          |        78 |
| Unclassified          | Urban             | 19                          |      4827 |
| Unclassified          | Urban             | 20                          |     82060 |
| Unclassified          | Urban             | 21                          |     30467 |
| Unclassified          | Urban             | 22                          |     77151 |
| Unclassified          | Urban             | 23                          |      4578 |
| Unclassified          | Urban             | 24                          |      3152 |
| Unclassified          | Urban             | 25                          |     44743 |
| Unclassified          | Urban             | 26                          |     29799 |
| Unclassified          | Urban             | 27                          |     14734 |
| Unclassified          | Urban             | 28                          |     48324 |
| Unclassified          | Urban             | 29                          |     27427 |
| Unclassified          | Urban             | 30                          |    401773 |
| Unclassified          | Urban             | 31                          |      1573 |
| Unclassified          | Urban             | 32                          |        24 |
| Unclassified          | Urban             | 33                          |       634 |
| Unclassified          | Urban             | 34                          |      5282 |
| Unclassified          | Urban             | 35                          |      2685 |
| Unclassified          | Urban             | 36                          |      2385 |
| Unclassified          | Urban             | 37                          |      1446 |
| Unclassified          | Urban             | 38                          |        56 |
| Unclassified          | Urban             | 39                          |       427 |
| Unclassified          | Urban             | 40                          |      1803 |
| Unclassified          | Urban             | 41                          |      2861 |
| Unclassified          | Urban             | 42                          |       680 |
| Unclassified          | Urban             | 43                          |       589 |
| Unclassified          | Urban             | 45                          |       159 |
| Unclassified          | Urban             | 46                          |      1151 |
| Unclassified          | Urban             | 47                          |         2 |
| Unclassified          | Urban             | 48                          |         7 |
| Unclassified          | Urban             | 49                          |         2 |
| Unclassified          | Urban             | 50                          |       218 |
| Unclassified          | Urban             | 51                          |         7 |
| Unclassified          | Urban             | 52                          |         9 |
| Unclassified          | Urban             | 53                          |         2 |
| Unclassified          | Urban             | 54                          |        11 |
| Unclassified          | Urban             | 55                          |        11 |
| Unclassified          | Urban             | 56                          |         1 |
| Unclassified          | Urban             | 58                          |         1 |
| Unclassified          | Urban             | 59                          |        11 |
| Unclassified          | Urban             | 60                          |      1111 |
| Unclassified          | Urban             | 62                          |         4 |
| Unclassified          | Urban             | 63                          |         2 |
| Unclassified          | Urban             | 65                          |         6 |
| Unclassified          | Urban             | 67                          |         3 |
| Unclassified          | Urban             | 69                          |         1 |
| Unclassified          | Urban             | 70                          |        96 |
| Unclassified          | Urban             | 72                          |         1 |
| Unclassified          | Urban             | 75                          |        17 |
| Unclassified          | Urban             | 80                          |        20 |
| Unclassified          | Urban             | 85                          |         7 |
| Unclassified          | Urban             | 87                          |         2 |
| Unclassified          | Urban             | 90                          |         8 |
| Unclassified          | Urban             | 95                          |         4 |
| Unclassified          | Urban             | 98                          |         1 |
| Unclassified          | Urban             | 100                         |         1 |
| Unclassified          | Urban             | 105                         |         1 |
| Unclassified          | Urban             | 110                         |         3 |
| Unclassified          | Urban             | 122                         |         1 |
| Unclassified          | Urban             | 125                         |         1 |
| Unclassified          | <NA>              | 9                           |         1 |
| Unclassified          | <NA>              | 10                          |         3 |
| Unclassified          | <NA>              | 15                          |        56 |
| Unclassified          | <NA>              | 17                          |        34 |
| Unclassified          | <NA>              | 19                          |       218 |
| Unclassified          | <NA>              | 20                          |       363 |
| Unclassified          | <NA>              | 21                          |       458 |
| Unclassified          | <NA>              | 22                          |       822 |
| Unclassified          | <NA>              | 23                          |       366 |
| Unclassified          | <NA>              | 24                          |        27 |
| Unclassified          | <NA>              | 25                          |       848 |
| Unclassified          | <NA>              | 26                          |       895 |
| Unclassified          | <NA>              | 27                          |       329 |
| Unclassified          | <NA>              | 28                          |      1199 |
| Unclassified          | <NA>              | 29                          |      1647 |
| Unclassified          | <NA>              | 30                          |      3845 |
| Unclassified          | <NA>              | 31                          |       187 |
| Unclassified          | <NA>              | 32                          |         1 |
| Unclassified          | <NA>              | 33                          |       637 |
| Unclassified          | <NA>              | 34                          |      2178 |
| Unclassified          | <NA>              | 35                          |      1574 |
| Unclassified          | <NA>              | 36                          |       717 |
| Unclassified          | <NA>              | 37                          |       683 |
| Unclassified          | <NA>              | 38                          |       152 |
| Unclassified          | <NA>              | 39                          |       250 |
| Unclassified          | <NA>              | 40                          |      1690 |
| Unclassified          | <NA>              | 41                          |      1047 |
| Unclassified          | <NA>              | 42                          |      1924 |
| Unclassified          | <NA>              | 43                          |      2031 |
| Unclassified          | <NA>              | 44                          |         1 |
| Unclassified          | <NA>              | 45                          |       401 |
| Unclassified          | <NA>              | 46                          |      1936 |
| Unclassified          | <NA>              | 47                          |         1 |
| Unclassified          | <NA>              | 50                          |        95 |
| Unclassified          | <NA>              | 54                          |         2 |
| Unclassified          | <NA>              | 55                          |        18 |
| Unclassified          | <NA>              | 60                          |      3882 |
| Unclassified          | <NA>              | 63                          |         3 |
| Unclassified          | <NA>              | 65                          |         1 |
| Unclassified          | <NA>              | 70                          |        25 |
| Unclassified          | <NA>              | 75                          |         1 |
| Unclassified          | <NA>              | 80                          |         1 |
| Unclassified          | <NA>              | 90                          |         1 |
| Unclassified          | <NA>              | 100                         |         3 |
| Unclassified          | <NA>              | 120                         |         1 |
| Unclassified          | <NA>              | 125                         |         1 |
| Unclassified          | <NA>              | <NA>                        |     54584 |
| Unknown               | Rural             | 6                           |         1 |
| Unknown               | Rural             | 9                           |         3 |
| Unknown               | Rural             | 10                          |       337 |
| Unknown               | Rural             | 14                          |         1 |
| Unknown               | Rural             | 15                          |      1643 |
| Unknown               | Rural             | 16                          |         1 |
| Unknown               | Rural             | 17                          |      2625 |
| Unknown               | Rural             | 19                          |      4931 |
| Unknown               | Rural             | 20                          |      5574 |
| Unknown               | Rural             | 21                          |      5211 |
| Unknown               | Rural             | 22                          |     15975 |
| Unknown               | Rural             | 23                          |      3154 |
| Unknown               | Rural             | 24                          |       107 |
| Unknown               | Rural             | 25                          |      6447 |
| Unknown               | Rural             | 26                          |      2464 |
| Unknown               | Rural             | 27                          |      1160 |
| Unknown               | Rural             | 28                          |      3721 |
| Unknown               | Rural             | 29                          |      3336 |
| Unknown               | Rural             | 30                          |      3219 |
| Unknown               | Rural             | 31                          |       109 |
| Unknown               | Rural             | 32                          |         2 |
| Unknown               | Rural             | 33                          |        66 |
| Unknown               | Rural             | 34                          |       725 |
| Unknown               | Rural             | 35                          |      1671 |
| Unknown               | Rural             | 36                          |       446 |
| Unknown               | Rural             | 37                          |       279 |
| Unknown               | Rural             | 38                          |        87 |
| Unknown               | Rural             | 39                          |        26 |
| Unknown               | Rural             | 40                          |       410 |
| Unknown               | Rural             | 41                          |       211 |
| Unknown               | Rural             | 42                          |       166 |
| Unknown               | Rural             | 43                          |      1263 |
| Unknown               | Rural             | 44                          |        11 |
| Unknown               | Rural             | 45                          |       331 |
| Unknown               | Rural             | 46                          |       276 |
| Unknown               | Rural             | 48                          |        18 |
| Unknown               | Rural             | 50                          |        79 |
| Unknown               | Rural             | 51                          |         2 |
| Unknown               | Rural             | 52                          |         8 |
| Unknown               | Rural             | 55                          |         3 |
| Unknown               | Rural             | 57                          |         1 |
| Unknown               | Rural             | 59                          |         2 |
| Unknown               | Rural             | 60                          |     53564 |
| Unknown               | Rural             | 62                          |         1 |
| Unknown               | Rural             | 63                          |         3 |
| Unknown               | Rural             | 65                          |         1 |
| Unknown               | Rural             | 68                          |         1 |
| Unknown               | Rural             | 70                          |        63 |
| Unknown               | Rural             | 75                          |         7 |
| Unknown               | Rural             | 77                          |         1 |
| Unknown               | Rural             | 80                          |         1 |
| Unknown               | Rural             | 90                          |         1 |
| Unknown               | Rural             | 98                          |         1 |
| Unknown               | Rural             | 100                         |        16 |
| Unknown               | Rural             | 110                         |         1 |
| Unknown               | Rural             | 117                         |         1 |
| Unknown               | Rural             | 125                         |         2 |
| Unknown               | Rural             | 134                         |         1 |
| Unknown               | Rural             | 143                         |         3 |
| Unknown               | Rural             | 195                         |         4 |
| Unknown               | Rural             | 224                         |        10 |
| Unknown               | Urban             | 6                           |         3 |
| Unknown               | Urban             | 8                           |         2 |
| Unknown               | Urban             | 9                           |         6 |
| Unknown               | Urban             | 10                          |      1048 |
| Unknown               | Urban             | 12                          |         3 |
| Unknown               | Urban             | 13                          |         1 |
| Unknown               | Urban             | 14                          |         4 |
| Unknown               | Urban             | 15                          |      2003 |
| Unknown               | Urban             | 16                          |         5 |
| Unknown               | Urban             | 17                          |     16123 |
| Unknown               | Urban             | 18                          |        37 |
| Unknown               | Urban             | 19                          |     12276 |
| Unknown               | Urban             | 20                          |     14389 |
| Unknown               | Urban             | 21                          |      8722 |
| Unknown               | Urban             | 22                          |     18496 |
| Unknown               | Urban             | 23                          |      2787 |
| Unknown               | Urban             | 24                          |      1057 |
| Unknown               | Urban             | 25                          |      8136 |
| Unknown               | Urban             | 26                          |      4371 |
| Unknown               | Urban             | 27                          |      1096 |
| Unknown               | Urban             | 28                          |      6131 |
| Unknown               | Urban             | 29                          |      4015 |
| Unknown               | Urban             | 30                          |     96201 |
| Unknown               | Urban             | 31                          |       273 |
| Unknown               | Urban             | 32                          |         7 |
| Unknown               | Urban             | 33                          |       150 |
| Unknown               | Urban             | 34                          |       807 |
| Unknown               | Urban             | 35                          |       912 |
| Unknown               | Urban             | 36                          |       632 |
| Unknown               | Urban             | 37                          |       438 |
| Unknown               | Urban             | 38                          |        27 |
| Unknown               | Urban             | 39                          |        35 |
| Unknown               | Urban             | 40                          |       555 |
| Unknown               | Urban             | 41                          |       389 |
| Unknown               | Urban             | 42                          |       183 |
| Unknown               | Urban             | 43                          |       450 |
| Unknown               | Urban             | 45                          |       272 |
| Unknown               | Urban             | 46                          |       214 |
| Unknown               | Urban             | 47                          |         2 |
| Unknown               | Urban             | 48                          |        34 |
| Unknown               | Urban             | 49                          |         1 |
| Unknown               | Urban             | 50                          |       103 |
| Unknown               | Urban             | 51                          |         3 |
| Unknown               | Urban             | 52                          |         4 |
| Unknown               | Urban             | 54                          |        10 |
| Unknown               | Urban             | 55                          |         8 |
| Unknown               | Urban             | 59                          |         3 |
| Unknown               | Urban             | 60                          |       179 |
| Unknown               | Urban             | 62                          |         4 |
| Unknown               | Urban             | 64                          |         1 |
| Unknown               | Urban             | 65                          |        10 |
| Unknown               | Urban             | 67                          |         1 |
| Unknown               | Urban             | 69                          |         4 |
| Unknown               | Urban             | 70                          |       111 |
| Unknown               | Urban             | 75                          |        12 |
| Unknown               | Urban             | 79                          |         1 |
| Unknown               | Urban             | 80                          |         6 |
| Unknown               | Urban             | 82                          |         1 |
| Unknown               | Urban             | 85                          |         9 |
| Unknown               | Urban             | 87                          |         3 |
| Unknown               | Urban             | 90                          |         6 |
| Unknown               | Urban             | 105                         |         5 |
| Unknown               | Urban             | 110                         |         8 |
| Unknown               | Urban             | 125                         |         3 |
| Unknown               | Urban             | 224                         |        18 |
| Unknown               | <NA>              | 9                           |         5 |
| Unknown               | <NA>              | 10                          |       149 |
| Unknown               | <NA>              | 11                          |        14 |
| Unknown               | <NA>              | 15                          |       460 |
| Unknown               | <NA>              | 16                          |         6 |
| Unknown               | <NA>              | 17                          |      1539 |
| Unknown               | <NA>              | 19                          |      2583 |
| Unknown               | <NA>              | 20                          |      3062 |
| Unknown               | <NA>              | 21                          |      3300 |
| Unknown               | <NA>              | 22                          |     11045 |
| Unknown               | <NA>              | 23                          |      2828 |
| Unknown               | <NA>              | 24                          |        57 |
| Unknown               | <NA>              | 25                          |      5562 |
| Unknown               | <NA>              | 26                          |      1245 |
| Unknown               | <NA>              | 27                          |       380 |
| Unknown               | <NA>              | 28                          |      1510 |
| Unknown               | <NA>              | 29                          |      1466 |
| Unknown               | <NA>              | 30                          |      1244 |
| Unknown               | <NA>              | 31                          |        44 |
| Unknown               | <NA>              | 33                          |        34 |
| Unknown               | <NA>              | 34                          |       609 |
| Unknown               | <NA>              | 35                          |      3147 |
| Unknown               | <NA>              | 36                          |       605 |
| Unknown               | <NA>              | 37                          |       172 |
| Unknown               | <NA>              | 38                          |        31 |
| Unknown               | <NA>              | 39                          |        36 |
| Unknown               | <NA>              | 40                          |      1169 |
| Unknown               | <NA>              | 41                          |       139 |
| Unknown               | <NA>              | 42                          |       266 |
| Unknown               | <NA>              | 43                          |      1610 |
| Unknown               | <NA>              | 44                          |         6 |
| Unknown               | <NA>              | 45                          |       348 |
| Unknown               | <NA>              | 46                          |       269 |
| Unknown               | <NA>              | 48                          |         1 |
| Unknown               | <NA>              | 50                          |        41 |
| Unknown               | <NA>              | 51                          |         2 |
| Unknown               | <NA>              | 54                          |         3 |
| Unknown               | <NA>              | 55                          |         7 |
| Unknown               | <NA>              | 60                          |       500 |
| Unknown               | <NA>              | 63                          |         4 |
| Unknown               | <NA>              | 64                          |         3 |
| Unknown               | <NA>              | 65                          |         2 |
| Unknown               | <NA>              | 69                          |         1 |
| Unknown               | <NA>              | 70                          |        47 |
| Unknown               | <NA>              | 75                          |         5 |
| Unknown               | <NA>              | 90                          |         1 |
| Unknown               | <NA>              | 110                         |         1 |
| Unknown               | <NA>              | 125                         |         1 |
| Unknown               | <NA>              | 134                         |         5 |
| Unknown               | <NA>              | 195                         |         3 |
| Unknown               | <NA>              | 224                         |        22 |
| Unknown               | <NA>              | <NA>                        |     74657 |

## Spot checks (100 rows)

| sample_category                  | link_id                              | road_classification   | ruc_urban_rural   |   speed_limit_mph_effective | speed_limit_source   |   centroid_lat |   centroid_lon | osm_url                                                   |
|:---------------------------------|:-------------------------------------|:----------------------|:------------------|----------------------------:|:---------------------|---------------:|---------------:|:----------------------------------------------------------|
| Motorway                         | E9DBFADE-5CAD-400E-B6B4-3FA01FFF2323 | Motorway              | Urban             |                          70 | lookup_motorway      |        52.599  |     -1.795     | https://www.openstreetmap.org/#map=18/52.599023/-1.794996 |
| Motorway                         | 96D02387-E93A-4191-B555-86F507797756 | Motorway              | Urban             |                          70 | osm                  |        52.6613 |     -1.92198   | https://www.openstreetmap.org/#map=18/52.661336/-1.921983 |
| Motorway                         | E69F5C69-697F-4F0C-BDD2-1ED388E14954 | Motorway              | <NA>              |                          70 | osm                  |        53.3538 |     -2.49808   | https://www.openstreetmap.org/#map=18/53.353814/-2.498085 |
| Motorway                         | D596EE34-5824-4D1D-8D4A-8090FF0DF4EB | Motorway              | Rural             |                          68 | osm                  |        53.7045 |     -0.912777  | https://www.openstreetmap.org/#map=18/53.704547/-0.912777 |
| Motorway                         | 404431C6-11DD-465C-80AB-D9415A393BF2 | Motorway              | Urban             |                          70 | lookup_motorway      |        53.7843 |     -2.30258   | https://www.openstreetmap.org/#map=18/53.784346/-2.302577 |
| Motorway                         | FD08AC5B-4605-4EFF-AF81-8EF264D833F7 | Motorway              | Urban             |                          70 | lookup_motorway      |        53.55   |     -2.2588    | https://www.openstreetmap.org/#map=18/53.550047/-2.258803 |
| Motorway                         | F696E4FE-E600-4323-8A00-CCD4F85412CE | Motorway              | Urban             |                          30 | osm                  |        52.5861 |     -2.01368   | https://www.openstreetmap.org/#map=18/52.586130/-2.013685 |
| Motorway                         | 4C615A0B-B349-4BE2-8300-66E2AE3BB343 | Motorway              | Urban             |                          70 | osm                  |        52.4612 |     -1.49004   | https://www.openstreetmap.org/#map=18/52.461232/-1.490035 |
| Motorway                         | 2C9BC2E1-3C12-4993-8475-67455D41BAE4 | Motorway              | <NA>              |                          70 | lookup_motorway      |        52.3565 |     -1.91752   | https://www.openstreetmap.org/#map=18/52.356471/-1.917516 |
| Motorway                         | 3BCD9083-1BD3-4B6B-A96C-DA446D2495BD | Motorway              | Rural             |                          70 | osm                  |        53.585  |     -0.418421  | https://www.openstreetmap.org/#map=18/53.584957/-0.418421 |
| Motorway                         | 9EE60EBA-49F5-4A67-BB4A-D9562A0291CF | Motorway              | <NA>              |                          70 | lookup_motorway      |        55.0003 |     -3.06507   | https://www.openstreetmap.org/#map=18/55.000288/-3.065073 |
| Motorway                         | DDC152DD-251A-4B56-9F02-6E6F5D0694C6 | Motorway              | Urban             |                          70 | osm                  |        53.0632 |     -1.26888   | https://www.openstreetmap.org/#map=18/53.063224/-1.268879 |
| Motorway                         | 44336555-00EC-4B67-85E9-F596A178D689 | Motorway              | <NA>              |                          70 | osm                  |        52.23   |     -1.52925   | https://www.openstreetmap.org/#map=18/52.229984/-1.529245 |
| Motorway                         | AEBB0B1A-07D9-46BE-870F-C2D0C5326F1C | Motorway              | Urban             |                          70 | lookup_motorway      |        53.3808 |     -2.50675   | https://www.openstreetmap.org/#map=18/53.380830/-2.506745 |
| Motorway                         | 13C1D729-E7AE-4D11-8B8B-6AA7EA5D285F | Motorway              | Urban             |                          70 | lookup_motorway      |        53.3979 |     -2.2684    | https://www.openstreetmap.org/#map=18/53.397866/-2.268402 |
| Motorway                         | 564467BC-5532-4442-A4F9-F9513EDFB880 | Motorway              | Rural             |                          70 | lookup_motorway      |        52.3507 |     -1.84963   | https://www.openstreetmap.org/#map=18/52.350735/-1.849626 |
| Motorway                         | AE6F7044-6020-4085-9280-EA54DC768969 | Motorway              | <NA>              |                          22 | osm                  |        53.3123 |     -2.41873   | https://www.openstreetmap.org/#map=18/53.312306/-2.418734 |
| Motorway                         | 60CAA5D9-C9C0-43F9-BB73-EC4E9B0B235A | Motorway              | <NA>              |                          70 | osm                  |        52.4467 |     -1.70863   | https://www.openstreetmap.org/#map=18/52.446706/-1.708633 |
| Motorway                         | 35DBA2A5-D237-4FBE-9F1C-BD411B13630C | Motorway              | Urban             |                          70 | lookup_motorway      |        53.7074 |     -2.67365   | https://www.openstreetmap.org/#map=18/53.707365/-2.673650 |
| Motorway                         | B8EBE849-B294-4AB2-AE38-4DF98FA58A74 | Motorway              | Urban             |                          70 | lookup_motorway      |        53.7997 |     -2.25061   | https://www.openstreetmap.org/#map=18/53.799654/-2.250611 |
| A-road single carriageway, Rural | 28D22AEB-7927-4028-9683-F104CD2FE215 | A Road                | Rural             |                          60 | osm                  |        52.8322 |     -2.06112   | https://www.openstreetmap.org/#map=18/52.832163/-2.061115 |
| A-road single carriageway, Rural | C68816EB-DAF6-495F-8235-763EA2A6EFF5 | A Road                | Rural             |                          60 | lookup_a_road_single |        52.3484 |     -2.93555   | https://www.openstreetmap.org/#map=18/52.348414/-2.935545 |
| A-road single carriageway, Rural | 901B42ED-2DE1-4348-8373-724B14A6BA49 | A Road                | Rural             |                          40 | osm                  |        51.9631 |     -0.51095   | https://www.openstreetmap.org/#map=18/51.963078/-0.510950 |
| A-road single carriageway, Rural | 1CC13CA7-E8F6-47DB-B233-06384F879EB1 | A Road                | Rural             |                          30 | osm                  |        52.4899 |      1.23575   | https://www.openstreetmap.org/#map=18/52.489900/1.235749  |
| A-road single carriageway, Rural | 9B3D46BE-570D-4B98-A6C8-B5655AEC9798 | A Road                | Rural             |                          50 | osm                  |        54.3058 |     -2.08189   | https://www.openstreetmap.org/#map=18/54.305758/-2.081890 |
| A-road single carriageway, Rural | 6D6BE126-2F91-45D0-AA42-8784D21A17E3 | A Road                | Rural             |                          30 | osm                  |        53.4281 |     -1.0208    | https://www.openstreetmap.org/#map=18/53.428130/-1.020800 |
| A-road single carriageway, Rural | 199B98A3-FC77-446B-9B8C-F9B9E7965896 | A Road                | Rural             |                          60 | lookup_a_road_single |        54.2657 |     -3.19861   | https://www.openstreetmap.org/#map=18/54.265738/-3.198612 |
| A-road single carriageway, Rural | 5D915EB8-F835-462D-BEB5-554AD59A5C04 | A Road                | Rural             |                          60 | osm                  |        53.1457 |      0.0296583 | https://www.openstreetmap.org/#map=18/53.145716/0.029658  |
| A-road single carriageway, Rural | 17482CDD-8E2F-472A-8BAC-410E8CB8DE94 | A Road                | Rural             |                          60 | lookup_a_road_single |        51.8304 |      0.183714  | https://www.openstreetmap.org/#map=18/51.830381/0.183714  |
| A-road single carriageway, Rural | 4DACA932-C80C-4F3B-AF28-BBD5F521FED8 | A Road                | Rural             |                          30 | osm                  |        52.7903 |     -3.07963   | https://www.openstreetmap.org/#map=18/52.790264/-3.079634 |
| A-road single carriageway, Rural | 6FC6A7FA-177B-4731-B8F5-2DEF9313F881 | A Road                | Rural             |                          60 | lookup_a_road_single |        53.1648 |     -3.04015   | https://www.openstreetmap.org/#map=18/53.164836/-3.040152 |
| A-road single carriageway, Rural | 5A447196-3062-44B9-A47D-EF8E386DFC5A | A Road                | Rural             |                          60 | osm                  |        53.8188 |     -0.776587  | https://www.openstreetmap.org/#map=18/53.818787/-0.776587 |
| A-road single carriageway, Rural | A73C47A4-FE0C-41E3-81F2-8D88FCD47A97 | A Road                | Rural             |                          60 | lookup_a_road_single |        54.0812 |     -2.80027   | https://www.openstreetmap.org/#map=18/54.081213/-2.800267 |
| A-road single carriageway, Rural | 9151A7F8-C86C-446F-9842-504271116ECE | A Road                | Rural             |                          40 | osm                  |        52.4617 |     -2.20398   | https://www.openstreetmap.org/#map=18/52.461651/-2.203976 |
| A-road single carriageway, Rural | 7DF03EFE-E820-4279-BA2A-237EF3DC0E6E | A Road                | Rural             |                          60 | lookup_a_road_single |        54.1113 |     -2.63661   | https://www.openstreetmap.org/#map=18/54.111327/-2.636613 |
| A-road single carriageway, Rural | 60E42DCA-E12C-4B39-A28D-F71DD32FFF7B | A Road                | Rural             |                          42 | osm                  |        53.446  |      0.136037  | https://www.openstreetmap.org/#map=18/53.446020/0.136037  |
| A-road single carriageway, Rural | 21CB5F4C-B25D-46F1-B95D-366567FD2BDF | A Road                | Rural             |                          30 | osm                  |        53.1116 |     -0.98191   | https://www.openstreetmap.org/#map=18/53.111644/-0.981910 |
| A-road single carriageway, Rural | 34AA5A32-4245-4499-8997-5A14E085B2B6 | A Road                | Rural             |                          30 | osm                  |        52.3316 |     -1.17625   | https://www.openstreetmap.org/#map=18/52.331553/-1.176251 |
| A-road single carriageway, Rural | B615DC19-BD94-48D8-9FE3-DCB2F25D2FA1 | A Road                | Rural             |                          60 | lookup_a_road_single |        52.9935 |     -1.48857   | https://www.openstreetmap.org/#map=18/52.993545/-1.488573 |
| A-road single carriageway, Rural | 1FBFE923-C412-4906-997D-03CC1E784BC0 | A Road                | Rural             |                          60 | osm                  |        55.6955 |     -1.95913   | https://www.openstreetmap.org/#map=18/55.695524/-1.959134 |
| B-road Urban                     | D2D0FFE4-8ED2-4C2A-8159-3913807BFE5C | B Road                | Urban             |                          30 | lookup_b_road_urban  |        52.9663 |     -1.0921    | https://www.openstreetmap.org/#map=18/52.966265/-1.092096 |
| B-road Urban                     | 87AF7352-2664-47F9-BC0E-233051A0F441 | B Road                | Urban             |                          30 | lookup_b_road_urban  |        51.8476 |     -2.17437   | https://www.openstreetmap.org/#map=18/51.847584/-2.174372 |
| B-road Urban                     | 146EF0C6-109D-49FE-A3C2-24C058F9889C | B Road                | Urban             |                          30 | osm                  |        52.5859 |     -2.06124   | https://www.openstreetmap.org/#map=18/52.585883/-2.061238 |
| B-road Urban                     | 28D5EDBC-02AB-4D7F-B695-AF54645F688A | B Road                | Urban             |                          30 | lookup_b_road_urban  |        53.6072 |     -2.32969   | https://www.openstreetmap.org/#map=18/53.607223/-2.329694 |
| B-road Urban                     | 5C943B89-01C6-426D-B5DB-F26F5D65C92F | B Road                | Urban             |                          30 | osm                  |        54.6111 |     -1.05953   | https://www.openstreetmap.org/#map=18/54.611052/-1.059529 |
| B-road Urban                     | 2FFA74A1-8F99-478B-8407-B262BD924453 | B Road                | Urban             |                          30 | lookup_b_road_urban  |        53.4566 |     -2.40171   | https://www.openstreetmap.org/#map=18/53.456643/-2.401714 |
| B-road Urban                     | 50E960D1-C5B2-4246-97C2-5876BD9941D7 | B Road                | Urban             |                          30 | osm                  |        52.438  |     -1.97648   | https://www.openstreetmap.org/#map=18/52.438019/-1.976477 |
| B-road Urban                     | 5AB68611-7DBC-4B2F-BE91-8E491D5F6D0E | B Road                | Urban             |                          30 | lookup_b_road_urban  |        53.6093 |     -1.8866    | https://www.openstreetmap.org/#map=18/53.609314/-1.886595 |
| B-road Urban                     | 027782B2-5B33-4EBB-82D2-FDDD3CE65EF2 | B Road                | Urban             |                          60 | osm                  |        54.8325 |     -1.47875   | https://www.openstreetmap.org/#map=18/54.832450/-1.478752 |
| B-road Urban                     | 9ED8B5F0-287C-45D8-9B55-FF8C0B1C9818 | B Road                | Urban             |                          28 | osm                  |        52.5966 |     -1.14055   | https://www.openstreetmap.org/#map=18/52.596557/-1.140547 |
| B-road Urban                     | 0816D6C7-70B2-484F-839D-15EEEEAFD230 | B Road                | Urban             |                          20 | osm                  |        53.3937 |     -2.5945    | https://www.openstreetmap.org/#map=18/53.393701/-2.594503 |
| B-road Urban                     | FCAF2A19-D6C0-4DAA-AC2A-682DEB4907FC | B Road                | Urban             |                          30 | osm                  |        53.8083 |     -1.50823   | https://www.openstreetmap.org/#map=18/53.808288/-1.508231 |
| B-road Urban                     | BFF60F6E-0AB9-42F4-91A1-10254B89993B | B Road                | Urban             |                          30 | osm                  |        52.9237 |     -1.21891   | https://www.openstreetmap.org/#map=18/52.923686/-1.218914 |
| B-road Urban                     | 6900B635-B3F5-4A5B-AA1B-D023EC5ECE48 | B Road                | Urban             |                          20 | osm                  |        52.2279 |     -0.269077  | https://www.openstreetmap.org/#map=18/52.227932/-0.269077 |
| B-road Urban                     | 0CD34BA1-8C81-4DD1-956E-DB5CD8C9DD10 | B Road                | Urban             |                          30 | lookup_b_road_urban  |        51.9179 |     -2.10861   | https://www.openstreetmap.org/#map=18/51.917935/-2.108615 |
| B-road Urban                     | 2C491418-E469-436E-8BC5-5B66AEBE2488 | B Road                | Urban             |                          30 | osm                  |        52.4325 |     -1.48155   | https://www.openstreetmap.org/#map=18/52.432475/-1.481547 |
| B-road Urban                     | AAAD4111-4A03-4B3A-9AFA-09F0E97443CD | B Road                | Urban             |                          30 | osm                  |        52.4287 |     -1.45569   | https://www.openstreetmap.org/#map=18/52.428661/-1.455693 |
| B-road Urban                     | F19B1B14-6AEE-4243-9E6C-F75CCD55CFA8 | B Road                | Urban             |                          30 | osm                  |        52.3125 |     -1.95466   | https://www.openstreetmap.org/#map=18/52.312469/-1.954664 |
| B-road Urban                     | 489C76A0-65C3-417A-90D6-86F55D0504F8 | B Road                | Urban             |                          30 | osm                  |        53.7256 |     -1.7482    | https://www.openstreetmap.org/#map=18/53.725558/-1.748203 |
| B-road Urban                     | 28A39D3B-D915-487E-B62A-82AEEFC1697F | B Road                | Urban             |                          30 | lookup_b_road_urban  |        53.4292 |     -2.30754   | https://www.openstreetmap.org/#map=18/53.429166/-2.307539 |
| Unclassified Urban               | A79432DA-83ED-4096-9D00-F0EE4EE903D3 | Unclassified          | Urban             |                          20 | osm                  |        53.9862 |     -1.05543   | https://www.openstreetmap.org/#map=18/53.986184/-1.055434 |
| Unclassified Urban               | 3CD93FCA-0C81-49EC-81A0-BCD672CA4974 | Unclassified          | Urban             |                          30 | osm                  |        53.445  |     -1.45338   | https://www.openstreetmap.org/#map=18/53.444986/-1.453378 |
| Unclassified Urban               | 1A90BD94-4D6D-450F-A727-2B64517DEE84 | Unclassified          | Urban             |                          22 | osm                  |        51.9131 |     -0.429917  | https://www.openstreetmap.org/#map=18/51.913052/-0.429917 |
| Unclassified Urban               | 60A1D9D7-A518-47CE-B2CA-F1B44E0655D8 | Unclassified          | Urban             |                          22 | osm                  |        53.7467 |     -1.73857   | https://www.openstreetmap.org/#map=18/53.746682/-1.738571 |
| Unclassified Urban               | 004FF436-B3BE-4A97-9EFC-66DE0217A53E | Unclassified          | Urban             |                          26 | osm                  |        52.929  |     -1.11785   | https://www.openstreetmap.org/#map=18/52.929009/-1.117853 |
| Unclassified Urban               | 34A6AEDD-64EF-45D5-A6C3-673BC809EA5A | Unclassified          | Urban             |                          20 | osm                  |        54.6729 |     -1.24116   | https://www.openstreetmap.org/#map=18/54.672888/-1.241158 |
| Unclassified Urban               | 66288A60-A209-47DE-90CD-329ABBFEC1B1 | Unclassified          | Urban             |                          34 | osm                  |        54.5372 |     -1.36147   | https://www.openstreetmap.org/#map=18/54.537164/-1.361474 |
| Unclassified Urban               | 82D240A1-4B10-43FE-B755-8E3BA1E5F684 | Unclassified          | Urban             |                          22 | osm                  |        53.1497 |     -2.36776   | https://www.openstreetmap.org/#map=18/53.149662/-2.367759 |
| Unclassified Urban               | 7B36A436-26D3-46AC-85E5-5CED2FF25D46 | Unclassified          | Urban             |                          30 | lookup_minor_urban   |        53.3141 |     -3.46545   | https://www.openstreetmap.org/#map=18/53.314093/-3.465447 |
| Unclassified Urban               | 2A283820-D896-4367-B17B-A3B0487D5A82 | Unclassified          | Urban             |                          28 | osm                  |        53.0446 |     -2.23106   | https://www.openstreetmap.org/#map=18/53.044598/-2.231062 |
| Unclassified Urban               | F0CD9E73-3E2E-49A4-897F-B8380B2B55A7 | Unclassified          | Urban             |                          25 | osm                  |        52.5498 |     -2.11027   | https://www.openstreetmap.org/#map=18/52.549849/-2.110265 |
| Unclassified Urban               | 6EBC5772-2599-4EF8-A789-B3CC4EB3BB82 | Unclassified          | Urban             |                          22 | osm                  |        53.5074 |     -1.36241   | https://www.openstreetmap.org/#map=18/53.507378/-1.362413 |
| Unclassified Urban               | CFD7EA29-F061-4CAF-8BE3-8D80D46CA102 | Unclassified          | Urban             |                          22 | osm                  |        53.2604 |     -2.13411   | https://www.openstreetmap.org/#map=18/53.260383/-2.134112 |
| Unclassified Urban               | ABE3B259-AFA1-4193-9E64-301B286BD784 | Unclassified          | Urban             |                          30 | lookup_minor_urban   |        53.415  |     -2.14479   | https://www.openstreetmap.org/#map=18/53.415036/-2.144794 |
| Unclassified Urban               | 34625FB5-4947-4E99-9831-1E476F84191B | Unclassified          | Urban             |                          30 | lookup_minor_urban   |        51.9547 |      0.648908  | https://www.openstreetmap.org/#map=18/51.954728/0.648908  |
| Unclassified Urban               | 1042629F-5811-4419-9BD2-BA399C74F9DD | Unclassified          | Urban             |                          20 | osm                  |        53.9435 |     -1.0855    | https://www.openstreetmap.org/#map=18/53.943518/-1.085502 |
| Unclassified Urban               | CB2EBACF-BFC0-4CC5-ABBD-245D36522E02 | Unclassified          | Urban             |                          30 | lookup_minor_urban   |        53.606  |     -3.04969   | https://www.openstreetmap.org/#map=18/53.605983/-3.049686 |
| Unclassified Urban               | 3FEB3F11-2B86-47F6-880A-3B87A382B14A | Unclassified          | Urban             |                          20 | osm                  |        53.7586 |     -1.61988   | https://www.openstreetmap.org/#map=18/53.758595/-1.619876 |
| Unclassified Urban               | 24134885-6D36-45AE-A3BE-94E815292689 | Unclassified          | Urban             |                          30 | osm                  |        53.8563 |     -0.434944  | https://www.openstreetmap.org/#map=18/53.856310/-0.434944 |
| Unclassified Urban               | 6053B45D-C298-4960-B235-8A6EEEE03476 | Unclassified          | Urban             |                          30 | lookup_minor_urban   |        53.5672 |     -2.45234   | https://www.openstreetmap.org/#map=18/53.567227/-2.452337 |
| Unclassified Rural               | BEF8AEAD-B5E8-4368-9AF1-95174AB66CBB | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        51.826  |     -1.05738   | https://www.openstreetmap.org/#map=18/51.826048/-1.057385 |
| Unclassified Rural               | 01273DC2-C9CD-446C-A8A3-CE0539B02E49 | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        53.128  |     -1.39618   | https://www.openstreetmap.org/#map=18/53.128018/-1.396177 |
| Unclassified Rural               | B9C86CCB-28F9-4253-8299-3F88E2B6FD7C | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        52.0376 |     -1.48988   | https://www.openstreetmap.org/#map=18/52.037634/-1.489885 |
| Unclassified Rural               | F8F123E6-63DB-44B8-8FE3-3BB744722C6A | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        53.2758 |     -1.6557    | https://www.openstreetmap.org/#map=18/53.275848/-1.655698 |
| Unclassified Rural               | 3E952EEF-F2B1-4154-AC04-58E2B00BD257 | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        52.9645 |     -3.15947   | https://www.openstreetmap.org/#map=18/52.964517/-3.159470 |
| Unclassified Rural               | BEDD5635-330C-4880-B475-2622501D9943 | Unclassified          | Rural             |                          27 | osm                  |        54.7195 |     -1.3984    | https://www.openstreetmap.org/#map=18/54.719482/-1.398398 |
| Unclassified Rural               | B239B0A9-2F2F-46FA-8E65-31BE15B2738A | Unclassified          | Rural             |                          30 | osm                  |        54.8373 |     -1.53891   | https://www.openstreetmap.org/#map=18/54.837287/-1.538913 |
| Unclassified Rural               | 8E9E49F8-CC6C-4B04-9492-AE43D8F355F0 | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        51.79   |     -3.87992   | https://www.openstreetmap.org/#map=18/51.789990/-3.879921 |
| Unclassified Rural               | 6278FCB8-3A13-42D8-841F-29A82440A656 | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        54.1598 |     -3.17717   | https://www.openstreetmap.org/#map=18/54.159771/-3.177166 |
| Unclassified Rural               | 02A16F52-0279-4AD9-BED2-ED1655A8468C | Unclassified          | Rural             |                          30 | osm                  |        52.2341 |      0.939383  | https://www.openstreetmap.org/#map=18/52.234141/0.939383  |
| Unclassified Rural               | 78AAC186-2B94-4587-8565-94CB4DAC2595 | Unclassified          | Rural             |                          28 | osm                  |        53.0578 |     -2.29217   | https://www.openstreetmap.org/#map=18/53.057777/-2.292174 |
| Unclassified Rural               | F6D86E48-0761-4A1D-8C2B-D030BF805C54 | Unclassified          | Rural             |                          29 | osm                  |        52.4482 |      1.44761   | https://www.openstreetmap.org/#map=18/52.448242/1.447605  |
| Unclassified Rural               | FA6F78DE-3D03-4B45-B3C3-5D1FF84CE8EB | Unclassified          | Rural             |                          43 | osm                  |        54.4786 |     -1.49938   | https://www.openstreetmap.org/#map=18/54.478596/-1.499380 |
| Unclassified Rural               | 9353D453-03EE-4E60-A71F-BD55EDC42064 | Unclassified          | Rural             |                          28 | osm                  |        52.8391 |     -1.34833   | https://www.openstreetmap.org/#map=18/52.839078/-1.348331 |
| Unclassified Rural               | 4B54A4F1-FE31-4D8F-86A3-62ECDA24B1A9 | Unclassified          | Rural             |                          30 | osm                  |        53.9853 |     -2.10177   | https://www.openstreetmap.org/#map=18/53.985334/-2.101772 |
| Unclassified Rural               | FB581A15-AB3B-40BD-AB42-0C09AA79FF30 | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        51.816  |     -0.724918  | https://www.openstreetmap.org/#map=18/51.815991/-0.724918 |
| Unclassified Rural               | 4C6274C7-F06E-4937-ACE7-1CC98916DBD5 | Unclassified          | Rural             |                          20 | osm                  |        53.4086 |     -2.46981   | https://www.openstreetmap.org/#map=18/53.408578/-2.469809 |
| Unclassified Rural               | D4DB43E6-C83C-480F-9566-EAFEF1FD65E3 | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        53.0797 |     -1.57274   | https://www.openstreetmap.org/#map=18/53.079715/-1.572743 |
| Unclassified Rural               | EA8D843A-A5D7-4EBB-83A7-679DE1B530FD | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        54.8684 |     -3.38694   | https://www.openstreetmap.org/#map=18/54.868450/-3.386944 |
| Unclassified Rural               | EFD941C4-F09A-4BAA-975D-B5143029DD51 | Unclassified          | Rural             |                          60 | lookup_minor_rural   |        52.137  |     -2.10478   | https://www.openstreetmap.org/#map=18/52.136994/-2.104776 |