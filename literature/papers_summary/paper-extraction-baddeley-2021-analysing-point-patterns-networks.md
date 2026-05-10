RAW_MARKDOWN_START
Save this as: paper-extraction-baddeley-2021-analysing-point-patterns-networks.md

# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: 91405.pdf
- Suggested Markdown filename: paper-extraction-baddeley-2021-analysing-point-patterns-networks.md
- AI tool used: Gemini
- Model name, if visible: Gemini
- Model version, if visible: not stated
- Interface used: API
- Input type: text pasted
- Output mode: raw Markdown copy block
- Was the full paper accessible to the model? yes
- Notes on access limitations: None

## 1. Citation

- Title: Analysing point patterns on networks - a review
- Authors: Adrian Baddeley, Gopalan Nair, Suman Rakshit, Greg McSwiggan, Tilman M. Davies
- Year: 2021
- DOI or URL, if present: 10.1016/j.spasta.2020.100435
- Country / region studied: Various (Examples from Western Australia, Chicago, USA)
- Study setting: mixed / theoretical review

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper reviews statistical methods for analysing exact spatial locations of events (point patterns) occurring continuously along a network of lines, highlighting the mathematical failures of applying traditional 2D spatial statistics to network geometries.
- Main purpose: descriptive analysis / simulation / model comparison / methodological review
- Evidence quote or page reference: "We review recent research on statistical methods for analysing spatial patterns of points on a network of lines, such as road accident locations along a road network. Due to geometrical complexities, the analysis of such data is extremely challenging, and we describe several common methodological errors." (Page 1)

## 3. Response Variable

- Target variable: Spatial point intensity (e.g., expected number of points per unit length of network).
- Collision type: all crashes (in applied examples).
- Severity handling: Conceptually notes that precise locations are often only available for high-severity crashes, introducing bias if low-severity crashes are ignored or only available as aggregate counts.
- Count, binary, rate, risk score, severity class, or other: Continuous spatial point intensity ($\lambda(u)$).
- Time window used for outcomes: Varies by dataset (e.g., 2011 for Perth data).
- Evidence quote or page reference: "The point process X has intensity function $\lambda(u)$, $u \in L$, if $E[N(X \cap B)] = \int_B \lambda(u)du$... we may interpret $\lambda(u)$ as yielding the expected number of points per unit length of network in the vicinity of location u." (Page 15)

## 4. Exposure Handling

- Exposure variable used, if any: Traffic volume (in Geelong dataset example).
- Traffic count source: VicRoads automated counting devices.
- Whether exposure is modelled, observed, assumed, or ignored: observed.
- Treatment of missing or sparse traffic counts: not stated.
- Whether offset terms, rates, denominators, or normalisation are used: Treated as a continuous spatial covariate for nonparametric curve estimation, rather than a fixed log-linear offset.
- Evidence quote or page reference: "The traffic volume is an example of an explanatory variable (spatial covariate) that should be included in any realistic analysis of accident risk... Suppose that Z is a spatial covariate function, and we believe that the intensity of the points depends only on Z through a relationship $\lambda(u) = \rho(Z(u))$" (Pages 7, 26)
- Transferability to my AADF/WebTRIS setup: low
- Notes: The paper models traffic as a continuous field modulating a spatial point process. This mathematical structure is fundamentally different from a link-level negative binomial/Poisson count model using an exposure offset denominator.

## 5. Spatial Unit of Analysis

- Unit: Exact spatial point coordinate on a continuous linear network.
- Segment length or segmentation rule: None. The methodology explicitly avoids segmenting the network into discrete units.
- How crashes are assigned to the network: Treated as true spatial coordinates projected onto the 1D graph of the road network.
- Treatment of junctions/intersections: Identified as mathematically distinct from the rest of the network (vertices vs edges). Some point process models forbid points exactly at vertices, requiring special adaptations or separate intersection-count models.
- Spatial aggregation risks: The paper explicitly warns that aggregating exact coordinates to segment-level counts (like OS Open Roads links) introduces "ecological fallacy" (MAUP) and destroys spatial clustering information.
- Evidence quote or page reference: "A pragmatic strategy is to aggregate the data by counting the number of accidents that occurred along each segment of road... Potential weaknesses of this crash frequency approach include substantial bias due to aggregation (the 'ecological fallacy' or 'modifiable unit area problem') and the loss of spatial information needed to assess evidence for clustering." (Page 10)
- Relevance to OS Open Roads link-based pipeline: High conceptually (serves as a strong methodological critique of Stage 2's fundamental link-year architecture), but practically low (migrating from a discrete XGBoost link model to a continuous `spatstat` point process is computationally and structurally unrealistic for the current Open Road Risk scale).

## 6. Temporal Unit of Analysis

- Years covered: Single years in examples.
- Temporal resolution: Mentions spatio-temporal dynamics (time of day, calendar date) as fertile future research.
- Whether seasonality or time-of-day is modelled: Identified as important surrogates for traffic/weather, but not formally modelled in the review's core equations.
- Whether before-after or panel structure is used: no.
- Evidence quote or page reference: "The time of day at which a road accident occurred is an important covariate; it determines the speed limit and road rules applicable at the time, and is a surrogate for unobserved variables such as traffic conditions..." (Page 14)
- Relevance to WebTRIS-style time profiles: Validates the use of time-of-day profiles as predictors.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Traffic Volume | VicRoads / Sensors | Interpolated as a continuous spatial covariate | Primary driver of exposure / point intensity. | Already present (Stage 1a). |
| Distance to nearest intersection | Map / Network geometry | Shortest-path distance computation | Captures conflict zones directly without aggregating to a segment. | Yes (Candidate feature for Stage 2). |

## 8. Model Architecture

- Algorithms/models used: Spatial Point Processes (Poisson Point Process, Cox Processes), Kernel Density Estimation (Heat Kernel/Diffusion, Equal-Split).
- Baseline model: Naive 2D planar Kernel Density Estimation.
- Final/preferred model: Heat Kernel (diffusion) density estimator on the network.
- Loss function or likelihood, if stated: Point process log-likelihood (Berman-Turner device).
- Offset/exposure term, if used: None explicitly fixed; treated as a $\rho(Z)$ covariate.
- Spatial autocorrelation handling: Evaluated via network K-functions and pair correlation functions. The paper proves that true "stationary" correlation is mathematically impossible on networks with loops, requiring fundamentally non-stationary models.
- Temporal dependence handling: Ignored in the specific model equations shown.
- Interpretability method: Non-parametric curves of intensity vs. covariate $\rho(z)$.
- Evidence quote or page reference: "The diffusion estimator of intensity $\hat{\lambda}^H(u)$ can be defined as a sum of heat kernels... Numerical solution of the heat equation is many orders of magnitude faster than path-enumeration algorithms..." (Page 20)

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Methodological Finding | Bias | Severe | Naive Network KDE | Replacing Euclidean distance with network distance in a standard 2D kernel formula violates probability rules and does not conserve mass. | Page 12 |
| Methodological Finding | Bias | Unbiased | Heat Kernel Estimator | Simulating heat diffusion along the network conserves mass and correctly estimates uniform intensity. | Page 21 |
| Methodological Finding | False Alarm Rate | High | 2D K-function on networks | Using Euclidean K-functions on road networks creates spurious evidence of clustering ("false alarms"). | Page 11, 31 |

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? Theoretical properties (bias, mass conservation) and cross-validated bandwidth selections.
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. N/A (Methodological theory paper).
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They test estimator validity (unbiasedness, mass conservation).
- Are any metrics likely to be optimistic for real-world deployment? N/A.
- Which metric, if any, is most relevant to Open Road Risk? The leave-one-out likelihood cross-validation used for KDE bandwidth selection provides a good conceptual framework for spatial evaluation.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: In a point process model, "zero counts" are not explicitly modelled as a distinct class; they simply represent areas of the continuous network with low point intensity. The "zero inflation" problem of link-count models does not directly apply.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Poisson Point Processes.
- Whether high-risk locations are evaluated separately: Localised adaptive smoothing techniques are recommended for highly skewed networks.
- Evidence quote or page reference: "It has been reported that accident count data are often over-dispersed and zero-inflated, relative to Poisson regression. This could be partly attributable to aggregation bias." (Page 10)
- Practical relevance to my sparse collision link-year dataset: Provides a theoretical argument that your zero-heavy problem might be partially a self-inflicted artefact of aggregating sparse points into artificial OS link boundaries.

## 11. Validation Strategy

- Train/test split method: Likelihood cross-validation (leave-one-out).
- Spatial holdout used? yes (leave-one-out point spatial holdout for bandwidth selection).
- Temporal holdout used? no.
- Grouped holdout used? no.
- Cross-validation type: Leave-one-out cross validation (Equation 18).
- Metrics: Cross-validation log-likelihood.
- External validation: None.
- Leakage or generalisation risks: The review heavily warns against "false alarms" caused by misapplying standard spatial tools, which is a form of methodological leakage/bias.
- Evidence quote or page reference: "They include likelihood cross-validation in which we maximise the criterion $cv(\sigma) = \sum \log(\hat{\lambda}_\sigma^{-i}(x_i)) - \int \hat{\lambda}_\sigma(u)du$ based on the Poisson point process likelihood, where $\hat{\lambda}_\sigma^{-i}(x_i)$ is the 'leave-one-out' kernel estimate..." (Page 21)
- What I should copy or avoid: Avoid using standard planar Kernel Density Estimation (KDE) to generate visual "hotspot" maps for stakeholders, as it will overestimate risk in dense urban grids.

## 12. Key Findings Relevant to My Project

- Finding: Aggregating accident locations into discrete road segment counts introduces aggregation bias (ecological fallacy/MAUP) and obscures true spatial clustering.
- Why it matters: This serves as a fundamental theoretical warning for Open Road Risk's Stage 2 model, which relies on link-year counts. It suggests that highly localised risk features (like intersections) might be diluted by link aggregation.
- Evidence quote or page reference: "Potential weaknesses of this crash frequency approach include substantial bias due to aggregation... and the loss of spatial information needed to assess evidence for clustering." (Page 10)
- Confidence: High.

- Finding: Evaluating spatial clustering using Euclidean distances (e.g., standard planar KDE or Ripley's K-function) on road networks yields mathematically invalid "false alarms."
- Why it matters: If Open Road Risk generates standard density maps (heatmaps) or calculates spatial autocorrelation (Moran's I) using straight-line distances, the dense urban networks will appear artificially high-risk simply because they contain more road length per square mile.
- Evidence quote or page reference: "A completely random point pattern on the network could produce values $\hat{K}(r) > \pi r^2$ for small r, because nearby points are constrained to lie on the same one-dimensional line... producing spurious evidence of clustering." (Page 31)
- Confidence: High.

- Finding: Traffic intersections represent discrete spatial phenomena that break standard continuous network mathematics.
- Why it matters: Supports the hypothesis that junctions must be modelled distinctly, either via dummy variables, junction counts per link, or separating node/link risk entirely.
- Evidence quote or page reference: "Road traffic accidents frequently occur at a road intersection... In many point process models, there is zero probability that a random point will occur at a predetermined fixed location. Point process models need to be modified to allow points to occur exactly at a vertex..." (Page 9)
- Confidence: High.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Feature: Distance to nearest intersection | Prevents junction risk from being smeared across long segments. | OS Network Nodes | City/State (e.g. 115k segments) | 2.1M links | Candidate feature (Stage 2) | Medium | Requires massive graph traversal to calculate distance from segment midpoint to nearest true junction. |
| Avoidance of Planar KDE | Prevents publishing misleading risk maps. | N/A | N/A | UK-wide | Validation/Documentation | Low | Stakeholders often demand standard heatmaps; educating them requires effort. |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Continuous Spatial Point Process Modeling (`spatstat`) | Open Road Risk is fundamentally a link-level (areal count) pipeline for Stage 2. Moving to exact coordinate modeling breaks the entire AADT/exposure matching logic currently built on OS Links. | N/A (Architecture mismatch) | Up to ~115k segments | Unrealistic for 2.1M links + massive tabular ML integration. | Continue using XGBoost/GLM on links, but note the MAUP limitations in documentation. | High |
| Heat Kernel Density Estimation | Highly computationally intensive to solve the differential heat equation on a 2.1M edge graph. | N/A | City-scale (Perth CBD) | Low | Use standard link-level predictions rather than diffusing individual crash points. | High |

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? It supports using exposure (traffic volume) as a fundamental explanatory variable, but does not explicitly demand a mathematical fixed offset structure over a flexible covariate curve ($\rho(z)$).
- Does it suggest better handling of AADT/AADF uncertainty? No.
- Does it suggest useful geometry or road-context features? Yes, strongly supports separating out junctions/intersections from mid-link segments.
- Does it suggest better modelling of junctions? Yes, by highlighting that collisions mathematically concentrate at graph vertices, meaning models assuming continuous distribution along the edges will fail near junctions.
- Does it suggest better treatment of severity? Conceptually warns that excluding damage-only or low-severity self-reported data degrades the true spatial point pattern due to under-reporting bias.
- Does it suggest better validation design? No, its validation is focused on bandwidth selection for density curves.
- Does it expose a weakness in my current approach? Yes, heavily critiques the "crash frequency approach" (counting crashes on defined segments) for introducing ecological fallacy and masking local hotspots.

## 15. Repo Actionability

1.  Suggested repo action: Add a documentation note outlining the limitations of the "Crash Frequency / Segment" approach.
    - Action type: documentation note
    - Relevant stage: documentation
    - Why the paper supports it: Explicitly lists the methodological drawbacks of the Stage 2 architecture you are using (aggregation bias, ecological fallacy). Acknowledging this builds statistical credibility.
    - Evidence quote or page reference: "Potential weaknesses of this crash frequency approach include substantial bias due to aggregation (the 'ecological fallacy' or 'modifiable unit area problem')..." (Page 10)
    - Effort: low
    - Risk if implemented badly: None.

2.  Suggested repo action: Do not use standard 2D spatial KDE (e.g., default QGIS/Python heatmaps) to visualize Open Road Risk outputs or raw crash data for stakeholders.
    - Action type: documentation note / diagnostic
    - Relevant stage: validation
    - Why the paper supports it: The paper mathematically proves that 2D planar density mapping overestimates risk in dense road networks because it does not conserve network mass.
    - Evidence quote or page reference: "Using only the two-dimensional point locations, a kernel estimate of the spatially-varying density of accidents in two dimensions would give spuriously high density values in areas where the road network is more dense." (Page 10)
    - Effort: low
    - Risk if implemented badly: None.

3.  Suggested repo action: Engineer a "Distance to nearest junction" feature for all OS Open Roads links (e.g., from link midpoint).
    - Action type: candidate feature
    - Relevant stage: feature engineering / Stage 2
    - Why the paper supports it: The paper highlights that intersections attract a distinctly non-continuous accumulation of crashes. A distance-to-junction feature helps a segment-level model proxy this vertex-level phenomenon.
    - Evidence quote or page reference: "Models have been fitted to traffic accident data including covariates such as traffic volume, speed limit, and distance to nearest road intersection." (Page 28)
    - Effort: medium
    - Risk if implemented badly: Computationally heavy on 2.1 million links.

## 16. Query Tags

- spatial-point-processes
- linear-networks
- kernel-density-estimation
- network-K-function
- ecological-fallacy
- modifiable-areal-unit-problem
- aggregation-bias
- heat-kernel-diffusion
- intersection-risk
- spatial-statistics

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: The paper is a theoretical review of continuous point processes; it does not provide predictive evaluation metrics (RMSE, AUC) comparing point processes directly against XGBoost/GLM discrete count models.
- Parts of the paper that need manual checking: If you ever attempt to use `spatstat.linnet` in R for a small pilot, carefully review Sections 5.2 and 5.4 to ensure you use the mass-conserving heat kernel rather than the fallacious default estimators.
- Any likely ambiguity or risk of misinterpretation: The paper critiques the segment count method, but this does not mean Open Road Risk is invalid. Continuous point processes are mathematically pure but often fail to scale to national datasets with highly imputed traffic covariates. The critique should be absorbed as a known limitation, not a pipeline-killing defect.