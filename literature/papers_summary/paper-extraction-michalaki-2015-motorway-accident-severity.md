RAW_MARKDOWN_START
Save this as: paper-extraction-michalaki-2015-motorway-accident-severity.md

# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: 1-s2.0-S0022437515000833-main.pdf
- Suggested Markdown filename: paper-extraction-michalaki-2015-motorway-accident-severity.md
- AI tool used: Gemini
- Model name, if visible: Gemini 3.1 Pro
- Model version, if visible: not stated
- Interface used: API
- Input type: PDF upload
- Output mode: raw Markdown copy block
- Was the full paper accessible to the model? yes
- Notes on access limitations: None

## 1. Citation

- Title: Exploring the factors affecting motorway accident severity in England using the generalised ordered logistic regression model
- Authors: Paraskevi Michalaki, Mohammed A. Quddus, David Pitfield, Andrew Huetson
- Year: 2015
- DOI or URL, if present: 10.1016/j.jsr.2015.09.004
- Country / region studied: England (United Kingdom)
- Study setting: motorway

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper aims to explain the factors affecting the severity of accidents occurring on the hard shoulder versus the main carriageway of motorways in England.
- Main purpose: descriptive analysis / explanatory modeling
- Evidence quote or page reference: "The aim of this study is to investigate the main factors affecting the severity of accidents in these two distinct parts of the motorway and to identify any differences between them." (Page 1)

## 3. Response Variable

- Target variable: Accident severity
- Collision type: injury / fatal / serious / slight
- Severity handling: Modelled as a three-level ordinal discrete variable (slight, serious, fatal).
- Count, binary, rate, risk score, severity class, or other: severity class
- Time window used for outcomes: 2005-2011
- Evidence quote or page reference: "The dependent variable of the models is ‘severity of accident,’ a discrete variable that can obtain three values: slight injury, serious injury and fatality." (Page 3)

## 4. Exposure Handling

- Exposure variable used, if any: None explicitly used in the model.
- Traffic count source: not stated (historical peak definitions were used to proxy flow states).
- Whether exposure is modelled, observed, assumed, or ignored: ignored (this is a severity model conditioned on a crash having already occurred; volume exposure is not used as a denominator).
- Treatment of missing or sparse traffic counts: not stated
- Whether offset terms, rates, denominators, or normalisation are used: No.
- Evidence quote or page reference: "Since no detailed traffic data were available, the way of incorporating this information in the model was by creating four variables according to the hour that the accident happened." (Page 6)
- Transferability to my AADF/WebTRIS setup: low
- Notes: Because this models severity *given* a crash (rather than crash frequency/risk), structural volume offsets are not required in their math. Their models cannot directly replace Stage 2 frequency models, but their findings inform feature engineering.

## 5. Spatial Unit of Analysis

- Unit: location type (Hard Shoulder vs. Main Carriageway)
- Segment length or segmentation rule: not stated. Data was filtered purely by STATS19 categorical location codes.
- How crashes are assigned to the network: Based on STATS20 definition of where the first impact occurred.
- Treatment of junctions/intersections: not stated.
- Spatial aggregation risks: Authors tested a multilevel model using English Counties to check for spatial correlation (ICC) but found it too low to justify the hierarchical structure.
- Evidence quote or page reference: "The distinction between the HS and MC accidents is based on the location where the accident happened. As described in STATS20... an accident should be located where the first impact occurred." (Page 3)
- Relevance to OS Open Roads link-based pipeline: Low for direct mapping, but provides a strong rationale for treating hard-shoulder environments as a distinct facility type or diagnostic subset.

## 6. Temporal Unit of Analysis

- Years covered: 2005-2011
- Temporal resolution: time-of-day (peak vs off-peak), day of week, and month.
- Whether seasonality or time-of-day is modelled: yes
- Whether before-after or panel structure is used: no
- Evidence quote or page reference: "...creating four variables according to the hour that the accident happened. These were based on historical data of peak in the morning, the late afternoon peak, normal and non-peak (quiet) traffic hours." (Page 6)
- Relevance to WebTRIS-style time profiles: High. Vindicates your Stage 1b goal to generate peak/off-peak fractions, as these are proven severity modulators.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Traffic peak state | Time of crash | Categorized into morning peak, afternoon peak, normal, non-peak based on historical data. | Proxy for traffic flow, congestion, and free-flow speed. | Yes (using WebTRIS time profiles). |
| HGV involvement | STATS19 vehicle type | Binary flag if at least 1 HGV involved in the crash. | Mass differential significantly increases severity. | Yes (as an aggregated HGV fraction from AADF for the link). |
| Single-vehicle crash | STATS19 vehicle records | Binary flag if exactly 1 vehicle involved. | Highly correlated with fatal outcomes (e.g., run-off-road). | Post-event only (good for diagnostics, bad for prediction). |
| Day of week | Date of crash | Dummy variables (e.g., Saturday, Sunday vs Friday). | Captures recreational vs commuter driving styles. | Yes. |

## 8. Model Architecture

- Algorithms/models used: Partially Constrained Generalized Ordered Logistic Regression.
- Baseline model: Ordered Logistic Regression and Multilevel Ordered Logistic Regression.
- Final/preferred model: Generalized Ordered Logistic Regression (which relaxes the parallel regression assumption for variables that violate it).
- Loss function or likelihood, if stated: Maximum likelihood estimation.
- Offset/exposure term, if used: None.
- Spatial autocorrelation handling: Tested a two-level model with random intercepts at the County level, but dropped it due to low Intra-class Correlation Coefficient (ICC).
- Temporal dependence handling: A yearly trend dummy variable was included.
- Interpretability method: Beta coefficients (constant across severity thresholds), Gamma coefficients (varying across thresholds), and Marginal Effects.
- Evidence quote or page reference: "In these models... two coefficients (M-1) are estimated for each of the explanatory variables that violated the parallel regression assumption: one coefficient represents the effect... on the outcome of slight relative to serious and fatal; and the other indicates the effect... on slight and serious relative to fatal." (Page 4)

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model Fit | Pseudo R-squared | 0.0708 | Main Carriageway | Low explanatory power for the MC severity model overall. | Table 2, p. 5 |
| Model Fit | Pseudo R-squared | 0.1241 | Hard Shoulder | Better explanatory power for the HS severity model. | Table 2, p. 5 |
| Effect Estimate | Beta Coefficient | +0.3353 | Main Carriageway (HGV) | HGV involvement significantly increases MC crash severity. | Table 2, p. 5 |
| Effect Estimate | Beta Coefficient | +0.7565 | Hard Shoulder (HGV) | HGV involvement increases HS severity drastically more than MC. | Table 2, p. 5 |
| Effect Estimate | Beta Coefficient | +0.3891 | Main Carriageway (Fatigue) | Driver fatigue increases MC severity. | Table 2, p. 5 |
| Marginal Effect | Probability | +0.0149 | Main Carriageway (Single-veh) | Single-vehicle crashes are 1.49% more likely to be fatal. | Table 3, p. 6 |

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? These are completely in-sample.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. These are **in-sample diagnostics**.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They test in-sample model fit and explanatory relationships (identifying factors associated with severity).
- Are any metrics likely to be optimistic for real-world deployment? Yes, Pseudo R-squared is an optimistic in-sample fit metric.
- Which metric, if any, is most relevant to Open Road Risk? The comparative Beta coefficients showing the massively different impact of HGVs on Hard Shoulders versus Main Carriageways.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Not applicable to frequency; this models severity. Fatality is a rare class (1.77% MC, 8.38% HS), but no explicit class balancing (like SMOTE) is applied.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: None. Uses standard Maximum Likelihood Estimation for discrete choices.
- Whether high-risk locations are evaluated separately: Yes. Hard Shoulder crashes (which represent only ~1.6% of crashes but have 5x the fatality rate) are strictly segregated into a completely separate model to avoid washing out their unique risk profile.
- Evidence quote or page reference: "The statistical models are applied to the HS and MC motorway accidents separately and the relationships between the levels of severity of these accidents are explored..." (Page 4)
- Practical relevance to my sparse collision link-year dataset: Suggests that treating vastly different facility types (like motorways vs rural lanes, or hard-shoulders vs live lanes) as homogeneous records in a single Stage 2 model may obscure critical risk multipliers.

## 11. Validation Strategy

- Train/test split method: None (the entire dataset from 2005-2011 was used for estimation).
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: None.
- Metrics: Log likelihood, Pseudo R-squared.
- External validation: None.
- Leakage or generalisation risks: Severe data leakage if interpreted predictively. The model uses post-event STATS19 variables (e.g., number of casualties, number of vehicles, police-assessed contributory factors like "fatigue" or "error") to "predict" the severity of the crash. This is valid for retrospective *explanatory* analysis, but entirely invalid for forward-looking *prediction* since those variables are unknown before the crash occurs.
- Evidence quote or page reference: "Contributory factors... are factors in a road accident in the opinion of the attendant police officer - that are the key actions and failures that led directly to the actual impact." (Page 4)
- What I should copy or avoid: Avoid using STATS19 vehicle counts, casualty counts, or contributory factors as input features in your Stage 2 model. They must only be used to define target slices or evaluate post-prediction diagnostics.

## 12. Key Findings Relevant to My Project

- Finding: Hard shoulder accidents have a fundamentally different, and much worse, severity profile compared to main carriageway accidents (almost 5x higher proportion of serious/fatal injuries).
- Why it matters: If Open Road Risk models all motorway links identically, it will miss the acute risk of breakdown/hard-shoulder environments. Identifying shoulder width or emergency refuge areas could be a valuable future feature.
- Evidence quote or page reference: "The percentage of accidents on the HS is almost five times than on the MC and the proportion of serious injury accidents is also noticeably higher on the HS." (Page 1) / Table 1.
- Confidence: High.

- Finding: The involvement of Heavy Goods Vehicles (HGVs) massively increases crash severity, particularly in hard-shoulder environments.
- Why it matters: Strongly supports the inclusion of "HGV proportion" (derived from AADF or WebTRIS) as a structural feature in your Stage 2 model.
- Evidence quote or page reference: "HGVs appear to have a positive coefficient... it is worthwhile to note that in the case of HS accidents, this variable has a much greater effect..." (Page 6)
- Confidence: High.

- Finding: Non-peak hours (quiet traffic) are associated with higher accident severity.
- Why it matters: Validates the use of Stage 1b (WebTRIS time profiles) to extract an "off-peak traffic fraction" as a feature. Free-flow conditions lead to higher kinetic energy upon impact.
- Evidence quote or page reference: "The model illustrates that if the hour is non-peak, the severity tends to be higher. This might be related to speed, which is generally higher during non-peak hours..." (Page 6)
- Confidence: High.

- Finding: Spatial correlation of severity at the regional (County) level is very weak.
- Why it matters: Suggests that unobserved regional/administrative variables do not heavily dictate motorway crash severity; physical link features and traffic flow are much more dominant.
- Evidence quote or page reference: "However, the ICC was found to be low (i.e., 0.016 for MC accidents and 0.1 for HS accidents) suggesting that the correlation among the accidents that occur in the same county is not strong enough to support the use of the multilevel model." (Page 4)
- Confidence: Medium (They only tested counties; closer link-level spatial autocorrelation wasn't measured).

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| HGV Proportion Feature | Physical mass disparity drives severity; proven highly significant. | AADF / WebTRIS | 47,000 crashes | 2.1M links | Stage 2 / feature engineering | Low | AADF HGV estimates can be sparse or heavily interpolated on minor roads. |
| Off-peak Fraction Feature | Free-flow speeds increase severity during quiet hours. | WebTRIS | 47,000 crashes | 2.1M links | Stage 2 / feature engineering | Low | Highly correlated with rural/urban designations; ensure no multicollinearity issues. |
| Hard-shoulder specific diagnostics | Proves hard shoulders behave differently than live lanes. | STATS19 Location codes | 776 HS crashes | UK-wide | validation / diagnostic | Medium | Mapping STATS19 hard-shoulder flags back to OS link geometries perfectly can be ambiguous. |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Generalized Ordered Logit with Post-crash features | Uses variables (fatigue, CFs, single-vehicle status) that are completely unknown prior to the collision, causing leakage. | Pre-event exposure data | 47,000 crashes | N/A (Method mismatch) | Frame Stage 2 as a pure pre-event frequency model. Use these variables only for post-hoc diagnostic grouping. | High |

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? N/A (It is a severity-given-crash model, not a frequency model).
- Does it suggest better handling of AADT/AADF uncertainty? No.
- Does it suggest useful geometry or road-context features? Yes. The impact of HGVs and time-of-day traffic profiles.
- Does it suggest better modelling of junctions? No.
- Does it suggest better treatment of severity? Yes. It highlights that the factors driving slight injuries are not perfectly parallel to those driving fatal injuries, supporting either distinct models for KSI vs slight, or sophisticated severity-weighting.
- Does it suggest better validation design? By negative example. It uses in-sample Pseudo R-squared and post-event features, illustrating the exact type of leakage Open Road Risk must avoid.
- Does it expose a weakness in my current approach? If Open Road Risk treats all motorway links homogeneously, it will overlook the massive specific risk variance of breakdown/hard-shoulder events.

## 15. Repo Actionability

1.  Suggested repo action: Implement "HGV Fraction" as a candidate feature in Stage 2.
    - Action type: candidate feature
    - Relevant stage: Stage 2
    - Why the paper supports it: The paper quantitatively isolates HGV involvement as a major driver of severe and fatal outcomes across both main carriageway and hard shoulder settings.
    - Evidence quote or page reference: Table 2 (Beta = +0.3353 for MC; +0.7565 for HS).
    - Effort: low
    - Risk if implemented badly: HGV estimates on non-trunk roads are often heavily imputed by DfT; this feature might inject noise on minor roads.

2.  Suggested repo action: Implement "Off-peak Traffic Fraction" (derived from WebTRIS profiles) as a Stage 2 feature.
    - Action type: candidate feature
    - Relevant stage: Stage 2
    - Why the paper supports it: Non-peak hours correlate with higher accident severity, likely due to free-flow travel speeds compared to congested peak hours.
    - Evidence quote or page reference: "The model illustrates that if the hour is non-peak, the severity tends to be higher." (Page 6)
    - Effort: low
    - Risk if implemented badly: None.

3.  Suggested repo action: Create a diagnostic slice evaluating model residuals specifically for crashes flagged in STATS19 as "Hard Shoulder".
    - Action type: diagnostic
    - Relevant stage: validation
    - Why the paper supports it: The severity profile is extreme (~5x higher serious/fatal proportion). If your baseline model systematically under-predicts risk on links with high hard-shoulder crash rates, this diagnostic will catch it.
    - Evidence quote or page reference: Table 1 (Frequency and relative frequency of main carriageway and hard-shoulder accidents).
    - Effort: low
    - Risk if implemented badly: None.

## 16. Query Tags

- motorway-accidents
- accident-severity
- hard-shoulder
- generalized-ordered-logit
- HGV-involvement
- time-of-day-severity
- off-peak-speed
- post-event-leakage
- STATS19-contributory-factors
- in-sample-diagnostic

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: The exact method the police use to guarantee the "first point of impact" is accurately recorded to separate Hard Shoulder from Main Carriageway accidents.
- Parts of the paper that need manual checking: If using the STATS19 Hard Shoulder flag for diagnostics, confirm the exact STATS20 variable encoding used to replicate their cohort isolation.
- Any likely ambiguity or risk of misinterpretation: The paper states it analyzes the "factors affecting motorway accident severity," but uses variables like "number of vehicles involved" and "number of casualties." These are *definitions* or *outcomes* of the crash mechanics, not predictive prior factors. Open Road Risk must not mistake these for predictive engineering features.