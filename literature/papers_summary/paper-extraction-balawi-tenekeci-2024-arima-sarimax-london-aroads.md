# Paper Extraction — Balawi & Tenekeci 2024

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Time_series_traffic_collision_analysis_of_London_hotspots__Patterns.pdf
- Suggested Markdown filename: paper-extraction-balawi-tenekeci-2024-arima-sarimax-london-aroads.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered in context as text + page images)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full paper accessible. However, several critical methodological details are absent or internally inconsistent (see Section 17). This extraction flags these issues explicitly throughout.

---

## CRITICAL PRE-EXTRACTION WARNING

**This paper has serious methodological problems that substantially limit its usefulness as a reference for Open Road Risk. The extractor flags the following before the structured extraction:**

1. **Wrong response variable.** The paper's primary response variable is "number of vehicles involved in an accident" (a per-collision characteristic), not "accident count" (a frequency outcome). An ARIMA model on daily counts of vehicles involved in accidents across four London A-roads is not an accident frequency prediction model in the road safety sense. This fundamentally misaligns with any SPF or link-level collision count framework.

2. **Correlation analysis is meaningless as stated.** Table 3 presents R-squared values between "number of vehicles" and STATS19 fields such as "Latitude" (R²=0.82), "Day of Week" (R²=0.82), and "Year" (R²=0.82). These values are implausibly high for raw STATS19 attributes and are inconsistent with what simple pairwise R² between unrelated STATS19 columns should produce. No explanation of how these were computed is given. These figures should not be taken as evidence of feature importance.

3. **SARIMAX produces negative predictions.** Table 7 (SARIMAX test data) shows negative predicted values (e.g., −15.107 on 02-12-2019, −5.171 on 04-12-2019) for a count variable that cannot be negative. This indicates a fundamental model specification error.

4. **The 80-20 train/test split is described but its temporal structure is unclear.** The paper states the training set "covered initial years" and validation evaluated "subsequent periods," but the ARIMA/SARIMAX test data tables (Tables 4, 7) show only December 2019 as holdout — a single month, not a structural temporal split.

5. **No exposure handling, no network link level.** The paper operates at corridor level (four A-roads as a whole) with daily time series of accident-related counts, not at segment × year level with exposure offsets.

6. **Overconfident claims.** The paper claims "statistically reliable formulation of the main factors" and presents results as generalizable globally from four London A-roads over four years. These claims are not supported by the analysis.

**Assessment: This paper has low methodological quality and near-zero transferability to Open Road Risk. It is documented here for completeness of the literature search. Do not use its findings as evidence for pipeline design decisions.**

---

## 1. Citation

- Title: Time series traffic collision analysis of London hotspots: Patterns, predictions and prevention strategies
- Authors: Mohammad Balawi, Goktug Tenekeci
- Year: 2024
- DOI or URL, if present: https://doi.org/10.1016/j.heliyon.2024.e25710
- Country / region studied: United Kingdom (London, A1, A3, A4, A6 corridors)
- Study setting: urban / mixed (London A-roads, urban and suburban portions)

---

## 2. Core Objective

- One-sentence description: The paper applies ARIMA and SARIMAX time series models to daily accident-related data from four London A-road corridors (2016–2019) to forecast accident frequency and identify contributing factors.
- Main purpose: accident frequency forecasting / descriptive analysis
- Evidence quote: "Predictive model development is conducted to analyse and forecast accident frequency using ARIMA and SARIMAX models" (Abstract, p. 1)
- **Extractor note:** Despite the stated objective of forecasting "accident frequency," the modelled variable appears to be "number of vehicles involved in accidents" per day (see Section 3 below), not a collision count per road segment.

---

## 3. Response Variable

- Target variable: "Number of vehicles" involved in accidents — this is the dependent variable in both the ARIMA and SARIMAX models, as explicitly stated in Table 6 ("Dependent Variable: number_of_vehicles") and Table 9.
- Collision type: All injury accident types included (fatal, severe, slight, plus "accidents with no reported injuries" mentioned p. 13). STATS19 injury data used but PDO inclusion is ambiguous.
- Severity handling: Not modelled separately. Severity is listed as a feature in the correlation table (R²=0.80 with number_of_vehicles) but is not the response variable.
- Count, binary, rate, risk score, severity class, or other: count (daily count of vehicles involved in accidents across the four A-road corridors in aggregate)
- Time window used for outcomes: daily; 2016–2019. Test period: December 2019 only (Table 4, Table 7).
- Evidence quote: "The ARIMA model was applied to the dataset with the objective of predicting the number of vehicles" (Section 4.3.3, p. 19); Table 6: "Dependent Variable: number_of_vehicles"
- **Critical extractor note:** "Number of vehicles involved in accidents" is a property of accident records (how many vehicles were in each collision), not the accident count itself. An ARIMA on this variable predicts daily total vehicle involvement, not daily accident frequency. This is a different quantity from what the paper claims to model.

---

## 4. Exposure Handling

- Exposure variable used: None. No traffic volume, AADT, or exposure offset is included in either model.
- Traffic count source: The paper acknowledges "the dataset obtained from the UK Department of Transport lacks certain crucial features like traffic flow" (Section 1.1, p. 3). DfT published traffic flows are mentioned as a mitigation but are not incorporated into the models.
- Whether exposure is modelled, observed, assumed, or ignored: ignored in both ARIMA and SARIMAX models.
- Treatment of missing or sparse traffic counts: Not addressed in modelling. Acknowledged as a limitation.
- Whether offset terms, rates, denominators, or normalisation are used: None.
- Evidence quote: "Missing Features: The dataset obtained from the UK Department of Transport lacks certain crucial features like traffic flow" (Section 1.1, p. 3)
- Transferability to my AADF/WebTRIS setup: Not applicable. The paper provides no exposure framework.
- Notes: The absence of any exposure denominator means the models cannot distinguish between high accident counts due to high traffic volume and genuinely elevated risk. This is a fundamental methodological gap relative to all other papers in this extraction series. The paper is aware of this but does not resolve it.

---

## 5. Spatial Unit of Analysis

- Unit: road corridor (four named A-roads in London: A1, A3, A4, A6) treated in aggregate as a single time series. No segment-level analysis.
- Segment length or segmentation rule: Not applicable. The paper states data was used for "entire length of all A-Road corridors in London" (Section 1.1, p. 3). No segmentation.
- How crashes are assigned to the network: Direct selection from STATS19 records for accidents located on A1, A3, A4, A6. No spatial snapping described.
- Treatment of junctions/intersections: Not addressed.
- Spatial aggregation risks: Very high. All accidents across entire lengths of four major corridors are aggregated into a single daily time series. Any spatial heterogeneity, road-type variation, or location-specific risk pattern is lost.
- Evidence quote: "focusing on a specific geographic area encompassing four major roads: A1, A3, A4, and A6" (Section 1, p. 2)
- Relevance to OS Open Roads link-based pipeline: None. The spatial unit is not compatible with link-level modelling.

---

## 6. Temporal Unit of Analysis

- Years covered: 2016–2019 (4 years; COVID-19 cited as reason for not extending to more recent years)
- Temporal resolution: daily (the ARIMA/SARIMAX time series appear to be daily based on Table 4 showing individual dates in December 2019)
- Whether seasonality or time-of-day is modelled: Seasonality is addressed via the SARIMAX seasonal components (seasonal period = 8 in the fitted model, Section 4.4.3). Seasonal decomposition plot (Fig. 8) shows monthly steps. Time of day is listed as a correlate in Table 3 but is not a model input.
- Whether before-after or panel structure is used: Simple time series. No panel, no before-after.
- Evidence quote: SARIMAX seasonal period of 8 (Table 9, p. 23) is an unusual value; if data is daily the seasonal period would typically be 7 (weekly) or 365 (annual). If monthly, a period of 8 is anomalous. Not stated.
- Relevance to WebTRIS-style time profiles: The paper's seasonal decomposition approach (STL or classical) is conceptually relevant to my Stage 1b time-zone profile work, but the paper does not describe the decomposition method in sufficient detail to be useful as a reference.

---

## 7. Engineered Features

The paper uses STATS19 fields as candidate features. Feature selection is described but the features actually entering the SARIMAX model are not fully stated. Table 3 lists R-squared values against "number_of_vehicles" — these are pairwise correlations, not model coefficients. Actual model features are not reported.

**Critical note on Table 3:** The R-squared values in Table 3 are described as measuring the "degree of correlation between the number of vehicles involved in accidents and different features." Values such as Latitude (0.82), Day of Week (0.82), Year (0.82), and Accident Severity (0.80) are implausibly high for simple pairwise correlations between raw STATS19 fields and a count variable within a single city corridor over 4 years. No explanation of how these were computed is provided. These figures are not reliable as evidence of feature importance and should not be used to support feature engineering decisions.

| Feature | Raw source | Engineering method | Why it matters (as stated) | Transferable to my pipeline? |
|---|---|---|---|---|
| Day of week | STATS19 | Extracted from date field | R²=0.82 (suspect — see note) | Not applicable to link-year model |
| Year | STATS19 | Extracted from date field | R²=0.82 (likely just trend capture) | Not applicable |
| Latitude | STATS19 | GPS coordinate from record | R²=0.82 (likely artefact of A-road spatial structure) | Not applicable |
| Accident severity | STATS19 | Ordinal code 1-3 | R²=0.80 — post-event variable; leakage if used as predictor | EXCLUDED from my pipeline — post-event variable |
| Speed limit | STATS19/road | Legal speed limit at accident location | R²=0.77 | Candidate in my pipeline; note endogeneity risk (see Chengye 2013 extraction) |
| Urban/rural area | STATS19 | Binary urban/rural classification | R²=0.76 | Already present in my pipeline |
| Road type | STATS19 | Road classification code | R²=0.72 | Already present |
| Hours of day | STATS19 | Hour extracted from timestamp | R²=0.72 | Not in my annual link-year model; relevant to Stage 1b time-zone work |
| Light condition | STATS19 | Coded field (daylight/darkness) | R²=0.47 | Not currently in my pipeline |
| Road surface conditions | STATS19 | Coded field (dry/wet/etc.) | R²=0.66 | Not currently in my pipeline |
| Weather condition | STATS19 | Coded field | R²=0.38 | Not currently in my pipeline |

**Important:** All of the above features are derived from STATS19 accident records (collision-derived context columns). Using them as predictors of accident frequency in the same dataset constitutes post-event leakage. The paper does not acknowledge this. These features tell you about accidents that already happened; they cannot be used to predict which locations will have accidents in future.

---

## 8. Model Architecture

- Algorithms/models used: ARIMA (AutoRegressive Integrated Moving Average) and SARIMAX (Seasonal ARIMA with Exogenous variables). Both applied as time series models to the aggregated daily "number_of_vehicles" series.
- Baseline model: Simple moving average or persistence model mentioned as benchmark concept (Section 3.2.7) but no actual baseline results are reported.
- Final/preferred model: ARIMA — stated as preferred based on lower MAE (15.56 vs SARIMAX 17.04) despite worse AIC/BIC than SARIMAX (ARIMA AIC 16230 vs SARIMAX AIC 15105).
- Loss function or likelihood: Maximum likelihood; AIC, BIC, and log-likelihood reported. MAE used for comparison.
- Offset/exposure term: None.
- Spatial autocorrelation handling: Not applicable (no spatial structure; corridor-level aggregate time series).
- Temporal dependence handling: ARIMA(5,4,7) — 5 AR terms, 4 differencing, 7 MA terms. Very high differencing order (d=4) for a count time series is unusual and suggests the series may have been non-stationary or the order selection was poorly constrained. SARIMAX(4,1,2)×(4,1,2,8) — seasonal period of 8.
- Interpretability method: Not applicable (no coefficients reported that relate features to accidents). The paper presents AIC/BIC/MAE only.
- Evidence quote: Table 6 (ARIMA): ARIMA(5,4,7); Table 9 (SARIMAX): SARIMAX(4,1,2)×(4,1,2,8), p. 20–23
- **Critical note on model order:** ARIMA(5,4,7) with d=4 (four rounds of differencing) is extremely unusual. Typically d=0, 1, or at most 2. d=4 on a daily count series suggests the series was not stationary even after three rounds of differencing, which would be unusual and warrants investigation. The paper does not discuss this. This order was selected by grid search over p∈{1..10}, d∈{3,4,5,6}, q∈{1..10}, which is an extremely wide search space and increases the risk of overfitting and spurious order selection.

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model fit | AIC | 16230.767 | ARIMA(5,4,7) | Higher AIC than SARIMAX (worse fit) | Table 6, p. 20 |
| Model fit | BIC | 16299.191 | ARIMA(5,4,7) | Higher BIC than SARIMAX (worse fit) | Table 6, p. 20 |
| Model fit | Log likelihood | −8102.384 | ARIMA(5,4,7) | Lower (more negative) than SARIMAX | Table 6, p. 20 |
| Model fit | AIC | 15105.141 | SARIMAX(4,1,2)×(4,1,2,8) | Lower AIC than ARIMA (better fit) | Table 9, p. 23 |
| Model fit | BIC | 15262.936 | SARIMAX(4,1,2)×(4,1,2,8) | Lower BIC than ARIMA (better fit) | Table 9, p. 23 |
| Model fit | Log likelihood | 7522.571 | SARIMAX(4,1,2)×(4,1,2,8) | Note: this is positive log likelihood; ARIMA reports negative. Inconsistent sign convention across tables — not comparable without clarification | Table 9, p. 23 |
| Predictive accuracy (holdout) | MAE | ~15.56 | ARIMA, December 2019 holdout | Average absolute error of ~15.6 vehicles/day | Section 4.3.2, p. 19 |
| Predictive accuracy (holdout) | MAE | ~17.04 | SARIMAX, December 2019 holdout | Marginally worse than ARIMA | Section 4.4.2, p. 23 |
| Correlation | R-squared | 0.82 | Latitude vs number_of_vehicles | Implausibly high — see Section 7 note | Table 3, p. 13 |
| Correlation | R-squared | 0.82 | Day of Week vs number_of_vehicles | Implausibly high — see Section 7 note | Table 3, p. 13 |

**Metric qualification:**

- All AIC, BIC, and log-likelihood values are **in-sample model comparison metrics only**. They do not test predictive generalisation.
- The MAE values on the December 2019 holdout are the only out-of-sample metrics. The holdout is a single month (30 days). This is an extremely short and temporally specific holdout (Christmas period, which the paper itself notes is anomalous). These MAE values are not reliable estimates of general prediction error.
- The ARIMA log likelihood (−8102) and SARIMAX log likelihood (+7522) have opposite signs, which is mathematically impossible for the same scale of data unless different likelihood formulations or data transformations were used. This inconsistency is not explained.
- The ARIMA is preferred based on lower MAE but has worse AIC and BIC than SARIMAX. The paper concludes ARIMA is better without acknowledging this contradiction.
- **Most relevant metric to Open Road Risk:** None. The response variable, spatial scale, temporal resolution, and absence of exposure all mean these metrics cannot inform my pipeline.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Not addressed. ARIMA and SARIMAX are continuous time series models not designed for count data with excess zeros. Applying them to a daily aggregate count series (number of vehicles) for four major London corridors means the counts are likely large enough that zeros are rare — but this is not a consequence of good methodology, it is a consequence of aggregating across a very large spatial area.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models: None. The paper does not use any count-data model.
- Whether high-risk locations are evaluated separately: No. All four A-roads are aggregated into a single series.
- Practical relevance: None. My pipeline has ~98–99% zeros at link-year level. An ARIMA on aggregated daily corridor-level counts is the opposite design choice; it hides exactly the sparse signal I need to detect.

---

## 11. Validation Strategy

- Train/test split method: 80-20 random split described in methodology (Section 3.2.5), but the actual holdout in results tables (Tables 4, 5, 7, 8) is December 2019 only — a 30-day period at the end of the dataset. These are inconsistent descriptions.
- Spatial holdout used: No
- Temporal holdout used: Partially — December 2019 used as test period. This is a single month (Christmas period), which is explicitly noted as seasonally anomalous.
- Grouped holdout used: No
- Cross-validation type: None
- Metrics: MAE reported for holdout period
- External validation: None
- Leakage or generalisation risks:
  - **STATS19 collision-derived fields used as features.** The paper uses accident severity, light condition, road surface conditions, and similar post-event STATS19 attributes as candidate features in the SARIMAX model. These fields are known only after an accident occurs; using them to predict accident counts is a form of post-event leakage.
  - The 80-20 split description (Section 3.2.5) appears to contradict the December 2019 test period in Tables 4 and 7. If the split is random rather than temporal, future data is used to train the model, which would be a leakage error for a time series.
  - The very short holdout (one month) evaluated during an anomalous period (Christmas) makes the MAE values unreliable for general prediction accuracy assessment.
- Evidence quote: "The dataset was split into an 80-to-20 ratio for model training and validation" (Section 3.2.5, p. 10)
- What I should copy or avoid:
  - **Avoid**: all aspects of this validation design. The collision-derived feature usage, ambiguous split methodology, and holiday-period holdout should not be replicated.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: The paper uses STATS19 data from the UK DfT (2016–2019) for four London A-road corridors, confirming that STATS19 open data is accessible and usable for time series analysis at corridor level.
- Why it matters: This is confirmation that STATS19 data is freely accessible and usable for analysis. This is already known and assumed in my pipeline.
- Evidence: Section 3.1, data collection description, pp. 6–7
- Confidence: high (trivially true; does not add new information)

**Finding 2:**
- Finding: The paper acknowledges that STATS19 lacks traffic flow data, which the authors identify as a "missing feature" that limits their analysis. DfT-published corridor-level traffic flows are mentioned as a partial substitute.
- Why it matters: Confirms that STATS19 alone is insufficient for exposure-normalised risk modelling — the same limitation that motivates my Stage 1a AADT estimation pipeline. This is background context, not a new finding.
- Evidence: Section 1.1, p. 3: "The dataset obtained from the UK Department of Transport lacks certain crucial features like traffic flow"
- Confidence: high (this is a known limitation, not a novel finding of this paper)

**Finding 3:**
- Finding: The paper identifies "hours of day," "light condition," and "road surface condition" as having moderate to high correlation (R²=0.47–0.72) with "number of vehicles" in STATS19 records. However, as noted in Section 7, these R-squared values are derived from accident records and therefore represent post-event correlations, not predictive features. Their high values likely reflect that more severe and daytime accidents involve more vehicles, not that time of day or light predict accident frequency.
- Why it matters: Provides no actionable feature engineering guidance for my pipeline. These are post-event accident characteristics, not road or traffic features predictive of future collision risk.
- Evidence: Table 3, p. 13
- Confidence: low (R-squared values are suspect; even if valid, features are post-event)

No further findings from this paper meet the threshold of relevance to Open Road Risk. The paper's core results (ARIMA/SARIMAX on corridor-level daily vehicle involvement) are not transferable to link-year collision frequency modelling.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

None. No technique from this paper transfers to my pipeline in a way that improves on what is already implemented or planned. The paper's contribution, such as it is, is confined to corridor-level temporal forecasting without exposure, which is not the modelling approach for Open Road Risk.

The seasonal decomposition methodology (STL or classical additive decomposition) is a general technique that is already well-documented in the Python statsmodels library. If I were to explore temporal trends in my Stage 2 outputs, I would not use this paper as the reference — I would use Box, Jenkins, Reinsel & Ljung (2015), which this paper itself cites.

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| ARIMA on daily corridor-level accident time series | Wrong spatial unit (corridor vs. link), wrong response variable (vehicles involved vs. collision count), no exposure | Traffic volume absent from model | 4 A-road corridors, London | Not applicable | Not applicable | High |
| SARIMAX with STATS19 fields as exogenous variables | Uses post-event accident attributes as predictors — leakage; no exposure; corridor-level aggregate | Post-event collision features not usable as risk predictors | 4 A-road corridors | Not applicable | Not applicable | High |
| R-squared correlation screening for feature selection | R-squared values are implausibly high and methodology is opaque; correlation between accident record attributes is not predictive feature selection | N/A | 4 corridors | Not applicable | Use SHAP or XGBoost feature importance instead | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Only negatively — by demonstrating what happens when exposure is omitted. The paper cannot distinguish high-risk corridors from high-volume corridors because it has no traffic volume denominator. This reinforces the importance of my Stage 2 exposure offset.

- **Does it suggest better handling of AADT/AADF uncertainty?** No. AADT is absent from the paper entirely.

- **Does it suggest useful geometry or road-context features?** No. The features examined are all post-event STATS19 attributes, not road geometry or context features usable for prediction.

- **Does it suggest better modelling of junctions?** No.

- **Does it suggest better treatment of severity?** No. Severity is used as a predictor of "number of vehicles" rather than being modelled as an outcome.

- **Does it suggest better validation design?** No. The validation design in this paper is weaker than my existing grouped link split.

- **Does it expose a weakness in my current approach?** No direct exposure of a pipeline weakness. Indirectly, it illustrates the risk of using STATS19 collision-derived attributes (light condition, road surface, accident severity) as model features — these appear to have high predictive power simply because they describe the accident itself, not because they identify risky road segments. My pipeline already guards against this by excluding collision-derived context columns from Stage 2 features.

---

## 15. Repo Actionability

**Action 1:**
- Suggested repo action: Add a documentation note to Stage 2 feature engineering explicitly flagging that STATS19-derived attributes (accident severity, light condition at accident, road surface condition at accident, weather condition at accident) must not be used as Stage 2 features. These are post-event characteristics that describe the collision rather than the road environment, and including them would constitute post-event leakage. Cite this paper as an example of the leakage risk and my own existing guardrail against it.
- Action type: documentation note
- Relevant stage: Stage 2 / feature engineering / documentation
- Why the paper supports it: The paper implicitly demonstrates the problem by treating accident severity, light condition, and road surface as "features" correlated with accident outcomes — their high correlations in Table 3 arise from the fact that these are recorded at the same time as the collision, not because they predict future accidents.
- Evidence: Table 3, p. 13; Section 7 feature selection discussion
- Effort: low
- Risk if implemented badly: None (documentation only)

No further repo actions are warranted from this paper. Its methodology does not support any pipeline changes.

---

## 16. Query Tags

- ARIMA
- SARIMAX
- time-series
- London-A-roads
- STATS19
- corridor-level
- no-exposure
- post-event-leakage
- low-transferability
- wrong-response-variable
- UK-data
- temporal-forecasting
- negative-predictions-error
- methodological-concerns
- do-not-use-as-evidence

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high confidence that the paper has the methodological problems described; low confidence that any findings are reliable
- Important details not stated in the paper:
  - How the R-squared values in Table 3 were computed. The methodology section mentions pairwise Pearson R; Table 3 header says "R-squared" but the values listed are R² values (0–1 scale). Values of 0.82 for Latitude vs. number_of_vehicles from a single London dataset over four years are not credible for simple pairwise linear regression without a major data error or methodological problem.
  - Which features were actually used as exogenous variables in the SARIMAX model. The pseudocode (Fig. 11) references "chosen_best_features" from an OLS feature selection step, but the specific features retained are not listed anywhere in the paper.
  - Why the ARIMA log likelihood is reported as negative (−8102.384) while the SARIMAX log likelihood is positive (7522.571). These should have the same sign if computed on the same data using the same software. This inconsistency is unexplained.
  - Whether the 80-20 split was random or temporal. If random, the model was trained on future data, which is leakage for a time series.
  - The exact response variable distribution. Are zeros present in the daily series? What is the mean count per day? These are not stated.
- Parts of the paper that need manual checking:
  - Table 3 R-squared values: these require independent verification before being cited as evidence of anything.
  - The ARIMA(5,4,7) order selection: d=4 is extremely unusual and should be independently verified against standard ARIMA diagnostics. The paper's grid search used d∈{3,4,5,6}, which excludes d=0, 1, 2 — the standard values. This suggests the grid search was misconfigured.
  - The log-likelihood sign inconsistency between Tables 6 and 9.
  - SARIMAX negative predictions in Table 7 should have caused model rejection; the paper reports them without comment.
- Any likely ambiguity or risk of misinterpretation:
  - The paper title, abstract, and conclusion use language that overstates both the rigour and generalisability of the findings. Phrases like "statistically reliable formulation of the main factors" and "global predictive and mitigation value" are not supported by the analysis. Anyone reading only the abstract would substantially overestimate the paper's contribution.
  - The paper is published in Heliyon, a broad-scope open-access journal with a different peer-review threshold than specialist transport safety journals. The methodological errors described above (wrong response variable, negative count predictions, implausible R-squared values) should have been caught in peer review.
  - This paper should not be cited in the Open Road Risk documentation as methodological support for any design decision.
