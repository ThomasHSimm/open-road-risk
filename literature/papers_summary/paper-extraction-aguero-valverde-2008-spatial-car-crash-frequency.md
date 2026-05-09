# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Paper08-0088RG.pdf
- Suggested Markdown filename: paper-extraction-aguero-valverde-2008-spatial-car-crash-frequency.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 21-page paper accessible including all tables and figures. Published as Transportation Research Record 2061, pp 55–63.

---

## 1. Citation

- Title: Analysis of Road Crash Frequency with Spatial Models
- Authors: Jonathan Aguero-Valverde, Paul P. Jovanis
- Year: 2008 (TRB Annual Meeting submission; published TRR 2061)
- DOI or URL: Not stated in paper. Published as: Aguero-Valverde, J. and Jovanis P. 2008. Transportation Research Record 2061, pp 55–63.
- Country / region studied: USA (Centre County, rural Pennsylvania)
- Study setting: rural (rural undivided two-lane roads only)

---

## 2. Core Objective

- One-sentence description: The paper tests whether adding spatially correlated random effects (Conditional Autoregressive, CAR) to a Full Bayes Poisson log-normal crash frequency model improves model fit and reduces parameter bias compared to a model with only unstructured heterogeneity, using segment-level crash data for rural two-lane roads.
- Main purpose: safety performance function (SPF) / model specification / spatial autocorrelation assessment
- Evidence quote or page reference: "The purpose of this research is to explore the effect of spatial correlation in models of road crash frequency at the segment level." (Abstract, p. 2)

---

## 3. Response Variable

- Target variable: Annual crash count per road segment (all reportable crashes, segment locations only — intersections and ramps excluded)
- Collision type: all injury crashes reportable to PennDOT; property-damage-only crashes under-represented due to reporting thresholds. Severity not separated.
- Severity handling: Combined (all reportable crashes). No severity stratification.
- Count, binary, rate, risk score, severity class, or other: count (Poisson)
- Time window used for outcomes: 4 years (2003–2006), modelled as segment × year panel (though the model structure in Equation 2 uses a time index, the results table does not show time-varying coefficients — temporal variation appears to be treated as additional within-segment variation absorbed by the random effects)
- Evidence quote or page reference: "The data for the models were obtained at the segment level for 4 years for the state-maintained rural undivided two-lane network of Centre County." (p. 9)

---

## 4. Exposure Handling

- Exposure variable used: AADT (segment-level Annual Average Daily Traffic) as a log-linear covariate; segment length as a log-linear offset fixed to coefficient 1.0
- Traffic count source: Pennsylvania Road Management System (RMS) — observed AADT per segment per year. Not stated whether these are directly counted or imputed/interpolated values.
- Whether exposure is modelled, observed, assumed, or ignored: AADT treated as observed covariate (βV × ln(AADT)); segment length treated as offset (coefficient fixed to 1). Preliminary models showed the length coefficient was not significantly different from 1, supporting this choice.
- Treatment of missing or sparse traffic counts: Not discussed. The data are from a state road management system with presumably complete AADT coverage for state-maintained roads. Sparse count handling is not a focus.
- Whether offset terms, rates, denominators, or normalisation are used: Yes — segment length included as a log-linear offset with coefficient fixed to 1.0. This is equivalent to modelling crash rate per unit length. AADT enters as a separate log-linear covariate (not as part of the offset), allowing the AADT elasticity to be freely estimated. The model does not use a vehicle-miles-travelled (VMT = AADT × length) combined offset; it separates length (offset) from AADT (covariate). This allows testing whether crash frequency scales proportionally with length and non-proportionally with AADT.
- Evidence quote or page reference: "Note also that the length of the segment is included as an offset in the model which means that crash frequency is considered proportional to segment length. Preliminary models showed that the coefficient for segment length was not significantly different from one...therefore, it was fixed to one." (p. 8)
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The mathematical exposure structure (length offset + AADT covariate) is directly analogous to Open Road Risk Stage 2, which uses log(AADT × length × 365 / 1e6) as a combined offset. The difference is that Open Road Risk's offset combines AADT and length into a single VMT-equivalent term rather than estimating the AADT elasticity freely. This paper estimates AADT elasticity (βV ≈ 0.63–0.71 across models, Table 2), which is informative for checking whether Open Road Risk's implicit assumption of elasticity = 1.0 (via combined offset) is appropriate. The paper's traffic count source (RMS — state road management system) is structurally equivalent to DfT AADF count data.

---

## 5. Spatial Unit of Analysis

- Unit: Road segment (state-maintained rural two-lane road segments, as defined by the Pennsylvania Road Management System)
- Segment length or segmentation rule: Segments defined by RMS — not fixed-length. Mean length 0.464 miles (std dev 0.107 miles), range 0.039–0.751 miles (Table 1). This is variable-length segmentation following administrative/geometric boundaries, directly comparable to OS Open Roads link geometry.
- How crashes are assigned to the network: Crashes spatially attributed to segments using a concatenated county-route-segment location code from PennDOT Crash Reporting System. Intersection and ramp crashes excluded.
- Treatment of junctions/intersections: Explicitly excluded. "The data includes reportable crashes for road segment locations only (i.e. those that do not occur at an intersection or ramp junction)." (p. 9). This means the results apply only to mid-link crashes, not junction crashes — a significant scope limitation.
- Spatial aggregation risks: Not discussed. Segments are administrative units; variable length means crash density varies by segment. The CAR model uses topology-based (adjacency) neighbouring rather than distance-based, which may not accurately represent the spatial decay of correlation along routes of different lengths.
- Evidence quote or page reference: "A total of 865 rural two-lane segments were included in the analysis." (p. 9)
- Relevance to OS Open Roads link-based pipeline: High. OS Open Roads links are structurally analogous to the RMS segments used here — variable-length, network-defined units. The segment-level CAR spatial model is directly conceptually applicable. The explicit exclusion of junction crashes is noted: Open Road Risk currently snaps all crashes to links (including junction-proximate crashes), which would introduce noise not present in this paper's data.

---

## 6. Temporal Unit of Analysis

- Years covered: 2003–2006 (4 years)
- Temporal resolution: Annual (crash counts aggregated by segment-year). The model includes a time index (t) in Equation 2, but the random effects (vi, ui) are segment-level only — they do not vary by year. Year-to-year variation within a segment is absorbed by the Poisson process variance and the segment-level random effects.
- Whether seasonality or time-of-day is modelled: Not modelled. Annual totals only.
- Whether before-after or panel structure is used: Panel structure (segment × year) in data collection, but the spatial model does not exploit the temporal dimension for trend or autocorrelation modelling.
- Evidence quote or page reference: "All data were collected for calendar years 2003 to 2006." (p. 9)
- Relevance to WebTRIS-style time profiles: None direct. The paper does not use time-of-day data.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| ln(AADT) | Pennsylvania RMS (state road management system) | Log-transformed continuous variable; freely estimated coefficient βV | Primary exposure/risk driver; elasticity ~0.63–0.71 across models | Already present in Open Road Risk — compare estimated AADT elasticity against this paper's values |
| Segment length (offset) | Pennsylvania RMS | Log-linear offset, coefficient fixed to 1.0 after preliminary testing | Normalises crash count to per-mile rate; controls for segment length variation | Already present in Open Road Risk as part of VMT offset |
| Shoulder width (categorical) | Pennsylvania RMS road inventory | Categorical indicators: <4', 4–6', 6' (base), 6–10', ≥10' | Shoulder width <4' and 6–10' significant in spatial models (positive sign, counterintuitively); not significant in heterogeneity-only model. Sign is unexpected. | Medium — UK equivalent is carriageway width or hard strip width from OS/OSM; not directly equivalent. Counterintuitive signs suggest confounding. |
| Lane width (categorical) | Pennsylvania RMS road inventory | Categorical indicators: <10', 10–12', 12' (base), 12–14', ≥14' | Significant in heterogeneity-only model but loses significance in spatial models — suggests spatial confounding was biasing the lane width estimate | Medium — UK lane width available in some datasets; not directly equivalent |
| Functional class (Expressway/Arterial vs. Collector/Local) | Pennsylvania RMS | Binary indicator | Not significant in any model (95% credible sets include zero) | Already present in Open Road Risk as road classification |
| Speed limit (≤35 MPH vs. >35 MPH) | Pennsylvania RMS | Binary categorical | Significant negative effect in all models (higher speed limit associated with fewer crashes in this rural context — likely confounded with road type and traffic volume) | Available in Open Road Risk via OSM; counterintuitive sign warrants caution |

---

## 8. Model Architecture

- Algorithms/models used: Full Bayes (FB) hierarchical Poisson log-normal models, estimated via MCMC (OpenBUGS 2.2, Metropolis-Hastings algorithm). Five model variants tested:
  - Model 1: Poisson log-normal with unstructured heterogeneity only (vi)
  - Model 2: Poisson log-normal with spatial correlation only — first-order CAR (ui)
  - Model 3: Poisson log-normal with both heterogeneity and first-order CAR (best-fitting model)
  - Model 4: Both, with second-order adjacency
  - Model 5: Both, with third-order adjacency
- Baseline model: Model 1 — Poisson log-normal with unstructured heterogeneity only (DIC 4203)
- Final/preferred model: Model 3 — Poisson log-normal with heterogeneity + first-order CAR (DIC 4180; ΔDIC = -23 vs. Model 1, exceeding the ΔDIC > 7 significance threshold)
- Loss function or likelihood: Poisson likelihood with log-normal random effects. Model comparison via DIC (Deviance Information Criterion).
- Offset/exposure term: ln(length) with coefficient fixed to 1.0; ln(AADT) as covariate with freely estimated coefficient.
- Spatial autocorrelation handling: Gaussian CAR prior (Besag et al. 1991) on spatially structured random effects ui. Neighbouring structures tested: first-order (directly connected segments), second-order, third-order adjacency. Weights = inverse of order (1, 1/2, 1/3). First-order adjacency provides best fit; adding higher-order neighbours does not improve DIC further (Models 4 and 5, DIC 4181, marginally worse than Model 3).
- Temporal dependence handling: Not modelled. Temporal variation absorbed into segment-level random effects and Poisson variance.
- Interpretability method: Posterior means and 95% credible intervals for all coefficients; DIC for model comparison; η (proportion of random effect variance attributable to spatial correlation) = 0.595 for Model 3.
- Evidence quote or page reference: "The proportion of variability in the random effects that is due to spatial correlation for model 3 (η) is around 59% and significantly greater than 50%." (p. 11)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model fit (comparison) | DIC | 4203 | Model 1 (heterogeneity only) | Baseline | Table 2, p. 18 |
| Model fit (comparison) | DIC | 4196 | Model 2 (spatial only, 1st order) | ΔDIC = -7; borderline significant improvement over Model 1 | Table 2, p. 18 |
| Model fit (comparison) | DIC | 4180 | Model 3 (heterogeneity + spatial, 1st order) | ΔDIC = -23 vs. Model 1; significantly better fit | Table 2, p. 18 |
| Model fit (comparison) | DIC | 4181 / 4181 | Models 4 and 5 (2nd/3rd order) | No improvement over Model 3; first-order adjacency is sufficient | Table 2, p. 18 |
| AADT coefficient | Posterior mean (95% CI) | 0.714 (0.593–0.835) | Model 1 | Heterogeneity-only estimate | Table 2, p. 18 |
| AADT coefficient | Posterior mean (95% CI) | 0.628 (0.464–0.799) | Model 2 | Spatial-only estimate; notably lower | Table 2, p. 18 |
| AADT coefficient | Posterior mean (95% CI) | 0.664 (0.482–0.840) | Model 3 | Combined model; lower than Model 1 but overlapping 95% CI | Table 2, p. 18 |
| Spatial correlation proportion | η | 0.595 (0.528–0.667) | Model 3 | ~60% of random effect variance is spatially structured | Table 2, p. 18 |
| Shoulder width <4' | Posterior mean (95% CI) | 0.240 (-0.046–0.525) | Model 1 | Not significant | Table 2, p. 18 |
| Shoulder width <4' | Posterior mean (95% CI) | 0.552 (0.139–0.967) | Model 3 | Significant (positive — counterintuitive) | Table 2, p. 18 |
| Speed limit >35 MPH | Posterior mean (95% CI) | -0.301 (-0.527 to -0.071) | Model 3 | Significant negative effect (higher speed limit → fewer crashes in this rural context) | Table 2, p. 18 |
| Mean crashes/segment/year | — | 0.310 | Observed data | Zero-heavy; very sparse | Table 1, p. 17 |

**Validation type:** In-sample model fit only (DIC). No held-out data, no cross-validation, no spatial holdout, no temporal holdout. All metrics are in-sample posterior model comparison statistics, not external predictive validation.

**Critical note on DIC:** DIC is a Bayesian model comparison metric analogous to AIC. A ΔDIC > 7 is used as the significance threshold (Spiegelhalter et al. 2002). It measures relative model fit, not absolute predictive accuracy. DIC cannot be used to claim predictive generalisation to new data.

**Are metrics likely to be optimistic for deployment?** Yes — DIC is in-sample. The paper makes no claims about external prediction; the contribution is model misspecification reduction (showing that parameter estimates change when spatial correlation is included), not predictive accuracy.

**Most relevant metric to Open Road Risk:** The AADT coefficient comparison across models is the most actionable finding. The heterogeneity-only model estimates βV = 0.714; the combined spatial model estimates βV = 0.664. If Open Road Risk Stage 2 Poisson GLM uses a VMT offset (implying elasticity 1.0 for both AADT and length), the freely estimated AADT elasticity of ~0.66 suggests the offset assumption may be slightly overweighting AADT's contribution to expected crash counts.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The mean crash count per segment per year is 0.310 (Table 1), max 7 — a very sparse, zero-heavy distribution. The Poisson log-normal model handles zero-heavy counts structurally through the Poisson likelihood combined with log-normal overdispersion (unstructured heterogeneity vi and/or spatial CAR ui). No zero-inflated or hurdle model is used.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson log-normal (PLN). The paper explicitly argues that PLN is preferable to Poisson-gamma (negative binomial) for handling low sample means (citing Lord and Miranda-Moreno, reference 37). Zero-heavy counts handled using PLN with random effects.
- Whether high-risk locations are evaluated separately: No explicit analysis of high-risk segments separately. Figure 3 maps segments with significant spatial correlation terms, which forms a natural grouping, but this is not evaluated as a separate high-risk stratum.
- Evidence quote or page reference: "Poisson log-normal specifications have being suggested recently in the context of highway safety analysis using FB hierarchical models as a better way to handle low sample mean, especially in comparison to the traditional Poisson-gamma or negative binomial approaches." (p. 8)
- Practical relevance to my sparse collision link-year dataset: High. Open Road Risk has mean collisions per link-year around 1–2% of rows with any collision — comparable sparsity to this paper's mean of 0.310 per segment-year. The PLN framing (Poisson + log-normal overdispersion) is conceptually the same as Open Road Risk's Stage 2 Poisson GLM with random effects. The paper supports this modelling choice directly.

---

## 11. Validation Strategy

- Train/test split method: None. All 865 × 4 = 3,460 segment-year observations used for model fitting and comparison.
- Spatial holdout used? No
- Temporal holdout used? No
- Grouped holdout used? No
- Cross-validation type: None. Model selection based on DIC only.
- Metrics: DIC (model comparison); posterior means and 95% credible intervals for parameters
- External validation: None
- Leakage or generalisation risks: The paper does not claim external predictive validity. It is a model specification study demonstrating that CAR random effects improve within-sample fit and reduce apparent parameter bias. The spatial CAR term is estimated from the same data as the outcome, so the spatial smoothing is an in-sample fitting operation — this is not leakage in the traditional sense but is a meaningful limitation on generalisability claims.
- Evidence quote or page reference: The paper makes no external validation claims and does not present held-out performance metrics. DIC-based model comparison is the only evaluation criterion.
- What I should copy or avoid: **Copy:** the DIC-based comparison of models with and without spatial effects as a diagnostic for whether spatial autocorrelation is present. **Copy:** the η metric (proportion of random effect variance attributable to spatial correlation) as a diagnostic. **Avoid:** treating DIC improvement as evidence of better out-of-sample prediction. **Note:** at Open Road Risk's scale (2.1M links), full Bayesian MCMC with CAR spatial effects is computationally infeasible as a production model — see Section 13.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: In this rural Pennsylvania case study, including spatial correlation (CAR) alongside unstructured heterogeneity in a Poisson log-normal model significantly improves model fit (ΔDIC = -23) compared to a heterogeneity-only model. Approximately 59% of the total random effect variance is attributable to spatial correlation.
- Why it matters: This provides evidence that crash counts on adjacent road segments are spatially correlated — adjacent links share unmeasured risk factors. Open Road Risk Stage 2 currently uses a grouped split by road link for validation but does not model spatial autocorrelation in the predictions. Ignoring spatial correlation may inflate apparent precision of parameter estimates (particularly the AADT coefficient).
- Evidence quote or page reference: Abstract and p. 11 (η = 0.595)
- Confidence: Medium — finding is from a small rural county (865 segments, one road type). Generalisation to Open Road Risk's mixed urban/rural/motorway 2.1M-link network is uncertain.

**Finding 2:**
- Finding: The estimated AADT coefficient decreases from 0.714 in the heterogeneity-only model to 0.664 in the combined spatial model (Model 3), and to 0.628 in the spatial-only model (Model 2). The paper interprets this as evidence that ignoring spatial correlation biases the AADT coefficient upward due to model misspecification.
- Why it matters: Open Road Risk Stage 2 Poisson GLM uses a combined VMT offset (AADT × length), which implicitly assumes AADT elasticity = 1.0. The freely estimated elasticity here is ~0.66. If this pattern holds in Open Road Risk, the combined offset may overstate the expected collision rate for high-AADT segments and understate it for low-AADT segments, potentially distorting the risk percentile ranking.
- Evidence quote or page reference: "More important yet is the potential of spatial correlation to reduce the bias associated with model misspecification, as shown by the change on the estimate of the AADT coefficient." (p. 11)
- Confidence: Medium — this is a 2008 result from 865 rural two-lane segments; applicability to a mixed-type UK network at 2.1M links needs testing. The credible intervals for the AADT coefficient overlap across Models 1 and 3, so the difference is not statistically distinguishable.

**Finding 3:**
- Finding: Shoulder width features that were not significant in the heterogeneity-only model (shoulder <4' and 6–10') become significant in the spatial models. Lane width <10', which was significant in the heterogeneity-only model, loses significance in the spatial models. Parameter estimates for several covariates change substantially when spatial correlation is included.
- Why it matters: This is a direct demonstration of model misspecification bias: covariates that appear significant or insignificant in non-spatial models may be confounded by unmeasured spatially correlated factors. For Open Road Risk, any spatial feature (road classification, rural/urban, geographic position) may be partially absorbing spatial autocorrelation rather than causal effects. This is a diagnostic concern for feature importance interpretation.
- Evidence quote or page reference: "the fact that the parameters did change indicates the importance of considering spatial correlation in the model." (p. 10)
- Confidence: Medium — pattern observed in a small homogeneous rural dataset; counterintuitive coefficient signs (shoulder width increases associated with more crashes) suggest residual confounding even in the spatial models.

**Finding 4:**
- Finding: First-order adjacency (directly connected segments) provides the best-fitting spatial correlation structure. Adding second and third-order neighbours does not improve DIC (Models 4 and 5, DIC 4181 vs. Model 3 DIC 4180). Spatial correlation attenuates rapidly beyond the immediate network neighbourhood.
- Why it matters: If spatial correlation is to be incorporated in Open Road Risk diagnostics, a simple first-order adjacency structure based on OS Open Roads link connectivity is sufficient — complex distance-weighted or higher-order structures add no apparent benefit in this case study.
- Evidence quote or page reference: "in the case of this analysis, the simplest spatial correlation structure (first-order adjacency) fits the data better." (Conclusions, p. 11)
- Confidence: Medium — result is consistent with Tobler's first law but based on a single rural county.

**Finding 5:**
- Finding: Segments with significant spatial correlation (ui significantly different from zero) form contiguous geographic corridors (Figure 3), which the authors suggest could be used to define project groupings for safety programming.
- Why it matters: The CAR spatial term identifies stretches of road that share correlated unexplained risk after controlling for AADT, geometry, and other covariates. This is conceptually related to Open Road Risk's goal of identifying high-risk corridors, and suggests that a spatial diagnostic run on GLM residuals could reveal corridor-level patterns not captured by link-level ranking.
- Evidence quote or page reference: "segments identified with significant spatial correlation can be grouped in corridors for further analysis and safety treatment." (p. 3)
- Confidence: Medium — the corridors in Figure 3 are visually coherent, but the paper does not quantify how much of the corridor grouping is explained by the spatial term vs. unmodelled road features.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Moran's I test on Stage 2 GLM residuals | Diagnostic: test whether GLM residuals are spatially autocorrelated. If significant, indicates spatial misspecification. Can be run on a sample of links. | OS Open Roads network topology + Stage 2 GLM residuals (already available) | 865 segments | Compatible as a diagnostic on a network sample (e.g. 10,000–100,000 links) | Stage 2 — diagnostic | Low–Medium (Python: PySAL or libpysal; requires building adjacency matrix for OS Open Roads) | Moran's I requires building an adjacency matrix; at 2.1M links this is large but sparse and feasible with sparse matrix tools |
| AADT elasticity diagnostic: freely estimate βV rather than using fixed VMT offset | Test whether the freely estimated AADT coefficient differs from 1.0 (the implicit assumption in the combined VMT offset). Run as a Stage 2 GLM diagnostic. | Existing Stage 2 data | Same as paper | Compatible — straightforward Poisson GLM modification | Stage 2 — diagnostic | Low | Freeing the AADT coefficient changes the interpretation of the exposure offset; requires careful documentation to avoid confusion with production model |
| η (spatial variance proportion) as a model diagnostic | After adding any spatial structure to a Stage 2 model variant, compute proportion of random effect variance attributable to spatial clustering | Stage 2 model outputs | Same as paper | Compatible as a diagnostic metric | Stage 2 — diagnostic | Low (if spatial model is already estimated) | Only relevant if a spatial random effect model is being tested |
| Corridor identification from spatial correlation clusters | Diagnostic: map Stage 2 GLM residuals spatially and identify persistent high-residual corridors | Stage 2 GLM residuals + OS Open Roads geometry | Same as paper | Compatible — residual mapping is feasible at 2.1M links | Stage 2 — diagnostic / documentation | Low (GIS mapping of residuals) | Residual corridors may reflect missing features rather than true spatial risk clustering |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full Bayes MCMC with CAR random effects as production model | MCMC with CAR priors requires building and inverting a sparse adjacency matrix for the full network and running tens of thousands of MCMC iterations. At 2.1M links this is computationally infeasible as a production pipeline. OpenBUGS/Stan approaches would require months of computation time at this scale. | Compute capacity | 865 segments, 4 years | Not compatible at production scale | Run on a small geographically stratified sample for diagnostic purposes only; or consider approximate spatial methods (INLA, GMRF approximations) as a research extension | High |
| Single road type (rural two-lane) model specification | Open Road Risk spans motorways, A-roads, B-roads, rural minor roads — a mixed-type network. The paper explicitly limits scope to rural two-lane roads and excludes intersection crashes. Applying these spatial correlation findings directly to a mixed network is not supported by the paper. | Not a data constraint; a scope constraint | 865 rural two-lane segments | Not directly compatible; would need road-type stratification | Stratify Stage 2 by road type/functional class and run spatial diagnostics separately per stratum | High |
| Intersection crash exclusion | The paper excludes intersection and ramp crashes. Open Road Risk snaps all STATS19 crashes to OS Open Roads links, including those near junctions. This means Open Road Risk's crash counts include junction-proximate collisions that are explicitly excluded here. | Not a data constraint; a design difference | Same | Not directly compatible | Document the difference; consider a sensitivity analysis snapping crashes to links only if >X metres from any junction | Medium |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Yes — directly. AADT is modelled as the primary covariate; segment length is used as an exposure offset. The freely estimated AADT coefficient (~0.66) is informative for checking Open Road Risk's implicit elasticity assumption.
- **Does it suggest better handling of AADT/AADF uncertainty?** Partially. The paper treats AADT as observed without discussing uncertainty. But the finding that AADT coefficient estimates change when spatial correlation is included suggests that AADT estimation error could propagate into collision model bias — relevant to Open Road Risk where Stage 1a AADT is estimated, not observed.
- **Does it suggest useful geometry or road-context features?** Yes — shoulder width and lane width are used as categorical features. Both show instability across model specifications (significance changes when spatial correlation is added), which is a warning about feature interpretation rather than a recommendation to add them.
- **Does it suggest better modelling of junctions?** No — the paper explicitly excludes junction crashes and does not model junctions. The paper notes that junction spatial correlation is a topic for future research.
- **Does it suggest better treatment of severity?** No — severity is not modelled separately.
- **Does it suggest better validation design?** The paper uses only DIC (in-sample) — no better validation design is offered. The absence of external validation is a gap.
- **Does it expose a weakness in my current approach?** Yes, on two points: (1) spatial autocorrelation in Stage 2 residuals is currently unaddressed; if significant, it implies parameter estimates are too precise (credible/confidence intervals too narrow), which would affect hotspot ranking confidence. (2) The implicit AADT elasticity = 1.0 in the VMT offset may be an incorrect assumption; the paper's freely estimated elasticity of ~0.66 is worth testing diagnostically.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Run a Moran's I spatial autocorrelation test on Stage 2 Poisson GLM residuals, using a random sample of OS Open Roads links (e.g. 20,000–50,000 links from one police force area) with a first-order adjacency matrix derived from OS Open Roads network topology. Report whether residuals are significantly spatially autocorrelated.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper demonstrates significant spatial autocorrelation in crash residuals in a rural US network. If present in Open Road Risk, it implies that the standard errors and ranking confidence intervals from the current Stage 2 GLM are too narrow.
- Evidence quote or page reference: "ignoring spatial dependence can lead to underestimation of variability." (p. 3)
- Effort: Medium (requires building OS Open Roads adjacency matrix and running Moran's I using PySAL/libpysal; feasible on a sample)
- Risk if implemented badly: Moran's I result is sensitive to adjacency definition; long links spanning multiple network contexts may produce spurious results. Should be run on a homogeneous road type subset first.

**Action 2**
- Suggested repo action: Run a diagnostic variant of the Stage 2 Poisson GLM with ln(AADT) and ln(length) as separate covariates (freely estimated coefficients) rather than the combined VMT offset. Compare the estimated AADT elasticity against 1.0 and against this paper's ~0.66. If the freely estimated elasticity is materially different from 1.0, document the implications for the production risk percentile.
- Action type: diagnostic / baseline comparison
- Relevant stage: Stage 2
- Why the paper supports it: AADT coefficient estimates range from 0.628–0.714 across models in this paper; the implicit elasticity = 1.0 assumption in the combined VMT offset is not tested in Open Road Risk.
- Evidence quote or page reference: Table 2, Volume (AADT) coefficients, p. 18
- Effort: Low (minor model specification change in existing Stage 2 pipeline)
- Risk if implemented badly: Freeing both AADT and length coefficients simultaneously may produce collinear estimates if AADT and length are correlated in the data. Run as a diagnostic only; do not replace the production model without careful validation.

**Action 3**
- Suggested repo action: Map Stage 2 Poisson GLM residuals geographically on OS Open Roads links and identify persistent high-residual corridors. Compare the geographic distribution of high residuals against road type, functional class, and rural/urban classification to test whether unexplained risk is spatially structured.
- Action type: diagnostic / documentation
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Figure 3 shows that significant spatial correlation terms form contiguous corridors in this case study. The same pattern in Open Road Risk residuals would suggest that unmeasured spatially correlated factors (weather patterns, local enforcement, road condition) are driving risk in specific corridors.
- Evidence quote or page reference: "segments identified with significant spatial correlation can be grouped in corridors for further analysis and safety treatment." (p. 3)
- Effort: Low (GIS residual mapping; Stage 2 residuals should already be available)
- Risk if implemented badly: Low — this is visualisation and exploration, not a model change.

**Action 4**
- Suggested repo action: Add a documentation note to the Stage 2 model documentation flagging that spatial autocorrelation is not currently modelled, that this may cause underestimation of parameter standard errors (and therefore overconfident hotspot rankings), and referencing this paper as the methodological basis for the concern.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper provides segment-level evidence of spatial autocorrelation in crash data and demonstrates that ignoring it biases both coefficient estimates and their precision.
- Evidence quote or page reference: "ignoring spatial dependence can lead to underestimation of variability." (p. 3); "the statistical and practical consequences of omitting consideration of spatial correlation in road segment crash models are largely unknown." (p. 5)
- Effort: Low
- Risk if implemented badly: Low — documentation only.

**Action 5**
- Suggested repo action: Consider adding Empirical Bayes (EB) shrinkage of link-level risk estimates as a production diagnostic (the paper notes EB reduces regression-to-the-mean bias in site ranking). Open Road Risk already has EB shrinkage as a diagnostic variant — document it explicitly as addressing the small-area estimation problem described in this paper.
- Action type: documentation note / validation
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper extensively discusses the small-area estimation problem (low crash counts per segment per year) and notes that EB and FB shrinkage approaches both address it. Open Road Risk's existing EB shrinkage module directly addresses this concern.
- Evidence quote or page reference: "by using spatial correlation, site estimates 'pool strength' from neighboring sites improving model estimation. This is especially true in circumstances with high random variability in the data, as is the case with most crash data." (p. 3)
- Effort: Low
- Risk if implemented badly: Low — documentation and existing feature validation.

---

## 16. Query Tags

- spatial-autocorrelation
- conditional-autoregressive
- CAR-model
- full-bayes
- Poisson-log-normal
- MCMC
- DIC
- segment-level-SPF
- AADT-elasticity
- exposure-offset
- rural-two-lane
- small-area-estimation
- regression-to-mean
- neighbouring-structure
- first-order-adjacency
- shoulder-width
- lane-width
- US-Pennsylvania
- zero-heavy-counts
- model-misspecification-bias

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: Whether the AADT values in the Pennsylvania RMS are directly counted or interpolated/imputed for each segment-year — this is relevant to exposure uncertainty. The paper does not discuss AADT uncertainty at all. The exact number of crashes per year (rather than the pooled mean across 4 years) is not shown — it is unclear how much year-to-year crash count variation exists. The paper does not test whether the spatial correlation structure differs by road type or AADT level.
- Parts of the paper that need manual checking: The counterintuitive signs for shoulder width (positive coefficient — wider shoulder associated with more crashes) and speed limit (negative — higher speed limit associated with fewer crashes) in several models are noted but not fully explained. These may reflect confounding with road type and land use not captured by the model. Before using shoulder width or speed limit as features in Open Road Risk based on this paper, the sign issue warrants review of additional literature.
- Any likely ambiguity or risk of misinterpretation: DIC must not be interpreted as external predictive accuracy. The paper's AADT elasticity findings (βV ≈ 0.66) apply to rural two-lane roads only; the elasticity for motorways, urban A-roads, and minor rural roads may differ substantially. The spatial CAR model is described as a full production-ready approach in the paper's conclusions, but at Open Road Risk's scale it is not computationally feasible — this limitation must be noted when citing the paper for guidance.