# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Negative_Binomial_Analysis_of_Intersection-Acciden.pdf
- Suggested Markdown filename: paper-extraction-poch-1996-intersection-negative-binomial.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The PDF text and page images were accessible. Some OCR/parsing artefacts appear in equations and tables, so key numerical values should be checked against the original PDF if used in formal reporting.

## 1. Citation

- Title: Negative Binomial Analysis of Intersection-Accident Frequencies
- Authors: Mark Poch; Fred Mannering
- Year: 1996
- DOI or URL, if present: Not stated
- Country / region studied: United States / Bellevue, Washington
- Study setting: urban / suburban intersections

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper estimates negative binomial regression models for annual accident frequency at urban/suburban intersection approaches, including total accidents and specific accident types.
- Main purpose: safety performance function / descriptive-explanatory modelling / exploratory accident prediction
- Evidence quote or page reference: Page 105 states that the paper “estimates a negative binomial regression of the frequency of accidents at intersection approaches” using seven-year histories from 63 intersections in Bellevue, Washington.

## 3. Response Variable

- Target variable: Annual accident frequency on an individual intersection approach.
- Collision type: all reported accidents, plus separate models for rear-end, angle, and approach-turn accidents.
- Severity handling: Severity is not modelled separately; the paper models accident frequency by accident type.
- Count, binary, rate, risk score, severity class, or other: Count.
- Time window used for outcomes: One-year intervals over 1987–1993, excluding the year in which an operational improvement occurred.
- Evidence quote or page reference: Page 106 states that four models predict total accident frequency, rear-end accident frequency, angle accident frequency, and approach-turn accident frequency, and that “the dependent variable (annual accident frequency) will be a non-negative integer.” Page 107 describes annual accident data by approach and the study period.

## 4. Exposure Handling

- Exposure variable used, if any: Traffic volumes are included as explanatory variables, including approach left-turn volume, right-turn volume, total opposing approach volume, total intersection volume, opposing left-turn volume, and related traffic measures depending on model.
- Traffic count source: City of Bellevue approach-level traffic counts expanded from morning peak, afternoon peak, and midday volumes into daily counts using standard expansion formulae and Bellevue yearly factors.
- Whether exposure is modelled, observed, assumed, or ignored: Traffic exposure is observed/estimated as explanatory variables; it is not used as a formal offset.
- Treatment of missing or sparse traffic counts: Missing annual traffic values were converted from known counts of a different year using city yearly factors for different growth-rate areas.
- Whether offset terms, rates, denominators, or normalisation are used: No offset, denominator, or explicit accident-rate normalisation is reported. The model uses log-linear expected counts with traffic variables as covariates.
- Evidence quote or page reference: Page 107 explains that traffic volumes were gathered for available years and expanded to daily counts; missing-year traffic counts used Bellevue yearly factors. Page 108 reports elasticities for traffic variables rather than an exposure offset.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The idea of using movement-specific flows is conceptually useful, especially at junctions, but the paper’s approach-level turning volumes are not generally available in Open Road Risk. The mathematical structure is less transferable to your Stage 2 model because it uses traffic variables as covariates, not an exposure offset.

Important:

- Mathematical exposure structure: Medium transferability as a count model with traffic-volume covariates; low transferability as an exposure-offset design because the paper does not use one.
- Specific traffic data source: Low transferability nationally, because detailed approach and turning volumes are not generally available in your open-data pipeline.

## 5. Spatial Unit of Analysis

- Unit: Intersection approach.
- Segment length or segmentation rule: Each intersection was divided into separate approaches; a four-leg intersection could produce northbound, southbound, eastbound, and westbound approach observations.
- How crashes are assigned to the network: Accidents were taken at each approach in one-year intervals. If the accident occurred in the intersection proper, it was assigned to the approach of the “at-fault” vehicle.
- Treatment of junctions/intersections: Intersections are the core unit, with approach-level geometry, traffic control, turning movements, sight distance, and lane configuration.
- Spatial aggregation risks: Repeated observations from the same intersection and multiple approaches from the same intersection could create correlated errors; the paper tests this using likelihood-ratio tests on segmented subsets.
- Evidence quote or page reference: Page 106 defines intersection approaches; page 107 describes assigning crashes in the intersection proper to the at-fault vehicle’s approach and notes possible correlation from repeated observations.
- Relevance to OS Open Roads link-based pipeline: High as a warning that junction/approach risk is structurally different from ordinary road-link risk. Direct implementation is limited because OS Open Roads link geometry does not naturally encode turning movements, signal phase, approach alignment, or approach-specific volumes.

## 6. Temporal Unit of Analysis

- Years covered: 1987–1993.
- Temporal resolution: Yearly.
- Whether seasonality or time-of-day is modelled: No; time-of-day traffic counts are used only to estimate daily counts.
- Whether before-after or panel structure is used: Repeated annual observations are used. Intersections targeted for operational improvements are included, and the operational-improvement year is excluded; however, the paper does not present a formal before-after treatment-effect design.
- Evidence quote or page reference: Page 107 states that accident data were taken in one-year intervals and gives an example of a four-approach intersection contributing observations for 1987, 1988, 1990, 1991, 1992, and 1993 if improved in 1989.
- Relevance to WebTRIS-style time profiles: Low to medium. The paper supports the importance of turning and approach volumes, but does not model hourly or peak/off-peak collision risk.

## 7. Engineered Features

List the most important engineered features, especially those I could recreate.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Approach left-turn volume | Bellevue traffic counts | Peak/midday counts expanded to daily traffic; modelled in thousands | Strong positive association with total, angle, and approach-turn accidents | Low directly; possible only with turning-count data |
| Approach right-turn volume | Bellevue traffic counts | Daily traffic estimate in thousands | Associated with total and rear-end accidents | Low directly; candidate only for local junction datasets |
| Total opposing approach volume | Bellevue traffic counts | Daily opposing approach volume in thousands | Represents conflict exposure for turning movements | Low directly; conceptually useful for junction diagnostics |
| Opposing left-turn volume | Bellevue traffic counts | Daily opposing left-turn volume in thousands | Used in rear-end and approach-turn models | Low directly |
| Number of approach / opposing / through lanes | Intersection design plans | Count of lanes by approach/opposing direction and lane type | Captures conflict exposure and crossing distance | Medium if lanes coverage improves; OSM lanes are sparse |
| Combined through-left lane / left-turn drop lane indicators | Intersection design plans | Binary indicators for lane configurations | Identifies configurations with rear-end and turning-conflict risk | Low to medium; may require manual or detailed mapping |
| Signal control | Traffic control inventory | Binary signal-control indicator | Signalisation associated with lower total/angle accidents in this selected sample | Low nationally; possible from OSM/signals but incomplete |
| Two-phase / eight-phase signal | Signal-control data | Binary signal-phase indicators | Captures permissive/protected turning and complex high-volume junctions | Low; signal phasing not available nationally |
| Protected / permissive left turn | Signal-control data | Binary movement-control indicators | Directly relates to left-turn conflict handling | Low |
| Sight-distance restriction | Field/design data | Binary indicator based on fixed objects, curvature, vegetation, or misaligned left-turn lanes | Strongly associated with accident frequency | Low directly; possible proxy via curvature/visibility diagnostics only |
| Speed limit | Road data | Approach and opposing approach speed limits | Higher approach speed generally increases accident frequency | Medium; OSM speed limit already partly present / compare implementation |
| Horizontal curve on approach/opposing approach | Road geometry/design plans | Binary curve indicators | Used in total/angle/approach-turn models | Medium; curvature already candidate/present / compare implementation |
| Greater than 5% uphill/downhill grade | Road geometry/design plans | Binary grade threshold | Associated with rear-end and angle accidents | Medium; grade from OS Terrain 50 is candidate / compare implementation |
| Local street / all approaches local streets | Road classification | Binary street-class indicators | Low-volume/local context associated with fewer accidents | Medium; road classification already present / compare implementation |
| CBD indicator | City location/context | Binary central business district indicator | Used as proxy for signal progression/context in rear-end model | Low directly; urban-centre proxies possible |

Only features actually used in the paper are included.

## 8. Model Architecture

- Algorithms/models used: Negative binomial regression; Poisson regression discussed as starting point; ordinary least squares used only for an informal functional-form check.
- Baseline model: Poisson regression is presented as the natural first model for non-negative count data but rejected when overdispersion is significant.
- Final/preferred model: Negative binomial regression for total, rear-end, angle, and approach-turn accident frequencies.
- Loss function or likelihood, if stated: Standard maximum likelihood estimation of the negative binomial model.
- Offset/exposure term, if used: No offset stated.
- Spatial autocorrelation handling: Not modelled directly; possible correlation across approaches from the same intersection is tested with likelihood-ratio tests on directional subsets.
- Temporal dependence handling: Not modelled directly; possible year-to-year correlation is tested with likelihood-ratio tests on year subsets.
- Interpretability method: Coefficients, t-statistics, elasticities for continuous variables, likelihood-ratio index `rho²`, and likelihood-ratio tests for specification concerns.
- Evidence quote or page reference: Pages 106–107 derive the Poisson and negative binomial formulations. Page 108 defines elasticity. Page 112 presents likelihood-ratio subset tests for correlation across approaches and years.

## 9. Reported Metrics / Quantitative Results

Extract the main quantitative results reported in the paper.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Sample size | Intersections | 63 | Bellevue targeted intersections | Non-random selected sample of operationally deficient intersections | Page 107 |
| Sample size | Observations | 1,385 | Intersection approach-year observations | Approach-level annual panel-like dataset | Page 107; Table 1 |
| Accident mix | Rear-end / angle / approach-turn / other | 26% / 30% / 32% / 12% | 1987–1993 recorded accidents | Supports separate accident-type models | Page 107 |
| Model fit | Log-likelihood at zero | -2,123.11 | Total accident model | Null model log-likelihood | Table 1, page 108 |
| Model fit | Log-likelihood at convergence | -1,698.26 | Total accident model | Fitted model log-likelihood | Table 1, page 108 |
| Model fit | `rho²` | 0.200 | Total accident model | Likelihood-ratio index; in-sample model fit | Table 1, page 108 |
| Dispersion | Negative binomial `alpha` | 0.346, t = 5.96 | Total accident model | Significant overdispersion; supports NB over Poisson | Table 1, page 108; discussion page 110 |
| Elasticity | Left-turn volume | 2.28 | Total accident model | 1% increase in left-turn volume associated with about 2.28% increase in total accidents | Table 2, page 108 |
| Elasticity | Right-turn volume | 0.92 | Total accident model | 1% increase in right-turn volume associated with about 0.92% increase in total accidents | Table 2, page 108 |
| Elasticity | Total opposing approach volume | 2.95 | Total accident model | Strong positive association with total accident frequency | Table 2, page 108 |
| Elasticity | Approach speed limit | 0.98 | Total accident model | Positive association with total accidents | Table 2, page 108 |
| Elasticity | Opposing approach speed limit | -0.34 | Total accident model | Negative coefficient likely due to interaction/correlation with approach speed limit | Table 2 and discussion, pages 108–110 |
| Model fit | `rho²` | 0.505 | Rear-end model | In-sample likelihood-ratio index | Table 3, page 110 |
| Model fit | `rho²` | 0.458 | Angle model | In-sample likelihood-ratio index | Table 4, page 110 |
| Model fit | `rho²` | 0.537 | Approach-turn model | In-sample likelihood-ratio index | Table 5, page 111 |
| Dispersion | Negative binomial `alpha` | 0.319, t = 2.26 | Rear-end model | Significant/positive dispersion estimate; supports NB model | Table 3, page 110 |
| Dispersion | Negative binomial `alpha` | 0.696, t = 3.61 | Angle model | Significant/positive dispersion estimate; supports NB model | Table 4, page 110 |
| Dispersion | Negative binomial `alpha` | 0.505, t = 3.74 | Approach-turn model | Significant/positive dispersion estimate; supports NB model | Table 5, page 111 |
| Specification test | Likelihood-ratio test by approach direction | Chi-square = 47.2; df = 54; p = 0.732 | Total accident model | No strong evidence that approach-direction subset coefficients differ from full-sample coefficients | Page 112 |
| Specification test | Likelihood-ratio test by year subset | Chi-square = 74.24; df = 90; p = 0.885 | Total accident model | No strong evidence that year-subset coefficients differ from full-sample coefficients | Page 112 |
| Functional-form check | OLS `R²` log-linear vs linear | 0.2186 vs 0.2129 | Informal check excluding zero-accident observations | Little difference between linear and log-linear OLS forms; not a validation of NB prediction | Page 112 |

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? The reported model-fit metrics are in-sample. The subset likelihood-ratio tests examine specification/correlation concerns, not predictive generalisation. No out-of-sample, spatial holdout, temporal holdout, cross-validation, or external validation is reported.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They mainly test in-sample model fit, overdispersion, coefficient significance, elasticity, and whether subset-specific models differ from full-sample estimates.
- Are any metrics likely to be optimistic for real-world deployment? Yes. The data are a selected sample of operationally deficient intersections, and all model-fit metrics are in-sample. They should not be treated as deployment accuracy.
- Which metric, if any, is most relevant to Open Road Risk? The most relevant metrics are the significant negative binomial dispersion estimates and the approach/year subset tests as examples of overdispersion and repeated-observation checks. The elasticities are useful as case-study evidence for junction feature importance, not as transferable effect sizes.

Important:

- The paper does not report cross-validated or external predictive accuracy.
- `rho²` is an in-sample likelihood-ratio index, not a predictive generalisation metric.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The paper uses negative binomial count models to handle overdispersed non-negative accident counts. It does not focus on excess-zero modelling.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Negative binomial regression. Poisson regression is discussed and rejected where overdispersion is significant.
- Whether high-risk locations are evaluated separately: The sample is explicitly drawn from intersections targeted for operational improvements, so it over-represents problematic/operationally deficient intersections rather than all intersections.
- Evidence quote or page reference: Page 106 states the negative binomial relaxes the Poisson mean-variance equality. Page 107 notes Bellevue’s interest in problematic intersections and that the selective nature of the sample must be kept in mind.
- Practical relevance to my sparse collision link-year dataset: Medium. It supports count models for crash-frequency data and overdispersion checks, but its sample has relatively accident-prone intersections and does not address extremely sparse national link-year data.

Important:

- The paper does not use a zero-inflated model.
- The data may be less zero-heavy than Open Road Risk because the sampled intersections were selected for operational deficiencies/high accident potential.

## 11. Validation Strategy

- Train/test split method: Not stated
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Not stated
- Metrics: In-sample likelihood, coefficient t-statistics, dispersion significance, elasticities, `rho²`, likelihood-ratio subset tests.
- External validation: Not stated
- Leakage or generalisation risks: The main generalisation risk is sample selection: the intersections were targeted for operational improvements, so the model may not transfer to a random or national population of intersections. Repeated approaches and repeated years may create correlated errors; the paper tests but does not model these directly.
- Evidence quote or page reference: Page 107 warns that the selective nature of the sample must be kept in mind. Page 112 reports likelihood-ratio tests for possible correlation from approaches and years.
- What I should copy or avoid: Copy the habit of testing repeated-observation correlation and reporting overdispersion. Avoid treating selected high-risk intersections as representative of all roads or junctions.

Important:

- The paper’s likelihood-ratio subset tests are specification checks, not validation of predictive deployment.
- The paper does not provide spatial or temporal holdout evidence.

## 12. Key Findings Relevant to My Project

Give 3–6 findings that are directly useful for my road-risk pipeline.

### Finding 1

- Finding: Negative binomial models were preferred over Poisson models because accident-frequency data were overdispersed.
- Why it matters: This supports checking overdispersion and considering NB-style alternatives or diagnostics for sparse crash counts, even if your current GLM uses Poisson with an exposure offset.
- Evidence quote or page reference: Page 110 states that the significant dispersion parameter justifies the negative binomial model and that Poisson would have produced considerable bias.
- Confidence: high

### Finding 2

- Finding: Junction approach risk depends strongly on turning volumes and opposing approach volume.
- Why it matters: Your OS Open Roads link model may miss important junction-conflict mechanisms if it only uses link-level exposure and road-class features.
- Evidence quote or page reference: Table 2 on page 108 reports elasticities of 2.28 for left-turn volume and 2.95 for total opposing approach volume in the total accident model.
- Confidence: high for this case study; medium for transfer to your pipeline because turning volumes are not available nationally.

### Finding 3

- Finding: Accident-type-specific models can reveal different relationships from an all-accident model.
- Why it matters: This supports using type/severity diagnostics rather than assuming one total-collision model explains every mechanism.
- Evidence quote or page reference: Page 107 states that separate rear-end, angle, and approach-turn models may uncover insights not visible in total accident frequency; Tables 3–6 report different predictors by accident type.
- Confidence: high

### Finding 4

- Finding: Some apparently counterintuitive coefficients may reflect omitted variables or proxy effects rather than direct causal effects.
- Why it matters: This is directly relevant to your caution around causal interpretation and feature leakage/proxy variables.
- Evidence quote or page reference: Page 109 discusses eight-phase signals being associated with higher accident frequencies because they proxy high-volume, congested, complex intersections, and warns that omitting the variable could cause omitted-variable bias.
- Confidence: high

### Finding 5

- Finding: Repeated approach/year observations can create possible correlation, and the paper uses subset likelihood-ratio tests as a diagnostic.
- Why it matters: Your link-year structure has repeated observations per link and should continue using grouped splits and repeated-unit diagnostics.
- Evidence quote or page reference: Page 112 discusses possible nonindependence from approaches and years and reports likelihood-ratio tests.
- Confidence: medium

### Finding 6

- Finding: Sight-distance restrictions, lane configurations, speed, grade, and curvature appear relevant for intersection/approach accident frequency in this selected sample.
- Why it matters: These support diagnostics or future features around junction geometry, visibility proxies, curvature, grade, and lane configuration, but not immediate production changes.
- Evidence quote or page reference: Tables 1, 3, 4, 5, and summary Table 6 list these variables across models.
- Confidence: medium because the sample is selected and not externally validated.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Overdispersion diagnostic / NB comparison | Tests whether Poisson count assumptions are too restrictive | Link-year collision counts, exposure offset, features | 1,385 approach-year observations | High conceptually; computationally feasible | Stage 2 / validation / baseline comparison | medium | NB may improve fit but not ranking or external validation |
| Accident-type-specific diagnostics | Different mechanisms may drive rear-end, angle, and turning crashes | STATS19 collision type or manoeuvre fields if available | 63 intersections, 1987–1993 | Medium; depends on reliable collision-type coding | Stage 2 / documentation / diagnostic | medium | Fragmenting already sparse data can destabilise estimates |
| Junction/approach-risk documentation note | Link-level models may miss approach-level conflict mechanisms | Existing model description plus literature evidence | Intersection approaches | High for documentation | documentation | low | Overclaiming without available turning-volume data |
| Curvature and grade diagnostic at junctions | Paper supports geometry relevance around intersections | OS Open Roads geometry, OS Terrain 50 grade, junction flags | Selected intersections | Medium | feature engineering / diagnostic | medium | DEM grade and link curvature may be noisy near complex junctions |
| Repeated-unit correlation checks | Mirrors link-year repeated observations | Link IDs, years, model residuals | Approach/year repeated data | High | validation | medium | Confusing specification checks with held-out validation |
| Facility/context split models | Paper models accident types and approach contexts separately | Road class, junction/ramp flags, urban/rural context | Intersection approaches | Medium | baseline comparison / diagnostic | medium | Smaller subsets may reduce stability |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Approach turning-volume covariates nationally | Open Road Risk lacks approach-level left/right-turn counts | Turning movement counts for every junction/approach | 63 intersections | Low | Use junction class, road hierarchy, turn-angle, or conflict proxies | high |
| Signal-phase variables | Two-phase/eight-phase/protected/permissive left-turn data are not open nationally | Signal phasing and movement control | Selected city intersections | Low | Use OSM traffic signals as weak proxy; document limitations | high |
| Sight-distance restriction indicator | Requires field/design assessment of visibility restrictions | Detailed sightline audits, vegetation/fixed object inventory | Intersection approaches | Low | Use curvature, grade, junction angle, road width proxies | high |
| Direct effect-size transfer | Coefficients/elasticities are from selected Bellevue intersections | Representative sample and compatible network/data | 1,385 approach-year observations | Low | Use findings as qualitative support only | high |
| Production model change from this paper alone | No external validation and selected sample | Generalisable validation evidence | Single city case study | Low | Use as diagnostic or baseline-comparison motivation | high |

Important:

- The most transferable part is methodological: count modelling, overdispersion, accident-type stratification, and repeated-observation diagnostics.
- The most useful substantive lesson is that junction conflicts need their own representation.
- The least transferable part is detailed approach-level traffic and signal-control data.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Partly. It supports using traffic volume as central to accident-frequency modelling, but it does not use an exposure offset or rate denominator. It does not directly support your exact exposure-offset structure.
- Does it suggest better handling of AADT/AADF uncertainty? Not directly. It does show that missing traffic counts were estimated using yearly expansion factors, but it does not model uncertainty in those estimates.
- Does it suggest useful geometry or road-context features? Yes. It supports diagnostics around lanes, approach/opposing approach structure, sight distance, speed, horizontal curvature, grade, local-street classification, and signal/control context.
- Does it suggest better modelling of junctions? Yes. This is the strongest implication. Junction approach accidents have mechanisms that ordinary link-level models may miss, especially turning conflicts and opposing approach volumes.
- Does it suggest better treatment of severity? No. It treats accident types, not injury severity.
- Does it suggest better validation design? It suggests useful specification checks for repeated approaches/years, but not modern held-out validation. It does not replace grouped, spatial, or temporal validation.
- Does it expose a weakness in my current approach? Yes: a link-based OS Open Roads model probably under-represents junction approach mechanics unless junction complexity/conflict proxies are explicitly engineered and documented.

## 15. Repo Actionability

Give up to 5 concrete implications for my repo.

### Action 1

- Suggested repo action: Add a documentation note that junction and approach-level mechanisms are likely under-represented in a pure link-level model.
- Action type: documentation note
- Relevant stage: documentation / Stage 2
- Why the paper supports it: The paper models accident frequency at intersection approaches and finds turning volumes, opposing volumes, lanes, sight distance, and signal/control variables important.
- Evidence quote or page reference: Page 105 states the study investigates geometric and traffic-related conditions on intersection approaches; Table 6 on page 111 summarises multiple approach-specific predictors.
- Effort: low
- Risk if implemented badly: Making it sound like the paper validates your UK model; it does not.

### Action 2

- Suggested repo action: Add a Stage 2 diagnostic comparing model residuals/risk percentiles for links near junctions versus non-junction links.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper shows intersection approaches have distinct accident-frequency mechanisms.
- Evidence quote or page reference: Page 107 argues that separate accident-type and approach models provide insights into approach conditions influencing accident frequency.
- Effort: medium
- Risk if implemented badly: Junction flags may be noisy and could conflate urban density with true junction conflict.

### Action 3

- Suggested repo action: Pilot junction-conflict proxy features rather than trying to recreate unavailable turning-volume variables directly.
- Action type: small pilot / candidate feature
- Relevant stage: feature engineering / Stage 2
- Why the paper supports it: Turning and opposing approach volumes are central in this study, but those exact data are unlikely to be available nationally.
- Evidence quote or page reference: Table 2 on page 108 reports large elasticities for left-turn volume and total opposing approach volume.
- Effort: medium to high
- Risk if implemented badly: Proxy features may be weak or misleading without careful validation.

### Action 4

- Suggested repo action: Compare Poisson GLM residual diagnostics against a negative-binomial-style baseline or overdispersion diagnostic.
- Action type: baseline comparison / diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper explicitly argues that Poisson is inappropriate when accident counts are overdispersed and uses significant dispersion estimates to justify negative binomial models.
- Evidence quote or page reference: Pages 106–107 derive the negative binomial model; page 110 states that significant `alpha` justifies NB over Poisson.
- Effort: medium
- Risk if implemented badly: Better in-sample fit may not improve external ranking; keep it as comparison, not automatic production replacement.

### Action 5

- Suggested repo action: Add accident-type or manoeuvre-type exploratory summaries where STATS19 coding supports it, but keep them diagnostic until sparsity is understood.
- Action type: diagnostic
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper estimates separate rear-end, angle, and approach-turn models and finds different predictors by type.
- Evidence quote or page reference: Page 107 motivates separate accident-type models; Tables 3–6 show accident-type-specific results.
- Effort: medium
- Risk if implemented badly: Sparse subtype counts can produce unstable or overinterpreted patterns.

Important:

- No production model change is recommended directly from this single selected-sample paper.
- The strongest immediate value is documentation and diagnostics around junction limitations.

## 16. Query Tags

- negative-binomial
- intersection-approach
- accident-frequency
- overdispersion
- count-model
- Poisson-comparison
- junction-risk
- turning-volume
- opposing-volume
- rear-end
- angle-crashes
- approach-turn
- sight-distance
- signal-control
- left-turn
- lane-configuration
- speed-limit
- curvature
- grade
- repeated-observations
- likelihood-ratio-test
- in-sample-diagnostic
- selected-sample

Important:

- No `zero-inflation` tag is used because the paper does not fit a zero-inflated model.

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: DOI/URL; external validation; train/test split; spatial holdout; temporal holdout; exact severity composition; whether property-damage-only crashes are included beyond “all reported accident types.”
- Parts of the paper that need manual checking: Some table values should be checked against the PDF before being used in a formal literature table, especially because the parsed text includes OCR artefacts.
- Any likely ambiguity or risk of misinterpretation: The study sample is not representative of all intersections; it consists of intersections targeted for operational improvements. Coefficients and elasticities should be treated as case-study evidence, not general UK transfer estimates. The paper supports junction diagnostics more than direct feature or production-model adoption.
