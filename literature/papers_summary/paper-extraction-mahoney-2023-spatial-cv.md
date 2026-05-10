# Paper Extraction: Mahoney et al. 2023 — Spatial Cross-Validation

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: ASSESSING_THE_PERFORMANCE_OF_SPATIAL_CROSS-VALIDATION.pdf
- Suggested Markdown filename: paper-extraction-mahoney-2023-spatial-cv.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: claude-sonnet-4-6
- Interface used: web chat (claude.ai)
- Input type: PDF upload (text extracted from document blocks in context)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 18-page paper including all figures and tables accessible. This paper is not a road safety paper — it is a methodology paper about spatial cross-validation. It is being extracted for its direct implications for Open Road Risk's validation design, not for road safety modelling content.

---

## 1. Citation

- Title: Assessing the Performance of Spatial Cross-Validation Approaches for Models of Spatially Structured Data
- Authors: Michael J Mahoney, Lucas K Johnson, Julia Silge, Hannah Frick, Max Kuhn, Colin M Beier
- Year: 2023 (arXiv preprint, 13 Mar 2023)
- DOI or URL: arXiv:2303.07334v1
- Country / region studied: Simulation study — no specific geography. Simulated 50×50 grid landscapes.
- Study setting: Not applicable (simulation)

---

## 2. Core Objective

- One-sentence description: The paper evaluates five cross-validation methods (resubstitution, V-fold, spatial blocking, spatial clustering, BLO3, LODO) on simulated spatially structured data to determine which produces the most accurate estimates of true out-of-sample model error.
- Main purpose: methodological evaluation / validation design guidance
- Evidence quote: "we evaluated the leading spatial CV approaches found in the literature, using random forest models fit on spatially structured data following the simulation approach of Roberts et al. (2017)" (Section 1, p. 3)

---

## 3. Response Variable

- Target variable: Simulated continuous outcome variable y (Equation 1, p. 5), a nonlinear function of spatially structured predictor fields
- Collision type: Not applicable
- Severity handling: Not applicable
- Count, binary, rate, risk score, severity class, or other: continuous (Gaussian)
- Time window used for outcomes: Not applicable (cross-sectional simulation)
- Evidence quote: "y = min(y) if X4 ≠ 0; X11 if y ≥ X11; X1 + X5 + X6 + X12 + X13, otherwise" (Equation 1, p. 5)

**Note for Open Road Risk:** The simulation uses a continuous outcome. Open Road Risk's collision outcome is a zero-heavy integer count. The paper's findings on spatial CV performance are expected to generalise to count outcomes, but this has not been directly tested in this paper. The qualitative finding — that spatial CV methods reduce optimistic bias from spatial autocorrelation — is broadly consistent with road safety literature and is likely to hold for count outcomes.

---

## 4. Exposure Handling

- Exposure variable used, if any: Not applicable — simulation study
- Traffic count source: Not applicable
- Whether exposure is modelled, observed, assumed, or ignored: Not applicable
- Treatment of missing or sparse traffic counts: Not applicable
- Whether offset terms, rates, denominators, or normalisation are used: Not applicable
- Transferability to my AADF/WebTRIS setup: Not applicable — this paper is about CV methodology, not exposure modelling
- Notes: Not applicable

---

## 5. Spatial Unit of Analysis

- Unit: Grid cell (50×50 regular grid = 2,500 observations per simulated landscape)
- Segment length or segmentation rule: Regular grid cells; each cell is one observation
- How crashes are assigned to the network: Not applicable
- Treatment of junctions/intersections: Not applicable
- Spatial aggregation risks: The simulation assumes regular, uniform sampling density across the grid. The paper explicitly acknowledges this as a limitation: uneven sampling density (as occurs in real road networks) is not investigated and may require different CV approaches.
- Evidence quote: "This simulation study assumed that spatial CV could take advantage of regularly distributed observations, such that all locations had a similar density of measurement points. This assumption is often violated" (Section 5.2, p. 12)
- Relevance to OS Open Roads link-based pipeline: The regular grid assumption does not match OS Open Roads geometry. Road network links are not uniformly distributed: motorways, A-roads, and urban roads are denser than rural minor roads. This is an important caveat when applying the paper's specific buffer/radius recommendations to Open Road Risk. The qualitative ranking of methods (spatial CV > random CV) is likely to transfer; the specific optimal buffer sizes (25–41% of grid length) may not directly translate to a road network context.

---

## 6. Temporal Unit of Analysis

- Years covered: Not applicable — simulation study
- Temporal resolution: Not applicable
- Whether seasonality or time-of-day is modelled: Not applicable
- Whether before-after or panel structure is used: Not applicable
- Relevance to WebTRIS-style time profiles: Not applicable

---

## 7. Engineered Features

Not applicable — simulation study. Simulated predictor fields (X2, X3, X6–X10) are used; these have no direct analogue in Open Road Risk.

---

## 8. Model Architecture

- Algorithms/models used: Random forests (ranger R package); 500 trees, 5 minimum observations per leaf, 2 variables per split — all default settings
- Baseline model: Resubstitution (train-on-full, predict-on-same)
- Final/preferred model: Not a predictive model paper; evaluates CV methods, not models
- Loss function or likelihood: RMSE (Equation 2, p. 8)
- Offset/exposure term, if used: None — not applicable
- Spatial autocorrelation handling: The paper evaluates how CV methods handle spatial autocorrelation; the random forest model itself has no explicit spatial autocorrelation handling
- Temporal dependence handling: Not applicable
- Interpretability method: Not applicable
- Evidence quote: "random forests were fit using the default hyperparameter settings of the ranger package, namely 500 decision trees, a minimum of 5 observations per leaf node, and two variables to split on per node" (Section 4.3, p. 5–6)

---

## 9. Reported Metrics / Quantitative Results

### Main results (Table 4, p. 9 — mean RMSE across all parameterisations)

| Result type | Metric | Value | SD | % within target RMSE range | Method | Evidence |
|---|---|---|---|---|---|---|
| True RMSE (target) | RMSE | 0.715 | 0.042 | 90.00% | Ideal (cross-landscape) | Table 4 |
| Spatial CV | RMSE | 0.743 | 0.161 | 36.97% | Clustered | Table 4 |
| Spatial CV | RMSE | 0.641 | 0.135 | 31.70% | LODO | Table 4 |
| Spatial CV | RMSE | 0.664 | 0.159 | 27.90% | Blocked | Table 4 |
| Non-spatial CV | RMSE | 0.440 | 0.076 | 2.00% | V-fold | Table 4 |
| Non-spatial CV | RMSE | 0.429 | 0.098 | 1.29% | BLO3 (no buffer) | Table 4 |
| Resubstitution | RMSE | 0.189 | 0.032 | 0.00% | Resubstitution | Table 4 |

### Best-parameterised results (Table 5, p. 10)

| Method | Best parameterisation | RMSE | % within target |
|---|---|---|---|
| Clustered | V=10, k-means, buffer=0.15 | 0.694 (0.087) | 60.00% |
| LODO | buffer=0.18, radius=0.21 | 0.718 (0.095) | 60.00% |
| Blocked | cell=1/9, buffer=0.24 | 0.738 (0.099) | 61.00% |
| V-fold | V=10 | 0.428 (0.071) | 2.00% |
| BLO3 | buffer=0.48 | 0.524 (0.070) | 7.00% |

### Assessment of metrics

- **Are these metrics in-sample, out-of-sample, cross-validated, or externally validated?** The "true" RMSE is estimated by training on one simulated landscape and predicting 99 independent landscapes — a genuine out-of-sample generalisation estimate. The CV estimates are compared against this true RMSE. This is a rigorous evaluation design.
- **Do these metrics test predictive generalisation or model fit?** Predictive generalisation — the explicit goal is to estimate how well a model fitted on one dataset will predict new, independent data from the same data-generating process.
- **Are any metrics likely to be optimistic for real-world deployment?** V-fold and resubstitution are shown to be strongly optimistic. The spatial CV methods (clustered, LODO, blocked) produce closer-to-true estimates when well-parameterised, but even the best methods only achieved ~60% of iterations within the target range.
- **Which metric is most relevant to Open Road Risk?** The "% within target RMSE range" result is directly relevant to the question: which CV method gives the most trustworthy estimate of true model performance? The answer from this paper is: spatial clustering or LODO with an exclusion buffer, tuned so that the minimum distance between Din and Dout exceeds the autocorrelation range of the outcome variable.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Not investigated. The paper uses a continuous Gaussian-like outcome. Zero-heavy or count outcomes are not considered.
- Relevant note: The paper explicitly flags this as a limitation — "we did not investigate any CV approaches which aim to preserve outcome or predictor distributions across Dout. When working with imbalanced outcomes, random sampling may produce Dout with notably different outcome distributions than the overall training data, which may bias performance estimates" (Section 5.2, p. 12–13). This is directly relevant to Open Road Risk's sparse collision data.
- Practical relevance: High concern. Open Road Risk link-years are ~98–99% zero collisions. A spatial CV fold drawn from a low-collision-density area may have zero positive examples in Dout, making RMSE/R² meaningless for evaluating risk discrimination. This interaction between spatial CV fold design and class imbalance is not resolved by this paper.

---

## 11. Validation Strategy

- The paper IS the validation strategy paper. It evaluates CV methods rather than using CV as a tool.
- Key design choice for evaluating CV methods: 100 independent landscape simulations. Each CV method applied to each landscape. True RMSE estimated by cross-landscape prediction (train on one landscape, predict 99 others). This is a rigorous external reference point.
- Key finding on buffer sizing: The optimal spatial separation between Din and Dout is approximately equal to the autocorrelation range of the outcome variable. The paper finds a mean autocorrelation range of 24.61% of grid length for the outcome variable (Figure 4, p. 12). Best CV results came from separations of 25–41% of grid length.
- Evidence quote: "spatial cross-validation approaches produce the best estimates of model performance when Dout is sufficiently separated from Din such that there is no spatial dependency in the outcome variable between the two sets" (Section 5.1, p. 9)

---

## 12. Key Findings Relevant to My Project

**Finding 1:** Random V-fold CV severely underestimates true prediction error for models fit to spatially autocorrelated data. V-fold produced RMSE estimates within the target range only 2% of the time, versus 37–37% for the best spatial CV methods.

- Why it matters: Open Road Risk's XGBoost model uses a grouped-by-road-link split (not spatial CV). This is better than pure random V-fold, but grouping by road link prevents the same link appearing in both train and test across years — it does not enforce spatial separation between links. Nearby links from the same road corridor will still share train/test sets, which may produce over-optimistic performance estimates for the XGBoost model specifically.
- Evidence: Table 4, p. 9 — V-fold 2.00% vs Clustered 36.97%
- Confidence: high — result is from a controlled simulation with a rigorous external reference point

**Finding 2:** Spatial CV methods combining spatially conjunct assessment sets with exclusion buffers produce the most accurate estimates of true model performance. Clustered CV (k-means, ~10 clusters, buffer ~15% of grid length) and LODO (buffer + inclusion radius together ~36–39% of grid length) consistently achieved ~60% of iterations within the target range when well-parameterised.

- Why it matters: This suggests a design for a more rigorous Stage 2 validation diagnostic in Open Road Risk. Grouping road links into spatial clusters (e.g. by LSOA, LAD, or k-means on coordinates) and using those clusters as folds, with a spatial exclusion buffer around each fold, would be more informative than the current link-level grouped split.
- Evidence: Table 5, p. 10; Section 5.1, p. 9
- Confidence: high for the general principle; medium for specific buffer sizes (not tested on road network data)

**Finding 3:** The optimal exclusion buffer distance is approximately equal to the spatial autocorrelation range of the outcome variable. For the simulated data, mean autocorrelation range was 24.61% of grid length; best results used separations of 25–41%.

- Why it matters: Open Road Risk could estimate the spatial autocorrelation range of its Stage 2 Poisson GLM residuals using an empirical variogram, then use that range to parameterise an exclusion buffer for a spatial CV diagnostic. This is a concrete, implementable next step.
- Evidence: Figure 4, p. 12; Section 5.1, p. 9
- Confidence: high within the simulation; moderate when generalising to road network data with irregular geometry

**Finding 4:** BLO3 CV (buffered leave-one-observation-out) performs poorly despite having the largest exclusion buffers tested. Even with buffers of 0.48 grid lengths, only 7% of iterations were within the target range (Table 5). This is counter-intuitive and the paper does not fully explain why.

- Why it matters: At Open Road Risk's scale (2.17M links), leave-one-observation-out CV is computationally infeasible regardless. But this finding also warns against assuming that larger buffers always improve estimates — the interaction between buffer size, assessment set size, and available training data matters.
- Evidence: Table 4 and Table 5, p. 9–10; Section 5.1, p. 9
- Confidence: high for the empirical result; low for understanding the mechanism

**Finding 5:** Removing too much data from Din (e.g. very large blocks or only 2 clusters) produces pessimistic over-estimates of RMSE. There is a trade-off between spatial separation (reducing optimistic bias) and training set size (reducing pessimistic bias from underfitting).

- Why it matters: At national scale (2.17M links), spatial holdout by region (e.g. holding out an entire police force area) risks losing so much training data that models underfit. The paper suggests that 9–25 spatial blocks or 5–10 clusters, rather than 2, is a better starting point. For Open Road Risk, regional holdout by police force code (of which there are ~13–16 in the study area) may be reasonable.
- Evidence: Figure 3A and 3B (p. 11); Section 5.1, p. 9
- Confidence: high for the general principle

**Finding 6:** Spatial clustering (k-means on coordinates) is the most robust spatial CV method to varying parameterisations. It achieved the highest overall proportion of iterations within the target range (36.97%) across all parameter combinations tested, not just at the optimal setting.

- Why it matters: For a practical implementation in Open Road Risk — where the correct buffer size is unknown — k-means spatial clustering is the most forgiving choice if parameterisation is uncertain. It is also computationally more tractable than LODO at 2.17M links.
- Evidence: "Clustering appeared to be the spatial CV method most robust to different parameterizations" (Section 5.1, p. 9); Table 4, p. 9
- Confidence: medium — this may partly reflect the narrower parameter range tested for clustering vs other methods

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Spatial clustering CV (k-means on coordinates, ~10 folds, buffer ~15% of study area diameter) | More accurate estimate of true model generalisation than current link-level grouped split; reduces optimistic bias from spatial autocorrelation | Road link coordinates (already available) | 2,500 obs / 50×50 grid | Medium — method scales, but optimal buffer size unknown for 2.17M-link network; treat as diagnostic, not as a replacement for current grouped split | Stage 2 / validation | Medium — requires estimating spatial autocorrelation range and implementing k-means fold assignment | Buffer size calibration; at national scale, police force boundaries may be more practical than continuous k-means |
| Empirical variogram of Stage 2 model residuals to estimate autocorrelation range | Provides principled basis for choosing exclusion buffer size in spatial CV | Stage 2 Poisson GLM residuals + link coordinates (already available) | N/A | High — variogram is computationally feasible on a sample of links | Validation / diagnostic | Low-medium (scipy or statsmodels spatial tools; or sample-based variogram) | Variogram estimation on 2.17M points requires subsampling; may need to subsample by road class to get stable estimates |
| Regional holdout by police force code as a practical spatial CV approximation | Police force boundaries (codes 12/13/14/16 + 4–7) are meaningful geographic groups with real administrative boundaries; holding out one force at a time tests geographic generalisation | Already coded in pipeline | ~13–16 regions | High — directly applicable | Stage 2 / validation | Low — already partially implemented for force-specific analysis | With ~13–16 forces, individual holdout folds will have unequal sizes; some forces have far fewer collisions than others |
| Documenting current grouped-by-road-link split as "temporal grouped CV, not spatial CV" | Current split prevents leakage across years for the same link but does not enforce spatial separation between neighbouring links; this distinction should be documented | N/A | N/A | High | Documentation | Low | None |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| LODO CV (leave-one-disc-out, iterating over every observation) | Computationally infeasible at 2.17M links — requires fitting a model for every link, not just every fold | N/A | 2,500 obs | Low — 2.17M iterations of model fitting is not practical | Approximate with spatial clustering or regional holdout | High |
| BLO3 CV (buffered leave-one-observation-out) | Same computational objection as LODO; additionally shown to perform poorly even in the paper's simulation | N/A | 2,500 obs | Low | Not recommended even at smaller scale based on paper's own results | High |
| Exact buffer sizing (25–41% of grid length) | Simulation used a regular 50×50 grid with known autocorrelation structure. Road networks are irregular, with autocorrelation range varying by road class, area type, and outcome density. The specific percentages do not translate directly. | Empirical variogram of Open Road Risk residuals | 2,500 obs grid | Low for direct transfer; high for the underlying principle (buffer ≈ autocorrelation range) | Estimate autocorrelation range from Stage 2 residuals and use that as buffer guidance | Medium |
| Stratified spatial CV preserving collision outcome distribution | Paper flags this as uninvestigated and difficult to implement for spatial group assignments. For Open Road Risk's zero-heavy link-years, naive spatial folds may have zero positive examples. | N/A | N/A | Low — not implemented in the paper or in standard tools | Manual stratification of folds to ensure minimum collision count per fold; complex to implement correctly | High (confidence in the problem existing) |

---

## 14. Pipeline Implications

**Does this paper support using exposure-normalised collision risk?**
Not directly — not a road safety paper. No exposure variable.

**Does it suggest better handling of AADT/AADF uncertainty?**
No.

**Does it suggest useful geometry or road-context features?**
No.

**Does it suggest better modelling of junctions?**
No.

**Does it suggest better treatment of severity?**
No.

**Does it suggest better validation design?**
Yes — this is the paper's sole contribution relative to Open Road Risk. It provides empirical evidence that:
1. Random V-fold CV produces severely optimistic performance estimates for spatially autocorrelated data.
2. Spatial clustering CV with exclusion buffers is the most robust and practical improvement.
3. The exclusion buffer should be sized to match or exceed the autocorrelation range of the outcome variable or model residuals.
4. The current grouped-by-road-link split in Open Road Risk prevents year-level leakage but does not address spatial autocorrelation between neighbouring links — this is a gap.

**Does it expose a weakness in my current approach?**
Yes, one specific weakness: the grouped-by-road-link temporal split controls for repeated-measures leakage (same link in train and test across years) but does not enforce spatial separation between nearby links. Two adjacent links from the same road — one in the training set, one in the test set — will share spatial autocorrelation in both the outcome variable and the engineered features. This means the current XGBoost R² and Poisson pseudo-R² may be optimistically biased to an unknown degree.

The magnitude of this bias depends on the spatial autocorrelation range of collision risk in Open Road Risk's network. This has not been measured. Estimating it via variogram of Stage 2 residuals is a concrete, low-effort diagnostic action.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Compute an empirical variogram of Stage 2 Poisson GLM residuals on a spatial sample of links to estimate the autocorrelation range of collision risk
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper's key practical recommendation is to size spatial CV exclusion buffers to match the autocorrelation range of the outcome or residuals. Without knowing this range for Open Road Risk, it is not possible to design a meaningful spatial CV evaluation or assess whether the current grouped split is spatially adequate.
- Evidence: Figure 4, p. 12; Section 5.1, p. 9
- Effort: low-medium — requires sampling Stage 2 residuals spatially and fitting a variogram (e.g. via scipy.spatial or a lightweight geostatistics library); subsample to ~10,000–50,000 links to keep computation tractable
- Risk if implemented badly: Variogram estimation is sensitive to the spatial sample design and to outliers. Use road-class-stratified subsampling to avoid motorway/rural bias.

**Action 2**
- Suggested repo action: Document the current grouped-by-road-link CV split explicitly as "temporal grouped CV" and note that it does not enforce spatial separation between neighbouring links; record this as a known limitation of the Stage 2 validation
- Action type: documentation note
- Relevant stage: Stage 2 / validation / documentation
- Why the paper supports it: The paper demonstrates that grouped splits which do not enforce spatial separation between Din and Dout remain subject to optimistic bias from spatial autocorrelation. The current split was designed to prevent same-link leakage across years, not to address spatial autocorrelation.
- Evidence: Section 5.1, p. 9; Table 4, p. 9
- Effort: low
- Risk if implemented badly: None (documentation only)

**Action 3**
- Suggested repo action: Pilot a police-force-level regional holdout as a spatial CV diagnostic — hold out each force area in turn as Dout, train on all others, evaluate Stage 2 XGBoost performance
- Action type: diagnostic / small pilot
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Police force boundaries are meaningful, pre-defined geographic groups of roughly comparable size. Holding out one force area at a time provides a practical approximation of spatial CV that enforces real geographic separation. The paper finds that ~5–10 folds (similar to the 13–16 force areas in Open Road Risk) is in the reasonable range for spatial clustering CV.
- Evidence: Table 5, p. 10 — V=10 clusters achieves 60% within target range; force holdout provides comparable spatial separation
- Effort: medium — requires ensuring the existing pipeline can be run with a force-area mask; may require some restructuring of the grouped split logic
- Risk if implemented badly: Force areas vary substantially in size and collision density (Yorkshire vs rural Midlands forces). Compare force-holdout RMSE/R² against current grouped-split metrics to quantify how much the spatial grouping changes the apparent performance.

**Action 4**
- Suggested repo action: Add a note to the Stage 1a validation section documenting that AADF count point locations are spatially clustered (concentrated on major roads and urban areas), and that spatial autocorrelation in the AADT predictor surface may propagate into Stage 2 feature estimates
- Action type: documentation note
- Relevant stage: Stage 1a / Stage 2 / documentation
- Why the paper supports it: The paper notes that uneven sampling density (concentrated observations, sparse elsewhere) is a limitation of regular-grid simulation results, and that spatial CV methods may behave differently under clustered sampling. AADF count points are highly spatially clustered in the actual road network, which may affect the spatial autocorrelation structure of AADT estimates in Stage 1a.
- Evidence: Section 5.2, p. 12 — "observations are often clustered in more convenient locations and relatively sparse in less accessible areas"
- Effort: low (documentation only)
- Risk if implemented badly: None

**Action 5**
- Suggested repo action: Flag in the Stage 2 validation documentation that zero-heavy collision outcomes are not covered by this paper's simulation findings, and that spatial CV fold design should ensure each fold contains a minimum number of positive collision link-years
- Action type: documentation note / validation design guardrail
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The paper explicitly notes it did not investigate imbalanced outcome distributions and that spatial folds may produce Dout with notably different outcome distributions. For a 98–99% zero outcome, spatial folds drawn from low-collision rural areas may have too few positive examples to meaningfully evaluate discriminative performance.
- Evidence: Section 5.2, p. 12–13
- Effort: low (documentation); medium if enforced programmatically (check minimum collision count per fold before running CV)
- Risk if implemented badly: Folds with zero positive examples will produce undefined or meaningless MAE/RMSE on the non-zero tail; this could silently inflate apparent performance if not detected.

---

## 16. Query Tags

- spatial-cross-validation
- spatial-autocorrelation
- validation-design
- grouped-CV
- spatial-blocking
- spatial-clustering
- LODO-CV
- BLO3-CV
- exclusion-buffer
- autocorrelation-range
- variogram
- optimistic-bias
- random-forest
- simulation-study
- V-fold-CV
- regional-holdout
- imbalanced-outcome-note
- UK-road-network-applicability

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper:
  - The paper does not test count or zero-heavy outcomes. All results apply to a continuous Gaussian-like outcome. Generalisation to Poisson or zero-inflated count outcomes is plausible but not demonstrated.
  - The paper does not test irregular or clustered sampling designs. Open Road Risk's link network is not a regular grid; links are denser in urban areas and on major roads. The specific buffer size recommendations may not transfer.
  - The paper does not provide guidance on how to handle cases where spatial folds are empty or near-empty for rare outcomes — a practical problem for Open Road Risk.
- Parts of the paper that need manual checking:
  - Table 4 and Table 5 values were read from text; verify against the original PDF tables if citing specific numbers.
  - The specific optimal buffer sizes (25–41% of grid length) should not be applied directly to Open Road Risk without first estimating the autocorrelation range of Open Road Risk residuals. They are simulation-specific values.
- Any likely ambiguity or risk of misinterpretation:
  - "BLO3 CV" (buffered leave-one-observation-out) performing poorly despite large buffers is counter-intuitive. The paper notes this without fully explaining it. Do not assume that a large exclusion buffer alone is sufficient — the spatial conjunctness of the assessment set (having multiple nearby observations in Dout together) also matters.
  - The paper's "true" RMSE is estimated by cross-landscape prediction under identical data-generating processes. In Open Road Risk, there is no equivalent "true" out-of-sample RMSE known in advance. The paper's target RMSE range is used as an evaluation benchmark, not as something that can be directly computed for a real dataset.
  - The paper focuses on predictive model evaluation, not map accuracy assessment. The authors explicitly distinguish between these two tasks and note that Wadoux et al. (2021) found spatial CV to be overly pessimistic for map accuracy. Open Road Risk's task is predictive model evaluation (does the model identify high-risk links?), not map accuracy assessment, so spatial CV is appropriate.
