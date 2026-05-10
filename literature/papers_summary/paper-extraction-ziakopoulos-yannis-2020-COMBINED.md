# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: A review of spatial approaches in road safety.pdf
- Suggested Markdown filename: final-ziakopoulos-yannis-2020-spatial-review.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: original PDF plus two Markdown extractions
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The uploaded PDF text was accessible. This is a literature review, not a primary empirical modelling paper, so reported quantitative values mainly describe findings from reviewed studies rather than original estimates. Exact details of individual cited studies should be checked in the original cited papers before being used as primary evidence.

## 1. Citation

- Title: A review of spatial approaches in road safety
- Authors: Apostolos Ziakopoulos; George Yannis
- Year: Not explicitly stated in the visible PDF metadata. The review cites studies up to 2019, so it appears to be circa 2020, but the year should be recorded as `Not stated` unless confirmed elsewhere.
- DOI or URL, if present: Not stated
- Country / region studied: International / multiple countries
- Study setting: Mixed; reviewed studies include road segments, intersections, corridors, grids, traffic analysis zones, census/geographic zones, regional units, urban/rural settings, and vulnerable-road-user analyses.

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper critically reviews how road-safety research handles spatial analysis, including spatial-unit choice, spatial dependence, spatial heterogeneity, boundary effects, MAUP, proximity structures, vulnerable-road-user studies, and spatial modelling approaches.
- Main purpose: literature review / methodological review.
- Evidence quote or page reference: Page 1 states that the aim is to “critically review the existing literature on different spatial approaches” used to handle the dimension of space in road-safety analyses.

## 3. Response Variable

- Target variable: Not a single target variable. Reviewed studies use crash counts, crash rates, injury severity rates, casualty rates, hotspot classifications, crash costs, and spatial crash distributions.
- Collision type: Mixed. The paper’s review tables distinguish total crashes, motorcycle crashes, single-vehicle crashes, vehicle-vehicle crashes, bicycle-vehicle crashes, pedestrian-vehicle crashes, and other specific categories.
- Severity handling: Mixed across reviewed studies. Some models address severity-specific outcomes, multivariate severity models, or joint crash-frequency/severity approaches. The review itself does not fit a severity model.
- Count, binary, rate, risk score, severity class, or other: Mixed across reviewed studies.
- Time window used for outcomes: Mixed across reviewed studies.
- Evidence quote or page reference: Page 3 states that spatial analyses examine road-safety indicators such as crash counts or rates and injury severity rates across spatial units. Page 4 defines crash-category abbreviations used in the review tables.

## 4. Exposure Handling

- Exposure variable used, if any: Mixed across reviewed studies. Exposure examples include traffic volume, AADT, vehicle distance travelled / VMT, road length, population, trips, and vulnerable-road-user exposure variables such as walking hours.
- Traffic count source: Mixed / study-specific; no single data source.
- Whether exposure is modelled, observed, assumed, or ignored: Mixed. Some studies include exposure variables, some use rates/denominators, some model or estimate vulnerable-road-user exposure, and some hotspot/spatial-statistic methods do not explicitly model exposure.
- Treatment of missing or sparse traffic counts: Not a central topic of the review. Sparse or estimated AADT handling is not discussed in a way that directly supports Open Road Risk’s Stage 1a design.
- Whether offset terms, rates, denominators, or normalisation are used: Mixed. The paper reviews count/rate models and exposure variables but does not prescribe a single offset structure.
- Evidence quote or page reference: Page 9 discusses zonal factors such as VMT shared by segments and intersections inside zones. Page 23 states that exposure parameters such as road length, AADT, and vehicle distance travelled generally increase crash risk overall, while also warning that exceptions exist.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes:
  - Conceptual transferability is high: exposure, spatial scale, and spatial dependence need to be considered together.
  - Direct mathematical transferability is mixed: the review does not validate a specific exposure-offset formulation.
  - Data-source transferability is variable: AADT/VMT studies are closer to Open Road Risk; VRU trip/walking-hour/survey-heavy studies are less directly transferable.

Important:

- Do not cite this review as proof that Open Road Risk’s exact `log(AADT × link_length_km × 365 / 1e6)` offset is optimal.
- Do cite it as support for documenting spatial-unit choice, exposure choice, spatial dependence, and hotspot sensitivity.

## 5. Spatial Unit of Analysis

- Unit: Mixed. Reviewed units include road segments, intersections, corridors, grids, fixed-distance cells, TAZs, TSAZs, census blocks, census block groups, census tracts, ZIP codes, census wards, traffic analysis districts, cities, counties, states, and conditional/link-based units.
- Segment length or segmentation rule: Mixed. Reviewed studies use road links/segments, homogeneous highway sections, fixed-length/lixel approaches for network KDE, grids, zones, regions, and multi-level segment/intersection/corridor structures.
- How crashes are assigned to the network: Mixed. Reviewed methods include link-based crash mapping, aggregation to zones, boundary assignment rules, KDE, network KDE, and spatial models with proximity weights.
- Treatment of junctions/intersections: Intersections are reviewed separately and jointly with road segments/corridors. The review highlights that intersection geometry, turning movements, signal phase coordination, and number of legs can matter, and that connected intersections and segments can be spatially correlated.
- Spatial aggregation risks: Boundary problem, MAUP, spatial proximity-structure sensitivity, spatial dependence, spatial heterogeneity, transferability limits, and hotspot sensitivity.
- Evidence quote or page reference: Page 3 states that spatial-unit selection directly influences scope, interpretability, and data preparation. Pages 4–5 discuss road-segment and intersection approaches and joint segment/intersection modelling. Pages 10–12 discuss boundary problems, MAUP, and spatial proximity structures.
- Relevance to OS Open Roads link-based pipeline: High. The review directly supports documenting that OS Open Roads links are a modelling choice with consequences for interpretability, boundary assignment, segment/junction interactions, and spatial dependence.

## 6. Temporal Unit of Analysis

- Years covered: Mixed across reviewed studies.
- Temporal resolution: Mixed; reviewed studies include annual, multi-year, daily, weekly, hourly, and spatio-temporal designs.
- Whether seasonality or time-of-day is modelled: Some reviewed studies examine time-of-day hotspots, daily/weekly/hourly prediction, weather/time interactions, and spatio-temporal effects.
- Whether before-after or panel structure is used: Mixed; empirical Bayes before-after and spatio-temporal hierarchical models are discussed among reviewed methods.
- Evidence quote or page reference: Page 13 states that hotspots can vary considerably across time of day. Page 19–20 discusses daily/weekly prediction comparisons in CNN/econometric work.
- Relevance to WebTRIS-style time profiles: Medium. The paper supports the general idea that spatial risk varies over time, but it does not specifically validate WebTRIS-derived time fractions or Open Road Risk’s Stage 1b workflow.

## 7. Engineered Features

This is a review paper. The table lists feature families explicitly discussed across reviewed studies.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Spatial unit definition | Road network / GIS / administrative data | Segment, intersection, corridor, grid, TAZ, census, or regional aggregation | Determines interpretability, model parameters, and hotspot identification | High; document OS Open Roads link choice |
| Traffic volume / AADT | Traffic counts or estimates | Used as covariate, rate denominator, exposure, or model input | Core exposure factor in many reviewed studies | Already present / compare uncertainty |
| Vehicle distance travelled / VMT | AADT × road length or trip data | Zonal/segment exposure measure | Connects volume and network length | Already analogous to exposure offset |
| Road length / segment length | Network geometry | Direct measurement or aggregation | Exposure and scale effect | Already present |
| Spatial adjacency / proximity weights | Network or zonal geometry | 0–1 adjacency, common-boundary length, centroid distance, crash-weighted centroid distance, route-informed adjacency, hierarchical weights | Defines spatial dependence and spillover structure | Medium to high as diagnostic |
| Road type / class | Road inventory | Segment/corridor classification | Different road types have different safety mechanisms | Already present |
| Intersection density / crosswalk density / unsignalized intersection density | Road/infrastructure GIS | Count or density within zone/segment/corridor | Urban conflict proxy | Candidate feature / junction diagnostic |
| Number of lanes / median opening density / access density | Road inventory | Counts/densities | Captures complexity and conflict opportunities | Candidate where coverage allows |
| Speed / speed limit / mean speed | Road inventory, probe data, traffic data | Segment or zonal summaries | Risk/context variable | Candidate/present partly |
| Curvature | Road geometry | Derived from segment geometry | Road-alignment risk factor | Candidate/present |
| Gradient / grade | Terrain/road inventory | Derived from DEM or inventory | Alignment risk factor; data availability can limit use | Candidate via OS Terrain 50 |
| Population / socioeconomic variables | Census/geodemographic data | Density, income, employment, school enrolment, deprivation, demographic composition | Macro/zonal and VRU risk context | Population density/IMD transferable |
| Land use / employment / network density / trip-generation density | Land-use and planning data | Zonal densities/accessibility measures | Activity and demand proxies | Medium as future context features |
| Weather variables | Weather stations / gridded weather | Spatial/temporal assignment to crashes or units | Important for some spatio-temporal analyses | Low to medium; data-source quality matters |
| VRU exposure | Travel surveys, trip estimates, walking hours, pedestrian/bicycle counts | Exposure models or denominators | Necessary for pedestrian/cycle crash risk | Low currently unless data added |
| Hotspot indicators / PSI | Model outputs and observed crashes | Potential safety improvement, KDE, Moran’s I, Getis-Ord Gi*, EB/FB rankings | Prioritisation and network screening | Medium; conceptually related to risk ranking |
| Network centrality / space syntax | Road network graph | Connectivity, local/global integration, betweenness-like measures | Captures network structure and movement potential | Already relevant / compare implementation |

## 8. Model Architecture

- Algorithms/models used: Review covers Poisson GLMs, negative binomial GLMs, Poisson-lognormal models, zero-inflated and hurdle variants in specific studies, GWR, geographically weighted negative binomial regression, semi-parametric GWR, CAR/SAR spatial priors, Bayesian hierarchical/joint/multivariate models, empirical Bayes/full Bayes methods, spatial spillover models, random forest, SVM, CNN/LSTM, KDE, and network KDE.
- Baseline model: Poisson and negative binomial models appear as common conventional baselines in the reviewed literature.
- Final/preferred model: Not stated. The review does not recommend one universal model. It emphasises that model choice depends on spatial unit, data, purpose, interpretability, and transferability.
- Loss function or likelihood, if stated: Mixed across reviewed methods; not extractable as one review-level likelihood.
- Offset/exposure term, if used: Mixed across reviewed studies.
- Spatial autocorrelation handling: Moran’s I, Local Moran’s I, Getis-Ord Gi*, CAR/SAR spatial priors, spatial weights, spatial lag/spillover, GWR/GWNBR, Bayesian spatial effects, and network KDE.
- Temporal dependence handling: Spatio-temporal Bayesian models, daily/weekly/hourly prediction models, temporal hotspot analysis, and temporal autocorrelation methods in some reviewed studies.
- Interpretability method: Coefficients, local parameter surfaces, spatial effects, hotspot maps, PSI, feature importance in ML, spatial residual dependence, and model comparisons.
- Evidence quote or page reference: Pages 13–20 review modelling approaches. Page 14 discusses GWR/GWNBR. Pages 15–18 discuss CAR/SAR, Bayesian, EB/FB, spillover and related methods. Pages 19–21 discuss machine learning, deep learning, KDE, network KDE, and VRU exposure.

## 9. Reported Metrics / Quantitative Results

This is a review paper. Extracted numbers are findings from cited studies, not original estimates produced by this review.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Review scope | Explicit spatial/spatio-temporal studies only | Qualitative inclusion rule | Literature review | Excludes non-spatial cross-sectional/case-control studies | Page 3 |
| Spatial-unit sensitivity | Smaller segment scales to larger segments | Crash counts move from Poisson-like to intermediate/normal distributions as segment length increases | Thomas 1996 reviewed result | Segment length changes crash-count distribution and modelling assumptions | Page 4 |
| Intersection mechanism | 3-leg vs 4-leg intersections | 3-legged intersections tend to have lower crash rates and different mechanisms | Abdel-Aty & Wang 2006 reviewed result | Junction typology matters | Page 5 |
| Segment/intersection dependence | Connected segments and intersections | Spatial correlations between intersections and connected segments more significant than intersections-only or segments-only | Zeng & Huang 2014 reviewed result | Link-only models can miss junction-link dependence | Page 5 |
| Spatial-unit aggregation | TAZ to TSAZ | About 1:2 aggregation found preferable in one study | Lee et al. 2014b reviewed result | Spatial zoning can affect model quality | Page 7 |
| Spatial transferability | Cross-country regional model transfer | Total/bicycle models transferable Italy to US; reverse mostly not; pedestrian models not transferable | Lee et al. 2019b reviewed result | Spatial model transferability is limited | Page 8 |
| Boundary buffer | Entropy-based variable buffer | 6 m and 9 m in Edmonton central/south areas | Cui et al. 2015 reviewed result | Boundary crash allocation can require local calibration | Page 10 |
| MAUP impact | MAUP effects | Significant impact on parameter estimates, model assessment, and hotspot identification | Zhai et al. 2019a reviewed result | Spatial zoning choices can change conclusions | Page 11 |
| Spatial proximity | Common-boundary length | Best fit in one TAZ spatial-weight comparison | Dong et al. 2014 reviewed result | Spatial weights matter | Page 11 |
| Space syntax | Global integration | Positively related to pedestrian-vehicle crashes in reviewed Hong Kong study | Guo et al. 2017 reviewed result | Network structure can matter for VRU crashes | Page 12 |
| Hotspot temporal variation | Time of day | Hotspots varied considerably by time of day | Soltani & Askari 2017 reviewed result | Static annual risk maps can hide temporal patterns | Page 13 |
| Random forest hotspot classification | Accuracy | About 80% | Jiang et al. 2016 reviewed result | ML can classify hot-zones, but validation detail is not sufficient in the review | Page 19 |
| Deep learning vs econometric | Temporal resolution | CNN better at daily level; econometric better at weekly level | Bao et al. 2019 reviewed result | No method dominates across temporal scales | Pages 19–20 |
| Network KDE | Network KDE vs regular KDE | Network KDE represented crash densities and road-network borders more precisely | Xie & Yan 2008 reviewed result | Road-network-aware density estimation can outperform planar KDE for crashes | Page 20 |
| VRU exposure | Walking hours | Best-performing pedestrian exposure variable in one integrated model | Lee et al. 2019a reviewed result | VRU exposure choice matters | Page 21 |
| Review conclusion | Lack of common framework | Qualitative | Spatial road-safety literature | Limits comparability and accumulated evidence | Page 23 |
| Review conclusion | Hotspot sensitivity | Qualitative | Spatial road-safety literature | Hotspots vary by user group, age, time of day, method, and included factors | Page 23 |

After the table:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? Mixed across reviewed studies and often not stated at the review level. The review does not provide a consistent validation protocol.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? Mixed. The review covers model fit, hotspot ranking, spatial autocorrelation/residual diagnostics, transferability, prediction performance, and methodological sensitivity.
- Are any metrics likely to be optimistic for real-world deployment? Yes, especially ML/hotspot accuracy values where validation detail is not reported in the review or where spatially related units may be split across train/test samples.
- Which metric, if any, is most relevant to Open Road Risk? MAUP/hotspot sensitivity, segment/intersection spatial dependence, and transferability findings are the most relevant. They warn that risk rankings can change with spatial units, spatial weights, and omitted neighbouring-unit structure.

Important:

- Do not treat any individual numeric finding as direct evidence for Open Road Risk unless the original cited study is checked.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Mixed across reviewed studies. The review covers Poisson, negative binomial, zero-inflated, hurdle, Poisson-lognormal, Bayesian spatial, EB/FB, KDE, and ML methods, but it does not make rare-event/zero-heavy modelling the central theme.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson, negative binomial, Poisson-lognormal, zero-inflated NB in some VRU studies, hurdle models in specific studies, EB/FB, Bayesian spatial models, and ML methods are mentioned.
- Whether high-risk locations are evaluated separately: Hotspot identification is a recurring theme, using EB/FB, KDE/network KDE, Moran’s I, Getis-Ord Gi*, ML hot-zone classification, and potential-safety-improvement approaches.
- Evidence quote or page reference: Page 17 mentions zero-inflated negative binomial models for pedestrian/bicycle crashes in a reviewed TAZ study. Pages 19–21 discuss ML and KDE/network KDE approaches for prediction and hotspot estimation.
- Practical relevance to my sparse collision link-year dataset: Medium. The review supports considering spatial structure and hotspot sensitivity, but it does not directly solve the extremely zero-heavy Open Road Risk link-year problem.

Important:

- Do not overclaim that the review recommends zero-inflated or hurdle models. It reports them as part of the literature.

## 11. Validation Strategy

- Train/test split method: Not applicable at review level.
- Spatial holdout used? Mixed / not stated across reviewed studies.
- Temporal holdout used? Mixed / not stated across reviewed studies.
- Grouped holdout used? Mixed / not stated across reviewed studies.
- Cross-validation type: Mixed / not stated.
- Metrics: Mixed across reviewed studies: AIC, DIC, MAD, Moran’s I, Getis-Ord Gi*, accuracy, residual spatial dependence, hotspot overlap, model comparison statistics, etc.
- External validation: Discussed conceptually through transferability studies, but not a review-level validation.
- Leakage or generalisation risks: Spatial transferability is often limited. Spatially proximate observations can produce optimistic validation if not properly held out. MAUP and boundary effects can change parameter estimates, model assessment, and hotspot identification.
- Evidence quote or page reference: Page 8 discusses cross-country transferability limitations. Page 11 discusses MAUP impacts. Page 23 notes limited transferability and lack of common analysis frameworks.
- What I should copy or avoid:
  - Copy the habit of explicitly discussing spatial unit, boundary effects, spatial proximity, and transferability.
  - Avoid treating a random link-level split as strong evidence of spatial generalisation.
  - Avoid assuming that a risk ranking is stable across segmentation choices.

## 12. Key Findings Relevant to My Project

1. Finding: Spatial-unit choice affects model interpretation, parameter estimates, and hotspot identification.
   - Why it matters: Open Road Risk’s use of OS Open Roads links is defensible but should be documented as a modelling choice, not a neutral fact.
   - Evidence quote or page reference: Page 3 states that spatial-unit choice directly influences scope, interpretability, and data preparation; page 11 reports MAUP impacts on parameter estimates, model assessment, and hotspot identification.
   - Confidence: high.

2. Finding: Segment-only models can miss spatial relationships with intersections and corridors.
   - Why it matters: Open Road Risk’s link-year model should document that junction risk and adjacent-link effects may not be fully captured.
   - Evidence quote or page reference: Page 5 states that spatial correlations between intersections and connected segments were more significant than those between intersections only or segments only in a reviewed joint model.
   - Confidence: high as literature-review evidence; medium for direct implementation.

3. Finding: Spatial weights/proximity structures materially affect model fit and interpretation.
   - Why it matters: If Open Road Risk adds spatial smoothing, EB shrinkage, or neighbourhood features, adjacency definition should be tested rather than assumed.
   - Evidence quote or page reference: Pages 11–12 review proximity structures including adjacency, common-boundary length, centroid distance, crash-weighted centroid distance, route-informed adjacency, and hierarchical spatial relationships.
   - Confidence: high.

4. Finding: Spatial transferability is limited even when variables look similar.
   - Why it matters: Published coefficients or thresholds should not be imported into Open Road Risk without local validation.
   - Evidence quote or page reference: Page 8 reports limited cross-country model transferability, including no transferable pedestrian model in the reviewed Italy/US comparison.
   - Confidence: high.

5. Finding: Hotspots vary by user group, time of day, method, and included factors.
   - Why it matters: Open Road Risk risk-percentile maps should be framed as model-specific prioritisation aids, not stable truths.
   - Evidence quote or page reference: Page 13 discusses time-of-day hotspot variation; page 23 states that hotspots differ by user group, age, time of day, methods, and factors.
   - Confidence: high.

6. Finding: Network-specific approaches such as network KDE and space-syntax/centrality can be more appropriate than planar or simple proximity methods for road crashes.
   - Why it matters: Open Road Risk’s network-based link modelling and centrality features are aligned with this literature, but implementation choices matter.
   - Evidence quote or page reference: Page 12 discusses space syntax/global integration and pedestrian-vehicle crashes; page 20 notes network KDE representing crash densities and borders more precisely than regular KDE.
   - Confidence: medium-high.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Documentation of OS Open Roads link unit and MAUP/segmentation limits | Clarifies that link-based rankings depend on spatial-unit choice | Current model docs and network metadata | Review-level | High | documentation | Low | Could sound defensive if not framed constructively |
| Sensitivity check by alternative segmentation / aggregation | Tests whether top risk rankings survive aggregation choices | OS links, route/corridor grouping, fixed-length segments or aggregation rules | Review-level | Medium | validation / diagnostic | Medium to high | Expensive and may create complex interpretation |
| Spatial residual autocorrelation diagnostic | Checks whether model residuals cluster spatially | Fitted residuals, link centroids/network adjacency | Review-level | High as diagnostic | Stage 2 / validation | Medium | Spatial weights are not obvious at 2.1M links |
| Adjacency/proximity structure comparison | Tests different neighbour definitions before smoothing/spatial priors | Network topology, distance, corridor/route data | Review-level | Medium | Stage 2 / validation / future model | Medium | Arbitrary weights can create false precision |
| Junction/adjacent-link limitation note | Captures known segment/intersection dependence | Existing docs, topology diagnostics | Review-level | High | documentation / future feature | Low | Could overstate weakness of current link model |
| Network KDE or hotspot-comparison diagnostic | Compare model risk hotspots with network-density hotspots | Crash points, network geometry | Review-level | Medium | validation / documentation | Medium | KDE is descriptive and exposure-blind unless adjusted |
| Spatio-temporal exploratory maps | Test whether risk patterns differ by time of day or period | Collision time fields, exposure/time profile outputs | Review-level | Medium | Stage 1b / Stage 2 diagnostic | Medium | Sparse counts by time band |
| Transferability warning in literature evidence register | Prevents overuse of coefficients from external papers | Literature register | Review-level | High | documentation | Low | None |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full CAR/SAR Bayesian spatial model at 2.1M links | Computationally heavy and requires carefully defined neighbourhoods | Scalable spatial priors/weights and compute | Mostly smaller reviewed studies | Low currently | Pilot on subset or aggregated areas | High |
| Direct GWR/GWNBR production model | Local coefficients are hard to interpret and transfer; compute heavy | Scalable local modelling and robust validation | Reviewed studies | Low to medium | Use as local diagnostic on sample areas | Medium-high |
| Importing coefficients/thresholds from reviewed studies | Review emphasises limited transferability | Local validation | Mixed studies | Low | Treat as candidate diagnostics only | High |
| Zonal TAZ/TSAZ modelling as replacement for links | UK/Open Road Risk network purpose is link-level; zones lose micro-level detail | Suitable safety zones | Zonal studies | Low as replacement | Use zones as context layer or aggregation check | High |
| ML hotspot classification accuracy as evidence of production performance | Review does not provide enough validation detail; spatial leakage risk | Proper spatial/temporal validation | Individual cited studies | Low | Use only after local grouped/spatial validation | High |

Important:

- Most useful repo actions are documentation and diagnostics, not immediate production model changes.
- This review argues for caution and sensitivity testing more than it argues for a single best spatial model.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Indirectly. It confirms that AADT, VMT, and road length are common exposure variables, but does not validate a specific offset.
- Does it suggest better handling of AADT/AADF uncertainty? No direct method. It does suggest exposure and spatial-unit sensitivity should be considered together.
- Does it suggest useful geometry or road-context features? Yes. Road class, segment length, speed, lanes, intersections, access/median density, curvature, grade, population/socioeconomic context, land use, network density, and centrality appear across reviewed spatial studies.
- Does it suggest better modelling of junctions? Yes conceptually. The review highlights segment-intersection dependence and joint models as important, but not directly scalable to Open Road Risk without a junction layer.
- Does it suggest better treatment of severity? It identifies multivariate and joint frequency/severity spatial models as part of the literature, but does not prescribe one method.
- Does it suggest better validation design? Indirectly. It warns that spatial transferability, MAUP, proximity definitions, and hotspot sensitivity matter. This supports spatial/grouped validation and sensitivity checks.
- Does it expose a weakness in my current approach? Yes: a link-based model and risk percentile map can be sensitive to segmentation, neighbouring-unit definitions, boundary assignment, and junction treatment. These should be documented and tested where feasible.

## 15. Repo Actionability

1. Suggested repo action: Add a methodology note explaining why OS Open Roads links are used, and list the consequences of this spatial-unit choice.
   - Action type: documentation note
   - Relevant stage: documentation / methodology
   - Why the paper supports it: The review states spatial-unit choice affects scope, interpretation, data preparation, parameters, model assessment, and hotspots.
   - Evidence quote or page reference: Pages 3 and 11.
   - Effort: low
   - Risk if implemented badly: Could read like an apology rather than a transparent scope statement.

2. Suggested repo action: Add a spatial residual autocorrelation diagnostic for the Stage 2 GLM/XGBoost residuals or risk scores.
   - Action type: diagnostic
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: Spatial dependence and autocorrelation are central themes; Moran’s I, Local Moran’s I and similar tools recur in the review.
   - Evidence quote or page reference: Pages 2–3 and 13–18.
   - Effort: medium
   - Risk if implemented badly: Spatial weights are hard at 2.1M links; start with sampled or aggregated diagnostics.

3. Suggested repo action: Add an aggregation sensitivity check for top-risk links, e.g. compare link-level hotspots with corridor/route or fixed-distance aggregation.
   - Action type: diagnostic / baseline comparison
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: MAUP and boundary effects can change hotspot identification.
   - Evidence quote or page reference: Pages 10–11.
   - Effort: medium to high
   - Risk if implemented badly: Alternative aggregation choices may be arbitrary; present as sensitivity, not truth.

4. Suggested repo action: Add a junction-scope limitation note and future junction-feature pilot.
   - Action type: documentation note / small pilot
   - Relevant stage: documentation / future feature engineering
   - Why the paper supports it: Reviewed studies show intersection-segment spatial correlations and different safety mechanisms between 3-leg and 4-leg intersections.
   - Evidence quote or page reference: Pages 4–5.
   - Effort: low for note; high for pilot
   - Risk if implemented badly: Naive junction features may add noise.

5. Suggested repo action: Add a literature-register tag for spatial review / MAUP / spatial autocorrelation / hotspot sensitivity.
   - Action type: documentation/indexing
   - Relevant stage: documentation
   - Why the paper supports it: This is a review-level source useful for methodological caveats rather than a direct model recipe.
   - Evidence quote or page reference: Full review, especially pages 1–3 and 23.
   - Effort: low
   - Risk if implemented badly: None.

6. Suggested repo action: Do not implement CAR/SAR/GWR production modelling from this paper alone.
   - Action type: avoid production change
   - Relevant stage: Stage 2 / future model
   - Why the paper supports it: The review emphasises method variety, transferability limits, and sensitivity to proximity structures rather than a universal best spatial model.
   - Evidence quote or page reference: Pages 11–20 and 23.
   - Effort: none
   - Risk if ignored: Significant compute and interpretation burden with unclear production benefit.

## 16. Query Tags

- spatial-road-safety
- literature-review
- spatial-dependence
- spatial-heterogeneity
- spatial-autocorrelation
- Moran-I
- Getis-Ord-Gi
- CAR
- SAR
- Bayesian-spatial
- Poisson-lognormal
- GWR
- GWNBR
- MAUP
- boundary-problem
- spatial-weights
- proximity-structure
- network-KDE
- hotspot-identification
- road-segments
- intersections
- corridor-models
- zonal-models
- TAZ
- VMT
- AADT
- vulnerable-road-users
- pedestrian-crashes
- transferability
- segmentation-sensitivity

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: Publication year and DOI/URL are not visible in the uploaded PDF; many reviewed studies’ exact validation designs are not described in detail; individual study metrics should be checked from original papers if used as primary evidence.
- Parts of the paper that need manual checking: Full review tables if extracting a study-by-study evidence register; individual cited papers for exact modelling specifications and validation methods.
- Any likely ambiguity or risk of misinterpretation: This is a review paper. Its value for Open Road Risk is methodological framing and caveat-setting, not direct evidence for one production model. Do not cite the review as proving that any specific spatial model, coefficient, feature threshold, or hotspot method will transfer to the UK link-level Open Road Risk pipeline.
