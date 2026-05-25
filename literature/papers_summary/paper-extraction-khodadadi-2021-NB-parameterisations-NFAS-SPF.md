# Paper Extraction — Methodological Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: 2021__A__Khodadadi_NFAS.pdf
- Suggested Markdown filename: paper-extraction-khodadadi-2021-NB-parameterisations-NFAS-SPF.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered as document text in context)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 10-page paper accessible. All tables (1–4) fully legible. Figure 1 (CURE plots) present as image; axis labels and curve identities legible from caption and surrounding text.

---

## 1. Citation

- Title: Application of different negative binomial parameterizations to develop safety performance functions for non-federal aid system roads
- Authors: Ali Khodadadi, Ioannis Tsapakis, Subasish Das, Dominique Lord, Yingfeng Li
- Year: 2021
- DOI or URL: https://doi.org/10.1016/j.aap.2021.106103
- Journal: Accident Analysis and Prevention 156, 106103
- Country / region studied: USA — Virginia (statewide; Virginia Department of Transportation data)
- Study setting: Rural and urban local roads; low-volume (AADT ≤ 2347 vpd); non-federal aid system (NFAS) roads — rural minor collector (6R), rural local (7R), urban local (7U)

---

## 2. Core Objective

- One-sentence description: The paper develops safety performance functions (SPFs) for low-volume NFAS roads by comparing six NB parameterisations (NB-1, NB-2, NB-P, NB1-L, NB2-L, NBP-L) across five dispersion structures in a full Bayesian framework, finding that NB-Lindley mixture models with length-only varying dispersion consistently outperform traditional NB models.
- Main purpose: Safety performance function (SPF) development; model comparison; methodological investigation of count model parameterisation for zero-heavy, low-sample-mean crash data.
- Evidence quote: "The main objective of this study is to bridge the gap in the literature and develop SPFs for NFAS roads." (Abstract, p.1)

---

## 3. Response Variable

- Target variable: Count of road crashes per segment over 5-year period (2014–2018)
- Collision type: All injury and property-damage crashes combined (total crash count; not severity-stratified in this paper). Intersection-related crashes excluded.
- Severity handling: Not separated in this study. Paper notes that separating by severity (KABCO, KAB, etc.) is identified as future work.
- Count, binary, rate, risk score, severity class, or other: Count (5-year aggregate per segment; AADT and segment length as free predictors, not formal offset)
- Time window: 2014–2018, 5-year aggregate
- Evidence quote: "the final database, including a five-year period information on 2598 segments and 5856 crashes was obtained." (p.5); "Separating the crash data by severity level (e.g., KABCO, KAB, etc.) and crash type would further improve the predictive accuracy of the model." (p.9)

---

## 4. Exposure Handling

- Exposure variable used: Ln(AADT) and segment length (miles) included as free predictors with estimated coefficients. No formal log-offset with coefficient fixed to 1.
- Traffic count source: Virginia Department of Transportation (VDOT) traffic volume data, 2014–2018. AADT counts collected from short-term count or permanent sites; some segments excluded due to "low-quality AADT counts (count estimates labeled as poor quality by the VDOT)." (p.5) This is directly analogous to Open Road Risk's AADF quality concern.
- Whether exposure is modelled, observed, assumed, or ignored: Observed for included segments; segments with poor-quality AADT excluded rather than imputed. AADT estimation error acknowledged: "Das et al. (2019) also found that AADT estimation error can affect the predicted number of crashes." (p.2)
- Treatment of missing or sparse traffic counts: Poor-quality AADT records excluded from the final dataset. No imputation performed.
- Whether offset terms, rates, denominators, or normalisation are used: No formal offset. "Segment length was considered as a separate covariate rather than an offset since its estimate was statistically different from one." (p.5) This directly parallels the Wang et al. M25 finding (length elasticity ≠ 1) and provides NFAS-specific justification for the same diagnostic in Open Road Risk.
- Evidence quote: "Segment length was considered as a separate covariate rather than an offset since its estimate was statistically different from one." (p.5)
- Transferability to my AADF/WebTRIS setup:
  - Mathematical model structure (NB with free AADT and length predictors): **High** — directly applicable to Open Road Risk's Stage 2 GLM. The key design choice — testing length as a free predictor rather than a fixed-coefficient offset — is directly relevant to the open diagnostic identified from Wang et al.
  - Data context (VDOT low-volume roads, US): **Medium** — Virginia NFAS roads are low-volume (AADT ≤ 2347 vpd), shorter segments, predominantly rural. This is more directly analogous to the lower road classes in Open Road Risk than the M25 motorway paper, though the US road classification system differs from the UK. The zero-heavy characteristic (~37% of segments zero crashes over 5 years, ~78% below 0.6 crashes/year) is closely analogous to Open Road Risk's sparse link-year structure.
- Notes: The exclusion of poor-quality AADT records rather than imputation is a different approach from Open Road Risk's Stage 1a AADT estimation for all links. If AADT estimation error inflates SPF uncertainty (as cited from Das et al. 2019), Open Road Risk's estimated-AADT approach carries a similar uncertainty that should be documented.

---

## 5. Spatial Unit of Analysis

- Unit: Road segment (NFAS road segment from VDOT roadway inventory)
- Segment length or segmentation rule: Variable length; mean 1.37 miles (range 0.1–5.73 miles) for rural minor collectors; shorter for urban local (mean 0.4 miles, range 0.1–4.52 miles). Segmentation follows VDOT road inventory; not fixed-length homogeneous segments.
- How crashes are assigned to the network: Not explicitly described; assumed standard VDOT GIS assignment from state crash database. Intersection-related crashes explicitly excluded.
- Treatment of junctions/intersections: "intersection related crashes" excluded from the dataset (p.5). This is consistent with Wang et al. but removes an important crash category.
- Spatial aggregation risks: Variable segment length introduces heterogeneity in observed crash counts — partially addressed by including length as a covariate with a varying dispersion parameter dependent on length. The authors specifically note "Cafiso et al. (2010) mentioned that in shorter segments, variability of the dispersion parameter matters more." (p.4)
- Evidence quote: "Finally, after excluding the missing records, outliers, roadways with low-quality AADT counts... and intersection related crashes, the final database, including a five-year period information on 2598 segments and 5856 crashes was obtained." (p.5)
- Relevance to OS Open Roads link-based pipeline: Moderate. NFAS road segments (mean ~1–1.4 miles = ~1.6–2.3 km) are longer than typical OS Open Roads links (~100–300m) but shorter than M25 segments (~5 km). The variable-length segmentation is analogous to OS Open Roads links. The finding that dispersion parameter varies significantly with segment length — especially for shorter segments — is directly relevant to Open Road Risk's short-link structure.

---

## 6. Temporal Unit of Analysis

- Years covered: 2014–2018 (5-year aggregate)
- Temporal resolution: Annual aggregate; 5 years pooled to a single count per segment. No within-year temporal structure.
- Whether seasonality or time-of-day is modelled: Not modelled. Cross-sectional design.
- Whether before-after or panel structure is used: Cross-sectional (single 5-year aggregate observation per segment). No panel.
- Evidence quote: "Virginia roadway information, traffic volume, and crash data from the Virginia Department of Transportation (VDOT) were gathered, processed, and integrated... from 2014 to 2018." (p.5)
- Relevance to WebTRIS-style time profiles: Not relevant to this paper. No time-of-day or seasonal structure.

---

## 7. Engineered Features

Only features explicitly used in the fitted models.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Ln(AADT) | VDOT traffic counts; short-term count or permanent sites | Natural log of annual average daily traffic (vehicles per day); poor-quality estimates excluded | Significant positive predictor in all models; AADT coefficient 0.63–0.74 across parameterisations | Already present — used as part of Open Road Risk's AADT offset; this paper uses it as free predictor. Compare implementation. |
| Segment length (miles) | VDOT roadway inventory | Raw segment length; included as free predictor (not log-transformed) | Significant positive predictor; coefficient 0.47–0.68 (sub-linear); statistically different from 1.0 | Already present as part of Open Road Risk's offset. Paper provides direct justification for testing it as a free predictor rather than fixed-offset coefficient. |
| Percentage of trucks | VDOT | Proportion of truck traffic | Tested but insignificant in all models; excluded from final models | Low — truck proportion is likely insignificant for low-volume rural roads in this context; may be more important for motorway-class links |
| Percentage of buses | VDOT | Proportion of bus traffic | Tested but insignificant in all models; excluded | Low |

Note: No geometric features (curvature, gradient, lane width, shoulder width) were available for this dataset at adequate coverage. "Roadway inventory attributes such as lane width, shoulder width, number of lanes, etc., were unfortunately, missing for a considerable number of segments." (p.5) This is a data availability constraint, not a methodological choice.

---

## 8. Model Architecture

- Algorithms/models used: Six NB parameterisations, each with five dispersion structures — 30 total model variants. All estimated under full Bayesian (FB) framework via MCMC using R package `rjags`.
  - NB-2: Standard NB (quadratic mean-variance); fixed dispersion ϕ
  - NB-1: Linear mean-variance; dispersion adjusts per site
  - NB-P: General NB; variance = μ + μᵖ/ϕ; p estimated freely
  - NB2-L: NB-2 mixed with Lindley distribution (zero-favoured)
  - NB1-L: NB-1 mixed with Lindley distribution
  - NBP-L: NB-P mixed with Lindley distribution
- Baseline model: NB-2 with fixed dispersion (most common in SPF literature)
- Final/preferred model: NB1-L and NB2-L with length-only varying dispersion (dispersion structures 3 and 4) — ranked best on WAIC, LOO, MAD, and CURE plot analysis. NB2-L best on WAIC/MASE; NB1-L best on LOO/MAD.
- Loss function or likelihood: Poisson log-likelihood (conditional on gamma or Lindley mixture); full Bayesian posterior estimation via MCMC.
- Offset/exposure term: None. Ln(AADT) and length are free predictors. Coefficient fixed at 1 not used.
- Spatial autocorrelation handling: Not addressed. Cross-sectional design; n = 2598 segments across Virginia — spatial structure not modelled.
- Temporal dependence handling: Not addressed — single 5-year aggregate cross-section.
- Interpretability method: Posterior means and standard deviations; 95% HPD credible intervals for coefficient significance (underlined if CI includes zero); CURE plots for residual diagnostics.
- MCMC details: 3 chains × 50,000 iterations; 10,000 burn-in per chain; thinning ratio 3:1. R package `rjags`.
- Dispersion structures tested:
  - Fixed ϕ (baseline)
  - ϕ = exp(η₀) × AADTη₁ × Lη₂ (AADT and length dependent)
  - ϕ = exp(η₀) × AADTη₁ × L (AADT and length, linear length)
  - ϕ = exp(η₀) × Lη₂ (length-only, power)
  - ϕ = exp(η₀) × L (length-only, linear)
- Evidence quote: Section 2, pp.2–5; Tables 2–4.

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| AADT coefficient (all models) | Posterior mean (SD) | 0.63–0.74 | All NB parameterisations, fixed dispersion | 1% increase in AADT → ~0.63–0.74% increase in crashes; sub-proportional exposure effect on low-volume roads | Tables 2–4 |
| Length coefficient (all models) | Posterior mean (SD) | 0.47–0.68 | All NB parameterisations | Sub-linear: length elasticity < 1.0; statistically different from 1.0 — fixed offset would be mis-specified | Tables 2–4 |
| Dispersion parameter ϕ (NB-2, fixed) | Posterior mean (SD) | 3.12 (0.25) | NB-2, fixed dispersion | Moderate over-dispersion; NB justified over Poisson | Table 2, p.6 |
| Lindley parameter θ (NB-L models) | Posterior mean (SD) | ~1.38–1.42 | All NB-L models, all dispersion structures | Consistently estimated; stable across parameterisations | Tables 2–4 |
| Model comparison (WAIC) | WAIC | 7481–7482 (best); 8087–8296 (traditional NB) | NB2-L / NB1-L vs NB-2 | NB-L models show WAIC ~600 lower than best traditional NB; very substantial improvement | Tables 2–4 |
| Model comparison (LOO) | LOO | 7971–7981 (NB-L); 8087–8296 (traditional NB) | NB-L vs traditional NB | NB-L consistently superior across LOO metric | Tables 2–4 |
| Model comparison (MAD) | MAD | 1.13–1.16 (NB-L); 1.24–1.38 (traditional NB) | NB-L vs traditional NB | NB-L slightly lower MAD (better predictive accuracy) | Tables 2–4 |
| Cumulative residuals (CURE) | Sum of all residuals | −3 (NB1-L); −26 (NB2-L); −235 to −339 (traditional NB) | All models, length-only dispersion | NB-L CURE converges near zero; traditional NB CURE systematically deviates | p.8 |
| Data characteristics | Zero proportion | 37% of 2598 segments | All NFAS roads | High zero-crash proportion confirms NB-L advantage | p.8 (Discussion) |
| Data characteristics | Skewness of crash counts | 2.83 | All NFAS roads | Above the Shirazi et al. (2017) threshold of 1.92 for NB-L preference | p.8 (Discussion) |
| Data characteristics | % segments < 0.6 crashes/year | 78% | All NFAS roads, annualised | Extremely low sample mean; analogous to Open Road Risk link-year sparsity | p.8 (Discussion) |
| Dispersion structure sensitivity | Performance variation across dispersion forms | Marked variation in WAIC/LOO across structures | Within each NB parameterisation | Dispersion structure choice is material; each NB variant favours different dispersion structure | Tables 2–4; Section 5 |

**Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, or not stated?**

WAIC and LOO are approximated leave-one-out cross-validation estimates computed from the full posterior without refitting — they use within-sample fits to estimate out-of-sample predictive accuracy. Specifically: "Leave-one-out cross-validation assesses the predictive accuracy of the model by estimating the prediction error for the sample i without using it to train the model... approximated by using the sample draws from the full posterior distribution." (p.8) This is stronger than DIC/AIC as a model selection criterion, but is not a fully independent spatial or temporal holdout. MAD and MASE are in-sample accuracy metrics.

**Do these metrics test predictive generalisation?**

WAIC and LOO approximate predictive generalisation using PSIS-LOO (importance sampling); they are the best available metrics in this study given no external test set is held out. They are more reliable than DIC for this type of Bayesian hierarchical model comparison. MAD and MASE measure in-sample fit only.

**Are any metrics likely to be optimistic?**

WAIC/LOO are computed on the same Virginia dataset — generalisation to other states, road systems, or time periods is not validated. The model is also flow-only (no geometric features), which means the AADT and length coefficients absorb any omitted geometric variation.

**Which metric is most relevant to Open Road Risk?**

The AADT and length coefficient values (~0.64 and ~0.50–0.68 respectively), the NB-L superiority under WAIC/LOO, and the data characteristic benchmarks (37% zeros, skewness 2.83) are most relevant. The CURE plot approach is directly implementable as a Stage 2 diagnostic.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: NB-L (Negative Binomial-Lindley) mixture model explicitly designed for datasets with large proportions of zeros and heavy tails. NB-L is described as preferred over zero-inflated (ZI) models: "The NB-L has been proposed as an alternative to the application of zero-inflated (ZI) models for handling datasets with a large percentage of zero responses. The NB-L model offers a single mean function that is never equal zero, which is not the case for the ZI model." (footnote 1, p.3)
- Use of Poisson / NB / zero-inflated / hurdle / NB-L models: NB-1, NB-2, NB-P (traditional NB), and NB1-L, NB2-L, NBP-L (NB-Lindley mixtures) — six model families, all Bayesian. No zero-inflated models. No hurdle models. Poisson not tested (implicitly dominated by NB).
- Whether high-risk locations are evaluated separately: No. All segments pooled. Road class stratification (6R, 7R, 7U) used in descriptive statistics (Table 1) but not in modelling — single combined model for all NFAS roads. Paper identifies separate-class SPFs as future work.
- Evidence quote: "In the dataset analyzed in this study, 37% and 20% of the roadways had recorded zero and one crashes for a five year period, respectively. Also... around 78% of the segments have crash frequencies below 0.6 crash per year." (p.8)
- Practical relevance to my sparse collision link-year dataset: **High and direct.** Open Road Risk's link-year structure has ~98–99% zero-crash link-years at annual resolution. The Khodadadi paper's 5-year aggregate data has 37% zeros — at annual link-year resolution the zero proportion would be much higher. This paper provides the most direct methodological guidance for handling Open Road Risk's zero-heavy counts: NB-L models outperform traditional NB models specifically when zero proportion is high and skewness exceeds ~1.92. Open Road Risk's link-year data almost certainly exceeds both thresholds.

---

## 11. Validation Strategy

- Train/test split method: None (cross-sectional; n = 2598)
- Spatial holdout used? No
- Temporal holdout used? No
- Grouped holdout used? No
- Cross-validation type: Approximate leave-one-out cross-validation (PSIS-LOO) computed from Bayesian posterior draws without re-fitting. This is the primary model selection criterion alongside WAIC.
- Metrics: WAIC, LOO (primary); MAD, MASE (secondary, in-sample); CURE plots (residual diagnostics); Log-likelihood.
- External validation: None. Virginia-only dataset; not validated on other states or road systems.
- Leakage or generalisation risks: All metrics computed on training data (LOO approximated rather than truly held out). Results specific to Virginia NFAS roads, 2014–2018. Flow-only model — geometric feature omission may bias coefficient estimates if geometry correlates with AADT or length (acknowledged as future work limitation).
- Evidence quote: "the leave-one-out cross-validation could be approximated by fitting the model once." (p.8)
- What I should copy or avoid: **Copy** the WAIC + LOO model comparison framework as primary Stage 2 model selection criteria, replacing or supplementing DIC. **Copy** the CURE plot approach for Stage 2 residual diagnostics. **Copy** the NB-L model as a candidate alternative to NB-2 for Open Road Risk Stage 2. **Avoid** treating the specific Virginia coefficient values as directly applicable to UK roads. **Note** that PSIS-LOO approximation quality should be checked (the `loo` R package provides diagnostics for whether the approximation is reliable for each observation).

---

## 12. Key Findings Relevant to My Project

**Finding 1**
- Finding: NB-Lindley (NB-L) models consistently and substantially outperform traditional NB models (NB-1, NB-2, NB-P) on datasets characterised by a large proportion of zeros (37% in this study) and high skewness (2.83). The WAIC advantage is ~600 units — not marginal. This is confirmed across multiple model specifications and multiple GOF metrics.
- Why it matters: Open Road Risk's link-year data almost certainly has a higher zero proportion and higher skewness than this study (5-year aggregate; annual link-year rate would push zeros close to 98–99%). The NB-L model is the natural next model to test after NB-2 in Stage 2. The paper also provides the threshold heuristic from Shirazi et al. (2017): skewness > 1.92 → NB-L preferred.
- Evidence: Abstract; Tables 2–4; Section 5 Discussion p.8; CURE plots Fig. 1.
- Confidence: High — consistent across 30 model variants; external validation absent but internal consistency is strong.

**Finding 2**
- Finding: Segment length coefficient is statistically significantly less than 1.0 (estimates 0.47–0.68 for NFAS roads), providing direct evidence that a fixed-offset parameterisation (coefficient constrained to 1.0) mis-specifies the mean function for this road type. This replicates the Wang et al. M25 finding in a very different road context (low-volume rural vs high-volume motorway).
- Why it matters: Two independent UK/US studies now support testing log(length) as a free predictor rather than a fixed offset in Open Road Risk Stage 2. The NFAS finding (elasticity 0.47–0.68) is particularly relevant because NFAS roads include short segments analogous to OS Open Roads links. Implementing the offset-vs-free-predictor diagnostic is now supported by two independent studies across very different road types.
- Evidence: Section 4 p.5: "Segment length was considered as a separate covariate rather than an offset since its estimate was statistically different from one."; Tables 2–4 (length coefficient 0.47–0.68 across all parameterisations).
- Confidence: High — result is consistent across all 30 model variants.

**Finding 3**
- Finding: AADT coefficient is 0.63–0.74 for NFAS roads — sub-proportional exposure effect (elasticity < 1.0). This is the opposite direction from the Wang et al. M25 finding (elasticity > 1.0). Together, these two papers suggest that AADT elasticity depends strongly on road class, and a single fixed-offset constraint is unlikely to be appropriate across a mixed-network pipeline.
- Why it matters: Open Road Risk models all road classes together with a single fixed offset. The evidence from two papers now suggests that AADT elasticity varies by road class: high (>1.0) for motorways, low (<1.0) for low-volume local roads. A facility-family split for the offset structure, or a road-class interaction with the AADT coefficient, would better reflect this variation. This is a documented TODO for Open Road Risk (facility-family split v2).
- Evidence: Tables 2–4; Wang et al. (M25, companion extraction) coefficient ~1.2–1.9.
- Confidence: High for directional finding; medium for specific values (US road context, not UK).

**Finding 4**
- Finding: Varying dispersion parameter dependent on segment length (ϕ = f(L)) outperforms fixed dispersion in all model variants. For NB-L models, length-only dispersion functions (structures 3 and 4) are preferred. For traditional NB models, AADT-and-length dependent functions are preferred. The choice of dispersion structure is both model-family-dependent and data-dependent.
- Why it matters: Open Road Risk's current Poisson GLM uses no dispersion parameter at all. If NB-2 is added as a diagnostic, the dispersion parameter should initially be fixed (standard NB-2), and then a varying-dispersion variant with length-dependent ϕ should be tested. The length-dependent dispersion finding is particularly important for short OS Open Roads links, where Cafiso et al. (2010) and this paper both show dispersion variation is more pronounced.
- Evidence: Section 5 p.8; Tables 2–4 (comparing WAIC/LOO across fixed vs varying dispersion structures).
- Confidence: High for the direction (varying > fixed); medium for which specific functional form is best (data-dependent).

**Finding 5**
- Finding: WAIC and LOO are superior to DIC for Bayesian model comparison in hierarchical count models where likelihood function and dispersion structure vary across models. DIC "lead[s] to different DIC values" depending on parameterisation and should not be used to compare models with different likelihood specifications.
- Why it matters: If Open Road Risk adds Bayesian NB or NB-L models to Stage 2, DIC should not be used as the primary comparison metric. WAIC (via the `loo` R package) is the appropriate criterion. This is an operational note for any Bayesian extension of Stage 2.
- Evidence: Section 5 p.8; Geedipally et al. (2014) cited.
- Confidence: High — well-established methodological point confirmed in this study.

**Finding 6**
- Finding: The CURE plot (cumulative residual plot) is used to diagnose model adequacy directly from residuals. NB-L CURE plots converge near zero with fewer excursions outside ±1.96 SD bounds; traditional NB CURE plots show systematic trends. The sum of cumulative residuals for NB1-L = −3 vs −235 to −339 for traditional NB models.
- Why it matters: CURE plots are a low-effort diagnostic for Stage 2 that are not currently implemented in Open Road Risk. They directly address the question of whether the GLM is systematically mis-fitted over the AADT range, which is one of the open diagnostics in the pipeline. The method requires only the observed counts and predicted means from any fitted SPF.
- Evidence: Section 4 pp.7–8; Fig. 1.
- Confidence: High — CURE is a standard and well-validated SPF diagnostic (Hauer and Bamfo 1997).

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| NB-L (NB-Lindley) model as Stage 2 candidate | Best-performing model for zero-heavy, high-skewness crash data; superior WAIC/LOO vs NB-2; Open Road Risk link-year data almost certainly exceeds the NB-L preference thresholds (37% zeros and skewness 2.83 in this paper; Open Road Risk likely ~98–99% zeros at link-year) | STATS19 crash counts (already in pipeline); AADT estimates from Stage 1a; link length | 2598 segments, Virginia | Compatible — model is computationally feasible at 21.7M rows using frequentist NB-L or Bayesian on a sample. Bayesian MCMC may require sampling strategy at full scale. | Stage 2 — candidate model extension | Medium (Bayesian: high compute cost at full scale; frequentist NB-L: available in R; consider on sampled subset first) | At 21.7M link-years, full Bayesian MCMC will be slow. Frequentist NB-L or approximate Bayesian (INLA) recommended. The model may be better tested on a motorway-class or high-volume subsample first. |
| CURE plots for Stage 2 residual diagnostics | Directly diagnoses systematic mis-fit over AADT range; low implementation effort; standard SPF diagnostic | Observed crash counts + GLM predicted means (already available from current Stage 2 GLM) | 2598 segments | Fully compatible — applicable to any count model | Stage 2 / validation / diagnostic | Low (compute cumulative residuals from existing GLM output; plot vs AADT and length) | None — pure diagnostic, no model change |
| Length as free predictor vs fixed offset (diagnostic) | Two papers now support testing this (Wang et al. M25, Khodadadi et al. NFAS). Khodadadi provides direct justification: "estimate was statistically different from one." | AADT and length (already in pipeline) | 2598 segments | Compatible | Stage 2 — diagnostic | Low (one additional model fit) | See Wang et al. extraction Action 2 |
| AADT as free predictor vs fixed offset (diagnostic) | NFAS AADT elasticity ~0.63–0.74; M25 elasticity ~1.2–1.9; both differ from 1.0 in opposite directions. Together they justify road-class-stratified offset testing in Open Road Risk. | AADT (already in pipeline); road class (already in pipeline) | 2598 segments | Compatible | Stage 2 — diagnostic | Low | See Wang et al. extraction Action 1 |
| Varying dispersion parameter dependent on length (NB-2 extension) | Addresses the known issue that shorter OS Open Roads links have higher dispersion; directly supported by this paper and Cafiso et al. (2010) | Length (already in pipeline) | 2598 segments | Compatible | Stage 2 — candidate model extension / diagnostic | Medium (requires NB-2 with varying dispersion; implementable in frequentist glmmTMB or Bayesian rjags/Stan) | Adds parameter estimation complexity; dispersion functional form is data-dependent and may need cross-validation to select |
| WAIC + LOO as primary Bayesian model comparison metrics (replacing DIC) | Paper and cited literature show DIC is unreliable when comparing models with different likelihood specifications; WAIC/LOO preferred | Full posterior draws (requires Bayesian estimation) | 2598 segments | Compatible | Stage 2 / validation — relevant if Bayesian models added | Low (use `loo` R package given MCMC output) | Only relevant if Bayesian estimation added to Stage 2; current frequentist GLM uses AIC/deviance |
| Skewness and zero-proportion as pre-modelling diagnostics for model family selection | Shirazi et al. threshold: skewness > 1.92 → NB-L preferred. Compute for Open Road Risk link-year crash distribution and document. | STATS19 crash counts (already in pipeline) | N/A | Fully compatible | Stage 2 / documentation / diagnostic | Low | None — descriptive statistic only |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full Bayesian MCMC at production scale | 50,000 iterations × 3 chains for n = 2598; at 21.7M link-years, MCMC is computationally infeasible | Compute cost; MCMC does not scale linearly | 2598 segments | Incompatible at full 21.7M-link scale | Frequentist NB-L (R package available); INLA for approximate Bayesian inference; Bayesian on a stratified sample (~50,000 link-years) | High |
| Flow-only SPF without geometric features | Khodadadi used flow-only because geometry data was missing; this is a data constraint, not a modelling recommendation. Open Road Risk has geometry features (gradient, curvature, road class) and should use them | Geometric data unavailable in VDOT NFAS dataset | 2598 segments | Incompatible as a design choice — Open Road Risk should retain geometry features | Not applicable — continue using geometry features | High |
| Virginia coefficient values for UK prediction | NFAS Virginia roads (AADT ≤ 2347 vpd, miles-scale lengths, US road geometry) are not directly comparable to UK OS Open Roads links | Different country, road system, casualty reporting (STATS19 vs VDOT), units | 2598 segments | Incompatible for direct coefficient transfer | Re-estimate on Open Road Risk data; treat Virginia values as directional benchmarks only | High |
| Segment-level SPF without road-class stratification (combined NFAS) | Paper explicitly identifies stratification by road class (6R, 7R, 7U) as future work because the combined model may mask class-specific effects | Single pooled model for heterogeneous road types | 2598 segments | Incompatible — Open Road Risk already uses road class as a feature; should retain or extend facility-family approach | Already addressed in Open Road Risk's facility-family split | Medium |

---

## 14. Pipeline Implications

**Does this paper support using exposure-normalised collision risk?**
Yes — AADT and segment length are confirmed as significant positive predictors in all 30 model variants. However, both have sub-linear elasticities on NFAS roads (AADT ~0.64, length ~0.50–0.68), directly supporting the recommendation to test these as free predictors rather than fixed-offset components in Open Road Risk.

**Does it suggest better handling of AADT/AADF uncertainty?**
Yes — the paper explicitly excludes poor-quality AADT estimates rather than imputing them, and cites Das et al. (2019) finding that AADT estimation error affects predicted crash frequencies. For Open Road Risk's Stage 1a estimated AADT, this implies that AADT uncertainty should be propagated into Stage 2 predictions. This is currently not implemented and should be documented as a known limitation.

**Does it suggest useful geometry or road-context features?**
Indirectly — by noting that geometry data was unavailable and that this is a limitation. The paper's flow-only result (AADT coefficient ~0.64) likely reflects partial absorption of geometric effects into the AADT term. Geometry features should be retained in Open Road Risk.

**Does it suggest better modelling of junctions?**
Not directly — junction crashes are excluded. This is a limitation shared with Wang et al.

**Does it suggest better treatment of severity?**
Yes — paper identifies severity stratification (KABCO, KAB) as future work and notes it would improve predictive accuracy. Open Road Risk models all injury collisions combined; a KSI sub-model would be a natural but sparse extension.

**Does it suggest better validation design?**
Yes — WAIC and LOO are recommended over DIC for Bayesian hierarchical model comparison. CURE plots are recommended as residual diagnostics for SPF adequacy. Neither is currently implemented in Open Road Risk.

**Does it expose a weakness in my current approach?**
Three specific weaknesses:
1. Fixed log-offset (β_length = β_AADT = 1) is now contradicted by two independent papers across different road types. Testing free predictors is a low-effort diagnostic that should be prioritised.
2. Poisson GLM (no dispersion) is a less appropriate model family than NB-2 or NB-L for zero-heavy data. NB-2 is already a documented TODO; NB-L is now a supported next step.
3. No CURE plots currently implemented — a standard SPF diagnostic that is straightforward to add.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Compute and report the skewness and zero proportion of the Open Road Risk link-year crash count distribution (annual and aggregated). Compare against the Shirazi et al. (2017) threshold (skewness > 1.92 → NB-L preferred) and document. This is a pre-modelling diagnostic that costs nothing and determines whether NB-L is a priority.
- Action type: Diagnostic
- Relevant stage: Stage 2 / pre-modelling data analysis
- Why the paper supports it: "for crash data with skewness higher than 1.92 (2.83 in this study) the NB-L model performs better." (p.8)
- Evidence: Section 5, p.8; Shirazi et al. (2017) threshold.
- Effort: Low (single descriptive statistics computation)
- Risk if implemented badly: None — descriptive only

**Action 2**
- Suggested repo action: Implement CURE plots for the current Stage 2 Poisson GLM (cumulative residuals sorted by AADT, then by link length). This directly tests whether the GLM is systematically mis-fitted over the AADT or length range. If CURE shows systematic trends, this motivates testing NB-2 or NB-L alternatives and/or freeing the offset coefficients.
- Action type: Diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: CURE plots are the primary residual diagnostic in this paper; the contrast between NB-L (near-zero cumulative residuals) and traditional NB models (−235 to −339) demonstrates diagnostic power. Standard SPF tool since Hauer and Bamfo (1997).
- Evidence: Section 4, p.7–8; Figure 1; Hauer and Bamfo (1997) cited.
- Effort: Low (compute cumulative sum of (observed − predicted) sorted by covariate; ±1.96×SD confidence bands)
- Risk if implemented badly: CURE plots require careful ordering by covariate and correct confidence band computation; see Hauer and Bamfo (1997) for exact specification.

**Action 3**
- Suggested repo action: Test NB-2 (negative binomial with quadratic mean-variance) as an alternative to the current Poisson GLM in Stage 2. Compare using AIC (frequentist) or WAIC/LOO (if Bayesian). If NB-2 substantially outperforms Poisson, add as the production GLM. This is already a documented TODO; this paper adds urgency to it.
- Action type: Diagnostic / candidate model extension
- Relevant stage: Stage 2
- Why the paper supports it: NB-2 with fixed dispersion has WAIC 8232 vs NB-1 WAIC 8296 — substantial improvement over linear variance structure. Even the simplest NB-2 substantially outperforms Poisson (not tested in this paper, but standard in the literature).
- Evidence: Table 2; Section 1 literature review.
- Effort: Low (NB-2 available in standard Python GLM libraries e.g., `statsmodels`, `glm` in R)
- Risk if implemented badly: Dispersion parameter estimation can be unstable with very low sample mean values (Lord and Miranda-Moreno, 2008 cited in paper). At link-year level with ~99% zeros, NB-2 dispersion may be poorly identified — start with a sampled or road-class-filtered subset.

**Action 4**
- Suggested repo action: Add NB-L (Negative Binomial-Lindley) as a candidate model for Stage 2, initially tested on a stratified sample (e.g., 100,000 link-years from the pipeline). Use frequentist implementation (R package for NB-L exists; Python implementation available via the paper's references) rather than full Bayesian MCMC at production scale. Compare against NB-2 using AIC or approximate LOO.
- Action type: Candidate model extension
- Relevant stage: Stage 2
- Why the paper supports it: NB-L consistently outperforms all traditional NB parameterisations with WAIC advantage of ~600+ units; superior CURE convergence; directly addresses the zero-heavy characteristic of Open Road Risk link-year data.
- Evidence: Tables 2–4; Section 5 p.8; footnote 1 p.3.
- Effort: Medium (frequentist NB-L implementation; sampling strategy for scale)
- Risk if implemented badly: NB-L is more complex than NB-2; identifiability of the Lindley parameter θ requires careful prior specification in Bayesian form. In frequentist form, maximum likelihood estimation of NB-L can be unstable for very small mean values. Test on a filtered subset with non-trivial crash counts first.

**Action 5**
- Suggested repo action: Document the joint finding from Wang et al. (M25) and Khodadadi et al. (NFAS) that segment length elasticity is significantly below 1.0 in both motorway (~0.68–0.79) and low-volume road (~0.47–0.68) contexts. Add a Stage 2 TODO: test log(length) as a free predictor, stratified by road class (motorway vs non-motorway), as a prerequisite to the facility-family split v2.
- Action type: Documentation note / diagnostic prerequisite
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Two independent papers with very different road contexts agree that length elasticity ≠ 1.0. The combined evidence is stronger than either paper alone.
- Evidence: Khodadadi et al. p.5; Wang et al. Tables 2–3 (companion extraction).
- Effort: Low (documentation); Low-Medium (diagnostic — one additional GLM fit per road class)
- Risk if implemented badly: None for documentation; see Wang et al. Action 2 for diagnostic risks.

---

## 16. Query Tags

- negative-binomial
- NB-Lindley
- NB-L
- zero-heavy-counts
- low-volume-roads
- NFAS
- rural-local
- SPF-development
- Bayesian-MCMC
- WAIC
- LOO-cross-validation
- CURE-plot
- dispersion-parameter
- varying-dispersion
- segment-length-elasticity
- AADT-elasticity
- flow-only-model
- rjags
- Virginia-USA
- low-sample-mean
- skewness-threshold
- over-dispersion-diagnostic
- no-geometry-features
- no-spatial-holdout

---

## 17. Confidence and Gaps

- Overall confidence in extraction: High
- Important details not stated or ambiguous:
  - The paper uses 5-year aggregate counts but the AADT is described as "AADT over 5 years (vpd)" in Table 1 — this appears to mean the 5-year average annual AADT, not a 5-year total. The maximum value (2347 vpd) confirms this is a daily flow rate, not a 5-year cumulative. **Confirm this interpretation** — it matters for computing the exposure term.
  - Road class stratification: all 2598 segments modelled jointly (not separately by 6R, 7R, 7U). Descriptive statistics by class are in Table 1 but no class-specific models are reported. Paper identifies this as future work.
  - Frequentist vs Bayesian implementation details for NB-L at scale: not discussed. For Open Road Risk, a frequentist implementation would be more practical; the paper does not assess frequentist NB-L.
  - The `rjags` MCMC details (thinning, convergence diagnostics beyond chain count) are not fully stated. Trace plots and Gelman-Rubin statistics are not reported.
- Parts needing manual checking:
  - Table 1: Urban local roads (N = 365) have mean AADT 874 vpd, mean length 0.4 miles — these are very short segments with low AADT. Ensure the pipeline equivalent (short OS Open Roads links in urban areas) has comparable exposure characteristics before applying NB-L thresholds.
  - Tables 2–4: Several dispersion function η coefficients are underlined (not significant) in the NB-L models with AADT-dependent dispersion — this drives the preference for length-only dispersion in NB-L models. Verify the underlined coefficients match the paper's stated criterion (95% HPD includes zero).
  - WAIC differences (~600 units between NB-L and traditional NB) are very large and should be treated as genuine rather than a computation artefact, given the CURE plot corroboration. However, WAIC computation requires the full N×S log-likelihood matrix — this is computationally intensive at scale.
- Any likely ambiguity or risk of misinterpretation:
  - The NB-L superiority finding applies to a dataset with 37% zeros over 5 years. Open Road Risk's link-year data has ~98–99% zeros annually. While this strengthens the case for NB-L, it also means Open Road Risk is in a more extreme regime than what is tested here. The NB-L advantage should be even greater, but this is an extrapolation from the paper's empirical range.
  - The paper uses "AADT over 5 years" as a label in Table 1 — this could be misread as a 5-year total. It is clearly a daily flow rate (max 2347 vpd) and should be interpreted as mean annual AADT over the study period.
  - The p-parameter in NB-P models: estimated P ≈ 2 in most cases, making NB-P similar to NB-2 in those cases. This means the NB-P vs NB-2 comparison is effectively a test of whether P = 2 is rejected by the data — it mostly isn't on this dataset. This does not generalise to other datasets where P might differ substantially from 2.
