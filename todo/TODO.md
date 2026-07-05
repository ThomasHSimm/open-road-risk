# TODO

Tracked here so nothing gets lost. Cross off as done.

This file is a thin index. Active work is split into category files in `todo/`;
queued task specifications (LLM-prompt-shaped) live in `todo/` as one file per
task.

---

## 🔴 High Priority

- [x] Fix middle panel in risk score distribution plot (section 5) — flat uniform
  distribution because it's plotting risk_percentile which is by construction uniform.
  Replace with collision count distribution on collision links instead.

- [ ] Stage 1a geometry fallback — EPSG:27700 transform was
  returning non-finite values in some environments, triggering a BNG coordinate
  fallback in `aadt.py`. Root cause not established. Fallback trigger counts
  are now logged and `docs/internal/aadt_geometry_issue.md` documents the
  observed failure mode; compare against an environment where EPSG:27700 works
  normally and decide whether the fallback should be a permanent path or a
  guarded workaround.


## Full GB output rebuild follow-up

Status: full GB road, traffic, collision, and risk-score rebuild has completed
and passed basic integrity checks.

Validated outputs:

- Open Roads links: 3,941,299
- Link-years: 39,412,990
- Processed STATS19 collision rows: 1,148,857
- Snapped/retained collisions used in road-link annual table: 1,145,198
- Positive road-link × year rows: 945,373
- Unique links with observed retained collisions: 531,442
- XGBoost zero policy: full-zero
- XGBoost pseudo-R²: 0.360
- GLM pseudo-R²: 0.505
- Risk-score output rows: 3,941,299
- Top 1% risk links: 39,413

Remaining work:

- Replace transitional reporting-area grouping with an explicit GB-wide dissolve
  policy.
- Remove dependency on the old partial `areas_study.geojson` grouping logic.
- Decide which compact urban/county-style areas should be merged for legibility.
- Keep the 10 km grid as the primary consistent geography.
- Document that named reporting areas are a simplified display geography, not a
  formal modelling unit.
- Check XGBoost calibration before presenting raw predicted counts as expected
  collision counts.
- Prefer risk percentiles / deciles for public-facing outputs.
- Consider precomputing key-figure map layers outside Quarto to reduce render
  time.

### Reporting-area map geography

The full GB key-figures map now has a GB-wide reporting-area layer. This is
currently a presentation layer built from local-authority / council-area
boundaries and dissolved into larger reporting areas where useful.

This layer is still being refined. The main comparison geography remains the
10 km grid, because it is consistent across Great Britain. The named-area view
is intended for readability, not as the primary modelling unit.


---

## Where to find the rest

| Category | File | Description |
|---|---|---|
| 🟡 Model | [`todo/model.md`](todo/model.md) | Medium-priority Stage 1/2 modelling work |
| 🟢 Infrastructure | [`todo/infrastructure.md`](todo/infrastructure.md) | Output, applications, infra hygiene |
| ⚪ Parked | [`todo/parked.md`](todo/parked.md) | Investigated and deprioritised, with reason |
| ✅ Done | [`todo/done.md`](todo/done.md) | Completed work archive |
| 📋 Queued tasks | `todo/*.md` | One file per LLM-prompt-shaped task spec |
| 📐 Execution notes | [`todo/execution_notes.md`](todo/execution_notes.md) | Order-of-operations guidance |
| 🔭 Future work | [`todo/future_work.md`](todo/future_work.md) | Open directions, low priority |

## Queued tasks at a glance

| Task | File | Status |
|---|---|---|
| MRDB ingest cleanup | [mrdb_ingest.md](todo/mrdb_ingest.md) | Active |
| External iRAP-class benchmark (Victoria/NZ/NSW) | [irap_benchmark.md](todo/irap_benchmark.md) | Active |
| OSM features with road-class-tiered imputation | [osm_features.md](todo/osm_features.md) | ✅ Done (24 April 2026) |
| Network Model GDB integration (SRN-only) | [network_model_gdb.md](todo/network_model_gdb.md) | Active |
| Curvature from OS Open Roads geometry | [curvature.md](todo/curvature.md) | Active |
| Grade from OS Terrain 50 DEM | [grade.md](todo/grade.md) | ✅ Done (1–2 May 2026) |
| IMD LSOA join | [imd.md](todo/imd.md) | ✅ Done (1 May 2026) |
| NaPTAN bus stops — buffer features | [naptan_bus_stops.md](todo/naptan_bus_stops.md) | Active |
| ONS Rural-Urban LSOA classification | [ons_ruc.md](todo/ons_ruc.md) | ✅ Done (23 April 2026) |
