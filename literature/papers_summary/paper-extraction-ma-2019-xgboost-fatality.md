# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: analyzing-the-leading-causes-of-traffic-fatalities-using-1jznp146gl.pdf
- Suggested Markdown filename: paper-extraction-ma-2019-xgboost-fatality.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 14-page paper accessible. All tables and figures readable.

---

## 1. Citation

- Title: Analyzing the Leading Causes of Traffic Fatalities Using XGBoost and Grid-Based Analysis: A City Management Perspective
- Authors: Jun Ma, Yuexiong Ding, Jack C. P. Cheng, Yi Tan, Vincent J. L. Gan, Jingcheng Zhang
- Year: 2019
- DOI or URL: https://doi.org/10.1109/ACCESS.2019.2946401
- Country / region studied: USA (Los Angeles County, California)
- Study setting: mixed (urban and peri-urban/rural areas within LA County)

---

## 2. Core Objective

- One-sentence description: The paper builds an XGBoost binary classifier to identify which features most strongly differentiate fatal from non-fatal accidents in a large police-reported crash dataset, then uses GIS grid-based spatial analysis to map the geographic distribution of those features against fatality rates.
- Main purpose: factors analysis / descriptive analysis / classification (not prediction of collision occurrence; not an SPF)
- Evidence quote or page reference: "The objective of this paper is to propose a Grid-based non-linear machine learning framework to analyze the critical factors that influence traffic accidents fatality." (p. 148060)

---

## 3. Response Variable

- Target variable: Binary — whether an accident involves a fatality (fatal = negative class; non-fatal = positive class)
- Collision type: all crashes with fatality indicator; fatal vs. non-fatal; injury severity of surviving parties not separately modelled
- Severity handling: Collapsed to binary (fatal / non-fatal). Severity gradient within injury crashes is not modelled.
- Count, binary, rate, risk score, severity class, or other: binary classification
- Time window used for outcomes: 2010–2012 (3 years combined, cross-sectional)
- Evidence quote or page reference: "3,146 fatal accidents are marked as negative cases while 304,825 non-fatal accidents are marked as positive cases." (p. 148062, Table 1)

---

## 4. Exposure Handling

- Exposure variable used, if any: None used in the XGBoost classification model. Traffic volume is absent from the main model.
- Traffic count source: Not used. The paper explicitly acknowledges this as a limitation: "Due to the availability of the data, some possible influential factors, such as traffic volume, education, and road width, are not considered for different grids." (p. 148070)
- Whether exposure is modelled, observed, assumed, or ignored: Ignored in the main classification model. The grid-based fatality rate (fatal accidents / total accidents) is not exposure-adjusted; it is a conditional severity rate given that an accident has occurred, not an exposure-normalised collision rate.
- Treatment of missing or sparse traffic counts: Not addressed.
- Whether offset terms, rates, denominators, or normalisation are used: No offset. Grid-based fatality rate R_f = N_f / N_a (fatal count / total accident count per grid cell). This is a severity conditional rate, not a traffic-exposure rate.
- Evidence quote or page reference: "this study focuses on the grid-based fatality rate. Future work will try to integrate traffic volume data and analyze the influential factors on accident rates." (p. 148069)
- Transferability to my AADF/WebTRIS setup: low
- Notes: This paper's exposure handling is incompatible with Open Road Risk's approach. The paper's fatality rate (fatal/total accidents) is a conditional severity measure, not an exposure-normalised risk measure. Open Road Risk uses log(AADT × length × 365 / 1e6) as an exposure offset. These are fundamentally different quantities. The paper's own conclusion acknowledges that traffic volume should be incorporated in future work.

---

## 5. Spatial Unit of Analysis

- Unit: Grid cell (60×60 fishnet grid over Los Angeles County); individual point-level accident records are aggregated into grid cells for spatial analysis. The XGBoost model operates on individual accident records, not on spatial units.
- Segment length or segmentation rule: Grid cells derived by dividing LA County map into a 60×60 fishnet. Cell size not stated in metres or km.
- How crashes are assigned to the network: Point-level crash coordinates (POINT_X, POINT_Y from SWITRS) are used for spatial mapping. These location fields are excluded from the XGBoost feature set as "not the potential causes of accident fatality." (p. 148063)
- Treatment of junctions/intersections: INTERSECT_ (whether at an intersection) is included as a binary feature in the full feature set (Table 2) but does not appear in the top 15 important features (Figure 5). Its contribution to fatality classification is not discussed.
- Spatial aggregation risks: The grid-based analysis aggregates accidents by area, not by road link. Spatial patterns at 60×60 grid resolution will obscure link-level variation. Grid cells may contain heterogeneous road types and network densities. No spatial autocorrelation testing is reported.
- Evidence quote or page reference: "It is drawn by firstly cutting the Los Angeles County map in Figure 6 (3) into 60*60 grids." (p. 148065)
- Relevance to OS Open Roads link-based pipeline: Limited. The grid-based spatial analysis is an area-level visualisation tool, not a road-link-level modelling approach. The XGBoost feature importance analysis is the more relevant component for Open Road Risk.

---

## 6. Temporal Unit of Analysis

- Years covered: 2010–2012 (pooled, cross-sectional)
- Temporal resolution: Time of day (3-hour intervals via TIMECAT), day of week (DAYWEEK), year (YEAR_), month (MONTH_) all included as features. No panel or before-after structure.
- Whether seasonality or time-of-day is modelled: Time of day and day of week are included as features and both appear in top-15 important features. Seasonality by month is not discussed as a finding.
- Whether before-after or panel structure is used: No. Single pooled cross-section.
- Evidence quote or page reference: "It records every traffic accident reported in Los Angeles County during 2010-2012, totaling 307,971 accidents." (p. 148062)
- Relevance to WebTRIS-style time profiles: Indirect. The finding that overnight hours (0:00–6:00) have a fatality rate of 3.724% vs. 0.817% for 6:00–24:00 supports the relevance of time-of-day as a risk modifier. Open Road Risk has WebTRIS-based time profiles available; this paper provides supporting evidence that time-of-day matters for fatality severity, though the direction of causation is confounded by traffic volume, alcohol, and enforcement patterns.

---

## 7. Engineered Features

Only features that appear in the top 15 important features (Figure 5) or are explicitly discussed as top-8 findings are listed. The full feature set is 53 raw variables (Table 2) expanded to 350 after cleaning and dummy encoding.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| ETOH (alcohol involvement) | SWITRS collision record | Binary flag from police report | Top-ranked fatality predictor; fatality rate 4.645% with vs 0.714% without alcohol | Not available in STATS19 as a direct equivalent; STATS19 records "junction detail", "special conditions", but alcohol flags may be recorded differently — check STATS19 data dictionary |
| PARTIES (number of parties) | SWITRS collision record | Numeric count of parties involved | Second-ranked; fatality rate rises with party count; single-vehicle also high risk | Not directly in OS Open Roads; STATS19 includes number of vehicles; transferable |
| CRASHTYP_C (rear-end collision) | SWITRS collision record | Binary/categorical crash type flag | Rear-end has lowest fatality rate (0.385%); distinguishes fatal from non-fatal | STATS19 records collision type including rear-end; transferable for stage 2 feature |
| LIGHTING_A (daylight) / LIGHTING_C (poor lighting) | SWITRS environment record | Categorical lighting condition at time of crash | Daylight fatality 0.604% vs 2.038% other; poor lighting (no street lights or malfunctioning) highest | STATS19 records lighting conditions; transferable. OSM lighting data is sparse but available |
| PEDCOL (pedestrian involvement) / PED_A | SWITRS collision record | Binary flag | Pedestrian fatality rate 4.547% vs 0.673% without pedestrians | STATS19 records pedestrian involvement; transferable |
| MCCOL (motorcycle involvement) | SWITRS collision record | Binary flag | Motorcycle fatality rate 3.240% vs 0.912% without | STATS19 records motorcycle involvement; transferable |
| DAYWEEK (day of week) | SWITRS time record | Categorical (7 days); weekend vs weekday summarised | Weekend fatality rate 1.414% vs weekday 0.904% | Derivable from STATS19 date field; already present or easily added |
| TIMECAT (time of day) | SWITRS time record | 3-hour interval categories | 0:00–6:00 fatality rate 3.724% vs 0.817% other hours | Derivable from STATS19 time field; already present or easily added |

**Important note on feature leakage risk for Open Road Risk Stage 2:** Several features in the paper — particularly CRASHSEV (explicitly deleted as high-correlational to the target), KILLED, and INJURED — are post-event collision-derived variables. The paper correctly deletes CRASHSEV. However, ETOH, PARTIES, CRASHTYP_C, PEDCOL, MCCOL, LIGHTING_A are all collision-record features — they describe the accident itself, not the road/environment before the accident. These are post-event variables and would constitute leakage if used in a collision occurrence or risk percentile model. They are valid for a severity model (conditional on a collision having occurred), but not for Open Road Risk Stage 2 which predicts collision frequency.

---

## 8. Model Architecture

- Algorithms/models used: XGBoost (binary classification), compared against MLR, LR, MLP, SVM, RF
- Baseline model: Multiple Linear Regression (MLR) and Logistic Regression (LR)
- Final/preferred model: XGBoost (Accuracy 0.8673, Precision 0.8758, Recall 0.8562)
- Loss function or likelihood, if stated: Regularized objective with L1/L2 regularization (Equations 1–4); standard binary cross-entropy implied. Not explicitly stated.
- Offset/exposure term, if used: None.
- Spatial autocorrelation handling: Not addressed.
- Temporal dependence handling: Not addressed. Cross-sectional pooled data.
- Interpretability method: XGBoost feature importance based on split frequency (weight) across all CARTs (Equations 5–6). Partial dependence or SHAP values are not used.
- Evidence quote or page reference: "Importance of a variable v (Wv) based on the weights can be calculated by Equation 5 and Equation 6." (p. 148061)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Classification accuracy | Accuracy | 0.8673 | XGBoost | Best among 6 models compared | Table 3, p. 148064 |
| Classification accuracy | Precision | 0.8758 | XGBoost | Best among 6 models | Table 3, p. 148064 |
| Classification accuracy | Recall | 0.8562 | XGBoost | Best among 6 models | Table 3, p. 148064 |
| Baseline comparison | Accuracy | 0.7739 / 0.7854 | MLR / LR | Linear models substantially weaker | Table 3, p. 148064 |
| Baseline comparison | Accuracy | 0.8278 / 0.8280 / 0.8463 | MLP / SVM / RF | Non-linear models competitive but below XGBoost | Table 3, p. 148064 |
| Conditional severity rate | Fatality rate with alcohol | 4.645% | Accident records with ETOH | ~6.5× higher than non-alcohol rate | Table 4, p. 148065 |
| Conditional severity rate | Fatality rate without alcohol | 0.714% | Accident records without ETOH | Baseline rate | Table 4, p. 148065 |
| Conditional severity rate | Fatality rate with pedestrian | 4.547% | Pedestrian accidents | ~7× higher than non-pedestrian | Table 4, p. 148065 |
| Conditional severity rate | Fatality rate, motorcycle | 3.240% vs 0.912% | Motorcycle vs non-motorcycle | ~3.5× higher | Table 4, p. 148065 |
| Conditional severity rate | Fatality rate, poor lighting | 2.038% vs 0.604% | Non-daylight vs daylight | ~3.4× higher | Table 4, p. 148065 |
| Conditional severity rate | Fatality rate, overnight | 3.724% (0:00–6:00) vs 0.817% (6:00–24:00) | Time of day | ~4.6× higher overnight | Table 4, p. 148065 |
| Conditional severity rate | Fatality rate, weekend | 1.414% vs 0.904% weekday | Day of week | ~1.6× higher on weekends | Table 4, p. 148065 |

**Validation type:** 5-fold cross-validation for parameter optimisation. The reported accuracy figures in Table 3 use 5-fold cross-validation on the balanced dataset (under-sampled 10 times, results averaged). This is the strongest validation in the paper but still within-sample geographically — no spatial holdout or temporal holdout (the 2010–2012 period is pooled).

**Critical note on class balancing:** The dataset is severely imbalanced (3,146 fatal vs 304,825 non-fatal). The paper addresses this by repeated under-sampling (10 iterations, each with 3,146 negative + 3,146 randomly sampled positive cases = 6,292 cases per run). This is a reasonable but imperfect approach — the reported accuracy figures apply to the balanced 6,292-case dataset, not the original 1:97 ratio. Performance on the original imbalanced dataset (which represents real-world conditions) would be substantially different. The paper does not report AUC or other threshold-free metrics.

**Do these metrics test predictive generalisation?** Partially. 5-fold cross-validation on the balanced dataset provides weak within-sample generalisation evidence. The feature importance results (the paper's primary contribution) are not validated on held-out data.

**Are metrics likely to be optimistic?** Yes, for two reasons: (1) the balanced dataset is constructed by under-sampling the majority class, so accuracy on the real-world imbalanced distribution is not tested; (2) no spatial or temporal holdout is used.

**Most relevant metric to Open Road Risk:** The conditional fatality rates in Table 4 are descriptively useful for understanding severity drivers. The XGBoost accuracy metrics are less directly relevant since Open Road Risk uses a frequency model, not a binary fatality classifier.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The paper explicitly addresses class imbalance. Fatal accidents (3,146) represent approximately 1.02% of total accidents (307,971). The paper uses repeated under-sampling: 10 iterations, each drawing a balanced 3,146/3,146 dataset; results averaged.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Repeated under-sampling (not oversampling, not SMOTE, not focal loss). Poisson regression is listed as a tested alternative but not selected.
- Whether high-risk locations are evaluated separately: Yes — the grid-based GIS analysis identifies 8 spatial areas with elevated fatality rates and analyses their feature profiles separately.
- Evidence quote or page reference: "we combine both undersampling and parts of oversampling concept to balance their disadvantages. This is achieved by conducting the under-sampling ten times and calculate the average performance." (p. 148063)
- Practical relevance to my sparse collision link-year dataset: Limited. Open Road Risk's sparsity problem is collision occurrence frequency on road links (most link-years have zero collisions), not binary fatal/non-fatal classification. The under-sampling approach here would discard the vast majority of non-collision link-years if applied directly, which is inappropriate for a frequency model. The paper does not use Poisson or negative binomial regression, which are the standard approaches for Open Road Risk's count data.

---

## 11. Validation Strategy

- Train/test split method: 5-fold cross-validation on the balanced dataset (10 repeated under-sampling iterations, results averaged). No explicit train/test split percentage stated.
- Spatial holdout used? No
- Temporal holdout used? No (2010–2012 pooled)
- Grouped holdout used? No
- Cross-validation type: 5-fold cross-validation for parameter optimisation and model comparison
- Metrics: Accuracy, Precision, Recall (Figure 4 defines these from the confusion matrix)
- External validation: None
- Leakage or generalisation risks: Two concerns. First, the balanced dataset (repeated under-sampling) means the reported accuracy figures do not reflect real-world class ratios. Second, no spatial holdout means that patterns learned from one area of LA County are evaluated on adjacent areas — geographic autocorrelation likely inflates performance. Third, features like PARTIES and CRASHTYP_C describe the accident itself and could be considered outcome-proximate (though not strictly post-event leakage in the way KILLED or INJURED would be). The paper correctly removes CRASHSEV.
- Evidence quote or page reference: "Note that all the optimization process was conducted using 5-fold cross-validation to obtain stable results." (p. 148063)
- What I should copy or avoid: **Copy:** the approach of testing multiple algorithms (MLR, LR, MLP, SVM, RF, XGBoost) head-to-head on the same balanced dataset with cross-validation — this is a useful model comparison template. **Avoid:** treating accuracy on a balanced sub-sample as representative of real-world performance. **Avoid:** the absence of spatial holdout for any geographically-structured model comparison.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: In this Los Angeles County case study, XGBoost outperforms linear classifiers (MLR, LR) and other non-linear classifiers (MLP, SVM, RF) on binary fatality classification, with accuracy 0.8673 vs. 0.7739–0.8463 for alternatives, on a balanced dataset with 5-fold cross-validation.
- Why it matters: Provides supporting evidence for Open Road Risk's use of XGBoost in Stage 2 risk ranking. The paper demonstrates that XGBoost's non-linear handling of collision features captures interactions that linear models miss.
- Evidence quote or page reference: Table 3, p. 148064
- Confidence: Medium — this is a binary fatality classification task on a balanced dataset, not a Poisson count model for collision frequency. The domains are related but not identical.

**Finding 2:**
- Finding: The paper identifies that fatality rate (fatal/total accidents) varies substantially by time of day (3.724% overnight 0:00–6:00 vs 0.817% other hours) and day of week (weekends ~1.6× weekday rates). These are consistently high-importance features in the XGBoost model.
- Why it matters: Supports including time-of-day and day-of-week signals in severity or risk analyses. Open Road Risk's WebTRIS time profiles could be combined with STATS19 collision timing data to test whether overnight or weekend collision rates are disproportionately elevated at specific links.
- Evidence quote or page reference: Table 4, p. 148065
- Confidence: Medium — finding is from a US urban dataset; directional consistency with UK evidence is plausible but not certain.

**Finding 3:**
- Finding: Lighting condition is a top-8 fatality predictor. Accidents in dark conditions with absent or non-functioning street lights have substantially higher fatality rates than daytime accidents (approximately 3× higher in this study).
- Why it matters: Supports the relevance of lighting as a Stage 2 feature candidate. Open Road Risk lists OSM lighting as a candidate feature but notes sparse coverage. This paper provides evidence that the signal exists and is material. The limitation is that OSM lighting coverage in England is uneven.
- Evidence quote or page reference: Table 4 and Section V.D, p. 148068
- Confidence: Medium — LA County is heavily car-dependent with different pedestrian infrastructure to England; magnitude may not transfer directly.

**Finding 4:**
- Finding: The grid-based fatality rate (fatal/total accidents) is not spatially correlated with accident density. Higher-volume urban areas have more accidents but not necessarily higher fatality rates. Higher fatality rates in this study appear in peri-urban and mountainous areas (areas A–H in Figure 6).
- Why it matters: Directly relevant to Open Road Risk's distinction between collision frequency and risk-adjusted collision rate. This paper provides US evidence that raw accident counts and risk-adjusted rates diverge spatially, supporting the exposure-normalisation approach.
- Evidence quote or page reference: "the distribution of the fatality rate is not highly correlated with the accident density. This is because the density of accidents mostly relies on traffic volumes." (p. 148065)
- Confidence: High within this case study — the finding is conceptually robust and consistent with road safety literature.

**Finding 5:**
- Finding: The paper explicitly acknowledges that its fatality rate metric (fatal/total accidents) is a conditional severity measure, not an exposure-normalised accident rate. The authors state that integrating traffic volume data to analyse accident rates is future work.
- Why it matters: Confirms that the paper's "fatality rate" is not comparable to Open Road Risk's exposure-normalised risk percentile. The paper's grid-level fatality rates should not be used as a benchmark for Open Road Risk outputs.
- Evidence quote or page reference: "Fatality rates represent the rates of the fatal accidents over all the accidents, while accident rates mean the proportion of accidents over traffic volume. These are two different problems." (p. 148069)
- Confidence: High — stated explicitly by the authors.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Multi-algorithm comparison framework (XGBoost vs. LR vs. RF) | Open Road Risk Stage 2 uses XGBoost and Poisson GLM; adding RF as a comparison baseline would follow a similar head-to-head pattern | Existing Stage 2 data | 307,971 accident records, LA County | Compatible — Open Road Risk has ~21.7M link-year rows; manageable with sampling | Stage 2 — validation / baseline comparison | Low | Metrics differ (regression/count vs. binary classification); comparison design needs care |
| XGBoost feature importance (split-frequency weight) | Already used in Open Road Risk Stage 2; paper validates the general approach for road safety factor analysis | Existing Stage 2 data | Same as above | Compatible | Stage 2 — already present / documentation | Low | Split-frequency importance is less reliable than SHAP or permutation importance; already noted as a limitation in the paper |
| Time-of-day and day-of-week features | Paper confirms these are material fatality risk factors; STATS19 contains both; WebTRIS time profiles already available | STATS19 date/time fields (already available) | Same as above | Compatible | Stage 2 — candidate features | Low | These are crash-record features (post-event); must treat as characteristics of the collision context, not road features, for Stage 2 |
| Grid-based spatial visualisation of risk rates | Useful for exploratory communication of Stage 2 outputs | Stage 2 risk outputs | Same as above | Compatible — GIS fishnet grids can be overlaid on Stage 2 link-level outputs | Documentation / visualisation | Low | Grid aggregation obscures link-level variation; useful for communication, not for model development |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Binary fatality classification as the primary model task | Open Road Risk models collision frequency (count per link-year), not conditional severity (fatal vs. non-fatal given a collision occurred). These are different statistical problems. | N/A — data is available; issue is framing | LA County, 307,971 accidents | Not compatible as a production model | Run as a separate exploratory diagnostic on STATS19 fatal vs. non-fatal; do not replace Stage 2 | High |
| Under-sampling for class balance | Open Road Risk's imbalance problem is zero-heavy collision counts across link-years; Poisson/NB models handle this structurally. Under-sampling the majority class discards useful non-collision link-year data. | N/A | Same | Not appropriate for count frequency model | Poisson GLM with offset is already the correct approach for zero-heavy count data | High |
| Crash-record features (ETOH, PARTIES, CRASHTYP) as Stage 2 model inputs | These are post-event collision-describing variables. Using them in a collision frequency or risk percentile model would constitute leakage: they describe the accident after it happens, not the road characteristics before. | N/A — data available but leakage applies | Same | Not transferable for Stage 2 frequency model | Usable for a separate conditional severity model; exclude from Stage 2 feature set | High |
| Absence of exposure normalisation | The paper's fatality rate (fatal/total accidents) ignores traffic volume. For Open Road Risk, which explicitly accounts for AADT × length exposure, this metric cannot be adopted. | Traffic volume not included in paper | Same | Not compatible | Not applicable | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Yes, indirectly. The paper explicitly distinguishes fatality rate (fatal/total accidents) from accident rate (accidents/traffic volume) and acknowledges that traffic volume must be incorporated for the latter. This supports Open Road Risk's exposure-offset approach rather than challenging it.
- **Does it suggest better handling of AADT/AADF uncertainty?** No. Traffic volume is absent from the paper.
- **Does it suggest useful geometry or road-context features?** Partially. Lighting condition and road type (via crash type patterns) are relevant candidates. The paper does not use geometric road features directly.
- **Does it suggest better modelling of junctions?** No. INTERSECT_ does not appear in the top-15 features, and junction modelling is not discussed.
- **Does it suggest better treatment of severity?** Yes — the paper demonstrates that severity (fatal vs. non-fatal) is separable from frequency and that different factors drive each. This supports treating severity as a distinct modelling layer rather than collapsing it with frequency. Open Road Risk currently combines all injury collisions without severity weighting; this paper provides motivation for a separate severity diagnostic.
- **Does it suggest better validation design?** It provides a negative example: the absence of spatial holdout and the use of balanced sub-samples mean the reported accuracy does not reflect deployment conditions. Open Road Risk's grouped-by-link validation is already more rigorous.
- **Does it expose a weakness in my current approach?** Potentially: Open Road Risk's Stage 2 outcome combines all injury severity levels. If lighting condition, time of day, and vulnerable road user involvement disproportionately drive fatal severity (rather than all-injury frequency), the current Stage 2 model may not capture the highest-consequence risk locations well. A severity-stratified diagnostic could be worthwhile.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add a documentation note clarifying the distinction between Open Road Risk's exposure-normalised collision frequency model and conditional severity models (fatal/non-fatal classifiers). File this paper as an example of the latter, noting that its outputs are not comparable to Stage 2 risk percentiles.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper explicitly distinguishes fatality rate from accident rate (p. 148069) and provides a clear worked example of a severity-conditional approach.
- Evidence quote or page reference: "Fatality rates represent the rates of the fatal accidents over all the accidents, while accident rates mean the proportion of accidents over traffic volume." (p. 148069)
- Effort: Low
- Risk if implemented badly: Low.

**Action 2**
- Suggested repo action: Run a diagnostic comparing Stage 2 XGBoost risk percentile ranking against a simplified severity-stratified view: check whether the top-1% highest-risk links by XGBoost percentile show elevated proportions of fatal or serious injury collisions relative to slight injury. This would test whether the current Stage 2 model implicitly captures severity or only frequency.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper demonstrates that severity is a distinct signal from frequency, and that certain road/context conditions disproportionately drive fatality rather than collision occurrence. If Open Road Risk Stage 2 is frequency-weighted, high-fatality links may be under-ranked.
- Evidence quote or page reference: Table 4 fatality rate differentials, p. 148065
- Effort: Low–Medium (requires STATS19 severity field to be available in Stage 2 diagnostic outputs)
- Risk if implemented badly: Low — this is a diagnostic, not a production change.

**Action 3**
- Suggested repo action: Add lighting condition (OSM lighting tag) and time-of-day collision distribution (STATS19 time field) as candidate Stage 2 features, noting that they are crash-context variables (post-event in a strict sense) and should be treated as road environment descriptors — not as collision-derived leakage. Document the distinction.
- Action type: candidate feature / documentation note
- Relevant stage: Stage 2 — feature engineering
- Why the paper supports it: Lighting condition is a top-8 fatality factor in this study. OSM lighting is already listed as a candidate feature in Open Road Risk but noted as sparse. STATS19 time-of-day can be used to compute proportion of link-level collisions occurring overnight, which is a road environment signal.
- Evidence quote or page reference: Table 4 and Section V.D, p. 148068
- Effort: Low (time-of-day from STATS19 already parseable; OSM lighting already ingested but sparse)
- Risk if implemented badly: OSM lighting sparsity may introduce noise. Using collision-time features requires care to avoid mixing prediction and description — document clearly as descriptive context, not a causal driver.

**Action 4**
- Suggested repo action: Add RF (Random Forest) as a third baseline comparison alongside Poisson GLM and XGBoost in Stage 2 model comparison documentation, following the multi-algorithm comparison structure of this paper.
- Action type: baseline comparison / documentation
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper demonstrates the value of head-to-head algorithm comparison using consistent metrics and cross-validation. The XGBoost advantage over RF (0.8673 vs. 0.8463 accuracy) in this study is modest, and a UK collision frequency context may produce different results.
- Evidence quote or page reference: Table 3, p. 148064
- Effort: Low (RF is trivially addable to Stage 2 comparison if XGBoost pipeline is already set up)
- Risk if implemented badly: Low — diagnostic addition.

**Action 5**
- Suggested repo action: Document the leakage risk for collision-record features (crash type, number of vehicles, pedestrian involvement, motorcycle involvement) if these are ever considered for Stage 2 features. They describe the accident after it occurs and would leak collision information into a collision frequency model.
- Action type: documentation note
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: The paper uses these features for conditional severity classification (valid in that context). The repo dossier already lists "collision-derived context columns are treated as diagnostics and excluded from Stage 2 model features to avoid post-event leakage" — this paper provides a concrete worked example of why that guardrail exists.
- Evidence quote or page reference: Repo dossier section "Collision-derived context columns are treated as diagnostics and excluded from Stage 2 model features to avoid post-event leakage."
- Effort: Low
- Risk if implemented badly: Low — documentation only.

---

## 16. Query Tags

- XGBoost
- binary-classification
- fatality-severity
- conditional-severity-rate
- no-exposure-normalisation
- class-imbalance
- under-sampling
- feature-importance
- lighting-condition
- time-of-day
- day-of-week
- pedestrian-risk
- motorcycle-risk
- alcohol-driving
- GIS-grid-analysis
- US-case-study
- no-spatial-holdout
- post-event-leakage-risk
- severity-frequency-distinction
- multi-algorithm-comparison

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: The exact regression type used for the final model training (the optimisation notes XGBoost but the description of Poisson regression as tested is not followed up with results). Grid cell physical size not stated. AUC or other threshold-free metrics not reported — only Accuracy, Precision, Recall on balanced data.
- Parts of the paper that need manual checking: The description "lr=1.0" in Figure 2 caption is unusual for a learning rate (typically 0–1, exclusive); the paper states the optimal pair is {lr, n_estimators} = {1.0, 920} which may be a misprint or nonstandard parameterisation — worth checking if replicating.
- Any likely ambiguity or risk of misinterpretation: The paper's "fatality rate" (fatal/total accidents) must not be confused with Open Road Risk's exposure-normalised collision rate. The paper is a conditional severity classifier, not a collision frequency or risk prediction model. Feature importance from split-frequency weighting is sensitive to the number of categories in dummy-encoded variables (highly cardinal features will appear more important due to more splits) — this may inflate the apparent importance of multi-category features vs. binary features.