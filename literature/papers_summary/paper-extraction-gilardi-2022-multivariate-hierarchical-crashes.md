RAW_MARKDOWN_START
Save this as: paper-extraction-gilardi-2022-multivariate-hierarchical-crashes.md

# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: jrsssa_185_3_1150.pdf
- Suggested Markdown filename: paper-extraction-gilardi-2022-multivariate-hierarchical-crashes.md
- AI tool used: Gemini
- Model name, if visible: Gemini 3.1 Pro
- Model version, if visible: not stated
- Interface used: API
- Input type: PDF upload
- Output mode: raw Markdown copy block
- Was the full paper accessible to the model? yes
- Notes on access limitations: None

## 1. Citation

- Title: Multivariate hierarchical analysis of car crashes data considering a spatial network lattice
- Authors: Andrea Gilardi, Jorge Mateu, Riccardo Borgoni, Robin Lovelace
- Year: 2022
- DOI or URL, if present: 10.1111/rssa.12823
- Country / region studied: United Kingdom (Leeds, West Yorkshire)
- Study setting: urban / mixed / metropolitan

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify: The paper models the spatial distribution and severity of road traffic collisions on an urban street network to identify high-risk segments, explicitly accounting for spatial autocorrelation and the correlated nature of different crash severities.
- Main purpose: hotspot detection / descriptive analysis / safety performance function
- Evidence quote or page reference: "This paper demonstrates a network lattice approach for identifying road segments of particular concern... We consider a family of Bayesian hierarchical models that include spatially structured and unstructured random effects to capture the dependencies between the severity levels." (Page 1)

## 3. Response Variable

- Target variable: Count of car crashes per street segment.
- Collision type: injury / fatal / serious / slight (grouped into 'severe' and 'slight').
- Severity handling: Severe (fatal + serious) and slight crashes are modelled simultaneously using a multivariate framework.
- Count, binary, rate, risk score, severity class, or other: Count (Poisson distributed).
- Time window used for outcomes: 8-year period (2011-2018), aggregated entirely (time dimension ignored).
- Evidence quote or page reference: "We decided to ignore the temporal dimension since severe crashes counts present an extreme sparsity, with more than 80% of zero counts during 2011-2018." (Page 8)

## 4. Exposure Handling

- Exposure variable used, if any: `E_i`, representing exposure as the product of segment length and estimated traffic flow.
- Traffic count source: Commuting journey Origin-Destination flows from the 2011 UK Census (WICID interface), routed onto the network via shortest path.
- Whether exposure is modelled, observed, assumed, or ignored: Estimated/Assumed based on commuting shortest paths.
- Treatment of missing or sparse traffic counts: The paper focuses on major roads (Motorways, Primary, A-roads) where flows are likely non-zero; it does not detail handling of zero-flow minor links.
- Whether offset terms, rates, denominators, or normalisation are used: Used as an offset term in the Poisson log-linear model.
- Evidence quote or page reference: "Poisson(E_i \lambda_{ij}), where E_i is an exposure parameter... given by the product of two quantities: the segment’s length and the estimate of traffic flow" (Page 9).
- Transferability to my AADF/WebTRIS setup: high (for the mathematical offset structure) / low (for the specific traffic data source).
- Notes: The exposure offset mathematical formulation is highly transferable and identical to standard practice. However, the use of Census commuting O-D flows as a surrogate for AADT is highly specific and likely inferior to Open Road Risk's WebTRIS/AADF ML estimator, so their specific data source should not be copied.

## 5. Spatial Unit of Analysis

- Unit: road segment
- Segment length or segmentation rule: Derived directly from Ordnance Survey Vector OpenMap Local road links. Short isolated islands were algorithmically removed. Segment lengths vary (mean 118m, sd 178m).
- How crashes are assigned to the network: Snapped to the nearest point on the simplified major road network (10m threshold used to drop unmatchable crashes).
- Treatment of junctions/intersections: Handled implicitly as the nodes where segments meet (first-order adjacency matrix defined by shared boundary points).
- Spatial aggregation risks: Modifiable Areal Unit Problem (MAUP) is explicitly evaluated by contracting the network (removing redundant vertices to merge contiguous segments). The statistical results were found to be robust to this modification.
- Evidence quote or page reference: "Our results tell a somewhat different story. The statistical analysis is found quite robust to MAUP when carried out on a network lattice, possibly because the road network has a physical geometrical meaning and, hence, a lower degree of arbitrariness than administrative boundaries." (Page 22)
- Relevance to OS Open Roads link-based pipeline: High. Validates that using raw OS links as the spatial unit is robust and likely does not suffer severely from MAUP issues compared to arbitrary polygons.

## 6. Temporal Unit of Analysis

- Years covered: 2011-2018.
- Temporal resolution: Aggregated across all 8 years.
- Whether seasonality or time-of-day is modelled: No.
- Whether before-after or panel structure is used: No.
- Evidence quote or page reference: "We decided to ignore the temporal dimension since severe crashes counts present an extreme sparsity" (Page 8).
- Relevance to WebTRIS-style time profiles: None. The paper ignores temporal dynamics.

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Segment length | OS OpenMap Local | Spatial measurement | Forms the baseline exposure metric. | Already present. |
| Traffic Volume Proxy | 2011 UK Census O-D data | Shortest-path routing of MSOA-to-MSOA commuter flows. | Represents vehicle exposure. | Low (Open Road Risk uses better AADF/WebTRIS ML estimates). |
| Road Type | OS OpenMap Local | Categorical extraction (Motorway, Primary, A Road). | Proxies road design and speeds. | Already present / compare implementation. |
| Dual Carriageway | OS OpenMap Local | Boolean dummy extraction. | Captures physical separation of flows. | Transferable (OS Open Roads attribute). |
| Edge Betweenness | Road graph | Computed centrality based on shortest paths traversing the segment. | Proxy for network importance / vehicle miles travelled (VMT). | Transferable (calculate via NetworkX / igraph). |
| Population Density | 2011 Census (LSOA) | Overlay/Intersection matching. | Captures urban density/pedestrian exposure context. | Transferable. |
| Employment Rate | 2011 Census (LSOA) | Overlay/Intersection matching. | Proxy for local economic activity. | Transferable. |

## 8. Model Architecture

- Algorithms/models used: Bayesian hierarchical Poisson models fitted via Integrated Nested Laplace Approximation (INLA).
- Baseline model: Independent intrinsic/proper multivariate conditional autoregressive (IIMCAR / IPMCAR) models.
- Final/preferred model: Model (F) - Multivariate spatial random effects (PMCAR) with correlated unstructured random effects across severities.
- Loss function or likelihood, if stated: Poisson likelihood.
- Offset/exposure term, if used: `log(traffic * length)`
- Spatial autocorrelation handling: Modelled using a Proper Multivariate Conditional Autoregressive (PMCAR) prior based on the graph adjacency matrix of the road segments.
- Temporal dependence handling: Ignored.
- Interpretability method: Direct interpretation of posterior means and 95% credible intervals for fixed-effect coefficients.
- Evidence quote or page reference: "Model (F) is the best one according to both criteria [DIC/WAIC]... includes a multivariate spatially unstructured random effect and a multivariate spatially structured PMCAR random effect." (Page 16, 23)

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model Fit | WAIC | 14086.46 | Model (F) - PMCAR | Lowest WAIC among tested models, indicating best parsimony/fit. | Table 4, p. 16 |
| Model Fit | DIC | 14103.44 | Model (F) - PMCAR | Lowest DIC among tested models. | Table 4, p. 16 |
| Classification (in-sample) | Balanced Accuracy | 0.675 | Severe crashes (Model F) | Using 0.975 quantile to separate 0 vs 1+ crashes performs moderately well. | Table 4, p. 16 |
| Classification (in-sample) | Balanced Accuracy | 0.720 | Slight crashes (Model F) | Using median to separate 0 vs 1+ crashes performs well. | Table 4, p. 16 |
| Fixed Effect | Coefficient (Mean) | -0.324 | Dual Carriageway (Slight) | Dual carriageways are associated with significantly fewer slight crashes. | Table 2, p. 14 |
| Fixed Effect | Coefficient (Mean) | 0.258 | Pop Density (Slight) | Higher population density correlates strongly with higher slight crashes. | Table 2, p. 14 |

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated? These are **in-sample posterior predictive diagnostics** and in-sample information criteria (DIC/WAIC).
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy. This applies to the reported "Balanced Accuracy."
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else? They test model fit, parsimony, and posterior predictive adequacy (via confusion matrices of binned counts).
- Are any metrics likely to be optimistic for real-world deployment? Yes, the balanced accuracy is completely in-sample and benefits from the local smoothing of the PMCAR spatial random effects, which is a form of leakage if evaluated for out-of-sample prediction.
- Which metric, if any, is most relevant to Open Road Risk? The use of Balanced Accuracy to diagnose heavily imbalanced bins (0 vs 1+) is conceptually useful for evaluating the Stage 2 models diagnostically.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Zero-heavy counts (80%+ zeros for severe crashes) are handled by a joint multivariate model structure. The model "borrows strength" from the more frequent 'slight' crashes via correlation parameters in both structured and unstructured spatial random effects.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Standard Poisson likelihood. No zero-inflation mechanism is explicitly used; the hierarchical random effects manage overdispersion.
- Whether high-risk locations are evaluated separately: No.
- Evidence quote or page reference: "The severe class is very sparse in the data set at hand, hence modelling both types of accidents simultaneously allows to borrow strength from the existing correlations and improves estimates." (Page 3)
- Practical relevance to my sparse collision link-year dataset: High conceptually. Using a multi-task setup (predicting severe and slight together, or predicting multiple collision types simultaneously) might improve regularisation and signal for the rarest collision types in Stage 2.

## 11. Validation Strategy

- Train/test split method: None. Entire dataset fitted simultaneously.
- Spatial holdout used? no
- Temporal holdout used? no
- Grouped holdout used? no
- Cross-validation type: None.
- Metrics: DIC, WAIC, Balanced Accuracy (in-sample).
- External validation: None.
- Leakage or generalisation risks: High generalisation risk. Because it uses PMCAR spatial random effects without a spatial/temporal holdout, the risk estimation for a segment heavily uses the observed crashes on that specific segment and its immediate neighbours during fitting. This is descriptive smoothing, not true out-of-sample prediction.
- What I should copy or avoid: Avoid the lack of holdout. Continue using spatial/grouped link splits in Open Road Risk. Copy the use of "Balanced Accuracy" (average of sensitivity and specificity) for evaluating highly imbalanced diagnostic bins.

## 12. Key Findings Relevant to My Project

- Finding: Network MAUP (Modifiable Areal Unit Problem) has a mild/negligible impact on lattice network models. Merging contiguous segments did not change fixed effect significance or order of magnitude.
- Why it matters: Validates Open Road Risk's decision to use raw OS Open Roads links rather than enforcing arbitrary 100m sub-segmentation.
- Evidence quote or page reference: "The statistical analysis is found quite robust to MAUP when carried out on a network lattice..." (Page 22)
- Confidence: High (explicit sensitivity analysis run to prove it).

- Finding: Modelling sparse severities jointly with common severities improves variance estimation.
- Why it matters: If Open Road Risk attempts KSI (Killed/Seriously Injured) specific modeling, doing so independently may fail due to sparsity. Multi-target modelling (e.g., predicting all crashes and KSIs jointly) could stabilise results.
- Evidence quote or page reference: "Models from (A) to (D)... exhibit a degenerate posterior distribution of \sigma^2_{\theta_1}... This problem gets mitigated once the correlation parameter between the two severity levels is included..." (Page 14)
- Confidence: High.

- Finding: Proper CAR (PMCAR) outperforms Intrinsic CAR (IMCAR) for network adjacency.
- Why it matters: If attempting spatial smoothing or explicit spatial dependency in Stage 2, allowing an estimated autoregression parameter ($\rho$) is better than assuming $\rho = 1$ (intrinsic).
- Evidence quote or page reference: "PMCAR models... are found to perform always better than their Intrinsic counterparts in terms of goodness of fit." (Page 16)
- Confidence: Medium (relies entirely on in-sample DIC/WAIC).

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Balanced Accuracy | Good diagnostic for zero-heavy counts. | Existing predictions | 3600 links | 2.1M links | Validation / Diagnostic | Low | None. |
| Network Betweenness Centrality | Captures route hierarchy beyond simple OS class. | OS Network geometry | 3600 links | 2.1M links | Candidate Feature (Stage 2) | Medium | Computationally expensive on a 2.1M node graph. |
| Multi-task learning (Severity) | Borrows strength for rare KSIs. | STATS19 severities | 3600 links | 2.1M links | Candidate model extension | High | XGBoost supports multi-target, but tuning becomes complex. |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full MCMC/INLA PMCAR | Computationally intractable at massive scale. | N/A (Method limitation) | ~3600 links | 2.1M links | Use localized Empirical Bayes smoothing or purely feature-based spatial coordinates. | High |
| Commuter O-D traffic surrogate | Weak proxy for true AADT; ignores freight/leisure. | N/A (Data choice) | Leeds City | UK-wide | Stage 1a ML AADT estimator already supersedes this. | High |

## 14. Pipeline Implications

- Does this paper support using exposure-normalised collision risk? Yes, strongly. It uses a log(exposure) offset exactly as Open Road Risk does.
- Does it suggest better handling of AADT/AADF uncertainty? No. It ignores traffic uncertainty, treating the O-D proxy as a fixed known offset.
- Does it suggest useful geometry or road-context features? Yes, edge betweenness centrality and dual-carriageway flags.
- Does it suggest better modelling of junctions? No, junctions are implicit points on the graph.
- Does it suggest better treatment of severity? Yes. It shows multi-target (multivariate) modeling prevents degenerate variance estimation for very rare (severe) crashes.
- Does it suggest better validation design? No, its validation is purely in-sample descriptive smoothing.
- Does it expose a weakness in my current approach? No explicit weakness exposed, but it highlights that spatial correlation (if unmodeled in XGBoost) holds substantial explanatory power.

## 15. Repo Actionability

1.  Suggested repo action: Note in documentation that network MAUP risks are low for OS links.
    - Action type: documentation note
    - Relevant stage: documentation
    - Why the paper supports it: The sensitivity analysis found fixed effects and risk estimates were robust to contracting the network and merging segments.
    - Evidence quote or page reference: "The statistical analysis is found quite robust to MAUP when carried out on a network lattice" (Page 22).
    - Effort: low
    - Risk if implemented badly: None.

2.  Suggested repo action: Evaluate Stage 2 model diagnostics using Balanced Accuracy for binned 0 vs 1+ crashes.
    - Action type: diagnostic
    - Relevant stage: validation
    - Why the paper supports it: Standard accuracy fails on 98% zero datasets. Balanced accuracy (Sensitivity + Specificity / 2) provides a fairer view of diagnostic cutoff utility.
    - Evidence quote or page reference: "The balanced accuracy... overcomes this drawback since it represents an average between the predictive performances on each class." (Page 18)
    - Effort: low
    - Risk if implemented badly: None (purely diagnostic).

3.  Suggested repo action: Calculate graph Edge Betweenness Centrality for Open Roads.
    - Action type: candidate feature
    - Relevant stage: feature engineering
    - Why the paper supports it: Used as a proxy for network routing importance and VMT beyond raw AADT.
    - Evidence quote or page reference: Table 2 (Though noted as non-significant in their specific Leeds subset, it is theoretically sound).
    - Effort: high (due to compute scaling on 2.1 million nodes).
    - Risk if implemented badly: Waste of compute time if it correlates perfectly with Stage 1a AADT estimates.

## 16. Query Tags

- AADT-proxy
- exposure-offset
- multivariate-model
- Bayesian-hierarchical
- INLA
- PMCAR
- MAUP
- network-lattice
- zero-heavy-counts
- severity-model
- UK-transferable
- segment-level
- in-sample-diagnostic

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: The exact handling of minor/unclassified roads (seems they were dropped to avoid isolated network islands, leaving only 3600 major segments).
- Parts of the paper that need manual checking: The precise algorithm used in `dodgr` for network contraction if you wish to replicate their MAUP test.
- Any likely ambiguity or risk of misinterpretation: The paper repeatedly uses the word "prediction", but mathematically all their procedures (including the Balanced Accuracy distributions) are posterior predictive checks on the *training* data. There is no spatial or temporal holdout. Readers must not confuse this with true forecasting accuracy.