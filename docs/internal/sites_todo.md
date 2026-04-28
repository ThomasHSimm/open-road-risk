# Site TODO

Outstanding work on the public Quarto documentation site
(<https://thomashsimm.github.io/open-road-risk/>). Engineering work belongs
in `TODO.md` at the repo root.

Last reviewed: 2026-04-28.

## In progress

.

## Data Sources menu — coverage gaps

The current menu has 5 entries but the pipeline uses more sources than that.
Decide structure once MRDB is rewritten.

- **OpenStreetMap** has no page. OSM features (`speed_limit_mph`, `lanes`,
  `surface`, `lit`) feed the model and are documented in
  `analysis/osm-coverage.qmd`, but the source itself is not described in
  Data Sources. No `ingest_osm.py` exists; loading happens via `osmnx` and
  `osmium` per the README.
- **LSOA population + area** (ONS) is listed in the README data sources table
  but has no site page.
- **Decision needed:** add three new pages, or fold into existing structure?
  Three pages would mean the Data Sources menu grows from 5 to 8.

## Methodology chronology — modelling gap

The Methodology menu walks readers through the pipeline:
data-joining → Stage 1a → Stage 1b → feature engineering → EB shrinkage →
COVID handling. The actual modelling step is missing from this flow — Models
is a separate top-level menu. Readers reading chronologically jump from
Feature Engineering straight to Empirical Bayes Shrinkage with no model
introduction in between.

Two options:

- Add a brief "Modelling overview" page or section into Methodology that
  cross-references the Models menu.
- Restructure so Models lives inside Methodology rather than as a sibling
  top-level section.

No urgency — the site works as-is — but worth resolving when next editing
the navbar.

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

- **"Yorkshire" terminology is stale.** Filenames (`mrdb_yorkshire.parquet`,
  `openroads_yorkshire.parquet`), constants (`YORKSHIRE_BBOX_BNG`,
  `YORKSHIRE_BBOX`), and docstrings in `ingest_mrdb.py` /
  `ingest_openroads.py` still say Yorkshire. Actual study area is Northern
  and Central England (Midlands through Yorkshire). Resolve in code, not by
  writing carefully around it on the site. *This is also an entry on the
  engineering TODO, but flagging here because public pages reference these
  filenames.*
- **`methodology/data-joining.qmd` does not mention MRDB explicitly.**
  Once the MRDB page exists, add a one-line cross-reference in Stage 4
  (AADF → road links) noting MRDB's role.
- **`README.md` data sources table lists 7 sources; site has 5.** See
  "Data Sources menu — coverage gaps" above.

## Decisions to make

- **`docs/internal/family-definition-rationale.md`**: convert to a public
  ADR-style page (`docs/decisions/`) or keep internal? Audit flagged it as
  "Design History (ADR)". Already largely covered in
  `methodology/facility-family-split.qmd`, so the case for a separate public
  page is weak.
- **Notebooks (`docs/notes/*.ipynb`)**: leave in place, move to a
  `notebooks/` directory, or convert any to .qmd as supplemental analysis?
  Currently three notebooks (motorwayrisk, temporal_explore, webtris_explore),
  all 1000+ lines and not site-quality.
- **`docs/notes_notgit/*`**: three files (`note_24apr_1.md`, `_2.md`, `_3.md`)
  in a deliberately untracked directory. Confirm intent and document.

## Closed / done

- Added two orphaned `.qmd` files to navbar
  (`analysis/collision-exposure-behaviour.qmd`,
  `methodology/facility-family-split.qmd`). 2026-04-27.
- Restructured navbar so Methodology and Models no longer duplicate three
  pages. 2026-04-27.
- Cleaned commented-out `timezone-profile.qmd` reference under EDA.
  2026-04-27.

- **Replace MRDB stub page (`quarto/data-sources/mrdb.qmd`).** Current page is
  a placeholder. Needs honest description of MRDB's auxiliary role: AADF
  count-point linkage on the Major Road Network, distinct from OS Open Roads
  which provides the full network backbone. Verification underway on whether
  `count_point_id` is actually used as a join key downstream (see
  `clean_join/clean.py` and `clean_join/join.py`)

- **OS Open Roads** has no dedicated page despite being the primary network
  geometry (2.1M links). Currently mentioned only in passing in the MRDB stub
  and in `methodology/data-joining.qmd`. Source material: `ingest_openroads.py`
  docstring is substantial.
---

*Maintained alongside `docs/internal/Changelog_April_12_2026.md` and
`TODO.md`. Site changes that involve code (e.g. ingest renames) should be
cross-referenced from the engineering TODO.*