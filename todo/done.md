## ✅ Done

- [x] STATS19 ingestion (102,361 Yorkshire collisions 2015–2024, forces 12/13/14/16)
- [x] AADF ingestion (5,260 rows, 2019/2021/2023)
- [x] WebTRIS ingestion (6,516 site × year rows)
- [x] MRDB ingestion (1,948 Yorkshire major road links)
- [x] OS Open Roads ingestion (705,672 links, Yorkshire bbox)
- [x] **Force code bug fixed** — was loading Lancashire/NW England (codes 4–7),
      now correctly loads Yorkshire (codes 12/13/14/16). Pipeline re-run April 2026.
- [x] LSOA coordinate validation (146 flagged suspect, 0.1%)
- [x] Weighted multi-criteria snap (current full-area run ~99.8%, score 0.860)
- [x] Snap quality filter in join.py (score ≥ 0.6, retains 97% of matches)
- [x] `road_link_annual.parquet` (84,146 rows × 37 cols, 49,247 links, 2015–2024)
- [x] `network_features.py` — degree, betweenness, betweenness_relative,
      dist_to_major, pop_density, speed_limit_mph, lanes, lit, is_unpaved
- [x] `model.py` Stage 1a — AADT estimator (counted-only CV R² 0.831)
- [x] `model.py` Stage 1b — temporal profiles (WebTRIS seasonal indices)
- [x] `model.py` Stage 2 — Poisson GLM (pseudo-R² 0.251 after provenance
      hardening) + XGBoost (0.858)
- [x] `03_model_results.ipynb` — full model results notebook with maps
- [x] Retired stale STATS19 coordinate notebook — direct raw-data check found
      Yorkshire BNG fields agree with lat/lon-derived BNG positions within a
      few metres; notebook archived under `notebooks/old/`.
- [x] README.md, CODE_README.md, TODO.md — updated April 2026
- [x] Hardcoded values audit — documented in CODE_README with derivation sources
- [x] OSM features via osmnx + osmium (Geofabrik county pbf files, full study area)
- [x] Post-event column provenance guard (21 April 2026) — STATS19 contextual
      aggregates in join.py
      (`pct_urban`, `pct_dark`, `pct_junction`, `pct_near_crossing`,
      `mean_speed_limit`) are post-event diagnostics. `collision.py` excludes
      them from the Stage 2 modelling dataframe via `FORBIDDEN_POST_EVENT_COLS`
      and asserts GLM/XGBoost feature lists are clean pre-training. Columns are
      also removed from the `risk_scores.parquet` output contract and Streamlit
      app config. Synthetic smoke test verifies they are dropped even when
      present upstream; Stage 2 was rerun and the current `risk_scores.parquet`
      has no forbidden columns.
- [x] `_fix_sd_se_error()` removed from clean.py (April 2026)
- [x] Study area extended to NW England + Midlands (2,167,557 links, 203,928+ collisions)
- [x] XGBoost now drives risk_percentile (not GLM) — GroupShuffleSplit by link_id, R² 0.858
- [x] hgv_proportion added to XGBoost (not GLM — failed 50% coverage threshold)
- [x] QMD site: eda-traffic, model-results, eda-collisions
- [x] R² reconciliation (19 April 2026) — fixed stale values in model-results.qmd
      (0.22/0.31 → 0.269/0.858), README.md, CODE_README.md. Added pseudo-R²
      comparability note flagging that GLM in-sample on downsampled set vs
      XGBoost out-of-sample on true distribution. Superseded by the 21 April
      counted-only/provenance-guard run (GLM 0.251, XGBoost 0.858).
- [x] OSM cache-trap fix (19 April 2026) — `network_features.py` now detects
      missing OSM columns in existing cache and triggers recompute without
      needing `--force`. README quick-start collapsed to single `--osm` call.
- [x] OSM enrichment run on full 2.16M-link study area (19 April 2026) — with
      per-county checkpointing, gc.collect() between counties, trimmed slim
      parquets (refactor to avoid OOM after initial failure on North Yorkshire).
- [x] OSM coverage diagnostic (`quarto/analysis/osm-coverage.qmd`, 19 April 2026)
      — no column × road-class combination reaches 80% coverage; `lanes` at 4–7%
      on minor roads; `speed_limit_mph` highest at 56% overall but lowest on
      motorways (46%, near-constant where populated).
- [x] Model inventory (`quarto/methodology/model-inventory.qmd`, refreshed 21 April 2026) — durable
      baseline of current Stage 2 features, hyperparameters, and training rows.
- [x] Stage 2 base-table size investigation (23 April 2026) — 40% reduction
      in GLM n_full (18.3M → 10.9M) traced to OSM speed_limit_mph at 56.4%
      coverage crossing the 50% direct-use threshold in train_collision_glm(),
      causing dropna cascade. Not caused by counted-only AADF filter. XGBoost
      n_train unchanged (uses fillna=0), production risk_percentile ranking
      unaffected. See reports/stage2_base_table_investigation.md. Short-term
      fix: raise coverage threshold to 80%. Long-term fix: OSM tiered
      imputation (already queued).
- [x] Counted-only AADF filter for Stage 1a (19 April 2026) — CV R² 0.72→0.83,
      local holdout R² 0.776→0.832, spatial holdout R² 0.707→0.788. Dropped
      1,288 count points (9.1%) that are always Estimated across 2015-2024.
      Major/Minor skew 11.2% vs 4.6%; regional distribution approximately
      uniform, with Wales higher at 17% on a small sample. Documented in
      exposure-model.qmd. Weighted-Estimated training considered and rejected
      as methodologically arbitrary.
- [x] ~~Download additional AADF years~~ — stale; AADF ingest already loads full
      2015-2024 range. Real issue was counted-vs-estimated, now handled by the
      counted-only filter.
- [x] Empirical Bayes shrinkage for risk ranking (25 April 2026) — v1
  implemented with positive-event weighted MoM k ≈ 3.07. Session 1: dispersion
  strongly non-constant across predicted-risk range (k_bin varies ~3,400× from
  low- to high-prediction bins); global-k is a known-imperfect summary. Session 2:
  EB does regression-to-the-mean correction at prediction/observation extremes
  (top-1% intersection 84.93%, ~3,267 links each entering/leaving). Does NOT
  improve cross-seed top-k stability — seed-churn population moved at parity with
  general population under EB. Adopted as additional ranking (`risk_percentile_eb`),
  not a replacement for `risk_percentile`. 5-seed EB comparison deferred — single-run
  §6.4 already answered the relevant question. Per-family or per-bin EB recommended
  for v2, paired with planned facility-family split. Outputs:
  `src/road_risk/model/eb_{dispersion,shrinkage}.py`,
  `src/road_risk/diagnostics/eb_validation.py`,
  `data/models/risk_scores_eb.parquet`,
  `data/provenance/eb_dispersion_provenance.json`,
  `reports/eb_{dispersion,validation}.md`,
  `quarto/methodology/empirical-bayes-shrinkage.qmd`.
  Production `risk_scores.parquet` unchanged throughout. Open caveat: ~4%
  top-1% membership churn from MoM aggregation choice; production k logged in
  provenance JSON. Per-family k removes this ambiguity.
- [x] OSM tiered speed-limit imputation + Stage 2 retrain (24 April 2026) —
      `speed_limit_mph_effective` replaces raw OSM-only feature in model. Coverage
      91.27% (1.98M / 2.17M links) via `road_classification × ruc_urban_rural` lookup;
      raw `speed_limit_mph` preserved as OSM-tagged-only. GLM `n_full` recovered to
      18.3M (matches pre-OSM baseline), GLM pseudo-R² 0.251 → 0.301, XGBoost
      unchanged at 0.858. Top-1% Jaccard 0.951, Spearman 0.996 — ranking essentially
      stable. Methodology page and model inventory updated.
- [x] [DONE] Investigate and resolve 335,692 links (15.5%) with no
      LSOA-derived features — characterised as boundary/coastal/peripheral,
      biased toward minor/rural `road_function`, and 99% outside the active
      `road_link_annual` network. Filled via two-stage approach: 238,507 links
      (71%) by nearest LSOA centroid within 5 km; 97,185 links (29%) with
      rural-default fallback. `speed_limit_mph_effective` recomputed from new
      RUC values. Audit columns `ruc_imputed`, `ruc_fill_method`, and
      `ruc_nearest_lsoa21cd` added. Practical impact of rural-default fallback:
      993 active modelled links (~0.05% of network) carry the default rather
      than spatially inferred values. 1,194 links remain incomplete on
      `dist_to_major_km` (separate gap, not LSOA-derived; deferred). Reports:
      `reports/ruc_fill.md`, `reports/ruc_fill_verification.md`. Provenance:
      `data/provenance/ruc_fill_provenance.json`. Backup:
      `data/features/network_features_pre_ruc_fill.parquet`.
- [x] Methodology Feature summary table verified (24 April 2026) — Network row
      correctly references `speed_limit_mph_effective` not `speed_limit_mph`.
- [x] `.coverage` and `htmlcov/` already ignored in root `.gitignore` — no
      additional housekeeping change needed.
- [x] 5-seed GroupShuffleSplit for rank stability (25 April 2026) — XGBoost evaluated 
      across seeds 42-46. Pseudo-R² highly stable (0.8590 ± 0.0014). Top-1% Jaccard 
      averages 0.918. Narrow top-k cuts show expected fuzzy boundary churn, but full-rank 
      Spearman correlation remains >0.998. See `reports/rank_stability.md`.
- [x] Facility-family split for Stage 2 (25–26 April 2026) — Sessions 1 & 2 complete;
      sessions 3–4 deferred. Split network into Motorway (4,084 links), Trunk A, Other-Urban,
      and Other-Rural based on ONS RUC and road function. Stitched all-links pseudo-R² 0.895
      vs global 0.888; held-out link-grain 0.8898 vs 0.8892 (baseline 0.859 is link-year grain).
      Held-out link-year deltas: trunk_a +0.006, other_urban +0.001, other_rural +0.002 —
      within seed-noise of zero. Motorway delta reverses on held-out (−0.027 vs +0.052
      all-data): overfitting on ~4k-link training set; global model generalises better
      out-of-sample on motorway. Motorway mean residual +0.13 (global −3.3): calibration
      improvement is robust. Adoption decision: do not replace `risk_percentile` with
      stitched ranking; v1 outputs available diagnostically in `risk_scores_family.parquet`.
      Boundary discontinuity max gap 0.0047 — stitching is clean. v2 candidates: motorway
      hyperparameter reduction / partial pooling with trunk-A; per-family EB k; network
      topology features. See `reports/family_validation.md`,
      `quarto/methodology/facility-family-split.qmd §11`.

