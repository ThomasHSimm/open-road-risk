# Staffordshire Data Quality Investigation

**Status:** diagnostic report only. No ingest, snap, model, decision-register, or
production artefact changes.

**Recommendation:** **scope restriction**. The Staffordshire anomaly is present
in raw STATS19 before ORR ingest and survives unchanged through processed,
cleaned, and snapped stages. DfT's published known-issues page confirms this is
an upstream Staffordshire police under-reporting issue affecting 2017-2023, not
an ORR pipeline defect. Future KSI revisit work should exclude Staffordshire by
default; all-injury outputs that surface Staffordshire results should carry a
source-data caveat citing DfT directly.

## Sources Checked

- `data/raw/stats19/dft-road-casualty-statistics-collision-1979-latest-published-year.csv`
- `data/processed/stats19/collision.parquet`
- `data/processed/stats19/collision_clean.parquet`
- `data/processed/stats19/snapped_weighted.parquet`
- `data/features/road_link_annual.parquet`
- `data/models/risk_scores.parquet`
- `src/road_risk/ingest/ingest_stats19.py`
- `src/road_risk/clean_join/clean.py`
- `src/road_risk/clean_join/join.py`
- `config/settings.yaml`
- DfT, "Road casualty statistics: known data issues", updated 29 May 2025:
  <https://www.gov.uk/government/publications/reported-road-casualty-statistics-background-quality-report/road-casualty-statistics-known-data-issues>

Neighbour comparison forces:

- 7 Cheshire
- 22 West Mercia
- 23 Warwickshire
- 30 Derbyshire

## Part 1: Staffordshire Pattern by Data Stage

The Staffordshire issue begins before the ORR pipeline. DfT's known-issues page
states that Staffordshire police under-reported collisions between 2017 and 2023
because reportable collisions in force systems were not fully and timely
included in STATS19 returns. The local raw data match that statement: raw
Staffordshire collisions drop from 2,582 in 2016 to 1,807 in 2017 while the
neighbour comparison set is broadly flat, the deepest trough is 507 in 2022, and
2024 rebounds to 1,496.

The 2022 Staffordshire count is already anomalously low in raw STATS19. It is
507 raw collisions, 507 processed, 507 cleaned, 507 snapped before the Part A
quality filter, and 506 after the `snap_method in {attribute, spatial, weighted}`
plus `snap_score >= 0.6` filter.

| year | raw | processed | clean | snapped_all | snapped_retained | retained drop from raw |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2015 | 2,599 | 2,599 | 2,599 | 2,599 | 2,583 | 0.62% |
| 2016 | 2,582 | 2,582 | 2,582 | 2,582 | 2,535 | 1.82% |
| 2017 | 1,807 | 1,807 | 1,807 | 1,807 | 1,790 | 0.94% |
| 2018 | 1,417 | 1,417 | 1,417 | 1,417 | 1,376 | 2.89% |
| 2019 | 1,312 | 1,312 | 1,312 | 1,312 | 1,309 | 0.23% |
| 2020 | 879 | 879 | 879 | 879 | 879 | 0.00% |
| 2021 | 819 | 819 | 819 | 819 | 819 | 0.00% |
| 2022 | 507 | 507 | 507 | 507 | 506 | 0.20% |
| 2023 | 883 | 883 | 883 | 883 | 883 | 0.00% |
| 2024 | 1,496 | 1,496 | 1,496 | 1,496 | 1,493 | 0.20% |

No raw-vs-processed discrepancy exceeds 5%; all raw-to-processed discrepancies
for Staffordshire and the four comparison forces are 0.0%. The issue is not
introduced by ORR ingest.

`road_link_annual.parquet` does not carry `police_force`, so it cannot be used
as a direct force/year count table. Using links with at least one retained
Staffordshire snapped collision as a Staffordshire-associated proxy, the annual
`road_link_annual` collision totals preserve the same 2022 trough and 2023-2024
rebound:

| year | snapped_retained Staffordshire count | road_link_annual count on Staffordshire-associated links |
| --- | ---: | ---: |
| 2015 | 2,583 | 2,272 |
| 2016 | 2,535 | 2,275 |
| 2017 | 1,790 | 1,609 |
| 2018 | 1,376 | 1,252 |
| 2019 | 1,309 | 1,150 |
| 2020 | 879 | 777 |
| 2021 | 819 | 730 |
| 2022 | 506 | 450 |
| 2023 | 883 | 792 |
| 2024 | 1,493 | 1,298 |

The `road_link_annual` proxy is lower than the force count because it is a
link-year table without police-force attribution and because the saved
production table was built from its own link/year aggregation surface. It is
useful for confirming the production table inherits the 2022 trough, not for
recovering an exact force-year count.

The anomaly is not a single missing month. Staffordshire 2022 is low across the
whole year:

| year | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2020 | 105 | 89 | 64 | 34 | 59 | 68 | 64 | 76 | 104 | 76 | 65 | 75 |
| 2021 | 60 | 55 | 62 | 74 | 89 | 84 | 75 | 74 | 71 | 64 | 61 | 50 |
| 2022 | 55 | 28 | 41 | 46 | 54 | 38 | 41 | 29 | 35 | 48 | 51 | 41 |
| 2023 | 50 | 53 | 57 | 58 | 80 | 72 | 101 | 83 | 73 | 87 | 97 | 72 |
| 2024 | 115 | 97 | 102 | 125 | 117 | 117 | 114 | 100 | 156 | 111 | 186 | 156 |

The anomaly is also not confined to Stoke-on-Trent or to Staffordshire County
Council roads. Both Staffordshire highway authorities fall in 2022 and rebound
afterwards:

| local_authority_highway | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E06000021 | 359 | 238 | 201 | 98 | 191 | 336 |
| E10000028 | 953 | 641 | 618 | 409 | 692 | 1,160 |

The road-class split shows the same broad pattern. Major classes are not
selectively dropped; the low count is visible across A roads, B roads,
unclassified roads, and the local-authority split.

## Part 2: Neighbour-Force Comparison

Raw counts and snapped-retained counts show the same story: Staffordshire is the
outlier after 2020. Neighbours generally show COVID reduction in 2020 followed by
flat or partial recovery in 2021-2024. Staffordshire falls again in 2022 and then
jumps sharply in 2023 and 2024.

### Raw Collision Counts

| force | 2020 | 2021 | 2022 | 2023 | 2024 | YoY 2021 | YoY 2022 | YoY 2023 | YoY 2024 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Cheshire | 1,363 | 1,597 | 1,685 | 1,533 | 1,475 | +17.2% | +5.5% | -9.0% | -3.8% |
| Staffordshire | 879 | 819 | 507 | 883 | 1,496 | -6.8% | -38.1% | +74.2% | +69.4% |
| West Mercia | 1,446 | 1,596 | 1,658 | 1,449 | 1,539 | +10.4% | +3.9% | -12.6% | +6.2% |
| Warwickshire | 855 | 856 | 865 | 994 | 1,092 | +0.1% | +1.1% | +14.9% | +9.9% |
| Derbyshire | 1,462 | 1,787 | 1,974 | 1,767 | 1,656 | +22.2% | +10.5% | -10.5% | -6.3% |

### Snapped-Retained Collision Counts

| force | 2020 | 2021 | 2022 | 2023 | 2024 | YoY 2021 | YoY 2022 | YoY 2023 | YoY 2024 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Cheshire | 1,355 | 1,586 | 1,674 | 1,527 | 1,463 | +17.0% | +5.5% | -8.8% | -4.2% |
| Staffordshire | 879 | 819 | 506 | 883 | 1,493 | -6.8% | -38.2% | +74.5% | +69.1% |
| West Mercia | 1,444 | 1,595 | 1,657 | 1,448 | 1,537 | +10.5% | +3.9% | -12.6% | +6.1% |
| Warwickshire | 855 | 856 | 865 | 993 | 1,092 | +0.1% | +1.1% | +14.8% | +10.0% |
| Derbyshire | 1,458 | 1,781 | 1,970 | 1,764 | 1,650 | +22.2% | +10.6% | -10.5% | -6.5% |

**Verdict:** the post-2020 anomaly is Staffordshire-specific, not a regional or
national recovery pattern. The neighbour median 2021-2022 raw change is +4.7%;
Staffordshire is -38.1%. A neighbour-normalised expectation from the 2021
Staffordshire count would be roughly 858 collisions in 2022, about 351 above the
507 raw records present.

## Part 3: Location and Likely Cause

### Raw Source

Confirmed contributor. The 2022 Staffordshire count is low in the raw DfT
collision CSV before any ORR processing. The 2022 drop is all-year and
all-authority rather than one missing month or one missing local authority.

Confirmed cause: DfT's published "Road casualty statistics: known data issues"
page identifies Staffordshire police under-reporting between 2017 and 2023 due
to incomplete and untimely STATS19 processing returns. DfT states that
rectifying actions have improved completeness by the end of the period, that
provisional 2024 completeness has returned to broadly expected levels, and that
the historical issue is unlikely to be rectified; no imputation has been
attempted. The local ORR pattern matches that account.

### Ingest Filter

Ruled out. `data/processed/stats19/collision.parquet` exactly matches the raw
counts for Staffordshire and neighbours by force/year. No raw-vs-processed
discrepancy exceeds 5%; all are 0.0%.

### Cleaning

Ruled out. `collision_clean.parquet` preserves the same Staffordshire
force/year counts as raw and processed. Cleaning flags coordinate quality but
does not drop collision records.

### Bounding Box Clipping

Ruled out as the 2022 cause. For Staffordshire:

| year | raw/processed rows | inside study bbox | share inside bbox |
| --- | ---: | ---: | ---: |
| 2015 | 2,599 | 2,589 | 99.62% |
| 2016 | 2,582 | 2,580 | 99.92% |
| 2017 | 1,807 | 1,802 | 99.72% |
| 2018 | 1,417 | 1,414 | 99.79% |
| 2019 | 1,312 | 1,312 | 100.00% |
| 2020 | 879 | 879 | 100.00% |
| 2021 | 819 | 819 | 100.00% |
| 2022 | 507 | 507 | 100.00% |
| 2023 | 883 | 883 | 100.00% |
| 2024 | 1,496 | 1,496 | 100.00% |

The configured WGS84 bbox covers all 2020-2024 Staffordshire collisions, so the
2022 low count is not caused by clipping.

### Spatial Snap

Ruled out as the 2022 cause. Staffordshire snap retention is normal in 2022:
507 snapped records become 506 retained records after the Part A / RLA snap
filter, a 0.20% drop. The largest Staffordshire snap-retention loss is 2.89% in
2018, not 2022.

Staffordshire snap method counts show only `weighted` and a few historic
`invalid_coords` rows; from 2019 onward there are no invalid-coordinate rows
until a single retained-filter drop in 2022.

### Filter Cascade

Ruled out as the 2022 cause. The post-snap Part A filter removes only one
Staffordshire 2022 row. Neighbour force snap-retention drops are similarly small
in 2022: Cheshire 0.65%, West Mercia 0.06%, Warwickshire 0.00%, Derbyshire
0.20%.

### Cause Finding

Cause identified at the source-data level: Staffordshire's 2017-2023 raw
collision volumes are affected by a DfT-acknowledged under-reporting issue. The
2022 trough is the deepest point, but the source issue starts in 2017 and
continues through 2023. ORR ingest, clean, bbox, snap, and Part A filters do not
introduce the anomaly.

## Part 4: All-Injury Model Impact

`risk_scores.parquet` has no police-force field, so this section uses a
collision-associated link proxy: links with at least one retained snapped
collision from the force in 2015-2024. This proxy is adequate for checking
whether Staffordshire-linked production scores look obviously broken, but it is
not a definitive administrative-boundary link set.

| force | collision-associated links | links in risk_scores | nonzero links | nonzero link share | observed collisions on associated links | mean observed per link | top-1% links | top-1% share | mean risk percentile |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Cheshire | 9,411 | 9,411 | 7,665 | 81.45% | 16,393 | 1.742 | 858 | 9.12% | 84.64 |
| Staffordshire | 8,326 | 8,326 | 6,796 | 81.62% | 12,605 | 1.514 | 698 | 8.38% | 84.48 |
| West Mercia | 10,603 | 10,603 | 8,760 | 82.62% | 16,006 | 1.510 | 646 | 6.09% | 84.10 |
| Warwickshire | 5,522 | 5,522 | 4,566 | 82.69% | 10,292 | 1.864 | 506 | 9.16% | 84.96 |
| Derbyshire | 8,684 | 8,684 | 7,303 | 84.10% | 16,108 | 1.855 | 600 | 6.91% | 85.73 |

The Staffordshire production scores do not look mechanically empty or obviously
detached from observed collision history. Staffordshire's associated-link
nonzero share is comparable to neighbours, and 8.38% of Staffordshire-associated
links are in the network-wide top 1%, between West Mercia / Derbyshire and
Cheshire / Warwickshire.

Top-100 Staffordshire-associated production links also look broadly defensible:

| metric | value |
| --- | ---: |
| mean risk percentile | 99.9319 |
| median risk percentile | 99.9260 |
| mean observed collisions | 11.47 |
| median observed collisions | 6.00 |
| mean fatal collisions | 0.41 |
| mean serious collisions | 1.83 |
| zero-observed links in top 100 | 3 |
| links with <=2 observed collisions in top 100 | 18 |
| road-class mix | 72 A Road, 26 Motorway, 2 B Road |

Impact assessment: there is no evidence of an ORR pipeline defect that drops
Staffordshire collisions or strips Staffordshire links from production scoring.
However, because the anomaly is already in source STATS19, the all-injury model
inherits the DfT-acknowledged Staffordshire under-count for 2017-2023. Some
Staffordshire links may therefore be under-counted and under-ranked relative to
their true but unobserved risk, to a varying degree across the affected years.
The current evidence supports a Staffordshire source-data caveat, not a
production rerun.

## Part 5: Recommendation

**Choose option 2: scope restriction.**

The issue is source-level, not an ORR pipeline bug:

- raw Staffordshire 2022 count is 507, matching processed and cleaned counts;
- the snapped Part A count is 506, so the snap/filter cascade removes only one
  2022 row;
- all 2022 Staffordshire rows are inside the configured study bbox;
- neighbouring forces do not show Staffordshire's -38.1% 2021-2022 drop or
  +69.4% 2023-2024 jump;
- the anomaly is all-year and all-authority, consistent with force-level source
  reporting/submission behaviour.

There is no defensible data fix inside ORR. DfT has already identified the issue
as historical Staffordshire under-reporting, has not imputed missing data, and
states the historical issue is unlikely to be rectified. The KSI revisit path
should treat Staffordshire as out of scope by default unless DfT publishes a
corrected historical series. For all-injury outputs, do not discard the existing
production model solely on this finding, but add Staffordshire caveat language
wherever local Staffordshire link rankings are interpreted operationally: the
model reflects published STATS19 counts, and those counts contain a
force-specific 2017-2023 under-reporting issue that may under-rank affected
Staffordshire links.

## Register-Ready Summary

## 2026-05-23: Staffordshire post-2017 collision under-reporting - DfT-acknowledged source issue; scope restriction

**Investigated:** are the persistent Staffordshire flags in the adjusted Part A
diagnostic a pipeline defect or a source-data issue, and how does the all-injury
model handle Staffordshire?

**Method:** stage-by-stage collision count comparison (raw -> processed ->
snapped -> road_link_annual) for Staffordshire and four neighbour forces
(Cheshire, West Mercia, Warwickshire, Derbyshire), 2015-2024; verified bbox
clipping, snap retention, and filter cascade rule out pipeline contributors;
assessed all-injury production scoring on Staffordshire-associated links. DfT's
published "Known data issues" page (updated 29 May 2025) was consulted after the
local investigation completed and confirms the upstream cause.

**Outcome:** the anomaly is DfT-acknowledged Staffordshire police
under-reporting between 2017 and 2023 due to incomplete and untimely STATS19
processing returns. The 2017 onset (raw 1,807, down from 2,582 in 2016 against
flat neighbours) matches the start of DfT's stated under-reporting window; the
2022 trough (raw 507) is its deepest point; 2024 recovery to 1,496 matches DfT's
note that completeness has returned to broadly expected levels. DfT states the
historical issue is unlikely to be rectified and no imputation has been
attempted. ORR pipeline transmits the source data faithfully; all-injury
production scores show no obvious failure but under-rank affected Staffordshire
links to a varying degree across 2017-2023.

**Artefacts:**
- `reports/staffordshire_data_quality.md`
- DfT, "Road casualty statistics: known data issues", updated 29 May 2025:
  <https://www.gov.uk/government/publications/reported-road-casualty-statistics-background-quality-report/road-casualty-statistics-known-data-issues>

**Revisit condition:** None - the upstream issue is acknowledged-permanent and
DfT has explicitly stated no imputation will be applied. For LA-facing outputs,
add Staffordshire caveat language citing the DfT known-issues page directly. The
KSI revisit condition (2026-05-22 entry) should reference this entry and treat
Staffordshire as out-of-scope by default for any future revisit.
