# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: road-traffic-congestion-and-crash-severity-econometric-2rrbyxf6f0.pdf
- Suggested Markdown filename: final-quddus-wang-ison-m25-severity-ordered-response.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: original PDF plus two Markdown extractions
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The uploaded file is an accepted manuscript from Loughborough's repository and asks readers to cite the published ASCE version. Parsed text and page images were accessible. Some equations have parsing artefacts, but the core methods, data section, model results, and key tables were readable from the manuscript/extractions.

## 1. Citation

- Title: Road Traffic Congestion and Crash Severity: An Econometric Analysis Using Ordered Response Models
- Authors: Mohammed A. Quddus; Chao Wang; Stephen G. Ison
- Year: Not clearly stated on the manuscript title page. The DOI points to the published ASCE version; one extraction records this as circa 2010. The repository/figshare wrapper gives a later repository record date. Use `Not stated` unless the publication year is verified separately.
- DOI or URL, if present: http://dx.doi.org/10.1061/(ASCE)TE.1943-5436.0000044
- Country / region studied: United Kingdom / M25 London orbital motorway
- Study setting: Motorway

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper estimates whether traffic congestion affects individual crash injury severity on the M25 motorway, controlling for traffic flow, traffic state, road geometry, crash characteristics, road surface, lighting, day/time, and year.
- Main purpose: explanatory severity modelling / econometric analysis.
- Evidence quote or page reference: Page 4 states that the objective is to explore the relationship between crash severity and traffic congestion using disaggregated crash records and a congestion measure while controlling for other contributory factors. Page 6 states that the study examines the association using ordered response models.

## 3. Response Variable

- Target variable: Ordered crash severity category for individual crashes.
- Collision type: STATS19 injury crashes on the M25 motorway.
- Severity handling: Severity is the primary modelled outcome, coded as slight, serious, and fatal.
- Count, binary, rate, risk score, severity class, or other: Ordered categorical severity class.
- Time window used for outcomes: STATS19 crash records from 2003–2006.
- Evidence quote or page reference: Page 6 describes slight, serious, and fatal as the ordered crash-severity categories. Page 9 states that 3,998 crashes occurred on the M25 between 2003 and 2006, with 1.28% fatal, 8.83% serious, and 89.89% slight injury crashes.

Important:

- This is a crash-conditional severity model. It does not model whether a crash occurs.
- It is not a crash-frequency SPF and not an exposure-normalised link-year risk model.

## 4. Exposure Handling

- Exposure variable used, if any: No exposure term is used in the Stage-2-frequency sense. Traffic flow is used as an explanatory variable for severity, conditional on a crash having occurred. Traffic congestion is measured by total delay and tested as the main explanatory variable.
- Traffic count source: UK Highways Agency traffic data for 72 M25 segments, both directions, at 15-minute intervals.
- Whether exposure is modelled, observed, assumed, or ignored: Observed traffic state is assigned to individual crash records by matching crash segment and crash time, using a 30-minute lag to reduce reverse causation from crash-induced congestion.
- Treatment of missing or sparse traffic counts: Not stated.
- Whether offset terms, rates, denominators, or normalisation are used: None. No offset, denominator, crash rate, or frequency exposure normalisation is used. This is appropriate for a conditional severity model.
- Evidence quote or page reference: Page 7 states that traffic congestion, speed, and flow data were available for 72 M25 segments at 15-minute intervals. Page 7 states that a 30-minute lag was used so traffic data before the crash were assigned to the crash. Model equations on pages 6–8 do not include an offset term.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes:
  - The 30-minute lag is useful as a design pattern for crash-time traffic-state analysis.
  - The data richness is higher than Open Road Risk’s current AADF/WebTRIS-wide exposure setup.
  - The model does not transfer directly to Open Road Risk Stage 2 frequency/ranking because it conditions on crash occurrence.

Important:

- Do not interpret the traffic-flow coefficient as crash occurrence risk.
- The paper estimates severity conditional on a crash, not expected collision count.

## 5. Spatial Unit of Analysis

- Unit: Individual crash records assigned to M25 motorway segments.
- Segment length or segmentation rule: 72 M25 motorway segments, both directions. Segments start and terminate at junctions. Traffic delay is averaged over a 10-km stretch to account for segment length.
- How crashes are assigned to the network: STATS19 crash coordinates are matched to motorway segments using crash direction, segment direction, and distance from crash point to segment. The paper refers readers to Wang et al. (2009) for details of the matching method.
- Treatment of junctions/intersections: The analysis is motorway-segment based, not an intersection model. Segments start/end at junctions, but junction effects are not modelled as a separate unit.
- Spatial aggregation risks: The paper assumes traffic state is uniform along each segment, which is questionable when queues are present. The authors explicitly flag this as a limitation.
- Evidence quote or page reference: Page 7 states that each segment starts and terminates at a junction and assumes delay, speed, and flow are the same across locations on the segment. Page 14 states that segments would not necessarily have uniform conditions over 10 km if queues are present.
- Relevance to OS Open Roads link-based pipeline: Medium for crash-to-network assignment and traffic-state matching logic; low as a direct modelling unit. OS Open Roads links are much finer than the 10-km traffic-state assumption, but Open Road Risk currently does not model individual crash severity.

## 6. Temporal Unit of Analysis

- Years covered: 2003–2006.
- Temporal resolution: Individual crash records matched to 15-minute traffic data, using traffic conditions 30 minutes before the crash.
- Whether seasonality or time-of-day is modelled: Time of day is represented with a peak/off-peak indicator; weekday/weekend and year indicators are used. Seasonality is not clearly modelled.
- Whether before-after or panel structure is used: No.
- Evidence quote or page reference: Page 7 states that traffic data were available at 15-minute intervals and that a 30-minute lag was applied. Table 1 includes peak/off-peak, weekday/weekend, light condition, and year variables.
- Relevance to WebTRIS-style time profiles: Medium for future crash-time severity diagnostics. It supports careful pre-crash time matching, but does not validate broad annual peak/off-peak exposure fractions for crash frequency.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Traffic congestion / total delay | UK Highways Agency 15-minute traffic data | Total delay in minutes encountered by all vehicles on the segment, averaged over 10 km and assigned with 30-minute lag | Main variable of interest; found statistically insignificant for severity | Low-to-medium; no network-wide open delay data in current pipeline |
| Traffic flow | UK Highways Agency traffic data | Vehicles/hour assigned to crash by segment/time with 30-minute lag; log transformed in models | Significant; higher flow associated with less severe outcomes in this case | Medium for temporal diagnostics; low for all-link production features |
| Average traffic speed | UK Highways Agency traffic data | Available but removed because it was highly negatively correlated with congestion | Potential severity mechanism, not in final model | Low-to-medium; observed speed differs from OSM speed limit |
| Radius of road curvature | UKHA road geometry | Minimum radius per segment, log transformed | Geometry control; larger radius/straighter sections associated with higher severity at weak significance | Medium; curvature is feasible, but sign is motorway/severity-specific |
| Gradient / vertical grade | UKHA road geometry | Maximum gradient per segment | Tested but not significant for severity | Medium as diagnostic; candidate via OS Terrain 50 |
| Number of lanes | UKHA road geometry | Categorical: three lanes or fewer, four lanes, five lanes or more | Three-or-fewer-lane stretches associated with higher serious injury probability than four-lane reference | Medium if lane data coverage allows |
| Wet road surface | STATS19 | Binary wet/dry condition at crash time | Wet surface associated with lower severity, plausibly through lower speed | Post-event/crash-time diagnostic only; not a pre-event ranking feature |
| Darkness / light condition | STATS19 | Binary darkness/daylight | Darkness associated with lower severity in this motorway case | Crash-time diagnostic only unless modelled from ambient light/infrastructure |
| Single-vehicle crash | STATS19 vehicle/crash data | Binary single vs multi-vehicle crash | Single-vehicle crashes more severe | Post-event variable; leakage for pre-crash risk ranking |
| Number of casualties per crash | STATS19 casualty file | Count of casualties involved | Severity association and heteroskedasticity source | Post-event and potentially partly circular for severity prediction |
| Peak/off-peak | Crash time | Binary time-period indicator | Tested; not the core significant result | Candidate only for diagnostics |
| Weekday/weekend | Crash date | Binary day-type indicator | Used as temporal/context control | Diagnostic only |
| Year indicators | STATS19 | Year dummies 2003–2006 | Captures temporal trend or unobserved annual effects | Already analogous to year controls |

Important leakage note:

- Several variables are valid for explanatory crash-severity analysis but not for prospective Open Road Risk production risk ranking: single-vehicle status, casualties per crash, road-surface condition, and crash-time lighting are all observed at/after the crash event.

## 8. Model Architecture

- Algorithms/models used: Ordered logit (OLOGIT), heterogeneous choice model (HCM), generalized ordered logit (GOLOGIT), partially constrained generalized ordered logit (PC-GOLOGIT), plus attempted random-parameter ordered logit and mixed multinomial logit checks.
- Baseline model: Ordered logit.
- Final/preferred model: PC-GOLOGIT is used for interpretation because the proportional-odds assumption is violated for traffic flow and number of vehicles, while the full GOLOGIT adds unnecessary parameters. HCM gives similar signs/significance and handles heteroskedasticity.
- Loss function or likelihood, if stated: Maximum likelihood; log-likelihood and likelihood-ratio statistics are reported.
- Offset/exposure term, if used: None.
- Spatial autocorrelation handling: Not stated.
- Temporal dependence handling: Year indicators and peak/off-peak/weekday-weekend variables; no temporal autocorrelation model.
- Interpretability method: Coefficients, threshold-specific coefficients, marginal effects, and predicted probability plots.
- Evidence quote or page reference: Pages 6–8 define OLOGIT, HCM, GOLOGIT, and PC-GOLOGIT. Page 11 states that PC-GOLOGIT is used to interpret the explanatory variables. Page 9 states random effects were not statistically significant in random-parameter and mixed multinomial logit checks.

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---:|---:|---|---|---|
| Dataset size | Total crashes | 3,998 | M25, 2003–2006 | Disaggregated crash records before modelling exclusions | Page 9 |
| Final model observations | Observations | 3,837 | Table 2 models | Modelled sample after exclusions/missingness | Table 2 |
| Outcome distribution | Slight / serious / fatal | 3,594 / 353 / 51 | M25 crashes | Strong class imbalance toward slight injury | Table 1 |
| Outcome distribution | Fatal / serious / slight percentages | 1.28% / 8.83% / 89.89% | M25 crashes | Fatal and serious crashes are rare relative to slight crashes | Page 9 |
| Descriptive traffic state | Mean delay by severity | Fatal 4 min; serious 8 min; slight 9.6 min | M25 crashes | Descriptive association suggests lower delay for fatal crashes, but model finds congestion not significant | Page 10 |
| Descriptive traffic state | Mean flow by severity | Fatal 2131 veh/h; serious 3345 veh/h; slight 3911 veh/h | M25 crashes | Higher flow associated descriptively with less severe outcomes | Page 10 |
| Descriptive traffic state | Mean speed by severity | Fatal 93 km/h; serious 86 km/h; slight 84.5 km/h | M25 crashes | Higher speed associated descriptively with higher severity | Page 10 |
| Model fit | Log-likelihood | -1306.55 | OLOGIT | In-sample fit; worse than HCM/GOLOGIT/PC-GOLOGIT | Table 2 |
| Model fit | Log-likelihood | -1299.21 | HCM | Better than OLOGIT; similar to PC-GOLOGIT | Table 2 |
| Model fit | Log-likelihood | -1294.29 | GOLOGIT | Best log-likelihood but more parameters | Table 2 |
| Model fit | Log-likelihood | -1300.03 | PC-GOLOGIT | Preferred parsimonious interpretation model | Table 2 |
| Model fit | LR Chi-square | 155.7 | OLOGIT | In-sample model comparison statistic | Table 2 |
| Model fit | LR Chi-square | 170.4 | HCM | Better than OLOGIT; reported significant improvement | Table 2 / results text |
| Model fit | LR Chi-square | 180.20 | GOLOGIT | Higher than PC-GOLOGIT but not significantly better for extra parameters | Table 2 / results text |
| Model fit | LR Chi-square | 169.68 | PC-GOLOGIT | Similar performance to HCM | Table 2 |
| Model fit | McFadden pseudo Rho-square | 0.096 / 0.099 / 0.090 / 0.100 | OLOGIT / HCM / GOLOGIT / PC-GOLOGIT | In-sample fit only; not predictive accuracy | Table 2 |
| Main coefficient | Traffic congestion / total delay | Not statistically significant | All ordered response models | No evidence that total delay affects crash severity on the M25 in this model | Results section / Table 2 |
| Main coefficient | Congestion index | Not statistically significant | Alternative congestion measure | Alternative congestion measure also insignificant | Results section |
| Main coefficient | log traffic flow | PC-GOLOGIT threshold y>1: about -0.509; y>2: about -0.869 | PC-GOLOGIT | Higher flow associated with lower severity, stronger near fatal threshold | Table 2 |
| Marginal effect | log traffic flow on slight injury probability | 0.0403 | PC-GOLOGIT | Higher flow increases probability of slight injury outcome | Table 3 |
| Marginal effect | log traffic flow on serious injury probability | -0.0343 | PC-GOLOGIT | Higher flow reduces probability of serious outcome | Table 3 |
| Marginal effect | log traffic flow on fatal probability | -0.006 | PC-GOLOGIT | Higher flow reduces probability of fatal outcome | Table 3 |
| Marginal effect | Single-vehicle crash on fatal probability | 0.0141 | PC-GOLOGIT | Single-vehicle crashes are more likely to be fatal | Table 3 |
| Marginal effect | Wet surface on slight injury probability | 0.0278 | PC-GOLOGIT | Wet surface associated with lower severity in this motorway case | Table 3 |
| Marginal effect | Three lanes or fewer on serious injury probability | 0.0321 | PC-GOLOGIT | Three-or-fewer-lane stretches associated with higher serious injury probability than four-lane reference | Table 3 |

After the table:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? They are in-sample model fit and marginal-effect estimates. No train/test split, cross-validation, spatial holdout, temporal holdout, grouped holdout, or external validation is reported.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They test model fit, coefficient/marginal-effect interpretation, heteroskedasticity, proportional-odds assumptions, and severity association. They do not test predictive generalisation or hotspot/ranking performance.
- Are any metrics likely to be optimistic for real-world deployment? Yes. They are in-sample and based on one motorway.
- Which metric, if any, is most relevant to Open Road Risk? The congestion null result and threshold-specific traffic-flow severity effects are useful for a possible future severity diagnostic, not for Stage 2 frequency production ranking.

Important:

- Pseudo Rho-square and LR Chi-square are not predictive validation metrics.
- The paper reports associations conditional on a crash having occurred.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Zero-crash locations are not part of the analysis because the model uses crash records only. Fatal and serious crashes are rare, but the ordered severity model uses individual crash records across four years to increase sample size.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Ordered response models only. No count model, zero-inflated model, hurdle model, resampling, or class weighting is reported.
- Whether high-risk locations are evaluated separately: No.
- Evidence quote or page reference: Page 9 reports the fatal/serious/slight distribution. Pages 6–8 describe ordered response models.
- Practical relevance to my sparse collision link-year dataset: Limited for frequency modelling, because zero-crash link-years are absent by design. More relevant as a possible separate conditional-severity module.

Important:

- This paper should not be tagged as a zero-heavy count model.
- It is not suitable evidence for choosing Poisson/NB/ZINB for link-year collision frequency.

## 11. Validation Strategy

- Train/test split method: Not stated / none.
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Not stated.
- Metrics: In-sample log-likelihood, LR Chi-square, McFadden pseudo Rho-square, coefficient significance, marginal effects, predicted probability plots.
- External validation: Not stated.
- Leakage or generalisation risks:
  - The model is explanatory and crash-conditional, so crash-time/post-event variables are legitimate within the stated design.
  - These same variables would be leakage in a pre-event risk-ranking model.
  - Traffic-state variables use a 30-minute lag, which is a useful mitigation against the crash itself affecting measured congestion/flow.
  - Segment-level traffic-state uniformity over up to 10 km is a limitation, especially under queuing.
- Evidence quote or page reference: Page 7 describes the 30-minute time lag; page 14 notes non-uniform traffic conditions over 10 km segments when queues are present.
- What I should copy or avoid: Copy the lagged traffic-state matching idea for future crash-time severity analysis. Avoid using post-event variables such as casualties, single-vehicle status, and road-surface condition in prospective risk ranking.

## 12. Key Findings Relevant to My Project

1. Finding: Traffic congestion, measured as total delay, was not statistically significant for crash severity on the M25.
   - Why it matters: Congestion proxies should not be prioritised as a general Stage 2 feature solely on this evidence. If used, they should be tested as diagnostics and kept motorway/time-state specific.
   - Evidence quote or page reference: Results section around pages 10–12 and Table 2.
   - Confidence: medium. Strong within this M25 case, weak for general UK mixed-road transfer.

2. Finding: Higher traffic flow is associated with less severe crash outcomes, conditional on a crash having occurred.
   - Why it matters: Exposure can raise crash opportunity/frequency while simultaneously being associated with lower conditional severity. Open Road Risk should keep frequency and severity concepts separate.
   - Evidence quote or page reference: Page 12 states that higher traffic flow reduces severity; Table 2 and Table 3 give threshold coefficients and marginal effects.
   - Confidence: medium.

3. Finding: The study uses a 30-minute lag for traffic variables to avoid reverse causation from the crash affecting congestion/flow.
   - Why it matters: This is a clean design pattern for any future crash-time WebTRIS or traffic-state severity diagnostic.
   - Evidence quote or page reference: Page 7.
   - Confidence: high.

4. Finding: Ordered-logit assumptions matter; proportional odds was violated for traffic flow and number of vehicles, leading to PC-GOLOGIT.
   - Why it matters: If Open Road Risk adds a severity model, a simple ordered logit may be too restrictive.
   - Evidence quote or page reference: Page 11 discusses Brant test results and PC-GOLOGIT model choice.
   - Confidence: high.

5. Finding: Some variables are valid for explanatory severity modelling but would leak information in a prospective risk model.
   - Why it matters: Features such as single-vehicle crash, number of casualties, wet surface, and crash-time lighting should be treated as severity/explanatory variables, not pre-event link-risk features.
   - Evidence quote or page reference: Table 1 and Table 3 list these variables and marginal effects.
   - Confidence: high.

6. Finding: Segment-level traffic assignment can be too coarse under queues.
   - Why it matters: Open Road Risk should be careful when assigning area/segment-level traffic states to specific crash locations, especially where congestion varies within a route section.
   - Evidence quote or page reference: Conclusion, page 14.
   - Confidence: high.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Separate conditional-severity model | Keeps crash frequency and severity mechanisms distinct | STATS19 severity records and crash-level features | 3,998 M25 crashes | Medium as future module; not current frequency model | future severity model / documentation | Medium | Sparse fatal/serious classes outside aggregation |
| PC-GOLOGIT / flexible ordered response comparison | Handles proportional-odds violations | Crash-level severity data | Individual crash records | Medium | future severity model | Medium | More complex interpretation |
| 30-minute lagged traffic-state matching | Avoids reverse causation from crash-caused congestion | WebTRIS/traffic-state data and crash time/location | M25 15-min traffic data | Medium for major roads only | Stage 1b / future severity diagnostic | Medium | Sparse/uneven sensor coverage |
| Congestion null-result documentation | Avoids over-prioritising congestion features | Literature note | M25 motorway | Medium-low | documentation | Low | M25 result may not generalise |
| Severity/frequency separation note | Prevents interpreting exposure effects incorrectly | Existing model docs | Case-study evidence | High | documentation / methodology | Low | None |
| Model-assumption checks for severity models | Brant test / heteroskedasticity checks | Severity model outputs | Ordered response models | High if severity module built | future validation | Low-medium | Not relevant until severity model exists |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Using congestion delay as production Stage 2 feature | Total delay not available network-wide and was not significant here | Network-wide delay data | M25 only | Low | Use only as local/WebTRIS diagnostic | High |
| Using crash-time/post-event variables for risk ranking | They are observed at/after crash occurrence | Pre-event feature availability | Individual crash records | Low | Use only in explanatory severity model | High |
| Direct coefficient transfer | M25 motorway-specific, conditional severity model | Local validation and model refit | One motorway | Low | Treat as qualitative evidence | High |
| Replacing frequency model with ordered severity model | Different estimand: severity conditional on crash | Crash occurrence model still needed | Crash records only | Low | Add separate severity module if useful | High |
| Using in-sample pseudo R² as validation | No held-out predictive validation | Cross/spatial/temporal validation | In-sample model | Low | Use modern validation if model implemented | High |

Important:

- This paper is useful for future severity modelling and for conceptual separation of frequency vs severity.
- It is not a production-change paper for Open Road Risk’s current exposure-adjusted collision-frequency ranking.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? No direct support. It is a conditional severity model, not a frequency model. It does reinforce that traffic flow can affect severity differently from crash occurrence.
- Does it suggest better handling of AADT/AADF uncertainty? No.
- Does it suggest useful geometry or road-context features? Curvature, lane count, and gradient are relevant as severity controls, but transfer should be cautious.
- Does it suggest better modelling of junctions? No. It is motorway-segment based.
- Does it suggest better treatment of severity? Yes. It supports modelling severity separately from frequency using ordered response methods, while testing proportional-odds and heteroskedasticity assumptions.
- Does it suggest better validation design? No. It has no held-out validation. The useful design contribution is lagging traffic-state variables.
- Does it expose a weakness in my current approach? It highlights that a frequency model alone cannot answer severity questions, and that variables useful for explaining severity can be invalid for pre-event frequency risk prediction.

## 15. Repo Actionability

1. Suggested repo action: Add a documentation note distinguishing collision frequency, conditional severity, and combined risk/severity scoring.
   - Action type: documentation note
   - Relevant stage: documentation / methodology
   - Why the paper supports it: The paper models severity conditional on a crash and explicitly does not estimate crash occurrence probability.
   - Evidence quote or page reference: Page 4 states no attempt is made to estimate the actual probability of a specific accident occurring.
   - Effort: low
   - Risk if implemented badly: Could distract from current frequency model if over-expanded.

2. Suggested repo action: Do not add congestion delay as a production feature from this paper alone.
   - Action type: avoid production change
   - Relevant stage: Stage 2 / feature engineering
   - Why the paper supports it: Congestion/total delay was statistically insignificant for M25 crash severity across model specifications.
   - Evidence quote or page reference: Results section and Table 2.
   - Effort: none
   - Risk if ignored: Adds unavailable or weakly supported feature complexity.

3. Suggested repo action: Add a future TODO for a separate severity module, not as part of the current Stage 2 frequency ranking.
   - Action type: small pilot / future model note
   - Relevant stage: future severity modelling
   - Why the paper supports it: Ordered response models are appropriate for slight/serious/fatal ordered outcomes.
   - Evidence quote or page reference: Pages 6–8.
   - Effort: medium
   - Risk if implemented badly: Fatal/serious classes are sparse and need aggregation/careful validation.

4. Suggested repo action: If WebTRIS crash-time diagnostics are attempted, assign traffic state before the crash, not at or after the crash time.
   - Action type: diagnostic design note
   - Relevant stage: Stage 1b / future severity diagnostic
   - Why the paper supports it: The paper uses a 30-minute lag to avoid the crash itself affecting traffic-state variables.
   - Evidence quote or page reference: Page 7.
   - Effort: low to medium
   - Risk if implemented badly: Sensor coverage and matching may be sparse.

5. Suggested repo action: Treat post-event STATS19 variables as off-limits for pre-event risk ranking.
   - Action type: methodological guardrail
   - Relevant stage: Stage 2 / documentation
   - Why the paper supports it: Its severity model uses crash-time/post-event features valid only because the model conditions on a crash.
   - Evidence quote or page reference: Table 1 and Table 3.
   - Effort: low
   - Risk if implemented badly: Leakage into production risk ranking.

6. Suggested repo action: For any severity module, test proportional-odds assumptions and compare OLOGIT with PC-GOLOGIT or related flexible models.
   - Action type: diagnostic / model comparison
   - Relevant stage: future severity model / validation
   - Why the paper supports it: Brant test found proportional-odds violation for traffic flow and number of vehicles.
   - Evidence quote or page reference: Page 11.
   - Effort: medium
   - Risk if implemented badly: More complex models may overfit sparse fatal outcomes.

## 16. Query Tags

- crash-severity
- ordered-logit
- generalized-ordered-logit
- PC-GOLOGIT
- heterogeneous-choice-model
- proportional-odds
- Brant-test
- heteroskedasticity
- M25
- motorway
- STATS19
- congestion
- total-delay
- traffic-flow
- traffic-speed
- 15-minute-traffic-data
- 30-minute-lag
- severity-conditional
- no-exposure-offset
- no-frequency-model
- curvature
- gradient
- lane-count
- wet-road-surface
- darkness
- single-vehicle
- post-event-leakage-risk

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: Clear publication year in manuscript metadata; held-out validation; external validation; treatment of missing traffic observations; exact crash-to-segment matching formula, which is referenced to Wang et al. (2009) rather than fully reproduced.
- Parts of the paper that need manual checking: Published version year and bibliographic details; exact Table 2/3 values if using for formal numeric reporting.
- Any likely ambiguity or risk of misinterpretation: This is a conditional severity model, not a crash-frequency model. Its traffic variables should not be interpreted as estimating crash occurrence risk. Crash-time/post-event variables are appropriate for explanatory severity analysis but would be leakage in Open Road Risk’s prospective link-risk ranking.
