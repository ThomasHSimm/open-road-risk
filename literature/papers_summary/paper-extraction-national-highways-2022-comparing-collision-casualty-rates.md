# Paper Extraction: Statistical Methods for Comparing Road Collision and Casualty Rates

## 0. Extraction Run Metadata

- Extraction date: 2026-05-12
- Source PDF filename: statistical-methods-for-comparing-road-collision-and-casualty-rates-proposed-approach.pdf
- Suggested Markdown filename: paper-extraction-national-highways-2022-comparing-collision-casualty-rates.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 27-page document accessible including appendices. No DOI stated in document.

---

## 1. Citation

- Title: Statistical methods for comparing road traffic collision and casualty rates: proposed approach
- Authors: Not stated (published by National Highways; Chief Analyst Mark Clements named in Foreword)
- Year: 2022 (feedback deadline August 2022 stated; publication code PR81/22)
- DOI or URL, if present: Not stated. Available at www.nationalhighways.co.uk. Publications code PR81/22.
- Country / region studied: England (National Highways network; motorway focus mentioned in conclusions)
- Study setting: mixed (motorways explicitly mentioned; methods framed for any road type)

---

## 2. Core Objective

- One-sentence description: The paper proposes statistical methods for calculating confidence intervals and hypothesis tests to compare road traffic collision rates and casualty rates between two roads (or road types, or a single road across time periods), using STATS19-derived data.
- Main purpose: descriptive analysis / safety performance comparison / hypothesis testing methodology development
- Evidence quote or page reference: "In this report we describe statistical methods that we propose can be used to compare road traffic collision rates and casualty rates." (Foreword, p.4). Developed in response to ORR recommendation to add significance testing to motorway casualty rate comparisons (Introduction, p.5).

---

## 3. Response Variable

- Target variable: (1) collision count per unit vehicle miles; (2) casualty count per unit vehicle miles
- Collision type: injury collisions only (STATS19 definition: personal injury, known to police within 30 days, on public highway, involves at least one vehicle)
- Severity handling: not modelled separately in the main methods; Section 6.7 notes that severity-adjusted STATS19 data would require method modification that is not developed here
- Count, binary, rate, risk score, severity class, or other: rate (collisions or casualties per vehicle mile); collision count modelled as Poisson
- Time window used for outcomes: not stated for any empirical application; guidance recommends same time period for both roads being compared (Section 6.3)
- Evidence quote or page reference: "a collision is defined as one which occurs on the public highway, involves at least one vehicle, becomes known to the police within 30 days, and causes personal injury" (Introduction, p.5)

---

## 4. Exposure Handling

- Exposure variable used, if any: vehicle miles (v_i), described as "road traffic observed" over the data collection period
- Traffic count source: not stated explicitly for empirical use; paper references DfT and National Highways existing practice; worked example uses fictitious data (v_1 = 25, v_2 = 58 — units not specified in example but implied to be hundred million vehicle miles by the rate scale)
- Whether exposure is modelled, observed, assumed, or ignored: assumed observed (the paper explicitly assumes vehicle miles are known; no treatment of estimated or imputed traffic)
- Treatment of missing or sparse traffic counts: not addressed. Paper notes traffic estimates "may be inaccurate" as a sensitivity analysis concern (Section 6.4) but provides no method to propagate traffic uncertainty
- Whether offset terms, rates, denominators, or normalisation are used: exposure enters as a denominator in the rate definition R_i = N_i / v_i and directly in the Poisson likelihood as the scale parameter: N_i ~ Poisson(gamma_i * v_i). This is mathematically equivalent to a Poisson offset log(v_i) in a GLM. (Section 3.1, p.7)
- Evidence quote or page reference: "N_i ~ Poisson(gamma_i * v_i)" (Section 3.1, p.7); "it is possible that road traffic estimates are inaccurate" (Section 6.4, p.17)
- Transferability to my AADF/WebTRIS setup: mixed
- Notes:
  - Mathematical exposure structure (Poisson with exposure scale / offset): **high transferability** — directly compatible with Open Road Risk Stage 2 Poisson GLM with log(AADT × length × 365 / 1e6) offset.
  - Paper's assumed data source (directly observed vehicle miles, no uncertainty): **low transferability** — Open Road Risk uses estimated AADT from Stage 1a, not directly counted vehicle miles for all links. The paper provides no method to handle exposure uncertainty, which is a central concern in Open Road Risk.

---

## 5. Spatial Unit of Analysis

- Unit: road (not further defined — "Road 1" and "Road 2" are abstract; could be road sections, road types, or individual roads)
- Segment length or segmentation rule: not stated
- How crashes are assigned to the network: not stated
- Treatment of junctions/intersections: not stated
- Spatial aggregation risks: not discussed
- Evidence quote or page reference: "In the remainder of this document, we describe our proposed methods to compare collision and casualty rates of two roads, which we call Road 1 and Road 2. Note that these could equally be two road types or a single road in two consecutive years." (Introduction, p.5)
- Relevance to OS Open Roads link-based pipeline: low for direct application. The paper operates at an aggregate road-level comparison (e.g. road type A vs road type B, or a whole road before/after). It is not designed for segment-level or link-year panel analysis at 2.1 million links. The statistical building blocks (Poisson likelihood, parametric bootstrap CI, likelihood ratio test) are individually relevant.

---

## 6. Temporal Unit of Analysis

- Years covered: not stated (no empirical data; worked example uses fictitious data)
- Temporal resolution: aggregate over collection period (not annual, monthly, or daily modelling)
- Whether seasonality or time-of-day is modelled: not modelled; guidance warns that comparing roads over different time periods can be misleading due to periodic collision intensity (Section 6.3, Figures 5–6)
- Whether before-after or panel structure is used: not used; methods support comparing "a single road in two consecutive years" as a special case but no panel structure
- Evidence quote or page reference: "we suggest that the methods proposed in this document are only used when the data used to compare two roads is collected over the same period of time" (Section 6.3, p.17)
- Relevance to WebTRIS-style time profiles: indirect. The paper's concern about time-varying collision intensity (non-homogeneous Poisson process) is conceptually consistent with WebTRIS-style within-day and seasonal traffic profiles. The paper does not operationalise time-zone profiles.

---

## 7. Engineered Features

The paper does not use engineered features. It is a statistical testing methodology paper, not a predictive modelling paper. No feature table is applicable.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Vehicle miles (v_i) | Assumed observed traffic data | Direct sum over collection period | Exposure denominator in Poisson likelihood | Concept transferable; specific data source not transferable — Open Road Risk uses estimated AADT |

---

## 8. Model Architecture

- Algorithms/models used: non-homogeneous Poisson process for collision counts; compound Poisson process for casualty counts; parametric bootstrap for CIs; Monte-Carlo likelihood ratio test for collision rate comparison; non-parametric permutation bootstrap for casualty-per-collision first-moment comparison; Fisher's method for combining p-values
- Baseline model: Z-test / chi-squared test with 1 df (existing DfT and National Highways practice) — proposed methods are improvements on this
- Final/preferred model: likelihood ratio test with Monte-Carlo p-value for collision rates; compound Poisson + non-parametric bootstrap for casualty rates
- Loss function or likelihood, if stated: Poisson likelihood (Equation 3, p.7); likelihood ratio test statistic (Equation 12, Appendix A.2)
- Offset/exposure term, if used: vehicle miles v_i as Poisson scale parameter (mathematically equivalent to offset); see Section 3.1
- Spatial autocorrelation handling: not addressed
- Temporal dependence handling: not addressed; independence of collisions assumed (Section 3.1: "the occurrence of one collision has no influence on the occurrence of another collision")
- Interpretability method: not stated; methods produce CIs and p-values, not feature coefficients
- Evidence quote or page reference: "We assume that road traffic collisions occur according to a non-homogeneous Poisson process" (Section 3.1, p.7); "we propose calculating a p-value using a Monte-Carlo approach" (Section 3.3, p.9)

---

## 9. Reported Metrics / Quantitative Results

Only a fictitious worked example is provided. No empirical validation metrics are reported.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Worked example — collision rate comparison | p-value (Monte-Carlo LR test) | 0.001 | Road 1 (N=117, v=25) vs Road 2 (N=382, v=58) | Reject H0; evidence that underlying collision rates differ | Section 5.1, p.13 |
| Worked example — casualty per collision first moment | p-value (non-parametric bootstrap) | 0.112 | Road 1 (mean x=1.744) vs Road 2 (mean x=1.901) | Fail to reject H0; no evidence of difference in mean casualties per collision | Section 5.2, p.14 |
| Worked example — combined Fisher p-value | Fisher combined p-value | 0.001 | Combined across both tests | Evidence of difference in at least one component | Section 5.2, p.14 |
| Worked example — collision rates | Observed rates | R1=4.680, R2=6.586 | Fictitious data | Road 2 higher | Table 1, p.12 |
| Worked example — casualty rates | Observed rates | Q1=8.160, Q2=12.517 | Fictitious data | Road 2 higher | Table 1, p.12 |

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? **Not applicable** — all results are from a fictitious worked example, not empirical data. No validation is reported.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? The p-values test statistical hypotheses about whether two rates differ. They do not test predictive generalisation.
- Are any metrics likely to be optimistic for real-world deployment? Not applicable; fictitious data only.
- Which metric, if any, is most relevant to Open Road Risk? The Monte-Carlo likelihood ratio test p-value for comparing Poisson rates is methodologically relevant as a formal test for whether two link-level collision rates differ significantly, accounting for small-N uncertainty.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: explicitly addressed for the case of zero collisions on one road. The paper notes that zero collisions prevent CI calculation (Poisson with rate zero has point mass at zero). Hypothesis testing remains possible even when one road has zero collisions (Section 6.1).
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson for collision counts. For casualties per collision, the paper explored Poisson, negative binomial, and geometric distributions and found all fits poor; also explored zero-truncated and one-inflated variants — "marginal improvements" only. Settled on non-parametric compound Poisson (no parametric distribution assumed for casualties per collision). The paper does **not** use a zero-inflated model.
- Whether high-risk locations are evaluated separately: not applicable (paper is a two-road comparison method, not a ranking or hotspot detection method)
- Evidence quote or page reference: "In the development of these methods we have explored fitting a Poisson, a negative-binomial and a geometric distribution to the number of casualties per collision but found the fit of all distributions to be poor." (Section 4.1, p.9); guidance on zero-collision case at Section 6.1, p.15
- Practical relevance to my sparse collision link-year dataset: medium. The paper's acknowledgement that parametric distributions fit poorly to casualties-per-collision data is consistent with the heterogeneity expected across diverse OS Open Roads links. The zero-collision handling (Section 6.1) is relevant since the majority of Open Road Risk link-years have zero collisions, though the paper's method is designed for aggregate road comparisons, not 21.7 million link-year rows.

---

## 11. Validation Strategy

- Train/test split method: not applicable — no predictive model is fitted; methods paper only
- Spatial holdout used? not applicable
- Temporal holdout used? not applicable
- Grouped holdout used? not applicable
- Cross-validation type: not applicable
- Metrics: p-values and confidence intervals from fictitious worked example only
- External validation: none
- Leakage or generalisation risks: not applicable
- Evidence quote or page reference: "Note that these statistics are based on fictitious data simply for this worked example." (Section 5, p.12)
- What I should copy or avoid: The paper provides no empirical validation of its proposed methods against real data (it explicitly states methods are not yet finalised and will be trialled). Do not treat the worked example results as evidence of method performance.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: The Poisson likelihood with exposure as a scale parameter (N_i ~ Poisson(gamma_i * v_i)) supports a Monte-Carlo likelihood ratio test for comparing collision rates that does not rely on asymptotic distributions, making it valid at low traffic volumes where Z-test p-values may be misleading.
- Why it matters: Open Road Risk has many low-AADT links and rare collision link-years. The asymptotic Z-test (equivalent to what DfT uses) may produce unreliable p-values at small exposure or small collision counts.
- Evidence quote or page reference: "When levels of road traffic are low, the distribution of the test statistic may be far from the asymptotic distribution of the test statistic, meaning that the p-values produced by these methods may be misleading." (Section 3.3, p.8)
- Confidence: medium — the claim is theoretically sound and supported by reference to Krishnamoorthy & Thomson (2004), but no empirical comparison against the Z-test is shown in this paper.

**Finding 2:**
- Finding: Parametric distributions (Poisson, negative binomial, geometric) and their zero-truncated / one-inflated variants all fit poorly to observed casualties-per-collision data; a non-parametric compound Poisson approach is preferred.
- Why it matters: This suggests that in Open Road Risk, severity-weighted outcomes (e.g. weighting by casualties per collision) would face similar distributional challenges. A non-parametric or semi-parametric treatment of casualties per collision may be more defensible than assuming a standard count distribution.
- Evidence quote or page reference: "found the fit of all distributions to be poor... made only marginal improvements" (Section 4.1, p.9)
- Confidence: low-medium — the finding is from National Highways' internal development work; the specific road data used is not described, so generalisability is uncertain.

**Finding 3:**
- Finding: The paper recommends sensitivity analysis of traffic estimates, noting that road traffic data may be inaccurate and that biases in traffic estimates will affect collision and casualty rate comparisons.
- Why it matters: Open Road Risk uses estimated AADT (Stage 1a, CV R² 0.83), not directly counted vehicle miles for all links. This is a documented limitation the paper identifies as requiring explicit sensitivity treatment.
- Evidence quote or page reference: "it is possible that road traffic estimates are inaccurate, as the road network is a complex system which spans a large geographical area" (Section 6.4, p.17)
- Confidence: high — the concern is directly applicable; the paper does not provide a method to address it.

**Finding 4:**
- Finding: Time period alignment is critical. Comparing roads over different calendar periods, or periods with different seasonal positions, can produce misleading apparent rate differences even when underlying rates are identical.
- Why it matters: Open Road Risk uses a link × year panel. Year-to-year comparisons or cross-link comparisons should account for temporal confounding. The paper illustrates this with periodic intensity function examples.
- Evidence quote or page reference: "we suggest that the methods proposed in this document are only used when the data used to compare two roads is collected over the same period of time" (Section 6.3, p.17)
- Confidence: high — the concern is standard and well-motivated.

**Finding 5:**
- Finding: Statistical significance of a rate difference does not imply practical significance. Small differences can be statistically detectable with large enough exposure, and p-value magnitude is sensitive to data collection period length.
- Why it matters: At Open Road Risk's scale (2.1M links, 10 years), high statistical power means many small rate differences will appear significant. The paper's explicit warning against treating statistical significance as practical importance is relevant to how risk percentiles and flagging thresholds are communicated.
- Evidence quote or page reference: "Small differences can be statistically different, but this does not mean that they are practically different or important" (Section 6.6, p.18)
- Confidence: high — this is a standard and correct statistical point.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Poisson likelihood with exposure scale (N ~ Poisson(gamma * v)) | Directly compatible with Stage 2 Poisson GLM offset structure; supports formal rate comparison | Collision counts + exposure (AADT × length) | Two-road aggregate comparison | Compatible at link-year level as mathematical structure; not designed for 2.1M simultaneous comparisons | Stage 2 / documentation | Low — already implicit in current model | None if used as documentation of existing structure |
| Monte-Carlo likelihood ratio test for comparing two Poisson rates | More valid than Z-test at low traffic / low collision counts; provides formal p-value for link-level rate comparison | Collision counts + exposure for two units being compared | Pairwise comparison | Applicable to pairwise diagnostics (e.g. compare a flagged link to its road-class average); not scalable to all 2.1M pairwise comparisons simultaneously | Validation / diagnostic | Low for pairwise; high for at-scale | Computationally prohibitive if applied naively across all links |
| Parametric bootstrap CI for collision rate | Uncertainty quantification for estimated collision rate at link level | Collision count + exposure | Single road | Applicable per-link; S=1e6 simulations per link is computationally unrealistic at scale; vectorised approximation feasible | Stage 2 / validation | Medium | Computational cost at 2.1M links |
| Non-parametric bootstrap for casualty-per-collision first moment | Avoids poor-fitting parametric distributions for casualty severity | Per-collision casualty counts | Single road | Applicable to aggregate severity diagnostics; not designed for link-year granularity | Future feature / diagnostic | Medium | Only meaningful where collision counts per link are non-trivial |
| Fisher's method for combining p-values (collision rate + mean casualties per collision) | Formal combined test for casualty rate differences | Two p-values from prior tests | Pairwise | Applicable in diagnostic / validation context | Validation / documentation | Low | Requires valid component p-values |
| Sensitivity analysis of traffic estimates on rate comparisons | Directly addresses AADT uncertainty in Stage 1a | Estimated AADT + plausible uncertainty range | Not scale-specific | Applicable at link-year level | Stage 1a / Stage 2 validation | Low-medium | Requires defining credible AADT uncertainty bounds |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Direct application of full method pipeline (CI + LRT + bootstrap) at 2.1M link-year scale | S=1e6 Monte-Carlo iterations per comparison × 2.1M links is computationally unrealistic | Compute budget | Two roads | Very low | Vectorised Poisson exact CI (e.g. Garwood) as approximation; asymptotic LRT for large-N links | High |
| Non-parametric distribution for casualties per collision at link level | Most OS Open Roads links have zero or one collision in any year; per-link casualties-per-collision distribution is uninformative | Sufficient per-link collision counts (paper's own Section 6.1 caution applies) | Single road with meaningful N | Very low for individual links | Aggregate by road class or facility family | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Yes, directly. The core model N_i ~ Poisson(gamma_i * v_i) is the same mathematical structure as Open Road Risk's Stage 2 Poisson GLM with log-exposure offset. The paper provides UK-official-source validation that this is the accepted approach for STATS19 data.

- **Does it suggest better handling of AADT/AADF uncertainty?** It identifies the problem (Section 6.4) but provides no solution. It recommends sensitivity analysis varying traffic estimates by a percentage, which is a useful diagnostic idea but not a formal uncertainty propagation method.

- **Does it suggest useful geometry or road-context features?** No. The paper contains no feature engineering.

- **Does it suggest better modelling of junctions?** No.

- **Does it suggest better treatment of severity?** Partially. It highlights that parametric distributions fit poorly to casualties-per-collision data and that formal severity-rate comparison requires a compound Poisson framework. It explicitly notes that severity-adjusted STATS19 data requires further methodological development not covered here.

- **Does it suggest better validation design?** Not directly. The paper is a testing methodology, not a predictive validation framework.

- **Does it expose a weakness in my current approach?** Yes, two:
  1. If Open Road Risk uses asymptotic Z-test-style inference for flagging high-risk links (e.g. comparing observed vs expected counts), this will be less reliable for low-AADT or low-collision links. The Monte-Carlo LRT is more valid in those cases.
  2. The paper formalises that traffic estimate uncertainty is unaddressed in standard Poisson rate comparisons — directly relevant to Open Road Risk's reliance on Stage 1a AADT estimates.

---

## 15. Repo Actionability

**1.**
- Suggested repo action: Add a documentation note confirming that the Stage 2 Poisson GLM exposure offset structure (log(AADT × length_km × 365 / 1e6)) is consistent with the National Highways / DfT statistical framework for STATS19 collision rate modelling.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper's N_i ~ Poisson(gamma_i * v_i) is mathematically identical to the GLM offset formulation. The paper cites DfT and National Highways as already using Poisson for this purpose (Section 3, p.6).
- Evidence quote or page reference: "The Poisson distribution is already used by both the Department for Transport (DfT) and National Highways to model road traffic collisions." (Section 3, p.6)
- Effort: low
- Risk if implemented badly: none — documentation only

**2.**
- Suggested repo action: Add a diagnostic note or EDA section documenting that for low-AADT links or link-years with zero or very few collisions, asymptotic p-values (Z-test equivalent) are less reliable, and flag this as a known limitation of the current Stage 2 GLM inference.
- Action type: documentation note / diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Section 3.3 explicitly identifies asymptotic test failure at low traffic levels and provides alternative (Monte-Carlo LRT).
- Evidence quote or page reference: "When levels of road traffic are low, the distribution of the test statistic may be far from the asymptotic distribution" (Section 3.3, p.8)
- Effort: low
- Risk if implemented badly: none — diagnostic only

**3.**
- Suggested repo action: Add a sensitivity analysis diagnostic varying AADT estimates by ±10% and ±25% to assess how Stage 2 risk percentiles change, as a proxy for Stage 1a estimation uncertainty.
- Action type: diagnostic / small pilot
- Relevant stage: Stage 1a / Stage 2 validation
- Why the paper supports it: Section 6.4 recommends varying traffic estimates to test how rate comparisons change; Open Road Risk's AADT is estimated, making this more important than for directly counted vehicle miles.
- Evidence quote or page reference: "a sensitivity analysis would determine the percentage change in road traffic that leads to the opposite conclusions" (Section 6.4, p.17)
- Effort: medium
- Risk if implemented badly: misinterpretation of AADT uncertainty range; should be documented as illustrative not as formal uncertainty propagation

**4.**
- Suggested repo action: Note in the Stage 2 model documentation that the non-parametric treatment of casualties per collision (compound Poisson without assumed parametric distribution for X_ij) is more robust than assuming Poisson or negative binomial for severity-weighted outcomes, consistent with National Highways' own finding that standard distributions fit poorly.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Section 4.1 documents failed parametric fits to casualties-per-collision data from National Highways' own internal analysis.
- Evidence quote or page reference: "found the fit of all distributions to be poor" (Section 4.1, p.9)
- Effort: low
- Risk if implemented badly: none — documentation only

**5.**
- Suggested repo action: Add an EDA section examining the distribution of casualties per collision across the STATS19 records in Open Road Risk's study area, to assess whether the National Highways finding (poor parametric fit) holds in the Yorkshire/NW/Midlands dataset.
- Action type: diagnostic / small pilot
- Relevant stage: feature engineering / Stage 2
- Why the paper supports it: The paper identifies this as an empirical question requiring data-specific investigation; Open Road Risk has the underlying STATS19 casualty-level records needed.
- Evidence quote or page reference: Section 4.1, p.9
- Effort: low-medium
- Risk if implemented badly: low — EDA only; findings would inform whether severity weighting is feasible

---

## 16. Query Tags

- Poisson-collision-rate
- exposure-offset
- non-homogeneous-Poisson
- vehicle-miles-exposure
- compound-Poisson
- casualty-rate
- likelihood-ratio-test
- Monte-Carlo-p-value
- parametric-bootstrap-CI
- non-parametric-bootstrap
- Fisher-combined-p-value
- STATS19
- UK-official-methodology
- low-count-robust
- severity-casualties-per-collision
- traffic-estimate-uncertainty
- sensitivity-analysis
- pairwise-rate-comparison
- National-Highways
- no-spatial-model

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper:
  - No empirical data is used; all quantitative results are from a fictitious worked example.
  - The paper is explicitly described as not yet finalised (feedback requested by August 2022); it is unclear whether a final version was subsequently published.
  - The specific road data used during method development (referenced in Sections 3.1, 6.3) is not described.
  - No author names beyond Mark Clements (Chief Analyst, Foreword) are given.
  - No DOI or formal publication reference.
  - S = 1e6 Monte-Carlo iterations recommended (Appendix A.2) with no computational timing reported.
- Parts of the paper that need manual checking:
  - Appendix C (comparing more than two roads using M-way likelihood ratio) — the test statistic d in Equation 17 uses subscript i both as summation index and road index in potentially ambiguous notation; manual review of the formula is recommended before implementation.
  - Whether a finalised version of this document was published after August 2022 feedback; the extraction is based on the "proposed approach" draft.
- Any likely ambiguity or risk of misinterpretation:
  - The paper's method is designed for aggregate road-level comparison (one rate per road over a collection period), not for link-year panel analysis. Applying the Monte-Carlo LRT link-by-link at Open Road Risk scale would require significant adaptation and would be computationally intensive.
  - The compound Poisson casualty framework requires sufficient collision counts per unit to estimate the casualties-per-collision distribution non-parametrically. At Open Road Risk's link-year granularity, most units have zero or one collision, making the casualty-rate method inapplicable directly.
