# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: McFadden logit.pdf
- Suggested Markdown filename: paper-extraction-mcfadden-not-stated-conditional-logit.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload; scanned/image PDF
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? uncertain
- Notes on access limitations: The PDF text was not machine-parsed. Extraction is based on the rendered page images available in the chat interface. Page references are therefore approximate page-image references, not verified publisher pagination beyond the visible page numbers.

## 1. Citation

- Title: Conditional logit analysis of qualitative choice behavior
- Authors: Daniel McFadden
- Year: Not stated
- DOI or URL, if present: Not stated
- Country / region studied: Not stated
- Study setting: not stated

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper formulates and estimates conditional logit models for qualitative choice behaviour, where individuals choose among discrete alternatives based on measured attributes of individuals and alternatives.
- Main purpose: methodological / choice modelling / statistical estimation
- Evidence quote or page reference: Page 106 states that the paper is concerned with “empirical models of population choice behavior from distributions of individual decision rules” and lists applications such as college attendance, occupation, labor force participation, mode choice, and destination choice.

## 3. Response Variable

- Target variable: Discrete choice among a finite set of alternatives.
- Collision type: Not stated
- Severity handling: Not stated
- Count, binary, rate, risk score, severity class, or other: Multinomial categorical choice; binary choice appears as a special case.
- Time window used for outcomes: Not stated
- Evidence quote or page reference: Page 107 defines the observed data as choice sets and “a sequence of choices observed for individuals,” and describes the probability that an individual chooses one alternative from a set.

## 4. Exposure Handling

- Exposure variable used, if any: Not stated
- Traffic count source: Not stated
- Whether exposure is modelled, observed, assumed, or ignored: Not applicable; the paper is not a crash-frequency or exposure-normalised road safety study.
- Treatment of missing or sparse traffic counts: Not stated
- Whether offset terms, rates, denominators, or normalisation are used: Not stated
- Evidence quote or page reference: Pages 107–110 formulate probabilities of discrete choices among alternatives, not crash rates, exposure denominators, or count offsets.
- Transferability to my AADF/WebTRIS setup: low
- Notes: The transferable part is not exposure handling. The relevant idea is conditional choice modelling: probabilities depend on alternative-specific attributes and choice sets. That may be conceptually relevant to driver route-choice or test-route selection, but not directly to AADT offset modelling.

Important:

- Mathematical exposure structure: Not applicable.
- Specific data-source transferability: Not applicable.

## 5. Spatial Unit of Analysis

- Unit: Individual decision-maker × choice set / alternative.
- Segment length or segmentation rule: Not stated
- How crashes are assigned to the network: Not stated
- Treatment of junctions/intersections: Not stated
- Spatial aggregation risks: Not stated
- Evidence quote or page reference: Page 107 frames the data as observations of decision-makers, measured attributes, and alternative sets. Page 106 lists “choice of shopping travel mode and destination” as an empirical application, but the visible pages do not provide road-network spatial units.
- Relevance to OS Open Roads link-based pipeline: Low for the core collision-risk model. Possible relevance only if modelling discrete route or mode choices, not link-level crash frequencies.

## 6. Temporal Unit of Analysis

- Years covered: Not stated
- Temporal resolution: Not stated
- Whether seasonality or time-of-day is modelled: Not stated
- Whether before-after or panel structure is used: Not stated
- Evidence quote or page reference: Page 107 mentions repeated observations may be available for individuals, but the displayed derivation does not specify a temporal panel design.
- Relevance to WebTRIS-style time profiles: Low. The paper does not model traffic profiles, temporal exposure, or traffic counts.

## 7. Engineered Features

List the most important engineered features, especially those I could recreate.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Individual attributes `s` | Observed attributes of decision-makers | Included in utility/probability function | Allows choice probabilities to vary by decision-maker | Low for link-risk model; possible for route-choice extension |
| Alternative attributes `x` | Measured attributes of alternatives | Included in conditional utility function | Allows probabilities to depend on properties of each available option | Medium for route-choice modelling; not a Stage 2 crash feature |
| Alternative-set membership `B` | Choice set available to each decision-maker | Conditions the probability on available alternatives | Critical because probabilities are defined relative to the set of available alternatives | Medium for route-choice / DTC route alternatives |
| Alternative-specific utility component `v(s, x)` | Modelled function of attributes | Linear-in-parameters form assumed for estimation in Section II | Produces estimable conditional logit probabilities | Conceptually transferable to route-choice modelling |
| Alternative effect / benchmark alternative | Alternative labels and availability | Utility may include measured taste and alternative effects; some effects may require normalisation | Identifiability depends on variation in choice sets | Low to medium; useful as a modelling caution |

Only features actually used or defined in the paper are included. These are not road-safety variables.

## 8. Model Architecture

- Algorithms/models used: Conditional logit model; binary logit as a special case; multinomial choice probability model.
- Baseline model: Not stated as a separate baseline.
- Final/preferred model: Conditional logit model derived from utility maximisation with independently and identically distributed Weibull / extreme-value disturbances.
- Loss function or likelihood, if stated: Maximum likelihood estimation of conditional logit probabilities.
- Offset/exposure term, if used: Not stated
- Spatial autocorrelation handling: Not stated
- Temporal dependence handling: Not stated
- Interpretability method: Coefficients in the utility function; likelihood-based hypothesis tests; coefficient of determination analogue.
- Evidence quote or page reference: Pages 108–112 derive selection probabilities and state the conditional logit formula. Page 110 gives the familiar conditional logit probability form. Pages 113–118 discuss conditional logit estimation, likelihood, first derivatives, second derivatives, and maximum likelihood computation.

## 9. Reported Metrics / Quantitative Results

Extract the main quantitative results reported in the paper.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Theoretical property | Independence of irrelevant alternatives | Assumed as Axiom 1 | Conditional logit derivation | Odds of choosing one alternative over another are independent of other available alternatives | Page 109 |
| Theoretical property | Positivity | Choice probability greater than zero | Conditional logit derivation | All alternatives in the choice set must have positive selection probability | Page 109 |
| Model form | Conditional logit probability | `P(x | s, B) = exp(v(s,x)) / sum exp(v(s,z))` | Conditional logit | Choice probability is normalised exponential utility over available alternatives | Page 110 |
| Estimation | Maximum likelihood | No empirical fit value stated in visible pages | Conditional logit estimation | Estimation uses likelihood over repeated trials and observed choice counts | Pages 113–115 |
| Statistical inference | Asymptotic normality / chi-square testing | Formulae provided; no empirical value stated | Maximum likelihood estimator | Large-sample inference for parameters and restrictions | Pages 119–122 |
| Goodness-of-fit analogue | Coefficient of determination analogue | Formula provided; no empirical value stated | Conditional logit | Likelihood-ratio-based analogue to `R²` for testing relative frequencies vs predictions | Page 121 |
| Numerical example | Simulated parameter estimates | Values shown in Table 1 | Example 1 | Demonstrates maximum likelihood estimation behaviour in simulated samples | Page 124 |

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? Mostly theoretical / asymptotic and in-sample likelihood-based. Table 1 appears to be a simulation example, not external validation.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They mainly support estimation, identification, and in-sample likelihood-based inference.
- Are any metrics likely to be optimistic for real-world deployment? Not applicable as predictive deployment metrics are not reported in the visible material.
- Which metric, if any, is most relevant to Open Road Risk? None for Stage 2 crash-risk prediction. The most relevant methodological item is the warning around choice-set definition and independence of irrelevant alternatives if modelling route choice.

Important:

- The paper does not report road-safety predictive metrics.
- The paper does not report hotspot performance, calibration, or external validation.
- The paper’s likelihood-based statistics should not be interpreted as evidence of predictive generalisation for road-risk modelling.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Not stated
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Not stated
- Whether high-risk locations are evaluated separately: Not stated
- Evidence quote or page reference: The visible pages concern discrete choice probabilities and conditional logit estimation, not rare crash counts.
- Practical relevance to my sparse collision link-year dataset: Low. Conditional logit is not a natural model for zero-heavy link-year collision counts unless the problem is reframed as discrete choice among alternatives, which would be a different target.

Important:

- The paper does not use a zero-inflated model.
- The paper does not address zero-heavy crash counts.

## 11. Validation Strategy

- Train/test split method: Not stated
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Not stated
- Metrics: Likelihood-based estimation and asymptotic test statistics; simulation table visible on page 124.
- External validation: Not stated
- Leakage or generalisation risks: Not stated for crash modelling. For choice modelling, the main limitation is structural: the independence of irrelevant alternatives assumption may be inappropriate when alternatives are close substitutes.
- Evidence quote or page reference: Page 113 explicitly warns that the model applies only when alternatives “can plausibly be assumed to be distinct and weighed independently.” Pages 119–122 discuss large-sample statistical properties and tests, not train/test validation.
- What I should copy or avoid: Copy the discipline of explicit behavioural assumptions. Avoid treating conditional logit as a generic predictive model unless the choice set and IIA assumption are defensible.

Important:

- There is no spatial/temporal validation design relevant to Open Road Risk.
- This is not a road-safety crash-frequency validation paper.

## 12. Key Findings Relevant to My Project

Give 3–6 findings that are directly useful for my road-risk pipeline.

### Finding 1

- Finding: Conditional logit is suitable for modelling choices among discrete alternatives when probabilities depend on individual and alternative attributes.
- Why it matters: This could be relevant only to a separate route-choice or route-selection component, not to link-year collision counts.
- Evidence quote or page reference: Page 106 lists “choice of shopping travel mode and destination” as an application; pages 107–110 formulate choice probabilities over alternative sets.
- Confidence: high

### Finding 2

- Finding: The model relies on the independence of irrelevant alternatives assumption.
- Why it matters: Route alternatives often share links or are close substitutes, so uncritical use for route choice could be misleading.
- Evidence quote or page reference: Page 109 states Axiom 1 as “Independence of Irrelevant Alternatives.” Page 113 notes the model applies where alternatives can plausibly be treated as distinct and independently weighed.
- Confidence: high

### Finding 3

- Finding: The conditional logit form follows from a utility-maximising model with additive stochastic utility terms under specific distributional assumptions.
- Why it matters: This is useful if Open Road Risk later models driver choices, but it does not directly justify any crash-risk model architecture.
- Evidence quote or page reference: Pages 108–112 derive the utility representation and logit selection probabilities.
- Confidence: high

### Finding 4

- Finding: Maximum likelihood estimation is central, but identification depends on variation in attributes and choice sets.
- Why it matters: If applying this to route alternatives, the data must contain enough variation across routes and observed choices; otherwise coefficients may be unidentified or unstable.
- Evidence quote or page reference: Pages 115–118 discuss rank, nonsingularity, and conditions for a unique maximum.
- Confidence: medium

### Finding 5

- Finding: The paper offers statistical tests and likelihood-based diagnostics, not evidence of out-of-sample predictive performance.
- Why it matters: It should not be used as evidence that a route-choice model will generalise across geography or time.
- Evidence quote or page reference: Pages 119–122 discuss asymptotic statistical properties and likelihood-ratio-type tests.
- Confidence: medium

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Conditional logit for route choice | Could model probability of choosing one route from a set of candidate routes | Observed choices, candidate alternatives, route attributes | Not stated in visible pages | Low for Stage 2; medium for a future route-choice module | future feature / documentation | medium | IIA assumption likely violated by overlapping routes |
| Utility-based framing for route alternatives | Provides a disciplined way to separate route attributes from choice probabilities | Candidate routes and attributes such as distance, time, risk, turns, road class | Not stated | Medium for small DTC route studies; low for national link-level crash model | documentation / small pilot | low to medium | Could be mistaken for causal preference evidence |
| Likelihood-based comparison of choice models | Could compare alternative route-choice specifications | Observed route choices or credible proxy choices | Not stated | Medium only if suitable choice observations exist | validation / baseline comparison | medium | In-sample likelihood does not prove predictive transferability |
| Explicit choice-set definition | Forces clarity on what alternatives were available | Candidate alternative generation logic | Not stated | Medium for route-choice; not relevant to link-year risk | documentation | low | Badly generated alternatives can dominate results |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Conditional logit as Stage 2 collision-count model | Stage 2 outcome is injury collision count, not a discrete choice among alternatives | Choice-set structure and chosen alternatives are absent | Not stated | Low | Keep count models / ML risk models for collisions | high |
| IIA-based multinomial route choice for overlapping road routes | Candidate routes often share segments and are not independent substitutes | Independence of irrelevant alternatives is doubtful | Not stated | Low to medium | Consider nested logit, path-size logit, mixed logit, or treat as exploratory only | high |
| Using likelihood diagnostics as deployment validation | The paper’s visible diagnostics are estimation/inference tools, not held-out validation | Spatial/temporal held-out data not discussed | Not stated | Low | Use grouped, spatial, and temporal validation separately | high |
| Direct road-safety feature recommendations | The paper does not analyse crashes, road geometry, traffic exposure, or severity | Road safety data absent | Not stated | Low | Use this only for methodology notes around route-choice modelling | high |

Important:

- The paper is conceptually transferable for qualitative route-choice problems.
- It is not directly transferable to exposure-adjusted road collision risk.
- It should not drive production changes to Open Road Risk’s Stage 2 collision model.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? No. It does not discuss crash exposure, traffic counts, offsets, or collision rates.
- Does it suggest better handling of AADT/AADF uncertainty? No.
- Does it suggest useful geometry or road-context features? Not for crash risk. It suggests that alternative-specific attributes can enter a choice model, which could include geometry if modelling route choices.
- Does it suggest better modelling of junctions? No.
- Does it suggest better treatment of severity? No.
- Does it suggest better validation design? Only indirectly: it reinforces that model assumptions and identification conditions must be explicit. It does not provide spatial, grouped, or temporal validation methods.
- Does it expose a weakness in my current approach? Not in the current Stage 2 collision-risk approach. It exposes a possible weakness in any future route-choice extension if overlapping or similar alternatives are treated as independent under a simple multinomial logit.

## 15. Repo Actionability

Give up to 5 concrete implications for my repo.

### Action 1

- Suggested repo action: Add a documentation note that McFadden conditional logit is relevant only to future route-choice or alternative-selection modelling, not to Stage 2 crash counts.
- Action type: documentation note
- Relevant stage: documentation
- Why the paper supports it: The paper is about qualitative choice behaviour and conditional choice probabilities, not crash-frequency modelling.
- Evidence quote or page reference: Pages 106–110 describe population choice behaviour, individual choice sets, and conditional logit probabilities.
- Effort: low
- Risk if implemented badly: Overstating relevance could confuse the literature record and imply support for a model the paper does not address.

### Action 2

- Suggested repo action: If route-choice modelling is piloted, explicitly document the candidate alternative set and why each alternative was available.
- Action type: documentation note / small pilot
- Relevant stage: future feature
- Why the paper supports it: Choice probabilities are conditioned on available alternatives.
- Evidence quote or page reference: Page 107 defines choice sets and probabilities conditional on the available set.
- Effort: low
- Risk if implemented badly: Poor choice-set generation can make coefficients meaningless.

### Action 3

- Suggested repo action: For any future route-choice pilot, add an assumption check or caveat for independence of irrelevant alternatives.
- Action type: diagnostic / documentation note
- Relevant stage: validation / future feature
- Why the paper supports it: IIA is a stated axiom and the paper warns about cases where alternatives are not distinct.
- Evidence quote or page reference: Page 109 states the IIA axiom; page 113 warns about close substitutes such as different bus options.
- Effort: low
- Risk if implemented badly: A simple logit may overstate substitution patterns between routes sharing many links.

### Action 4

- Suggested repo action: Treat conditional logit as a baseline comparison only if observed route choices or credible revealed-preference data are available.
- Action type: baseline comparison
- Relevant stage: future feature / validation
- Why the paper supports it: Estimation is based on observed choices and maximum likelihood over trials.
- Evidence quote or page reference: Pages 113–115 formulate conditional logit estimation from observed choices and repeated trials.
- Effort: medium
- Risk if implemented badly: Using synthetic “choices” as if observed choices could create false behavioural conclusions.

### Action 5

- Suggested repo action: Do not alter Stage 2 crash-risk modelling based on this paper.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper does not model crash counts, exposure, rare events, severity, or network risk.
- Evidence quote or page reference: The visible paper is consistently framed around qualitative choice behaviour, not road collisions.
- Effort: low
- Risk if implemented badly: Applying conditional logit to the wrong target would be a category error.

## 16. Query Tags

- conditional-logit
- multinomial-logit
- qualitative-choice
- discrete-choice
- utility-maximisation
- IIA
- independence-of-irrelevant-alternatives
- choice-set
- alternative-specific-attributes
- route-choice
- maximum-likelihood
- likelihood-ratio
- revealed-preference
- behavioural-model
- not-crash-frequency
- not-exposure-model
- model-identification
- asymptotic-inference

Important:

- No `zero-inflation` tag is used because the paper does not fit a zero-inflated model.

## 17. Confidence and Gaps

- Overall confidence in extraction: medium
- Important details not stated in the paper: Publication year, full book/source metadata, DOI/URL, empirical application details beyond the visible section headings, and any complete applied results beyond the visible simulation table.
- Parts of the paper that need manual checking: The empirical application section listed in the contents appears not to be fully visible in the supplied page images, or at least was not available as parseable text. The publication metadata should be checked manually from the book or source record.
- Any likely ambiguity or risk of misinterpretation: This is a foundational econometric choice-modelling paper, not a road-safety paper. Its relevance to Open Road Risk is indirect and should be limited to possible route-choice or route-selection extensions. It does not support production changes to collision-frequency or exposure-offset modelling.
