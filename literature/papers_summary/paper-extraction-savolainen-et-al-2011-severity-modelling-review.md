# Paper Extraction: Savolainen et al. (2011) — The Statistical Analysis of Highway Crash-Injury Severities: A Review and Assessment of Methodological Alternatives

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: Savolainen-Mannering-AAP-2011.pdf
- Suggested Markdown filename: paper-extraction-savolainen-et-al-2011-severity-modelling-review.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered in context as page images + text)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 11-page paper accessible. Table 1 (model taxonomy) fully legible. Note: this paper is a methodological review, not an empirical study. Most extraction sections are either "not applicable" or produce documentation-relevant notes rather than data-driven findings.

---

## 1. Citation

- Title: The statistical analysis of highway crash-injury severities: A review and assessment of methodological alternatives
- Authors: Peter T. Savolainen, Fred L. Mannering, Dominique Lord, Mohammed A. Quddus
- Year: 2011
- DOI or URL, if present: doi:10.1016/j.aap.2011.03.025
- Journal: Accident Analysis and Prevention 43 (2011) 1666–1676
- Country / region studied: Not applicable — review paper, primarily US literature
- Study setting: Not applicable — review

---

## 2. Core Objective

- One-sentence description: The paper reviews the methodological landscape for modelling crash-injury severity as a discrete outcome (from no-injury to fatal), covering ordered and unordered logit/probit models, mixed logit, Bayesian approaches, and data issues including underreporting, endogeneity, and spatial/temporal correlation.
- Main purpose: methodological review / reference taxonomy
- Evidence quote or page reference: "The intent of this paper is to provide a similar assessment of data characteristics and methodological alternatives and limitations for examining crash-severity data." (p. 1666)

---

## 3. Response Variable

- Target variable: Crash-injury severity at the individual crash or occupant level, typically categorised as the KABCO scale: Fatal (K), Incapacitating injury (A), Non-incapacitating (B), Possible injury (C), Property damage only (O)
- Collision type: All crash types; review covers literature across road types and crash configurations
- Severity handling: Severity is the dependent variable; this paper is about severity modelling, not frequency modelling
- Count, binary, rate, risk score, severity class, or other: discrete ordinal or nominal category
- Time window used for outcomes: Not applicable — review
- Evidence quote or page reference: "Injury-severity data are generally represented by discrete categories such as fatal injury or killed, incapacitating injury, non-incapacitating, possible injury, and property damage only." (p. 1667)

---

## 4. Exposure Handling

- Exposure variable used: Not applicable — severity models condition on a crash having occurred; exposure to risk (traffic volume, VMT) is not part of the severity modelling problem
- Notes relevant to Open Road Risk: The paper explicitly notes (footnote 1, p. 1666) that joint frequency-severity models are limited to non-crash-specific data: "models that simultaneously consider frequency and severity can only use non-crash-specific data (roadway geometry, traffic volumes, etc.)." This is a direct statement about the data available to Open Road Risk's Stage 2 — which uses exactly those variables. The implication is that if Open Road Risk ever extends to severity modelling, a joint approach would be feasible with existing features, but a pure severity model would require per-crash data (vehicle type, occupant age, restraint use) that are not currently in the pipeline at link level.
- Transferability to my AADF/WebTRIS setup: Not applicable for severity modelling; medium relevance as a design reference if joint frequency-severity is considered

---

## 5. Spatial Unit of Analysis

- Unit: Individual crash (disaggregate); not a link-level or area-level model
- Relevance to OS Open Roads link-based pipeline: Low direct relevance. Severity models operate at the crash level (one observation per crash or occupant), whereas Open Road Risk operates at link × year level. Aggregating severity outcomes to link × year (e.g., fraction of crashes that are serious or fatal) is possible but would require a different modelling approach than reviewed here.

---

## 6. Temporal Unit of Analysis

- Not applicable — review paper; individual crash-level data with no temporal structure discussed
- Relevance to WebTRIS-style time profiles: Not applicable

---

## 7. Engineered Features

Not applicable — review paper. The paper identifies common explanatory variables used in the severity literature across many studies, but does not engineer features from a specific dataset. Variables commonly found in the literature include: road class, speed limit, lighting, weather, vehicle type, occupant age/gender, restraint use, alcohol involvement, crash type. Several of these are already in Open Road Risk's feature set or are candidate features.

---

## 8. Model Architecture — Summary of Reviewed Methods

This section summarises the model taxonomy from Table 1 and the text, for reference.

**Binary outcome models:** Binary logit/probit (injury vs. no-injury); bivariate/multivariate binary probit (for endogeneity or within-crash correlation); Bayesian hierarchical binary logit.

**Ordered discrete outcome models:** Ordered logit/probit (most common); heteroskedastic ordered logit (variance as function of covariates); generalised ordered logit (relaxes proportional odds assumption); partial proportional odds model; bivariate ordered probit (for endogeneity); Bayesian ordered probit; mixed generalised ordered logit (random parameters + generalised thresholds); copula-based multivariate ordered approach (for within-crash correlation).

**Unordered multinomial models:** Multinomial logit (MNL); nested logit (relaxes IIA); sequential logit/probit; Markov switching multinomial logit; mixed logit / random parameters logit (most flexible; accounts for unobserved heterogeneity by allowing parameters to vary across observations).

**Other:** Artificial neural networks; classification and regression trees.

**Key model selection guidance from the paper:**
- Ordered models are susceptible to underreporting bias and impose proportional odds restrictions that may not hold.
- MNL is susceptible to IIA violations and within-crash correlation.
- Mixed logit is the most flexible but computationally expensive; it handles unobserved heterogeneity that fixed-parameter models miss.
- For small samples, simpler fixed-parameter models may be preferred.
- The appropriate model depends heavily on available data and sample size.

---

## 9. Key Data Issues Relevant to Open Road Risk

These are the paper's data characteristic discussions most relevant to Open Road Risk's design, even though severity modelling is not the pipeline's current focus.

**Underreporting (Section 2.1):**
- Hauer and Hakkert (1989) meta-analysis: approximately 20% of severe injuries, 50% of minor injuries, and up to 60% of no-injury crashes are not reported to police.
- Elvik and Myssen (1999) meta-analysis: underreporting rates of 30%, 75%, and 90% for serious, slight, and very slight injuries respectively.
- NHTSA (2009): 25% of minor injury crashes and 50% of no-injury crashes unreported; fatal crashes nearly 100% reported.
- **Relevance to Open Road Risk:** Open Road Risk uses STATS19-style injury collision data, which excludes property-damage-only crashes by definition. The outcome variable "injury collision count" therefore mixes fatals, serious, and slight injuries, each with different reporting rates. Fatal and serious injury counts are more complete; slight injury counts are more underreported. This means the Stage 2 model outcome is biased toward under-counting slight injuries, particularly on lower-traffic links where police reporting rates may be lower. This is a known limitation worth documenting.
- Evidence quote: "approximately 20 percent of severe injuries, 50 percent of minor injuries, and up to 60 percent of no-injury crashes are not reported." (p. 1667, citing Hauer and Hakkert, 1989)

**Ordinal nature of severity data (Section 2.2):** Not directly applicable to Open Road Risk's frequency model, but relevant if severity weighting is added.

**Omitted variable bias (Section 2.4):** Directly applicable. Open Road Risk's Stage 2 GLM and XGBoost models omit many variables that influence both crash frequency and severity (individual driver behaviour, vehicle fleet composition, precise junction geometry). The paper confirms this is a standard limitation.

**Endogeneity (Section 2.6):** Not currently a concern for Open Road Risk's link-level features, but would become relevant if post-crash variables (e.g., collision-derived speed estimates) were used as features — which the pipeline explicitly excludes.

**Spatial and temporal correlations (Section 2.8):** The paper identifies this as an unresolved challenge: "crashes that occur in close proximity in space or in time are likely to share unobserved effects." This is directly relevant to Open Road Risk's panel structure. The paper notes that "the complexity of the model structure when discrete data are involved is a major barrier to model development" — consistent with the Quddus (2007) INAR paper's finding that serial correlation is difficult to address for count data at fine spatial/temporal resolution.
- Evidence quote: "If such correlations are ignored, there will be a loss of efficiency and parameters will be estimated with less precision." (p. 1668)

**Joint frequency-severity models (footnote 1, p. 1666):** The paper notes that joint models "can only use non-crash-specific data (roadway geometry, traffic volumes, etc.)" — which is exactly what Open Road Risk uses. This confirms that a joint frequency-severity extension to Stage 2 would be technically compatible with the existing feature set.

---

## 10. Reported Metrics / Quantitative Results

Not applicable — review paper. No empirical model is estimated. The paper references log-likelihood, McFadden ρ², AIC/BIC, and likelihood ratio tests as model comparison criteria in the reviewed literature, but does not report specific values.

---

## 11. Validation Strategy

Not applicable — review paper. The paper identifies the lack of external validation as a general weakness in the severity modelling literature but does not address it methodologically.

---

## 12. Key Findings Relevant to My Project

**Finding 1**
- Finding: Joint frequency-severity models are limited to non-crash-specific data (road geometry, traffic volumes), which is precisely the data available to Open Road Risk. If a severity dimension is ever added to Stage 2, a joint approach is feasible without requiring per-crash data.
- Why it matters: Validates that the current feature set (road classification, AADT, length, geometry, land use) could support a joint frequency-severity model extension without needing post-crash data.
- Evidence quote: "models that simultaneously consider frequency and severity can only use non-crash-specific data (roadway geometry, traffic volumes, etc.)" (footnote 1, p. 1666)
- Confidence: **high** — explicit statement, not an inference

**Finding 2**
- Finding: STATS19-style police-reported crash data systematically underreports slight injuries (~75% underreporting) and especially no-injury crashes (~90% underreporting), while fatal crashes are nearly 100% reported. The reporting rate is outcome-dependent, creating a non-random sample that can bias parameter estimates.
- Why it matters: Open Road Risk's Stage 2 outcome (injury collision count) mixes crash severities with different reporting rates. Links with predominantly slight-injury crashes will be more underrepresented than links with fatal/serious crashes. This creates a systematic bias in the exposure-adjusted risk estimate for lower-severity, lower-traffic links.
- Evidence quote: "Elvik and Myssen (1999) found underreporting rates of 30, 75, and 90 percent for serious, slight, and very slight injuries, respectively." (p. 1667)
- Confidence: **high** for the general pattern; **medium** for the specific magnitude in UK STATS19 data (these figures are from a US/European meta-analysis)

**Finding 3**
- Finding: Spatial and temporal correlations among crash observations at the same location or in the same time period introduce unobserved shared effects. Standard discrete outcome models (and by extension, Poisson/NB count models) that ignore such correlations produce less precise parameter estimates. This remains an unresolved challenge even in severity modelling.
- Why it matters: Consistent with the serial correlation concern raised by Quddus (2007). Corroborates that Open Road Risk's grouped-by-link validation split and cluster-robust standard errors are the right direction, even if full spatial autocorrelation modelling is not feasible.
- Evidence quote: "crashes that occur in close proximity in space ... or in time ... are likely to share important unobserved effects. If such correlations are ignored, there will be a loss of efficiency." (p. 1673)
- Confidence: **high** — methodological consensus point

**Finding 4**
- Finding: Ordered probability models impose a proportional odds assumption (parameters have the same sign and relative magnitude across all severity levels) that is often violated in practice. This restriction can produce incorrect inferences about specific severity outcomes. The generalised ordered logit or mixed logit relaxes this restriction.
- Why it matters: If Open Road Risk ever models severity as an ordered outcome (e.g., predicting KSI vs. slight injury rates per link), the proportional odds assumption should be tested with a Brant test before defaulting to ordered logit. A generalised ordered logit or multinomial logit would be more flexible.
- Evidence quote: "traditional ordered probability models cannot account for this possibility because the shift in thresholds are constrained to move in the same direction. This is a major restriction of the ordered probability approach." (p. 1670)
- Confidence: **high** for the methodological limitation; **low** for direct applicability to Open Road Risk's current models (which are count models, not severity models)

**Finding 5**
- Finding: The mixed logit (random parameters logit) is the most flexible discrete outcome model for severity data, accounting for unobserved heterogeneity by allowing parameters to vary across observations. It is computationally expensive but tractable for individual-crash datasets of typical size.
- Why it matters: If a future severity model is added to Open Road Risk (e.g., predicting KSI fraction per link-year), the mixed logit is the recommended approach in the literature, particularly for pedestrian/cyclist crashes where individual vulnerability varies widely. Python has scikit-learn and pylogit implementations; R has mlogit.
- Evidence quote: "The mixed logit addresses the limitations of the multinomial logit by allowing for heterogeneous effects and correlation in unobserved factors." (p. 1672)
- Confidence: **high** for the methodological recommendation; **medium** for feasibility at Open Road Risk's link × year aggregation level

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement (future extensions)

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Joint frequency-severity model (Bayesian multivariate Poisson + ordered logit, as in Ma & Kockelman 2006 or Park & Lord 2007 cited in footnote 1) | Would add a severity dimension to Stage 2; feasible with existing link-level features | Severity-weighted crash counts per link × year (derivable from STATS19 KSI flag) | Individual crash level in cited papers | Medium: link × year aggregation loses individual crash detail; aggregate severity share is feasible | Future Stage 2 extension | High | Link-level KSI fraction is sparse; model may not be identifiable at fine link granularity |
| Severity weighting of Stage 2 outcome (e.g., weight crashes by STATS19 severity code before aggregating to link × year) | Distinguishes KSI from slight injuries in the risk index; more policy-relevant | STATS19 severity codes; already available | Not applicable | Compatible; low implementation complexity | Stage 2 / candidate extension | Low–medium | STATS19 severity codes have known classification inconsistencies between police forces |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Open Road Risk scale compatibility | Confidence |
|---|---|---|---|---|
| Individual-crash severity models (MNL, ordered logit, mixed logit at crash level) | Require per-crash covariates (vehicle type, occupant age, restraint use, alcohol) not available at link level | Post-crash covariates not in pipeline | Very low at production scale | High |
| Copula-based within-crash correlation models | Require multiple injury observations per crash; link × year aggregation loses this structure | Individual occupant injury records | Very low | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Not directly — severity models condition on crash occurrence and do not use traffic exposure. The paper's note on joint models confirms the exposure features already in Stage 2 are the right inputs for any future extension.

- **Does it suggest better handling of AADT/AADF uncertainty?** No.

- **Does it suggest useful geometry or road-context features?** Indirectly — road class, speed limit, lighting, geometry appear consistently significant in the severity literature and are candidate or existing features in Stage 2.

- **Does it suggest better modelling of junctions?** No specific junction modelling contribution, though intersection vs. mid-block distinction appears in several cited studies.

- **Does it suggest better treatment of severity?** Yes — the paper provides the reference framework for adding a severity dimension to Stage 2 if desired. The underreporting section is directly relevant to interpreting STATS19-based outcomes.

- **Does it suggest better validation design?** No new validation methodology beyond what is already in the pipeline.

- **Does it expose a weakness in my current approach?** Two relevant weaknesses:
  1. Open Road Risk's Stage 2 outcome (total injury collision count) mixes crash severities with different reporting rates. Slight injuries are substantially underreported. This means the risk index is biased toward under-counting slight-injury crashes, particularly on lower-traffic links.
  2. Spatial and temporal correlations among crash observations at the same link across years remain unaddressed in the standard Poisson GLM (corroborating Quddus 2007).

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add a documentation note to Stage 2 model notes stating that the STATS19 injury collision outcome mixes severities with substantially different police-reporting rates (approximately 30% underreporting for serious, 75% for slight, per Elvik & Myssen 1999). This means the Stage 2 risk index reflects the reported injury collision rate, not the true injury collision rate, with a systematic bias toward undercounting slight injuries.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Section 2.1 and citing Elvik & Myssen (1999); Hauer & Hakkert (1989)
- Evidence quote: "Elvik and Myssen (1999) found underreporting rates of 30, 75, and 90 percent for serious, slight, and very slight injuries, respectively." (p. 1667)
- Effort: low
- Risk if implemented badly: none (documentation only)

**Action 2**
- Suggested repo action: Add a candidate future feature to the Stage 2 backlog: KSI-weighted crash count per link × year (where KSI = killed + seriously injured), derived from STATS19 severity codes. Compare the KSI-weighted risk percentile against the unweighted risk percentile to assess whether the severity dimension identifies meaningfully different high-risk links.
- Action type: candidate feature / diagnostic
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Footnote 1 confirms joint frequency-severity is feasible with non-crash-specific features; the underreporting discussion motivates severity stratification.
- Evidence quote: Footnote 1 (p. 1666)
- Effort: low–medium
- Risk if implemented badly: STATS19 KSI classification has known inconsistencies across police forces and over time; treat as diagnostic, not production change.

**Action 3**
- Suggested repo action: Add a documentation note that Open Road Risk's feature set (road geometry, AADT, land use, etc.) is compatible with joint frequency-severity modelling as described in the literature (Ma & Kockelman 2006; Park & Lord 2007). Flag this as a potential future extension if a severity dimension is prioritised.
- Action type: documentation note
- Relevant stage: documentation / future Stage 2 extension
- Why the paper supports it: Footnote 1 explicitly identifies non-crash-specific data as the appropriate input for joint models.
- Effort: low
- Risk if implemented badly: none

---

## 16. Query Tags

- severity-modelling-review
- discrete-outcome-models
- ordered-logit-probit
- mixed-logit
- random-parameters
- unobserved-heterogeneity
- underreporting-bias
- STATS19-severity
- KSI-weighting
- joint-frequency-severity
- spatial-temporal-correlation
- endogeneity
- IIA-assumption
- proportional-odds
- crash-data-characteristics
- US-literature
- reference-taxonomy
- not-transferable-directly

---

## 17. Confidence and Gaps

- Overall confidence in extraction: **high** for what the paper covers; the paper is a review so there are no primary empirical results to misinterpret
- Important details not stated in the paper:
  - UK-specific underreporting rates for STATS19 are not provided; the rates cited are from US/European meta-analyses. Actual STATS19 underreporting rates should be verified against UK sources (e.g., TRL or DfT underreporting studies) before using these figures in documentation.
  - The paper does not address the case where severity data is aggregated to link × year level (as in Open Road Risk); all reviewed models operate at individual crash level.
- Parts of the paper that need manual checking: None — this is a clean methodological review with no complex empirical results.
- Any likely ambiguity or risk of misinterpretation:
  - The paper reviews severity modelling (predicting injury level given a crash), not frequency modelling (predicting crash counts). Do not cite this paper as evidence for or against any Stage 2 frequency modelling choice except where explicitly noted above (underreporting, joint models, spatial correlation).
  - The underreporting figures cited are from 1989–1999 studies; UK STATS19 reporting rates may have changed, particularly with increased minor injury reporting from insurance requirements.
