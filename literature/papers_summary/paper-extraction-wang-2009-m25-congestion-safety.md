# Paper Extraction: Wang, Quddus, Ison — M25 Congestion and Road Safety

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Wang_et_al_AAP_Final_submitted1.pdf
- Suggested Markdown filename: paper-extraction-wang-2009-m25-congestion-safety.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (full text in context)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Tables 2 and 3 with coefficient results are present in full. No page numbers embedded in PDF text; page references below are based on sequential document pages as extracted.

---

## 1. Citation

- Title: Impact of Traffic Congestion on Road Safety: A Spatial Analysis of the M25 Motorway in England
- Authors: Chao Wang, Mohammed A. Quddus, Stephen G. Ison
- Year: Not stated in document (submitted version); estimated circa 2009 based on citations up to 2008
- DOI or URL, if present: Not stated
- Country / region studied: England (M25 London orbital motorway)
- Study setting: Motorway

---

## 2. Core Objective

- One-sentence description: The paper investigates whether traffic congestion (measured by a congestion index) affects the frequency of road accidents on the M25 motorway, while controlling for traffic flow, road geometry, and segment length.
- Main purpose: Safety performance function / causal inference (congestion–safety relationship)
- Evidence quote or page reference: "The aim of this paper is to explore the effects of traffic congestion on road safety using a spatial analysis approach while controlling for the other contributing factors." (p. 2)

---

## 3. Response Variable

- Target variable: Count of road accidents per road segment
- Collision type: (1) Fatal and serious injury accidents combined; (2) Slight injury accidents (modelled separately)
- Severity handling: Modelled separately by severity band. Fatal and serious combined due to low fatal counts per segment. Slight injury modelled as separate outcome.
- Count, binary, rate, risk score, severity class, or other: Count
- Time window used for outcomes: STATS19 data aggregated over 2004–2006 (3 years). Traffic characteristic data from 2006.
- Evidence quote or page reference: "STATS19 data for 2004 to 2006 were aggregated." (p. 4); "Hourly traffic characteristic data for the year 2006." (p. 3)

---

## 4. Exposure Handling

- Exposure variable used, if any: AADT (Annual Average Daily Traffic) and segment length, both included as covariates in log-linear form. Segment length included as a continuous covariate, not as an offset. AADT entered as log(AADT).
- Traffic count source: UK Highways Agency (UKHA) — observed hourly counts for M25 segments for 2006. Not sparse; near-complete observed counts for all 70 segments.
- Whether exposure is modelled, observed, assumed, or ignored: Observed directly from UKHA for all segments. No imputation required.
- Treatment of missing or sparse traffic counts: Not applicable. Two segments excluded due to missing data; no imputation described.
- Whether offset terms, rates, denominators, or normalisation are used: **No offset term used.** AADT and segment length enter as covariates in the log-linear predictor, not as a formal exposure offset. This is a key distinction from Open Road Risk's current offset structure.
- Evidence quote or page reference: "log(μᵢ) = α + βXᵢ + vᵢ + uᵢ" with log(AADT) and segment length as elements of Xᵢ (p. 6); Tables 2 and 3 show both as covariate terms.
- Transferability to my AADF/WebTRIS setup: Mixed
- Notes: The observed UKHA traffic data is high-transferability in structure (analogous to AADF counts) but is complete for all segments, unlike Open Road Risk's sparse AADF coverage requiring Stage 1a estimation. The mathematical exposure structure (covariate rather than offset) is lower transferability for Open Road Risk because it does not enforce proportional exposure scaling and does not separate exposure uncertainty from predictor uncertainty. The paper's exposure handling is simpler and less principled than Open Road Risk's current offset approach.

---

## 5. Spatial Unit of Analysis

- Unit: Road segment (motorway segment between junctions)
- Segment length or segmentation rule: Segments defined by junction-to-junction boundaries on the M25. Mean length 5.26 km (SD 3.42 km), range 0.76–15.40 km (Table 1).
- How crashes are assigned to the network: Custom weighting score combining perpendicular distance from accident point to segment centreline and angular difference between vehicle direction at time of accident and segment direction. Formula: WSᵢ = (1/dᵢ) × (1 + cos(Δθᵢ)) (p. 5, Section 3.1).
- Treatment of junctions/intersections: Junction accidents (~15% of total) explicitly excluded from analysis. (p. 4)
- Spatial aggregation risks: Segments are long (mean 5.26 km). Aggregation over 3 years further reduces granularity. Spatial heterogeneity within segments not addressable.
- Evidence quote or page reference: "Accidents coded as junction accidents (about 15% of total accidents) were also excluded from the analysis." (p. 4)
- Relevance to OS Open Roads link-based pipeline: Low direct relevance at segment design level. M25 junction-to-junction segments are much longer than typical OS Open Roads links. The accident-to-segment snapping methodology (weighting score using perpendicular distance and bearing) is conceptually relevant to Open Road Risk's snapping quality problem, though simpler than needed at 2.1M link scale.

---

## 6. Temporal Unit of Analysis

- Years covered: STATS19 2004–2006 (3-year aggregate outcome); traffic data 2006 only
- Temporal resolution: Annual aggregate (no sub-annual resolution used in models)
- Whether seasonality or time-of-day is modelled: Not modelled. Congestion index uses annual average; no temporal disaggregation in the model.
- Whether before-after or panel structure is used: No. Single cross-sectional observation per segment (3-year aggregated accident count matched to 2006 traffic).
- Evidence quote or page reference: "STATS19 data for 2004 to 2006 were aggregated." (p. 4); no panel or before-after structure described.
- Relevance to WebTRIS-style time profiles: None directly. The paper acknowledges that congestion is time-of-day specific and that its annual CI may miss peak/off-peak effects, but does not implement temporal profiling.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Congestion Index (CI) | UKHA hourly travel time and delay data | (T − T₀)/T₀ where T₀ = free-flow travel time estimated as actual time minus weighted delay | Primary research variable; proxy for congestion intensity | Low — requires complete hourly delay data per segment from a highways operator; not available in open data |
| log(AADT) | UKHA observed counts | Log transform of annual average daily traffic (per lane) | Main exposure proxy; elasticity interpretation | Already present / compare implementation — Open Road Risk uses estimated AADT with offset; paper uses observed AADT as covariate |
| Segment length (km) | UKHA road infrastructure data | Continuous covariate, not offset | Accounts for exposure to risk proportional to length | Already present — compare whether used as offset component or covariate |
| log(minimum radius of curvature) | UKHA road infrastructure data | Log transform of minimum radius in metres | Horizontal geometry; sharper curves may increase risk | Candidate feature — curvature flagged as future feature in Open Road Risk; paper finds it insignificant on M25 (note: limited curvature variation on motorway) |
| Maximum gradient (%) | UKHA road infrastructure data | Continuous covariate | Vertical geometry; steeper grades associated with more accidents | Already present as candidate — OS Terrain 50 grade available; paper finds this significant |
| Number of lanes | UKHA road infrastructure data | Integer count | Lane count affects traffic interaction and slight injury risk | Candidate feature — OSM lanes flagged as sparse in Open Road Risk |
| Direction (clockwise/anticlockwise) | UKHA / GIS | Binary dummy | Controls for directional asymmetries | Not directly applicable — Open Road Risk uses undirected OS Open Roads links |
| Average vehicle speed | UKHA | Weighted harmonic mean of hourly speeds | Excluded from final models due to high collinearity with CI (r = −0.71) | Low — requires complete hourly speed data per segment |

---

## 8. Model Architecture

- Algorithms/models used: (1) Poisson-lognormal; (2) Poisson-gamma (Negative Binomial); (3) Poisson-lognormal with CAR priors, 1st-order neighbours; (4) Poisson-lognormal with CAR priors, 2nd-order neighbours
- Baseline model: Poisson-lognormal (heterogeneity only, no spatial correlation)
- Final/preferred model: Poisson-gamma noted as slightly better DIC fit, particularly for slight injury accidents; all specifications give consistent results
- Loss function or likelihood: Poisson likelihood with log link; models estimated under full hierarchical Bayesian framework via MCMC (WinBUGS)
- Offset/exposure term, if used: None. AADT and segment length enter as covariates, not as an offset.
- Spatial autocorrelation handling: CAR (Conditional Autoregressive) priors on spatial random effects using Besag (1974) specification. Two neighbour structures tested: 1st-order (directly connected segments, wᵢⱼ = 1) and 2nd-order (connected to 1st-order neighbours, wᵢⱼ = 0.5). Contiguity-based weights.
- Temporal dependence handling: None — single cross-section.
- Interpretability method: Posterior means and standard deviations of coefficients; DIC for model comparison; elasticity interpretation of log-transformed predictors.
- Evidence quote or page reference: Model specification p. 6–7; CAR prior definition p. 7; DIC discussion p. 8.

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model comparison | DIC | 283.6 / 281.0 / 282.4 / 284.0 | Poisson-lognormal / Poisson-gamma / CAR 1st / CAR 2nd — fatal & serious | All similar; Poisson-gamma marginally best | Table 2, p. 20 |
| Model comparison | DIC | 490.1 / 482.2 / 490.3 / 489.1 | Poisson-lognormal / Poisson-gamma / CAR 1st / CAR 2nd — slight | Poisson-gamma notably better for slight injury | Table 3, p. 21 |
| Coefficient | Posterior mean of log(AADT) | 1.21 to 1.86 (fatal/serious); 1.03 to 1.53 (slight) | All four specifications | Elasticity: 1% AADT increase → ~1.2–1.9% more fatal/serious accidents | Tables 2–3 |
| Coefficient | Posterior mean of segment length | ~0.135 (fatal/serious); ~0.150–0.158 (slight) | All specifications | Length elasticity approx 0.68 (fatal/serious) and 0.79 (slight) | Tables 2–3, p. 10 |
| Coefficient | Posterior mean of maximum gradient | ~0.187–0.210 (fatal/serious); ~0.190–0.229 (slight) | All specifications; significant at 90–95% credible interval | Positive association with accident frequency | Tables 2–3 |
| Coefficient | Congestion index | −0.588 to −0.784 (fatal/serious); −0.118 to +0.373 (slight) | All specifications | **Statistically insignificant** in all models | Tables 2–3, p. 9 |
| Random effects SD | SD of uncorrelated heterogeneity (v) | 0.32–0.53 (fatal/serious); 0.42–0.53 (slight) | All specifications | Heterogeneity significant in all models | Tables 2–3 |
| Random effects SD | SD of spatial correlation (u) | 0.12–0.24 (fatal/serious); 0.10–0.13 (slight) | CAR models only | Spatial correlation significant but smaller than heterogeneity | Tables 2–3 |

**Validation type:** These are all **in-sample model fit and model comparison metrics**. DIC is a Bayesian model comparison criterion, not a predictive generalisation metric. No train/test split, no cross-validation, no spatial holdout, no temporal holdout, and no external validation are reported.

**Do these metrics test predictive generalisation?** No. DIC and posterior coefficient credible intervals assess in-sample goodness of fit and parameter uncertainty within the fitted dataset of 70 segments.

**Are any metrics likely to be optimistic?** Yes — DIC is an in-sample diagnostic. With n=70 segments, any held-out evaluation would be very limited in power.

**Most relevant metric for Open Road Risk:** The AADT elasticity estimates (1.0–1.9 range) and the gradient coefficient direction are potentially useful for cross-checking Open Road Risk's own Stage 2 GLM coefficients — but with low confidence given the different road type (motorway only), aggregation scale, and absence of an exposure offset.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Fatal accidents are rare per segment and are combined with serious injury accidents to reduce zero counts. Slight injury accidents are modelled separately and have higher counts (mean 38.6 per segment over 3 years).
- Model family: Poisson-lognormal (overdispersion via lognormal random effect); Poisson-gamma (Negative Binomial, explicit overdispersion parameter). Neither is a zero-inflated model.
- Zero-heavy counts: The paper notes the motivation for aggregating across 3 years as avoiding "a lot of motorway segments with zero or low accident counts, especially for the case of fatal and serious accidents" (p. 4). This is a data-level workaround, not a zero-inflated model.
- Whether high-risk locations are evaluated separately: Not stated.
- Evidence quote or page reference: "In order to avoid a lot of motorway segments with zero or low accident counts...STATS19 data for 2004 to 2006 were aggregated." (p. 4)
- Practical relevance to my sparse collision link-year dataset: The paper's workaround (multi-year aggregation) is directly relevant as a diagnostic reference. Open Road Risk's link-year data is far more zero-heavy (~98–99% zero) than this study's segment-level aggregates. The paper does not offer a solution to the level of sparsity in Open Road Risk; it sidesteps it by aggregation and motorway-only scope.

---

## 11. Validation Strategy

- Train/test split method: None — all 70 segments used for fitting
- Spatial holdout used? No
- Temporal holdout used? No
- Grouped holdout used? No
- Cross-validation type: None
- Metrics: DIC only (model comparison, not predictive validation)
- External validation: None
- Leakage or generalisation risks: With n=70 and full in-sample fitting, there is no meaningful assessment of out-of-sample performance. The spatial CAR model uses information from neighbouring segments during fitting (in-sample spatial smoothing), which is not data leakage but does mean spatial random effects cannot be transferred to new locations without re-fitting. No data leakage in the classic sense is present.
- Evidence quote or page reference: No mention of train/test split or cross-validation anywhere in the paper.
- What I should copy or avoid: The accident-to-segment snapping method (Section 3.1, weighting score) is worth reviewing as a methodological reference. Do not treat DIC differences as evidence of predictive superiority. The absence of any held-out validation is a significant limitation for transferring findings to Open Road Risk.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: Traffic congestion (as measured by a precise CI) is statistically insignificant in explaining accident frequency on the M25 in this case study, across all model specifications and both severity bands.
- Why it matters: Suggests that adding a congestion proxy to Open Road Risk's Stage 2 feature set may not improve predictive performance for motorways, though this finding is specific to this network and period.
- Evidence quote or page reference: "Traffic congestion has no impact on the frequency of accidents...according to the data on the M25." (p. 9)
- Confidence: Medium — finding is consistent across four model specifications, but study is motorway-only, n=70, and uses a single-year CI. Does not prove the same for mixed road networks.

**Finding 2:**
- Finding: AADT elasticity for accident frequency on this motorway ranged from approximately 1.0 to 1.9 depending on severity and model, which is higher than elasticities reported in non-motorway studies (0.6–0.7).
- Why it matters: Suggests AADT elasticity is road-type-dependent. Open Road Risk's Poisson GLM AADT coefficient can be cross-checked against this range for motorway links specifically, and against lower values for rural two-lane roads.
- Evidence quote or page reference: "The elasticity of AADT appears a little high in this study compared with some of the previous studies which reported that the elasticity ranges from 0.6–0.7." (p. 10)
- Confidence: Medium — the paper provides a plausible mechanism (motorway road type) but this is a single case study.

**Finding 3:**
- Finding: Maximum vertical gradient is a statistically significant positive predictor of accident frequency in all model specifications and both severity bands. Horizontal curvature (radius) is not significant on the M25, possibly due to limited variation across segments.
- Why it matters: Supports including grade from OS Terrain 50 in Open Road Risk. The curvature null result is a caution: insignificance on a motorway with low curvature variation does not generalise to mixed networks.
- Evidence quote or page reference: "Gradient (%) which represents the vertical grade of the segment was...found to be statistically significant and positively associated with accidents in all models." (p. 11)
- Confidence: Medium for gradient (consistent across models), low for curvature null result (likely network-specific).

**Finding 4:**
- Finding: Spatial correlation among neighbouring motorway segments is statistically significant (SD of u significant in CAR models), but adding CAR priors does not substantially change coefficient estimates or DIC relative to non-spatial Poisson models.
- Why it matters: In this case study, spatial random effects improved model completeness but not model comparison metrics. This suggests that at segment level, non-spatial Poisson models may be adequate if other features are well-specified, but does not rule out spatial effects being more important at Open Road Risk's link scale.
- Evidence quote or page reference: "The results are very similar to the non-spatial models." (p. 11–12)
- Confidence: Low for generalisation — 70-segment motorway is not representative of 2.1M mixed-network links.

**Finding 5:**
- Finding: The paper develops a weighted accident-to-segment snapping method combining perpendicular distance and vehicle heading angle (bearing), which reduced ambiguous assignments to approximately 2% of accidents. A sensitivity analysis on randomly assigned ambiguous accidents showed no significant difference in results.
- Why it matters: Provides a methodological reference for Open Road Risk's own snapping quality concern. The bearing-direction component is additional to distance-only snapping.
- Evidence quote or page reference: Section 3.1, p. 5. "There were about 2% such accidents in our data."
- Confidence: High as a methodological description; transferability to Open Road Risk's scale is medium (the approach is simple but would require vehicle direction data from STATS19).

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Accident-to-segment snapping using perpendicular distance + bearing angle | Methodological reference for snapping quality diagnostics | STATS19 vehicle direction field (available) | 70 segments | Compatible conceptually; scale not an issue | Validation / diagnostic | Low | STATS19 bearing data quality may be poor; bearing field has known recording errors |
| Gradient as a model feature | Positive, consistent association across all model specs; supports existing candidate feature | OS Terrain 50 (already planned) | 70 segments / motorway only | Compatible | Stage 2 candidate feature — already planned | Low | Aggregation to long M25 segments; effect may be attenuated on shorter OS Open Roads links |
| Severity-stratified modelling (fatal+serious vs. slight) | Demonstrates that severity bands have different predictor relationships | STATS19 severity field (available) | 70 segments | Compatible in principle | Stage 2 / future extension | Medium | Small counts in fatal+serious band at link-year level; may not be feasible without further aggregation |
| Poisson-gamma (Negative Binomial) as overdispersion model | DIC marginally favours NB over Poisson-lognormal for slight injury; handles overdispersion | No extra data | 70 segments | Compatible | Stage 2 — already considered as GLM family option | Low | No out-of-sample validation; DIC comparison in-sample only |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Congestion Index (CI) as model feature | Requires complete hourly travel time and delay data per segment from a highways operator (UKHA) | Hourly delay data not in open data stack | 70 segments | Incompatible at national scale | V/C ratio as proxy if modelled AADT and capacity estimates available — but this is a coarse approximation | High |
| Bayesian CAR spatial model (WinBUGS/MCMC) | Computationally infeasible at 2.1M links; WinBUGS is not scalable; CAR requires constructing full spatial adjacency matrix | No data gap; computational barrier | 70 segments | Incompatible at production scale | Spatial random effects via sparse INLA or spatial lag features as approximations; feasible only as small-area diagnostic | High |
| Complete observed AADT for all segments (exposure as covariate) | Open Road Risk uses sparse AADF requiring Stage 1a estimation; all 70 M25 segments have observed UKHA counts | Sparse AADF coverage in Open Road Risk | 70 segments | Low compatibility for general network | Stage 1a estimated AADT with uncertainty is the correct approach for Open Road Risk; paper's method is not applicable | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Partially. The paper uses AADT and segment length as covariates (not an offset), but this is a weaker approach than Open Road Risk's offset structure. The paper's AADT elasticities well above 1.0 imply non-proportional exposure, which is a reason to prefer a flexible covariate or to treat the offset coefficient as a testable constraint rather than an assumption. This suggests Open Road Risk could diagnostically check whether constraining the AADT log-offset coefficient to 1.0 is supported by the data, particularly for motorway links.

- **Does it suggest better handling of AADT/AADF uncertainty?** No. The paper uses complete observed AADT and does not address estimation uncertainty.

- **Does it suggest useful geometry or road-context features?** Yes. Gradient (vertical grade) is supported as a significant predictor. Curvature is not supported for motorway-only networks with low variation; this does not rule it out for mixed networks.

- **Does it suggest better modelling of junctions?** No. Junction accidents are explicitly excluded. The paper acknowledges this as a limitation.

- **Does it suggest better treatment of severity?** Yes — it demonstrates that severity bands can have meaningfully different predictor relationships (e.g., number of lanes significant only for slight, gradient more significant for fatal/serious). This supports treating severity bands separately in Open Road Risk diagnostics.

- **Does it suggest better validation design?** No. The paper has no held-out validation, which is a methodological weakness relative to Open Road Risk's current grouped-split approach.

- **Does it expose a weakness in my current approach?** One worth noting: Open Road Risk currently constrains exposure as a log-offset (implying elasticity = 1.0 for AADT × length). This paper's high AADT elasticities (1.0–1.9 on motorways) suggest the true elasticity may differ substantially by road type. Open Road Risk's GLM could diagnostically estimate the AADT coefficient freely rather than constraining it as an offset, at least for motorway-class links.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add a diagnostic check in Stage 2 GLM that estimates the log(AADT) coefficient freely (as a covariate rather than fixed-offset constraint) for motorway-class links, and compare to the assumed offset value of 1.0.
- Action type: Diagnostic
- Relevant stage: Stage 2
- Why the paper supports it: Paper finds AADT elasticities of 1.2–1.9 on motorways, above the proportional assumption implicit in an exposure offset. This may indicate the offset constraint is too strong for motorway links specifically.
- Evidence: Tables 2–3, coefficient of log(AADT); p. 10 elasticity discussion.
- Effort: Low
- Risk if implemented badly: If applied globally rather than as a diagnostic for motorways, it undermines the interpretable offset structure and makes model outputs harder to compare across segments.

**Action 2**
- Suggested repo action: Document the gradient (vertical grade) feature as having external empirical support from a UK motorway study, and prioritise its validation in Stage 2 once OS Terrain 50 grade is integrated.
- Action type: Documentation note → validation when grade feature is added
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Gradient is significant at 90–95% credible interval across all four model specifications and both severity bands on a UK motorway.
- Evidence: Tables 2–3, p. 11.
- Effort: Low
- Risk if implemented badly: Gradient effect may be attenuated or non-linear on short OS Open Roads links; do not assume the M25 coefficient magnitude transfers directly.

**Action 3**
- Suggested repo action: Review STATS19 vehicle direction/bearing field coverage and assess feasibility of incorporating bearing angle into the snapping quality score, as a diagnostic supplement to distance-only snapping.
- Action type: Diagnostic
- Relevant stage: Feature engineering / snapping quality
- Why the paper supports it: Section 3.1 demonstrates that combining perpendicular distance with vehicle heading angle reduces ambiguous assignments to ~2% and that sensitivity to the assignment threshold is low.
- Evidence: Section 3.1, p. 5.
- Effort: Medium (requires checking STATS19 bearing field quality at scale)
- Risk if implemented badly: STATS19 bearing data has known quality issues; a noisy bearing field could degrade rather than improve snapping accuracy.

**Action 4**
- Suggested repo action: Add a documentation note that CAR spatial models are theoretically supported (spatial correlation among M25 segments is statistically significant) but computationally infeasible at Open Road Risk scale, and that spatial lag features or local density features are the practical alternative.
- Action type: Documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: CAR models confirm spatial autocorrelation in segment-level accident counts, but do not substantially change coefficient estimates vs. non-spatial Poisson in this case study.
- Evidence: p. 11–12; Table 2–3 DIC values.
- Effort: Low
- Risk if implemented badly: None for documentation.

**Action 5**
- Suggested repo action: Note in project documentation that congestion proxies (V/C ratio, time-delay index) are low-priority Stage 2 features given this study's null result for congestion on a UK motorway, and that their absence from Open Road Risk's current feature set is defensible pending evidence from mixed road-type studies.
- Action type: Documentation note
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Congestion index insignificant across all four model specifications (p. 9).
- Evidence: Section 5.1, p. 9.
- Effort: Low
- Risk if implemented badly: The null result is motorway-specific; congestion effects on urban roads may differ.

---

## 16. Query Tags

- poisson-gamma
- poisson-lognormal
- CAR-spatial-model
- bayesian-hierarchical
- STATS19
- UK-motorway
- segment-level
- congestion-index
- AADT-elasticity
- exposure-as-covariate
- no-exposure-offset
- gradient-feature
- severity-split
- snapping-quality
- DIC-model-comparison
- in-sample-only-validation
- spatial-autocorrelation
- overdispersion
- zero-heavy-aggregation-workaround
- motorway-only

---

## 17. Confidence and Gaps

- Overall confidence in extraction: High — the full paper text was available and tables are complete.
- Important details not stated in the paper: Year of publication not present in document (estimated ~2009 from citation dates). No DOI stated. Exact WinBUGS convergence diagnostics not reported beyond burn-in counts.
- Parts of the paper that need manual checking: Table 1 variable statistics (checked against text — consistent). Coefficient tables (Tables 2–3) verified as present and complete.
- Any likely ambiguity or risk of misinterpretation: (1) The paper uses AADT as a log-transformed covariate, not an exposure offset. This is an important structural difference from Open Road Risk and should not be glossed over when comparing results. (2) The DIC differences between model specifications are small (1–8 units); these should not be treated as strong evidence of model superiority. (3) The congestion index null result is specific to the M25 motorway with its particular traffic and geometry characteristics; it does not support a general conclusion that congestion is irrelevant to road safety on all road types.
