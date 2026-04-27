# Content Audit Report (Revised) — 2026-04-27

This audit provides a comprehensive evaluation of all documentation, research, and analysis files in the repository. It supersedes the previous audit by providing deeper content summaries, explicit overlap analysis, and evidence-based staleness verdicts.

---

## 1. Project-Level & Protected Files
These files are core to the repository's operation or agent tooling and are excluded from general reorganization.

| File | Content Summary | Status |
| :--- | :--- | :--- |
| `README.md` | • High-level project goal: predicting road collision risk.<br>• Installation and quickstart instructions.<br>• Overview of the multi-stage modelling pipeline. | **Protected** |
| `TODO.md` | • Active roadmap with explicit dependencies.<br>• Tracks Stage 1b (temporal) and Stage 2 (facility-split) tasks.<br>• Records engineering debt (e.g., latent leakage fix). | **Protected** |
| `CODE_README.md` | • Status tracker for individual Python modules.<br>• Engineering conventions (linting, testing, typing).<br>• Documentation of internal data flows and schema contracts. | **Protected** |
| `CLAUDE.md` | • Instructions for the AI agent (Gemini/Claude).<br>• Guidelines for using the `code-review-graph` MCP tools.<br>• Critical workflow reminders for codebase exploration. | **Protected** |
| `.claude/skills/*.md` | • Specialized agent instructions (e.g., `debug-issue.md`, `refactor-safely.md`).<br>• Encapsulates expert workflows for common engineering tasks. | **Protected** |
| `.gitignore` | • Standard Python/Node/Quarto ignore patterns.<br>• Explicitly ignores `docs/notes_notgit/` and build artifacts. | **Protected** |

---

## 2. Site Content (`quarto/`)
These files constitute the source code for the published documentation site. They are correctly placed in the `quarto/` directory.

### 2.1 Core Pages
*   **`quarto/index.qmd`**: Home page. Explains the project's disruptive goal (open data vs. proprietary ratings) and provides a visual map of the multi-stage pipeline.
*   **`quarto/future-work.qmd`**: Research extensions. Covers temporal disaggregation, junction-level modelling, weather integration, and AV-specific risk factors.

### 2.2 Data Sources
*   **`quarto/data-sources/stats19.qmd`**: Deep dive into DfT collision records. Covers the 2015-2024 filter rationale and coordinate quality findings.
*   **`quarto/data-sources/network-model-gdb.qmd`**: Technical specification of the OS Network Model. Explains road classification and functional hierarchy.
*   **`quarto/data-sources/aadf.qmd`**: Documentation of AADF traffic counts. Explains the sparse coverage on minor roads (62% within 2km).
*   **`quarto/data-sources/webtris.qmd`**: Documentation of National Highways sensor data. Covers the 15k site-year rows and their use in temporal profiling.
*   **`quarto/data-sources/mrdb.qmd`**: Brief overview of the Major Road Database. (Note: Currently a placeholder with minimal content).

### 2.3 Methodology
*   **`quarto/methodology/exposure-model.qmd`**: Stage 1a AADT estimation. Explains the use of OSM and network centrality to fill traffic gaps.
*   **`quarto/methodology/timezone-profile.qmd`**: Stage 1b temporal profiling. Covers the core-daytime vs. overnight fraction modelling.
*   **`quarto/methodology/data-joining.qmd`**: Spatial join technicals. Explains the 25m geometry densification and KD-tree snapping scoring.
*   **`quarto/methodology/feature-engineering.qmd`**: Comprehensive list of all model features. Covers network topology, OSM proxies, and RUC-based imputation.
*   **`quarto/methodology/empirical-bayes-shrinkage.qmd`**: Explains Stage 2 EB shrinkage. Details why link-year weighted dispersion was chosen over global-k.
*   **`quarto/methodology/facility-family-split.qmd`**: Outcome of the per-family modelling experiment. **Note:** Summarizes findings but references `docs/internal/family-definition-rationale.md` for full design history.
*   **`quarto/methodology/model-inventory.qmd`**: Canonical list of currently trained models and hyperparameters. Supersedes `reports/model_inventory.md`.
*   **`quarto/methodology/modelling.qmd`**: High-level overview of XGBoost vs. Poisson GLM. (Note: Short, needs expansion of actual model structure).
*   **`quarto/methodology/covid-handling.qmd`**: Rationale for including `is_covid` flag. (Note: Short, focused solely on the flag).

### 2.4 Analysis & Results
*   **`quarto/analysis/eda-collisions.qmd`**: Spatial and temporal EDA of STATS19 records. Identifies high-risk clusters and long-term trends.
*   **`quarto/analysis/eda-traffic.qmd`**: EDA of traffic volume. Correlates AADT with road class and urban/rural character.
*   **`quarto/analysis/road-curvature.qmd`**: Results of the curvature feature implementation. Demonstrates predictive lift on rural A-roads.
*   **`quarto/analysis/model-results.qmd`**: Main results page. Shows SHAP importance, pseudo-R² comparisons, and calibration curves.
*   **`quarto/analysis/collision_exposure_behaviour.qmd`**: Technical deep dive into sub-linear scaling (collisions ∝ AADT^0.8).
*   **`quarto/analysis/osm-coverage.qmd`**: Diagnostic of OSM tag sparsity. Justifies the use of median-imputed proxies for lanes and surface.
*   **`quarto/analysis/temporal-exploration.qmd`**: Exploratory results from Stage 1b. Justifies focusing on time-of-day rather than seasonality.
*   **`quarto/analysis/vehicle-mix.qmd`**: (Note: Nearly empty placeholder).

---

## 3. Internal Technical Docs (`docs/internal/`)
These files contain project rationale, technical workarounds, and internal changelogs.

| File | Content Summary | Status |
| :--- | :--- | :--- |
| `aadt_geometry_issue.md` | • Documents a BNG projection failure (EPSG:27700) returning non-finite coordinates.<br>• Details the local Proj-based Transverse Mercator fallback.<br>• Lists conditions for re-evaluating the workaround. | **Internal Technical Note** |
| `data-quality-notes.md` | • Log of data quality audits (STATS19, AADF, WebTRIS).<br>• Evidence-based denial of the "grid-letter error" theory in STATS19.<br>• Documentation of the LSOA-centroid coordinate validation method. | **Technical Appendix** |
| `family-definition-rationale.md` | • Decision record for the four-family split (Motorway, Trunk, Urban, Rural).<br>• Detailed "why not" reasoning for rejected splits (e.g., `form_of_way`, `is_primary`).<br>• **Overlap:** Logic is summarized in `quarto/methodology/facility-family-split.qmd`, but this doc is the primary decision history. | **Decision Record** |
| `temporal_changes_plan.md` | • Roadmap for Stage 1b implementation.<br>• Design for an ablation study to test "link-shape descriptors" as model features.<br>• Supersedes `docs/notes/temporal_plan_raw_ideas.md`. | **Active Roadmap** |
| `Changelog_April_12_2026.md`| • High-level summary of study area expansion (Yorkshire + NW England).<br>• Records the refactor of `model.py` into the `road_risk.model` package. | **Archival Record** |

---

## 4. Research & Analysis Notes (`docs/notes/`)
These files capture deep research experiments, validation strategies, and exploratory analysis.

| File | Content Summary | Status |
| :--- | :--- | :--- |
| `2026-04-19-deep-research-report.md` | • Critical codebase audit covering latent leakage and citation errors.<br>• Corrects author names for key road safety papers.<br>• Recommends the four-arm ablation for OSM/Family-split experiments. | **Audit / Roadmap** |
| `deep-research-roadcurvature.md` | • Research into curvature-risk relationship in UK road safety literature.<br>• Implementation plan using interior turning-angle density (deg/km).<br>• Reference script for resampling LineStrings at 15m intervals. | **Research Implementation** |
| `deep-research-terrain50.md` | • Research into OS Terrain 50 as a source for vertical grade features.<br>• Strategy for handling bridges and tunnels via endpoint fallback.<br>• Technical warning against using nearest-neighbor sampling on 50m DEMs. | **Research Plan** |
| `duckdb-wasm-workflow.md` | • Strategic plan for deploying a zero-cost, high-performance web app.<br>• Outlines a pipeline to output spatially sorted Parquet for DuckDB-Wasm.<br>• Explains the use of HTTP Range Requests for remote querying. | **Technical Workflow** |
| `evaluation_ideas.md` | • Proposals for model validation: future-year holdout (2015-21 train / 2022-24 test).<br>• Naive baseline comparison (`AADT * length`) to isolate ML value-add.<br>• FOI strategies for independent traffic ground-truth data. | **Validation Strategy** |
| `geo-data-hosting-guide.md`| • Guide for hosting large geo-Parquet files on GitHub Releases or S3.<br>• Explains the "S3-as-database" paradigm for web-based GIS. | **Technical Workflow** |
| `2026-04-19-deep-research-report-followup.md` | • Follow-up to the 19 April audit, refining experiment priorities. | **Active Note** |
| `deep-research-report-validation.md` | • Validation of repo updates against research findings. | **Active Note** |
| `temporal_plan_raw_ideas.md`| • Early raw brainstorming for temporal features.<br>• **Verdict:** Stale. Superseded by `docs/internal/temporal_changes_plan.md`. | **Stale** |

### 4.1 Exploratory Notebooks
These notebooks are large (1200–2000 lines) and primarily scratchpads for initial data exploration.
*   **`docs/notes/motorwayrisk.ipynb`**: Investigates the under-prediction bias of the global model on motorway links.
*   **`docs/notes/temporal_explore.ipynb`**: Early exploration of WebTRIS seasonality and day-of-week patterns.
*   **`docs/notes/webtris_explore.ipynb`**: Initial characterization of the WebTRIS sensor network.

---

## 5. Quantitative Reports (`reports/`)
These files are technical artifacts documenting the results of specific modelling runs or data cleaning operations.

| File | Content Summary | Verdict |
| :--- | :--- | :--- |
| `eb_dispersion.md` | • Results of method-of-moments (MoM) estimation for dispersion k.<br>• Shows 3400x variation in k across the risk range, justifying non-constant dispersion. | **Active Validation** |
| `eb_validation.md` | • Comparison of XGBoost rank vs. EB-shrunk rank.<br>• Identifies links that "entered" or "left" the top-1% risk set after shrinkage. | **Active Validation** |
| `family_validation.md` | • Comparative results of per-family vs. global modelling.<br>• Reports +0.007 pseudo-R² gain on motorways and significantly improved residuals. | **Active Validation** |
| `rank_stability.md` | • Multi-seed (5 seeds) evaluation of rank stability.<br>• Reports mean Spearman correlation of 0.998 and mean top-1% Jaccard of 0.918. | **Active Validation** |
| `rank_stability_investigation.md` | • Deep dive into why top-1000 Jaccard is lower than top-10000.<br>• Rules out predicted-risk clustering as the cause. | **Diagnostic Report** |
| `ruc_fill.md` | • Characterization of the 15.5% LSOA-feature gap.<br>• Documentation of the spatial-join (within 5km) and rural-default fallback fill. | **Data Characterization** |
| `ruc_fill_verification.md` | • Verification of the RUC fill impact on Stage 2 training.<br>• Confirms that 99% of filled links land in the correct rural/urban category. | **Verification** |
| `ruc_null_characterisation.md`| • Detailed breakdown of road functions and form-of-way for no-LSOA links. | **Redundant with `ruc_fill.md`** |
| `speed_limit_effective_verification.md` | • 1140-line list of specific links and their imputed speed limits.<br>• Used for manual spot-checking against OSM during implementation. | **Artifact** |
| `stage2_base_table_investigation.md` | • Investigation into the composition of the 21.7M row training table. | **Diagnostic Report** |
| `temporal_findings.md` | • Key finding: weekday/weekend and seasonal variation is global, not link-specific.<br>• Recommends focusing solely on time-of-day link descriptors. | **Key Research Finding** |
| `model_inventory.md` | • List of model features and training row counts.<br>• **Verdict:** Stale/Redundant. Completely covered by `quarto/methodology/model-inventory.qmd`. | **Stale** |

---

## 6. Overlap & Redundancy Analysis

### 6.1 `reports/model_inventory.md` vs. `quarto/methodology/model-inventory.qmd`
*   **Content:** Both files provide training row counts (e.g., ~17.3M XGBoost train rows), feature lists, and metrics (pseudo-R² 0.857).
*   **Overlap:** 95% identical. The Quarto version includes additional hyperparameters (`max_depth=6`, `learning_rate=0.05`) and a "Comparability caveat" section not present in the report.
*   **Verdict:** `reports/model_inventory.md` is **redundant** and can be deleted.

### 6.2 `docs/internal/family-definition-rationale.md` vs. `quarto/methodology/facility-family-split.qmd`
*   **Content:** The internal doc explains *why* certain splits were rejected (e.g., "Why not add is_primary"). The Quarto page explains the *outcome* and "why not to adopt" the v1 split for production yet.
*   **Overlap:** Significant overlap in the "Family definitions" table. However, the internal doc holds the "Decision Record" (ADR) value that is too detailed for a site methodology page.
*   **Verdict:** Keep both, but move `family-definition-rationale.md` to a dedicated `docs/decisions/` folder.

### 6.3 `reports/ruc_null_characterisation.md` vs. `reports/ruc_fill.md`
*   **Content:** `ruc_fill.md` incorporates the characterization tables from `ruc_null_characterisation.md` into its Stage 1 section.
*   **Verdict:** `ruc_null_characterisation.md` is **redundant**.

---

## 7. Re-evaluation of Previous Recommendations

1.  **Bulk `reports/` → `docs/reports/` recommendation:** This recommendation is **retracted**. The current `reports/` folder acts as an "Artifacts" directory for quantitative validation outputs, which is a standard data science practice. Moving them to `docs/` implies they are prose documentation, which they are not.
2.  **`docs/internal/aadt_geometry_issue.md` to `quarto/`**: This is **retracted**. This is a niche environment-specific technical note (reproducible on some machines, not others). It is not core methodology for users and should remain internal.
3.  **Expand `modelling.qmd` and `covid-handling.qmd`**: These recommendations are **retracted**. While short, they are focused and serve their purpose. Content gaps should be addressed as part of research tasks, not as a documentation cleanup operation.

---

## 8. Summary of Proposed Actions

1.  **Delete Stale/Redundant Files:**
    *   `reports/model_inventory.md`
    *   `reports/ruc_null_characterisation.md`
    *   `docs/notes/temporal_plan_raw_ideas.md`
2.  **Rename/Move Research Notes:**
    *   Move `.ipynb` files from `docs/notes/` to `notebooks/exploratory/`.
    *   Move `docs/internal/family-definition-rationale.md` to `docs/decisions/`.
    *   Rename `docs/notes/` to `docs/research/` to better reflect content (deep-dive plans vs. scratch work).
3.  **Archive Technical Guides:**
    *   Move `duckdb-wasm-workflow.md` and `geo-data-hosting-guide.md` to `docs/technical/`.
4.  **Local Stash:**
    *   Explicitly maintain `docs/notes_notgit/` as a local-only stash (already ignored).

---
*Report generated by Gemini CLI.*
