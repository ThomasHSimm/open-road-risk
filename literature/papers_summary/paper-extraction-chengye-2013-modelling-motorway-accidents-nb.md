RAW_MARKDOWN_START
Save this as: paper-extraction-chengye-2013-modelling-motorway-accidents-nb.md

# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Modelling Motorway Accidents using Negative  Binomial Regression.pdf
- Suggested Markdown filename: paper-extraction-chengye-2013-modelling-motorway-accidents-nb.md
- AI tool used: Gemini
- Model name, if visible: Gemini
- Model version, if visible: not stated
- Interface used: API
- Input type: PDF upload
- Output mode: raw Markdown copy block
- Was the full paper accessible to the model? yes
- Notes on access limitations: None

## 1. Citation

- Title: Modelling Motorway Accidents using Negative Binomial Regression
- Authors: Pan CHENGYE, Prakash RANJITKAR
- Year: 2013
- DOI or URL, if present: not stated (Proceedings of the Eastern Asia Society for Transportation Studies)
- Country / region studied: New Zealand (Auckland)
- Study setting: motorway / urban / rural

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper develops Negative Binomial regression models to predict annual accident frequencies on motorway segments based on non-behavioural factors such as traffic volume, road geometry, and weather.
- Main purpose: safety performance function / prediction / explanatory modeling
- Evidence quote or page reference: "This paper investigates motorway safety by developing accident prediction models that link accident frequencies to their non-behavioural contributing factors, including traffic conditions, geometric and operational characteristics of road, and weather conditions." (Page 1)

## 3. Response Variable

- Target variable: Accident frequency (per segment per year).
- Collision type: all crashes
- Severity handling: All severities are pooled together.
- Count, binary, rate, risk score, severity class, or other: Count (Negative Binomial distributed).
- Time window used for outcomes: 1 year (annual counts).
- Evidence quote or page reference: "Let $y_i$ be the random variable that represents the number of accidents occurring at a given motorway segment i during a given time interval (one year in this case)..." (Page 7)

## 4. Exposure Handling

- Exposure variable used, if any: Average Annual Daily Traffic (AADT) per lane, and segment length.
- Traffic count source: Traffic Monitoring System (TMS) vehicle sensors.
- Whether exposure is modelled, observed, assumed, or ignored: observed.
- Treatment of missing or sparse traffic counts: not stated.
- Whether offset terms, rates, denominators, or normalisation are used: Exposure variables (`Ln length` and `Ln AADT per lane`) are treated as independent explanatory covariates with estimated coefficients, rather than as a mathematically fixed structural offset.
- Evidence quote or page reference: "$E(y_i) = e^{\beta_0 + \beta_1 \times Ln~length + \beta_2 \times Ln~AADT~per~lane + \dots}$" (Page 9)
- Transferability to my AADF/WebTRIS setup: medium
- Notes: Open Road Risk strictly enforces `log(AADT * length)` as a structural offset with a fixed coefficient of 1. This paper allows the model to learn the elasticity of length and AADT independently. This represents a methodological divergence; their feature set is transferable, but their specific mathematical handling of exposure should be compared rather than blindly copied.

## 5. Spatial Unit of Analysis

- Unit: road segment
- Segment length or segmentation rule: Homogeneous road segments defined primarily by the presence of ramps (on-ramp, off-ramp, or no ramp) and constant cross-section features. Lengths were strictly constrained to be between 0.2 km and 3.0 km.
- How crashes are assigned to the network: Snapped to the 137 defined homogeneous segments.
- Treatment of junctions/intersections: Ramps are the primary classification boundary. A segment is classified as "with on-ramp", "with off-ramp", or "without ramp".
- Spatial aggregation risks: Minor. The authors deliberately avoided segments shorter than 0.2km to prevent excess zeros and heteroskedasticity.
- Evidence quote or page reference: "Segments shorter than 0.2 km or longer than 3 km were avoided to mitigate the heteroskedasticity problem. Short segments can potentially lead to excess zeros in the crash data." (Page 5)
- Relevance to OS Open Roads link-based pipeline: High conceptually, but computationally contrary. Open Road Risk uses raw OS links (often <50m). This paper demonstrates that standard Negative Binomial GLMs struggle with short segments, validating the need for XGBoost or specialized rare-event handling at the raw OS link scale.

## 6. Temporal Unit of Analysis

- Years covered: 2004-2010 (7 years).
- Temporal resolution: yearly.
- Whether seasonality or time-of-day is modelled: no.
- Whether before-after or panel structure is used: Temporal holdout used (train on 2004-2008, test on 2009-2010).
- Evidence quote or page reference: "A 5-year period (2004 to 2008) dataset was employed in the model development, and a 2-year period (2009 and 2010) dataset was used for testing the prediction performance." (Page 10)
- Relevance to WebTRIS-style time profiles: None.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Ramp Presence | RAMM / Highway geometry | Categorical indicator (On-ramp, Off-ramp, None) used to split data into sub-models. | Merging/diverging traffic creates distinct conflict profiles. | Yes (Spatial join of OS Links to slip roads). |
| Heavy Vehicle % | TMS | Proportion of HGV. | Trucks occupy wider lanes and create speed variance. | Yes (AADF HGV proportion). |
| Ramp AADT | TMS | Traffic volume entering/exiting via the ramp. | Captures the intensity of merging/diverging conflicts. | Conceptually yes, but hard to map accurately to mainline OS links automatically. |
| Average Curvature | RAMM | Average radius of horizontal curves. | Sharp curves induce driver caution ("risk compensation") or loss of control. | Yes (derive from OS geometry). |
| Gradient | RAMM | Maximum up-grade / down-grade. | Up-grades increase speed variance; down-grades increase stopping distance. | Yes (OS Terrain 50). |

## 8. Model Architecture

- Algorithms/models used: Negative Binomial (NB) Regression. Evaluated Generalized Estimating Equations (GEE) but preferred NB.
- Baseline model: Overall Negative Binomial model for the entire motorway.
- Final/preferred model: Segment-specific Negative Binomial models (separate models for No-ramp, On-ramp, and Off-ramp segments).
- Loss function or likelihood, if stated: Maximum Likelihood Estimation of the Negative Binomial distribution.
- Offset/exposure term, if used: None (AADT and length treated as standard log-linear covariates).
- Spatial autocorrelation handling: None.
- Temporal dependence handling: Ignored during fitting; 5 separate yearly observations per segment were pooled. Evaluated via a strictly future temporal holdout.
- Interpretability method: Coefficient estimates and t-statistics.
- Evidence quote or page reference: "Prediction model was also developed for overall accident frequency by applying GEE technique... This outcome indicated that negative binomial model slightly surpass GEE model in terms of predictive ability in this case." (Page 16)

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model Fit | Pseudo R-squared ($\rho^2$) | 0.119 | Overall Model | Baseline variance explained. | Table 3, p. 11 |
| Model Fit | Pseudo R-squared ($\rho^2$) | 0.194 | On-ramp Segments | Splitting by facility type drastically improves model fit for on-ramp sections. | Table 5, p. 14 |
| Predictive Error | MAD | 3.70 | Split Models (Pred) | Lowest mean absolute deviance on the 2009-2010 held-out data. | Table 6, p. 16 |
| Predictive Error | MSPE | 27.87 | Split Models (Pred) | Lowest mean-squared predictive error on held-out data. | Table 6, p. 16 |
| Fixed Effect | Coefficient | +0.166 | Heavy vehicle % (No ramp) | Higher HGV percentage significantly increases accidents on mainline segments. | Table 5, p. 14 |
| Fixed Effect | Coefficient | -2.089 | Avg. Curvature (Off-ramp) | Sharper curves reduce accidents, likely due to visual warning and speed reduction. | Table 5, p. 14 |

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? Both in-sample (Fit) and temporally held out (Pred).
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. MAD_Fit and MSPE_Fit are in-sample diagnostics. MAD_Pred and MSPE_Pred are temporal out-of-sample validation metrics.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? Predictive generalisation to future years (temporal holdout).
- Are any metrics likely to be optimistic for real-world deployment? No, the temporal holdout is a rigorous real-world benchmark.
- Which metric, if any, is most relevant to Open Road Risk? The reduction in MSPE_Pred when moving from an "Overall model" to "Split models" strongly supports building separate Stage 2 models (or very strong tree interactions) for junctions versus mainline links.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The researchers explicitly altered the spatial geometry of the data to *avoid* zero-heavy data. They refused to use segments shorter than 200m specifically because such segments produce too many zeros for standard Negative Binomial / Poisson models to handle reliably.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Evaluated Zero-Inflated Poisson (ZIP) but discarded it because altering the segment lengths artificially removed the zero-inflation problem. Negative Binomial was used to handle the remaining overdispersion.
- Whether high-risk locations are evaluated separately: Yes, models are split by the presence of ramps.
- Evidence quote or page reference: "Zero-inflated Poisson model is inappropriate as there are not many sections with zero accident frequency... Segments shorter than 0.2 km or longer than 3 km were avoided to mitigate the heteroskedasticity problem. Short segments can potentially lead to excess zeros in the crash data." (Pages 5, 7)
- Practical relevance to my sparse collision link-year dataset: This highlights a fundamental constraint of GLMs. Because Open Road Risk uses raw OS links (often <50m), you *will* have the excess zeros that this paper avoided. This validates your choice of XGBoost or hurdle models for Stage 2, as standard Negative Binomial regression would likely fail on your unaggregated link geometry.

## 11. Validation Strategy

- Train/test split method: Temporal split (Train: 2004-2008. Test: 2009-2010).
- Spatial holdout used? no
- Temporal holdout used? yes
- Grouped holdout used? no
- Cross-validation type: None (strict train/test block).
- Metrics: Mean Absolute Deviance (MAD), Mean-Squared Predictive Error (MSPE).
- External validation: None.
- Leakage or generalisation risks: Minimal. A strict temporal holdout is highly robust for evaluating forecasting ability, assuming road geometries did not radically change.
- Evidence quote or page reference: "The 5 years data between 2004 and 2008 were used to fit the model, and 2 years data of 2009 and 2010 were applied to test the predictive performance of model." (Page 15)
- What I should copy or avoid: Copy the temporal holdout strategy. Testing Stage 2 models on future years (e.g., train 2015-2022, test 2023-2024) is the gold standard for road risk pipelines to prove they can proactively identify persistent risk rather than just memorizing historical hotspots.

## 12. Key Findings Relevant to My Project

- Finding: Splitting models by facility type (segments without ramps, with on-ramps, with off-ramps) significantly improves predictive accuracy over a single monolithic model.
- Why it matters: Motorway junctions have fundamentally different crash mechanics than mainline links. Open Road Risk should either fit a separate Stage 2 model for links near junctions, or ensure XGBoost has a clear "junction proximity" categorical feature to split on at the root.
- Evidence quote or page reference: "Therefore a conclusion is drawn that applying different models for motorway segments without ramp, with on-ramp and with off-ramp can obtain more precise accident frequency prediction." (Page 16)
- Confidence: High.

- Finding: High traffic volumes entering via on-ramps actually *decrease* expected accident frequencies on those segments.
- Why it matters: This counterintuitive finding indicates that congestion forces slower speeds, reducing severe crashes on merging segments. It highlights that raw AADT is not a strictly monotonic risk multiplier; congestion states matter.
- Evidence quote or page reference: "...whilst for segments with on-ramp, the ramp AADT has a negative impact on accidents... This result can be attributed to congested traffic flow conditions near motorway sections on upstream side of the on-ramps with heavy entering traffic." (Page 13)
- Confidence: Medium (specific to highly congested urban motorways).

- Finding: Greater horizontal curvature (sharper curves) decreases accident likelihood.
- Why it matters: Drivers compensate for visible risks (sharp curves) by slowing down, reducing crash frequency compared to straight, high-speed sections where inattention is fatal. Your model may learn a negative coefficient for curvature; do not assume this is a bug.
- Evidence quote or page reference: "Generally greater horizontal curvature of a segment, either average or maximum curvature, tends to decrease accident likelihood by virtue of the visual effect that can caution the drivers." (Page 16)
- Confidence: High.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Temporal Holdout Validation | Proves the model can forecast future risk, not just memorize history. | Collision years 2015-2024 | 959 segment-years | 21.7M link-years | Validation | Low | True changes in network/AADT over time might degrade the test set if Stage 1a is inaccurate. |
| Feature: Heavy Vehicle Proportion | Highly significant predictor of mainline crashes. | AADF / WebTRIS HGV% | 137 segments | 2.1M links | Stage 2 Feature | Low | DfT imputes HGV counts heavily on minor roads; could introduce noise outside the SRN. |
| Facility-type Sub-models | Junctions obey different physics than mainlines. | OS Network nodes (junction flags) | 137 segments | 2.1M links | Stage 2 Architecture | Medium | Classifying OS links neatly into "mainline" vs "slip road/junction" can be topologically tricky. |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Dropping links < 200m | Open Road Risk needs to predict risk for the *entire* OS Open Roads network, where many natural links are <50m. | N/A (Method mismatch) | Minimum 270m segments | Incompatible with OS link geometry | Keep short links and use XGBoost/zero-heavy models instead of standard Negative Binomial GLMs. | High |
| Independent Exposure Covariates | Treating log(Length) and log(AADT) as free parameters risks the model learning unphysical elasticities (e.g. risk decreasing as length increases) on a noisy national dataset. | N/A | Localized highly-controlled 74km corridor | UK-wide noisy data | Stick to the strict `log(AADT * Length)` offset for stability, but perhaps test the free-covariate version as a diagnostic. | Medium |

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? It supports using exposure, but treats it flexibly via regression coefficients rather than a strict normalisation offset.
- Does it suggest better handling of AADT/AADF uncertainty? No.
- Does it suggest useful geometry or road-context features? Yes, strongly supports HGV percentage, ramp/junction proximity, gradient, and curvature.
- Does it suggest better modelling of junctions? Yes. It explicitly proves that splitting the network into junction vs non-junction segments yields higher predictive accuracy than a global model.
- Does it suggest better treatment of severity? No, pools all accidents.
- Does it suggest better validation design? Yes. The use of a strict temporal holdout (Train Past, Predict Future) is highly recommended for Open Road Risk.
- Does it expose a weakness in my current approach? Highlights that standard Negative Binomial GLMs will likely fail or mis-estimate dispersion if applied to your short, zero-heavy OS links.

## 15. Repo Actionability

1.  Suggested repo action: Implement a temporal holdout split (e.g., Train: 2015-2022, Test: 2023-2024) in the Stage 2 validation pipeline.
    - Action type: validation
    - Relevant stage: Stage 2
    - Why the paper supports it: Standard practice for proving predictive generalization in road safety. It verifies whether the pipeline can actually identify proactive future risk.
    - Evidence quote or page reference: "The 5 years data between 2004 and 2008 were used to fit the model, and 2 years data of 2009 and 2010 were applied to test the predictive performance of model." (Page 15)
    - Effort: low
    - Risk if implemented badly: The test set may look artificially bad if COVID-19 pandemic years (2020-2021) are mixed poorly between train and test sets. Choose the split year carefully.

2.  Suggested repo action: Create a boolean flag for OS links indicating if they are part of, or immediately adjacent to, a motorway slip road / junction.
    - Action type: candidate feature
    - Relevant stage: feature engineering / Stage 2
    - Why the paper supports it: The presence of merging/diverging ramps fundamentally alters crash frequency and the relevance of other variables (like median width and curvature).
    - Evidence quote or page reference: "Therefore a conclusion is drawn that applying different models for motorway segments without ramp, with on-ramp and with off-ramp can obtain more precise accident frequency prediction." (Page 16)
    - Effort: medium
    - Risk if implemented badly: None.

3.  Suggested repo action: Note in documentation that sharp horizontal curvature may legitimately output a negative coefficient (lower risk).
    - Action type: documentation note
    - Relevant stage: documentation
    - Why the paper supports it: Prevents stakeholders from assuming the model is broken if it says sharp curves are "safer". It is a known phenomenon of visual risk compensation.
    - Evidence quote or page reference: "Generally greater horizontal curvature of a segment... tends to decrease accident likelihood by virtue of the visual effect that can caution the drivers." (Page 16)
    - Effort: low
    - Risk if implemented badly: None.

## 16. Query Tags

- negative-binomial
- temporal-holdout
- homogeneous-segments
- motorway-crashes
- junction-proximity
- heavy-vehicles
- horizontal-curvature
- risk-compensation
- overdispersion
- predictive-validation

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: The exact method used to deal with crashes located exactly on the boundary between a ramp segment and a mainline segment.
- Parts of the paper that need manual checking: If considering unconstraining the exposure offset in Stage 2, review Equation 10 carefully to see how they specified `Ln AADT` and `Ln length`.
- Any likely ambiguity or risk of misinterpretation: The paper states that "speed limit" increases crash frequency. This is a classic endogeneity/reverse-causality error (speed limits were lowered to 80km/h *because* the segment was dangerous). Open Road Risk must be careful not to let the ML model misinterpret remedial safety treatments (like lowered speed limits or concrete barriers) as the *cause* of crashes.