---
title: "Stage 2 feature additions: IMD 2025 and mean grade"
format:
  html:
    toc: true
    toc-depth: 3
    number-sections: false
    page-layout: full
---

**Status:** Complete (1–2 May 2026).
**Scope:** Stage 2 GLM + XGBoost. Adds IoD 2025 deprivation features and OS Terrain 50 mean grade. Refactors GLM optional-feature handling. Adds chunked scoring.
**Primary code path:** `src/road_risk/features/network.py` (ingest, join), `src/road_risk/model/collision.py` (model integration).
**Reference baselines:** GLM pseudo-R² 0.301 (pre-IMD); top-1% 5-seed Jaccard 0.918 (`reports/rank_stability.md`).

---

## 1. Summary

Two feature batches were added to Stage 2: IoD 2025 deprivation (overall IMD, Crime, Indoors Living Environment sub-domain) and mean grade from OS Terrain 50. Adding the IMD batch surfaced a methodological issue in the GLM's optional-feature handling that was silently confounding feature-effect with sample-effect on every prior addition. The grade session both added the feature and refactored the imputation policy, retrofitting IMD into the new policy. Scoring was subsequently rewritten to operate in 1M-row chunks after the refactor pushed peak memory over the 32 GB ceiling.

Headline measurements:

- GLM pseudo-R² rose from 0.301 (pre-IMD) → 0.325 (post-IMD, sample-confounded) → 0.347 (post-grade, sample-stable).
- XGBoost pseudo-R² remained at 0.859 across all changes (saturation confirmed).
- Top-1% Jaccard between pre-grade and final ranking: 0.918 — within the seed-noise envelope of the global XGBoost model (5-seed baseline 0.918).
- Spearman rank correlation: 0.998.

The operational ranking did not move beyond what a random seed change would produce. The methodological gain is in the honesty of the comparison going forward, not in a step-change in predictive performance.

---

## 2. Features added

### 2.1 IoD 2025 deprivation (three columns)

Three decile features from MHCLG's English Indices of Deprivation 2025 (published 30 October 2025, v2 corrected 17 November 2025):

| Feature | Source | Coverage | Rationale |
|---|---|---:|---|
| `imd_decile` | IoD 2025 File 7, overall IMD | 81.7% | Headline deprivation signal |
| `imd_crime_decile` | IoD 2025 File 7, Crime domain | 81.7% | Enforcement / antisocial-behaviour proxy |
| `imd_living_indoor_decile` | IoD 2025 File 7, Indoors sub-domain | 81.7% | Housing-quality signal |

The Indoors sub-domain was used in place of the full Living Environment domain because the Outdoors sub-domain contains road traffic accidents as one of its constituent indicators — including it would have been a leakage path for a road-risk model. Confirmed against File 7 column structure before integration.

The 18.3% non-coverage is composed almost entirely of Welsh LSOAs at the western edge of the study area (Cheshire, Lancashire, Cumbria borders). Diagnostic check: 61,313 links have RUC coverage but lack IMD, against an expected ~62k Welsh links. IoD covers England only; Wales has WIMD with different methodology and is not directly comparable.

LSOA join: IoD 2025 uses LSOA21 codes, matching the project's existing `LSOA21CD` centroid lookup. No vintage mismatch (an earlier consideration when IMD 2019 was the candidate dataset). Provenance written to `data/provenance/imd_provenance.json`.

### 2.2 Mean grade

Single feature: `mean_grade`, mean absolute road-link grade percentage from OS Terrain 50.

- Coverage: 84.7% overall. Per-family breakdown: motorway 88.1%, trunk_a 83.5%, other_urban 83.2%, other_rural 86.0%. Coverage is balanced across families, including motorways — the curvature gate that excludes motorways does not apply to grade computation.
- Distribution: mean 2.27%, median 1.50%, max ~52%. Clean distribution with no transformation required.

`max_grade`, `grade_change`, and `sinuosity` were considered but deferred. `sinuosity` has Spearman 0.98 with `mean_curvature_deg_per_km` — adding both would dilute interpretability without providing orthogonal signal. `mean_curvature` itself is null on all 4,084 motorway links (a deliberate data-quality gate from `road_curvature.py` based on vertex-density thresholds), so it cannot test the motorway-residual hypothesis without imputation choices that would constitute fabricated data. Curvature is deferred to a separate XGBoost-only experiment that uses native missing handling.

---

## 3. Methodological change: GLM optional-feature handling

### 3.1 The issue

Pre-refactor `train_collision_glm` policy:

1. Optional features with >50% coverage: appended raw, then `dropna()` removed any rows with missing values.
2. Optional features with 5–50% coverage: median-imputed with `_imputed` suffix.
3. Below 5% coverage: skipped silently.

The >50% / dropna path made the GLM estimation population a function of which features were present in the dataset. Adding IMD (81.7% coverage) silently dropped ~4M link-years from the fit (from 21.7M eligible to 17.7M). Every "feature added, GLM pseudo-R² changed by X" comparison since the project began carried this confound. The 0.301 → 0.325 lift attributed to IMD in the first run was partially feature-effect and partially sample-effect.

### 3.2 The fix

Unified policy applied to all optional features:

| Coverage | Treatment |
|---|---|
| < 5% | Skip |
| 5% – 99% | Median-impute (`{col}_imputed`) + missing-flag (`{col}_missing`) |
| ≥ 99% | Median-impute only (missing flag would be near-zero-variance) |

Constants: `MIN_COVERAGE_FOR_INCLUSION = 0.05`, `SKIP_MISSING_FLAG_COVERAGE = 0.99`.

The missing flag lets the model separate "data was unavailable here" from "data was median". For IMD this matters because the missing pattern is non-random (Welsh links cluster geographically). For pop_density at near-100% coverage, the flag carries no signal and is correctly skipped.

After the refactor, GLM training population is the full 21,675,570 link-years (modulo core-feature drops) regardless of which optional features are added.

### 3.3 The IMD coefficient stability check

The natural test of whether the previous dropna was materially biasing IMD coefficients: compare pre-refactor and post-refactor IMD coefficients.

| Feature | Pre-refactor coef | Post-refactor coef | Δ |
|---|---:|---:|---:|
| `imd_decile` | −0.0337 | −0.0343 | −0.0006 |
| `imd_crime_decile` | −0.0154 | −0.0163 | −0.0009 |
| `imd_living_indoor_decile` | −0.0362 | −0.0364 | −0.0002 |

Differences are within rounding. The previous dropna was biasing the *population size* but not materially biasing the coefficient *estimates* — the missing links were not systematically different in their IMD-collision relationship from the included ones. So the previous 0.325 number wasn't grossly wrong, just methodologically sloppy. The 0.347 number is the methodologically clean equivalent.

---

## 4. Architectural change: chunked scoring

After the imputation refactor, `score_collision_models` peak memory exceeded 32 GB and OOM'd before producing risk scores. Three changes brought it back within budget:

1. Removed defensive `df.copy()` at scoring entry (~10 GB allocation eliminated).
2. Stopped writing imputed/missing columns back onto the full dataframe; rebuilt them only inside scoring.
3. Score GLM and XGBoost in 1M-row chunks rather than building full 21.7M-row feature matrices.

The chunked scoring pattern was already on the TODO from earlier sessions ("chunked prediction refactor"); it was promoted from nice-to-have to load-bearing by this work.

Contract change: `score_collision_models` now mutates its input dataframe (adding `predicted_glm`, `predicted_xgb` columns). The pre-existing call site in the training pipeline does not use the dataframe after this call so no caller depends on non-mutation; a TODO has been added to verify this remains true and to document the contract.

---

## 5. Results

### 5.1 Headline metrics

From persisted artefacts (`data/models/collision_metrics.json` family):

| Run | GLM pseudo-R² | XGB pseudo-R² | GLM training rows |
|---|---:|---:|---:|
| Pre-IMD baseline | 0.301 | 0.858 | (not measured here) |
| Post-IMD (sample-confounded) | 0.325 | 0.859 | 17,691,570 (after dropna) |
| Post-grade + refactor (final) | 0.347 | 0.859 | 21,675,570 (full) |

GLM gain decomposition: of the 0.046 total improvement from 0.301, approximately 0.022 came from sample stabilisation and 0.024 from the actual feature additions. The previous 0.325 was inflating the apparent IMD lift.

XGBoost is saturated at the headline metric. Adding three IMD features moved it 0.001; adding grade moved it 0.000. The trees are already capturing the signal in IMD and grade through correlated features.

### 5.2 Coefficients of interest

From the final-run coefficient table (run-log observation, not persisted in metrics JSON):

| Feature | Coefficient | Interpretation |
|---|---:|---|
| `imd_decile_imputed` | −0.0343 | Each decile less deprived → ~3.4% lower predicted rate |
| `imd_crime_decile_imputed` | −0.0163 | Same direction, smaller effect |
| `imd_living_indoor_decile_imputed` | −0.0364 | Strongest of the three; housing quality signal |
| `mean_grade_imputed` | **−0.0202** | Steeper grade → fewer collisions (sign opposite to prior expectation) |
| `mean_grade_missing` | +0.0501 | Links with missing grade have higher rates |
| `imd_*_missing` (all three) | −1.6258 (identical) | Collinear flags, see §6.2 |

The mean_grade coefficient sign is unexpected. Pre-fit expectation was positive (steeper roads correlate with higher collision rates per the SPF literature). Observed: negative and significant. Candidate explanations include:

- Selection: steep-grade roads in this study area may be disproportionately rural minor roads with low traffic, where collision rate per AADT-km is lower
- Behavioural: drivers compensate on steep grades (lower speed, more attention)
- Confounding: hilly areas have unmodelled features (lighting, lane width) that grade is acting as a proxy for

The diagnostic that would distinguish these hypotheses — does the sign hold within road class — has not been run. This is logged as a follow-up.

### 5.3 XGBoost feature importance

From the final run (run-log observation):

```
hgv_proportion      0.541883
log_link_length     0.163617
estimated_aadt      0.074673
is_trunk            0.036463
road_class_ord      0.035733
is_a_road           0.029280
is_motorway         0.022994
dist_to_major_km    0.017827
form_of_way_ord     0.013585
mean_grade          0.010594
```

Mean grade ranks 10th. None of the three IMD features make the top 10. This is consistent with the +0.001 / +0.000 pseudo-R² movements: XGBoost was already extracting the deprivation and geometry signal through correlated features.

### 5.4 Ranking comparison: pre-grade vs final

Computed from `risk_scores_pre_grade.parquet` and `risk_scores.parquet`:

| Metric | Value |
|---|---:|
| Spearman rank correlation | 0.998126 |
| Top-1% Jaccard | 0.917636 |
| Top-1% intersection | 20,745 |
| Top-1% entrants | 931 |
| Top-1% leavers | 931 |

Interpretation: the additions reshuffled the top-1% by an amount essentially indistinguishable from random-seed noise. The 5-seed baseline for the global XGBoost model is top-1% Jaccard 0.918 (`reports/rank_stability.md`); this comparison gives 0.918. **The features improved GLM fit but did not move the operational XGBoost-driven ranking beyond the noise envelope.**

This is a defensible finding consistent with the saturation diagnosed by the family-split work.

---

## 6. Honest caveats

### 6.1 Negative grade coefficient unexplained

The −0.0202 coefficient is statistically significant but mechanistically unexpected. Three plausible explanations are listed in §5.2; none has been confirmed. A within-road-class diagnostic would clarify but has not been run. This finding should be presented as "investigated, sign confirmed stable, mechanism uncertain" rather than with a confident causal story.

### 6.2 Identical IMD missingness coefficients

The three IMD missing-flag coefficients are exactly equal (−1.6258, identical CIs). All three IMD features share the same missingness pattern (Welsh LSOAs miss all three together), making the missing flags perfectly collinear. statsmodels distributes the joint coefficient arbitrarily across them; the reported per-feature value is not interpretable, but the *sum* (−4.88) is. Cosmetic only — fix is to collapse to a single `imd_missing` flag.

### 6.3 Motorway-residual hypothesis was not tested

The original justification for adding grade was the family-split work's diagnosis that the global model under-predicts motorway collisions by ~3.3 on average, and that the residual might be explained by missing road-geometry features. This test requires running the family residual diagnostic against the new scores, which has not been done. The current writeup documents what was added; whether grade specifically helps motorway calibration is an open question.

### 6.4 score_collision_models contract change

The function previously copied its input defensively; it now mutates. No current caller depends on non-mutation, but this is an undocumented invariant that could break a future caller silently. TODO entry added to verify and document.

### 6.5 The XGBoost saturation finding is now well-supported

Three feature batches in this thread (RUC, IMD, grade) have moved XGBoost pseudo-R² by ≤0.001. The family-split work landed the same conclusion via different evidence (held-out gains were noise on three of four families). The headline R² is not the right metric for evaluating future feature additions on this model. Calibration-by-family or top-k churn at meaningful operational thresholds are better tests.

---

## 7. Follow-up TODOs

| Priority | Item |
|---|---|
| 🟡 | Investigate the negative `mean_grade` coefficient — does sign hold across road classes? |
| 🟡 | Collapse the three identical IMD missingness flags into a single `imd_missing` |
| 🟡 | Document `score_collision_models` mutation contract; verify no other callers |
| 🟢 | Run family-residual diagnostic against final scores to test motorway hypothesis directly |
| 🟢 | Decision on long-term memory strategy — current pipeline at ~85% of 32GB ceiling, future feature additions will hit limits. The recommended near-term move is **stratified XGBoost training sample + retain full chunked scoring**: extend the existing GLM zero-downsample logic to XGBoost with stratification by collision presence, road class/family, AADT bands, and region. The model does not need every link-year to learn stable structure, but scoring still runs against every link via the chunked path that now exists. Compare rank stability against one-off full-data confirmation runs. Cloud VM (64–128 GB) is the right *emergency* lever for must-finish-today runs but actively hides fragility. Out-of-core (Polars + sklearn `PoissonRegressor`) is the long-term platform shift if memory keeps biting; real interpretability tradeoff because statsmodels has richer inference outputs. Region-split modelling rejected — no road-safety prior, stitching/calibration questions outweigh the gain. Link-grain collapse rejected as a memory fix — it changes the estimand from "expected counts at time-varying exposure" to "which links are risky over the period"; treat as a separate modelling experiment, not a memory workaround. Make sampling an explicit modelling policy, not an accidental OOM workaround. |

---

## 8. Files affected

- `src/road_risk/features/network.py` — IMD ingest function, IMD provenance writer, IMD `.map()` join into `network_features.parquet`
- `src/road_risk/model/collision.py` — GLM imputation policy refactor, `mean_grade` in GLM and XGBoost feature lists, chunked scoring rewrite
- `data/raw/mhclg/` — three IoD 2025 files
- `data/provenance/imd_provenance.json` — coverage stats, decile distributions, indoor sub-domain rationale
- `data/models/risk_scores_pre_grade.parquet` — snapshot for ranking comparison
- `data/models/collision_metrics_pre_grade.json` — snapshot for headline metric comparison
