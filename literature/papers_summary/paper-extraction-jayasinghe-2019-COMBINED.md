# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: 1-s2.0-S2215016119301128-main.pdf
- Suggested Markdown filename: final.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: original PDF plus two Markdown extractions
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The uploaded PDF text was accessible. Page-image/table snippets were used where available, especially Tables 3–5 and the conclusion/limitations sections.

## 1. Citation

- Title: A novel approach to model traffic on road segments of large-scale urban road networks
- Authors: Amila Jayasinghe; Kazushi Sano; C. Chethika Abenayake; P.K.S. Mahanama
- Year: 2019
- DOI or URL, if present: https://doi.org/10.1016/j.mex.2019.04.024
- Country / region studied: Sri Lanka, Cambodia, Vietnam, Pakistan, and Tanzania
- Study setting: Urban road networks in five developing-country case-study cities: Colombo, Phnom Penh, Hanoi, Karachi, and Dar es Salaam.

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper proposes and validates a network-centrality-based method for estimating road-segment-level traffic volume / AADT using betweenness centrality, closeness centrality, and a road-type-weighted path-distance measure.
- Main purpose: prediction / traffic volume modelling / exposure modelling.
- Evidence quote or page reference: Page 1149 states that the objective is “to develop a network centrality-based method to model the vehicular traffic volume of road segments at macro level road networks.”

## 3. Response Variable

- Target variable: Annual Average Daily Traffic (AADT), converted to Passenger Car Units (PCU) per day.
- Collision type: Not applicable. This is not a collision modelling paper.
- Severity handling: Not applicable.
- Count, binary, rate, risk score, severity class, or other: Continuous traffic-volume count.
- Time window used for outcomes: Single cross-sectional base year per city: Colombo 2013, Phnom Penh 2012, Hanoi 2007, Karachi 2010, and Dar es Salaam 2008.
- Evidence quote or page reference: Page 1153 states that traffic volume was reported as AADT and converted to PCU per day using AASHTO PCU factors. Table 2 on page 1153 gives the case-study years.

## 4. Exposure Handling

- Exposure variable used, if any: AADT is the response variable, not an exposure variable in a collision model.
- Traffic count source: JICA database: CoMTrans Urban Transport Master Plan for Colombo and Person Trip Survey databases for the other four cities.
- Whether exposure is modelled, observed, assumed, or ignored: Exposure is modelled. Observed AADT counts are used for calibration and validation.
- Treatment of missing or sparse traffic counts: The paper is explicitly motivated by sparse or costly traffic-count coverage. It tests repeated random sub-sampling and reports that about 40 calibration observations can produce acceptable RMSE below 30% in the studied cities.
- Whether offset terms, rates, denominators, or normalisation are used: No exposure offset. Centrality measures may be normalised for comparison, and path-distance uses metric distance weighted by road-type speed factors.
- Evidence quote or page reference: Page 1153 describes the JICA AADT sources and 80/20 calibration/validation split. Page 1155 states that trained datasets of increasing sizes were randomly selected and accuracy assessed using the remaining validation data. Table 5 on page 1155 reports RMSE by calibration sample size.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The paper is highly relevant to Stage 1a as a traffic-exposure modelling paper, but the direct method is not automatically transferable. It was tested on developing-country urban networks, with city-by-city recalibration and random validation splits. Open Road Risk's UK mixed urban/rural/motorway network, OS Open Roads segmentation, and sparse AADF/WebTRIS coverage create a different setting.

Important:

- This paper does not model collision risk.
- It does not support any Stage 2 collision-risk modelling change directly.
- It is most useful as a Stage 1a feature-engineering and validation reference.

## 5. Spatial Unit of Analysis

- Unit: Road segment.
- Segment length or segmentation rule: Not fixed-length. The study uses road centreline data and a road-segment graph representation.
- How crashes are assigned to the network: Not applicable; no crash data are used.
- Treatment of junctions/intersections: The paper focuses on road segments rather than junctions. It discusses the dual-graph method, where road segments are represented as nodes and relationships between segments are represented through the graph.
- Spatial aggregation risks: The paper does not explicitly assess spatial aggregation risk or boundary effects. Centrality values depend on network extent and the chosen search radius, so boundary effects are a likely implementation concern. Random train/test splits may also be optimistic because nearby segments in the same network can be structurally similar.
- Evidence quote or page reference: Page 1150 states that because the focus is road segments rather than junctions, the dual-graph method was employed. Page 1152 describes use of road centreline vector line data.
- Relevance to OS Open Roads link-based pipeline: Medium to high. The road-segment focus is compatible with OS Open Roads links in principle, but direct transfer depends on how links are converted into the graph, how junctions/dual-graph edges are defined, and whether centrality can be computed at Open Road Risk scale.

## 6. Temporal Unit of Analysis

- Years covered: Single base year per city: 2007, 2008, 2010, 2012, or 2013 depending on case study.
- Temporal resolution: Annual average daily traffic.
- Whether seasonality or time-of-day is modelled: No.
- Whether before-after or panel structure is used: No. The paper uses cross-sectional traffic-volume modelling.
- Evidence quote or page reference: Page 1159 states that validation does not explicitly account for seasonal traffic-volume variations or daily peak flow.
- Relevance to WebTRIS-style time profiles: Low. The paper is relevant to annual exposure estimation, not Stage 1b time-of-day profile modelling.

## 7. Engineered Features

Only features actually used in the final model are listed.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Betweenness centrality with path-distance, BC(PD) | Road centreline network and road type | Computed using sDNA on the road graph, with path-distance as the custom distance; 20 km radius used | Intended to capture pass-by trips through a road segment | Medium to high as a Stage 1a diagnostic/candidate feature; exact computation at 2.1M links may be difficult |
| Closeness centrality with path-distance, CC(PD) | Road centreline network and road type | Computed using sDNA on the road graph, with path-distance as the custom distance; 20 km radius used | Intended to capture O-D trip potential / accessibility | Medium to high as a Stage 1a diagnostic/candidate feature; computational and boundary effects need testing |
| Path distance, PD | Metric distance and road type | `PD = Ty × MD`, where MD is metric distance and Ty is a road-type speed/impedance factor | Attempts to capture both topological/mobility characteristics and road hierarchy | Medium; UK road-class/speed mappings would need recalibration |
| Road type speed/impedance factor, Ty | Road hierarchy categories | Suggested values include 1/80 for expressways, 1/60 for major arteries, 1/40 for minor arteries, 1/25 for collectors, and 1/15 for local roads | Weights centrality by approximate travel-time / mobility hierarchy rather than pure length | Medium; usable conceptually, but the values are not UK-calibrated |

Features explicitly not used:

- Land-use data are not used.
- OD matrices are not used.
- Extensive traffic-count coverage is not required.
- Collision variables are not used.

## 8. Model Architecture

- Algorithms/models used: OLS, Robust Regression, and Poisson Regression are mentioned as statistical techniques considered. The reported final structure is a linear regression of traffic volume on BC(PD) and CC(PD).
- Baseline model: A BC-only model is discussed as weaker, with R² below 0.8 and RMSE above 40%.
- Final/preferred model: `TV(i) = a + b × CC(i) + c × BC(i)`, where centrality is computed using path-distance.
- Loss function or likelihood, if stated: Not explicitly stated for the selected model. OLS-style R² and regression coefficients are reported.
- Offset/exposure term, if used: None. AADT is the target.
- Spatial autocorrelation handling: Not stated. No explicit spatial error, spatial lag, or spatial holdout is reported.
- Temporal dependence handling: Not applicable; cross-sectional.
- Interpretability method: Regression coefficients, partial correlations, part correlations, and mapped comparisons of centrality/AADT patterns.
- Evidence quote or page reference: Page 1151 gives the model form `TV(i) = a + b[CC(i)] + c[BC(i)]`. Page 1153 states that OLS, Robust Regression, and Poisson Regression were used for model formulation. Table 3 on page 1154 reports coefficients and part/partial correlations.

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Calibration fit | R² | 0.928 | Colombo | High in-sample fit for traffic volume | Table 3, page 1154 |
| Calibration fit | R² | 0.936 | Phnom Penh | High in-sample fit | Table 3, page 1154 |
| Calibration fit | R² | 0.916 | Hanoi | High in-sample fit | Table 3, page 1154 |
| Calibration fit | R² | 0.977 | Karachi | Very high in-sample fit | Table 3, page 1154 |
| Calibration fit | R² | 0.967 | Dar es Salaam | Very high in-sample fit | Table 3, page 1154 |
| Validation fit | R² | 0.935 | Colombo random 20% validation | High random-holdout fit | Table 3, page 1154 |
| Validation fit | R² | 0.942 | Phnom Penh random 20% validation | High random-holdout fit | Table 3, page 1154 |
| Validation fit | R² | 0.923 | Hanoi random 20% validation | High random-holdout fit | Table 3, page 1154 |
| Validation fit | R² | 0.951 | Karachi random 20% validation | High random-holdout fit | Table 3, page 1154 |
| Validation fit | R² | 0.959 | Dar es Salaam random 20% validation | High random-holdout fit | Table 3, page 1154 |
| Calibration error | MdAPE | 12.6%–18.4% | Five cities | Median absolute percent error in calibration | Table 3, page 1154 |
| Validation error | MdAPE | 10.5%–17.3% | Five cities | Median absolute percent error in random validation | Table 3, page 1154 |
| Contribution | Partial correlation² for BC | 58%–62% | Five cities | BC captures a large share of AADT variability | Table 3, page 1154 |
| Contribution | Partial correlation² for CC | 32%–35% | Five cities | CC adds additional explanatory signal | Table 3, page 1154 |
| Error by AADT category | Average RMSE | 14.2%–19.1% | City averages | Average RMSE reported within FHWA-style threshold | Table 4, page 1155 |
| Low-AADT weakness | RMSE for AADT < 1000 | 193.1% Colombo; 412.5% Phnom Penh; not reported for other cities | Very low AADT category | Very poor relative error in low-volume category where available | Table 4, page 1155 |
| Sparse calibration | RMSE at 40 observations | 29% Colombo; 23% Phnom Penh; 22% Hanoi; 17% Karachi; 18% Dar es Salaam | Repeated random sub-sampling / calibration-size test | Around 40 random calibration observations reaches <30% RMSE in all five cities | Table 5, page 1155 |
| Sparse calibration | RMSE at 10 observations | 72%–129% | Repeated random sub-sampling / calibration-size test | Very small calibration samples are unstable | Table 5, page 1155 |
| Baseline comparison | R² | `< 0.8` | BC-only model | Weaker than BC+CC | Page 1154 |
| Baseline comparison | RMSE | `> 40%` | BC-only model | Weaker than BC+CC | Page 1154 |

After the table:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? Calibration metrics are in-sample. Validation metrics use a random 20% holdout within each city. The repeated random sub-sampling analysis tests sensitivity to calibration sample size. There is no spatial holdout, temporal holdout, grouped holdout, or held-out-city external validation.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy. The calibration R²/MdAPE are in-sample diagnostics. The validation R²/MdAPE are random-holdout diagnostics, not spatial or external validation.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They test traffic-volume model fit and random-holdout prediction of AADT within the same city networks. They do not test collision risk, safety ranking, or exposure-adjusted collision modelling.
- Are any metrics likely to be optimistic for real-world deployment? Yes. Random splitting within road networks can be optimistic because nearby road segments may share centrality, hierarchy, and flow structure. The paper also fits/recalibrates models city by city rather than holding out an entire city.
- Which metric, if any, is most relevant to Open Road Risk? The sparse-calibration analysis in Table 5 is the most useful validation idea. The low-AADT RMSE in Table 4 is the most important warning for rural/minor-road exposure modelling.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Not applicable. The paper does not model collisions.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson Regression is mentioned as a tested traffic-volume modelling technique, but no rare-event collision framework is used.
- Whether high-risk locations are evaluated separately: Not applicable.
- Evidence quote or page reference: Page 1153 states that OLS, Robust Regression, and Poisson Regression were used for model formulation. The response variable is AADT, not crashes.
- Practical relevance to my sparse collision link-year dataset: Indirect only. The paper is relevant to exposure estimation in Stage 1a, not to sparse collision count modelling in Stage 2.

## 11. Validation Strategy

- Train/test split method: Random 80% calibration and 20% validation within each city.
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Repeated random sub-sampling validation is used for the minimum-observations sensitivity analysis, not as a spatial or temporal validation design.
- Metrics: R², adjusted R², MdAPE, RMSE by AADT category, RMSE by calibration sample size.
- External validation: No strict external validation. The model structure is replicated across five cities, but parameters are fitted per city and no whole-city holdout is reported.
- Leakage or generalisation risks: Random splitting within a spatial network does not test transfer to unseen corridors, regions, or future years. Adjacent or structurally similar links may appear in both training and validation data. No explicit spatial autocorrelation analysis is reported.
- Evidence quote or page reference: Page 1153 states that the study used randomly selected 80% calibration data and 20% validation data. Page 1155 describes repeated random sub-sampling by training set size.
- What I should copy or avoid: Copy the learning-curve / calibration-sample-size diagnostic. Avoid relying on random link-level splits as strong evidence of Stage 1a spatial generalisation; Open Road Risk's grouped/spatial validation should remain stronger.

## 12. Key Findings Relevant to My Project

1. Finding: BC(PD) and CC(PD) together produce high random-holdout AADT fit in five developing-country urban networks.
   - Why it matters: Supports testing closeness centrality alongside betweenness in Open Road Risk Stage 1a.
   - Evidence quote or page reference: Table 3 on page 1154 reports validation R² from 0.923 to 0.959 and validation MdAPE from 10.5% to 17.3%.
   - Confidence: medium. The result is strong within the paper but transfer to UK mixed networks is untested.

2. Finding: BC contributes more than CC, but CC still adds non-trivial explanatory signal.
   - Why it matters: If Open Road Risk already uses betweenness but not closeness, CC is a plausible candidate feature or diagnostic.
   - Evidence quote or page reference: Table 3 on page 1154 reports partial correlation² around 58%–62% for BC and 32%–35% for CC.
   - Confidence: medium.

3. Finding: Very low AADT categories are weakly estimated by this centrality-based method where data are reported.
   - Why it matters: Open Road Risk contains many low-volume rural/minor links, exactly where exposure estimation is hardest.
   - Evidence quote or page reference: Table 4 on page 1155 reports RMSE of 193.1% for Colombo and 412.5% for Phnom Penh in the `< 1000` AADT category.
   - Confidence: high for the paper result; medium for transferability.

4. Finding: A road-type-weighted path-distance variable is central to the paper's method.
   - Why it matters: Open Road Risk should check whether its current network centrality features are unweighted, metric-weighted, or travel-time/road-class weighted.
   - Evidence quote or page reference: Page 1152 defines `PD = Ty × MD`, and the conclusion on pages 1157–1159 says path distance accounts for road hierarchy and metric distance.
   - Confidence: high.

5. Finding: A learning-curve diagnostic based on number of calibration observations is directly useful.
   - Why it matters: Open Road Risk can test how Stage 1a performance changes as AADF count coverage is reduced, but should combine this with grouped/spatial validation.
   - Evidence quote or page reference: Table 5 on page 1155 reports RMSE by training set size; around 40 observations gives RMSE below 30% in all five case studies.
   - Confidence: high for diagnostic value; medium for direct benchmark transfer.

6. Finding: The paper does not address seasonality, daily peak flow, or dynamic congestion propagation.
   - Why it matters: It is not a substitute for WebTRIS-style Stage 1b temporal traffic profiles.
   - Evidence quote or page reference: Page 1159 states that validation does not explicitly account for seasonal variations or daily peaks, and page 1160 notes the need for dynamic models.
   - Confidence: high.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Add/test closeness centrality as Stage 1a feature | CC adds O-D/accessibility signal beyond BC in the paper | OS Open Roads graph | 679–2397 counted segments per city; city networks 785–2075 km | Conceptually compatible, but compute cost at 2.1M links needs benchmarking | Stage 1a / feature engineering | Medium | CC may be correlated with existing features or expensive at scale |
| Compare unweighted, metric-weighted, and road-class/speed-weighted centrality | Paper's path-distance concept may improve centrality relevance to traffic | Road length, road classification, speed proxies | Five city networks | Compatible in principle | Stage 1a / validation | Medium | Ty values need UK calibration; speed-limit data coverage may be uneven |
| Learning-curve diagnostic for AADF count sparsity | Quantifies how model performance degrades with fewer count points | AADF/WebTRIS count data and Stage 1a model | Table 5 tests N from 10 to 1500 | Directly applicable as a diagnostic | Stage 1a / validation / documentation | Low | Random sub-sampling alone is optimistic; should add spatial/grouped variants |
| Low-AADT subgroup error reporting | Paper shows very poor low-AADT RMSE, a relevant warning | AADF observed counts and Stage 1a predictions | AADT category table | Directly applicable | Stage 1a / validation | Low | Need enough observed low-AADT count points for stable estimates |
| Documentation note on centrality-based exposure modelling | Provides literature support for centrality as traffic-exposure proxy | Existing extraction and Stage 1a docs | Five case cities | Useful as context, not proof | documentation | Low | Overstating transferability from urban developing-country networks |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Replacing Stage 1a with two-predictor OLS | Open Road Risk already uses richer AADF/WebTRIS/road/context features; two-predictor OLS would likely be weaker | No missing data; methodological downgrade | City-level urban networks | Low as production replacement | Use BC/CC/PD features inside current model family | High |
| Using the paper's Ty values directly | Ty values are tied to generic/developing-country road hierarchy and speed bands | UK-calibrated speed/road-class mapping | Five developing-country cities | Low for direct reuse | Recalibrate Ty using UK road class/speed data | High |
| Treating random validation R² as spatial generalisation | Random splits do not test unseen regions/corridors | Spatial/grouped holdout | Within-city random splits | Low | Use grouped/spatial validation by count point/corridor/region | High |
| Applying the method to Stage 2 collision risk | The paper models AADT only and has no collision outcome | Collision data, safety model | No crash data | Low | Use only as Stage 1a exposure feature reference | High |
| Assuming strong performance on low-volume rural roads | The paper is urban and shows poor RMSE for very low AADT categories where reported | Rural/minor-road validation | Urban networks | Low to medium | Validate low-AADT/rural subsets separately | High |

Important:

- This is a useful Stage 1a paper, not a Stage 2 safety model paper.
- Treat the paper's accuracy as an urban traffic-volume benchmark, not proof that centrality will solve low-volume rural AADT estimation.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Indirectly only. It supports methods for estimating exposure/AADT, not collision risk.
- Does it suggest better handling of AADT/AADF uncertainty? Yes. It suggests centrality-based features and learning-curve validation for sparse traffic-count settings.
- Does it suggest useful geometry or road-context features? Yes. Betweenness centrality, closeness centrality, and road-type/speed-weighted path-distance are the main features.
- Does it suggest better modelling of junctions? No. Junctions are not the target unit; the model focuses on road segments.
- Does it suggest better treatment of severity? No. No collision severity is modelled.
- Does it suggest better validation design? It suggests a calibration-sample-size sensitivity analysis. Its own random split is weak for spatial generalisation, so Open Road Risk should use stronger grouped/spatial validation.
- Does it expose a weakness in my current approach? If Open Road Risk's Stage 1a lacks closeness centrality or road-class/speed-weighted centrality, these are reasonable feature checks. It also reinforces that low-AADT subgroup performance should be reported separately.

## 15. Repo Actionability

1. Suggested repo action: Add or test closeness centrality as a Stage 1a AADT feature alongside existing betweenness/degree features.
   - Action type: candidate feature / diagnostic
   - Relevant stage: Stage 1a / feature engineering
   - Why the paper supports it: The paper's final model combines BC and CC, with CC contributing additional explanatory signal.
   - Evidence quote or page reference: Equation 6 on page 1151 and Table 3 on page 1154.
   - Effort: medium
   - Risk if implemented badly: Full-network closeness can be computationally expensive and sensitive to graph boundaries.

2. Suggested repo action: Compare current centrality implementation against a road-class/speed-weighted path-distance variant.
   - Action type: diagnostic / candidate feature
   - Relevant stage: Stage 1a / validation
   - Why the paper supports it: The paper introduces `PD = Ty × MD` to account for road hierarchy and metric distance.
   - Evidence quote or page reference: Page 1152 and Table 1 on page 1153.
   - Effort: medium
   - Risk if implemented badly: Imported Ty values may not reflect UK road classes; recalibration is needed.

3. Suggested repo action: Add a Stage 1a learning-curve diagnostic showing performance as the number of training count points is reduced.
   - Action type: diagnostic
   - Relevant stage: Stage 1a / validation
   - Why the paper supports it: The paper uses repeated random sub-sampling to test minimum calibration observations.
   - Evidence quote or page reference: Table 5 and Figure 6 around pages 1155–1156.
   - Effort: low
   - Risk if implemented badly: Random sub-sampling will be optimistic unless paired with grouped/spatial variants.

4. Suggested repo action: Report Stage 1a error by AADT band, especially low-AADT links.
   - Action type: validation diagnostic
   - Relevant stage: Stage 1a / validation / documentation
   - Why the paper supports it: Table 4 shows acceptable average RMSE but very poor relative RMSE in the `<1000` AADT category where reported.
   - Evidence quote or page reference: Table 4 on page 1155.
   - Effort: low
   - Risk if implemented badly: Low-AADT percentage errors can look extreme; include absolute-error context too.

5. Suggested repo action: Add a documentation note that centrality-based AADT models are promising but the evidence here is urban, cross-sectional, and randomly validated.
   - Action type: documentation note
   - Relevant stage: Stage 1a / documentation
   - Why the paper supports it: The paper validates across five cities but does not use spatial or temporal holdout and notes temporal limitations.
   - Evidence quote or page reference: Pages 1153, 1155, 1159–1160.
   - Effort: low
   - Risk if implemented badly: Overstating the paper as proof for UK rural/motorway exposure estimation.

## 16. Query Tags

- AADT-estimation
- traffic-volume-modelling
- betweenness-centrality
- closeness-centrality
- path-distance
- road-type-weighting
- speed-weighted-centrality
- space-syntax
- sDNA
- road-segment-level
- dual-graph
- sparse-count-calibration
- learning-curve-validation
- random-holdout
- low-AADT-error
- urban-networks
- developing-countries
- Stage-1a
- exposure-modelling
- no-collision-data

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: No spatial autocorrelation check; no spatial holdout; no temporal holdout; no held-out-city validation; no collision outcome; no seasonal or peak-hour modelling; no sensitivity test for the 20 km radius; no UK/European transfer test; no direct test on rural low-volume networks.
- Parts of the paper that need manual checking: The final selected regression type is implied by the reported linear equation and R² tables, but the paper states that OLS, Robust Regression, and Poisson Regression were used without clearly documenting a full model-selection table for those alternatives.
- Any likely ambiguity or risk of misinterpretation: The high R² values are random-holdout results within the same city networks, not spatial generalisation. “N < 40” / “about 40 observations” should be read as a random sub-sampling result in these case studies, not a universal minimum count requirement. The method is useful for Stage 1a exposure modelling, not Stage 2 collision-risk modelling.
