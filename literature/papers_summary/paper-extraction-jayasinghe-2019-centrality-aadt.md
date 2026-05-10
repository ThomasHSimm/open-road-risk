# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: 1-s2_0-S2215016119301128-main.pdf
- Suggested Markdown filename: paper-extraction-jayasinghe-2019-centrality-aadt.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 17-page paper accessible. All tables and figures readable. No OCR errors apparent.

---

## 1. Citation

- Title: A novel approach to model traffic on road segments of large-scale urban road networks
- Authors: Amila Jayasinghe, Kazushi Sano, C. Chethika Abenayake, P.K.S. Mahanam
- Year: 2019
- DOI or URL: https://doi.org/10.1016/j.mex.2019.04.024
- Country / region studied: Sri Lanka, Cambodia, Vietnam, Pakistan, Tanzania (five developing-country cities)
- Study setting: urban

---

## 2. Core Objective

- One-sentence description: The paper proposes and validates a network centrality-based method to estimate AADT at the road segment level using only road network geometry and a small number of observed traffic counts, without requiring land-use data, OD matrices, or extensive count coverage.
- Main purpose: prediction (AADT estimation / traffic volume modelling)
- Evidence quote or page reference: "The objective of this study is to develop a network centrality-based method to model the vehicular traffic volume of road segments at macro level road networks." (p. 1149)

---

## 3. Response Variable

- Target variable: Annual Average Daily Traffic (AADT), expressed as Passenger Car Units (PCU) per day
- Collision type: Not applicable — this is a traffic volume modelling paper, not a collision paper
- Severity handling: Not applicable
- Count, binary, rate, risk score, severity class, or other: continuous count (AADT in PCU/day)
- Time window used for outcomes: Single cross-sectional year per city (Colombo 2013, Phnom Penh 2012, Hanoi 2007, Karachi 2010, Dares Salaam 2008)
- Evidence quote or page reference: "Traffic volume has been reported as Annual Average Daily Traffic (AADT), converted to Passenger Car Unit (PCU) per day using the recommended AASHTO PCU factors." (p. 1153)

---

## 4. Exposure Handling

- Exposure variable used, if any: Not applicable. AADT is the target variable, not an exposure offset. The paper estimates traffic volume, not collision risk.
- Traffic count source: JICA database (CoMTrans Urban Transport Master Plan for Colombo; Person Trip Survey for other cities). Sample surveys over 7,000 road segments across five cities.
- Whether exposure is modelled, observed, assumed, or ignored: AADT is the modelled output, not an input. A small subset of observed AADT counts is used for model calibration (as few as 40 observations).
- Treatment of missing or sparse traffic counts: Central to the paper's motivation. The method is designed to work with very few count observations. Repeated random sub-sampling validation shows acceptable RMSE (< 30%) after ~40 calibration observations (Table 5, p. 1155).
- Whether offset terms, rates, denominators, or normalisation are used: No offset terms. Centrality values are normalised within the network. Road-type speed values (Ty) are used to weight metric distance in the path-distance variable.
- Evidence quote or page reference: "the study found that the centrality based AADT estimation model can be calibrated by using a little number of observation points (N < 40) with an acceptable level of accuracy." (p. 1159)
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The mathematical structure (regression of AADT on BC and CC) is medium-transferable as a conceptual benchmark or diagnostic check on whether Stage 1a centrality features add predictive value. The paper's specific traffic data (JICA surveys) has no direct equivalent, but Open Road Risk already uses AADF counts for calibration — a directly comparable setup. The key limitation is that this paper applies to developing-country urban networks; transferability to England's mixed urban/rural/motorway network at 2.1M links is uncertain and untested.

---

## 5. Spatial Unit of Analysis

- Unit: road segment (dual-graph representation)
- Segment length or segmentation rule: Not fixed-length. Segments follow the road centreline geometry of the input network. The paper uses a dual-graph in which each road segment is a node. Segment definition follows source GIS data (road centrelines).
- How crashes are assigned to the network: Not applicable — no collision data used.
- Treatment of junctions/intersections: In the dual-graph method, intersections are represented as edges between segment-nodes, not as primary units. The paper explicitly chooses dual graph over primal graph because focus is on road segments, not junctions (p. 1150).
- Spatial aggregation risks: The paper does not discuss spatial aggregation risks explicitly. Centrality values are global (computed across the whole network within a 20 km radius), which means centrality scores for any given segment depend on the full network topology — a potential boundary effect not discussed.
- Evidence quote or page reference: "As the focus of this method is road segments, not the junctions, the dual graph method was employed." (p. 1150)
- Relevance to OS Open Roads link-based pipeline: Direct. OS Open Roads links are structurally equivalent to the dual-graph road segments used here. Betweenness centrality is already listed as a feature in Open Road Risk. The paper's dual-graph approach is consistent with OS Open Roads link geometry.

---

## 6. Temporal Unit of Analysis

- Years covered: Single cross-sectional year per city (see Section 3 above)
- Temporal resolution: Annual (AADT only)
- Whether seasonality or time-of-day is modelled: Not modelled. The paper explicitly acknowledges this as a limitation: "the validation does not explicitly account the seasonal variations of traffic volumes and the daily peaks flow." (p. 1159)
- Whether before-after or panel structure is used: No — single time point per city
- Evidence quote or page reference: "Further studies are required to test the sensitivity of this model to such fluctuations and congestions propagation." (p. 1160)
- Relevance to WebTRIS-style time profiles: None. The paper acknowledges the need for dynamic/temporal models but does not develop them. No time-of-day or seasonal modelling is present.

---

## 7. Engineered Features

Only features actually used in the paper's model (Eq. 6: TV(i) = a + b[CC(i)] + c[BC(i)]):

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Betweenness Centrality with path-distance (BC_PD) | Road network centreline GIS data | Dual-graph BC computed via sDNA tool using path-distance (PD = MD × Ty) as edge weight; 20 km radius | Captures pass-by trip volume; partial R² ~60% of AADT variability in this study | Already present in Open Road Risk — compare implementation against sDNA path-distance variant |
| Closeness Centrality with path-distance (CC_PD) | Road network centreline GIS data | Dual-graph CC computed via sDNA tool using path-distance as edge weight; 20 km radius | Captures O-D trip generation; partial R² ~32–35% of AADT variability | Already present in Open Road Risk — compare implementation against sDNA path-distance variant |
| Path Distance (PD = MD × Ty) | Road type classification + segment metric length | Road type mapped to average speed band (Ty values: 1/80 for expressway down to 1/15 for local road); multiplied by metric distance | Weights shortest-path computation by road mobility characteristics rather than pure topology or metric distance | Medium — Open Road Risk has road classification; Ty speed-band mapping could be approximated with OS road hierarchy. UK speed bands would need recalibration. |

No other features are used in the model. The paper explicitly excludes land use and OD data.

---

## 8. Model Architecture

- Algorithms/models used: Ordinary Least Squares Regression (OLS), Robust Regression (RR), Poisson Regression (PR) — all tested. OLS selected as best fit based on R² and MdAPE (Table 3 implies OLS; Poisson regression mentioned as a tested alternative but not selected as the reported model).
- Baseline model: BC alone as single predictor (R² < 0.8, RMSE > 40%)
- Final/preferred model: TV(i) = a + b[BC_PD(i)] + c[CC_PD(i)] — linear regression with two centrality predictors. R² > 0.90, RMSE < 30%, MdAPE < 20%.
- Loss function or likelihood, if stated: Not stated explicitly. OLS implied by R² and RMSE reporting.
- Offset/exposure term, if used: None. AADT is the response variable, not offset-adjusted.
- Spatial autocorrelation handling: Not addressed. The paper does not test for spatial autocorrelation in residuals.
- Temporal dependence handling: Not applicable (cross-sectional).
- Interpretability method: Partial and part correlations reported to decompose BC vs CC contribution (Table 3, p. 1154).
- Evidence quote or page reference: "the proposed model comprised of BC and CC as explanatory variables produces a higher goodness of fit values (R² > 0.9) and lesser Percent Root Mean Squared Error (RMSE < 20%) compared to the model comprised of BC as the explanatory variable (R² < 0.8, RMSE > 40%)." (p. 1154)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Goodness of fit (calibration) | R² | 0.916–0.977 | BC+CC model, all five cities | High proportion of AADT variance explained in training data | Table 3, p. 1154 |
| Goodness of fit (validation) | R² | 0.923–0.959 | BC+CC model, all five cities | Similar R² on held-out 20% random sample | Table 3, p. 1154 |
| Error (calibration) | MdAPE | 12.6%–18.4% | BC+CC model, all five cities | Median absolute percent error within international standards | Table 3, p. 1154 |
| Error (validation) | MdAPE | 10.5%–17.3% | BC+CC model, all five cities | MdAPE on held-out 20% random sample | Table 3, p. 1154 |
| Error by AADT category | RMSE | Varies; within FHWA thresholds for most categories | All five cities | RMSE < 30% for most AADT categories; worst for very low AADT (< 1,000): RMSE 193% Colombo, 412% Phnom Penh | Table 4, p. 1155 |
| Sensitivity: minimum observations | RMSE at N=40 | < 30% across all cities | BC+CC model | Acceptable accuracy with ~40 count observations | Table 5 and Fig. 6, p. 1155 |
| Baseline (BC only) | R² | < 0.8 | BC-only model | Substantially weaker than combined model | p. 1154 |
| Baseline (BC only) | RMSE | > 40% | BC-only model | Fails international standards | p. 1154 |
| Partial correlation² | BC contribution | ~59–62% | BC+CC model, all cities | BC explains majority of AADT variance | Table 3, p. 1154 |
| Partial correlation² | CC contribution | ~32–35% | BC+CC model, all cities | CC adds substantial independent contribution | Table 3, p. 1154 |

**Validation type:** Mixed. Calibration metrics are in-sample. Validation R² and MdAPE use a randomly held-out 20% subset — this is a random split, not a spatial holdout or temporal holdout. There is no spatial or temporal cross-validation.

**Critical note on low-AADT accuracy:** RMSE for segments with AADT < 1,000 is extremely high (193% in Colombo, 412% in Phnom Penh). This is directly relevant to Open Road Risk because low-traffic rural links are common in the study area. The model is most reliable for higher-volume roads.

**Do these metrics test predictive generalisation?** Partially. The random 80/20 split provides a weak out-of-sample check, but random splits from the same spatial network do not test spatial generalisation. Results may be optimistic for deployment to new network areas. No spatial holdout is used.

**Most relevant metric to Open Road Risk:** The sensitivity analysis (Table 5) showing acceptable RMSE at N=40 is the most directly useful finding, as it addresses how few count observations are needed to calibrate a centrality-based AADT model — relevant to Stage 1a sparse AADF count coverage.

---

## 10. Rare Event / Class Imbalance Handling

- Not applicable. This paper models AADT (a continuous count), not collision occurrence.
- The paper does not discuss zero-heavy counts or rare events.
- The high RMSE for very low AADT segments (< 1,000) is the closest analogue — the model performs poorly on low-volume roads, which is a relevant limitation for rural links in Open Road Risk.
- Evidence quote or page reference: Table 4, p. 1155 — RMSE for AADT < 1,000: 193.1% (Colombo), 412.5% (Phnom Penh).
- Practical relevance to my sparse collision link-year dataset: Indirect. The poor performance at low AADT is a signal that centrality-only AADT estimation degrades on low-hierarchy roads. Open Road Risk Stage 1a already uses gradient boosting with additional features, which may handle low-traffic links better than the two-predictor linear model here.

---

## 11. Validation Strategy

- Train/test split method: Random 80/20 split of available count observations within each city
- Spatial holdout used? No
- Temporal holdout used? No (single cross-sectional time point per city)
- Grouped holdout used? No
- Cross-validation type: Repeated random sub-sampling validation used only for the minimum-observations sensitivity analysis (Table 5). Standard model validation uses a single 80/20 random split.
- Metrics: R², MdAPE, RMSE by AADT category
- External validation: The five cities constitute cross-city validation in that the model structure is fixed and parameters are recalibrated per city. However, the paper does not hold out an entire city as a test case — parameters are fitted city by city.
- Leakage or generalisation risks: The random 80/20 split does not guard against spatial autocorrelation. Road segments that are spatially adjacent to training observations will likely have similar centrality values, so the validation R² is likely optimistic for truly unseen spatial areas. This is not classic data leakage but is a meaningful spatial generalisation limitation. The paper does not discuss this.
- Evidence quote or page reference: "The study has initially utilized randomly selected 80% of the data for calibration and 20% to validation." (p. 1153)
- What I should copy or avoid: **Avoid** treating the validation R² as evidence of spatial generalisation. **Note for Open Road Risk:** Stage 1a already uses grouped validation by count point, which is substantially stronger than the random split used here. The sub-sampling sensitivity analysis (Table 5) is worth documenting as a reference for minimum count coverage requirements.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**  
- Finding: In these five developing-country urban case studies, a two-predictor linear regression using betweenness centrality (BC) and closeness centrality (CC), weighted by a road-type path-distance, achieves R² > 0.90 and MdAPE < 20% for AADT estimation at the road segment level.
- Why it matters: Provides a published benchmark for centrality-based AADT estimation accuracy. Open Road Risk already uses BC and degree centrality as features; this paper supports their relevance to AADT prediction and suggests CC may also warrant inclusion.
- Evidence quote or page reference: Table 3, p. 1154
- Confidence: Medium — results are from developing-country urban networks only, not UK mixed urban/rural networks. Spatial generalisation is not tested rigorously.

**Finding 2:**  
- Finding: Betweenness centrality alone explains approximately 60% of AADT variance in these case studies; adding closeness centrality increases explained variance and substantially reduces RMSE.
- Why it matters: Suggests that BC alone (as used in Open Road Risk Stage 1a) may leave material predictive variance uncaptured. CC as an additional Stage 1a feature is worth a diagnostic comparison.
- Evidence quote or page reference: Partial correlation² values, Table 3, p. 1154
- Confidence: Medium — urban developing-country context; not directly testable without UK-specific validation.

**Finding 3:**  
- Finding: The centrality-based model performs poorly for very low AADT links (AADT < 1,000): RMSE 193%–412% in two cities.
- Why it matters: Open Road Risk includes many low-traffic rural links. Centrality features alone may have limited predictive power for this segment of the network. Stage 1a's additional features (road classification, spatial context, etc.) may be necessary to compensate.
- Evidence quote or page reference: Table 4, p. 1155
- Confidence: High within this study's context — the pattern is consistent across multiple cities.

**Finding 4:**  
- Finding: Acceptable AADT estimation accuracy (RMSE < 30%) is achievable with as few as ~40 observed count points for calibration, according to the repeated sub-sampling analysis.
- Why it matters: Provides a reference for how sensitive a centrality-based AADT model is to sparse count coverage. Open Road Risk Stage 1a uses AADF count points (likely thousands, not tens) — a much denser calibration base, which should support better accuracy.
- Evidence quote or page reference: Table 5 and Fig. 6, p. 1155
- Confidence: Medium — the sub-sampling is done by random selection within a single city, not by spatial withholding. Actual count sparsity in rural England is geographically structured, which this analysis does not address.

**Finding 5:**  
- Finding: The path-distance variable (metric distance weighted by road-type speed band) consistently outperforms topological distance alone. Coefficient values for BC and CC are similar across all five cities, suggesting some structural robustness.
- Why it matters: Supports the use of road-type-weighted centrality rather than unweighted topology. Open Road Risk's BC feature implementation should be checked against whether it uses metric, topological, or speed-weighted distance.
- Evidence quote or page reference: "One notable fact was that the coefficient values for BC and CC are much similar in all five case study areas." (p. 1154)
- Confidence: Low-to-medium — cross-city coefficient similarity in five developing-country cities does not prove transferability to UK road networks with different hierarchy structures.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Closeness Centrality (CC) as Stage 1a AADT feature | BC is already used; CC explained 32–35% additional variance independently in this study; worth testing whether CC adds signal in Stage 1a | OS Open Roads geometry (already available) | 679–2,397 segments per city | Compatible in principle; compute cost at 2.1M links needs benchmarking — sDNA or NetworkX; 20 km radius scope | Stage 1a — candidate feature | Medium (computational cost at scale unclear; sDNA or Python graph library required) | Betweenness and closeness may be correlated in UK network; collinearity and compute cost at 2.1M links are real concerns |
| Path-distance weighting for centrality (road-type speed bands as edge weights) | May improve BC/CC predictive quality vs unweighted metric distance | OS Open Roads road classification (already available) | Same as above | Compatible in principle | Stage 1a — candidate feature / compare against current BC implementation | Medium | Needs recalibration of Ty speed values for UK road hierarchy; original values are for developing-country networks |
| Sub-sampling sensitivity analysis (minimum count coverage test) | Useful diagnostic: how does Stage 1a CV R² degrade as AADF count density decreases? | Stage 1a AADF count data (already available) | N/A | Directly applicable | Stage 1a — diagnostic / validation | Low | Random sub-sampling does not test spatial generalisation; results would still be somewhat optimistic |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Two-predictor linear regression (BC + CC only) as production AADT estimator | Open Road Risk Stage 1a already uses gradient boosting with many features and achieves CV R² 0.83; a two-predictor OLS model is a step backward in terms of complexity and feature coverage | N/A — data is available; the issue is model adequacy | 679–2,397 segments per city | Not compatible as a production replacement | Use as a simple baseline to compare against Stage 1a | High |
| sDNA software for centrality computation | sDNA is GIS-based (Cardiff University tool); at 2.1M links, sDNA's scalability is not demonstrated. Python (NetworkX, graph-tool) is more tractable at this scale | sDNA software; computational capacity | Up to ~2,400 segments per city | Low at 2.1M links — sDNA not validated at this scale | Use Python graph-tool or similar for large-scale BC/CC computation | Medium |
| Cross-city parameter stability as evidence of UK transferability | The five cities are all developing-country, high-density urban networks. UK network includes motorways, rural A-roads, and minor rural links with different topology and traffic patterns | UK-specific validation data | Urban developing-country cities only | Not directly transferable without UK-specific recalibration | Recalibrate using UK AADF counts; treat as diagnostic comparison | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** No. The paper does not address collision risk at all. It is purely a traffic volume estimation method.
- **Does it suggest better handling of AADT/AADF uncertainty?** Indirectly. The sub-sampling analysis (Table 5) provides a reference for how accuracy degrades with fewer count observations, which is relevant to understanding Stage 1a sensitivity to AADF count sparsity in rural areas.
- **Does it suggest useful geometry or road-context features?** Yes — closeness centrality (not currently stated as a Stage 1a feature) may add independent predictive signal for AADT. Path-distance weighting of centrality by road type is a potentially useful refinement worth testing.
- **Does it suggest better modelling of junctions?** No — the paper explicitly uses a road-segment (dual-graph) representation and treats junctions as edges, not as primary analysis units.
- **Does it suggest better treatment of severity?** Not applicable.
- **Does it suggest better validation design?** It provides a negative example: the random 80/20 split is weaker than Open Road Risk's grouped-by-count-point validation. No new validation design is suggested.
- **Does it expose a weakness in my current approach?** Possibly: the current Stage 1a betweenness centrality feature may be computed using unweighted metric distance rather than road-type speed-weighted path-distance. The paper provides a concrete operationalisation of path-distance weighting that could be tested diagnostically against the current BC implementation.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Document the path-distance weighting approach (PD = MD × Ty) as a potential variant for computing betweenness centrality in Stage 1a; compare feature importance and AADT CV R² against the current BC implementation.
- Action type: documentation note / diagnostic
- Relevant stage: Stage 1a
- Why the paper supports it: The paper shows that speed-band-weighted path-distance consistently outperforms unweighted topological distance for AADT prediction across five case studies. If Open Road Risk BC is computed with unweighted distance, this is a testable improvement.
- Evidence quote or page reference: p. 1152: "this study proposes 'path distance' (i.e. PD), which is a function of the average speed by road type (Ty) and the angular change-adjusted metric distance (MD)"
- Effort: Medium
- Risk if implemented badly: Ty speed-band values are calibrated to developing-country road types; UK mapping would require review. Mismatch between OS road classification and paper's road hierarchy could introduce noise.

**Action 2**
- Suggested repo action: Test closeness centrality (CC) as an additional candidate feature in Stage 1a; run feature importance comparison against existing BC and degree centrality.
- Action type: candidate feature / diagnostic
- Relevant stage: Stage 1a
- Why the paper supports it: In this study, CC explained 32–35% of AADT variance independently of BC (partial R²). The two features are non-collinear in most case cities (VIF < 2). CC captures O-D trip generation, which BC does not.
- Evidence quote or page reference: Table 3, p. 1154 — partial correlation values and VIF
- Effort: Medium (compute cost at 2.1M links needs assessment before implementation)
- Risk if implemented badly: CC computation at 2.1M links may be prohibitively slow without appropriate graph tools. UK network topology may produce higher BC-CC collinearity than in the case study cities.

**Action 3**
- Suggested repo action: Add a documentation note on low-AADT accuracy degradation for centrality-based features; flag that Stage 1a accuracy on links with AADT < 1,000 may be lower than overall CV R² suggests, and consider stratified reporting of Stage 1a error by AADT category.
- Action type: documentation note / diagnostic
- Relevant stage: Stage 1a / validation
- Why the paper supports it: Table 4 shows RMSE > 100% for AADT < 1,000 in two of five cities for a centrality-only model. Open Road Risk Stage 1a uses more features, but the low-traffic performance gap is likely to persist in some form.
- Evidence quote or page reference: Table 4, p. 1155
- Effort: Low
- Risk if implemented badly: Low — this is diagnostic documentation.

**Action 4**
- Suggested repo action: Run a sub-sampling sensitivity analysis on Stage 1a: progressively reduce the number of AADF count points used for training and report CV R² degradation curve. Use as a diagnostic to quantify how sensitive Stage 1a is to count sparsity.
- Action type: diagnostic
- Relevant stage: Stage 1a
- Why the paper supports it: The paper's Fig. 6 / Table 5 methodology (repeated random sub-sampling at increasing N) is a straightforward diagnostic transferable to Stage 1a with minimal implementation effort. Results would document Stage 1a robustness to count coverage variation.
- Evidence quote or page reference: "the study performed a 'repeated random sub-sampling validation' to identify the minimum number of observations that required in calibrating the model." (p. 1155)
- Effort: Low
- Risk if implemented badly: Random sub-sampling does not test spatial generalisation; results will be somewhat optimistic. Should be noted in documentation.

**Action 5**
- Suggested repo action: Add this paper to the Stage 1a literature dossier as a reference for centrality-based AADT estimation benchmarks (R² > 0.90, MdAPE < 20% at 40+ count points). Note the developing-country urban context limitation and the weak random-split validation when citing accuracy figures.
- Action type: documentation note
- Relevant stage: Stage 1a / documentation
- Why the paper supports it: Provides a peer-reviewed published benchmark using only network geometry and a small number of count observations.
- Evidence quote or page reference: Conclusion section, p. 1159
- Effort: Low
- Risk if implemented badly: Low.

---

## 16. Query Tags

- betweenness-centrality
- closeness-centrality
- AADT-estimation
- network-centrality
- path-distance-weighting
- road-segment-level
- dual-graph
- space-syntax
- sDNA
- sparse-count-calibration
- sub-sampling-sensitivity
- urban-network
- developing-country
- low-AADT-accuracy
- random-split-validation
- no-collision-data
- Stage1a-feature-candidate
- traffic-volume-model
- road-type-classification

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: The exact regression type selected as final model (OLS vs RR vs PR) is not definitively stated; OLS is implied by R² reporting but not confirmed. The spatial extent of the search radius (20 km) is stated but its sensitivity is not tested. No information on whether CC uses directed or undirected graph computation.
- Parts of the paper that need manual checking: Table 4 RMSE figures for very low AADT categories — the numbers are striking (193%, 412%) and worth verifying against the original. The VIF value for Hanoi (4.253) is notably higher than other cities and warrants attention if replicating.
- Any likely ambiguity or risk of misinterpretation: The paper reports "R² > 0.90 for calibration and validation" — this is a randomly split 80/20 holdout, not spatial holdout. Do not treat these R² values as evidence of spatial generalisation. The paper's Ty speed-band values (Table 1) are explicitly for developing-country road types and would need recalibration for UK application. The paper is a traffic volume modelling paper, not a road safety paper — it has no collision data, no exposure offset structure, and no Stage 2 relevance beyond providing a potential AADT feature engineering approach.