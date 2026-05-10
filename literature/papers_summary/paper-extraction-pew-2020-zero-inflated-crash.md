# Paper Extraction: Pew et al. 2020 — Zero-Inflated Models in Crash Frequency Analysis

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: Justification_for_considering_zero-inflated_models_in_crash_frequency_analysis.pdf
- Suggested Markdown filename: paper-extraction-pew-2020-zero-inflated-crash.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: claude-sonnet-4-6
- Interface used: web chat (claude.ai)
- Input type: PDF upload (text extracted from document blocks in context)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 11-page paper including appendix tables accessible. Figure 1 (Utah map) and Figure 2 (histograms) described in text; content not needed for quantitative extraction.

---

## 1. Citation

- Title: Justification for considering zero-inflated models in crash frequency analysis
- Authors: Timo Pew, Richard L. Warr, Grant G. Schultz, Matthew Heaton
- Year: 2020
- DOI or URL: https://doi.org/10.1016/j.trip.2020.100249
- Journal: Transportation Research Interdisciplinary Perspectives, Vol. 8
- Country / region studied: United States (Utah statewide)
- Study setting: mixed — all signalised intersections on state routes, federal aid routes, and other signalised intersections throughout Utah; urban and rural

---

## 2. Core Objective

- One-sentence description: The paper argues that zero-inflated models should not be categorically excluded from crash frequency modelling on theoretical grounds, and demonstrates via Bayesian hierarchical model comparison on Utah intersection crash data that zero-inflated negative binomial performs at least as well as the negative binomial-Lindley alternative.
- Main purpose: methodological justification + model comparison (goodness-of-fit, predictive accuracy, hot spot identification)
- Evidence quote: "The primary purpose of this paper is to evaluate zero-inflated models to determine if they are a suitable method for modeling crash counts" (Abstract, p. 1)

---

## 3. Response Variable

- Target variable: injury or fatal crash count per intersection per year
- Collision type: injury and fatal only ("crashes that resulted in injury or death and were marked as 'intersection related'") — property damage only excluded
- Severity handling: not modelled separately; injury and fatal crashes are pooled into a single count. Severity is not decomposed.
- Count, binary, rate, risk score, severity class, or other: count (non-negative integer)
- Time window used for outcomes: annual (2014–2017 for model fitting; 2018 held out for prediction and hot spot identification)
- Evidence quote: "We only consider crashes that resulted in injury or death and were marked as 'intersection related'" (Section 3.1, p. 4)

**Note for Open Road Risk:** The response variable is directly analogous to Open Road Risk's Stage 2 outcome — injury collision count per unit per year. The spatial unit (intersection vs road link) differs, but the outcome type and temporal aggregation (annual) are compatible.

---

## 4. Exposure Handling

- Exposure variable used, if any: entering vehicles per day (AADT equivalent), used as a covariate in the log-linear regression equation — not as a formal offset
- Traffic count source: UDOT Open Data Portal and UDOT Traffic and Safety Division; described as "number of entering vehicles per day" per intersection per year
- Whether exposure is modelled, observed, assumed, or ignored: observed and included as a covariate; however, it is **not used as a log-offset** — it enters the regression linearly (after standardisation) via the log-linear link alongside other intersection attributes
- Treatment of missing or sparse traffic counts: not discussed; all 1,738 intersections appear to have entering vehicle counts for all five years
- Whether offset terms, rates, denominators, or normalisation are used: **No offset.** Traffic volume enters as a standardised covariate, not as a formal exposure offset. This is a meaningful distinction from Open Road Risk's design.
- Evidence quote: "number of entering vehicles per day" listed as one of five covariates in Table 1 (p. 4); regression equation `ln(λ_ij) = β_0 + x'_ij β_k + η_i` (Eq. 3, p. 4) with no offset term
- Transferability to my AADF/WebTRIS setup: mixed
  - Mathematical exposure structure: **low** — no offset used; entering vehicles is treated as a predictor rather than exposure denominator. Open Road Risk uses `log(AADT × length × 365 / 1e6)` as a formal offset.
  - General principle: **medium** — the paper demonstrates that annual traffic volume is an important predictor (largest positive effect on expected crash count, Section 4). This aligns with Open Road Risk's exposure design.
- Notes: The absence of a formal exposure offset means the paper's GLM coefficients are not directly interpretable as collision rates per vehicle-km. For Open Road Risk, the formal offset design is preferable and already in place. This paper does not provide evidence against the offset approach.

---

## 5. Spatial Unit of Analysis

- Unit: intersection (signalised only)
- Segment length or segmentation rule: not applicable — intersection-level, not segment-level
- How crashes are assigned to the network: crashes marked as "intersection related" in police reports (DI-9 reports); not spatially snapped
- Treatment of junctions/intersections: intersections are the primary unit of analysis — this paper is entirely intersection-focused
- Spatial aggregation risks: not discussed; intersections are treated as independent observations conditional on covariates and random effects
- Evidence quote: "The data includes all (1,738 total intersections) state route to state route, state route to federal aid route, and any other signalized intersections throughout the state of Utah" (Section 3.1, p. 4)
- Relevance to OS Open Roads link-based pipeline: limited. Open Road Risk models road links, not intersections. The paper's intersection-level findings do not directly transfer to link-level modelling. However, the distributional modelling choices (ZIP, ZINB, NB-Lindley) are relevant to any count outcome with excess zeros, regardless of spatial unit. The paper's general argument that ZINB outperforms plain Poisson/NB for zero-heavy intersection counts may extend to link-year counts, but this has not been tested here.

---

## 6. Temporal Unit of Analysis

- Years covered: 2014–2018 (5 years); 2014–2017 for model fitting, 2018 held out
- Temporal resolution: annual
- Whether seasonality or time-of-day is modelled: no
- Whether before-after or panel structure is used: panel (intersection × year, 4 years of training data). The random effect η_i induces correlation across years for the same intersection.
- Evidence quote: "we index the year starting at 1 corresponding to 2014 up to year 4 corresponding to 2017. We withheld 2018 for prediction purposes" (Section 3, p. 4)
- Relevance to WebTRIS-style time profiles: none

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Entering vehicles per day | UDOT traffic counts | Standardised (mean-subtracted, divided by SD); used as covariate in log-linear regression | Strongest predictor of intersection crash count (rural: crash count exp{1.83} ≈ 6× per SD increase) | Medium — analogous to AADT in Open Road Risk; already present as Stage 2 feature and exposure offset. Note: this paper uses it as a covariate, not an offset. |
| Percentage of vehicles that are trucks | UDOT traffic data | Standardised; used as covariate | HGV proportion; negative effect on crashes in rural areas, Salt Lake City, small urban — possibly because HGV routes tend to be better-maintained or have fewer conflicting movements | Already present / compare implementation |
| Maximum number of lanes | Intersection inventory | Standardised; categorical-like integer variable | Positive effect on crash count in 6 of 7 urban codes | Candidate feature; lane count is sparse in OSM for Open Road Risk |
| Maximum roadway width | Intersection inventory | Standardised | Not significant in any region — weakest predictor | Low priority; not in current pipeline and not shown to be useful here |
| Maximum speed limit | Intersection inventory | Standardised | Significant positive effect in small urban and Salt Lake City regions | Already present (OSM speed limit, imputed); compare to paper's findings |
| Urban code classification (7 classes) | UDOT administrative classification | Used as hierarchical grouping variable for Bayesian random-effects coefficients | Accounts for regional heterogeneity in effect sizes — rural vs urban effects differ substantially | Analogue: police force codes or rural/urban classification already in Open Road Risk; compare implementation |
| Intersection-level random effect (η_i) | Estimated | Gamma-distributed multiplicative random effect on expected crash count | Captures unobserved intersection heterogeneity; induces within-intersection correlation across years | Analogous to grouped-by-road-link split in Open Road Risk; Bayesian random effects are a more principled treatment |

---

## 8. Model Architecture

- Algorithms/models used: Bayesian hierarchical zero-inflated Poisson (ZIP), zero-inflated negative binomial (ZINB), negative binomial-Lindley (NB-L). All fitted via MCMC using JAGS (10 chains, 25,000 iterations, 5,000 burn-in, thinned to 1,000 draws per chain = 10,000 total).
- Baseline model: Not stated explicitly; NB-Lindley treated as the strongest prior comparator based on existing literature
- Final/preferred model: ZINB — best goodness-of-fit (Bayesian χ² proportion closest to 0.05), best zero modelling (posterior predictive proportion = 0.50), comparable predictive accuracy
- Loss function or likelihood: Bayesian negative log-likelihood; model comparison via Bayesian χ² goodness-of-fit, RPMSE, MAD, WAIC
- Offset/exposure term, if used: None — entering vehicles is a standardised covariate
- Spatial autocorrelation handling: None — intersections assumed conditionally independent given covariates and random effects; no spatial random field or adjacency structure
- Temporal dependence handling: intersection-level random effect η_i induces positive correlation across years for the same intersection (multiplicative effect on expected count); no explicit autoregressive or time-series structure
- Interpretability method: posterior means and SDs of regression coefficients reported (Table A1, Appendix); coefficients interpreted as multiplicative effects on expected crash count per standard deviation change in covariate; urban-code-specific effects shown
- Evidence quote: "For each model we ran 10 independent chains... 25,000 iterations from which we removed the first 5,000 as a burn-in period and saved every 20th draw" (Section 3.6, p. 6)

**Important note on NB-Lindley comparison:** The paper argues that previous studies showing NB-Lindley superiority did not equip ZIP/ZINB models with equivalent random effects. When both zero-inflated models include intersection-level random effects (η_i), they perform comparably to or better than NB-Lindley. This is a methodological point with direct relevance to any comparison Open Road Risk might make between models.

---

## 9. Reported Metrics / Quantitative Results

### Goodness-of-fit (Table 2, p. 7)

| Result type | Metric | Value | Model | Interpretation | Evidence |
|---|---|---|---|---|---|
| Goodness-of-fit | Bayesian χ² proportion > 0.95 quantile | 0.0666 | ZIP | Close to ideal 0.05; adequate fit | Table 2 |
| Goodness-of-fit | Bayesian χ² proportion > 0.95 quantile | 0.0630 | ZINB | Closest to 0.05; best fit | Table 2 |
| Goodness-of-fit | Bayesian χ² proportion > 0.95 quantile | 0.0804 | NB-L | Slightly further from 0.05; adequate | Table 2 |

### Posterior predictive zero check (Table 3, p. 7)

| Result type | Metric | Value | Model | Interpretation | Evidence |
|---|---|---|---|---|---|
| Zero-fit | Proportion of simulated datasets with more zeros than observed | 0.2102 | ZIP | Underestimates zeros somewhat | Table 3 |
| Zero-fit | Proportion of simulated datasets with more zeros than observed | 0.4988 | ZINB | Best calibration for zeros (closest to 0.50) | Table 3 |
| Zero-fit | Proportion of simulated datasets with more zeros than observed | 0.8599 | NB-L | Overestimates zeros — expects more zeros than observed | Table 3 |

### Out-of-sample predictive accuracy (Table 4, p. 8)

| Result type | Metric | Value | Model | Interpretation | Evidence |
|---|---|---|---|---|---|
| Predictive accuracy | RPMSE (2018 held out) | 1.189 | ZIP | Comparable across models | Table 4 |
| Predictive accuracy | RPMSE (2018 held out) | 1.189 | ZINB | Comparable across models | Table 4 |
| Predictive accuracy | RPMSE (2018 held out) | 1.191 | NB-L | Marginally worse | Table 4 |
| Predictive accuracy | MAD (2018 held out) | 0.753 | ZIP | Comparable across models | Table 4 |
| Predictive accuracy | MAD (2018 held out) | 0.754 | ZINB | Comparable across models | Table 4 |
| Predictive accuracy | MAD (2018 held out) | 0.754 | NB-L | Comparable across models | Table 4 |

### WAIC (Table 6, p. 8)

| Result type | Metric | Value | Model | Interpretation | Evidence |
|---|---|---|---|---|---|
| Information criterion | WAIC | 14279 | ZIP | Highest (worst) — large penalty for complexity | Table 6 |
| Information criterion | WAIC | 14278 | ZINB | Similar to ZIP | Table 6 |
| Information criterion | WAIC | 14262 | NB-L | Lowest (best) WAIC; authors note this conflicts with predictive accuracy results | Table 6 |

### Assessment of metrics

- **Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, or temporally held out?** RPMSE and MAD are **temporally held out** (2018 predicted using 2014–2017 model). Bayesian χ² and WAIC are **in-sample / posterior predictive** diagnostics, not predictive accuracy metrics. The zero posterior predictive check is also in-sample. The paper correctly weights the held-out RPMSE/MAD more heavily than WAIC.
- **Do these metrics test predictive generalisation or model fit?** RPMSE/MAD test one-year-ahead predictive generalisation. Goodness-of-fit tests assess whether the model adequately approximates the training data distribution. WAIC is a penalised in-sample metric.
- **Are any metrics likely to be optimistic for real-world deployment?** The one-year-ahead held-out test is the most rigorous metric here and is reasonably informative. However, 2018 is immediately adjacent to the training period; longer-horizon or geographically held-out evaluation is not attempted. The WAIC ranking differs from the predictive accuracy ranking, which the authors note and handle correctly.
- **Which metric is most relevant to Open Road Risk?** RPMSE and MAD on the held-out year are most relevant. The posterior predictive zero check (Table 3) is also directly relevant — Open Road Risk faces the same zero-calibration problem and the ZINB's near-0.50 score on this test is informative.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: explicitly via zero-inflated distributions (ZIP, ZINB) and via the NB-Lindley distribution as an alternative. All three models are designed for zero-heavy count data.
- Model type: **zero-inflated Poisson (ZIP)** and **zero-inflated negative binomial (ZINB)** are explicitly fitted as zero-inflated models. NB-Lindley is a zero-heavy alternative that does not use a formal zero-inflation parameter but achieves similar distributional flexibility via a compound random effect.
- Zero rate in the data: median crash count = 0, mean = 0.91 per intersection-year (Table 1, p. 4). Approximate zero rate not stated explicitly, but given median = 0 and mean = 0.91 across 1,738 intersections × 4 years = 6,952 intersection-years, the zero rate is high — consistent with the paper's description of "a high proportion of sites with zero crashes."
- Whether high-risk locations are evaluated separately: yes — hot spot identification (Section 4.3) ranks intersections by how far observed 2018 crash counts exceed the posterior predictive distribution. Top 10 hot spots listed in Table 7.
- Evidence quote: "One common challenge of modeling intersection related crash data is the high proportion of sites with zero crashes" (Abstract, p. 1)
- Practical relevance to my sparse collision link-year dataset: High. The zero-inflation structure, distributional comparison, and posterior predictive zero check methodology are all directly applicable to Open Road Risk's link-year data. The ZINB outperforming plain Poisson on zero-heavy intersection data in this case study is consistent with theoretical expectation and the broader literature.

**Critical note on the ZIP π parameter:** Table A1 (Appendix, p. 10) shows the posterior mean of π ≈ 0.00 (SD = 0.01) for both ZIP and ZINB. This means the estimated additional zero-inflation probability is effectively zero — the models converge to their base distributions (Poisson and NB respectively). Despite this, ZINB still outperforms NB-L on goodness-of-fit and zero calibration. This is notable: it suggests the NB's extra dispersion parameter (ϕ), not the zero-inflation parameter per se, is the main source of improvement over Poisson in this dataset. This is an important nuance for Open Road Risk when deciding whether zero-inflation or overdispersion is the primary concern.

---

## 11. Validation Strategy

- Train/test split method: temporal holdout — 4 years (2014–2017) for fitting, 1 year (2018) for prediction
- Spatial holdout used? No
- Temporal holdout used? Yes — one-year-ahead holdout
- Grouped holdout used? No — same intersections in train and test
- Cross-validation type: none — single temporal holdout
- Metrics: RPMSE, MAD (predictive); Bayesian χ² goodness-of-fit, posterior predictive zero check, WAIC (in-sample/posterior diagnostics)
- External validation: none
- Leakage or generalisation risks:
  1. Same intersections in train and test — the intersection-level random effects η_i are estimated from 2014–2017 data and then used when predicting 2018. For hot spot identification, this is reasonable (intersections with high historical crash rates tend to have high future rates). For coefficient inference, there is no leakage concern.
  2. No spatial holdout — generalisation to intersections in a different region or state is not tested.
  3. Single year holdout — one-year-ahead prediction from a 4-year training window is a reasonable but limited validation. Temporal instability of crash rates (Mannering 2018) is not assessed.
- Evidence quote: "we will use each model to predict the 2018 crashes and compare the predictive accuracy of each model" (Section 1.2, p. 2)
- What I should copy or avoid:
  - **Copy:** The posterior predictive zero check (proportion of simulated datasets with more zeros than observed) is a simple, informative diagnostic for zero-calibration. Directly applicable to Open Road Risk's Stage 2 Poisson GLM.
  - **Copy:** Hot spot ranking by proportion of posterior predictive draws below observed count — more principled than raw predicted vs observed comparison; directly relevant to Open Road Risk's hotspot output.
  - **Avoid:** Treating the held-out year RPMSE as a robust estimate of generalisation — single-year holdout is limited. Open Road Risk's current grouped-by-link split across years is already more structured than this.

---

## 12. Key Findings Relevant to My Project

**Finding 1:** Zero-inflated models do not require a philosophical commitment to "inherently safe sites" and should not be excluded from candidate model sets on those grounds. The only distributional assumption is that excess zeros exist — which is testable and not implied to be permanent.

- Why it matters: Open Road Risk currently uses a Poisson GLM for Stage 2, which does not model zero-inflation. The paper removes the theoretical objection to considering ZIP or ZINB as candidate Stage 2 models, grounding the decision in predictive performance rather than interpretation of the data-generating process.
- Evidence: Section 2.2, p. 3 — PMF analysis showing no zero-probability mass assigned to positive integers under zero-inflated models
- Confidence: high — this is a logical/theoretical argument, not an empirical claim subject to generalisation uncertainty

**Finding 2:** When zero-inflated models (ZIP, ZINB) are given comparable random effects to the NB-Lindley model, they perform at least as well as NB-Lindley on goodness-of-fit, zero calibration, and out-of-sample prediction. ZINB performs best overall.

- Why it matters: Previous literature claiming NB-Lindley superiority over zero-inflated models used comparisons where NB-Lindley had a site-level random effect and the zero-inflated models did not — an unfair comparison. This paper levels the playing field. For Open Road Risk, this suggests that a ZINB GLM with road-link-level random effects is a credible Stage 2 alternative worth piloting.
- Evidence: Table 2, Table 3, Table 4, p. 7–8; "one of the contributing reasons the negative binomial-Lindley was not superior... is because we allowed the zero-inflated models to have random effects" (Section 4.4, p. 9)
- Confidence: medium — this is a single dataset (Utah intersections, ~1,738 sites, 4 years); the result does not generalise to all crash contexts

**Finding 3:** The posterior predictive zero check is a useful, simple diagnostic for whether a model adequately handles zero-heavy count data. ZINB achieved a proportion of 0.499 (ideal = 0.50); NB-L severely overestimated zeros (0.86); ZIP slightly underestimated (0.21).

- Why it matters: Open Road Risk could apply the same posterior predictive zero check to its current Poisson GLM to assess whether it under- or over-predicts zeros. Given the Poisson GLM imposes mean = variance and does not allow zero-inflation, it is likely to underestimate zeros at the link-year level where ~98–99% of observations are zero.
- Evidence: Table 3, p. 7; Section 4.1, p. 7
- Confidence: high for the diagnostic methodology; medium for inference about Open Road Risk's specific behaviour (not tested here)

**Finding 4:** The additional zero-inflation parameter π estimated to be effectively 0 (posterior mean ≈ 0.00, SD = 0.01) in both ZIP and ZINB models. The main improvement over Poisson appears to come from the negative binomial's dispersion parameter ϕ (posterior mean = 17.04 for ZINB), not from zero-inflation per se.

- Why it matters: This suggests that for the Utah intersection dataset, overdispersion (variance > mean) is the primary data challenge, not structural zero-inflation. For Open Road Risk's link-year data at annual resolution, the primary challenge may also be overdispersion rather than true structural zero-inflation — annual counts aggregate enough daily variation that the zero-heavy structure may be better described as overdispersion than as a mixing process. A negative binomial GLM with exposure offset may capture most of the improvement without the zero-inflation complication.
- Evidence: Table A1 (Appendix, p. 10) — π posterior mean ≈ 0.00 for both ZIP and ZINB; ϕ = 17.04 (ZINB)
- Confidence: medium — this interpretation is mine, not the paper's; the paper does not highlight this finding

**Finding 5:** Entering vehicles (AADT equivalent) has by far the largest positive effect on expected crash count, with the effect size varying substantially by urban code (rural: exp{1.83} ≈ 6× per SD increase; Salt Lake City: exp{0.29} ≈ 1.3× per SD increase).

- Why it matters: Confirms that traffic volume is the dominant crash predictor — consistent with Open Road Risk's exposure offset design. The regional variation in the entering-vehicles effect is analogous to the facility-family split in Open Road Risk's Stage 2 and supports the case for road-class-stratified or region-stratified modelling.
- Evidence: Section 4, p. 7; Table A1 (Appendix, p. 10) — β42 = 1.83 (Rural), β52 = 0.29 (Salt Lake City)
- Confidence: medium — applies to Utah signalised intersections only; link-level road segments have a different traffic-crash relationship

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Posterior predictive zero check | Simple diagnostic for zero-calibration of any count model; directly answers "does the current Poisson GLM handle zeros adequately?" | Stage 2 Poisson GLM posterior predictive samples or bootstrap predictions (already producible from fitted GLM) | 1,738 intersections × 4 years | High — applicable at any scale; computationally cheap | Stage 2 / validation / diagnostic | Low — requires sampling from fitted model's predictive distribution and comparing zero counts to observed | Result likely unfavourable for Poisson GLM; document as evidence for NB or ZINB pilot |
| Negative binomial GLM with exposure offset as Stage 2 candidate | The ZINB improvement over Poisson in this paper appears largely driven by the NB dispersion parameter, not by zero-inflation. A NB GLM with the existing exposure offset is a straightforward, lower-risk step up from the current Poisson GLM. | Same as current Stage 2 (STATS19 + AADF) | N/A | High — statsmodels supports NB GLM with offset | Stage 2 candidate model comparison | Low-medium — requires fitting NB GLM and comparing to Poisson GLM using held-out grouped CV | Dispersion parameter estimation can be sensitive to influential observations; check for motorway overfitting noted in current pipeline |
| ZINB GLM with exposure offset as Stage 2 candidate | If NB GLM does not fully resolve zero-calibration, ZINB adds explicit zero-inflation. Paper provides methodological justification for its use without requiring theoretical commitment to "inherently safe links." | Same as current Stage 2 | N/A | High in principle; less mature tooling in Python than R | Stage 2 candidate model extension | Medium — Python ZINB GLM with offset requires statsmodels ZINFL or manual likelihood; less well-supported than R | π may estimate near zero (as in this paper), making ZINB equivalent to NB in practice; test carefully |
| Hot spot ranking by posterior predictive exceedance probability | More principled hotspot identification than raw predicted vs observed: rank links by P(predicted < observed). Analogous to Empirical Bayes ranking but from a Bayesian predictive distribution. | Bayesian model or bootstrap from GLM | 1,738 intersections | Medium — computationally intensive at 2.17M links; feasible on subsampled or flagged links | Stage 2 / validation / hotspot output | High for full Bayesian; medium for bootstrap approximation | Bootstrap approximation of posterior predictive exceedance may not match true Bayesian ranking; acceptable for exploratory use |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full Bayesian MCMC hierarchical model (JAGS/Stan) at national scale | MCMC on 2.17M link-years × multiple parameters is computationally infeasible without substantial approximation. The paper's model runs on 1,738 × 4 = 6,952 observations with 10 chains × 25,000 iterations — already relatively expensive. | Computational feasibility | 6,952 obs | Low — 2.17M rows is ~300× larger; MCMC would take days to weeks | Variational Bayes or INLA as approximations; or fit Bayesian model on a stratified sample | High |
| Urban code hierarchical structure (7 fixed UDOT-defined groups) | UDOT's urban code classification is Utah-specific. Open Road Risk uses police force codes and rural/urban classification, which provide a different but analogous grouping. | UDOT-specific administrative classification | N/A | Low (direct transfer); Medium (concept) | Road class × rural/urban classification already provides analogous grouping in Open Road Risk | High |
| Intersection-specific attributes (number of lanes, roadway width, max speed limit per intersection) | Open Road Risk models road links, not intersections. Intersection-level attributes (entry volumes, lane counts per approach) are not directly available for all OS Open Roads links. | Intersection-level inventory data | N/A | Low for intersection attributes; Medium for link-level analogues (OSM lanes, speed limits) | OSM lane count and speed limit are already candidate features in Open Road Risk; these partially substitute | Medium |

---

## 14. Pipeline Implications

**Does this paper support using exposure-normalised collision risk?**
Indirectly — entering vehicles is the strongest predictor, confirming traffic volume is the dominant crash predictor. However, the paper does not use a formal exposure offset. The paper does not provide evidence against Open Road Risk's offset design.

**Does it suggest better handling of AADT/AADF uncertainty?**
No — traffic volume is treated as an observed covariate, not as estimated with uncertainty. AADT uncertainty is not addressed.

**Does it suggest useful geometry or road-context features?**
Limited — the intersection-level features (lanes, width, speed limit, truck %) have partial analogues in OS Open Roads (length, speed limit) and OSM (lanes, sparse). The paper confirms speed limit and lane count are worth including where available.

**Does it suggest better modelling of junctions?**
No — the paper models intersections as the unit of analysis. It does not model junction effects on adjacent link segments, which is what would be relevant for Open Road Risk.

**Does it suggest better treatment of severity?**
No — injury and fatal crashes are pooled; severity is not modelled separately.

**Does it suggest better validation design?**
Partially — the posterior predictive zero check (Table 3) is a useful diagnostic addition to Open Road Risk's current validation. The one-year-ahead temporal holdout is weaker than Open Road Risk's current grouped-by-link split and is not a model to emulate.

**Does it expose a weakness in my current approach?**
Yes — the current Stage 2 Poisson GLM likely underestimates zeros (Poisson restricts variance = mean; with ~98–99% zero link-years, the Poisson is likely to predict a distribution with lower zero probability than observed). The posterior predictive zero check should be run on the current Stage 2 Poisson GLM to quantify this.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Implement a posterior predictive zero check on the Stage 2 Poisson GLM to test whether it adequately models the zero rate in link-year collision data
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Table 3 (p. 7) shows the posterior predictive zero check detects meaningful differences in zero-calibration between models. The Poisson GLM (not tested in this paper, but a special case of ZIP with π=0) is likely to underestimate the zero rate given the data's high zero fraction. Confirming this with a diagnostic is low effort and provides concrete evidence for whether a NB or ZINB alternative is warranted.
- Implementation: sample ~1,000 predictive realisations from the fitted Poisson GLM (using Poisson draws from predicted λ per link-year), count zeros in each realisation, compare to observed zero count. Record proportion of simulated datasets with more zeros than observed.
- Effort: low
- Risk if implemented badly: The Poisson GLM's predicted λ values include the exposure offset; ensure predictive draws incorporate the correct offset per link-year. Draws should be at the link-year level, not averaged.

**Action 2**
- Suggested repo action: Fit a negative binomial GLM with the existing exposure offset as a Stage 2 candidate model and compare to current Poisson GLM using the grouped-by-link cross-validated holdout
- Action type: baseline comparison / candidate model comparison
- Relevant stage: Stage 2
- Why the paper supports it: The paper's ZINB improvement over Poisson appears primarily driven by the NB dispersion parameter (π ≈ 0; ϕ = 17). A NB GLM with exposure offset is a straightforward step up from the current Poisson GLM that addresses overdispersion without the complications of zero-inflation. This is the least disruptive modelling change consistent with the paper's evidence.
- Evidence: Table A1, p. 10 — π ≈ 0.00 for ZINB; ϕ = 17.04 suggesting substantial overdispersion
- Effort: low-medium — statsmodels supports NB GLM with offset (`sm.NegativeBinomial`); retain existing grouped-by-link CV structure
- Risk if implemented badly: NB GLM dispersion parameter estimation can produce convergence issues with sparse count data; check ϕ stability across road classes and facility families. The motorway overfitting issue noted in the current pipeline may be amplified.

**Action 3**
- Suggested repo action: Document the paper's argument that ZINB does not imply "inherently safe links" as a methodological note in the Stage 2 model selection documentation
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The primary theoretical objection to zero-inflated models in traffic safety (Lord et al. 2005, 2007) — that they assume some sites are permanently safe — is rebutted here via PMF analysis. If Open Road Risk ever considers a ZINB GLM, this objection need not block it.
- Evidence: Section 2.2, p. 3
- Effort: low
- Risk if implemented badly: None (documentation only)

**Action 4**
- Suggested repo action: Add a hot spot ranking diagnostic based on predictive exceedance probability — for a held-out year, rank link-years by P(predicted collision count < observed), using bootstrap draws from the Stage 2 model
- Action type: diagnostic / validation
- Relevant stage: Stage 2 / hotspot output
- Why the paper supports it: Table 7 (p. 9) shows that hotspot identification is robust across ZIP, ZINB, and NB-L; the top 10 intersections are nearly identical. But the ranking method (posterior predictive exceedance probability) is more principled than raw predicted vs observed. A bootstrap approximation from the Poisson GLM or NB GLM would give the same information at lower computational cost than full Bayesian MCMC.
- Effort: medium — requires a held-out year and bootstrap resampling from fitted model; feasible on a subsample of links for a diagnostic run
- Risk if implemented badly: Bootstrap draws from a Poisson GLM do not propagate coefficient uncertainty; use parametric bootstrap from the coefficient posterior if MCMC is not feasible. Computationally expensive at 2.17M links — run on a stratified sample or on the flagged top-percentile links only.

**Action 5**
- Suggested repo action: When comparing Stage 2 model variants (Poisson vs NB vs ZINB), ensure all candidate models have comparable random effect structures before drawing conclusions about distributional family differences
- Action type: documentation note / validation design guardrail
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper's central methodological contribution is that prior literature unfairly disadvantaged ZIP/ZINB by not giving them the same random effects as NB-Lindley. For Open Road Risk, if an NB GLM with road-link random effects is compared to a Poisson GLM without them, the comparison conflates distributional family with random effect structure — the same methodological error.
- Evidence: Section 4.4, p. 9
- Effort: low (documentation); medium (implementation — ensure grouped random effects are consistently present across compared models)
- Risk if implemented badly: Confounded comparisons could lead to incorrect conclusions about which distribution family best fits the data.

---

## 16. Query Tags

- zero-inflated-poisson
- zero-inflated-negative-binomial
- negative-binomial-Lindley
- Bayesian-hierarchical
- crash-count-modelling
- overdispersion
- zero-heavy-counts
- intersection-level
- hotspot-identification
- posterior-predictive-check
- WAIC
- annual-panel
- Utah-intersections
- temporal-holdout
- exposure-as-covariate
- no-exposure-offset
- random-effects
- model-selection-pragmatic

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper:
  - The observed zero rate (proportion of intersection-years with zero crashes) is not explicitly reported. It can be inferred as high from the median = 0 in Table 1, but the exact percentage is not stated.
  - The paper does not report whether MCMC convergence was verified (e.g. R-hat statistics) for any of the three models.
  - The paper does not test sensitivity of results to prior specification. The Beta(0.15, 1) prior on π is informative (centred at 13% excess zeros) — results may depend on this choice, especially given π estimated near 0 in the posterior.
  - No spatial autocorrelation analysis or spatial CV is performed; all intersections treated as conditionally independent.
- Parts of the paper that need manual checking:
  - Table A1 (Appendix) — posterior means should be verified against original PDF if citing specific coefficient values.
  - The claim that π ≈ 0.00 for both ZIP and ZINB is extracted from Table A1; this is the key nuance about zero-inflation vs overdispersion and should be confirmed from the original.
- Any likely ambiguity or risk of misinterpretation:
  - The paper concludes ZINB "performs best overall" but the differences across all three models are small (RPMSE: 1.189 vs 1.191; Bayesian χ²: 0.063 vs 0.080). The practical significance of these differences for hotspot identification is unclear — Table 7 shows nearly identical hot spot rankings across all three models. Do not overstate ZINB superiority.
  - The finding that π ≈ 0 in the posterior is buried in the appendix and not highlighted in the main text. It is the most important nuance in this paper for Open Road Risk's decision about whether to use zero-inflation or plain overdispersion modelling.
  - The paper's spatial unit (signalised intersection) does not match Open Road Risk's spatial unit (road link). The count distributions at link level will differ from intersection level — links typically have lower traffic exposure and lower crash rates than signalised intersections. The zero rate on link-years will be much higher than on intersection-years.
