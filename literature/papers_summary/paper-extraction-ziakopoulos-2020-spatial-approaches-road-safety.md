# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: A review of spatial approaches in road safety.pdf
- Suggested Markdown filename: paper-extraction-ziakopoulos-2020-spatial-approaches-road-safety.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The PDF text was accessible, though the file-search preview truncated later sections. Targeted search was used for the later discussion and modelling sections. Tables were referenced from parsed text where visible, but exact tabular rows should be manually checked if used for formal evidence tables.

## 1. Citation

- Title: A review of spatial approaches in road safety
- Authors: Apostolos Ziakopoulos; George Yannis
- Year: Not stated in visible metadata
- DOI or URL, if present: Not stated
- Country / region studied: Multiple countries / literature review
- Study setting: mixed

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper critically reviews how road-safety researchers use spatial and spatio-temporal approaches to analyse crash occurrence, hotspot identification, spatial dependence, spatial heterogeneity, areal-unit choice, boundary problems, proximity structures, vulnerable road users, and modelling methods.
- Main purpose: literature review / methodological review / spatial road safety analysis
- Evidence quote or page reference: Page 1 states that the aim is to “critically review the existing literature on different spatial approaches” and investigate areal units, modelling approaches, boundary problems, MAUP, spatial proximity structures, vulnerable road users, and modelling approaches.

## 3. Response Variable

- Target variable: Not a single empirical target; reviewed studies examine crash counts, crash rates, injury severity rates, hotspot status, crash costs, and related road safety indicators.
- Collision type: Mixed; the review explicitly includes total crashes, motorcycle crashes, single-vehicle crashes, vehicle-vehicle crashes, bicycle-vehicle crashes, pedestrian-vehicle crashes, and other specified crash categories.
- Severity handling: Reviewed studies include severity rates, severity-specific models, multivariate severity models, and vulnerable road-user analyses, but the review itself does not fit a severity model.
- Count, binary, rate, risk score, severity class, or other: Mixed across reviewed studies.
- Time window used for outcomes: Mixed across reviewed studies.
- Evidence quote or page reference: Page 3 defines road safety indicators as crash counts or rates, injury severity rates, etc. Page 4 lists crash category abbreviations used in the review tables.

## 4. Exposure Handling

- Exposure variable used, if any: Mixed across reviewed studies; examples include traffic volume, AADT, VMT, population, vehicle/pedestrian/bicycle trips, walking hours, and road network/trip generation densities.
- Traffic count source: Mixed / study-specific; not a single source.
- Whether exposure is modelled, observed, assumed, or ignored: Mixed. Some reviewed studies include exposure variables in crash models, some estimate exposure first, and some hotspot/spatial-statistic methods do not model exposure explicitly.
- Treatment of missing or sparse traffic counts: Not a central review focus; specific studies vary.
- Whether offset terms, rates, denominators, or normalisation are used: Mixed. The review discusses crash counts/rates, VMT, population exposure, estimated VRU exposure, and spatial models, but does not prescribe one exposure-offset structure.
- Evidence quote or page reference: Page 9 notes zonal factors such as VMT shared by segments/intersections inside zones. Page 16 mentions daily VMT in spatio-temporal hierarchical Bayesian models. Page 21 notes pedestrian exposure modelling and walking hours as a performing exposure variable.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The paper supports the importance of exposure-aware spatial modelling, but it is a review and does not validate a specific AADT offset. Its most relevant transfer is conceptual: exposure, spatial scale, and spatial dependence need to be handled together.

Important:

- Mathematical exposure structure: Mixed transferability. The review covers many exposure approaches but does not establish a single exposure-offset method.
- Specific data-source transferability: Medium where studies use AADT/VMT-like traffic measures; low where they require detailed VRU trips, travel surveys, signal data, or high-resolution proprietary sources.
- Do not use this review alone as proof that Open Road Risk’s exact `log(AADT × length × 365 / 1e6)` offset is optimal.

## 5. Spatial Unit of Analysis

- Unit: Mixed; reviewed units include road segments, intersections, corridors, grids, TAZs, TSAZs, census blocks/block groups/tracts, ZIP codes, census wards, traffic analysis districts, regions/counties/cities/states, and conditional/link-based units.
- Segment length or segmentation rule: Mixed; the review notes fixed grids, road segments, corridor/sub-corridor splits, link-based crash mapping, and multi-level integration.
- How crashes are assigned to the network: Mixed; reviewed approaches include crash mapping to road segments/links, aggregation to zones/regions, boundary assignment methods, kernel density estimation, and network KDE.
- Treatment of junctions/intersections: Intersections are reviewed both individually and jointly with road segments/corridors. Intersection geometry, traffic by turning movement, signal phase coordination, and number of legs are noted as relevant in spatial analyses.
- Spatial aggregation risks: Boundary problem, modifiable areal unit problem, proximity-structure sensitivity, transferability limits, and hotspot sensitivity.
- Evidence quote or page reference: Pages 3–4 state that spatial-unit choice directly affects scope, interpretability, and data preparation. Pages 10–12 discuss boundary problem, MAUP, and proximity structures. Page 8 notes that link-based approaches can be problematic for interpretable results.
- Relevance to OS Open Roads link-based pipeline: High. The review directly highlights risks from using one spatial unit such as road links: MAUP-like scale effects, boundary/assignment issues, spatial dependence between nearby links/intersections, and transferability problems.

## 6. Temporal Unit of Analysis

- Years covered: Mixed across reviewed studies.
- Temporal resolution: Mixed; reviewed studies include yearly, daily, weekly, hourly, and spatio-temporal analyses.
- Whether seasonality or time-of-day is modelled: Some reviewed studies model time-of-day, daily/weekly/hourly risk, temporal hotspots, weather/time interactions, and spatio-temporal effects.
- Whether before-after or panel structure is used: Mixed; EB before-after and spatio-temporal hierarchical models are discussed.
- Evidence quote or page reference: Page 13 notes hotspots varying across times of day. Page 16 discusses high-temporal-resolution daily intervals and spatial/temporal/spatio-temporal Bayesian structures. Page 19 describes CNN/LSTM weekly, daily, and hourly prediction models.
- Relevance to WebTRIS-style time profiles: Medium. The review supports the general importance of spatio-temporal crash risk and time-of-day variation, but does not specifically validate WebTRIS-derived traffic fractions.

## 7. Engineered Features

List the most important engineered features, especially those I could recreate.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Road segment/intersection/corridor unit | Road network GIS | Define spatial units for aggregation/modelling | Unit choice affects interpretability and model results | Already present / compare OS Open Roads link choice |
| Spatial adjacency / proximity weights | Network or zonal geometry | 0–1 adjacency, common-boundary length, centroid distance, crash-weighted centroid distance, route-informed adjacency | Defines spatial correlation and spillover structure | Medium to high for diagnostics |
| Road class / road type | Road network inventory | Segment/corridor classification | Different mechanisms by highway, urban/rural, divided/undivided roads | Already present / compare implementation |
| AADT / traffic volume / VMT | Traffic counts/modelled demand | Include as covariate/exposure or zonal factor | Central exposure and heterogeneity factor | Already present partly; compare AADT uncertainty |
| Segment length | Road geometry | Length of segment/unit | Affects crash counts and interacts with spatial-unit scale | Already present |
| Intersection density / unsignalized intersections / crosswalk density | Road/infrastructure data | Count or density per zone/segment | Associated with crash occurrence in reviewed urban studies | Candidate feature / junction diagnostics |
| Number of lanes / accesses / median opening density | Road inventory | Counts or densities | Captures road complexity and conflict opportunities | Candidate feature where coverage allows |
| Speed / mean speed / speed limit | OSM, traffic data, road inventory | Segment or zonal speed measures | Important risk/context variable in reviewed models | Already candidate/present partly; compare implementation |
| Curvature | Road geometry | Segment or area-wide curvature measures | Reviewed as road-level factor influencing safety | Already candidate/present / compare implementation |
| Population / socioeconomic variables | Census/geodemographic data | Area-level demographics, income, employment, school enrolment | Important in zonal/VRU studies and macro-level risk | Population density already present; IMD candidate/present |
| Land use / network density / trip generation density | GIS / planning data | Zonal density or accessibility indicators | Used in macro spatial models and VRU models | Medium as future context features |
| Weather variables | Weather stations / gridded weather | Spatial/temporal assignment to crashes or units | Relevant but data-source fitness varies by condition | Low to medium; weather not current core feature |
| VRU exposure | Travel surveys, trip estimates, walking hours | Model exposure then use in crash models | Important for pedestrian/cycle risk | Low currently unless data added |
| Hotspot indicators / PSI | Model predictions and observed crashes | Potential safety improvement or hotspot ranking | Used for prioritisation | Medium; conceptually similar to risk ranking |

Only features/feature families actually discussed in the review are included.

## 8. Model Architecture

- Algorithms/models used: Literature review of multiple model families, including GLMs, Poisson and negative binomial variants, GWR, geographically weighted negative binomial regression, semi-parametric GWR, CAR/SAR spatial models, Bayesian hierarchical/joint/multivariate models, empirical Bayes/full Bayes, spatial spillover models, Poisson-lognormal models, random forest, SVM, CNN/LSTM deep learning, KDE and network KDE.
- Baseline model: GLM / Poisson / negative binomial models are repeatedly treated as common baselines or conventional methods in the reviewed literature.
- Final/preferred model: Not stated; the review does not prescribe one universal best model.
- Loss function or likelihood, if stated: Mixed across reviewed methods; not extracted as a single likelihood.
- Offset/exposure term, if used: Mixed across reviewed studies.
- Spatial autocorrelation handling: Moran’s I, Local Moran’s I, Getis-Ord Gi*, CAR/SAR priors/effects, spatial weights, spatial lag/spillover, GWR/GWNBR, Bayesian spatial effects, network KDE.
- Temporal dependence handling: Spatio-temporal Bayesian models, daily/weekly/hourly CNN/LSTM models, temporal hotspot analysis, temporal autocorrelation in crash count models.
- Interpretability method: Coefficients, local parameter surfaces, spatial effects, hotspot maps, PSI, feature importance in ML, spatial residual dependence, and model comparisons.
- Evidence quote or page reference: Pages 13–20 review modelling approaches. Page 14 discusses GWR/GWNBR. Pages 15–18 discuss CAR/SAR, Bayesian, EB/FB, spillover, and alternative priors. Pages 19–21 discuss ML/deep learning and KDE/network KDE.

## 9. Reported Metrics / Quantitative Results

Extract the main quantitative results reported in the paper.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Review scope | Explicit spatial/spatio-temporal studies only | Qualitative inclusion criterion | Literature review | Excludes non-spatial cross-sectional/case-control studies | Page 3 |
| Spatial-unit issue | TAZ aggregation to TSAZ | About 1:2 aggregation reported as preferable in one reviewed study | Macroscopic safety modelling | Example of spatial-unit sensitivity | Page 7 |
| Spatial transferability | Cross-country regional model transfer | Total and bicycle crash models transferable Italy to US; reverse not true for most areas; pedestrian models not transferable | Lee et al. 2019b reviewed result | Demonstrates limited transferability even with common variables | Page 8 |
| Boundary buffer example | Entropy-based variable buffer | 6 m and 9 m in Edmonton central/south areas | Boundary crash allocation | Example of boundary-method sensitivity | Page 10 |
| MAUP finding | MAUP impact | Significant on parameter estimates, model assessment, and hotspot identification | Zhai et al. 2019a reviewed result | Spatial zoning choices affect conclusions | Page 11 |
| Proximity structure | Spatial weights comparison | Common-boundary length best in one TAZ study | Dong et al. 2014 reviewed result | Spatial-weight choice affects model fit | Page 11 |
| GWR/GWNBR | GWNBR reduced spatial dependence of residuals | Qualitative result | GWNBR studies | Spatially varying local models can address overdispersion and residual dependence | Page 14 |
| ML performance | Random forest hotspot classification | About 80% accuracy in one reviewed TAZ hot-zone study | Jiang et al. 2016 reviewed result | ML can rank/classify hotspots, but interpretation limits remain | Page 19 |
| Deep learning | Prediction resolution effect | Performance decreases as spatio-temporal outcome resolution approaches hourly | Bao et al. 2019 reviewed result | Higher-resolution prediction is harder | Page 19 |
| KDE | Network KDE vs regular KDE | Network KDE described crash densities and borders more precisely | Xie and Yan 2008 reviewed result | Network-specific density estimation better matches road crashes than planar KDE | Page 20 |
| VRU exposure | Walking hours | Best-performing pedestrian exposure variable in one integrated model | Lee et al. 2019a reviewed result | Exposure choice matters for pedestrian fatality estimation | Page 21 |
| Review conclusion | Lack of common framework | Qualitative | Spatial road safety literature | Limits comparability of spatial analyses | Page 23 |
| Review conclusion | Hotspot sensitivity | Qualitative | Spatial road safety literature | Hotspots vary by user group, age, time of day, methods, and included factors | Page 23 |

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? Mixed across reviewed studies and often not stated in the review. The review itself does not provide a single validation protocol.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? Mixed. The review covers model fit, hotspot ranking, spatial autocorrelation/residual diagnostics, transferability, and prediction performance.
- Are any metrics likely to be optimistic for real-world deployment? Yes, especially ML/hotspot accuracy metrics when based on spatially related data without clear spatial/temporal external validation.
- Which metric, if any, is most relevant to Open Road Risk? MAUP/hotspot sensitivity and spatial transferability findings are most relevant methodologically; they warn that risk rankings and maps are sensitive to unit choice, spatial weights, and omitted factors.

Important:

- This is a review, so extracted numbers are mostly findings from cited studies, not original estimates from the paper.
- Do not treat any single cited metric as direct evidence for Open Road Risk without checking the original study.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Mixed across reviewed studies. The review covers count models, Bayesian models, spatial priors, EB/FB, zero-inflated models in some VRU/spillover contexts, and ML methods.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson, negative binomial, Poisson-lognormal, CAR/SAR, zero-inflated negative binomial in reviewed VRU/spillover studies, EB/FB, ML methods.
- Whether high-risk locations are evaluated separately: Hotspots, hot zones, PSI, KDE/network KDE, and hotspot ranking are repeatedly discussed.
- Evidence quote or page reference: Page 13 describes GLMs for countable crash events. Page 17 discusses EB/FB and hotspot identification. Page 17 mentions zero-inflated negative binomial models in pedestrian/bicycle crash spillover analysis.
- Practical relevance to my sparse collision link-year dataset: High conceptually. The review supports the need for spatial diagnostics, hotspot sensitivity checks, and careful validation. However, it does not solve the rare-event link-year modelling problem directly.

Important:

- Use the `zero-inflated` label only for reviewed studies that explicitly used zero-inflated models, not for the review as a whole.
- The review does not say zero-inflated models should be the default for Open Road Risk.

## 11. Validation Strategy

- Train/test split method: Mixed / not stated as a single protocol.
- Spatial holdout used? Mixed across reviewed studies; the review discusses spatial transferability but does not establish a standard holdout design.
- Temporal holdout used? Mixed across reviewed studies.
- Grouped holdout used? Not stated as a central design.
- Cross-validation type: Mixed / not stated.
- Metrics: AIC, DIC, MAD, predictive accuracy, hotspot classification accuracy, spatial autocorrelation metrics, Moran’s I, Getis-Ord Gi*, model fit, PSI, and other study-specific metrics.
- External validation: Discussed mainly through transferability across regions/countries and model applicability, but not consistently.
- Leakage or generalisation risks: Spatial autocorrelation can make random splits optimistic; spatial unit choice, MAUP, boundary allocation, and proximity structures can change conclusions and hotspot maps.
- Evidence quote or page reference: Page 8 discusses limited transferability across US/Italy regional models. Page 11 notes MAUP significantly affects parameters, assessment, and hotspot identification. Page 23 states transferability is limited and there is no common established methodology to compare spatial analyses.
- What I should copy or avoid: Copy the explicit sensitivity testing of spatial units/proximity structures. Avoid relying on a single risk map without unit-scale and spatial-dependence diagnostics.

Important:

- This paper gives strong support for validation/sensitivity design, not a single model choice.
- Spatially random validation is likely insufficient for Open Road Risk if spatial dependence is strong.

## 12. Key Findings Relevant to My Project

Give 3–6 findings that are directly useful for my road-risk pipeline.

### Finding 1

- Finding: Spatial dependence and spatial heterogeneity are core issues in crash analysis.
- Why it matters: Your link-year model should not assume neighbouring links are independent in interpretation, even if grouped train/test splits reduce repeated-link leakage.
- Evidence quote or page reference: Page 2 defines spatial dependence and spatial heterogeneity and explains why spatial analyses are informative in crash analysis.
- Confidence: high

### Finding 2

- Finding: Spatial unit choice materially affects interpretability, parameter estimates, model assessment, and hotspot identification.
- Why it matters: OS Open Roads links are a convenient unit, but risk rankings may change under fixed-length segments, junction clusters, corridors, or zones.
- Evidence quote or page reference: Page 3 says spatial-unit choice affects scope, interpretability, and data preparation; page 11 reports MAUP effects on parameters, assessment, and hotspots.
- Confidence: high

### Finding 3

- Finding: Segments, intersections, and corridors can be jointly modelled, and spatial correlations between intersections and connected segments may be stronger than segment-segment or intersection-intersection correlations.
- Why it matters: This supports a diagnostic or future pilot that treats junction-adjacent links differently from ordinary links.
- Evidence quote or page reference: Page 5 describes Bayesian spatial joint models for road segments and intersections and notes stronger correlations between intersections and connected segments.
- Confidence: high

### Finding 4

- Finding: Spatial weights/proximity structures are not neutral modelling choices.
- Why it matters: For Open Road Risk, adjacency, route distance, common boundaries, network distance, and road hierarchy could produce different residual/risk patterns.
- Evidence quote or page reference: Pages 11–12 discuss multiple proximity structures and note that common-boundary weighting or adjacency-based models can perform best in different studies.
- Confidence: high

### Finding 5

- Finding: Bayesian spatial models and GWR/GWNBR are powerful but can be complex, local, and hard to transfer.
- Why it matters: They are useful as comparison or pilot methods, but not obvious production replacements at 2.1M-link scale.
- Evidence quote or page reference: Pages 14–16 discuss GWNBR/S-GWR transferability limits and Bayesian model strengths/limitations.
- Confidence: high

### Finding 6

- Finding: Hotspot maps are sensitive to vehicle/user type, age, time of day, methods, and included/omitted variables.
- Why it matters: Your production risk percentile should be documented as one risk view, not a definitive “true hotspot” map.
- Evidence quote or page reference: Page 23 states hotspots vary by road user, age, time of day, methodology, and included elements.
- Confidence: high

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Spatial residual autocorrelation diagnostics | Check whether Stage 2 residuals/risk errors cluster spatially | Link residuals, road geometry, adjacency/network distance | Review covers many scales | High for sampled/full network diagnostics | validation | medium | Large-scale computation and defining neighbours |
| MAUP / segmentation sensitivity pilot | Test whether risk ranking changes under OS links vs fixed-length/corridor aggregation | Link risk outputs, geometry, aggregation rules | Review shows MAUP effects | Medium to high | validation / documentation | medium | Could become a large scope expansion |
| Junction-near vs non-junction diagnostics | Tests segment/intersection interaction issue | Junction flags, node degree, distance to intersections | Review supports segment-intersection joint concerns | High | Stage 2 / validation | medium | Junction definitions may be noisy |
| Spatial-weight sensitivity | Compare adjacency, network distance, road-class/corridor proximity | Network topology, residuals/risk scores | Review covers proximity structures | Medium | validation | medium/high | Different weights may imply different stories |
| GWNBR / S-GWR small-area pilot | Explore spatially varying coefficients for AADT/length/road class | Local subset, collision counts, exposure, features | Review supports usefulness but low transfer | Low full-scale; medium pilot | baseline comparison / small pilot | high | Local models may not transfer and may be computationally heavy |
| Network KDE / hotspot diagnostic | Compare model risk hotspots with event-density hotspots | Snapped collision points, network | Review supports network KDE over planar KDE | Medium for exploratory maps | validation / documentation | medium | Density hotspots are not exposure-adjusted risk |
| VRU-specific spatial diagnostic | Separate pedestrian/cyclist patterns where data support it | STATS19 casualty/user type, exposure proxies | Review highlights VRU spatial studies | Medium | future feature / validation | medium | Exposure for VRUs may be weak |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full Bayesian spatial joint model over 21.7M link-years | Computationally heavy and model complexity high | Scalable inference, adjacency matrices, spatial priors | Reviewed studies mostly smaller | Low production compatibility | Pilot on selected region or aggregated units | high |
| High-resolution CNN grid approach | Requires custom high-resolution gridded features and opaque model | 100x100 grid cells / 17-layer matrices in reviewed example | Low with current link pipeline | Low | Use ML baseline on link features instead | high |
| Direct transfer of hotspot thresholds from reviewed studies | Hotspot definitions vary by unit, user type, method, and context | Common framework absent | Mixed | Low | Define project-specific benchmark and sensitivity tests | high |
| VRU exposure models using walking hours/trips | Open Road Risk currently lacks robust pedestrian/cycle exposure | Travel survey / mobility data | Regional/MSA studies | Low currently | Add as future separate module if data found | high |
| Treating zonal VMT/spatial models as direct replacement for link exposure model | Different unit and target | Zonal demand/VMT and aggregation | Zonal studies | Low | Use zonal factors as contextual covariates/diagnostics | medium |

Important:

- The review is highly transferable for validation design and cautionary framing.
- It is less transferable as direct production-model architecture.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Yes in broad principle, because spatial safety studies repeatedly use exposure and crash counts/rates. It does not specifically validate your offset formula.
- Does it suggest better handling of AADT/AADF uncertainty? Indirectly. It highlights exposure sensitivity, spatial unit issues, and AADT sensitivity in spatial models, but not a concrete AADF uncertainty method.
- Does it suggest useful geometry or road-context features? Yes. It supports road type, length, speed, curvature, intersections, density of unsignalized intersections/crosswalks, lanes/accesses, road network density, land use, population/demographics, and macro context.
- Does it suggest better modelling of junctions? Yes. It strongly supports separate or joint treatment of segments/intersections/corridors and attention to connected segment-intersection spatial correlations.
- Does it suggest better treatment of severity? Yes, in the sense that multivariate and severity-specific spatial models are reviewed. It supports severity diagnostics, not necessarily a combined severity-frequency production score.
- Does it suggest better validation design? Yes. It supports spatial autocorrelation diagnostics, spatial-unit sensitivity, boundary/MAUP analysis, proximity-structure sensitivity, and transferability checks.
- Does it expose a weakness in my current approach? Yes: a single OS Open Roads link-level risk percentile may be sensitive to spatial unit choice, junction handling, spatial dependence, and omitted macro/zonal context. That is a real limitation to document and test.

## 15. Repo Actionability

Give up to 5 concrete implications for my repo.

### Action 1

- Suggested repo action: Add a spatial validation section to the methodology docs covering spatial dependence, MAUP, boundary effects, and proximity-structure sensitivity.
- Action type: documentation note
- Relevant stage: documentation / validation
- Why the paper supports it: The review identifies these as central issues in spatial road-safety analysis.
- Evidence quote or page reference: Pages 1, 10–12, and 23 discuss boundary problem, MAUP, proximity structures, and lack of common framework.
- Effort: low
- Risk if implemented badly: Could read as hand-waving unless linked to actual diagnostics.

### Action 2

- Suggested repo action: Add a diagnostic notebook testing residual/risk clustering by network adjacency or network distance.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Spatial dependence is core to crash data; spatial autocorrelation metrics and spatial effects are repeatedly used in the reviewed literature.
- Evidence quote or page reference: Page 2 defines spatial dependence; page 13 mentions Moran’s I, Local Moran’s I, and Getis-Ord Gi*.
- Effort: medium
- Risk if implemented badly: Spatial residual clustering may reflect omitted exposure/context rather than pure model failure.

### Action 3

- Suggested repo action: Pilot a MAUP/segmentation sensitivity analysis comparing OS Open Roads link-level ranking with aggregated corridors or fixed-length segments.
- Action type: small pilot / validation
- Relevant stage: validation / feature engineering
- Why the paper supports it: The review reports that MAUP can affect parameter estimates, model assessment, and hotspot identification.
- Evidence quote or page reference: Page 11 discusses MAUP and reports significant effects in reviewed work.
- Effort: medium to high
- Risk if implemented badly: Aggregation may obscure true local issues or create artificial stability.

### Action 4

- Suggested repo action: Add a junction-adjacent diagnostic or facility-family split to compare model behaviour around intersections and connected segments.
- Action type: diagnostic / baseline comparison
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Reviewed joint models find segment-intersection correlations and show different mechanisms across segments, intersections, and corridors.
- Evidence quote or page reference: Page 5 discusses Bayesian spatial joint models and stronger correlations between intersections and connected segments.
- Effort: medium
- Risk if implemented badly: Junction definitions from OS topology may not represent real conflict geometry.

### Action 5

- Suggested repo action: Treat network KDE or spatial hotspot maps as a comparison layer, not as the production risk metric.
- Action type: diagnostic / documentation note
- Relevant stage: validation / web map
- Why the paper supports it: The review explains KDE/network KDE is useful for hotspot detection but also sensitive to bandwidth and not a direct analytical exposure-adjusted method.
- Evidence quote or page reference: Pages 20–21 discuss KDE/network KDE, kernel radius/bandwidth sensitivity, and lixels.
- Effort: medium
- Risk if implemented badly: Users may confuse collision-density hotspots with exposure-adjusted high-risk links.

Important:

- No production model rewrite is recommended directly from this review.
- The strongest repo value is validation discipline and limitation documentation.

## 16. Query Tags

- spatial-analysis
- road-safety-review
- spatial-dependence
- spatial-heterogeneity
- MAUP
- boundary-problem
- proximity-structures
- spatial-autocorrelation
- Moran-I
- Getis-Ord-Gi
- CAR
- SAR
- Bayesian-spatial
- GWR
- GWNBR
- spatial-spillover
- network-KDE
- hotspot-sensitivity
- segment-intersection-joint-model
- spatial-validation
- transferability
- VRU
- exposure
- AADT
- VMT
- spatial-unit
- corridor-level
- macro-micro-integration

Important:

- `zero-inflated` is not used as a general tag because this is not a zero-inflated modelling paper, though the review mentions zero-inflated models in some cited studies.

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: Publication year and DOI were not visible in the provided PDF metadata. The paper is a review, so many claims depend on cited studies that should be checked directly before using exact numerical values.
- Parts of the paper that need manual checking: Tables 1–4 and any specific study-level claims you plan to quote in the literature database. The review’s own summary is reliable for high-level methodological extraction, but exact row-level evidence belongs in the cited primary papers.
- Any likely ambiguity or risk of misinterpretation: The review supports spatial validation, sensitivity analysis, and methodological caution. It does not prove that any one spatial model is best for Open Road Risk, and it does not validate a direct production change from XGBoost/GLM to Bayesian spatial models or GWR.
