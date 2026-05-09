# Paper Extraction: Gilardi et al. 2022 — Multivariate Hierarchical Analysis of Car Crashes on a Spatial Network Lattice

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: jrsssa_185_3_1150.pdf
- Suggested Markdown filename: paper-extraction-gilardi-2022-network-lattice-crashes.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (full paper rendered in context as document)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: All 28 pages were rendered as text in context. Figures and maps were not directly viewable but are described in text sufficiently for extraction purposes. Table 2 fixed-effects values were available in full. Supplementary material referenced in the paper was not accessible.

---

## 1. Citation

- Title: Multivariate hierarchical analysis of car crashes data considering a spatial network lattice
- Authors: Andrea Gilardi, Jorge Mateu, Riccardo Borgoni, Robin Lovelace
- Year: 2022
- DOI or URL: https://doi.org/10.1111/rssa.12823
- Country / region studied: United Kingdom (Leeds, West Yorkshire, England)
- Study setting: mixed (urban metropolitan area, major roads including motorways, primary roads and A roads)

---

## 2. Core Objective

- One-sentence description: The paper estimates exposure-adjusted road segment crash rates jointly for two severity levels (slight and severe) using a family of Bayesian hierarchical multivariate models on an OS road network lattice, in order to identify hotspot segments in Leeds.
- Main purpose: hotspot detection / safety performance function
- Evidence quote or page reference: "This paper demonstrates a network lattice approach for identifying road segments of particular concern" (Abstract, p.1150); "a statistical model to identify street sections with anomalously high car crashes rates" (p.1151)

---

## 3. Response Variable

- Target variable: Count of road traffic collisions per road segment, modelled jointly for two severity levels (slight; severe = serious + fatal combined)
- Collision type: injury (personal injury only; excludes property-damage-only); fatal and serious aggregated into "severe"; slight modelled separately
- Severity handling: bivariate — slight and severe modelled simultaneously with shared spatial and unstructured random effects; fatal (~1% of total) merged into severe due to sparsity
- Count, binary, rate, risk score, severity class, or other: count (Poisson likelihood); crash rate λ_ij is the modelled quantity (crashes per unit of exposure)
- Time window used for outcomes: 8-year aggregate 2011–2018 (temporal dimension collapsed; not modelled as panel)
- Evidence quote or page reference: "We decided to ignore the temporal dimension since severe crashes counts present an extreme sparsity, with more than 80% of zero counts during 2011–2018" (p.1157)

---

## 4. Exposure Handling

- Exposure variable used: E_i = segment length (km) × estimated traffic flow (daily commuters from Census OD routing) — used as a Poisson offset
- Traffic count source: 2011 UK Census commuting origin-destination flow data, aggregated at MSOA level; shortest-path routing used to assign flow-through volumes to each MSOA; then spatially overlaid to assign traffic estimates to road segments
- Whether exposure is modelled, observed, assumed, or ignored: partially observed / estimated. Census OD flows are a proxy for traffic; they are not direct vehicle counts. Authors acknowledge this is an estimate.
- Treatment of missing or sparse traffic counts: not directly addressed. The Census routing approach assigns a traffic estimate to every MSOA and hence every segment; no segment is left without an exposure estimate. However, uncertainty in the traffic proxy is not propagated into the collision model.
- Whether offset terms, rates, denominators, or normalisation are used: yes — log(E_i) = log(segment_length × traffic_flow) is used as an offset in the Poisson log-linear model, so the model estimates crash rates rather than raw counts
- Evidence quote or page reference: "the exposure parameter, E_i, is given by the product of two quantities: the segment's length and the estimate of traffic flow" (p.1158, Section 3); "The exposure accounts for the fact that a longer street segment has a higher collision risk than a shorter one" (p.1158)

### Transferability to my AADF/WebTRIS setup

- Mathematical exposure-offset structure (log-offset of length × flow): **high transferability** — directly analogous to the offset already used in Open Road Risk Stage 2 (`log(AADT × link_length_km × 365 / 1e6)`)
- Paper's specific traffic data source (Census commuting OD flows routed via shortest path): **low transferability** — this is a commuting-only proxy with known biases; Open Road Risk uses AADF-based AADT estimates which are more directly comparable to vehicle kilometres travelled
- Notes: The paper's Census-derived flow is explicitly a proxy and is acknowledged to undercount non-commute trips. Open Road Risk's AADF-derived AADT estimate is more methodologically sound as a traffic exposure proxy, even accounting for estimation uncertainty. The paper does not propagate traffic-proxy uncertainty into the model — a gap also present in Open Road Risk's current Stage 2.

---

## 5. Spatial Unit of Analysis

- Unit: road segment (OS Vector OpenMap Local Roads and Tunnels layer)
- Segment length or segmentation rule: OS-defined segments, not fixed-length. Length range 0.1 m to 2597 m, mean 118 m (SD 178 m). (p.1155–1156)
- How crashes are assigned to the network: crashes projected to nearest point on the road network; events farther than 10 m from the nearest segment excluded (p.1157)
- Treatment of junctions/intersections: not explicitly modelled as separate units. Segment adjacency (shared boundary points) defines the spatial neighbourhood; overpasses/bridges correctly handled — segments that cross without sharing a boundary point are not treated as neighbours (p.1156, Figure 3)
- Spatial aggregation risks: MAUP explicitly investigated. Network contracted from 3661 to ~2700 segments using redundant-vertex removal algorithm; fixed effects found robust; spatial hyperparameters (σ²_φ1, σ²_φ2) more sensitive to segmentation (p.1170–1172). Authors conclude network-lattice MAUP is less severe than administrative-zone MAUP.
- Evidence quote or page reference: "Our results tell a somewhat different story. The statistical analysis is found quite robust to MAUP when carried out on a network lattice" (p.1171)
- Relevance to OS Open Roads link-based pipeline: high — Open Road Risk uses OS Open Roads segments as its spatial unit, which is the same data family (different OS product but same fundamental structure). The adjacency/neighbourhood construction approach and the MAUP robustness finding are directly relevant.

---

## 6. Temporal Unit of Analysis

- Years covered: 2011–2018 (8 years)
- Temporal resolution: yearly data available but collapsed to 8-year aggregate for the main models due to severe crash sparsity
- Whether seasonality or time-of-day is modelled: no — not modelled
- Whether before-after or panel structure is used: no — cross-sectional aggregate only. Authors explicitly note spatiotemporal extension as future work and flag that >95% of segment-year cells have zero fatal/serious crashes (p.1173)
- Evidence quote or page reference: "A space-time representation" referenced in supplementary material; "We decided to ignore the temporal dimension since severe crashes counts present an extreme sparsity" (p.1157)
- Relevance to WebTRIS-style time profiles: low — the paper does not model time-of-day or seasonal variation. This is a gap the paper itself acknowledges. Open Road Risk's Stage 1b WebTRIS profiles are not supported or challenged by this paper's methodology.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Segment length | OS road network geometry | Direct from OS segment geometry | Required for exposure offset (length × flow); longer segments have higher expected counts | Already present — used in exposure offset |
| Estimated traffic flow (commuting proxy) | 2011 Census MSOA-level OD flows | Shortest-path routing assigns flow-through to each MSOA; MSOA value overlaid onto segments by spatial intersection | Used as traffic exposure denominator in offset | Partially — mathematical structure transferable; Open Road Risk uses AADF-derived AADT which is more direct. Compare implementation rather than adopt. |
| Road type dummy (Motorway / Primary / A Road) | OS road classification | Categorical variable derived from OS attribute | Fixed effect; Primary and Motorway found safer than A roads for severe crashes | Already present as road classification feature — compare coefficient direction |
| Dual carriageway dummy | OS road attribute | Binary flag from OS data | Significant negative association with slight crashes | Already present or straightforward to derive from OS Open Roads — check presence |
| Population density | 2011 Census LSOA data | LSOA-level ratio of residents to area (m²); spatially overlaid onto segments | Significant positive predictor of both slight and severe crashes | Already present as candidate feature — validate and document |
| Employment rate | 2011 Census LSOA data | Ratio of employed 16–64 to total 16–64 population; LSOA overlaid onto segments | Tested as proxy for local economic activity; found not significant | Low priority — not significant in this study; note for documentation |
| Edge betweenness centrality | OS road network graph | Number of shortest paths traversing each segment (graph measure) | Used as proxy for VMT; found not significant (95% CI included zero) | Already present in Open Road Risk — note non-significance result here; diagnostic interest |
| Segment adjacency matrix (W) | OS road network graph | Dual representation: vertices = segments, edges = shared boundary points | Defines spatial neighbourhood for CAR random effects | Not applicable to current XGBoost/GLM setup; relevant if Bayesian spatial model piloted |

---

## 8. Model Architecture

- Algorithms/models used: family of 6 Bayesian hierarchical Poisson models (A–F) with ICAR/PCAR spatially structured random effects and unstructured random effects; bivariate (two severity levels modelled jointly). Model G (separate ρ per level) also tested but not preferred.
- Baseline model: (A) IIMCAR spatial effects + independent Gaussian unstructured effects (= two independent ICAR models); (B) IPMCAR + independent Gaussian unstructured effects
- Final/preferred model: Model (F) — PMCAR spatial effects + correlated bivariate Gaussian unstructured effects (correlated across both severity levels)
- Loss function or likelihood: Poisson likelihood; Y_ij | λ_ij ~ Poisson(E_i × λ_ij) where log(λ_ij) = β_0j + Σ β_mj X_ijm + θ_ij + φ_ij
- Offset/exposure term: log(E_i) = log(segment_length × traffic_flow), entered as fixed offset
- Spatial autocorrelation handling: IMCAR (intrinsic multivariate CAR) or PMCAR (proper multivariate CAR) priors on spatially structured random effects; adjacency defined by shared boundary points on the road network graph. PMCAR includes parameter ρ controlling spatial autocorrelation strength.
- Temporal dependence handling: not modelled (8-year aggregate)
- Interpretability method: posterior means and credible intervals for fixed effects; posterior maps of crash rates per segment; balanced accuracy evaluated via simulated posterior predictive samples
- Estimation: INLA (R-INLA package) with simplified Laplace approximation; ~30–45 minutes per model on 6-core virtual machine with 32 GB RAM, for 3661 segments
- Evidence quote or page reference: Section 3 (pp.1158–1162); "It took approximately 30–45 min to estimate each model using a virtual machine with an Intel Xeon E5-2690 v3 processor, six cores, and 32GB of RAM" (p.1162)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model comparison | DIC | 14103.44 | Model (F) — best | Lower is better; (F) outperforms all others | Table 4, p.1166 |
| Model comparison | WAIC | 14086.46 | Model (F) — best | Lower is better; (F) outperforms all others | Table 4, p.1166 |
| Model comparison | DIC | 14462.56 | Model (A) — worst | Baseline, no cross-severity correlation | Table 4, p.1166 |
| Classification / posterior predictive | Balanced accuracy (severe crashes) | ~0.675 | Model (F), 0.975-quantile threshold | Average of sensitivity and specificity on zero vs ≥1 binarisation | Table 4 / Figure 6a, pp.1166–1168 |
| Classification / posterior predictive | Balanced accuracy (slight crashes) | ~0.720 | Model (F), median threshold | Average of sensitivity and specificity | Table 4 / Figure 6b, pp.1166–1168 |
| Hyperparameter estimate | Unstructured cross-severity correlation ρ_θ | ~0.40 | Models (E) and (F) | Mild-to-moderate positive correlation between severe and slight unstructured effects at same segment | Table 3, p.1165 |
| Hyperparameter estimate | Spatial cross-severity correlation ρ_φ | ~0.83–0.90 | Models (C)–(F) | Strong positive spatial correlation between severity levels | Table 3, p.1165 |
| Fixed effect | Motorway vs A Road (severe crashes) | ~−0.76 to −0.85 (posterior mean) | Models (A)–(F) | Motorways significantly less prone to severe crashes than A roads | Table 2, p.1164 |
| Fixed effect | Primary Road vs A Road (severe crashes) | ~0.33–0.52 (posterior mean) | Models (A)–(F) | Primary roads less safe than expected vs A roads for severe (positive but with SD overlap) | Table 2, p.1164 |
| Fixed effect | Population density (slight crashes) | ~0.24–0.27 (posterior mean) | Models (A)–(F) | Significant positive association | Table 2, p.1164 |
| Fixed effect | Edge betweenness centrality | ~0 (95% CI includes 0) | All models, both severities | Not significant; VMT proxy does not predict crash rate after other adjustment | Table 2, p.1164 |
| Fixed effect | Dual carriageway (slight crashes) | ~−0.30 to −0.32 (posterior mean) | All models | Significant negative: dual carriageways safer for slight crashes | Table 2, p.1164 |
| Fixed effect | Employment rate | ~0 (95% CI includes 0) | All models | Not significant | Table 2, p.1164 |
| MAUP sensitivity | Fixed effects direction/significance | Unchanged | Model (F) contracted network (~2700 segments) | Robust to network contraction | Tables 6–7, p.1170–1171 |

**Metric qualification:**

- DIC and WAIC are in-sample model comparison criteria penalised for complexity. They are **not** external predictive validation metrics and do not demonstrate out-of-sample predictive accuracy.
- Balanced accuracy is computed as a **posterior predictive diagnostic on the same dataset used for fitting** (in-sample posterior predictive diagnostic). The model was not held out, spatially split, or temporally split. This assesses posterior fit adequacy, not generalisation.
- No out-of-sample, cross-validated, spatially held-out, or temporally held-out predictive metrics are reported.
- These metrics are therefore **not evidence of predictive generalisation**. They are in-sample goodness-of-fit and diagnostic adequacy measures.
- Most relevant metric for Open Road Risk: the balanced accuracy procedure (binarise zero vs ≥1, simulate from posterior) is conceptually useful as a **diagnostic** for sparse count models, but cannot be directly borrowed as a validation result.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Poisson likelihood inherently handles zero counts. Temporal dimension collapsed to 8-year aggregate to reduce sparsity (>80% of segments have zero severe crashes in any given year). Bivariate joint modelling of severe and slight allows borrowing of strength from less sparse slight crashes to improve severe crash estimates.
- Use of Poisson / negative binomial / zero-inflated models: Poisson only. No negative binomial, no zero-inflated, no hurdle model.
- Zero-heavy counts handled using: 8-year aggregation to reduce zeros + bivariate joint Bayesian model borrowing strength across severity levels + posterior predictive simulation with 0.975-quantile threshold (rather than posterior mean) for binary classification of sparse severe crashes
- Whether high-risk locations are evaluated separately: posterior crash rate maps produced per segment; sensitivity analysis stratified by road type and carriageway type, finding no systematic differences in balanced accuracy (p.1169)
- Evidence quote or page reference: "the severe class is very sparse in the data set at hand, hence modelling both types of accidents simultaneously allows to borrow strength from the existing correlations" (p.1152); "more than 80% of zero counts during 2011–2018" (p.1157)
- Practical relevance: The aggregation-to-reduce-sparsity approach is directly applicable to Open Road Risk's situation (~1–2% of link-years with any collision). However, Open Road Risk uses a panel structure (link × year) rather than a temporal aggregate, which increases sparsity but preserves temporal variation. The multivariate borrowing-of-strength idea is potentially useful if a future severity-split model is piloted. The balanced accuracy procedure for binarised posterior predictive diagnostics is worth documenting.

---

## 11. Validation Strategy

- Train/test split method: none — no train/test split performed
- Spatial holdout used: no
- Temporal holdout used: no
- Grouped holdout used: no
- Cross-validation type: none
- Metrics: DIC, WAIC (model comparison only); balanced accuracy computed on full fitted dataset as posterior predictive diagnostic (in-sample)
- External validation: none
- Leakage or generalisation risks: The spatial CAR random effects use the observed crash counts from neighbouring segments during fitting. This is in-sample spatial smoothing (standard for this model class), not classic data leakage (no future data or post-event variables used). However, it means posterior rate estimates at each segment are partially informed by neighbouring segment counts — posterior predictions cannot be cleanly interpreted as predictions for unseen locations.
- Evidence quote or page reference: Section 5.1 (pp.1166–1169); DIC/WAIC in Table 4
- What I should copy: the balanced accuracy posterior predictive procedure (binarise → simulate N=5000 from posterior → compute sensitivity/specificity) is worth implementing as a diagnostic for Stage 2 sparse counts. The DIC/WAIC comparison approach could inform future Bayesian model comparison if a Bayesian component is ever piloted.
- What I should avoid: treating the paper's balanced accuracy values as out-of-sample benchmarks; they are in-sample posterior predictive diagnostics.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: A road network lattice (OS segment-level) is substantially more robust to MAUP than administrative zone aggregations. Fixed effects were stable under network contraction from 3661 to ~2700 segments; spatial hyperparameters showed some sensitivity but the crash rate maps were similar.
- Why it matters: Open Road Risk uses OS Open Roads links as its spatial unit. This provides some evidence that the choice of OS-defined segment as the spatial unit is defensible and less MAUP-sensitive than area-based alternatives.
- Evidence: Section 5.3, pp.1170–1172: "The statistical analysis is found quite robust to MAUP when carried out on a network lattice"
- Confidence: medium — single city case study; robustness found under one specific contraction algorithm. Does not test all possible network configurations.

**Finding 2:**
- Finding: In this Leeds case study, the bivariate joint modelling of slight and severe crashes substantially improved estimation of severe crashes (rare events), with balanced accuracy for severe improving from 0.631 (Model A) to 0.675 (Model F) as cross-severity correlations were added. The spatial correlation between severity levels (ρ_φ ≈ 0.83–0.90) is strong; the unstructured correlation (ρ_θ ≈ 0.40) is moderate.
- Why it matters: Open Road Risk currently models only injury collision counts without severity breakdown. This suggests that severity-split modelling with cross-level correlation could improve sparse severe-crash estimation — relevant for a future extension.
- Evidence: Table 4, p.1166; "The relevant interactions between the two severity levels allow one level to borrow strength from the other" (p.1173)
- Confidence: medium — single city dataset; the DIC/balanced accuracy improvement is shown but without external validation.

**Finding 3:**
- Finding: Edge betweenness centrality, used as a proxy for VMT (vehicle miles travelled), was not significant in any model for either severity level (95% CI always includes zero). Road type classification and population density were significant.
- Why it matters: Open Road Risk includes betweenness centrality as a candidate feature. This study provides evidence (in a Leeds major-road context) that it may not add predictive value once road classification and exposure offset are included.
- Evidence: Table 2, p.1164; "The coefficients of edge betweenness centrality measures are found close to zero for all models, and their 95% credible interval always include the value zero" (p.1163)
- Confidence: medium — specific to major-road network in Leeds; betweenness centrality definition and network scope may differ from Open Road Risk's implementation.

**Finding 4:**
- Finding: The PCAR/PMCAR model (with spatial autocorrelation parameter ρ) consistently outperformed the ICAR/IMCAR model (which forces ρ → 1) by DIC and WAIC. The posterior mean of ρ was near 1.0 in all PCAR models, which the authors note is common for this model type.
- Why it matters: If a Bayesian spatial model were ever piloted on Open Road Risk, this suggests PCAR/PMCAR is preferred over ICAR/IMCAR despite the near-unity ρ, because it provides a proper joint distribution and avoids rank-deficiency issues.
- Evidence: Table 4, p.1165–1166; Section 4.3
- Confidence: medium — consistent finding within this paper; ρ near 1 is acknowledged as a known feature of PMCAR in this data type.

**Finding 5:**
- Finding: The posterior predictive balanced accuracy procedure — binarising at zero vs ≥1, simulating N=5000 draws from the posterior, and using the 0.975-quantile (not the mean) for predicting rare severe events — is a practical diagnostic for sparse count model adequacy.
- Why it matters: Open Road Risk's Stage 2 XGBoost and GLM currently lack a formal diagnostic procedure adapted to zero-heavy collision link-year data. This paper describes a methodology worth implementing as a diagnostic.
- Evidence: Section 5.1, pp.1166–1169, Figure 6, Table 5
- Confidence: high as a methodological procedure; the specific accuracy values are not transferable (different model, different geography).

**Finding 6:**
- Finding: Motorways were found significantly less prone to severe crashes than A roads in this Leeds case study; dual carriageways significantly less prone to slight crashes. Population density positively and significantly associated with both severities. Employment rate not significant.
- Why it matters: These provide directional priors for feature engineering in Open Road Risk. Road type direction (motorway safer than A road for severe crashes) and population density direction are consistent with general road safety knowledge and support their continued inclusion as features.
- Evidence: Table 2, p.1164; Section 4.1 discussion, p.1163
- Confidence: medium for direction; specific coefficient magnitudes are not transferable (different exposure measure, different geography, different model structure).

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Exposure offset structure: log(length × flow) | Directly analogous to current Stage 2 offset; confirms mathematical approach | Segment length + traffic estimate — both already present | 3661 segments, Leeds only | High — same approach already in use | Stage 2 — validation / documentation | Low (already implemented) | None for structure; exposure quality is the real risk |
| Balanced accuracy posterior predictive diagnostic (binarise → simulate → sensitivity/specificity) | Practical sparse-count diagnostic adaptable to GLM posterior or XGBoost output | Observed collision counts + model predicted means or distributions | City-scale | High — adaptable to any predicted count model | Stage 2 — validation / diagnostic | Low–medium | Requires careful threshold selection; values not benchmarkable against paper |
| OS road network segment adjacency matrix construction via dual graph representation | Documents how to build a valid adjacency structure for spatial models; MAUP robustness finding is reassuring for OS Open Roads segmentation | OS road network geometry | 3661 segments | High (conceptual); computationally challenging at 2.17M links | Future feature / documentation | High at full scale; feasible for pilot area | Computational cost at national scale; INLA may not scale to 2.17M units |
| MAUP sensitivity test via network contraction | Useful robustness diagnostic for Open Road Risk's OS Open Roads segmentation | OS road network geometry (redundant-vertex removal) | 3661 → ~2700 segments | Medium — algorithm exists (dodgr R package); feasible on a city-scale pilot | Validation / diagnostic | Medium | Requires pilot area; not straightforward at national scale |
| Population density as crash predictor | Supported as significant in this study | Census / ONS population density — already available | City | High | Stage 2 — candidate feature (already present or straightforward) | Low | Collinearity with road type; LSOA-to-link overlay precision |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Full Bayesian hierarchical INLA estimation on entire network | Computationally prohibitive at 2.17M links; paper took 30–45 min at 3661 segments | Feasible compute budget; INLA memory constraints | 3661 segments | Low at national scale | Pilot on single police force area (e.g., one of Yorkshire's ~50k links) | High confidence in infeasibility at national scale |
| Bivariate joint severity modelling (PMCAR on both slight + severe) | Requires severity-split collision data and substantially more model complexity; current Open Road Risk does not stratify by severity | STATS19 severity fields are available but model architecture would need redesign; Bayesian machinery not currently in use | 3661 segments | Medium for a future extension; low for production change based on this single paper | Document as candidate future direction; pilot on small area | Medium |
| Census commuting OD routing as traffic exposure | Underestimates non-commute travel; Open Road Risk already has a more direct AADF-based AADT | AADF already available; Census OD routing is a worse proxy for general traffic | City | Not applicable — Open Road Risk already has better data | N/A | High |
| Betweenness centrality as VMT proxy in lieu of traffic data | Paper used it as a proxy and found it not significant; Open Road Risk already has AADT which is a better direct measure | N/A — Open Road Risk has better exposure data | — | Low — already superseded by AADT | Keep in feature set as diagnostic; do not rely on it as primary exposure proxy | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?**
  Yes — the Poisson offset approach (length × traffic flow) is directly confirmed. The paper uses an identical mathematical structure to Open Road Risk Stage 2.

- **Does it suggest better handling of AADT/AADF uncertainty?**
  Indirectly — the paper uses a clearly imperfect traffic proxy (Census commuting flows) and does not propagate that uncertainty into the model. This is the same gap present in Open Road Risk Stage 2. The paper does not offer a solution but confirms this as an acknowledged limitation of the field.

- **Does it suggest useful geometry or road-context features?**
  Road type classification, dual carriageway flag, and population density are supported as significant. Edge betweenness centrality was not significant after other adjustment in this case study — worth noting for Open Road Risk's feature evaluation.

- **Does it suggest better modelling of junctions?**
  No — junctions are not modelled separately. Segments connected at shared boundary points are treated as spatial neighbours but junction-specific risk is not isolated. The paper itself notes junctions as an unmeasured confounder absorbed into random effects (p.1172).

- **Does it suggest better treatment of severity?**
  Yes — bivariate joint modelling of severity levels, borrowing strength from slight crashes to improve severe crash estimation, is the paper's main methodological contribution. Relevant as a future direction for Open Road Risk if severity breakdown is needed.

- **Does it suggest better validation design?**
  Partially — it highlights the absence of spatial/temporal holdout as a limitation (not addressed in this paper either). The balanced accuracy posterior predictive procedure is a practical improvement over simple RMSE or R² for zero-heavy count data.

- **Does it expose a weakness in my current approach?**
  Yes — two weaknesses are implicitly highlighted:
  1. Open Road Risk Stage 2 treats all link-years independently without spatial autocorrelation structure. The paper demonstrates substantial unexplained spatial structure (large spatial random effect variances) that Open Road Risk's current GLM and XGBoost would absorb into residuals without explicitly modelling.
  2. Open Road Risk has no formal diagnostic adapted to zero-heavy count data. The balanced accuracy binarisation approach is worth implementing.

---

## 15. Repo Actionability

**Action 1:**
- Suggested repo action: Implement the balanced accuracy posterior predictive diagnostic — binarise link-year predictions at zero vs ≥1 collision, simulate N ≥ 1000 draws from the Stage 2 predicted Poisson distribution, compute sensitivity/specificity/balanced accuracy distribution, and vary the prediction quantile threshold. Compare results across road types.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Paper provides a concrete worked procedure for evaluating sparse Poisson count model adequacy on road network data; current Open Road Risk validation relies on R² / XGBoost metrics that are not well suited to zero-heavy count data (p.1166–1169)
- Evidence: Section 5.1, Table 5, Figure 6
- Effort: low–medium
- Risk if implemented badly: threshold choice may be arbitrary; results may be misleading if compared to non-equivalent benchmarks

**Action 2:**
- Suggested repo action: Document the non-significance of edge betweenness centrality in this Leeds case study as a note in the feature engineering documentation. Flag that betweenness centrality may not add predictive value once road classification and AADT are included, and plan a feature importance / ablation test in Stage 2.
- Action type: documentation note → candidate diagnostic
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Betweenness centrality found non-significant (95% CI includes zero) in all 6 model variants after road type and exposure adjustment (Table 2, p.1164)
- Evidence: Table 2, Section 4.1
- Effort: low
- Risk if implemented badly: low — this is a documentation note / diagnostic, not a deletion

**Action 3:**
- Suggested repo action: Document population density as an empirically supported crash predictor, and verify its current implementation in Stage 2 (LSOA or equivalent area-to-link overlay). Note that the paper found population density significant for both slight and severe crashes in a UK context.
- Action type: documentation note / validation of existing feature
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Population density consistently significant across all model variants for both severities (Table 2, p.1164)
- Evidence: Table 2, p.1164: "we found that population density significantly correlates to both slight and severe accidents"
- Effort: low
- Risk if implemented badly: low

**Action 4:**
- Suggested repo action: Add a note in Stage 2 documentation acknowledging the absence of spatial autocorrelation modelling as a known limitation. The paper quantifies substantial unexplained spatial structure (large σ²_φ values) on a comparable OS road network dataset. Document this as a gap and as a candidate for a future small pilot (e.g. INLA-based CAR model on a single police force area).
- Action type: documentation note → future pilot candidate
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Spatial random effects are large and significant in all model variants; ignoring spatial autocorrelation in the GLM may inflate standard errors or miss spatial patterns. Paper demonstrates feasibility at city scale (3661 segments, 30–45 min INLA runtime).
- Evidence: Tables 3, p.1165; discussion p.1172–1173
- Effort: low (documentation); high (if pilot implemented)
- Risk if implemented badly: INLA at 2.17M links would be computationally infeasible; pilot must be restricted to a small area

**Action 5:**
- Suggested repo action: Run a small MAUP sensitivity test on a pilot area (one police force, ~50k links) by applying the dodgr-style redundant-vertex contraction to OS Open Roads and comparing Stage 2 feature coefficients and risk percentile distributions before and after contraction. This would provide evidence on whether OS Open Roads segment granularity materially affects Open Road Risk results.
- Action type: small pilot / diagnostic
- Relevant stage: Validation / feature engineering
- Why the paper supports it: Paper demonstrates network-lattice MAUP robustness in Leeds but at 3661 major-road segments. Open Road Risk has 2.17M links including minor roads where segment splitting may be more arbitrary.
- Evidence: Section 5.3, pp.1170–1172
- Effort: medium
- Risk if implemented badly: Contraction may change exposure (link length changes) in ways that confound the MAUP test; care needed to re-assign collision counts and AADT estimates to contracted segments

---

## 16. Query Tags

- bayesian-hierarchical
- ICAR
- PMCAR
- multivariate-severity
- spatial-network-lattice
- exposure-offset
- poisson-count
- zero-heavy-counts
- OS-road-network
- STATS19
- MAUP
- network-contraction-robustness
- balanced-accuracy-diagnostic
- betweenness-centrality
- population-density
- severity-joint-model
- INLA
- UK-transferable
- segment-level
- Leeds-case-study

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper:
  - Full model run times and memory usage for larger-than-Leeds networks are not stated
  - The exact algorithm for traffic flow routing (shortest path implementation details) is only partially described
  - Supplementary material (pseudo-code for balanced accuracy, sensitivity analysis tables, contracted-network rate maps) was not accessible; results are described from the main text only
  - Specific LSOA-to-segment overlay methodology for socio-economic covariates is briefly described but not fully detailed
- Parts of the paper that need manual checking:
  - Table 2 fixed effects: the dual-carriageway coefficient sign for severe crashes is ambiguous across models (some positive, some negative with SD overlap) — manual check against original PDF recommended
  - The MAUP contracted-network rate maps are in supplementary material and cannot be confirmed here
  - Model G (separate ρ per severity level) is described as not improving on Model F but results are only in supplementary material
- Any likely ambiguity or risk of misinterpretation:
  - The balanced accuracy values (0.675, 0.720) are in-sample posterior predictive diagnostics, not predictive accuracy on held-out data. There is a real risk of misreading Table 4 as reporting out-of-sample performance.
  - The traffic flow variable is commuting OD flows, not observed vehicle counts — this is materially different from AADF/AADT and should not be equated with Open Road Risk's traffic data even though the mathematical exposure structure is identical.
  - The paper studies major roads only (motorways, primary, A roads — 3661 of ~50,000 total OS segments). Open Road Risk covers all road types. Feature effect directions (e.g. motorway safer than A road) may not hold on the full network including unclassified and minor roads.