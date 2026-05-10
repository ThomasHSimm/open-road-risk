# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: 1-s2.0-S0022437515000833-main.pdf
- Suggested Markdown filename: paper-extraction-michalaki-2015-motorway-accident-severity.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The full parsed text was available. The paper is about accident severity after a crash has occurred, not crash-frequency or exposure-adjusted collision risk.

## 1. Citation

- Title: Exploring the factors affecting motorway accident severity in England using the generalised ordered logistic regression model
- Authors: Paraskevi Michalaki; Mohammed A. Quddus; David Pitfield; Andrew Huetson
- Year: 2015
- DOI or URL, if present: http://dx.doi.org/10.1016/j.jsr.2015.09.004
- Country / region studied: England
- Study setting: motorway

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper estimates factors associated with the severity of motorway accidents in England, comparing hard-shoulder accidents with main-carriageway accidents.
- Main purpose: severity modelling / explanatory analysis / road-safety countermeasure targeting
- Evidence quote or page reference: Page 89 states that the paper applies a generalized ordered logistic regression model to identify factors affecting the severity of hard-shoulder and main-carriageway accidents on motorways.

## 3. Response Variable

- Target variable: Accident severity.
- Collision type: Police-reported personal-injury motorway accidents; damage-only collisions are not included.
- Severity handling: Three ordered severity categories: slight injury, serious injury, fatal.
- Count, binary, rate, risk score, severity class, or other: Ordinal severity class.
- Time window used for outcomes: Final modelling uses 2005–2011 accidents; descriptive motorway data are also mentioned for 1985–2011.
- Evidence quote or page reference: Page 91 defines accident severity as slight, serious, and fatal. Page 92 states that the modelling data used for both models are from 2005 to 2011 and gives frequencies by severity.

## 4. Exposure Handling

- Exposure variable used, if any: No formal exposure variable. Traffic is represented indirectly using accident time categories: morning peak, afternoon peak, normal traffic, and non-peak.
- Traffic count source: Not used directly. Historical traffic patterns are used to define broad time-of-day traffic categories.
- Whether exposure is modelled, observed, assumed, or ignored: Exposure is not directly modelled. Traffic conditions are proxied by time-of-day categories.
- Treatment of missing or sparse traffic counts: Not stated
- Whether offset terms, rates, denominators, or normalisation are used: No offset, denominator, rate, or exposure normalisation is used.
- Evidence quote or page reference: Page 94 states that no detailed traffic data were available and that traffic was incorporated by creating four variables according to accident hour. Page 96 identifies indirect traffic incorporation as a limitation.
- Transferability to my AADF/WebTRIS setup: low / mixed
- Notes: The severity-model structure is partly transferable for severity diagnostics, but the paper’s exposure handling is weak for Open Road Risk. It does not support using time-of-day proxy variables as a substitute for AADT/WebTRIS exposure when better exposure data are available.

Important:

- Mathematical exposure structure: Low transferability; no exposure-offset or traffic denominator is used.
- Specific data source: Low transferability; traffic was proxied rather than observed.
- Transferable part: The distinction between crash occurrence modelling and crash severity modelling is useful.

## 5. Spatial Unit of Analysis

- Unit: Accident.
- Segment length or segmentation rule: Not stated
- How crashes are assigned to the network: Motorway accidents are extracted from STATS19 and divided into main carriageway and hard shoulder based on the location of the first impact.
- Treatment of junctions/intersections: Not stated
- Spatial aggregation risks: County-level clustering was tested for multilevel modelling, but the intra-class correlation was low and did not support multilevel models.
- Evidence quote or page reference: Page 91 states the unit of analysis is the accident and explains the hard-shoulder/main-carriageway distinction by first-impact location. Page 92 reports ICC values of 0.016 for main-carriageway accidents and 0.1 for hard-shoulder accidents.
- Relevance to OS Open Roads link-based pipeline: Low for the link-year frequency model. Medium for a future severity module because severity is modelled at accident level after occurrence, not at link-year level.

## 6. Temporal Unit of Analysis

- Years covered: 2005–2011 for final models.
- Temporal resolution: Accident-level; time represented through broad traffic/time categories and yearly trend dummy variables.
- Whether seasonality or time-of-day is modelled: Yes. Day of week, month, traffic time categories, and yearly trend dummies are included or tested.
- Whether before-after or panel structure is used: No.
- Evidence quote or page reference: Page 92 says day of week, month, speed limit, traffic, weather, surface and light conditions are dummy-coded and that trend is included as a yearly dummy variable. Page 94 discusses peak and non-peak traffic periods.
- Relevance to WebTRIS-style time profiles: Medium conceptually. The paper supports time-of-day relevance for severity, but it used crude time categories because detailed traffic data were unavailable. WebTRIS-style profiles would be a stronger exposure/context source than the paper’s proxy.

## 7. Engineered Features

List the most important engineered features, especially those I could recreate.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Hard shoulder vs main carriageway | STATS19 accident location / first impact | Split motorway accidents by location of first impact | Distinguishes two motorway safety contexts with different severity mechanisms | Medium if STATS19 location supports similar coding |
| Accident severity | STATS19 accident record | Ordinal target: slight, serious, fatal | Main response variable | High for severity diagnostics |
| Number of vehicles | STATS19 vehicle records | Count vehicles involved in accident | Associated with severity in MC model | High for accident-level severity model |
| Number of casualties | STATS19 casualty records | Count casualties per accident | Associated with severity in both models | High, but post-event and not usable for ex-ante link risk |
| Single-vehicle accident | STATS19 vehicle records | Binary flag | Significant in MC model | High for accident-level diagnostics; not ex-ante |
| HGV involvement | STATS19 vehicle records | Binary flag if at least one HGV involved | Strong severity factor, especially HS accidents | Medium; HGV proportion already candidate/present as exposure context |
| Left-hand-side drive vehicle | STATS19 vehicle records | Binary flag | Significant in MC model | Low for ex-ante link model |
| Time-of-day traffic proxy | Accident time | Morning peak, afternoon peak, normal, non-peak | Proxy for traffic/speed conditions | Medium; replace with WebTRIS-style profiles if possible |
| Speed limit category | STATS19 / road context | Dummy variables for 70, 60, 50 mph, reference 40 mph or lower | Higher speed limits increase MC severity | Medium; speed limit already candidate/present partly |
| Lighting condition | STATS19 accident record | Daylight/dark lights on/dark no lights | Better visibility reduces severity | Medium if lighting coverage improves |
| Road surface condition | STATS19 accident record | Dry vs non-dry | Dry surface associated with higher MC severity, likely via speed/driver behaviour | Accident-level diagnostic only |
| Weather condition | STATS19 accident record | Fine/fog/other | Fine and fog significant in MC model | Accident-level diagnostic only |
| Roadworks | STATS19 accident record | Binary flag | Associated with reduced severity, likely due to speed restriction/caution | Medium for roadworks-specific studies; not core long-term link risk |
| Contributory factor: fatigue | STATS19 contributory factors | Binary category created from police-recorded contributory factor | Strongly increases severity, especially HS accidents | Low for ex-ante link risk; useful as severity diagnostic |
| Contributory factor groups | STATS19 contributory factors | Recoded into driver error, behaviour, impairment, road, vehicle, distraction, pedestrian | Behavioural context for severity | Mostly post-event; avoid as Stage 2 features |
| Pedestrian involvement contributory factor | STATS19 contributory factors | Binary category | Highest coefficient among contributory factors | Useful only for severity/type diagnostics |

Only features actually used or discussed in the paper are included.

## 8. Model Architecture

- Algorithms/models used: Simple ordered logit, multilevel ordered logit, and generalized ordered logit / partial proportional odds model.
- Baseline model: Ordered logit and multilevel ordered logit were initially tested.
- Final/preferred model: Partially constrained generalized ordered logit models, estimated separately for main-carriageway and hard-shoulder accidents.
- Loss function or likelihood, if stated: Maximum likelihood estimation.
- Offset/exposure term, if used: None.
- Spatial autocorrelation handling: County-level multilevel structure was considered but rejected due to low ICC.
- Temporal dependence handling: Year dummy variables included as trend controls; no temporal autocorrelation model.
- Interpretability method: Coefficients, z-statistics, Gamma parameters for violations of the parallel regression assumption, marginal effects, observed vs predicted probabilities for selected variables.
- Evidence quote or page reference: Pages 90–91 describe ordered, multilevel ordered, and generalized ordered logit models. Page 92 reports rejection of multilevel and ordered logit assumptions, leading to generalized ordered logit. Page 93 shows model coefficients; page 94 shows marginal effects.

## 9. Reported Metrics / Quantitative Results

Extract the main quantitative results reported in the paper.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Descriptive sample | GB motorway accidents 1985–2011 | 199,388 | Motorway accidents | 2.3% fatal, 13.0% serious, 84.7% slight | Page 91 |
| Modelling sample | Main-carriageway accidents | 47,094 | 2005–2011 | 88.28% slight, 9.95% serious, 1.77% fatal | Table 1, page 92 |
| Modelling sample | Hard-shoulder accidents | 776 | 2005–2011 | 71.65% slight, 19.97% serious, 8.38% fatal | Table 1, page 92 |
| Relative severity | Hard shoulder fatal share vs main carriageway fatal share | 8.38% vs 1.77% | 2005–2011 | Fatal share about 4.7 times higher on HS | Table 1, page 92 |
| Multilevel test | ICC | 0.016 MC; 0.1 HS | County-level random intercept ordered logit | County clustering not strong enough to support multilevel model | Page 92 |
| Model choice | Brant test | Parallel regression assumption violated | Ordered logit | Generalized ordered logit preferred | Page 92 |
| Model fit | Log likelihood | -17,984.448 | Main-carriageway generalized ordered logit | In-sample likelihood | Table 2, page 93 |
| Model fit | Pseudo R-squared | 0.0708 | Main-carriageway model | In-sample fit indicator | Table 2, page 93 |
| Model fit | Log likelihood | -522.214 | Hard-shoulder generalized ordered logit | In-sample likelihood | Table 2, page 93 |
| Model fit | Pseudo R-squared | 0.1241 | Hard-shoulder model | In-sample fit indicator | Table 2, page 93 |
| Coefficient | HGV involvement | 0.3353 MC; 0.7565 HS | Beta coefficients | HGV involvement increases severity; stronger for HS | Table 2, page 93 |
| Coefficient | Driver fatigue | 0.3891 MC; 0.7928 HS | Contributory factor | Fatigue increases severity; stronger for HS | Table 2, page 93 |
| Marginal effect | Fatigue on fatal probability | +0.0054 MC; +0.0522 HS | Dummy fatigue changes 0 to 1 | Fatal probability rises by about 0.54 percentage points for MC and 5.22 percentage points for HS | Table 3, page 94; discussion page 95 |
| Marginal effect | HGV on fatal probability | +0.0099 MC; +0.0729 HS | HGV involvement | Fatal probability increase much larger for HS | Table 3, page 94 |
| Coefficient | Roadworks | -0.2917 MC; -1.2136 HS | Roadworks present | Associated with lower severity; stronger reduction for HS | Table 2, page 93 |
| Coefficient | Daylight | -0.2825 MC; -0.4982 HS | Visibility condition | Daylight associated with reduced severity | Table 2, page 93 |
| Descriptive comparison | Fatal accidents involving fatigue | 23.08% HS vs 11.63% MC | Fatal accidents | Fatigue more common in HS fatal accidents | Page 92 |
| Descriptive comparison | Fatal accidents involving HGVs | 80% HS vs 44.36% MC | Fatal accidents | HGV involvement more common in HS fatal accidents | Page 92 |

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? The reported likelihood and pseudo R-squared values are in-sample. No train/test, cross-validation, spatial holdout, temporal holdout, or external validation is reported.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They mainly test in-sample fit, model specification assumptions, coefficient significance, and marginal effects.
- Are any metrics likely to be optimistic for real-world deployment? Yes, if interpreted as predictive performance. The model explains severity among observed crashes rather than predicting crash occurrence or future risk.
- Which metric, if any, is most relevant to Open Road Risk? The hard-shoulder/main-carriageway severity contrast and the marginal effects of HGV/fatigue are useful for severity diagnostics, but not for exposure-adjusted link collision frequency.

Important:

- Do not treat pseudo R-squared as external predictive accuracy.
- Do not treat contributory-factor coefficients as ex-ante risk predictors because they are recorded after a crash and can leak crash circumstances.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Not applicable; the dataset contains only observed injury accidents, not link-years with zero collisions.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: None. Generalized ordered logit is used for severity categories.
- Whether high-risk locations are evaluated separately: Hard-shoulder and main-carriageway accidents are modelled separately; this is a roadway-location severity split, not a hotspot analysis.
- Evidence quote or page reference: Page 92 gives 776 HS accidents and 47,094 MC accidents for 2005–2011. Page 92 describes the final use of generalized ordered logit after rejecting multilevel and simple ordered logit models.
- Practical relevance to my sparse collision link-year dataset: Low for frequency modelling. It is useful only if building a separate accident-level severity model or severity weighting diagnostic.

Important:

- The paper does not address zero-heavy link-year crash counts.
- The paper does not use a zero-inflated model.

## 11. Validation Strategy

- Train/test split method: Not stated
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Not stated
- Metrics: Log likelihood, pseudo R-squared, coefficient z-statistics, marginal effects, observed vs predicted probability plots for selected variables.
- External validation: Not stated
- Leakage or generalisation risks: Contributory factors are post-crash police judgements and should not be used as ex-ante predictors in a production link-risk model. The paper also uses proxy variables for traffic flow and speed rather than actual traffic conditions.
- Evidence quote or page reference: Page 92 notes contributory factors are subjective police-recorded factors explaining why the accident occurred. Page 96 states limitations related to data integrity, subjective contributory factors, and proxy traffic/speed variables.
- What I should copy or avoid: Copy the model-selection discipline: test multilevel need, test parallel regression, use generalized ordered logit if proportional odds is violated. Avoid using contributory factors in Stage 2 risk prediction because they are post-event and would leak crash information.

Important:

- The paper is not validated for predictive deployment.
- It is better used as methodological support for accident-level severity modelling and as evidence that severity mechanisms differ by motorway location.

## 12. Key Findings Relevant to My Project

Give 3–6 findings that are directly useful for my road-risk pipeline.

### Finding 1

- Finding: Hard-shoulder motorway accidents are much more severe than main-carriageway accidents in the study data.
- Why it matters: If Open Road Risk models motorway risk, severity may vary sharply by facility/location context even within the motorway class.
- Evidence quote or page reference: Table 1 on page 92 reports 8.38% fatal for hard-shoulder accidents compared with 1.77% for main-carriageway accidents.
- Confidence: high for this dataset.

### Finding 2

- Finding: HGV involvement is associated with increased accident severity, with a stronger effect for hard-shoulder accidents.
- Why it matters: HGV exposure/proportion could be useful in severity diagnostics, not just frequency/exposure modelling.
- Evidence quote or page reference: Table 2 on page 93 reports HGV coefficients of 0.3353 for MC and 0.7565 for HS; Table 3 on page 94 reports fatal marginal effects of 0.0099 and 0.0729 respectively.
- Confidence: high

### Finding 3

- Finding: Driver fatigue is associated with higher severity, especially on the hard shoulder.
- Why it matters: Fatigue itself is not an ex-ante link feature in your open-data pipeline, but time-of-day / motorway context / HGV exposure may be relevant diagnostic proxies.
- Evidence quote or page reference: Page 95 states fatigue is much more important in the HS model, with fatal marginal effects of 0.0054 for MC and 0.0522 for HS.
- Confidence: high

### Finding 4

- Finding: The generalized ordered logit was preferred because the proportional-odds/parallel-regression assumption was violated.
- Why it matters: If you build a severity model, do not default to simple ordered logit without testing this assumption.
- Evidence quote or page reference: Page 92 states the Brant test found the ordered logit inappropriate and required a generalized ordered logit model.
- Confidence: high

### Finding 5

- Finding: County-level multilevel structure was tested but not supported by ICC in this motorway severity dataset.
- Why it matters: This is a useful reminder that hierarchical/spatial structure should be tested, not assumed.
- Evidence quote or page reference: Page 92 reports ICC values of 0.016 for MC and 0.1 for HS, judged too low to support multilevel modelling.
- Confidence: medium; the county grouping may be too coarse for spatial dependence.

### Finding 6

- Finding: Contributory-factor data are useful but subjective and post-event.
- Why it matters: In Open Road Risk, contributory factors should be treated as diagnostics or severity-analysis variables, not Stage 2 production predictors.
- Evidence quote or page reference: Page 92 explains that contributory factors depend on the investigating officer’s judgement; page 96 lists this as a data-integrity limitation.
- Confidence: high

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Accident-level severity model | Separates severity mechanisms from frequency risk | STATS19 accident/casualty/vehicle records | 47,094 MC and 776 HS accidents, 2005–2011 | Medium for observed crashes; not link-year production | future feature / validation | medium | Confusing severity conditional on crash with crash risk |
| Generalized ordered logit / partial proportional odds | Handles ordinal severity when parallel regression fails | Severity categories and predictors | National motorway accidents in England | Medium | future severity model | medium | Requires careful interpretation of multiple thresholds |
| Hard-shoulder / carriageway split | Captures motorway-specific severity context | Accident location / first impact fields | England motorways | Medium if location coding available | diagnostic / future feature | low to medium | Not relevant to non-motorway links |
| HGV severity diagnostic | Tests whether HGV involvement/proportion relates to severity | Vehicle type and/or HGV exposure | England motorways | Medium; HGV proportion already candidate/present | validation / future severity | low to medium | HGV involvement is post-crash; HGV proportion is not equivalent |
| Time-of-day severity diagnostic | Checks severity differences by traffic/time bands | Accident time and WebTRIS-style profiles | England motorways | Medium | Stage 1b / future severity | medium | Time proxy may confound speed, fatigue, darkness, and traffic |
| Model assumption tests for severity | Brant test, ICC/multilevel checks | Severity model data | England motorways | High for severity modelling | validation | low to medium | Tests may be sensitive to scale and grouping |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Use contributory factors as Stage 2 predictors | They are post-crash police judgements and would leak event information | Ex-ante availability absent | Accident-level | Low for production risk | Use only diagnostics or separate severity analysis | high |
| Use casualties count as predictor for prospective severity/risk | Number of casualties is outcome-related and post-event | Not known before crash | Accident-level | Low for ex-ante model | Use for descriptive severity only | high |
| Direct transfer of hard-shoulder findings to all roads | Study is motorway-specific and hard shoulder/main carriageway-specific | Facility context differs | England motorways | Low for local roads | Treat as motorway-only evidence | high |
| Replace exposure-adjusted collision model with severity logit | Severity model conditions on a crash having occurred | Does not model collision frequency or exposure | Accident-level | Low | Keep as separate severity layer | high |
| Use traffic peak proxy instead of AADT/WebTRIS | Proxy used because detailed traffic data were unavailable | Detailed traffic data absent in paper | Accident-level | Low as a best practice | Use WebTRIS/AADT where possible | high |

Important:

- The severity model is conceptually useful but should remain separate from the frequency/exposure model.
- Several strong predictors in the paper are post-event and must not enter production risk prediction.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? No. It models injury severity conditional on an accident and does not use exposure offsets.
- Does it suggest better handling of AADT/AADF uncertainty? No. It explicitly lacked detailed traffic data and used broad time proxies.
- Does it suggest useful geometry or road-context features? Indirectly. It highlights motorway context, hard shoulder/main carriageway, speed limit, roadworks, lighting, weather, and surface conditions; however, it does not model OS link geometry.
- Does it suggest better modelling of junctions? No.
- Does it suggest better treatment of severity? Yes. It supports treating severity as an ordinal outcome and testing whether generalized ordered logit is needed rather than using a simple severity weighting.
- Does it suggest better validation design? Only for severity model specification: test ICC/multilevel need and proportional-odds assumptions. It does not provide held-out validation.
- Does it expose a weakness in my current approach? Yes, if your production risk percentile combines or ignores severity without a separate severity layer. Frequency and severity mechanisms may differ, especially for motorway/HGV/fatigue contexts.

## 15. Repo Actionability

Give up to 5 concrete implications for my repo.

### Action 1

- Suggested repo action: Add a documentation note separating crash-frequency risk from conditional severity modelling.
- Action type: documentation note
- Relevant stage: documentation / Stage 2
- Why the paper supports it: The paper models accident severity after a crash occurs, not crash occurrence or exposure-adjusted frequency.
- Evidence quote or page reference: Page 91 states the unit of analysis is the accident and the dependent variable is severity.
- Effort: low
- Risk if implemented badly: Users may confuse “high severity if crash occurs” with “high crash risk.”

### Action 2

- Suggested repo action: Add a severity-analysis TODO: test ordered logit versus generalized ordered logit if building an accident-level severity module.
- Action type: diagnostic / small pilot
- Relevant stage: future feature / validation
- Why the paper supports it: The Brant test rejected the parallel regression assumption, so generalized ordered logit was used.
- Evidence quote or page reference: Page 92 explains that ordered logit was inappropriate because the parallel regression assumption was violated.
- Effort: medium
- Risk if implemented badly: Misinterpreting threshold-specific coefficients or treating ordinal classes as linear.

### Action 3

- Suggested repo action: Keep STATS19 contributory factors out of Stage 2 production predictors; use them only for diagnostics/literature comparison.
- Action type: documentation note / diagnostic
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Contributory factors are subjective police judgements about why the crash occurred.
- Evidence quote or page reference: Page 92 says contributory factors depend on the officer’s skill and experience and should be based on evidence rather than guesswork.
- Effort: low
- Risk if implemented badly: Post-event leakage would make the model look stronger than it is.

### Action 4

- Suggested repo action: Add an HGV/severity diagnostic comparing observed severity distribution by HGV involvement and, separately, by modelled HGV proportion where available.
- Action type: diagnostic
- Relevant stage: validation / future severity
- Why the paper supports it: HGV involvement is a stronger severity factor for hard-shoulder accidents than main-carriageway accidents.
- Evidence quote or page reference: Table 2 on page 93 and Table 3 on page 94 show larger HGV coefficients and fatal marginal effects for HS.
- Effort: low to medium
- Risk if implemented badly: HGV involvement in a crash is not the same as HGV exposure on a link.

### Action 5

- Suggested repo action: For motorway-only analysis, consider a diagnostic split for carriageway/hard-shoulder or equivalent location context if STATS19 coding and OS mapping support it.
- Action type: diagnostic / small pilot
- Relevant stage: future feature / validation
- Why the paper supports it: HS accidents had substantially higher fatal and serious shares and different significant predictors.
- Evidence quote or page reference: Table 1 on page 92 shows HS accidents have 8.38% fatal and 19.97% serious compared with 1.77% fatal and 9.95% serious for MC.
- Effort: medium
- Risk if implemented badly: Location coding may not transfer cleanly to OS Open Roads links or non-motorway contexts.

Important:

- Do not recommend a production change from this paper alone.
- The most useful actions are severity documentation and diagnostics.

## 16. Query Tags

- accident-severity
- motorway
- England
- STATS19
- hard-shoulder
- main-carriageway
- generalized-ordered-logit
- partial-proportional-odds
- Brant-test
- ordinal-severity
- HGV
- fatigue
- contributory-factors
- post-event-leakage
- speed-limit
- roadworks
- lighting
- traffic-time-proxy
- severity-diagnostic
- not-frequency-model

Important:

- No `zero-inflation` tag is used because the paper does not fit a zero-inflated model.

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: Held-out predictive performance, spatial holdout, temporal holdout, cross-validation, direct traffic flow/speed data, and direct exposure measures.
- Parts of the paper that need manual checking: Exact interpretation of some Gamma/threshold coefficients if used in a statistical-methods note; exact STATS19 coding for hard-shoulder/main-carriageway transfer to the current project.
- Any likely ambiguity or risk of misinterpretation: The largest risk is using post-event variables such as contributory factors, number of casualties, or crash-involved HGV flags as if they were pre-crash predictors for link risk. This paper is valuable for conditional severity modelling, not for prospective exposure-adjusted collision-frequency modelling.
