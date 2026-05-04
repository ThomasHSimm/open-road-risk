# TODO

Tracked here so nothing gets lost. Cross off as done.

This file is a thin index. Active work is split into category files in `todo/`;
queued task specifications (LLM-prompt-shaped) live in `todo/` as one file per
task.

---

## 🔴 High Priority

- [ ] Fix temporal trend chart in `03_model_results.ipynb` — observed collision bars
  are invisible because the y-axis is dominated by the predicted × 1000 line. Either
  drop the ×1000 scaling or use a secondary y-axis.
  Notebooks no longer in repo but the figure needs incoporation in qmd files.
  
- [ ] Fix middle panel in risk score distribution plot (section 5) — flat uniform
  distribution because it's plotting risk_percentile which is by construction uniform.
  Replace with collision count distribution on collision links instead.

- [ ] Stage 1a geometry fallback — EPSG:27700 transform was
  returning non-finite values in some environments, triggering a BNG coordinate
  fallback in `aadt.py`. Root cause not established. Fallback trigger counts
  are now logged and `docs/internal/aadt_geometry_issue.md` documents the
  observed failure mode; compare against an environment where EPSG:27700 works
  normally and decide whether the fallback should be a permanent path or a
  guarded workaround.

- [ ] Fix `pct_attribute_snapped` in `road_link_annual` — always 0 because snap
  method name changed to "weighted". Column is misleading, should be removed or
  recalculated as `pct_weighted_snapped`.


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
