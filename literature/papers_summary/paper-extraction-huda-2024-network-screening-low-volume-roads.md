# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: dot_78279_DS1.pdf
- Suggested Markdown filename: paper-extraction-huda-2024-network-screening-low-volume-roads.md
- AI tool used: ChatGPT
- Model name, if visible: not stated
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The PDF text was accessible across 13 pages. Some figure text was visible through rendered page images. The extraction relies on the uploaded paper only and does not assume access to the Open Road Risk repository code.

## 1. Citation

- Title: Network Screening on Low-Volume Roads Using Risk Factors
- Authors: Kazi Tahsin Huda; Ahmed Al-Kaisy
- Year: 2024
- DOI or URL, if present: https://doi.org/10.3390/futuretransp4010013
- Country / region studied: United States / Oregon
- Study setting: rural low-volume two-lane paved roads

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper develops simple regression models to estimate expected crashes on rural low-volume road segments for network screening, using classified roadway risk factors with and without traffic volume.
- Main purpose: network screening / safety performance support / hotspot candidate identification
- Evidence quote or page reference: Page 3 states that the objective was to develop “a practical and effective method for network screening on rural LVRs which requires a minimal amount of information and technical expertise for implementation by local agencies.”

## 3. Response Variable

- Target variable: Empirical Bayes expected number of crashes per year for each 0.05-mile roadway section.
- Collision type: all reported crashes / not separated by severity in the model description
- Severity handling: Crash severity is discussed in the background motivation for safety programmes, but the proposed models use total expected crashes and do not model fatal, serious, slight, or severity classes separately.
- Count, binary, rate, risk score, severity class, or other: Expected crash count; later converted to crash density for ranking.
- Time window used for outcomes: Crash data from 2004 to 2013.
- Evidence quote or page reference: Page 5 states that “the dependent variable was the expected crash numbers (from the HSM EB method).” Page 9 defines `Exp = EB expected number of crashes per year`. Page 4 states that crash data from 2004 to 2013 were collected for each 0.05-mile section.

## 4. Exposure Handling

- Exposure variable used, if any: AADT traffic volume.
- Traffic count source: Oregon Department of Transportation online databases.
- Whether exposure is modelled, observed, assumed, or ignored: Traffic volume is used as an observed or compiled explanatory variable in the first regression model. A second no-volume model is deliberately developed for cases where traffic data are unavailable.
- Treatment of missing or sparse traffic counts: The paper does not impute missing traffic counts. Instead, it provides a second model excluding AADT for agencies without traffic volume data.
- Whether offset terms, rates, denominators, or normalisation are used: No offset is used in the proposed OLS regression models. AADT and segment length enter the HSM safety performance function used to calculate the EB expected crash response, and AADT is also included as an explanatory variable in the first proposed regression model. Ranking uses crash density after summing section estimates and dividing by segment length.
- Evidence quote or page reference: Page 4 states that the HSM rural two-lane SPF uses “AADT and segment length” under base conditions. Page 6 states that two models were developed, one with “classified roadway factors and traffic exposure (AADT)” and one with “only classified roadway factors.” Page 11 Figure 5 shows the workflow: use the volume or no-volume equation, estimate EB expected crashes for 0.05-mile sections, then “sum section estimates for segments and divide by segment length to find crash density.”
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The general idea of comparing a volume and no-volume variant is transferable as a diagnostic for low-volume roads. The exact HSM/Oregon SPF calibration and the paper's AADT availability are less directly transferable. The proposed model does not match Open Road Risk's exposure-offset structure; it treats AADT as a predictor in a regression trained to reproduce EB expected crashes.

Important:

- The mathematical exposure-offset structure is not present in the proposed model.
- The paper's use of AADT in the HSM SPF and regression is partly transferable, but its Oregon-calibrated HSM setup is not directly reusable in a UK OS Open Roads / AADF pipeline.

## 5. Spatial Unit of Analysis

- Unit: roadway segment / roadway section
- Segment length or segmentation rule: 0.05-mile roadway sections were used as analysis units.
- How crashes are assigned to the network: The paper states that crash data were collected for each 0.05-mile section, but does not provide detailed geocoding or snapping procedure.
- Treatment of junctions/intersections: Intersections are excluded. The paper focuses solely on roadway segments.
- Spatial aggregation risks: The fixed 0.05-mile segmentation captures changes in roadside and roadway characteristics more precisely than long segments, but may not align with OS Open Roads link geometry. Excluding intersections limits applicability to junction risk.
- Evidence quote or page reference: Page 3 states that data were collected for roadway sections “0.05 miles in length (analysis units).” Page 4 states that the research “focused solely on roadway segments” and that intersections would need a similar approach using different variables.
- Relevance to OS Open Roads link-based pipeline: Medium. The segment-level approach is conceptually compatible with link-level screening, but Open Road Risk uses OS Open Roads links rather than fixed 0.05-mile sections. A direct transfer would require either splitting links into fixed lengths or aggregating paper-style features back to OS links.

## 6. Temporal Unit of Analysis

- Years covered: Crash data from 2004 to 2013.
- Temporal resolution: Annual expected crashes; the modelling equations define expected crashes per year.
- Whether seasonality or time-of-day is modelled: No.
- Whether before-after or panel structure is used: No before-after design is used. No explicit panel model is described.
- Evidence quote or page reference: Page 4 states that crash data from 2004 to 2013 were collected. Page 9 defines `Exp` as “EB expected number of crashes per year.”
- Relevance to WebTRIS-style time profiles: Low. The paper does not model time of day, peak/off-peak exposure, or within-day traffic profiles.

## 7. Engineered Features

List the most important engineered features, especially those I could recreate.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Lane width category | ODOT databases / video logs | Classified into `< 11 ft` and `>= 11 ft`; CART was trivial, so descriptive statistics and engineering judgement were used | Narrower lanes are treated as higher-risk conditions | Medium; OSM lanes/width coverage may be sparse, so mostly candidate diagnostic / external feature if available |
| Shoulder width category | ODOT data | CART split at about 1.8 ft, rounded to 2 ft: `< 2 ft` vs `>= 2 ft` | Narrow shoulders may reduce recovery space and correlate with expected crashes | Low to medium; not usually complete in open UK data unless derived from other sources |
| Degree of horizontal curvature category | Road geometry | CART classes: straight; mild; moderate; sharp, with thresholds around 8.9 degrees and 28 degrees | Curvature is a plausible road-geometry risk factor | High; curvature is already a candidate / present direction in Open Road Risk, so compare implementation and thresholds rather than simply add |
| Vertical grade category | Road geometry / elevation | Classified as `< 4%` vs `>= 4%` using observed crash-per-mile trend rather than CART | Steeper grades were associated with higher observed crashes per mile in this case study | High; OS Terrain 50 can support grade features, so this supports validation/comparison of existing candidate grade approach |
| Driveway density | Maps / aerial photography | Exact number of driveways per mile | Access points may increase conflict opportunities | Medium to low at national scale; manual collection is not scalable, but proxy features may be possible using address/access-point data if available |
| Side slope category | ODOT video logs | Already collected categorically as steep, moderate, flat | Roadside severity/recovery condition proxy | Low; likely requires inspection/video/manual/commercial inventory |
| Fixed objects category | ODOT video logs | Already collected categorically as many, some, few | Roadside hazard proxy | Low; likely requires inspection/video/manual/commercial inventory |
| AADT / volume | ODOT online databases | Exact traffic volume used in volume model; excluded from no-volume model | Exposure and traffic demand correlate with expected crashes | Medium; AADF/WebTRIS support exposure modelling, but sparse counts and UK extrapolation differ from paper context |

Only features actually used in the paper are included above.

## 8. Model Architecture

- Algorithms/models used: Empirical Bayes expected crashes from the HSM method; CART for classifying selected variables; multivariate ordinary least squares linear regression for the proposed screening models.
- Baseline model: The paper motivates against simple crash history/rates and uses HSM EB expected crashes as the target basis. It does not present a formal baseline model comparison table against historical crash frequency, crash rate, or HSM EB ranking.
- Final/preferred model: Two proposed OLS log-linear equations: one with AADT and one without AADT.
- Loss function or likelihood, if stated: Not stated for OLS beyond use of linear regression. No Poisson or negative-binomial likelihood is used for the proposed final models.
- Offset/exposure term, if used: No offset in proposed OLS models. AADT appears as an explanatory variable in the volume model and is part of the HSM SPF used to construct EB expected crash values.
- Spatial autocorrelation handling: Not stated.
- Temporal dependence handling: Not stated.
- Interpretability method: Simple coefficients from log-linear regression; CART-derived cut-offs for classified risk factors.
- Evidence quote or page reference: Page 5 gives the EB formula `Nexpected = w × Npredicted + (1 − w) × Nobserved`. Page 5 states that CART was used to set cut-off values for classified variables. Page 9 states that “Multivariate ordinary least squares linear regression analysis was used” and provides Equation 4; page 10 provides Equation 5.

## 9. Reported Metrics / Quantitative Results

Extract the main quantitative results reported in the paper.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model fit | Adjusted R-squared | 0.915 | Model with AADT | Explains most variation in EB expected crash target within this Oregon dataset | Page 10, Table 2 |
| Model fit | Adjusted R-squared | 0.905 | No-volume model | Similar in-sample fit despite excluding AADT | Page 10, Table 3 |
| Coefficients | Lane width | -0.88; p < 2e-6 | Model with AADT | Wider lane category associated with lower log expected crashes, within this model coding | Page 10, Table 2 |
| Coefficients | Shoulder width | -0.34; p < 2e-6 | Model with AADT | Wider shoulder category associated with lower log expected crashes | Page 10, Table 2 |
| Coefficients | Driveway density | 0.016; p < 2e-6 | Model with AADT | Higher driveway density associated with higher log expected crashes | Page 10, Table 2 |
| Coefficients | Volume / AADT | 0.001; p < 2e-6 | Model with AADT | Higher AADT associated with higher log expected crashes | Page 10, Table 2 |
| Coefficients | Degree of curvature | 0.24; p < 2e-6 | Model with AADT | Sharper curvature category associated with higher log expected crashes | Page 10, Table 2 |
| Coefficients | Side slope | -0.31; p < 2e-6 | Model with AADT | Flatter/safer side-slope coding associated with lower log expected crashes | Page 10, Table 2 |
| Coefficients | Fixed objects | -0.21; p < 2e-6 | Model with AADT | Fewer fixed objects associated with lower log expected crashes | Page 10, Table 2 |
| Validation aggregate | Actual expected crash mean / total | 0.087 / 1213 | Training data | Reference value for training comparison | Page 12, Table 4 |
| Validation aggregate | Model estimate mean / total | 0.085 / 1192 | Training data, with AADT | Close aggregate match to EB expected crash target | Page 12, Table 4 |
| Validation aggregate | No-volume estimate mean / total | 0.076 / 1057 | Training data, no AADT | Lower aggregate estimate than target | Page 12, Table 4 |
| Validation aggregate | Actual expected crash mean / total | 0.084 / 294 | Random testing data | Reference value for testing comparison | Page 12, Table 4 |
| Validation aggregate | Model estimate mean / total | 0.086 / 301 | Random testing data, with AADT | Close aggregate match to EB expected crash target | Page 12, Table 4 |
| Validation aggregate | No-volume estimate mean / total | 0.077 / 268 | Random testing data, no AADT | Lower aggregate estimate than target | Page 12, Table 4 |
| Validation error | MBE | -0.0015 training; 0.0018 testing | Model with AADT | Mean bias close to zero | Page 12, Table 4 |
| Validation error | MBE | -0.011 training; -0.007 testing | No-volume model | Small negative mean bias | Page 12, Table 4 |
| Validation error | RMSE | 0.18 training; 0.19 testing | Model with AADT | Error against EB expected crash target | Page 12, Table 4 |
| Validation error | RMSE | 0.17 training; 0.18 testing | No-volume model | Error against EB expected crash target | Page 12, Table 4 |
| CART split | Horizontal curvature terminal means | 0.067, 0.14, 0.23 shown in figure; text also states 0.86 for sharp-curve group | Curvature CART | Higher curvature groups have higher expected crash values, but text/figure appear inconsistent for the sharp group value | Page 8, Figure 1 and page 7 text |
| CART split | Shoulder width terminal means | 0.068 vs 0.099 | Shoulder-width CART | Narrower shoulder group has higher expected crash value | Page 8, Figure 2 |
| Descriptive comparison | Observed crashes per mile by lane width | 1.55 for `< 11 ft`; 1.49 for `>= 11 ft` | Lane width categories | Narrower lane category has slightly higher observed crashes per mile | Page 9, Figure 3 |
| Descriptive comparison | Observed crashes per mile by grade | 1.50 for `< 4%`; 1.55 for `>= 4%` | Grade categories | Steeper grade category has slightly higher observed crashes per mile | Page 9, Figure 4 |

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? The R-squared values are model-fit metrics on the fitted regression. The validation metrics use a random 80/20 train/test split from the same Oregon dataset. There is no spatial holdout, temporal holdout, grouped holdout, cross-validation, or external validation reported.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. The adjusted R-squared values should be treated as in-sample model-fit diagnostics. The training MBE/RMSE values are in-sample diagnostics. The testing MBE/RMSE values are random holdout diagnostics against the EB expected crash target, not external validation of future observed crashes.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They mainly test fit and aggregate error against the EB expected crash target. They do not directly test future crash prediction, external generalisation, spatial transfer, or hotspot/ranking usefulness.
- Are any metrics likely to be optimistic for real-world deployment? Yes. The random split from the same network may be optimistic for applying the model to different regions or to a UK open-data pipeline. Also, the target is EB expected crashes partly derived from observed crashes and an HSM SPF, not independently observed future crashes.
- Which metric, if any, is most relevant to Open Road Risk? The random test RMSE/MBE and aggregate mean/total comparison are the most relevant, but only as examples of validating a simplified surrogate model against a derived risk target. They are less relevant than spatial or grouped validation would be for Open Road Risk.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The paper motivates the method by noting sporadic crashes on low-volume roads. It handles sparse crash histories by using EB expected crashes as the response variable and by screening using risk factors rather than raw crash counts alone.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: The proposed final models use OLS regression on log EB expected crashes. The EB target uses an HSM SPF and observed crashes. Poisson and negative binomial models are discussed in background literature but are not the proposed final model. No zero-inflated model is used.
- Whether high-risk locations are evaluated separately: Not stated. The method ranks priority sites by crash density, but no separate high-risk subgroup validation is reported.
- Evidence quote or page reference: Page 1 states that conventional hotspot methods may be unsuitable because crashes on low-volume roads are sporadic. Page 4 states that EB expected crashes were selected as the basis for screening. Page 11 Figure 5 shows ranking using crash density.
- Practical relevance to my sparse collision link-year dataset: Medium. The paper supports the general concern that low event counts make raw crash-frequency screening unstable. Its solution is less directly transferable because Open Road Risk already models link-year counts with an exposure offset and larger-scale data.

## 11. Validation Strategy

- Train/test split method: Random 80/20 split. About 680 miles were used for training and about 170 miles for testing.
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Not stated
- Metrics: Mean bias error, RMSE, mean actual/predicted expected crashes, and total actual/predicted expected crashes. Adjusted R-squared is also reported for fitted models.
- External validation: No.
- Leakage or generalisation risks: The random split is weaker than spatial, temporal, or grouped validation. The target is EB expected crashes, which combines observed crashes and HSM predictions, so the proposed regression is learning to reproduce a derived EB score rather than directly validating future crash performance. This is not necessarily classic data leakage, but it limits claims about external predictive generalisation.
- Evidence quote or page reference: Page 9 states that the data were split randomly into 80% training and 20% testing. Page 11 states that the testing dataset contained 20% of the original dataset and was selected randomly. Page 12 reports Table 4 validation metrics.
- What I should copy or avoid: Copy the idea of testing simplified models against a clear target and reporting aggregate bias/RMSE. Avoid relying on random split alone for production claims; Open Road Risk should continue preferring grouped and spatial validation where possible.

## 12. Key Findings Relevant to My Project

Give 3–6 findings that are directly useful for my road-risk pipeline.

1. Finding: For low-volume rural roads, the paper argues that raw crash frequency/rate screening is unstable because crashes are sparse and scattered.
   - Why it matters: This supports Open Road Risk's choice to avoid raw crash counts alone and to use exposure/context-adjusted screening.
   - Evidence quote or page reference: Page 1 states that crashes on low-volume roads are “scattered sporadically” and that crash-frequency screening may not rank sites consistently.
   - Confidence: high

2. Finding: AADT can be included in a simplified screening model, but the paper also tests a no-volume alternative for agencies without traffic counts.
   - Why it matters: This supports documenting sensitivity to exposure availability and comparing volume vs no-volume diagnostics, especially for sparse traffic-count areas.
   - Evidence quote or page reference: Page 6 states that one model used classified roadway factors and AADT, while the second used only classified roadway factors.
   - Confidence: high

3. Finding: Curvature and grade are operationalised as categorical geometric risk factors using simple thresholds.
   - Why it matters: This supports using curvature and grade as interpretable diagnostics or feature checks, not necessarily as identical production thresholds.
   - Evidence quote or page reference: Pages 7–9 describe CART splits for horizontal curvature and a 4% threshold for vertical grade.
   - Confidence: medium

4. Finding: Roadside features such as shoulder width, side slope, and fixed objects are important in the paper's screening model but depend on data that may not be available in open UK data.
   - Why it matters: This exposes a limitation of Open Road Risk if it lacks reliable roadside hazard and shoulder data.
   - Evidence quote or page reference: Page 6 Table 1 lists shoulder width, side slope, and fixed objects as explanatory variables; page 4 says video logs were used for driveway density, side-slope rating, and fixed-object rating.
   - Confidence: high

5. Finding: The paper's strong R-squared values should not be read as external predictive validation.
   - Why it matters: This is a useful caution for Open Road Risk reporting: distinguish model fit, random holdout against derived targets, and true spatial/temporal generalisation.
   - Evidence quote or page reference: Page 10 reports adjusted R-squared above 0.90; page 11 states that the testing data were randomly selected from the original dataset.
   - Confidence: high

6. Finding: Intersections are explicitly out of scope.
   - Why it matters: The paper does not provide direct support for junction modelling in Open Road Risk, although it notes that a similar approach could be applied with different variables.
   - Evidence quote or page reference: Page 4 states that the research focused solely on roadway segments and that intersections would need a similar approach using different variables.
   - Confidence: high

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Volume vs no-volume sensitivity comparison | Tests how much risk ranking changes when exposure is unavailable or uncertain | Estimated AADT plus all non-AADT features | Around 850 miles of Oregon LVRs; 0.05-mile units | High as a diagnostic; not a replacement for exposure-offset model | validation / documentation / Stage 2 diagnostic | Low to medium | Could be misread as evidence to ignore exposure rather than as a sensitivity check |
| Curvature threshold diagnostic | Paper gives interpretable curvature bands associated with higher expected crashes in this case study | Link geometry and curvature calculation | 0.05-mile rural segments | Medium to high; Open Road Risk scale is much larger but curvature is computable | feature engineering / validation / documentation | Medium | Thresholds may not transfer from Oregon LVRs to UK mixed roads |
| Grade threshold diagnostic | 4% grade threshold is simple and compatible with DEM-derived grade checks | OS Terrain 50 or other DEM; link geometry | 0.05-mile rural segments | Medium; DEM-derived link grade is scalable but bridge/tunnel issues remain | future feature / validation / documentation | Medium | DEM sampling can be wrong for bridges/tunnels; threshold may not transfer |
| EB/shrinkage framing for sparse crashes | Supports shrinkage/expected-crash thinking for sparse low-volume settings | Observed crashes, SPF or baseline expected-crash model, exposure/context features | Around 850 miles; 2004–2013 crashes | Conceptually useful but direct HSM EB formula may not fit current pipeline | Stage 2 / validation / documentation | Medium | Learning from a derived EB target can hide assumptions in the SPF |
| Classified-variable robustness check | Tests whether coarse versions of features retain ranking signal | Existing continuous features recoded into simple bins | 0.05-mile rural segments | High as a diagnostic; scalable | validation / documentation | Low | Coarse bins may reduce useful signal or create arbitrary cut-offs |
| Random holdout aggregate bias/RMSE reporting | Useful as a supplementary diagnostic for model bias against a target | Model predictions and target values | 80/20 random split, about 680/170 miles | Medium; should be secondary to grouped/spatial validation | validation | Low | Random holdout may overstate generalisation |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Direct use of Oregon-calibrated equations | Coefficients and categories are region-specific and built for Oregon rural LVRs | Oregon-specific roadway data, HSM calibration, local crash regime | Around 850 miles of Oregon state-owned LVRs | Low | Refit locally using UK data if the target and features are suitable | High |
| Manual/video-log roadside feature collection at national scale | Side slope and fixed-object categories came from video logs/manual-like extraction | Consistent UK roadside inventory or scalable image-derived features | 0.05-mile rural sections | Low for 2.1M links without automated/commercial data | Use proxies, pilots, or selective validation areas | High |
| Fixed 0.05-mile segmentation as a full pipeline replacement | Open Road Risk currently uses OS Open Roads links; full resegmentation would be disruptive | Rebuilt segmentation, crash assignment, feature aggregation | 0.05-mile sections | Medium to low as production replacement; possible as pilot | Pilot on selected areas or aggregate fixed-length features to links | Medium |
| Excluding intersections from the safety model | Open Road Risk likely needs junction/context handling across a mixed network | Junction-specific variables and assignment rules | Rural two-lane segments only | Low as a general road-risk model | Build separate junction diagnostics or facility-family split | High |
| Treating high R-squared against EB expected crashes as production validation | The target is derived from EB/HSM and observed crashes, not future external outcomes | Independent future/spatial validation | Same-network random split | Low | Use spatial/grouped/temporal validation and ranking diagnostics | High |

Important:

- Several techniques are conceptually transferable but should be treated as diagnostics or pilots rather than direct production changes.
- The study scale is much smaller and more homogeneous than Open Road Risk: around 850 miles of rural low-volume, two-lane, paved Oregon roads with posted speed limit 55 mph, split into 0.05-mile sections.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Partly. It supports the need to move beyond raw crash history on low-volume roads and uses AADT in the HSM EB target and one proposed model. It does not directly support Open Road Risk's specific exposure offset formulation.
- Does it suggest better handling of AADT/AADF uncertainty? It suggests a useful diagnostic: compare a volume model with a no-volume model to understand dependence on traffic data. It does not propose uncertainty propagation or traffic-count imputation.
- Does it suggest useful geometry or road-context features? Yes. It supports curvature, grade, lane width, shoulder width, driveway density, side slope, and fixed objects as segment-level risk factors in this Oregon low-volume-road case study. For Open Road Risk, curvature and grade are most realistically transferable.
- Does it suggest better modelling of junctions? No direct method. Intersections are explicitly excluded, though the authors state a similar approach could be applied with different variables.
- Does it suggest better treatment of severity? No. The proposed model uses total expected crashes and does not separate severity.
- Does it suggest better validation design? Indirectly. It reports a random 80/20 validation with MBE/RMSE, but for Open Road Risk this mainly highlights the need to go beyond random holdout to grouped/spatial/temporal validation.
- Does it expose a weakness in my current approach? It exposes potential weakness around missing roadside inventory features: shoulder width, side slope, fixed objects, and driveway/access density may matter but may not be well captured in open UK data. It also reinforces the need to be careful with low-volume, sparse-collision rankings.

## 15. Repo Actionability

Give up to 5 concrete implications for my repo.

1. Suggested repo action: Add a documentation note distinguishing raw crash counts, exposure-adjusted risk, EB/shrinkage logic, and simplified risk-factor screening for sparse low-volume roads.
   - Action type: documentation note
   - Relevant stage: documentation / Stage 2
   - Why the paper supports it: The paper explicitly argues that raw crash-frequency/rate screening can be unsuitable for low-volume roads and motivates EB/risk-factor screening.
   - Evidence quote or page reference: Pages 1–3 discuss sporadic crashes on LVRs and the motivation for a practical risk-factor-based method.
   - Effort: low
   - Risk if implemented badly: Could overstate the paper as validating Open Road Risk rather than supporting a general rationale.

2. Suggested repo action: Add a volume-sensitivity diagnostic comparing Stage 2 rankings with full exposure, reduced/no AADT features, or binned AADT variants in selected low-volume subsets.
   - Action type: diagnostic
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: The paper explicitly compares a model with AADT against a no-volume model for agencies lacking traffic data.
   - Evidence quote or page reference: Page 6 states that two models were developed, one with traffic exposure and one without; pages 10–12 compare their metrics.
   - Effort: medium
   - Risk if implemented badly: Could be misinterpreted as evidence that exposure is unnecessary across all road types.

3. Suggested repo action: Use the paper as support for a small curvature/grade threshold comparison against current continuous feature engineering.
   - Action type: small pilot / baseline comparison
   - Relevant stage: feature engineering / validation
   - Why the paper supports it: The paper classifies curvature using CART and grade using a 4% threshold, and uses both in screening models.
   - Evidence quote or page reference: Pages 7–9 describe curvature classes and grade classification.
   - Effort: low to medium
   - Risk if implemented badly: Oregon thresholds may be treated as universal; they should be tested as diagnostics only.

4. Suggested repo action: Add a documentation gap note for roadside inventory variables that are likely relevant but weakly covered in open UK data.
   - Action type: documentation note
   - Relevant stage: documentation / future feature
   - Why the paper supports it: Side slope and fixed objects are included as risk factors and were collected from ODOT video logs.
   - Evidence quote or page reference: Page 4 describes video-log collection for side-slope and fixed-object ratings; page 6 Table 1 lists these variables.
   - Effort: low
   - Risk if implemented badly: Could imply these missing features invalidate the model rather than mark an uncertainty/gap.

5. Suggested repo action: Add a validation note that random holdout metrics are weaker than grouped/spatial/temporal validation, especially for safety-performance claims.
   - Action type: documentation note / validation diagnostic
   - Relevant stage: validation / documentation
   - Why the paper supports it: The paper uses random 80/20 validation and reports favourable errors, but does not test spatial or temporal transfer.
   - Evidence quote or page reference: Page 9 and page 11 state the random 80/20 train/test split; page 12 reports validation metrics.
   - Effort: low
   - Risk if implemented badly: Could sound like a criticism of the paper rather than a scope limitation relevant to Open Road Risk.

## 16. Query Tags

- low-volume-roads
- rural-roads
- network-screening
- Empirical-Bayes
- HSM-SPF
- AADT
- no-volume-model
- exposure-sensitivity
- risk-factors
- CART-thresholds
- curvature
- vertical-grade
- shoulder-width
- lane-width
- driveway-density
- roadside-hazards
- fixed-objects
- random-holdout
- zero-heavy-counts
- Oregon

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: Detailed crash assignment/geocoding method; exact crash severity inclusion rules; whether property-damage-only crashes are included; spatial autocorrelation treatment; temporal validation; external validation; detailed handling of missing traffic volume; whether intersections near segment endpoints are excluded or assigned; uncertainty intervals for predictions.
- Parts of the paper that need manual checking: The curvature CART result appears internally inconsistent: page 7 text states the sharp-curve group has average expected crashes of 0.86, while Figure 1 on page 8 appears to show 0.23 for the sharpest group. Check the original PDF figure/table before using that value.
- Any likely ambiguity or risk of misinterpretation: The high adjusted R-squared values describe fit to an EB expected-crash target, not necessarily independent future crash prediction. The no-volume model result should not be interpreted as proof that exposure is unimportant outside this low-volume Oregon setting.
