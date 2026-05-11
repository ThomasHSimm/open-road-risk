# Paper Extraction: Quddus (2007) — Time Series Count Data Models: An Empirical Application to Traffic Accidents

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: AAP_2007_INAR_revised_Final.pdf
- Suggested Markdown filename: paper-extraction-quddus-2007-inar-time-series-count.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered in context as page images + text)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 26-page accepted manuscript accessible. Tables 1–2 fully legible. Figures 1–6 visible (time series plots and ACF plots). Note: this is the Loughborough Repository accepted manuscript, not the final published version; cite accordingly.

---

## 1. Citation

- Title: Time Series Count Data Models: An Empirical Application to Traffic Accidents
- Authors: Mohammed A. Quddus
- Year: 2007 (accepted manuscript date 12 November 2007; published in Accident Analysis and Prevention)
- DOI or URL, if present: https://hdl.handle.net/2134/5308 (repository record)
- Journal: Accident Analysis and Prevention (publisher: Elsevier)
- Country / region studied: Great Britain (aggregated dataset); London congestion charging zone (disaggregated dataset)
- Study setting: national aggregate (GB annual fatalities) and urban area aggregate (London CC zone monthly casualties)

---

## 2. Core Objective

- One-sentence description: The paper introduces Integer-Valued Autoregressive (INAR(1)) Poisson models for time series accident count data and compares their performance against ARIMA, NB, and NB-with-trend models on two GB datasets: annual national fatalities (1950–2005) and monthly car casualties in the London congestion charging zone (1991–2005).
- Main purpose: methodological comparison / time series modelling / intervention analysis
- Evidence quote or page reference: "The primary objective of this paper is to introduce the class of integer-valued autoregressive (INAR) models for the time series analysis of traffic accidents in Great Britain." (p. 3, abstract section)

---

## 3. Response Variable

- Target variable: (1) Annual road traffic fatalities in Great Britain, 1950–2005 (n=55 years); (2) Monthly car casualties within the London congestion charging zone, January 1991–October 2005 (n=178 months)
- Collision type: (1) Fatalities only; (2) car casualties (injury severity not further specified — drawn from STATS19)
- Severity handling: Not modelled separately; dataset 1 is fatalities only; dataset 2 is casualties (all severities combined for the CC zone)
- Count, binary, rate, risk score, severity class, or other: counts (non-negative integers)
- Time window used for outcomes: Annual (dataset 1); monthly (dataset 2)
- Evidence quote or page reference: "The highly aggregated time series data considered in this study is the annual road traffic fatalities in GB between 1950 to 2005." (p. 6); "the monthly car casualties within the London congestion charging (CC) zone between January 1991 to October 2005." (p. 7)

---

## 4. Exposure Handling

- Exposure variable used, if any: (1) Annual vehicle-kilometres travelled (VKT) in GB — used as control variable; (2) Total monthly road traffic accidents in Greater London — used as exposure-to-risk control variable
- Traffic count source: (1) DfT Transport Statistics GB (VKT); (2) STATS19 / Transport for London (monthly London accidents)
- Whether exposure is modelled, observed, assumed, or ignored: Observed; included as a covariate (not as a log-offset). VKT enters as a continuous predictor in all models for dataset 1.
- Treatment of missing or sparse traffic counts: Not applicable; both datasets are aggregate counts over large spatial units with no missing observations stated
- Whether offset terms, rates, denominators, or normalisation are used: No explicit log-offset; exposure enters as a covariate. For dataset 2, ln(monthly accidents in Greater London) is used as a control variable (coefficient 0.87 in INAR(1), Table 2).
- Evidence quote or page reference: "The annual VKT data of GB are then collected from the DfT." (p. 6); "The total number of monthly road traffic accidents within greater London will be taken in all models as an exposure to risk of accidents." (p. 7)
- Transferability to my AADF/WebTRIS setup: **low for model class; medium for exposure concept**
- Notes: The paper's exposure handling (VKT or total accidents as covariate) is conceptually weaker than Open Road Risk's log-offset structure, which explicitly separates exposure from risk. The INAR model class is designed for pure aggregate time series, not for the cross-sectional link × year panel structure of Open Road Risk.

---

## 5. Spatial Unit of Analysis

- Unit: (1) Great Britain as a whole (single time series); (2) London congestion charging zone (single time series)
- Segment length or segmentation rule: Not applicable — both datasets are spatially aggregated to a single geographic unit
- How crashes are assigned to the network: Pre-assigned to geographic units by DfT / TfL / STATS19; no spatial matching methodology discussed
- Treatment of junctions/intersections: Not applicable
- Spatial aggregation risks: Entire analytical approach is based on single-location time series; spatial heterogeneity within GB or within the CC zone is not modelled
- Evidence quote or page reference: Not stated beyond dataset descriptions
- Relevance to OS Open Roads link-based pipeline: **Low.** Open Road Risk operates at individual link level with ~2.17M links. The INAR model as applied here is for a single time series (one observation per time period for one spatial unit). It does not scale to cross-sectional or panel link-level data without substantial extension.

---

## 6. Temporal Unit of Analysis

- Years covered: Dataset 1: 1950–2005 (55 years); Dataset 2: January 1991–October 2005 (178 months)
- Temporal resolution: Annual (dataset 1); monthly (dataset 2)
- Whether seasonality or time-of-day is modelled: Seasonality is explicitly modelled in dataset 2 via SARIMA seasonal differencing and seasonal MA components (SMA1, SMA2). The INAR(1) model does not directly handle seasonality — this is flagged as a limitation.
- Whether before-after or panel structure is used: Intervention analysis (before-after) using step-function dummy variables: seat-belt law 1983, safety legislation 1989 (dataset 1); London congestion charge February 2003 (dataset 2)
- Evidence quote or page reference: "The paper ends with a discussion on the limitations of INAR models to deal with the seasonality and unobserved heterogeneity." (p. 3, abstract)
- Relevance to WebTRIS-style time profiles: Low direct relevance. The paper's temporal analysis is at annual/monthly aggregate level, not at hourly or sub-hourly level.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Annual VKT (GB) | DfT Transport Statistics | Raw annual total | Exposure control for national-level trend model | Not directly applicable at link level; analogous to national AADF trends |
| Seat-belt law intervention (1983) | Policy record | Binary step-function dummy (0 before, 1 from 1983 onward) | Captures permanent effect of a road safety policy change | Low: Open Road Risk does not currently model policy interventions |
| Safety legislation intervention (1989) | Policy record | Binary step-function dummy | Same | Low |
| London CC zone intervention (Feb 2003) | TfL | Binary step-function dummy | Captures ~27% casualty reduction post-charge | Potentially useful as a reference for evaluating policy effects in UK road safety context |
| ln(monthly accidents in Greater London) | STATS19 / TfL | Log of total monthly accidents in wider area | Exposure-to-risk proxy for the CC zone subset | Concept transferable: using a wider-area crash count as an exposure proxy for a subarea |
| Serial correlation diagnostics (ACF plots) | Modelled data | Sample autocorrelation function | Identifies serial correlation structure in time series count data | Relevant diagnostic for any temporal trend analysis in Open Road Risk |

---

## 8. Model Architecture

- Algorithms/models used: ARIMA(1,1,1) / SARIMA(0,1,1)×(0,1,2)₁₂; Negative Binomial (NB) regression; NB with linear time trend; INAR(1) Poisson
- Baseline model: NB regression (standard road safety practice)
- Final/preferred model: ARIMA for aggregated annual data (best RFE); INAR(1) Poisson for disaggregated monthly data (best RFE and within-sample fit)
- Loss function or likelihood, if stated: ARIMA uses SIC for model selection; NB uses log-likelihood; INAR(1) uses Exact Maximum Likelihood (EM algorithm, Karlis 2006)
- Offset/exposure term, if used: No log-offset; exposure enters as covariate
- Spatial autocorrelation handling: Not applicable
- Temporal dependence handling: ARIMA/SARIMA handles serial correlation via AR/MA components; INAR(1) handles it via binomial thinning operator α on lagged count Yₜ₋₁; NB ignores serial correlation (identified as a weakness)
- Interpretability method: Coefficient tables with t-statistics (Tables 1–2); ACF plots for serial correlation diagnosis; within-sample fit metrics and out-of-sample RFE

**INAR(1) model structure:**
The INAR(1) Poisson model replaces standard AR(1) scalar multiplication with a binomial thinning operation:

    Yₜ = α ∘ Yₜ₋₁ + eₜ

where α ∘ Yₜ₋₁ = Σᵢ uᵢ (sum of Yₜ₋₁ independent Bernoulli trials with success probability α), and eₜ ~ Poisson(λₜ) is the innovation term. The mean and variance of the process are both λ/(1−α). α is the "thinning parameter" representing temporal autocorrelation.

- Evidence quote or page reference: Equations 4–6 (pp. 5–6)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Within-sample fit, aggregated annual data | MAPE | 4.73% | ARIMA(1,1,1) | Best within-sample fit for annual GB fatalities | Table 1, p. 21 |
| Within-sample fit, aggregated annual data | MAPE | 23.27% | NB with trend | Worst fit — NB + trend performs poorly for long time series | Table 1 |
| Within-sample fit, aggregated annual data | MAPE | 23.52% | INAR(1) Poisson | Similar to NB; worse than ARIMA for high-count annual data | Table 1 |
| Out-of-sample forecast error, annual data | RFE (2001–2005) | 2.79% | ARIMA(1,1,1) | Best forecast accuracy for annual fatalities | Table 1 |
| Out-of-sample forecast error, annual data | RFE | 5.97% | INAR(1) Poisson | Second best for annual data | Table 1 |
| Thinning parameter, annual data | α | 0.125 (t=3.02) | INAR(1), annual GB | Low but significant temporal autocorrelation in annual fatalities | Table 1 |
| Within-sample fit, disaggregated monthly data | MAPE | 18.23% | INAR(1) Poisson | Best within-sample fit for monthly CC zone casualties | Table 2, p. 22 |
| Within-sample fit, disaggregated monthly data | MAPE | 25.27% | SARIMA | Worst fit for monthly data | Table 2 |
| Out-of-sample forecast error, monthly data | RFE (Jan–Oct 2005) | 0.91% | INAR(1) Poisson | Best forecast accuracy for monthly casualty data | Table 2 |
| Out-of-sample forecast error, monthly data | RFE | 1.36% | SARIMA | Worst forecast accuracy for monthly data | Table 2 |
| Thinning parameter, monthly CC zone data | α | 0.355 (t=10.46) | INAR(1), monthly CC | Substantial temporal autocorrelation in monthly casualties | Table 2 |
| Intervention effect, congestion charge | Coefficient | −0.308 (t=−4.68) | INAR(1), monthly CC | Introduction of London CC reduces car casualties by ~27% | Table 2 |
| Overdispersion parameter | k | 0.0110 (t=3.67) | NB, monthly CC | Significant overdispersion in monthly casualty counts | Table 2 |

**Validation status:** Train/test temporal split — all models trained on early period, validated on withheld recent observations (2001–2005 for annual; Jan–Oct 2005 for monthly). This is a **temporal holdout**, which is the appropriate validation design for time series data.

**What these metrics test:** Forecasting accuracy for aggregate time series counts at national/city level. These are not cross-sectional link-level predictions; they are temporal extrapolations for single spatial units.

**Most relevant metric to Open Road Risk:** The thinning parameter α = 0.355 for monthly CC zone data indicates that approximately 35% of the accidents in one month persist (as a stochastic carry-over) into the next month, after controlling for exposure. This quantifies the magnitude of serial correlation in UK urban monthly crash counts — directly relevant to understanding whether ignoring temporal autocorrelation in Open Road Risk's link × year panel model introduces bias.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Dataset 1 (annual national fatalities, mean ~5,769) has no zero-count or rarity issue. Dataset 2 (monthly CC zone casualties, mean ~61) is also not particularly sparse, though it is over-dispersed (variance 239.77 vs mean 60.98, ratio ~3.9).
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson (INAR(1)); Negative Binomial; ARIMA/SARIMA. No zero-inflated or hurdle models — not needed given the mean counts involved.
- Whether high-risk locations are evaluated separately: Not applicable — single spatial unit
- Evidence quote or page reference: "For cross-sectional count data that contain many zero observations (i.e., excess zero-count data), then a zero-inflated Poisson (or NB) model or the Hurdle count data model is more appropriate." (p. 5) — cited as background, not applied here
- Practical relevance to my sparse collision link-year dataset: The paper explicitly notes that standard NB and Poisson models assume observations are independent. For Open Road Risk's panel structure (same road link observed over multiple years), this independence assumption is violated — year-to-year serial correlation within a link is analogous to the temporal autocorrelation this paper addresses. The magnitude of the problem depends on the autocorrelation structure; the paper suggests this matters most when mean counts are low.

---

## 11. Validation Strategy

- Train/test split method: Temporal holdout — early observations for training, most recent observations for validation
- Spatial holdout used? Not applicable (single spatial unit)
- Temporal holdout used? Yes — dataset 1: 1950–2000 train / 2001–2005 test; dataset 2: Jan 1991–Dec 2004 train / Jan–Oct 2005 test
- Grouped holdout used? Not applicable
- Cross-validation type: None; single temporal split
- Metrics: MAPE, MAD, MSD, RMSE (within-sample); RFE (out-of-sample)
- External validation: None; both datasets are from GB
- Leakage or generalisation risks: Temporal split is appropriate for time series; no leakage concern. However, a 5-observation (years) or 10-observation (months) holdout is very short and validation metrics have high variance.
- Evidence quote or page reference: "Each of the datasets is divided into two parts. One part is used to estimate the model parameters and the other part is used to validate the corresponding model." (p. 7)
- What I should copy or avoid: The temporal holdout design is the correct approach for time series count data. For Open Road Risk's panel data, the analogous design is a temporal holdout (hold out most recent year(s)) combined with a grouped-by-link spatial holdout — more rigorous than either alone.

---

## 12. Key Findings Relevant to My Project

**Finding 1**
- Finding: Standard NB models (without a serial correlation correction) perform substantially worse than INAR(1) or ARIMA for both time series datasets. MAPE for NB with trend is 23.27% vs. 4.73% for ARIMA on annual data. This is because NB assumes independent observations, which is inappropriate for serially correlated time series count data.
- Why it matters: Open Road Risk's Stage 2 Poisson GLM with a grouped-by-link split partially addresses this by not training and testing on the same link. However, if year-to-year crash counts on the same link are serially correlated (which the paper suggests is likely), the GLM's standard errors may be underestimated, inflating apparent statistical significance of coefficients. This is a diagnostic concern.
- Evidence quote or page reference: "Modelling time series count data using these [NB/Poisson] models may result in inefficient estimates of the parameters as time series data are normally serially correlated." (p. 2)
- Confidence: **high** for the general principle; **medium** for the magnitude in Open Road Risk's specific panel structure

**Finding 2**
- Finding: For low-count time series (monthly CC zone data, mean ~61), INAR(1) Poisson outperforms ARIMA both within-sample (MAPE 18.23% vs 25.27%) and out-of-sample (RFE 0.91% vs 1.36%). The integer-valued property and Poisson distribution of the innovations matter when counts are low. For high-count annual data (mean ~5,769), ARIMA performs best because the normal approximation is adequate.
- Why it matters: Open Road Risk's link-year crash counts are very low (mean well below 1 for most links). If any aggregate temporal trend model is ever needed (e.g., for calibration or policy monitoring), INAR(1) Poisson would be more appropriate than ARIMA.
- Evidence quote or page reference: "The integer-valued discrete property of count data is not so important if the mean of the counts associated with a time series process are high. However, if the counts associated with a time series process exhibit low values, the distribution of count data follows a Poisson distribution and the properties of integer-valued count data becomes important." (p. 11)
- Confidence: **high** for this case study; **medium** for generalisation

**Finding 3**
- Finding: The thinning parameter α = 0.355 for the London CC zone monthly data indicates that ~35% of one month's casualty count carries over stochastically into the next month, after controlling for exposure. This is meaningful temporal autocorrelation that NB ignores.
- Why it matters: For Open Road Risk's link × year panel, the analogous quantity is the year-to-year within-link autocorrelation. If a similar magnitude of autocorrelation exists at link × year level, clustering standard errors by link (or using a random-effects model) is necessary for valid inference on GLM coefficients. The current grouped-split validation addresses predictive leakage but does not explicitly correct for within-link autocorrelation in coefficient standard errors.
- Evidence quote or page reference: "Thinning parameter: 0.3545 (t=10.46)" (Table 2, p. 22)
- Confidence: **high** for the London monthly data; **low** for direct transfer to link × year structure

**Finding 4**
- Finding: The INAR(1) model finds that the London congestion charge reduced car casualties by approximately 27% (coefficient −0.308, t=−4.68), consistent with TfL's own estimate of 40–70 fewer casualty crashes per year. This result is robust across all model types.
- Why it matters: This is a UK-specific reference result using STATS19 data, demonstrating that STATS19-based count models can detect policy interventions of ~25–30% magnitude with monthly temporal resolution. This provides a calibration reference for what effect sizes are detectable in UK crash data.
- Evidence quote or page reference: "The coefficient value of this variable is found to be -0.31 in the INAR(1) model suggesting that the introduction of the congestion charging zone within central London reduces car casualties by about 27%." (p. 10)
- Confidence: **high** — consistent across all four model types

**Finding 5**
- Finding: The INAR(1) model has a known limitation: the basic INAR(1) Poisson process assumes stationarity, which means it cannot handle non-stationary time series (upward or downward trends). Extensions (INAR(1) NB, INARMA(1,1) NB) exist but their parameter estimation methods were not readily available to the author at the time. Seasonality is also not natively handled.
- Why it matters: Any application of INAR models to Open Road Risk would need the NB extension (for overdispersion) and seasonal components. These are non-trivial to implement and may not be available in standard Python libraries. This is a practical barrier.
- Evidence quote or page reference: "The INAR(1) Poisson process is a stationary time series process that has a limitation to deal with the presence of over-dispersion commonly found in accident data." (p. 12)
- Confidence: **high** — explicitly stated as a known limitation

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Temporal holdout validation (hold out most recent year(s)) | Correct validation design for panel data with temporal structure; complements grouped-by-link holdout | Existing Stage 2 data | 2 time series | Compatible; apply to link × year panel by holding out 2023–2024 observations | Stage 2 / validation | Low | Short holdout period if only 1–2 years available |
| ACF diagnostic on link × year within-link crash counts | Quantifies year-to-year serial correlation within individual road links; determines whether clustering standard errors is needed | Existing Stage 2 panel | Single time series per link | Apply to a sample of links (e.g., 100 highest-crash links); not full 2.17M | Stage 2 / diagnostic | Low–medium | Most links have too few crashes per year for meaningful ACF |
| Clustered standard errors by road link in Stage 2 GLM | Corrects for within-link serial correlation without requiring INAR model; robust inference | Existing Stage 2 data | N/A | Compatible with Poisson GLM; statsmodels supports cluster-robust SEs | Stage 2 | Low | Requires grouping by link ID; already implied by grouped split but not explicitly implemented |
| INAR(1) Poisson as aggregate temporal trend model | For national-level calibration or policy monitoring (e.g., tracking year-on-year change in Open Road Risk network-wide predicted vs observed crashes) | Annual aggregate crash counts from STATS19 | GB annual / London monthly | Compatible at aggregate level only | Documentation / future diagnostic | Medium | Requires specialist implementation (Karlis EM algorithm not standard in Python/R packages as of 2007; check current availability) |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| INAR(1) Poisson at link × year level | INAR assumes a single stationary time series; applying it to 2.17M separate links is computationally infeasible and each link has too few observations (≤10 years) for reliable INAR parameter estimation | Sufficient within-link time series length (minimum ~20+ observations recommended) | Single time series | Very low | Not applicable at production scale | High |
| SARIMA for seasonal monthly link-level crash modelling | Same data constraint; also seasonal ARIMA is designed for single time series, not panels | Per-link monthly crash counts (extremely sparse) | Single time series | Very low | Aggregate to area or road-type level if seasonal trend analysis needed | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Indirectly — VKT is used as an exposure control, consistent with Open Road Risk's offset approach. The paper does not add to the theoretical basis for log-offsets.

- **Does it suggest better handling of AADT/AADF uncertainty?** No — not addressed.

- **Does it suggest useful geometry or road-context features?** No — purely temporal modelling.

- **Does it suggest better modelling of junctions?** No.

- **Does it suggest better treatment of severity?** No — single severity category per dataset.

- **Does it suggest better validation design?** Yes — temporal holdout is the appropriate validation design for time-dependent data. Open Road Risk's current grouped-by-link split addresses spatial leakage but a combined temporal + spatial holdout would be more rigorous.

- **Does it expose a weakness in my current approach?** One specific weakness: the Stage 2 Poisson GLM assumes independent observations. Year-to-year crash counts on the same road link are likely serially correlated (as are monthly counts in the London data). If this autocorrelation is non-trivial, GLM coefficient standard errors will be underestimated. The practical fix — cluster-robust standard errors by link — is low-effort and should be checked.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add a diagnostic to Stage 2: compute ACF of year-to-year crash counts for a sample of road links (e.g., top 500 links by total crash count, where the time series is long enough to be meaningful). If average ACF at lag 1 exceeds ~0.15, add cluster-robust standard errors by link to the Stage 2 Poisson GLM.
- Action type: diagnostic
- Relevant stage: Stage 2
- Why the paper supports it: The paper demonstrates that standard NB/Poisson models produce inefficient estimates when observations are serially correlated; α = 0.355 for the London monthly data suggests meaningful autocorrelation is common in UK crash count time series.
- Evidence quote or page reference: "Modelling time series count data using these [Poisson/NB] models may result in inefficient estimates of the parameters as time series data are normally serially correlated." (p. 2)
- Effort: low–medium
- Risk if implemented badly: ACF on sparse crash counts (most links have 0–2 crashes/year) will be noisy; restrict to links with ≥3 crashes in at least 5 years.

**Action 2**
- Suggested repo action: Add a temporal holdout validation to complement the existing grouped-by-link split. Hold out the most recent 1–2 years of crash data (e.g., 2023–2024) and evaluate Stage 2 model predictions on these unseen years. Report temporal holdout RMSE alongside grouped-CV metrics.
- Action type: validation
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper uses temporal train/test splits as the appropriate validation design for time-dependent data. Open Road Risk's current grouped split handles spatial leakage but not temporal leakage.
- Evidence quote or page reference: "Each of the datasets is divided into two parts. One part is used to estimate the model parameters and the other part is used to validate the corresponding model." (p. 7)
- Effort: low
- Risk if implemented badly: Short holdout period (1–2 years) means validation metrics have high variance; interpret cautiously.

**Action 3**
- Suggested repo action: Document in Stage 2 model notes that the Poisson GLM assumes independent observations, and that year-to-year within-link serial correlation (if present) inflates apparent coefficient significance. Note INAR(1) NB as a candidate model for future temporal extension, with the caveat that it requires stationarity and overdispersion extensions not readily available in standard Python libraries.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper demonstrates the problem and the model class, while being honest about the implementation barrier.
- Evidence quote or page reference: "The extensions of this model are an INAR(1) NB model or an INARMA(1,1) NB model that could potentially control for both non-stationary time series process and over-dispersion. However, the methods of estimating parameters for such models are very complex." (p. 12)
- Effort: low
- Risk if implemented badly: none (documentation only)

**Action 4**
- Suggested repo action: Use the paper's London CC zone result (~27% casualty reduction, detectable with monthly STATS19 data over 12 years) as a calibration reference. When evaluating Open Road Risk's ability to detect safety interventions (e.g., speed limit changes, road improvements), this result sets a realistic lower bound on detectable effect sizes at link or small-area level using STATS19.
- Action type: documentation note
- Relevant stage: documentation / validation
- Why the paper supports it: The result is directly from UK STATS19 data and is robust across all four model types.
- Evidence quote or page reference: "the introduction of the congestion charging zone within central London reduces car casualties by about 27%" (p. 10)
- Effort: low
- Risk if implemented badly: none (documentation reference only)

---

## 16. Query Tags

- INAR
- integer-valued-autoregressive
- time-series-count-data
- serial-correlation
- ARIMA
- SARIMA
- negative-binomial
- temporal-autocorrelation
- thinning-parameter
- UK-STATS19
- Great-Britain
- London-congestion-charge
- intervention-analysis
- temporal-holdout-validation
- cluster-robust-standard-errors
- panel-data-temporal-dependence
- aggregate-time-series
- low-count-data
- Loughborough

---

## 17. Confidence and Gaps

- Overall confidence in extraction: **high**
- Important details not stated in the paper:
  - The exact published journal reference (volume, issue, pages) is not in the manuscript; this is an accepted manuscript from the Loughborough repository
  - NB model coefficients are not reported for dataset 1 (Table 1 shows only ARIMA, NB-with-trend, and INAR columns — the plain NB model results appear to be merged or omitted in the manuscript version)
  - Standard errors for INAR parameter estimation (EM algorithm details) are not fully described; readers are referred to Karlis (2006)
  - Python/R package availability for INAR models was limited as of 2007; current availability should be verified before implementation
- Parts of the paper that need manual checking:
  - Table 1: the column for plain "NB" model appears to share values with "NB with a time trend" in some rows — verify against published version
  - The INAR(1) Poisson mean/variance relationship (both equal λ/(1−α)) implies that overdispersion cannot be modelled by INAR(1) Poisson; the NB extension would be needed for Open Road Risk data
- Any likely ambiguity or risk of misinterpretation:
  - The paper's finding that ARIMA outperforms INAR for the aggregated annual data should not be interpreted as ARIMA being generally superior; it reflects the fact that when counts are large, normal approximation is adequate and the integer-valued property matters less
  - The thinning parameter α = 0.355 from the London monthly data should not be directly applied to Open Road Risk's link × year structure; the spatial and temporal aggregation levels are completely different
  - INAR(1) assumes stationarity; Open Road Risk's crash counts have a secular downward trend (UK road safety improvements over time), which would violate this assumption for most link-level time series
