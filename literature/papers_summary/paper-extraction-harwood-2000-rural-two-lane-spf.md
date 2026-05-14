# Paper Extraction: Prediction of the Expected Safety Performance of Rural Two-Lane Highways

## 0. Extraction Run Metadata

- Extraction date: 2026-05-14
- Source PDF filename: Prediction-safety-for-Two-Lane.pdf
- Suggested Markdown filename: paper-extraction-harwood-2000-rural-two-lane-spf.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: claude-sonnet-4-6
- Interface used: web chat
- Input type: PDF upload (text-extracted)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes — main report and appendices accessible; some dense appendix B tables (data ranges) were partially reviewed
- Notes on access limitations: Appendix B model development tables (tables 30–44) not fully extracted here; values in Appendix C calibration procedure not numerically extracted. Equation rendering in extracted text is imperfect for some symbols; manual PDF check recommended before quoting exact equations.

---

## 1. Citation

- Title: Prediction of the Expected Safety Performance of Rural Two-Lane Highways
- Authors: D.W. Harwood, F.M. Council, E. Hauer, W.E. Hughes, A. Vogt
- Year: 2000 (December 2000; report date FHWA-RD-99-207)
- DOI or URL, if present: Not stated. Publicly available from FHWA.
- Country / region studied: USA (Minnesota, Washington, California, Michigan — varies by base model)
- Study setting: rural two-lane highways (roadway segments and at-grade intersections)

---

## 2. Core Objective

- One-sentence description: Develop an accident prediction algorithm for rural two-lane highways combining NB regression base models, accident modification factors (AMFs), a calibration procedure, and an empirical Bayes (EB) procedure for network screening and project-level safety analysis.
- Main purpose: safety performance function development / network screening / project-level analysis
- Evidence quote or page reference: "This report documents the algorithm for predicting the safety performance of rural two-lane highways that forms the basis for the Crash Prediction Module of the Interactive Highway Safety Design Model." (Foreword, p. i)

---

## 3. Response Variable

- Target variable: total accident frequency per year per roadway segment or per at-grade intersection
- Collision type: total accidents (all crash types); separate severity distributions (fatal/injury/PDO) are provided as default tables and can be calibrated; intersection models also cover total accidents
- Severity handling: base models predict total accidents; severity distributions applied separately as proportional lookup tables (Tables 1 and 2); EB procedure applied separately to total, fatal/injury, and PDO
- Count, binary, rate, risk score, severity class, or other: count (accidents per year)
- Time window used for outcomes: 5-year accident data for Minnesota models (1985–1989); 3-year accident data for Washington and California/Michigan models (1993–1995)
- Evidence quote or page reference: Section 3, p. 18 — "This model was developed with negative binomial regression analysis for data from 619 rural two-lane highway segments in Minnesota and 712 roadway segments in Washington."

---

## 4. Exposure Handling

- Exposure variable used, if any: EXPO = exposure in million vehicle-miles of travel per year = `(ADT)(365)(L)(10^-6)`, where ADT is average daily traffic (veh/day) and L is segment length (miles)
- Traffic count source: observed AADT from FHWA Highway Safety Information System (HSIS); complete observed counts for every modelled segment — no estimated or imputed traffic
- Whether exposure is modelled, observed, assumed, or ignored: observed; complete coverage assumed
- Treatment of missing or sparse traffic counts: not discussed — complete AADT coverage assumed for all segments in HSIS dataset
- Whether offset terms, rates, denominators, or normalisation are used: EXPO enters the base model as a multiplicative factor (not a log-offset in GLM terms); the simplified base model equation (6) is `Nbr = (ADT)(L)(365)(10^-6) × exp(−0.4865)`, which is equivalent to `log(Nbr) = log(EXPO) + (−0.4865)` — i.e., a unit-elasticity log-offset at base conditions. However, in the full model, EXPO is a direct multiplier while the other covariates enter as exponential terms, so the effective elasticity on ADT within the EXPO term is constrained to 1.0 by construction in the base model. For intersections, ADT1 and ADT2 are free log covariates with estimated exponents (e.g., 0.79 and 0.49 for three-leg STOP, 0.60 and 0.61 for four-leg STOP), not forced to 1.0.
- Evidence quote or page reference: Section 3, p. 17–18 — equation (5) and equation (6); Section 3, p. 20 — equation (8) intersection base model with free ADT exponents.
- Transferability to my AADF/WebTRIS setup: mixed
- Notes:
  - The EXPO = ADT × L × 365 / 10^6 structure is mathematically identical to Open Road Risk's exposure offset (`log(AADT × link_length_km × 365 / 1e6)`). High transferability for the structural form.
  - The complete observed AADT assumption does not transfer — Open Road Risk relies on Stage 1a estimated AADT for the majority of links.
  - The free-ADT-coefficient structure of the intersection models (exponents 0.49–0.79) is directly relevant to the fixed-offset vs free-elasticity debate for the Stage 2 GLM. These are authoritative published values from a foundational SPF.
  - The segment base model uses a unit-elasticity EXPO multiplier by construction, not a freely estimated AADT exponent — this is a stronger constraint than typical NB GLM formulations and is worth noting as a design choice, not universal SPF practice.

---

## 5. Spatial Unit of Analysis

- Unit: road segment (between intersections, homogeneous characteristics); at-grade intersection (within 76 m / 250 ft of intersection centre)
- Segment length or segmentation rule: homogeneous segments with respect to lane width, shoulder width, horizontal alignment, grade, roadside hazard rating, and driveway density; variable length
- How crashes are assigned to the network: non-intersection accidents assigned to segments; intersection-related accidents (within 76 m / 250 ft) assigned to intersection model; explicit separation of segment and intersection crash accounting
- Treatment of junctions/intersections: fully separate model family from segments; intersection models cover three-leg STOP, four-leg STOP, and four-leg signalised types; intersection-related crashes within 250 ft of centre are excluded from segment model
- Spatial aggregation risks: explicit; the algorithm requires spatial separation of intersection and segment crash zones. Overlapping zones at high-density locations not discussed.
- Evidence quote or page reference: Section 3, p. 19 — "The base models for each of these intersection types predict total accident frequency per year for intersection-related accidents within 76 m (250 ft) of a particular intersection."
- Relevance to OS Open Roads link-based pipeline: OS Open Roads links are not segmented between intersections — they include the approach to intersections. The 76 m / 250 ft intersection exclusion zone used here is not replicable without explicit junction geometry. This is a structural incompatibility with a link-level model that does not separate intersection and mid-link exposure.

---

## 6. Temporal Unit of Analysis

- Years covered: Minnesota data 1985–1989 (5 years); Washington 1993–1995 (3 years); California/Michigan 1993–1995 (3 years)
- Temporal resolution: annual; model predicts accidents per year
- Whether seasonality or time-of-day is modelled: not modelled
- Whether before-after or panel structure is used: cross-sectional NB regression; not panel; years pooled within each state dataset
- Evidence quote or page reference: Section 3, p. 18 — "The database available for model development included 5 years of accident data (1985-1989) for each roadway segment in Minnesota and 3 years of accident data (1993-1995) for each roadway segment in Washington."
- Relevance to WebTRIS-style time profiles: not addressed; temporal exposure disaggregation not part of this algorithm

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| ADT / EXPO (AADT × length × 365 / 10^6) | HSIS observed AADT | Direct multiplication | Primary exposure variable in segment base model | Yes — already present as Stage 1a output; structural form identical |
| Lane width (LW) | State DOT road inventory | Field survey or inventory record | Negative coefficient (wider = safer); base = 12 ft | Low — not available nationally in UK open data |
| Shoulder width (SW) | State DOT road inventory | Field survey or inventory record | Negative coefficient (wider = safer); base = 6 ft | Low — not available nationally in UK open data |
| Roadside hazard rating (RHR) | Manual field inspection | Expert-rated integer 1–7 | Positive coefficient (higher hazard = more accidents) | Very low — requires manual audit; no national open-data equivalent |
| Driveway density (DD) | Road inventory / field survey | Driveways per mile | Positive coefficient; proxy for access conflict density | Low — not available nationally; OSM POI counts are a weak proxy |
| Horizontal curve degree of curvature (DEG) | Survey / design plans | Degrees per 100 ft; weighted by curve fraction of segment | Positive coefficient (sharper curves = more accidents) | Low — OS Terrain 50 does not give curvature; could be derived from OS Open Roads geometry at reduced accuracy |
| Grade (GR) | Survey / OS Terrain equivalent | Absolute % grade; AMF = 1.6% increase per 1% grade | Positive effect; not statistically significant in base model but included as AMF | Partial — OS Terrain 50 gives elevation; grade derivable but coarser than field survey |
| Major road ADT1 (intersections) | HSIS observed | Direct; free log covariate | Primary intersection exposure; exponent 0.60–0.79 | Low — Open Road Risk does not currently model intersections as separate units |
| Minor road ADT2 (intersections) | HSIS observed | Direct; free log covariate | Secondary intersection exposure; exponent 0.20–0.61 | Very low — minor road AADT not available nationally in UK open data |
| Intersection skew angle | Road inventory / GIS | Angle in degrees from perpendicular | Negative coefficient (skew reduces accidents in four-leg model — counterintuitive; noted as possible artefact) | Low — derivable from OS Open Roads geometry but requires intersection detection |

---

## 8. Model Architecture

- Algorithms/models used: negative binomial (NB) regression for base model development; multiplicative accident modification factors (AMFs) for geometric features beyond base condition; empirical Bayes (EB) procedure for site-specific expected accident estimation
- Baseline model: Poisson not directly discussed as alternative; NB selected throughout as appropriate for zero-heavy count data
- Final/preferred model: NB base model × calibration factor × product of AMFs, combined with EB weighting using site-specific observed history
- Loss function or likelihood, if stated: negative binomial log-likelihood (implied by NB regression); not explicitly stated in main text
- Offset/exposure term, if used: segment model — EXPO = ADT × L × 365 / 10^6 as a direct linear multiplier (unit-elasticity by construction); intersection models — free log(ADT1) and log(ADT2) with estimated exponents
- Spatial autocorrelation handling: not modelled; segments treated as independent
- Temporal dependence handling: not modelled; years pooled
- Interpretability method: coefficient signs checked; AMF values from literature review and expert judgment; calibration factor diagnostics; no CURE plots mentioned in main text (referenced to SPF Development Guide in Srinivasan 2013)
- Evidence quote or page reference: Section 3, p. 17 — equation (5); Section 3, p. 20 — equation (8) intersection model with free exponents; Table 23, p. 81 — overdispersion parameters k

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Overdispersion parameter | k (NB dispersion) | 0.31 | Roadway segments | Lower k = more overdispersion relative to Poisson; k = 0.31 is moderate | Table 23, p. 81 |
| Overdispersion parameter | k | 0.54 | Three-leg STOP intersections | Slightly less overdispersed than segments | Table 23, p. 81 |
| Overdispersion parameter | k | 0.24 | Four-leg STOP intersections | More overdispersed | Table 23, p. 81 |
| Overdispersion parameter | k | 0.11 | Four-leg signalised intersections | Highest overdispersion (small n = 49) | Table 23, p. 81 |
| Minimum EB accident frequency | 1/k | 3 (segments), 2 (3-leg), 4 (4-leg STOP), 9 (signalised) | Per model type | Minimum predicted accidents needed for reliable EB shrinkage | Table 23, p. 81 |
| ADT coefficient — segment | Free exponent on ADT | 1.0 (by construction — unit-elasticity EXPO multiplier) | Segment base model | AADT elasticity forced to 1.0 in segment model — a design choice, not an empirical finding | Equations (5) and (6), p. 17–18 |
| ADT1 coefficient — intersection | Free log coefficient | 0.79 (3-leg STOP); 0.60 (4-leg STOP, signalised) | Intersection base models | Sub-unit AADT elasticity on major road; empirically estimated | Equations (7), (9), (11), p. 20–23 |
| ADT2 coefficient — intersection | Free log coefficient | 0.49 (3-leg STOP); 0.61 (4-leg STOP); 0.20 (signalised) | Intersection base models | Sub-unit AADT elasticity on minor road; empirically estimated | Equations (7), (9), (11), p. 20–23 |
| Grade AMF | Effect per % grade | 1.6% increase in accidents per 1% grade | Roadway segment | Not statistically significant but included based on expert judgment | Section 4, Table 4, p. 40 |
| Training sample | Number of segments | 619 (Minnesota) + 712 (Washington) | Segment base model | 5 years MN + 3 years WA data | Section 3, p. 18 |
| Training sample — intersections | Number of intersections | 382 (3-leg STOP, MN); 324 (4-leg STOP, MN); 49 (signalised, CA/MI) | Intersection base models | Signalised intersection model based on very small n = 49 | Section 3, p. 19–23 |

**Validation status:** In-sample model development only. No held-out test set, no temporal validation, no spatial holdout. Calibration factors are the mechanism for local adaptation rather than a validation against held-out data. The EB procedure uses observed history from the same sites during a calibration period — this is an in-sample posterior predictive approach, not external validation.

**Most relevant metric for Open Road Risk:** The overdispersion parameters (k values) are directly useful as reference values for comparing against Open Road Risk's Stage 2 Poisson GLM residuals. If the Poisson GLM shows overdispersion comparable to these k values, NB is warranted. The sub-unit ADT elasticities on intersection approaches confirm that unit-elasticity is not an empirical finding even in foundational SPF work.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: not explicitly discussed as a modelling problem; the EB procedure is the recommended tool for sparse sites — where observed accident history is near zero, the EB procedure down-weights the observed count and relies more heavily on the model prediction
- Use of Poisson / negative binomial / zero-inflated models: NB regression throughout; zero-inflated models not mentioned
- Whether high-risk locations are evaluated separately: network screening via EB expected accident frequency is the explicit application; sites with predicted frequency below 1/k are recommended to be aggregated for EB analysis
- Evidence quote or page reference: Table 23, p. 81 — "Where the fatal and injury accident frequency of particular roadway segments or intersections is less than 1/k, such segments and intersections may be aggregated into larger analysis units for application of the EB procedure."
- Practical relevance to my sparse collision link-year dataset: the EB aggregation recommendation is relevant — Open Road Risk's link-year rows with near-zero expected collisions correspond exactly to the situation where EB shrinkage is most important and where the EB minimum frequency criterion applies. The 1/k threshold (approximately 3 predicted accidents per year for segments) is far higher than most Open Road Risk link-years, suggesting that EB shrinkage for individual link-years requires either multi-year aggregation or acceptance of high shrinkage weights.

---

## 11. Validation Strategy

- Train/test split method: none — all data used for model development
- Spatial holdout used? no
- Temporal holdout used? no (Minnesota 5-year and Washington 3-year data pooled for estimation)
- Grouped holdout used? no
- Cross-validation type: none reported
- Metrics: no predictive validation metrics reported; model quality assessed via goodness-of-fit in appendix B (details not extracted) and calibration factor deviation from 1.0
- External validation: calibration to other states is the intended adaptation mechanism, not a validation
- Leakage or generalisation risks: the AMFs for some features (e.g., lighting, access control) are noted to have counterintuitive signs in example models (p. 2–3), which the authors attribute to collinearity and omitted variable bias — this is a documented overfitting/confounding risk in cross-sectional regression SPFs
- Evidence quote or page reference: Section 1, p. 2–3 — discussion of counterintuitive coefficient signs as artefacts of correlation; Section 3, p. 18 — "The model predictions are reliable only within the ranges of independent variables for which data were available in the database."
- What I should copy or avoid: The EB procedure and calibration factor framework are directly usable as diagnostic tools. Do not copy the base model coefficients directly — they require calibration even within the US and are not transferable to UK conditions. The counterintuitive-sign warning on p. 2–3 is a useful citation for documenting the limits of coefficient interpretation in cross-sectional SPFs.

---

## 12. Key Findings Relevant to My Project

**Finding 1:** The segment base model uses a unit-elasticity EXPO multiplier by construction, making it structurally identical to Open Road Risk's fixed-offset design — but this is an explicit modelling choice, not an empirically tested finding.
- Why it matters: This is the foundational FHWA rural two-lane SPF. The fact that it uses unit-elasticity EXPO does not validate the approach — the authors made a design choice to use EXPO as a multiplier rather than estimating AADT and length coefficients freely. Open Road Risk's fixed-offset makes the same choice implicitly.
- Evidence: Equations (5) and (6), p. 17–18
- Confidence: high

**Finding 2:** Intersection base models use freely estimated sub-unit ADT exponents (0.49–0.79 on major road, 0.20–0.61 on minor road).
- Why it matters: The same authors who imposed unit-elasticity on the segment model used free ADT exponents for intersections, finding consistently sub-unit values. This directly supports testing free AADT elasticity as a diagnostic in the Stage 2 GLM.
- Evidence: Equations (7), (8), (9), (10), (11), (12), p. 20–23
- Confidence: high

**Finding 3:** The overdispersion parameter k for the segment base model is 0.31; for intersections it ranges from 0.11 to 0.54.
- Why it matters: These are reference NB overdispersion values from a foundational study on comparable crash count data. Open Road Risk can compare its Stage 2 Poisson GLM Pearson dispersion statistic against these values to judge whether NB is warranted.
- Evidence: Table 23, p. 81
- Confidence: high (well-documented in the report)

**Finding 4:** Calibration factors are the required mechanism for adapting the algorithm to any jurisdiction other than the original study states; even within Minnesota, calibration is recommended for different time periods.
- Why it matters: This is a direct authoritative statement that SPF coefficients do not transfer without recalibration — not just across countries but even across US states and time periods. Directly supports Open Road Risk's transferability framing.
- Evidence: Section 3, p. 25 — "Calibration would even be desirable to apply the algorithm in Minnesota to a time period other than the period for which the base models were developed."
- Confidence: high

**Finding 5:** The grade AMF (1.6% increase per 1% grade) is included despite not being statistically significant, based on expert panel judgment.
- Why it matters: Grade is a candidate feature in Open Road Risk (OS Terrain 50 derivable). This finding suggests the effect size is small and uncertain even in a dedicated rural two-lane study with complete geometric survey data. Deriving grade from OS Terrain 50 at coarser resolution will add further noise.
- Evidence: Section 4, Table 4, p. 40 — "both studies found this effect to be not statistically significant"
- Confidence: high

**Finding 6:** Counterintuitive coefficient signs in cross-sectional SPF regression (lighting and access control with negative signs) are explicitly flagged as artefacts of collinearity, not evidence that the features are beneficial.
- Why it matters: This is a foundational warning about interpreting GLM coefficients in road safety models — directly relevant to how Open Road Risk should present its Stage 2 GLM coefficients, particularly for features like IMD, rural/urban classification, or road class that may be correlated with unmeasured confounders.
- Evidence: Section 1, p. 2–3
- Confidence: high

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| EXPO = AADT × L × 365 / 10^6 as exposure multiplier | Validates current offset structure as a recognised approach in foundational SPF literature | AADT + length | ~1,300 segments (MN+WA) | High — already implemented | Stage 2 documentation | Low (documentation only) | None |
| Calibration factor (observed/predicted ratio) by road class | Checks whether Stage 2 GLM predictions match aggregate STATS19 experience | STATS19 counts + Stage 2 predictions | Any | High | Stage 2 / validation | Low | Must use random sample by facility type, not high-crash selection |
| Overdispersion parameter k as diagnostic reference | Compare Poisson GLM Pearson statistic against NB k = 0.31 (segments) to decide whether NB extension is warranted | Stage 2 GLM residuals | ~1,300 segments | High — applicable at any scale | Stage 2 diagnostic | Low | Segments in this paper are homogeneous rural two-lane; Open Road Risk links are mixed |
| EB shrinkage using model prediction + observed history | Reduces regression-to-the-mean bias in high-collision link identification; requires NB overdispersion estimate | NB k + STATS19 counts + Stage 2 predictions | Any | Medium — EB already in repo as diagnostic variant | Stage 2 / EB variant | Medium | 1/k minimum frequency threshold (~3 accidents/year) rarely met at individual link-year level; aggregation needed |
| Grade as candidate feature | OS Terrain 50 grade derivable; this paper gives a reference effect size (1.6%/% grade) and caveat about non-significance | OS Terrain 50 elevation | Rural two-lane | High — already candidate feature | Stage 2 candidate feature / diagnostic | Medium | Effect is not statistically significant even with complete survey data; OS Terrain 50 is coarser |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Base model coefficients (lane width, shoulder width, RHR, driveway density) | US-specific, rural two-lane only; UK conditions differ; calibration required even within US; no open UK equivalent for lane/shoulder/RHR data | Complete geometric survey inventory | ~1,300 segments | Very low | Develop local NB GLM using available OS/OSM features (already done in Stage 2) | High |
| Intersection base models (three-leg STOP, four-leg STOP, signalised) | Requires separate intersection unit with major and minor road AADT; intersection-specific crash assignment within 76 m buffer; minor road AADT unavailable nationally | Minor road AADT; intersection inventory | ~380–49 intersections | Very low | Future work; out of scope for current link-level pipeline | High |
| AMFs for lane width, shoulder width, passing lanes, TWLTL | Requires complete lane and shoulder inventory not available in OS/OSM at national scale | Complete geometric inventory | Segment-level | Very low | Not applicable to Open Road Risk | High |
| AMFs for superelevation deficiency | Requires horizontal curve inventory and design superelevation values | Survey-grade curve data | Segment-level | Very low | Not applicable | High |
| Roadside hazard rating (RHR) | Manual expert rating; no national open-data equivalent | Field inspection | Segment-level | Very low | Not applicable | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Yes — EXPO = AADT × L × 365 / 10^6 is exactly Open Road Risk's offset structure, used by the foundational US rural two-lane SPF. However, this paper uses complete observed AADT, not estimated AADT.
- **Does it suggest better handling of AADT/AADF uncertainty?** No — complete observed AADT is assumed throughout. AADT estimation uncertainty is not discussed.
- **Does it suggest useful geometry or road-context features?** Lane width, shoulder width, grade, driveway density, and horizontal curvature are all modelled, but none are available nationally in UK open data at the required resolution. Grade is the most feasible partial transfer (OS Terrain 50), but its effect is small and non-significant even in this study.
- **Does it suggest better modelling of junctions?** Yes — the structural separation of intersection and segment crash models, and the separate exposure treatment for junctions (major+minor road AADT as free log covariates), are directly relevant to junctions-and-conflict-structure.qmd. It confirms that a link-level model cannot adequately capture intersection-specific risk without dedicated intersection units.
- **Does it suggest better treatment of severity?** Severity distributions are provided as post-hoc proportion tables applied to total accident predictions, not modelled jointly. Consistent with current scope boundary.
- **Does it suggest better validation design?** Not directly — no held-out validation. The calibration factor framework is the only validation-adjacent procedure. CURE plots are not discussed in this report (referenced to other FHWA documents).
- **Does it expose a weakness in my current approach?** Yes — two relevant weaknesses: (1) the unit-elasticity EXPO assumption in the segment base model is a design choice, not an empirical finding; (2) intersection and segment crashes are conflated in Open Road Risk link-year rows, whereas this algorithm requires explicit spatial separation.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add Harwood et al. 2000 to exposure-and-traffic-volume.qmd as the citation for EXPO = AADT × L × 365 / 10^6 as the canonical exposure multiplier form, alongside Gilardi 2022 and Hauer 2001. Note explicitly that the segment base model uses unit-elasticity by design choice, not empirical estimation.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Equation (5) and (6) show the EXPO structure directly. The unit-elasticity design choice is stated, not empirically derived.
- Evidence: Equations (5) and (6), p. 17–18
- Effort: low
- Risk if implemented badly: none

**Action 2**
- Suggested repo action: Use NB overdispersion parameter k = 0.31 (segments) from Table 23 as a reference value when diagnosing whether Stage 2 Poisson GLM residuals show comparable overdispersion. Document in crash-frequency-models.qmd.
- Action type: diagnostic reference / documentation note
- Relevant stage: Stage 2 / diagnostic
- Why the paper supports it: Table 23 provides the best available published k values for a comparable segment-level NB model fitted with a similar EXPO structure.
- Evidence: Table 23, p. 81
- Effort: low
- Risk if implemented badly: Open Road Risk links are not homogeneous rural two-lane segments; k will likely differ. Use as reference band, not as a target value.

**Action 3**
- Suggested repo action: Cite Harwood et al. 2000 equations (7)–(12) in exposure-and-traffic-volume.qmd to support the free-AADT elasticity diagnostic. These are sub-unit ADT exponents (0.49–0.79) from the same foundational report that also uses unit-elasticity for segments — demonstrating that even the original authors did not treat unit-elasticity as universal.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Direct evidence that the same research team used free ADT exponents where data supported it.
- Evidence: Equations (7), (9), p. 20–21
- Effort: low
- Risk if implemented badly: none

**Action 4**
- Suggested repo action: Add a sentence to junctions-and-conflict-structure.qmd noting that the foundational US rural two-lane SPF explicitly spatially excludes intersection-related crashes (within 76 m) from segment models, and uses separate intersection units with their own AADT structure. Document this as further evidence that link-level and intersection-level risk are structurally distinct.
- Action type: documentation note
- Relevant stage: documentation / future feature
- Why the paper supports it: Section 3, p. 19 explicitly defines the 76 m intersection exclusion zone and the need for separate models.
- Evidence: Section 3, p. 19
- Effort: low
- Risk if implemented badly: none

**Action 5**
- Suggested repo action: Add a caution in crash-frequency-models.qmd (or transferability page) citing Harwood et al. p. 2–3 on counterintuitive coefficient signs as an artefact of collinearity. Use this to frame why Open Road Risk should treat Stage 2 GLM coefficients as descriptive associations, not causal effect estimates.
- Action type: documentation note
- Relevant stage: documentation / Stage 2
- Why the paper supports it: The authors explicitly warn about counterintuitive signs (lighting, access control) in NB regression SPFs as collinearity artefacts — this is from the same foundational paper that established the EXPO structure used in Open Road Risk.
- Evidence: Section 1, p. 2–3
- Effort: low
- Risk if implemented badly: none

---

## 16. Query Tags

- rural-two-lane
- SPF-development
- negative-binomial
- AADT-elasticity
- exposure-offset
- unit-elasticity
- free-AADT-coefficient
- overdispersion-parameter
- empirical-Bayes
- calibration-factor
- AMF
- intersection-SPF
- segment-level
- junction-separation
- grade-feature
- HSIS
- FHWA-report
- US-not-directly-transferable
- coefficient-interpretation-caution
- IHSDM

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high for main report structure, base model equations, overdispersion parameters, and calibration framework; medium for appendix B model development detail (tables 30–44 not fully extracted)
- Important details not stated (or not extracted): full model development statistics from Appendix B (goodness-of-fit, likelihood ratios, data range tables); full Appendix C calibration procedure steps; AMF sensitivity analysis results from Section 5 not extracted in detail
- Parts of the paper that need manual checking: Equation (5) symbol rendering in PDF extraction (sum product notation for horizontal curves, vertical curves, and grades is complex — check original PDF before quoting); overdispersion parameter k values in Table 23 (extracted values 0.31, 0.54, 0.24, 0.11 — confirm against original); signalised intersection model n = 49 (very small; coefficients unreliable)
- Any likely ambiguity or risk of misinterpretation: The unit-elasticity EXPO structure in the segment base model (equations 5 and 6) may be misread as empirical support for unit AADT elasticity. It is a design choice — the EXPO multiplier is constructed to have unit elasticity by definition. Do not cite this as evidence that AADT elasticity = 1 is empirically supported.
