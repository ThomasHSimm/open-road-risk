# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: dot_78279_DS1.pdf
- Suggested Markdown filename: final.md
- AI tool used: ChatGPT
- Model name, if visible: GPT-5.5 Thinking
- Model version, if visible: not stated
- Interface used: web chat
- Input type: original PDF plus two Markdown extractions
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: The uploaded PDF text was accessible across 13 pages. Page-image checks were used for figures on pages 8, 9, and 11 where the parsed text or prior extractions were ambiguous.

## 1. Citation

- Title: Network Screening on Low-Volume Roads Using Risk Factors
- Authors: Kazi Tahsin Huda; Ahmed Al-Kaisy
- Year: 2024
- DOI or URL, if present: https://doi.org/10.3390/futuretransp4010013
- Country / region studied: United States / Oregon
- Study setting: State-owned rural low-volume two-lane paved roads in Oregon; all segments had posted speed limit 55 mph. Low-volume roads are defined as rural roads with AADT ≤ 1000 vehicles per day, although Table 1 reports a maximum volume of 2500 in the study variable summary.

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper develops regression models for network screening on rural low-volume roads by predicting Empirical Bayes expected crash counts from classified roadway risk factors, with and without traffic volume.
- Main purpose: Network screening / hotspot candidate identification / safety-performance support.
- Evidence quote or page reference: Page 3 states that the objective was to develop “a practical and effective method for network screening on rural LVRs which requires a minimal amount of information and technical expertise.”

## 3. Response Variable

- Target variable: Empirical Bayes expected number of total crashes per year for each 0.05-mile roadway section.
- Collision type: Total reported crashes; the paper does not clearly state whether property-damage-only crashes are included or excluded.
- Severity handling: Severity is not modelled separately. The response is total expected crashes.
- Count, binary, rate, risk score, severity class, or other: Continuous EB-smoothed expected crash count. The implementation workflow later converts section estimates to crash density for ranking.
- Time window used for outcomes: Crash data from 2004 to 2013.
- Evidence quote or page reference: Page 4 states that crash data from 2004 to 2013 were collected for each 0.05-mile section. Page 4 states that “the EB expected number of total crashes was selected as a basis for network screening.” Page 5 states that the dependent variable was the expected crash number from the HSM EB method. Page 9 defines `Exp = EB expected number of crashes per year`.

Important modelling note:

- The response is not raw observed crash count.
- It is a derived EB expected-crash quantity blending HSM-predicted crashes and observed crashes.
- Reported R² values therefore measure fit to a smoothed derived target, not direct prediction of raw future crashes.

## 4. Exposure Handling

- Exposure variable used, if any: AADT.
- Traffic count source: Oregon Department of Transportation online databases. The paper says AADT is usually measured or estimated by highway agencies; it does not specify which records in the study sample were directly counted versus estimated.
- Whether exposure is modelled, observed, assumed, or ignored: AADT is used in three different ways:
  - as an input to the HSM SPF used in the EB expected-crash response,
  - as a covariate in the first proposed regression model,
  - deliberately excluded from the second no-volume regression model.
- Treatment of missing or sparse traffic counts: The paper does not impute missing traffic counts. It proposes a no-volume model for situations where local agencies lack traffic-volume data.
- Whether offset terms, rates, denominators, or normalisation are used: No exposure offset is used in the proposed OLS models. AADT enters as a linear covariate in Model 1. Section estimates are later summed and divided by segment length to create crash density for ranking.
- Evidence quote or page reference: Page 4 states that the HSM SPF uses AADT and segment length under base conditions. Page 6 states that the first model uses classified roadway factors and AADT, while the second uses only classified roadway factors. Page 9 gives Equation 4 with AADT as `V`. Page 11 Figure 5 shows the workflow: estimate EB expected crashes for 0.05-mile sections, sum section estimates for segments, and divide by segment length to find crash density.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The volume/no-volume comparison is useful as a diagnostic for low-volume roads. The exact Oregon/HSM calibration is not directly transferable. The proposed model does not match Open Road Risk's exposure-offset structure.

Important:

- The paper does not support replacing an exposure offset with AADT-as-covariate in Open Road Risk.
- The no-volume result is specific to rural low-volume roads and should not be generalised to higher-volume roads.

## 5. Spatial Unit of Analysis

- Unit: Roadway section / road segment.
- Segment length or segmentation rule: Fixed 0.05-mile sections.
- How crashes are assigned to the network: The paper says crash data were collected for each 0.05-mile section, but does not describe the geocoding or snapping procedure in detail.
- Treatment of junctions/intersections: Intersections are excluded. The paper focuses solely on roadway segments.
- Spatial aggregation risks: Fixed 0.05-mile sections do not directly match OS Open Roads link geometry. Random splitting of short adjacent sections may also allow spatially similar sections from the same road corridor into both train and test sets.
- Evidence quote or page reference: Page 3 says data were collected for roadway sections 0.05 miles in length. Page 4 says the research “focused solely on roadway segments” and that intersections would need a similar approach using different variables.
- Relevance to OS Open Roads link-based pipeline: Medium. The unit is closer to link-scale screening than large corridor studies, but direct transfer would require either fixed-length segmentation or careful aggregation to/from OS Open Roads links.

## 6. Temporal Unit of Analysis

- Years covered: 2004–2013.
- Temporal resolution: EB expected crashes per year.
- Whether seasonality or time-of-day is modelled: No.
- Whether before-after or panel structure is used: No before-after design and no explicit panel model. Crashes are aggregated across the study period and expressed as annual EB expected crashes.
- Evidence quote or page reference: Page 4 states that 2004–2013 crash data were collected. Page 9 defines expected crashes per year.
- Relevance to WebTRIS-style time profiles: Low. The paper does not model time of day, peak/off-peak traffic, or within-day exposure profiles.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Lane width | ODOT database | Binary: `< 11 ft` vs `>= 11 ft`; CART was uninformative, so descriptive statistics and engineering judgement were used | Narrower lane category had higher observed crashes per mile | Low to medium; lane/width coverage in OSM is uneven |
| Shoulder width | ODOT database | CART split at 1.8 ft, rounded to `< 2 ft` vs `>= 2 ft` in Table 1 | Narrow shoulder group had higher EB expected crashes | Low; shoulder width is not reliably available in current open UK data |
| Degree of horizontal curvature | ODOT / road geometry | CART categories: straight, mild, moderate, sharp using thresholds around 8.9° and 28° | Sharper curvature groups had higher EB expected crashes | High as a diagnostic/candidate feature; thresholds should be recalibrated |
| Grade | ODOT / road geometry | CART was uninformative; descriptive crash-rate plot used `< 4%` vs `>= 4%` | Steeper grade category had higher observed crashes per mile | Medium to high as a diagnostic using OS Terrain 50; but note grade is not in final regression equations |
| Driveway density | ODOT video logs / maps / aerial imagery | Exact driveways per mile | Access points may increase conflict opportunities | Low to medium; possible proxy/pilot only unless scalable access-point data are found |
| Side slope | ODOT video logs | Pre-classified as steep, moderate, flat | Roadside recovery / run-off-road context | Low; likely requires inventory/video/audit data |
| Fixed objects | ODOT video logs | Pre-classified as many, some, few | Roadside hazard proxy | Low; likely requires inventory/video/audit data |
| AADT / volume | ODOT databases | Exact value used in Model 1; excluded from Model 2 | Traffic exposure / demand | Medium; Open Road Risk estimates AADT, but UK sparse-count uncertainty differs |

Important correction:

- Grade appears in Table 1 and Figures 4, but it is not included in Equation 4, Equation 5, Table 2, or Table 3. Treat grade as a discussed/classified risk factor, not as a final regression predictor in the proposed equations.

## 8. Model Architecture

- Algorithms/models used: HSM Empirical Bayes expected crashes; CART for classifying selected variables; multivariate OLS regression on log-transformed EB expected crashes.
- Baseline model: No formal baseline comparison table against raw crash frequency, raw crash rate, or HSM EB ranking is provided. The paper motivates the use of EB over simpler screening approaches through background evidence.
- Final/preferred model: Two OLS log-linear equations:
  - Model 1 with AADT,
  - Model 2 without AADT.
- Loss function or likelihood, if stated: OLS. No Poisson, negative-binomial, zero-inflated, or hurdle likelihood is used for the proposed final models.
- Offset/exposure term, if used: No offset in the proposed OLS models. AADT is a covariate in Model 1.
- Spatial autocorrelation handling: Not stated.
- Temporal dependence handling: Not stated.
- Interpretability method: Coefficient signs/magnitudes, classified risk factors, CART-derived thresholds, and simple equations.
- Evidence quote or page reference: Page 5 gives the EB equation. Page 5 explains CART classification. Page 9 states that multivariate ordinary least squares linear regression was used. Pages 9–10 provide Equations 4 and 5 and Tables 2 and 3.

Important modelling note:

- The proposed OLS equations predict a derived EB expected-crash target, not raw crash counts.
- The modelling structure is therefore not directly comparable with Open Road Risk's Stage 2 Poisson GLM with exposure offset or XGBoost count/ranking model.

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model fit | Adjusted R² | 0.915 | Model 1 with AADT | High in-sample fit to log EB expected-crash target | Page 10, Table 2 |
| Model fit | Adjusted R² | 0.905 / 0.9057 | Model 2 without AADT | Similar in-sample fit after excluding AADT | Page 10, Table 3 and surrounding text |
| Coefficient | Lane width | -0.88; p < 2e-6 | Model 1 | Wider lane coding associated with lower log expected crashes | Page 10, Table 2 |
| Coefficient | Shoulder width | -0.34; p < 2e-6 | Model 1 | Wider shoulder coding associated with lower log expected crashes | Page 10, Table 2 |
| Coefficient | Driveway density | 0.016; p < 2e-6 | Model 1 | Higher driveway density associated with higher log expected crashes | Page 10, Table 2 |
| Coefficient | Volume / AADT | 0.001; p < 2e-6 | Model 1 | Higher AADT associated with higher log expected crashes | Page 10, Table 2 |
| Coefficient | Degree of curvature | 0.24; p < 2e-6 | Model 1 | Sharper curvature coding associated with higher log expected crashes | Page 10, Table 2 |
| Coefficient | Side slope | -0.31; p < 2e-6 | Model 1 | Safer/flatter coding associated with lower log expected crashes | Page 10, Table 2 |
| Coefficient | Fixed objects | -0.21; p < 2e-6 | Model 1 | Fewer fixed objects associated with lower log expected crashes | Page 10, Table 2 |
| Coefficient | Lane width | -0.53; p < 2e-6 | No-volume model | Wider lane coding associated with lower log expected crashes | Page 10, Table 3 |
| Coefficient | Shoulder width | -0.46; p < 2e-6 | No-volume model | Wider shoulder coding associated with lower log expected crashes | Page 10, Table 3 |
| Coefficient | Driveway density | 0.02; p < 2e-6 | No-volume model | Higher driveway density associated with higher log expected crashes | Page 10, Table 3 |
| Coefficient | Degree of curvature | 0.27; p < 2e-6 | No-volume model | Sharper curvature coding associated with higher log expected crashes | Page 10, Table 3 |
| Coefficient | Side slope | -0.28; p < 2e-6 | No-volume model | Safer/flatter coding associated with lower log expected crashes | Page 10, Table 3 |
| Coefficient | Fixed objects | -0.25; p < 2e-6 | No-volume model | Fewer fixed objects associated with lower log expected crashes | Page 10, Table 3 |
| CART split | Curvature terminal means | 0.067, 0.14, 0.23 in Figure 1; text states 0.86 for the sharp group | Curvature CART | Direction is higher EB expected crashes for sharper curvature; exact sharp-group value is internally inconsistent between figure and text | Pages 7–8, Figure 1 |
| CART split | Shoulder-width terminal means | 0.068 vs 0.099 | Shoulder-width CART | Narrow shoulder group had higher EB expected crashes | Page 8, Figure 2 |
| Descriptive comparison | Observed crashes per mile by lane width | 1.55 for `< 11 ft`; 1.49 for `>= 11 ft` | Lane width classes | Narrower lanes had slightly higher observed crashes per mile | Page 9, Figure 3 |
| Descriptive comparison | Observed crashes per mile by grade | 1.50 for `< 4%`; 1.55 for `>= 4%` | Grade classes | Steeper grades had slightly higher observed crashes per mile | Page 9, Figure 4 |
| Validation aggregate | Actual expected crash mean / total | 0.087 / 1213 | Training data | Reference EB target aggregate | Page 12, Table 4 |
| Validation aggregate | Model estimate mean / total | 0.085 / 1192 | Training data, Model 1 | Close aggregate match to EB target | Page 12, Table 4 |
| Validation aggregate | No-volume model estimate mean / total | 0.076 / 1057 | Training data, Model 2 | Lower aggregate estimate than EB target | Page 12, Table 4 |
| Validation aggregate | Actual expected crash mean / total | 0.084 / 294 | Testing data | Reference EB target aggregate | Page 12, Table 4 |
| Validation aggregate | Model estimate mean / total | 0.086 / 301 | Testing data, Model 1 | Close aggregate match to EB target | Page 12, Table 4 |
| Validation aggregate | No-volume model estimate mean / total | 0.077 / 268 | Testing data, Model 2 | Lower aggregate estimate than EB target | Page 12, Table 4 |
| Validation error | MBE | -0.0015 training; 0.0018 testing | Model 1 | Mean bias close to zero against EB target | Page 12, Table 4 |
| Validation error | MBE | -0.011 training; -0.007 testing | Model 2 | Small negative mean bias | Page 12, Table 4 |
| Validation error | RMSE | 0.18 training; 0.19 testing | Model 1 | Error against EB expected-crash target | Page 12, Table 4 |
| Validation error | RMSE | 0.17 training; 0.18 testing | Model 2 | Error against EB expected-crash target | Page 12, Table 4 |

After the table:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? The adjusted R² values are in-sample model-fit diagnostics. MBE/RMSE and aggregate mean/total comparisons are reported for both training data and a random 20% testing set from the same original Oregon dataset. No spatial holdout, temporal holdout, grouped holdout, cross-validation, or external validation is reported.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample diagnostic**, not unqualified predictive accuracy. The training metrics are in-sample diagnostics. The testing metrics are random-holdout diagnostics against a derived EB expected-crash target.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They mainly test model fit and aggregate error against the EB expected-crash target. They do not directly test future observed crash prediction, spatial transfer, or external hotspot/ranking usefulness.
- Are any metrics likely to be optimistic for real-world deployment? Yes. The response is a smoothed EB target, and the random split may put nearby or correlated sections in both training and testing data.
- Which metric, if any, is most relevant to Open Road Risk? The volume vs no-volume comparison is useful as an AADT-sensitivity diagnostic for low-volume links. The MBE/RMSE reporting is useful as an example of target-level validation, but weaker than grouped/spatial validation.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The paper avoids modelling raw sparse crash counts directly by using EB expected crashes as the response.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: The proposed models use OLS on log EB expected crashes. Poisson and negative-binomial models are discussed in background literature but are not used as the final proposed model family.
- Whether high-risk locations are evaluated separately: Not stated. The method ranks priority sites, but no separate validation for high-risk locations is reported.
- Evidence quote or page reference: Page 1 states that crashes on low-volume roads are sporadic and may make conventional crash-history screening unsuitable. Page 4 states that EB expected total crashes were selected as the screening basis. Page 11 Figure 5 shows use of crash density to rank priority sites.
- Practical relevance to my sparse collision link-year dataset: Medium. The paper supports EB/shrinkage thinking for sparse low-volume-road crashes. Direct transfer is limited because Open Road Risk models raw link-year counts with an exposure offset and uses a much larger, mixed road network.

## 11. Validation Strategy

- Train/test split method: Random 80/20 split; about 680 miles for training and 170 miles for testing.
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: Not stated.
- Metrics: MBE, RMSE, mean actual/predicted EB expected crashes, total actual/predicted EB expected crashes, and adjusted R².
- External validation: No.
- Leakage or generalisation risks: Random splitting of 0.05-mile sections may allow spatially adjacent or otherwise correlated road sections into both train and test sets. The target is EB expected crashes, which already blends observed crashes with HSM-predicted crashes. This is not classic feature leakage, but it limits claims about independent future/spatial predictive performance.
- Evidence quote or page reference: Page 9 says the data were randomly split into 80% training and 20% testing. Page 11 says the testing data were randomly selected from the original dataset. Page 12 provides Table 4 validation metrics.
- What I should copy or avoid: Copy the practice of reporting aggregate bias and RMSE against a clearly defined target. Avoid treating high R² against EB expected crashes, or random holdout alone, as enough for production validation.

## 12. Key Findings Relevant to My Project

1. Finding: The paper supports the concern that raw crash-history screening is unstable on low-volume roads.
   - Why it matters: This aligns with Open Road Risk's use of exposure/context-adjusted and shrinkage-style diagnostics rather than raw counts alone.
   - Evidence quote or page reference: Page 1 says low-volume-road crashes are limited and scattered sporadically.
   - Confidence: high

2. Finding: The paper compares a volume model against a no-volume model, with only a small adjusted R² difference.
   - Why it matters: This is useful as an AADT-sensitivity diagnostic for Open Road Risk's low-volume rural links.
   - Evidence quote or page reference: Pages 9–10 show Equations 4 and 5; adjusted R² values are 0.915 and about 0.905/0.906.
   - Confidence: high for the paper result; medium for transferability.

3. Finding: Horizontal curvature is operationalised as an interpretable classified risk factor.
   - Why it matters: Curvature is derivable from OS Open Roads geometry and is a realistic Open Road Risk diagnostic/candidate feature.
   - Evidence quote or page reference: Pages 7–8 describe CART thresholds around 8.9° and 28°. Figure 1 shows higher EB expected crashes for higher curvature groups, although the sharp-group value differs between text and figure.
   - Confidence: medium.

4. Finding: Grade is discussed and classified, but not included in the final regression equations.
   - Why it matters: The paper supports checking grade descriptively but should not be cited as evidence that grade was a significant final-model predictor in this paper.
   - Evidence quote or page reference: Page 8 and Figure 4 discuss the 4% grade split. Equations 4 and 5 and Tables 2 and 3 do not include grade.
   - Confidence: high.

5. Finding: Several roadway/roadside predictors used in the paper have low transferability to a national open-data UK pipeline.
   - Why it matters: Shoulder width, side slope, fixed objects, and driveway density may represent relevant omitted context, but they are hard to implement at Open Road Risk scale without extra data.
   - Evidence quote or page reference: Page 4 describes use of ODOT video logs for driveway density, side-slope rating, and fixed-object rating. Table 1 lists these variables.
   - Confidence: high.

6. Finding: The paper's high R² values are not external predictive validation.
   - Why it matters: Open Road Risk documentation should distinguish fit to an EB target from spatial/temporal generalisation to future observed collisions.
   - Evidence quote or page reference: Pages 9–12 show OLS models, random split validation, and Table 4 metrics.
   - Confidence: high.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Volume vs no-volume sensitivity comparison | Tests how dependent low-volume-road rankings are on uncertain AADT estimates | Stage 2 features with and without AADT/exposure variants | Around 850 miles; 0.05-mile sections | High as a diagnostic; not a replacement for exposure-offset modelling | Stage 2 / validation / documentation | Low to medium | Could be misread as evidence that exposure does not matter generally |
| Curvature threshold diagnostic | Provides a simple geometry-risk check | OS Open Roads geometry and curvature calculation | 0.05-mile rural sections | Medium to high; thresholds need UK recalibration | feature engineering / validation / documentation | Medium | Oregon thresholds may not transfer |
| Grade diagnostic | Supports testing whether DEM-derived grade relates to risk patterns | OS Terrain 50 or other DEM; bridge/tunnel handling | 0.05-mile rural sections | Medium; scalable but DEM sampling has known issues | future feature / validation / documentation | Medium | Grade was not in the final regression equations |
| EB/shrinkage framing for sparse crashes | Supports expected-crash and shrinkage language for sparse low-volume roads | Observed crashes, baseline expected-crash model, exposure/context features | Around 850 miles | Conceptually useful; direct HSM EB not transferable | Stage 2 / validation / documentation | Medium | Can hide assumptions in the baseline SPF |
| Classified-variable robustness check | Tests whether coarse bins retain signal and improve interpretability | Existing continuous features recoded into bins | 0.05-mile rural sections | High as a diagnostic | validation / documentation | Low | Bins may be arbitrary or overfit |
| Aggregate bias/RMSE reporting | Adds simple target-level diagnostic reporting | Model predictions and targets | Random 80/20 split | Medium; should be secondary to grouped/spatial validation | validation | Low | Random holdout may overstate generalisation |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Direct use of Oregon-calibrated equations | Coefficients and thresholds are local to Oregon low-volume roads | Oregon HSM calibration and roadway inventory | Around 850 miles | Low | Refit locally using UK data and compatible features | High |
| HSM SPF as the EB base model | HSM SPF is not UK-calibrated and differs from Open Road Risk's structure | UK-calibrated HSM SPF | Around 850 miles | Low | Use Open Road Risk's own baseline GLM/SPF-like model for shrinkage | High |
| Shoulder width, side slope, fixed objects as full-network features | Requires consistent roadside inventory/video-log data | Roadside inventory | Around 850 miles | Low | Use pilots, proxies, or commercial/local datasets if available | High |
| Driveway density at national scale | Requires consistent access-point data or image extraction | Driveway/access inventory | Around 850 miles | Low to medium | Pilot using OSM/address/access proxies | Medium to high |
| Full fixed 0.05-mile segmentation replacement | Would disrupt OS Open Roads link-based pipeline | Rebuilt segmentation and crash assignment | 0.05-mile sections | Medium to low as full replacement | Pilot or aggregate fixed-length diagnostics to links | Medium |
| OLS on log EB expected crashes as primary production model | Predicts a derived model output rather than raw collision counts | Methodological mismatch rather than data gap | Around 850 miles | Low | Keep as diagnostic/surrogate idea only | High |

Important:

- Most transferable ideas are diagnostics, documentation notes, or small pilots, not production changes.
- The study is much smaller and more homogeneous than Open Road Risk.

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Partly. It supports moving beyond raw crash counts and uses AADT in the HSM SPF/EB target and in one proposed model. It does not directly support Open Road Risk's exposure-offset formulation.
- Does it suggest better handling of AADT/AADF uncertainty? It suggests a useful sensitivity diagnostic: compare volume and no-volume variants, especially for low-volume rural links. It does not provide traffic-count imputation or uncertainty propagation.
- Does it suggest useful geometry or road-context features? Yes. Curvature is the most realistic transferable feature. Grade is useful as a descriptive diagnostic but was not included in the final regression equations. Lane width, shoulder width, side slope, fixed objects, and driveway density are conceptually relevant but have weaker open-data transferability.
- Does it suggest better modelling of junctions? No. Intersections are explicitly out of scope.
- Does it suggest better treatment of severity? No. Total crashes are used.
- Does it suggest better validation design? Indirectly. It uses random holdout validation, but for Open Road Risk this mainly highlights the need for grouped, spatial, or temporal validation.
- Does it expose a weakness in my current approach? It highlights missing roadside-inventory variables and the need to test sensitivity of low-volume-road rankings to AADT uncertainty.

## 15. Repo Actionability

1. Suggested repo action: Add a documentation note distinguishing raw crash counts, exposure-adjusted risk, EB/shrinkage logic, and risk-factor screening for sparse low-volume roads.
   - Action type: documentation note
   - Relevant stage: documentation / Stage 2
   - Why the paper supports it: The paper motivates EB/risk-factor screening because low-volume-road crashes are sparse and scattered.
   - Evidence quote or page reference: Pages 1–4.
   - Effort: low
   - Risk if implemented badly: Could overstate the paper as validating Open Road Risk.

2. Suggested repo action: Add a low-volume subset diagnostic comparing Stage 2 rankings under full exposure, binned exposure, and reduced/no-AADT variants.
   - Action type: diagnostic
   - Relevant stage: Stage 2 / validation
   - Why the paper supports it: The paper explicitly compares with-AADT and no-AADT screening models.
   - Evidence quote or page reference: Pages 6 and 9–12.
   - Effort: medium
   - Risk if implemented badly: Could be misread as evidence that exposure is unnecessary.

3. Suggested repo action: Use the paper as support for a curvature diagnostic, but recalibrate thresholds on Open Road Risk data rather than importing Oregon thresholds.
   - Action type: diagnostic / small pilot
   - Relevant stage: feature engineering / validation
   - Why the paper supports it: The paper uses CART-derived curvature categories and reports higher expected crashes for sharper curves.
   - Evidence quote or page reference: Pages 7–8 and Figure 1.
   - Effort: low to medium
   - Risk if implemented badly: Oregon degree-of-curvature thresholds may be treated as universal.

4. Suggested repo action: Treat grade as a candidate diagnostic after OS Terrain 50 integration, but do not cite this paper as evidence that grade was a final-model predictor.
   - Action type: diagnostic / documentation note
   - Relevant stage: feature engineering / validation
   - Why the paper supports it: Grade is discussed and classified descriptively, but omitted from the final equations.
   - Evidence quote or page reference: Pages 8–10, Figure 4, Equations 4–5, Tables 2–3.
   - Effort: low to medium
   - Risk if implemented badly: Could overclaim evidence for grade.

5. Suggested repo action: Add a documentation gap note for roadside inventory variables that are plausible but weakly covered in open UK data.
   - Action type: documentation note
   - Relevant stage: documentation / future feature
   - Why the paper supports it: Shoulder width, side slope, fixed objects, and driveway density are included or discussed as risk factors.
   - Evidence quote or page reference: Page 4 and Table 1.
   - Effort: low
   - Risk if implemented badly: Could imply the model is invalid rather than documenting a data limitation.

6. Suggested repo action: Add a validation note that high R² against EB expected crashes is not comparable to Open Road Risk's raw-count model metrics.
   - Action type: documentation note
   - Relevant stage: validation / documentation
   - Why the paper supports it: The reported R² values are for OLS prediction of a smoothed EB target.
   - Evidence quote or page reference: Pages 9–12.
   - Effort: low
   - Risk if implemented badly: Could sound like a criticism of the paper rather than a scope caveat.

## 16. Query Tags

- low-volume-roads
- rural-roads
- network-screening
- hotspot-detection
- Empirical-Bayes
- HSM-SPF
- AADT
- no-volume-model
- exposure-sensitivity
- risk-factors
- OLS-on-EB-response
- CART-thresholds
- curvature
- vertical-grade
- shoulder-width
- lane-width
- driveway-density
- roadside-hazards
- fixed-objects
- random-holdout
- spatial-leakage-risk
- zero-heavy-counts
- Oregon

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: Detailed crash geocoding or snapping method; whether property-damage-only crashes are included; exact observed-vs-estimated status of AADT records; spatial autocorrelation handling; temporal validation; external validation; high-risk subgroup/ranking validation; prediction intervals or uncertainty intervals.
- Parts of the paper that need manual checking: The curvature CART sharp-group value is internally inconsistent: page 7 text states 0.86, while Figure 1 on page 8 appears to show 0.23 for the sharpest group. Use the direction and thresholds cautiously unless checking with the authors or original figure source.
- Any likely ambiguity or risk of misinterpretation: The high R² values describe fit to an EB expected-crash target, not independent future crash prediction. The no-volume result should not be interpreted as proof that exposure is unimportant outside Oregon low-volume roads. Grade is classified and discussed but not used in the final regression equations.
