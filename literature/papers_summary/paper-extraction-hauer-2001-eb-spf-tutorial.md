# Paper Extraction — Hauer et al. 2001

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: SPF_Basic_Tutorial_2001_by_Ezra_Hauer.pdf
- Suggested Markdown filename: paper-extraction-hauer-2001-eb-spf-tutorial.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered in context as text + page images)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: This is a practitioner tutorial distributed at the 2009 National SPF Summit; it is not a peer-reviewed journal article. No formal abstract beyond the opening summary. The document is self-contained and fully accessible.

---

## 1. Citation

- Title: Estimating Safety by the Empirical Bayes Method: A Tutorial
- Authors: Ezra Hauer, Douglas W. Harwood, Forrest M. Council, Michael S. Griffith
- Year: 2001 (August 2001; distributed at 2009 National SPF Summit, Chicago)
- DOI or URL, if present: Not stated. Noted as shared with permission of Dr. Hauer.
- Country / region studied: United States (examples draw on US SPF parameters and FHWA models, though the method is general)
- Study setting: mixed (road segments and intersections; rural and urban examples)

---

## 2. Core Objective

- One-sentence description: The paper provides a step-by-step worked tutorial on applying the Empirical Bayes (EB) method to estimate the expected accident frequency of road entities by combining site-specific accident counts with Safety Performance Function (SPF) predictions for similar entities.
- Main purpose: methodological tutorial / safety performance function application / hotspot detection support tool
- Evidence quote: "The purpose of this paper is to facilitate the transition from theory into practice" (p. 2); "The purpose of this paper is to illustrate that what may seem to be a complex theory can be put into daily practice" (Section 6, p. 14)

---

## 3. Response Variable

- Target variable: Expected accident frequency for a road entity (segment or intersection), expressed as accidents per km-year for segments or accidents per year for intersections
- Collision type: All injury severities illustrated; Example 5 specifically works through EB estimates by severity class (fatal K, incapacitating injury A, non-incapacitating injury B, possible injury C, property damage only PDO)
- Severity handling: Primarily total accidents; severity-specific EB estimation demonstrated in Example 5 using proportional severity splits applied to total SPF prediction. Overdispersion parameter is noted to be unchanged when SPF is multiplied by a severity proportion constant.
- Count, binary, rate, risk score, severity class, or other: count (accidents per km-year for segments; accidents per year for intersections); EB estimate is a smoothed expected count
- Time window used for outcomes: flexible; examples use 1, 2, 3, or 9 years; the paper argues the full procedure should use as many years as available
- Evidence quote: "The full version of the EB procedure makes use of a longer accident and traffic flow history. Because the full procedure uses more accident counts, the estimate of the full procedure is more precise" (Section 2, p. 3)

---

## 4. Exposure Handling

- Exposure variable used: ADT (Average Daily Traffic) / AADT, used as the primary predictor variable in the SPF. Exposure is embedded in the SPF as a power-law term (e.g. µ = 0.0224 × ADT^0.564 accidents/km-year). Segment length L and years Y are used multiplicatively to compute the expected count η = µ × L × Y.
- Traffic count source: Not stated for a specific dataset; examples use hypothetical ADT values drawn from illustrative SPF parameters sourced from published US studies (Vogt and Bared 1998, Persaud and Dzbik 1993, etc.)
- Whether exposure is modelled, observed, assumed, or ignored: observed (tutorial assumes ADT is known for each year; the full procedure explicitly accommodates year-by-year ADT changes)
- Treatment of missing or sparse traffic counts: Not addressed. The tutorial assumes ADT is available for all years of the accident record. The full procedure (Example 8) requires year-specific ADT values.
- Whether offset terms, rates, denominators, or normalisation are used: SPF predictions function as the "expected accidents on similar entities" term in the EB weighted average, not a formal offset in the Poisson/GLM sense. However, length L and years Y enter multiplicatively: η = µ × L × Y, which is structurally equivalent to a log-linear offset of log(L × Y) applied to a rate µ.
- Evidence quote: "µ the number of accidents/(km-year) for expected on similar segments… η the number of accidents during a specified period given by µ×L×Y expected for similar segments" (Section 3, p. 4)
- Transferability to my AADF/WebTRIS setup: mixed
- Notes:
  - Mathematical structure of EB weighting: high transferability. The weight formula (equation 2: weight = 1 / [1 + (µ×Y)/φ]) and the EB estimate formula (equation 1) are directly applicable to my pipeline. My repo already has an EB shrinkage diagnostic variant; this tutorial is the primary reference for that implementation.
  - SPF-as-exposure structure: high transferability. My Stage 2 Poisson GLM plays the role of the SPF; my XGBoost predicted rate plays the role of µ. The EB step can be applied on top of either model output.
  - Year-specific ADT in full procedure: high transferability. My Stage 1a estimates AADT per link per year, which directly supports the full procedure (equation 7: weight = 1 / [1 + Σµ_year / φ]).
  - Overdispersion parameter φ: medium transferability. The tutorial assumes φ is estimated from SPF calibration data (negative binomial regression). My Poisson GLM does not currently produce a φ estimate for use in EB weighting; this is a concrete gap (see Section 15).
  - US-specific SPF parameters in examples: low transferability for the specific coefficient values. The method itself transfers fully; the example SPF equations do not apply to UK roads.

---

## 5. Spatial Unit of Analysis

- Unit: road segment or intersection (entity-level)
- Segment length or segmentation rule: Arbitrary; the tutorial uses a 1.5 km and 1.8 km segment in examples. Segment length L enters as a multiplier. Example 4 demonstrates how a segment composed of geometrically distinct subsections can be handled by computing expected accidents per subsection and summing before applying EB.
- How crashes are assigned to the network: Assumed to be available at segment or intersection level; no spatial snapping method described (this is a methods tutorial, not a data paper).
- Treatment of junctions/intersections: Explicitly handled as a separate entity type. For intersections, L=1 (length is not a denominator); µ is accidents/year not accidents/km-year; φ is not per-unit-length. Example 6 and Example 7 work through intersection EB estimation including the case where accident counts are available only for a group of intersections jointly.
- Spatial aggregation risks: Not discussed explicitly. Example 4 (subsections) is the closest treatment: the paper aggregates subsection predictions and treats the combined segment as one entity, noting this is a practical simplification.
- Evidence quote: "For intersections L is taken to be one" (Section 3, p. 4)
- Relevance to OS Open Roads link-based pipeline: High relevance. My OS Open Roads links are the direct equivalent of the "road segment" entity in this tutorial. The subsection example (Example 4) is particularly relevant because OS Open Roads links vary in length and may represent portions of longer homogeneous segments. The intersection handling is relevant to future junction-level risk work.

---

## 6. Temporal Unit of Analysis

- Years covered: Tutorial examples use 1, 2, 3, or 9 years; the framework is general
- Temporal resolution: annual (accident counts and ADT values per year)
- Whether seasonality or time-of-day is modelled: No. Annual totals only.
- Whether before-after or panel structure is used: Panel structure implicit in the full procedure (Example 8, 9): year-by-year ADT and accident counts for a single entity over multiple years. Yearly multipliers (secular trend terms) from a multivariate SPF model are incorporated in Example 9.
- Evidence quote: "The full procedure differs from the abridged procedure in that year to year changes in ADT and in other variables can be brought into estimation thereby allowing use of longer accident histories" (Section 5, p. 11)
- Relevance to WebTRIS-style time profiles: Indirect. The tutorial's yearly multipliers (secular trend) concept is analogous to year fixed effects in my Stage 2 model. Time-of-day profiles are not relevant to this tutorial; it operates at annual resolution only.

---

## 7. Engineered Features

The tutorial is a methods paper, not a feature engineering paper. Features used in SPF examples are illustrative only.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| ADT / AADT | Traffic counts (assumed observed) | Direct input to SPF power-law term: µ = a × ADT^b | Primary exposure predictor in SPF; drives EB expected count η = µ×L×Y | Already present — my Stage 1a estimates AADT for all links; compare implementation |
| Segment length L | Road network geometry | Multiplies µ to give expected accidents per segment per year | Required for correct exposure scaling; segments of different lengths are not comparable without this | Already present — link_length_km in my Stage 2 offset |
| Accident Modification Factors (AMFs) | Engineering knowledge / prior studies | Multiplicative adjustments to µ for known deviations from SPF baseline conditions (e.g. shoulder width, intersection control type) | Allow the SPF to be applied to sites that differ from the calibration average | Partially present — road classification, form of way, and other features in my Stage 2 implicitly play an AMF-like role; explicit AMF framework not used |
| Yearly multipliers (secular trend) | SPF calibration; year fixed effects | Multiplicative annual adjustment to µ estimated alongside SPF regression coefficients | Corrects for system-wide year-to-year changes in safety (vehicle fleet, enforcement, weather patterns) | Partially present — year could be added as a feature or offset multiplier in my Stage 2; not currently explicit |
| Overdispersion parameter φ | SPF calibration (negative binomial regression) | Estimated per unit length for segments; used to compute EB weight | Determines how much weight is given to site accident count vs. SPF prediction; larger φ means more weight on counts | Gap — my Poisson GLM does not currently produce a fitted φ for use in EB weighting |

---

## 8. Model Architecture

- Algorithms/models used:
  - Safety Performance Function (SPF): power-law regression model of form µ = a × ADT^b (× AMFs), calibrated using negative binomial regression
  - Empirical Bayes estimator: weighted combination of SPF prediction (η = µ×L×Y) and observed accident count (x), using weight = 1/[1 + η/φ] (abridged) or weight = 1/[1 + Σµ_year/φ] (full procedure)
- Baseline model: SPF prediction alone (µ for similar entities); EB is explicitly an improvement over using either counts alone or SPF alone
- Final/preferred model: Full EB procedure incorporating year-specific ADT and secular trend multipliers (Example 8/9)
- Loss function or likelihood: SPF calibrated under negative binomial likelihood (not derived in this tutorial; referenced to Hauer 1997 and Hauer 2001)
- Offset/exposure term: η = µ×L×Y is the expected count for the entity over the observation period; functionally equivalent to an offset in a GLM. No formal log-link offset notation used.
- Spatial autocorrelation handling: Not addressed. EB is site-specific; no spatial smoothing across neighbouring sites.
- Temporal dependence handling: Full procedure accommodates year-specific ADT changes and secular trend multipliers. No formal time-series model.
- Interpretability method: Direct: the weight parameter quantifies how much the site's own accident count is trusted vs. the SPF prior. Standard deviation of EB estimate given by equation 3: σ(estimate) = √[(1−weight) × estimate].
- Evidence quote: "The EB estimator pulls the accident count towards the mean and thereby accounts for the regression to mean bias" (Section 4, p. 5)

---

## 9. Reported Quantitative Results

This is a tutorial, not an empirical study. No model fit or validation metrics are reported. All numerical results are worked examples with illustrative hypothetical data.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| EB estimate (worked example) | Expected accidents in 1 year | 8.48 ± 2.14 | 1.8 km segment, ADT=4000, 1-yr count=12, SPF η=4.34 | EB pulls count (12) toward SPF mean (4.34); weight=0.46 | Example 1, p. 5 |
| EB estimate (worked example) | Expected accidents in 3 years | 23.92 ± 4.32 | Same segment, 3-yr counts (12,7,8) | More years of data → lower weight on SPF (0.22 vs 0.46) | Example 2, p. 6–7 |
| EB estimate (worked example) | Expected accidents in 2 years | 8.78 ± 2.34 | 1.5 km segment with subsections, 2-yr count=11 | Subsection SPFs aggregated before EB step | Example 4, p. 7–8 |
| EB estimate by severity (worked example) | Expected fatal accidents in 3 years | 0.295 ± 0.136 | Severity K (fatal); SPF proportion 0.019; count=1 | Weight=0.937 for rare severity; EB dominated by SPF prior | Example 5, p. 8–9 |
| EB estimate by severity (worked example) | Sum of severity-specific estimates | 20.35 vs. 23.92 (total-count estimate) | All severities vs. total in Example 2 | Severity-split EB systematically under-estimates relative to total EB due to smaller µ per severity class; ad-hoc correction factor 23.92/20.35=1.118 proposed | Example 5, p. 9 |
| EB estimate (full procedure) | Expected accidents per year (9-yr history) | 71.52 ± 8.11 (9-yr total); 8.15 ± 0.92 (for year 1997) | 1.8 km, varying ADT over 9 years | Very low weight=0.079 on SPF prior; dominated by 9-yr accident record | Example 8, p. 12–13 |

**Metric qualification:**

- All quantitative results are **worked examples with illustrative data, not empirical validation results**. There are no in-sample or out-of-sample model performance metrics.
- The paper makes no predictive accuracy claims. Its purpose is to demonstrate correct computation of the EB estimator, not to validate it against held-out data.
- The theoretical justification for the EB weight formula (minimising variance of the combined estimate) is referenced to Hauer (1997, pp. 193–194), not derived here.
- No metrics are relevant to direct comparison with my XGBoost or GLM output; the tutorial provides the computational procedure, not benchmark numbers.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The EB procedure is specifically designed for sparse accident data. When expected counts are low (rare events), the weight given to the SPF prior increases toward 1.0, so the EB estimate is dominated by the expected count for similar entities rather than the site's own record. This is the core mechanism: "It is the property of the EB procedure that estimates will not be dominated by the random occurrence of rare events" (Example 5, p. 9).
- Use of Poisson / negative binomial / zero-inflated models / hurdle models: The SPF is calibrated under a negative binomial distribution to handle overdispersion. Poisson is noted as the earlier practice, now superseded. Zero-inflated models not mentioned.
- Whether high-risk locations are evaluated separately: Not in this tutorial. Hotspot identification is not the focus; EB estimation is the focus. The regression-to-mean correction is specifically motivated by the selection bias that arises when sites are chosen because they appear to have high accident counts.
- Evidence quote: "when it takes a long time for few accidents to occur, the estimate is imprecise. Thus, e.g., if one expects… one accident in ten years then, with three years of accident counts, the estimate… has a standard deviation of 180% of the mean" (p. 1–2)
- Practical relevance: Very high for my pipeline. My link-year dataset has ~98–99% zeros. The EB mechanism directly addresses this: for links with zero or very few observed accidents, the EB estimate will be pulled almost entirely toward the SPF-predicted rate (high weight on prior), producing stable non-zero risk estimates. This is precisely what my current EB shrinkage diagnostic variant is doing, and this tutorial is the foundational reference for that approach.

---

## 11. Validation Strategy

- Train/test split method: Not applicable; this is a tutorial on computation, not a validation study.
- Spatial holdout used: Not applicable
- Temporal holdout used: Not applicable
- Grouped holdout used: Not applicable
- Cross-validation type: None
- Metrics: None (worked examples only)
- External validation: None in this document; references Hauer (1997) for theoretical derivation and justification
- Leakage or generalisation risks: Not applicable to this tutorial. The theoretical literature on EB is referenced for derivation; the tutorial demonstrates correct application of established formulae.
- Evidence quote: "For a full derivation and justification, see (1, pp. 193-194)" [reference 1 = Hauer 1997]
- What I should copy or avoid: This tutorial should be the primary cited reference for my EB shrinkage diagnostic implementation. The specific weight formula (equations 2 and 7) and the standard deviation formula (equation 3) should be directly cited in my pipeline documentation.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: The EB weight formula (weight = 1/[1 + (µ×Y)/φ]) correctly balances the SPF prior against site accident counts, with the weight on the SPF increasing as: (a) expected accident frequency µ is lower, (b) fewer years of data Y are available, and (c) overdispersion φ is higher. For sparse data (rare events), the EB estimate is almost entirely determined by the SPF.
- Why it matters: This formalises the shrinkage behaviour of my existing EB diagnostic variant. Links with zero observed accidents are not simply assigned zero risk; they are assigned approximately µ×L×Y, the SPF-predicted count. This is the theoretically correct treatment for my ~98–99% zero link-years.
- Evidence: Equations 1 and 2, Section 3–4, pp. 3–5; illustrated in Example 5 where weight=0.937 for rare fatal accidents
- Confidence: high (established theory, not an empirical claim)

**Finding 2:**
- Finding: The full EB procedure (equation 7) accommodates year-specific ADT changes by replacing the single µ×Y term with Σµ_year in the weight denominator, enabling use of a longer accident history without assuming constant traffic. This uses more accident data and produces more precise estimates.
- Why it matters: My Stage 1a estimates AADT per link per year. The full procedure is directly implementable in my pipeline: for each link, compute the year-specific predicted count η_year = µ_year × L, sum across years, and apply equation 7. This would allow me to use the full 10-year accident record (2015–2024) including COVID-affected years with correctly adjusted exposure.
- Evidence: Section 5, Example 8, equation 7, pp. 11–13
- Confidence: high

**Finding 3:**
- Finding: When severity-specific EB estimates are computed by applying proportional splits to the total SPF prediction, the sum of severity-specific estimates will differ from the total EB estimate. The discrepancy arises because smaller per-severity µ values produce larger weights on the SPF prior. An ad-hoc correction ratio is possible, but the paper acknowledges this is not theoretically clean and references more formal multivariate procedures (Flowers 1981; Heydecker and Wu 1991) that require additional parameters not readily available.
- Why it matters: If I add a severity-split EB output, I should be aware that naively summing severity-specific EB estimates will not equal the total EB estimate. The paper flags this as a known limitation with no straightforward fix given available data.
- Evidence: Example 5, p. 9: "The sum of expected accidents when estimated separately for each severity is 20.35. When the same has been estimated in example 2 using the total accidents without differentiation by severity, the estimate was 23.92"
- Confidence: high (arithmetic consequence of the method, not an empirical claim)

**Finding 4:**
- Finding: The overdispersion parameter φ is estimated per unit length for road segments (units: 1/km or 1/mile) and is not per unit length for intersections. When a SPF is multiplied by a constant (e.g. a severity proportion or an AMF), φ is unchanged. This means the same φ can be used for severity-split EB estimation when the SPF is constructed by multiplying the total SPF by a fixed severity proportion.
- Why it matters: My Poisson GLM does not currently produce φ in this sense. To implement the full EB procedure, I need to either (a) refit my SPF as a negative binomial GLM and extract the dispersion parameter, or (b) estimate φ from the ratio of the Pearson chi-squared to degrees of freedom. This is a concrete gap in my current EB implementation.
- Evidence: Section 3, p. 4: "the overdispersion parameter is estimated per-unit-length"; Example 5, p. 9: "the overdispersion parameter φ remains 2.05/km for all severities because it can be shown that when the SPF is multiplied by a constant, the overdispersion parameter is unchanged"
- Confidence: high

**Finding 5:**
- Finding: The regression-to-mean bias arises whenever sites are selected for attention because their accident counts appear unusually high or low. Any estimate of expected accidents at a selected site based only on its own counts will be biased. The EB correction is the only theoretically sound remedy; failure to apply it produces inflated estimates of countermeasure effectiveness.
- Why it matters: My XGBoost risk percentile is used to identify high-risk links. If I subsequently evaluate safety improvements at those links using before/after counts without EB correction, I will overestimate treatment effectiveness. This is directly relevant to any downstream use of my pipeline outputs for intervention prioritisation.
- Evidence: Section 1, p. 2: "the EB estimator pulls the accident count towards the mean and thereby accounts for the regression to mean bias… incorrect claims caused by failure to recognize this bias are still being published in the literature"
- Confidence: high

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| EB weight formula (equation 2 / abridged) | Converts SPF-predicted rate + observed count into a shrinkage estimate; directly applicable to any link-year with a GLM or XGBoost predicted count | Predicted count η from SPF (my Stage 2 GLM or XGBoost), observed count x, overdispersion parameter φ | Single entity; scales to any number of links | High — applies independently per link; no MCMC or spatial structure needed | Stage 2 (EB shrinkage diagnostic already present; document and formalise) | Low | φ must be estimated correctly from negative binomial calibration; using Poisson φ=∞ would collapse EB to the observed count |
| Full EB procedure with year-specific ADT (equation 7) | Uses all 10 years of accident history per link with year-specific AADT estimates from Stage 1a; produces more precise EB estimates than abridged version | Year-specific AADT per link (available from Stage 1a), observed annual collision counts, φ per facility family | Single entity over multiple years | High — my link-year panel structure directly supports this | Stage 2 / EB shrinkage | Medium | Requires φ to be estimated; COVID years (2020–2021) affect AADT estimates and should be flagged |
| Secular trend (yearly) multipliers in SPF (Example 9) | Removes system-wide annual trend from site-specific estimates; equivalent to year fixed effects in my GLM | Year fixed effects or multipliers estimated in Stage 2 SPF calibration | Not stated (general method) | High — year can be added as a covariate or offset multiplier in Stage 2 | Stage 2 / feature engineering | Low-medium | Year effects estimated from my study area data only; may conflate COVID effects with secular trend |
| Subsection aggregation (Example 4) | Handles case where collision record is available for a longer segment but SPF is computed per sub-link | Predicted counts per OS Open Roads link; collision snapping to link | Not stated (general method) | Medium — relevant if collisions are snapped to a parent road rather than individual links | Stage 2 / collision snapping diagnostic | Low (diagnostic) | Collision snapping quality affects this; currently ~99.8% snap rate but ambiguous matches remain |
| Severity-specific EB (Example 5 with correction ratio) | Provides severity-stratified EB estimates; ad-hoc correction ratio partially addresses the systematic under-estimation | Severity proportions by facility family from STATS19; total SPF predicted count | Not stated (general method) | Medium — feasible but KSI counts at link-year level will be very sparse | Stage 2 / future feature | Medium | The ad-hoc correction (multiply by total-EB/sum-of-severity-EB) is acknowledged as imprecise; formal multivariate EB requires additional parameters not readily available |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| US-specific SPF coefficient values (e.g. µ = 0.0224×ADT^0.564) | These are calibrated for US road types and jurisdictions; not applicable to UK roads | UK-calibrated SPF required | US roads | Not applicable | My Stage 2 GLM is the UK-calibrated SPF; coefficients from this tutorial are illustrative only | High |
| Formal multivariate EB for severity (Flowers 1981; Heydecker 1991 approach) | Requires additional cross-severity covariance parameters not available from standard SPF calibration; paper explicitly notes these are not easily available | Cross-severity covariance estimates | Not stated | Low (parameter availability) | Severity-split EB with ad-hoc correction ratio as approximation | High |
| AMF-based adjustment for individual geometric features (shoulder width, etc.) | Requires published AMF values calibrated for UK road types; not generally available for OS Open Roads features | UK AMFs for specific geometric variables | US roads | Low (data availability) | Road classification and OSM features in Stage 2 features implicitly play AMF-like role; explicit AMF framework not applicable without UK AMF literature | Medium |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Yes, directly. The SPF structure (µ = f(ADT) per km-year) is the canonical exposure-normalised form. The tutorial confirms that ADT × length × years is the correct exposure scaling for segment-level expected counts. My Stage 2 offset is consistent with this.

- **Does it suggest better handling of AADT/AADF uncertainty?** Partially. The full procedure (equation 7) requires year-specific AADT estimates per link, which my Stage 1a provides. The tutorial does not address uncertainty propagation from estimated (rather than observed) AADT into the EB weight — this remains a gap not addressed by this paper.

- **Does it suggest useful geometry or road-context features?** Only indirectly via AMFs. The tutorial demonstrates that known geometric differences from the SPF calibration baseline (e.g. shoulder width) should be applied as multiplicative AMFs on µ before computing EB weights. Road classification and form of way in my pipeline serve this role implicitly.

- **Does it suggest better modelling of junctions?** Yes, in that intersections are explicitly treated as separate entity types with different SPF form (accidents/year, not accidents/km-year) and with φ not per unit length. This is relevant if I add junction-level risk modelling as a future feature.

- **Does it suggest better treatment of severity?** Yes, with caveats. Example 5 provides the correct EB procedure for severity-specific estimation and explicitly flags the systematic discrepancy between total EB and the sum of severity-specific EB estimates. The paper recommends formal multivariate EB (Flowers/Heydecker) as the correct solution but notes it is not practically available.

- **Does it suggest better validation design?** No. This is a methods tutorial; validation is not in scope.

- **Does it expose a weakness in my current approach?** Yes — two concrete gaps:
  1. My Poisson GLM does not currently produce a negative-binomial overdispersion parameter φ, which is required for the correct EB weight. My current EB implementation may be using an incorrect φ or a proxy. This should be checked.
  2. My EB shrinkage diagnostic does not currently use the full procedure (equation 7) with year-specific AADT, even though my Stage 1a produces the required year-specific AADT estimates. The abridged procedure is being used where the full procedure is available.

---

## 15. Repo Actionability

**Action 1:**
- Suggested repo action: Verify that the existing EB shrinkage diagnostic uses the correct negative-binomial overdispersion parameter φ (in units of 1/km for segments), as specified in equations 2/3 of this tutorial. If the current implementation uses a Poisson assumption or a Pearson chi-squared proxy, document the approximation and assess the sensitivity of EB weights to different φ values.
- Action type: diagnostic
- Relevant stage: Stage 2 / EB shrinkage diagnostic
- Why the paper supports it: The weight formula depends critically on φ; using the wrong φ will produce incorrect EB weights, either over-shrinking (φ too small) or under-shrinking (φ too large) toward the SPF prior
- Evidence: Equation 2, Section 3, p. 4–5; "the overdispersion parameter is estimated per-unit-length"
- Effort: low (audit) to medium (refit as negative binomial if needed)
- Risk if implemented badly: Incorrect φ produces biased EB estimates; over-shrinkage toward SPF prior is particularly problematic for high-risk links with genuine elevated counts

**Action 2:**
- Suggested repo action: Upgrade the EB shrinkage diagnostic from the abridged procedure (single-year or fixed-period µ) to the full procedure (equation 7: weight = 1 / [1 + Σµ_year / φ]), using year-specific AADT predictions from Stage 1a to compute µ_year per link per year. This uses the full 2015–2024 accident record per link and is more precise.
- Action type: candidate model extension (EB diagnostic)
- Relevant stage: Stage 2 / EB shrinkage diagnostic
- Why the paper supports it: "the full procedure uses more accident counts, the estimate of the full procedure is more precise than the estimate produced by the abridged procedure" (Section 2, p. 3); equation 7 directly supports year-varying AADT
- Evidence: Section 5, Examples 8 and 9, equations 7, pp. 11–13
- Effort: medium
- Risk if implemented badly: COVID years (2020–2021) have anomalous AADT estimates; may need to flag or down-weight those years in the Σµ_year sum

**Action 3:**
- Suggested repo action: Add documentation to the EB shrinkage module citing this tutorial (Hauer et al. 2001) as the primary methodological reference. Document the weight formula (equation 2), the standard deviation formula (equation 3), and the full-procedure weight (equation 7) explicitly. Note the known limitation that severity-split EB estimates do not sum to the total EB estimate and that the ad-hoc correction ratio (total-EB / Σseverity-EB) is an approximation.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Tutorial provides the canonical formulation and numerical worked examples for all relevant EB cases
- Evidence: Equations 1, 2, 3, 7; Example 5 severity discrepancy discussion, p. 9
- Effort: low
- Risk if implemented badly: None (documentation only)

**Action 4:**
- Suggested repo action: Add a documentation note flagging the regression-to-mean bias as a downstream risk for any user of the pipeline outputs who performs before/after evaluation of interventions at links identified as high-risk. The pipeline identifies high-risk links partly because their observed counts are high; naive before/after comparison at those links without EB correction will overestimate treatment effectiveness.
- Action type: documentation note
- Relevant stage: documentation / user guidance
- Why the paper supports it: Section 1, p. 2: the regression-to-mean bias is explicitly demonstrated to produce inflated countermeasure effectiveness estimates; the paper notes "incorrect claims caused by failure to recognize this bias are still being published"
- Evidence: Section 1, pp. 1–2
- Effort: low
- Risk if implemented badly: None (documentation only)

**Action 5:**
- Suggested repo action: When adding facility-family split models (currently deferred for v2), calibrate a negative binomial SPF per facility family and extract the per-family φ estimate. This enables correct EB weighting per family, rather than using a single global φ across all road types. The tutorial explicitly motivates using family-specific SPFs as the "similar entities" reference.
- Action type: candidate model extension (future)
- Relevant stage: Stage 2 / facility-family split
- Why the paper supports it: The SPF defines what "similar entities" means for the EB prior; a single global SPF applied to motorways and minor urban roads simultaneously is a poor prior for either class. Per-family SPFs with per-family φ would give correctly calibrated EB weights.
- Evidence: Section 3, p. 3–4: SPF is defined for "a certain kind of road in a given jurisdiction"; the concept of "similar entities" requires homogeneous facility families
- Effort: medium-high
- Risk if implemented badly: Motorway over-fitting noted as a known issue in existing facility-family v1; φ estimation with small within-family sample sizes is unstable

---

## 16. Query Tags

- empirical-bayes
- SPF
- safety-performance-function
- EB-shrinkage
- regression-to-mean
- overdispersion-parameter
- negative-binomial
- weight-formula
- AADT-exposure
- segment-level
- intersection-level
- severity-split-EB
- full-EB-procedure
- year-specific-ADT
- AMF
- accident-modification-factor
- sparse-collision-counts
- zero-heavy-counts
- tutorial-methods-reference
- UK-transferable

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper:
  - The SPF calibration procedure (negative binomial regression to obtain φ) is referenced to Hauer (1997) and Hauer (2001) but not derived or detailed here; implementation of correct φ estimation requires those references
  - Formal multivariate EB for severity (Flowers 1981; Heydecker and Wu 1991) is referenced as the correct method for severity-split EB but not described; obtaining these older references may be necessary if severity-split EB is prioritised
  - No empirical validation of the EB method's performance is provided in this document; the tutorial assumes the theoretical optimality properties (minimum variance estimator) as established in Hauer (1997)
- Parts of the paper that need manual checking:
  - Example 6 (intersection) references "Vogt and Bared (7)" for the intersection SPF but labels this as reference 7 in-text while the reference list shows Hauer et al. (1989) as reference 7 for signalized intersections; Vogt and Bared (1998) is reference 10. This appears to be a citation numbering error in the original document. The SPF formula quoted (6.54×10^-5 × ADTmainline × ADTminor) should be verified against Vogt and Bared (1998) if this example is used as a reference.
  - Equation 6 (weight for correlated intersections, ρ_ij = 1) contains a nested square root expression; the typesetting in the PDF should be verified against Hauer (1997) if this formula is implemented.
- Any likely ambiguity or risk of misinterpretation:
  - The tutorial uses "µ" for both the SPF-predicted rate (accidents/km-year) and implicitly for the expected count η = µ×L×Y; these are different quantities and the notation is context-dependent. When implementing the weight formula, η (the expected count over the observation period) is what enters equation 2, not the rate µ alone. The tutorial is careful about this but the notation could cause confusion in code.
  - The overdispersion parameter φ is "per unit length" for segments. If φ is estimated in units of 1/km and L is in metres, the weight formula will be wrong. Units must be consistent throughout.
  - The ad-hoc correction ratio for severity-split EB (23.92/20.35 = 1.118 in Example 5) is presented as a practical approximation, not a theoretically correct fix. It should not be presented as equivalent to the formal multivariate EB approach.
