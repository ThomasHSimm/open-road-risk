# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: Negative_Binomial_Analysis_of_Intersection-Acciden.pdf
- Suggested Markdown filename: final-poch-mannering-1996-nb-intersection.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: original PDF plus two Markdown extractions
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The PDF text and page images were accessible, but several table/equation passages have OCR artefacts. Numerical values used below were reconciled against the original PDF snippets and the two prior extractions, but table values should still be manually checked before formal publication.

## 1. Citation

- Title: Negative Binomial Analysis of Intersection-Accident Frequencies
- Authors: Mark Poch; Fred Mannering
- Year: 1996
- DOI or URL, if present: Not stated
- Journal / venue, if present: Journal of Transportation Engineering, Vol. 122, No. 2, March/April 1996, pp. 105–113
- Country / region studied: United States / Bellevue, Washington
- Study setting: Urban and suburban intersections, specifically intersections targeted for operational improvements.

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper estimates negative binomial regression models of annual accident frequency on individual intersection approaches, including total accidents and separate accident-type models.
- Main purpose: safety performance function / descriptive-explanatory accident-frequency modelling / methodological comparison of Poisson vs negative binomial.
- Evidence quote or page reference: Page 105 states that the paper estimates “a negative binomial regression of the frequency of accidents at intersection approaches” using seven-year accident histories from 63 Bellevue intersections. Page 106 states that the objective is to develop statistical models of annual accident frequency on individual intersection approaches.

## 3. Response Variable

- Target variable: Annual accident frequency on an individual intersection approach.
- Collision type: Total approach accidents include all reported accident types in Bellevue. Separate models are estimated for rear-end, angle, and approach-turn accidents.
- Severity handling: Severity is not modelled separately. The paper models total accident frequency and accident mechanism/type, not fatal/serious/minor/property-damage severity classes.
- Count, binary, rate, risk score, severity class, or other: Count; non-negative integer annual accident frequency.
- Time window used for outcomes: Annual observations from 1987–1993, excluding the year in which an operational improvement occurred.
- Evidence quote or page reference: Page 106 says four models predict total accident frequency, rear-end accident frequency, angle accident frequency, and approach-turn accident frequency, and that the dependent variable is a non-negative integer. Page 107 states that accident data were taken at each approach in one-year intervals and gives the 1987–1993 study period.

Important:

- The paper uses “accidents,” not the STATS19 injury-collision-only scope used in Open Road Risk.
- The PDF states that total approach accidents include all reported accident types, including angle, sideswipe/lane change, rear-end, head-on, fixed object/parked vehicle, approach turn, pedestrian/bicyclist, and others.
- Whether the dataset includes property-damage-only accidents is likely but not explicitly separable from the text; do not overstate severity composition beyond “all reported accident types.”

## 4. Exposure Handling

- Exposure variable used, if any: Traffic-volume variables are included as covariates. These include approach left-turn volume, right-turn volume, total opposing approach volume, total intersection volume or related movement/approach volumes depending on model.
- Traffic count source: City of Bellevue traffic counts. Morning peak, afternoon peak, and midday traffic volumes were expanded to daily counts using standard expansion formulas. Missing-year counts were converted from known counts using Bellevue yearly factors for different growth-rate areas.
- Whether exposure is modelled, observed, assumed, or ignored: Traffic exposure is observed/estimated and included as explanatory variables. It is not used as a formal offset.
- Treatment of missing or sparse traffic counts: Missing traffic values in some years were estimated using city yearly expansion factors from counts of a different vintage.
- Whether offset terms, rates, denominators, or normalisation are used: No offset, denominator, or accident-rate normalisation is reported. The negative binomial mean is log-linear in the covariates.
- Evidence quote or page reference: Page 107 describes gathering peak/midday traffic volumes, expanding them to daily counts, and using yearly factors for missing traffic years. Page 108 reports elasticities for traffic variables. The negative binomial model form on pages 106–107 uses `ln(lambda_i) = beta X_i + epsilon_i`, with no exposure offset.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The principle that traffic volumes matter strongly is transferable. The detailed approach/turning movement volumes are not generally available in Open Road Risk's open-data pipeline. The exposure structure is also different from Open Road Risk's offset-based model.

Important:

- Mathematical exposure-offset structure: low transferability, because the paper does not use an offset.
- Junction/turning-volume concept: medium conceptual value, but low direct implementation value nationally.

## 5. Spatial Unit of Analysis

- Unit: Intersection approach.
- Segment length or segmentation rule: Each intersection is divided into approach observations. A four-leg intersection can contribute northbound, southbound, eastbound, and westbound approaches.
- How crashes are assigned to the network: Accidents were recorded at each approach in annual intervals. If an accident occurred in the intersection proper, it was assigned to the approach of the at-fault vehicle.
- Treatment of junctions/intersections: Intersections are the core study object. The modelling is approach-level and includes approach-specific geometry, traffic control, turning movements, sight distance, lane configuration, and traffic volumes.
- Spatial aggregation risks: Multiple approaches from the same intersection and repeated annual observations could create correlated errors. The paper checks this using likelihood-ratio tests on approach-direction and year subsets, but does not fit an explicit random-effects, clustered, or spatial model.
- Evidence quote or page reference: Page 106 defines intersection approaches. Page 107 describes splitting intersections into approaches, assigning accidents in the intersection proper to the at-fault approach, and notes the possible correlation problem from repeated observations.
- Relevance to OS Open Roads link-based pipeline: Medium as a warning / junction-method paper, low as a direct model transfer. OS Open Roads links do not naturally encode approach-turn volumes, signal phasing, protected turns, or approach-specific sight distance. It is most useful for documenting that junction/approach risk has mechanisms not captured by ordinary link-level features.

## 6. Temporal Unit of Analysis

- Years covered: 1987–1993.
- Temporal resolution: Annual.
- Whether seasonality or time-of-day is modelled: No. Peak and midday counts are only used to estimate daily traffic counts.
- Whether before-after or panel structure is used: The data are approach-year observations around operational improvements, and the improvement year is excluded. The paper does not estimate a formal before-after treatment-effect model.
- Evidence quote or page reference: Page 107 explains that if an improvement occurred in 1989, the intersection would contribute approach observations for 1987, 1988, 1990, 1991, 1992, and 1993.
- Relevance to WebTRIS-style time profiles: Low. The paper uses daily traffic estimates and annual crashes, not hourly or peak/off-peak crash modelling.

## 7. Engineered Features

List the most important engineered features, especially those that could be recreated.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Left-turn volume | City traffic counts | Peak/midday counts expanded to daily traffic; modelled in thousands of average daily traffic | Strong positive association with total accident frequency; left-turn conflicts are central to junction risk | Low directly; national turning-count data are not available in Open Road Risk |
| Right-turn volume | City traffic counts | Expanded to daily traffic; modelled in thousands | Associated with total/rear-end accidents | Low directly |
| Total opposing approach volume | City traffic counts | Expanded to daily traffic; modelled in thousands | Represents conflict exposure for turning movements; strongest elasticity in total model | Low to medium; opposing-link AADT proxy may be possible, but not movement-specific |
| Opposing left-turn volume | City traffic counts | Expanded daily count | Used in accident-type models | Low directly |
| Number of approach/opposing/through lanes | Intersection design plans | Count variables by approach and lane type | Captures conflict exposure, crossing distance, and lane complexity | Medium only where lane data are reliable; OSM lanes coverage may be sparse |
| Combined through-left lane / left-turn drop lane indicators | Design plans | Binary indicators for lane configuration | Identifies turning/rear-end conflict patterns | Low to medium; may require detailed/manual junction mapping |
| Signal control | Traffic-control inventory/design records | Binary indicator | Signalisation associated with lower total and angle accidents in this selected sample | Low to medium; OSM traffic signals exist but phase/control detail is incomplete |
| Two-phase / eight-phase signal | Signal-control data | Binary indicators | Captures permissive/protected turning and complex high-volume junction operation | Low; signal phasing not nationally available |
| Protected left turn | Signal-control data | Binary movement-control indicator | Protected left turns reduce conflict in this sample | Low |
| Sight-distance restriction | Field/design data | Binary indicator based on fixed objects, curvature, vegetation, misaligned left-turn lanes, or other visibility constraints | Strong positive association with total and type-specific accident frequency | Low directly; curvature/visibility proxies possible only as diagnostics |
| Speed limit | Road data/design plans | Approach and opposing approach speed limits | Continuous speed variables used in total model elasticities | Medium; speed limits partly available/imputable in Open Road Risk |
| Horizontal curve | Road geometry/design plans | Binary approach/opposing-approach curve indicator in type-specific models | Proxy for visibility/alignment risk | Medium; curvature is feasible from geometry |
| Grade greater than 5% uphill/downhill | Design plans/road geometry | Binary threshold | Used in rear-end/angle models | Medium; OS Terrain 50 could support grade diagnostics, but bridge/tunnel handling matters |
| Local street / all approaches local streets | City road classification | Binary indicators | Lower-volume/local context associated with fewer accidents | Medium; road classification is available but UK classes differ |
| CBD/location/year indicators | City context/year | Indicator variables | Controls for city context and year-specific effects | Low to medium; urban-centre proxies and year effects are possible |

Only features actually used or described as model candidates in the paper are included.

## 8. Model Architecture

- Algorithms/models used: Poisson regression introduced as the natural starting point; negative binomial regression used for final models. Ordinary least squares is used only for an informal functional-form check.
- Baseline model: Poisson regression is the statistical baseline but is rejected where the negative binomial dispersion parameter is significant.
- Final/preferred model: Negative binomial regression models for:
  - total accident frequency,
  - rear-end accident frequency,
  - angle accident frequency,
  - approach-turn accident frequency.
- Loss function or likelihood, if stated: Maximum likelihood estimation of the negative binomial model.
- Offset/exposure term, if used: No offset stated.
- Spatial autocorrelation handling: Not modelled directly. Possible within-intersection/approach correlation is examined using likelihood-ratio tests on approach-direction subsets.
- Temporal dependence handling: Not modelled directly. Possible year-to-year correlation is examined using likelihood-ratio tests on year subsets. Year indicators are included in the candidate variable set.
- Interpretability method: Coefficients, t-statistics, elasticities for continuous variables, likelihood-ratio index `rho²`, and likelihood-ratio tests for specification/correlation concerns.
- Evidence quote or page reference: Pages 106–107 derive the Poisson and negative binomial formulations. Page 107 states that standard maximum-likelihood procedures are used. Page 108 defines elasticity. Page 112 presents likelihood-ratio subset tests.

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Sample size | Intersections | 63 | Bellevue targeted intersections | Non-random sample of intersections targeted for operational improvements | Page 105; page 107 |
| Sample size | Observations | 1,385 | Intersection approach-year observations | Approach-level repeated annual dataset | Page 107; Table 1 |
| Accident mix | Total accidents | 1,396 | 1987–1993 recorded accidents | Overall recorded accident count in study sample | Page 107 |
| Accident mix | Rear-end / angle / approach-turn / other | 26% / 30% / 32% / 12% | 1987–1993 recorded accidents | Supports separate accident-type models | Page 107 |
| Model fit | Log-likelihood at zero | -2,123.11 | Total accident model | Null model log-likelihood | Table 1, page 108 |
| Model fit | Log-likelihood at convergence | -1,698.26 | Total accident model | Fitted model log-likelihood | Table 1, page 108 |
| Model fit | `rho²` | 0.200 | Total accident model | In-sample likelihood-ratio index | Table 1, page 108 |
| Dispersion | Negative binomial `alpha` | 0.346; t = 5.96 | Total accident model | Significant overdispersion; supports NB over Poisson | Table 1, page 108; discussion around page 110 |
| Elasticity | Left-turn volume | 2.28 | Total accident model | 1% increase in left-turn volume associated with about 2.28% higher total accident frequency in this fitted model | Table 2, page 108 |
| Elasticity | Right-turn volume | 0.92 | Total accident model | 1% increase in right-turn volume associated with about 0.92% higher total accident frequency | Table 2, page 108 |
| Elasticity | Total opposing approach volume | 2.95 | Total accident model | Strong positive association with total accident frequency | Table 2, page 108 |
| Elasticity | Approach speed limit | 0.98 | Total accident model | Positive association with total accidents | Table 2, page 108 |
| Elasticity | Opposing approach speed limit | -0.34 | Total accident model | Negative coefficient likely reflects correlation/proxy structure, not a causal safety benefit | Table 2 and discussion around pages 108–110 |
| Model fit | `rho²` | 0.505 | Rear-end model | In-sample likelihood-ratio index | Table 3 |
| Model fit | `rho²` | 0.458 | Angle model | In-sample likelihood-ratio index | Table 4 |
| Model fit | `rho²` | 0.537 | Approach-turn model | In-sample likelihood-ratio index | Table 5 |
| Dispersion | Negative binomial `alpha` | 0.319; t = 2.26 | Rear-end model | Significant/positive dispersion estimate | Table 3 |
| Dispersion | Negative binomial `alpha` | 0.696; t = 3.61 | Angle model | Significant/positive dispersion estimate | Table 4 |
| Dispersion | Negative binomial `alpha` | 0.505; t = 3.74 | Approach-turn model | Significant/positive dispersion estimate | Table 5 |
| Specification test | Likelihood-ratio test by approach direction | Chi-square = 47.2; df = 54; p = 0.732 | Total accident model | No strong evidence that approach-direction subset coefficients differ from full-sample coefficients | Page 112 |
| Specification test | Likelihood-ratio test by year subset | Chi-square = 74.24; df = 90; p = 0.885 | Total accident model | No strong evidence that year-subset coefficients differ from full-sample coefficients | Page 112 |
| Functional-form check | OLS `R²` log-linear vs linear | 0.2186 vs 0.2129 | Informal check excluding zero-accident observations | Little difference between two OLS forms; not predictive validation | Page 112 |

After the table:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? The reported model-fit metrics are in-sample. The likelihood-ratio subset tests are specification/correlation checks, not predictive validation. No train/test split, cross-validation, spatial holdout, temporal holdout, or external validation is reported.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They test in-sample model fit, coefficient significance, overdispersion, elasticities, and subset stability. They do not test deployment accuracy or future prediction.
- Are any metrics likely to be optimistic for real-world deployment? Yes. The sample is selected from intersections targeted for operational improvements, and all fit statistics are in-sample.
- Which metric, if any, is most relevant to Open Road Risk? The most relevant results are the significant negative binomial dispersion estimates and the approach/year subset tests as examples of overdispersion and repeated-observation diagnostics. Elasticities are useful for junction-feature interpretation but not transferable effect sizes.

Important:

- `rho²` is an in-sample likelihood-ratio index, not an out-of-sample predictive metric.
- The selected-sample design means coefficients and elasticities should not be treated as representative of all intersections.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The paper models overdispersed non-negative accident counts using negative binomial regression. It does not use zero-inflated or hurdle models.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Negative binomial regression. Poisson is discussed as the natural first count model and rejected where overdispersion is significant.
- Whether high-risk locations are evaluated separately: The whole sample is selected from intersections targeted for operational improvements, so it is biased toward operationally deficient / higher-priority intersections rather than a representative intersection population.
- Evidence quote or page reference: Page 106 explains the Poisson variance limitation and the use of negative binomial when overdispersion exists. Page 107 says the selective nature of the sample must be kept in mind.
- Practical relevance to my sparse collision link-year dataset: Medium. It supports overdispersion checks and NB-style count modelling, but the data are intersection approaches selected for operational deficiencies, not extremely sparse national link-year injury-collision data.

Important:

- Do not tag this as zero-inflated. The paper does not fit a zero-inflated model.
- Do not infer the zero rate unless checked directly from the data; it is not stated in the paper.

## 11. Validation Strategy

- Train/test split method: Not stated / none.
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Not stated.
- Metrics: In-sample log-likelihood, `rho²`, coefficient t-statistics, dispersion significance, elasticities, likelihood-ratio subset tests.
- External validation: Not stated.
- Leakage or generalisation risks: The main risk is sample selection: intersections were chosen because they were targeted for operational improvements. Repeated approaches and repeated years may create correlated errors; the paper tests this but does not model it directly. There is no held-out validation.
- Evidence quote or page reference: Page 107 states that intersections with operational improvements were selected and that the selective nature of the sample must be kept in mind. Page 112 reports likelihood-ratio tests for possible approach and year correlation.
- What I should copy or avoid: Copy the overdispersion test and repeated-observation diagnostic mindset. Avoid copying the in-sample-only validation standard or treating selected high-risk intersections as representative of a full road network.

## 12. Key Findings Relevant to My Project

1. Finding: Negative binomial models are justified over Poisson when the dispersion parameter is significant.
   - Why it matters: Open Road Risk's Stage 2 Poisson GLM should report overdispersion diagnostics and compare NB-style alternatives or robust variance checks.
   - Evidence quote or page reference: Page 106 describes why Poisson is inappropriate under overdispersion. Table 1 reports alpha = 0.346 with t = 5.96 for total accidents.
   - Confidence: high for this dataset; medium for direct transfer to Open Road Risk.

2. Finding: Junction accident frequency depends strongly on movement-specific traffic volumes, especially opposing approach and left-turn volumes.
   - Why it matters: A link-level AADT offset may miss important junction-conflict exposure. Open Road Risk should document this as a limitation for junction/approach risk.
   - Evidence quote or page reference: Table 2 reports elasticities of 2.95 for total opposing approach volume and 2.28 for left-turn volume.
   - Confidence: high for this case study; low to medium for national open-data implementation.

3. Finding: Accident-type-specific models show different mechanisms from the total accident model.
   - Why it matters: STATS19 subtype diagnostics may reveal mechanism-specific patterns that a total-collision model hides, but sparsity will be a constraint.
   - Evidence quote or page reference: Page 107 says separate rear-end, angle, and approach-turn models may provide insights not uncovered by total accident frequency.
   - Confidence: high.

4. Finding: Sight-distance restriction has a strong positive association with accident frequency in the total and accident-type models.
   - Why it matters: Open Road Risk lacks direct sight-distance data. Curvature, grade, junction layout, or visibility proxies may be useful but should be treated as proxies, not direct equivalents.
   - Evidence quote or page reference: Table 1 reports a positive coefficient for sight-distance restriction in the total model; the discussion on page 109 explains sight-distance restrictions from fixed objects, curvature, vegetation, and misaligned left-turn lanes.
   - Confidence: high for the case study; medium for proxy transfer.

5. Finding: Counterintuitive coefficients can represent proxy effects rather than causal effects.
   - Why it matters: This directly supports cautious interpretation of model features in Open Road Risk, especially for variables that encode complex operational context.
   - Evidence quote or page reference: Page 109 explains that eight-phase signal indicators may proxy high-volume, congested, complex intersections and warns that omitting such variables may cause omitted-variable bias.
   - Confidence: high.

6. Finding: Repeated approach/year observations create possible correlation; the paper tests this using likelihood-ratio subset checks.
   - Why it matters: Open Road Risk's link-year structure should keep using grouped validation and repeated-entity diagnostics.
   - Evidence quote or page reference: Page 112 reports approach-direction and year-subset likelihood-ratio tests.
   - Confidence: medium. The paper's tests are useful but not a replacement for modern grouped/spatial validation.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Negative binomial overdispersion diagnostic | Tests whether Poisson variance assumptions are badly violated | Stage 2 count outcome, offset, current covariates | 1,385 approach-year observations | High as diagnostic | Stage 2 / validation | Low to medium | Full 21.7M-row fitting may be heavy; start on stratified samples |
| Compare Poisson vs NB or robust-Poisson variant | Helps decide whether GLM diagnostics need NB, quasi-Poisson, or robust SE reporting | Same as Stage 2 model | 1,385 observations | Medium to high as diagnostic | Stage 2 / validation | Medium | NB may improve variance fit but not necessarily ranking |
| Report dispersion by facility family | Dispersion likely differs by road class, link type, and urban/rural context | Stage 2 model residuals by group | Intersection sample only | High as diagnostic | Stage 2 / documentation | Low | Small groups may be unstable |
| Junction limitation documentation | Paper shows junction risk depends on turning and opposing flows not available in Open Road Risk | Existing docs plus feature inventory | Approach-level Bellevue data | High as documentation | documentation / Stage 2 | Low | Could overstate weakness if framed as invalidating the link model |
| Accident-type / manoeuvre-type exploratory summaries | Separate models reveal different mechanisms | STATS19 collision type / manoeuvre variables if available | Rear-end/angle/approach-turn models | Medium as diagnostic | Stage 2 / documentation | Medium | Sparse subtype counts can be unstable |
| Sight-distance / curvature / grade proxy diagnostics | Paper supports geometry/visibility mechanisms | OS geometry, OS Terrain 50, curvature, grade proxies | Intersection approaches | Medium as proxy diagnostics | feature engineering / validation | Medium | Proxies are not equivalent to measured sight distance |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Direct approach-turn volume features | Movement-specific turning counts are unavailable nationally | Turn-movement counts | 63 selected intersections | Low | Use junction class/proxy features or local pilot datasets | High |
| Signal phase / protected-left-turn variables | Signal phasing is not available nationally in open data | Signal phase/control records | Bellevue intersections | Low | Use OSM signal presence only as weak proxy | High |
| Direct sight-distance restriction feature | Requires field/design-plan assessment | Sight-distance survey/design data | Bellevue intersections | Low | Use curvature, grade, visibility, junction-layout proxies | Medium |
| Direct coefficient or elasticity transfer | Coefficients are from selected 1990s Bellevue intersections | Comparable UK approach-level data | 1,385 observations | Low | Treat as qualitative evidence only | High |
| In-sample-only model assessment | Below current validation standards | Held-out validation | 1996 study conventions | Low | Keep Open Road Risk's grouped/spatial validation | High |
| Full junction-approach model at national scale | Requires approach segmentation, turns, signal control, opposing flows | Junction inventory and movement data | Intersection approaches | Low currently | Build a small pilot in one local area if data exists | High |

Important:

- This is a junction/approach paper, not a general road-link model paper.
- Its strongest value is methodological: NB overdispersion handling, accident-type separation, and junction-feature limitations.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Indirectly. It shows traffic volumes strongly predict accident frequency, but it uses volumes as covariates rather than an exposure offset.
- Does it suggest better handling of AADT/AADF uncertainty? No. It uses estimated daily traffic counts from city data but does not model traffic-count uncertainty.
- Does it suggest useful geometry or road-context features? Yes. Sight-distance restriction, horizontal curvature, grade >5%, lane configuration, speed limit, traffic control, and road class are relevant. Many are junction-specific and not nationally available.
- Does it suggest better modelling of junctions? Yes conceptually. It shows that approach-level turning movements, opposing volumes, and signal control matter. Direct implementation is limited by data availability.
- Does it suggest better treatment of severity? No. It models accident type/mechanism, not severity.
- Does it suggest better validation design? Not by modern standards. It offers useful specification checks, but no out-of-sample validation.
- Does it expose a weakness in my current approach? Yes: a link-level model without turning movements or opposing approach volumes will struggle to represent junction-conflict exposure. This should be documented rather than patched with unsupported proxies.

## 15. Repo Actionability

1. Suggested repo action: Run an NB overdispersion diagnostic against the current Stage 2 Poisson GLM, using the same outcome, offset, and covariates where possible.
   - Action type: diagnostic
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: The paper uses NB because accident-frequency data are overdispersed and Poisson can bias coefficients/standard errors.
   - Evidence quote or page reference: Pages 106–107 and Table 1.
   - Effort: low to medium
   - Risk if implemented badly: Fitting NB at full 21.7M-row scale may be slow; start with stratified or facility-family samples.

2. Suggested repo action: Add a documentation note on junction/approach limitation: movement-specific turning volumes and opposing approach volumes are important but unavailable nationally.
   - Action type: documentation note
   - Relevant stage: documentation / Stage 2
   - Why the paper supports it: Table 2 shows high elasticities for total opposing approach volume and left-turn volume.
   - Evidence quote or page reference: Table 2, page 108.
   - Effort: low
   - Risk if implemented badly: Could imply the whole link model is invalid; frame it as a known limitation for junction-specific interpretation.

3. Suggested repo action: Add accident-type / manoeuvre-type exploratory summaries if STATS19 fields support it, but keep them diagnostic.
   - Action type: diagnostic
   - Relevant stage: Stage 2 / documentation
   - Why the paper supports it: The paper estimates separate rear-end, angle, and approach-turn models and argues they reveal different mechanisms.
   - Evidence quote or page reference: Page 107 and Tables 3–5.
   - Effort: medium
   - Risk if implemented badly: Sparse subtype counts may produce unstable apparent patterns.

4. Suggested repo action: Test grade and curvature as proxy diagnostics for visibility/sight-distance mechanisms, not as direct measured sight-distance features.
   - Action type: diagnostic / candidate feature
   - Relevant stage: feature engineering / validation
   - Why the paper supports it: Sight-distance restrictions and geometry-related features are associated with accident frequency, but direct sight distance requires field/design data.
   - Evidence quote or page reference: Page 109 sight-distance discussion; Tables 1, 3, 4, and 5.
   - Effort: medium
   - Risk if implemented badly: Curvature/grade are imperfect proxies and should not be labelled as measured sight distance.

5. Suggested repo action: Add a validation note that in-sample likelihood indices such as `rho²` should not be compared with Open Road Risk's grouped/spatial validation metrics.
   - Action type: documentation note
   - Relevant stage: validation / documentation
   - Why the paper supports it: The paper reports in-sample likelihood metrics and no held-out validation.
   - Evidence quote or page reference: Tables 1, 3, 4, 5 and page 112.
   - Effort: low
   - Risk if implemented badly: Could sound like dismissing the paper; present it as a scope/era limitation.

## 16. Query Tags

- negative-binomial
- overdispersion
- Poisson-comparison
- count-model
- accident-frequency
- intersection-approach
- junction-risk
- annual-counts
- exposure-as-covariate
- no-exposure-offset
- turn-volume
- opposing-volume
- left-turn
- rear-end
- angle-crashes
- approach-turn
- sight-distance
- lane-configuration
- signal-control
- signal-phasing
- protected-left-turn
- speed-limit
- horizontal-curvature
- grade
- selected-sample
- in-sample-diagnostic
- likelihood-ratio-test

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: DOI/URL; train/test split; external validation; spatial holdout; temporal holdout; exact severity composition; exact zero rate; full details for every accident-type model coefficient in the extracted text.
- Parts of the paper that need manual checking: Exact table values for accident-type-specific predictors in Tables 3–5, because PDF parsing/OCR is imperfect. The total model values in Tables 1–2 are clearer.
- Any likely ambiguity or risk of misinterpretation: The sample is selected from operationally deficient intersections, not a representative intersection population. `rho²` is in-sample fit, not predictive accuracy. Traffic-volume elasticities are case-study associations, not causal estimates. The paper supports NB diagnostics and junction limitation documentation more than direct Open Road Risk production changes.
