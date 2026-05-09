# Paper Extraction: Roll, Anderson, McNeil — Developing a Pedestrian Safety Performance Function for Oregon

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: dot_89189_DS1.pdf
- Suggested Markdown filename: paper-extraction-roll-2026-oregon-pedestrian-spf.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (binary; text extracted via pdftotext for analysis)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? Partial — text extracted from all 210 pages via pdftotext; tables and figures not fully readable in text extraction. Table values quoted below are from extracted text sections that were machine-readable. Coefficient tables for all 16 SPF types were not fully extracted; representative examples are used.
- Notes on access limitations: This is a 210-page technical report. Key sections (Introduction, Data Development, Methodology, Summary) were read in full. The 16 individual SPF result tables were partially readable; exact coefficient values for most SPF subtypes are not extracted here. Section 4.9 (Summary) and Appendix A (exposure-only model comparisons) were read.

**Scope warning:** This report is primarily about pedestrian crash prediction at urban intersections. It has **low direct relevance** to Open Road Risk, which models all-injury vehicle crash frequency on road links (not intersections, not pedestrian-specific). The extraction focuses on the limited transferable elements: data fusion methodology for sparse exposure estimation, and the NB SPF modelling approach. The pedestrian-specific content is noted but not extracted in detail.

---

## 1. Citation

- Title: Developing a Pedestrian Safety Performance Function for Oregon
- Authors: Josh Roll (Oregon DOT), Jason Anderson (Portland State University), Nathan McNeil (Portland State University)
- Year: 2026 (February 2026; report date January 2026)
- DOI or URL: FHWA-OR-RD-26-06; https://www.oregon.gov/ODOT/TD/TP_RES/
- Country / region studied: USA (Oregon, urban areas statewide; focus on Portland and Portland/Corvallis urban areas)
- Study setting: Urban (urban intersections only)

---

## 2. Core Objective

- One-sentence description: The report develops pedestrian crash frequency safety performance functions (SPFs) for urban intersections in Oregon, using estimated pedestrian volumes (AADPT) derived from a machine learning data fusion model as the primary exposure variable, alongside vehicle AADT.
- Main purpose: Safety performance function development; exposure estimation for sparse pedestrian counts
- Evidence quote: "This report details the development of a pedestrian safety performance function (SPF) for intersections in urban areas in the state of Oregon." (Abstract, p. iii)

---

## 3. Response Variable

- Target variable: Count of pedestrian injury crashes per intersection per year
- Collision type: All pedestrian crash types and severities combined (injury crashes involving a pedestrian)
- Severity handling: Not modelled separately — all severities combined
- Count, binary, rate, risk score, severity class, or other: Count (non-negative integer)
- Time window used for outcomes: Not precisely stated in extracted sections; implied multi-year from crash database (year range not confirmed from extracted text)
- Evidence quote: "For this work, all pedestrian crash types and severities were considered." (Section 4.1, p. 11)

---

## 4. Exposure Handling

- Exposure variable used, if any: Two exposure variables used jointly — (1) vehicle AADT at intersection (entering AADT calculated from approach legs); (2) Annual Average Daily Pedestrian Traffic (AADPT) estimated via data fusion model
- Traffic count source: Vehicle AADT from HPMS (Highway Performance Monitoring System) + INRIX probe data + data fusion model for missing segments. Pedestrian AADPT from traffic signal push-button actuations (558 intersections) + short-duration video counts (340 intersections) + ML data fusion model for all remaining urban intersections.
- Whether exposure is modelled, observed, assumed, or ignored: Both vehicle and pedestrian exposure are estimated via data fusion; not fully observed. HPMS provides observed AADT for higher-classification roads; lower-classification roads use INRIX or ML-estimated AADT.
- Treatment of missing or sparse traffic counts: Three-tier approach for vehicle AADT: (1) HPMS observed, (2) INRIX probe-based estimate, (3) random forest data fusion model using functional class, network centrality, access to jobs, connected segment volumes, urban area. Nine sub-models developed based on data availability. For pedestrian AADPT: data fusion model trained on 868 AADPT observations (558 signal push-button + 340 short-duration counts), applied to all urban intersections statewide.
- Whether offset terms, rates, denominators, or normalisation are used: Not stated in extracted sections for SPF structure. Standard SPF form (Poisson/NB) implies log(AADT × AADPT) or log(AADT) + log(AADPT) as offsets or covariates. From Section 4.1 and Table 4.9: AADT and AADPT enter as covariates (in thousands), not as a single combined offset. Exact offset structure not confirmed from extracted text.
- Evidence quote: "Nine models are developed based on data availability so that no segment is discarded due to one or more variables missing when the model is applied." (Section 3.4.3)
- Transferability to my AADF/WebTRIS setup: Mixed — the three-tier AADT estimation approach (observed → probe → ML data fusion) is structurally analogous to Open Road Risk's Stage 1a AADT estimator, though using different data sources. The pedestrian AADPT estimation pipeline is not relevant to Open Road Risk.
- Notes: The INRIX probe-based AADT tier is commercially licensed; not in Open Road Risk's open-data stack. HPMS is a US federal data system with no UK equivalent; the analogous UK source is AADF counts.

---

## 5. Spatial Unit of Analysis

- Unit: Urban road intersection (node-level), disaggregated by intersection type (3-leg / 4-leg), traffic control (signalised / unsignalised), and presence of marked crossings
- Segment length or segmentation rule: Not applicable — intersection-level analysis, not segment-level
- How crashes are assigned to the network: Crashes assigned to intersections using spatial proximity to intersection nodes; intersection contraction algorithm used to merge nearby nodes into single intersection entities (Figure 3.8 in report)
- Treatment of junctions/intersections: This paper is exclusively about intersections — the opposite of Open Road Risk's current focus on road links (excluding junctions)
- Spatial aggregation risks: Intersection contraction may merge distinct conflict points; not discussed as a concern
- Relevance to OS Open Roads link-based pipeline: Very low — Open Road Risk currently models road links. This paper's unit of analysis is intersections. The two approaches are complementary, not competing.

---

## 6. Temporal Unit of Analysis

- Years covered: Pedestrian count data 2017–2023; crash data year range not confirmed in extracted text
- Temporal resolution: Annual (AADPT and AADT are annual averages)
- Whether seasonality or time-of-day is modelled: Seasonal factoring methods tested for short-duration pedestrian counts (AASHTO method vs day-of-year method); seasonality addressed in the exposure estimation step, not in the SPF
- Whether before-after or panel structure is used: Not stated; likely cross-sectional SPF
- Relevance to WebTRIS-style time profiles: The short-duration factoring methodology (expanding a short count to an annual average) is structurally analogous to what Open Road Risk does with WebTRIS time profiles. The report tests AASHTO vs day-of-year factoring methods; this may be a useful methodological reference if Open Road Risk extends WebTRIS profile factoring.

---

## 7. Engineered Features

Only features relevant to Open Road Risk are noted. Full feature set for pedestrian AADPT model is not extracted.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Vehicle AADT (entering) | HPMS / INRIX / random forest data fusion | Three-tier: observed → probe estimate → ML fusion; 9 sub-models for different data availability patterns | Primary vehicle exposure for SPF | Medium — analogous to Stage 1a; US data sources differ but approach transferable |
| Pedestrian AADPT | Push-button actuations + short-duration video counts | ML data fusion (random forest best performer in 10-fold CV) trained on 868 observations; applied to all urban intersections | Pedestrian exposure — primary innovation of report | Low — no equivalent push-button data source in UK open data stack; pedestrian SPF out of Open Road Risk scope |
| Functional classification | HPMS / OSM | Used in AADT data fusion sub-models | Road type as AADT predictor | Already present — OS Open Roads road classification used similarly in Stage 1a |
| Network centrality measures | OSM-derived | Betweenness / degree centrality for intersection context | Network position as AADT proxy | Already present in Open Road Risk Stage 1a / candidate Stage 2 feature |
| Access to jobs | Census / land use data | Spatial join; used in AADT data fusion | Demand proxy for trip generation | Candidate — IMD employment domain available in UK as proxy |
| Urban area classification | Census geographies | Spatial join to assign intersections to urban area bounds | Controls for systematic urban area differences | Already present — rural/urban classification in Open Road Risk |
| Marked crosswalk presence | Field observation / GIS | Binary indicator; used to stratify SPF models | Crosswalk affects pedestrian exposure and safety | Not applicable — pedestrian infrastructure data not in Open Road Risk |
| Intersection typology (3-leg / 4-leg, signal / unsignalised) | OSM + signal database | Graph-based contraction algorithm + recursive partitioning for traffic control classification | Stratification variable for SPF | Candidate for future junction model in Open Road Risk; not current scope |

---

## 8. Model Architecture

- Algorithms/models used: (1) Poisson regression; (2) Negative Binomial (NB) if overdispersion detected; both applied for each of 16 intersection type × geography × system combinations. For AADT estimation: random forest data fusion (best performer). For pedestrian AADPT estimation: multiple ML models tested (random forest best); NB with mixed effects used for AADPT demand model (Table 3.6).
- Baseline model: Poisson SPF estimated first; overdispersion test applied; NB estimated if overdispersion present
- Final/preferred model: Negative Binomial for most SPF types (overdispersion present in pedestrian crash data)
- Loss function or likelihood: Maximum likelihood (NB log-likelihood)
- Offset/exposure term, if used: AADT and AADPT enter as covariates (in thousands) in the SPF equations, not as a formal log-offset. Coefficient signs and significance reported per intersection type and geography (Tables 4.1–4.16).
- Spatial autocorrelation handling: None described for SPF; NB with mixed effects used for AADPT demand model (Table 3.6)
- Temporal dependence handling: Not described
- Interpretability method: Coefficient direction and significance per intersection type; CURE plots for model fit assessment; Appendix A provides full-model vs exposure-only model comparisons
- Evidence quote: "To develop the pedestrian crash frequency models, count-data models were used based on the nature of the dependent variable; that is, non-negative integer counts." (Section 4.1, p. 11)

**Important finding on model complexity:** The report explicitly chose exposure-only models (vehicle AADT + pedestrian AADPT only) over more complex models including built-environment features, because "despite some improvements in model fit (per the log-likelihood values), overall, there were not substantial improvements in how the model estimated expected crash frequencies." (Section 4.1, p. 11) This is a directly relevant finding for Open Road Risk's feature selection philosophy.

---

## 9. Reported Metrics / Quantitative Results

Full coefficient tables for all 16 SPF types are not completely extracted from the 210-page report. Representative results from extracted text:

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence |
|---|---|---|---|---|---|
| SPF coefficient direction | AADT effect on pedestrian crashes | Positive (some NS) | 4-leg signalised, statewide, state system | Higher vehicle volume → more pedestrian crashes (expected) | Table 4.9 extracted text |
| SPF coefficient direction | AADPT effect on pedestrian crashes | Positive (significant: *) | 3-leg signalised, statewide, state system (n=169) | Higher pedestrian volume → more pedestrian crashes | Table 4.9 extracted text |
| SPF coefficient direction | AADT (Portland City Limits) | Negative (NS) | 3-leg signalised, Portland City Limits (n=36) | AADT not significant in smaller geographic subsets — small n problem | Table 4.9 extracted text |
| AADPT ML model validation | 10-fold cross-validation | Best performer: random forest | vs NB mixed effects, other ML methods | Random forest most accurate for AADPT estimation | Section 3.7.6; Table 3.7 |
| AADT estimation | Median absolute percent error | Shown in Figure 3.6 (not numerically extracted) | Random forest data fusion | ODOT previously validated INRIX AADT estimates as accurate vs observed counts | Section 3.4.3 |
| Model complexity finding | Full model vs exposure-only | No substantial improvement from adding built-environment features | All intersection types | Adding complexity did not materially improve expected crash frequency prediction | Section 4.1; Appendix A |

**Validation type:** The AADPT data fusion model uses 10-fold cross-validation on the 868 AADPT observations. The SPF models do not describe a holdout validation — model fit is assessed via log-likelihood and CURE plots (cumulative residual plots), which are in-sample diagnostics. No external validation of the SPFs on held-out intersections is described.

**Most relevant metric for Open Road Risk:** The 10-fold cross-validated AADPT model performance (Table 3.7) is methodologically relevant as a benchmark for how a sparse-observation data fusion model for pedestrian counts was validated — analogous to Open Road Risk's Stage 1a grouped cross-validation for AADT. Exact error values from Table 3.7 not extracted (table not machine-readable from text extraction).

---

## 10. Rare Event / Class Imbalance Handling

- How rare events are handled: Pedestrian crashes are rare per intersection; the NB model addresses overdispersion. The report does not describe zero-inflated modelling; NB is the chosen response to overdispersion.
- Model family: Negative Binomial (when overdispersion detected); Poisson (when overdispersion not detected)
- Zero-heavy counts: Not explicitly described as zero-inflated; NB handles overdispersion. Some intersection subtypes have small n (e.g., n=36 for Portland City Limits 3-leg signalised), which limits reliability of those models.
- Practical relevance: Limited — Open Road Risk's zero-heavy link-year counts on road segments are a different and more extreme sparsity problem than intersection-level pedestrian crashes in urban areas.

---

## 11. Validation Strategy

- Train/test split method: AADPT data fusion model: 10-fold cross-validation on 868 observations. SPF models: no described train/test split; CURE plots used for in-sample fit assessment.
- Spatial holdout used? Not stated for SPFs; 10-fold CV for AADPT model (likely random folds, not spatial)
- Temporal holdout used? No
- Grouped holdout used? Not stated
- Cross-validation type: 10-fold for AADPT ML model; none described for SPFs
- Metrics: APE and RMSE for AADPT model; log-likelihood and CURE plots for SPFs
- External validation: None described
- Leakage risks: AADPT push-button counts and short-duration counts used to train data fusion model are drawn from across the state; some intersections with push-button counts may be similar to validation intersections if random folds rather than spatial folds are used. Not discussed.
- What I should copy or avoid: The CURE plot approach for SPF fit assessment is a useful diagnostic — CURE plots show cumulative residuals against AADT and flag model misspecification at specific volume ranges. This could be applied to Open Road Risk's Poisson GLM as a diagnostic. Do not adopt the SPF model structure directly (pedestrian-specific, intersection-level, Oregon-calibrated).

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: Adding built-environment, land use, and sociodemographic features to the pedestrian SPF did not substantially improve prediction of expected crash frequency over a simpler exposure-only model (vehicle AADT + pedestrian AADPT). This held across all intersection types and geographies examined.
- Why it matters: This is the most directly relevant finding for Open Road Risk's feature engineering strategy. It suggests that for crash frequency prediction, the exposure variables (AADT × pedestrian/network exposure) dominate, and adding contextual features may improve log-likelihood marginally without meaningfully improving how well the model estimates expected crashes. This does not prove the same for Open Road Risk's all-vehicle model, but it is a methodological data point supporting parsimony.
- Evidence: "despite some improvements in model fit (per the log-likelihood values), overall, there were not substantial improvements in how the model estimated expected crash frequencies. For this reason, the trade-off between usability and complexity of model specifications was carefully considered, where the overall usability of the models was chosen over complex model specifications." (Section 4.1, p. 11)
- Confidence: Medium — consistent across 16+ SPF variants within this study; pedestrian intersection context may not generalise to all-vehicle road link models.

**Finding 2:**
- Finding: A three-tier AADT estimation pipeline (observed counts → INRIX probe estimates → random forest data fusion using functional class, centrality, jobs access, connected volumes) was implemented to ensure complete AADT coverage for urban intersections in Oregon. The data fusion model was evaluated with a 10-fold cross-validation using median absolute percent error and RMSE.
- Why it matters: The hierarchical exposure estimation approach is structurally analogous to Open Road Risk's Stage 1a, with the same challenge of partial observability. The specific use of network centrality and connected segment volumes as predictors in the data fusion model is directly relevant — both are already in Open Road Risk's Stage 1a feature set. The random forest outperforming statistical models for AADT estimation is consistent with Open Road Risk's Stage 1a gradient boosting approach.
- Evidence: Section 3.4.3; Figure 3.6 (10-fold CV error by AADT band)
- Confidence: Medium — analogous methodology but different data sources and geography.

**Finding 3:**
- Finding: Random forest was the best-performing model for pedestrian AADPT data fusion in 10-fold cross-validation, outperforming negative binomial mixed effects and other ML approaches (Table 3.7). The key predictors for pedestrian volume included operational speed, school area proximity, and median income.
- Why it matters: Confirms ML (specifically tree-based ensemble) superiority over statistical models for sparse-count exposure estimation — directly analogous to Stage 1a finding. The sociodemographic predictors (income, school proximity) are worth noting as potential exposure proxies for pedestrian risk at intersections, though not directly applicable to Open Road Risk's vehicle-focused scope.
- Evidence: Section 3.7.6; Table 3.7; Figures 3.19–3.21 (marginal effects on AADPT)
- Confidence: High within this study; random forest superiority for AADT/exposure estimation is a consistent finding across multiple contexts.

**Finding 4:**
- Finding: The AADPT variable is often statistically insignificant in SPF models for smaller geographic subsets (e.g., Portland City Limits models with n=36), even though it is significant in statewide models (n=169). This is a small-sample problem, not necessarily evidence that pedestrian exposure is unimportant.
- Why it matters: Open Road Risk faces an analogous problem at facility-family level — splitting the full dataset into subgroups (e.g., motorway-only, rural A-road) reduces n per model and risks losing statistical power for exposure coefficients. The report's approach of maintaining statewide models alongside subgroup models as a fallback is a practical design precedent.
- Evidence: Table 4.9 (AADPT NS for Portland City Limits n=36 vs significant for statewide n=169)
- Confidence: High as an illustration of small-n effects; generalisation to Open Road Risk design is straightforward.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| CURE plots for SPF fit assessment | Cumulative residual plots flag model misspecification at specific AADT or link-length ranges; complement to pseudo-R² and AIC | Open Road Risk GLM predictions + observed counts (already available) | Urban intersections Oregon | Compatible — applicable to any count model | Stage 2 / validation diagnostic | Low | CURE plots are easier to interpret when model is well-specified; may be hard to interpret with 2.1M observations without binning |
| Three-tier exposure estimation with 10-fold CV evaluation by data tier | Hierarchical fallback for exposure coverage; CV-based evaluation disaggregated by data source quality | AADF observed + candidate proxies | Urban Oregon intersections | Compatible in principle; Stage 1a already uses similar tiering implicitly | Stage 1a / documentation | Low (document existing approach; no new implementation needed) | None for documentation |
| Exposure-only model as parsimony baseline | Use exposure-only NB/Poisson as baseline against which to test feature additions; if full model does not substantially outperform exposure-only, prefer simpler model | Open Road Risk Stage 2 data | Urban Oregon intersections | Compatible | Stage 2 / validation | Low | Pedestrian crash context may not apply to all-vehicle link model; test independently |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Pedestrian SPF (AADPT as exposure) | Open Road Risk models all-vehicle crashes on road links, not pedestrian crashes at intersections | AADPT data not available in UK open data | Urban Oregon | Incompatible — different outcome, different unit of analysis | Not applicable | High |
| Traffic signal push-button derived pedestrian counts | Requires access to traffic signal controller data from a highways agency; not available in UK open data at national scale | Push-button actuation data | 558 Oregon intersections | Incompatible | No open UK equivalent; Strava pedestrian/cycling data is a possible partial proxy | High |
| INRIX probe-based AADT estimates | Commercial product; not in Open Road Risk's open-data stack | INRIX licence | Urban Oregon | Incompatible | WebTRIS probe vehicle data (National Highways only) is partial equivalent for motorways; not nationally available | High |
| Intersection-level SPF structure | Open Road Risk's unit is OS Open Roads links, not intersections. Junctions are currently excluded from the modelling approach | No data gap; structural mismatch | Urban Oregon | Incompatible with current scope | A future junction module could use an intersection-level approach; not current production | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Indirectly — both vehicle AADT and pedestrian AADPT are used as exposure covariates. The exposure-only model performs nearly as well as the full model, supporting exposure as the dominant predictor.
- **Does it suggest better handling of AADT/AADF uncertainty?** Yes — the three-tier hierarchical estimation approach and 10-fold CV evaluation by data source tier are methodologically relevant to Open Road Risk's Stage 1a. Confirms random forest superiority for sparse-count exposure estimation.
- **Does it suggest useful geometry or road-context features?** For the pedestrian AADPT model: operational speed and school area proximity are significant. For vehicle SPFs: only AADT and AADPT used. No new geometry features for Open Road Risk.
- **Does it suggest better modelling of junctions?** Tangentially — the intersection contraction algorithm (merging nearby nodes into intersection entities) is relevant if Open Road Risk were to add a junction module. Not current scope.
- **Does it suggest better treatment of severity?** No — all severities combined.
- **Does it suggest better validation design?** The CURE plot approach is worth adopting as a Stage 2 diagnostic alongside existing metrics.
- **Does it expose a weakness in my current approach?** One point: Open Road Risk does not currently have a systematic way to compare feature-rich vs exposure-only models. This paper demonstrates a clean Appendix A approach (full model vs exposure-only comparison across all intersection types) that could be adopted as a standard diagnostic for Open Road Risk's Stage 2.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Implement CURE plots as a Stage 2 Poisson GLM diagnostic — plot cumulative residuals against log(AADT), link length, and road classification to check for model misspecification at specific ranges. Flag as a validation diagnostic, not a model selection criterion.
- Action type: Diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: CURE plots used throughout Section 4 to assess SPF fit across AADT ranges; standard in HSM SPF development.
- Effort: Low (CURE plots are straightforward to compute from GLM residuals)
- Risk if implemented badly: CURE plots with 2.1M observations require binning by AADT quantile to be interpretable; individual-point CURE plots would be unreadable at scale.

**Action 2**
- Suggested repo action: Add a Stage 2 documentation note that an exposure-only model (log offset only, no geometry features) should be run as a baseline, with log-likelihood and pseudo-R² compared to the full feature model. If the full model does not substantially outperform the exposure-only baseline, document this and consider whether feature additions are justified.
- Action type: Documentation note / baseline comparison
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Report found no substantial improvement from adding built-environment features over exposure-only for pedestrian SPFs; Appendix A provides the comparison template.
- Effort: Low (exposure-only model already implicitly available as a degenerate case of current GLM)
- Risk if implemented badly: The null result for pedestrian intersections may not hold for all-vehicle road links; do not use this finding to discard feature engineering without testing.

**Action 3**
- Suggested repo action: Document that Open Road Risk's Stage 1a three-tier AADT estimation (AADF observed → interpolated → estimated) is analogous to the Oregon HPMS → INRIX → data fusion pipeline, and that random forest / gradient boosting superiority for sparse exposure estimation is now supported by two independent studies (this report + Open Road Risk's own Stage 1a CV R² 0.83). Add this as a literature support note.
- Action type: Documentation note
- Relevant stage: Stage 1a / documentation
- Why the paper supports it: Section 3.4.3 random forest best performer for AADT data fusion; 10-fold CV validation.
- Effort: Low
- Risk if implemented badly: None for documentation.

**Action 4**
- Suggested repo action: Note in Stage 2 documentation that small geographic or facility-family subsets (e.g., motorway-only, n < 100 link-years with crashes) will have insufficient power to detect significant exposure coefficients, analogous to Portland City Limits n=36 subsets in this report. Recommend a minimum sample size threshold before interpreting subgroup model coefficients.
- Action type: Documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: AADT and AADPT insignificant in n=36 Portland City Limits subsets despite being significant statewide (Table 4.9).
- Effort: Low
- Risk if implemented badly: None for documentation.

---

## 16. Query Tags

- pedestrian-SPF
- negative-binomial
- Poisson
- intersection-level
- AADPT-exposure
- pedestrian-volume-estimation
- data-fusion-ML
- random-forest-AADT
- HPMS-OSM-conflation
- CURE-plots
- exposure-only-baseline
- sparse-exposure-estimation
- 10-fold-cross-validation
- urban-Oregon
- network-centrality-AADT
- low-transferability-pedestrian
- SPF-complexity-tradeoff
- small-n-subgroup-warning
- three-tier-AADT-pipeline

---

## 17. Confidence and Gaps

- Overall confidence in extraction: Medium — the 210-page report was read by text extraction; individual SPF coefficient tables for all 16 intersection subtypes were not fully machine-readable. Key methodology sections, data development, and summary were read in full. The specific coefficient values in Tables 4.1–4.16 are not individually extracted here.
- Important details not stated in extracted text: Exact crash year range for SPF development. Exact RMSE and APE values from Table 3.7 (10-fold CV for AADPT model — table was not machine-readable). Exact SPF equation form (whether AADT/AADPT enter as offsets or free covariates — inferred as free covariates from Table 4.9 structure but not confirmed from a model equation in extracted text).
- Parts of the paper that need manual checking: Table 3.7 (10-fold CV AADPT model error metrics) — verify best model error magnitude. Section 4.9 Summary — verify that the "no substantial improvement" finding applies consistently across all 16 SPF types, not just a subset.
- Any likely ambiguity or risk of misinterpretation: (1) The "no substantial improvement" from adding features is a deliberate design choice trading usability for accuracy; it does not mean features are irrelevant to pedestrian crash risk — only that they did not improve this SPF's expected frequency estimates enough to justify the complexity. This should not be read as evidence that features are unimportant for Open Road Risk's all-vehicle model. (2) The pedestrian SPF is entirely different in scope from Open Road Risk; the extraction should not imply otherwise.
