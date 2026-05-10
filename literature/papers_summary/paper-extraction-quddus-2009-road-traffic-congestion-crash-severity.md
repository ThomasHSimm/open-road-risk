# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: road-traffic-congestion-and-crash-severity-econometric-2rrbyxf6f0.pdf
- Suggested Markdown filename: paper-extraction-quddus-2009-road-traffic-congestion-crash-severity.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The uploaded file is an accepted manuscript from Loughborough's repository. The first page asks readers to cite the published ASCE version. The parsed text and page images were available.

## 1. Citation

- Title: Road Traffic Congestion and Crash Severity: An Econometric Analysis Using Ordered Response Models
- Authors: Mohammed A. Quddus; Chao Wang; Stephen G. Ison
- Year: Published version appears to be 2010 by DOI context; repository record page states 2019 for the figshare record. The manuscript itself does not clearly state publication year on the title page.
- DOI or URL, if present: http://dx.doi.org/10.1061/(ASCE)TE.1943-5436.0000044
- Country / region studied: United Kingdom; M25 London orbital motorway
- Study setting: motorway

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper estimates the relationship between individual crash injury severity and traffic congestion on the M25 motorway while controlling for traffic flow, road geometry, crash characteristics, lighting, surface condition, and time-related factors.
- Main purpose: explanatory severity modelling / econometric analysis
- Evidence quote or page reference: Abstract, p. 2 of manuscript: "The objective of this study is to explore the relationship between the severity of road crashes and the level of traffic congestion using disaggregated crash records and a measure of traffic congestion while controlling for other contributory factors."

## 3. Response Variable

- Target variable: Ordered crash severity category.
- Collision type: injury crashes; categories are slight, serious, and fatal.
- Severity handling: Severity is modelled directly as an ordered categorical response with three levels.
- Count, binary, rate, risk score, severity class, or other: Severity class.
- Time window used for outcomes: STATS19 crash records from 2003 to 2006.
- Evidence quote or page reference: Data section, p. 7: "STATS19 UK road crash data from 2003 and 2006 were obtained"; Table 1, p. 18: "1=Slight (count=3594), 2=Serious (count=353), 3=Fatal (count=51)."

## 4. Exposure Handling

- Exposure variable used, if any: Traffic flow in vehicles per hour is used as an explanatory variable. Traffic congestion is measured by total delay in minutes. Average speed is initially available but excluded due to high negative correlation with congestion.
- Traffic count source: UK Highways Agency traffic characteristics data for 72 M25 segments at 15-minute intervals.
- Whether exposure is modelled, observed, assumed, or ignored: Observed traffic data are assigned to crashes using segment and time matching with a 30-minute lag.
- Treatment of missing or sparse traffic counts: Not stated.
- Whether offset terms, rates, denominators, or normalisation are used: No exposure offset, denominator, crash rate, or normalised collision frequency model is used. This is a conditional severity model for crashes that have already occurred.
- Evidence quote or page reference: Data section, p. 7: traffic congestion, speed, and flow were available "for a total of 72 segments of the M25 (both directions) at 15-minute intervals"; p. 7: "In order to avoid the impact of the crash itself on the traffic variables, a 30-minute time lag was considered."
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The use of time-lagged traffic state before a crash is conceptually relevant to WebTRIS-style temporal traffic profiles. The exact M25 traffic data are much richer than AADF and more directly observed than Open Road Risk's network-wide estimated AADT. The mathematical structure is not an exposure-offset SPF and does not transfer directly to Stage 2 frequency modelling.

Important:

- The paper's traffic-state matching is useful as a severity-analysis design pattern, not as a direct replacement for exposure-normalised link-year collision risk.
- The traffic-flow variable is used conditionally on a crash having occurred, so it should not be interpreted as estimating crash occurrence risk.

## 5. Spatial Unit of Analysis

- Unit: Individual crashes assigned to motorway segments.
- Segment length or segmentation rule: 72 M25 motorway segments, both directions; each segment starts and terminates at a junction. Delay is averaged over a 10-km stretch to account for segment length.
- How crashes are assigned to the network: Crash easting/northing coordinates are matched to motorway segments using crash direction, segment direction, and distance from crash location to segment.
- Treatment of junctions/intersections: Segments start and terminate at junctions, but the analysis is motorway-segment based, not an intersection model.
- Spatial aggregation risks: Traffic conditions are assumed uniform across each segment; the paper explicitly notes this as a limitation, especially where queues are present.
- Evidence quote or page reference: Data section, p. 7: "Since each segment starts and also terminates at a junction, it is reasonable to assume that delays, traffic speed and traffic flow are the same on different locations of the segment." Conclusions, p. 14: "segments would not necessarily have uniform conditions over 10km length if queues are present."
- Relevance to OS Open Roads link-based pipeline: The crash-to-network matching logic is relevant, but the spatial unit is much coarser and motorway-specific. The 10-km assumption would be unsuitable for fine-grained OS Open Roads link-year modelling without aggregation or route-section definitions.

## 6. Temporal Unit of Analysis

- Years covered: 2003-2006.
- Temporal resolution: Crash-level model with 15-minute traffic data assigned using a 30-minute lag; year, peak/off-peak, weekday/weekend, and lighting are included.
- Whether seasonality or time-of-day is modelled: Time of day is represented using a peak/off-peak dummy; year indicators are used. Seasonality is not clearly modelled.
- Whether before-after or panel structure is used: No.
- Evidence quote or page reference: Data section, p. 7: traffic data were available at "15-minute intervals"; p. 7: "a 30-minute time lag was considered"; Table 1, p. 18 includes peak/off-peak, weekdays/weekends, darkness/daylight, and year indicators.
- Relevance to WebTRIS-style time profiles: Supports the idea that time-specific traffic state can be relevant for severity diagnostics. It does not validate using broad peak/off-peak fractions for frequency risk unless crash-time matching is possible.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Traffic congestion / total delay | UK Highways Agency traffic data | Total delay in minutes encountered by all vehicles on segment, averaged over 10 km; assigned to crashes using 30-minute lag | Main explanatory variable of interest; tests whether congestion affects severity | Low to medium; WebTRIS may support temporal traffic state on major roads, but network-wide delay is not available |
| Traffic flow | UK Highways Agency traffic data | Vehicles/hour assigned to each crash using segment/time match and 30-minute lag; log transformed in models | Found significant; higher traffic flow associated with lower severity in this M25 case study | Medium; AADF/WebTRIS can approximate flow, but crash-time hourly flow is not generally available for all links |
| Average traffic speed | UK Highways Agency traffic data | Available but excluded from final models due to high negative correlation with congestion | Potential severity-relevant variable but not used in final model | Low to medium; OSM speed limits are different from observed speed |
| Radius of road curvature | UK Highways Agency road geometry | Minimum radius of curvature per segment; log transformed in models | Road geometry control; straighter roads associated with higher severity at 90% level in this case | Already present / compare implementation via curvature feature |
| Gradient | UK Highways Agency road geometry | Maximum gradient per segment | Tested but not significant | Already candidate / compare implementation with OS Terrain 50 grade |
| Number of lanes | UK Highways Agency road geometry | Categorised as three lanes or less, four lanes, five lanes or higher | Three-lane-or-less stretches associated with higher severity than four-lane reference | Candidate feature where OSM lane coverage is sufficient; coverage risk |
| Road surface condition | STATS19 | Wet vs dry indicator | Wet surface associated with lower severity in this motorway case, plausibly via reduced speed | Collision-derived/contextual at crash time; diagnostic only, not suitable as Stage 2 production feature for future risk unless using weather/surface proxies |
| Lighting condition | STATS19 | Darkness vs daylight | Darkness associated with lower severity at 90% level in this case | Collision-time diagnostic only unless using static lighting / ambient darkness estimates |
| Single-vehicle crash | STATS19 vehicle/crash data | Indicator for single-vehicle vs multi-vehicle crash | Single-vehicle crashes more severe | Post-event variable; not suitable for pre-event Stage 2 production features |
| Number of casualties | STATS19 casualty data | Count of casualties per crash | Severity increases with casualty count | Post-event variable; leakage if used for prediction before crashes occur |
| Year indicators | STATS19 | Categorical indicators for 2003-2006 | Captures downward severity trend | Already analogous to year_norm / temporal diagnostics |

## 8. Model Architecture

- Algorithms/models used: Ordered logit model (OLOGIT), heterogeneous choice model (HCM), generalized ordered logit (GOLOGIT), and partially constrained generalized ordered logit (PC-GOLOGIT).
- Baseline model: Ordered logit.
- Final/preferred model: PC-GOLOGIT is used for interpretation, with HCM also fitting similarly.
- Loss function or likelihood, if stated: Maximum likelihood estimation is stated for ordered logit cut-points and parameters.
- Offset/exposure term, if used: None.
- Spatial autocorrelation handling: Not stated.
- Temporal dependence handling: Year categorical variables and peak/off-peak indicator; no panel or autocorrelation model.
- Interpretability method: Coefficients, threshold-specific coefficients, marginal effects, and predicted probability plots.
- Evidence quote or page reference: Methods section, p. 6: the study employs "three ordered response models: (1) an OLOGIT (2) a HCM and (3) a PC – GOLOGIT." Results section, p. 9: "the PC-GOLOGIT model will be used to interpret the effects of the explanatory variables on the crash severity."

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Dataset size | Crashes | 3,998 total crashes; final model observations 3,837 | M25, 2003-2006 | Model fitted to disaggregated crash records after exclusions | Data section p. 7; Table 2 p. 20 |
| Outcome distribution | Severity counts | Slight 3,594; serious 353; fatal 51 | M25, 2003-2006 | Strong class imbalance toward slight injury | Table 1 p. 18 |
| Model fit | Log-likelihood | -1306.55 | OLOGIT | Worse than HCM/GOLOGIT/PC-GOLOGIT | Table 2 p. 20 |
| Model fit | Log-likelihood | -1299.21 | HCM | Better than OLOGIT; similar to PC-GOLOGIT | Table 2 p. 20 |
| Model fit | Log-likelihood | -1294.29 | GOLOGIT | Best log-likelihood but more parameters | Table 2 p. 20 |
| Model fit | Log-likelihood | -1300.03 | PC-GOLOGIT | Similar to HCM with fewer parameters than GOLOGIT | Table 2 p. 20 |
| Model fit | LR Chi-square | 155.7 | OLOGIT | Overall model significance / fit comparison | Table 2 p. 20 |
| Model fit | LR Chi-square | 170.4 | HCM | Better than OLOGIT; difference reported significant | Table 2 p. 20; Results p. 8 |
| Model fit | LR Chi-square | 180.20 | GOLOGIT | Higher than PC-GOLOGIT but with more degrees of freedom | Table 2 p. 20 |
| Model fit | LR Chi-square | 169.68 | PC-GOLOGIT | Similar explanatory performance to HCM | Table 2 p. 20 |
| Model fit | McFadden pseudo Rho-square | 0.096 | OLOGIT | In-sample model fit only | Table 2 p. 20 |
| Model fit | McFadden pseudo Rho-square | 0.099 | HCM | In-sample model fit only | Table 2 p. 20 |
| Model fit | McFadden pseudo Rho-square | 0.09 | GOLOGIT | In-sample model fit only | Table 2 p. 20 |
| Model fit | McFadden pseudo Rho-square | 0.10 | PC-GOLOGIT | In-sample model fit only | Table 2 p. 20 |
| Main coefficient | Traffic congestion | Not statistically significant across all ordered response models | All models | Total delay did not affect severity in this M25 case | Results p. 10; Table 2 p. 20 |
| Main coefficient | ln(traffic flow) | PC-GOLOGIT threshold y>1: -0.509***; y>2: -0.869*** | PC-GOLOGIT | Higher traffic flow associated with lower crash severity, with stronger effect for fatal threshold | Table 2 p. 20 |
| Marginal effect | ln(traffic flow) on slight injury probability | 0.0403** | PC-GOLOGIT | Higher flow increases probability of slight injury outcome | Table 3 p. 21 |
| Marginal effect | ln(traffic flow) on serious injury probability | -0.0343** | PC-GOLOGIT | Higher flow reduces probability of serious injury outcome | Table 3 p. 21 |
| Marginal effect | ln(traffic flow) on fatal probability | -0.006** | PC-GOLOGIT | Higher flow reduces probability of fatal outcome | Table 3 p. 21 |
| Marginal effect | Single-vehicle crash on fatal probability | 0.0141** | PC-GOLOGIT | Single-vehicle crashes more likely to be fatal than multi-vehicle crashes | Table 3 p. 21 |
| Marginal effect | Wet surface on slight injury probability | 0.0278** | PC-GOLOGIT | Wet surface associated with less severe outcomes in this case | Table 3 p. 21 |
| Marginal effect | Three lanes or less on serious injury probability | 0.0321** | PC-GOLOGIT | Three-lane-or-less stretches associated with more serious injury probability than four-lane reference | Table 3 p. 21 |

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? In-sample model fit and in-sample marginal effects. No train/test split, cross-validation, spatial holdout, temporal holdout, or external validation is reported.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy. The predicted probability plots are in-sample diagnostics.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They test model fit, coefficient interpretation, proportional-odds assumptions, heteroskedasticity handling, and severity association. They do not test predictive generalisation or hotspot ranking usefulness.
- Are any metrics likely to be optimistic for real-world deployment? Yes. The model fit and predicted probabilities are based on the same crash data used for estimation and may overstate deployment performance.
- Which metric, if any, is most relevant to Open Road Risk? The threshold-specific traffic-flow coefficients and marginal effects are relevant for a possible severity diagnostic, but not for production link-year frequency risk.

Important:

- The paper does not report predictive accuracy metrics such as held-out MAE, RMSE, AUC, log loss, calibration, or ranking metrics.
- Pseudo Rho-square and LR Chi-square should not be treated as predictive validation.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The model is conditional on crashes having occurred, so zero-crash locations are not part of the analysis. Fatal and serious crashes are rare relative to slight crashes, but the ordered severity model directly models the three severity categories.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Ordered response models: OLOGIT, HCM, GOLOGIT, PC-GOLOGIT. No resampling or class weighting is stated.
- Whether high-risk locations are evaluated separately: No.
- Evidence quote or page reference: Table 1, p. 18 gives the severity counts: slight 3,594, serious 353, fatal 51. Methods section, p. 6 states that ordered response models are used for the ordered dependent variable.
- Practical relevance to my sparse collision link-year dataset: Limited for Stage 2 frequency modelling because zero-crash link-years are excluded by design. More relevant for conditional severity modelling after a crash has occurred or for a separate severity module.

Important:

- This is not a zero-heavy count model. It is an ordered crash-severity model using crash records only.

## 11. Validation Strategy

- Train/test split method: Not stated; no split reported.
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Not stated.
- Metrics: In-sample log-likelihood, LR Chi-square, McFadden pseudo Rho-square, coefficient significance, marginal effects, and predicted probability plots.
- External validation: Not stated.
- Leakage or generalisation risks: Several explanatory variables are post-event or crash-time variables, including single-vehicle status, number of casualties, road surface condition, and lighting condition. These are valid for explanatory severity analysis but would leak information if used to predict risk before crashes occur. Segment-level traffic state is assigned with a 30-minute lag to reduce the risk that the crash itself affects congestion/speed/flow variables.
- Evidence quote or page reference: Data section, p. 7: "In order to avoid the impact of the crash itself on the traffic variables, a 30-minute time lag was considered." Conclusions, p. 14: traffic conditions assigned by segment may be non-uniform over 10 km when queues are present.
- What I should copy or avoid: Copy the idea of carefully lagging traffic-state variables before crash occurrence in temporal diagnostics. Avoid treating crash-time and post-crash variables as production predictors for future link-level risk.

Important:

- The paper's use of crash-time variables is not classic leakage within its stated explanatory design, because the model conditions on a crash having occurred. It would become leakage if copied into a pre-event risk-ranking model.

## 12. Key Findings Relevant to My Project

- Finding: Traffic congestion measured as total delay was not statistically significant for crash severity in this M25 case study.
  - Why it matters: This cautions against assuming congestion or low-speed traffic states automatically explain severity once flow and other controls are included.
  - Evidence quote or page reference: Results section, p. 10: "our data from the M25 motorway do not support this hypothesis and this is the case for all ordered response models estimated in this study."
  - Confidence: high

- Finding: Traffic flow was statistically significant and higher flow was associated with lower severity, conditional on a crash occurring.
  - Why it matters: This supports separating crash frequency/exposure effects from conditional severity effects; high flow may raise crash frequency but reduce severity in some motorway contexts.
  - Evidence quote or page reference: Results section, p. 10: "if traffic flow increases then the level of crash severity decreases"; Table 2, p. 20 reports significant negative traffic-flow coefficients.
  - Confidence: high

- Finding: PC-GOLOGIT was preferred over simple ordered logit because proportional odds were violated for traffic flow and number of vehicles involved.
  - Why it matters: Severity effects may differ between slight-vs-serious and serious-vs-fatal thresholds; a single coefficient may hide important structure.
  - Evidence quote or page reference: Results section, p. 9: Brant test found traffic flow and number of vehicles involved did not meet proportional odds assumption.
  - Confidence: high

- Finding: Several significant predictors are post-event crash characteristics, especially single-vehicle crash and number of casualties.
  - Why it matters: These are useful for explaining severity but unsuitable for a pre-crash production risk model.
  - Evidence quote or page reference: Table 2, p. 20 and Table 3, p. 21 report significant single-vehicle and casualty effects.
  - Confidence: high

- Finding: Geometry variables were tested, but gradient was insignificant and radius of curvature was only weakly significant.
  - Why it matters: Curvature/grade should be treated as diagnostics or candidate features requiring validation, not assumed strong production predictors from this paper alone.
  - Evidence quote or page reference: Table 2, p. 20 shows gradient not significant and curvature significant at p<=0.1 only.
  - Confidence: medium

- Finding: The paper highlights a spatial assignment limitation where segment-average traffic states may not represent conditions at the exact crash location.
  - Why it matters: Open Road Risk's link-level traffic estimates also need uncertainty/assignment caveats, especially if temporal or local traffic-state features are added.
  - Evidence quote or page reference: Conclusions, p. 14: "segments would not necessarily have uniform conditions over 10km length if queues are present."
  - Confidence: high

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Conditional severity model using ordered response methods | Separates severity from frequency; can test whether predictors affect slight/serious/fatal thresholds differently | STATS19 severity categories and candidate predictors | 3,998 M25 crashes; 3,837 observations in models | Medium; crash-level severity model is much smaller than link-year frequency table | Future severity model / validation / documentation | Medium | May not support pre-event link risk if post-event variables are included |
| Partial proportional odds / generalized ordered logit diagnostic | Tests whether severity predictors have different effects by threshold | Crash severity categories and explanatory features | M25 crash-level data | Medium; feasible on crash records, not directly on 21.7M link-years | Future severity model | Medium | More complex to explain and implement than GLM; Python ecosystem support may be less convenient than R/Stata |
| 30-minute lagged traffic-state assignment | Reduces reverse causality where crash itself affects congestion/speed/flow | Crash time/location and high-resolution traffic sensor data | 72 M25 segments, 15-minute traffic data | Low to medium; feasible only near WebTRIS or equivalent sensors | Stage 1b / temporal validation / small pilot | Medium | Sparse sensor coverage and segment mismatch |
| Predicted probability curves for severity outcomes | Useful for communicating how severity probabilities vary with traffic flow or casualties | Fitted severity model | Figures 2-4 in manuscript | High for documentation/diagnostics if severity model exists | Documentation / validation | Low | Could be overinterpreted as causal or general predictive evidence |
| Explicit note that crash-time variables are conditional severity controls | Helps governance and avoids leakage into production risk features | STATS19 variable classification | Paper uses crash-time/post-event variables | High | Documentation / methodology | Low | Users may confuse explanatory severity analysis with prospective risk ranking |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Using total delay as a network-wide production feature | Open Road Risk does not have observed delay for every OS Open Roads link-year | Segment-level 15-minute delay data across full network | 72 M25 motorway segments | Low | Use WebTRIS temporal profiles as limited motorway/major-road diagnostics, not full-network feature | High |
| Using post-event variables in Stage 2 risk ranking | Single-vehicle status and casualties are only known after a crash | Future crash details are unavailable before event | Crash-record model | Low for production prediction | Keep in separate explanatory severity model | High |
| Assuming segment traffic state is uniform over long sections | Paper itself notes this limitation; OS Open Roads links are much finer | Uniform segment traffic conditions | 10-km averaged M25 traffic segments | Low | Use finer link-level assignment where observed data exist; document uncertainty | High |
| Directly applying M25 motorway findings to mixed rural/urban roads | Study is one motorway with specific geometry, traffic, and severity patterns | Evidence outside M25 and non-motorway contexts | UK motorway only | Low | Treat as motorway severity evidence only; compare against STATS19 in project area | High |
| Replacing frequency model with severity ordered model | The paper does not model crash occurrence or zero-crash exposure | Conditional crash records only | 3,837 crash observations | Low for Stage 2 collision frequency | Use as separate severity layer, not replacement for exposure-offset count model | High |

Important:

- This paper is more relevant to conditional severity modelling and temporal traffic-state diagnostics than to exposure-adjusted frequency risk ranking.
- The study scale is small compared with Open Road Risk's 21.7 million link-year rows and is restricted to one motorway.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Not directly. It discusses traffic flow and congestion but models severity conditional on a crash, not crash frequency per exposure.
- Does it suggest better handling of AADT/AADF uncertainty? Not directly. It uses observed high-resolution traffic data, not sparse AADF estimation.
- Does it suggest useful geometry or road-context features? Weakly. It tests curvature/radius, gradient, and number of lanes. Curvature and lane count show some relevance; gradient is insignificant in this case.
- Does it suggest better modelling of junctions? No. It is motorway-segment based.
- Does it suggest better treatment of severity? Yes. It supports treating severity as a separate ordered outcome and checking proportional-odds assumptions rather than collapsing severity into a single score without testing.
- Does it suggest better validation design? Limited. It does not provide held-out validation, but it does show useful specification diagnostics: Brant test, heteroskedasticity checks via HCM, model comparison, and marginal effects.
- Does it expose a weakness in my current approach? It reinforces that frequency and severity are different targets. A frequency model driven by exposure-adjusted counts should not be assumed to capture severity patterns without a separate severity check or severity-weighted diagnostic.

## 15. Repo Actionability

- Suggested repo action: Add a documentation note distinguishing exposure-adjusted collision frequency from conditional crash severity.
  - Action type: documentation note
  - Relevant stage: documentation / Stage 2
  - Why the paper supports it: The paper models severity conditional on crashes and finds traffic flow effects on severity that differ from frequency literature.
  - Evidence quote or page reference: Introduction, p. 6: "no attempt is made to estimate the actual probability of a specific accident occurring."
  - Effort: low
  - Risk if implemented badly: Users may misread the production risk percentile as a severity ranking.

- Suggested repo action: Create a small crash-level severity diagnostic using STATS19 severity as an ordered outcome, excluding post-event predictors from any pre-event risk model.
  - Action type: small pilot
  - Relevant stage: validation / future severity model
  - Why the paper supports it: Ordered response models are explicitly used for slight/serious/fatal severity categories.
  - Evidence quote or page reference: Methods section, p. 6: severity is categorical and ordinal; ordered logit/probit are appropriate.
  - Effort: medium
  - Risk if implemented badly: Accidentally mixing crash-only variables into prospective link risk features.

- Suggested repo action: Add a leakage guardrail table classifying variables as pre-event static, time-varying pre-event, crash-time, or post-event.
  - Action type: documentation note / diagnostic
  - Relevant stage: documentation / feature engineering
  - Why the paper supports it: Several significant variables are crash-time or post-event variables: single-vehicle crash, number of casualties, wet surface, lighting.
  - Evidence quote or page reference: Table 2, p. 20 and Table 3, p. 21.
  - Effort: low
  - Risk if implemented badly: Over-restricting useful diagnostic variables that are safe outside production modelling.

- Suggested repo action: If WebTRIS crash-time matching is attempted, use a lagged traffic-state assignment rather than same-interval traffic state.
  - Action type: small pilot / diagnostic
  - Relevant stage: Stage 1b / validation
  - Why the paper supports it: The authors used a 30-minute lag to avoid the crash affecting traffic variables.
  - Evidence quote or page reference: Data section, p. 7: "In order to avoid the impact of the crash itself on the traffic variables, a 30-minute time lag was considered."
  - Effort: medium
  - Risk if implemented badly: Sparse sensor coverage could create a biased motorway-only diagnostic.

- Suggested repo action: Use curvature and grade as validation/comparison diagnostics rather than upgrading them to production importance based on this paper.
  - Action type: diagnostic / baseline comparison
  - Relevant stage: feature engineering / validation
  - Why the paper supports it: Curvature was weakly significant and gradient was insignificant in this motorway severity model.
  - Evidence quote or page reference: Table 2, p. 20.
  - Effort: low
  - Risk if implemented badly: Overclaiming causal or general safety relevance from one motorway severity study.

## 16. Query Tags

- crash-severity
- ordered-logit
- generalized-ordered-logit
- partial-proportional-odds
- heterogeneous-choice-model
- M25
- STATS19
- motorway
- traffic-flow
- congestion
- total-delay
- temporal-traffic-state
- crash-time-matching
- severity-model
- curvature
- gradient
- lane-count
- post-event-leakage
- in-sample-diagnostic
- UK-transferable-partial

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: No held-out validation; no cross-validation; no external validation; no clear publication year in the manuscript title pages; no detailed treatment of missing traffic data; no spatial autocorrelation treatment.
- Parts of the paper that need manual checking: Published ASCE version details and final citation year; exact formatting of Tables 2 and 3 against the published version; any differences between accepted manuscript and final version.
- Any likely ambiguity or risk of misinterpretation: The paper's finding that higher traffic flow is associated with lower severity is conditional on crashes that occurred. It should not be interpreted as saying higher flow is generally safer overall. The congestion result is M25-specific and should not be generalised to all road types.
