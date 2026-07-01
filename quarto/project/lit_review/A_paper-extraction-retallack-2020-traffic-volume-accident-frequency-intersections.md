# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-07-01
- Source PDF filename: ijerph-17-01393.pdf
- Suggested Markdown filename: paper-extraction-retallack-2020-traffic-volume-accident-frequency-intersections.md
- AI tool used: ChatGPT
- Model name, if visible: not stated
- Model version, if visible: not stated
- Interface used: not stated
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The full uploaded PDF was accessible. No repository code or supplementary implementation files were provided beyond the project dossier.

## 1. Citation

- Title: Relationship Between Traffic Volume and Accident Frequency at Intersections
- Authors: Angus Eugene Retallack; Bertram Ostendorf
- Year: 2020
- DOI or URL, if present: 10.3390/ijerph17041393
- Country / region studied: Adelaide City Council area, South Australia, Australia
- Study setting: urban intersections

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper examines how hourly traffic volume, expressed both as raw flow and a within-intersection congestion index, relates to intersection accident frequency, and secondarily whether that relationship varies by rainfall and severity.
- Main purpose: descriptive analysis / other
- Evidence quote or page reference: "This study aims to analyse how traffic volumes affect accident frequency..." and "Separate analyses look at the effect of congestion on accident severity and the effects of rainfall on accident risk across these congestion levels." (p. 2)

## 3. Response Variable

- Target variable: Accident frequency counts within grouped intersection-congestion strata; secondary outcomes were severity-specific accident frequencies and rainfall-conditioned accident risks.
- Collision type: all crashes
- Severity handling: Main frequency analysis pooled motor vehicle crashes. Severity was later split into property damage only (PDO), minor injury (MI), and serious injury (SI), but SI was dropped because only 20 SI crashes had matched traffic volume data; there were no fatal intersection crashes in the study period.
- Count, binary, rate, risk score, severity class, or other: Count for the main models; risk and relative risk for rainfall analysis; severity-class descriptive comparison for PDO vs MI.
- Time window used for outcomes: Accidents from 2010-2014, with accident times rounded down to the previous hour to match hourly traffic measurements.
- Evidence quote or page reference: Accident times were "rounded down to the nearest hour to match the hourly timestamps of the traffic volume data" (p. 4). The joined dataset contained "a total of 1629 accidents" with associated traffic volumes (p. 5). Severity analysis details are on p. 7.

## 4. Exposure Handling

- Exposure variable used, if any: Hourly intersection traffic volume; additionally a 15-level within-intersection congestion index derived from quantile bins of each intersection's own traffic distribution.
- Traffic count source: Sydney Coordinated Adaptive Traffic System (SCATS) hourly intersection counts, publicly available through data.sa.gov.au.
- Whether exposure is modelled, observed, assumed, or ignored: Observed, but only at monitored intersections and only as total intersection hourly volume, not directional lane-group flow. The paper models traffic volume/congestion as the main explanatory quantity rather than an offset.
- Treatment of missing or sparse traffic counts: Two intersections with implausible near-zero medians were removed; long runs of repeated counts were treated as errors and removed; hourly counts were corrected by a sensor valid-ratio; lack of directional counts prevented standard v/c calculation.
- Whether offset terms, rates, denominators, or normalisation are used: No offset term was used in the count models. Traffic volume was normalized into 15 within-intersection quantile bins to create a congestion index. For rainfall analysis, accident risk was computed as accidents divided by the number of hourly periods in rain or no-rain conditions at each congestion level, and relative risk was the ratio of those risks.
- Evidence quote or page reference: SCATS hourly count source and lack of directional data are described on p. 4. Error correction and valid-ratio adjustment are on p. 5. The congestion-index normalization is described on p. 6. Rainfall risk denominators and relative risk equations are on p. 7.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The mathematical idea that exposure should be normalized for differing facility capacity is transferable. The paper's specific exposure source is less transferable because it depends on dense hourly signal-system intersection counts, not sparse annual link counts. The paper does not use an exposure offset of the kind in your Stage 2 model.

Important:

- Mathematical transferability: medium. The general idea of conditioning collision frequency on traffic exposure and normalizing across heterogeneous facilities is relevant.
- Data-source transferability: low to medium. Hourly SCATS counts at 120 monitored intersections are much richer and more localized than sparse AADF plus inferred profiles.

## 5. Spatial Unit of Analysis

- Unit: intersection
- Segment length or segmentation rule: Not stated; monitored signalized intersections were the analysis units.
- How crashes are assigned to the network: Crash points were spatially joined to intersection traffic-volume points within 20 m, then filtered to exact matched hour timestamps.
- Treatment of junctions/intersections: Junctions are the core study object; analysis is explicitly intersection-based rather than segment-based.
- Spatial aggregation risks: The study aggregates to 45 groups for the main modelling step (3 intersection-size ranks x 15 congestion levels), which suppresses intersection-level heterogeneity. The authors also note parsimonious models may omit heterogeneous covariates.
- Evidence quote or page reference: 120 intersections are described on pp. 1, 4. The 20 m spatial join is on p. 5. The grouping into 45 strata is on p. 6.
- Relevance to OS Open Roads link-based pipeline: Limited direct compatibility. It is useful for junction-focused diagnostics, but it does not map cleanly onto OS Open Roads link-year modelling without a separate junction representation.

## 6. Temporal Unit of Analysis

- Years covered: 2010-2014 for the joined crash-traffic analysis; rainfall series available from 1995-2015 but joined to the study period.
- Temporal resolution: hourly
- Whether seasonality or time-of-day is modelled: Time-of-day is only used indirectly through hourly matching; no explicit seasonality model is stated.
- Whether before-after or panel structure is used: no
- Evidence quote or page reference: The traffic data span 2010-2014 at 60-minute resolution (pp. 4-5). Accidents were rounded to the prior hour (p. 4). Rainfall was available at 30-minute resolution (p. 5).
- Relevance to WebTRIS-style time profiles: Conceptually relevant. The paper shows value in higher temporal-resolution exposure alignment, but it does not provide a reusable link-based temporal weighting framework for sparse open-data national-scale modelling.

## 7. Engineered Features

List the most important engineered features, especially those I could recreate.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Corrected hourly intersection volume | SCATS counts | Multiplied each hourly count by the "valid ratio" derived from the provided error ratio | Reduces sensor-count error in the core exposure variable | Low - requires comparable sensor QA metadata |
| Congestion index (1-15) | Hourly intersection volume | Within each intersection, assigned each hourly measurement to one of 15 quantile bins | Normalizes traffic conditions across intersections with different capacities | Medium conceptually; compare implementation for node-based diagnostics, not direct link-year production |
| Intersection size rank | Median intersection traffic volume | Grouped intersections into low-, middle-, and high-volume ranks | Lets the study compare volume-frequency shape across facility size classes | Medium for diagnostics if you build a junction layer |
| Rain / no-rain indicator | BOM rainfall data | Joined rainfall periods to traffic periods and stratified accident counts by weather condition | Supports relative-risk analysis under weather exposure | Medium; weather joins are feasible if suitable UK temporal weather data are available |
| Severity grouping (PDO / MI / SI) | Crash records | Filtered crashes by severity class | Tests whether congestion-frequency patterns differ by severity | Already present / compare implementation if you run severity-specific diagnostics |
| Prior-hour crash matching | Crash timestamps + hourly traffic timestamps | Rounded accident time down to the previous hour before joining | Avoids using traffic counts potentially affected by the crash itself | High; this is a clean anti-post-event-leakage rule for high-frequency exposure matching |
| 20 m spatial assignment rule | Crash coordinates + intersection coordinates | Spatial join within 20 m | Operational rule for attaching events to monitored junctions | Medium for junction diagnostics; threshold choice would need UK-specific validation |

Only features actually used in the paper are listed.

## 8. Model Architecture

- Algorithms/models used: Poisson generalized linear models; negative binomial models where overdispersion was detected; quadratic and natural-spline variants; loess smoothing for visualization.
- Baseline model: Linear count model of accident frequency ~ traffic volume.
- Final/preferred model: Quadratic Poisson model for low-volume intersections; quadratic negative binomial model for middle-volume intersections; for high-volume intersections the quadratic and natural-spline negative binomial models were both supported, with weak preference for quadratic by AICc.
- Loss function or likelihood, if stated: Poisson and negative binomial count likelihoods are implied; exact estimation details are not otherwise stated.
- Offset/exposure term, if used: Not stated / none used in the frequency models.
- Spatial autocorrelation handling: Not stated.
- Temporal dependence handling: Not stated.
- Interpretability method: Functional-form comparison (linear vs quadratic vs spline), AICc model ranking, dispersion testing, and visual loess/regression plots.
- Evidence quote or page reference: Model forms and AICc selection are given on p. 6. Overdispersion testing and model preference results are on p. 8.

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Sample construction | Matched crash count | 1629 | Joined accident-volume dataset | Final number of crashes with matched hourly traffic volumes | p. 5 |
| Dispersion diagnostic | Dispersion ratio | 1.37; p = 0.164 | Low-volume intersections, Poisson fit | No strong evidence of overdispersion | p. 8, Table 4 |
| Dispersion diagnostic | Dispersion ratio | 3.77; p < 0.001 | Middle-volume intersections, Poisson fit | Overdispersion present; negative binomial preferred | p. 8, Table 4 |
| Dispersion diagnostic | Dispersion ratio | 3.25; p < 0.001 | High-volume intersections, Poisson fit | Overdispersion present; negative binomial preferred | p. 8, Table 4 |
| Model comparison | AICc | 69.3 | Low-volume quadratic | Best-supported low-volume model | p. 8, Table 5 |
| Model comparison | Delta AICc | 5.8 vs spline; 9.3 vs linear | Low-volume quadratic vs alternatives | Stronger support for quadratic non-linearity than spline or linear-only | p. 8, Table 5 |
| Model comparison | Evidence ratio | 17.7 | Low-volume quadratic | Substantially favored over next-best model | p. 8, Table 5 |
| Model comparison | AICc | 108.1 | Middle-volume quadratic | Best-supported middle-volume model | p. 8, Table 5 |
| Model comparison | Delta AICc | 4.9 vs spline; 9.2 vs linear | Middle-volume quadratic vs alternatives | Supports non-linear quadratic shape | p. 8, Table 5 |
| Model comparison | Evidence ratio | 11.5 | Middle-volume quadratic | Substantially favored over next-best model | p. 8, Table 5 |
| Model comparison | AICc | 119.1 | High-volume quadratic | Slightly better than spline, but not decisive | p. 8, Table 5 |
| Model comparison | Delta AICc | 1.2 vs spline; 7.8 vs linear | High-volume quadratic vs alternatives | Non-linear models clearly beat linear, but quadratic vs spline is ambiguous | p. 8, Table 5 |
| Rainfall relative risk | Relative risk | Approximately 5 at congestion level 1 | Rain vs no rain | Rain-associated accident risk much higher at low congestion | pp. 10-11, Figure 5 and text |
| Rainfall relative risk | Relative risk | Approaches 1 at congestion level 15 | Rain vs no rain | Rain penalty falls toward none at highest congestion | pp. 10-11, Figure 5 and text |
| Severity comparison | MI/PDO ratio trend | No clear change | Across congestion levels | No significant congestion effect on severity composition detected | pp. 9-10, Figure 4 and text |

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? In-sample model-comparison and descriptive diagnostics. No train/test split, cross-validation, spatial holdout, temporal holdout, or external validation is stated.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. These are in-sample diagnostics and model-comparison statistics, not demonstrated predictive accuracy.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? Mostly model fit / functional-form comparison and descriptive risk-pattern analysis.
- Are any metrics likely to be optimistic for real-world deployment? Yes. All apparent performance claims are optimistic for deployment because there is no held-out evaluation and the study is tightly localized.
- Which metric, if any, is most relevant to Open Road Risk? The overdispersion diagnostics and the qualitative comparison between linear and non-linear count responses are more relevant than the AICc values themselves. The paper is more useful for structural reasoning than for transferable performance benchmarks.

Important:

- The paper does not report usable out-of-sample predictive validation.
- AICc and dispersion tests do not establish deployment-ready predictive skill.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The paper addresses rarity by combining long temporal coverage, 120 intersections, and more than 5 million hourly traffic measurements so enough matched crashes are available for count modelling.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson for low-volume grouped counts; negative binomial for middle- and high-volume grouped counts after overdispersion checks. No zero-inflated or hurdle model is used.
- Whether high-risk locations are evaluated separately: Not as hotspot ranking. The study stratifies by intersection size and congestion level rather than estimating location-specific risk rankings.
- Evidence quote or page reference: The rarity rationale is discussed on p. 2 and p. 12. Model choices are on pp. 6 and 8.
- Practical relevance to my sparse collision link-year dataset: Moderately relevant. The paper reinforces that overdispersed count models are sensible when modelling rare crash counts, but it does not directly solve link-year sparsity or the very high share of zero rows in your Stage 2 table.

## 11. Validation Strategy

- Train/test split method: Not stated
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Not stated
- Metrics: Dispersion statistics, AICc, evidence ratios, descriptive figure-based risk comparisons, and relative risk values
- External validation: no
- Leakage or generalisation risks: Strong risk of overinterpreting in-sample fit as generalizable. The study uses matched accident-hour and traffic-hour data from the same localized setting and does not test transfer across intersections, years, or cities. There is no obvious classic leakage in the hourly matching rule; rounding down to the previous hour is actually a protective design choice. The larger limitation is weak external generalisation.
- Evidence quote or page reference: The fitting and comparison setup is on pp. 6-8; no separate validation section is provided.
- What I should copy or avoid: Copy the anti-post-event rule of using prior-hour traffic conditions when matching high-frequency exposure to crashes. Avoid treating AICc-selected in-sample functional form as proof of predictive superiority in your production pipeline.

## 12. Key Findings Relevant to My Project

For each finding:

- Finding: In this case study, accident frequency rose roughly linearly through most of the traffic range but increased faster in the highest congestion conditions, especially in middle- and high-volume intersections.
- Why it matters: This supports testing non-linear exposure-response structure around high-congestion conditions rather than assuming a globally linear relationship.
- Evidence quote or page reference: The paper reports a "significant quadratic explanatory term" at high traffic volumes in the abstract (p. 1) and AICc support for non-linear models in Table 5 (p. 8).
- Confidence: medium

- Finding: The study treats facility comparability as an exposure-normalization problem and replaces conventional v/c ratios with a within-intersection congestion index because geometry and signal data were unavailable.
- Why it matters: That is relevant to open-data settings where ideal engineering covariates are missing. It suggests that practical normalization proxies can still be informative, though they are facility-type-specific.
- Evidence quote or page reference: The v/c limitation and 15-bin congestion-index construction are described on p. 6.
- Confidence: high

- Finding: Rain-associated crash risk was much higher at low congestion and diminished as congestion rose, approaching no extra relative risk at the highest congestion level.
- Why it matters: This suggests weather effects may interact with traffic state rather than acting as a single global multiplier.
- Evidence quote or page reference: Relative risk was "approximately five" at congestion level 1 and approached 1 at level 15 (pp. 10-11).
- Confidence: medium

- Finding: No clear congestion effect on PDO vs minor-injury mix was observed in this dataset.
- Why it matters: For your repo, this is a warning not to assume that exposure/congestion effects on crash frequency automatically imply transferable effects on severity composition.
- Evidence quote or page reference: "No significant effect of congestion index on accident severity was detected" (abstract, p. 1); see also Figure 4 discussion on pp. 9-10.
- Confidence: medium

- Finding: The study gets usable signal from a parsimonious model because it has high-frequency exposure data and a localized, relatively homogeneous study area.
- Why it matters: This supports careful scope control. What works for a compact urban intersection sample may not scale cleanly to multi-region link-year modelling without stronger validation.
- Evidence quote or page reference: The authors attribute detectability partly to "5.2 million data points" and the "increased homogeneity of the highly localized study area" (p. 12).
- Confidence: high

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Test non-linear exposure-response terms or splines in count-risk diagnostics | The paper suggests accident frequency may accelerate in the highest congestion/volume regime rather than staying linear | Link-level exposure estimates, collision counts, facility grouping | 120 intersections; 1629 matched crashes; 2010-2014 | Medium - computationally feasible if done on sampled diagnostics or compact GLM variants, but interpretation differs for links vs intersections | Stage 2 / validation | Medium | Spurious curvature from estimated exposure error or facility-mix confounding |
| Add or document anti-post-event temporal matching rules where high-frequency auxiliary data are used | Clean methodological guardrail against using traffic conditions affected by the crash itself | Crash timestamps plus high-frequency sensor/profile data | Hourly matched intersection data | High - directly compatible in any future hourly diagnostic work | validation / documentation / Stage 1b future linkage | Low | False confidence if timestamp quality is weak |
| Build a junction-focused pilot layer rather than forcing intersection logic directly into link-year production | The paper is genuinely about intersections, not road segments | Junction geometry, snapped collision allocation, optional traffic/junction proxies | 120 monitored intersections | Medium - suitable as a pilot or sidecar diagnostic, not as a drop-in main-table replacement | future feature / validation | Medium to high | Poor transfer if junction assignment is noisy |
| Explore interaction diagnostics between weather and traffic state | The paper suggests weather risk is state-dependent, not constant | Weather joins, exposure state or temporal profile state, collision records | 15 congestion levels with rain/no-rain comparison | Medium - possible for targeted diagnostics or temporal-risk outputs | Stage 1b / Stage 2 diagnostic | Medium | Weak signal and heavy confounding by geography, season, and measurement timing |
| Document limitations of using simple annual counts without facility-capacity normalization | The paper explicitly shows why raw volumes are not comparable across differently sized intersections | Existing repo docs only | 120 intersections | High - easy documentation win | documentation | Low | Overstating direct comparability to link-based AADT offset modelling |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Direct use of hourly SCATS-style intersection volumes as the primary exposure variable | Your pipeline does not have dense observed hourly counts for every road link or junction | Complete monitored intersection-hour flows; signal-system data | 120 monitored intersections in one city | Low | Approximate temporal state using WebTRIS-derived profiles and estimated AADT, but that is not the same information | High |
| Within-intersection quantile congestion index as a production-wide core exposure metric | It depends on repeated high-frequency observations per facility and is built for monitored intersections, not millions of mostly unmonitored links | Full hourly volume distributions for each unit | 120 intersections | Low for production; maybe medium for small pilots | Use link-class or facility-family normalization proxies instead | High |
| Treating in-sample AICc-selected quadratic form as enough evidence for production model change | The paper has no held-out predictive validation | Validation design | Single localized study | Low | Use it only as a hypothesis for baseline comparison | High |
| Porting intersection findings directly to OS Open Roads link-year risk without a junction model | The study unit is the junction, where conflict structure is different from mid-link segments | Junction-specific representation and assignment logic | Urban monitored intersections | Low | Run a separate junction-risk pilot or add junction-complexity features instead | High |

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Partly. It strongly supports the general idea that crash frequency should be interpreted relative to traffic exposure and facility capacity/context, but it does not test a link-length x AADT offset structure like your Stage 2 model.
- Does it suggest better handling of AADT/AADF uncertainty? Only indirectly. It shows the value of richer temporal exposure data and explicit acknowledgement of unavailable ideal traffic measures, but it does not provide a method for propagating AADT estimation uncertainty.
- Does it suggest useful geometry or road-context features? Only in a negative sense: the paper explains that signal timing, directional flows, and intersection geometry would matter for ideal v/c measurement, but they were unavailable and not modelled.
- Does it suggest better modelling of junctions? Yes. It suggests junctions may need dedicated treatment rather than being folded invisibly into generic segment models.
- Does it suggest better treatment of severity? Weakly. It suggests congestion-frequency effects did not clearly translate into PDO-vs-MI differences in this case study, so severity should be tested separately rather than assumed.
- Does it suggest better validation design? Yes, mostly by omission. The paper is a reminder not to rely on in-sample AICc/model fit when choosing production models for large-scale deployment.
- Does it expose a weakness in my current approach? It highlights a likely blind spot if junction-specific congestion or capacity effects are important but your main unit remains generic OS Open Roads links without explicit junction representation.

## 15. Repo Actionability

For each:

- Suggested repo action: Add a documentation note distinguishing your exposure-offset framework from junction-level congestion-state analysis, and record that this paper supports the latter only indirectly.
- Action type: documentation note
- Relevant stage: documentation / Stage 2
- Why the paper supports it: The paper uses observed hourly intersection flow and congestion bins, not a link-year offset model.
- Evidence quote or page reference: Exposure normalization and congestion-index construction are described on p. 6.
- Effort: low
- Risk if implemented badly: Conceptual confusion between link exposure offsets and junction-state diagnostics.

- Suggested repo action: Run a small diagnostic comparing linear vs non-linear exposure-response structure in Stage 2 GLM variants, especially in upper exposure ranges or by facility family.
- Action type: small pilot
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Non-linear models beat linear-only models in this case study, especially at high congestion/volume.
- Evidence quote or page reference: Table 5 on p. 8 and discussion on p. 12.
- Effort: medium
- Risk if implemented badly: You may fit curvature caused by exposure-estimation error, spatial confounding, or road-class mix rather than true risk dynamics.

- Suggested repo action: Preserve or strengthen rules that avoid post-event leakage when linking any high-frequency temporal covariates to crash events.
- Action type: diagnostic
- Relevant stage: validation / Stage 1b future linkage
- Why the paper supports it: The study rounds accident times down to the prior hour specifically so the traffic measure is not affected by the accident itself.
- Evidence quote or page reference: p. 4
- Effort: low
- Risk if implemented badly: Misaligned timestamps can still create hidden contamination or attenuate signal.

- Suggested repo action: Create a junction-focused pilot dataset for a limited region to test whether explicit junction context materially improves residual diagnostics or risk ranking.
- Action type: small pilot
- Relevant stage: future feature / validation
- Why the paper supports it: The entire signal in the paper is intersection-based and may not be recoverable from generic mid-link modelling.
- Evidence quote or page reference: Study objective and unit are explicitly 120 intersections (pp. 1-2, 4).
- Effort: high
- Risk if implemented badly: Noisy crash-to-junction assignment and duplicate attribution around closely spaced nodes.

- Suggested repo action: Test weather x traffic-state interaction as a diagnostic analysis rather than a production feature change.
- Action type: diagnostic
- Relevant stage: Stage 1b / Stage 2 / validation
- Why the paper supports it: Relative rainfall risk changed materially across congestion levels in this case study.
- Evidence quote or page reference: Figure 5 and text on pp. 10-11.
- Effort: medium
- Risk if implemented badly: Interaction estimates may be unstable and confounded by route type, season, and exposure mismeasurement.

## 16. Query Tags

- traffic-volume
- hourly-counts
- intersections
- congestion-index
- SCATS
- accident-frequency
- Poisson-GLM
- negative-binomial
- overdispersion
- quadratic-effect
- nonlinear-response
- rainfall-risk
- relative-risk
- severity-analysis
- urban-intersections
- spatiotemporal-join
- prior-hour-matching
- junction-modelling
