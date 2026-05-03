## 🟢 Infrastructure / Output

- [ ] `db.py` — PostGIS loader for all processed parquets + model outputs. Required
  for Streamlit app queries.

- [ ] Streamlit app skeleton — map with road links coloured by risk percentile,
  sidebar filters for road type / year / severity.

- [ ] GeoPackage export — ESRI-compatible output layer (link_id, geometry,
  estimated_aadt, risk_percentile, road_classification). Useful.

- [ ] `data/README.md` — download instructions for all large raw files not in git
  (STATS19 CSV, OS Open Roads GeoPackage, AADF zip, OSM pbf files, MRDB).

- [ ] Add "Related work / where this fits" page — short, written from
  your perspective with verified citations. Position project relative
  to Lovelace / Leeds ITS active travel work, any UK SPF-style work
  surfaced by OS conversation, and proprietary commercial work. Wait
  until after OS contact response so the page reflects specific
  references rather than generic ecosystem framing.

- [ ] Kaggle dataset — upload processed parquets so others can skip ingest/clean/snap.

- [ ] Provenance directory restructure (small session) — move
  `curvature_provenance.json`, `ruc_provenance.json`,
  `speed_limit_effective_provenance.json` from `data/features/` to
  `data/provenance/`. Update code paths that write these. gitignore
  already allow-lists the directory.

- [ ] Minimal CI workflow — add GitHub Actions for PRs and pushes to `main`
  running `pytest -x --tb=short` and `ruff check`. Do not run the full
  pipeline in CI: it is too slow and depends on raw data not stored in git.

- [ ] `config/model.yaml` migration — split model/runtime constants out of
  `config/settings.yaml`. Create `config/model.yaml`, migrate
  `RANDOM_STATE = 42` and `COVID_YEARS = {2020, 2021}`, and update
  `config.py` to load both YAML files with consistent fail-loud errors.
  `clean.py` currently reads COVID years from `cfg["years"]["covid"]`;
  after migration, `model/constants.py` should become the canonical model-side
  source.

- [ ] Add argparse to pipeline entrypoints — `python -m road_risk.<module> --help`
  should print usage rather than running the pipeline. Cover entrypoints in
  `clean_join/`, `ingest/`, `model/`, and `features/`; support `--help`,
  `--dry-run`, and module-specific arguments.

- [ ] Fix STATS19 expected-column validation timing — `ingest_stats19.py`
  currently warns that `collision_date` is missing because `EXPECTED_COLS`
  uses post-rename names while validation runs before rename. Either validate
  pre-rename names (`date`) or move validation after rename. Low priority:
  warning only, no current breakage.

- [ ] Add smoke tests for ingest/clean/model modules — current tests mainly
  cover feature engineering. Add synthetic-fixture tests for
  `ingest_stats19.load_stats19()` and clean/model entrypoints so config/path
  refactors do not rely only on manual end-to-end runs. Keep tests fast and
  CI-compatible; avoid real raw-data dependencies.

- [ ] Force-area vs bbox coverage audit — current STATS19 filtering combines
  `police_force` membership with coordinate bbox clipping. Audit listed force
  areas against `study_area.bbox_wgs84`, identify partially clipped forces
  such as Cheshire/Lincolnshire if present, and either expand the bbox or
  document intentional partial coverage. Force boundaries are available from
  data.police.uk.

- [ ] Derive `bbox_bng` from `bbox_wgs84` — settings currently stores both
  coordinate systems by hand, creating drift risk. Keep one source of truth
  (probably WGS84) and derive BNG bounds in code via `pyproj`. Low priority:
  current values work, but this is config hygiene.

- [ ] Add YAML schema validation when config complexity justifies it — use
  Pydantic for `settings.yaml` and future `config/model.yaml` once settings
  exceeds ~100 lines or after the next config-related debugging session.
  Below that threshold, schema overhead likely outweighs benefit.

- [ ] Logger integration and print triage — `road_risk.utils.logger` now supports
  file logging under `_ROOT/logs/`, but entrypoints still mostly use local
  `logging.basicConfig()` and many run summaries use `print()`. Decide which
  prints are CLI-only versus run diagnostics, then route important summaries
  through the logger.


---

## 🔵 Applications / Demonstrations

- [ ] Risk-normalised output table — "Top 1% highest-risk road segments controlling
  for traffic" as a clean publishable output.

