# Paper Extraction — Methodological Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: QUASI-POISSON_VS__NEGATIVE_BINOMIAL_REGRESSION__HOW_SHOULD_WE_MOD.pdf
- Suggested Markdown filename: paper-extraction-verhoef-boveng-2007-quasipoisson-vs-NB-overdispersion.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered as document text in context)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 7-page paper accessible. Figures 1 and 2 present as images; content described in text and derivable from equations. This is not a road safety paper — it is an ecology/statistical methods paper. Its relevance to Open Road Risk is methodological, not substantive.

---

## 1. Citation

- Title: Quasi-Poisson vs. Negative Binomial Regression: How Should We Model Overdispersed Count Data?
- Authors: Jay M. Ver Hoef, Peter L. Boveng
- Year: 2007
- Journal: Ecology, Vol. 88, No. 11, pp. 2766–2772
- DOI or URL: https://digitalcommons.unl.edu/usdeptcommercepub/142
- Country / region studied: USA — Alaska (harbor seal aerial surveys); domain is ecology, not road safety
- Study setting: Not applicable to road safety — this is an ecological count data problem (harbor seal abundance estimation). The paper is relevant to Open Road Risk as a statistical methods reference only.

---

## 2. Core Objective

- One-sentence description: The paper explains the theoretical difference between quasi-Poisson and Negative Binomial regression for overdispersed count data, specifically the different variance-mean relationships (linear vs quadratic) and their implications for IWLS weighting of observations, illustrated with a harbor seal survey example where the two methods give dramatically different results.
- Main purpose: Statistical methods comparison — not a safety performance function, not a road safety study. Directly relevant as a methodological reference for Open Road Risk's Stage 2 model family choice.
- Evidence quote: "The objective of this statistical report is to introduce some concepts that will help an ecologist choose between a quasi-Poisson regression model and a negative binomial regression model for overdispersed count data." (p.2766)

---

## 3. Response Variable

- Target variable: Count of harbor seals per aerial survey site per survey pass
- Collision type: Not applicable — no road safety outcome
- Severity handling: Not applicable
- Count, binary, rate, risk score, severity class, or other: Count (non-negative integer)
- Time window: 18–27 August 1998 (southern Southeast Alaska annual survey)
- Evidence quote: "Harbor seals were counted from aircraft from 18 August to 27 August 1998." (p.2769)

**Note on relevance:** The specific application (harbor seal counts) is not transferable to Open Road Risk. The statistical methodology — specifically the derivation of IWLS weights for quasi-Poisson vs NB, the variance-mean diagnostic plot, and the decision framework — is directly transferable.

---

## 4. Exposure Handling

- Exposure variable used: Not applicable in this paper's context (no traffic exposure). Site-level random effects (b₀,ᵢ per site) serve as a partial analogue, absorbing site-level baseline count variation.
- Traffic count source: Not applicable.
- Transferability to my AADF/WebTRIS setup: Not applicable for exposure specifically. The paper's methodological content (variance-mean relationship and IWLS weighting) applies to any Poisson-family count model, including Open Road Risk's Stage 2 GLM with log-offset.

---

## 5. Spatial Unit of Analysis

- Unit: Individual haul-out site (423 sites identified; 197 small + 226 large in the analysis split)
- Relevance to OS Open Roads link-based pipeline: Partial structural analogy only — haul-out sites as individual counting units are analogous to road links as individual counting units. The key relevant lesson is about how NB and quasi-Poisson weight small-count vs large-count units differently, which applies directly to Open Road Risk's link-year data where most links have zero or very low crash counts.

---

## 6. Temporal Unit of Analysis

- Years covered: 1998 (single survey period)
- Temporal resolution: Per-survey-pass (multiple counts per site over 10 days)
- Relevance to WebTRIS-style time profiles: Not applicable.

---

## 7. Engineered Features

Not applicable as a road safety features table. The covariates in the harbor seal model are date, time of day, and relative tide height — all ecological variables with no road safety analogue. The relevant content from this paper is the mathematical derivation of IWLS weights, not any specific feature.

---

## 8. Model Architecture

This is the core relevant section for Open Road Risk.

**Quasi-Poisson:**
- E(Y) = μ; Var(Y) = θμ (linear variance-mean relationship; θ is a constant overdispersion parameter)
- IWLS weight for observation i: wᵢ = μᵢ / θ (proportional to the mean — large-count observations get linearly more weight)
- θ is a nuisance parameter; quasi-Poisson does not define a full distributional likelihood, only the first two moments. Consequence: AIC cannot be computed; only QAIC (for within-class model selection only); Bayes factors not applicable.

**Negative Binomial:**
- E(Y) = μ; Var(Y) = μ + κμ² (quadratic variance-mean relationship; κ is the dispersion parameter)
- IWLS weight for observation i: wᵢ = μᵢ / (1 + κμᵢ) (concave relationship with mean — weights level off to 1/κ for large μ; small-count observations get relatively more weight than under quasi-Poisson)
- NB has a full likelihood; AIC, BIC, Bayes factors all computable.

**The critical distinction for Open Road Risk:**

At low mean values (small-count links, which are the majority of Open Road Risk's link-years), NB gives approximately equal weight to all these links regardless of their mean. Quasi-Poisson gives them weight proportional to their mean — meaning the very many near-zero-count links get very little influence on coefficient estimates under quasi-Poisson. Conversely, for high-count links (motorway segments with multiple crashes per year), quasi-Poisson gives them disproportionately more influence than NB.

This has a direct implication for Open Road Risk: if the goal is to rank all links by risk including the low-crash-rate majority, NB's weighting scheme gives zero-sparse links more relative influence in coefficient estimation than quasi-Poisson does. Whether this is desirable depends on the scientific question.

- Evidence quote: "For quasi-Poisson, weights are directly proportional to the mean, and for negative binomial, weights have a concave relationship to the mean; that is, very small mean values get very little weight, but as the mean increases, weights level off to 1/j." (p.2769, Eqs. 4–5)

**Overdispersion parameters in the example:**
- Quasi-Poisson: θ̂ = 25.91 (constant overdispersion across all site sizes)
- NB: κ̂ = 0.7717 (overdispersion increases with mean; equal overdispersion to quasi-Poisson at μ ≈ 32)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Overdispersion parameter | θ̂ (quasi-Poisson) | 25.91 | Quasi-Poisson, all sites | Very high constant overdispersion | p.2769 |
| Overdispersion parameter | κ̂ (NB) | 0.7717 | NB, all sites | Quadratic overdispersion; at μ = 10, overdispersion factor = 1 + 0.77×10 = 8.72 | p.2769 |
| Crossover point | Equal overdispersion between QP and NB | μ ≈ 32 | Both models | Below μ=32: QP has higher variance; above μ=32: NB has higher variance | p.2769 |
| Abundance estimate | Adjusted harbor seal count | 38,884 (QP) vs 80,609 (NB) | Full dataset, 18 August | 2.07× difference in abundance estimate from model choice alone | p.2770 |
| Date effect | Multiplicative effect on 18 August | 2.45 (NB) vs 1.17 (QP) | Full dataset | NB driven by small sites' date sensitivity; QP driven by large sites | p.2770, Fig. 2 |
| Large-site NB estimate | Adjusted count | 34,239 | NB, large sites only (n=226) | Close to QP full-dataset result — confirms QP is dominated by large sites | p.2771 |
| Small-site NB estimate | Adjusted count | 84,343 | NB, small sites only (n=197) | Implausibly high; NB over-leverages small-site date sensitivity | p.2771 |

**Are these metrics in-sample, out-of-sample, or not stated?**

In-sample abundance estimates and fitted effects. No external validation. The paper is a statistical methods illustration, not a predictive model.

**Which metric is most relevant to Open Road Risk?**

None of the seal-count metrics are directly relevant. The methodological finding — that NB gives small-count observations relatively more weight than quasi-Poisson, with the crossover depending on the dispersion parameters — is the directly relevant result.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions handled: The harbor seal example actually has the **opposite** sparsity structure from Open Road Risk — most sites have non-trivial counts (the example shows means up to ~140 seals). The low-mean regime (μ < 32) represents the minority of sites.
- However, the theoretical content is directly applicable to sparse data: for observations with very low mean (μ → 0), NB weights approach 0 × 1/(1 + κ×0) = 0, while quasi-Poisson weights also approach 0 (proportional to μ). Both down-weight near-zero observations, but the paper shows NB down-weights them less severely relative to moderate-count observations.
- This is the key tension for Open Road Risk: with ~98–99% zero link-years, both NB and quasi-Poisson will assign very low weight to zero-crash links. The Khodadadi (2021) NB-L finding that NB-L better handles a 37% zero dataset suggests that for Open Road Risk's more extreme zero-heavy structure, NB-L may be even more important than the NB vs quasi-Poisson distinction.
- Evidence quote: "very small mean values get very little weight" (p.2769, NB weighting discussion)
- Practical relevance: The paper provides the theoretical machinery to understand *why* model family matters for sparse count data. It should be read alongside Khodadadi (2021) when implementing the Stage 2 model family diagnostic.

---

## 11. Validation Strategy

- Train/test split method: None
- Spatial holdout used? No
- Temporal holdout used? No
- Cross-validation type: Cross-validation is mentioned as a principled model selection approach (Vehtari and Lampinen 2003 cited) but not implemented in this paper.
- Metrics: No formal fit metrics reported; model comparison is diagnostic (variance-mean plot) and scientific reasoning (which sites should dominate abundance estimates).
- External validation: None
- What I should copy: The variance-mean diagnostic plot (Fig. 1A equivalent) — plot (Yᵢ − μ̂ᵢ)² against μ̂ᵢ, bin by mean, average within bins. This directly diagnoses whether variance scales linearly (quasi-Poisson appropriate) or quadratically (NB appropriate) with the mean. This is a one-plot diagnostic that should precede the model family choice in Stage 2.

---

## 12. Key Findings Relevant to My Project

**Finding 1 — Core theoretical result**
- Finding: Quasi-Poisson and NB differ structurally in their variance-mean relationship: quasi-Poisson assumes Var(Y) = θμ (linear); NB assumes Var(Y) = μ + κμ² (quadratic). This difference propagates into IWLS weights: quasi-Poisson weights scale linearly with μ; NB weights have a concave ceiling at 1/κ. The practical consequence is that quasi-Poisson gives high-count observations proportionally more influence on coefficient estimates, while NB gives low-to-moderate-count observations more relative influence.
- Why it matters for Open Road Risk: Open Road Risk's link-year data has a bimodal structure — the vast majority of links have zero or very low crash counts; a small minority of high-volume or complex links have multiple crashes per year. Quasi-Poisson will be more strongly influenced by the high-crash-rate minority; NB will give more relative weight to the zero-sparse majority. Given that the goal is to rank all 2.17M links (not just the high-crash ones), understanding which model's weighting better serves the ranking objective is a non-trivial decision that this paper informs.
- Evidence: Eqs. 4–5, p.2769; Fig. 1B.
- Confidence: High — this is a mathematical derivation, not an empirical finding.

**Finding 2 — Diagnostic tool**
- Finding: Plotting averaged squared residuals (Yᵢ − μ̂ᵢ)² against binned fitted means μ̂ᵢ provides an empirical diagnostic for whether the variance-mean relationship is better described as linear (quasi-Poisson) or quadratic (NB). The paper recommends this as a precursor to model family choice.
- Why it matters: This is the same diagnostic that should precede Stage 2 model family selection in Open Road Risk. It requires only the fitted means from any baseline Poisson GLM and the observed crash counts. If the binned squared residuals track a line through the origin, quasi-Poisson is appropriate; if they curve upward quadratically, NB is more appropriate.
- Evidence: Fig. 1A; Discussion p.2771.
- Confidence: High — standard statistical diagnostic, clearly derived.

**Finding 3 — AIC cannot compare quasi-Poisson and NB directly**
- Finding: AIC/BIC/Bayes factors cannot be used to choose between quasi-Poisson and NB because quasi-Poisson does not have a full distributional likelihood — only a quasi-likelihood defined by its first two moments. QAIC exists but is only valid within the quasi class. The paper notes this explicitly and points to goodness-of-fit or cross-validation approaches as alternatives.
- Why it matters: This is an important operational constraint for Open Road Risk. If quasi-Poisson is added as a Stage 2 candidate alongside NB-2, the standard AIC comparison used to select between NB parameterisations (as in Khodadadi 2021) cannot be applied directly. The variance-mean diagnostic plot, cross-validation, or CURE plots are the appropriate tools. This is a practical limitation to document.
- Evidence: Introduction p.2767: "quasi models are only characterized by their mean and variance, and do not necessarily have a distributional form... any model selection method that depends on full distributional likelihoods... would not help choose between a quasi-Poisson and negative binomial model."
- Confidence: High — established statistical fact, not an empirical finding.

**Finding 4 — No general answer; context determines the choice**
- Finding: "There is no general answer" to which is better. The choice should be informed by (a) the empirical variance-mean diagnostic, (b) the scientific question (which observations should have more influence on coefficient estimates), and (c) cross-validation if needed. In the harbor seal example, quasi-Poisson was preferred because the goal was abundance estimation dominated by large sites.
- Why it matters: For Open Road Risk, the scientific question differs from the harbor seal case. The goal is risk ranking across all links — including the many sparse links that quasi-Poisson would down-weight heavily. This suggests NB may be preferable on scientific grounds for Open Road Risk, independent of formal model selection. This reasoning should be documented when the model family choice is made.
- Evidence: Discussion p.2771–2772.
- Confidence: High for the framework; Medium for the conclusion applied to Open Road Risk (which requires assessing the specific variance-mean structure of the link-year data).

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Variance-mean diagnostic plot (averaged squared residuals vs binned fitted means) | Determines empirically whether quasi-Poisson or NB better describes the variance structure of Open Road Risk link-year crash counts; direct precursor to model family choice | Observed crash counts + fitted means from current Poisson GLM (already available) | 423 sites (ecology); applicable to any n | Fully compatible at any scale | Stage 2 / diagnostic — should precede NB implementation | Low (bin fitted means, average squared residuals within bins, plot with QP and NB variance curves) | Requires enough non-zero observations per bin to estimate variance accurately; with ~99% zeros, most bins will be at μ ≈ 0; consider stratifying by road class or filtering to links with ≥1 crash event |
| IWLS weighting framework as scientific justification for model family choice | Provides principled reasoning for NB over quasi-Poisson when the goal is to give low-crash-rate links adequate influence in coefficient estimation | Theoretical only; no new data needed | N/A | Fully compatible | Stage 2 / documentation | Low | None — documentation of reasoning |
| Cross-validation as model comparison when AIC is unavailable (QP vs NB) | Provides valid comparison between quasi-Poisson and NB without relying on likelihood | Observed crash counts, cross-validation splits | N/A | Compatible | Stage 2 / validation | Medium (implement k-fold CV for GLM; measure mean squared prediction error or equivalent) | Cross-validation at 21.7M link-year scale requires careful sampling strategy; subsample first |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Harbor seal abundance estimation methodology | Ecology-specific; site-fixed-effects model for repeated aerial surveys; no road safety analogue | No road safety application | 423 sites, Alaska | Incompatible | Not applicable | High |
| QAIC for quasi-Poisson model selection | Only valid within quasi class (covariate selection); cannot compare QP vs NB | Quasi-likelihood only defined by moments | N/A | Not useful for Open Road Risk's NB vs QP choice | Use variance-mean diagnostic + CURE plots + cross-validation instead | High |

---

## 14. Pipeline Implications

**Does this paper support using exposure-normalised collision risk?**
Not directly — no exposure offset in this paper. Methodologically neutral on this question.

**Does it suggest better handling of AADT/AADF uncertainty?**
No.

**Does it suggest useful geometry or road-context features?**
No.

**Does it suggest better modelling of junctions?**
No.

**Does it suggest better treatment of severity?**
No.

**Does it suggest better validation design?**
Yes — implicitly. The paper identifies cross-validation (Vehtari and Lampinen 2003) as a valid model comparison tool when AIC is unavailable (quasi-Poisson case). This supports the LOO/WAIC approach recommended in Khodadadi (2021), and suggests cross-validation as the appropriate standard for Open Road Risk's model family comparison.

**Does it expose a weakness in my current approach?**
Yes, one specific point: if Open Road Risk ever tests quasi-Poisson alongside NB-2, the Poisson GLM's current use of AIC for model comparison cannot be directly extended to the QP vs NB comparison. The variance-mean diagnostic plot and CURE plots are the appropriate tools. This should be documented before any model family comparison is implemented.

Additionally: the paper's weighting analysis suggests that Open Road Risk's current Poisson GLM (which is a special case of quasi-Poisson with θ = 1, i.e., no overdispersion) implicitly gives linearly increasing weight to higher-crash-rate links. To the extent that coefficient estimates are dominated by the small number of high-crash-rate links, the Poisson GLM's risk rankings for the zero-sparse majority may be less well-calibrated than NB would provide. This is a known concern worth documenting explicitly.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Before implementing NB-2 or NB-L as Stage 2 alternatives, add a variance-mean diagnostic plot to the Stage 2 pipeline: bin the fitted Poisson means (μ̂ᵢ) into ~10 categories, compute average (Yᵢ − μ̂ᵢ)² per bin, and overlay the fitted quasi-Poisson (linear: θ × bin_mean) and NB (quadratic: bin_mean + κ × bin_mean²) variance curves. This directly answers whether Var ∝ μ or Var ∝ μ² better describes the data.
- Action type: Diagnostic
- Relevant stage: Stage 2 / pre-model-family-choice diagnostic
- Why the paper supports it: Fig. 1A methodology; Discussion p.2771.
- Effort: Low (15–20 lines of Python/R using existing GLM output)
- Risk if implemented badly: With ~99% zero link-years, most binned means will be near zero. The diagnostic is more informative if computed on non-zero link-years or filtered to links with ≥1 crash. Document this filtering choice.

**Action 2**
- Suggested repo action: Add a documentation note to Stage 2 explaining the quasi-Poisson vs NB weighting difference: quasi-Poisson weights scale linearly with mean crash rate (high-crash links dominate coefficient estimation); NB weights level off at 1/κ (low-crash links get more relative influence). Document that for Open Road Risk's goal of ranking all links — including the zero-sparse majority — NB's weighting is more appropriate on scientific grounds, following the Ver Hoef and Boveng (2007) framework.
- Action type: Documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Eqs. 4–5; Discussion pp.2771–2772.
- Effort: Low
- Risk if implemented badly: None — documentation only

**Action 3**
- Suggested repo action: Document that AIC cannot be used to compare quasi-Poisson against NB-2 or NB-L, because quasi-Poisson lacks a full distributional likelihood. If quasi-Poisson is tested as a Stage 2 alternative, use the variance-mean diagnostic, CURE plots, and cross-validation (not AIC) for the comparison.
- Action type: Documentation note
- Relevant stage: Stage 2 / validation / documentation
- Why the paper supports it: Introduction p.2767 (QAIC validity discussion).
- Effort: Low
- Risk if implemented badly: None — documentation only

---

## 16. Query Tags

- quasi-Poisson
- negative-binomial
- overdispersion
- variance-mean-relationship
- IWLS-weights
- count-data
- model-family-choice
- variance-diagnostic
- ecology-methods
- not-road-safety
- methodological-reference
- no-exposure-offset
- no-AIC-for-QP-vs-NB
- cross-validation-recommended
- low-count-weighting
- quadratic-variance
- linear-variance
- statistical-methods
- generalised-linear-models

---

## 17. Confidence and Gaps

- Overall confidence in extraction: High (the paper is methodologically transparent and clearly written; findings are mathematically derived, not empirical)
- Important details not stated or gaps:
  - The paper does not address zero-inflated or NB-Lindley extensions, which are covered better by Khodadadi (2021) for the specific case of zero-heavy road safety data.
  - The harbor seal example has very high overdispersion (θ̂ = 25.91 for quasi-Poisson; κ̂ = 0.7717 for NB) — likely much higher than Open Road Risk's link-year data per se. The crossover point (μ ≈ 32) is specific to these parameters; for Open Road Risk's data, the crossover point will differ depending on the estimated κ.
  - The paper does not address offset terms (exposure) at all. The IWLS weighting analysis still applies when a log-offset is included — the offset enters through μᵢ (the fitted mean incorporates the offset) — but this is not discussed explicitly.
- Parts needing manual checking:
  - Eqs. 4 and 5: The quasi-Poisson weight derivation gives wᵢ = μᵢ/θ (proportional to mean). The NB weight derivation gives wᵢ = μᵢ/(1 + κμᵢ). Both are correct from standard IWLS theory and can be verified by substituting the variance functions into the general IWLS weight formula.
  - The abundance estimates (38,884 vs 80,609) are cited in the text; they are outcomes of the ecological analysis and do not need verification for Open Road Risk purposes.
- Any likely ambiguity or risk of misinterpretation:
  - This paper should not be cited as evidence that quasi-Poisson is better than NB in general — the paper explicitly states "there is no general answer" and concludes quasi-Poisson was better in their specific harbour seal context for a specific reason (large sites should dominate abundance estimation). For Open Road Risk's risk-ranking goal across all links, the scientific reasoning points in the opposite direction.
  - The paper's context (ecology, harbor seals, NOAA) may initially seem irrelevant to road safety. It is included because it provides the clearest available derivation of the quasi-Poisson vs NB weighting distinction, which is a general statistical point applicable to any count regression context including road safety SPFs.
