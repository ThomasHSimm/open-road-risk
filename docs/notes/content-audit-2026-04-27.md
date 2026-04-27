# Content Audit Report - 2026-04-27

## 1. Site Framework and Conventions
The repository uses **Quarto** as its site framework.
- **Source Files:** Primarily `.qmd` files located in the `quarto/` directory.
- **Structure:** Defined in `quarto/_quarto.yml`. It includes sections for Data Sources, Methodology, Exploratory Data Analysis, and Models.
- **Output:** Rendered to `quarto/_site/` (git-ignored).
- **Conventions:** 
    - Published content lives in `quarto/`.
    - Internal plans and rationale live in `docs/internal/`.
    - Deep research and exploratory notes live in `docs/notes/`.
    - Validation and characterisation reports live in `reports/`.

## 2. Protected Files
These files are conventionally kept in place and should be excluded from reorganization:
- `README.md`: Main project overview.
- `TODO.md`: Project roadmap and task tracker.
- `CODE_README.md`: Module status and engineering conventions tracker.
- `.gitignore`: Git exclusion rules.
- `quarto/_quarto.yml`: Quarto site configuration.
- `docs/internal/Changelog_April_12_2026.md`: Specific session changelog.

---

## 3. Audit Table

| Path | Summary | Length (Lines) | Last Modified | Classification | Recommended Action | Confidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `quarto/index.qmd` | Home page of the site, explaining project goals and pipeline stages. | 108 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/future-work.qmd` | Detailed list of future research questions and extensions. | 405 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/analysis/temporal-exploration.qmd` | Analysis of months, days, and time-of-day traffic patterns. | 238 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/analysis/road-curvature.qmd` | Analysis of road curvature features and their impact. | 437 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/analysis/eda-collisions.qmd` | Exploratory data analysis of collision records. | 349 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/analysis/model-results.qmd` | Summary of model performance and SHAP importance. | 453 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/analysis/vehicle-mix.qmd` | Placeholder or brief analysis of vehicle mix. | 19 | 2026-04-27 | site content (correctly placed) | Expand or merge with other EDA. | Medium |
| `quarto/analysis/osm-coverage.qmd` | Evaluation of OSM attribute coverage across the network. | 110 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/analysis/collision_exposure_behaviour.qmd` | Deep dive into sub-linear exposure scaling and speed/severity. | 292 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/analysis/eda-traffic.qmd` | Exploratory data analysis of traffic volume counts. | 469 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/methodology/modelling.qmd` | Overview of the modelling approach (XGBoost/Poisson). | 21 | 2026-04-27 | site content (correctly placed) | Expand content. | Medium |
| `quarto/methodology/covid-handling.qmd` | Strategy for handling traffic anomalies during 2020-2021. | 20 | 2026-04-27 | site content (correctly placed) | Expand content. | Medium |
| `quarto/methodology/facility-family-split.qmd` | Rationale for splitting models by road facility family. | 636 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/methodology/model-inventory.qmd` | List of models currently used in the pipeline. | 152 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/methodology/timezone-profile.qmd` | Methodology for Stage 1b time-zone traffic profiles. | 267 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/methodology/exposure-model.qmd` | Methodology for Stage 1a AADT estimation. | 372 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/methodology/empirical-bayes-shrinkage.qmd` | Methodology for Empirical Bayes shrinkage in Stage 2. | 780 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/methodology/feature-engineering.qmd` | Overview of network and contextual feature engineering. | 591 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/methodology/data-joining.qmd` | Technical details on spatial joins and snapping. | 469 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/data-sources/mrdb.qmd` | Source page for the Major Road Database. | 26 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/data-sources/aadf.qmd` | Source page for AADF traffic counts. | 289 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/data-sources/network-model-gdb.qmd` | Source page for the OS Network Model GeoPackage. | 1177 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/data-sources/webtris.qmd` | Source page for WebTRIS sensor data. | 697 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/data-sources/stats19.qmd` | Source page for STATS19 collision records. | 739 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `quarto/api-reference/index.qmd` | Entry point for code and module documentation. | 20 | 2026-04-27 | site content (correctly placed) | Keep in place. | High |
| `docs/internal/aadt_geometry_issue.md` | Tech note on EPSG:27700 projection issues and workarounds. | 92 | 2026-04-21 | site content (misplaced) | Move to `quarto/methodology/` as a technical appendix. | High |
| `docs/internal/data-quality-notes.md` | Log of data quality issues (STATS19, AADF, WebTRIS). | 172 | 2026-04-22 | site content (misplaced) | Move to `quarto/methodology/` or link from data source pages. | High |
| `docs/internal/family-definition-rationale.md` | Deep dive into facility family definitions for Stage 2. | 236 | 2026-04-25 | site content (misplaced) | Move to `quarto/methodology/` (mostly redundant with `facility-family-split.qmd`). | High |
| `docs/internal/temporal_changes_plan.md` | Strategy for incorporating temporal features into models. | 227 | 2026-04-27 | working notes / drafts | Keep in `docs/plans/` or similar. | High |
| `docs/notes/2026-04-19-deep-research-report.md` | Comprehensive research report on repo status and experiments. | 271 | 2026-04-22 | working notes / drafts | Archive after tasks are completed. | High |
| `docs/notes/2026-04-19-deep-research-report-followup.md` | Follow-up to the deep research report. | 299 | 2026-04-21 | working notes / drafts | Archive after tasks are completed. | High |
| `docs/notes/deep-research-report-validation.md` | Validation of repo updates against research findings. | 186 | 2026-04-22 | working notes / drafts | Archive after tasks are completed. | High |
| `docs/notes/deep-research-roadcurvature.md` | Research and implementation plan for road curvature. | 344 | 2026-04-21 | working notes / drafts | Archive after implementation (already in `quarto/analysis/road-curvature.qmd`). | High |
| `docs/notes/deep-research-terrain50.md` | Research and implementation plan for road terrain/grade. | 559 | 2026-04-21 | working notes / drafts | Keep as reference for future grade implementation. | High |
| `docs/notes/duckdb-wasm-workflow.md` | Notes on using DuckDB-Wasm for web-based analysis. | 63 | 2026-04-25 | working notes / drafts | Move to `docs/technical/`. | High |
| `docs/notes/evaluation_ideas.md` | Ideas for internal and independent model validation. | 87 | 2026-04-22 | site content (misplaced) | Move to `quarto/analysis/evaluation-strategy.qmd`. | High |
| `docs/notes/geo-data-hosting-guide.md` | Guide for hosting geospatial data for the web app. | 32 | 2026-04-25 | working notes / drafts | Move to `docs/technical/`. | High |
| `docs/notes/temporal_plan_raw_ideas.md` | Initial raw ideas for temporal features. | 64 | 2026-04-26 | stale / redundant | Delete (superceded by `temporal_changes_plan.md`). | High |
| `docs/notes/motorwayrisk.ipynb` | Exploratory analysis of motorway risk. | 1834 | 2026-04-26 | working notes / drafts | Move to `notebooks/exploratory/`. | High |
| `docs/notes/temporal_explore.ipynb` | Exploratory analysis of temporal patterns. | 1231 | 2026-04-27 | working notes / drafts | Move to `notebooks/exploratory/`. | High |
| `docs/notes/webtris_explore.ipynb` | Exploratory analysis of WebTRIS sensor data. | 2035 | 2026-04-27 | working notes / drafts | Move to `notebooks/exploratory/`. | High |
| `reports/eb_dispersion.md` | Report on Empirical Bayes dispersion estimation. | 51 | 2026-04-25 | working notes / drafts | Move to `docs/reports/` or include in site as appendix. | High |
| `reports/eb_validation.md` | Validation results for EB shrinkage. | 153 | 2026-04-25 | working notes / drafts | Move to `docs/reports/` or include in site as appendix. | High |
| `reports/family_validation.md` | Validation results for facility-family split models. | 167 | 2026-04-26 | working notes / drafts | Move to `docs/reports/` or include in site as appendix. | High |
| `reports/model_inventory.md` | Detailed inventory of models (redundant with `quarto`). | 112 | 2026-04-24 | stale / redundant | Delete (superceded by `quarto/methodology/model-inventory.qmd`). | High |
| `reports/rank_stability.md` | Analysis of rank stability across different model seeds. | 69 | 2026-04-25 | working notes / drafts | Move to `docs/reports/`. | High |
| `reports/rank_stability_investigation.md` | Detailed investigation into Jaccard non-monotonicity. | 57 | 2026-04-25 | working notes / drafts | Move to `docs/reports/`. | High |
| `reports/ruc_fill.md` | Report on RUC fill methodology and results. | 175 | 2026-04-25 | working notes / drafts | Move to `docs/reports/`. | High |
| `reports/ruc_fill_verification.md` | Verification of RUC fill accuracy. | 98 | 2026-04-25 | working notes / drafts | Move to `docs/reports/`. | High |
| `reports/ruc_null_characterisation.md` | Characterisation of links with null RUC values. | 100 | 2026-04-25 | working notes / drafts | Move to `docs/reports/`. | High |
| `reports/speed_limit_effective_verification.md` | Verification of effective speed limit imputation. | 1140 | 2026-04-24 | working notes / drafts | Move to `docs/reports/`. | High |
| `reports/stage2_base_table_investigation.md` | Investigation into the Stage 2 training table composition. | 382 | 2026-04-23 | working notes / drafts | Move to `docs/reports/`. | High |
| `reports/temporal_findings.md` | Summary of findings from temporal analysis. | 213 | 2026-04-27 | working notes / drafts | Move to `docs/reports/`. | High |

---

## 4. Folder Structure Assessment
The current folder structure successfully separates the **published site content** (`quarto/`) from the **internal development documents** (`docs/`, `reports/`).

### Strengths:
- **Clean Site Source:** `quarto/` is dedicated to the website, making it easy to manage what is public.
- **Categorisation:** `docs/internal/` and `docs/notes/` separate high-level plans from deep-dive research.

### Weaknesses:
- **Redundancy:** Several files in `docs/` and `reports/` contain content that has already been promoted to the site or superceded by newer plans (e.g., `model_inventory.md`, `temporal_plan_raw_ideas.md`).
- **Ambiguous Boundaries:** The distinction between `docs/notes/` and `reports/` is blurry. `reports/` tends to be more quantitative validation, but many "notes" are also quantitative.
- **Notebook Placement:** `.ipynb` files are mixed with markdown notes in `docs/notes/`.

---

## 5. Proposed Structure
To improve clarity and maintainability, I propose the following structure:

```text
.
├── quarto/               # STAYS: Published site source (qmd)
├── docs/
│   ├── plans/           # High-level plans and roadmap documents
│   ├── research/        # Deep research reports (former docs/notes/*.md)
│   ├── reports/         # Quantitative validation reports (former reports/*.md)
│   ├── technical/       # Technical guides and workflow notes (e.g. duckdb, hosting)
│   └── internal/        # STAYS: Core project rationale and changelogs
├── notebooks/
│   ├── exploratory/     # Scratchpads and initial research (former docs/notes/*.ipynb)
│   └── validation/      # Notebooks generating the reports
└── [Protected Files]    # README.md, TODO.md, etc.
```

---

## 6. Unclear Files & Questions
The following files are flagged for clarification before any cleanup:

1. **`quarto/analysis/collision_exposure_behaviour.qmd` vs `docs/internal/family-definition-rationale.md`**: Much of the rationale in the internal doc is now reflected in the site. Is the internal doc still needed as a "decision record", or can it be safely archived?
2. **`reports/speed_limit_effective_verification.md`**: This is a very large file (1140 lines). Is this intended to be a permanent record, or was it a one-off diagnostic for a specific commit?
3. **`docs/notes/motorwayrisk.ipynb`**: This notebook is over 1800 lines. Does it contain stable analysis that should be converted to a `.qmd` page, or is it purely scratch work?
4. **`quarto/analysis/vehicle-mix.qmd`**: Currently almost empty (19 lines). Should this be prioritised for content, or merged into `quarto/methodology/timezone-profile.qmd`?

---
*Report generated by Gemini CLI.*
