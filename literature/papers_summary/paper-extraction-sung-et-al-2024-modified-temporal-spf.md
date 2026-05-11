# Paper Extraction: Sung et al. (2024) — Development of Modified Temporal Safety Performance Function Considering Various Time Flows

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: Development_of_Modified_Temporal_Safety_Performanc.pdf
- Suggested Markdown filename: paper-extraction-sung-et-al-2024-modified-temporal-spf.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered in context as page images + text)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 11-page paper accessible. Tables 3–6 and Figure 2 fully legible. Figure 1 (data pipeline) legible. No OCR degradation issues.

---

## 1. Citation

- Title: Development of Modified Temporal Safety Performance Function Considering Various Time Flows
- Authors: Yeji Sung, Seunghwan Kim, Juneyoung Park, Ling Wang
- Year: 2024
- DOI or URL, if present: https://doi.org/10.1155/2024/7970454
- Journal: Journal of Advanced Transportation, Volume 2024, Article ID 7970454
- Country / region studied: South Korea — nationwide highway network
- Study setting: motorway / national highway (Korea Expressway Corporation network)

---

## 2. Core Objective

- One-sentence description: The paper develops a "modified temporal SPF" that predicts 15-minute crash risk on Korean national highways by ensemble-averaging four hourly SPF models with different 15-minute-offset start times, using Dirichlet-distribution-optimised weights, and compares this against traditional AADT, hourly, and 15-minute aggregation models.
- Main purpose: safety performance function development / predictive modelling / temporal aggregation comparison
- Evidence quote or page reference: "This study recognizes the importance of the 15 min time interval and proposes a new approach by developing a modified hourly model that aggregates data at fine-grained 15 min intervals (00, 15, 30, and 45 min, both at the beginning and end), instead of the traditional hourly data that starts and ends at the peak of each hour." (p. 1, abstract)

---

## 3. Response Variable

- Target variable: Crash frequency per segment per aggregation period (annual, hourly, or 15-minute)
- Collision type: Total crashes (all types combined); crash severity not stated as a filter; the paper uses "total crashes" from Korea Expressway Corporation data
- Severity handling: Not modelled separately; crash type not disaggregated
- Count, binary, rate, risk score, severity class, or other: count (crash frequency); at 15-minute resolution the counts are near-binary in practice (mean 0.048, max 2.0 per Table 2)
- Time window used for outcomes: 2018–2022 (5 years); averaged across years to produce annual average crash frequencies per segment per time period
- Evidence quote or page reference: "Three main datasets — VDS data, crash data, and geometric data — were collected from 2018 to 2022 in each of the 1092 segments." (p. 4)

---

## 4. Exposure Handling

- Exposure variable used, if any: Traffic volume (VDS-measured) at the matching aggregation level: AADT for annual models, Average Hourly Traffic (AHT) for hourly models, Average 15-minute Traffic (AMT) for 15-min models; also segment length and number of lanes as geometric exposure components
- Traffic count source: Vehicle Detector System (VDS) — permanent in-road sensors on all Korean national highway mainline sections; effectively full-coverage continuous counting
- Whether exposure is modelled, observed, assumed, or ignored: Directly observed from permanent VDS at 15-minute resolution; AADT and AHT are derived aggregations of this base data
- Treatment of missing or sparse traffic counts: Segments with missing traffic data due to detector errors removed from final dataset (1561 → 1095 segments retained)
- Whether offset terms, rates, denominators, or normalisation are used: Traffic volume enters as a predictor variable in the NB model (Equation 3–4), not as a log-offset. Segment length and number of lanes are separate independent variables. The NB model is of the form μ = exp(β₀ + β₁X₁ + ... + βₙXₙ + ε); no explicit log-offset for exposure is reported. Machine learning models treat volume as a feature.
- Evidence quote or page reference: "It usually uses traffic volume and section length as exposure coefficients." (p. 1); Equation 4 (p. 6)
- Transferability to my AADF/WebTRIS setup: **low for data; medium for structure**
- Notes:
  - The paper's key advantage — full-coverage VDS at 15-minute resolution for all 1,095 segments — does not transfer to Open Road Risk. AADF in UK covers only a fraction of links; WebTRIS covers National Highways sites only.
  - The mathematical concept (staggered hourly windows + ensemble averaging) is transferable in principle, but requires at minimum reliable hourly traffic estimates per link, which Open Road Risk does not currently have except via Stage 1b approximation.
  - The NB model structure (volume as feature rather than offset) differs from Open Road Risk's log-offset Poisson GLM; this is a methodological choice worth noting but not a transferability blocker.

---

## 5. Spatial Unit of Analysis

- Unit: Highway segment ("cone zone") — a section between consecutive interchange, junction, or tollgate nodes with constant traffic volume
- Segment length or segmentation rule: Variable; mean 7,544 m (SD 5,054 m), range 110–26,610 m (Table 2). Defined by Korea Expressway Corporation's operational segmentation, not fixed-length.
- How crashes are assigned to the network: Pre-assigned by Korea Expressway Corporation to segments; matching method not described in detail
- Treatment of junctions/intersections: Junctions (JC), interchanges (IC), and tollgates (TG) serve as segment boundaries, not modelling units; mid-segment analysis only
- Spatial aggregation risks: Variable segment length means longer segments have more exposure; length is included as a covariate but not as an offset, which may conflate length effects with flow effects
- Evidence quote or page reference: "A highway section with a constant number of passing vehicles, such as IC, JC, and TG, was treated as a segment." (p. 4)
- Relevance to OS Open Roads link-based pipeline: The segment definition is operationally similar to OS Open Roads links (both follow natural network units rather than fixed length). However, Korean highway segments average ~7.5 km — much longer than typical OS Open Roads links. Variable-length segments without a length offset introduce a known bias that Open Road Risk's log(length) offset avoids.

---

## 6. Temporal Unit of Analysis

- Years covered: 2018–2022 (5 years)
- Temporal resolution: Six aggregation levels tested: AADT (annual), AHT (hourly, starting :00), Modified AHT-15 (hourly, starting :15), Modified AHT-30 (hourly, starting :30), Modified AHT-45 (hourly, starting :45), AMT (15-minute, starting :00)
- Whether seasonality or time-of-day is modelled: Not explicitly modelled as factors; data are averaged across all years and all days to produce annual average values per period. No daytime/nighttime split, no peak/off-peak stratification — all hours treated as separate model instances.
- Whether before-after or panel structure is used: Panel (5 years per segment); averaged to annual mean per segment × time-period cell. No year fixed effects reported for NB model.
- Evidence quote or page reference: "averaging all the 15 min data across 2018–2022 generated 96 (15 min periods) of data for every segment." (p. 4)
- Relevance to WebTRIS-style time profiles: **Indirect.** The paper's motivation — that hourly aggregation with arbitrary start times misses temporal crash patterns — is consistent with Mensah & Hauer (1998) and Qin et al. (2006). The modified hourly / sliding window approach is a practical engineering solution to reduce start-time sensitivity, different from but complementary to the time-zone profile approach in Stage 1b.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Traffic volume at aggregation level (AADT / AHT / AMT) | VDS 15-min counts | Aggregated and averaged across 5 years per segment × time period | Primary exposure variable; tested at multiple temporal resolutions | Low for data: VDS full coverage not available in UK. Partial via Stage 1a AADT + Stage 1b fractions |
| Average speed at aggregation level | VDS 15-min speed | Aggregated and averaged | Speed as risk indicator; included alongside volume | Partial: not available at link level in Open Road Risk currently; OSM speed limits are a proxy |
| Traffic density at aggregation level | VDS-derived | Volume / speed / lanes | Captures congestion state; included alongside volume and speed | Low: requires continuous VDS; not available at scale |
| Volume 15 min before | VDS | Lagged 15-min volume preceding the observation window | Captures pre-crash traffic buildup; used as predictor in AHT models | Low: requires continuous per-link VDS |
| Speed 15 min before | VDS | Lagged 15-min speed | Pre-crash speed environment | Low: same constraint |
| Volume 30 min before | VDS | Lagged 30-min volume | Longer pre-crash window | Low |
| Fatigue Surrogate Index (FSI) — daily and time-zone | GPS/transponder vehicle tracking | CDTᵢ − α / α, where α = 120 min continuous driving threshold; summed per segment | Captures driver fatigue from continuous driving; Korea-specific | Very low: requires individual vehicle trajectory data; not available in UK open data |
| Speed limit | Road inventory | Raw field (80–110 km/h for Korean highways) | Controls for road environment | Already present in Open Road Risk via OSM |
| Segment length | Road inventory | Raw field (metres) | Exposure control; used as feature not offset | Already present in Open Road Risk; note paper uses as feature not log-offset |
| Number of lanes | Road inventory | Raw count | Controls for road capacity | Already present in Open Road Risk |

---

## 8. Model Architecture

- Algorithms/models used: Negative Binomial (NB) regression; Random Forest (RF); XGBoost (Extreme Gradient Boosting); LightGBM (LGBM); final ensemble: Dirichlet-weighted combination of four AHT RF models
- Baseline model: NB regression (HSM standard); AADT-level as standard reference
- Final/preferred model: Modified Temporal SPF = weighted ensemble of four RF models (AHT at :00, :15, :30, :45 starts), weights optimised via Monte Carlo search under Dirichlet distribution constraint; optimal weights w₀₀=0.071, w₁₅=0.011, w₃₀=0.859, w₄₅=0.059
- Loss function or likelihood, if stated: NB uses gamma-distributed error term for overdispersion (standard NB GLM); ML models use MSE/RMSE/MAD as evaluation criteria; weight optimisation minimises combined MSE/RMSE/MAD
- Offset/exposure term, if used: No log-offset; volume, length, and lanes enter as predictor variables in NB model (Equations 3–4). This is a notable methodological difference from Open Road Risk's log-offset structure.
- Spatial autocorrelation handling: Not addressed
- Temporal dependence handling: Not addressed; year-to-year variation absorbed by averaging across 5 years
- Interpretability method: R² for ML models; NB coefficients not reported (only GOF metrics); feature importance not reported
- Evidence quote or page reference: "The value of the optimized weight set is w₀₀=0.071189, w₁₅=0.010813, w₃₀=0.858779, and w₄₅=0.059219." (p. 8)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| R² in-sample (same aggregation) | R² | 0.834 | AADT XGBoost | Best single model at annual aggregation | Table 3, p. 8 |
| R² in-sample (same aggregation) | R² | 0.741 | AADT LGBM | Second best at annual level | Table 3 |
| R² in-sample (same aggregation) | R² | 0.609 | AADT RF | Third at annual level | Table 3 |
| R² in-sample (same aggregation) | R² | 0.676 | AHT LGBM | Best at hourly level | Table 3 |
| R² in-sample (modified AHT) | R² | 0.434 | Modified AHT30 RF and Modified AHT45 RF | Best RF models at modified hourly level | Table 4, p. 8 |
| Cross-aggregation prediction: 15-min crash frequency | RMSE | 0.141 | AMT LGBM | Best for predicting 15-min crashes from 15-min model | Table 5, p. 9 |
| Cross-aggregation prediction: 15-min crash frequency | RMSE | 0.180 | AHT RF | Best hourly model for predicting 15-min crashes | Table 5 |
| Modified Temporal SPF vs. AMT (15-min) model | RMSE | 0.172 vs. 0.225 | Modified Temporal SPF vs. AMT LGBM | Modified temporal SPF outperforms simple 15-min model on 15-min crash frequency prediction | Table 6, p. 9 |
| Modified Temporal SPF vs. AMT (15-min) model | MSE | 0.029 vs. 0.197 | Modified Temporal SPF vs. AMT LGBM | Large improvement in MSE | Table 6 |
| Modified Temporal SPF vs. AMT (15-min) model | MAD | 0.133 vs. 0.197 | Modified Temporal SPF vs. AMT LGBM | Meaningful improvement in MAD | Table 6 |

**Validation status:** Results are a mix of **in-sample R²** (Tables 3–4) and **random 8:2 train/test split** metrics (Tables 5–6). No spatial holdout, no temporal holdout, no grouped split by road link. The 8:2 split is random across segment × time-period observations, meaning training and test sets can share the same road link in different years or time periods — this is a weak validation design that likely overestimates generalisation performance.

**Critical methodological concern — undersampling:** The 15-minute model training data was undersampled to a 1:1 crash/no-crash ratio (from ~18% crash rate). This dramatically changes the effective base rate and makes all 15-minute model metrics incomparable to real-world deployment conditions where crashes are rare. The reported RMSE/MAD values for the Modified Temporal SPF (Table 6) are evaluated on a similarly balanced 1:1 dataset, not on the natural class distribution. This is not acknowledged as a limitation in the paper.

**What these metrics test:** Predictive accuracy within a randomly split version of the training distribution (not external validation). R² tests in-sample explanatory power. The cross-aggregation comparison (Table 5) is the most informative evaluation but still uses random splits.

**Likely optimism:** High. Random split, balanced sampling, no grouped validation, Korean highway context only. R² of 0.83 for AADT XGBoost is plausible but not verified on held-out road links.

**Most relevant metric to Open Road Risk:** The cross-aggregation comparison (Table 5) showing that AHT RF outperforms AMT LGBM for predicting 15-minute crashes is the most conceptually relevant result — it suggests that hourly models generalise better to fine-grained prediction than purpose-built fine-grained models, which supports the argument for improving Stage 2's exposure conditioning rather than building a fully disaggregate model.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: At 15-minute resolution, crashes are rare (~18% of segment × period observations have ≥1 crash per Table 2 mean 0.048). The paper addresses this by **undersampling non-crash observations to 1:1 ratio** for training the 15-minute models. Annual and hourly models are not undersampled ("no imbalance existed").
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: NB regression (standard, not zero-inflated); undersampling for ML 15-min models; no zero-inflated or hurdle models
- Whether high-risk locations are evaluated separately: Not addressed
- Evidence quote or page reference: "In the 15 min aggregation dataset, there were 19,260 crash data points, accounting for approximately 18% of the entire dataset. To address the scarcity of crash data, under sampling of noncrash data was performed to match the number of crash data, resulting in a balanced 1:1 ratio for building the training data." (p. 7)
- Practical relevance to my sparse collision link-year dataset: The undersampling approach is not recommended for Open Road Risk. At link × year resolution, crash prevalence is ~1–2%, much lower than the paper's 18% at 15-minute Korean highway resolution. Undersampling to 1:1 would discard ~98% of the non-crash data and produce a model that over-predicts crash probability by a factor of ~50× relative to the true base rate. The NB GLM approach (which handles zero-heavy counts without resampling) used in Open Road Risk's Stage 2 is more appropriate.

---

## 11. Validation Strategy

- Train/test split method: Random 8:2 split of the final dataset for each aggregation level
- Spatial holdout used? No — random split does not ensure held-out road links
- Temporal holdout used? No — data averaged across years; no year held out
- Grouped holdout used? No — no grouping by segment ID
- Cross-validation type: Grid search cross-validation for hyperparameter optimisation (method not specified in detail); no k-fold CV reported for final model evaluation
- Metrics: R², MSE, RMSE, MAD
- External validation: None; single country, single road operator
- Leakage or generalisation risks: Random split likely allows the same road segment to appear in both training and test sets (different time periods or years). This is a standard data leakage pattern in panel datasets. Given that the data is averaged across years (reducing within-segment year-to-year variation), the effective leakage risk is moderate but real: the model learns segment-level characteristics that are present in both train and test.
- Evidence quote or page reference: "The models were trained by dividing the constructed training data into training and test sets in an 8:2 ratio." (p. 7)
- What I should copy or avoid:
  - **Copy:** The idea of evaluating model performance across aggregation levels using a common outcome (e.g., predicting annual 15-min crash frequency using models trained at different temporal resolutions). This cross-aggregation evaluation design is worth adopting for comparing Stage 2 model variants.
  - **Avoid:** Random splits for panel/link-year data; undersampling for rare-event count models; treating R² from random splits as evidence of generalisation.

---

## 12. Key Findings Relevant to My Project

**Finding 1**
- Finding: Hourly aggregation models (AHT) perform better than simple 15-minute models (AMT) when predicting 15-minute crash frequencies in cross-aggregation evaluation. The hourly RF model achieves RMSE 0.180 vs. AMT LGBM RMSE 0.141 for 15-min prediction — the AMT model is better on its own scale but the AHT model generalises more stably.
- Why it matters: This suggests that for Open Road Risk, improving the temporal conditioning of the hourly/annual model (e.g., via Stage 1b time-zone fractions) is likely more productive than building a purpose-built fine-grained model, which would require per-link traffic counts not available in UK open data.
- Evidence quote or page reference: Table 5 (p. 9); "a Modified Temporal SPF for 15 min predictions was developed" selecting AHT RF as the base model
- Confidence: **medium** — result is from one country with full VDS coverage; no external validation; undersampled test set

**Finding 2**
- Finding: The Modified Temporal SPF (ensemble of four RF models at :00/:15/:30/:45 start times with Dirichlet weights) outperforms the simple 15-minute AMT model on all three metrics (MSE 0.029 vs. 0.197; RMSE 0.172 vs. 0.225; MAD 0.133 vs. 0.197). This improvement is achieved without requiring per-15-minute traffic data at inference time — only hourly volume is needed.
- Why it matters: The ensemble approach demonstrates that combining models with overlapping temporal windows improves stability compared to a single fine-grained model. The concept is transferable to Open Road Risk's Stage 2 in principle: combining models trained on different temporal aggregations (or peak/off-peak subsets) and averaging predictions could improve robustness.
- Evidence quote or page reference: Table 6 (p. 9)
- Confidence: **low–medium** — the improvement is large but evaluated on a balanced 1:1 dataset, not the natural crash rate; optimised Dirichlet weights may be overfitted to the training distribution

**Finding 3**
- Finding: The optimal Dirichlet weight for the :30-minute start model is 0.859, while :00 (0.071), :15 (0.011), and :45 (0.059) have near-zero weights. This asymmetry suggests that the :30-minute offset window captures crash-relevant traffic patterns better than the conventional :00-start hourly window for this Korean dataset.
- Why it matters: This is a curious result whose interpretation is unclear — it may reflect the timing of Korean highway peak periods (where crashes tend to cluster in the second half of an hour) or may be an artefact of overfitting. It should not be transferred directly to UK roads without validation.
- Evidence quote or page reference: "w₀₀=0.071189, w₁₅=0.010813, w₃₀=0.858779, w₄₅=0.059219" (p. 8)
- Confidence: **low** — single country, no robustness check, likely dataset-specific

**Finding 4**
- Finding: XGBoost and LGBM consistently outperform NB regression across all aggregation levels (R² 0.83 vs. not reported for NB at AADT level; RMSE improvements in Table 5). The NB model is competitive at annual level but underperforms at hourly level.
- Why it matters: Consistent with Open Road Risk's current architecture where XGBoost drives the production risk percentile and the Poisson GLM is used for diagnostics. This paper provides additional evidence (from a large national dataset) that gradient boosting approaches outperform NB for crash frequency prediction, though the validation weakness limits confidence.
- Evidence quote or page reference: Tables 3–5 (pp. 8–9)
- Confidence: **medium** — consistent with literature but validated only on random splits

**Finding 5**
- Finding: The paper explicitly notes that the AADT-based model "may mask the safety effects of operational improvements to roadways" and that Korean highways have "high variation in traffic volumes by time of day" — motivating finer temporal resolution.
- Why it matters: This is an empirical confirmation, on a large national dataset, of the theoretical concerns raised by Mensah & Hauer (1998) and Qin et al. (2006). The Korean context (high temporal flow variation) may be more extreme than UK roads, but the direction of the concern is applicable.
- Evidence quote or page reference: "the use of the AADT in safety analysis may be too general for capturing all changes in traffic flow throughout the day, and may mask the safety effects of operational improvements to roadways." (p. 1)
- Confidence: **medium** for the general point; **low** for the specific magnitude of the effect in UK context

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Cross-aggregation evaluation: test Stage 2 model at multiple temporal granularities using a common outcome metric | Provides a principled way to compare Stage 2 model variants (e.g., with/without Stage 1b time fractions) | Existing Stage 2 outputs; STATS19 crash time-of-day | 1,095 segments, 5 years | Compatible; apply to road-type subsets first | Stage 2 / validation | Low–medium | Requires defining a common outcome metric across aggregation levels |
| Ensemble / weighted average of models trained on different temporal windows (e.g., peak vs. off-peak) | Reduces sensitivity to arbitrary time-window definitions; improves stability | Stage 1b time fractions; STATS19 time-of-day | 1,095 segments | Medium: feasible at road-type level; computationally feasible at full scale | Stage 2 / candidate model extension | Medium | Weight optimisation requires a held-out validation set; Dirichlet approach is susceptible to overfitting without proper holdout |
| Document the sliding-window concept as a candidate design for future temporal SPF refinement | Provides theoretical motivation for Stage 1b integration | None — documentation only | N/A | Compatible | Documentation | Low | None |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| 15-minute AMT model using VDS continuous counts | Requires per-link 15-min traffic counts for all segments | Full-coverage VDS (Korea Expressway Corp.) | 1,095 segments | Very low: UK open data has no equivalent for 2.17M OS Open Roads links | Not applicable at production scale; pilot only on WebTRIS-covered links | High |
| Fatigue Surrogate Index (FSI) | Requires individual vehicle GPS/transponder travel history; Korea-specific data product | Korea Expressway Corp. tracking data | Korea only | None | Not applicable | High |
| Undersampling to 1:1 crash/no-crash ratio | Inflates apparent crash rate; produces miscalibrated predictions at natural prevalence; inappropriate for count regression | Not a data constraint — a methodological choice to avoid | N/A | Not applicable — counterproductive | Use NB/Poisson GLM with proper rare-event handling | High |
| Dirichlet weight optimisation on training data | Without a properly held-out optimisation set, weights overfit to training distribution; not validated externally | Held-out optimisation set (not used in paper) | 1,095 segments | Low confidence in transferability of specific weights | Use cross-validation to optimise weights if adopting ensemble approach | Medium |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Indirectly yes — the paper uses volume as a predictor, confirms that AADT is inadequate for capturing temporal variation, and shows hourly volume improves model performance. It does not use a log-offset, so it does not directly validate Open Road Risk's offset structure.

- **Does it suggest better handling of AADT/AADF uncertainty?** No — the paper has full VDS coverage and does not address sparse count estimation (Stage 1a concern).

- **Does it suggest useful geometry or road-context features?** Speed and density at the observation period are included and likely contribute to ML model performance, but feature importance is not reported. Speed limit and number of lanes are standard features already in Open Road Risk.

- **Does it suggest better modelling of junctions?** No — junctions are segment boundaries, not modelled explicitly.

- **Does it suggest better treatment of severity?** No — severity not addressed.

- **Does it suggest better validation design?** Yes, by negative example: the paper's random-split, balanced-sample validation is weak, and this paper should be noted in documentation as a case where reported R² values are likely optimistic. Open Road Risk's grouped-by-link validation split is stronger than what is done here.

- **Does it expose a weakness in my current approach?** One minor weakness: the paper motivates finer temporal conditioning for SPFs, which reinforces the case for integrating Stage 1b time fractions into Stage 2. Otherwise, Open Road Risk's validation design (grouped split by road link) is already more rigorous than this paper's approach.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add a documentation note flagging the Modified Temporal SPF ensemble concept as a candidate future architecture if per-link hourly volume estimates become available (e.g., if Stage 1b coverage improves). Note the Dirichlet weight optimisation approach and its overfitting risk.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The ensemble of staggered hourly windows is a novel approach that addresses temporal aggregation sensitivity without requiring fine-grained data at inference time.
- Evidence quote or page reference: Equation 10 (p. 9); Table 6 (p. 9)
- Effort: low
- Risk if implemented badly: none (documentation only)

**Action 2**
- Suggested repo action: When reporting Stage 2 model performance, add a note in documentation that random train/test splits for panel (link × year) data overestimate generalisation performance, and that Open Road Risk's grouped-by-link split is more appropriate. Cite this paper as an example of the weaker design.
- Action type: documentation note
- Relevant stage: Stage 2 / validation / documentation
- Why the paper supports it: The paper uses random 8:2 splits on panel data, which allows the same link to appear in both train and test sets; this is a known limitation.
- Evidence quote or page reference: "The models were trained by dividing the constructed training data into training and test sets in an 8:2 ratio." (p. 7)
- Effort: low
- Risk if implemented badly: none

**Action 3**
- Suggested repo action: Add a documentation note warning against undersampling (or oversampling) for rare crash events in count regression models. The paper's 1:1 undersampling approach inflates apparent model performance and is not appropriate for Open Road Risk's link × year framework at ~1–2% crash prevalence.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper demonstrates the approach but does not evaluate on the natural class distribution; this is a methodological gap worth flagging.
- Evidence quote or page reference: "under sampling of noncrash data was performed to match the number of crash data, resulting in a balanced 1:1 ratio" (p. 7)
- Effort: low
- Risk if implemented badly: none

**Action 4**
- Suggested repo action: Run a diagnostic cross-aggregation comparison for Stage 2: evaluate the current Stage 2 model (trained on link × year with AADT offset) on a time-stratified outcome (e.g., peak-hour crash counts derived from STATS19 time-of-day). This mirrors the paper's cross-aggregation evaluation (Table 5) and would quantify how much temporal information the current annual model loses.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Table 5 shows that cross-aggregation evaluation is informative for understanding model temporal limitations; applying the same logic to Open Road Risk would reveal whether Stage 2 is missing temporal risk patterns.
- Evidence quote or page reference: Table 5 (p. 9): cross-aggregation evaluation design
- Effort: medium
- Risk if implemented badly: STATS19 time-of-day coding has some quality issues; aggregate to peak/off-peak rather than individual hours.

**Action 5**
- Suggested repo action: Note in the Stage 2 model documentation that the NB model used in this paper does not use a log-offset for exposure, unlike Open Road Risk's Poisson GLM. The two approaches are not directly comparable; the log-offset structure in Open Road Risk is theoretically better motivated (separates exposure from risk) but requires AADT estimation quality (Stage 1a) to be adequate.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Comparing Equation 4 (p. 6) with Open Road Risk's offset structure highlights a methodological choice worth documenting.
- Evidence quote or page reference: Equation 4 (p. 6): NSPF = exp(β₀ + β₁X₁ + ... + βₙXₙ + εᵢ) with no offset term
- Effort: low
- Risk if implemented badly: none

---

## 16. Query Tags

- modified-temporal-SPF
- sliding-window-aggregation
- 15-min-aggregation
- hourly-vs-AADT
- Dirichlet-ensemble-weighting
- negative-binomial
- XGBoost
- LightGBM
- random-forest
- Korean-highway
- VDS-required
- undersampling-bias
- random-split-weakness
- cross-aggregation-evaluation
- no-spatial-holdout
- no-severity-split
- no-external-validation
- temporal-SPF
- traffic-aggregation-level
- function-averaging-empirical

---

## 17. Confidence and Gaps

- Overall confidence in extraction: **high** for what the paper reports; **low** confidence in the transferability of specific numerical results
- Important details not stated in the paper:
  - NB model coefficients not reported (only GOF metrics); impossible to assess which variables are significant
  - Feature importance for RF/XGBoost/LGBM not reported
  - The weight optimisation procedure for the Dirichlet ensemble is described but the validation set used for optimisation is not distinguished from the test set — likely the same 20% holdout, meaning weights may be optimised on the test set (a form of leakage)
  - Crash severity filter not stated
  - Whether the 8:2 split is stratified by segment ID or purely random is not stated
  - Year-to-year crash trend not discussed; averaging across 2018–2022 may mask COVID-19 traffic changes (2020–2021)
- Parts of the paper that need manual checking:
  - Table 6 MSE comparison (0.029 vs. 0.197): the large gap between Modified Temporal SPF and AMT LGBM is surprising given that LGBM outperforms RF in most other comparisons; verify that the evaluation dataset is indeed comparable (both use the 1:1 balanced 38,520-row test set)
  - The Dirichlet weight optimisation description (Section 4.4) should be read carefully to confirm whether the Monte Carlo weight search uses the test set or a separate validation set
- Any likely ambiguity or risk of misinterpretation:
  - The paper's R² values (Tables 3–4) are from random splits and should not be directly compared to Open Road Risk's grouped-CV R² of 0.858 for XGBoost; the validation designs are different and the Open Road Risk metric is more conservative
  - The MSE improvement in Table 6 (0.029 vs. 0.197) is very large and may reflect the undersampled evaluation design rather than a genuine performance difference at natural crash prevalence
  - "Annual 15 min crash frequency" as an outcome (Table 5) means: average number of crashes per 15-min period per year per segment — a quantity close to zero for most segments; interpreting RMSE in absolute terms requires reference to the mean outcome (0.048 from Table 2)
