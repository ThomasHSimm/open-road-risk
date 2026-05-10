# Paper Extraction: Poch and Mannering 1996 — Negative Binomial Analysis of Intersection-Accident Frequencies

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: Negative_Binomial_Analysis_of_Intersection-Acciden.pdf
- Suggested Markdown filename: paper-extraction-poch-mannering-1996-nb-intersection.md
- AI tool used: Claude Sonnet 4.6 (claude-sonnet-4-6)
- Interface used: web chat (claude.ai)
- Input type: PDF upload (text extracted from document blocks in context)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes: 1996 paper; no held-out test set, no spatial CV — conventions of the era. Extracting primarily for NB vs Poisson overdispersion evidence and feature engineering record.

---

## 1. Citation

- Title: Negative Binomial Analysis of Intersection-Accident Frequencies
- Authors: Mark Poch, Fred Mannering
- Year: 1996
- Journal: Journal of Transportation Engineering, Vol. 122, No. 2, March/April 1996, pp. 105-113. ASCE ISSN 0733-947X. Paper No. 10216.
- Country / region studied: United States (Bellevue, Washington)
- Study setting: urban and suburban signalised and unsignalised intersections

---

## 2. Core Objective

- One-sentence description: Estimates negative binomial regression models of annual accident frequency at intersection approaches in Bellevue, Washington, to identify geometric and traffic-related predictors and provide an empirical basis for prioritising intersection improvements.
- Main purpose: safety performance function estimation; feature importance
- Evidence quote: "The objective of our study is to develop statistical models of the annual accident frequency on individual intersection approaches" (Modeling Approach section, p. 107)

---

## 3. Response Variable

- Target variable: annual accident frequency per intersection approach
- Collision type: all reported accident types (injury + property damage); separate models for rear-end, angle, approach-turn
- Severity handling: not modelled — all crashes pooled for total model; accident mechanism modelled separately, not severity level
- Count type: count (non-negative integer, annual)
- Time window: annual; 1987-1993 (7 years), excluding the year of operational improvement
- Evidence quote: "accident data were taken at each approach in one-yr intervals" (Data section, p. 107)

Note for Open Road Risk: Response is structurally analogous to annual injury collision count per link-year. This paper includes property-damage crashes; Open Road Risk uses injury-only. The overdispersion issue is identical.

---

## 4. Exposure Handling

- Exposure variable used: approach traffic volumes (left-turn, right-turn, total opposing approach, total intersection) in thousands ADT — used as covariates, not as a formal offset
- Traffic count source: Bellevue city data — peak-period counts expanded to daily; missing years imputed via city-specific expansion factors for four geographic growth zones
- Whether offset terms are used: No formal offset. Volume enters multiplicatively via exp(beta * volume) — partial exposure control but not a theoretically correct offset.
- Evidence quote: regression equation ln(lambda_i) = beta*X_i (Eq. 2, p. 106) with no offset term
- Transferability to AADF/WebTRIS setup: mixed
  - Mathematical exposure structure: low — no offset used; Open Road Risk's formal offset design is more correct
  - General principle: medium — dominant role of opposing volume (elasticity 2.95) confirms exposure is the primary predictor

---

## 5. Spatial Unit of Analysis

- Unit: intersection approach (each leg of an intersection is a separate observation)
- How crashes are assigned: crashes in the intersection proper assigned to the at-fault vehicle's approach from police records
- Spatial aggregation risks: within-intersection correlation tested via likelihood ratio test — not found significant (chi2 = 47.2, 54 df, p = 0.732)
- Relevance to OS Open Roads pipeline: limited — spatial unit does not match; paper provides methodological precedent for NB regression on annual count data

---

## 6. Temporal Unit of Analysis

- Years covered: 1987-1993 (7 years)
- Temporal resolution: annual
- Panel structure: yes (approach x year, up to 6 years per approach); year indicator variables included
- Year-to-year correlation tested: not found significant (chi2 = 74.24, 90 df, p = 0.885)

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Left-turn volume (thousands ADT) | City traffic counts | Peak counts expanded to daily; missing years imputed | Elasticity 2.28; highest-impact turning-conflict exposure | Low — turn-movement counts not in AADF/WebTRIS |
| Right-turn volume (thousands ADT) | City traffic counts | Same | Elasticity 0.92; important for rear-end | Low — same data gap |
| Total opposing approach volume (thousands ADT) | City traffic counts | Same | Elasticity 2.95; dominant predictor | Medium — opposing-link AADT approximable from road graph |
| Number of approach lanes | Design plans | Count | Positive effect on total accidents | Medium — OSM lane count, sparse in pipeline |
| Speed limit (approach + opposing) | Design plans | Numeric, km/h | Net positive effect; approach elasticity 0.98 | Already present (OSM, imputed) / compare |
| Signal control indicator | Traffic ops records | Binary | Significant negative effect on total and angle accidents | Road classification as partial proxy; already present |
| Protected left turn indicator | Traffic ops records | Binary | Negative effect on total accidents (-0.468, t=-4.48) | Not available nationally |
| Sight-distance restriction | Field inspection | Binary | Strong positive effect on total, angle, approach-turn (1.123, t=4.35) | Not directly available; curvature as partial proxy — already candidate feature |
| Horizontal curve indicator | Design plans | Binary | Positive effect on angle and approach-turn | Medium — OS Terrain 50 curvature already candidate / compare |
| Grade > 5% | Design plans | Binary threshold | Positive effect on rear-end (0.454, t=3.34) and angle | Already present as continuous; binary threshold worth testing |
| Local street classification | City classification | Binary | Negative effect on total and approach-turn | Already present (road classification) / compare |

---

## 8. Model Architecture

- Algorithms/models used: negative binomial regression, maximum likelihood; Poisson rejected
- Baseline model: Poisson — rejected due to significant overdispersion (alpha t = 5.96)
- Final/preferred model: NB regression — four models (total, rear-end, angle, approach-turn)
- Loss function: negative log-likelihood (standard MLE)
- Offset/exposure term: none
- Spatial autocorrelation handling: none; tested via likelihood ratio tests — not significant
- Temporal dependence handling: none; tested via likelihood ratio tests — not significant; year indicators included
- Evidence quote: "the use of the negative binomial model is justified by the highly significant value of alpha (t-statistic = 5.96). Use of the Poisson regression would have produced considerable bias in coefficient estimates." (p. 110)

---

## 9. Reported Metrics / Quantitative Results

### Model fit

| Metric | Value | Model | Interpretation | Evidence |
|---|---|---|---|---|
| rho-squared (in-sample) | 0.200 | NB total accidents | Moderate in-sample fit | Table 1, p. 110 |
| rho-squared | 0.505 | NB rear-end | Better fit for specific type | Table 3 |
| rho-squared | 0.458 | NB angle | Better fit | Table 4 |
| rho-squared | 0.537 | NB approach-turn | Best fit | Table 5 |
| alpha (t-statistic) | 0.346 (5.96) | NB total | Strongly significant; NB preferred | Table 1 |
| alpha (t-statistic) | 0.319 (2.26) | NB rear-end | Significant | Table 3 |
| alpha (t-statistic) | 0.696 (3.61) | NB angle | Significant | Table 4 |
| alpha (t-statistic) | 0.505 (3.74) | NB approach-turn | Significant | Table 5 |

### Elasticities (Table 2, total accident model)

| Variable | Elasticity |
|---|---|
| Total opposing approach volume | 2.95 |
| Left-turn volume | 2.28 |
| Approach speed limit | 0.98 |
| Right-turn volume | 0.92 |
| Opposing approach speed limit | -0.34 |

### Assessment of metrics

All metrics are in-sample. rho-squared is analogous to McFadden's pseudo-R2. No held-out evaluation. The alpha significance test is the most directly relevant result for Open Road Risk — it tests whether NB is warranted over Poisson. rho-squared values will overstate predictive accuracy; do not compare to Open Road Risk's out-of-sample CV R2.

---

## 10. Rare Event / Class Imbalance Handling

- Model type: negative binomial — not zero-inflated. Overdispersion, not structural zero-inflation, is the motivation.
- Zero rate: not stated; mean approx 1.0 accident/approach/year — much lower zero rate than Open Road Risk's link-years (~98-99% zeros). At Open Road Risk's scale the dispersion parameter would likely be substantially larger.
- Practical relevance: NB without zero-inflation may be sufficient at intersection scale where zero rate is moderate; at link-year scale with extreme zero rates, ZINB may be more appropriate (cross-reference Pew et al. 2020).

---

## 11. Validation Strategy

- Train/test split method: none — all data used for fitting
- Spatial holdout: no; temporal holdout: no; grouped holdout: no
- Metrics: in-sample rho-squared, alpha significance, t-statistics
- External validation: none
- What I should copy: alpha significance test as a one-time diagnostic; likelihood ratio test for within-group correlation pattern
- What I should avoid: in-sample-only evaluation; Open Road Risk's existing CV design is more rigorous

---

## 12. Key Findings Relevant to My Project

**Finding 1:** NB dispersion parameter alpha highly significant (t = 5.96) across all four accident-type models. Poisson would have produced biased coefficients and understated standard errors.

- Why it matters: Direct empirical precedent that annual crash counts at traffic units are overdispersed and NB is preferred. Same test should be run on Open Road Risk's Stage 2 Poisson GLM.
- Evidence: Table 1, p. 108
- Confidence: high for this dataset; medium for generalisation to UK road links

**Finding 2:** Traffic volume dominates accident frequency. Opposing approach volume (elasticity 2.95) and left-turn volume (2.28) are the strongest predictors — both elastic.

- Why it matters: Supports Open Road Risk's exposure offset design. Near-proportional volume-accident relationship is consistent with log-linear offset formulation.
- Evidence: Table 2, p. 108
- Confidence: medium — urban US intersections; link-level elasticities likely differ

**Finding 3:** Sight-distance restriction is among the strongest geometric predictors (coefficient 1.123, t = 4.35 in total; 1.621, t = 5.60 in angle; 1.764, t = 7.05 in approach-turn). Consistent across multiple accident types.

- Why it matters: Supports curvature as a candidate proxy feature in Open Road Risk. Direct measurement not feasible at national scale in open data.
- Evidence: Tables 1, 4, 5
- Confidence: medium — field-inspected variable; proxy validity uncertain

**Finding 4:** Grade > 5% increases rear-end accident frequency (coefficient 0.454, t = 3.34). Supports grade as a Stage 2 feature.

- Why it matters: Supports the grade candidate feature in Open Road Risk. Binary threshold may capture non-linearity better than continuous grade.
- Evidence: Table 3
- Confidence: medium — intersection approach context; link-level effect may differ

**Finding 5:** Likelihood ratio tests for within-intersection and year-to-year correlation both found no significant violation (p = 0.732, p = 0.885). NB conditional independence assumption holds in this dataset.

- Why it matters: Template for a diagnostic check on Open Road Risk's Stage 2 model on a stratified subsample.
- Evidence: Specification Issues and Tests section, p. 112
- Confidence: medium — small sample, low power

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful | Required data | Paper scale | Compatibility | Stage | Difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| NB dispersion alpha significance test | Confirms NB preferred over Poisson; one-time diagnostic | Stage 2 Poisson GLM + NB GLM with same offset | 1,385 obs | High | Stage 2 / diagnostic | Low | None as diagnostic |
| Binary grade > 5% feature | Paper supports grade as predictor; threshold may capture non-linearity | OS Terrain 50 grade (already present) | Small | High | Stage 2 candidate feature | Low | Calibrate threshold for UK links |
| Likelihood ratio test for within-group correlation | Checks conditional independence assumption | Stratified subsets by road class or police force | 1,385 obs | Medium | Stage 2 / validation | Low-medium | Low power in small subgroups |
| Elasticity computation for continuous features post-estimation | Interpretable effect size summary | Stage 2 fitted GLM | N/A | High | Documentation / interpretability | Low | Elasticities at sample mean; add caveat |

### Techniques that probably do not transfer

| Technique | Why not | Missing data | Compatibility | Workaround |
|---|---|---|---|---|
| Turn-movement volume features | Not available for OS Open Roads links nationally | Turn-movement counts absent from AADF | Low | Total AADT as aggregate proxy |
| Signal phase / protected left-turn indicators | UK signal phase data not publicly available nationally | Phase data unavailable | Low | Road classification as partial proxy |
| In-sample-only validation | Below current methodological standards | N/A | Low | Not applicable |

---

## 14. Pipeline Implications

Does this paper support using exposure-normalised collision risk? Yes, indirectly — dominant role of opposing volume confirms traffic exposure is the primary crash predictor.

Does it suggest better handling of AADT/AADF uncertainty? No.

Does it suggest useful geometry or road-context features? Yes: curvature as sight-distance proxy (already candidate), grade > 5% threshold (already candidate), lane count (already candidate).

Does it suggest better modelling of junctions? Partially — signal phase and turn-pocket features are significant but not available at national scale.

Does it suggest better validation design? No — 1996 standards are weaker than current Open Road Risk design.

Does it expose a weakness in my current approach? One: the Stage 2 Poisson GLM's variance-mean constraint is likely violated for annual link-year counts, just as for annual intersection-approach counts. Run the alpha test.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Run NB dispersion parameter alpha significance test — fit NB GLM with same exposure offset and features as Poisson GLM; test alpha via likelihood ratio or t-statistic
- Action type: diagnostic
- Relevant stage: Stage 2
- Evidence: Table 1, p. 108 — alpha = 0.346, t = 5.96
- Effort: low
- Risk if implemented badly: Ensure same offset specification; fit on stratified sample first at 21.7M scale to check convergence

**Action 2**
- Suggested repo action: Add binary grade > 5% as comparison variant alongside continuous grade; test which form produces better Stage 2 CV performance
- Action type: candidate feature / comparison
- Relevant stage: Stage 2 / feature engineering
- Evidence: Table 3, p. 110 — grade > 5%, coefficient 0.454, t = 3.34
- Effort: low
- Risk if implemented badly: Calibrate threshold to UK data rather than applying US value directly

**Action 3**
- Suggested repo action: Compute elasticities at the mean for continuous Stage 2 features (AADT, link length, betweenness centrality) post-estimation as an interpretability addition
- Action type: documentation / interpretability
- Relevant stage: Stage 2 / documentation
- Evidence: Table 2 methodology, p. 108
- Effort: low
- Risk if implemented badly: Document that elasticities are evaluated at sample mean; add distributional caveat

**Action 4**
- Suggested repo action: Document that turn-movement volume disaggregation is the strongest predictor set in this paper and its absence from Open Road Risk's data sources is a known gap in junction-risk modelling
- Action type: documentation note
- Relevant stage: documentation
- Evidence: Table 2 — opposing volume 2.95, left-turn volume 2.28
- Effort: low

**Action 5**
- Suggested repo action: Note in Stage 2 documentation that alpha should be reported separately by facility family — dispersion is likely to vary substantially between road classes
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Evidence: Motorway overfitting already noted in Open Road Risk; paper fits single alpha across all intersection types
- Effort: low

---

## 16. Query Tags

- negative-binomial
- overdispersion-test
- intersection-approach
- annual-count
- safety-performance-function
- exposure-as-covariate
- no-exposure-offset
- sight-distance
- grade-feature
- horizontal-curvature
- turn-volume
- speed-limit
- signal-control
- lane-count
- elasticity
- in-sample-only-validation
- 1996-baseline-methods
- urban-intersections
- US-Bellevue

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated: zero rate not stated; inferred as moderate (~1.0/approach/year) — much lower than Open Road Risk's link-year zero rate. No spatial autocorrelation analysis. Selective sample (high-accident intersections only).
- Parts needing manual checking: Table 1 coefficient values; likelihood ratio test chi2 and p-values in Specification section
- Ambiguity or misinterpretation risks:
  - rho-squared = 0.200 is in-sample; do not compare to Open Road Risk's out-of-sample CV R2
  - Elasticities are from 1990s US urban intersections; specific magnitudes should not be applied to UK road links
  - alpha = 0.346 represents moderate overdispersion; Open Road Risk's extreme zero rate (~98-99%) will produce a much larger alpha
  - Selective sample means coefficients are unlikely to generalise to the full UK road network; use paper for methodological precedent (NB preferred over Poisson), not for empirical benchmarks
