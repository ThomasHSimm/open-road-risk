# Paper Extraction: SPF Decision Guide — Calibration vs Development

## 0. Extraction Run Metadata

- Extraction date: 2026-05-14
- Source PDF filename: dot_49504_DS1.pdf
- Suggested Markdown filename: paper-extraction-srinivasan-2013-spf-decision-guide.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: claude-sonnet-4-6
- Interface used: web chat
- Input type: PDF upload (rendered in context as text/image)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 31-page document accessible. No equations were illegible. Appendix C state examples (Colorado, Florida, Illinois, North Carolina, Utah, Virginia) are brief summaries; detailed coefficient tables are not included in those appendices.

---

## 1. Citation

- Title: Safety Performance Function Decision Guide: SPF Calibration versus SPF Development
- Authors: Raghavan Srinivasan, Daniel Carter, Karin Bauer
- Year: 2013 (report date September 2013; report number FHWA-SA-14-004)
- DOI or URL, if present: Not stated. Publicly available from FHWA Office of Safety.
- Country / region studied: USA (guidance document; references state case studies from multiple states)
- Study setting: mixed (rural two-lane, rural multilane, urban/suburban arterials, freeways, intersections, ramps)

---

## 2. Core Objective

- One-sentence description: This guidebook provides a structured decision process for highway agencies to determine whether to calibrate existing HSM/Safety Analyst SPFs for their jurisdiction or develop jurisdiction-specific SPFs from scratch.
- Main purpose: descriptive analysis / practitioner guidance / decision framework
- Evidence quote or page reference: "This guidebook is intended to provide guidance on whether an agency should calibrate the safety performance functions (SPFs) from the Highway Safety Manual (HSM) (AASHTO, 2010) or develop jurisdiction-specific SPFs." (Executive Summary, p. 6)

---

## 3. Response Variable

- Target variable: crash frequency per site-year (total crashes, injury crashes, fatal crashes, or crash type subsets depending on SPF application)
- Collision type: varies — total crashes for network screening; injury and fatal for project-level SPFs; crash-type-specific SPFs discussed in development steps
- Severity handling: separate SPFs by severity are discussed as an option in development (Step 10); calibration typically uses total crashes
- Count, binary, rate, risk score, severity class, or other: count (crashes per segment-mile per year, or crashes per intersection per year)
- Time window used for outcomes: minimum 3 years of data recommended (Table 1); calibration period not otherwise fixed
- Evidence quote or page reference: "At least 3 years of data are recommended." (Table 1, p. 21)

---

## 4. Exposure Handling

- Exposure variable used, if any: AADT (traffic volume) is the primary and often sole independent variable in network screening SPFs; segment length is a multiplier; major and minor road AADT for intersections
- Traffic count source: state DOT roadway inventory (HPMS), Safety Analyst defaults, or jurisdiction-collected data; minor road AADT identified as a common data gap
- Whether exposure is modelled, observed, assumed, or ignored: observed AADT assumed available for calibration; noted as a data gap for minor roads and some facility types
- Treatment of missing or sparse traffic counts: minor road AADT gaps explicitly flagged as a problem for intersection SPFs; Ohio DOT example uses a hierarchical fallback (adjacent segment data → MPO data → functional-class default values) (Appendix B, p. 26)
- Whether offset terms, rates, denominators, or normalisation are used: SPFs for network screening predict crashes per mile per year (implicit length normalisation); the example Safety Analyst SPF uses `P = L × e^(−5.05) × (AADT)^(0.66)` where L is segment length (p. 8); Part C HSM SPFs use AADT as a free log covariate with estimated coefficient
- Evidence quote or page reference: "These models always include traffic volume (AADT) but may also include site characteristics such as lane width, shoulder width, radius/degree of horizontal curves..." (Section 2, p. 8)
- Transferability to my AADF/WebTRIS setup: mixed
- Notes:
  - The mathematical SPF structure (NB regression with AADT and length as inputs) is highly transferable.
  - The specific HSM/Safety Analyst SPF coefficients are US-derived and not directly transferable to UK conditions.
  - The calibration factor concept (ratio of observed to predicted crashes) is transferable as a diagnostic framework.
  - The free-AADT coefficient in the example (`AADT^0.66`) directly illustrates that unit-elasticity is not the default SPF assumption; this is directly relevant to Open Road Risk's fixed-offset design.
  - Minor road AADT gap discussion (Appendix B) is analogous to Open Road Risk's AADF sparsity problem on minor roads.

---

## 5. Spatial Unit of Analysis

- Unit: road segment or intersection (separate SPF families for each)
- Segment length or segmentation rule: homogeneous segments with respect to site characteristics and traffic volume are recommended; longer non-homogeneous sections noted as an alternative to account for spatial correlation (Martinelli et al. 2009, cited on p. 16)
- How crashes are assigned to the network: not discussed in this guidance document
- Treatment of junctions/intersections: treated as a separate facility type from roadway segments; major and minor road AADT used for intersections; intersection inventory construction discussed in Appendix B
- Spatial aggregation risks: not explicitly discussed; homogeneity requirement implicitly addresses this
- Evidence quote or page reference: "A common approach is to use homogenous segments with respect to site characteristics and traffic volume. This often results in short segments. However, others have suggested using longer, though non-homogenous, sections to account for spatial correlation." (Section 4, p. 16)
- Relevance to OS Open Roads link-based pipeline: OS Open Roads links are variable-length and not guaranteed homogeneous; the document supports using variable-length segments provided facility type is stratified. The non-homogeneity warning is relevant to Open Road Risk's mixed-length link set.

---

## 6. Temporal Unit of Analysis

- Years covered: guidance document; state examples use varying periods (at least 3 years recommended)
- Temporal resolution: annual crash frequency
- Whether seasonality or time-of-day is modelled: not discussed
- Whether before-after or panel structure is used: before-after structure is mentioned for treatment evaluation (Section 3, p. 10) but not the focus of this guide
- Evidence quote or page reference: "At least 3 years of data are recommended." (Table 1, p. 21)
- Relevance to WebTRIS-style time profiles: not addressed in this document

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| AADT (segment) | State DOT roadway inventory | Direct observed count or estimation | Primary exposure variable in all SPFs | Yes — already present as Stage 1a output |
| Segment length | Roadway inventory / GIS | Direct measurement | Length normalisation; multiplier in crash rate | Yes — already present in OS Open Roads |
| Major road AADT (intersections) | DOT inventory | Observed or estimated | Intersection SPF exposure | Partial — link-level model only; junction work future |
| Minor road AADT (intersections) | DOT inventory | Observed or estimated; hierarchical fallback common | Intersection SPF exposure; frequently missing | Low — minor road AADT not available nationally |
| Facility type classification | Roadway inventory | Rule-based classification by road type, lanes, control | Stratifies SPF family | Yes — already present via OS road classification |
| Grade (% grade) | Terrain survey | Derived from elevation profile | Included in more complex SPFs (Bauer and Harwood example) | Partial — OS Terrain 50 available but coarser than survey |
| Horizontal curve radius | Road inventory / survey | Geometric field survey or design plans | Included in Bauer and Harwood rural two-lane SPF | Low — not available nationally in open data |

---

## 8. Model Architecture

- Algorithms/models used: negative binomial (NB) regression via generalised linear models (GLM); this is stated as the standard SPF form throughout
- Baseline model: Poisson GLM (not explicitly stated as baseline, but NB is described as the standard because "crashes typically follow a negative binomial distribution, not a normal distribution", p. 16)
- Final/preferred model: negative binomial GLM with log-linear functional form; jurisdiction-specific NB SPF if calibration quality is poor
- Loss function or likelihood, if stated: NB log-likelihood (implied); GLM framework
- Offset/exposure term, if used: length × AADT as the primary exposure structure; the example SPF uses `L × e^(b0) × AADT^(b1)` form (not a fixed-offset log(AADT × L) form); AADT coefficient is estimated, not fixed at 1.0
- Spatial autocorrelation handling: mentioned as a reason some practitioners use longer non-homogeneous segments; not formally modelled
- Temporal dependence handling: not modelled; panel effects not discussed
- Interpretability method: coefficient signs, CURE plots, goodness-of-fit, Cook's D for outliers (Section 4 Step 5, p. 16)
- Evidence quote or page reference: "These include checking the sign of the parameters' coefficients, examining residuals via residual plots and cumulative residual plots (i.e., CURE plots), and identifying potential outliers using Cook's D or other tools, and examining goodness-of-fit measures." (Section 4, p. 16)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Calibration quality indicator | Calibration factor (C) | 1.0 = perfect match | Any facility type | Ratio of observed to predicted crashes; large deviation from 1.0 indicates poor transferability | Section 5 Step 7, p. 19 |
| Calibration linearity check | Exponent d in `observed = C × predicted^d` | d ≈ 1.0 = linear | Any SPF | If d differs substantially from 1.0, a calibration function rather than a scalar factor is needed | Section 4, p. 13 |
| Staff time estimate — calibration | Hours (data collection + preparation) | 24–40 hrs (network screening); 150–350 hrs (project level) | Per SPF | Calibration requires little statistical expertise | Table 1, p. 21 |
| Staff time estimate — development | Hours (data collection + preparation) | 24–40 hrs (network screening); 450–1050 hrs (project level) | Per SPF | Development requires statistical expertise; much higher data burden | Table 1, p. 21 |
| Sample size — calibration | Sites; crashes/year | 30–50 sites; ≥100 crashes/yr total (project level) | HSM guidance | Minimum for statistically reliable calibration factor | Section 5 Step 4, p. 17–18 |
| Sample size — development | Sites; crashes/year | 100–200 intersections or 100–200 miles; ≥300 crashes/yr total | HSM guidance | Larger sample needed than calibration | Section 5 Step 9, p. 20 |
| Example AADT elasticity | AADT coefficient | 0.66 (Safety Analyst rural multilane divided) | SPF example, p. 8 | Estimated AADT elasticity is sub-unit; not constrained to 1.0 | Section 2, p. 8 |

**Validation status:** This is a guidance document, not an empirical study. No model performance metrics from a held-out validation are reported. The calibration factor and sample size figures are prescriptive recommendations based on practitioner judgment and HSM guidance, not empirical test results.

**Metric relevance to Open Road Risk:** The AADT elasticity example (0.66) is directly relevant to the fixed-offset assumption in Stage 2. The calibration factor framework (observed/predicted ratio) is a transferable diagnostic approach. CURE plots are endorsed as the primary functional-form diagnostic.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: not explicitly discussed as a modelling challenge in this document
- Use of Poisson / negative binomial / zero-inflated models: negative binomial is recommended as the standard distribution because crashes are count data, not normally distributed; zero-inflation not mentioned
- Whether high-risk locations are evaluated separately: network screening is explicitly the context for identifying high-risk sites; EB procedure (Hauer 1997) referenced for regression-to-the-mean correction
- Evidence quote or page reference: "it is important to consider in the modeling effort that crashes typically follow a negative binomial distribution, not a normal distribution." (Section 4, p. 16)
- Practical relevance to my sparse collision link-year dataset: the NB recommendation is directly relevant. The document does not discuss zero-heavy link-year data at 2M+ link scale, so the sparse-count problem specific to Open Road Risk is not addressed here.

---

## 11. Validation Strategy

- Train/test split method: not applicable — guidance document, not an empirical study
- Spatial holdout used? not applicable
- Temporal holdout used? not applicable (calibration period is described as a data requirement, not a validation design)
- Grouped holdout used? not applicable
- Cross-validation type: not discussed
- Metrics: calibration factor (C), calibration linearity check (d), CURE plots, goodness-of-fit
- External validation: not applicable
- Leakage or generalisation risks: the document explicitly warns against selecting high-crash sites for calibration samples, which would bias the calibration factor (Section 5 Step 4, p. 18)
- Evidence quote or page reference: "the agency should not hand pick a group of high crash sites simply to meet the minimum crash frequency requirement. Doing so would strongly bias the calibration process." (Section 5 Step 4, p. 18)
- What I should copy or avoid: the calibration factor diagnostic (observed/predicted ratio check) is a useful and simple tool for assessing whether the Stage 2 GLM is systematically over- or under-predicting by facility type or AADT band. CURE plots are explicitly endorsed as a functional-form diagnostic. Both are low-effort diagnostics applicable to Open Road Risk.

---

## 12. Key Findings Relevant to My Project

**Finding 1:** AADT coefficients in standard SPFs are estimated, not constrained to 1.0.
- Why it matters: The Safety Analyst example gives `AADT^0.66`; the Bauer and Harwood rural two-lane model uses a free `b1 × ln(AADT)` term. Open Road Risk's fixed-offset imposes elasticity = 1.0 by construction. This document provides authoritative support for treating free-elasticity as the standard SPF approach, not an exotic alternative.
- Evidence: Section 2, p. 8 — `P = L × e^(−5.05) × (AADT)^(0.66)`
- Confidence: high

**Finding 2:** Calibration factors substantially different from 1.0 indicate that an existing SPF does not transfer to the jurisdiction without recalibration.
- Why it matters: This directly supports Open Road Risk's position that published SPF coefficients from other geographies should not be transferred without local validation. The calibration-factor framework is a practical tool for quantifying this gap.
- Evidence: Section 5 Step 7, p. 19 — "If the calibration factor is very different from 1.0 (i.e., much less or much greater), this would indicate that the agency's crash experience is much different from the data that were used to estimate the original SPFs."
- Confidence: high

**Finding 3:** CURE plots are the recommended diagnostic for assessing SPF functional form, not just overall goodness-of-fit.
- Why it matters: CURE plots detect systematic residual patterns over AADT or length ranges, which would reveal whether the fixed-offset assumption holds across the AADT distribution. This document provides a second authoritative source for CURE plots alongside Roll 2026 and Dutta & Fontaine 2020 in the register.
- Evidence: Section 4 Step 5, p. 16 and Section 5 Step 7, p. 19
- Confidence: high

**Finding 4:** Calibration samples must be randomly selected from the network, not selected on the basis of crash counts.
- Why it matters: If Open Road Risk computes any form of calibration diagnostic (e.g., observed/predicted ratio by facility type), the comparison sample should cover the full network for that facility type, not just the high-collision links. This is directly analogous to the random-split-vs-spatial-holdout issue.
- Evidence: Section 5 Step 4, p. 18
- Confidence: high

**Finding 5:** Separate calibration factors may be needed by terrain, climate, AADT band, or region within a jurisdiction.
- Why it matters: Open Road Risk spans urban, suburban, rural, motorway, and minor road contexts across a large multi-force geography. A single calibration check across the whole network may mask systematic errors within subgroups. This supports the facility-family split approach already present as a diagnostic variant.
- Evidence: Section 5 Step 6, p. 19 — "separate calibration factors may be needed for each specific terrain type, region, climate, or AADT category"
- Confidence: medium (guidance-level recommendation, not empirically tested in this document)

**Finding 6:** Minor road traffic volume is the most common data gap when constructing intersection inventories.
- Why it matters: Open Road Risk does not currently model intersection-specific risk, but this confirms that minor road AADT is a fundamental data gap for any future junction layer, consistent with the junctions-and-conflict-structure.qmd findings.
- Evidence: Appendix B, p. 26 — "it can be a problem for obtaining volumes on the minor roads. The state roadway inventory may not contain volume data on the minor road of the intersection, especially if it is not a state-owned road."
- Confidence: high (consistent with UK open-data situation)

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Calibration factor check (observed/predicted ratio by facility type) | Quantifies whether Stage 2 GLM systematically over- or under-predicts by road class or AADT band | Stage 2 GLM predictions + STATS19 observed counts | Any | High — straightforward scalar comparison | Stage 2 / validation | Low | Must use random sample of network, not high-crash selection |
| CURE plots over AADT and link length | Detects functional-form misspecification; tests whether fixed-offset assumption holds | Stage 2 GLM residuals + AADT + length | Any | High | Validation / Stage 2 diagnostics | Low–medium | Sensitive to scale; AADT estimation noise will blur CURE signal |
| Free-AADT elasticity diagnostic model | Tests whether unit-elasticity assumption holds; provides alternative beta estimate | Stage 2 data | Any | High | Stage 2 diagnostic | Low | Not a production change; purely diagnostic |
| Stratified calibration check by facility family | Identifies road classes where GLM is most misspecified | Stage 2 predictions + road class | Any | High | Stage 2 / validation | Low | Motorway sample size may be small |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Direct use of HSM/Safety Analyst SPF coefficients | Estimated from US data; calibration factors from UK data would be needed | UK equivalent of HSM doesn't exist in open form | US national | Low | Develop local NB GLM (already done in Stage 2) | High |
| Project-level CMF application | Requires detailed geometric inventory (lane width, shoulder, curve radius, grade, access control) not available nationally in open UK data | Detailed road inventory | Site-specific | Very low | Document as out of scope | High |
| Intersection inventory with minor road AADT | Minor road AADT not available nationally in UK open data | Minor road count data | Any | Low | Future work; OSM proxy only | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Yes, explicitly. All SPFs in the HSM/Safety Analyst framework use AADT and length as the primary exposure inputs. The document treats this as the standard approach.
- **Does it suggest better handling of AADT/AADF uncertainty?** Indirectly — it flags minor road AADT as a common data gap and recommends hierarchical fallback approaches. It does not discuss estimated (vs observed) AADT uncertainty propagation, which is more specific to Open Road Risk's Stage 1a design.
- **Does it suggest useful geometry or road-context features?** Grade and horizontal curvature are mentioned in more complex SPFs (Bauer and Harwood example), but these require survey data not available at national scale in open UK data. Road classification and facility type stratification are explicitly recommended and already present.
- **Does it suggest better modelling of junctions?** Yes — it distinguishes segments and intersections as separate SPF families and identifies minor road AADT as the key gap for intersection modelling. Consistent with junctions-and-conflict-structure.qmd.
- **Does it suggest better treatment of severity?** Step 10 recommends separate SPFs by crash type and severity for development; calibration typically uses total crashes. Not a new finding for Open Road Risk but confirms the separation is standard practice.
- **Does it suggest better validation design?** Yes — the calibration factor check (observed/predicted by facility type) and CURE plots are both practical low-effort diagnostics not yet implemented in Open Road Risk.
- **Does it expose a weakness in my current approach?** Yes — the AADT elasticity example (0.66) is an authoritative illustration that the standard SPF practice does not constrain AADT elasticity to 1.0. Open Road Risk's fixed-offset does. This is the most important pipeline implication from this document.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add Srinivasan et al. 2013 as an authoritative citation in exposure-and-traffic-volume.qmd for the statement that estimated AADT elasticity is typically below 1.0 in SPF practice.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: The Safety Analyst example SPF explicitly shows `AADT^0.66`; this is an official FHWA document, not a single research study.
- Evidence: Section 2, p. 8
- Effort: low
- Risk if implemented badly: none

**Action 2**
- Suggested repo action: Add calibration factor diagnostic to Stage 2 validation — compute ratio of total observed STATS19 collisions to total GLM-predicted collisions, stratified by road class and AADT quartile. Flag if any stratum ratio deviates substantially from 1.0.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: The calibration factor check is the recommended first step in assessing SPF quality. It is low-cost and directly interpretable.
- Evidence: Section 5 Step 7, p. 19
- Effort: low
- Risk if implemented badly: Must use a random sample of links per stratum, not high-crash selections. Requires that GLM is run on a held-out or validation set to be a genuine diagnostic.

**Action 3**
- Suggested repo action: Implement CURE plots over AADT and link length for Stage 2 GLM residuals. This directly tests whether the fixed-offset assumption introduces systematic bias over the AADT distribution.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: CURE plots are explicitly recommended as the primary functional-form diagnostic in both calibration quality assessment (Step 7) and SPF development diagnostics (Step 5).
- Evidence: Section 4 Step 5, p. 16; Section 5 Step 7, p. 19
- Effort: medium
- Risk if implemented badly: AADT is estimated, not observed, for most links; residual patterns may partly reflect Stage 1a estimation error rather than GLM misspecification. Interpret with caution for estimated-AADT links.

**Action 4**
- Suggested repo action: Document in literature-pipeline-alignment.qmd that the free-AADT elasticity diagnostic is supported by the standard SPF practice as described in FHWA guidance, not only by individual research studies. Reference Srinivasan et al. 2013 alongside Aguero-Valverde 2008 and Chengye 2013.
- Action type: documentation note
- Relevant stage: documentation / Stage 2
- Why the paper supports it: This is official FHWA practitioner guidance, not a research paper. It gives the fixed-offset limitation stronger institutional grounding.
- Evidence: Section 2, p. 8
- Effort: low
- Risk if implemented badly: none

**Action 5**
- Suggested repo action: Note in junctions-and-conflict-structure.qmd or transferability-and-open-data-limits.qmd that the minor road AADT gap is a recognised obstacle to intersection SPF development even in the US context with full DOT inventories.
- Action type: documentation note
- Relevant stage: documentation / future feature
- Why the paper supports it: Appendix B explicitly discusses the cost and difficulty of obtaining minor road AADT for intersection modelling; Ohio DOT used a hierarchical fallback to functional-class defaults.
- Evidence: Appendix B, p. 26
- Effort: low
- Risk if implemented badly: none

---

## 16. Query Tags

- SPF-calibration
- SPF-development
- AADT-elasticity
- free-AADT-coefficient
- negative-binomial
- exposure-offset
- CURE-plots
- calibration-factor
- network-screening
- facility-stratification
- HSM
- FHWA-guidance
- transferability
- jurisdiction-specific-SPF
- segment-level
- intersection-SPF
- minor-road-AADT
- functional-form-diagnostic
- US-not-directly-transferable

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper: no empirical validation results; sample size recommendations are described as based on "judgment of the project team" (Table 1 footnote c); the specific AADT elasticity value (0.66) is an example from a single SPF and is not a universal estimate.
- Parts of the paper that need manual checking: the Safety Analyst SPF equation on p. 8 (formula rendering in PDF); the Bauer and Harwood (2012) formula on p. 8 (complex equation — check symbol rendering if quoting).
- Any likely ambiguity or risk of misinterpretation: The document is US-specific and the HSM/Safety Analyst SPF coefficients are not transferable to UK conditions. The value of this document for Open Road Risk is the decision framework, CURE plot endorsement, and AADT elasticity illustration — not the specific SPF values. Do not cite the 0.66 elasticity as a target value for Open Road Risk; cite it as evidence that unit elasticity is not the SPF convention.
