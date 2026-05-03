# QMD / Notebook Gap Audit

Date: 3 May 2026  
Scope: local `notebooks/` contents, with emphasis on `notebooks/03_model_results.ipynb`, compared against tracked Quarto source under `quarto/analysis/` and `quarto/methodology/`.

## Summary

The current Quarto pages are the better canonical documentation surface. They are tracked, fresher, and mostly reflect the post-fix full-area pipeline. The `03_model_results.ipynb` notebook is still useful as a historical sketch of the results-page shape, but it is Yorkshire-pilot era and several numerical claims are now stale.

The main gap is not that the QMD site lacks model results. It already has a strong `quarto/analysis/model-results.qmd`. The gap is that a few notebook-only interpretive sections were not evolved into current QMD form:

- a compact Stage 1a feature-importance / "why the traffic model believes what it believes" panel;
- a current temporal observed-vs-expected trend diagnostic;
- a richer explanatory table for risk by road class that explicitly states the exposure-normalisation insight;
- an honest replacement for the notebook's confidence tiers;
- optional model explainability, because the QMD navigation currently promises SHAP but the model-results page does not include SHAP.

These should be ported as small sections inside existing QMD files, not by resurrecting the notebook or creating a parallel report stack.

## Current QMD Status

### `quarto/analysis/model-results.qmd`

What works:

- Covers the current Stage 2 surface: GLM summary, coefficients, XGBoost feature importance, GLM-vs-XGBoost agreement, risk score distribution, road-class percentile distribution, residuals, full-network risk maps, top-1% maps, and excess-risk maps.
- Uses current post-fix framing: `risk_scores.parquet` is one row per link, no year dimension.
- Correctly avoids the old flat `risk_percentile` histogram problem by plotting observed collision counts instead.
- Carries the important pseudo-R2 caveat: current XGBoost baseline is about `0.323`, not the old pre-fix `~0.86`.

What does not work / needs care:

- It has no temporal observed-vs-expected chart. That is sensible with the current pooled `risk_scores.parquet`, but it leaves a visible hole compared with the notebook.
- It does not include SHAP, even though `quarto/methodology/modelling.qmd` says SHAP fills the XGBoost interpretability gap.
- Some map sections are more useful than the notebook versions, but they are expensive and full-network oriented; a small collision-link-only diagnostic map/table may still help readers connect predictions to observed harm.

### `quarto/analysis/eda-traffic.qmd` and `quarto/methodology/exposure-model.qmd`

What works:

- Together they now cover the Stage 1a story much better than the notebook: counted-only AADF target, GroupKFold validation, external/local/spatial validation, full-network AADT estimates, geographic distribution, and measured-vs-estimated sanity checks.
- They use the expanded 2.1M-link framing rather than the notebook's 705k Yorkshire pilot.

What is missing from the notebook:

- The notebook printed a simple permutation-importance list for the traffic estimator (`road_class_ord`, `hgv_proportion`, `pop_density_per_km2`, `betweenness`, `dist_to_major_km`, coordinates, `link_length_km`). A current version of that would be useful in `eda-traffic.qmd` or `exposure-model.qmd`.
- The old importance values should not be copied verbatim because Stage 1a has changed since that notebook. Recompute or read from current artefacts if persisted.

### `quarto/methodology/modelling.qmd`

What works:

- Good orientation page for the three-stage model sequence.
- Correctly explains why Stage 1a exposure estimation and Stage 2 collision modelling are separate.
- Contains the current post-fix validation numbers.

What does not work:

- It says "SHAP values fill that gap" and links the Stage 2 page as if SHAP interpretation exists there. The current QMD source does not contain a SHAP section. Either add a modest SHAP section later or soften that wording.

### `quarto/methodology/feature-engineering.qmd`

What works:

- This is the strongest canonical pipeline explanation: training table construction, post-event feature exclusion, Poisson offset, GLM zero-downsampling, XGBoost `base_margin`, imputation policy, pooled scoring, residual semantics, feature summary, and limitations.
- It already evolved beyond the notebook by explaining why the output is pooled to link grain.

What needs care:

- The feature summary says IMD deciles and `mean_grade` are Stage 2 context, while `model-inventory.qmd` still lists an older trained artefact feature set without them in the explicit GLM/XGB feature tables. That may be a refresh issue rather than a notebook gap, but it is worth reconciling before adding more results text.

### Other QMDs

- `quarto/analysis/eda-collisions.qmd` covers most of the Stats19 exploratory material from `01_eda_stats19*.ipynb` and `stats19.ipynb`.
- `quarto/methodology/timezone-profile.qmd`, `quarto/analysis/temporal-exploration.qmd`, and `quarto/data-sources/webtris.qmd` cover most WebTRIS notebook material.
- `quarto/methodology/data-joining.qmd` covers the join/snap concepts that were explored in `02_eda_joins.ipynb`, although the old SD-to-SE coordinate issue should remain historical/archived rather than resurfaced unless it is still operationally relevant.
- `quarto/analysis/vehicle-mix.qmd` is still a placeholder. The vehicle-mix/HGV sections in the notebooks are a possible future source, but recent HGV leakage fixes mean any port should use current supporting reports rather than old notebook output.

## Notebook-Only Material Worth Porting

### 1. Stage 1a traffic-model feature importance

Source in notebook: `03_model_results.ipynb`, Stage 1a section.

Suggested QMD destination: `quarto/analysis/eda-traffic.qmd`, after "Cross-validation results", or `quarto/methodology/exposure-model.qmd`, after "Feature-target relationships".

Evolution path:

- Add a short chart/table titled "What drives the AADT estimator?"
- Use current persisted model artefacts if they include permutation importance; otherwise recompute on the counted-only training table as a lightweight diagnostic.
- Explain that road class dominates, but HGV share, population density, centrality, distance to major roads, coordinates, and link length add within-class signal.

Do not copy:

- The old numeric values from the notebook; they are Yorkshire-pilot era and pre-counted-only-filter.

### 2. Temporal observed-vs-expected diagnostic

Source in notebook: Section 7, temporal trend chart.

Suggested QMD destination: `quarto/analysis/model-results.qmd`, after residual analysis, or `quarto/methodology/covid-handling.qmd` if framed as a COVID/trend diagnostic.

Evolution path:

- Rebuild from the link-year Stage 2 modelling table, not from `risk_scores.parquet`, because `risk_scores.parquet` is now pooled to one row per link.
- Plot observed annual collisions and predicted annual collisions on the same scale, or use a secondary y-axis if the units genuinely differ.
- Use current coefficients from the GLM artefact rather than hardcoded text.
- Mention that temporal features are training features only and are pooled away in the final score.

Do not copy:

- The notebook's `total_predicted * 1000` line. That is the original visual bug.
- The notebook's hardcoded `year_norm` / `is_covid` interpretation. Current temporal work concluded the production adoption case is more nuanced.

### 3. Risk by road class with the exposure-normalisation insight

Source in notebook: "Risk by road classification" table and printed key insight.

Suggested QMD destination: `quarto/analysis/model-results.qmd`, near "Risk percentile by road class" or "Residuals by road class".

Evolution path:

- Add one compact table by `road_classification`: link count, mean `predicted_xgb`, median `risk_percentile`, share in top 10%, mean/median `residual_glm`, total observed collisions.
- Add a short interpretation: high-traffic major roads can have high expected collision counts while still having low or negative residuals per exposure.
- Use current full-area data, not the notebook's 2023/Yorkshire subset.

This is probably the best "evolution not revolution" port: the QMD already has the ingredients, but the notebook's reader-friendly explanation is stronger.

### 4. Confidence / data-support tiers

Source in notebook: Section 8, road-class confidence tiers.

Suggested QMD destination: `quarto/analysis/model-results.qmd` as a caveat box, or `quarto/methodology/model-inventory.qmd` as a data-support table.

Evolution path:

- Replace the old hand-written tiers with current evidence columns: direct AADF support, HGV coverage, speed-limit-effective coverage, IMD coverage, grade coverage, curvature coverage once adopted, and collision count support.
- Call it "data support by road class" rather than "confidence". Confidence implies calibrated uncertainty, which the current model does not produce.
- Keep the tone cautious: this is about input support and interpretability, not a formal uncertainty interval.

Do not copy:

- "Unclassified = low confidence because low snap rate." The current snap rate is about 99.8% and that old rationale is stale.

### 5. SHAP / model explainability

Source in notebook: Section 4 has commented-out SHAP code.

Suggested QMD destination: either a small "Not yet included" note in `model-results.qmd`, or a future `quarto/analysis/model-explainability.qmd` if a real SHAP run is created.

Evolution path:

- Short term: fix the wording in `modelling.qmd` so it does not promise SHAP as current content.
- Medium term: add SHAP only if the page can reconstruct the exact XGBoost feature matrix. Current `risk_scores.parquet` deliberately contains only output and selected context columns, not every training feature.
- Consider saving a small, deterministic explainability sample during Stage 2 scoring rather than recomputing from scratch in Quarto.

Do not copy:

- The commented notebook SHAP block. It samples from `risk` and uses only features present in the scored output, which is no longer enough for current XGBoost feature attribution.

### 6. Interactive Folium map

Source in notebook: optional top-5% Folium map.

Suggested destination: not a priority for QMD. Better suited to the Streamlit app or an exported HTML demo.

Evolution path:

- Keep QMD maps static and reproducible.
- If an interactive artefact is needed, create it as a separate app/demo output rather than embedding a heavy Folium loop in the documentation render.

## Material Already Covered Well Enough

- Stage 2 model overview: covered in `model-results.qmd`, `modelling.qmd`, and `feature-engineering.qmd`.
- GLM coefficients and incidence rate ratios: covered in `model-results.qmd`.
- XGBoost feature importance: covered in `model-results.qmd`.
- Risk score distribution: covered, and the old notebook's middle-panel problem has effectively been fixed in QMD.
- Full-network and top-1% maps: covered in `model-results.qmd`, with a more current full-study-area framing.
- Stage 1a AADT distributions: covered in `eda-traffic.qmd` and `exposure-model.qmd`.
- WebTRIS/time-zone work: covered in `timezone-profile.qmd`, `temporal-exploration.qmd`, and `webtris.qmd`.
- Stats19 EDA: covered in `eda-collisions.qmd` and `data-sources/stats19.qmd`.

## Material That Should Stay Historical

- Yorkshire pilot counts and geometry extents from `03_model_results.ipynb`.
- Old Stage 2 metrics: GLM pseudo-R2 `0.083`, XGBoost `0.330` from the pilot-era notebook.
- Any claim that `risk_scores.parquet` is link-year grain. Current output is one row per link.
- Notebook code that filters to "2023" from `risk_scores.parquet`; current production scores have no year column.
- The old temporal chart scaling `predicted * 1000`.
- The old "Unclassified low snap rate" confidence explanation.
- SD-to-SE coordinate repair material from join notebooks, unless reintroduced strictly as archived history.

## Recommended Small Work Plan

1. Add a short "Risk by road class: counts vs residuals" subsection to `quarto/analysis/model-results.qmd`.
   - Low risk, high explanatory value.
   - Uses existing `risk_scores.parquet`.

2. Add a "Data support by road class" table, replacing the notebook's confidence tiers.
   - Best placed in `model-results.qmd` or `model-inventory.qmd`.
   - Use current coverage fields instead of hand-written labels.

3. Add current AADT feature importance to `eda-traffic.qmd` or `exposure-model.qmd`.
   - Only if current importance can be read or recomputed cleanly.
   - Avoid stale notebook numbers.

4. Decide the SHAP stance.
   - Either add a small honest note that SHAP is planned/not currently rendered, or build a proper current explainability sample.
   - Also update `modelling.qmd` so it does not overpromise.

5. Add a temporal diagnostic only after deciding the source table.
   - Use link-year Stage 2 data or a persisted supporting CSV.
   - Keep units consistent; no scaling hack.

## Bottom Line

The QMD site is not missing the notebook wholesale. It is missing a handful of explanatory conveniences from the notebook, while the notebook itself is stale on geography, metrics, output grain, and several modelling assumptions. The right move is to port the narrative ideas, not the code cells: add two or three small current sections to existing QMDs and leave the notebook as historical scaffolding.
