# Paper Extraction: Ziakopoulos & Yannis — A review of spatial approaches in road safety

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-10
- Source PDF filename: A_review_of_spatial_approaches_in_road_safety.pdf
- Suggested Markdown filename: paper-extraction-ziakopoulos-yannis-2020-spatial-review.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat (claude.ai)
- Input type: PDF upload (full text available in context window)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: All 43 pages including all four summary tables were available in context. The paper contains no downloadable data. The tables reference studies but do not include raw quantitative results — these are study-design summaries only.

---

## 1. Citation

- Title: A review of spatial approaches in road safety
- Authors: Apostolos Ziakopoulos, George Yannis
- Year: Not explicitly stated in the provided text; the tables reference studies up to 2019 and the paper discusses WHO 2018 data, suggesting publication circa 2020. **Year not explicitly stated in the document.**
- DOI or URL, if present: Not stated
- Country / region studied: International review (studies from USA, UK, Canada, Belgium, China, Iran, Turkey, Brazil, Australia, Costa Rica, Hong Kong, South Korea, Italy, Nigeria, New Zealand, Czech Republic, and others)
- Study setting: mixed (urban, rural, motorway, zonal, regional — covers all settings across reviewed studies)

---

## 2. Core Objective

- One-sentence description: Critically reviews how researchers handle the spatial dimension in road safety studies, covering areal unit selection, modelling approaches, boundary/MAUP problems, spatial proximity structures, and vulnerable road user analyses.
- Main purpose: descriptive analysis / methodological review
- Evidence quote or page reference: "The aim of the present research is to critically review the existing literature on different spatial approaches through which researchers handle the dimension of space in its various aspects in their studies and analyses." (Abstract, p.1)

---

## 3. Response Variable

- Target variable: Not a primary modelling paper; reviews studies that use crash counts, crash rates, injury severity rates, casualty rates, and spatial distributions thereof.
- Collision type: injury / fatal / serious / slight / property-damage-only — varies across reviewed studies; all crash types appear in the tables.
- Severity handling: Varies by reviewed study. Some reviewed studies combine severity levels; multivariate models handling multiple severity levels simultaneously are noted as a trend. The paper specifically identifies joint frequency-and-severity modelling as an underexplored future direction.
- Count, binary, rate, risk score, severity class, or other: Varies by reviewed study.
- Time window used for outcomes: Varies by reviewed study; not stated for the review itself.
- Evidence quote or page reference: Tables 1–4 document the dependent variables used across reviewed studies; see "Crash count/frequency", "Crash rate", "Injury Severity", "Casualty rate" columns.

---

## 4. Exposure Handling

- Exposure variable used, if any: This is a review paper, not a primary model. Across reviewed studies, exposure variables include AADT/traffic volume, vehicle distance travelled (VMT/VDT), number of trips/OD counts, road length, and population counts (for pedestrian/VRU analyses).
- Traffic count source: Varies across reviewed studies; AADT and VMT are the most commonly cited. No uniform source.
- Whether exposure is modelled, observed, assumed, or ignored: The review notes that "Several studies include exposure parameters in order to establish a common baseline for crash risk comparisons between models." (p.23) Exposure is observed in some studies and ignored in others.
- Treatment of missing or sparse traffic counts: Not addressed explicitly. The review does not discuss imputation or handling of sparse AADT.
- Whether offset terms, rates, denominators, or normalisation are used: Not stated for individual reviewed studies in the text. Tables show "Traffic volume" and "Vehicle distance traveled" as binary indicators of whether these were included as independent variables, not whether they were used as offsets.
- Evidence quote or page reference: "When exposure parameters such as road length, AADT and vehicle distance travelled are examined, they are found to increase crash risk overall, as expected, however there are particular cases where these results might not apply or even be reversed." (p.23)
- Transferability to my AADF/WebTRIS setup: mixed
- Notes: The review confirms that AADT and road length are standard exposure variables in segment-level models, which is consistent with the Open Road Risk offset structure. However, the review does not discuss AADT estimation uncertainty, sparse count handling, or exposure offsets specifically — these are not addressed as methodological concerns in the reviewed literature. The mathematical exposure structure used in Open Road Risk (log-offset) is broadly consistent with what is implied by reviewed Poisson/NB models, but this paper provides no direct evidence on how to handle sparse or estimated AADT.

---

## 5. Spatial Unit of Analysis

- Unit: Review covers road segment / intersection / grid cell / zone (TAZ, CT, BG, ZIP, ward, enumeration district) / regional (county, state, metropolitan area) / conditional (pre-crash condition, lixel-based network KDE)
- Segment length or segmentation rule: Varies. Reviewed segment studies use OS-style links, highway homogeneous segments, fixed-length lixels (for network KDE), or variable-length segments defined by road infrastructure. Thomas (1996) examined the effect of segment length on crash count distributions (p.4).
- How crashes are assigned to the network: Link-based crash mapping algorithms noted as a conditional approach (p.8): "link-based approaches that utilize crash-mapping algorithms and assign crashes to each road segment." The paper notes this "can be problematic in providing interpretable results."
- Treatment of junctions/intersections: Explicit separation of segment and intersection analysis is a core theme. Joint simultaneous modelling of intersections and segments (Zeng & Huang 2014; Alarifi et al. 2017) is highlighted as an advance. "Spatial correlations between intersections and their connected segments were more significant than those found between intersections or between segments only." (p.5)
- Spatial aggregation risks: MAUP is discussed at length (pp.10–11). Larger zones tend to produce higher predictive accuracy in some studies but mask micro-level variation. The paper notes that "the impact of MAUP was significant on parameter estimates, model assessment and hotspot identification." (p.11, citing Zhai et al. 2019a)
- Evidence quote or page reference: Section 2 (pp.3–12) covers all spatial unit types and associated issues.
- Relevance to OS Open Roads link-based pipeline: High conceptual relevance. The paper confirms that link/segment-level analysis is a legitimate and well-studied spatial unit for road safety modelling, and highlights that junction treatment is a known unresolved issue at this level. The OS Open Roads link structure (which does not separate out junctions explicitly) is flagged implicitly by the review's discussion of junction-segment spatial correlation.

---

## 6. Temporal Unit of Analysis

- Years covered: Varies; reviewed studies span from 1996 to 2019.
- Temporal resolution: Mostly annual or multi-year aggregated in the reviewed studies. Daily resolution appears in Ma et al. (2017) for highway segments. Hourly/peak examined in Soltani & Askari (2017) at TAZ level.
- Whether seasonality or time-of-day is modelled: Soltani & Askari (2017) found hotspots vary considerably across times of day (p.13). Weather effects on pedestrian crashes examined in Zhai et al. (2019b). These are minority approaches in the reviewed literature.
- Whether before-after or panel structure is used: Before-after studies mentioned in an EB context (Lee et al. 2017b). Panel (multi-year) structures exist in some reviewed studies but are not the dominant design.
- Evidence quote or page reference: "Crashes face the typical issues of all point data: spatial dependence and spatial heterogeneity." (p.2); temporal autocorrelation noted as a complement to spatial autocorrelation (p.15).
- Relevance to WebTRIS-style time profiles: The review provides weak indirect support. Soltani & Askari (2017) finding that hotspots vary by time of day is relevant background context. The review does not address within-day traffic profiling as a modelling component, and WebTRIS-style time-zone features are not discussed. No direct support for or against the Stage 1b approach.

---

## 7. Engineered Features

This is a review paper. The table below lists feature categories that appear frequently across reviewed studies, based on Table 1–4 column headers and the narrative text. Only features with explicit mention in the paper are included.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Traffic volume / AADT | Traffic counts (source varies) | Used directly as covariate or exposure | Consistently significant across reviewed studies; standard exposure proxy | Already present / compare implementation |
| Vehicle distance travelled (VMT/VDT) | AADT × road length | Product of AADT and segment length | Used as exposure denominator in many reviewed studies | Already present as offset component / compare |
| Road length / segment length | Road network geometry | Direct measurement or derived from GIS | Significant predictor and exposure component; Thomas (1996) showed crash counts follow Poisson at shorter segment lengths | Already present / compare |
| Speed limit | Road network data | Categorical or continuous covariate | Used in many reviewed studies; noted as a network characteristic rather than a measured traffic parameter in recent studies (p.24) | Already present (OSM-derived) / compare coverage |
| Lane number | Road network / survey data | Count variable | Significant in several reviewed studies at intersection and segment level | Candidate feature; sparse in OSM |
| Intersection density / number | Road network GIS | Count or density within a zone or corridor | Significant at multiple spatial scales; joint modelling of intersections and segments recommended | Candidate feature; derivable from OS Open Roads topology |
| Population density | Census data | Density per spatial unit | Standard demographic covariate, particularly for VRU crash models | Candidate feature / already present indirectly via IMD |
| Curvature | Road geometry | Derived from segment shape | Listed in reviewed studies (Table 1 columns); noted as receiving less attention in recent years due to data gaps (p.24) | Already present / document that coverage is partial |
| Gradient | Terrain data | Derived from DEM | Listed in Table 1 column header; noted as increasingly omitted due to data availability issues (p.24); gradient column was blank in Table 2 and was removed | Already present (OS Terrain 50) / worth noting in documentation |
| Land use factors | Land use datasets | Various categorical/continuous | Significant in many TAZ-level studies | Candidate feature; not currently in pipeline |
| Employment density | Census / employment data | Density per zone | Significant in some pedestrian crash models | Candidate feature |
| Spatial autocorrelation term (CAR/SAR prior) | Model structure | Neighbouring unit specification | Consistently improves model fit across reviewed studies; "pooling strength" from neighbours | Not currently in pipeline; computationally significant decision |
| Road network connectivity / space syntax | Road network GIS | Graph-theoretic measures | Guo et al. (2017) found global integration (space syntax) positively related to pedestrian-vehicle crashes; betweenness/centrality are analogues | Already present (betweenness, degree centrality) / compare |

---

## 8. Model Architecture

- Algorithms/models used (across reviewed studies): Poisson GLM, Negative Binomial GLM, Poisson Lognormal (multivariate, hierarchical, Bayesian), CAR/SAR spatial priors, Full Bayes hierarchical models, Empirical Bayes, GWR/GWNBR, S-GWR, Random Forest, SVM, CNN + LSTM, Kernel Density Estimation (planar and network), zero-inflated NB (in specific VRU studies), hurdle models (specific studies).
- Baseline model: Negative Binomial or Poisson regression used as baseline across most reviewed studies.
- Final/preferred model: No single preferred model; Bayesian hierarchical models with CAR spatial priors are the dominant high-performance approach in reviewed literature. Machine learning methods (RF, CNN) are noted as competitive for prediction but weak on interpretation. GWR/GWNBR are noted as local but non-transferable.
- Loss function or likelihood, if stated: Varies; Poisson and negative binomial likelihoods most common. Not stated at review level.
- Offset/exposure term, if used: Used in Poisson-family models across reviewed studies; exposure variables include road length, AADT, VMT. Not consistently described as a log-offset at this review level of abstraction.
- Spatial autocorrelation handling: CAR (conditional autoregressive) and SAR (simultaneous autoregressive) priors are the dominant methods. CAR is more common. Multiple membership models, joint prior distributions, and spatially varying coefficients are advanced variants. "CAR models have been found to perform better than Poisson models and Multiple Membership models, by explaining a high degree of spatial heterogeneity." (p.15)
- Temporal dependence handling: Temporal autocorrelation addressed in some reviewed studies (e.g. Wang & Abdel-Aty 2006). Spatiotemporal Bayesian models (Ma et al. 2017, Li et al. 2019) represent the frontier. Not a primary focus of the review.
- Interpretability method: GLMs and GWR noted as more interpretable. ML methods (SVM, CNN) noted as difficult to interpret. SHAP or equivalent not mentioned.
- Evidence quote or page reference: Section 3 (pp.13–20) covers all modelling approaches. "Functional models appear to be more straightforward in their interpretation and assessment of results." (p.23)

---

## 9. Reported Metrics / Quantitative Results

This is a review paper. It does not report primary quantitative results or model metrics. Individual reviewed studies report their own metrics (DIC, AIC, MAD, prediction accuracy, Moran's I, etc.) but these are described qualitatively rather than tabulated in this review paper.

Specific quantitative claims from the narrative:

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Hotspot identification accuracy | Classification accuracy | ~80% | Random Forest, TAZ-level (Jiang et al. 2016) | RF models can identify hot-zones at ~80% accuracy using big data | p.19 |
| Spatial effective range | Distance | ~168m | Joint prior Bayesian model (Aguero-Valverde 2014) | Spatial correlation has a limited effective range; beyond ~168m, no significant residual correlation in that case study | p.18 |
| MAUP impact | Qualitative | Significant | Zhai et al. 2019a, four zonal configurations | Zonal boundary choice significantly affects parameter estimates, model assessment, and hotspot ID | p.11 |
| CNN vs econometric | Predictive accuracy comparison | CNN better at daily level; econometric better at weekly level | Bao et al. 2019 | Neither ML nor econometric approaches are universally superior across temporal resolutions | p.19–20 |

**Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated?**
Not stated at the review level. The review does not critically evaluate the validation methods of the studies it cites; it summarises findings as reported. Most cited model-comparison metrics (DIC, AIC) in the underlying studies are in-sample fit statistics.

**Do these metrics test predictive generalisation?**
The review acknowledges limited transferability of spatial models as a recurrent theme but does not provide meta-analytic validation evidence. The ~80% hotspot accuracy figure from Jiang et al. (2016) is not described with sufficient validation detail to assess whether it reflects held-out performance.

**Are any metrics likely to be optimistic for real-world deployment?**
Likely yes for many cited results, given the review's own observation that "results of spatial studies have also been reported to have limited transferability." (p.23)

**Which metric, if any, is most relevant to Open Road Risk?**
The ~168m effective spatial range finding (Aguero-Valverde 2014) is potentially relevant for understanding spatial autocorrelation at OS Open Roads link scale, but it comes from a specific US rural road case study and should not be generalised.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Not directly addressed as a topic in the review. Zero-heavy count data is an inherent property of crash data at fine spatial resolutions, but the review does not discuss it as a methodological challenge. This is a notable gap relative to the Open Road Risk context.
- Use of specific models: Zero-inflated negative binomial models mentioned explicitly only in Cai et al. (2016) for pedestrian/bicycle crashes at TAZ level (p.17): "The zero-inflated negative binomial models were found to have the best fit for pedestrian and bicycle crashes." Hurdle models mentioned in Table 2 for Cai et al. (2016). These are described, not recommended broadly.
- Whether high-risk locations are evaluated separately: Hotspot identification is a recurring topic but not through class-imbalance methods. Prioritisation through EB or FB methods, KDE, and Moran's I are standard approaches.
- Evidence quote or page reference: p.17 for zero-inflated NB mention. General zero-heavy handling is not addressed.
- Practical relevance to my sparse collision link-year dataset: Limited direct guidance from this paper. The review does not discuss sparse event rates at link-year resolution (~1–2% non-zero). This is a known gap — the review focuses on aggregated spatial models where zero-inflation at fine resolution is less prominent.

---

## 11. Validation Strategy

- Train/test split method: Not stated at review level. Individual reviewed studies vary.
- Spatial holdout used? Not stated at review level. GWR/S-GWR noted as non-transferable spatially (p.14–15), implying spatial holdouts exist in some underlying studies, but the review does not track this systematically.
- Temporal holdout used? Not stated at review level.
- Grouped holdout used? Not stated at review level.
- Cross-validation type: Not stated at review level.
- Metrics: DIC, AIC, MAD mentioned in specific reviewed studies. No meta-analysis of validation metrics.
- External validation: Lee et al. (2019b) examined cross-country transferability of macro-level SPFs between US and Italy; found limited transferability for most model types (p.8). This is the closest the review comes to discussing external validation.
- Leakage or generalisation risks: The review repeatedly notes limited spatial transferability of spatial models (GWR, S-GWR, CAR priors). This is a generalisation concern rather than a classic data leakage problem. The review does not discuss temporal leakage or within-site leakage.
- Evidence quote or page reference: "The authors comment that GWNBR models are highly localized, thus the transferability of their predictions is limited and need to be reapplied to each area." (p.14); "results of spatial studies have also been reported to have limited transferability." (p.23)
- What I should copy or avoid: The review implicitly supports grouped/spatial validation by revealing how often spatial models fail to transfer. For Open Road Risk, this suggests that grouped-by-road-link validation (already in place for Stage 2) is important, and that spatial holdout validation would be a meaningful future diagnostic.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: Spatial correlation between intersections and their adjacent segments is consistently more significant than within-segment or within-intersection spatial correlation alone. Joint modelling of intersections and segments improves model performance.
- Why it matters: Open Road Risk uses OS Open Roads links, which do not distinguish junction nodes from mid-segment links. This finding suggests that junction-adjacent links may have systematically different crash risk properties that are not captured by current features.
- Evidence quote or page reference: "The spatial correlations between intersections and their connected segments were more significant than those found between intersections or between segments only, presumably due to common unobserved parameters such as speed." (p.5, citing Zeng & Huang 2014)
- Confidence: medium (based on specific US urban case studies; generalisation uncertain)

**Finding 2:**
- Finding: AADT sensitivity in spatial models is flagged as a matter for further investigation. The effect of AADT is not uniformly positive and can be reversed in some configurations.
- Why it matters: This is relevant to how AADT is used in Stage 2. If AADT sensitivity varies spatially (e.g. between motorway and minor road contexts), a single global AADT coefficient in a Poisson GLM may be misspecified. The XGBoost model may handle this implicitly.
- Evidence quote or page reference: "The authors suggest that the sensitivity of AADT in the models is a matter for further investigation." (p.12, citing Alarifi et al. 2018); "AADT and vehicle distance travelled are found to increase crash risk overall, as expected, however there are particular cases where these results might not apply or even be reversed." (p.23)
- Confidence: medium (observation from specific studies; mechanism not explained)

**Finding 3:**
- Finding: Geometric features (gradient, curvature, lane width) are increasingly omitted from recent spatial road safety studies due to data availability issues, not because they are unimportant.
- Why it matters: Open Road Risk has gradient (OS Terrain 50) and curvature already in the pipeline but with uncertain coverage quality. This finding supports documenting their inclusion and limitations explicitly, rather than treating their absence from recent literature as evidence of irrelevance.
- Evidence quote or page reference: "certain geometrical features seem to be used less frequently, such as road gradient, curvature and lane width... This decline in use can be attributed to missing data for many study areas, or to difficulty in data acquisition." (p.24)
- Confidence: high (explicit authorial observation across reviewed studies)

**Finding 4:**
- Finding: Hotspot locations are sensitive to which variables are included in models, which user types are considered, and which time periods are examined. "It can be reasonably surmised that many elements that are introduced to an analysis radically change the hotspot map." (p.23)
- Why it matters: Open Road Risk's production risk percentile should be interpreted with caution. Hotspot rankings from XGBoost will shift if features change, if year ranges change, or if severity weighting is introduced. This supports framing the output as exploratory and diagnostically useful rather than definitive.
- Evidence quote or page reference: p.23 (Section 5.1 Discussion)
- Confidence: high (well-supported across multiple reviewed studies)

**Finding 5:**
- Finding: Macro-level (zonal) models and micro-level (segment/intersection) models identify different significant variables and serve different purposes. Integrating both levels improves model performance but adds complexity.
- Why it matters: Open Road Risk is a micro-level pipeline. The finding suggests that adding macro-level contextual variables (e.g. TAZ-level VMT, population density at ward level) as features in Stage 2 may improve model performance. IMD deprivation decile and population density are already candidate features, which is consistent with this direction.
- Evidence quote or page reference: "micro-level modelling provided more informative and precise insights for directly improving road safety, while macro-level modelling allows for incorporating safety improvements in long term transportation planning." (p.9–10, citing Huang et al. 2016)
- Confidence: medium (multi-study finding but mostly US context)

**Finding 6:**
- Finding: Spatial autocorrelation in crash frequency models has a limited effective range (Aguero-Valverde 2014 estimated ~168m in one case study), beyond which neighbouring correlations are negligible.
- Why it matters: At OS Open Roads link level, many links are shorter than 168m. This implies that neighbouring-link effects may be relevant for a significant proportion of the network. The current Stage 2 model does not account for spatial autocorrelation between adjacent links. This is a known diagnostic gap.
- Evidence quote or page reference: "the effective range was determined (at about 168m)" (p.18, citing Aguero-Valverde 2014). Caution: this is a single US rural case study result.
- Confidence: low (single case study; not verified for UK mixed urban-rural network at OS Open Roads scale)

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Spatial autocorrelation diagnostic (Moran's I / Getis-Ord Gi*) on Stage 2 GLM residuals | Quantify whether residuals are spatially clustered, supporting or undermining independence assumption | GLM residuals + link geometry (already available) | Various; well-established at segment and zone levels | High — standard GIS tools; computationally feasible at link level with spatial sampling | Validation / diagnostic | Low | Interpreting results correctly; identifying appropriate neighbourhood definition for 2.1M links |
| Junction indicator feature (binary: is this link a junction connector?) | Capture documented junction-segment spatial correlation effect | OS Open Roads topology (already available) | Segment/intersection studies, US mostly | High — derivable from existing network data | Stage 2 candidate feature | Low–Medium | Junction definition ambiguity in OS Open Roads; risk of noise if definition is imprecise |
| Network-based spatial proximity definition (route adjacency rather than Euclidean) | Reviewed literature shows route-based proximity outperforms simple adjacency for spatial models | Road network graph (already available) | Aguero-Valverde & Jovanis 2010 | Computationally feasible for diagnostic at sample level; full-network CAR model is unrealistic at 2.1M links | Validation / future feature | Medium | Computational cost at full network scale; neighbourhood matrix size |
| Zonal macro-level features as Stage 2 inputs (ward/LSOA-level traffic density, employment density) | Multiple reviewed studies show including macro-level variables improves micro-level model performance | Census/geodemographic data (partially available via IMD) | TAZ/CT/ward level studies | High for feature addition; no architectural change needed | Stage 2 candidate feature | Low | Risk of zonal boundary mismatch (MAUP effect documented in this review) |
| Empirical Bayes shrinkage as alternative ranking | EB methods documented as improving hotspot identification over naive ranking; more reliable than naive before-after comparison | Already implemented in pipeline (noted in dossier) | Well-established across many reviewed studies | High | Stage 2 / validation — already present, needs comparison | Low (already in repo) | Comparison against XGBoost ranking not yet completed; this paper supports documenting the EB approach |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Bayesian CAR / SAR spatial random effects in production Stage 2 model | Computationally infeasible at 2.1M links; MCMC-based Bayesian spatial models require neighbourhood matrices and burn-in iterations that are prohibitive at this scale | Neighbourhood matrix for 2.1M links; MCMC compute infrastructure | Reviewed studies max out at thousands of links or TAZs | Low at production scale; medium for a sampled diagnostic pilot | Apply to a small geographic pilot (e.g. single county) as a diagnostic, not production | High |
| Geographically Weighted Regression / GWNBR | Explicitly noted as non-transferable spatially (requires refit for each area); also computationally demanding at network scale | Full covariate matrix for all links | TAZ/segment scale studies | Low — requires refitting per area; interpretability limited | Not recommended even as diagnostic given explicit transferability limitation stated in review | High |
| CNN-based spatiotemporal crash prediction | Requires high-resolution grid data with 100×100 cell resolution and 17 data layers; custom data collection framework needed | High-resolution grid data not available; custom labelling | City-block grid scale | Low | Not worth pursuing; the data requirements are not compatible with open-data pipeline | High |
| Space syntax for road network structure | Computationally intensive; results are specific to urban grid configurations; paper finding limited to Hong Kong TAZ level | Space syntax software or implementation | TAZ level, Hong Kong urban | Low at OS Open Roads link scale; network centrality measures already cover similar ground | Betweenness and degree centrality already in pipeline; document as covering this concept | Medium |
| Joint simultaneous segment-intersection modelling (Zeng & Huang 2014 style) | Requires explicit separation of junction and non-junction links, and a joint likelihood linking the two; significant modelling complexity | OS Open Roads does not cleanly separate junction links from mid-segment links | Individual intersections and segments | Low for production; medium for a pilot on a small network extract | Add binary junction-proximity feature as a simpler proxy | Medium |

---

## 14. Pipeline Implications

**Does this paper support using exposure-normalised collision risk?**
Yes, indirectly. The review confirms AADT and road length are standard components of crash risk analysis at the segment level, and their product (VMT/VDT) is used as an exposure denominator in many reviewed studies. This is consistent with the Open Road Risk log-offset approach. However, the paper does not discuss log-offset structure specifically.

**Does it suggest better handling of AADT/AADF uncertainty?**
No. The review does not address AADT estimation uncertainty, sparse count handling, or AADF-to-AADT conversion. This is a gap in the reviewed literature as well as in this paper. The paper flags AADT sensitivity as needing further investigation but does not propose methods to handle it.

**Does it suggest useful geometry or road-context features?**
Yes. The review confirms that road length, lane number, speed limit, intersection density, curvature, and gradient have all been used in segment-level models. It notes gradient and curvature are declining in use due to data gaps, not irrelevance. Junction density (intersection density) is flagged as significant at multiple spatial scales. Network connectivity measures (betweenness, degree centrality — already in pipeline) are supported by the space syntax findings.

**Does it suggest better modelling of junctions?**
Yes, this is the strongest practical signal from the review. The consistent finding that junction-segment spatial correlations are significant, and that junction and segment risks differ systematically, supports adding a junction-proximity indicator feature to Stage 2, and documenting junction treatment as a known limitation.

**Does it suggest better treatment of severity?**
Weakly. The review identifies joint frequency-severity modelling and severity proportion modelling as underexplored directions. Multivariate models handling multiple severity levels are noted as better-performing. However, Open Road Risk currently treats severity as a future extension; this review provides methodological context but no specific implementation guidance.

**Does it suggest better validation design?**
Yes. The review's repeated finding that spatial models have limited transferability, and that GWR/CAR models are non-transferable spatially, supports the case for spatial holdout validation. The current grouped-by-road-link validation in Stage 2 guards against year-level leakage but not spatial holdout. A spatial holdout (held-out geographic area) would provide stronger evidence of model generalisation.

**Does it expose a weakness in my current approach?**
Yes, two weaknesses are highlighted:
1. No spatial autocorrelation handling in Stage 2. The review provides strong evidence that spatial correlation between adjacent road links is real and that ignoring it in a Poisson GLM leads to biased standard errors. The production XGBoost model does not address this either. This does not require immediate action but should be documented.
2. Junction treatment is absent. OS Open Roads links include junction-area links but they are not distinguished. The review provides consistent evidence that junction links have different crash risk mechanisms.

---

## 15. Repo Actionability

**1. Add junction-proximity indicator to Stage 2 feature set**
- Action type: candidate feature
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Consistent finding across multiple reviewed studies (Zeng & Huang 2014; Alarifi et al. 2017, 2018; Abdel-Aty & Wang 2006; Guo et al. 2010) that junction-segment spatial correlations are the strongest spatial dependency in road safety models. Current pipeline does not distinguish junction-adjacent links.
- Evidence quote or page reference: "The spatial correlations between intersections and their connected segments were more significant than those found between intersections or between segments only." (p.5)
- Effort: Low–Medium (OS Open Roads topology supports this derivation)
- Risk if implemented badly: Imprecise junction definition will add noise. Need to define clearly what constitutes a "junction link" in OS Open Roads (degree > 2 nodes, roundabout form of way, etc.) and document the definition.

**2. Document spatial autocorrelation as a known unaddressed limitation**
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Strong consensus across reviewed studies that CAR/SAR spatial priors improve model fit by "pooling strength" from neighbouring locations. Open Road Risk Stage 2 ignores spatial correlation. Full Bayesian CAR at 2.1M links is computationally infeasible, but the limitation should be documented.
- Evidence quote or page reference: "by accounting for spatial dependence and heterogeneity in the estimates, spatial analyses describe how regions affect and are affected by the road safety attributes of their neighbors." (p.2); "CAR models have been found to perform better than Poisson models." (p.15)
- Effort: Low
- Risk if implemented badly: Not applicable (documentation only).

**3. Add spatial autocorrelation diagnostic on Stage 2 GLM residuals**
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Moran's I and Getis-Ord Gi* are standard spatial autocorrelation diagnostics used across reviewed studies. If GLM residuals show significant spatial clustering, this quantifies the magnitude of the unaddressed spatial correlation and provides evidence about whether it is a material problem at Open Road Risk scale.
- Evidence quote or page reference: "For the precise examination of autocorrelation phenomena, various geo-spatial statistics have been adopted by scientists for decades, such as Moran's I, Local Moran's I, and Getis-Ord-Gi* statistics." (p.13)
- Effort: Low (spatial sampling of residuals with pysal or esda; full-network computation may need subsampling)
- Risk if implemented badly: Full-network Moran's I on 2.1M links requires a sparse weight matrix; constructing this naively will exhaust memory. Use a spatially sampled subset or a distance-band approach.

**4. Add spatial holdout validation as a diagnostic validation variant**
- Action type: diagnostic / validation
- Relevant stage: Validation
- Why the paper supports it: The review's consistent finding that spatial models have limited transferability implies that geographic holdout performance is more informative than random holdout performance. Current grouped-by-road-link CV guards against year-level leakage but not spatial generalisation. A spatial holdout (e.g. hold out one police force area) would complement existing validation.
- Evidence quote or page reference: "results of spatial studies have also been reported to have limited transferability." (p.23); Lee et al. (2019b) found models were not transferable between US counties and Italian provinces (p.8).
- Effort: Medium (requires restructuring the CV split to be geographically stratified)
- Risk if implemented badly: A single holdout area may be unrepresentative; use multiple holdout areas or k-fold spatial cross-validation. Results will likely be worse than grouped random CV, which is the honest finding.

**5. Document geometric features (gradient, curvature) as present but declining in literature due to data gaps, not irrelevance**
- Action type: documentation note
- Relevant stage: Feature engineering / documentation
- Why the paper supports it: "certain geometrical features seem to be used less frequently, such as road gradient, curvature and lane width... This decline in use can be attributed to missing data for many study areas, or to difficulty in data acquisition." (p.24). Open Road Risk already has these features; documenting this context is useful for users who might question why they are included despite sparse literature support.
- Evidence quote or page reference: p.24
- Effort: Low
- Risk if implemented badly: Not applicable (documentation only).

---

## 16. Query Tags

- spatial-autocorrelation
- CAR-prior
- Bayesian-hierarchical
- segment-level
- intersection-junction-risk
- MAUP
- boundary-problem
- exposure-offset
- AADT-covariate
- GWR-GWNBR
- empirical-bayes
- full-bayes
- network-KDE
- zero-heavy-counts
- hotspot-detection
- spatial-holdout-transferability
- junction-segment-correlation
- gradient-curvature-geometry
- macro-micro-integration
- UK-partial-relevance

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high for what the review states; medium for implications for Open Road Risk
- Important details not stated in the paper:
  - Year of publication not explicitly stated in the document text (estimated ~2020 from internal references).
  - The paper does not report primary quantitative model results; all numerical findings cited are from reviewed papers, not this paper itself.
  - Validation methods of individual reviewed studies are not critically assessed; findings are reported as stated by original authors without independent appraisal.
  - Exposure handling details (offset vs. covariate, log-offset structure) are not discussed at the review level despite being methodologically important.
  - Zero-heavy count handling at fine spatial resolution (link-year level) is not addressed.
  - AADT estimation uncertainty and sparse traffic count imputation are not discussed.
- Parts of the paper that need manual checking:
  - Tables 1–4 column assignments (filled circle vs. open circle = "considered in study design" vs. "considered as filter") are worth reviewing directly for any studies of particular interest.
  - The paper references Imprialou et al. (2016) on pre-crash conditional approaches being more transferable; this specific paper may be worth obtaining separately given its UK context and focus on crash-speed relationships.
  - Wang et al. (2009) is listed in Table 1 as a UK motorway study (M25) — a potentially relevant reference for a UK pipeline that was not discussed in the narrative.
- Any likely ambiguity or risk of misinterpretation:
  - The ~168m effective spatial range (Aguero-Valverde 2014) is from a single US rural road case study. It should not be treated as a general benchmark for OS Open Roads link spacing.
  - The ~80% hotspot classification accuracy (Jiang et al. 2016) is not described with sufficient validation context to know whether it is held-out or in-sample.
  - "Limited transferability" in the review refers primarily to spatial transferability of spatially-weighted models (GWR, CAR) to new geographic areas — not to the general robustness of Poisson/NB models or XGBoost. These concepts should not be conflated.
