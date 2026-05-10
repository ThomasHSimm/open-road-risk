# Paper Extraction: Gao et al. 2024 — STZITD-GNN

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: Uncertainty-Aware_Probabilistic_Graph_Neural_Networks_for_Road-Level.pdf
- Suggested Markdown filename: paper-extraction-gao-2024-stzitd-gnn.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: claude-sonnet-4-6
- Interface used: web chat (claude.ai)
- Input type: PDF upload (text extracted from document blocks in context)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 40-page paper including appendices was accessible. Tables 3 and 4 and Figures 1–7 were readable via text extraction; figure content was supplementary to the written descriptions.

---

## 1. Citation

- Title: Uncertainty-Aware Probabilistic Graph Neural Networks for Road-Level Traffic Crash Prediction
- Authors: Xiaowei Gao, Xinke Jiang, Dingyi Zhuang, Huanfa Chen, Shenhao Wang, Stephen Law, James Haworth
- Year: 2024 (arXiv preprint, submitted July 2024; preprint v4 dated 27 Jul 2024)
- DOI or URL: arXiv:2309.05072v4
- Country / region studied: United Kingdom (London: Lambeth, Tower Hamlets, Westminster boroughs)
- Study setting: urban

---

## 2. Core Objective

- One-sentence description: The paper proposes STZITD-GNN, a spatiotemporal graph neural network using a zero-inflated Tweedie (ZITD) distribution decoder to produce probabilistic, multi-step, road-level crash risk predictions that simultaneously model frequency, severity, and uncertainty.
- Main purpose: prediction (multi-step, probabilistic, road-level crash risk); also uncertainty quantification and hotspot identification
- Evidence quote: "our model aims to predict the future crash risk score in the next p time windows and the confidence interval of the predicted results per road" (Section 3.1, p. 9)

---

## 3. Response Variable

- Target variable: crash risk score per road per daily time step
- Collision type: all injury crashes (minor, serious, fatal); property-damage-only not stated as included
- Severity handling: frequency and severity are jointly modelled. Severity levels l = 1 (minor injury), 2 (serious injury), 3 (fatal) are used as multiplicative weights in a composite risk score formula: `y_it = sum over j of (C^t_{i,k} * l_j)`. This is a severity-weighted count, not a raw count.
- Count, binary, rate, risk score, severity class, or other: continuous severity-weighted risk score (zero-inflated, long-tailed)
- Time window used for outcomes: daily resolution; 2019 data only; 14-day forward prediction horizon
- Evidence quote: "y_it = sum_{j=1}^{3} C^t_{i,k} × l^j ... l is assigned the values 1, 2, and 3, representing minor injury, serious injury, and fatal crash severities" (Section 3.1, Eq. 1, p. 9)

**Note for Open Road Risk:** The response variable is a severity-weighted composite score, not a raw injury count. This is a modelling choice that conflates frequency and severity into one quantity. Open Road Risk's current Stage 2 outcome is an injury collision count. The two approaches are not directly comparable. Adopting this severity-weighting scheme would require assigning numeric severity weights to STATS19 severity categories — a substantive design decision with its own assumptions.

---

## 4. Exposure Handling

- Exposure variable used, if any: None. No traffic exposure variable, offset, or denominator is used.
- Traffic count source: Not used. The paper uses STATS19-style crash data and road/contextual features but no AADF, AADT, or traffic flow data in the final model. (The conclusion mentions GPS data as a future direction.)
- Whether exposure is modelled, observed, assumed, or ignored: **Ignored.** No exposure normalisation is applied.
- Treatment of missing or sparse traffic counts: Not applicable — not used.
- Whether offset terms, rates, denominators, or normalisation are used: No offset. The model predicts a raw severity-weighted crash risk score, not an exposure-normalised rate.
- Evidence quote: "Our study includes spatial features such as road types, road lengths and widths, road conditions, and census characteristics... Temporal features... encompass weather information such as sunrise and sunset times, humidity, visibility, rainfall..." (Section 3.1, p. 9). No mention of traffic counts or exposure offsets anywhere in the paper.
- Transferability to my AADF/WebTRIS setup: **Low** — the paper's mathematical exposure structure does not transfer because there is no exposure structure. The ZITD distributional assumption is mathematically separable from the exposure question and could in principle be combined with an offset, but the paper does not demonstrate or test this.
- Notes: The absence of traffic exposure is a significant methodological gap relative to Open Road Risk's design. A model that does not account for exposure cannot distinguish high-risk roads from high-traffic roads. The paper makes no acknowledgment of this limitation.

---

## 5. Spatial Unit of Analysis

- Unit: road segment (individual road links in a road network graph)
- Segment length or segmentation rule: follows the road network graph structure from DfT road traffic data (https://roadtraffic.dft.gov.uk/downloads); segment definition not explicitly stated. Node counts suggest OS-style road link granularity: Westminster 4,822 nodes, Lambeth 5,659 nodes, Tower Hamlets 4,688 nodes (Table 3, p. 16).
- How crashes are assigned to the network: "We allocate the crash point to its closest road" (Section 3.1, p. 9). Snapping quality, snap rate, and ambiguous-match handling are not discussed.
- Treatment of junctions/intersections: Edges represent road connections (adjacency matrix A); junctions are implicit in graph connectivity but not separately modelled as spatial units.
- Spatial aggregation risks: Not discussed. With daily resolution and 95–97% zero-inflation rates, many time steps have no crashes on any given road; the model's ability to distinguish zero from near-zero is central to its design.
- Evidence quote: "The road network is represented as a graph G = (V, E, A)... An entry A_{i,j} = 1 indicates the existence of an edge between road v_i and v_j" (Section 3.1, p. 9)
- Relevance to OS Open Roads link-based pipeline: The road-link spatial unit is directly compatible with OS Open Roads geometry. The graph structure (adjacency matrix from road connectivity) is also achievable with OS Open Roads. However, the paper's scale is three small urban boroughs (~4,700–5,700 nodes each), not the 2.17M-link national-scale network of Open Road Risk.

---

## 6. Temporal Unit of Analysis

- Years covered: 2019 only (single year)
- Temporal resolution: daily (each time step is one day)
- Whether seasonality or time-of-day is modelled: Temporal features include sunrise/sunset times, humidity, visibility, rainfall, holiday/working day indicators. Time-of-day sub-daily profiles are not modelled. Seasonality is implicitly present in the weather features but not explicitly decomposed.
- Whether before-after or panel structure is used: No. Single year, no before-after design, no multi-year panel.
- Evidence quote: "The train, validation and test data are all from 2019, as the ratio is 8:2:2" (Section 4.2, p. 16)
- Relevance to WebTRIS-style time profiles: No direct relevance. The paper does not use within-day traffic profiles, peak/off-peak fractions, or AADT. Weather-based temporal features (humidity, visibility) are used instead. These are not part of Open Road Risk's current pipeline and would require a separate data source.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Road type | DfT road network data / OS-style | Direct attribute from road network graph | Road type is a primary risk predictor | Already present / compare implementation |
| Road length | Road network geometry | Direct attribute | Longer segments have higher exposure to crashes (though no formal offset is used here) | Already present / compare implementation |
| Road width | Road network data | Direct attribute | Width affects risk, especially for cyclists and pedestrians | Candidate feature; OSM width coverage is sparse in Open Road Risk |
| Road condition | Not explicitly sourced | Direct attribute (stated but source unclear) | Surface quality affects crash risk | Candidate feature; OSM surface sparse in Open Road Risk |
| Census characteristics (LSOA level) | UK census | Assigned to roads via spatial join to LSOA | Captures sociodemographic context | Already present (population density, IMD); compare implementation |
| Weather: sunrise/sunset times | Not stated (likely derived from date/location) | Daily temporal feature | Proxy for daylight hours; affects crash rates | Low: not currently in Open Road Risk; derivable from date/lat-lon |
| Weather: humidity, visibility, rainfall | Not stated (likely Met Office or similar) | Daily temporal feature | Adverse weather increases crash risk | Low: requires a daily weather data feed not currently in pipeline |
| Holiday / working day indicator | Not stated | Binary temporal flag | Traffic volume and crash patterns differ significantly | Medium: derivable from UK bank holiday calendars; low engineering effort |
| Historical crash risk scores (lagged) | STATS19 | Used as input Y_{1:t} to the GRU encoder | Recent crash history informs short-term predictions | **Caution: leakage risk for Open Road Risk's yearly aggregation frame** |

**Important note on historical crash as input:** The model uses lagged crash risk Y_{1:t} as a direct input feature to the temporal encoder. In a daily-resolution short-term forecasting context this is not leakage — the historical values precede the prediction window. However, in Open Road Risk's annual link-year framework, incorporating crash history as a feature would introduce post-event correlation and should be treated as a potential leakage pathway. This distinction is critical and should not be overlooked if any adaptation is attempted.

---

## 8. Model Architecture

- Algorithms/models used: GRU (temporal encoder) + GAT (spatial encoder) + ZITD distribution decoder; full end-to-end model named STZITD-GNN
- Baseline model: HA (historical average), STGCN, STGAT, STG-GNN (Gaussian), STNB-GNN (Negative Binomial), STTD-GNN (Tweedie without ZI), STZINB-GNN (Zero-Inflated NB)
- Final/preferred model: STZITD-GNN (Zero-Inflated Tweedie with GRU+GAT encoder)
- Loss function or likelihood: Negative log-likelihood of the ZITD distribution, with L2 regularisation: `NLL_STZITD = NLL_{y=0} + NLL_{y>0} + η||Θ||²` (Section 3.4, Eq. 12, p. 14)
- Offset/exposure term, if used: None
- Spatial autocorrelation handling: Graph Attention Network (GAT) with multi-head attention captures spatial dependencies between connected road segments. Attention weights are learned from road embeddings, not from fixed spatial distance.
- Temporal dependence handling: GRU captures sequential temporal dependencies across the input history window 1:t. Output is a 14-step-ahead prediction sequence.
- Interpretability method: The four ZITD parameters (π, µ, ϕ, ρ) are individually interpretable: π = zero-inflation probability, µ = expected crash risk, ϕ = dispersion, ρ = tail index. Choropleth maps of predicted vs actual risk shown (Figure 3). 3D parameter surface plots shown (Figure 7).
- Evidence quote: "The proposed framework integrates a cohesive encoder that combines a Gated Recurrent Unit (GRU) for capturing temporal dynamics and a Graph Attention Network (GAT) for spatial relationships" (Section 1, p. 4); "The decoder leverages a Tweedie (TD)-based distribution, a flexible compound Poisson-gamma model that simultaneously models both exact zero occurrences and continuous positive values" (Section 1, p. 4)

---

## 9. Reported Metrics / Quantitative Results

### Main results table (Table 4, p. 21 — 14-day multi-step prediction, 2019 test data)

| Result type | Metric | Value (STZITD-GNN) | Improvement over 2nd best | Dataset | Evidence |
|---|---|---|---|---|---|
| Point estimation | MAE | 0.0238 | +21.19% over STTD-GNN (0.0302) | Lambeth | Table 4 |
| Point estimation | MAPE | 0.0135 | +49.06% over STZINB-GNN (0.0265) | Lambeth | Table 4 |
| Point estimation | RMSE | 0.0947 | +13.75% over STTD-GNN (0.1098) | Lambeth | Table 4 |
| Uncertainty | MPIW | 0.0204 | +55.07% over STZINB-GNN (0.0454) | Lambeth | Table 4 |
| Uncertainty | PICP | 0.9899 | +0.26% over STTD-GNN (0.9873) | Lambeth | Table 4 |
| Zero-crash ID | ZR | 0.7870 | +15.09% over STTD-GNN (0.6838) | Lambeth | Table 4 |
| Hit rate | AccHR@20 | 0.7659 | +7.52% over STTD-GNN (0.7123) | Lambeth | Table 4 |
| Point estimation | MAE | 0.0271 | +11.15% over STGAT (0.0305) | Tower Hamlets | Table 4 |
| Point estimation | RMSE | 0.0918 | +22.60% over STTD-GNN (0.1186) | Tower Hamlets | Table 4 |
| Uncertainty | MPIW | 0.0156 | +47.30% over STZINB-GNN (0.0296) | Tower Hamlets | Table 4 |
| Uncertainty | PICP | 0.9871 | +0.26% over STTD-GNN (0.9845) | Tower Hamlets | Table 4 |
| Zero-crash ID | ZR | 0.8876 | +17.94% over STZINB-GNN (0.7526) | Tower Hamlets | Table 4 |
| Hit rate | AccHR@20 | 0.7224 | +3.94% over STGAT (0.6950) | Tower Hamlets | Table 4 |
| Point estimation | MAE | 0.0357 | +38.34% over STTD-GNN (0.0579) | Westminster | Table 4 |
| Point estimation | RMSE | 0.1015 | +34.60% over STTD-GNN (0.1552) | Westminster | Table 4 |
| Uncertainty | MPIW | 0.0259 | +47.46% over STZINB-GNN (0.0493) | Westminster | Table 4 |
| Uncertainty | PICP | 0.9893 | +0.94% over STTD-GNN (0.9801) | Westminster | Table 4 |
| Zero-crash ID | ZR | 0.7328 | +16.54% over STZINB-GNN (0.6288) | Westminster | Table 4 |
| Hit rate | AccHR@20 | 0.6898 | +13.55% over STTD-GNN (0.6075) | Westminster | Table 4 |

### Assessment of metrics

- **Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, or externally validated?** Temporally held out within a single year (2019). The train/val/test split is 8:2:2 chronologically within 2019. This is a **within-year temporal holdout**, not a cross-year or spatial holdout. There is no external validation.
- **Do these metrics test predictive generalisation, model fit, or something else?** Within-year temporal generalisation only. The model is tested on the final ~20% of 2019 (roughly October–December). Generalisation to other years, other areas, or different traffic conditions is not tested.
- **Are any metrics likely to be optimistic?** Yes, several risks:
  1. Single year, single city: no test of transferability.
  2. The train/val/test split ratio is 8:2:2, which is unusual — the validation and test sets are each 20% of a single year. The paper does not clarify whether these are sequential (temporally ordered) or random. If random, temporal leakage is possible.
  3. The MPIW improvement is large but the PICP improvement is marginal (~0.26%), suggesting the narrower intervals may be systematically optimistic about coverage.
  4. No spatial holdout means that roads in the test set are the same roads seen during training, which allows the model to memorise per-road risk profiles.
- **Which metric is most relevant to Open Road Risk?** AccHR@20 (hit rate on top-20% high-risk roads) is closest to Open Road Risk's risk percentile ranking objective. ZR (zero-crash road identification) is also relevant given the sparse link-year collision data. Neither is directly comparable to Open Road Risk's annual aggregation frame.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Via the ZITD distribution, which explicitly models excess zeros through a sparsity parameter π and uses a compound Poisson-Gamma (Tweedie) distribution for non-zero crash risk values. Zero-inflation rates in the study data are 95.72% (Westminster), 96.71% (Lambeth), 96.28% (Tower Hamlets) at daily resolution (Table 3, p. 16).
- Model type: **Zero-inflated Tweedie (ZITD)**. The paper explicitly introduces and fits a zero-inflated model. The zero-inflated tag is appropriate here.
- Whether high-risk locations are evaluated separately: Partially — AccHR@20 evaluates whether the top 20% of predicted high-risk roads correspond to actual crash roads. This is a coarse precision metric on the high-risk tail, not a separate model for high-risk segments.
- Evidence quote: "we introduce a refinement, known as the Zero-Inflated Tweedie (ZITD) model... The ZITD model includes a distinctive feature, a sparsity parameter (π) that specifically addresses the skewness of the data characterised by an excess of zeros" (Section 3.2.2, p. 11)
- Practical relevance to my sparse collision link-year dataset: High conceptual relevance. Open Road Risk faces a similar zero-heavy structure (~98–99% of link-years have zero collisions, at annual resolution). However, Open Road Risk currently uses a Poisson GLM offset model (which handles zeros without explicit zero-inflation) and XGBoost. The paper's evidence that a ZITD outperforms plain Tweedie and ZINB in this setting is interesting, but the comparison is at daily urban road resolution — a different data regime from annual UK-wide links.

---

## 11. Validation Strategy

- Train/test split method: Temporal split within a single year (2019). Ratio 8:2:2 (train:val:test). Whether this is strictly chronological or randomly sampled is not explicitly stated; "all from 2019" with 8:2:2 ratio is the only description.
- Spatial holdout used? No
- Temporal holdout used? Yes — within-year temporal split (partial). No cross-year holdout.
- Grouped holdout used? No. Roads in the test set are the same roads seen in training.
- Cross-validation type: None reported
- Metrics: MAE, MAPE, RMSE (point estimation); MPIW, PICP (uncertainty quantification); ZR (zero-crash identification); AccHR@20 (hit rate on high-risk roads)
- External validation: None
- Leakage or generalisation risks:
  1. No spatial holdout: the model learns per-road patterns and is tested on the same roads. This is standard for short-term forecasting but limits evidence of spatial generalisation.
  2. Historical crash values Y_{1:t} are used as input features. In a daily forecasting context this is lagged input, not leakage. But if this design were adapted to Open Road Risk's annual frame, past-year crash counts as input would introduce correlation with the target.
  3. Single-year training: the model has not been tested under different traffic conditions, post-COVID patterns, or year-to-year variation. Temporal instability of crash frequency is a known problem in road safety modelling (paper cites Mannering 2018 on this point but does not test across years).
  4. The 8:2:2 split means test data is ~2.4 months of a single year. Whether the model generalises to a different seasonal period or a different year is unknown.
- Evidence quote: "The train, validation and test data are all from 2019, as the ratio is 8:2:2" (Section 4.2, p. 16)
- What I should copy or avoid:
  - **Avoid:** Direct adoption of this validation design for Open Road Risk. A single-year, no-spatial-holdout, no-cross-year design is insufficient for a national annual pipeline.
  - **Copy (as diagnostic):** The AccHR@20 metric (hit rate at top-k% of predicted risk) is a useful complement to PICP/MPIW and is directly applicable to Open Road Risk's percentile ranking evaluation.
  - **Copy (as diagnostic):** MPIW and PICP as uncertainty quantification metrics if Open Road Risk adds probabilistic outputs.

---

## 12. Key Findings Relevant to My Project

**Finding 1:** The Zero-Inflated Tweedie (ZITD) distribution outperforms both standard Tweedie (without zero-inflation) and Zero-Inflated Negative Binomial across all four evaluation dimensions in three London boroughs at daily road-level resolution.

- Why it matters: Open Road Risk uses a Poisson GLM and XGBoost. The paper provides evidence (in this case study) that a distribution explicitly modelling zero-inflation and long-tail severity simultaneously outperforms simpler alternatives. This is a potentially relevant distributional choice for any future probabilistic extension of Stage 2.
- Evidence: Table 4, p. 21 — STZITD-GNN leads on MAE, MAPE, RMSE, MPIW, ZR, AccHR@20 across all three boroughs.
- Confidence: medium — result is from a single year, one city, three boroughs, at daily resolution. It does not prove the same result would hold at annual UK-wide link resolution.

**Finding 2:** Gaussian distributional assumptions perform significantly worse than skewed/zero-inflated alternatives for road-level crash prediction. The STG-GNN (Gaussian) model is consistently the worst or near-worst performer across all metrics.

- Why it matters: Open Road Risk's XGBoost does not model output distribution explicitly. Any future Bayesian or probabilistic output layer should avoid Gaussian assumptions for crash counts or severity-weighted scores. The evidence aligns with the general road safety literature on overdispersion.
- Evidence: "Among probabilistic models, those that assume Gaussian distributions perform poorly... far worse performance 50% compared to the STZITD-GNN model" (Section 4.5, p. 19)
- Confidence: medium — consistent across three boroughs; consistent with external literature.

**Finding 3:** The sparsity parameter π in the ZITD distribution significantly improves zero-crash road identification over plain Tweedie, with improvements of 15–18% ZR across boroughs.

- Why it matters: Open Road Risk has ~98–99% zero link-years. Accurately identifying true-zero links matters for distinguishing roads with genuinely no risk from roads with unobserved risk. This supports the case for explicit zero-inflation modelling in any future distributional extension.
- Evidence: "in the Tower Hamlets and Westminster cases, the ZI parameter significantly increases performance in zero-rate predictions compared to the NB distribution, showing improvements of 16.54% and 17.94%, respectively" (Section 4.5, p. 20)
- Confidence: medium — applies in this case study at daily resolution; annual link-year zero rates may behave differently.

**Finding 4:** Using historical crash risk as an input feature (lagged Y_{1:t}) within a temporal encoder enables effective multi-step prediction at road level, but this design is not directly portable to an annual panel framework without introducing leakage.

- Why it matters: Flagged as a design risk for Open Road Risk, not an opportunity. This is a short-term forecasting architecture. Any adaptation to annual link-year modelling would need careful treatment of crash history as a feature.
- Evidence: "our methodology starts with the deployment of a GRU acting as a temporal encoder... accommodates the feature sequence over past time windows 1:t" (Section 3.3, p. 12)
- Confidence: high — this is an architectural observation, not a statistical finding.

**Finding 5:** The AccHR@20 metric (hit rate on top-20% predicted high-risk roads against actual crash locations) is a practically useful evaluation criterion for road-level risk ranking, complementing standard regression metrics.

- Why it matters: Open Road Risk's primary output is a risk percentile ranking. AccHR@k provides a more direct evaluation of ranking quality than RMSE or MAE, which average over all roads including the majority with zero crashes. Open Road Risk does not currently report this metric.
- Evidence: "we use the accuracy hit rate in a (AccHR@20) metric... we focus on the top 20% (a = 20%) of roads considered high-risk to verify if these areas actually correspond to actual crash occurrence" (Section 4.3.4, p. 17)
- Confidence: high — this is a well-defined metric applicable without the STZITD-GNN architecture.

**Finding 6:** Model performance degrades gracefully over the 14-day prediction horizon, with MPIW widening over time. The STZITD-GNN shows smoother degradation than baseline models, suggesting the ZITD distribution provides better-calibrated uncertainty growth over time.

- Why it matters: Limited direct relevance to Open Road Risk's annual frame, but the principle — that a well-specified output distribution produces better-calibrated uncertainty intervals — is relevant if Open Road Risk adds confidence intervals to its risk estimates.
- Evidence: Figure 4 (p. 23), temporal MPIW plots; "this increase is smoother in our STZITD-GNNs model compared to the more erratic fluctuations observed in baseline models" (Section 4.6.1, p. 23)
- Confidence: medium — single-year, one-city case study.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| AccHR@k metric | Direct evaluation of risk ranking quality; more meaningful than RMSE for ranking-focused outputs | Predicted risk percentiles + STATS19 crash locations (already in pipeline) | 3 boroughs / ~5,000 nodes | High — applies at any scale | Validation | Low | Choice of k is somewhat arbitrary; ensure k is calibrated to the actual % of risky links |
| MPIW / PICP metrics | Evaluate calibration of any future probabilistic output | Predicted intervals (requires probabilistic output first) | 3 boroughs | High — metric scales | Validation (future) | Low | Requires a probabilistic model before these metrics are applicable |
| Zero-inflated Tweedie (ZITD) as output distribution | Better distributional fit for zero-heavy, long-tailed crash data than Poisson or NB; explicit uncertainty quantification | Same data as current Stage 2 | 3 boroughs / ~5,000 nodes daily | Medium — daily urban resolution vs annual national scale; behaviour at annual resolution not tested | Stage 2 candidate model extension | High (requires probabilistic GNN or distributional GLM framework) | Open Road Risk's annual aggregation will have different zero-inflation structure than daily urban data; requires separate validation |
| Holiday / working day binary temporal feature | Low-effort feature capturing traffic pattern variation | UK bank holiday calendar (publicly available) | Small; derivable from date | High | Stage 2 candidate feature | Low | Minimal improvement expected for annual aggregation; more relevant if Open Road Risk moves to sub-annual resolution |
| Tweedie GLM (without GNN, without ZI) as a simpler alternative | The Tweedie family includes Poisson as a special case; a Tweedie GLM with exposure offset is a conservative step up from Poisson GLM | STATS19 + AADF (already in pipeline) | N/A | High | Stage 2 candidate model comparison | Medium | Requires testing whether dispersion parameter ρ is stable across road types and facility families; interaction with exposure offset needs careful specification |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full STZITD-GNN architecture (GRU + GAT + ZITD) | Designed for daily multi-step forecasting, not annual risk ranking. Requires lagged crash history as input. No exposure normalisation. Computationally intensive. | Daily crash time series per road; temporal encoder requires contiguous daily data; no AADT integration | 3 boroughs / ~5,000 nodes | Low — computationally unrealistic at 2.17M links; architectural mismatch with annual panel design | Not recommended; consider distributional output layer (ZITD) separately from the GNN architecture | High |
| Graph Attention Network (GAT) spatial encoder at national scale | GAT requires constructing and propagating attention over a full road adjacency matrix. At 2.17M links, this is computationally unrealistic without substantial partitioning and approximation. | Full road graph adjacency matrix at national scale | 3 boroughs / ~5,000 nodes | Low | Regional subgraph partitioning could allow a local GAT, but this is a significant research and engineering effort, not a pipeline extension | High |
| Daily temporal resolution | Open Road Risk operates at annual link-year resolution. Moving to daily resolution would increase data volume by ~365x and require daily AADT/exposure estimates, which do not exist. | Daily AADT or traffic flow per link | Daily, one year | Low | Not applicable at current pipeline design | High |
| Severity-weighted composite risk score as response variable | Open Road Risk currently uses injury collision count as the response variable. Adopting the severity-weighted score y_it = sum(C * l) requires assigning numeric severity weights (1/2/3) to STATS19 severity categories. This is a substantive design decision not validated for the UK-wide pipeline. | Consistent severity weighting scheme | N/A | Medium (architecturally possible but requires design choices) | Could be piloted as a diagnostic variant of Stage 2, not as a production change | Medium |
| Weather features (humidity, visibility, rainfall) as daily temporal covariates | Open Road Risk aggregates annually. Daily weather variation averages out at annual resolution. A meaningful annual weather signal would require annual summary statistics (mean annual rainfall, fog days per year, etc.) not currently in the pipeline. | Daily meteorological data per road link (Met Office or equivalent) | Daily, one year | Low for direct adoption; medium for annual weather summaries | Annual weather summaries (e.g. from HadUK-Grid) could be a candidate feature, but evidence for annual-resolution improvement is absent from this paper | Medium |

---

## 14. Pipeline Implications

**Does this paper support using exposure-normalised collision risk?**
No. The paper explicitly ignores traffic exposure. It does not validate or challenge exposure normalisation. The absence of exposure is a methodological weakness in this paper relative to Open Road Risk's design. The paper does not provide evidence on whether exposure normalisation improves or degrades the outputs it reports.

**Does it suggest better handling of AADT/AADF uncertainty?**
No. Traffic count data is not used.

**Does it suggest useful geometry or road-context features?**
Partially. Road type, length, width, and road condition are listed as spatial features. Road type and length are already in Open Road Risk. Road width (from OSM) is a candidate feature but has sparse coverage. Road condition is listed without a clear source.

**Does it suggest better modelling of junctions?**
No. Junctions are represented implicitly through graph connectivity only. No separate junction model or junction-specific feature engineering is described.

**Does it suggest better treatment of severity?**
Yes, partially. The ZITD distribution jointly models frequency and severity via a compound Poisson-Gamma structure. This is a more principled approach than treating severity as a separate binary outcome. However, the severity weighting scheme (l = 1/2/3) is simple and fixed, not estimated. The evidence is limited to one city and one year.

**Does it suggest better validation design?**
Partially. The AccHR@k metric is a direct improvement over relying solely on RMSE/MAE for a ranking-focused pipeline. However, the paper's own validation design (single year, no spatial holdout, no cross-year test) is weaker than Open Road Risk's current grouped-by-road-link split.

**Does it expose a weakness in my current approach?**
Yes, one: Open Road Risk does not currently report a precision-at-k metric for its risk percentile ranking. AccHR@k (or equivalent) would provide direct evidence on whether the top-percentile predictions correspond to actual crash locations — which is the pipeline's primary purpose. This is a gap in the current validation reporting.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Implement AccHR@k (accuracy hit rate at top-k% predicted risk roads) as a validation metric for Stage 2 outputs
- Action type: diagnostic / validation metric addition
- Relevant stage: Stage 2 / validation
- Why the paper supports it: AccHR@20 directly evaluates whether high-percentile risk predictions correspond to roads with actual collisions — the primary purpose of Open Road Risk's risk percentile output. The metric is defined clearly in Eq. 16, p. 18.
- Evidence: "we use the accuracy hit rate in a (AccHR@20) metric... to verify if these areas actually correspond to actual crash occurrence" (Section 4.3.4, p. 17)
- Effort: low — requires predicted risk percentiles (already produced) and STATS19 crash locations (already in pipeline)
- Risk if implemented badly: Choice of k matters. k=20% is very broad for a 2.17M-link network. Consider AccHR@5, AccHR@1, or AccHR at the top-N links to align with operationally relevant thresholds.

**Action 2**
- Suggested repo action: Document the zero-inflated Tweedie distribution as a candidate Stage 2 model extension in a documentation note or research backlog item
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper provides evidence (in this case study) that a ZITD distributional assumption outperforms Poisson, Negative Binomial, and standard Tweedie for zero-heavy, long-tailed crash data. The mathematical structure (compound Poisson-Gamma with zero-inflation parameter) is compatible in principle with an exposure-offset GLM framework.
- Evidence: Table 4, p. 21; Section 3.2.2, p. 11
- Effort: low (documentation only); medium-high if piloted
- Risk if implemented badly: A ZITD GLM without exposure offset would not be appropriate for Open Road Risk. Any pilot must retain the AADF-based offset. The daily vs annual aggregation difference may alter the effective zero-inflation structure.

**Action 3**
- Suggested repo action: Pilot a Tweedie GLM (without zero-inflation) as a Stage 2 baseline comparison against the current Poisson GLM, using the same exposure offset
- Action type: baseline comparison
- Relevant stage: Stage 2
- Why the paper supports it: The Tweedie compound Poisson-Gamma family generalises the Poisson (ρ=1) and Gamma (ρ=2) distributions. With 1<ρ<2, it handles overdispersion more flexibly than a Poisson GLM. The paper's results suggest Tweedie outperforms Poisson/Gaussian assumptions in zero-heavy count data. A plain Tweedie GLM (statsmodels supports this) is a low-effort intermediate step before considering zero-inflation or GNN architecture.
- Evidence: STTD-GNN (Tweedie without ZI) consistently outperforms STG-GNN (Gaussian) and HA, Table 4, p. 21
- Effort: medium — requires specifying the Tweedie GLM with exposure offset and verifying ρ stability across road subgroups
- Risk if implemented badly: The Tweedie family requires ρ to be specified or estimated; misspecification of ρ could degrade performance. Ensure grouped cross-validation is retained from the current pipeline design.

**Action 4**
- Suggested repo action: Add documentation note flagging the absence of traffic exposure in this paper as a methodological limitation that limits comparability with Open Road Risk
- Action type: documentation note
- Relevant stage: documentation
- Why the paper supports it: The paper is a UCL-based UK study using STATS19 data and road-level graph models — superficially close to Open Road Risk. The absence of any exposure normalisation is a critical gap that should be recorded so future readers of the extraction do not over-apply the paper's findings.
- Evidence: No mention of AADT, AADF, or exposure offset anywhere in the paper. Conclusion lists GPS data as a future direction (Section 5, p. 28).
- Effort: low
- Risk if implemented badly: None (documentation only)

**Action 5**
- Suggested repo action: Review whether MPIW and PICP uncertainty metrics should be added to the Stage 2 evaluation framework as future targets, conditional on adding a probabilistic output layer
- Action type: documentation note / future validation design
- Relevant stage: Stage 2 / validation
- Why the paper supports it: If Open Road Risk adds empirical Bayes shrinkage intervals, Poisson confidence intervals, or any distributional uncertainty quantification, MPIW and PICP provide a principled framework for evaluating whether the intervals are well-calibrated. The paper defines these metrics clearly.
- Evidence: Section 4.3.2, p. 17, Eq. 14
- Effort: low (documentation); medium if probabilistic outputs are added
- Risk if implemented badly: PICP is sensitive to the chosen confidence level (paper uses 5%–95%); calibration should be evaluated across multiple levels, not just one.

---

## 16. Query Tags

- zero-inflated-tweedie
- ZITD-distribution
- compound-poisson-gamma
- graph-neural-network
- GAT-spatial-encoder
- GRU-temporal-encoder
- daily-temporal-resolution
- severity-weighted-score
- no-exposure-offset
- zero-heavy-counts
- road-level-prediction
- urban-boroughs
- STATS19-UK
- AccHR-metric
- MPIW-PICP-uncertainty
- multi-step-forecasting
- within-year-validation
- no-spatial-holdout
- hotspot-identification

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper:
  - The exact source of road width and road condition data is not stated (mentioned as features but no data provenance given).
  - Whether the 8:2:2 train/val/test split is strictly chronological or randomly sampled is not stated. This is important for assessing temporal leakage risk.
  - The road network data source URL given in Table 3 footnote (https://roadtraffic.dft.gov.uk/downloads) refers to DfT traffic counts, not to a road geometry source. The paper may be conflating the traffic count source with the road geometry source, or using a different road network for geometry.
  - Computational runtime and memory requirements for STZITD-GNN are not stated beyond the hardware used (NVIDIA GeForce RTX 3090, 24 GB).
  - The paper does not report confidence intervals on any of the performance metrics; it is not possible to assess whether differences between models are statistically significant.
- Parts of the paper that need manual checking:
  - Table 4 values should be verified against the original paper if these results are cited, as extraction from PDF tables can introduce transcription errors.
  - The GitHub repository (https://github.com/STTDAnonymous/STTD) is listed but may have changed or been made private since the arXiv preprint. Verify accessibility before attempting code re-use.
- Any likely ambiguity or risk of misinterpretation:
  - The response variable y_it is a severity-weighted composite score, not a raw collision count. Comparisons with Open Road Risk's Poisson GLM (which uses raw injury counts) are not straightforward. Do not interpret AccHR@20 improvements in this paper as evidence that the same improvements would appear for raw count prediction.
  - The paper's zero-inflation rates (95–97%) are at daily temporal resolution. Open Road Risk's zero-inflation rate (~98–99%) is at annual link-year resolution. The two rates reflect different phenomena: the daily rate is dominated by the rarity of crashes on any given day on most roads; the annual rate reflects roads that genuinely never record an injury crash in a given year. These may respond differently to zero-inflation modelling choices.
  - The PICP improvement of ~0.26% over the second-best model is marginal. The headline MPIW improvement (47–55%) is the stronger result, but a narrower interval that is equally or less well-calibrated is not necessarily better. The near-identical PICP values should be noted when interpreting the uncertainty quantification results.
