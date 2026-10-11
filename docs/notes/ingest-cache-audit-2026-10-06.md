# Ingest cache audit — 2026-10-06

Trigger: the AADF Stage-1a training data was silently clipped to a 52.0–55.2°N
subset by a cache that was keyed only on the study-area name and reused after the
configured bbox was widened (filters can only shrink a cache, never re-add dropped
points). This audits every ingest/feature cache for the same pattern and verifies
each current artefact's extent against the full-GB bbox (lat 49.8–60.9, lon −8.7–2.1).

## The bug pattern
name-keyed cache file + a bbox/area filter applied on **cache read** that can only
**shrink** the cached rows → widening the bbox returns a stale, narrower result.

## Findings

| source | cache keyed on | filter-on-read | shrink-only bug? | current artefact extent | status |
|---|---|---|---|---|---|
| **AADF** (`load_aadf`) | study-area **name** | bbox (study area) | **YES** | `aadf_clean` 52.0–55.2°N | **BUG — fixed in code; data stale, rebuild in D** |
| **WebTRIS raw** (`get_all_sites`, chunk/site caches) | fixed names | none (bbox applied downstream) | no | raw `sites.parquet` 50.1–55.8°N (national SRN) | OK |
| **WebTRIS processed** (`webtris_clean.parquet`) | — (build output) | bbox at build | no (rebuilt from full raw) | 52.0–55.2°N | **stale subset — rebuild (not AADF scope)** |
| **STATS19** (`load_stats19`) | — (reads raw CSVs each run) | bbox after load | no | `collision_clean` 49.9–60.8°N | OK (full GB) |
| **Open Roads** (`load_openroads`) | — (rebuilds from gpkg) | bbox_bng at load | no | `openroads.parquet` 49.9–60.8°N | OK (full GB) |
| **network_features** / deprivation / population / rural-urban / terrain / curvature | fixed path, **link_id**-keyed incremental merge | none (join by link_id) | no | 3,941,299 links, England+Scotland+Wales | OK (full GB) |

## Fixes
- `ingest_aadf.load_aadf`: cache filename now includes a hash of bbox + filter
  settings (`_cache_key`), and a sidecar `.meta.json` records the build bbox;
  `_assert_cache_covers_bbox` raises if a cache was built under a bbox smaller
  than the configured one. Test: `tests/test_aadf_cache.py`.

## Left to rebuild (data staleness, not code bugs)
- AADF chain (`aadf_filtered`/`aadf_raw`/`aadf_clean`) — scheduled for D.
- `webtris_clean.parquet` (recovers ~50.1–55.8°N SRN coverage). Only feeds Stage 1b
  timezone profiles and `WEBTRIS_AADT_FEATURES` (currently empty), so it does not
  affect Stage 1a AADT; flagged for a separate rebuild.
