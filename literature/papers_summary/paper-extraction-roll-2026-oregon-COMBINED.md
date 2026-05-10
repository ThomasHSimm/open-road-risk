# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: dot_89189_DS1.pdf
- Suggested Markdown filename: final-roll-2026-oregon-pedestrian-spf.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: original PDF plus two Markdown extractions
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The report is a long 208-page technical report with appendices. This final record focuses on the main report, especially the abstract, data-development sections, pedestrian-volume data-fusion modelling, SPF methodology, summary/limitations, and reported validation tables. Full appendix coefficient tables are not exhaustively transcribed.

## 1. Citation

- Title: Developing a Pedestrian Safety Performance Function for Oregon
- Authors: Josh Roll; Jason Anderson; Nathan McNeil
- Year: 2026
- DOI or URL, if present: Not stated. Report number FHWA-OR-RD-26-06. Distribution page states copies are available from NTIS and online from Oregon DOT Research.
- Country / region studied: United States / Oregon
- Study setting: Urban intersections in Oregon, covering state and non-state systems and multiple urban geographies.

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The report develops pedestrian crash-frequency safety performance functions for Oregon urban intersections using vehicle exposure and estimated pedestrian exposure.
- Main purpose: safety performance function / crash prediction / systemic pedestrian safety / exposure modelling.
- Evidence quote or page reference: The technical report abstract states that the report develops a pedestrian SPF for urban intersections in Oregon, uses pedestrian traffic volume estimates from signal push-button actuations, and constructs SPFs for various intersection types with different traffic control. Page 1 states that the report documents development of a pedestrian crash-injury SPF and develops pedestrian volumes using novel data sources and data-fusion modelling.

## 3. Response Variable

- Target variable: Pedestrian crash frequency at intersections.
- Collision type: Pedestrian crashes.
- Severity handling: Main SPF models combine all pedestrian crash types and severities. Fatal and incapacitating-only models were considered but excluded because they required a more complex modelling framework due to significant underdispersion.
- Count, binary, rate, risk score, severity class, or other: Non-negative integer count.
- Time window used for outcomes: Crash data are described for 2007–2022 in the traffic-control mining section. The exact crash-year window used in every final SPF model is not clearly stated in the extracted main SPF sections.
- Evidence quote or page reference: Page 82 states that all pedestrian crash types and severities were considered and that count-data models were used because the dependent variable is a non-negative integer count. Page 145 states that fatal/incapacitating-only SPFs were considered but excluded due to significant underdispersion.

## 4. Exposure Handling

- Exposure variable used, if any: Vehicle exposure and pedestrian exposure.
- Traffic count source:
  - Vehicle AADT: HPMS where available, INRIX-derived estimates for some segments, and random-forest data-fusion estimates where HPMS/INRIX were unavailable.
  - Pedestrian AADPT: signal push-button-derived pedestrian volumes, short-duration pedestrian counts, and a data-fusion model applied to all urban intersections.
- Whether exposure is modelled, observed, assumed, or ignored: Mixed. Vehicle AADT is observed, externally estimated, or modelled depending on data availability. Pedestrian AADPT is observed at a subset of intersections and modelled for statewide urban-intersection coverage.
- Treatment of missing or sparse traffic counts:
  - Vehicle AADT gaps are filled using INRIX estimates or random-forest data-fusion models using connected segment volumes, functional class, access to jobs, network centrality, and urban area.
  - Pedestrian AADPT gaps are filled using data-fusion models tested across statistical and machine-learning approaches.
- Whether offset terms, rates, denominators, or normalisation are used: The SPF models use AADT and AADPT as explanatory exposure variables, not as an explicit offset. The report does not present a collision-risk exposure offset equivalent to Open Road Risk's `log(AADT × link_length_km × 365 / 1e6)`.
- Evidence quote or page reference: Page 47 states that missing AADT can be estimated using a data-fusion model. Page 58 treats push-button-derived pedestrian counts as continuous/permanent pedestrian counters. Page 62 states that data fusion is used to estimate pedestrian volumes at all urban intersections. Page 82 states that the final crash-frequency models considered only vehicle volume and pedestrian volume.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes:
  - Vehicle AADT gap-filling is conceptually relevant to Open Road Risk Stage 1a.
  - Pedestrian AADPT estimation is useful as an exposure-modelling example but has low direct transferability unless equivalent pedestrian count/proxy data are available.
  - The SPF exposure concept is useful, but the model does not use Open Road Risk's offset formulation.

## 5. Spatial Unit of Analysis

- Unit: Intersection.
- Segment length or segmentation rule: Not applicable to the final SPF models. Segment data are built during data preparation, but the SPF output is intersection-based.
- How crashes are assigned to the network: Crash records with spatial coordinates are joined to intersection points; crash-derived traffic-control information is also used to help infer traffic signal presence. The exact pedestrian-crash assignment buffer/rule for the final SPF outcome is not fully stated in the extracted main sections.
- Treatment of junctions/intersections: Intersections are classified by number of legs, traffic control, marked-crossing presence, geographic area, and state/non-state system. Complex intersections are simplified using contraction methods so divided roads and lane-level geometries do not incorrectly inflate leg counts.
- Spatial aggregation risks: Intersection contraction, crash assignment near complex junctions, and traffic-control inference from crash reports can introduce classification errors. Some manual validation was used.
- Evidence quote or page reference: Page 50 describes classifying nodes into driveways, three-leg, four-leg, and five-or-more-leg intersections and applying a contraction algorithm. Page 51 states that 908 intersections, about 1.5% of roughly 64,000 nodes, required manual classification. Page 56 reports 3,144 unique traffic signals after integrating multiple sources.
- Relevance to OS Open Roads link-based pipeline: Medium. The intersection engineering is useful for future junction-complexity features or a separate junction layer, but the main unit is not directly compatible with Open Road Risk's current OS Open Roads link-year modelling table.

## 6. Temporal Unit of Analysis

- Years covered:
  - Short-duration pedestrian counts: 2017–2023.
  - Traffic signal push-button pedestrian volumes: annualised where sufficient days of data are available.
  - Crash data mentioned for traffic-control mining: 2007–2022.
  - Final SPF crash outcome period: Not clearly stated in the extracted SPF methodology.
- Temporal resolution: Annual average daily exposure measures, AADT and AADPT.
- Whether seasonality or time-of-day is modelled: Seasonality is handled in pedestrian short-duration count expansion using AASHTO and day-of-year factoring methods. Time-of-day is not used directly in the final SPF models.
- Whether before-after or panel structure is used: No before-after design is stated. Final SPF models are cross-sectional by intersection typology/geography/system grouping.
- Evidence quote or page reference: Page 59 describes AASHTO and day-of-year factoring methods. Page 75 describes independent 10-fold cross-validation of 868 AADPT observations. Page 64 describes the mixed-effects negative binomial model for pedestrian-volume estimation.
- Relevance to WebTRIS-style time profiles: Medium. The short-duration-to-annual exposure expansion is conceptually relevant, but it is pedestrian-count annualisation rather than a motor-traffic time-of-day profile model.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Entering vehicle AADT | HPMS, INRIX, random-forest AADT imputation | Sum entering-leg AADT after intersection typology/contraction | Core vehicle exposure in pedestrian SPF | Medium; AADF equivalent exists, but link-to-junction aggregation is needed |
| Pedestrian AADPT | Signal push-button actuations, short-duration pedestrian counts, data fusion | Annualised and modelled for all urban intersections | Core pedestrian exposure | Low-to-medium; useful concept, but UK open pedestrian exposure data are sparse |
| Intersection typology | OSM/base/all-streets network | Node classification and contraction for 3-leg/4-leg/complex intersections | Separates facility families | Medium; useful for future junction work |
| Traffic signal presence | ODOT, city inventories, OSM, crash records | Integrated signal inventory and inference | Splits signalized/unsignalized models | Medium as signal-presence proxy; signal phasing remains unavailable |
| Marked crossing presence | Crossing/local pedestrian infrastructure data | Crossing development and marked/no-marked model stratification | Important pedestrian-facility split | Low-to-medium; OSM crossing coverage is uneven |
| Transit stop proximity | GTFS | Counts/stops within 50m and 100m buffers | Pedestrian activity proxy | High if GTFS available |
| Network density | Base/all-streets networks | Link density by class within buffers | Connectivity/urban form | High; similar to existing network features |
| Betweenness centrality | Base/all-streets network; AADT impedance | igraph betweenness using shortest paths with AADT impedance | Network importance/activity proxy | High conceptually; already relevant to Open Road Risk |
| Strava pedestrian activity | Strava walk/jog/run activity | Aggregated near intersections | Pedestrian activity proxy | Low for open-data production; likely proprietary |
| Access to jobs, schools, parks, amenities | Census/EPA/local accessibility data | Walk/drive-shed access measures | Pedestrian demand predictors | Medium; UK census/IMD/accessibility proxies possible |
| Operational speed | INRIX probe speed data | Network conflation and speed summaries | Exposure/risk context | Low-to-medium; depends on UK speed data access |
| Census and sociodemographic measures | Census geographies / Smart Location Database | Spatial joins and apportionment | Demand/risk context | Medium; UK census/IMD transfer possible |

Important:

- Many contextual features were engineered for pedestrian-volume modelling, but the final crash SPF models deliberately use only exposure variables: vehicle AADT and pedestrian AADPT.

## 8. Model Architecture

- Algorithms/models used:
  - Pedestrian AADPT estimation: negative binomial mixed effects, Poisson, random forest, XGBoost, neural-network approaches; random forest selected for final AADPT prediction.
  - Crash SPF models: Poisson first, then negative binomial where overdispersion is significant.
- Baseline model:
  - AADPT modelling: statistical models act as comparators to ML models.
  - SPF modelling: Poisson count model.
- Final/preferred model:
  - AADPT: random forest using the `caret` package, selected based on cross-validation and reasonable statewide predictions.
  - SPF: typology-specific exposure-only Poisson or negative binomial models using AADT and AADPT.
- Loss function or likelihood, if stated:
  - Poisson and negative binomial likelihoods are described.
  - ML models are evaluated using RMSE, absolute percent error, and R².
- Offset/exposure term, if used: No explicit offset term stated for final SPFs. AADT and AADPT enter as exposure predictors.
- Spatial autocorrelation handling: No explicit spatial autocorrelation model for final SPFs.
- Temporal dependence handling: Not stated for final SPFs.
- Interpretability method: SPF coefficient signs/significance, CURE plots, and ML variable importance.
- Evidence quote or page reference: Pages 82–85 describe Poisson, dispersion testing, and negative binomial modelling. Page 75 reports 10-fold cross-validation for AADPT models. Page 80 explains why random forest `caret` was selected. Page 85 states that model summaries and CURE plots are presented.

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---:|---:|---|---|---|
| AADPT model validation | Observations | 868 | AADPT model CV dataset | Count of pedestrian-volume observations used in independent 10-fold CV | Page 75 |
| AADPT model validation | RMSE | 434 | Negative binomial | Worse than ML alternatives on RMSE | Table 3.7, page 75 |
| AADPT model validation | R² | 0.51 | Negative binomial | Moderate cross-validated fit | Table 3.7, page 75 |
| AADPT model validation | RMSE | 397 | Poisson | Better than NB, worse than RF | Table 3.7, page 75 |
| AADPT model validation | R² | 0.56 | Poisson | Moderate cross-validated fit | Table 3.7, page 75 |
| AADPT model validation | RMSE | 336 | Random forest, ranger | Best RMSE | Table 3.7, page 75 |
| AADPT model validation | R² | 0.67 | Random forest, ranger | Strong cross-validated fit | Table 3.7, page 75 |
| AADPT model validation | RMSE | 337 | Random forest, caret | Near-best RMSE | Table 3.7, page 75 |
| AADPT model validation | R² | 0.68 | Random forest, caret | Highest R² in Table 3.7 | Table 3.7, page 75 |
| AADPT model validation | RMSE | 365 | XGBoost | Better than Poisson/NB but worse than RF | Table 3.7, page 75 |
| AADPT model validation | Median absolute percent error | 28% | XGBoost | Lowest median APE, but application produced negative estimates | Table 3.7, page 75; Table 3.8, page 80 |
| AADPT application sanity check | Minimum predicted AADPT | -61.6 | XGBoost | Invalid negative pedestrian volumes | Table 3.8, page 80 |
| AADPT application sanity check | Maximum predicted AADPT | 649,564,547 | Negative binomial | Implausible extreme predictions | Table 3.8, page 80 |
| AADPT application sanity check | Maximum predicted AADPT | 5,912 | Random forest, caret | Plausible statewide prediction range; selected final AADPT model | Table 3.8, page 80 |
| SPF model diagnostics | CURE plots | Reported throughout Chapter 4 | Typology-specific SPFs | In-sample cumulative residual diagnostics | Page 85 and Figures 4.1–4.16 |
| SPF validation | Held-out / spatial / temporal validation | Not stated | Final crash SPFs | No clear holdout validation for final SPFs | Chapter 4 methodology |
| Model complexity comparison | Exposure-only vs full contextual models | Full models sometimes improve log-likelihood but not expected crash-frequency estimates substantially | SPF model development | Simpler exposure-only models chosen for usability and stability | Page 82 / Section 4.1 and Appendix A |
| Serious crash models | Fatal/incapacitating-only SPF | Not used | Severe pedestrian crashes | Excluded due to significant underdispersion and need for more complex framework | Page 145 |

After the table:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? AADPT exposure model metrics are 10-fold cross-validated. SPF crash-model diagnostics are in-sample CURE/log-likelihood-style diagnostics. No clear held-out, spatial, temporal, grouped, or external validation is stated for the final crash SPFs.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy. CURE plots and SPF log-likelihood comparisons are in-sample diagnostics.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? AADPT metrics test exposure-model prediction under random CV. SPF metrics mainly test fit and model adequacy, not external predictive generalisation.
- Are any metrics likely to be optimistic for real-world deployment? Yes. Random CV for exposure models may not test spatial transfer; SPF diagnostics are not held-out validation.
- Which metric, if any, is most relevant to Open Road Risk? The AADPT/AADT data-fusion validation approach and the exposure-only vs full-model comparison are the most relevant. The final pedestrian SPF coefficients are less directly relevant.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Count-data SPFs are used. Poisson is estimated first; dispersion is tested; negative binomial is used where overdispersion is present. Severe-only pedestrian crashes were not modelled because of significant underdispersion and the need for a more complex framework.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson and negative binomial. No zero-inflated or hurdle model is reported for the final SPFs.
- Whether high-risk locations are evaluated separately: Not stated as a separate high-risk validation. The report stratifies intersections by typology, traffic control, marked crossing status, geography, and state/non-state system.
- Evidence quote or page reference: Pages 82–85 describe Poisson, dispersion testing, and negative binomial. Page 145 discusses severe-crash model exclusion due to underdispersion.
- Practical relevance to my sparse collision link-year dataset: Medium. It supports dispersion testing and careful facility-family stratification, but pedestrian intersections are not equivalent to all-injury road-link-year data.

## 11. Validation Strategy

- Train/test split method:
  - AADPT exposure model: independent 10-fold cross-validation over 868 observations.
  - Final crash SPFs: no train/test split stated.
- Spatial holdout used? no / not stated.
- Temporal holdout used? no / not stated.
- Grouped holdout used? no / not stated.
- Cross-validation type: 10-fold CV for AADPT data-fusion models. Not stated for final crash SPFs.
- Metrics: For exposure models: RMSE, absolute percent error, R², application sanity checks. For crash SPFs: coefficient summaries, dispersion tests, log-likelihood comparisons, CURE plots.
- External validation: Not stated.
- Leakage or generalisation risks: Crash-derived traffic-control inference can be useful for inventory QA but may be risky if not separated from outcome modelling. Random CV for exposure models may be optimistic where nearby intersections share similar built environment. SPF models do not appear to have held-out validation.
- Evidence quote or page reference: Page 75 describes 10-fold cross-validation of 868 AADPT observations. Page 85 describes presentation of CURE plots. Page 56 describes integrating multiple signal sources including crash-record-derived evidence.
- What I should copy or avoid: Copy the exposure-model CV, application sanity checks, CURE-style diagnostics, and model-complexity discipline. Avoid treating the final crash SPFs as externally validated or directly transferable to road-link crash modelling.

## 12. Key Findings Relevant to My Project

1. Finding: Exposure dominates the final SPF design: final crash models use vehicle AADT and pedestrian AADPT rather than complex contextual feature sets.
   - Why it matters: This supports testing whether simpler exposure-focused baselines perform competitively before adding many contextual features in Open Road Risk.
   - Evidence quote or page reference: Page 82 says final models considered only vehicle volume and pedestrian volume; the report notes full models did not substantially improve expected crash-frequency estimates.
   - Confidence: medium. Strong within this pedestrian-intersection context, but not proof for all-vehicle road-link risk.

2. Finding: Random forest performed best or near-best for pedestrian AADPT data fusion and produced plausible statewide predictions.
   - Why it matters: Supports tree-based data-fusion approaches for sparse exposure estimation, similar to Open Road Risk Stage 1a.
   - Evidence quote or page reference: Page 75 and Table 3.7 report RF CV performance; page 80 and Table 3.8 show RF produced plausible prediction ranges and was selected.
   - Confidence: high for this report.

3. Finding: Application sanity checks matter, not just CV metrics.
   - Why it matters: XGBoost had attractive error metrics but produced negative AADPT estimates; NB produced implausible extreme maxima. Open Road Risk should check full-network prediction distributions after CV.
   - Evidence quote or page reference: Table 3.8 on page 80 reports negative XGBoost predictions and extreme NB predictions.
   - Confidence: high.

4. Finding: Intersection typology and contraction are substantial data-engineering tasks.
   - Why it matters: Future Open Road Risk junction features need careful graph contraction/typology work; naive node degree may misclassify divided roads and complex intersections.
   - Evidence quote or page reference: Pages 50–56 describe intersection typology, contraction, manual classification, and signal assignment.
   - Confidence: high.

5. Finding: CURE plots are used as model-fit diagnostics for SPF models.
   - Why it matters: Cumulative residual diagnostics could be useful for Open Road Risk's GLM baseline across exposure and key predictors.
   - Evidence quote or page reference: Page 85 and Figures 4.1–4.16.
   - Confidence: high.

6. Finding: Small disaggregated SPF groups can be unstable.
   - Why it matters: Open Road Risk should be cautious before fitting separate production models by facility family, geography, or rare crash subtype.
   - Evidence quote or page reference: Page 144/145 summary and serious-crash underdispersion note; small subgroup examples are visible in model tables.
   - Confidence: medium.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Full-network prediction sanity checks after exposure-model CV | Detects implausible distributions not caught by CV alone | Stage 1a predictions and observed counts | Statewide Oregon urban intersections | High | Stage 1a / validation | Low | Need sensible thresholds by road class |
| Tree-based exposure data fusion | Supports random forest/boosting for sparse exposure estimates | AADF/WebTRIS/OS features | Oregon vehicle/pedestrian exposure models | High conceptually | Stage 1a | Already partly implemented | Different data sources and geography |
| AADF/AADT error by data-source tier | Oregon uses observed/probe/modelled tiers | AADF/WebTRIS/proxy tiers | Statewide Oregon | High | Stage 1a / documentation | Low | Risk of over-comparing incompatible sources |
| CURE/cumulative residual diagnostics | Checks GLM fit over predictor/exposure ranges | Stage 2 fitted GLM predictions/residuals | SPF models | Medium to high | Stage 2 / validation | Medium | In-sample diagnostic, not validation |
| Exposure-only vs full-feature baseline comparison | Tests whether added features materially improve expected crash predictions | Stage 2 model variants | Pedestrian-intersection SPFs | Medium | Stage 2 / validation | Low to medium | Pedestrian-intersection result may not generalise |
| Junction typology pilot | Supports future junction-complexity features | OS/OSM graph, signals/crossings proxies | Oregon intersections | Medium | future feature / documentation | High | Misclassification can create false precision |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Direct pedestrian SPF coefficients | Oregon urban pedestrian-intersection models differ from UK road-link all-injury risk | Pedestrian volumes, intersection unit, Oregon calibration | Oregon urban intersections | Low | Treat as methodology only | High |
| Push-button-derived AADPT at scale | UK open-data equivalent may not exist | Signal push-button logs | Oregon urban intersections | Low | Use local pilots or alternative pedestrian proxies | High |
| Strava-based pedestrian activity as production feature | Proprietary/non-open and sampling biased | Strava access and bias correction | Oregon pedestrian exposure | Low | Document as possible non-open enrichment | High |
| Crash-derived traffic-control inference as production feature | Uses outcome records to infer inventory; possible leakage if not handled carefully | Separate inventory validation | Oregon crash/signal integration | Low to medium | Use for QA only or freeze inventory before modelling | Medium |
| Final SPF model form as Stage 2 replacement | Intersection pedestrian crash model, not link-year all-injury model | Different outcome/unit/exposure | Urban intersections | Low | Use only for diagnostics/literature context | High |

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Indirectly. It strongly supports exposure-aware pedestrian crash modelling, but uses AADT/AADPT as predictors rather than Open Road Risk's offset formulation.
- Does it suggest better handling of AADT/AADF uncertainty? Yes. It supports hierarchical/data-fusion exposure estimation and full-network sanity checks after CV.
- Does it suggest useful geometry or road-context features? Yes for future junction/intersection work: typology, traffic control, marked crossings, network density, centrality, transit access, and accessibility measures. However, final SPFs use only exposure variables.
- Does it suggest better modelling of junctions? Yes. The report is a detailed example of intersection typology, contraction, and signal/crossing inventory development.
- Does it suggest better treatment of severity? No for current implementation. Severe-only pedestrian SPFs were considered but not used due to underdispersion.
- Does it suggest better validation design? It suggests better exposure-model validation and CURE diagnostics, but final crash SPFs lack clear holdout validation.
- Does it expose a weakness in my current approach? Yes: Open Road Risk should be clear that road-link risk does not fully represent pedestrian/intersection conflict risk and that exposure estimates need full-network plausibility checks, not just CV metrics.

## 15. Repo Actionability

1. Suggested repo action: Add full-network Stage 1a prediction distribution checks by road class, urban/rural category, and AADT band.
   - Action type: diagnostic
   - Relevant stage: Stage 1a / validation
   - Why the paper supports it: The report selected random forest partly because application sanity checks found invalid or implausible outputs from other models.
   - Evidence quote or page reference: Table 3.8, page 80.
   - Effort: low
   - Risk if implemented badly: Thresholds could be arbitrary; use them as flags, not hard truth.

2. Suggested repo action: Add an exposure-only baseline comparison for Stage 2, then compare contextual features against it.
   - Action type: baseline comparison
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: Oregon's final SPFs prioritised exposure-only models because contextual full models did not substantially improve expected crash-frequency estimates.
   - Evidence quote or page reference: Page 82 / Section 4.1 and Appendix A.
   - Effort: low to medium
   - Risk if implemented badly: Do not assume the pedestrian-intersection result generalises to all road-link crashes.

3. Suggested repo action: Add CURE-style or cumulative-residual diagnostics for the GLM baseline.
   - Action type: diagnostic
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: The report uses CURE plots throughout Chapter 4 for SPF fit assessment.
   - Evidence quote or page reference: Page 85 and Figures 4.1–4.16.
   - Effort: medium
   - Risk if implemented badly: CURE plots are in-sample diagnostics, not predictive validation.

4. Suggested repo action: Add a documentation note that pedestrian/intersection risk needs a separate junction/exposure layer rather than being fully solved by the current link model.
   - Action type: documentation note
   - Relevant stage: documentation / future feature
   - Why the paper supports it: The report's full modelling unit is intersection-based, with typology, signal status, marked crossings, and pedestrian exposure.
   - Evidence quote or page reference: Pages 50–56 and Chapter 4.
   - Effort: low
   - Risk if implemented badly: Could overstate a limitation; frame as scope boundary.

5. Suggested repo action: Pilot junction typology construction separately from production risk ranking.
   - Action type: small pilot
   - Relevant stage: future feature / feature engineering
   - Why the paper supports it: The Oregon report required contraction, typology validation, and signal inventory integration before modelling intersections.
   - Evidence quote or page reference: Pages 50–56.
   - Effort: high
   - Risk if implemented badly: Naive node-degree features may be noisy or misleading.

6. Suggested repo action: Add a facility-family split diagnostic before fitting separate production models.
   - Action type: diagnostic / baseline comparison
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: Disaggregated pedestrian SPF groups can become unstable where samples are small or outcomes are rare.
   - Evidence quote or page reference: Page 145 severe-crash underdispersion note and Chapter 4 subgroup model structure.
   - Effort: medium
   - Risk if implemented badly: Sparse strata can produce unstable rankings.

## 16. Query Tags

- pedestrian-SPF
- Oregon
- urban-intersections
- AADT
- AADPT
- pedestrian-exposure
- exposure-modelling
- data-fusion
- random-forest
- XGBoost
- negative-binomial
- Poisson
- dispersion-testing
- underdispersion
- CURE-plots
- intersection-typology
- traffic-signal-inference
- marked-crossings
- push-button-counts
- short-duration-counts
- annualisation
- exposure-only-model
- full-model-comparison
- sparse-count-validation
- junction-risk
- systemic-safety

## 17. Confidence and Gaps

- Overall confidence in extraction: medium-high
- Important details not stated or not fully extracted: Exact SPF crash outcome period; precise crash-to-intersection assignment buffer/rule; exhaustive coefficients/standard errors/log-likelihoods/dispersion parameters for all appendix SPF models; whether any spatial dependence diagnostics were attempted outside CURE plots.
- Parts of the paper that need manual checking: Appendix B/C if exact SPF coefficients are required; Appendix A for detailed exposure-only vs full-model comparisons; data-development appendix if exact crash assignment rules are needed.
- Any likely ambiguity or risk of misinterpretation: AADPT data-fusion models are cross-validated, but final crash SPFs are not clearly externally or spatially validated. The report supports exposure-aware modelling and exposure data fusion, not direct adoption of Oregon pedestrian-intersection SPFs for Open Road Risk's link-level all-injury model.
