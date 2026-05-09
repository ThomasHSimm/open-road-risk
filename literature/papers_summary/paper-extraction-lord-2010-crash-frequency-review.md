# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Lord-Mannering_Review.pdf
- Suggested Markdown filename: paper-extraction-lord-2010-crash-frequency-review.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The PDF text was accessible through parsed upload text. Some table formatting was degraded by PDF extraction, so the extraction relies mainly on the paper text and visible table content rather than trying to reconstruct every row of the large review tables.

## 1. Citation

- Title: The Statistical Analysis of Crash-Frequency Data: A Review and Assessment of Methodological Alternatives
- Authors: Dominique Lord; Fred Mannering
- Year: 2010
- DOI or URL, if present: 10.1016/j.tra.2010.02.001
- Country / region studied: Not a single empirical region; review paper drawing on highway-safety literature, heavily including US and international studies.
- Study setting: mixed / not stated

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper reviews methodological issues and statistical model families used to analyse crash-frequency data, where the target is the number of crashes in a roadway unit over a defined time period.
- Main purpose: methodological review / crash-frequency modelling / safety performance function / other
- Evidence quote or page reference: Page 2 states that the paper provides “a detailed review of the key issues associated with crash-frequency data” and the “strengths and weaknesses of the various methodological approaches.” Page 3 states that researchers commonly study “the number of crashes occurring in some geographical space ... over some specified time period.”

## 3. Response Variable

- Target variable: Crash frequency: number of crashes occurring in a geographical unit such as a roadway segment or intersection over a specified time period.
- Collision type: all crashes / severity-specific crashes / collision-type-specific crashes, depending on the reviewed study; not a single empirical target.
- Severity handling: The review notes that the most common approach is to model all crashes together and handle injury severity separately after total crashes are determined, but also discusses severity-specific and crash-type-specific count models.
- Count, binary, rate, risk score, severity class, or other: Count.
- Time window used for outcomes: Review examples include week, month, year, or multiple years; no single time window.
- Evidence quote or page reference: Page 3 describes crash-frequency data as crashes in a geographical space over a specified time period “(week, month, year, number of years).” Pages 7–8 discuss severity and crash-type correlation when modelling separate severity or collision-type counts.

## 4. Exposure Handling

- Exposure variable used, if any: Traffic flow and segment length are discussed as common exposure-related variables; vehicle-miles travelled is identified as the product of traffic flow and segment length.
- Traffic count source: Not stated; review-level discussion rather than one empirical data source.
- Whether exposure is modelled, observed, assumed, or ignored: Mixed across reviewed studies. The paper discusses traffic flow and segment length as explanatory/exposure variables and warns that their functional form can be contentious.
- Treatment of missing or sparse traffic counts: Not stated directly for traffic counts. The review discusses low sample mean, small sample size, omitted variables, and aggregation problems, but not a specific traffic-count imputation method.
- Whether offset terms, rates, denominators, or normalisation are used: The paper discusses exposure conceptually but does not prescribe a single offset/denominator structure. It notes that most count models use explanatory variables in a linear/log-linear form, and that exposure relationships may be non-linear.
- Evidence quote or page reference: Page 10 notes that “traffic flow” has been used as a measure of exposure. Page 11 states that multiplying traffic flow and segment length gives “a traditional exposure measure (vehicle-miles traveled)” and warns that conflicting exposure findings may reflect unobserved heterogeneity or specification problems.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The general warning is highly transferable: exposure form should be tested, not assumed. The paper does not provide an AADF/WebTRIS imputation method. It supports documenting and stress-testing your current offset structure, but it does not directly validate your estimated-AADT offset.

Important:

- Mathematical exposure structure transferability: medium/high at the conceptual level because count models commonly place traffic flow and segment length into crash-frequency models.
- Specific data-source transferability: low/not applicable because the paper is a review and does not provide a concrete traffic-count source or imputation design for Open Road Risk.

## 5. Spatial Unit of Analysis

- Unit: road segment / intersection / other, depending on reviewed studies.
- Segment length or segmentation rule: Not stated as a single rule. The review frames crash-frequency units as roadway entities, usually roadway segments or intersections.
- How crashes are assigned to the network: Not stated.
- Treatment of junctions/intersections: Intersections are one common roadway entity in the reviewed literature; no single assignment method is specified.
- Spatial aggregation risks: The paper discusses spatial correlation: nearby roadway entities may share unobserved effects, causing correlated disturbances and affecting parameter estimation.
- Evidence quote or page reference: Page 3 refers to “some geographical space (usually a roadway segment or intersection).” Page 6 notes spatial correlation where nearby roadway entities may share unobserved effects.
- Relevance to OS Open Roads link-based pipeline: High as a methodological warning. OS Open Roads link-years are repeated spatial units and are likely to share unobserved effects with neighbouring links. This supports grouped/spatial validation and residual diagnostics, but not a specific segmentation change.

## 6. Temporal Unit of Analysis

- Years covered: Not applicable; review paper. It discusses crash data over week, month, year, and multiple-year periods.
- Temporal resolution: mixed: week / month / year / number of years in the reviewed literature.
- Whether seasonality or time-of-day is modelled: The review discusses time-varying explanatory variables and the loss of within-period information, using precipitation as an example. It does not present a time-of-day model.
- Whether before-after or panel structure is used: Panel/repeated-measure structures are discussed through generalized estimating equations, random effects, negative multinomial models, and temporal correlation.
- Evidence quote or page reference: Pages 5–6 warn that explanatory variables may vary within the analysis period and that aggregation loses information. Page 6 discusses repeated observations from the same roadway entity over time and resulting temporal correlation.
- Relevance to WebTRIS-style time profiles: Medium. The paper supports the concern that annual/monthly aggregation loses within-period exposure/context variation. It does not provide a WebTRIS-like temporal exposure method.

## 7. Engineered Features

List the most important engineered features, especially those I could recreate.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Traffic flow / exposure | Traffic counts in reviewed studies | Used as explanatory variable or exposure proxy | Core determinant of crash frequency; functional form can alter inference | already present / compare implementation |
| Segment length | Road network geometry | Used as exposure-related covariate, sometimes combined with flow as vehicle-miles travelled | Longer segments have greater opportunity for crashes; relationship may be non-linear | already present / compare implementation |
| Vehicle-miles travelled | Traffic flow + segment length | Product of traffic flow and segment length | Traditional exposure measure | partially present through AADT × link length offset / compare implementation |
| Time-varying weather/context | Weather or operational data | Aggregated over the crash-frequency time window in many studies | Aggregation can lose explanatory information | candidate diagnostic / future feature, especially for temporal exposure |
| Spatial grouping / region effects | Roadway entity location or grouping | Random effects, fixed effects, spatial models, hierarchical models | Captures shared unobserved effects across nearby units | validation / candidate model extension |
| Severity-specific crash counts | Crash records | Separate or multivariate count models by severity | Severity counts are correlated; independent models can lose efficiency | candidate model extension, not production |
| Collision-type-specific crash counts | Crash records | Separate or multivariate count models by type | Collision-type counts are correlated | candidate diagnostic / future feature |
| Under-reporting adjustment | Crash reporting data, hospital/police comparison in some literature | Explicit under-reporting models | Less severe crashes may be missing, biasing estimates | documentation note; limited for STATS19 injury-only scope |

Only include features actually used in the paper.

If a feature is already part of Open Road Risk, mark it as "already present / compare implementation" rather than suggesting it as new.

## 8. Model Architecture

- Algorithms/models used: Review of Poisson regression, negative binomial / Poisson-gamma, Poisson-lognormal, zero-inflated Poisson and negative binomial, Conway-Maxwell-Poisson, gamma models, generalized estimating equations, generalized additive models, random-effects models, negative multinomial models, random-parameter models, bivariate/multivariate models, finite mixture / Markov switching models, duration models, hierarchical/multilevel models, neural networks, Bayesian neural networks, and support vector machines.
- Baseline model: Poisson regression is described as the count-data starting point.
- Final/preferred model: No single preferred final model. The review stresses that model choice depends on data characteristics and trade-offs between statistical sophistication, prediction, interpretability, and practical forecasting.
- Loss function or likelihood, if stated: Poisson probability model and negative binomial / Poisson-gamma likelihood structure are described; many reviewed methods use maximum likelihood or Bayesian estimation.
- Offset/exposure term, if used: Not stated as a single offset; traffic flow and segment length are discussed as exposure-related variables.
- Spatial autocorrelation handling: Discussed through random effects, fixed effects, spatial models, hierarchical models, and correlation over nearby roadway entities.
- Temporal dependence handling: Discussed through generalized estimating equations, panel/repeated measurements, random effects, negative multinomial models, and duration models.
- Interpretability method: Traditional count models provide interpretable parameters. Neural networks, Bayesian neural networks, and support vector machines are criticised as black-boxes that do not provide interpretable parameters.
- Evidence quote or page reference: Pages 12–14 describe Poisson and negative binomial models. Page 17 describes generalized estimating equations for repeated measurements. Pages 18–21 discuss random effects, negative multinomial, and random-parameter models. Pages 25–26 discuss neural networks and support vector machines and note black-box limitations. Page 27 discusses maximum likelihood and Bayesian estimation.

## 9. Reported Metrics / Quantitative Results

Extract the main quantitative results reported in the paper.

Include:

- model comparison metrics,
- predictive metrics,
- calibration metrics,
- classification metrics,
- uncertainty intervals,
- headline coefficient/effect estimates,
- ranking/hotspot performance,
- sensitivity-analysis results.

Use a table where possible.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Review claim | No empirical validation metric | Not stated | Not applicable | This is a methodological review, not a new empirical model evaluation | Pages 2–4 |
| Count-data property | Poisson mean-variance equality | `E[y_i] = VAR[y_i]` implied/discussed | Poisson regression | Violated by overdispersion or underdispersion | Pages 4, 12–13 |
| Negative binomial variance | `VAR[y_i] = E[y_i] + αE[y_i]^2` | Formula stated | Negative binomial / Poisson-gamma | Allows variance to exceed mean through overdispersion parameter α | Page 13 |
| Methodological issue table | Data/methodological issues | Overdispersion, underdispersion, time-varying explanatory variables, spatial/temporal correlation, low sample mean/small sample size, severity/type correlation, under-reporting, omitted variables, endogenous variables, functional form, fixed parameters | Crash-frequency data generally | Checklist of risks for crash-frequency modelling | Table 1, pages 43–44 |

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? Not applicable / not stated. The paper is a review and does not report a new empirical model with its own validation split.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. Not applicable.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? Mostly methodological comparison and theoretical/statistical adequacy, not direct predictive validation.
- Are any metrics likely to be optimistic for real-world deployment? Not applicable to new metrics. The paper explicitly warns that superior statistical fit does not necessarily imply practical predictive capability or transferability.
- Which metric, if any, is most relevant to Open Road Risk? No single metric. The most relevant content is the diagnostic checklist: overdispersion, low mean/zero-heavy data, temporal/spatial correlation, omitted variables, functional form, and fixed/random parameter assumptions.

Important:

- Do not invent metrics.
- Do not call a metric "predictive accuracy" without qualification unless the paper uses held-out, cross-validated, temporal, spatial, or external validation data.
- Do not treat DIC, AIC, BIC, WAIC, posterior fit, or in-sample accuracy as equivalent to external predictive validation.
- If the paper reports only model-comparison metrics, say that clearly.
- If the paper reports no usable quantitative validation, write `Not stated`.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The paper discusses low sample mean, small sample size, and preponderance of zeros as major crash-frequency problems. It reviews several count-model families affected by or designed for these issues.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson, negative binomial / Poisson-gamma, Poisson-lognormal, zero-inflated Poisson, zero-inflated negative binomial, Conway-Maxwell-Poisson, gamma models, finite mixture / Markov switching models, and others are discussed. Zero-inflated models are explicitly discussed, but the paper also warns that they may be theoretically problematic for highway safety because the zero/safe state implies a long-term mean of zero.
- Whether high-risk locations are evaluated separately: Not as a new empirical analysis. The review discusses model use for crash frequencies and site-level roadway entities.
- Evidence quote or page reference: Page 7 says low sample means and many zero observations can cause incorrectly estimated parameters and erroneous inferences. Page 15 describes zero-inflated models and the criticism that a long-term zero-crash state may not reflect the crash-data generating process.
- Practical relevance to my sparse collision link-year dataset: High. Your link-year table has rare injury collisions and many zeros, so this paper supports careful diagnostics of dispersion, low mean, and zero-heavy behaviour. It does not mean zero-inflated models should be adopted by default.

Important:

- Do not use the tag or phrase `zero-inflated` unless the paper explicitly uses a zero-inflated model.
- If the data are zero-heavy but the model is not zero-inflated, say `zero-heavy counts handled using...`.

## 11. Validation Strategy

- Train/test split method: Not stated; review paper.
- Spatial holdout used? not stated
- Temporal holdout used? not stated
- Grouped holdout used? not stated
- Cross-validation type: Not stated.
- Metrics: Not stated as new validation metrics.
- External validation: Not stated.
- Leakage or generalisation risks: The review identifies several risks that affect generalisation or inference: temporal/spatial correlation, time aggregation, omitted variables, endogenous variables, fixed-parameter assumptions, and poor functional form. It also notes that black-box methods may not generalise to other datasets.
- Evidence quote or page reference: Pages 6–7 discuss temporal and spatial correlation. Page 9 discusses omitted variable bias. Pages 9–10 discuss endogenous variables. Page 11 discusses fixed parameters and unobserved heterogeneity. Page 26 warns that neural and support vector machine methods often cannot be generalised to other datasets.
- What I should copy or avoid:
  - Copy: Use the paper as a methodological risk checklist for validation and diagnostics.
  - Copy: Keep grouped-by-link validation and consider spatial/temporal validation where feasible.
  - Avoid: Treating improved statistical fit as sufficient evidence of real-world predictive usefulness.
  - Avoid: Adding zero-inflated or highly complex random-parameter models simply because they fit better in-sample.

Important:

- Distinguish classic data leakage from weaker external generalisation.
- If a spatial random-effect model uses neighbouring observed outcomes during fitting, describe this as an in-sample spatial smoothing/generalisation limitation unless the paper makes a true leakage error.
- Do not overstate this as leakage without evidence.

## 12. Key Findings Relevant to My Project

Give 3–6 findings that are directly useful for my road-risk pipeline.

For each finding:

- Finding: Crash-frequency data are count data and ordinary least squares is generally inappropriate.
- Why it matters: Supports using Poisson/negative-binomial-style GLMs or other count models for Stage 2 rather than treating crash counts as continuous.
- Evidence quote or page reference: Page 12 states that because crash-frequency data are non-negative integers, ordinary least-squares regression is not appropriate.
- Confidence: high

- Finding: Overdispersion is a core issue, but the negative binomial model is not a complete solution.
- Why it matters: Your GLM baseline should report dispersion diagnostics and avoid treating NB as automatically correct, especially with low mean or sparse link-year counts.
- Evidence quote or page reference: Pages 4 and 13–14 discuss overdispersion and the negative binomial model; page 14 notes limitations with underdispersion, low sample mean, and small samples.
- Confidence: high

- Finding: Low sample mean and many zeros can create estimation problems and bias in traditional count models.
- Why it matters: Your 1–2% non-zero link-year collision outcome is exactly the kind of sparse setting where naive model comparison can mislead.
- Evidence quote or page reference: Page 7 says low sample means and a preponderance of zeros can result in incorrectly estimated parameters and erroneous inferences.
- Confidence: high

- Finding: Exposure functional form is not trivial; traffic flow and segment length may have non-linear or specification-sensitive relationships with crash frequency.
- Why it matters: Your exposure offset `log(AADT × length × 365 / 1e6)` is defensible but should be compared against alternative forms or diagnostics, not assumed final.
- Evidence quote or page reference: Pages 10–11 discuss traffic flow and segment length as exposure measures and warn that conflicting findings may indicate unobserved heterogeneity or specification problems.
- Confidence: high

- Finding: Spatial and temporal correlation matter when the same roadway entity appears repeatedly or nearby roadway entities share unobserved effects.
- Why it matters: Supports grouped-by-link validation and residual checks for spatial structure; also supports caution when interpreting link-year rows as independent.
- Evidence quote or page reference: Page 6 discusses repeated observations from the same roadway entity and spatial correlation among nearby roadway entities.
- Confidence: high

- Finding: More complex models may improve statistical fit but can reduce interpretability, transferability, or feasibility.
- Why it matters: Supports your current split between interpretable GLM diagnostics and ML ranking/benchmarking, with caution against over-claiming the ML output.
- Evidence quote or page reference: Pages 21 and 26 discuss random-parameter and black-box model limitations, including transferability and interpretability.
- Confidence: high

Important:

- Do not overgeneralise from a small or simplified study area.
- If the finding supports a direction rather than proves a repo decision, say that.
- Preserve the paper's scope. Use phrases like "in this case study" or "this suggests" where appropriate.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Dispersion diagnostics for GLM | Checks whether Poisson assumptions are badly violated | Link-year crash counts and fitted means | Review-level | High | Stage 2 / validation / documentation | low | Treating dispersion as a single global truth when structure varies by road class |
| Negative binomial comparison | Standard overdispersion alternative to Poisson | Link-year counts and covariates | Review-level | High | Stage 2 / baseline comparison | low/medium | NB can still struggle with low mean and small samples; may not solve spatial/temporal dependence |
| Alternative exposure functional forms | Tests whether AADT and length should enter only as fixed offset | AADT, link length, crash counts | Review-level | High | Stage 2 / validation | medium | Data dredging or weakening interpretability if not pre-specified |
| Spatial and grouped validation diagnostics | Tests robustness beyond repeated link-years | Link IDs, geography, fitted predictions/residuals | Review-level | High | validation | medium | Spatial split design can be arbitrary and pessimistic/optimistic depending on geography |
| Temporal holdout or year-block checks | Assesses performance across time | Crash years, feature years | Review-level | High | validation | medium | Confounds with COVID/year effects and changing reporting/exposure |
| Severity/type multivariate scoping note | Captures dependence between crash severity/type counts | Severity/type crash counts | Review-level | Medium | future feature / documentation | high | Overcomplication with sparse fatal/serious outcomes |
| Omitted-variable and endogeneity audit | Documents variables that could bias inference | Model feature list and plausible causal ordering | Review-level | High | documentation / validation | low | Can become generic unless tied to specific features |
| Fixed vs random parameter sensitivity | Tests whether effects differ by road family/area | Enough data by road family/area | Review-level | Medium | candidate model extension | high | Computational cost and weak transferability at 21.7M rows |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full random-parameter count model across all links | Computationally heavy and observation-specific; paper warns transferability may suffer | Very large-scale estimation infrastructure and strong modelling assumptions | Review-level | Low/medium at 21.7M link-years | Use stratified GLMs by road family or random-effect approximations on samples | medium |
| Full multivariate severity model as production output | Sparse severe/fatal counts and correlated outcomes make estimation complex | Sufficient severity counts by link/year | Review-level | Low/medium | Start with severity diagnostics or separate aggregate severity model | high |
| Zero-inflated model by default | Paper explicitly notes theoretical criticism of long-term zero-crash state | Need credible structural zero process | Review-level | Low unless structural-zero logic is defensible | Compare as diagnostic only, not default | high |
| Black-box neural/SVM production model for risk ranking | Interpretability and transferability concerns | Stable feature distribution and external validation | Review-level | Medium technically, low as sole production rationale | Keep ML as benchmark/ranker with GLM diagnostics and calibration checks | high |
| Detailed naturalistic-driving causal modelling | Requires acceleration, braking, steering, driver response, black-box data | Data not in open-data UK pipeline | Review-level | Low | Use open-data proxy features and avoid causal claims | high |

Important:

- A technique can be conceptually transferable but practically difficult at Open Road Risk scale.
- Mark computationally unrealistic methods as medium or low transferability even if they are statistically attractive.
- Do not recommend adding features that are already in the repo; instead suggest validation, comparison, or documentation of existing features.
- Include the study scale from the paper where available, such as number of links, intersections, crashes, years, or regions.

## 14. Pipeline Implications

Answer these directly:

- Does this paper support using exposure-normalised collision risk? Yes, indirectly. It supports the importance of exposure variables such as traffic flow and segment length, and describes vehicle-miles travelled as a traditional exposure measure. It does not specifically endorse your exact offset.
- Does it suggest better handling of AADT/AADF uncertainty? Indirectly. It warns about time-varying explanatory variables, omitted variables, and functional form, but does not give a traffic-count uncertainty method.
- Does it suggest useful geometry or road-context features? Broadly yes: it supports inclusion of relevant road/context variables to reduce omitted-variable bias. It does not list a specific UK open-data feature set.
- Does it suggest better modelling of junctions? Indirectly. It frames intersections as a major roadway entity and discusses spatial/temporal correlation, but does not provide a junction-specific method.
- Does it suggest better treatment of severity? Yes as a caution: severity-specific counts are correlated, so independent severity count models can be statistically inefficient or misleading.
- Does it suggest better validation design? Yes. It strongly supports checks for temporal/spatial correlation and the danger of treating repeated or nearby roadway entities as independent.
- Does it expose a weakness in my current approach? Yes: the current offset structure and XGBoost production percentile need careful documentation and validation because exposure functional form, omitted variables, low mean/zero-heavy outcomes, and spatial/temporal correlation can distort estimates and rankings.

## 15. Repo Actionability

Give up to 5 concrete implications for my repo.

For each:

- Suggested repo action: Add a Stage 2 modelling limitations note covering overdispersion, low mean/zero-heavy counts, exposure functional form, spatial/temporal correlation, omitted variables, and endogeneity.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The review identifies these as core data and methodological issues for crash-frequency data.
- Evidence quote or page reference: Table 1, pages 43–44; discussion pages 4–11.
- Effort: low
- Risk if implemented badly: Becoming generic boilerplate rather than linked to Open Road Risk-specific diagnostics.

- Suggested repo action: Add a dispersion and zero-heavy diagnostic report by road class/form-of-way/facility family for the GLM baseline.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper warns that overdispersion, underdispersion, low sample mean, and many zeros can bias traditional count models.
- Evidence quote or page reference: Pages 4–7 and 13–16.
- Effort: medium
- Risk if implemented badly: Misinterpreting zero-heavy data as automatic support for zero-inflated models.

- Suggested repo action: Run a baseline comparison of the current fixed exposure offset against one or two alternative exposure specifications, such as AADT and length as covariates/splines or exposure offset plus interaction with road family.
- Action type: baseline comparison
- Relevant stage: Stage 2 / validation
- Why the paper supports it: It notes that traffic flow and segment length exposure relationships may be non-linear and that conflicting findings can reflect unobserved heterogeneity or specification problems.
- Evidence quote or page reference: Pages 10–11.
- Effort: medium
- Risk if implemented badly: Overfitting exposure form to in-sample fit and weakening the interpretability of exposure-adjusted risk.

- Suggested repo action: Add grouped and spatial/temporal validation summary tables for Stage 2 rankings, separate from in-sample fit diagnostics.
- Action type: diagnostic / baseline comparison
- Relevant stage: validation
- Why the paper supports it: It discusses repeated observations from roadway entities and nearby units sharing unobserved effects, which can affect estimation and generalisation.
- Evidence quote or page reference: Page 6.
- Effort: medium/high
- Risk if implemented badly: A poorly chosen spatial split may look rigorous but not answer the deployment question.

- Suggested repo action: Keep XGBoost framed as a predictive/ranking benchmark and add a clear interpretability caveat; do not let it replace count-model diagnostics without calibration and external-style validation.
- Action type: documentation note / diagnostic
- Relevant stage: Stage 2 / documentation / validation
- Why the paper supports it: The review warns that black-box models can be difficult to interpret and may not generalise to other datasets.
- Evidence quote or page reference: Pages 25–26.
- Effort: low/medium
- Risk if implemented badly: Overstating the production percentile as a validated safety-performance function rather than an exploratory ranking.

Important:

- Suggested actions should be realistic for Open Road Risk.
- Prefer the least disruptive useful action.
- If a feature already exists, suggest testing, documenting, validating, or comparing it rather than "add feature".
- Do not suggest large architecture changes unless the paper gives strong support.
- Prefer diagnostic additions over disruptive model rewrites unless evidence is strong.
- Avoid recommending production changes directly from a single paper.

## 16. Query Tags

- crash-frequency
- count-data-models
- Poisson
- negative-binomial
- Poisson-gamma
- overdispersion
- underdispersion
- low-sample-mean
- zero-heavy-counts
- zero-inflated-models
- exposure
- vehicle-miles-travelled
- spatial-correlation
- temporal-correlation
- omitted-variable-bias
- endogenous-variables
- random-effects
- random-parameters
- multivariate-counts
- severity-correlation

Important:

- Do not use `zero-inflation` unless the paper explicitly fits a zero-inflated model.
- Prefer precise tags over fashionable ones.

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: No single empirical dataset, train/test split, spatial holdout, temporal holdout, quantitative predictive validation result, or production-ready model recommendation is provided because this is a review paper.
- Parts of the paper that need manual checking: The large review tables on pages 45 onward may be useful if you want a separate model-family comparison table with every cited study and method. The extraction here does not attempt to reproduce the full bibliography-level table.
- Any likely ambiguity or risk of misinterpretation: The paper is a methodological review, so it should not be treated as evidence that any one model family is best for Open Road Risk. Its strongest value is as a checklist for risks, diagnostics, and conservative model framing.
