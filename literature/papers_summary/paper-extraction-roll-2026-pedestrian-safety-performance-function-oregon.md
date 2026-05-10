# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: dot_89189_DS1.pdf
- Suggested Markdown filename: paper-extraction-roll-2026-pedestrian-safety-performance-function-oregon.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The PDF text was accessible, but this is a long 208-page technical report with appendices. Extraction focuses on the main report, especially Chapters 3 and 4, and uses reported summary tables rather than exhaustively transcribing appendix model specifications.

## 1. Citation

- Title: Developing a Pedestrian Safety Performance Function for Oregon
- Authors: Josh Roll; Jason Anderson; Nathan McNeil
- Year: 2026
- DOI or URL, if present: Not stated in the report metadata. Distribution page states copies are available online from Oregon DOT Research.
- Country / region studied: United States / Oregon
- Study setting: urban intersections; mixed state and non-state road systems

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The report develops pedestrian crash-frequency safety performance functions for Oregon urban intersections, using vehicle exposure and estimated pedestrian exposure.
- Main purpose: safety performance function / crash prediction / network screening support / systemic pedestrian safety
- Evidence quote or page reference: Page 1 states that the report documents “the process of developing a high-quality safety performance function for pedestrian crash injuries in Oregon” and develops pedestrian volumes using “novel data sources and an advanced data fusion modeling technique.” The technical report abstract states that SPFs are constructed for various intersection types with different traffic control and that models using pedestrian volume estimates and pedestrian-volume proxies are compared.

## 3. Response Variable

- Target variable: Pedestrian crash frequency at intersections.
- Collision type: Pedestrian crashes; all pedestrian crash types and severities for the main SPF models.
- Severity handling: Main SPF models combine all pedestrian crash types and severities. Fatal and incapacitating-only models were considered but excluded because they required a more complex framework due to significant underdispersion.
- Count, binary, rate, risk score, severity class, or other: Non-negative integer count.
- Time window used for outcomes: Crash data are described for 2007 to 2022 in the traffic-control mining section. The exact crash-year window used in every SPF model is not stated in the extracted main-model sections.
- Evidence quote or page reference: Page 82 states that “all pedestrian crash types and severities were considered.” Page 82 also states that count-data models were used because the dependent variable is “non-negative integer counts.” Page 145 states that serious-crash-only SPFs were considered but excluded because of significant underdispersion.

## 4. Exposure Handling

- Exposure variable used, if any: Vehicle exposure and pedestrian exposure.
- Traffic count source:
  - Vehicle AADT: HPMS where available, INRIX-derived AADT for some segments, and random-forest data-fusion estimates where HPMS/INRIX were unavailable.
  - Pedestrian exposure: AADPT estimated from traffic signal push-button derived pedestrian counts, short-duration video pedestrian counts, and a data-fusion model applied to all urban intersections.
- Whether exposure is modelled, observed, assumed, or ignored: Mixed. Vehicle AADT is observed or externally estimated for many links, with modelled estimates for missing cases. Pedestrian AADPT is observed at a subset of intersections and modelled for system-wide coverage.
- Treatment of missing or sparse traffic counts:
  - Vehicle AADT gaps are filled by INRIX estimates or a random forest data-fusion model using connected segment volumes, functional classification, access to jobs, network centrality, and urban area.
  - Pedestrian AADPT gaps are filled by data-fusion models tested using negative binomial mixed effects, random forest, XGBoost, and neural-network approaches.
- Whether offset terms, rates, denominators, or normalisation are used: The SPF models use AADT and AADPT as explanatory exposure variables, not as an explicit offset. The report does not present an exposure offset term for the pedestrian crash-frequency SPFs.
- Evidence quote or page reference: Page 82 states that final crash-frequency models considered “only vehicle volume and pedestrian volume.” Page 47 states that missing AADT can be estimated using a data-fusion model. Page 58 states that push-button-derived pedestrian counts are treated as continuous/permanent pedestrian counters, and page 62 states that data fusion is used to estimate pedestrian volumes at all urban intersections.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes:
  - Mathematical exposure concept: high transferability. The paper strongly supports including both motor-vehicle exposure and relevant vulnerable-road-user exposure when modelling pedestrian crash frequency.
  - Specific pedestrian exposure source: low-to-medium transferability. Traffic-signal push-button data and Oregon-specific pedestrian count infrastructure may not be available in the Open Road Risk road-link pipeline.
  - Vehicle AADT gap-filling approach: medium transferability. The idea of combining authoritative count sources with model-based imputation is highly relevant, but the paper uses Oregon HPMS/INRIX/OSM workflows rather than UK AADF/WebTRIS/OS Open Roads.
  - Offset structure: low direct transferability because the paper does not use an offset formulation comparable to `log(AADT × link_length_km × 365 / 1e6)`.

## 5. Spatial Unit of Analysis

- Unit: Intersection.
- Segment length or segmentation rule: Not applicable to the SPF models. The data-development process also creates segment datasets, but the main SPF output is intersection-based.
- How crashes are assigned to the network: Crash records with latitude/longitude are joined to intersection points; crash-derived traffic-control signals are also used to infer traffic signal presence. The exact pedestrian-crash assignment buffer/rule for SPF construction is not fully stated in the extracted main sections.
- Treatment of junctions/intersections: Intersections are classified by number of legs, traffic control, marked-crossing presence, geographic area, and state/non-state system. Complex intersections are simplified using edge/node contraction so divided roads and lane-level geometries do not inflate the number of legs.
- Spatial aggregation risks: Intersection contraction, crash assignment near complex junctions, and traffic-control inference from crash reports can introduce classification errors. Manual validation was used for some typology issues.
- Evidence quote or page reference: Page 50 describes classifying nodes into driveways, three-leg, four-leg, and five-or-more-leg intersections and applying a contraction algorithm for complex geometries. Page 51 states that 908 intersections, 1.5% of about 64,000 intersection nodes, required manual classification. Page 56 reports 3,144 unique traffic signals after integrating multiple sources.
- Relevance to OS Open Roads link-based pipeline: Medium. The intersection-typology and contraction logic is useful for future junction-complexity work, but the main unit is not compatible with Open Road Risk’s current OS Open Roads link-year unit without a separate intersection layer or a link-to-junction feature join.

## 6. Temporal Unit of Analysis

- Years covered:
  - Pedestrian short-duration counts: 2017–2023.
  - Traffic signal push-button pedestrian volumes: calculated where at least 350 days of data are available; specific years not fully stated in the extracted main text.
  - Crash data mentioned for traffic-control mining: 2007–2022.
  - SPF outcome period: Not stated clearly in the extracted SPF method sections.
- Temporal resolution: Annual average daily exposure measures: AADT and AADPT. Short-duration pedestrian counts are expanded to annual average pedestrian volume.
- Whether seasonality or time-of-day is modelled: Seasonality is handled for pedestrian short-duration count expansion using annual factoring methods, including AASHTO and day-of-year factors. Time-of-day is not used directly in the final SPF models.
- Whether before-after or panel structure is used: No before-after design stated. The pedestrian-volume data-fusion statistical model uses a mixed-effects structure for grouped/panel differences by urban area; the final SPF models are cross-sectional crash-frequency SPFs by intersection typology.
- Evidence quote or page reference: Page 59 describes AASHTO and day-of-year factors to expand short-duration pedestrian counts. Page 75 describes independent 10-fold cross-validation of 868 AADPT observations. Page 64 describes the mixed-effects negative binomial model for pedestrian-volume estimation.
- Relevance to WebTRIS-style time profiles: Medium. The paper’s pedestrian-count expansion process is conceptually relevant to turning short-duration counts into annual exposure estimates. It is not directly a motor-traffic time-zone profile model.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Entering vehicle AADT | HPMS, INRIX, modelled AADT | Sum entering-leg AADT after intersection typology/contraction | Core vehicle exposure in pedestrian SPF | Medium; AADF/AADT equivalent exists, but link-to-intersection aggregation would need a junction layer |
| Pedestrian AADPT | Push-button signal actuations; short-duration video counts | Permanent-count style annualisation and data-fusion model to estimate all urban intersections | Core pedestrian exposure in pedestrian SPF | Low-to-medium; useful concept, but UK open pedestrian exposure data may be sparse |
| Intersection typology | OSM/base network/all-streets network | Node classification plus edge/node contraction for complex geometries | Separates 3-leg vs 4-leg and handles divided roads | Medium; useful for future junction complexity features |
| Traffic signal presence | ODOT, Portland, Eugene, OSM, crash reports | Integrated signal inventory plus crash-data mining rules | Splits signalized/unsignalized models | Medium; OSM signal tags exist but coverage and crash-derived inference may differ |
| Marked crossing presence | Pedestrian crossing / OpenSidewalks-style data, local data | Crossing and crossing-distance development step | Splits marked/no-marked crossing models | Low-to-medium; OSM crossings exist but uneven coverage |
| Transit stop proximity | GTFS | Counts within 50m and 100m buffers | Pedestrian activity proxy / candidate exposure predictor | High as a candidate contextual feature if GTFS is available |
| Network density | Base and all-streets networks | Link density by class within buffers | Captures connectivity and urban form | High; already similar to network features in Open Road Risk / compare implementation |
| Betweenness centrality | Base/all-streets networks; AADT impedance | igraph betweenness using shortest paths with AADT as impedance | Captures network importance/connectivity | High conceptually; already present / compare implementation |
| Strava pedestrian activity | Strava walk/jog/run trips | Aggregated trips within 10m and 25m buffers | Proxy for pedestrian activity in AADPT model | Low for open-data production; may be proprietary/commercial |
| Access/connectivity to jobs, schools, parks, amenities | Census, EPA Smart Location Database, network routing | Walk/drive-shed access measures | Strong predictors for pedestrian-volume model | Medium; similar UK census/accessibility measures are possible |
| Operational speed | INRIX probe speeds | Network conflation from INRIX XD to base OSM network; speed summaries | Candidate predictor for pedestrian exposure/risk | Low-to-medium; UK open speed trace coverage may be limited |
| Census and sociodemographic measures | Census geographies, SLD | Segment/intersection apportionment and joins | Demand/risk context | Medium; UK census/IMD transferable in principle |

Only features actually used or explicitly developed in the report are included. Many detailed contextual features were developed, but final SPF models deliberately used only vehicle and pedestrian exposure.

## 8. Model Architecture

- Algorithms/models used:
  - Pedestrian-volume estimation: mixed-effects negative binomial, random forest, XGBoost, neural-network approaches tested; random forest selected for final AADPT prediction.
  - SPF crash-frequency models: Poisson first, then negative binomial where overdispersion was significant.
- Baseline model: For crash SPFs, Poisson count model. For pedestrian AADPT data fusion, negative binomial mixed-effects model is used as a statistical comparator.
- Final/preferred model:
  - Pedestrian AADPT: random forest using the `caret` package, selected because of cross-validation performance and reasonable statewide predictions.
  - Crash SPF: typology-specific Poisson or negative binomial exposure-only models using vehicle AADT and pedestrian AADPT.
- Loss function or likelihood, if stated:
  - Poisson likelihood and negative binomial likelihood are described.
  - Machine learning models are selected using RMSE, mean/median absolute percent error, and R².
- Offset/exposure term, if used: No explicit offset term stated for final SPF models. AADT and AADPT enter as exposure predictors.
- Spatial autocorrelation handling: No explicit spatial autocorrelation model for final SPFs. Future work suggests considering spatial heterogeneity.
- Temporal dependence handling: Not stated for final SPFs.
- Interpretability method:
  - SPF models are interpretable through coefficient signs and significance.
  - CURE plots are used for model-fit diagnostics.
  - Machine-learning pedestrian-volume models use variable importance.
- Evidence quote or page reference: Pages 82–85 describe Poisson, dispersion testing, and negative binomial modelling. Page 75 reports 10-fold cross-validation for AADPT models. Page 80 explains why the random forest `caret` model was selected. Page 85 says CURE plots and model summaries are presented for the SPF models.

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---:|---:|---|---|---|
| AADPT model validation | RMSE | 434 | Negative binomial | Worse than ML alternatives on RMSE | Table 3.7, p. 75 |
| AADPT model validation | R² | 0.51 | Negative binomial | Moderate cross-validated fit | Table 3.7, p. 75 |
| AADPT model validation | RMSE | 397 | Poisson | Better than NB, worse than RF | Table 3.7, p. 75 |
| AADPT model validation | R² | 0.56 | Poisson | Moderate cross-validated fit | Table 3.7, p. 75 |
| AADPT model validation | RMSE | 336 | Random forest, ranger | Best RMSE | Table 3.7, p. 75 |
| AADPT model validation | R² | 0.67 | Random forest, ranger | Strongest or near-strongest cross-validated fit | Table 3.7, p. 75 |
| AADPT model validation | RMSE | 337 | Random forest, caret | Near-best RMSE | Table 3.7, p. 75 |
| AADPT model validation | R² | 0.68 | Random forest, caret | Highest R² in Table 3.7 | Table 3.7, p. 75 |
| AADPT model validation | RMSE | 365 | XGBoost | Better than Poisson/NB but worse than RF | Table 3.7, p. 75 |
| AADPT model validation | Median absolute % error | 28% | XGBoost | Lowest median APE, but application produced negative estimates | Table 3.7, p. 75; Table 3.8, p. 80 |
| AADPT model application sanity check | Minimum predicted AADPT | -61.6 | XGBoost | Invalid negative pedestrian volumes | Table 3.8, p. 80 |
| AADPT model application sanity check | Maximum predicted AADPT | 649,564,547 | Negative binomial | Implausible extreme values | Table 3.8, p. 80 |
| AADPT model application sanity check | Maximum predicted AADPT | 5,912 | Random forest, caret | Plausible range; selected final AADPT model | Table 3.8, p. 80 |
| AADT imputation | Median absolute percent error | Less than 20% in most models; as low as <1% | Random forest AADT data fusion | Used to fill missing vehicle AADT | Figure 3.6 / p. 47–48 |
| Traffic-signal mining validation | Balanced accuracy | 91.7% | Recursive partitioning model | Initial traffic-signal inference model | p. 54 |
| Traffic-signal mining validation | Sensitivity | 97.5% | Recursive partitioning model | High signal detection sensitivity | p. 54 |
| Traffic-signal mining validation | Specificity | 86% | Recursive partitioning model | Lower specificity, false positives possible | p. 54 |
| Traffic-signal rule validation | Accuracy | 94% | Conservative crash-data mining rules | Manual review of 50 inferred signalized intersections | p. 56 |
| SPF summary | Direction/significance | Vehicle and pedestrian volume generally positive; stronger consistency for 4-leg and large non-state samples | SPF models | Supports exposure-only pedestrian SPF usability but with limitations | Chapter 4 tables; summary p. 144 |
| SPF diagnostics | CURE plots | Mostly qualitative | SPF models | Used to assess cumulative residual behaviour; no single numeric predictive metric | Chapter 4 |

After the table:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated?
  - AADPT data-fusion metrics are 10-fold cross-validated.
  - AADT imputation metrics are 10-fold cross-validated.
  - Traffic-signal recursive partitioning is reported from 10-fold cross-validation and then a small manual validation of the conservative rules.
  - SPF model diagnostics appear to be in-sample fit diagnostics using coefficient significance, log-likelihood/model fit comparisons, and CURE plots. The report does not state a held-out, spatial holdout, temporal holdout, or external validation design for the final SPF crash models.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy.
  - The SPF CURE plots should be treated as in-sample diagnostics unless a held-out process is stated elsewhere.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else?
  - AADPT and AADT data-fusion metrics test cross-validated predictive performance for exposure estimation.
  - CURE plots and coefficient summaries test model fit and functional-form adequacy, not external predictive generalisation.
  - The report does not provide a direct hotspot-ranking performance metric.
- Are any metrics likely to be optimistic for real-world deployment?
  - The SPF CURE plots and coefficient summaries may be optimistic if used as evidence of predictive generalisation, because they are not clearly held-out validation.
  - The AADPT cross-validation is more credible but still may not reflect spatial transfer to areas with systematically different pedestrian-count coverage.
- Which metric, if any, is most relevant to Open Road Risk?
  - For exposure modelling: cross-validated RMSE/R² and application sanity checks for predicted exposure distributions are highly relevant.
  - For collision-risk modelling: CURE plots are relevant as a GLM diagnostic, but they do not replace grouped/spatial/temporal validation.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The paper uses count-data models, primarily Poisson with overdispersion testing and negative binomial models where needed. The final approach does not use a zero-specific model, though the limitations section explicitly discusses possible future models to account for zeros.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson and negative binomial are used. Zero-specific models are only discussed as possible future work; no zero-inflated SPF is reported as a final model.
- Whether high-risk locations are evaluated separately: Not stated as a separate high-risk-location validation. The purpose is systemic SPF/network screening support.
- Evidence quote or page reference: Page 82 states Poisson and negative binomial frameworks are considered. Page 84 states negative binomial is estimated where significant overdispersion is present. Page 145 says preliminary results suggest no significant zero-related effects but that more sophisticated models for zeros may improve model fit and crash estimation.
- Practical relevance to my sparse collision link-year dataset: Medium. The paper supports Poisson/NB count modelling and explicit dispersion testing. It does not directly solve the much larger zero-heavy road-link-year case, and it does not provide a production-ready zero-heavy framework.

Important:

- The phrase `zero-inflated` is not used here as a fitted model label because the report does not state that a zero-inflated SPF was fitted as the final model.
- The data are zero-heavy in some disaggregated cases, but zero-heavy counts are handled using Poisson/NB and diagnostic discussion, not a final zero-specific model.

## 11. Validation Strategy

- Train/test split method:
  - AADPT model: independent 10-fold cross-validation of 868 AADPT observations.
  - AADT data-fusion model: 10-fold cross-validation.
  - Traffic-signal inference: 10-fold cross-validation for recursive partitioning plus manual review of 50 inferred signalized intersections using conservative rules.
  - SPF crash models: No train/test split stated in the main SPF methodology sections.
- Spatial holdout used? no / not stated
- Temporal holdout used? no / not stated
- Grouped holdout used? not stated
- Cross-validation type:
  - 10-fold cross-validation for AADPT data-fusion model.
  - 10-fold cross-validation for AADT data-fusion model.
  - 10-fold cross-validation for recursive partitioning traffic-signal inference model.
- Metrics:
  - AADPT: RMSE, absolute percent error, mean absolute percent error, median absolute percent error, R².
  - AADT: median absolute percent error.
  - SPF: CURE plots, coefficient sign/significance, log-likelihood/model fit comparison in appendices; no held-out predictive metrics stated.
- External validation: Not stated for SPF crash models.
- Leakage or generalisation risks:
  - Exposure models may generalise poorly where pedestrian-count collection is non-representative or where push-button/signal data are unavailable.
  - Crash-data mining for traffic-control assignment uses crash reports to infer traffic signals. This is not necessarily leakage for exposure-only SPFs if traffic control is used only for typology construction, but it is a methodological dependency on post-event crash-report attributes. For Open Road Risk, similar use of crash-derived context would need clear separation from model features and careful documentation.
  - The final SPF model fit evidence appears mainly in-sample, so it should not be treated as deployment predictive accuracy.
- Evidence quote or page reference: Page 75 describes 10-fold cross-validation for the AADPT models. Page 47–48 describes 10-fold cross-validation for AADT data fusion. Pages 54–56 describe traffic-signal inference validation. Pages 82–85 describe count-model diagnostics and CURE plots.
- What I should copy or avoid:
  - Copy: exposure-model cross-validation plus applied-distribution sanity checks; CURE plots for GLM diagnostics; typology-specific model diagnostics; explicit dispersion testing.
  - Avoid: treating in-sample CURE plots or coefficient significance as evidence of external predictive generalisation; relying on crash-derived variables as production predictors without leakage review.

## 12. Key Findings Relevant to My Project

1. 
- Finding: Pedestrian crash SPFs in this report were ultimately kept exposure-only, using vehicle AADT and pedestrian AADPT.
- Why it matters: This supports a disciplined baseline-first modelling approach: exposure can carry substantial signal, and complex contextual models should be justified by clear diagnostic or validation improvement.
- Evidence quote or page reference: Page 82 states that usability was chosen over complex specifications, leading all crash-frequency models to consider only vehicle and pedestrian volume.
- Confidence: high

2. 
- Finding: Exposure estimation quality is treated as a modelling problem in its own right, with cross-validation and application sanity checks.
- Why it matters: This directly supports Open Road Risk’s concern that Stage 1a AADT uncertainty should be documented and sanity-checked before being used in Stage 2 collision models.
- Evidence quote or page reference: Table 3.7 on page 75 reports cross-validated AADPT metrics; Table 3.8 on page 80 shows that otherwise good-looking models can produce implausible applied predictions.
- Confidence: high

3. 
- Finding: The selected AADPT model was not chosen by one metric alone; random forest was selected because cross-validation results and statewide application behaviour were reasonable.
- Why it matters: This is a useful guardrail for Open Road Risk: model selection should include distributional plausibility on the full network, not only validation scores.
- Evidence quote or page reference: Page 80 states that the random forest model was chosen based on producing reasonable values when applied and its cross-validation results.
- Confidence: high

4. 
- Finding: Intersection typology and complex-intersection simplification are substantial data-engineering tasks, not trivial joins.
- Why it matters: If Open Road Risk adds junction features, it should probably treat junction construction as a dedicated feature-engineering component with validation, not a quick OSM tag join.
- Evidence quote or page reference: Pages 50–51 describe node classification, contraction for complex geometries, validation using crash data, and manual review of 908 intersections.
- Confidence: high

5. 
- Finding: Smaller disaggregated groups produced unstable or insignificant SPF results, especially in some 3-leg and no-marked-crossing cases.
- Why it matters: This supports caution before splitting Open Road Risk’s Stage 2 models too finely by facility family, region, road class, or urban/rural type without checking sample size and zero counts.
- Evidence quote or page reference: Page 144 states that 3-leg intersections had fewer crashes and more zero-crash intersections, causing issues for disaggregated model estimates.
- Confidence: medium-high

6. 
- Finding: The paper explicitly flags estimated exposure as a source of counterintuitive SPF behaviour.
- Why it matters: Open Road Risk’s production risk percentile uses estimated AADT; uncertainty propagation or exposure-quality diagnostics are not optional polish if rankings are sensitive to exposure estimates.
- Evidence quote or page reference: Page 145 states that both vehicle and pedestrian volumes are estimates and that unexpected/counterintuitive results may stem from exposure-estimation error.
- Confidence: high

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Exposure model application sanity checks | Detects implausible full-network predictions even when CV metrics look acceptable | Stage 1a predictions; observed count distributions | Applied to all Oregon urban intersections for AADPT | High; directly relevant to full-network AADT estimates | Stage 1a / validation / documentation | Low | Passing CV but producing collapsed or implausible network-wide AADT |
| Cross-validated exposure imputation | Treats missing exposure as a modelling task with measurable uncertainty | AADF/WebTRIS counts; road/context features | 868 AADPT observations; AADT network with HPMS/INRIX/model sources | High | Stage 1a / validation | Medium | Spatial transfer may be weaker than random CV suggests |
| CURE plots for GLM crash model | Useful GLM functional-form and residual diagnostic | Stage 2 GLM predictions/residuals | Many disaggregated Oregon intersection models | Medium-high; useful for GLM baseline, not XGBoost alone | Stage 2 / validation | Medium | Misread as predictive validation |
| Poisson-first dispersion testing then NB where needed | Disciplined count-model workflow | Link-year crash counts; exposure offset/predictors | Urban intersection SPFs | High for GLM baseline | Stage 2 / validation | Low-medium | Over-splitting can make dispersion estimates unstable |
| Intersection typology/contraction workflow | Helps produce junction-complexity features and avoid divided-road artefacts | OS Open Roads/OSM/all-streets network | About 64,000 Oregon intersections | Medium; scalable but non-trivial on UK network | future feature / feature engineering | High | Bad contraction or junction assignment contaminates features |
| Applied-distribution checks for model selection | Prevents selecting models with invalid predictions | Full-network prediction frame | AADPT RF vs NB vs XGBoost comparison | High | Stage 1a / Stage 2 validation | Low | Over-focusing on a single score such as R² |
| Exposure-only baseline comparison | Clarifies added value of contextual features | AADT/exposure and crash counts | Oregon SPF models | High | Stage 2 / baseline comparison | Low | Baseline may be underfit if used as final answer without diagnostics |
| Facility-family disaggregation checks | Tests whether separate models by road/intersection class are stable | Road class, urban/rural, sample sizes, crash counts | 3-leg/4-leg, signalized/unsignalized, marked/no-marked crossing | Medium | Stage 2 / validation | Medium | Small strata create unstable rankings |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Traffic signal push-button pedestrian AADPT estimation | UK-wide open data equivalent is unlikely to exist | Continuous pedestrian push-button actuation data and local calibration | 558 signal intersections with at least 350 days of data | Low for current road-link pipeline | Use OSM crossings, census, land use, transit, pedestrian-demand proxies; pilot only where counts exist | High |
| Strava pedestrian activity as production feature | Likely proprietary/commercial and biased toward recreational users | Strava Metro-style pedestrian trip data | Aggregated around Oregon intersections | Low for open-source production | Treat as optional validation/pilot layer, not core open pipeline | Medium-high |
| Oregon-specific SPF equations | Region-specific, intersection-specific, and pedestrian-specific | Oregon urban intersection data and AADPT | Oregon urban intersections | Low for direct production | Copy modelling discipline, not coefficients | High |
| Crash-data mining to infer traffic-control inventory | Uses crash-report attributes to construct infrastructure inventory; may be unavailable or leakage-sensitive | Long crash history with traffic-control fields | Oregon crash records 2007–2022 | Low-to-medium | Use OSM/official signal inventories; use crash-derived signals only for diagnostic QA | Medium |
| Serious-crash-only SPF as presented | The paper did not present a working production model; it says serious-only models needed complex underdispersion handling | Enough fatal/incapacitating pedestrian crashes and specialised count models | Oregon pedestrian intersection crashes | Low for immediate adoption | Document severity limitation; pilot separate severity models later | High |

Important scale note: the Oregon report’s main SPF scale is urban intersections, including about 64,000 developed intersection nodes before disaggregation. Open Road Risk is a road-link-year pipeline with around 2.17 million links and about 21.7 million link-year rows. Statistically attractive but computationally or data-engineering-heavy methods should therefore be piloted before being considered for production.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk?
  - Yes, conceptually. It strongly supports exposure-aware crash modelling, especially the need for both vehicle exposure and vulnerable-user exposure in pedestrian safety. It does not specifically support the exact Open Road Risk offset formula because its SPFs use exposure variables as predictors, not a link-length exposure offset.
- Does it suggest better handling of AADT/AADF uncertainty?
  - Yes. The strongest transferable lesson is to validate exposure models independently, inspect applied prediction distributions, and treat exposure errors as a likely cause of counterintuitive risk-model behaviour.
- Does it suggest useful geometry or road-context features?
  - Yes, but mainly as diagnostic or future-feature support. The paper developed network density, centrality, speed, crossing, transit, access/connectivity, and sociodemographic features, but final SPF models did not use them because the authors prioritised usability.
- Does it suggest better modelling of junctions?
  - Yes. It provides strong support for a dedicated junction-typology and contraction workflow before deriving intersection-level features.
- Does it suggest better treatment of severity?
  - Only cautiously. The paper notes that fatal/incapacitating pedestrian crash models were considered but not presented because of significant underdispersion and the need for alternate count models.
- Does it suggest better validation design?
  - Yes for exposure models: cross-validation plus full-network sanity checks. For crash SPFs, it supports CURE plots and dispersion testing, but it does not provide strong held-out crash prediction validation.
- Does it expose a weakness in my current approach?
  - Yes. If Open Road Risk’s XGBoost production risk percentile depends heavily on estimated AADT, then full-network exposure distribution checks and uncertainty/sensitivity diagnostics are needed. The report is also a warning against over-splitting models by facility type before checking sample size, zeros, and fit.

## 15. Repo Actionability

1. 
- Suggested repo action: Add a Stage 1a “applied exposure sanity check” page/table comparing observed AADF, held-out predictions, and full-network estimated AADT distributions by road class, urban/rural, trunk/primary, and region.
- Action type: diagnostic
- Relevant stage: Stage 1a / validation / documentation
- Why the paper supports it: The Oregon report chose the AADPT model partly because its applied statewide predictions were plausible, while other models produced negative or absurdly large estimates.
- Evidence quote or page reference: Table 3.8, page 80.
- Effort: low-medium
- Risk if implemented badly: Cosmetic distribution plots could miss systematic spatial failure if not stratified by important road classes/geographies.

2. 
- Suggested repo action: Add a short documentation note distinguishing exposure-model validation from crash-model validation.
- Action type: documentation note
- Relevant stage: documentation / validation
- Why the paper supports it: The report validates exposure data-fusion models separately from SPF model diagnostics.
- Evidence quote or page reference: Table 3.7, page 75; Chapter 4 SPF diagnostics.
- Effort: low
- Risk if implemented badly: Users may incorrectly treat AADT model R² as evidence that risk rankings are externally valid.

3. 
- Suggested repo action: Add CURE-style plots or equivalent cumulative residual diagnostics for the Stage 2 Poisson GLM baseline, stratified by exposure and key predictors.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The Oregon report uses CURE plots throughout Chapter 4 to assess crash-frequency model fit over the range of crash values.
- Evidence quote or page reference: Page 85 and Chapter 4 figures.
- Effort: medium
- Risk if implemented badly: CURE plots could be oversold as predictive validation rather than in-sample fit diagnostics.

4. 
- Suggested repo action: Pilot a junction-feature construction notebook using OSM/OS Open Roads to classify nearby junction type, signal proxy, crossing proxy, and leg count for links.
- Action type: small pilot
- Relevant stage: future feature / feature engineering
- Why the paper supports it: The report shows that intersection typology, traffic-control assignment, and crossing status are central to pedestrian SPFs and require careful data engineering.
- Evidence quote or page reference: Pages 50–56.
- Effort: high
- Risk if implemented badly: Junction misclassification could add noise or create false precision in route/link difficulty scores.

5. 
- Suggested repo action: Add a facility-family split diagnostic before fitting separate production models by road class or urban/rural type.
- Action type: diagnostic / baseline comparison
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Disaggregated Oregon SPF models became unstable where sample sizes were small and zero counts were common, especially for some 3-leg/no-marked-crossing groups.
- Evidence quote or page reference: Page 144 summary.
- Effort: medium
- Risk if implemented badly: Separate models may produce unstable percentile rankings for sparse strata.

## 16. Query Tags

- pedestrian-SPF
- Oregon
- urban-intersections
- AADT
- AADPT
- pedestrian-exposure
- exposure-model-validation
- data-fusion
- random-forest
- XGBoost
- negative-binomial
- Poisson
- dispersion-testing
- CURE-plots
- intersection-typology
- traffic-signal-inference
- marked-crossings
- zero-heavy-counts
- underdispersion
- vulnerability-user-risk

## 17. Confidence and Gaps

- Overall confidence in extraction: medium-high
- Important details not stated in the paper:
  - The exact SPF crash outcome period is not clearly stated in the main SPF methodology sections extracted here.
  - The exact crash-to-intersection assignment rule/buffer for pedestrian SPF outcomes is not fully stated in the extracted sections.
  - Full coefficient estimates and likelihood metrics are in appendices and were not exhaustively transcribed into this metadata record.
  - The report does not state a held-out, spatial, temporal, grouped, or external validation process for the final crash SPFs in the main Chapter 4 methodology.
- Parts of the paper that need manual checking:
  - Appendix B and Appendix C if exact coefficients, standard errors, log-likelihoods, or dispersion parameters are needed.
  - Appendix A if comparing exposure-only vs full contextual SPF models in detail.
  - Data-development appendix if precise crash assignment rules are needed.
- Any likely ambiguity or risk of misinterpretation:
  - The report’s AADPT data-fusion models are cross-validated, but this should not be confused with external validation of the crash SPF models.
  - The report supports exposure-aware modelling but not necessarily Open Road Risk’s exact exposure-offset structure.
  - Crash-derived traffic-control inference is useful for inventory QA but could be inappropriate as a production feature if not separated carefully from outcome modelling.
  - Some exposure and SPF results are Oregon-specific and intersection-specific; coefficients should not be transferred directly to UK OS Open Roads links.
