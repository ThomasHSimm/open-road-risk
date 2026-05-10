# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Modelling Motorway Accidents using Negative Binomial Regression.pdf
- Suggested Markdown filename: paper-extraction-pan-2013-motorway-negative-binomial.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The PDF text was accessible. Some equations and table formatting were imperfectly parsed, so page/table references should be preferred over exact formula transcription where formatting is unclear.

## 1. Citation

- Title: Modelling Motorway Accidents using Negative Binomial Regression
- Authors: Pan Chengye; Prakash Ranjitkar
- Year: 2013
- DOI or URL, if present: Proceedings of the Eastern Asia Society for Transportation Studies, Vol. 9, 2013. DOI not stated.
- Country / region studied: New Zealand / Auckland motorway, State Highway 1N, Northern Motorway and Southern Motorway
- Study setting: motorway; mixed rural and urban motorway sections

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper develops accident prediction models for Auckland motorway segments, relating annual accident frequency to traffic, road geometry, operational, ramp, and weather variables.
- Main purpose: safety performance function / accident prediction model / descriptive model comparison
- Evidence quote or page reference: Page 2 states: "The main objective of this paper is to develop accident prediction models for Auckland motorway." Page 1 states that the models link accident frequencies to "traffic conditions, geometric and operational characteristics of road, and weather conditions."

## 3. Response Variable

- Target variable: Annual accident frequency per motorway segment-year.
- Collision type: all reported crashes on the selected motorway mainline; injury/fatal subset is mentioned descriptively but the model target appears to use all retrieved crashes, not injury-only crashes.
- Severity handling: Severity is present in the CAS source data, but severity is not modelled separately in the reported models.
- Count, binary, rate, risk score, severity class, or other: Count.
- Time window used for outcomes: One year per segment sample; study data cover 2004–2010.
- Evidence quote or page reference: Page 4 states that 10,149 crashes occurred over 1 January 2004 to 31 December 2010 and were retrieved from CAS. Page 7 defines `yi` as the number of accidents at a segment during "one year in this case". Page 5 states that "Each year data from a segment was treated as a sample giving a total of 959 data samples."

## 4. Exposure Handling

- Exposure variable used, if any: AADT per lane, with segment length also included in the model.
- Traffic count source: Traffic Monitoring System (TMS), using sensors/detectors along the State Highway.
- Whether exposure is modelled, observed, assumed, or ignored: Observed for motorway mainline/ramp locations, with some missing AADT and heavy-vehicle percentage figures noted in Table 1.
- Treatment of missing or sparse traffic counts: Not stated beyond noting missing AADT and heavy-vehicle percentage values in Table 1.
- Whether offset terms, rates, denominators, or normalisation are used: No formal exposure offset is used. The final model includes `Ln length` and `Ln AADT per lane` as explanatory variables in the log-link model rather than as a fixed-offset exposure term.
- Evidence quote or page reference: Page 4 says AADT data were extracted from TMS and ranged from 18,625 to 102,420 vehicles/day on the motorway mainline; ramp AADT ranged from 430 to 24,217 vehicles/day. Page 9 shows the explicit model form using `Ln L` and `LnAADTperlane`. Tables 3–5 report coefficients for `Ln length` and `Ln AADT per lane`.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The mathematical idea of including traffic volume and segment length is highly relevant. The specific data setup has lower transferability because this paper uses observed motorway sensor/TMS AADT for a short motorway corridor, whereas Open Road Risk estimates AADT across a much larger OS Open Roads network with sparse counted observations. The paper does not address uncertainty in estimated AADT.

## 5. Spatial Unit of Analysis

- Unit: Motorway segment-year.
- Segment length or segmentation rule: 137 homogeneous directional motorway segments after filtering; segment lengths ranged from 0.27 km to 2.94 km. Segments shorter than 0.2 km or longer than 3 km were avoided. Segmentation was based primarily on ramp presence, then changes in roadway elements such as number of lanes and horizontal curvature.
- How crashes are assigned to the network: CAS crash locations were used, but the exact spatial assignment/matching method is not stated.
- Treatment of junctions/intersections: Motorway ramps are central to segmentation. Segments are categorised as with off-ramp, with on-ramp, or without ramp. Ramp crashes themselves were excluded, but ramp flow was included as an explanatory factor for mainline crashes.
- Spatial aggregation risks: Homogeneous-segment aggregation may better align with roadway features than fixed-length segmentation, but segment definitions are tailored to this corridor and are not directly equivalent to OS Open Roads links. Use of contiguous segments sharing weather data may introduce spatial smoothing.
- Evidence quote or page reference: Page 5 states that the remaining 67 km of motorway were disaggregated into 137 segments, with northbound and southbound carriageways treated separately. Page 5 states segments were homogeneous in traffic and design characteristics and that ramp presence was the primary segmentation factor. Page 5 also says segments under 0.2 km or over 3 km were avoided.
- Relevance to OS Open Roads link-based pipeline: Conceptually relevant for facility-family or ramp-proximity diagnostics, but not directly compatible with OS Open Roads link segmentation. It suggests that link-level modelling may need diagnostics by facility context, especially motorway links near ramps.

## 6. Temporal Unit of Analysis

- Years covered: 2004–2010.
- Temporal resolution: Yearly segment observations.
- Whether seasonality or time-of-day is modelled: No. Weather is represented annually using annual rainfall and annual wet days.
- Whether before-after or panel structure is used: Segment-year panel-style data are used, but the chosen negative binomial models do not explicitly model temporal dependence. The paper mentions GEE as tested, but the final preferred approach is negative binomial regression.
- Evidence quote or page reference: Page 5 says each year of data from a segment was treated as a sample. Page 10 states that 2004–2008 were used for model development and 2009–2010 for testing.
- Relevance to WebTRIS-style time profiles: Low direct relevance. The paper motivates traffic exposure and ramp flows but does not model within-day profiles, peak/off-peak fractions, or temporal traffic states.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Segment length | RAMM / segment geometry | Homogeneous segments; log length used in model | Exposure proxy and scale factor for expected accident counts | Already present / compare implementation |
| AADT per lane | TMS traffic monitoring | Mainline AADT divided by number of lanes; log used in model | Strong traffic exposure/intensity predictor | Medium; mathematical feature transferable, but full-network AADT must be estimated in Open Road Risk |
| Heavy vehicle percentage | TMS traffic monitoring | Percentage of heavy traffic | Captures vehicle mix and speed/size differences | Already partly present / compare implementation |
| On-ramp AADT | TMS / ramp flow data | Ramp traffic volume used for segments with or near on-ramp | Proxy for merging conflict and congestion effects | Medium for motorways if ramp-flow proxy can be built; low for all roads |
| Off-ramp AADT | TMS / ramp flow data | Ramp traffic volume used for segments with or near off-ramp | Proxy for diverging conflict | Medium for motorways if ramp-flow proxy can be built; low for all roads |
| Presence of on-ramp/off-ramp | RAMM / road inventory | Segments categorised by ramp presence | Facility/context split improves model fit | Future feature / small pilot for motorway subset |
| Number of lanes | RAMM | Count of lanes per segment | Strong predictor in all model categories | Candidate feature; OSM lanes sparse, OS/RAMS equivalent unavailable nationally |
| Lane width | RAMM | Binary indicator: 3.6 m vs 3.5 m | Cross-section feature in rural model | Low to medium; not generally available in open national data |
| Shoulder width | RAMM | Width in metres | Cross-section feature, effects differ by segment type | Low; likely not available nationally in open data |
| Median width | RAMM | Width in metres | Protective effect in some rural/off-ramp models | Low; likely unavailable in Open Roads |
| Median type | RAMM | Steel vs concrete indicator | Acts partly as region/urban proxy; paper warns interpretation is confounded | Low as feature; useful as cautionary example |
| Horizontal curvature | RAMM alignment data | Average and maximum curve radius/curvature | Geometry feature associated with accident frequency | Already planned/present as curvature / compare implementation |
| Vertical grade | RAMM alignment data | Average/max up-grade and down-grade | Grade affects speed variation and braking distance | Already planned via OS Terrain 50 / compare implementation |
| Speed limit | Highway Information Sheets | Binary 80 km/h vs 100 km/h | Operational context; may be endogenous to existing high-risk locations | Already partly available via OSM/imputation; treat carefully |
| Annual rainfall | NIWA weather database | Nearest weather station assigned to proximate segments | Environmental context | Candidate contextual feature; coarse transferability |
| Annual wet days | NIWA weather database | Days with >=1 mm rain per year, nearest station assigned | Environmental context | Candidate contextual feature; coarse transferability |
| Rural/urban model split | Road/region classification | Separate models for rural and urban motorway sections | Captures different relationships by facility context | Already planned/present as rural/urban classification / compare implementation |
| Ramp-type model split | Segment categories | Separate models for no-ramp, on-ramp, off-ramp segments | Improved MAD/MSPE relative to overall model | Future diagnostic / small pilot for motorway subset |

## 8. Model Architecture

- Algorithms/models used: Poisson regression, negative binomial regression, zero-inflated negative binomial, GEE were tested; negative binomial regression was selected as the preferred approach.
- Baseline model: Overall negative binomial regression for all motorway segments.
- Final/preferred model: Separate negative binomial models for segments without ramp, with on-ramp, and with off-ramp gave the best reported predictive performance.
- Loss function or likelihood, if stated: Maximum likelihood estimation for Poisson and negative binomial regression.
- Offset/exposure term, if used: No fixed offset stated. Segment length and AADT per lane enter as log-transformed regressors.
- Spatial autocorrelation handling: Not stated.
- Temporal dependence handling: GEE was tested, but the reported preferred model does not explicitly handle temporal dependence. The paper uses a temporal train/test split: 2004–2008 fit, 2009–2010 prediction.
- Interpretability method: Regression coefficients and t-statistics are interpreted.
- Evidence quote or page reference: Page 7 states that Poisson, negative binomial, zero-inflated negative binomial, and GEE models were tested and negative binomial was most desirable. Page 8 describes the gamma-distributed error term in the negative binomial model. Tables 3–5 report coefficients and t-statistics. Page 16 states that the ramp-segment-specific models produced improved prediction results.

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Data summary | Accident frequency per year | min 0; max 69; mean 8.77; SD 9.85 | 959 segment-year samples | Counts are overdispersed relative to mean | Table 1, page 6 |
| Data summary | Segment length | min 0.27 km; max 2.94 km; mean 0.97 km | 959 samples | Segment lengths are not fixed but bounded | Table 1, page 6 |
| Data summary | AADT per lane | min 6.25; max 28.15; mean 16.25 thousand vehicles | Mainline segments | Main exposure/intensity variable | Table 1, page 6 |
| Overall NB fit | Overdispersion alpha | 0.183; t = 9.196 | Overall model | Supports NB over Poisson in this case | Table 3, page 11 |
| Overall NB fit | Pseudo-R² | 0.119 | Overall model | In-sample goodness-of-fit/model comparison only | Table 3, page 11 |
| Overall NB coefficients | Ln AADT per lane | coefficient 2.006; t = 19.307 | Overall model | Strong positive association with accident count | Table 3, page 11 |
| Overall NB coefficients | Ln length | coefficient 0.806; t = 12.231 | Overall model | Longer segments have higher expected accident counts | Table 3, page 11 |
| Overall NB coefficients | Number of lanes | coefficient 0.634; t = 15.890 | Overall model | More lanes associated with higher accident frequency | Table 3, page 11 |
| Rural model fit | Pseudo-R² | 0.163 | Rural motorway model | Better in-sample fit than urban model | Table 4, page 12 |
| Urban model fit | Pseudo-R² | 0.088 | Urban motorway model | Lower in-sample fit than rural model | Table 4, page 12 |
| Ramp-category model fit | Pseudo-R² | 0.131 / 0.194 / 0.110 | No-ramp / on-ramp / off-ramp models | On-ramp model has highest reported pseudo-R² | Table 5, page 14 |
| Validation | MADFit | 3.71 / 3.62 / 3.21 | Overall / rural+urban / ramp-category models | In-sample fitting error decreases with ramp-category models | Table 6, page 16 |
| Validation | MSPEFit | 33.25 / 31.55 / 24.92 | Overall / rural+urban / ramp-category models | In-sample fitting error decreases with ramp-category models | Table 6, page 16 |
| Validation | MADPred | 4.07 / 3.98 / 3.70 | Overall / rural+urban / ramp-category models | Temporal holdout error lowest for ramp-category models | Table 6, page 16 |
| Validation | MSPEPred | 36.60 / 34.23 / 27.87 | Overall / rural+urban / ramp-category models | Temporal holdout error lowest for ramp-category models | Table 6, page 16 |
| Alternative model comparison | GEE MADFit; MSPEFit | 3.74; 34.46 | Overall GEE model | Slightly worse than overall NB model on fitting metrics | Page 16 |

After the table:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? Pseudo-R² and coefficient/t-statistic results are in-sample. MADFit and MSPEFit are in-sample. MADPred and MSPEPred are temporally held out using 2009–2010 after fitting on 2004–2008. Spatial holdout and external validation are not stated.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. The reported fit-set pseudo-R², MADFit, and MSPEFit should be treated as in-sample diagnostics.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? MADPred and MSPEPred test short-horizon temporal predictive performance on the same corridor. Pseudo-R² tests model fit/model comparison. The paper does not test ranking/hotspot performance, calibration, spatial transfer, or external validation.
- Are any metrics likely to be optimistic for real-world deployment? Yes. The temporal holdout uses the same motorway corridor, same segment definitions, and adjacent years. It does not test geographic transfer or performance under sparse/estimated AADT.
- Which metric, if any, is most relevant to Open Road Risk? MADPred/MSPEPred are most relevant as examples of temporal holdout metrics for count prediction, but they are not directly sufficient for Open Road Risk's wider link-level risk ranking.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The paper uses negative binomial regression to handle overdispersion. It explicitly states that zero-inflated Poisson was inappropriate because there were not many zero-accident sections.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Negative binomial regression is the selected approach. Poisson, zero-inflated negative binomial, and GEE were tested. Zero-inflated Poisson was considered inappropriate.
- Whether high-risk locations are evaluated separately: Not directly. The paper splits by rural/urban and ramp category, not by high-risk status.
- Evidence quote or page reference: Page 3 discusses negative binomial regression as a response to overdispersion and mentions zero-inflated Poisson/negative binomial for excessive zeros. Page 7 states that zero-inflated Poisson was inappropriate because "there are not many sections with zero accident frequency." Table 1 page 6 reports mean annual accident frequency 8.77 and minimum 0.
- Practical relevance to my sparse collision link-year dataset: Limited but useful. Open Road Risk has much rarer link-year collisions than this motorway study. The paper supports checking overdispersion and facility-level model splits, but its rejection of zero-inflated methods does not transfer to a 1–2% nonzero link-year dataset.

## 11. Validation Strategy

- Train/test split method: Temporal split: 2004–2008 for model development, 2009–2010 for testing prediction performance.
- Spatial holdout used? no
- Temporal holdout used? yes
- Grouped holdout used? not stated
- Cross-validation type: Not stated.
- Metrics: MAD and MSPE on fitting and prediction datasets; pseudo-R² for in-sample fit.
- External validation: No external geography or independent network validation stated.
- Leakage or generalisation risks: No obvious classic leakage is stated. However, the temporal holdout uses the same corridor and same segment definitions, so it tests short-term temporal generalisation rather than spatial generalisation. Observed traffic and road features for the same segments likely make the validation easier than Open Road Risk's full-network sparse AADT setting.
- Evidence quote or page reference: Page 10 states 2004–2008 data were used for model development and 2009–2010 for testing. Page 15 defines MAD and MSPE and states the 5-year fit / 2-year test design.
- What I should copy or avoid: Copy the idea of reporting explicit holdout prediction metrics and comparing facility-family split models against a single pooled baseline. Avoid treating same-corridor temporal prediction as evidence of national spatial generalisation.

## 12. Key Findings Relevant to My Project

1. Finding: Traffic volume, segment length, and number of lanes are consistently important predictors in this motorway case study.
   - Why it matters: These are direct checks for Open Road Risk's exposure model and Stage 2 collision model; failure to recover sensible relationships would be a red flag.
   - Evidence quote or page reference: Page 16 states that "segment length, AADT per lane and number of lanes were identified as the most critical factors in all the models."
   - Confidence: high

2. Finding: Negative binomial regression was favoured over Poisson because the accident data were overdispersed.
   - Why it matters: Supports testing overdispersion diagnostics and comparing Poisson GLM against negative binomial variants, especially for facility subsets with non-rare counts.
   - Evidence quote or page reference: Page 11 states that estimated alpha suggests overdispersion and confirms the negative binomial formulation was favoured rather than Poisson.
   - Confidence: high

3. Finding: Separate models by ramp context improved temporal prediction metrics compared with an overall motorway model.
   - Why it matters: Supports a diagnostic or small pilot for facility-family splits, particularly motorway links near ramps, rather than assuming one model fits all contexts.
   - Evidence quote or page reference: Page 16 states the third category of models gave improved prediction results; Table 6 shows MADPred improving from 4.07 overall to 3.70 for ramp-category models and MSPEPred from 36.60 to 27.87.
   - Confidence: medium

4. Finding: Ramp flow effects differed by context, including a negative coefficient for on-ramp AADT in the on-ramp segment model.
   - Why it matters: This cautions against naive interpretation of ramp or traffic variables; congestion and operational context may reverse simple exposure expectations.
   - Evidence quote or page reference: Page 13 says on-ramp AADT had a negative impact for on-ramp segments and attributes this to congested, slow-moving traffic upstream of on-ramps.
   - Confidence: medium

5. Finding: Geometry effects such as curvature and grade appear in the models, but some signs are context-specific and may reflect driver behaviour or confounding.
   - Why it matters: Supports using curvature/grade as diagnostics and candidate features, but not assuming universal monotonic effects.
   - Evidence quote or page reference: Page 11 discusses negative curvature effects and possible "risk compensation"; page 16 reports that grade effects differ by segment category.
   - Confidence: medium

6. Finding: Some variables may act as proxies for unmodelled context or prior safety interventions.
   - Why it matters: Open Road Risk should treat features such as speed limits, median type, and urban proxies carefully to avoid overinterpreting coefficients causally.
   - Evidence quote or page reference: Page 10 says concrete median type likely reflects urban motorway context rather than a direct median effect. Page 13 says 80 km/h speed limit is likely introduced as an improvement measure on already high-accident segments.
   - Confidence: high

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Negative binomial baseline comparison | Handles overdispersed count outcomes more flexibly than Poisson | Link-year collision counts, exposure, road/context features | 959 segment-years, 137 motorway segments | Medium; feasible statistically, but 21.7M rows may need scalable implementation | Stage 2 / baseline comparison | Medium | Computational cost and interpretation with very sparse link-years |
| Temporal holdout metrics | Tests whether model trained on earlier years predicts later years | Yearly link outcomes and features | 2004–2008 train, 2009–2010 test | High; Open Road Risk has 2015–2024 panel | Validation | Low to medium | Same-geography temporal holdout still does not test spatial transfer |
| Facility-family split diagnostics | Tests whether relationships differ by motorway/rural/urban/ramp context | Facility labels, rural/urban, ramp proximity if available | Rural/urban and ramp-category splits | Medium; rural/urban present, ramp features require engineering | Stage 2 / validation / documentation | Medium | Too many splits may create unstable estimates for rare events |
| Ramp-proximity motorway pilot | Captures merging/diverging context not represented by ordinary links | Motorway ramps or junction topology, road class, link geometry | Motorway-only corridor | Low to medium; limited to motorway subset | Future feature / small pilot | Medium | Ramp flow not available nationally; ramp proximity may be a weak proxy |
| Curvature and grade diagnostics | Paper uses alignment variables and finds context-specific effects | Geometry curvature; DEM-derived grade | Homogeneous motorway segments | Medium to high for geometry; grade from OS Terrain 50 approximate | Feature engineering / documentation | Medium | DEM grade can be wrong at bridges/tunnels; signs may be confounded |
| Compare pooled vs stratified models | Paper shows lower MAD/MSPE for ramp-category models | Same features plus segment categories | 3 model categories | Medium; feasible on subsets or as interactions | Stage 2 / validation | Medium | Stratification may reduce data per subgroup and hurt generalisation |
| Report MAD/MSPE alongside ranking metrics | Provides count prediction diagnostics | Observed/predicted counts | 2-year temporal test | High | Validation / documentation | Low | Count error does not directly measure hotspot/risk-ranking quality |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full use of observed AADT per lane across every segment | Open Road Risk does not have observed AADT for all OS Open Roads links | Complete mainline/ramp traffic monitoring | 67 km motorway corridor | Low nationally | Use Stage 1a estimated AADT and propagate uncertainty | high |
| Shoulder width, median width, lane width at national scale | These detailed RAMM-style engineering attributes are not generally available in open UK data | Road inventory / asset management database | 137 motorway segments | Low | Use OSM/OS proxies where coverage is acceptable; document missingness | high |
| Ramp AADT as a production feature | Ramp flows are observed in this paper but not generally available in Open Road Risk | Ramp traffic counts | Motorway corridor | Low across full network | Use ramp proximity/topology as a diagnostic proxy on motorways | medium |
| Homogeneous motorway segmentation as main spatial unit | Open Road Risk currently uses OS Open Roads links, not bespoke homogeneous motorway segments | Manual/rule-based segmentation by ramp and road characteristics | 137 segments | Low as a full replacement | Aggregate OS links into facility-homogeneous sections for a pilot | medium |
| Direct transfer of coefficient signs | The paper is one Auckland motorway case study with contextual confounding | Same road design, driving behaviour, traffic operations, weather context | Single corridor | Low | Use as prior diagnostic expectation, not as coefficient target | high |

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Partly. It strongly supports accounting for traffic volume and segment length, but it does not use an offset-normalised risk structure. It treats log length and log AADT per lane as fitted regressors.
- Does it suggest better handling of AADT/AADF uncertainty? No. It uses observed TMS traffic data and does not discuss uncertainty in estimated or sparse AADT.
- Does it suggest useful geometry or road-context features? Yes. It supports checking curvature, grade, number of lanes, ramp context, rural/urban context, speed limit, and heavy-vehicle proportion, while treating coefficient signs cautiously.
- Does it suggest better modelling of junctions? For motorways, yes. It suggests ramp context matters and that separate no-ramp/on-ramp/off-ramp models can improve prediction metrics. It does not address ordinary road junctions/intersections.
- Does it suggest better treatment of severity? No. Severity is available in the source crash data but is not modelled separately.
- Does it suggest better validation design? Yes. It supports explicit temporal holdout using later years and reporting count prediction errors. It does not provide spatial holdout.
- Does it expose a weakness in my current approach? It suggests a possible weakness if the current Stage 2 model pools very different facility contexts without diagnostics or interactions, especially motorways near ramps. It also highlights that using AADT as a model feature/offset without lane context may miss intensity-per-lane effects.

## 15. Repo Actionability

1. Suggested repo action: Add a documentation note comparing Open Road Risk's exposure offset with this paper's treatment of `Ln length` and `Ln AADT per lane` as fitted regressors.
   - Action type: documentation note
   - Relevant stage: Stage 2 / documentation
   - Why the paper supports it: The paper uses segment length and AADT per lane as central predictors rather than a fixed offset, making it a useful contrast for methodological justification.
   - Evidence quote or page reference: Page 9 gives the model form using `Ln L` and `LnAADTperlane`; Table 3 shows both are significant.
   - Effort: low
   - Risk if implemented badly: Overclaiming that the paper validates the exact Open Road Risk offset structure.

2. Suggested repo action: Add a temporal holdout diagnostic for Stage 2, e.g. train on earlier years and test on later years, reporting MAE/MAD and MSPE/RMSE-style count errors alongside ranking metrics.
   - Action type: diagnostic
   - Relevant stage: validation
   - Why the paper supports it: It uses 2004–2008 for model development and 2009–2010 for testing with MAD/MSPE.
   - Evidence quote or page reference: Page 15 defines MAD/MSPE and describes the 5-year fitting, 2-year testing setup.
   - Effort: medium
   - Risk if implemented badly: Treating same-geography temporal holdout as proof of spatial generalisation.

3. Suggested repo action: Run a small pilot comparing pooled Stage 2 performance against rural/urban or facility-family split models/interactions.
   - Action type: small pilot
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: Rural/urban and ramp-category model splits produced different fit statistics and, for ramp categories, better temporal prediction metrics.
   - Evidence quote or page reference: Tables 4–6; page 16 states ramp-category models obtained improved prediction results.
   - Effort: medium
   - Risk if implemented badly: Fragmenting already sparse collision data and producing unstable subgroup models.

4. Suggested repo action: For motorway links only, create a ramp-proximity diagnostic rather than a production feature: compare residuals/risk rankings near on-ramps/off-ramps versus other motorway links.
   - Action type: diagnostic
   - Relevant stage: feature engineering / Stage 2
   - Why the paper supports it: Ramp context and ramp flows are repeatedly associated with accident frequency, and ramp-category models improve prediction.
   - Evidence quote or page reference: Page 5 explains segmentation by ramp presence; Tables 3 and 5 include on-ramp/off-ramp AADT and ramp-type model results.
   - Effort: medium
   - Risk if implemented badly: Using ramp proximity as if it were observed ramp traffic volume, or applying motorway-specific logic to non-motorway roads.

5. Suggested repo action: Add a coefficient/residual sanity-check page for geometry features, especially curvature and grade, with separate plots by facility family.
   - Action type: diagnostic
   - Relevant stage: feature engineering / documentation
   - Why the paper supports it: The paper finds curvature and grade effects, but signs differ or require behavioural/confounding explanations.
   - Evidence quote or page reference: Page 11 discusses negative curvature effects and risk compensation; page 16 reports different grade effects across segment categories.
   - Effort: medium
   - Risk if implemented badly: Treating coefficient signs as causal effects rather than case-study associations.

## 16. Query Tags

- motorway-safety
- negative-binomial
- overdispersion
- accident-prediction-model
- safety-performance-function
- AADT-per-lane
- exposure-as-feature
- segment-length
- temporal-holdout
- MAD
- MSPE
- ramp-context
- on-ramp
- off-ramp
- rural-urban-split
- curvature
- vertical-grade
- heavy-vehicle-percentage
- lane-count
- zero-heavy-counts

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper:
  - Exact spatial crash-to-segment assignment method.
  - How missing AADT and heavy-vehicle percentage values were handled.
  - Whether all crashes or only injury/fatal crashes were modelled; the text implies all CAS-retrieved mainline crashes, but the abstract and data source discussion do not explicitly define the response by severity.
  - Whether standard errors were robust to repeated segment observations over years.
  - Whether any spatial autocorrelation diagnostics were performed.
  - Whether weather assignment to nearest stations was distance-weighted or simple nearest-neighbour.
- Parts of the paper that need manual checking:
  - Equation formatting on pages 8–9, because the PDF text parsing of formulas is imperfect.
  - Table 5 values, especially duplicated median-type coefficients for on-ramp/off-ramp models, should be checked against the original PDF rendering if used quantitatively.
  - The rural/urban segment lengths reported on page 11 appear internally odd relative to the selected 67 km after filtering and should be checked before citing.
- Any likely ambiguity or risk of misinterpretation:
  - The paper's "predictive performance" is a same-corridor temporal holdout, not external validation.
  - The negative finding for rainfall and the positive/negative signs for some road-design features may be confounded by traffic volume, urban context, or prior safety interventions.
  - The study is motorway-only and does not automatically transfer to local roads, junction-heavy urban streets, or OS Open Roads link-year modelling at national scale.
