# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: 1-s2.0-S2046043017300199-main.pdf
- Suggested Markdown filename: paper-extraction-pan-2017-global-road-safety-performance-function-dbn.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The extraction is based on the uploaded PDF text and rendered page images. No repository code was accessed.

## 1. Citation

- Title: Development of a global road safety performance function using deep neural networks
- Authors: Guangyuan Pan; Liping Fu; Lalita Thakali
- Year: 2017
- DOI or URL, if present: http://dx.doi.org/10.1016/j.ijtst.2017.07.004
- Country / region studied: Canada and United States; Highway 401 in Ontario, Colorado highways, and Washington State highways.
- Study setting: mixed; includes urban and rural highway segments, multilane access-controlled highway, rural two-lane highways, rural multilane highways, urban two-lane highways, and urban multilane highways.

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper tests whether a deep belief network can be trained as a global safety performance function to predict expected crash frequencies across highway types and regions.
- Main purpose: prediction / safety performance function / model comparison.
- Evidence quote or page reference: Page 1 states that the paper applies machine learning to develop a global road safety performance function that can predict expected crash frequencies of different highways from different regions. Page 2 says the research explores a modelling framework where datasets from multiple regions are pooled into one modelling step to generate a single global model.

## 3. Response Variable

- Target variable: Crash or collision frequency per road segment-year observation.
- Collision type: all crashes / not fully stated by severity. The paper uses historical crash records and collision frequencies; it does not state that the target is restricted to injury crashes.
- Severity handling: Not stated. Severity is not modelled separately in the reported DBN or NB models.
- Count, binary, rate, risk score, severity class, or other: Count; annual crash/collision frequency.
- Time window used for outcomes: Ontario Highway 401: 2000–2008, with 2000–2006 for training and 2007–2008 for testing. Colorado: 1991–1998, with 1991–1996 for training and 1997–1998 for testing. Washington: yearly highway inventory and crash data, but exact calendar years are not stated in the extracted text.
- Evidence quote or page reference: Page 5 describes historical crash records for Highway 401 from 2000 to 2008. Page 5 describes the Colorado dataset as observations from 1991 to 1998. Page 6 says crashes were aggregated on an annual basis over homogeneous segments in the Washington inventory file.

## 4. Exposure Handling

- Exposure variable used, if any: AADT, segment length, and in the Ontario case commercial AADT. Some NB models use `log(AADT * Length * 365 / 10^6)` as a combined exposure feature; others use `log(AADT)` and `log(Length)` separately.
- Traffic count source: Ontario: Ministry of Transportation Ontario Traffic Volume Inventory System. Colorado: existing Colorado rural two-lane highway dataset downloaded from supplementary data linked to Hauer's road safety regression modelling book. Washington: FHWA Highway Safety Information System highway inventory data.
- Whether exposure is modelled, observed, assumed, or ignored: Observed or assigned from traffic count/inventory data. For Ontario, each homogeneous segment was assigned the nearest traffic observation from 170 traffic counting stations.
- Treatment of missing or sparse traffic counts: Washington records with missing traffic data were removed. Ontario assigned nearest traffic observations to homogeneous segments. No traffic count imputation model is described.
- Whether offset terms, rates, denominators, or normalisation are used: The NB benchmark models use exposure-related terms as explanatory variables, not clearly as fixed-offset terms. The DBN uses normalized input features, including AADT and segment length where available.
- Evidence quote or page reference: Page 5 states that Highway 401 AADT ranged from 14,500 to 442,900 and that traffic data came from MTO's TVIS. Page 6 says Washington records with missing traffic data were removed. Page 9 states that AADT and segment length were tested either as combined `log(AADT*Length*365/10^6)` or individually as `log(AADT)` and `log(Length)`.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The broad mathematical idea of using AADT and length as exposure-like predictors is highly transferable. The paper does not address sparse national AADF coverage, estimated traffic counts, or uncertainty propagation, so its specific exposure handling has only medium transferability to Open Road Risk. It is weaker than your current explicit exposure-offset framing because the benchmark NB models treat exposure as estimated covariates rather than clearly as an offset.

Important:

- Mathematical exposure structure: medium/high transferability as a comparison or diagnostic because `log(AADT * length * time)` is close to your current exposure offset.
- Specific traffic data source: low/medium transferability because the paper uses richer highway inventory and count data than may exist for every OS Open Roads link.

## 5. Spatial Unit of Analysis

- Unit: Road segment / homogeneous highway section.
- Segment length or segmentation rule: Ontario generated homogeneous sections with similar characteristics; shortest length 0.2 km; 418 unique sections covering about 800 km. Colorado used rural two-lane highway sections of 0.21 to 31.76 km. Washington used homogeneous inventory segments and removed records with segment length less than 0.16 km.
- How crashes are assigned to the network: Crashes are geocoded or aggregated to homogeneous sections using linear highway reference systems or route/milepost fields.
- Treatment of junctions/intersections: Washington removed crashes at intersections, interchanges, ramps, driveways, and other records outside the highway segment study scope. Ontario and Colorado are treated as highway segment datasets; explicit junction treatment is not fully stated.
- Spatial aggregation risks: The paper uses agency-defined or generated homogeneous segments, not OS Open Roads links. Segment lengths can be much longer than typical OS links, especially in Colorado and Ontario. This may smooth risk and reduce compatibility with highly granular link-level modelling.
- Evidence quote or page reference: Page 5 states that Highway 401 generated 418 homogeneous sections from 0.2 km to 12.7 km. Page 5 states the Colorado dataset covered 4593 unique sections from 0.21 to 31.76 km. Page 6 states Washington removed records with segment length less than 0.16 km and excluded intersection/interchange/ramp/driveway crashes.
- Relevance to OS Open Roads link-based pipeline: Conceptually relevant for segment-level SPF modelling, but direct transfer is limited by much coarser and more homogeneous highway segmentation than OS Open Roads link geometry.

## 6. Temporal Unit of Analysis

- Years covered: Ontario: 2000–2008. Colorado: 1991–1998. Washington: not stated in the extracted text.
- Temporal resolution: yearly segment observations.
- Whether seasonality or time-of-day is modelled: No.
- Whether before-after or panel structure is used: Panel-like segment-year observations are used, but the paper does not model temporal dependence as a panel process. Training/testing splits are by years for Ontario and Colorado.
- Evidence quote or page reference: Page 5 describes Ontario data for 2000–2008 and Colorado observations from 1991–1998. Page 6 says crashes were aggregated on an annual basis over individual homogeneous segments for Washington.
- Relevance to WebTRIS-style time profiles: Low direct relevance. The paper does not model time-of-day or peak/off-peak exposure profiles.

## 7. Engineered Features

List the most important engineered features actually used in the paper.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| AADT | MTO TVIS; Colorado dataset; FHWA HSIS inventory | Used directly, normalized for DBN; log-transformed in NB models | Main vehicle exposure variable | already present / compare implementation |
| Segment length | Highway inventory / generated homogeneous sections | Used directly, normalized for DBN; log-transformed in NB models | Exposure and spatial scale | already present / compare implementation |
| `log(AADT * Length * 365 / 10^6)` | AADT and segment length | Combined exposure feature in Ontario NB model | Closest paper analogue to vehicle-km exposure | already present as offset-like structure / compare implementation |
| Commercial AADT | MTO traffic data | Used as input feature in Ontario NB/DBN setup | Heavy/commercial vehicle exposure proxy | partially transferable if HGV proportion/counts available |
| Number of lanes | Highway inventory | Used as input for DBN where available; high correlation with AADT led to exclusion in NB example | Captures road capacity/type | candidate feature if reliable lanes coverage improves; currently sparse OSM coverage |
| Lane width | Highway inventory | Used as input/coefficients in Washington NB models; available to DBN where present | Road geometry/context | low/medium; not widely available in open UK data |
| Median width | Highway inventory | Used in NB/DBN where available | Divided/high-capacity road context | medium if form of way/divided-road proxies are used; exact width low |
| Left/right shoulder width | Highway inventory | Used in NB/DBN where available | Roadside design and recovery area | low for national open UK pipeline unless OSM/other proxy coverage improves |
| Curve deflection per km | GIS-derived from Highway 401 curves | Curvature sections created and joined to homogeneous segments | Geometry/risk context | already present or candidate comparison for curvature implementation |
| Terrain | Colorado/Washington inventory | Categorised as mountainous, rolling, level/flat | Captures topography/geometric environment | partially transferable via OS Terrain 50 grade/terrain features |
| Rural/urban / city type | Google Earth for Ontario; dataset flags for others | Encoded as input indicator; in NB example excluded for Ontario when it made geometry variables insignificant | Road environment type | already present/candidate via rural-urban classification |
| Location indicator | Case study dataset ID | Encoded as constant 1/2/3 for global DBN | Allows global model to learn regional differences | useful only as diagnostic/facility-family or regional indicator |
| Access type | Dataset/inventory | Encoded as DBN input indicator | Highway class/access control differences | partly transferable via road classification/form of way |

## 8. Model Architecture

- Algorithms/models used: Deep belief network (DBN), Bayesian artificial neural network, and negative binomial regression benchmark models.
- Baseline model: Locally calibrated negative binomial models for each highway type/geographical location.
- Final/preferred model: Global DBN trained across multiple datasets, with experiments for separate local DBN training, simultaneous global DBN training, and sequential retraining with new data.
- Loss function or likelihood, if stated: For DBN supervised fine-tuning, objective combines mean squared prediction error and Bayesian regularisation term: `FW = aP + bEW`, where `P` is based on squared output error and `EW` is mean square of weights. NB models are estimated using maximum likelihood.
- Offset/exposure term, if used: Not a fixed offset in the DBN. NB benchmark models use exposure-like predictors including `log(AADT * Length * 365 / 10^6)` or separate `log(AADT)` and `log(Length)`.
- Spatial autocorrelation handling: Not stated. No explicit spatial random effects, spatial lag, or spatial holdout design is reported.
- Temporal dependence handling: Not stated. Temporal train/test splits are used in some experiments, but no temporal dependence model is reported.
- Interpretability method: NB coefficients are reported. DBN interpretability is limited; no feature importance or explainability method is reported.
- Evidence quote or page reference: Page 2 describes the global DBN architecture with visible, hidden, and output layers. Page 4 states Bayesian regularization is used instead of back propagation for fine-tuning. Page 9 states NB uses an exponential function for expected crash frequency and that coefficients are estimated by maximum likelihood in R.

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---:|---|---|---|
| Dataset scale | Training / testing observations | 2926 / 836 | Ontario Highway 401 | Temporal train/test split, 2000–2006 vs 2007–2008 | Pages 6 and 11, Table 8 |
| Dataset scale | Training / testing observations | 27,558 / 9186 | Colorado rural two-lane | Temporal train/test split, 1991–1996 vs 1997–1998 | Pages 5–6 and 11, Table 8 |
| Dataset scale | Training / testing observations | 28,436 / 16,569 | Washington rural two-lane | Train/test split; basis not fully stated | Page 7, Table 3 |
| Dataset scale | Training / testing observations | 3381 / 3456 | Washington rural multilane | Train/test split; basis not fully stated | Page 7, Table 3 |
| Dataset scale | Training / testing observations | 3566 / 1138 | Washington urban two-lane | Train/test split; basis not fully stated | Page 7, Table 3 |
| Dataset scale | Training / testing observations | 5377 / 2533 | Washington urban multilane | Train/test split; basis not fully stated | Page 7, Table 3 |
| Local model comparison | MAE | NB 12.39; Bayesian ANN 11.61; DBN 9.59 | Ontario Highway 401 | DBN improves MAE by 22.60% over NB | Page 11, Table 6 |
| Local model comparison | RMSE | NB 28.94; Bayesian ANN 26.81; DBN 19.58 | Ontario Highway 401 | DBN improves RMSE by 32.34% over NB | Page 11, Table 6 |
| Local model comparison | MAE | NB 0.83; Bayesian ANN 0.83; Global DBN 0.81 | Colorado rural highways | DBN improves MAE by 2.40% over NB | Page 11, Table 7 |
| Local model comparison | RMSE | NB 1.67; Bayesian ANN 1.60; Global DBN 1.48 | Colorado rural highways | DBN improves RMSE by 11.38% over NB | Page 11, Table 7 |
| Simultaneous global training | MAE | NB 12.39; global DBN 10.00 | Ontario Highway 401 | Global DBN improves MAE by 19.29% over NB | Page 12, Table 8 |
| Simultaneous global training | RMSE | NB 28.94; global DBN 22.24 | Ontario Highway 401 | Global DBN improves RMSE by 23.15% over NB | Page 12, Table 8 |
| Simultaneous global training | MAE | NB 0.83; global DBN 0.82 | Colorado rural | Small MAE improvement of 1.20% | Page 12, Table 8 |
| Simultaneous global training | RMSE | NB 1.67; global DBN 1.52 | Colorado rural | RMSE improvement of 8.98% | Page 12, Table 8 |
| Simultaneous global training | MAE | NB 0.50; global DBN 0.47 | Washington rural two-lane | MAE improvement of 6.00% | Page 12, Table 8 |
| Simultaneous global training | RMSE | NB 0.79; global DBN 0.82 | Washington rural two-lane | RMSE worse than NB by 3.80% | Page 12, Table 8 |
| Simultaneous global training | MAE | NB 0.98; global DBN 0.98 | Washington rural multilane | No MAE improvement | Page 12, Table 8 |
| Simultaneous global training | RMSE | NB 1.56; global DBN 1.59 | Washington rural multilane | RMSE worse than NB by 1.92% | Page 12, Table 8 |
| Simultaneous global training | MAE | NB 0.66; global DBN 0.59 | Washington urban two-lane | MAE improvement of 10.61% | Page 12, Table 8 |
| Simultaneous global training | RMSE | NB 0.93; global DBN 0.93 | Washington urban two-lane | No RMSE improvement | Page 12, Table 8 |
| Simultaneous global training | MAE | NB 2.04; global DBN 1.91 | Washington urban multilane | MAE improvement of 6.37% | Page 12, Table 8 |
| Simultaneous global training | RMSE | NB 3.81; global DBN 3.45 | Washington urban multilane | RMSE improvement of 9.45% | Page 12, Table 8 |
| Sequential retraining | MAE | NB 12.39; DBN after new data 10.68 | Ontario Highway 401 | Sequential model improves MAE by 13.80% over NB | Page 14, Table 9 |
| Sequential retraining | RMSE | NB 28.94; DBN after new data 22.24 | Ontario Highway 401 | Sequential model improves RMSE by 23.15% over NB | Page 14, Table 9 |
| Sequential retraining | MAE | NB 0.83; DBN after new data 0.82 | Colorado rural | Small MAE improvement of 1.20% | Page 14, Table 9 |
| Sequential retraining | RMSE | NB 1.67; DBN after new data 1.51 | Colorado rural | RMSE improvement of 9.58% | Page 14, Table 9 |

After the table:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? The main metrics are out-of-sample test-set metrics. For Ontario and Colorado they are temporally held out by year. For Washington, the paper reports training/testing splits but the exact split method is not fully stated in the extracted text. They are not spatially held out and not externally validated beyond using multiple regions within the same study.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. The main MAE/RMSE results are test-set diagnostics, not purely in-sample diagnostics.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They test average predictive error on held-out segment-year observations. They do not directly test hotspot ranking, calibration, uncertainty, spatial transfer, or safety-treatment usefulness.
- Are any metrics likely to be optimistic for real-world deployment? Yes. The test data are from the same regions and facility datasets as training, with no explicit spatial holdout. The global model includes location/type indicators and uses inventory-quality features, so deployment to a new geography or sparse open-data network could perform worse.
- Which metric, if any, is most relevant to Open Road Risk? MAE/RMSE on temporally held-out segment-year counts are relevant as a benchmark diagnostic, but not sufficient for your risk-percentile/ranking use case. A grouped-by-link and spatially held-out ranking/calibration evaluation would be more relevant.

Important:

- The paper does not report ranking/hotspot performance.
- The paper does not report calibration curves, prediction intervals, or uncertainty propagation.
- The paper does not report spatially held-out validation.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Crash counts are modelled using NB regression benchmarks and DBN count prediction. The paper does not describe special rare-event, imbalance, hurdle, or zero-heavy count handling.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Negative binomial regression is used as the traditional benchmark. DBN is used as the proposed machine-learning model. Bayesian regularisation is used for DBN fine-tuning.
- Whether high-risk locations are evaluated separately: Not stated. No hotspot-specific or high-risk-tail evaluation is reported.
- Evidence quote or page reference: Page 5 states that NB is the most widely used technique in road safety analysis and is used as a benchmark. Page 9 gives the NB expected crash frequency model and maximum likelihood estimation approach. Pages 11–14 report MAE and RMSE, not rare-event-specific metrics.
- Practical relevance to my sparse collision link-year dataset: Limited. The paper includes sparse datasets such as Colorado and Washington rural highways with low mean annual crashes, but it does not present zero-heavy diagnostics or methods tailored to rare injury-collision outcomes.

Important:

- Do not tag this paper as `zero-inflation`; it does not fit a zero-inflated model.
- The correct conservative description is: zero-heavy counts are handled using NB regression benchmarks and DBN count prediction, without explicit zero-heavy model design.

## 11. Validation Strategy

- Train/test split method: Ontario: 2000–2006 training, 2007–2008 testing. Colorado: 1991–1996 training, 1997–1998 testing. Washington: training/testing samples are reported, but exact split logic is not stated in the extracted text.
- Spatial holdout used? no
- Temporal holdout used? yes for Ontario and Colorado; not stated for Washington.
- Grouped holdout used? not stated
- Cross-validation type: Not used for the main test metrics. Repeated training/bootstrapping is used to reduce initialization/training-set effects: 100 repetitions for Highway 401, 25 for Colorado, and 10 for global/sequential experiments.
- Metrics: MAE and RMSE.
- External validation: Not true external validation. The model is tested on held-out observations from the same source datasets. The multi-region design gives some evidence of cross-dataset pooling but does not test deployment to a completely unseen region.
- Leakage or generalisation risks: No clear classic leakage is stated. Main risks are weak spatial generalisation testing, possible repeated sections across years in temporal splits, and reliance on rich agency inventory variables unavailable in many open-data settings. Because the same road segments may appear in both train and test years, the test is temporal rather than independent link-level generalisation.
- Evidence quote or page reference: Page 6 describes Ontario and Colorado train/test year splits. Page 6 gives repeated training counts. Page 11 states the global DBN training set has 71,244 observations and each includes 13 features. Page 14 frames sequential retraining as a generalisation test when new datasets become available.
- What I should copy or avoid: Copy the idea of comparing local vs pooled/facility-family models under held-out evaluation. Avoid treating global pooled DBN gains as evidence for production deep learning unless spatial, grouped, calibration, and ranking validation are added.

Important:

- The paper's validation is stronger than in-sample fit because it uses held-out test sets.
- It is still weaker than Open Road Risk ideally needs because it does not include spatial holdout, grouped-by-link holdout, or hotspot/ranking validation.

## 12. Key Findings Relevant to My Project

1. Finding: A pooled/global model can sometimes match or outperform locally calibrated NB models across multiple highway datasets.
   - Why it matters: This supports testing whether facility-family or region-pooled models can improve stability in sparse crash settings.
   - Evidence quote or page reference: Page 14 concludes that a single DBN trained globally with multiple datasets predicted expected crash frequencies with performance at least comparable to traditional NB models.
   - Confidence: medium

2. Finding: The global DBN did not outperform NB in every subgroup.
   - Why it matters: This argues against assuming a global machine-learning model is uniformly better; subgroup/facility-family diagnostics are necessary.
   - Evidence quote or page reference: Page 14 states that rural Washington cases WA-R2 and WA-RM were exceptions where the global DBN was slightly outperformed by local NB models; Table 8 shows worse RMSE for WA-R2 and WA-RM.
   - Confidence: high

3. Finding: Temporal holdout evaluation using MAE and RMSE is feasible and used in SPF model comparison.
   - Why it matters: Open Road Risk can report held-out error for collision counts, but should add spatial/grouped and ranking diagnostics beyond this paper.
   - Evidence quote or page reference: Page 6 describes training on earlier years and testing on later years for Ontario and Colorado; page 7 defines MAE and RMSE.
   - Confidence: high

4. Finding: Exposure variables are central in both traditional and DBN models.
   - Why it matters: Supports continuing exposure-aware modelling rather than raw crash frequency ranking.
   - Evidence quote or page reference: Page 9 states AADT and segment length were tested in combined and separate log forms, with the decision based on test-set MAE/RMSE.
   - Confidence: high

5. Finding: Segment definition and minimum segment length matter.
   - Why it matters: The paper explicitly avoids very short segments due to uncertainty/exposure problems, relevant to OS Open Roads links which can be very short.
   - Evidence quote or page reference: Page 5 notes the shortest Ontario homogeneous section was 0.2 km and cites literature suggesting very short road segments may have higher uncertainty and lower exposure problems; page 6 removes Washington records shorter than 0.16 km.
   - Confidence: medium/high

6. Finding: DBN modelling gives limited interpretability compared with NB coefficients.
   - Why it matters: For Open Road Risk's public decision-support role, black-box gains should be weighed against explainability and governance concerns.
   - Evidence quote or page reference: Pages 9–10 report interpretable NB coefficients, while DBN sections report architecture and MAE/RMSE without feature importance or explanation.
   - Confidence: medium

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Local NB/GLM vs ML benchmark comparison | Gives a transparent baseline against a flexible model | Link-year crashes, AADT/exposure, length, road features | Six highway classes across Ontario, Colorado, Washington | High conceptually; your GLM/XGBoost setup already does this partly | Stage 2 / validation | low/medium | Focusing on count error instead of ranking/calibration usefulness |
| Temporally held-out model evaluation | Tests whether model trained on earlier years predicts later years | Multi-year link-year data | Ontario 2000–2006 train, 2007–2008 test; Colorado 1991–1996 train, 1997–1998 test | High; your data cover 2015–2024 | validation | medium | Same links in train and test may still overstate new-location generalisation |
| Pooled global model with facility/region indicators | Could test whether a single model across road classes performs acceptably or whether split models are needed | Road class, form of way, region, exposure, geometry/context features | 71,244 training observations across 6 highway classes | Medium/high computationally; your scale is much larger but XGBoost/HGB can handle pooled features | Stage 2 / validation | medium | Masking subgroup failure; rural/minor-road performance may degrade |
| Sequential retraining / adding new data diagnostic | Relevant to annual updates as new STATS19/AADF data arrive | Versioned annual datasets and repeatable validation | Sequential addition of Washington data after Ontario/Colorado | Medium; useful as documentation/diagnostic rather than production method | validation / documentation | medium | Updating may shift rankings and reduce reproducibility if not versioned |
| Minimum segment length sensitivity diagnostic | Tests whether very short OS links create unstable rates/residuals | Link length and collision/exposure outputs | Paper excludes very short segments below 0.16–0.2 km | High as a diagnostic; not necessarily as exclusion rule | validation / feature engineering | low | Excluding short links could remove junction approaches or urban micro-links |
| Compare combined exposure term vs separate exposure predictors | Tests whether fixed offset, learned exposure elasticity, or separate AADT/length terms are more stable | Estimated AADT, length, collision counts | Paper tests combined and separate exposure forms in NB | High as a baseline comparison | Stage 2 / validation | low/medium | Letting model learn exposure elasticity can confound risk with volume if not interpreted carefully |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Production DBN as main risk model | Paper does not show clear advantage over all subgroups, interpretability is weak, and validation lacks spatial/grouped/ranking tests | Need robust, explainable, scalable model governance and tuning | 71k training rows; Open Road Risk has ~21.7m link-year rows | Low/medium; computationally possible but not justified by this paper alone | Use XGBoost/GLM baseline plus optional neural diagnostic pilot | high |
| Direct use of exact lane/shoulder/median widths | These are from highway inventories; open UK coverage is limited | Reliable national lane width, shoulder width, median width | Highway agency datasets with detailed geometry | Low for full OS Open Roads network | Use form of way, road class, OSM lanes where coverage allows, and curvature/grade proxies | high |
| Applying paper's trained/global model to UK roads | Geography, reporting, road classification, inventory definitions, and exposure sources differ | Same feature definitions and crash reporting context | Ontario/Colorado/Washington highways | Low | Rebuild models using UK data; use paper only for method comparison | high |
| Treating temporal test MAE/RMSE as enough for deployment | Does not validate spatial generalisation, ranking, calibration, or high-risk tail usefulness | Spatial holdout, grouped link holdout, ranking metrics | Same-region test sets | Low as sole validation | Add spatial block, grouped-by-link, calibration, residual, and top-risk diagnostics | high |
| Removing all short segments below 0.16–0.2 km as a production rule | OS Open Roads links may be inherently short; junction areas may be important | Alternative segmentation strategy | Homogeneous highway segments | Low as direct rule | Use sensitivity analysis or aggregate short links in diagnostics | medium |

Important:

- The study scale is much smaller than Open Road Risk but still useful as a methodological comparison paper.
- The most transferable contribution is not deep learning itself; it is the disciplined comparison between local and global models under held-out predictive metrics.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Yes, partly. It reinforces the importance of AADT and segment length in SPF modelling, but it does not use the same explicit fixed exposure offset structure as Open Road Risk.
- Does it suggest better handling of AADT/AADF uncertainty? No. It uses observed/assigned traffic inventory data and removes Washington records with missing traffic data. It does not model count uncertainty or sparse AADT coverage.
- Does it suggest useful geometry or road-context features? Yes. It supports comparing curvature, lane/shoulder/median width, terrain, road type, access type, and rural/urban indicators where available. Several are already present or planned in Open Road Risk.
- Does it suggest better modelling of junctions? No. The Washington case explicitly removes intersection, interchange, ramp, and driveway crashes from the segment study scope.
- Does it suggest better treatment of severity? No. Severity is not separately modelled.
- Does it suggest better validation design? Partly. It supports temporal train/test validation and local-vs-global model comparison. It does not provide spatial or grouped validation, which remain important for your pipeline.
- Does it expose a weakness in my current approach? It raises two useful checks: first, whether the production XGBoost global ranking underperforms in specific facility families; second, whether very short OS links have unstable exposure/risk estimates and need sensitivity diagnostics.

## 15. Repo Actionability

1. Suggested repo action: Add a validation note comparing global pooled Stage 2 modelling with facility-family subgroup diagnostics.
   - Action type: documentation note / diagnostic
   - Relevant stage: Stage 2 / validation / documentation
   - Why the paper supports it: The paper's global DBN performs well overall but has subgroup exceptions, especially rural Washington classes.
   - Evidence quote or page reference: Page 14 states that WA-R2 and WA-RM were exceptions where local NB slightly outperformed global DBN; Table 8 gives subgroup MAE/RMSE.
   - Effort: low/medium
   - Risk if implemented badly: Overstating this as proof that global models are bad or good; the right action is subgroup testing.

2. Suggested repo action: Add a temporal holdout diagnostic, e.g. train on 2015–2021 and test on 2022–2024, alongside grouped/spatial validation.
   - Action type: diagnostic / baseline comparison
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: The paper uses earlier years for training and later years for testing in Ontario and Colorado.
   - Evidence quote or page reference: Page 6 describes 2000–2006 training and 2007–2008 testing for Highway 401, and 1991–1996 training and 1997–1998 testing for Colorado.
   - Effort: medium
   - Risk if implemented badly: Treating temporal holdout as sufficient despite repeated links and no spatial holdout.

3. Suggested repo action: Add a short-link sensitivity diagnostic for risk percentiles and GLM residuals by link-length bands.
   - Action type: diagnostic
   - Relevant stage: validation / feature engineering
   - Why the paper supports it: The paper applies minimum segment lengths and cites uncertainty/lower exposure issues for very short segments.
   - Evidence quote or page reference: Page 5 states the shortest Ontario homogeneous section was 0.2 km and that very short road segments may have higher uncertainty and lower exposure problems; page 6 removes Washington records shorter than 0.16 km.
   - Effort: low
   - Risk if implemented badly: Blindly excluding short OS links could bias urban/junction risk analysis.

4. Suggested repo action: Compare fixed exposure offset vs learned exposure elasticity as a documented baseline, not a production replacement.
   - Action type: baseline comparison
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: The NB benchmark tests combined exposure and separate AADT/length predictors and chooses based on test performance.
   - Evidence quote or page reference: Page 9 states exposure features were tested as `log(AADT*Length*365/10^6)` and separately as `log(AADT)` and `log(Length)`.
   - Effort: low/medium
   - Risk if implemented badly: Letting the model learn exposure response can blur the distinction between exposure and excess risk.

5. Suggested repo action: Document why deep neural models are not yet justified as production models, but could be a later benchmark if validation matures.
   - Action type: documentation note
   - Relevant stage: documentation / Stage 2
   - Why the paper supports it: DBN performance is broadly comparable and sometimes better than NB, but not consistently better across subgroups and lacks interpretability/ranking validation.
   - Evidence quote or page reference: Page 14 concludes DBN is at least comparable to NB, while also noting unresolved questions about robustness to network structure and size.
   - Effort: low
   - Risk if implemented badly: Sounding anti-ML rather than evidence-led; the point is governance and validation, not rejecting flexible models.

## 16. Query Tags

- safety-performance-function
- global-SPF
- deep-belief-network
- deep-learning
- negative-binomial
- exposure-feature
- AADT
- segment-length
- temporal-holdout
- MAE
- RMSE
- highway-segments
- local-vs-global-model
- facility-family
- subgroup-validation
- curvature
- terrain
- lane-width
- shoulder-width
- short-segment-sensitivity

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: Severity inclusion/exclusion; exact Washington calendar years and split method; whether repeated road segments appear across train/test in Washington; calibration quality; uncertainty intervals; ranking/hotspot performance; spatial autocorrelation; treatment of zero-heavy counts beyond NB/DBN modelling.
- Parts of the paper that need manual checking: Exact definitions of Washington highway classes and whether Table 3 duplicates rural multilane and urban multilane summary statistics due to a source/table issue; whether any supplementary material gives more detail on Washington years; implementation details of DBN tuning and normalization if reproducing the method.
- Any likely ambiguity or risk of misinterpretation: The term "global" should not be read as globally valid across all road networks. In this paper it means pooled across the included Ontario, Colorado, and Washington datasets. The reported MAE/RMSE values are useful predictive diagnostics, not proof of hotspot ranking quality or causal road-feature effects.
