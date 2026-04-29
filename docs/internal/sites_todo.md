# Site TODO

Outstanding work on the public Quarto documentation site
(<https://thomashsimm.github.io/open-road-risk/>). Engineering work belongs
in `TODO.md` at the repo root.

Last reviewed: 2026-04-28.

## In progress

*(none — see Closed for this session's work)*

## Data Sources menu — coverage gaps

- **OpenStreetMap** has no page. OSM features (`speed_limit_mph`, `lanes`,
  `surface`, `lit`) feed the model and are documented in
  `analysis/osm-coverage.qmd`, but the source itself is not described in
  Data Sources. No `ingest_osm.py` exists; loading happens via `osmnx` and
  `osmium` per the README. Drafting requires pointer to actual loading code.
- **LSOA population + area** (ONS) is listed in the README data sources table
  but has no site page. Lower priority — population density features are
  derived from this, but the source description would be brief.

## Validation content — potential new subsection

Three validation reports in `reports/` contain site-worthy content currently
not on the site:

- `reports/eb_validation.md` — quantifies impact of EB shrinkage on motorway
  ranks, top-1% intersection.
- `reports/family_validation.md` — per-family modelling gains and held-out
  reversal warning.
- `reports/rank_stability.md` — Spearman 0.998 and Jaccard 0.918 across seeds.

These are working reports, not site-ready prose. Adapting them into a
Methodology > Validation subsection (or appending to relevant existing pages)
would close a credibility gap — the site explains *how* EB and the family
split work but doesn't show *that* they produced the claimed effects. Real
work, not just relocation.

## Documentation/code mismatches to resolve

- **"Yorkshire" terminology is stale.** Several backwards-compat constants,
  WebTRIS/MRDB names, and app module names still say Yorkshire. Actual study
  area is Northern and Central England. Resolve in code, not by writing
  carefully around it on the site. Cross-listed in `TODO.md`.
- **`methodology/data-joining.qmd` does not mention OS Open Roads as the
  geometry backbone explicitly.** Could add a one-line cross-reference now
  that the OS Open Roads source page exists. Low priority.
- **`README.md` data sources table.** MRDB row has been removed. OSM and LSOA
  rows still listed without dedicated site pages — see "Coverage gaps" above.

## Decisions to make

- **`docs/internal/family-definition-rationale.md`**: convert to a public
  ADR-style page (`docs/decisions/`) or keep internal? Already largely
  covered in `methodology/facility-family-split.qmd`, so the case for a
  separate public page is weak. Lean toward keeping internal.
- **Notebooks (`docs/notes/*.ipynb`)**: leave in place, move to a
  `notebooks/` directory, or convert any to .qmd as supplemental analysis?
  Currently three notebooks (motorwayrisk, temporal_explore, webtris_explore),
  all 1000+ lines and not site-quality.
- **`docs/notes_notgit/*`**: three files (`note_24apr_1.md`, `_2.md`, `_3.md`)
  in a deliberately untracked directory. Confirm intent and document.
- **Stage 2 page rename**: `analysis/model-results.qmd` is functionally the
  Stage 2 model page, not just a results page. Renaming to
  `methodology/stage2-collision.qmd` would be more honest but triggers
  cross-reference updates. Navbar label has been updated; file rename
  deferred.

## Future drafts

- Year encoding section. The modelling overview deliberately omits year
  handling because the actual encoding wasn't verified against
  `model/collision.py`. Worth adding once confirmed.
- Stage 2 hyperparameter / training detail. Currently distributed across
  `model-results.qmd`, `model-inventory.qmd`, and `CODE_README.md`.
  Consolidation would help.

## Closed / done

**2026-04-28 session:**

- Removed MRDB from public site (page deleted, navbar entry removed) after
  code investigation confirmed `mrdb_clean.parquet` is produced but never
  consumed downstream. MRDB is functionally orphaned. Engineering follow-up
  added to `TODO.md`.
- Removed MRDB row from `README.md` data sources table.
- Added new OS Open Roads data source page (`quarto/data-sources/openroads.qmd`)
  with substantive content drawn from `ingest_openroads.py`.
- Restructured Methodology and Models menus. Stage 1a (exposure model) and
  Stage 1b (timezone profile) moved from Methodology to Models so all three
  pipeline stages live together. Methodology now covers data-joining,
  feature engineering, and EB shrinkage.
- Removed `covid-handling.qmd` from the site — page was a placeholder with
  little to add. COVID handling is a one-line decision that fits inline
  elsewhere if needed.
- Added Methodology landing page (`methodology/index.qmd`) explaining the
  Methodology vs Models distinction and listing pages in the section.
- Replaced empty `modelling.qmd` stub with substantive Models landing page
  covering the three-stage pipeline at orientation level.
- Renamed Models menu entry "Model Results & SHAP" → "Stage 2: Collision
  Risk Model" to reflect that the page is actually the Stage 2 model
  documentation, not a downstream interpretation page.

**2026-04-27:**

- Added two orphaned `.qmd` files to navbar
  (`analysis/collision-exposure-behaviour.qmd`,
  `methodology/facility-family-split.qmd`).
- Cleaned commented-out `timezone-profile.qmd` reference under EDA.

---

*Maintained alongside `docs/internal/Changelog_April_12_2026.md` and
`TODO.md`. Site changes that involve code (e.g. ingest renames) should be
cross-referenced from the engineering TODO.*
