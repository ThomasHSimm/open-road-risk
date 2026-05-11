# Paper Extraction: Qin et al. (2006) — Bayesian Estimation of Hourly Exposure Functions by Crash Type and Time of Day

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: AAP-2006-Hourlyexposure-1tfliyv_Bayesian_estimation_of_hourly_exposure_functions_by_crash_type_and_time_of_day.pdf
- Suggested Markdown filename: paper-extraction-qin-et-al-2006-bayesian-hourly-exposure.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered in context as page images + text)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 10-page paper accessible. Figures 1–3 (predicted crash curves) and Tables 6–7 (MCMC exponent comparisons) visible. Some right-column text on pages 3, 5, 9 partially truncated in OCR rendering but core content recoverable. Table 2 crash counts fully legible.

---

## 1. Citation

- Title: Bayesian estimation of hourly exposure functions by crash type and time of day
- Authors: Xiao Qin, John N. Ivan, Nalini Ravishanker, Junfeng Liu, Donald Tepas
- Year: 2006
- DOI or URL, if present: doi:10.1016/j.aap.2006.04.012
- Journal: Accident Analysis and Prevention 38 (2006) 1071–1080
- Country / region studied: USA — Michigan and Connecticut
- Study setting: rural two-lane highways

---

## 2. Core Objective

- One-sentence description: The paper estimates the relationship between crash occurrence probability and hourly traffic volume, separately by crash type (single-vehicle, multi-vehicle same/opposite/intersecting direction) and three time-of-day periods, using hierarchical Bayesian binary regression.
- Main purpose: safety performance function estimation / exposure function estimation / predictive modelling by crash type and time of day
- Evidence quote or page reference: "The subject of this research is to formulate and estimate disaggregate crash prediction models of the actual hourly volume and segment length based on functions that are proportional to crash incidence, and whose parameters vary by crash type and by time of day." (p. 1072)

---

## 3. Response Variable

- Target variable: Binary indicator of crash occurrence within a one-hour observation period at a road segment
- Collision type: Injury/all crashes — the paper does not specify injury-only vs. all reported crashes; it uses police-reported crash records from HSIS (Michigan) and ConnDOT (Connecticut); severity is not stated as a filter
- Severity handling: Not modelled separately; four crash types by movement direction, not by severity
- Count, binary, rate, risk score, severity class, or other: binary (0/1 per segment-hour); "Here, the time interval is an hour, therefore the corresponding number of crashes is unlikely to exceed one." (p. 1072)
- Time window used for outcomes: One-hour intervals; study periods: Michigan 1995–1997, Connecticut 1995–2000
- Evidence quote or page reference: "the dependent variable can be defined as crash occurrence denoted by a binary indicator assuming either zero or one." (p. 1072)

---

## 4. Exposure Handling

- Exposure variable used, if any: Hourly directional volume (v1 and v2, one per direction of travel on a two-lane highway); combined as either additive (v1 + v2) or multiplicative (v1 × v2) exposure functions; also segment length L
- Traffic count source: Automatic Traffic Recorders (ATR) from Michigan DOT and Connecticut DOT, co-located with or near study segments; not AADT from sparse counts
- Whether exposure is modelled, observed, assumed, or ignored: Directly observed hourly counts from permanent ATR stations; this is the study's key departure from AADT-based approaches
- Treatment of missing or sparse traffic counts: Not explicitly addressed; the design requires ATR co-location with crash segments; segments without ATR coverage are excluded
- Whether offset terms, rates, denominators, or normalisation are used: Exposure enters as a power function inside a logit-link binary GLM (Equations 4–5), not as a log-offset in the Poisson sense. The exponent on volume (αv) is estimated; when αv = 1 the relationship is linear (proportional), and the paper demonstrates αv ≠ 1 throughout.
- Evidence quote or page reference: "the crash exposure proposed in this study is a function of the hourly volume and segment length with significant exponents different from one in each case." (p. 1079)
- Transferability to my AADF/WebTRIS setup: **mixed — see notes**
- Notes:
  - The *conceptual contribution* — that hourly volume is a better exposure measure than AADT, and that the flow-crash relationship varies by crash type and time of day — is highly transferable and directly relevant to Stage 1b and Stage 2.
  - The *data requirement* — continuous per-segment ATR counts — does not transfer. Open Road Risk has AADF sparse counts for a subset of links, and Stage 1b WebTRIS profiles for a subset of road types, not hourly counts for every segment. This is the dominant transferability constraint.
  - The additive vs. multiplicative exposure function distinction (Equations 4–5) applies to two-lane two-directional flow; this is specific to the rural two-lane setting. Open Road Risk covers mixed road types. For motorways and urban roads, the directionality structure differs.
  - The finding that αv ≠ 1 (non-linearity between crash occurrence and hourly volume) is consistent with the Mensah & Hauer (1998) argument-averaging analysis and supports Open Road Risk's use of log(AADT) as an exposure offset with an estimated exponent rather than a fixed proportional offset.

---

## 5. Spatial Unit of Analysis

- Unit: road segment
- Segment length or segmentation rule: Michigan — variable length segments from HSIS, range 0.01–6 miles, mean 1.66 miles; Connecticut — fixed 0.5-mile (approx. 0.8 km) segments defined to be homogeneous and contiguous to ATR stations
- How crashes are assigned to the network: Pre-assigned by state DOTs; not described in detail; geometric features cross-referenced with photolog archive for Connecticut
- Treatment of junctions/intersections: Not addressed; study is for mid-block segments on rural two-lane highways
- Spatial aggregation risks: Variable segment length in Michigan may conflate heterogeneous road conditions within a segment; acknowledged implicitly by the inclusion of segment length L as a covariate
- Evidence quote or page reference: "For Connecticut, we defined one-half mile (about 0.8 km) segments, each with homogeneous cross-sectional features, close to the ATR stations." (p. 1073)
- Relevance to OS Open Roads link-based pipeline: The segment-level binary response structure is conceptually compatible with Open Road Risk's link × year framework. However, the hourly temporal resolution (requiring ATR) cannot be replicated at Open Road Risk scale. The finding that segment length is a significant covariate with estimated exponent αL ≠ 1 is relevant to Open Road Risk's use of log(length) in the exposure offset.

---

## 6. Temporal Unit of Analysis

- Years covered: Michigan 1995–1997 (3 years); Connecticut 1995–2000 (6 years)
- Temporal resolution: Hourly (the fundamental observation unit is one segment-hour)
- Whether seasonality or time-of-day is modelled: Time-of-day is the primary stratification variable; three shifts: 7am–3pm, 3pm–11pm, 11pm–7am. Year indicators included as fixed effects to absorb year-to-year variation. Seasonality within year not modelled.
- Whether before-after or panel structure is used: Panel (multiple years per segment), with year fixed effects; not a before-after study
- Evidence quote or page reference: "We selected time periods of 7 a.m.–3 p.m., 3 p.m.–11 p.m. and 11 p.m.–7 a.m. in order to be consistent with commonly defined work shifts." (p. 1073)
- Relevance to WebTRIS-style time profiles: **Directly relevant.** The paper's three-shift structure is coarser than WebTRIS peak/pre-peak/off-peak, but the conceptual motivation is the same: the flow-crash relationship differs by time of day, and collapsing to AADT obscures this. The paper provides empirical evidence (from two US states, two-lane rural) that time-of-day stratification significantly changes the estimated flow exponent αv for at least some crash types. This supports documenting Stage 1b outputs as a candidate for Stage 2 conditioning.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Hourly volume v1, v2 (directional) | ATR permanent counters | Direct hourly count per direction | Core exposure variable; replaces AADT; allows non-linear, time-varying flow-crash relationship | Low at production scale: requires ATR co-location; not available for 2.17M links. Partial via Stage 1b time fractions × AADT |
| Additive exposure v1 + v2 | ATR | Sum of directional hourly volumes | Exposure proxy for single-vehicle and non-directional conflict types | Partial: derivable approximately as AADT × time fraction |
| Multiplicative exposure v1 × v2 | ATR | Product of directional hourly volumes | Proxy for opposing-direction conflict opportunities (head-on, crossing) | Low: requires directional split per hour; not available at scale |
| Segment length L | Road inventory / GIS | Raw field, log-transformed as ln(L) in model | Controls for exposure proportional to segment length; exponent αL estimated, found ≠ 1 | Already present in Open Road Risk; compare exponent assumption |
| Pavement width W | Road inventory / photolog | Raw field | Controls for road geometry; sign inconsistent across states | Partially available via OSM; sparse coverage |
| Speed limit S | Road inventory | Raw field | Controls for speed environment; sign inconsistent across states | Already present / candidate feature via OSM |
| Year indicators | Administrative | Binary dummy per year | Absorbs secular trend and year-to-year variation | Already present in Open Road Risk panel structure (year as feature) |
| AADT (V) | DOT records | Annual average; included as covariate (not offset) alongside hourly volume | Controls for site-level average flow; ln(V) coefficient in Tables 3–4 | Already present; relevant comparison: paper includes both hourly volume and AADT simultaneously |

---

## 8. Model Architecture

- Algorithms/models used: Hierarchical Bayesian binary logistic regression; MCMC estimation via Gibbs sampling and Metropolis-Hastings algorithm
- Baseline model: Not stated explicitly; the paper compares additive vs. multiplicative exposure specifications within the Bayesian framework
- Final/preferred model: Neither additive nor multiplicative is definitively preferred; pseudo-Bayes factors (PsBF) show weak differences (all PsBF < 3.0 by Raftery criteria); additive model preferred for simplicity since it does not require directional volume split
- Loss function or likelihood, if stated: Binary logistic likelihood (Bernoulli); posterior ∝ likelihood × diffuse Normal prior N(0, σ²I)
- Offset/exposure term, if used: No log-offset in the Poisson sense; exposure enters as a power function η = (v1 + v2)^αv · L^αL inside the logit link (Equations 4–5). The exponent αv is estimated, not fixed at 1.
- Spatial autocorrelation handling: Not addressed
- Temporal dependence handling: Year fixed effects only; within-year serial correlation across hours not modelled
- Interpretability method: Posterior means and credible intervals for each parameter reported in Tables 3–4; pairwise MCMC comparison of αv across crash types in Tables 6–7; predicted crash curves in Figures 1–3
- Evidence quote or page reference: Equations 1–5 (pp. 1074–1075); "The Metropolis-Hastings algorithm creates a sequence of random points, whose distribution converges to the target posterior distribution." (p. 1074)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model selection | Pseudo-Bayes factor (PsBF) | All values < 3.0 (range ~0.25–3.39) | Additive vs. multiplicative, all crash types and time periods, both states | Weak evidence for either model; no confident conclusion on directional split necessity | Table 5, p. 1077 |
| Exponent on hourly volume αv | Posterior mean, additive model | Connecticut SV 7am–3pm: −0.396; SV 3pm–11pm: −0.051; SV 11pm–7am: −0.004 | Single-vehicle crashes, Connecticut | SV crash probability decreases or is flat with increasing hourly volume in daytime; near-zero at night | Table 3, p. 1076 |
| Exponent on hourly volume αv | Posterior mean, additive model | Connecticut SD 7am–3pm: 0.392; SD 3pm–11pm: 0.795 | Same-direction multi-vehicle crashes, Connecticut | Multi-vehicle crashes increase with hourly volume; effect stronger in evening peak | Table 3, p. 1076 |
| Exponent on hourly volume αv | Posterior mean, additive model | Michigan SV 7am–3pm: 0.197; SV 3pm–11pm: −0.145; SV 11pm–7am: 0.477 | Single-vehicle crashes, Michigan | SV exponent sign varies by time of day; not consistent with Connecticut | Table 4, p. 1076 |
| MCMC pairwise comparison of αv | 95% credible interval excludes zero | SV vs. SD: significant at 7am–3pm and 3pm–11pm for both states; not at 11pm–7am | Connecticut and Michigan | Crash types differ significantly in their flow-crash relationship during daytime and evening; converge at night | Tables 6–7, pp. 1077–1078 |
| Linearity test | 95% credible interval for αv excludes 1.0 | Significant for most crash types and time periods | Both states | Flow-crash relationship is non-linear; proportional crash rate assumption rejected | p. 1078 |
| Predicted crash occurrence curves | Graphical | SV: decreasing or flat with volume at some times; SD: increasing concave; OD: low and flat; ID: intermediate | Connecticut, Figures 1–3 | Crash type strongly determines the shape of the SPF; mixing types in one model obscures this | Figures 1–3, pp. 1077–1079 |

**Validation status:** Results are **in-sample posterior estimates** from a Bayesian MCMC fit. No held-out test set, no spatial cross-validation, no temporal holdout. The pseudo-Bayes factor (CPO-based) is a leave-one-out cross-validation approximation and provides some internal model comparison, but does not constitute external predictive validation.

**What these metrics test:** Primarily model fit and parameter credibility within the training data. The CPO/PPD criterion tests relative model comparison (additive vs. multiplicative), not absolute predictive accuracy on unseen segments or time periods.

**Likely optimism:** High. Small sample (32 segments Michigan, 17 Connecticut). Posterior means may not generalise to other road types, regions, or segment samples. The authors explicitly acknowledge this: "the small sample size limited the prediction accuracy and significance of the covariates." (p. 1079)

**Most relevant metric to Open Road Risk:** The pairwise MCMC comparison of αv across crash types and time periods (Tables 6–7), which provides evidence that (a) single-vehicle vs. multi-vehicle distinction is statistically meaningful, and (b) time-of-day stratification changes the flow-crash relationship significantly for at least some crash types.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: The binary formulation (0/1 per segment-hour) sidesteps the zero-inflation problem by construction: at hourly resolution, crashes exceeding 1 per segment-hour are negligible, so the Bernoulli model is appropriate. This is the paper's structural solution to the rare-event problem.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other: Binary logistic regression (Bernoulli likelihood); not Poisson or negative binomial
- Whether high-risk locations are evaluated separately: Not addressed
- Evidence quote or page reference: "the time interval is an hour, therefore the corresponding number of crashes is unlikely to exceed one. Consequently, the dependent variable can be defined as crash occurrence denoted by a binary indicator." (p. 1072)
- Practical relevance to my sparse collision link-year dataset: Medium. Open Road Risk operates at link × year resolution, not segment × hour. At that resolution, crash counts > 1 per link-year are common on high-flow links, so the binary trick does not directly apply. However, the conceptual point — that temporal disaggregation reduces the zero-heavy count problem — is relevant: at shorter time windows, the Bernoulli approximation improves, and the function-averaging problem (Mensah & Hauer 1998) is reduced.

---

## 11. Validation Strategy

- Train/test split method: None; all data used for posterior estimation
- Spatial holdout used? No
- Temporal holdout used? No
- Grouped holdout used? No
- Cross-validation type: CPO (conditional predictive ordinate) / leave-one-observation-out approximation via MCMC, used for model *selection* (additive vs. multiplicative), not for predictive validation
- Metrics: Pseudo-Bayes factor (PsBF) based on log product predictive density (log PPD)
- External validation: None. The authors note: "These findings should be validated and clarified through estimation with a larger data set." (p. 1079)
- Leakage or generalisation risks: Parameter estimates derived from small convenience samples (32 and 17 segments respectively) with ATR co-location requirement. Results may not generalise to other road types, regions, or segments without ATRs. The authors flag inconsistency in parameter signs between Michigan and Connecticut as evidence of limited transferability.
- Evidence quote or page reference: "the exposure factor such as hourly volume and risk factors such as roadway width, speed limit are inconsistent from Connecticut to Michigan, indicating the necessity for calibrating the model for transferability." (p. 1079)
- What I should copy or avoid: **Copy:** the CPO/PPD approach as a model selection criterion for comparing Stage 2 model variants (e.g. with vs. without time-zone fractions). **Avoid:** treating the specific αv estimates as applicable to UK roads; the sign and magnitude vary between states and are not externally validated.

---

## 12. Key Findings Relevant to My Project

**Finding 1**
- Finding: The flow-crash relationship is non-linear for all four crash types and all time periods tested; the exponent αv on hourly volume is significantly different from 1.0 in the majority of cases.
- Why it matters: Open Road Risk's log-exposure offset assumes log(AADT × length × 365 / 1e6), which implicitly treats the crash-exposure relationship as proportional (exponent = 1). This paper provides empirical evidence — from two US states — that the relationship is non-linear. The GLM β coefficient on log(AADT) in Stage 2 should be interpreted as an estimated exponent, not a fixed proportionality assumption. If β ≠ 1 in Stage 2, the pipeline is already implicitly handling this.
- Evidence quote or page reference: "even under models disaggregated by crash type, time of the day with actual hourly volume, the relationship between crash occurrence and traffic volume or segment length is not linear." (p. 1078)
- Confidence: **high** for the non-linearity finding within this case study; **medium** for generalisation to UK road network

**Finding 2**
- Finding: The flow exponent αv for single-vehicle crashes is frequently negative (crash probability decreases as hourly volume increases at some times of day), while multi-vehicle crash types show positive αv. Combining crash types in a single model produces a mixed signal that obscures these opposing relationships.
- Why it matters: Open Road Risk's Stage 2 models total injury collisions as the outcome. The opposing flow-crash relationships for single-vehicle vs. multi-vehicle types will partially cancel, potentially producing a GLM that misestimates both. This is the empirical counterpart to Mensah & Hauer's function-averaging-over-accident-types concern.
- Evidence quote or page reference: "The exponents on hourly volume during a majority of the time periods exhibit a positive relationship for multi-vehicle crash occurrence and a negative one for single-vehicle crash occurrence." (p. 1078)
- Confidence: **medium** — finding is consistent across both states for daytime/evening periods but converges near zero at 11pm–7am; based on small samples

**Finding 3**
- Finding: The flow-crash relationship varies significantly by time of day for at least some crash types; fitting a single annual model conflates conditions with different underlying SPFs. The authors explicitly connect this to circadian factors, light conditions, alcohol/drug use, and trip purpose.
- Why it matters: This is empirical evidence supporting Stage 1b's relevance as a conditioning variable for Stage 2. The paper provides US case-study support for what Mensah & Hauer (1998) argued theoretically: a single annual SPF is a composite of multiple distinct functions.
- Evidence quote or page reference: "For both states, in at least one crash type the exponent on hourly volume varies by time of day, strongly suggesting the necessity of defining crash prediction models by time of day." (p. 1078)
- Confidence: **medium** — statistically demonstrated within these two samples but with small N; direction of effect consistent with theoretical expectation

**Finding 4**
- Finding: Neither additive (v1 + v2) nor multiplicative (v1 × v2) exposure functions significantly outperform each other (all PsBF < 3.0); the additive model is preferred for practical simplicity since it does not require directional volume.
- Why it matters: Open Road Risk does not have directional volume splits for most links. This finding suggests that for the purposes of an exposure function, the two-way (additive) flow is an adequate proxy, and the added complexity of directional data is not justified by model performance.
- Evidence quote or page reference: "The additive exposure model, which does not require directional volume (two-way), is simpler and more commonly accepted." (p. 1077)
- Confidence: **medium** — result is from rural two-lane highways only; directional split may matter more on different road types

**Finding 5**
- Finding: Parameter estimates (signs and magnitudes) for roadway width and speed limit are inconsistent between Michigan and Connecticut, indicating that models fitted to one context require recalibration before transfer to another.
- Why it matters: This is a direct warning against applying US-derived SPF parameters to UK roads without recalibration. It also suggests that Open Road Risk should validate Stage 2 feature coefficients by road type/region rather than assuming they generalise across the full network.
- Evidence quote or page reference: "the exposure factor such as hourly volume and risk factors such as roadway width, speed limit are inconsistent from Connecticut to Michigan, indicating the necessity for calibrating the model for transferability." (p. 1079)
- Confidence: **high** for the transferability limitation; standard finding in road safety literature

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Time-of-day stratification of Stage 2 model (separate models or interaction terms for peak/off-peak) | Provides time-conditioned crash risk estimates; reduces function-averaging bias; aligns with Stage 1b outputs | Stage 1b peak/off-peak fractions; collision time-of-day from STATS19 | 32–49 segments, 2 states | Compatible as a Stage 2 feature or model stratification; STATS19 includes time-of-day for each collision | Stage 2 / candidate feature | Medium | Sparse collision counts per link-year per time band may reduce statistical power; aggregate to facility family first |
| Crash type disaggregation (single-vehicle vs. multi-vehicle) | Avoids function-averaging over accident types; single-vehicle and multi-vehicle have opposing flow relationships | STATS19 collision records include crash type / movement classification | 32–49 segments | Compatible; STATS19 includes collision configuration; requires mapping to SV/MV categories | Stage 2 / candidate model extension | Medium | STATS19 movement coding is less granular than the paper's four-way direction classification; sample sizes per type may be small |
| Non-proportional segment length offset (estimate αL rather than fix = 1) | Paper shows αL estimated ≠ 1 in some cases; current Open Road Risk offset fixes length exponent at 1 | OS Open Roads link length; already in pipeline | 32–49 segments | Compatible; straightforward to test in Stage 2 GLM by freeing length coefficient | Stage 2 / diagnostic | Low | Small improvement likely; link length in OS Open Roads may have its own measurement inconsistencies |
| CPO / pseudo-Bayes factor for Stage 2 model selection | Provides leave-one-out predictive criterion for comparing Stage 2 model variants | Existing Stage 2 model outputs | Not applicable | Compatible with Bayesian Stage 2 variants; approximated via LOO-CV in frequentist frameworks | Stage 2 / validation | Medium | CPO requires MCMC or LOO approximation (e.g. using loo package in R or arviz in Python); not directly available from XGBoost |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Hourly binary model at segment level using ATR counts | Requires per-segment hourly traffic counts from co-located ATRs; not available for 2.17M links | Per-link hourly ATR data | 32–49 segments | Very low: ATR coverage is a tiny fraction of OS Open Roads network | Use AADT × Stage 1b time fraction as approximate hourly volume; apply to road-type aggregates only, not individual links | High |
| Multiplicative exposure v1 × v2 | Requires directional hourly volume split | Directional hourly counts | Same | Very low | Not applicable at scale | High |
| Fully Bayesian hierarchical MCMC at link × year scale | Computationally prohibitive at ~21.7M link-year rows with MCMC | Computational | 32–49 segments × ~8 years × 8760 hours | Very low | Use variational Bayes or empirical Bayes approximations; MCMC feasible only on subsets or road-type aggregates | High |
| Separate SPF by all four crash direction types | STATS19 movement coding is less granular; sample sizes per link-year per type would be extremely sparse | Directional crash classification at link level | Small samples | Low at link level; medium at road-type aggregate level | Binary SV vs. MV split is achievable; four-way directional split is not realistic | Medium |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Yes — it confirms that the flow-crash relationship is non-linear (αv ≠ 1), which validates using an estimated log(AADT) coefficient rather than a fixed proportional offset. The current Stage 2 GLM with log(AADT × length × 365 / 1e6) as offset already partially accommodates this if the GLM β on the offset is not constrained to 1.

- **Does it suggest better handling of AADT/AADF uncertainty?** Indirectly: the paper argues for hourly volume over AADT as exposure, which directly addresses the argument-averaging problem. It does not, however, address AADT estimation uncertainty from sparse counts (Stage 1a concern).

- **Does it suggest useful geometry or road-context features?** Pavement width and speed limit are included but show inconsistent results between states; they are already candidate features in Open Road Risk. The paper does not add novel geometry features.

- **Does it suggest better modelling of junctions?** No — mid-block segments only; junctions explicitly excluded.

- **Does it suggest better treatment of severity?** No — severity not modelled; crash type by movement direction is the focus.

- **Does it suggest better validation design?** Yes, implicitly: the paper's own acknowledged weakness (no external validation, inconsistent inter-state parameters) highlights the need for spatial holdout validation in Open Road Risk. The CPO/PPD framework is a useful internal model comparison tool.

- **Does it expose a weakness in my current approach?** Two weaknesses:
  1. Combining single-vehicle and multi-vehicle crashes in one Stage 2 model conflates opposing flow-crash relationships; this is an empirical counterpart to Mensah & Hauer's function-averaging concern.
  2. Fitting a single Stage 2 model across all time-of-day conditions, without conditioning on peak/off-peak fractions, risks obscuring time-varying risk patterns that Stage 1b is positioned to address.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Add a documentation note to Stage 2 model notes that the total-crash outcome combines single-vehicle and multi-vehicle crashes, which have opposing flow-crash relationships per this paper and Mensah & Hauer (1998). Flag this as a known source of function-averaging ambiguity in the current Stage 2 output.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Tables 3–4 and Figures 1–3 show that SV αv is negative at several time periods while MV αv is positive; combining them produces a mixed signal.
- Evidence quote or page reference: "the relationship between total vehicle crash occurrence and hourly volume may display a U-shape if the relationship for single-vehicle crashes is convex downward while that for multi-vehicle crashes is convex upward." (p. 1079)
- Effort: low
- Risk if implemented badly: none (documentation only)

**Action 2**
- Suggested repo action: Run a diagnostic Stage 2 model stratified by single-vehicle vs. multi-vehicle collision type (derivable from STATS19) and compare GLM β coefficients on log(AADT). Check whether the log(AADT) coefficient differs in sign or magnitude between types. Do not change production output.
- Action type: diagnostic
- Relevant stage: Stage 2
- Why the paper supports it: The paper provides empirical evidence from two US states that SV and MV crash types have meaningfully different and sometimes opposing flow relationships. If this holds in UK data, a combined model is a biased aggregate.
- Evidence quote or page reference: "the exponents on hourly volume during a majority of the time periods exhibit a positive relationship for multi-vehicle crash occurrence and a negative one for single-vehicle crash occurrence." (p. 1078)
- Effort: medium
- Risk if implemented badly: STATS19 collision type coding may not cleanly separate SV/MV at link level with sufficient sample size; aggregate to road type first.

**Action 3**
- Suggested repo action: Test whether including Stage 1b peak/off-peak fraction (or day/night fraction, if derivable from WebTRIS) as a feature in Stage 2 improves out-of-sample log-likelihood or grouped CV R². Compare against current Stage 2 baseline. This is the lowest-cost implementation of the time-of-day conditioning the paper demonstrates is meaningful.
- Action type: baseline comparison / candidate feature
- Relevant stage: Stage 2 / Stage 1b
- Why the paper supports it: The paper demonstrates that the flow exponent varies by time of day for at least some crash types; Stage 1b time fractions are an available proxy for time-of-day conditioning.
- Evidence quote or page reference: "For both states, in at least one crash type the exponent on hourly volume varies by time of day, strongly suggesting the necessity of defining crash prediction models by time of day." (p. 1078)
- Effort: medium
- Risk if implemented badly: WebTRIS coverage is not uniform; missing values may require imputation by road type. Treat as candidate feature, not production change.

**Action 4**
- Suggested repo action: Test whether freeing the log(length) coefficient in Stage 2 (rather than fixing the length exponent at 1 in the offset) improves model fit. The paper shows αL ≠ 1 in at least some subgroups.
- Action type: diagnostic
- Relevant stage: Stage 2
- Why the paper supports it: ln(L) appears with estimated αL in Equations 4–5; in Tables 3–4 the ln(L) coefficients are non-zero for Michigan data (though not always significant for Connecticut fixed-length segments).
- Evidence quote or page reference: ln(L) coefficients in Table 4 (p. 1076), e.g. Michigan 11pm–7am: ln(L) = 0.166 (SV additive), significantly non-zero.
- Effort: low
- Risk if implemented badly: OS Open Roads link lengths vary widely; very short links may have noisy length measurements. Check length distribution before freeing the coefficient.

**Action 5**
- Suggested repo action: Note in documentation that US-derived SPF parameters (including those in this paper) should not be applied directly to UK roads without recalibration. This is supported by the paper's own finding that Michigan and Connecticut parameters are inconsistent with each other.
- Action type: documentation note
- Relevant stage: documentation / Stage 2
- Why the paper supports it: "the exposure factor such as hourly volume and risk factors such as roadway width, speed limit are inconsistent from Connecticut to Michigan." (p. 1079)
- Effort: low
- Risk if implemented badly: none

---

## 16. Query Tags

- hourly-exposure
- binary-response-model
- hierarchical-Bayesian
- MCMC
- Metropolis-Hastings
- crash-type-disaggregation
- single-vehicle-vs-multi-vehicle
- time-of-day-SPF
- non-linear-flow-crash
- flow-exponent
- additive-vs-multiplicative-exposure
- two-lane-rural
- segment-length-exponent
- pseudo-Bayes-factor
- CPO-model-selection
- Stage-1b-relevance
- function-averaging
- ATR-required
- US-only-validation
- small-sample

---

## 17. Confidence and Gaps

- Overall confidence in extraction: **high**
- Important details not stated in the paper:
  - Severity filter not stated (injury-only vs. all reported crashes); assumed to use all police-reported crashes.
  - The paper does not describe the crash spatial matching/snapping procedure in detail.
  - The prior distribution is diffuse Normal N(0, σ²I) with σ² "a large number" — exact value not stated; sensitivity to prior not tested.
  - MCMC chain length, burn-in, and convergence diagnostics not reported in the main paper.
  - The paper does not report segment-level out-of-sample predictive accuracy (only CPO-based model selection).
- Parts of the paper that need manual checking:
  - Tables 6–7 (MCMC pairwise comparison): bold formatting (indicating significance at 5%) visible in context but cross-referencing specific cell values requires care; verify Michigan Table 7 SD v OD row for 3pm–11pm.
  - Figures 1–3: visible in context but precise curve shapes (especially Fig. 3, 11pm–7am) are low-resolution; curves appear nearly flat at this time period, consistent with near-zero αv in Table 3.
- Any likely ambiguity or risk of misinterpretation:
  - The binary logistic model operates at segment × hour resolution; this is fundamentally different from Open Road Risk's Poisson GLM at link × year resolution. The flow exponents αv from this paper cannot be directly compared with Stage 2 GLM β values without accounting for the temporal aggregation (Mensah & Hauer 1998 correction factor applies).
  - The CPO/PPD is used here for model *selection* between additive and multiplicative specifications, not for absolute predictive validation. It should not be interpreted as evidence that the models generalise well to new segments.
  - The negative αv for single-vehicle crashes at some times of day (decreasing crash probability with increasing flow) is a real phenomenon (lower speeds at higher volumes) but may not manifest the same way in annual-aggregate UK data where flow and other risk factors co-vary differently.
