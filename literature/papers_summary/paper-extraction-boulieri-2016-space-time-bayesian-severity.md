# Paper Extraction — Boulieri et al. 2016

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Boulieri_et_al-2016-Journal_of_the_Royal_Statistical_Society__Series_A_Statistics_in_Society.pdf
- Suggested Markdown filename: paper-extraction-boulieri-2016-space-time-bayesian-severity.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered in context as text + page images)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Supporting material referenced in paper (online appendix with additional figures and maps) not included in uploaded PDF; those figures are not available to the model.

---

## 1. Citation

- Title: A space–time multivariate Bayesian model to analyse road traffic accidents by severity
- Authors: Areti Boulieri, Silvia Liverani, Kees de Hoogh, Marta Blangiardo
- Year: 2016
- DOI or URL, if present: Published in J. R. Statist. Soc. A (2016); DOI not printed on pages provided but article is open access via Wiley. ISSN 0964-1998.
- Country / region studied: England
- Study setting: mixed (all road types aggregated to ward level; motorways, A-roads, urban and rural areas included)

---

## 2. Core Objective

- One-sentence description: The paper develops a Bayesian hierarchical space–time multivariate model to jointly analyse road traffic accident counts at two levels of severity (slight vs. severe/fatal) across English electoral wards over 2005–2013, accounting for spatial and temporal correlation and the dependence between severity levels.
- Main purpose: hotspot detection / descriptive spatial analysis / safety performance mapping (the authors explicitly state this is exploratory, not causal inference and not formal hotspot analysis in the engineering sense)
- Evidence quote: "we should treat this as an explorative analysis, aiming solely at investigating the spatial and temporal pattern of accidents and at identifying areas that are characterized by particularly high risks" (Section 5, p. 18)

---

## 3. Response Variable

- Target variable: Count of road traffic accident records per electoral ward per year, separately for low severity (slight) and high severity (severe + fatal combined)
- Collision type: injury only (STATS19 records; fatal and severe combined into one category, slight as the other)
- Severity handling: Two severity levels modelled jointly in a multivariate framework. Fatal and severe are combined because "fatalities account for an average of 0.014% of the total number of accidents for each year" (Section 2, p. 4). Separate temporal trends are estimated per severity.
- Count, binary, rate, risk score, severity class, or other: count, modelled as Poisson with offset; posterior accident rates reported as the key output
- Time window used for outcomes: annual counts, 2005–2013 (9 years)
- Evidence quote: "We analysed the data for the years 2005–2013 for England. For each accident the location and its severity are available" (Section 2, p. 4)

---

## 4. Exposure Handling

- Exposure variable used: Ward-level total traffic volume, computed as the sum over all road segments in the ward of (AADF × segment length), i.e. TVw = Σ (length_rs × AADF_rs)
- Traffic count source: Department for Transport Road Traffic Statistics Branch annual average daily flow (AADF) counts for motorways and A-roads (980 motorway count points, 16,941 A-road count points). Year 2009 (middle of study period) used for all years because counts were "very stable across all the years" (Section 2, p. 4–5).
- Whether exposure is modelled, observed, assumed, or ignored: Partially observed. AADF counts are available for major roads only. Missing link-level counts imputed by averaging traffic counts of bordering road segments (one cited method: Eeftens et al. 2012; de Hoogh et al. 2013). Minor roads not covered.
- Treatment of missing or sparse traffic counts: Simple neighbour-average imputation for segments lacking a count. No formal uncertainty propagation for this imputation step.
- Whether offset terms, rates, denominators, or normalisation are used: Used as an offset in the Poisson log-linear model: log(λ_it^(j)) = α^(j) + BYM^(j) + δ_t^(j), with Offi (traffic volume) as the offset (equation 1, p. 7). The offset is on the count scale, not the log scale of AADT; it is the product of AADF and road length summed across segments.
- Evidence quote: "Y_it^(j) ~ Poisson(λ_it^(j) Offi)" and "the offset variable by Offi, which here is taken as the traffic volume described in Section 2" (Section 3.1, p. 7)
- Transferability to my AADF/WebTRIS setup: mixed
- Notes:
  - Mathematical exposure-offset structure: high transferability. The Poisson log-linear model with an AADF × length traffic-volume offset is directly analogous to my Stage 2 offset structure.
  - Paper's specific data source: medium transferability. The paper uses DfT AADF counts for major roads only, which is essentially what my AADF pipeline also uses. However, the paper fixes exposure to a single year (2009) and uses simple neighbour-average imputation without uncertainty, whereas my pipeline estimates AADT via a trained model (Stage 1a). The paper does not attempt to estimate AADT for unobserved minor roads.
  - Important gap: the paper operates at ward level, aggregating across all road types. It does not propagate AADT estimation uncertainty into the collision model. My pipeline's use of estimated (not directly observed) AADT for all links is not addressed here; the paper's exposure handling is simpler and more conservative about what roads are included.

---

## 5. Spatial Unit of Analysis

- Unit: electoral ward (administrative area)
- Segment length or segmentation rule: Not applicable as primary unit. Road segments used only to compute ward-level traffic volumes via GIS intersection with ward boundaries.
- How crashes are assigned to the network: Crashes aggregated to ward by location. No link-level snapping described; spatial join to ward polygon geography.
- Treatment of junctions/intersections: Not stated. Junctions are not distinguished from mid-links at ward level.
- Spatial aggregation risks: Ward-level aggregation masks within-ward heterogeneity. The paper uses this level explicitly because it is compatible with disease-mapping methodology and prior work, not because it is the natural unit for road risk. Ecological fallacy risk when interpreting results.
- Evidence quote: "The study analyses road traffic accidents data at ward level in England over the period 2005–2013" (Abstract, p. 1); 7932 wards in England used (Section 3.1, p. 7).
- Relevance to OS Open Roads link-based pipeline: Low direct relevance for spatial unit. My pipeline operates at road link level (~2.17 million links), which is orders of magnitude finer than wards. The statistical machinery (Poisson + spatial random effects + offset) transfers, but the specific spatial smoothing via CAR neighbourhood structure over wards does not apply directly to link-level data at my scale. Bayesian spatial smoothing over 2+ million links via MCMC is computationally unrealistic (see Section 13 below).

---

## 6. Temporal Unit of Analysis

- Years covered: 2005–2013 (9 years)
- Temporal resolution: annual counts
- Whether seasonality or time-of-day is modelled: No. Annual aggregation only; no sub-annual or time-of-day structure.
- Whether before-after or panel structure is used: Panel structure (ward × year); temporal random effect modelled via random walk of order 1 (RW1) to capture year-to-year correlation.
- Evidence quote: "For the temporal component δ_t a normal random-walk prior of order 1, RW1, is used" (Section 3.1, p. 7)
- Relevance to WebTRIS-style time profiles: None direct. The paper models annual temporal trends only, not within-day traffic profiles. No sub-daily structure is used or relevant to the paper's RW1 temporal component.

---

## 7. Engineered Features

Only features actually used in the model are included.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Ward-level total traffic volume (TVw) | DfT AADF count points (major roads only) | GIS: road segments intersected with ward boundaries; TVrs = length × AADF; summed within ward | Primary exposure offset; replaces population as the denominator | Partially — mathematical structure transfers; my pipeline estimates link-level AADT rather than aggregating observed counts to ward level |
| Road network (Ordnance Survey Meridian) | OS Meridian road network | Used to assign AADF points to road links by road name or nearest distance, then intersect with wards | Required to construct traffic volume offset | Medium — OS Open Roads replaces OS Meridian; same general approach but different network product |
| Severity category (low / high) | STATS19 | Slight = low; severe + fatal = high | Defines the two response variables for multivariate modelling | Already present — my pipeline uses STATS19 severity; compare implementation of severity grouping |
| Ward adjacency matrix | Ward boundary geography | Constructed from shared borders to define CAR neighbourhood structure | Required for BYM spatial random effects | Not directly applicable at link scale — ward-level adjacency not relevant for link-level modelling |

No additional engineered features (road geometry, speed, land use, demographics, etc.) are used in the models. The paper explicitly notes these as future work.

---

## 8. Model Architecture

- Algorithms/models used: Bayesian hierarchical Poisson log-normal models with combinations of spatially structured (CAR / MCAR), spatially unstructured (normal / multivariate normal), and temporally structured (RW1) random effects. Six models compared (A–F, see Table 2 and Table 3 in paper).
- Baseline model: Model A — independent BYM spatial effects per severity, independent RW1 temporal effects per severity (standard univariate approach run twice)
- Final/preferred model: Model E — correlated space effects (MBYM = multivariate CAR + multivariate normal for unstructured effects), independent RW1 temporal effects per severity. Chosen on lowest DIC (392,900 vs next best 413,300 for model F).
- Loss function or likelihood: Poisson likelihood with log link; model comparison via DIC (Spiegelhalter et al. 2002). Lower DIC = better.
- Offset/exposure term: log(TVw) implicitly as the offset Offi in Poisson parameterisation (not shown explicitly as log in the equations as written, but standard Poisson GLM practice; confirmed by equation 1 context)
- Spatial autocorrelation handling: BYM (Besag–York–Mollié) structure = CAR (spatially structured) + exchangeable normal (unstructured heterogeneity). Extended to MBYM (multivariate BYM) in preferred model using MCAR and multivariate normal priors with estimated cross-severity correlations ρφ and ρθ.
- Temporal dependence handling: RW1 random walk on annual time points; either severity-specific (models A, C, E) or shared (models B, D, F).
- Interpretability method: Posterior mean accident rates mapped spatially; posterior probability of belonging to top 800 wards used as hotspot indicator; posterior rank means compared to crude-rate ranks.
- Evidence quote: "the MBYM specification… consists of both multivariate spatially structured and unstructured effects that assume a degree of correlation in the respective components between severities" (Section 5, p. 18)
- Implementation: OpenBUGS; two MCMC chains, ~50,000 iterations, 5,000–10,000 burn-in; convergence checked via Gelman–Rubin statistic, trace plots, autocorrelation plots, MC error < 5% of posterior SD. Runtime: 20–27 hours per model.

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model comparison | DIC | 527,400 | Model A (independent BYM, severity-specific RW1) | Baseline; worst of independent-effects group | Table 4, p. 11 |
| Model comparison | DIC | 540,100 | Model B (independent BYM, common RW1) | Worse than A | Table 4, p. 11 |
| Model comparison | DIC | 542,300 | Model C (common BYM, severity-specific RW1) | Worst group overall | Table 4, p. 11 |
| Model comparison | DIC | 543,200 | Model D (common BYM, common RW1) | Worst single model | Table 4, p. 11 |
| Model comparison | DIC | 392,900 | Model E (MBYM, severity-specific RW1) — preferred | Best fitting model; ~135,000 DIC improvement over model A | Table 4, p. 11 |
| Model comparison | DIC | 413,300 | Model F (MBYM, common RW1) | Second best; severity-specific temporal trends preferred | Table 4, p. 11 |
| Parameter estimate | exp(α) intercept, low severity | 0.192 (SE < 0.001) | Model E | Overall mean accident rate per unit traffic volume for low severity | Table 5, p. 12 |
| Parameter estimate | exp(α) intercept, high severity | 0.033 (SE < 0.001) | Model E | Overall mean accident rate for high severity; ~6× lower than low severity | Table 5, p. 12 |
| Spatial fraction | fracφ, low severity | 0.646 (SD 0.009) | Model E | ~65% of spatial variability is spatially structured (vs. unstructured heterogeneity) | Table 5, p. 12–13 |
| Spatial fraction | fracφ, high severity | 0.602 (SD 0.010) | Model E | ~60% spatially structured for high severity | Table 5, p. 12–13 |
| Cross-severity correlation | ρφ (spatially structured) | 0.769 (SD 0.009) | Model E | High spatial correlation between severity types in structured component | Table 5, p. 12 |
| Cross-severity correlation | ρθ (spatially unstructured) | 0.643 (SD 0.010) | Model E | Substantial correlation in unstructured heterogeneity too | Table 5, p. 12 |
| Cross-severity correlation | ρtot (total spatial) | 0.740 (SD 0.007) | Model E | Combined correlation ~0.74 | Table 5, p. 12 |
| Posterior predictive check | % areas with extreme pBayes | 11–17% | Model E, all years | Acceptable fit; mean pBayes 0.54–0.63 (target ~0.5) | Table 6, p. 15 |
| Ranking comparison | % top-100 areas with rank difference >15 places (crude vs. posterior) | 0.02% low severity; 0.26% high severity | Model E | Model substantially reorders rankings for high severity; less so for low severity | Section 4, p. 15 |
| Ranking comparison | % top-800 areas with rank difference >15 places | 0.27% low severity; 0.75% high severity | Model E | Larger reordering effect at 800-area threshold | Section 4, p. 15 |

**Metric qualification:**

- All metrics are **in-sample posterior predictive diagnostics or in-sample model-comparison metrics**. No held-out data, no cross-validation, no temporal or spatial holdout, no external validation is performed.
- DIC is a model-comparison criterion only. It does not test predictive generalisation to new areas or future years.
- Posterior predictive checks (pBayes) are in-sample adequacy checks; a good pBayes means the model can reproduce data it was fitted to, not that it generalises.
- There are no predictive accuracy metrics (RMSE, MAE, AUC, etc.) on unseen data.
- The ranking-stability comparison (crude vs. posterior ranks) is a within-sample diagnostic showing the effect of smoothing, not a validation against ground truth.
- **Most relevant metric to Open Road Risk**: the ranking comparison (crude rates vs. posterior-smoothed ranks) is conceptually closest to my use case, because it directly illustrates when Bayesian spatial smoothing changes hotspot identification. However, it is still in-sample.
- The DIC gap between Model E and all others is large (>100,000 units) and suggests the multivariate correlation structure is capturing real signal; but this should not be interpreted as external predictive validation.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Zero-heavy counts handled using Poisson log-normal Bayesian hierarchical model with spatial and temporal random effects. Bayesian borrowing of information from neighbouring wards provides smoothing for low-count areas. The paper explicitly motivates the Bayesian approach partly because "classical" models "give unstable estimates due to the large variability from one area to another, especially when the population size and/or the geographical scale of the analysis is small" (Section 1, p. 2).
- Use of Poisson / negative binomial / zero-inflated models / hurdle models: Poisson log-normal with random effects. Negative binomial and zero-inflated models are mentioned in the introduction as alternatives but **not used** in the paper. The paper notes zero-inflated models "are appropriate for data that exhibit excess 0s" (p. 2) as background, not as a method adopted here.
- Whether high-risk locations are evaluated separately: No — the modelling is applied uniformly across all 7,932 wards. Hotspot identification is post-hoc via posterior probability maps and rankings, not a separate modelling step.
- Evidence quote: "Bayesian hierarchical methods facilitate smoothing by borrowing information from neighbouring units, which is an essential point in case of low counts" (Section 1, p. 2)
- Practical relevance: The approach is relevant to my sparse link-year dataset in principle (Bayesian smoothing handles zeros and low counts naturally). However, at ward level the zero rate for high severity is 16–22% (Table 1), which is manageable. My link-year dataset has ~98–99% zeros, which is far more extreme; the degree of sparsity is qualitatively different and would require a more aggressive treatment.

---

## 11. Validation Strategy

- Train/test split method: None. No train/test split performed.
- Spatial holdout used: No
- Temporal holdout used: No
- Grouped holdout used: No
- Cross-validation type: None
- Metrics: DIC (in-sample model comparison); posterior predictive checks with pBayes (in-sample adequacy); sensitivity analysis with alternative priors (robustness check, not predictive validation)
- External validation: None
- Leakage or generalisation risks: The spatial CAR/MCAR random effects use observed neighbouring counts during fitting (standard BYM behaviour). This is **not classical data leakage** but is an in-sample spatial smoothing mechanism. The model learns the spatial correlation structure from all data simultaneously; there is no equivalent of "training on neighbours, predicting at held-out location". This is expected behaviour for disease-mapping models and is not a flaw, but it means reported fit metrics do not test generalisation.
- Evidence quote: "we use the deviance information criterion (DIC)… solely used for building the models to find the most suitable for the data at hand, and it is not intended as an absolute measure" (Section 3.5, p. 9–10)
- What I should copy or avoid:
  - **Copy**: the posterior predictive check approach (pBayes) as a model adequacy diagnostic, and the prior sensitivity analysis methodology.
  - **Avoid**: treating DIC as evidence of predictive performance. The paper is explicit about this limitation. No validation design here is usable as a template for my Stage 2 validation; my pipeline uses grouped link-level splits which are more rigorous.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: In this case study, the multivariate model jointly modelling low and high severity substantially outperformed independent univariate models on DIC (Model E DIC ~393k vs Model A DIC ~527k), suggesting that severity levels share substantial spatial structure (ρtot ~0.74).
- Why it matters: This provides evidence that modelling injury and KSI counts jointly, rather than separately, captures structure that univariate models miss. This may be relevant if I consider adding a severity-split output to my pipeline.
- Evidence quote: "The benefit of including a multivariate structure in the spatial effects (the MBYM specification) can be seen in the correlated space effects, where the DIC decreased greatly" (Section 4, p. 11)
- Confidence: medium (in-sample DIC only; no external validation; ward level not link level)

**Finding 2:**
- Finding: In this case study, Bayesian spatial smoothing substantially changed rank orderings for high-severity (rare) accidents but had little effect on low-severity (common) accident rankings. Among top 100 areas, 0.26% of high-severity ranks shifted >15 places vs 0.02% for low severity.
- Why it matters: This directly supports using exposure-adjusted smoothed risk estimates (such as Empirical Bayes or full Bayesian) for hotspot identification rather than crude rates, especially for rare outcomes. My current XGBoost risk percentile implicitly does something analogous, but the paper provides explicit evidence that smoothing matters most for rare/high-severity outcomes.
- Evidence quote: "for high severity, they differ importantly… suggesting that the features of the model have an important influence on the results" (Section 4, p. 15)
- Confidence: medium (in-sample, ward level; direction of effect is plausible and well-motivated)

**Finding 3:**
- Finding: The paper confirms that ward-level traffic volume (AADF × road length summed) is an operationally feasible exposure offset for Poisson-based road accident models using DfT AADF data and OS road network data. Single-year traffic counts were used across the full 9-year study period without instability.
- Why it matters: Supports the mathematical structure of my Stage 2 Poisson offset. The exposure construction (AADF × length) is structurally similar to my log(AADT × link_length_km × 365 / 1e6) offset.
- Evidence quote: "traffic counts based on the middle year, 2009, were used for the analysis… very stable across all the years that were considered in the study" (Section 2, p. 4–5)
- Confidence: medium (different spatial unit; no uncertainty propagation tested)

**Finding 4:**
- Finding: The paper reports that approximately 60–65% of spatial variability in accident rates is spatially structured (CAR component) rather than unstructured heterogeneity (fracφ = 0.60–0.65 for preferred model E). This is after controlling for traffic-volume exposure.
- Why it matters: This suggests that substantial spatial autocorrelation remains in road accident data even after exposure adjustment. For my pipeline, this is relevant to whether residuals from my Poisson GLM/XGBoost model are spatially autocorrelated, and whether a spatial random effect or spatial features (e.g. centrality, neighbouring road class) would improve fit.
- Evidence quote: "the spatial fraction fracφ… distributed around 0.646 for accidents of low severity, and 0.602 for accidents of high severity" (Section 4, p. 13)
- Confidence: low-medium (ward level; may not transfer to link level where spatial structure is very different)

**Finding 5:**
- Finding: The paper shows a downward temporal trend in accident rates 2005–2013 for both severity levels, with different trend shapes: near-linear for low severity, flattening after 2010 for high severity. Separate temporal components per severity were preferred over a shared trend.
- Why it matters: My pipeline uses 2015–2024 data. A known temporal trend in raw counts means that including year as a feature or modelling temporal effects is important to avoid confounding time trends with spatial risk signals. The different trend shapes by severity suggest a year-by-severity interaction may be needed if I split by severity.
- Evidence quote: "Although for low severity an almost linear pattern is observed, for high severity the downward trend becomes flatter after 2010" (Section 4, p. 13)
- Confidence: medium (England-wide trend confirmed by DfT data; may differ for my 2015–2024 window)

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Poisson log-linear model with AADF × length traffic-volume offset | Mathematical structure directly matches my Stage 2 offset; confirms approach | STATS19, AADF, road lengths | 7,932 wards × 9 years | High — I already use this structure | Stage 2 (already present; document/validate) | Low | Not novel; already implemented |
| Posterior predictive checks (pBayes) as model adequacy diagnostic | Tests whether model can reproduce observed count distribution; not in my current pipeline | Fitted Bayesian model or posterior samples | Any scale | High | Stage 2 / validation | Low-medium | In-sample only; does not replace held-out validation |
| Severity-split modelling (separate or joint outputs for KSI vs. slight) | Paper provides evidence that severity levels have different spatial patterns and should not be collapsed; supports adding a severity-stratified output | STATS19 severity field | Ward level | Medium — feasible at link level but rare counts for KSI will be very sparse at link-year level | Stage 2 / future feature | Medium | KSI counts at link-year level will be near-zero for most rows; may need aggregation |
| Ranking comparison: crude rates vs. model-smoothed rates | Diagnostic to show effect of smoothing on hotspot identification; quantifies how much modelling changes rankings | Existing pipeline outputs | Any | High | Validation / documentation | Low | In-sample only |
| Prior sensitivity analysis (alternative hyperpriors on variance parameters) | Good practice to check robustness of Bayesian model outputs | Existing Bayesian model | Any | High | Stage 2 / validation | Low | Only relevant if Bayesian model is used |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full Bayesian MCMC spatial random effects (BYM/MBYM) at link level | Paper ran for 20–27 hours per model at 7,932 wards × 9 years. At 2.17M links × 10 years, MCMC is computationally unrealistic. | No specific data gap; purely computational | 7,932 × 9 = ~71k rows | Very low | Approximate methods (INLA) or spatial features as proxies for spatial autocorrelation; Empirical Bayes shrinkage (already in repo as diagnostic) | High confidence this does not transfer at production scale |
| MCAR (multivariate CAR) joint severity modelling via MCMC | Requires full MCMC; even more expensive than univariate BYM at link scale | Computational | 7,932 wards | Very low | Separate XGBoost models per severity class as proxy; or aggregate to small area for exploratory analysis | High |
| Ward-level spatial aggregation as primary analysis unit | Masks within-ward variation; not meaningful for link-level risk | Ward geography | England (7,932 wards) | Not applicable — different spatial scale | Not applicable; my unit is the link | N/A |
| Single-year traffic volume fixed across all years | Paper justifies this with stability of DfT counts 2005–2013; my 2015–2024 period includes COVID disruption (2020–2021) with large traffic volume changes | Temporally stable traffic counts | England | Low — COVID years make fixed exposure incorrect | Year-specific estimated AADT already in my pipeline; correct approach | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Yes, directly. The paper uses an AADF × road-length traffic-volume offset as the Poisson denominator, which is structurally identical to my current Stage 2 exposure offset. This is one of the paper's central methodological choices.

- **Does it suggest better handling of AADT/AADF uncertainty?** No. The paper uses a single fixed-year AADF value per segment with simple neighbour-average imputation for missing values and no uncertainty propagation. My approach (Stage 1a ML estimator with CV R² 0.83) is already more sophisticated. The paper offers no guidance on uncertainty propagation from estimated AADT into the collision model.

- **Does it suggest useful geometry or road-context features?** Not directly — the paper uses no road geometry or context features in the model. The Discussion section mentions road type, rural/urban classification, and motorway presence as candidate future covariates (Section 5, p. 18), consistent with features already in my pipeline.

- **Does it suggest better modelling of junctions?** No. Junctions are not addressed at ward level.

- **Does it suggest better treatment of severity?** Yes, conditionally. The paper provides evidence that slight and severe/fatal accidents have different spatial patterns and temporal trends, and that modelling them jointly improves fit. This supports considering a severity-stratified output in my pipeline, though the computational approach (MBYM via MCMC) does not transfer at my scale.

- **Does it suggest better validation design?** No — the paper has no holdout validation. It does not improve on my existing grouped link-split validation design.

- **Does it expose a weakness in my current approach?** Partially. My current Stage 2 does not model severity separately — it uses total injury collision count. The paper provides evidence (from a different spatial scale) that severity levels are correlated but distinct in spatial structure, which I am not currently exploiting.

---

## 15. Repo Actionability

**Action 1:**
- Suggested repo action: Add documentation note to Stage 2 documenting that the Poisson log-linear structure with an AADF × link-length offset is consistent with the Bayesian road accident literature (Boulieri et al. 2016 and cited papers). Note that the paper confirms the mathematical exposure-offset choice but at a coarser spatial scale.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Paper uses structurally identical Poisson offset; confirms this is standard in the field
- Evidence: Equation 1 and Section 2 traffic volume construction, pp. 5 and 7
- Effort: low
- Risk if implemented badly: None (documentation only)

**Action 2:**
- Suggested repo action: Add a diagnostic comparing crude collision rate rankings vs. model-smoothed risk percentile rankings for high-severity (KSI) links, to quantify how much Stage 2 modelling changes hotspot identification relative to raw counts.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Paper shows (in-sample) that smoothing substantially reorders high-severity rankings; analogous diagnostic would confirm my XGBoost risk percentile is doing useful work beyond crude rates
- Evidence: Section 4, Fig. 4, rank comparison results, p. 15
- Effort: low
- Risk if implemented badly: Low; purely diagnostic, no production change

**Action 3:**
- Suggested repo action: Add a documentation note or design discussion on severity-stratified outputs (separate KSI vs. slight models). Note that at link-year level, KSI counts will be extremely sparse (far more so than at ward level in this paper) and that direct replication of the paper's approach is not computationally or statistically feasible at 2.17M links. Flag as a future feature requiring spatial or temporal aggregation before severity splitting is stable.
- Action type: documentation note / candidate future feature
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Paper provides evidence of distinct spatial and temporal patterns per severity; at ward level this is tractable; at link level, KSI sparsity is a significant obstacle
- Evidence: Section 4 severity-specific results and Discussion p. 18
- Effort: low (documentation); high (implementation)
- Risk if implemented badly: KSI model at link-year level will be degenerate or require heavy regularisation; naive implementation will produce unstable rankings

**Action 4:**
- Suggested repo action: Add a note to the AADT/exposure section of Stage 2 documentation that the paper treats traffic volume as fixed across years (single 2009 AADF), and flag that my 2015–2024 window includes COVID-affected years (2020–2021) where this simplification would be incorrect. Document that year-specific AADT estimation (Stage 1a) is the appropriate approach for this reason.
- Action type: documentation note
- Relevant stage: Stage 1a / Stage 2 / documentation
- Why the paper supports it: Paper's single-year-exposure assumption is a methodological simplification that my pipeline already avoids; documenting why strengthens the design rationale
- Evidence: Section 2, traffic count discussion, p. 4–5
- Effort: low
- Risk if implemented badly: None

**Action 5:**
- Suggested repo action: If a Bayesian model is added in future (e.g. INLA-based spatial model as a diagnostic variant), implement posterior predictive checks (pBayes) as an adequacy diagnostic alongside DIC for model comparison, following the methodology in Section 3.5 of this paper.
- Action type: candidate model extension (future) / documentation of methodology
- Relevant stage: Stage 2 / validation
- Why the paper supports it: pBayes is a principled in-sample adequacy check for Bayesian models; the paper provides a clean implementation reference
- Evidence: Section 3.5, pp. 9–10; Table 6, p. 15
- Effort: low (if INLA model already exists); medium (if new Bayesian model needed)
- Risk if implemented badly: pBayes must not be misrepresented as external validation; it is in-sample only

---

## 16. Query Tags

- STATS19
- severity-model
- exposure-offset
- AADF-traffic-volume
- ward-level
- Bayesian-hierarchical
- BYM
- MCAR
- multivariate-severity
- space-time-model
- Poisson-lognormal
- CAR-random-effects
- RW1-temporal
- hotspot-ranking
- posterior-predictive-check
- DIC-model-comparison
- England-study-area
- in-sample-only
- MCMC-computationally-intensive
- no-holdout-validation

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper:
  - Exact imputation procedure for missing AADF links is only briefly described (neighbour average); no details on how many links were imputed or the magnitude of this uncertainty
  - Supporting material figures (additional pBayes maps, sensitivity analysis plots) are referenced but not available in the uploaded PDF
  - The paper does not report predictive metrics on held-out data; it is not possible to assess external predictive performance from this paper alone
  - Road type breakdown within wards (e.g. proportion motorway vs. A-road vs. minor) is not reported; minor roads are excluded from the traffic volume calculation without explicit justification of coverage impact
- Parts of the paper that need manual checking:
  - Table 5 parameter estimates: the paper notes a correction to the published text on page 13 regarding φi variance changes; the correction has been applied in the version provided, but the reader should verify the corrected sentence is the version they are using
  - The Wishart prior diagonal entries (500 for diagonal, 0.0005 for off-diagonal) and sensitivity analysis alternatives should be verified against the online supporting material if this methodology is to be replicated
- Any likely ambiguity or risk of misinterpretation:
  - The DIC improvement from model A to model E (~135,000 units) is very large and may be misread as strong external validation evidence. It is not. DIC is in-sample model comparison only, as the authors explicitly state.
  - The paper uses the term "hot spots" loosely in places; the authors explicitly clarify they are not doing formal hotspot analysis in the engineering/network screening sense (Section 5, p. 18). This distinction matters for how findings are interpreted relative to my pipeline.
  - The spatial fraction (fracφ ~0.60–0.65) is computed from conditional variances and is an approximation of the marginal spatial fraction; it should not be directly compared across different model specifications or different spatial scales without adjustment.
