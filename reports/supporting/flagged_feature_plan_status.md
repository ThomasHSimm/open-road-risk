# Flagged Feature Plan Status

## Summary

The missingness audit flags are consistent with OSM coverage patterns, not with
the HGV source-table bug shape. The four columns do not all have the same
production status:

| Feature | Plan status | Current state | Action |
|---|---|---|---|
| `speed_limit_mph` | Partially implemented replacement | Raw OSM/provenance column remains; production model uses `speed_limit_mph_effective` | Do not use raw `speed_limit_mph` as a model feature; audit flag is on stale/provenance column |
| `lanes` | Implemented as sparse OSM input under current docs | Computed, joined, GLM-imputed, raw in XGBoost | Accepted OSM coverage limitation unless the older default-lanes TODO is revived |
| `is_unpaved` | Implemented as sparse OSM input under current docs | Computed, joined, GLM-imputed, raw in XGBoost | Accepted OSM coverage limitation unless the older default-surface TODO is revived |
| `lit` | Not a current production model feature | Computed and joined, but excluded from GLM/XGBoost and final score output | Audit flag is on a non-production column; decide separately whether to model lighting |

No code was changed for this reconciliation.

## Sources Checked

Checked documentation and plans:

- `README.md`, `CODE_README.md`
- `TODO.md`, `todo/osm_features.md`, `todo/done.md`, `todo/parked.md`
- `reports/model_inventory.md`
- `reports/stage2_base_table_investigation.md`
- `reports/speed_limit_effective_verification.md`
- `reports/ruc_fill.md`
- `quarto/analysis/osm-coverage.qmd`
- `quarto/methodology/feature-engineering.qmd`
- `quarto/methodology/model-inventory.qmd`
- `quarto/methodology/methodology-index.qmd`
- `docs/internal/*`, `docs/notes/*`
- docstrings and comments in `src/road_risk/features/`, `src/road_risk/clean_join/`, and `src/road_risk/model/`
- `config/settings.yaml` TODO/FIXME comments
- recent commit messages touching the relevant files

Recent commit messages found:

- `f762431 2026-04-24 Add speed limit lookup and re-ran`
- Later relevant commits are broad documentation/feature commits such as
  `04ab2dd TODO clean up`, `381db60 Optimisation avoid kills temp and summary doc`,
  `18e0f70 Add curvature`, and `eea7962 DONE temporal plan`; no recent commit
  message specifically names `lanes`, `lit`, or `is_unpaved`.

## `speed_limit_mph`

### Documented Plan Or Status

The documented plan says raw OSM speed coverage was too sparse for direct global
use and should be replaced by a tiered lookup feature:

- `README.md` and `CODE_README.md` say raw `speed_limit_mph` coverage is 56.4%,
  while `speed_limit_mph_effective` raises coverage to about 91.27%.
- `todo/osm_features.md` records the road-class-tiered imputation plan and the
  problem it was meant to solve: raw OSM speed at 56.4% was shrinking the GLM
  training set.
- `todo/done.md` says the speed-limit task was completed on 24 April 2026:
  `speed_limit_mph_effective` replaces raw OSM-only speed in the model, while
  raw `speed_limit_mph` is preserved as OSM-tagged-only.
- `reports/model_inventory.md` and `quarto/methodology/model-inventory.qmd`
  explicitly state that raw `speed_limit_mph` is retained as provenance but is
  not in the trained feature list.
- `reports/speed_limit_effective_verification.md` verifies that raw
  `speed_limit_mph` was unchanged, `speed_limit_mph_effective` reached 91.27%
  coverage, and `speed_limit_source` records lookup provenance.

There is also an older research note in
`docs/notes/2026-04-19-deep-research-report-followup.md` warning that the raw
speed extraction semantics may be imperfect because the extractor uses
OSMnx `add_edge_speeds()` when `speed_kph` is available. That is a separate
semantic hardening issue, not the missingness plan that this audit surfaced.

### Current Code And Artefacts

Current code matches the replacement plan:

- `src/road_risk/features/network.py` computes raw `speed_limit_mph`, then
  adds `speed_limit_mph_effective`, `speed_limit_mph_imputed`, and
  `speed_limit_source` via `apply_speed_limit_effective_lookup()`.
- `network_features.parquet` currently contains all four columns:
  - `speed_limit_mph`: 56.43% non-null
  - `speed_limit_mph_effective`: 91.27% non-null
  - `speed_limit_mph_imputed`: 100% non-null
  - `speed_limit_source`: 100% non-null
- `src/road_risk/model/collision.py` includes `speed_limit_mph_effective` in
  both GLM and XGBoost candidate lists.
- Raw `speed_limit_mph` is not in either trained feature list in
  `data/models/collision_metrics.json`.
- `risk_scores.parquet` still includes raw `speed_limit_mph` and
  `speed_limit_mph_effective`; it does not include `speed_limit_source` or
  `speed_limit_mph_imputed`.

### Reconciliation

`speed_limit_mph_effective` is the intended production feature.
`speed_limit_source` and `speed_limit_mph_imputed` are provenance/audit fields.
Raw `speed_limit_mph` should not be in the Stage 2 model feature set, and
currently is not.

The audit flag on `speed_limit_mph` is therefore a stale/provenance-column flag,
not evidence of an unfinished HGV-style join bug. Keeping raw
`speed_limit_mph` in the Stage 2 dataframe and score output is consistent with
the documented provenance plan, but future model-feature audits should treat it
as provenance unless the question is explicitly "all columns in the Stage 2
base table."

## `lanes`

### Documented Plan Or Status

The documentation consistently identifies `lanes` as sparse OSM coverage:

- `README.md` and `CODE_README.md` report about 7.3% coverage and say sparse
  OSM fields are median-imputed where retained in the GLM.
- `quarto/analysis/osm-coverage.qmd` reports 7.3% overall coverage, with
  especially low coverage on `Unclassified`, `Not Classified`, and `Unknown`
  roads.
- `reports/model_inventory.md` and `quarto/methodology/model-inventory.qmd`
  list `lanes_imputed` for GLM and raw `lanes` for XGBoost.
- `reports/ruc_fill.md` records the current GLM policy: `lanes` has low
  coverage and is median-imputed.

There is one older/broader plan in `todo/osm_features.md` that expected
road-class lane defaults and `_imputed` flags. The later done note in
`todo/done.md`, however, describes the completed 24 April task specifically as
speed-limit imputation, not a completed default-lanes implementation.

### Current Code And Artefacts

Current code computes and uses `lanes`:

- `src/road_risk/features/network.py` parses OSM `lanes` into the `lanes`
  column and joins it to OS Open Roads by nearest OSM edge.
- `network_features.parquet` contains `lanes` with 7.30% non-null coverage.
- `build_collision_dataset()` joins all network features, so `lanes` is present
  in the Stage 2 dataframe.
- `train_collision_glm()` includes `lanes` as an optional candidate. In the
  current metrics, it appears as `lanes_imputed` and `lanes_missing`.
- `train_collision_xgb()` includes raw `lanes` when the column is present.
- `risk_scores.parquet` does not carry `lanes`.

### Reconciliation

Under current model documentation, the `lanes` flag matches documented intent:
it is a sparse OSM feature, accepted with imputation in GLM and raw missingness
handling in XGBoost. The audit flag is therefore best interpreted as OSM
coverage correlated with road importance and collision history, not a
collision-aggregate-first source-table bug.

The only unresolved documentation tension is the older default-lanes plan in
`todo/osm_features.md`. That plan is not implemented. If the project still wants
lane defaults, that should be reopened as separate feature engineering work.
It is not required to explain the current audit flag.

## `is_unpaved`

### Documented Plan Or Status

The documented status mirrors `lanes`: sparse OSM surface coverage, retained
with cautious imputation.

- `README.md` and `CODE_README.md` say surface-derived flags remain sparse
  and are median-imputed where retained.
- `quarto/analysis/osm-coverage.qmd` reports `is_unpaved` at about 16.2%
  overall coverage, with lower coverage on minor and unknown classes.
- `reports/model_inventory.md` and `quarto/methodology/model-inventory.qmd`
  list `is_unpaved_imputed` for GLM and raw `is_unpaved` for XGBoost.
- `reports/ruc_fill.md` records `is_unpaved` as a median-imputed GLM feature.

As with `lanes`, `todo/osm_features.md` contains an older/broader expectation
that `is_unpaved` might default to `False` for common road classes. The later
completed task text narrowed the finished work to speed-limit imputation.

### Current Code And Artefacts

Current code computes and uses `is_unpaved`:

- `src/road_risk/features/network.py` parses OSM `surface` into
  `is_unpaved`.
- `network_features.parquet` contains `is_unpaved` with 16.17% non-null
  coverage.
- `build_collision_dataset()` joins it through `net_features`.
- `train_collision_glm()` includes it as an optional candidate. In current
  metrics it appears as `is_unpaved_imputed` and `is_unpaved_missing`.
- `train_collision_xgb()` includes raw `is_unpaved`.
- `risk_scores.parquet` does not carry `is_unpaved`.

### Reconciliation

Under current model documentation, the `is_unpaved` flag matches documented
intent: accepted sparse OSM coverage with GLM imputation and XGBoost raw
handling. The audit flag is an OSM coverage correlation, not a known join-grain
bug.

If the older `default = False` plan is still desired, it remains unfinished and
should be documented as separate feature-engineering work. The current
production state does not depend on that defaulting scheme.

## `lit`

### Documented Plan Or Status

`lit` is documented as sparse OSM coverage, but not as a current trained Stage 2
model feature.

- `README.md` and `CODE_README.md` report `lit` at about 9.3% coverage and
  describe sparse OSM fields as imputed where retained.
- `quarto/analysis/osm-coverage.qmd` reports `lit` coverage by road class and
  notes very low coverage on minor/unknown classes.
- `quarto/methodology/model-inventory.qmd` explicitly says `lit` is present in
  `network_features.parquet` but is not currently in the trained feature list.
- `docs/notes/2026-04-19-deep-research-report-followup.md` says lighting needs
  better explicit provenance (`lit_explicit`, `lit_present`, `lit_source`) and
  true non-null coverage reporting before deciding on modelling.

Some older docs are looser. For example, `docs/internal/sites_todo.md` says OSM
features including `lit` feed the model, but the current model inventory is more
specific and says `lit` is not in the trained feature list.

### Current Code And Artefacts

Current code computes and joins `lit`, but does not model it:

- `src/road_risk/features/network.py` parses OSM `lit` into a nullable boolean
  column.
- `network_features.parquet` contains `lit` with 9.29% non-null coverage.
- `build_collision_dataset()` joins it because all network feature columns are
  merged into the Stage 2 base dataframe.
- `train_collision_glm()` does not list `lit` in `network_candidates`.
- `train_collision_xgb()` does not list `lit` in its optional features.
- `data/models/collision_metrics.json` confirms `lit` is absent from both
  trained feature lists.
- `risk_scores.parquet` does not carry `lit`.

### Reconciliation

The audit flag on `lit` is on a non-production Stage 2 dataframe column. It does
not contradict the current model plan, because `lit` is not currently used by
GLM or XGBoost.

The documented plan is not fully settled: the current inventory says it is not
modelled, while research notes recommend adding explicit lighting provenance
before any future modelling decision. Action is therefore not "fix join grain";
it is "decide separately whether lighting should become a production feature,
and if so add explicit provenance first."

## Overall Classification

### Fully Implemented / Accepted Coverage Limitation

- `lanes`
- `is_unpaved`

These are documented sparse OSM features. They are computed, joined, and used
as current model inputs (`*_imputed` plus missing flags in GLM, raw columns in
XGBoost). The audit flags are expected OSM coverage correlations.

### Partially Implemented / Replacement Exists Alongside Original

- `speed_limit_mph`

The intended production feature is `speed_limit_mph_effective`. The raw column
still exists as provenance and is intentionally not a trained feature. The audit
flag is therefore on the stale/provenance version, not on the production
replacement.

### Not A Current Production Feature

- `lit`

`lit` is computed and joined but not used by current trained Stage 2 models.
The audit flag is useful if the project later considers modelling lighting, but
it is not an active model-feature defect today.

### Not Implemented / Separate Future Work

- Defaulted `lanes` and defaulted `is_unpaved` from the older broad
  `todo/osm_features.md` plan are not implemented.
- OSM speed semantic hardening from the 2026-04-19 research note is not fully
  implemented; raw `speed_limit_mph` still comes through the current OSM
  extraction path. This is separate from the already implemented
  `speed_limit_mph_effective` replacement.

### No Documented Plan Found

No flagged feature lacked documentation. All four are covered by README/CODE
README, Quarto pages, model inventory, TODO records, or research notes.
