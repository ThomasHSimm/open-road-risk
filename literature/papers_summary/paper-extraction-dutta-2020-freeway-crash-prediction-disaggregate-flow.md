# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: dot_54482_DS1.pdf
- Suggested Markdown filename: paper-extraction-dutta-2020-freeway-crash-prediction-disaggregate-flow.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The PDF text was available, but some tables and figures were parsed imperfectly. Key results were checked against parsed text and visible page images where available.

## 1. Citation

- Title: Improving Freeway Crash Prediction Models Using Disaggregate Flow State Information
- Authors: Nancy Dutta; Michael D. Fontaine
- Year: 2020
- DOI or URL, if present: http://www.virginiadot.org/vtrc/main/online_reports/pdf/20-r15.pdf
- Country / region studied: United States / Virginia
- Study setting: motorway / freeway; mixed rural and urban freeway segments

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The report develops freeway crash prediction models using sub-daily traffic volume and flow-state variables, then compares them with AADT-based crash prediction models.
- Main purpose: safety performance function / prediction / model comparison
- Evidence quote or page reference: Abstract, page iii: "This study developed a methodology for creating crash prediction models using traffic, geometric, and control information that is provided at sub-daily aggregation intervals." Purpose and Scope, page 2: the first objective was to "Determine whether sub-daily crash predictions models can provide better safety predictions than AADT-based models".

## 3. Response Variable

- Target variable: Crash frequency on basic freeway segments.
- Collision type: total crashes; fatal and injury crashes.
- Severity handling: Severity is handled by estimating separate models for total crashes and fatal/injury crashes. Fatal and injury crashes are combined; injury severity is not separately modelled.
- Count, binary, rate, risk score, severity class, or other: Count.
- Time window used for outcomes: Crash data from 2011–2017; models are estimated at annual, average hourly, average 15-minute, and raw hourly aggregation variants, with hourly predictions converted to annual values for validation.
- Evidence quote or page reference: Crash Data section, page 5: "For all the segments, crash information was also collected from 2011-2017. For this analysis, the researchers examined total crashes as well as fatal and injury crashes." Model Validation section, page 12: hourly predictions were summed or averaged and annualised so GOF comparisons could be made consistently.

## 4. Exposure Handling

- Exposure variable used, if any: AADT in baseline models; average hourly volume, average 15-minute volume, and raw hourly volume in disaggregate models. Segment length is used as an offset.
- Traffic count source: VDOT continuous count stations and short count stations.
- Whether exposure is modelled, observed, assumed, or ignored: Observed traffic volume from count stations; short-count stations provide partial-period observed data used to construct average volumes. The paper does not train a separate traffic-imputation model in the way Open Road Risk does for AADT.
- Treatment of missing or sparse traffic counts: Raw hourly data with missing quality-screened observations performed poorly. Average hourly volumes smoothed missing-data issues. Short count stations were tested explicitly and found not to diminish model quality when combined with speed-related variables.
- Whether offset terms, rates, denominators, or normalisation are used: Segment length is used as an offset variable; volume is included as a predictor/exposure term rather than as a pure offset.
- Evidence quote or page reference: Methods, page 13: "To be consistent with the HSM, length was used as an offset variable in the models." Conclusions, pages 38–39: "Models using raw hourly data were inferior..." and "Using averages of available data in each hour improved the model performance significantly over AADT models." Conclusions, page 39: short-count inclusion improved MAD/MSPE for rural and urban segments.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The mathematical idea of using time-disaggregated traffic exposure is highly transferable to Open Road Risk's WebTRIS-style time-profile work. The exact data arrangement is only partly transferable because this report uses freeway detector volume and speed data tied to homogeneous freeway segments. Open Road Risk has sparse AADF and WebTRIS-style data, not complete hourly volume for every OS Open Roads link. The most transferable element is the validation question: compare AADT-only exposure against average-hourly exposure profiles before using temporal weighting in production.

Important:

- The exposure structure is more transferable than the paper's data availability.
- The paper supports an average-hourly representation over raw hourly data where raw hourly data are incomplete.

## 5. Spatial Unit of Analysis

- Unit: directional basic freeway segment.
- Segment length or segmentation rule: Homogeneous freeway segments surrounding detector stations; selected so that no entry/exit ramps were within 0.5 miles of segment start/end; if homogeneous section exceeded 2 miles, a maximum 1 mile upstream/downstream buffer around detector location was used.
- How crashes are assigned to the network: Crashes were obtained from VDOT's Roadway Network System for the selected segments.
- Treatment of junctions/intersections: Ramps and interchanges were excluded; only basic freeway segments were included.
- Spatial aggregation risks: The freeway segment/detector-unit design is cleaner than OS Open Roads link segmentation but is less transferable to dense all-road networks. The report uses VDOT district as a coarse spatial random-effect grouping, not local adjacency or network-neighbour smoothing.
- Evidence quote or page reference: Data Collection and Preparation, pages 3–5: "Only homogeneous basic freeway segments that had volume data and were free from ramps or interchanges were considered for modeling." Page 15: district random effects are used to account for spatial correlation.
- Relevance to OS Open Roads link-based pipeline: Medium. The modelling logic can inform motorway/trunk-road submodels or temporal exposure diagnostics. It is not directly compatible with raw OS Open Roads links without aggregation or careful handling of detector-to-link representativeness.

## 6. Temporal Unit of Analysis

- Years covered: 2011–2017.
- Temporal resolution: Annual AADT baseline; raw hourly; average 15-minute; average hourly.
- Whether seasonality or time-of-day is modelled: Time of day is represented through average hourly or average 15-minute volumes and speed variables. The GLMM variant includes random effects for year and hour.
- Whether before-after or panel structure is used: Panel data structure is used because the same sites appear repeatedly over multiple years.
- Evidence quote or page reference: Selection of Data Structure, page 5: "Because of these benefits, the crash data used in this study were analyzed as panel data." Experimental Design, page 13: volume was examined at raw hourly, average 15-minute, average hourly, and AADT intervals.
- Relevance to WebTRIS-style time profiles: High as a validation/design reference. The paper gives direct support for average-hourly traffic representations and warns that raw hourly data can be worse when data quality is incomplete.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| AADT | VDOT count stations | Annual average daily traffic baseline | Baseline exposure model comparable to HSM-style SPF | Already present / compare implementation |
| Average hourly volume | VDOT continuous and short count stations | Average data for each hour of day for each site/year | Captures within-day exposure variation while smoothing missing raw data | High conceptually; implement via WebTRIS-style profile × AADT |
| Average 15-minute volume | VDOT count stations | Average data for each 15-minute period | Tested whether finer temporal aggregation improved crash prediction | Medium; likely not currently available at network scale |
| Raw hourly volume | VDOT count stations | Observed hourly volumes each day | Tested highly disaggregate exposure; performed poorly with missing data | Low-to-medium; use mainly as warning/diagnostic |
| Average hourly speed | Continuous count stations and INRIX probe speed | Aggregated to selected temporal interval | Flow-state proxy; improved prediction when added with volume | Medium; OSM/free-flow and limited probe data may substitute only partly |
| Speed standard deviation | Speed data | Standard deviation of hourly speed | Captures variability in flow quality | Medium; needs reliable speed distribution data |
| Difference between speed limit and average speed | Speed limit plus speed data | Speed-limit minus average-speed difference | Operational congestion/speed-state signal | Medium; possible where observed/probe speeds are available |
| Segment length | VDOT geometry | Used as offset | Normalises crash counts by segment exposure length | Already present / compare implementation |
| Horizontal curvature | VDOT curvature database | Radius and length/presence of curve measures | Geometric crash-risk feature | Already present / compare implementation with curvature feature |
| Vertical curvature / grade | VDOT geometry | Difference in slope and length of curve, expressed as percent grade | Geometry/slope risk feature | Candidate validation/comparison for OS Terrain 50 grade |
| Median width | VDOT geometry | Segment-level width | Road cross-section context | Partly transferable; OS Open Roads lacks reliable width |
| Shoulder width | VDOT geometry | Segment-level median/right shoulder width | Roadside/cross-section context | Low-to-medium; not consistently available in UK open data |
| Speed limit | VDOT traffic control data | Segment-level posted speed | Baseline operating/control characteristic | Already present partly via OSM / compare coverage |

Only features actually used or tested in the paper are included.

## 8. Model Architecture

- Algorithms/models used: Negative binomial generalized linear models; zero-inflated negative binomial models tested; generalized linear mixed models with random effects for district, year, and hour.
- Baseline model: AADT-based model with volume, segment length, and geometric variables.
- Final/preferred model: Average-hourly volume, geometry, and speed/flow-state negative binomial or GLMM models, with continuous and short count stations included.
- Loss function or likelihood, if stated: Maximum likelihood estimation for negative binomial / GLM / GLMM models.
- Offset/exposure term, if used: Segment length offset.
- Spatial autocorrelation handling: District-level random intercept used as a coarse spatial random effect.
- Temporal dependence handling: Year and hour random effects in GLMM variants.
- Interpretability method: Coefficient estimates, goodness-of-fit / validation metrics, and CURE plots.
- Evidence quote or page reference: Model Form section, pages 5–10: negative binomial, ZINB, GLM, and GLMM structures are described. Page 15: random effects by district, year, and hour. Page 17: validation uses MAPE, MAD, MSPE, and CURE plots.

## 9. Reported Metrics / Quantitative Results

Extract the main quantitative results reported in the paper.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---:|---:|---|---|---|
| Study scale | Rural segments | 110 segments, 195.07 miles | Rural 4-lane directional freeway segments | Moderate freeway sample | Table 1, page 22 |
| Study scale | Urban segments | 80 segments, 125.42 miles | Urban 6-lane directional freeway segments | Moderate freeway sample | Table 1, page 22 |
| Temporal aggregation | MAD / MAPE / MSPE improvement | 20% / 22% / 38% | Urban total crashes; average hourly volume + geometry + flow vs AADT | Average hourly flow-state model improved out-of-sample validation metrics over AADT model | Conclusions, page 39; Table 6, page 37 |
| Temporal aggregation | MAD / MAPE / MSPE improvement | 11% / 33% / 29% | Rural total crashes; average hourly volume + geometry + flow vs AADT | Average hourly flow-state model improved validation metrics over AADT model | Conclusions, page 39; Table 5, page 31 |
| Temporal aggregation | MAD / MAPE / MSPE improvement | 10% / 16% / 25% | Rural continuous-count fatal/injury crashes; average hourly flow-state vs AADT | Improvement over AADT, but smaller than total-crash improvement | Page 31 |
| Temporal aggregation | MAD improvement | 9% | Urban fatal/injury crashes; average hourly flow-state vs AADT | Abstract reports 9% MAD improvement for injury crashes | Abstract, page iii |
| Short counts | MAD / MSPE improvement | 52% / 72% | Rural hourly models; continuous+short counts vs continuous-count-only | Adding short counts improved model quality substantially | Table 11, page 38 |
| Short counts | MAD / MSPE improvement | 58% / 27% | Urban hourly models; continuous+short counts vs continuous-count-only | Adding short counts improved model quality substantially | Table 11, page 38 |
| Spatial/temporal correlation | MAD / MSPE improvement | 14% / 17% | Rural; correlation model vs same dataset without correlation | Correlation handling helped, but less than adding short counts | Conclusions, page 39 |
| Spatial/temporal correlation | MAD / MSPE improvement | 21% / 43% | Urban; correlation model vs same dataset without correlation | Correlation handling helped more for urban locations than rural | Conclusions, page 39 |
| Final rural GLMM comparison | MAD / MAPE / MSPE | 1.11 / 43% / 2.59 | Rural total crashes, average hourly volume + geometry + flow | Better than AADT model and volume+geometry-only hourly model | Table 9, page 36 |
| Final rural GLMM comparison | MAD / MAPE / MSPE | 0.66 / 28% / 1.39 | Rural fatal/injury crashes, average hourly volume + geometry + flow | Better than AADT and volume+geometry-only hourly model | Table 9, page 36 |
| Final urban GLMM comparison | MAD / MAPE / MSPE | 1.45 / 29% / 36.95 | Urban total crashes, average hourly volume + geometry + flow | Better than AADT and volume+geometry-only hourly model | Table 10, page 37 |
| Final urban GLMM comparison | MAD / MAPE / MSPE | 0.93 / 8% / 3.63 | Urban fatal/injury crashes, average hourly volume + geometry + flow | Better than AADT and volume+geometry-only hourly model | Table 10, page 37 |
| Model form | Vuong / model selection | Negative binomial selected for consistency | Most model categories | ZINB usually not preferred; injury raw-hourly exception noted but not carried forward | Page 23; Appendix C |
| Model diagnostics | CURE plots | Within ±2 standard deviation limits | Average hourly volume in volume-flow-geometry models | Supports functional form for average-hourly volume | Figure 6, page 35 |

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? The main predictive validation uses a random 70% model-building / 30% testing split. It is out-of-sample by random split, not spatially held out and not temporally held out.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. The CURE plots and information criteria are in-sample diagnostics. MAD/MAPE/MSPE are reported for validation data and are the most relevant predictive metrics.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? MAD/MAPE/MSPE test random-split predictive performance. AIC/BIC/log-likelihood and CURE plots assess model fit/functional form. They do not directly test hotspot ranking.
- Are any metrics likely to be optimistic for real-world deployment? Yes. The 70/30 split is random, not spatial or temporal. It may be optimistic for new corridors, new regions, or future years with changed traffic patterns. District random effects also use broad grouping rather than truly held-out spatial transfer.
- Which metric, if any, is most relevant to Open Road Risk? MAD/MSPE improvements comparing AADT-only against average-hourly volume + flow-state models are most relevant, especially as a validation pattern for Stage 1b temporal exposure weighting.

Important:

- Do not treat AIC/BIC/CURE plots as external predictive validation.
- The validation is useful, but weaker than a spatial or temporal holdout.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Count models are used. Negative binomial models are selected as the consistent preferred form. ZINB models are tested because disaggregated data create more zero observations, but generally not selected.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Negative binomial and zero-inflated negative binomial are tested; negative binomial is selected for most models.
- Whether high-risk locations are evaluated separately: Not stated. The focus is prediction model performance, not hotspot/ranking evaluation.
- Evidence quote or page reference: Page 6: the report states that more disaggregate temporal aggregation is expected to create more zero crash observations and that both negative binomial and ZINB forms were developed. Page 23: negative binomial models were selected for both total and injury crashes to maintain consistency.
- Practical relevance to my sparse collision link-year dataset: High as a caution. The report explicitly tests zero-inflated models rather than assuming them. For Open Road Risk, the relevant copyable practice is to test whether zero-heavy link-year data actually require a zero-inflated model rather than using the label loosely.

Important:

- The paper explicitly uses zero-inflated negative binomial candidate models, so `zero-inflated` is a valid tag for this paper.
- The preferred production-like model is not zero-inflated.

## 11. Validation Strategy

- Train/test split method: Random 70% model-building / 30% testing split.
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no, not as the main validation split; district/year/hour random effects were used in GLMMs to account for correlation.
- Cross-validation type: Not stated.
- Metrics: MAPE, MAD, MSPE; CURE plots for functional form; AIC/BIC/log-likelihood for model selection; Vuong tests for NB vs ZINB comparisons.
- External validation: no
- Leakage or generalisation risks: No clear classic leakage is described. However, random splits and district/year/hour random effects may make generalisation appear better than true deployment to new regions or future years. Since the data are panel-like, random splitting may put related site/time observations in both train and test.
- Evidence quote or page reference: Model Validation, page 12: "Model building used a random selection of 70% of the available data; the remaining 30% was used for testing and validation." Page 15: models cluster data by district, year, and hour.
- What I should copy or avoid: Copy the direct comparison between AADT and average-hourly exposure, the explicit testing of ZINB vs NB, and CURE plots for functional form. Avoid treating random-split gains as proof of spatial or temporal generalisation.

Important:

- The correlation modelling is not a leakage error by itself; it is an in-sample/panel generalisation limitation unless tested on held-out regions or periods.

## 12. Key Findings Relevant to My Project

### Finding 1

- Finding: Average-hourly volume models outperformed AADT-based models across validation measures, whereas raw hourly models were inferior when data were missing.
- Why it matters: This directly supports testing WebTRIS-style average time-profile exposure rather than raw high-frequency traffic data for Open Road Risk.
- Evidence quote or page reference: Conclusions, pages 38–39: "Models using raw hourly data were inferior..." and "For both rural and urban segments, models based on average hourly data outperformed the AADT-based models across all MOEs."
- Confidence: high

### Finding 2

- Finding: Adding speed/flow-state variables improved crash prediction across validation measures.
- Why it matters: Open Road Risk currently has candidate speed-limit and temporal profile features; this paper supports piloting speed/flow-state diagnostics where observed or proxy speed data are available.
- Evidence quote or page reference: Abstract, page iii: average hourly speed, speed standard deviation, and speed-limit/average-speed difference had statistically significant relationships with crash frequency; predictions improved when speed components were added.
- Confidence: high

### Finding 3

- Finding: Probe speed data and detector speed data produced similar results in this freeway setting.
- Why it matters: This suggests that if direct speed observations are unavailable, probe-like speed sources may still be usable for a pilot, but this is not the same as OSM posted speed limits.
- Evidence quote or page reference: Conclusions, page 38: "Speeds from both continuous count stations and probe data provided similar results."
- Confidence: medium

### Finding 4

- Finding: Adding short count stations improved model performance, despite lower data completeness than continuous count stations.
- Why it matters: This is relevant to Open Road Risk's sparse AADF/WebTRIS environment: broader but imperfect count coverage may be more useful than a tiny set of pristine sites, provided quality checks are explicit.
- Evidence quote or page reference: Table 11, page 38; conclusions, page 39: rural MAD/MSPE improved 52%/72%; urban MAD/MSPE improved 58%/27% when short counts were added.
- Confidence: high

### Finding 5

- Finding: Spatial and temporal correlation modelling improved fit, but added less benefit than expanding the dataset with short counts in this case.
- Why it matters: For Open Road Risk, this suggests first improving exposure/data coverage and validation before investing heavily in complex correlation structures.
- Evidence quote or page reference: Conclusions, page 39: correlation models improved MAD/MSPE by 14%/17% for rural and 21%/43% for urban, but benefits were smaller than short-count inclusion for rural sites.
- Confidence: medium

### Finding 6

- Finding: The study is limited to Virginia freeway basic segments and does not cover junctions, arterials, rural local roads, or full-network road-link analysis.
- Why it matters: The paper is strongly relevant to motorway/trunk-road exposure modelling, but should not be overgeneralised to all OS Open Roads links.
- Evidence quote or page reference: Scope, page 3: the study was limited to two-lane rural freeway directional segments and three-lane urban freeway directional segments.
- Confidence: high

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Compare AADT-only exposure against average-hourly profile exposure | Directly tests whether temporal exposure weighting improves collision prediction | AADT estimates; WebTRIS-derived hourly fractions; link-year crashes | 110 rural + 80 urban freeway segments, 2011–2017 | Medium; very relevant for motorways/major roads, weaker for minor roads | Stage 1b / Stage 2 / validation | medium | Apparent improvement may reflect WebTRIS site bias rather than general link behaviour |
| Use segment length as offset and time-disaggregated volume as exposure predictor | Similar to current exposure-offset logic but tests temporal granularity | Link length; volume/exposure profile | Freeway segments | High mathematically, medium practically | Stage 2 / validation | low-to-medium | Double-counting exposure if not clearly separated from offset |
| Test speed/flow-state variables as diagnostics | Paper finds speed variables improve prediction | Speed limit; observed/probe speed if available; average speed by period | Freeway segments | Medium; observed speed data may be limited | future feature / validation | medium | OSM speed limit is not equivalent to observed speed |
| CURE plots for exposure variables | Functional-form diagnostic for volume/exposure | Fitted count models and residuals | Used for average-hourly volume models | High | validation / documentation | low | CURE plots can reassure functional form but do not prove external validity |
| Test NB vs ZINB rather than assuming zero-inflation | Important for rare link-year crash data | Collision counts and model candidates | Freeway panel data | High | Stage 2 / validation | medium | ZINB may be computationally heavy at full 21.7M rows |
| Pilot GLMM/random effects for year/hour/region | Tests whether temporal/spatial grouping matters | Region/year/hour grouping variables | VDOT district/year/hour random effects | Medium to low at full scale; feasible on sampled pilots | candidate model extension / validation | high | Computational cost; random split may overstate benefit |
| Broader-but-imperfect count data inclusion | Supports using short counts where data are imperfect but widespread | Sparse traffic counts plus quality controls | Continuous + short count stations | High as design principle for Stage 1a exposure | Stage 1a / documentation | low | Bad count quality can still bias exposure model if not validated |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Direct application of Virginia freeway SPFs | Facility type, geography, crash reporting, traffic conditions, and data definitions differ | Virginia freeway model coefficients | 190 directional freeway segments | Low | Use as methodological reference only | high |
| Full hourly detector-based model for every OS Open Roads link | Requires observed hourly volume/speed at each modelled segment | Dense detector coverage | Detector-centred freeway segments | Low for full network | Use WebTRIS profiles and sparse validation | high |
| District-level random effects as spatial correlation solution | VDOT districts do not map to UK road-risk geography and are too coarse for link-level risk | Equivalent district grouping with known behaviour similarity | Virginia DOT districts | Low-to-medium | Use region/local-authority/geohash pilots; spatial holdout validation | medium |
| Applying speed probe findings directly to OSM speed limits | Probe average speed and posted speed limit are different variables | Observed speed distributions | Freeway speed/probe data | Low if only OSM limits available | Use OSM speed limit as static context; seek probe/open speed data for pilot | high |
| Extending conclusions to junctions and minor urban roads | Study excludes ramps/interchanges and is freeway-only | Non-freeway facility data | Basic freeway directional segments | Low | Treat as motorway/trunk-road evidence only | high |

Important:

- The paper is highly useful for validation design around exposure/time profiles, but not a direct production-model template for a whole UK open-road network.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Yes. It supports the importance of traffic exposure, but more specifically argues that AADT alone may be too aggregate and that sub-daily exposure can improve crash prediction on freeways.
- Does it suggest better handling of AADT/AADF uncertainty? Indirectly. It does not model AADT uncertainty, but it shows that broader short-count data can improve models and that raw disaggregate data can underperform when missingness/quality is poor.
- Does it suggest useful geometry or road-context features? Yes. Segment length, horizontal curvature, vertical curvature/grade, median width, and shoulder width are used/tested. For Open Road Risk, curvature and grade are especially relevant because they are already present or planned.
- Does it suggest better modelling of junctions? No. The study excludes ramps/interchanges and basic freeway segments only.
- Does it suggest better treatment of severity? Partly. It models total crashes and combined fatal/injury crashes separately, but does not model severity classes separately.
- Does it suggest better validation design? Yes. It supports explicit AADT-vs-hourly comparisons, external validation metrics on a held-out set, model-form comparison, and CURE plots. It does not provide spatial or temporal holdout validation.
- Does it expose a weakness in my current approach? Yes: if Open Road Risk relies on annual AADT exposure only, it may miss time-of-day exposure/flow-state effects on major roads. But the paper does not prove that temporal profiles will improve full-network UK link-level risk; this requires a pilot.

## 15. Repo Actionability

### Action 1

- Suggested repo action: Add a documentation note in the Stage 1b / methodology page explaining why average-hourly traffic profiles are being considered, citing this paper as freeway evidence that average-hourly exposure can outperform AADT-only models.
- Action type: documentation note
- Relevant stage: Stage 1b / documentation
- Why the paper supports it: It directly compares AADT, raw hourly, average 15-minute, and average hourly volume representations.
- Evidence quote or page reference: Conclusions, page 39: average-hourly models outperformed AADT across all MOEs; raw hourly models were inferior with missing data.
- Effort: low
- Risk if implemented badly: Overstating the result as general proof for all UK roads rather than freeway-specific evidence.

### Action 2

- Suggested repo action: Create a small diagnostic comparing Stage 2 collision model performance with current annual exposure offset versus a pilot temporal-exposure variant for motorway/trunk/A-road subsets.
- Action type: small pilot
- Relevant stage: Stage 1b / Stage 2 / validation
- Why the paper supports it: It reports consistent validation gains for average-hourly volume + flow-state models compared with AADT-based models.
- Evidence quote or page reference: Tables 9–10, pages 36–37; conclusions, page 39.
- Effort: medium
- Risk if implemented badly: Confounding exposure profile quality with road-class/geography differences; avoid production change until spatial/temporal validation is done.

### Action 3

- Suggested repo action: Add CURE or cumulative residual plots for exposure/AADT bins and possibly average-hourly exposure bins in model diagnostics.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The report uses CURE plots to assess whether average-hourly volume has a suitable functional form in the selected models.
- Evidence quote or page reference: Figure 6 and page 35: hourly-volume CURE plots were within two standard-deviation limits.
- Effort: low-to-medium
- Risk if implemented badly: Treating CURE plots as predictive validation rather than functional-form diagnostics.

### Action 4

- Suggested repo action: In model comparison notes, explicitly test NB / Poisson-like GLM / zero-inflated or hurdle alternatives on a sampled link-year dataset, but avoid adopting zero-inflated language unless the model is actually fitted and justified.
- Action type: baseline comparison
- Relevant stage: Stage 2 / validation
- Why the paper supports it: It tests ZINB because disaggregate data produce many zero observations, but generally selects negative binomial for consistency and performance.
- Evidence quote or page reference: Pages 6 and 23; Appendix C.
- Effort: medium
- Risk if implemented badly: Applying computationally heavy zero-inflated models to the full network without evidence that they improve validation.

### Action 5

- Suggested repo action: Add a validation note that raw high-frequency traffic data may be worse than smoothed average profiles when coverage/missingness is uneven.
- Action type: documentation note / diagnostic
- Relevant stage: Stage 1b / validation / documentation
- Why the paper supports it: Raw hourly models underperformed because 23% of validation raw hourly data failed quality checks.
- Evidence quote or page reference: Page 31 and conclusions, page 38.
- Effort: low
- Risk if implemented badly: Using the finding to dismiss high-frequency data generally; the issue is missingness/quality, not high frequency itself.

## 16. Query Tags

- freeway-SPF
- safety-performance-function
- AADT
- hourly-exposure
- average-hourly-volume
- traffic-flow-state
- speed-variables
- INRIX
- probe-speed-data
- short-counts
- continuous-counts
- negative-binomial
- zero-inflated-negative-binomial
- GLMM
- spatial-random-effects
- temporal-random-effects
- CURE-plots
- validation-MAD
- exposure-comparison
- motorway-transferable

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: The report does not provide spatial or temporal holdout validation. It does not provide a direct implementation recipe for non-freeway roads, junctions, or dense link-level national networks. It does not model uncertainty in traffic estimates in the same way Open Road Risk may need to handle estimated AADT.
- Parts of the paper that need manual checking: Appendix parameter tables if exact coefficient values are needed for a coefficient-level evidence register; Table 7 and Table 8 model specification details if the repo wants to reproduce the exact VDOT pilot model structure.
- Any likely ambiguity or risk of misinterpretation: The improvements are for Virginia freeway segments and should not be treated as evidence that hourly profiles improve all road types. The validation is random split, so claims about new-region or future-year generalisation should remain cautious.
