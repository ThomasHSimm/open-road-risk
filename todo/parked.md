## ⚪ Parked (investigated, deprioritised — with reason)

- **Standalone KSI atlas — parked.** Part A of the pre-registered KSI
  diagnostic (`reports/ksi_reporting_consistency.md`,
  `reports/preregistration/ksi_diagnostic_preregistration.md`,
  May 2026) found heterogeneous force/year KSI-to-all-injury ratio
  instability across the study area's 23 forces. 28 force/year rows were
  flagged under the pre-registered ±20% year-on-year ratio-change rule, and
  26 of those survived a practical sensitivity threshold requiring an
  absolute KSI count change of at least 25 collisions. The flag pattern is
  consistent with the documented 2016–2019 CRaSH/COPA injury-based
  severity reporting reform plus Staffordshire-specific anomalies, but does
  not collapse cleanly under tested restricted windows (2017–2024,
  2017–2023, 2019–2023). The adjusted Part A rerun using DfT's collision-level
  severity probabilities (`reports/ksi_reporting_consistency_adjusted.md`)
  reduced the flag count but still failed the pre-registered gate. Staffordshire
  is now confirmed as a DfT-acknowledged 2017–2023 source under-reporting issue
  (`reports/staffordshire_data_quality.md`). Strict pre-registered verdict:
  per-force handling required before KSI modelling is defensible. Part B is not
  run. Revisit only if (a) adjusted Part A passes on a restricted 2019–2023
  ex-Staffordshire window with explicit expected-count and EB methodology, or
  (b) DfT publishes a corrected historical Staffordshire series and the
  full-window adjusted diagnostic then passes.

- **Temporal descriptor integration into Stage 2** — completed evaluation.
  `core_overnight_ratio` and the WebTRIS HGV% descriptor both produced small,
  reproducible improvements in the post-fix collision model, but neither
  cleared the pre-registered adoption threshold. Config C delivered about
  +0.006 pseudo-R² and about 0.85% deviance reduction across all 5 seeds,
  which is real but below threshold. Do not revisit at the same threshold on
  the current evidence. Reopen only if project priorities change or the
  underlying Stage 1b time-zone / WebTRIS HGV models improve materially.

- **Seasonal / month-at-link-grain temporal modelling** — parked. WebTRIS
  shows real seasonal variation, but it is effectively global rather than
  link-specific in the available data, and the higher-priority time-of-day/HGV
  descriptors already failed the production adoption rule.

- **OSM global retrain without class-tiered imputation** — coverage diagnostic
  (19 April 2026) showed no column × road-class combination reaches 80% coverage.
  Median imputation at 5–16% true coverage injects bias that correlates with road
  class. See `quarto/analysis/osm-coverage.qmd`. Replaced by the road-class-tiered
  imputation task below.

- **OS MasterMap Highways (RAMI)** — blocked pending OS Data Hub licensing
  clarification on development-mode use for a public portfolio site. RAMI gives
  lanes and widths on the full GB network but "live application" vs "development
  mode" boundary is not defined clearly enough to commit. Revisit if OS Support
  responds with a specific answer permitting portfolio use.

- **Common-basis pseudo-R²** — deprioritised in favour of 5-seed rank stability
  (see queued tasks). Pseudo-R² isn't the operationally relevant metric; rank
  stability of the top-1% list is.

- **Strava Metro for active travel exposure** — technically free for researchers
  on application but not open data; redistribution of derivatives restricted.
  Portfolio publication friction outweighs benefit. Pedestrian/cyclist exposure
  gap remains open; potential alternative is DfT active travel statistics at
  LSOA level if needed.

- **SCRIM skid resistance** — National Highways collects pavement friction
  continuously but typically does not publish as open data due to liability
  concerns. Checked; no viable open source identified. Parked permanently unless
  a specific LA publishes their local surveys.
