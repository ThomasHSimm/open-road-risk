# Paper Extraction: Pan et al. 2017 — Development of a Global Road Safety Performance Function Using Deep Neural Networks

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: 1-s2_0-S2046043017300199-main.pdf
- Suggested Markdown filename: paper-extraction-pan-2017-deep-belief-network-global-spf.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (full paper rendered in context as document)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: All 15 pages were rendered as text in context. Figures 3–8 are referenced but not viewable; their numerical results are reported in tables and described in text sufficiently for extraction. No supplementary material referenced.

---

## 1. Citation

- Title: Development of a global road safety performance function using deep neural networks
- Authors: Guangyuan Pan, Liping Fu, Lalita Thakali
- Year: 2017
- DOI or URL: http://dx.doi.org/10.1016/j.ijtst.2017.07.004
- Country / region studied: Canada (Ontario, Highway 401) and United States (Colorado; Washington State)
- Study setting: mixed — multilane access-controlled highway (Ontario), rural two-lane (Colorado, Washington), rural multilane (Washington), urban two-lane (Washington), urban multilane (Washington)

---

## 2. Core Objective

- One-sentence description: The paper investigates whether a single Deep Belief Network (DBN) model, trained on pooled crash data from multiple highway types and geographic regions, can predict crash frequencies with performance at least comparable to locally calibrated negative binomial (NB) models.
- Main purpose: safety performance function / prediction
- Evidence quote or page reference: "explore the feasibility of developing a modelling framework where datasets coming from multiple regions could be pooled together into a same modelling step and used to generate a single global model" (p.160); "a single DBN could be trained globally with multiple datasets to predict the expected crash frequencies with a performance at least comparable to the traditional NB model" (Conclusions, p.172)

---

## 3. Response Variable

- Target variable: Annual crash frequency per road segment (count of all crashes per homogeneous section per year)
- Collision type: all crashes (not stated to be injury-only; appears to include all reported crashes regardless of severity)
- Severity handling: not modelled — single undifferentiated crash count used as target
- Count, binary, rate, risk score, severity class, or other: count (raw crash frequency per segment-year); not rate-normalised in the DBN output — exposure is handled as an input feature, not an offset
- Time window used for outcomes: annual; panel structure by year. Ontario 2000–2008; Colorado 1991–1998; Washington not explicitly stated but implied annual
- Evidence quote or page reference: "predict the expected crash frequencies" (Abstract); Tables 1–3 show "Collisions (per year)" as the response variable

---

## 4. Exposure Handling

- Exposure variable used: AADT and segment length — included as input features in the DBN. In the NB benchmark models, log(AADT) and log(Length) are used as separate covariates (or combined as log(AADT × Length × 365 / 10^6) for Ontario).
- Traffic count source: Ontario — MTO Traffic Volume Inventory System (TVIS), counts from ~170 counting stations assigned to 418 homogeneous sections; nearest station within 2 km assigned for ~85% of sections. Colorado and Washington — FHWA HSIS observed annual AADT per segment.
- Whether exposure is modelled, observed, assumed, or ignored: observed traffic counts used directly. For Ontario ~15% of segments assigned from stations beyond 2 km — minor sparse-count issue, not explicitly addressed.
- Treatment of missing or sparse traffic counts: not explicitly addressed. Records with missing traffic data excluded from Washington dataset (p.164). No imputation described.
- Whether offset terms, rates, denominators, or normalisation are used:
  - NB benchmark: log(AADT × Length × 365 / 10^6) used as a covariate with coefficient ~0.83 (Ontario), or log(AADT) + log(Length) separately (Colorado, Washington) — not a true fixed-offset but near-offset form.
  - DBN: AADT and length are normalised to [0,1] and used as input features — no formal Poisson offset structure; the model is not a Poisson/count model and has no explicit exposure offset term.
- Evidence quote or page reference: Table 4 (NB coefficients); p.167: "for the exposure related features, namely, AADT and segment length, we used their log forms so that their transformations lead to the case of zero crash for zero values"

### Transferability to my AADF/WebTRIS setup

- NB benchmark exposure structure (log-offset / near-offset of AADT × length): **high transferability** — directly analogous to Open Road Risk Stage 2 offset. NB coefficient on log(AADT × Length × 365 / 10^6) is 0.827 for Ontario, close to unity as expected under a Poisson rate model.
- DBN exposure handling (AADT and length as normalised input features, no offset): **low transferability for Open Road Risk** — treating exposure as a feature rather than a constraint is methodologically weaker for a count model on rare events; does not guarantee rate-proportional predictions.
- Notes: The paper does not propagate traffic count uncertainty into either model. The Ontario nearest-station assignment (85% within 2 km) is similar in spirit to Open Road Risk's AADF-based AADT estimation, but the paper does not address uncertainty propagation. The DBN's lack of an exposure offset is a structural weakness relative to Open Road Risk's current Poisson GLM.

---

## 5. Spatial Unit of Analysis

- Unit: homogeneous road section (HS) — segments with uniform geometric characteristics
- Segment length or segmentation rule: generated by splitting at changes in geometric features (number of lanes, shoulder width, median, curvature) using GIS overlay. Minimum length threshold 0.2 km for Ontario and Colorado; 0.16 km for Washington. Ontario: 418 HS sections ranging 0.2–12.7 km, mean ~1.95 km. Colorado: 4593 sections ranging 0.21–31.76 km. Washington: varies by highway type (mean ~0.39–0.93 km by class).
- How crashes are assigned to the network: geocoded crash records linked to HS sections using linear referencing (MTO LHRS for Ontario; milepost referencing for Washington HSIS). Annual aggregation per HS section.
- Treatment of junctions/intersections: intersections, interchanges, ramps, and driveways explicitly excluded from Washington dataset (p.164). Not separately modelled.
- Spatial aggregation risks: not discussed. Segment length varies widely (0.2 to 31.76 km) — longer segments have higher expected counts, partially controlled by length as a feature but without a formal offset structure in the DBN.
- Evidence quote or page reference: p.163: "generate a set of homogenous sections (HS) in which each HS section represents segments with similar characteristics"
- Relevance to OS Open Roads link-based pipeline: partial — OS Open Roads uses fixed OS-defined segments (not homogeneous-section splits), which means segments are shorter and more numerous than the paper's HS units. The minimum-length threshold concept (exclude very short segments due to higher uncertainty) is relevant to Open Road Risk's handling of very short links.

---

## 6. Temporal Unit of Analysis

- Years covered: Ontario 2000–2008 (9 years); Colorado 1991–1998 (8 years); Washington — not explicitly stated
- Temporal resolution: annual — crashes aggregated per segment per year; each segment-year is one observation
- Whether seasonality or time-of-day is modelled: no
- Whether before-after or panel structure is used: panel structure (segment × year) used implicitly as the observation unit; no temporal random effects or autocorrelation modelled. Train/test split is temporal (earlier years train, later years test).
- Evidence quote or page reference: "the training set used year 2000–2006, and the testing set is 2007–2008" (Ontario); "training set designed is data 1991–1996 and testing is 1997–1998" (Colorado) (p.163)
- Relevance to WebTRIS-style time profiles: not relevant — no time-of-day or peak/off-peak modelling.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| AADT | Traffic counting stations (MTO TVIS / FHWA HSIS) | Nearest-station assignment; annual value per segment | Primary exposure measure; used as DBN input feature and NB predictor | Already present — Open Road Risk uses AADF-derived AADT. Compare implementation rather than add. |
| Segment length (km) | Road inventory / GIS | Direct from HS section definition; minimum threshold 0.16–0.2 km applied | Exposure component; used as DBN input and NB predictor | Already present in exposure offset |
| Number of lanes | Road inventory (HIMS / HSIS) | Direct categorical or count field | Road capacity proxy; included in DBN | Already present or derivable from OS Open Roads / OSM |
| Lane width (m) | Road inventory | Direct field from HSIS | Road geometry feature; significant in NB for Washington | Candidate feature — available from OSM (sparse); note significance in this study |
| Median width (m) | Road inventory | Direct field | Road geometry / division feature; significant in some NB models | Candidate feature — partially available from OSM |
| Left / right shoulder width (m) | Road inventory | Direct fields | Road geometry; significant in most NB models for Washington | Low transferability — not available in OS Open Roads or OSM at useful coverage |
| Terrain type (flat / rolling / mountainous) | Road inventory | Categorical classification per section | Significant in Colorado and Washington rural NB models | Candidate — partially derivable from OS Terrain 50 grade/elevation; already a candidate in Open Road Risk |
| Rural/urban flag | Google Maps (Ontario); HSIS classification (Washington) | Binary or categorical field | Used as DBN feature and NB predictor | Already present via rural/urban classification in Open Road Risk |
| Curve deflection (per km) | GIS curve layer overlaid on HIMS | Curvature extracted from GIS map and disaggregated into HS sections | Significant in Ontario NB (negative sign — more curvature, fewer crashes on this access-controlled highway); note: counterintuitive for motorway context | Already a candidate feature (curvature) in Open Road Risk — note the negative coefficient on this motorway dataset |
| Commercial AADT | MTO TVIS | Separate count of commercial vehicles per day | Significant in Ontario NB | Candidate — HGV proportion already in Open Road Risk candidate features |
| Location / road type / access type indicator | Dataset label | Constant encoded as integer (1/2/3 for Ontario/Colorado/Washington; dummy for road type, access type) | Used in global DBN to distinguish data sources | Not directly applicable to Open Road Risk; analogous to road classification already present |

---

## 8. Model Architecture

- Algorithms/models used: Deep Belief Network (DBN) with continuous RBM layers; negative binomial (NB) regression as benchmark; Bayesian regularised ANN as secondary benchmark
- Baseline model: locally calibrated NB model (separate model per highway type and region); also Bayesian regularised ANN
- Final/preferred model: global DBN (simultaneously trained on all datasets) — described as the paper's main contribution
- Loss function or likelihood: DBN fine-tuned using Bayesian regularisation objective: F_W = αP + βE_W where P = mean squared error of predicted vs observed crash counts and E_W = mean squared weights. This is a continuous regression objective (MSE), not a Poisson likelihood.
- Offset/exposure term: none in DBN — AADT and length are normalised input features, not a formal offset. NB benchmark uses log(AADT × Length × 365 / 10^6) as a near-offset covariate.
- Spatial autocorrelation handling: none — observations treated as independent
- Temporal dependence handling: none — segment-year observations treated as independent
- Interpretability method: none described for DBN (black box); NB coefficients reported in Tables 4 and 5 with p-values
- Architecture specifics: 2 hidden layers; structures tested from 8–14 hidden neurons per layer; input layer size 13 features; output layer 1 unit (crash frequency). Greedy layer-wise unsupervised pre-training (RBM-based) followed by Bayesian regularisation supervised fine-tuning. Implemented in Matlab using code from www.deeplearning.net.
- Evidence quote or page reference: Section "Global deep belief network model", pp.160–162; Section "Model settings", pp.166–167

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Predictive error (held-out test set) | MAE | 9.59 | DBN, Ontario HWY401 | vs 12.39 for NB; 22.6% improvement | Table 6, p.168 |
| Predictive error (held-out test set) | RMSE | 19.58 | DBN, Ontario HWY401 | vs 28.94 for NB; 32.3% improvement | Table 6, p.168 |
| Predictive error (held-out test set) | MAE | 9.59 (before), 10.00 (global) | DBN individual vs global, Ontario | Global DBN slightly worse than individual; both better than NB | Table 8, p.170 |
| Predictive error (held-out test set) | MAE | 0.81 | DBN, Colorado rural two-lane | vs 0.83 for NB; 2.4% improvement | Table 7, p.169 |
| Predictive error (held-out test set) | RMSE | 1.48 | DBN, Colorado | vs 1.67 for NB; 11.4% improvement | Table 7, p.169 |
| Predictive error (held-out test set) | MAE | 0.47 | Global DBN, WA-R2 (rural 2-lane) | vs 0.50 for NB; 6.0% improvement | Table 8, p.170 |
| Predictive error (held-out test set) | MAE | 0.98 | Global DBN, WA-RM (rural multilane) | vs 0.98 for NB; 0% improvement | Table 8, p.170 |
| Predictive error (held-out test set) | MAE | 0.59 | Global DBN, WA-U2 (urban 2-lane) | vs 0.66 for NB; 10.6% improvement | Table 8, p.170 |
| Predictive error (held-out test set) | MAE | 1.91 | Global DBN, WA-UM (urban multilane) | vs 2.04 for NB; 6.4% improvement | Table 8, p.170 |
| Predictive error (held-out test set, sequential) | MAE | 10.68 | DBN after sequential retraining, Ontario | vs 12.39 for NB; 13.8% improvement; worse than simultaneously trained (10.00) | Table 9, p.172 |
| Benchmark comparison | MAE / RMSE | Various | Bayesian ANN, Ontario | MAE 11.61 vs DBN 9.59 — DBN outperforms Bayesian ANN | Table 6, p.168 |

**Metric qualification:**

- All reported MAE and RMSE values are computed on **temporally held-out test sets** (later years withheld during training). This constitutes genuine out-of-sample temporal validation — the most credible form of validation in this paper.
- No spatial holdout is used. Train and test sets are from the same geographic corridors, split only in time.
- No grouped holdout by road segment. Segment-year rows from the same physical segments appear in both train and test sets; only the years differ.
- The improvements over NB are modest for most cases (0–11% MAE) and negligible or negative in some cases (WA-RM rural multilane: 0% improvement; sequential training introduces some degradation on previously seen data).
- MAE and RMSE are mean absolute / root mean squared errors on raw crash count predictions — they are not rate-based or exposure-normalised metrics. High-AADT, long segments dominate the error on the Ontario case (mean 23.81 crashes/year).
- These metrics test **predictive generalisation in time** but not across geography or road types unseen during training.
- No calibration metrics, no overdispersion assessment, no Pearson or deviance goodness-of-fit reported.
- Most relevant metric for Open Road Risk: temporal MAE/RMSE on a held-out test set is a reasonable model comparison criterion, but it is insensitive to zero-heavy sparse counts (the metric is dominated by high-crash segments). Not directly benchmarkable against Open Road Risk's current metrics.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: not explicitly addressed. The paper uses MSE-based training which gives equal weight to all residuals in MAE but squares large errors in RMSE — neither is adapted to zero-heavy count data.
- Use of Poisson / negative binomial / zero-inflated models: NB is used as benchmark only; DBN uses MSE regression objective with no count distribution assumption. No zero-inflated or hurdle model.
- Zero-heavy counts handled using: not handled. Colorado dataset mean is 0.9 crashes/year with many zeros (min 0, high SD); Washington WA-R2 mean 0.47 crashes/year. The paper does not discuss zero excess or count distribution mismatch.
- Whether high-risk locations are evaluated separately: no. Results aggregated over all segments.
- Evidence quote or page reference: Tables 2–3 show many zero-crash segment-year observations (min = 0 in all datasets); no methodological discussion of this
- Practical relevance: The paper is largely silent on zero-heavy count structure — a significant methodological gap relative to Open Road Risk's needs. MSE regression on zero-heavy count data will underestimate uncertainty and produce non-integer, potentially negative predictions. This is a direct reason why the DBN approach, as implemented here, is not appropriate for Open Road Risk's link-year dataset where ~98–99% of rows have zero collisions.

---

## 11. Validation Strategy

- Train/test split method: temporal split — earlier years used for training, later years reserved for testing (Ontario: 2000–2006 train / 2007–2008 test; Colorado: 1991–1996 train / 1997–1998 test; Washington: not explicitly stated but same pattern implied)
- Spatial holdout used: no — same road segments appear in both train and test sets across years
- Temporal holdout used: yes — later years held out
- Grouped holdout used: no — segment-year independence assumed; same physical segments in train and test
- Cross-validation type: none — no cross-validation. Bootstrap resampling used to estimate variability of MAE/RMSE: 100 repetitions for Ontario Experiment 1; 25 for Colorado; 10 for Experiments 2 and 3 (this reduces initialisation variance, not train/test leakage)
- Metrics: MAE and RMSE on held-out test years
- External validation: none — Washington data is used in Experiments 2 and 3 as a "new" dataset for sequential training, but it is not an independent external validation; it is incorporated into the global model and evaluated on its own held-out years
- Leakage or generalisation risks:
  1. Same physical road segments appear in train and test sets (only years differ). Segment-specific characteristics that are stable over time will allow the model to partially memorise segment-level patterns. This is not classic data leakage but it means the temporal test overstates generalisation to new road segments.
  2. The paper's global DBN encodes dataset identity (location, road type, access type) as input features — this means the model is not truly "global" in the sense of generalising to unseen road types or regions; it is a multi-task model that requires explicit dataset labels at prediction time.
  3. Bootstrap repetitions re-use the same train/test split; they measure initialisation variance, not generalisation variance.
- Evidence quote or page reference: Section "Experimental design", p.163; "Repeat Step 2) for several times to reduce the error of affection of training set (100 times for HWY401)" (p.163)
- What I should copy: temporal train/test split is straightforward and used in Open Road Risk already (grouped split by road link). The bootstrap-of-initialisation approach for neural networks is worth noting if a DNN is ever evaluated.
- What I should avoid: treating temporal MAE/RMSE on same-segment test sets as strong evidence of generalisation to new road segments or new regions.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: In this study, a DBN trained with MSE regression achieves MAE/RMSE performance broadly comparable to or slightly better than locally calibrated NB models on temporally held-out test sets, across six highway types in North America. Improvements over NB range from 0% to 32% depending on the case, with the largest improvement on the Ontario multilane highway (high-volume, fewer zeros).
- Why it matters: This provides weak evidence that gradient-boosting-style non-parametric models can match NB for crash count prediction. However, the improvement is modest and the architecture (DBN with MSE loss) is not appropriate for Open Road Risk's zero-heavy link-year data. Open Road Risk's XGBoost already likely captures similar non-linear feature interactions without the exposure-offset problem introduced by the DBN.
- Evidence: Table 8, p.170
- Confidence: low for Open Road Risk generalisation — different highway types (no minor roads), different country, all crashes (not injury-only), no zero-heavy sparse link-year structure comparable to Open Road Risk's ~98% zero rate.

**Finding 2:**
- Finding: NB model coefficients for log(AADT) and log(Length) are close to 1.0 across all highway types and regions (Ontario: 0.827 for combined AADT × Length × 365 / 10^6; Colorado: 0.87 AADT + 0.97 length; Washington: 0.77–1.32 AADT + 0.85–1.00 length). This is consistent with the assumption that crash counts scale roughly proportionally with vehicle-kilometres travelled.
- Why it matters: Confirms the log-offset structure used in Open Road Risk Stage 2 is consistent with empirically estimated NB coefficients across multiple highway types. The near-unity coefficients support using a fixed offset (coefficient constrained to 1.0) rather than estimating it freely.
- Evidence: Tables 4 and 5, pp.167–168
- Confidence: medium — consistent finding across 6 highway types from 3 regions, though all are North American highways. UK road context may differ.

**Finding 3:**
- Finding: Shoulder width (both left and right) is significant and negative in most NB models for Washington highways (wider shoulders associated with fewer crashes). Lane width is also significant and negative (wider lanes associated with fewer crashes). Median width is significant (positive — wider medians associated with more crashes on some road types, possibly reflecting higher-speed divided roads).
- Why it matters: These geometry features are candidates for Open Road Risk's feature set. Shoulder width and lane width are not well covered in OS Open Roads or OSM at useful UK coverage, limiting immediate transferability. This finding supports their inclusion if coverage improves.
- Evidence: Table 5, p.168
- Confidence: medium for direction; low transferability to UK context (different road design standards, different speed environments).

**Finding 4:**
- Finding: Terrain type (mountainous / rolling / flat) is significant and positive in Colorado and Washington rural NB models — mountainous terrain associated with more crashes than flat terrain, after controlling for AADT and road geometry.
- Why it matters: Open Road Risk includes grade from OS Terrain 50 as a candidate feature. This paper provides supporting evidence that terrain/grade is a significant predictor on rural roads. The effect is only tested for rural highway types; urban models in this paper do not include terrain.
- Evidence: Tables 4 and 5, pp.167–168
- Confidence: medium — consistent across rural highway types in two US states; transferability to UK minor roads is uncertain.

**Finding 5:**
- Finding: Curve deflection (per km) has a significant negative coefficient in the Ontario NB model (more curvature → fewer crashes), which is counterintuitive. Authors do not comment on this. This is likely a confound specific to the access-controlled Highway 401 context, where curved sections may have lower speeds.
- Why it matters: Open Road Risk includes curvature as a candidate feature. This finding is a caution against expecting a universally positive effect of curvature on crash rates — the direction may reverse on high-speed access-controlled roads compared to minor roads. Feature effect direction should be validated by road class in Open Road Risk.
- Evidence: Table 4, p.167 (Curve deflection coefficient −0.132)
- Confidence: low for generalisability — specific to one access-controlled highway in Ontario; likely a confound with speed rather than a genuine safety effect of curvature.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| NB model structure with log(AADT × length) near-offset | Confirms Open Road Risk Stage 2 Poisson GLM offset structure; near-unity AADT and length coefficients support fixed offset approach | AADT, length — both present | 418–57k segments per dataset | High — already implemented in analogous form | Stage 2 — validation / documentation | Low (already implemented) | None for structure; confirms existing approach |
| Temporal train/test split (earlier years train, later years test) | Straightforward temporal validation design applicable to Open Road Risk panel data | Link-year panel — already structured | Multi-year panel | High — already used in Open Road Risk | Validation — documentation | Low | Segment-level leakage if same segments appear in both splits without grouped holdout |
| Terrain/grade as crash predictor (rural roads) | Provides supporting evidence for including OS Terrain 50 grade as Stage 2 feature | OS Terrain 50 — already a candidate | Rural highway context | Medium — effect may differ on full road network including urban and minor roads | Stage 2 — candidate feature documentation | Low | Effect direction may differ by road class; validate before using in production |
| Minimum segment length threshold (exclude very short links) | Supports Open Road Risk's handling of very short OS Open Roads links which have higher exposure uncertainty | OS Open Roads link length — already present | 0.16–0.2 km minimum used | High — applicable to Open Road Risk filtering | Stage 2 / feature engineering — documentation | Low | Threshold choice is empirical; 0.16 km may not translate directly to OS Open Roads context |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| DBN (Deep Belief Network) with MSE regression as crash count model | MSE regression is not appropriate for zero-heavy count data (~98–99% zeros in Open Road Risk); no Poisson offset structure; produces non-integer continuous predictions; no uncertainty quantification; no coefficient interpretability | Architecture mismatch with Poisson count structure; DBN requires tuning of multiple hyperparameters empirically | 71k–100k segment-year obs in this study | Low — DBN MSE regression fundamentally mismatched to Open Road Risk's sparse injury collision count data | Not recommended; XGBoost with Poisson objective is a better-suited non-parametric alternative already in use | High confidence in non-transferability |
| Global DBN pooling across highway types and regions | Requires dataset identity as explicit input; not truly global — still requires region/type label at prediction time; modest performance gains do not justify complexity over simpler road-type stratification | Dataset label encoding is ad-hoc; no principled pooling mechanism | 6 highway types, 3 regions | Low — Open Road Risk already covers multiple road types within a single model; XGBoost handles this via road classification features | Road type as feature already present in Open Road Risk | High |
| Shoulder width and lane width as features | Not available at useful coverage in OS Open Roads or OSM for UK road network at national scale | OS/OSM data coverage insufficient | Segment-level (GIS inventory) | Low for production; medium if OSM coverage improves | Document as future candidate; monitor OSM coverage | Medium |
| Sequential retraining / incremental DBN update | Performance gains from sequential retraining are small or negative in some cases; adds significant complexity | DBN architecture; iterative retraining infrastructure | Multi-year update scenario | Low — not a priority given the marginal gains shown | Not recommended | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?**
  Yes, via the NB benchmark results — near-unity coefficients on log(AADT × length) across all highway types and regions confirm the proportionality assumption underlying the log-offset approach in Open Road Risk Stage 2.

- **Does it suggest better handling of AADT/AADF uncertainty?**
  No — the paper assigns nearest observed count station without uncertainty propagation, similar to Open Road Risk's current approach. This is not addressed.

- **Does it suggest useful geometry or road-context features?**
  Partially — lane width, shoulder width, and terrain type are confirmed significant in NB models. Lane width and terrain grade are candidates in Open Road Risk; shoulder width has insufficient UK open-data coverage. Curve deflection shows a counterintuitive sign on an access-controlled highway — a caution for Open Road Risk's curvature feature.

- **Does it suggest better modelling of junctions?**
  No — intersections are explicitly excluded from the analysis.

- **Does it suggest better treatment of severity?**
  No — all crash types pooled as a single count with no severity breakdown.

- **Does it suggest better validation design?**
  Marginally — temporal holdout is used and is straightforward. However, grouped holdout by road segment (which Open Road Risk already uses) is absent in this paper and would be a stronger design.

- **Does it expose a weakness in my current approach?**
  Indirectly — the paper demonstrates that using AADT and length as unconstrained input features (rather than as a formal offset) in a non-parametric model is feasible but produces a continuous MSE-regression model that is poorly suited to zero-heavy count data. This is a warning about any future attempt to replace the Poisson GLM exposure offset with feature-engineering exposure in a gradient-boosted or neural model. Open Road Risk's current Poisson GLM correctly handles this; the XGBoost model's lack of a formal Poisson offset is the analogous concern in the existing pipeline.

---

## 15. Repo Actionability

**Action 1:**
- Suggested repo action: Add a documentation note to Stage 2 confirming that near-unity NB coefficients on log(AADT × length) across six highway types (Ontario, Colorado, Washington) support the fixed log-offset approach used in Open Road Risk's Poisson GLM. This provides cross-study evidence for the offset constraint.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: NB coefficients on AADT and length are consistently close to 1.0 across all six highway types and three regions (Tables 4–5), spanning urban and rural contexts
- Evidence: Tables 4 and 5, pp.167–168
- Effort: low
- Risk if implemented badly: low

**Action 2:**
- Suggested repo action: Add a documentation note that terrain type / grade is an empirically supported crash predictor on rural roads (this study, Colorado and Washington rural highways), supporting retention of the OS Terrain 50 grade feature as a Stage 2 candidate. Note the caveat that the effect is shown for rural highways only and may differ on urban or minor roads.
- Action type: documentation note / candidate feature validation
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Terrain-mountainous and terrain-rolling significant predictors in Colorado and Washington rural NB models (Tables 4–5)
- Evidence: Tables 4 and 5
- Effort: low
- Risk if implemented badly: low

**Action 3:**
- Suggested repo action: Add a note to the curvature feature documentation flagging that on access-controlled highways, curvature may have a counterintuitive negative association with crashes (more curvature → lower crash rate, likely confounded with speed). Validate curvature coefficient direction separately by road class (motorway/primary vs A/B/unclassified) in Stage 2 feature importance analysis.
- Action type: documentation note → diagnostic
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Ontario NB model shows significant negative curvature coefficient (−0.132) on Highway 401 access-controlled multilane highway (Table 4)
- Evidence: Table 4, p.167
- Effort: low (documentation); medium (if feature importance by road class is run)
- Risk if implemented badly: low — this is a diagnostic flag, not a production change

**Action 4:**
- Suggested repo action: Document that the DBN/DNN approach as implemented in this paper (MSE regression loss, AADT/length as features rather than offset, no count distribution) is not appropriate for Open Road Risk's sparse injury collision link-year data. If a neural model is ever evaluated for Stage 2, it should use a Poisson or negative binomial loss with a formal exposure offset, not MSE regression.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The paper's DBN uses MSE regression on zero-heavy count data without a Poisson offset — a structural mismatch that is illustrated by the fact that improvements over NB are modest and disappear for the rural multilane case (WA-RM: 0% MAE improvement). The paper itself acknowledges "several unsolved questions" remain (p.172).
- Evidence: Model architecture sections pp.160–162; Table 8 results
- Effort: low
- Risk if implemented badly: low

**Action 5:**
- Suggested repo action: Add a minimum segment length threshold check to the Open Road Risk data pipeline. The paper uses 0.16–0.2 km minimums citing "higher uncertainty and lower exposure problems" for very short road segments. Investigate the distribution of OS Open Roads link lengths and flag or filter links below a defensible threshold in Stage 2 diagnostics.
- Action type: diagnostic / documentation note
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Minimum-length exclusion is standard practice in SPF literature (multiple citations in paper, p.163); links below threshold have unreliable exposure estimates
- Evidence: p.163: "the shortest length of HS section was 0.2 km. This selection of a certain lower threshold value complies with literature"
- Effort: low
- Risk if implemented badly: low if diagnostic only; filtering too aggressively could remove legitimate short links in dense urban areas

---

## 16. Query Tags

- deep-belief-network
- DBN
- global-SPF
- negative-binomial
- MSE-regression
- exposure-offset
- AADT-feature
- temporal-holdout
- multi-highway-pooling
- terrain-feature
- lane-width
- shoulder-width
- curvature-sign-caution
- near-unity-AADT-coefficient
- homogeneous-section
- segment-length-threshold
- North-America
- low-UK-transferability
- zero-heavy-counts-unaddressed
- safety-performance-function

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high for the NB benchmark results and methodology; medium for DBN-specific technical details (Matlab implementation, exact RBM training convergence behaviour not fully verifiable)
- Important details not stated in the paper:
  - Washington dataset years not explicitly stated
  - Overdispersion parameter k of the NB models not reported
  - Whether crash data is injury-only or all-crash (implied to be all-crash but not stated)
  - Negative binomial model fit diagnostics (AIC, BIC, Pearson chi-squared) not reported
  - DBN training time and computational cost not stated
  - Whether AADT for Ontario is observed or interpolated for the ~15% of segments beyond 2 km from a counting station
- Parts of the paper that need manual checking:
  - Figures 3–8 (model performance plots) were not viewable; results described from tables which appear consistent with the text
  - Table 9 sequential training results contain a typographic ambiguity ("ON-R" referenced but not defined — likely "CO-R" Colorado rural)
- Any likely ambiguity or risk of misinterpretation:
  - The paper's headline claim ("at least comparable to NB") is technically true but the improvements are small and inconsistent. The Ontario improvement (32% RMSE) is driven by a single high-volume access-controlled highway where DBN's ability to capture non-linear interactions with geometric features is most useful; this should not be generalised to rural or minor roads with sparse zero-heavy counts.
  - The "global" model label is misleading — the model requires dataset identity labels at prediction time and is not transferable to road types or regions not represented in training data.
  - The DBN's lack of a Poisson offset structure is a fundamental methodological concern for sparse count data that the paper does not discuss. MAE and RMSE metrics do not expose this weakness because they are dominated by high-crash segments.