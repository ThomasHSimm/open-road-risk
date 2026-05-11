# Paper Extraction — Methodological Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: ImpactofReal-timeTrafficCharacteristicsonFreewayCrashOccurrence-SystematicReviewandMeta-analysis.pdf
- Suggested Markdown filename: paper-extraction-roshandel-2015-realtime-traffic-freeway-crash.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered as document text in context)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 31-page document text was accessible. Tables and figures partially rendered; key quantitative tables (Tables 7, 10) fully legible.

---

## 1. Citation

- Title: Impact of Real-time Traffic Characteristics on Freeway Crash Occurrence: Systematic Review and Meta-analysis
- Authors: Saman Roshandel, Zuduo Zheng, Simon Washington
- Year: Not explicitly stated in document body; paper covers studies 1997–2012. Publication year inferred as approximately 2015 based on content references (NHTSA 2013 cited). **Not confirmed — check journal version.**
- DOI or URL, if present: Not stated
- Country / region studied: International (systematic review synthesising studies primarily from USA, with some from Korea and Japan)
- Study setting: Motorway / freeway (all selected studies focused on freeway segments)

---

## 2. Core Objective

- One-sentence description: The paper synthesises evidence from prior studies on the relationship between real-time traffic characteristics (speed, density, volume, and their variations) and crash occurrence on freeways, providing quantitative summary effect sizes via meta-analysis.
- Main purpose: Systematic review + meta-analysis (descriptive synthesis / effect-size estimation); not a primary prediction model.
- Evidence quote or page reference: "This paper addresses this need by undertaking a systematic literature review to identify current knowledge, challenges, and opportunities, and then conducts a meta-analysis of existing studies to provide a summary impact of traffic characteristics on crash occurrence." (Abstract, p.2)

---

## 3. Response Variable

- Target variable: Binary crash occurrence (crash vs. non-crash condition)
- Collision type: All injury crashes combined (the review explicitly excluded studies focusing on specific crash types such as sideswipe-only)
- Severity handling: Not modelled; studies included in the meta-analysis focused on occurrence (frequency), not severity. One excluded study (Moore et al., 1995) focused on severity.
- Count, binary, rate, risk score, severity class, or other: Binary (case-control design; odds ratios reported)
- Time window used for outcomes: Per-crash event; traffic characteristics measured in short intervals (typically 5–15 minutes) immediately preceding crash
- Evidence quote or page reference: "As this study focuses on all crash type rather than a specific type of crash, it is inappropriate to combine results from general crashes with those from a specific crash type." (Table 3 notes, p.8–9)

---

## 4. Exposure Handling

- Exposure variable used, if any: Not used as an offset or explicit denominator. The studies reviewed use a case-control design where crash conditions (cases) are matched against non-crash conditions (controls) at equivalent times/locations. Volume (average vehicles per time slice) is included as a predictor variable, not as an exposure offset.
- Traffic count source: Loop detector data (85% of included studies); vehicle trajectory data from video surveillance (2 studies — Hourdos et al., 2006, 2008)
- Whether exposure is modelled, observed, assumed, or ignored: In the case-control framework, exposure is implicitly controlled by the matching design (location, time of day, day of week) rather than being explicitly modelled as a denominator or offset.
- Treatment of missing or sparse traffic counts: Not addressed. The paper notes that loop detector data have "limited and discontinuous data coverage, both spatially and temporally" (p.24–25), and acknowledges this as a methodological weakness. Sparse coverage is not handled; studies simply used available detector data.
- Whether offset terms, rates, denominators, or normalisation are used: No offset terms used. This is a fundamental structural difference from Open Road Risk's Poisson GLM with log-exposure offset. The meta-analysis synthesises log-odds ratios from binary logistic regression models.
- Evidence quote or page reference: "Loop detector data were predominantly used in the selected studies (85%) as they were widely available and accessible." (p.11, Section 2.2); "researchers are often forced to use data collected from loop detectors far from crash locations and must estimate traffic characteristics prior to a crash." (p.24–25)
- Transferability to my AADF/WebTRIS setup:
  - Mathematical exposure structure: **Low** — the case-control/binary logistic framework is structurally incompatible with an annual link-year Poisson count model. No offset is used; these are not SPFs.
  - Substantive finding about which traffic characteristics matter: **Low to medium** — directional signals (speed variation, speed difference increasing risk) are suggestive, but the variables are real-time sub-minute to 15-minute measurements, which are not available in Open Road Risk.
- Notes: The paper explicitly excludes AADT-based studies from its meta-analysis on grounds that "aggregated loop detector data (e.g., AADT) are inherently not suitable for testing the association between real-time traffic conditions and crash occurrence." (Table 3 notes, p.8). This demarcation is important: the paper is about a *different research question* from Open Road Risk's aggregate SPF approach.

---

## 5. Spatial Unit of Analysis

- Unit: Freeway segment (basic freeway segment, not intersections)
- Segment length or segmentation rule: Defined by loop detector station placement; segments are bounded by adjacent detector pairs. Length not stated uniformly; varies by site.
- How crashes are assigned to the network: Police reports provide crash location; matched to nearest upstream/downstream loop detector station. Temporal precision of police reports identified as a major weakness (p.25).
- Treatment of junctions/intersections: Ramp studies explicitly excluded (Lee and Abdel-Aty, 2008 excluded). Weaving segments noted as a research gap (p.22). Basic freeway segments only.
- Spatial aggregation risks: Loop detector placement may not coincide with crash location; spatial mismatch acknowledged as a problem (p.24–25).
- Evidence quote or page reference: "researchers are often forced to use data collected from loop detectors far from crash locations and must estimate traffic characteristics prior to a crash." (p.24–25)
- Relevance to OS Open Roads link-based pipeline: Low. Freeway-segment/loop-detector spatial unit is incompatible with OS Open Roads link geometry, which covers the full network including urban and rural roads. The freeway-segment unit is also defined by detector placement, not fixed network topology.

---

## 6. Temporal Unit of Analysis

- Years covered: Studies published 1997–2012; individual study observation periods not stated for most studies in the meta-analysis.
- Temporal resolution: Sub-hourly (typically 5–15 minute aggregation of loop detector raw data, which is collected every 20–30 seconds). This is the defining characteristic of the "real-time" approach.
- Whether seasonality or time-of-day is modelled: Time of day controlled as a confounder in most case-control studies (listed as variable T in Table 1 coding). Seasonality not stated as explicitly modelled.
- Whether before-after or panel structure is used: Neither. Case-control design: each crash event is one case, matched with non-crash controls from equivalent time-location windows in the same or other weeks.
- Evidence quote or page reference: "traffic characteristics during a certain time interval immediately before the crash are often measured and linked to crash likelihood. Most of the selected studies split a certain period prior to a crash into equal time segments." (p.24)
- Relevance to WebTRIS-style time profiles: Limited. The paper confirms that time-of-day is an important confounder in crash occurrence — consistent with the rationale for Stage 1b. However, the paper's time resolution (minutes before a crash) is entirely different from WebTRIS annual average peak/off-peak fractions.

---

## 7. Engineered Features

Only features explicitly used in the included meta-analysis studies are listed.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Average speed (S) | Loop detector (20–30s raw, aggregated to 5–15 min) | Mean speed across vehicles in time slice | Summary odds ratio 0.952 — lower average speed associated with higher crash risk (stop-go conditions) | No — requires sub-hourly sensor data not available in Open Road Risk |
| Speed variation (SV) | Loop detector | Standard deviation of speed within time interval before crash | Strongest significant predictor; summary OR 1.225 per unit increase | No — requires sub-hourly sensor data |
| Coefficient of variation of speed (CVS) | Loop detector | SD of speed / mean speed | Statistically insignificant after publication bias correction; directionally suggests risk increase | No — requires sub-hourly sensor data |
| Speed difference (SD) | Loop detector | Speed difference between specific downstream and upstream detector positions | Summary OR 1.032; only 2 estimates — interpret with caution | No — requires paired detector positions |
| Average density (D) | Loop detector | Mean vehicle density (vehicles/lane/km) in time slice | After publication bias correction, OR 0.909 — higher density associated with reduced crash risk when not location-stratified, possibly confounded | No — requires sub-hourly sensor data |
| Density variation | Loop detector | Absolute difference between density at time t and daily average | Summary OR 0.876 — large variations correspond to off-peak hours | No — requires sub-hourly sensor data |
| Average volume (V) | Loop detector | Mean vehicle count in time slice | Summary OR 1.001 — very small positive effect; practically marginal | No — requires sub-hourly sensor data |
| Time of day | Police report / calendar | Categorical or continuous confounder | Controlled in most studies as confounder | Already present / compare implementation |
| Road geometry (curvature, ramp presence) | Road inventory | Categorical confounder | Controlled in better-quality studies | Already present / compare implementation |
| Weather / pavement condition | Weather records | Categorical confounder (wet/dry) | Controlled in higher-quality studies | Candidate feature for Stage 2 (limited open data availability) |

---

## 8. Model Architecture

- Algorithms/models used: Binary logistic regression (dominant), matched case-control logistic regression, Bayesian belief networks, classification trees, multi-layer perceptron, normalised radial basis function, Kohonen clustering (across the 13 studies reviewed)
- Baseline model: Matched case-control logistic regression (most common in reviewed literature)
- Final/preferred model: Not applicable — this is a meta-analysis, not a primary model. Meta-analysis uses random-effects or fixed-effects weighted average of log-odds ratios.
- Loss function or likelihood, if stated: Logistic likelihood (binary outcome) in primary studies; random-effects meta-analysis uses inverse-variance weighting
- Offset/exposure term, if used: No offset used in any reviewed study. Binary logistic framework, not count/rate model.
- Spatial autocorrelation handling: Not addressed in any reviewed study; identified as a gap.
- Temporal dependence handling: Handled implicitly via matched case-control design (matching on time of day and weekday). Not addressed as a formal panel/time-series problem.
- Interpretability method: Log-odds ratios / odds ratios reported; marginal effects not computed
- Evidence quote or page reference: "Most studies used matched case-control design and logistic regression to assess possible relationships." (p.6, Section 2.2); meta-analysis methodology in Section 3.

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Meta-analytic summary effect | Summary odds ratio | 0.952 (CI: 0.909–0.996) | Average speed, all locations | Per-unit increase in speed associated with 4.8% decrease in crash odds | Table 7, p.16 |
| Meta-analytic summary effect | Summary odds ratio | **1.225** (CI: 1.132–1.326) | Speed variation | Per-unit increase in speed SD associated with 22.5% increase in crash odds | Table 7, p.16 |
| Meta-analytic summary effect | Summary odds ratio | 2.76 (CI: 0.969–7.863); adjusted 2.842 (CI: 0.985–8.195) | CVS | Not significant at 5% level after publication bias correction | Table 7, p.16 |
| Meta-analytic summary effect | Summary odds ratio | **1.032** (CI: 1.026–1.038) | Speed difference | Per-unit increase associated with 3.2% increase; only 2 estimates, interpret with caution | Table 7, p.16 |
| Meta-analytic summary effect | Summary odds ratio | 0.968 (unadjusted); **0.909** adjusted (CI: 0.831–0.993) | Average density | After publication bias correction, higher density associated with lower crash odds (off-peak confound likely) | Table 7, p.16 |
| Meta-analytic summary effect | Summary odds ratio | **0.876** (CI: 0.866–0.886) | Density variation | Lower crash risk with higher density variation (off-peak hours effect) | Table 7, p.16 |
| Meta-analytic summary effect | Summary odds ratio | **1.001** (CI: 1.000–1.002) | Average volume | Marginal positive effect; OR barely exceeds 1.0 | Table 7, p.16 |
| Location-stratified effect | Summary odds ratio | 2.914 (CI: 1.937–4.385) | CVS at downstream | Very large effect when measured downstream of crash | Table 10, p.20 |
| Location-stratified effect | Summary odds ratio | 0.817 (CI: 0.674–0.990) | CVS at upstream | Opposite direction when measured upstream | Table 10, p.20 |
| Primary study prediction accuracy | Correct prediction rate | 69% | Abdel-Aty et al., 2004 (logistic regression) | False negative 38.8%, false positive 5.39% | p.26 |
| Primary study prediction accuracy | Correct prediction rate | 80% | Hourdos et al., 2006 (trajectory data) | False positive rate 15% | p.26 |
| Primary study prediction accuracy | Correct prediction rate | 66% | Hossain & Muromachi, 2012 (Bayesian belief net) | False positive rate 20% | p.26 |
| Sensitivity analysis | Correlation between time interval and estimate | 0.998 | CVS | Very strong: choice of time window near-perfectly correlates with CVS estimate magnitude | Table 9, p.19 |
| Sensitivity analysis | Correlation between time interval and estimate | 0.822 | Speed variation | Strong: longer time windows inflate speed variation estimates | Table 9, p.19 |

**Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated?**

The meta-analysis summary effects are derived from published log-odds ratios. These are not predictions from a model fitted in this paper. Of the 13 primary studies: 8 reported some form of validation ("model application" treated as equivalent to validation by the authors); 5 did not validate. Validation methods varied and are generally not spatially or temporally held out by modern standards. The paper itself notes this as a significant weakness.

**Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, or calibration?**

The primary study prediction accuracy figures (66–80%) test binary classification performance on a held-aside sample in some studies. However, case-control ratios (1:1 to 1:5) mean false positive rates are not representative of operational deployment conditions (p.27). These should not be treated as operationally valid prediction accuracy estimates.

**Are any metrics likely to be optimistic for real-world deployment?**

Yes. The paper explicitly states: "using a 1:1 case control design will bias false positive rates to be really low, because in practice there are far more 'real' controls than the one used in the study." (p.27). The meta-analytic odds ratios also come from studies that excluded behavioural factors accounting for ~93% of crash causation, which structurally limits discriminative power.

**Which metric, if any, is most relevant to Open Road Risk?**

None directly. Open Road Risk is an annual aggregate count model, not a real-time binary classifier. The meta-analytic finding that speed variation is the strongest real-time precursor (OR 1.225) is relevant as context, but not actionable without sub-hourly sensor data.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Case-control matching is used. The paper notes that crashes are rare events and explicitly discusses case-control design as "an efficient method of studying the relative risks of rare events" (p.22). Controls are matched at equivalent locations/times/weekdays to reduce confounding.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models: Not used in any reviewed study. Binary logistic regression is standard. Zero-heavy counts handled implicitly by the case-control design (non-crash conditions = controls).
- Whether high-risk locations are evaluated separately: Some studies differentiate by upstream/downstream detector position and by location type (weaving, merge, diverge); see Table 10. Hourdos et al. (2006, 2008) focused specifically on "high-crash freeway locations."
- Evidence quote or page reference: "case-control design is an efficient method of studying the relative risks of rare events, and is widely used in epidemiology." (p.22)
- Practical relevance to my sparse collision link-year dataset: Limited. The case-control approach is used here because the response is binary (crash/no-crash per time slice), not a count. Open Road Risk's link-year unit has many zero-collision years, but the model family (Poisson/NB) handles this differently from case-control binary logistic. The paper's approach is not transferable to the count structure.

---

## 11. Validation Strategy

- Train/test split method: Varies across the 13 primary studies. Most used temporal or location-based splits — e.g., training on one site or time period, testing on another. Not stated uniformly.
- Spatial holdout used? Not stated (varies by primary study; "validated against other sites or another time period" per quality criterion C3, Table 4)
- Temporal holdout used? Not stated (some studies used a different time period for validation)
- Grouped holdout used? Not stated
- Cross-validation type: Not used in any primary study; not used in meta-analysis
- Metrics: Prediction accuracy (% correct), false positive rate, false negative rate (primary studies). Meta-analysis uses Q-test for heterogeneity, funnel plots and trim-and-fill for publication bias.
- External validation: Not performed in this meta-analysis paper. Some primary studies validated against held-out sites or time periods.
- Leakage or generalisation risks: Case-control ratio mismatch (1:1 study vs. operational reality with vastly more controls) inflates apparent false-positive performance. The paper identifies this as an unaddressed issue. The paper itself is a meta-analysis and does not fit a primary model.
- Evidence quote or page reference: "using a 1:1 case control design will bias false positive rates to be really low, because in practice there are far more 'real' controls than the one used in the study." (p.27)
- What I should copy or avoid: The paper's Q-test + random-effects meta-analytic framework is relevant if I ever conduct a systematic review of SPF literature. The case-control design itself is not appropriate for Open Road Risk. The explicit discussion of publication bias and sensitivity to time-interval choice is methodologically instructive for any meta-analysis I might conduct.

---

## 12. Key Findings Relevant to My Project

**Finding 1**
- Finding: Speed variation (standard deviation of speed in the minutes before a crash) is the strongest real-time predictor of freeway crash occurrence, with a summary odds ratio of 1.225 per unit increase.
- Why it matters: Provides directional evidence that traffic flow instability — not just volume — is associated with crash risk. Consistent with the rationale for including time-zone profile features in Open Road Risk, though the timescale (minutes) is entirely different from annual AADT-based exposure.
- Evidence: Table 7, p.16; Section 3.4, p.15.
- Confidence: Medium (synthesises 5 studies; heterogeneity present; measurement unit unstandardised across studies)

**Finding 2**
- Finding: Average volume has a very small effect on crash occurrence (OR 1.001), suggesting that volume alone is a weak discriminator of crash risk compared to speed variation.
- Why it matters: This supports caution about over-relying on estimated AADT as the sole exposure variable in Stage 2. It suggests that flow instability and speed characteristics carry risk information beyond what volume captures. However, this paper uses real-time volume (per 5–15 minute slice), not annual AADT, so direct comparison is not straightforward.
- Evidence: Table 7, p.16.
- Confidence: Medium

**Finding 3**
- Finding: The relationship between traffic characteristics and crash occurrence is strongly confounded by the upstream/downstream location of the detector relative to the crash. CVS measured downstream shows OR 2.914 (very high risk signal), while CVS upstream shows OR 0.817 (opposite direction).
- Why it matters: Illustrates that spatial position of measurement relative to the event matters enormously. For Open Road Risk, this is a caution about how road network features measured at or near a link may be influenced by post-event states. It also reinforces why collision-derived contextual columns are correctly excluded from Stage 2 features in this pipeline.
- Evidence: Table 10, p.20; Section 3.5, p.19–20.
- Confidence: High (directly observed in multiple studies)

**Finding 4**
- Finding: The time interval chosen to aggregate traffic measurements has a strong relationship with both study quality and effect size estimates — correlations between time interval and estimate range from 0.505 (volume) to 0.998 (CVS). This was arbitrarily selected in most studies.
- Why it matters: Suggests that temporal aggregation choices are a major source of inconsistency in the literature. For Open Road Risk, this is context for understanding why real-time traffic predictor studies show inconsistent results. It does not directly affect annual aggregate modelling.
- Evidence: Table 9, p.19; Section 3.5, p.18–19.
- Confidence: High

**Finding 5**
- Finding: The paper demonstrates that behavioural factors account for approximately 93% of crash causation, with road environment factors accounting for 34% (with substantial overlap). Traffic-only models therefore have a structural ceiling on discriminative power.
- Why it matters: Provides a principled explanation for why any road-environment model (including Open Road Risk) will exhibit high residual variance. This is not a failure of modelling — it reflects the actual causal structure of crashes. Useful for documentation of expected model limitations.
- Evidence: Figure 6 (Lum and Reagan, 1995, cited in paper), p.21–22.
- Confidence: High for the cited statistic; note it is from a US 1995 source — exact proportions may differ for UK context.

**Finding 6**
- Finding: Most real-time crash prediction models reviewed achieved only 66–80% prediction accuracy with false positive rates of 5–20%, and the paper concludes these models are "currently unsuitable for implementation at the real world operational level."
- Why it matters: Calibrates expectations for what real-time prediction models can achieve even with sub-minute traffic data. Open Road Risk, operating at annual link-year level, should not be expected to achieve high individual-event prediction accuracy — its purpose is aggregate risk ranking, which is a different and more appropriate objective.
- Evidence: p.4 (introduction); p.26 (Section 4.5).
- Confidence: High

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Q-test + random-effects meta-analysis framework | Useful if conducting systematic review of SPF literature for Open Road Risk | Published study results (log-odds ratios or coefficients + SEs) | 13 studies, 46 estimates | Fully compatible — not computationally demanding | Documentation / future review task | Low | Publication bias issues acknowledged by paper |
| Sensitivity analysis against time-interval choice | Concept transferable: test how temporal aggregation (e.g., yearly vs multi-year window) affects estimates | Annual STATS19 data | Applicable conceptually | Compatible | Stage 2 / validation | Low | Different mechanism — time-interval sensitivity in this paper is about sub-hour aggregation, not annual panels |
| Confounder control for time-of-day and location type | Conceptual support for including time-zone profiles and road classification in Stage 2 | WebTRIS profiles (already in pipeline), road classification (already in pipeline) | All 13 studies | Compatible | Stage 2 — already partially implemented | Already present | None new |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Real-time crash prediction using speed/density/volume from loop detectors | Requires sub-hourly loop detector data per segment; Open Road Risk has annual AADF counts at sparse locations | No sub-hourly per-link sensor data; loop detector density in the UK is much lower than US freeway networks | Individual freeway segments, minutes resolution | Incompatible — wrong temporal and spatial scale | None — fundamentally different data regime | High |
| Case-control binary logistic regression for crash occurrence | Structurally incompatible with link-year count model; requires non-crash observation matching; no exposure offset | No per-event non-crash comparison observations in STATS19-style data at link-year unit | Per-crash event | Incompatible | Not applicable | High |
| Speed variation (SD of speed) as a feature | Requires continuous speed observations within a short time window; not available from AADF | No sub-hourly speed data per link | Minutes resolution | Incompatible | Possibly proxy via OSM speed limits combined with AADT/capacity ratio, but this is speculative and distant from the paper's variable | High |
| Vehicle trajectory extraction from video surveillance | Very high cost, manual, site-specific; not scalable | No national video trajectory dataset | Single freeway sites | Incompatible | Not applicable at 2.17M links | High |

---

## 14. Pipeline Implications

**Does this paper support using exposure-normalised collision risk?**
Indirectly. The paper is about real-time binary prediction (crash/no-crash), not aggregate rate modelling. However, its finding that average volume has minimal discriminative power (OR 1.001) and its exclusion of AADT-based studies from the meta-analysis on grounds of being "not suitable for testing real-time conditions" both implicitly affirm that aggregate exposure (AADT) and real-time risk are distinct phenomena. This is consistent with Open Road Risk's approach of using AADT as an exposure offset rather than as a risk predictor.

**Does it suggest better handling of AADT/AADF uncertainty?**
No. The paper explicitly excludes AADT-based studies. It does not address exposure estimation uncertainty.

**Does it suggest useful geometry or road-context features?**
Marginally. Road geometry (curvature) and segment type (weaving, merge, diverge) are noted as important confounders that most studies failed to control adequately. This is consistent with including road classification and form-of-way in Stage 2. No new specific geometry features are identified that are not already in the pipeline.

**Does it suggest better modelling of junctions?**
Not directly. Ramp studies were excluded from the reviewed literature. Weaving segments are identified as a research gap. No junction modelling method is proposed.

**Does it suggest better treatment of severity?**
No. Severity is explicitly out of scope for all 13 included studies. One excluded study (Moore et al., 1995) focused on severity and was excluded for incompatibility.

**Does it suggest better validation design?**
Yes — methodologically instructive. The paper identifies: (a) case-control ratio mismatch inflates false positive performance; (b) time-interval choice has large effects on estimates; (c) location position (upstream vs downstream) of measurement matters. For Open Road Risk, the relevant takeaway is to be explicit about which validation split method is used and whether grouped/spatial holdout adequately prevents leakage.

**Does it expose a weakness in my current approach?**
Not a direct weakness. The paper operates in a different paradigm (real-time, binary, sub-hourly). It does confirm that aggregate traffic-only models face a structural explanatory ceiling because behavioural factors dominate crash causation — this should be documented as a known limitation of Open Road Risk.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add documentation note to Stage 2 README explaining the distinction between aggregate SPF approaches (Open Road Risk) and real-time crash prediction approaches (this paper's domain), and why the structural explanatory ceiling (93% behavioural factors) is expected.
- Action type: Documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Paper explicitly quantifies the structural limitation (Figure 6, p.21–22) and concludes real-time models are unsuitable for operational deployment at current accuracy levels.
- Evidence: "only 3% of all crashes are the result of roadway factors alone" (p.21); "the performance of the existing crash prediction models are inaccurate, imprecise, and reveal inconsistent results" (p.21)
- Effort: Low
- Risk if implemented badly: None — documentation change only

**Action 2**
- Suggested repo action: Add documentation note to Stage 1b (WebTRIS time profiles) explaining that time-of-day is a well-established confounder in crash occurrence (controlled in 61% of reviewed real-time studies), supporting the rationale for learning peak/off-peak fractions even if not currently in Stage 2 features.
- Action type: Documentation note
- Relevant stage: Stage 1b / documentation
- Why the paper supports it: Time of day coded as confounder T in all reviewed studies; meta-analysis sensitivity analysis confirms confounding by location and time.
- Evidence: Table 1 coding variables, p.6; Section 3.5.
- Effort: Low
- Risk if implemented badly: None

**Action 3**
- Suggested repo action: When reporting Stage 2 validation metrics, document explicitly whether the validation split is temporal, spatial, or grouped — and flag that case-control ratio choices in the literature inflate apparent performance. Use this as justification for the grouped-by-road-link split currently in use.
- Action type: Documentation note / validation
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Paper demonstrates how case-control ratio choice "will bias false positive rates to be really low" (p.27) — an analogous concern to using random (non-grouped) splits in link-year panel data.
- Evidence: Section 4.5, p.26–27.
- Effort: Low
- Risk if implemented badly: None

**Action 4**
- Suggested repo action: When evaluating any future candidate feature derived from traffic flow (e.g., capacity utilisation ratio derived from AADT and road class), document that the feature is a static annual proxy for what this literature shows matters at minute-level resolution. Note that such proxies are theoretically plausible but empirically distant from what the real-time literature measures.
- Action type: Documentation note / candidate feature context
- Relevant stage: Feature engineering / Stage 2
- Why the paper supports it: Speed variation (real-time, minutes) is the strongest predictor (OR 1.225), but no AADT-based proxy can capture this. Annual AADT ÷ capacity is a very different construct.
- Evidence: Table 7 results; Section 4.3 discussion of aggregation issues.
- Effort: Low
- Risk if implemented badly: None

**Action 5**
- Suggested repo action: No new model changes recommended. The paper does not provide transferable primary modelling methods for Open Road Risk's pipeline.
- Action type: No action required
- Relevant stage: N/A
- Why: The paper's methods (real-time binary logistic, case-control, loop detector data) are structurally incompatible with Open Road Risk's annual count model, UK open-data context, and 2.17M-link scale.
- Effort: N/A
- Risk if implemented badly: N/A

---

## 16. Query Tags

- real-time-crash-prediction
- freeway-only
- case-control-design
- binary-logistic-regression
- speed-variation
- loop-detector-data
- meta-analysis
- systematic-review
- odds-ratio
- publication-bias
- sensitivity-analysis
- time-interval-sensitivity
- location-confounding
- motorway-applicable
- not-transferable-aggregate-model
- behavioural-factors-dominate
- no-exposure-offset
- sub-hourly-temporal-resolution
- prediction-accuracy-ceiling
- UK-low-transferability

---

## 17. Confidence and Gaps

- Overall confidence in extraction: High
- Important details not stated in the paper:
  - Publication year of the paper itself is not stated in the document body (inferred as ~2015 from reference to NHTSA 2013)
  - DOI or journal name not stated
  - Individual primary study observation periods (years of data) are not reported in Tables 2–3
  - Exact segmentation lengths for each study's freeway segments not stated
  - Whether UK/European studies are included is not stated; review appears predominantly US-focused
- Parts of the paper that need manual checking:
  - Table 10 (location-stratified results): partially legible in rendered PDF; confidence intervals should be verified against original
  - Figure 6 (crash causation proportions): reproduced from Lum and Reagan (1995); verify the original source and note it is US-specific and dated
- Any likely ambiguity or risk of misinterpretation:
  - The paper's exclusion of AADT-based studies is sometimes misread as a general critique of AADT as an exposure variable; it is actually a domain-specific exclusion (AADT is inappropriate for *real-time* prediction, not for aggregate SPFs)
  - The meta-analysis reports effects for one-unit increases in traffic variables; without knowing the units and scale of each variable across studies, absolute magnitude comparisons across OR values are difficult
  - "Model application" is treated as equivalent to "model validation" by the authors (p.6, footnote to Table 2) — this is a weaker standard than independent validation
