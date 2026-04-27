# Content Audit Report (High-Fidelity) — 2026-04-27

This audit provides an exhaustive, granular evaluation of all documentation, research, and analysis files in the repository. It identifies specific technical claims, methodology details, and concrete evidence for overlap or staleness.

---

## 1. Project-Level & Protected Files
These files are the "connective tissue" of the repository and are excluded from reorganization.

| File | High-Fidelity Content Detail | Status |
| :--- | :--- | :--- |
| `README.md` | • **Pipeline Architecture:** Defines the 3-stage flow (1a: AADT, 1b: Temporal, 2: Collision Risk).<br>• **Dataset Registry:** Lists STATS19, AADF, WebTRIS, and OS Open Roads as primary inputs.<br>• **Engineering Pillars:** Emphasizes reproducibility, modular Python components, and Quarto-based reporting. | **Protected** |
| `TODO.md` | • **Active Dependencies:** Tracks the link between Stage 1b completion and Stage 2 temporal integration.<br>• **Critical Fixes:** Includes the "latent leakage" fix (removing collision context from Stage 2 train table).<br>• **Backlog:** Mentions future Met Office weather integration and area-level SHAP analysis. | **Protected** |
| `CODE_README.md` | • **Module Status:** Binary tracker (Live/Stale/Beta) for every file in `src/road_risk/`.<br>• **Schema Contracts:** Defines expected column types for `risk_scores.parquet` and `network_features.parquet`.<br>• **Tooling:** Documents the use of `ruff` for linting and `pytest` for validation. | **Protected** |
| `CLAUDE.md` | • **Graph Tools:** Instructions for `detect_changes` and `query_graph` to maintain structural integrity.<br>• **Context Policy:** Mandates checking for existing tests before every refactor.<br>• **Architecture:** Defines the `src/` layout and the `road_risk` package structure. | **Protected** |
| `.claude/skills/` | • `debug-issue.md`: Process for isolating BNG projection errors.<br>• `refactor-safely.md`: Checklists for splitting large modules (e.g., the `model.py` refactor).<br>• `review-changes.md`: Standards for PR reviews, focusing on test coverage and schema drift. | **Protected** |

---

## 2. Quarto Site Content (`quarto/`)
The primary source for the public-facing documentation.

### 2.1 Methodology Deep-Dives
*   **`quarto/methodology/empirical-bayes-shrinkage.qmd`**:
    *   • **The Mechanism:** Explains the weighted average of the XGBoost prior and observed collision counts.
    *   • **The "k" Finding:** Details why a global k ≈ 3.07 (positive-event weighted) was chosen over the MoM weighted k ≈ 146.
    *   • **Operational Shift:** Notes that EB moves motorway links with zero collisions *down* in rank and high-observation A-roads *up*.
*   **`quarto/methodology/feature-engineering.qmd`**:
    *   • **Feature Taxonomy:** Categorizes features into Network (betweenness, degree), Geometry (curvature, length), and Context (population density, RUC).
    *   • **Imputation Logic:** Documents the median-imputation for OSM `lanes` and `surface` due to <20% coverage.
    *   • **Pseudo-R² Caveat:** Explains why GLM (0.25) and XGBoost (0.86) metrics are not directly comparable due to different null models.
*   **`quarto/methodology/exposure-model.qmd`**:
    *   • **Stage 1a Logic:** Uses a Random Forest regressor to estimate AADT for links without AADF count points.
    *   • **Validation:** Reports a CV R² of 0.72 for the traffic exposure model.
    *   • **Data Filter:** Explicitly notes that DfT "Estimated" counts are excluded to prevent training on government guesses.

### 2.2 Analysis & Results
*   **`quarto/analysis/model-results.qmd`**:
    *   • **Visuals:** Includes SHAP summary plots, GLM coefficient bar charts (IRRs), and residual histgrams.
    *   • **Key Findings:** Confirms XGBoost's 3x predictive lift over GLM on the link-year training set.
    *   • **Residuals:** Identifies "Excess Risk" links (residual > 2) as candidates for engineering audit.
*   **`quarto/analysis/road-curvature.qmd`**:
    *   • **Methodology:** Explains LineString resampling at 15m intervals and turning-angle density (deg/km) calculation.
    *   • **Quality Gate:** Details the 40 vertices/km median threshold required for road classes to be eligible for curvature features.
    *   • **Findings:** Demonstrates that curvature is a significant predictor in rural Poisson models.
*   **`quarto/analysis/temporal-exploration.qmd`**:
    *   • **Seasonality:** Finds that 30% winter-to-summer traffic swings are global across all road classes.
    *   • **Time-of-Day:** Proves that `core_overnight_ratio` varies significantly by link, justifying link-level profiling.
    *   • **HGV Artefact:** Explains that the summer drop in HGV% is due to passenger traffic dilution, not a drop in freight volume.

---

## 3. Internal Technical Docs (`docs/internal/`)

| File | Granular Content Detail | Verdict |
| :--- | :--- | :--- |
| `aadt_geometry_issue.md` | • **The Bug:** `pyproj` returns `inf` for BNG projections on certain Linux environments.<br>• **The Workaround:** A local Transverse Mercator fallback (`+proj=tmerc`) ensuring Stage 1a snapping continues.<br>• **Validation:** Confirms fallback snap distances are within 0.1m of EPSG:27700. | **Technical Debt Record** |
| `data-quality-notes.md` | • **STATS19 Audit:** Proves lat/lon fields match BNG easting/northing within 2.5m for Yorkshire forces.<br>• **LSOA Validation:** Sets a 10km haversine threshold to flag "coords_suspect" collisions.<br>• **Road Numbers:** Justifies W_NUMBER = 0.10 weighting due to manual officer entry errors. | **Data Governance** |
| `family-definition-rationale.md`| • **The Families:** 1. Motorway, 2. Trunk A, 3. Other-Urban, 4. Other-Rural.<br>• **Exclusions:** Details why `is_primary` (route status) was rejected in favor of `is_trunk` (design standard).<br>• **Sample Sizes:** Notes that the Motorway family (~4k links) is the lower bound for stable XGBoost training. | **Design History (ADR)** |
| `temporal_changes_plan.md` | • **Scope:** Replaces "conditional flows" with "link-level shape descriptors" (e.g., `core_overnight_ratio`).<br>• **Ablation Design:** Pits Stage 2 + Descriptors vs. Stage 2 + Road-Class Proxies.<br>• **Band Fix:** Renames mislabelled cumulative WebTRIS windows (e.g., `peak_frac` 07:00-18:59). | **Active Roadmap** |

---

## 4. Research & Analysis Notes (`docs/notes/`)

| File | Granular Content Detail | Verdict |
| :--- | :--- | :--- |
| `deep-research-roadcurvature.md`| • **Literature:** Cites FHWA safety performance functions and the Quddus et al. (2010) severity paper.<br>• **Technical:** Recommends a 10,000 deg/km cap on `max_curvature` to prevent single-vertex noise.<br>• **Code:** Provides a complete `resample_linestring` implementation using `shapely.interpolate`. | **Research Artifact** |
| `deep-research-terrain50.md` | • **Source:** Mandates OS Terrain 50 ASCII Grid over GeoPackage (contours) for raster sampling.<br>• **Resolution:** Sets a 45-60m effective baseline for slope to avoid 50m cell-edge artefacts.<br>• **Bridges/Tunnels:** Defines the endpoint fallback logic (rise/run) for OSM-tagged structures. | **Research Artifact** |
| `duckdb-wasm-workflow.md` | • **Optimization:** Mandates Douglas-Peucker simplification (0.0005 tol) and spatial sorting (Hilbert or Centroid).<br>• **Frontend:** Explains using HTTP Range Requests to query remote Parquet assets without full downloads. | **Tech Stack Workflow** |
| `evaluation_ideas.md` | • **Naive Baseline:** `Risk = AADT * length * 365`.<br>• **FOI Targets:** Lists Leeds Data Mill and local planning application ATCs as independent traffic sources.<br>• **Time-Series:** Recommends a 2015-21 train / 2022-24 test split to prove "future" predictive power. | **Strategy Doc** |

---

## 5. Quantitative Reports (`reports/`)

| File | Granular Content Detail | Verdict |
| :--- | :--- | :--- |
| `eb_dispersion.md` | • **MoM Results:** Binned dispersion varies from 273.2 (low-risk) to 0.11 (high-risk).<br>• **Formula:** k_bin = (Var(y) - E(y)) / E(y)^2.<br>• **Binning:** 20 quantile bins merged to 17 based on a 100-positive-event minimum per bin. | **Validation Artifact** |
| `family_validation.md` | • **Performance:** Stitched pseudo-R² improved to 0.895 vs. 0.888 global baseline.<br>• **Motorway Fix:** Reduces mean residual from -3.3 to +0.13, proving per-family modelling fixes the bias.<br>• **Overfit Warning:** Notes that motorway pseudo-R² reverses on held-out data (delta -0.027). | **Validation Artifact** |
| `rank_stability.md` | • **Stability:** Top-1% Jaccard mean = 0.918 across 5 seeds.<br>• **Spearman:** Pairwise mean correlation = 0.998.<br>• **Findings:** Confirms Seed 42 is representative; rank stability is high but fuzzy at narrow cuts (k=1000). | **Validation Artifact** |
| `ruc_fill.md` | • **Coverage:** Fills 335,692 links (15.5% of network).<br>• **Strategy:** 71% filled via nearest-LSOA (within 5km), 29% via Rural-default fallback.<br>• **Density:** Fallback links assigned median rural density of 174.3/km². | **Data Characterization** |
| `temporal_findings.md` | • **Core Ratio:** Median `core_overnight_ratio` is 7.07; varies by 3-4x across sites.<br>• **Weekday/Weekend:** Constant mean of 1.08 across road types; parked for link-level modelling.<br>• **Seasonality:** 30% swing is global; parked for link-level modelling. | **Key Findings** |
| `model_inventory.md` | • **Detail:** Lists 21.7M rows, 20 GLM features, 22 XGBoost features.<br>• **Verdict:** Stale. 100% redundant with `quarto/methodology/model-inventory.qmd`. | **Delete** |

---

## 6. Detailed Overlap Analysis

### 6.1 `reports/ruc_fill.md` vs. `reports/ruc_null_characterisation.md`
*   **Exact Overlap:** `ruc_fill.md` contains the *exact* table from `ruc_null_characterisation.md` (Stage 1: Road-function comparison, counts: 142k Restricted Access, 101k Minor Road).
*   **Evidence:** Both files reference the same `335,692` link count and 15.49% network share.
*   **Verdict:** `ruc_null_characterisation.md` is a subset and should be deleted.

### 6.2 `reports/model_inventory.md` vs. `quarto/methodology/model-inventory.qmd`
*   **Exact Overlap:** Both list the XGBoost metrics (Pseudo-R² 0.8575, Test deviance 104,503) and GLM metrics (Pseudo-R² 0.3013).
*   **Unique Content:** Only the Quarto version includes the `n_estimators=500`, `max_depth=6`, and `learning_rate=0.05` hyperparameter tables.
*   **Verdict:** `reports/model_inventory.md` is stale and should be deleted.

---

## 7. Revised Reorganization Plan

1.  **Move & Rename:**
    *   `docs/internal/family-definition-rationale.md` → `docs/decisions/facility-split-ADR.md`
    *   `docs/notes/*.ipynb` → `notebooks/exploratory/`
    *   `docs/notes/` → `docs/research/` (to distinguish from technical guides).
2.  **Archive Technicals:**
    *   `docs/research/duckdb-wasm-workflow.md` → `docs/technical/deployment-duckdb.md`
    *   `docs/research/geo-data-hosting-guide.md` → `docs/technical/hosting-geoparquet.md`
3.  **Clean Artifacts:**
    *   Delete `reports/model_inventory.md`
    *   Delete `reports/ruc_null_characterisation.md`
    *   Delete `docs/research/temporal_plan_raw_ideas.md`

---
*Report generated by Gemini CLI.*
