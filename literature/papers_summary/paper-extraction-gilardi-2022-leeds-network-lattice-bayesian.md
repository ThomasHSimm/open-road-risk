# Paper Extraction: Gilardi, Mateu, Borgoni, Lovelace — Multivariate Hierarchical Analysis of Car Crashes on a Spatial Network Lattice

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: jrsssa_185_3_1150.pdf
- Suggested Markdown filename: paper-extraction-gilardi-2022-leeds-network-lattice-bayesian.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (full text in context)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full text, all tables, model equations accessible. Supplementary material not in PDF; referenced but not extracted. Code available at https://github.com/agila5/multivariate-analysis-car-crashes.

---

## 1. Citation

- Title: Multivariate hierarchical analysis of car crashes data considering a spatial network lattice
- Authors: Andrea Gilardi, Jorge Mateu, Riccardo Borgoni, Robin Lovelace
- Year: 2022
- DOI: https://doi.org/10.1111/rssa.12823
- Journal: Journal of the Royal Statistical Society: Series A (Statistics in Society), 185(3), 1150–1177
- Country / region studied: UK (City of Leeds, West Yorkshire)
- Study setting: Urban (major roads in a metropolitan area — motorways, primary roads, A roads)

---

## 2. Core Objective

- One-sentence description: The paper develops multivariate Bayesian hierarchical models on a road network lattice (OS segment-level) to estimate exposure-adjusted crash rates for slight and severe injury separately, accounting for spatial autocorrelation and between-severity correlation to identify high-risk road segments across the Leeds network.
- Main purpose: Hotspot detection / safety performance function / spatial modelling methodology
- Evidence quote: "This paper demonstrates a network lattice approach for identifying road segments of particular concern...We conclude that our methods enable a reliable estimation of road safety levels to help identify 'hotspots' on the road network." (Abstract)

**Direct relevance flag:** This is the most geographically and methodologically aligned paper extracted so far. It uses UK STATS19 data, OS road network data, covers a major northern English city (Leeds — within Open Road Risk's Yorkshire coverage), uses road segment-level analysis, and explicitly uses an exposure offset. Many design decisions mirror Open Road Risk's current approach. The key differences are: Bayesian INLA vs frequentist/XGBoost, multivariate severity modelling, and a spatial CAR random effect structure.

---

## 3. Response Variable

- Target variable: Count of car crashes per OS road segment, modelled separately by severity: (1) severe (serious + fatal combined); (2) slight
- Collision type: Injury crashes only (personal injury, occurring on public roads, reported to police within 30 days)
- Severity handling: Modelled jointly as a bivariate outcome — severe (serious + fatal combined, due to sparsity of fatal-only) and slight. Severity levels treated as correlated outcomes in a multivariate Bayesian framework.
- Count, binary, rate, risk score, severity class, or other: Count (non-negative integer); rates λᵢⱼ estimated from Poisson likelihood with exposure offset
- Time window used for outcomes: 2011–2018 (8 years aggregated); temporal dimension excluded to avoid extreme sparsity of severe crashes (>80% zero severe counts per segment-year)
- Evidence quote: "We decided to ignore the temporal dimension since severe crashes counts present an extreme sparsity, with more than 80% of zero counts during 2011–2018." (p. 1157)

**Important design choice:** The 8-year aggregation was explicitly adopted to manage severe crash sparsity. Even with aggregation, >80% of segments had zero severe crashes. This is directly analogous to Open Road Risk's link-year sparsity problem — the paper provides a worked example of how to handle this at a comparable spatial scale.

---

## 4. Exposure Handling

- Exposure variable used, if any: Eᵢ = segment length (km) × estimated traffic flow (number of daily commuters through the segment's MSOA, from 2011 Census OD data routed via shortest paths)
- Traffic count source: 2011 UK Census commuting origin-destination flows (WICID interface, UK Data Service). Not AADF. Flows routed through MSOA graph to estimate how many commuter trips pass through each MSOA, then assigned to road segments via spatial overlay. This is a Census-derived traffic proxy, not an observed vehicle count.
- Whether exposure is modelled, observed, assumed, or ignored: Estimated via Census routing — not directly observed. Acknowledged as a significant limitation.
- Treatment of missing or sparse traffic counts: Census-based routing applied to all segments. No imputation needed as the Census provides full coverage. However, the traffic measure captures commuter flows only (not all vehicle trips) and is from 2011 only (static for the whole 2011–2018 period).
- Whether offset terms, rates, denominators, or normalisation are used: **Formal log-offset used.** Exposure Eᵢ = length × traffic flow enters as log(Eᵢ) in the Poisson log-linear model. This ensures the model estimates crash rates per unit length per unit traffic, not raw crash counts. This is structurally identical to Open Road Risk's Stage 2 offset.
- Evidence quote: "The exposure parameter, Eᵢ, is given by the product of two quantities (Wang et al., 2009): the segment's length and the estimate of traffic flow...The exposure accounts for the fact that a longer street segment has a higher collision risk than a shorter one." (p. 1158)
- Transferability to my AADF/WebTRIS setup: High for the mathematical structure (log-offset of length × flow). Medium-low for the specific traffic data source (Census commuting OD flows are not AADF; they capture only commuting, miss HGV, leisure, freight; fixed at 2011).
- Notes: The Census-based traffic proxy is a deliberate open-data workaround — exactly the same challenge faced by Open Road Risk. The authors acknowledge it as a limitation. Open Road Risk's Stage 1a estimated AADT is a substantially better traffic proxy than 2011 Census commuting flows, which is a direct advantage for Open Road Risk over this paper's approach.

---

## 5. Spatial Unit of Analysis

- Unit: OS road segment (from OS Vector OpenMap Local — Roads and Tunnels layers)
- Segment length or segmentation rule: OS-defined variable-length segments. Mean length 118 m (SD 178 m), range 0.1 m to 2597 m. Major roads only (motorways, primary roads, A roads) — 3661 segments selected from ~50,000 total OS segments.
- How crashes are assigned to the network: STATS19 coordinates projected to nearest point on road network; crashes >10 m from nearest segment excluded. This 10 m threshold matches the precision of STATS19 coordinates.
- Treatment of junctions/intersections: Not modelled separately. Junctions are implicitly included in the segment-level analysis — segments share boundary points that define the adjacency matrix. No explicit junction exclusion (contrast: M25 papers excluded ~15% junction crashes).
- Spatial aggregation risks: Variable-length segments create heterogeneous units. The exposure offset (length × flow) partially addresses this but residual heterogeneity in segment-level risk remains.
- Evidence quote: "The segments have different lengths, ranging from 0.1 m to 2597 m, with an average value of 118 m (sd = 178 m)." (p. 1155); "we adopted this value [10m] as a threshold to account for the potential misalignment between the event locations and the network." (p. 1157)
- Relevance to OS Open Roads link-based pipeline: **High.** Open Road Risk also uses OS Open Roads variable-length links for major roads. This paper directly validates the OS segment-level approach for UK crash modelling. The adjacency matrix construction from OS segment boundary-sharing is directly applicable.

---

## 6. Temporal Unit of Analysis

- Years covered: 2011–2018 (8 years)
- Temporal resolution: All 8 years aggregated into a single cross-section per segment
- Whether seasonality or time-of-day is modelled: No
- Whether before-after or panel structure is used: No — single cross-sectional observation per segment (crash counts aggregated over 8 years). Temporal dimension explicitly dropped due to severe crash sparsity.
- Evidence quote: "We decided to ignore the temporal dimension since severe crashes counts present an extreme sparsity, with more than 80% of zero counts during 2011–2018." (p. 1157); "These numbers highlight a common temporal trend between the 8 years." (p. 1157)
- Relevance to WebTRIS-style time profiles: None — temporal analysis not pursued.

**Note for Open Road Risk:** The decision to collapse 8 years into a single cross-section due to severe crash sparsity is a direct methodological precedent for how to handle the fatal/serious sub-band in Open Road Risk's link-year data. The paper's supplementary material reportedly includes a space-time representation confirming the temporal trend is stable.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Segment length | OS Vector OpenMap Local | Direct from geometry | Part of exposure offset | Already present — OS Open Roads link length |
| Traffic flow (Census routing) | 2011 UK Census OD commuting flows (WICID) | Shortest-path routing of OD flows through MSOA graph; flow assigned to segments via spatial overlay | Part of exposure offset; accounts for differential exposure | Medium — structurally transferable; Open Road Risk uses estimated AADT which is superior to Census commuting proxy |
| Road type (motorway / primary / A road) | OS classification | Categorical dummy variables (A road as reference) | Strong predictor; motorways and primary roads safer than A roads for both severity types | Already present — OS Open Roads road classification |
| Dual carriageway flag | OS classification | Binary dummy | Significant for slight crashes (lower risk); not significant for severe | Candidate — OS Open Roads form-of-way field encodes dual carriageway; already in pipeline |
| Edge betweenness centrality | OS road network (computed) | Graph-theoretic betweenness centrality of each segment (number of shortest paths traversing it) | Used as VMT proxy; **found statistically insignificant** in all models | Already present in Open Road Risk; paper's null result is a useful diagnostic reference |
| Population density | 2011 UK Census (LSOA level) | Matched to segments via spatial overlay | Significant positive predictor for both slight and severe crashes | Candidate — UK census data available; already flagged as potential feature |
| Employment rate | 2011 UK Census (LSOA level) | Matched to segments via spatial overlay | **Not significant** in any model | Low priority — paper finds this null for Leeds |
| Spatial random effects (CAR/ICAR/PMCAR) | Latent field — no external data | Bayesian MCAR prior on segment adjacency graph | Captures spatial autocorrelation and unobserved heterogeneity | Low for direct implementation — computationally infeasible at 2.1M links; conceptually relevant |

---

## 8. Model Architecture

- Algorithms/models used: Six Bayesian hierarchical models (A–F) estimated via INLA (R-INLA + INLAMSM package). All share a Poisson likelihood with log-offset (length × flow). Models differ in prior structure for spatial (ICAR/PCAR) and unstructured random effects, and whether severity levels are modelled independently or jointly.
- Baseline models: (A) Independent IIMCAR spatial + independent unstructured; (B) independent IPMCAR spatial + independent unstructured
- Final/preferred model: **(F)** — Correlated Gaussian unstructured random effects + PMCAR (proper CAR) spatially structured random effects with between-severity correlation. Best by DIC, WAIC, and balanced accuracy.
- Loss function or likelihood: Poisson log-likelihood; log(λᵢⱼ) = β₀ⱼ + Σβ_mX_ijm + θᵢⱼ + φᵢⱼ where θ is unstructured and φ is spatially structured random effect
- Offset/exposure term, if used: **Yes — formal log-offset:** log(Eᵢ) = log(length × traffic flow). Crash rate λᵢⱼ estimated per unit exposure (per km per thousand daily commuters).
- Spatial autocorrelation handling: ICAR (intrinsic) and PCAR (proper) CAR priors; PMCAR (multivariate) captures between-severity spatial correlation. Adjacency matrix W built from OS segment boundary-sharing (dual representation of road network). First-order neighbours tested; second and third order also tested in sensitivity analysis.
- Temporal dependence handling: None — cross-sectional model
- Interpretability method: Posterior means and credible intervals for fixed effects (Table 2); posterior crash rate maps (Figure 5); balanced accuracy for hotspot classification (Table 4); MAUP sensitivity analysis via network contraction
- Evidence quote: "The exposure parameter, Eᵢ, is given by the product of two quantities (Wang et al., 2009): the segment's length and the estimate of traffic flow." (p. 1158)

**Computational note:** Each model took 30–45 minutes on a 6-core server with 32GB RAM for 3661 segments. MCMC was considered computationally infeasible at this scale; INLA used instead. At 2.1M Open Road Risk links, even INLA would face severe computational challenges. This is the central scalability constraint for this methodology.

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model comparison | DIC | 14103.44 (best) | Model F | Best-fitting model by DIC | Table 4, p. 1165 |
| Model comparison | WAIC | 14086.46 (best) | Model F | Best-fitting model by WAIC | Table 4 |
| Predictive fit | Balanced accuracy — severe | 0.675 (at 0.975-quantile) | Model F | Reasonable performance for sparse severe crashes | Table 4; Figure 6 |
| Predictive fit | Balanced accuracy — slight | 0.720 (at median) | Model F | Better performance for more common slight crashes | Table 4 |
| Fixed effect | Road type: Motorways vs A roads (severe) | −0.758 (Model F) | Severe crashes | Motorways significantly safer than A roads for severe crashes | Table 2, p. 1164 |
| Fixed effect | Road type: Motorways vs A roads (slight) | −0.055 (NS, Model F) | Slight crashes | Motorways not significantly safer than A roads for slight crashes | Table 2 |
| Fixed effect | Road type: Primary roads vs A roads (severe) | +0.473 (Model F) | Severe crashes | Primary roads slightly more prone to severe crashes than A roads | Table 2 |
| Fixed effect | Population density (severe) | +0.155 (Model F) | Severe crashes | Positive, significant | Table 2 |
| Fixed effect | Population density (slight) | +0.256 (Model F) | Slight crashes | Positive, stronger effect for slight crashes | Table 2 |
| Fixed effect | Employment rate | Not significant | Both severities | No significant relationship | Table 2; p. 1163 |
| Fixed effect | Edge betweenness centrality | Near zero, NS | Both severities | Insignificant VMT proxy | Table 2; p. 1163 |
| Fixed effect | Dual carriageway | −0.299 (significant) | Slight crashes | Dual carriageways safer for slight crashes | Table 2 |
| Fixed effect | Dual carriageway | −0.053 (NS) | Severe crashes | No effect on severe crashes | Table 2 |
| Hyperparameter | Between-severity correlation (spatial), ρ_φ | 0.829 (Model F) | Spatial random effects | Strong positive correlation between severe and slight spatial patterns | Table 3, p. 1165 |
| Hyperparameter | Between-severity correlation (unstructured), ρ_θ | 0.405 (Model F) | Unstructured random effects | Moderate positive correlation | Table 3 |
| MAUP sensitivity | Fixed effect sign/significance change under network contraction | None — signs and significance stable | Model F, contracted network (2700 vs 3661 segments) | Network lattice models are robust to MAUP | Section 5.3; Table 6 |

**Validation type:** DIC and WAIC are **in-sample model comparison** criteria. Balanced accuracy is computed via posterior predictive simulation (5000 Monte Carlo samples from posterior), not on held-out data. There is **no train/test split, no spatial holdout, no temporal holdout**. All validation is posterior predictive checking on the full dataset. This is the standard approach for Bayesian hierarchical models but means out-of-sample performance is not assessed.

**Are metrics likely to be optimistic?** Balanced accuracy from posterior predictive simulation (not held-out) is a measure of in-sample predictive adequacy, not external generalisation. It is somewhat more informative than DIC/WAIC but still not a holdout metric. The 0.675 balanced accuracy for severe crashes should be interpreted as "the model classifies zero vs non-zero severe crash segments reasonably well on the training data."

**Most relevant metric for Open Road Risk:** The balanced accuracy approach (binary zero/non-zero classification with simulation from posterior) is directly applicable as a Stage 2 diagnostic for Open Road Risk's Poisson GLM on the severe/KSI subset of crashes. It addresses the core sparsity problem more honestly than pseudo-R² alone.

---

## 10. Rare Event / Class Imbalance Handling

- How rare events are handled: Severe crashes (serious + fatal) aggregated to avoid extreme sparsity. >80% of segments have zero severe crashes over 8 years. The multivariate model borrows strength from the more common slight crash spatial pattern (ρ_φ = 0.83, ρ_θ = 0.41) to improve estimation of severe crash rates.
- Model family: Poisson with hierarchical random effects; negative binomial not used (overdispersion addressed through random effects). Zero-heavy counts handled through EB-like shrinkage via PMCAR spatial smoothing.
- Whether high-risk locations evaluated separately: Not stated separately; balanced accuracy evaluated by road class and carriageway type (no relevant differences found).
- Evidence quote: "The severe class is very sparse in the data set at hand, hence modelling both types of accidents simultaneously allows to borrow strength from the existing correlations and improves estimates." (p. 1152); "the correlation between spatially structured effects is found stronger than the other [unstructured]" (p. 1173)
- Practical relevance: **High.** The borrowing-strength mechanism via multivariate CAR models is the most principled approach found across all papers extracted so far for handling severe crash sparsity at road segment level. It is computationally infeasible at 2.1M links but conceptually highly relevant, and the balanced accuracy methodology for evaluation is directly adoptable.

---

## 11. Validation Strategy

- Train/test split method: None
- Spatial holdout used? No
- Temporal holdout used? No
- Grouped holdout used? No
- Cross-validation type: None — all validation is posterior predictive checking
- Metrics: DIC, WAIC (model comparison); balanced accuracy via 5000 posterior predictive simulations (model criticism)
- External validation: None
- Leakage or generalisation risks: Bayesian posterior predictive checks use the same data for fitting and evaluation. This is not data leakage in the classic sense — it is standard Bayesian model criticism — but it means predictive performance on new roads or new time periods is unknown. The MAUP sensitivity analysis (contracting the network) provides some robustness evidence but is not an external holdout.
- Evidence quote: "We simulated n Poisson random variables (one for each road segment) with mean equal to the mean of each posterior distribution...The distribution of the balanced accuracy measure was finally approximated by repeating this procedure N = 5000 times." (p. 1167–1168)
- What I should copy or avoid: Adopt the balanced accuracy simulation approach as a Stage 2 diagnostic for the zero/non-zero classification of severe crashes. Do not treat DIC/WAIC differences as measures of predictive generalisation. The approach to MAUP analysis (network contraction + re-estimation) is a methodological template for Open Road Risk's own MAUP sensitivity if segment definitions are changed.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: Road type (OS classification) is the strongest consistent fixed-effect predictor in all models. Motorways are significantly less prone to severe crashes than A roads. Primary roads are more prone to severe crashes than A roads (positive coefficient, significant). Neither road type is significantly associated with slight crash rates in the same direction.
- Why it matters: Confirms OS road classification as a reliable predictor in a UK network lattice model on a dataset closely analogous to Open Road Risk (STATS19, OS segments, Yorkshire). The opposite direction for motorways vs primary roads for severe crashes is important: if Open Road Risk's Stage 2 uses road type dummies, the sign and magnitude from this paper (Leeds, 2011–2018) provide a UK-specific reference for cross-checking.
- Evidence: Table 2; p. 1163 discussion.
- Confidence: High — stable across all 6 model specifications and both severity types.

**Finding 2:**
- Finding: Edge betweenness centrality is statistically insignificant in all models as a predictor of both slight and severe crash rates, even though it was used as a proxy for vehicle miles travelled (VMT). The authors flag this as "an unexpected result which may deserve further investigation."
- Why it matters: Open Road Risk includes betweenness centrality as a candidate Stage 1a/Stage 2 feature. This null result — from a UK network lattice model that uses centrality as a VMT proxy — suggests that centrality may not add predictive value once road type and length × flow exposure are controlled for. This is a direct caution for the feature's inclusion in Stage 2 without diagnostic validation.
- Evidence: Table 2; p. 1163: "The coefficients of edge betweenness centrality measures are found close to zero for all models."
- Confidence: High within this case study — stable across all 6 specifications. Does not rule out centrality being useful in a different model family (XGBoost may capture non-linear interactions where GLM finds it insignificant).

**Finding 3:**
- Finding: Dual carriageway is significantly associated with fewer slight crashes (coefficient −0.299 in best model) but has no significant effect on severe crashes. This is consistent with Castle and Lynam (2008) and another finding from the companion M25 study.
- Why it matters: Dual carriageway flag is already in Open Road Risk as a candidate feature from OS Open Roads form-of-way. This paper provides within-sample evidence for its relevance at the slight crash level in a UK urban network, with the direction matching physical expectation. The severity-specific nature of the effect reinforces the case for severity-stratified analysis.
- Evidence: Table 2; p. 1163: "dual carriageway roads have been found significantly less prone to slight car accidents, whereas no impact has been found for severe car crashes."
- Confidence: High — stable across all 6 model specifications.

**Finding 4:**
- Finding: Population density is significantly positively associated with both slight and severe crash rates, with a stronger effect for slight crashes. Employment rate is not significant in any model.
- Why it matters: Population density is a candidate feature for Open Road Risk (IMD data available). This paper provides direct UK evidence of its significance at the road segment level. Employment rate's null result suggests not prioritising employment-based proxies in Stage 2 feature engineering.
- Evidence: Table 2; p. 1163.
- Confidence: Medium — population density significant but effect magnitude moderate; single UK city case study.

**Finding 5:**
- Finding: The multivariate model structure substantially improves estimation of severe crash rates by borrowing strength from the correlated slight crash pattern. The spatial correlation between severity levels is ρ_φ ≈ 0.83 (spatial) and ρ_θ ≈ 0.41 (unstructured). Without the multivariate structure, the posterior variance of the severe crash random effect is degenerate (model A). Including correlation (model F) reduces DIC by ~360 units and improves balanced accuracy from 0.631 to 0.675.
- Why it matters: Provides strong evidence that modelling severe and slight crashes simultaneously rather than independently is beneficial when severe counts are highly sparse. For Open Road Risk, this suggests that a future severity-extension could jointly model slight and KSI crash counts rather than treating them as independent models.
- Evidence: Tables 3–4; p. 1163–1165; p. 1173.
- Confidence: High within this model family — consistent improvement across model hierarchy A→F.

**Finding 6:**
- Finding: The network lattice approach is robust to MAUP: contracting the OS network from 3661 to ~2700 segments (by removing redundant vertices) does not materially change the sign, magnitude, or significance of any fixed-effect coefficient. Random effect hyperparameters show slightly higher spatial uncertainty in the contracted network but predicted crash rate maps are similar.
- Why it matters: Open Road Risk uses OS Open Roads links, which are already a simplification of the raw OS network. This finding provides direct evidence that OS-segment-based models are robust to reasonable changes in segment definition — reassuring for Open Road Risk's use of the OS Open Roads schema.
- Evidence: Section 5.3; Tables 6–7; p. 1171–1172.
- Confidence: High within this case study — MAUP test is thorough and results clearly stated.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Exposure offset: log(length × AADT) | Paper demonstrates this is the correct structure for a UK OS-segment crash model; identical to Open Road Risk's current approach | Already in pipeline (estimated AADT × link length) | 3661 major-road segments, Leeds | Already implemented — confirms current design | Stage 2 — already present; document literature support | None | None — already done |
| Balanced accuracy (binary zero/non-zero) as sparse-count evaluation metric | Addresses sparsity honestly; avoids misleading standard accuracy; evaluable via posterior predictive simulation for Poisson GLM | Open Road Risk GLM posterior predictions + observed counts | 3661 segments | Compatible — scales to any segment count with binning | Stage 2 / validation | Low | At 2.1M links, requires binning by subgroup; threshold choice (zero vs non-zero) may need adjusting for link-year vs 8-year aggregate counts |
| OS segment adjacency matrix (dual graph representation) | Paper demonstrates construction of W from boundary-sharing for CAR spatial models; same approach applicable if Open Road Risk adds any spatial model | OS Open Roads geometry | 3661 segments | Computationally feasible for adjacency construction; not for INLA at 2.1M scale | Future spatial extension / documentation | Medium (adjacency matrix construction scales to 2.1M with sparse methods) | Dense adjacency matrix for 2.1M links is infeasible; sparse row-by-row construction required |
| Road type and dual carriageway as fixed effects | Both significant in UK network lattice model; signs and magnitudes provide UK-specific reference values for cross-checking Open Road Risk's Stage 2 GLM coefficients | Already in pipeline | 3661 segments, Leeds 2011–2018 | Compatible | Stage 2 / validation / documentation | Low — already in pipeline; use coefficients as reference | Paper is Leeds-only; Open Road Risk covers a broader geography |
| Population density as fixed effect | Significant predictor at segment level in UK urban context | UK census (available) | 3661 segments | Compatible | Stage 2 candidate feature | Low | Paper covers urban Leeds only; effect in rural areas may differ |
| MAUP sensitivity analysis via network contraction | Tests robustness of results to OS segment definition choices; directly applicable to Open Road Risk's OS Open Roads schema | OS Open Roads geometry + R/Python network tools | 3661 → ~2700 segments | Compatible as a small diagnostic pilot on a subset of the network | Validation / diagnostic | Medium (requires implementing contraction algorithm or using dodgr R package) | Computationally intensive at full Open Road Risk scale; feasible on a sub-regional pilot |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full Bayesian MCAR/PMCAR model via INLA | 30–45 min per model for 3661 segments on a 32GB server. At 2.1M links, this is computationally infeasible. INLA does not scale linearly with n for spatial models. | No data gap — computational barrier | 3661 segments | Computationally incompatible at production scale | Spatial lag features as a deterministic approximation; INLA feasible on sub-regional pilot (e.g., Yorkshire only, ~200k links) | High |
| Census commuting OD flows as traffic proxy | Captures commuting only (not freight, leisure, HGV); from 2011 Census; no update for 2011–2018 period. Open Road Risk uses estimated AADT which is substantially superior. | 2011 Census WICID available; but outdated and partial | 3661 segments | Not applicable — Open Road Risk's Stage 1a AADT is already a better proxy | No workaround needed — AADT is already the correct approach | High |
| Multivariate severity modelling (slight + severe jointly) | Joint bivariate Poisson MCAR requires INLA or MCMC; not feasible at 2.1M links. Separate models for slight and severe are more practical at scale. | No data gap — computational barrier | 3661 segments | Low at production scale | Compute correlation between Stage 2 GLM residuals for slight and KSI as a diagnostic; separate models for each severity band | Medium |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Yes, strongly. The paper uses an identical log-offset structure (length × traffic flow) and finds it essential for comparable risk estimation across segments of different lengths and traffic volumes. This is the highest-quality independent support found across all papers extracted so far for Open Road Risk's offset design, and it uses UK data on OS segments.
- **Does it suggest better handling of AADT/AADF uncertainty?** Indirectly — the paper uses Census commuting flows as a deliberately open-data proxy for traffic, acknowledging AADF as the preferred but unavailable source. This validates Open Road Risk's choice to estimate AADT from AADF counts rather than use Census-derived proxies.
- **Does it suggest useful geometry or road-context features?** Yes: road type (OS classification), dual carriageway, population density confirmed as significant. Betweenness centrality null result is a useful caution.
- **Does it suggest better modelling of junctions?** No — junctions not modelled separately.
- **Does it suggest better treatment of severity?** Yes — the joint multivariate approach for slight and severe provides the strongest methodological case for combined severity modelling. At Open Road Risk scale, the full MCAR approach is infeasible, but the finding that ρ_φ ≈ 0.83 between severity levels supports using the slight crash model to improve the severe crash ranking diagnostically.
- **Does it suggest better validation design?** Yes — the balanced accuracy approach with posterior predictive simulation addresses zero-heavy count data more honestly than standard accuracy or pseudo-R².
- **Does it expose a weakness in my current approach?** Two. First: Open Road Risk's current Stage 2 does not evaluate the severe/KSI sub-band separately with a zero/non-zero balanced accuracy metric — the paper demonstrates this is necessary given the sparsity. Second: betweenness centrality is in Open Road Risk's feature set but is insignificant in this comparable UK model; it should be validated rather than assumed to add value.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add a documentation note citing this paper as the primary UK literature support for Open Road Risk's log-offset structure (log(AADT × link_length_km × 365 / 1e6)). Document that the paper uses an identical mathematical structure on OS segments with STATS19 data in Yorkshire, providing direct validation of the design choice.
- Action type: Documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Equation in Section 3, p. 1158; same structure as Open Road Risk's offset; same data sources (STATS19 + OS).
- Effort: Low
- Risk if implemented badly: None for documentation.

**Action 2**
- Suggested repo action: Implement balanced accuracy (binary zero/non-zero classification, 5000 Monte Carlo simulations from Poisson posterior) as a Stage 2 diagnostic, specifically for the severe/KSI crash sub-band. Report alongside pseudo-R² and RMSE.
- Action type: Diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Paper demonstrates this is the appropriate metric for sparse-count binary classification (Section 5.1; Table 4; Figure 6). Standard accuracy is "biased and overly optimistic in case of unbalanced classes."
- Effort: Low — straightforward to implement from Poisson GLM predictions
- Risk if implemented badly: For link-year data (not 8-year aggregates), the zero fraction is much higher (~98–99%). The threshold may need adjustment or subgroup stratification to be meaningful. Do not assume the 0.675 balanced accuracy from Leeds is a useful benchmark.

**Action 3**
- Suggested repo action: Run a diagnostic in Stage 2 checking whether edge betweenness centrality contributes predictive value once road type and the AADT offset are included. The paper finds it insignificant in a comparable UK GLM; if it is also near-zero in Open Road Risk's GLM, consider removing it from the GLM feature set (retaining it in XGBoost where non-linear interactions may capture indirect effects).
- Action type: Diagnostic
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Table 2: "The coefficients of edge betweenness centrality measures are found close to zero for all models." (p. 1163)
- Effort: Low (check existing GLM coefficients)
- Risk if implemented badly: Betweenness centrality may still be useful in XGBoost for non-linear patterns not captured by the GLM; do not remove from XGBoost feature set without testing.

**Action 4**
- Suggested repo action: Confirm that the dual carriageway flag from OS Open Roads form-of-way is correctly implemented in Stage 2 and document the expected sign (negative coefficient for slight crashes; near-zero for severe) based on this paper's results.
- Action type: Documentation note / validation
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Table 2, Model F: dual carriageway coefficient −0.299 for slight, −0.053 (NS) for severe; "dual carriageway roads have been found significantly less prone to slight car accidents." (p. 1163)
- Effort: Low
- Risk if implemented badly: None for documentation; coefficient magnitude may differ in Open Road Risk's multi-road-type dataset vs Leeds urban major-roads-only.

**Action 5**
- Suggested repo action: Add a documentation note that a full spatial MCAR/CAR model (INLA-based) is the methodologically optimal approach for this problem but computationally infeasible at Open Road Risk's 2.1M link scale. Document that spatial lag features (local crash density, neighbouring link crash history) and grouped validation by road corridor are the practical alternatives that partially replicate the spatial smoothing benefit.
- Action type: Documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Model F (PMCAR) substantially outperforms non-spatial baselines (DIC 14103 vs 14462); paper demonstrates 30–45 min per model for 3661 segments.
- Effort: Low
- Risk if implemented badly: None for documentation.

---

## 16. Query Tags

- Bayesian-hierarchical
- INLA
- PMCAR
- IMCAR
- CAR-spatial-model
- network-lattice
- OS-segments
- STATS19
- UK-Leeds
- Yorkshire
- exposure-offset
- multivariate-severity
- borrowing-strength
- severe-slight-joint-model
- betweenness-centrality-null
- dual-carriageway
- population-density
- road-type-OS
- MAUP-network
- balanced-accuracy
- zero-heavy-counts
- in-sample-validation-only
- Census-traffic-proxy
- open-data-UK

---

## 17. Confidence and Gaps

- Overall confidence in extraction: High — full paper text, all tables, and model equations are in context.
- Important details not stated in the paper: Supplementary material (space-time representation, pseudo-code for balanced accuracy, alternative prior sensitivity results) not in PDF. Exact number of crashes per segment by road type not stated. Crash year range is stated (2011–2018) but whether STATS19 ONS severity adjustment was applied uniformly to all 8 years is described qualitatively but not verified numerically.
- Parts of the paper that need manual checking: Table 2 is very wide (14 columns); cross-check that the dual carriageway coefficient for slight crashes (−0.299 in Model F) is correctly attributed to slight and not severe — the table layout is dense. Confirm that Primary Roads coefficient in Model F (severe: +0.473, slight: +0.599) is statistically significant — the paper states "Primary Roads have been found safer than A roads both for severe and slight" (p. 1163) but the positive coefficient sign in Table 2 for both severity types contradicts this claim in the text. This may be a sign convention issue in the table (where positive means more prone to crashes relative to A roads, and A roads are the baseline). Manual check recommended.
- Any likely ambiguity or risk of misinterpretation: (1) Table 2 fixed effect signs: positive coefficient for Primary Roads vs A roads in both severity levels suggests Primary Roads have higher crash rates than A roads, not lower. The text's claim that "Primary Roads have been found safer than A roads" may be incorrect or the reference category interpretation may differ. **This should be manually verified before citing specific coefficient directions.** (2) The Census commuting flow exposure proxy is acknowledged as a major limitation — it is not AADF and likely understates exposure for non-commuting traffic. Open Road Risk's estimated AADT is a substantially better proxy. (3) The balanced accuracy values (0.675 for severe, 0.72 for slight) are from posterior predictive checking, not holdout testing, and should not be read as external validation accuracy.
