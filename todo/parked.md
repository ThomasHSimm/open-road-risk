## ⚪ Parked (investigated, deprioritised — with reason)

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

