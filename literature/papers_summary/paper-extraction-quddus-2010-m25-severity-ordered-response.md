# Paper Extraction: Quddus, Wang, Ison — M25 Crash Severity, Ordered Response Models

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: road-traffic-congestion-and-crash-severity-econometric-2rrbyxf6f0.pdf
- Suggested Markdown filename: paper-extraction-quddus-2010-m25-severity-ordered-response.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (full text in context)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full text, tables, and figures present. Published version DOI: http://dx.doi.org/10.1061/(ASCE)TE.1943-5436.0000044. Repository record dates deposit as 2019 but publication year from DOI journal (ASCE JTTE) is circa 2010. Page numbers from sequential PDF pages.

**Relationship to companion paper:** This paper is a companion to Wang, Quddus and Ison (the M25 frequency paper previously extracted). Both use the same M25 motorway, same data sources (STATS19 + UKHA), and overlapping study periods. The frequency paper models accident counts at the segment level; this paper models individual crash severity using disaggregated crash records. Findings on congestion (null result) and gradient (insignificant here vs significant in frequency paper) are directly comparable.

---

## 1. Citation

- Title: Road Traffic Congestion and Crash Severity: Econometric Analysis Using Ordered Response Models
- Authors: Mohammed A. Quddus, Chao Wang, Stephen G. Ison
- Year: circa 2010 (published ASCE Journal of Transportation Engineering; DOI: 10.1061/(ASCE)TE.1943-5436.0000044)
- DOI: http://dx.doi.org/10.1061/(ASCE)TE.1943-5436.0000044
- Country / region studied: England (M25 London orbital motorway)
- Study setting: Motorway

---

## 2. Core Objective

- One-sentence description: The paper investigates whether traffic congestion affects the severity (slight, serious, fatal) of individual road crashes on the M25, using disaggregated crash records and ordered response models, while controlling for traffic flow, road geometry, crash characteristics, and environmental conditions.
- Main purpose: Causal inference (congestion–severity relationship); severity modelling
- Evidence quote or page reference: "The primary aim of this study is to investigate the association between the severity (slight, serious and fatal) of individual crashes and the level of traffic congestion measured by total delay." (p. 4)

**Key contrast with companion frequency paper:** The frequency paper (Wang et al.) models crash counts aggregated over 70 segments across 3 years. This paper models each individual crash record (n=3,998) as an ordered categorical outcome. The unit of analysis, response variable, and model family are all different.

---

## 3. Response Variable

- Target variable: Severity of individual crash (ordinal categorical: 1=slight, 2=serious, 3=fatal)
- Collision type: All injury crashes (slight, serious, fatal); property-damage-only not included
- Severity handling: Modelled as the primary outcome using ordered response models. This is a severity-conditional model — it models severity given a crash has already occurred. It does not model crash frequency.
- Count, binary, rate, risk score, severity class, or other: Ordered severity class (disaggregated, one record per crash)
- Time window used for outcomes: STATS19 2003–2006 (4 years, individual crash records)
- Evidence quote or page reference: "1=Slight (count=3594), 2=Serious (count=353), 3=Fatal (count=51)" (Table 1, p. 18); "no attempt is made to estimate the actual probability of a specific accident occurring" (p. 4)

**Important modelling distinction for Open Road Risk:** This paper is entirely about severity given a crash. It does not model whether a crash occurs. Open Road Risk currently models crash frequency (count), not conditional severity. These are complementary modelling problems, not the same problem.

---

## 4. Exposure Handling

- Exposure variable used, if any: None. This is a crash-conditional model; exposure to collision risk is not modelled.
- Traffic count source: UKHA 15-minute interval traffic flow and speed data for all 72 M25 segments, 2003–2006.
- Whether exposure is modelled, observed, assumed, or ignored: Ignored in the severity model — by design. Traffic flow enters as a predictor of severity, not as an exposure term.
- Treatment of missing or sparse traffic counts: Not applicable; complete UKHA data for all segments.
- Whether offset terms, rates, denominators, or normalisation are used: No offset. Not applicable to a crash-conditional severity model.
- Evidence quote or page reference: Model equations (p. 4–6) — no offset term present.
- Transferability to my AADF/WebTRIS setup: Not applicable — this modelling approach does not require exposure data.
- Notes: The absence of exposure handling is structurally correct for a severity-conditional model. This is not a limitation; it is a different problem from Open Road Risk's frequency model.

---

## 5. Spatial Unit of Analysis

- Unit: Individual crash record, matched to a motorway segment
- Segment length or segmentation rule: Same 72 junction-to-junction segments as companion paper. Mean segment length not restated here but approximately 5.3 km (from companion paper). Traffic variables assigned at segment level; crashes matched to segments.
- How crashes are assigned to the network: Same weighted score method (perpendicular distance + angular difference) as companion paper, described as "see Wang et al., 2009 for details" (p. 7).
- Treatment of junctions/intersections: Not stated whether junction crashes are excluded in this paper. Companion paper excluded ~15% junction accidents; not confirmed repeated here.
- Spatial aggregation risks: Traffic characteristics (flow, speed, congestion delay) assigned at segment level and assumed uniform across a segment (~5–10 km). Paper acknowledges this as a limitation: "segments would not necessarily have uniform conditions over 10km length if queues are present." (p. 14)
- Evidence quote or page reference: "Traffic congestion at each of these segments is measured by the total delay...averaged over a 10-km stretch." (p. 7); limitation noted p. 14.
- Relevance to OS Open Roads link-based pipeline: Low direct relevance. OS Open Roads links are much shorter (~median <1 km). The uniform-segment-conditions assumption is more defensible at OS Open Roads link scale. However, severity modelling is not currently part of Open Road Risk.

---

## 6. Temporal Unit of Analysis

- Years covered: STATS19 2003–2006 (4 years); traffic data 2003–2006 at 15-minute intervals
- Temporal resolution: Individual crash events matched to 15-minute traffic intervals. A 30-minute time lag applied (traffic conditions 30 minutes before crash used to avoid crash-induced traffic distortion).
- Whether seasonality or time-of-day is modelled: Yes — peak/off-peak indicator, day of week, year dummies included as covariates. Hourly delay pattern shown in Figure 1.
- Whether before-after or panel structure is used: No. Cross-sectional crash record model.
- Evidence quote or page reference: "In order to avoid the impact of the crash itself on the traffic variables, a 30-minute time lag was considered." (p. 7)
- Relevance to WebTRIS-style time profiles: The 30-minute time lag is a methodologically clean approach to avoid reverse causation (crash causing measured congestion). This is a useful design note for any future Open Road Risk work linking WebTRIS time profiles to crash records.

---

## 7. Engineered Features

Differences from companion frequency paper are flagged. Features already covered in companion extraction are marked.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Total delay per segment (congestion measure) | UKHA 15-min interval delay data | Sum of delay (minutes) for all vehicles on segment, averaged per 10 km stretch | Primary congestion variable; found statistically insignificant for severity | Low — requires complete UKHA delay data; not in open data stack |
| log(Traffic flow, veh/h) | UKHA 15-min interval | Log transform of flow at crash time (30-min lag) | Key severity predictor; higher flow → less severe crash | Low for severity model; medium for frequency diagnostics (open AADF available annually, not 15-min) |
| log(Radius of curvature) | UKHA road geometry | Log transform; minimum radius per segment | Higher curvature (sharper bend) associated with less severe crashes on M25 — counterintuitive result, discussed below | Candidate — already flagged in companion paper; note sign direction differs between frequency and severity |
| Maximum gradient (%) | UKHA road geometry | Continuous; maximum per segment | **Statistically insignificant** for crash severity (contrast: significant for frequency in companion paper) | Note contradictory result vs companion paper |
| Number of lanes (categorical) | UKHA | Three categories: ≤3, 4, ≥5 | Three-lane stretches associated with more severe crashes | Candidate — OSM lanes sparse in Open Road Risk |
| Wet road surface | STATS19 | Binary indicator | Wet surface → less severe crash (speed reduction mechanism) | Already present in STATS19; candidate for severity model only |
| Single-vehicle crash | STATS19 vehicle file | Binary indicator | Single-vehicle crashes substantially more severe | STATS19 available; relevant only to severity model, not frequency |
| Number of casualties per crash | STATS19 casualty file | Integer count | More casualties → more severe classification; used to control for multi-casualty slight crashes | STATS19 available; note potential post-event circularity in a predictive model |
| Peak/off-peak time of day | Derived from time of crash | Binary indicator | Statistically insignificant for severity; uncorrelated with congestion delay (r=0.2) | Already present as WebTRIS output; useful null result |
| Day of week | STATS19 | Binary: weekdays vs weekends | Weekdays → more severe crashes on M25 | STATS19 available |
| Light conditions (darkness) | STATS19 | Binary: darkness vs daylight | Darkness → less severe crash on M25 (counterintuitive vs some urban studies) | STATS19 available |
| Year dummy (2003–2006) | STATS19 | Categorical | Downward severity trend over time; captures unmeasured temporal factors | STATS19 available |

---

## 8. Model Architecture

- Algorithms/models used: (1) Ordered Logit (OLOGIT); (2) Heterogeneous Choice Model (HCM); (3) Generalised Ordered Logit (GOLOGIT); (4) Partially Constrained GOLOGIT (PC-GOLOGIT)
- Baseline model: OLOGIT (standard proportional odds)
- Final/preferred model: PC-GOLOGIT — selected because proportional odds assumption is violated for two variables (log traffic flow, number of vehicles involved); PC-GOLOGIT addresses this while being more parsimonious than full GOLOGIT
- Loss function or likelihood: Maximum likelihood; log-likelihood and LR Chi-square reported for model comparison
- Offset/exposure term, if used: None
- Spatial autocorrelation handling: None — individual crash records, no spatial random effects
- Temporal dependence handling: Year dummies only; no panel structure
- Interpretability method: Marginal effects on probability of each severity outcome (Table 3); predicted probability plots by traffic flow and casualty count (Figures 2, 4)
- Evidence quote or page reference: Model selection p. 9; PC-GOLOGIT preferred p. 9; Brant test for proportional odds p. 9.

**Note on model family relevance to Open Road Risk:** These ordered response models are designed for a severity-conditional problem. They are not a substitute for or extension of Open Road Risk's Poisson/XGBoost frequency model. If Open Road Risk were to add a severity model, the PC-GOLOGIT approach would be a credible candidate, but this would be a separate modelling stage.

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model comparison | Log-likelihood at convergence | −1306.55 / −1299.21 / −1294.29 / −1300.03 | OLOGIT / HCM / GOLOGIT / PC-GOLOGIT | PC-GOLOGIT preferred over OLOGIT; GOLOGIT not significantly better than PC-GOLOGIT | Table 2, p. 20 |
| Model comparison | LR Chi-square | 155.7 / 170.4 / 180.2 / 169.7 | As above | HCM and PC-GOLOGIT similar fit; GOLOGIT 10.5 units better but not significant (p=0.65, 13 df) | Table 2, p. 20 |
| Model fit | McFadden pseudo R² | 0.096 / 0.099 / 0.090 / 0.100 | As above | Low but typical for disaggregated crash severity data | Table 2 |
| Key coefficient | log(Traffic flow) | −0.534 (OLOGIT); threshold-varying in PC-GOLOGIT (−0.509 slight/serious; −0.869 serious/fatal) | All models | Higher flow → less severe crash; effect stronger near fatal threshold | Table 2 |
| Key coefficient | Congestion (total delay) | −0.0005 to −0.0006 across all models | All models | **Statistically insignificant** in all specifications | Table 2 |
| Key coefficient | log(Radius of curvature) | +0.232 (OLOGIT) | All models | Higher radius (straighter road) → more severe crash; significant at 90% | Table 2 |
| Key coefficient | Single-vehicle dummy | +0.671 (OLOGIT); threshold-varying in PC-GOLOGIT (0.658 / 1.199) | All models | Single-vehicle crashes substantially more severe | Table 2 |
| Marginal effect | log(Traffic flow) on Pr(slight) | +0.040 | PC-GOLOGIT | 1 unit increase in log flow increases P(slight) by 4.0 pp | Table 3 |
| Marginal effect | log(Traffic flow) on Pr(fatal) | −0.006 | PC-GOLOGIT | 1 unit increase in log flow decreases P(fatal) by 0.6 pp | Table 3 |
| Marginal effect | Single-vehicle on Pr(slight) | −0.064 | PC-GOLOGIT | Single-vehicle crash reduces P(slight) by 6.4 pp | Table 3 |
| Marginal effect | Wet surface on Pr(slight) | +0.028 | PC-GOLOGIT | Wet surface increases P(slight) by 2.8 pp | Table 3 |
| Predicted probability | Pr(slight/serious/fatal) at mean flow | 0.80 / 0.17 / 0.03 | PC-GOLOGIT at average conditions | Baseline probabilities for a single-vehicle crash at mean conditions | p. 10 |

**Validation type:** All metrics are **in-sample model fit and model comparison**. No train/test split, no cross-validation, no spatial or temporal holdout, no external validation. McFadden R² is an in-sample fit statistic, not predictive accuracy.

**Are any metrics likely to be optimistic?** Yes — all goodness-of-fit metrics are in-sample. With n=3,998 crash records from a single motorway, out-of-sample performance on different road types is unknown.

**Most relevant metric for Open Road Risk:** The marginal effect of traffic flow on severity probability is potentially useful for cross-referencing any future severity extension. The congestion null result replicates the companion frequency paper's finding on a different model and response variable.

---

## 10. Rare Event / Class Imbalance Handling

- How rare events are handled: Fatal crashes are rare (n=51, 1.28% of records). The paper uses disaggregated individual crash data across 4 years to accumulate sufficient fatal and serious events, specifically noting "the number of fatal and serious crashes on the M25 is quite low" as a motivation for using individual records rather than segment aggregates.
- Model family: Ordered logit and extensions — appropriate for ordinal categorical outcome. Not a count model. Zero-inflation not relevant (every record is a crash that occurred).
- Whether high-severity locations evaluated separately: Not stated. Single-vehicle crashes are discussed as a subgroup but not modelled separately (noted as future work).
- Evidence quote or page reference: "there were 23 people killed and 116 seriously injured on the M25 in 2006. In order to tackle this problem...crash data for multiple years (2003 to 2006) are considered." (p. 7)
- Practical relevance to my sparse collision link-year dataset: Limited direct relevance — this is a severity model, not a frequency model. However, the observation that fatal counts are very low even on a busy motorway over 4 years reinforces why fatal-only analysis at Open Road Risk link-year level is not viable without substantial aggregation.

---

## 11. Validation Strategy

- Train/test split method: None — all 3,998 crash records used for fitting
- Spatial holdout used? No
- Temporal holdout used? No
- Grouped holdout used? No
- Cross-validation type: None
- Metrics: Log-likelihood, LR Chi-square, McFadden pseudo R², marginal effects
- External validation: None
- Leakage or generalisation risks: The variable "number of casualties per crash" is a post-event variable that could be partially endogenous to severity classification in STATS19. The paper uses it as a control variable, which is defensible for a descriptive model but would be inappropriate as a feature in any prospective severity prediction system. This is not labelled as data leakage by the authors but should be noted as a feature selection risk if the approach were adapted for prediction.
- Evidence quote or page reference: No holdout description anywhere in paper.
- What I should copy or avoid: The 30-minute time-lag approach for traffic variables is worth copying if Open Road Risk ever links WebTRIS time profiles to crash-level records. Avoid treating McFadden R² ≈ 0.10 as evidence of strong predictive performance.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: Traffic congestion (total delay, congestion index) is statistically insignificant for crash severity on the M25, replicating the null result from the companion frequency paper using a different response variable (severity vs count), different model family (ordered logit vs Poisson), and disaggregated vs aggregated data.
- Why it matters: The null congestion result now holds across two complementary modelling approaches on the same network. This strengthens (within this case study) the case for not prioritising congestion proxies in Open Road Risk's feature set.
- Evidence: p. 10, Table 2; companion frequency paper Section 5.1.
- Confidence: Medium — consistent across two papers and multiple model specifications, but both restricted to M25 motorway. Does not generalise to mixed road networks.

**Finding 2:**
- Finding: Higher traffic flow is associated with less severe individual crashes on the M25 (higher flow → higher probability of slight injury, lower probability of fatal). This is the opposite direction to the flow–frequency relationship (higher flow → more crashes). The paper explicitly notes this contrast.
- Why it matters: This flow–severity inverse relationship, if present in Open Road Risk data, means that high-AADT links might have more crashes but they could be less severe on average. This has implications for how Open Road Risk interprets risk percentiles: links with high AADT may rank highly on frequency-based risk but not on severity-weighted risk.
- Evidence: p. 10–11, Table 2–3, Figure 2.
- Confidence: Medium — consistent across all four model specifications on M25, but motorway-only. Urban road findings may differ.

**Finding 3:**
- Finding: Gradient (vertical grade) is statistically insignificant for crash severity on the M25, despite being a significant predictor of crash frequency in the companion paper. Curvature (radius) shows a counterintuitive positive association with severity (straighter roads → more severe crashes), significant at 90%.
- Why it matters: Gradient may influence how often crashes occur but not how severe they are when they do. The curvature result suggests that road geometry's effect on severity may operate differently from its effect on frequency — relevant if Open Road Risk were to add a severity model. More generally, it cautions against assuming that features significant for frequency will be significant for severity.
- Evidence: Table 2, p. 12 (gradient insignificant); p. 13 (curvature discussion).
- Confidence: Medium for the null gradient result; low confidence in curvature direction generalising beyond M25.

**Finding 4:**
- Finding: Single-vehicle crashes are substantially more severe than multi-vehicle crashes on the M25 (3.4% vs 0.9% fatal rate; 14% vs 8% serious rate). The effect is non-uniform across the severity threshold, captured only by the PC-GOLOGIT model.
- Why it matters: If Open Road Risk were to extend to severity modelling, crash type (single vs multi-vehicle) from STATS19 would be a high-priority feature. For the current frequency model, this is not directly applicable, but it suggests that links with a high single-vehicle crash proportion may have a disproportionate severity burden not reflected in frequency-based risk rankings.
- Evidence: p. 11, Table 2–3.
- Confidence: High within this case study — consistent across models and confirmed by raw observed proportions in Table 1.

**Finding 5:**
- Finding: Wet road surface conditions are associated with less severe crashes, not more. The mechanism proposed is speed reduction. Similarly, darkness is associated with less severe crashes. Both findings are counterintuitive from a frequency perspective but consistent with other motorway-specific studies cited.
- Why it matters: Road surface and lighting conditions from STATS19 may have opposite signs for severity vs frequency models. Open Road Risk should not assume that features associated with more crashes are also associated with more severe crashes.
- Evidence: p. 12 (surface), p. 13 (light); marginal effects Table 3.
- Confidence: Medium — consistent across model specifications; may be motorway-specific (speed compensation on wet roads at motorway speeds).

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| 30-minute time-lag when joining traffic data to crash records | Avoids reverse causation (crash-induced congestion contaminating the traffic predictor) | STATS19 crash time field + time-stamped traffic data | 72 segments, 3,998 crashes | Compatible as a design principle; relevant if WebTRIS profiles are ever linked to crash-level records | Stage 1b / future design note | Low (design principle, not code) | Only applicable if Open Road Risk moves to sub-annual crash-level modelling |
| PC-GOLOGIT / ordered logit severity model structure | Appropriate model family for ordinal severity outcome if severity model added | STATS19 severity field (available) | 3,998 crashes, single motorway | Compatible in principle; feasible as a separate modelling stage | Future extension / Stage 2 variant | Medium | Small fatal/serious counts at link-year level; would require pooling across links or years |
| Separation of frequency and severity modelling | Demonstrates that frequency and severity have different and sometimes opposing predictor relationships (flow, surface, gradient) | Same data as current pipeline | Any scale | Compatible | Documentation / future Stage 2 design | Low | Risk of over-reading a motorway-only finding |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Total delay / congestion index as severity predictor | Requires complete UKHA 15-minute interval delay data per segment; not in open data stack | UKHA delay data | 72 M25 segments | Incompatible at national scale | No practical open-data workaround | High |
| Disaggregated crash-level severity model at link-year resolution | Fatal counts at individual OS Open Roads link-year level are near-zero; model would be numerically unstable without substantial aggregation | No data gap; statistical feasibility problem | 3,998 crashes over 4 years on one motorway | Low for fatal/serious subsets at link-year level; medium if aggregated to link or area | Pool across years and/or use severity index (average severity weight per link) | Medium |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Not applicable — severity-conditional model; exposure not relevant.
- **Does it suggest better handling of AADT/AADF uncertainty?** No. Traffic flow used as a complete observed predictor, not estimated.
- **Does it suggest useful geometry or road-context features?** Gradient: insignificant for severity (contrast with frequency). Curvature: counterintuitive positive severity association. Lanes: significant — three-lane stretches more severe. These suggest geometry features may work differently for severity vs frequency.
- **Does it suggest better modelling of junctions?** No. Not addressed.
- **Does it suggest better treatment of severity?** Yes — primary contribution. It demonstrates that severity and frequency have different determinants, and that ordered response models with relaxed proportional odds are needed for severity. If Open Road Risk adds a severity layer, this is a useful methodological reference.
- **Does it suggest better validation design?** No — no holdout validation.
- **Does it expose a weakness in my current approach?** One indirect point: Open Road Risk's risk_percentile currently ranks by XGBoost-predicted frequency (or Empirical Bayes shrinkage). If severity distribution differs systematically by road type, frequency-based ranking may not identify the links with the highest severity burden. This paper does not prove this for Open Road Risk but raises it as a diagnostic question.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add a documentation note that frequency and severity have documented opposing relationships with traffic flow on UK motorways (higher flow → more crashes but less severe), and that Open Road Risk's frequency-based risk ranking may not reflect severity burden. Flag this as a potential future diagnostic.
- Action type: Documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Paper finds higher flow reduces severity probability; companion paper finds higher flow increases frequency. Both results are consistent across multiple model specifications.
- Evidence: Table 2–3 of this paper; companion frequency paper Tables 2–3.
- Effort: Low
- Risk if implemented badly: None for documentation.

**Action 2**
- Suggested repo action: Note in documentation that gradient is significant for frequency (companion paper) but insignificant for severity (this paper). When OS Terrain 50 grade is integrated into Stage 2, document this distinction and consider whether frequency-only modelling is sufficient or whether a severity-weighted outcome would change the gradient effect.
- Action type: Documentation note → candidate diagnostic when grade feature is active
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Gradient coefficient insignificant in all four severity model specifications (Table 2).
- Evidence: Table 2, p. 14 (conclusions).
- Effort: Low
- Risk if implemented badly: None for documentation.

**Action 3**
- Suggested repo action: If Open Road Risk ever links WebTRIS 15-minute profile data to crash-level records for temporal analysis, adopt the 30-minute pre-crash time-lag design to avoid contamination of traffic predictors by crash-induced congestion.
- Action type: Documentation note / design principle for future Stage 1b or crash-level work
- Relevant stage: Stage 1b / future design
- Why the paper supports it: "In order to avoid the impact of the crash itself on the traffic variables, a 30-minute time lag was considered." (p. 7)
- Effort: Low (design note)
- Risk if implemented badly: If lag is not applied, traffic conditions measured after a crash onset will be endogenous to the crash event.

**Action 4**
- Suggested repo action: Document that single-vehicle crash type from STATS19 is a strong severity predictor, and consider whether links with a high proportion of single-vehicle crashes (derivable from STATS19 history) could be used as a diagnostic feature or a severity-weighted ranking supplement in future.
- Action type: Documentation note / candidate future feature
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Single-vehicle crashes have 3.4× higher fatal rate and 1.75× higher serious rate than multi-vehicle on M25 (Table 1 + p. 11).
- Effort: Low for note; medium if implemented as a link-level proportion feature
- Risk if implemented badly: Single-vehicle proportion derived from historical collisions is a post-event variable; would need careful treatment to avoid leakage if used as a Stage 2 feature.

**Action 5**
- Suggested repo action: Add a brief literature note that two independent modelling approaches (segment-level Poisson frequency model; disaggregated ordered logit severity model) on the same UK motorway both find traffic congestion statistically insignificant, supporting the current decision to exclude congestion proxies from Open Road Risk's Stage 2 feature set.
- Action type: Documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Congestion insignificant in all models (Table 2, p. 10); consistent with companion frequency paper.
- Effort: Low
- Risk if implemented badly: None. Note should specify this is motorway-only evidence.

---

## 16. Query Tags

- ordered-logit
- PC-GOLOGIT
- heterogeneous-choice-model
- crash-severity-model
- severity-conditional
- STATS19
- UK-motorway
- disaggregated-crash-records
- congestion-null-result
- traffic-flow-severity-inverse
- gradient-insignificant-severity
- curvature-severity
- single-vehicle-severity
- no-exposure-offset
- in-sample-only-validation
- McFadden-pseudo-R2
- proportional-odds-violation
- frequency-severity-distinction
- time-lag-design
- motorway-only

---

## 17. Confidence and Gaps

- Overall confidence in extraction: High — full paper text, tables, and figures present.
- Important details not stated in the paper: Exact publication year not in document (circa 2010 from DOI journal). Whether junction crashes were excluded (as in companion paper) is not restated here. Sample sizes per year not broken out (only totals by severity in Table 1).
- Parts of the paper that need manual checking: Table 2 coefficient values for GOLOGIT (some cells show "−" indicating constrained/absent terms — verify interpretation against paper text p. 9). The heterogeneous choice model variance equation variables are described in text but the table layout is dense; confirm that the "Factors affecting the error variance" row entries (single-vehicle, casualties) are variance-equation terms, not mean-equation terms.
- Any likely ambiguity or risk of misinterpretation: (1) The curvature–severity positive association (straighter roads more severe) is counterintuitive and road-type specific; do not generalise to mixed networks. (2) Wet surface and darkness reducing severity is specific to motorway speed dynamics and should not be applied to urban or rural road contexts. (3) The null congestion result from two companion papers is now stronger evidence than either paper alone, but still motorway-specific.
