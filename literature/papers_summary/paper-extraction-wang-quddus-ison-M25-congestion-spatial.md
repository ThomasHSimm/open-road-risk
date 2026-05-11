# Paper Extraction — Methodological Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: Wang_et_al_AAP_Final_submitted1.pdf
- Suggested Markdown filename: paper-extraction-wang-quddus-ison-M25-congestion-spatial.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered as document text in context)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 21-page submitted manuscript accessible. Tables 1–3 fully legible. Figures 3 and 4 (scatter plots of accidents vs AADT and CI) present as images but their axes and structure are described in text. Publication venue not explicitly stated in PDF; the filename suffix "_AAP_Final_submitted1" suggests Accident Analysis & Prevention. Year not stated in document; estimated ~2009–2010 based on reference dates. **Check published version for DOI and year.**

---

## 1. Citation

- Title: Impact of Traffic Congestion on Road Safety: A Spatial Analysis of the M25 Motorway in England
- Authors: Chao Wang, Mohammed A. Quddus, Stephen G. Ison
- Year: Not stated in PDF; estimated 2009–2010 from reference dates (most recent cited work is 2008). **Verify against published version.**
- DOI or URL, if present: Not stated
- Country / region studied: England — M25 London orbital motorway
- Study setting: Motorway only (M25, junction-to-junction segments)

---

## 2. Core Objective

- One-sentence description: The paper investigates whether traffic congestion (measured by a precise congestion index) has a statistically significant effect on road accident frequency on the M25, while controlling for traffic flow, segment geometry and road characteristics, using Bayesian Poisson-based spatial and non-spatial models.
- Main purpose: Safety performance function (SPF) — segment-level Poisson count model; causal inference question (congestion → accidents); spatial autocorrelation modelling.
- Evidence quote or page reference: "The aim of this paper is to explore the effects of traffic congestion on road safety using a spatial analysis approach while controlling for the other contributing factors." (p.2)

---

## 3. Response Variable

- Target variable: Count of road accidents per M25 segment over 3-year aggregation period (2004–2006)
- Collision type: Injury collisions only (STATS19); split into two groups: (1) fatal and serious injury combined, (2) slight injury. Damage-only not included.
- Severity handling: Modelled separately — distinct models for KSI (fatal + serious combined due to low fatal counts) and for slight. This mirrors the Wedagama (2008) approach.
- Count, binary, rate, risk score, severity class, or other: Count (with AADT and segment length as exposure-related variables; no formal offset used — see Section 4)
- Time window used for outcomes: 2004–2006 (3-year aggregate). Traffic characteristic data from 2006.
- Evidence quote or page reference: "STATS19 data for 2004 to 2006 were aggregated. This can also ease the variability of accident frequency from year to year." (p.4)

---

## 4. Exposure Handling

- Exposure variable used: log(AADT) and segment length (km) included as standard predictors (not as a formal log-offset with coefficient fixed to 1). AADT is per-lane: "AADT was normalised by the number of lanes (i.e. AADT per lane)" (p.10).
- Traffic count source: UK Highways Agency (UKHA) — hourly traffic characteristic data for 2006 including AADT, average travel time, average travel speed, total vehicle delay. These are full observed counts from a managed motorway, not sparse AADF estimates.
- Whether exposure is modelled, observed, assumed, or ignored: Observed (complete coverage of all 70 M25 segments from UKHA). No exposure estimation needed.
- Treatment of missing or sparse traffic counts: Not applicable — full coverage of all segments. Two segments excluded due to missing data for key variables.
- Whether offset terms, rates, denominators, or normalisation are used: No formal log-offset. log(AADT) and segment length are included as free predictors with estimated coefficients. This is a methodological choice that differs from Open Road Risk. The paper reports AADT elasticity of accidents (coefficient of log(AADT) ≈ 1.21–1.86 for KSI; 1.03–1.53 for slight), which is not constrained to 1.0 as a fixed offset would be.
- Evidence quote or page reference: "AADT and road segment length are the two most important factors explaining road accident frequency in the models. AADT and road segment length are both statistically significant and positively associated with accidents in all models." (p.10)
- Transferability to my AADF/WebTRIS setup:
  - Mathematical structure (Poisson count model with log(AADT) as free predictor): **High** — the model family is compatible. Using log(AADT) as a free predictor rather than a fixed-coefficient offset is an alternative parameterisation worth noting; Open Road Risk currently uses a fixed offset, which constrains the AADT elasticity to 1.0. This paper's results suggest the true elasticity on the M25 is higher (~1.2–1.9), which would mean a fixed-offset model slightly mis-specifies exposure.
  - Specific data source (full UKHA hourly loop data): **Low** — Open Road Risk relies on sparse AADF counts with Stage 1a estimated AADT; this paper has complete observed traffic data for all 70 segments.
- Notes: The paper's exposure approach differs from Open Road Risk's in an important way. Using log(AADT) as a free predictor estimates the elasticity empirically, while a fixed log-offset constrains it to 1.0. The paper's estimated elasticity (~1.2–1.9 for KSI on a major motorway) is above 1.0, suggesting that for motorway-class links in particular, a fixed offset may under-attribute risk to high-AADT segments. This is worth noting as a diagnostic direction.

---

## 5. Spatial Unit of Analysis

- Unit: Road segment (motorway junction-to-junction segment)
- Segment length or segmentation rule: Junction-to-junction; 72 segments defined by UK Highways Agency; 2 excluded due to missing data; 70 used. Mean length 5.26 km (range 0.76–15.40 km). Both directions modelled as separate observations (70 = ~35 physical sections × 2 directions).
- How crashes are assigned to the network: STATS19 provides easting/northing coordinates. A weighted score (WS) method assigns each accident to the most likely segment based on perpendicular distance and angular difference between accident direction and segment direction. ~2% of accidents could not be confidently assigned and were randomly allocated; sensitivity analysis showed no significant effect.
- Treatment of junctions/intersections: Junction accidents (~15% of total) explicitly excluded. "Accidents coded as junction accidents... were also excluded from the analysis." (p.4) Motorway junctions excluded due to design complexity and difficulty obtaining junction-level traffic flow.
- Spatial aggregation risks: Junction-to-junction segments average 5.26 km — considerably longer than Open Road Risk's OS Open Roads links. Within-segment variation in geometry, traffic, and accident risk is averaged. Excluding junction accidents removes ~15% of events, which may introduce selection bias.
- Evidence quote or page reference: "A road segment starts or ends at a junction." (p.4); "Accidents coded as junction accidents (about 15% of total accidents) were also excluded." (p.4)
- Relevance to OS Open Roads link-based pipeline: Partial. The junction-to-junction segment is conceptually similar to an OS Open Roads link but much longer (~5 km vs typical OS Open Roads link of ~100–300m). The snapping methodology (WS score using perpendicular distance + angular direction) is more sophisticated than a simple nearest-line snap and directly relevant to Open Road Risk's snapping quality concern. The angular component exploits the vehicle direction field in STATS19, which is potentially usable in Open Road Risk.

---

## 6. Temporal Unit of Analysis

- Years covered: Accident data 2004–2006 (3-year aggregate); traffic data 2006 only.
- Temporal resolution: Annual aggregate (no within-year temporal structure). The congestion index is computed from 2006 hourly data but averaged to a single segment-level index.
- Whether seasonality or time-of-day is modelled: Not in the main models. The paper notes that Shefer and Rietveld (1997) differentiated by peak/off-peak, and Noland and Quddus (2005) modelled peak and off-peak separately, but this paper uses annual aggregate congestion index.
- Whether before-after or panel structure is used: Cross-sectional (single 3-year aggregate observation per segment). No panel/longitudinal structure.
- Evidence quote or page reference: "Hourly traffic characteristic data for the year 2006... were obtained from the UK Highways Agency." (p.4); accident data 2004–2006 aggregated (p.4).
- Relevance to WebTRIS-style time profiles: Limited for this paper. However, the paper acknowledges that a congestion index averaged over all hours likely masks peak/off-peak effects — consistent with the rationale for Stage 1b. The paper cites peak-hour fatality rate differences (Shefer and Rietveld 1997) as motivation for more temporal precision.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Congestion index (CI) | UKHA hourly average travel time and vehicle delay, 2006 | CI = (T − T₀) / T₀ where T = actual travel time, T₀ = free-flow travel time (= T − weighted average delay). Dimensionless, segment-level annual average. | Primary study variable; found statistically insignificant in all models | Low — requires complete hourly travel time data per segment from a managed network. Not available in Open Road Risk's open-data pipeline. |
| log(AADT) | UKHA, 2006 (per-lane AADT) | Natural log of AADT / number of lanes | Strongest predictor in all models; elasticity ~1.2–1.9 (KSI) and 1.0–1.5 (slight) | Already present / compare implementation — Open Road Risk uses AADT in offset; this paper uses it as free predictor |
| Segment length (km) | UKHA road infrastructure data | Raw length in km (not log-transformed) | Significant in all models; elasticity ~0.68–0.79 (below 1, suggesting non-linear relationship) | Already present — used as part of Open Road Risk's offset; this paper uses it as free predictor |
| Maximum vertical gradient (%) | UKHA road infrastructure data | Maximum gradient (%) per segment | Significant in all models; positive association with accidents; stronger for KSI | Already present as candidate (OS Terrain 50 grade in pipeline) / compare implementation |
| Number of lanes | UKHA road infrastructure data | Count of lanes per carriageway | Significant for slight injury accidents in most models; not significant for KSI | Candidate feature — not currently in pipeline; derivable from OSM lanes tag (sparse coverage) |
| Minimum radius of curvature (m) | UKHA road infrastructure data | Minimum horizontal radius per segment (metres), log-transformed | Not significant in any model — possibly insufficient variation on M25 or mixed effects | Already present as candidate (curvature in pipeline) / compare implementation |
| Direction (dummy) | UKHA | Binary: clockwise (1) vs anticlockwise (0) | Not significant; included to control for possible directional asymmetry | Not applicable to Open Road Risk (OS Open Roads links are bidirectional) |
| Weighting score (WS) for accident assignment | STATS19 (easting/northing + vehicle direction) + UKHA segment geometry | WS = cos(Δθ) / d + 1 where d = perpendicular distance (m), Δθ = angular difference between accident direction and link direction | Methodological tool for snap quality; ~2% of accidents unresolvable | Medium — the angular component is potentially usable in Open Road Risk's snapping pipeline if STATS19 vehicle direction field is exploited |

---

## 8. Model Architecture

- Algorithms/models used:
  1. Poisson-lognormal (heterogeneity only, no spatial correlation)
  2. Poisson-gamma / Negative Binomial (heterogeneity only)
  3. Poisson-lognormal with CAR priors, 1st-order neighbours (heterogeneity + spatial correlation)
  4. Poisson-lognormal with CAR priors, 2nd-order neighbours (heterogeneity + spatial correlation)
  All estimated under full hierarchical Bayesian framework using WinBUGS / MCMC.
- Baseline model: Poisson-lognormal (simplest; heterogeneity only)
- Final/preferred model: Poisson-gamma fitted data slightly better for slight injury accidents (lowest DIC = 482.197); no single model clearly dominant for KSI (DIC range 281–284, very similar). CAR models confirm spatial correlation is significant but do not substantially change coefficient estimates.
- Loss function or likelihood, if stated: Poisson log-likelihood; random effects specified as lognormal (vi ~ N(0, τv²)) or gamma (exp(vi) ~ Gamma(φ,φ)); spatial term ui modelled via intrinsic CAR (Besag 1974).
- Offset/exposure term, if used: No formal log-offset. log(AADT) and segment length are free predictors with estimated coefficients. This is a deliberate choice — the paper does not constrain AADT elasticity to 1.0.
- Spatial autocorrelation handling: CAR model (conditional autoregressive, Besag 1974) using contiguity-based weights. First-order: directly connected segments (wij = 1); second-order: segments connected through first-order neighbours (wij = 0.5). Spatial correlation SD (u) found statistically significant in both KSI and slight models.
- Temporal dependence handling: Not addressed — cross-sectional design.
- Interpretability method: Posterior means and standard deviations of coefficients from MCMC; 90% and 95% credible intervals used for significance. DIC for model comparison.
- Evidence quote or page reference: Model specifications in Section 4, pp.6–8; results Tables 2–3, pp.20–21.

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Congestion index coefficient | Posterior mean (SD) | −0.588 (0.696) to −0.784 (0.749) | Fatal/serious, all 4 model specs | Negative sign (expected direction) but statistically insignificant across all specs | Table 2, p.20 |
| Congestion index coefficient | Posterior mean (SD) | −0.118 (0.420) to +0.373 (0.549) | Slight injury, all 4 model specs | Mixed sign, statistically insignificant | Table 3, p.21 |
| AADT elasticity (KSI) | log(AADT) coefficient | 1.212 to 1.856 | Fatal/serious, all specs | 1% increase in AADT → ~1.2–1.9% increase in fatal/serious accidents | Table 2, p.20 |
| AADT elasticity (slight) | log(AADT) coefficient | 1.026 to 1.525 | Slight injury, all specs | 1% increase in AADT → ~1.0–1.5% increase in slight injury accidents | Table 3, p.21 |
| Segment length coefficient | Posterior mean | ~0.135 (KSI); ~0.151–0.158 (slight) | All specs, both severity types | Mean elasticity ~0.68 (KSI), ~0.79 (slight); sub-linear relationship | Tables 2–3 |
| Gradient coefficient | Posterior mean | 0.187–0.210 (KSI); 0.190–0.229 (slight) | All specs, both severity types | Positive, significant in all models — steeper grades associated with more accidents | Tables 2–3 |
| Number of lanes | Posterior mean | Not sig (KSI); 0.191–0.262 (slight) | Slight injury, most specs | More lanes associated with more slight injury accidents | Table 3, p.21 |
| Heterogeneity SD (v) | SD of random effect | 0.149–0.529 | All models, both severity types | Statistically significant — unexplained heterogeneity exists across segments | Tables 2–3 |
| Spatial correlation SD (u) | SD of CAR term | 0.096–0.238 | CAR models, both severity types | Statistically significant — accidents are spatially correlated among neighbouring segments | Tables 2–3 |
| Model comparison | DIC | 281–284 (KSI); 482–490 (slight) | All 4 specs | Very similar DIC across specifications; Poisson-gamma marginally best for slight | Tables 2–3 |

**Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, or not stated?**

All metrics are in-sample Bayesian posterior estimates. DIC is a model complexity-penalised goodness-of-fit criterion, not an external predictive validation metric. No train/test split, no spatial holdout, no temporal holdout. With n = 70 segments this is expected.

**Do these metrics test predictive generalisation or model fit?**

Model fit and model comparison only (DIC, posterior means/SDs, credible intervals). DIC should not be interpreted as equivalent to held-out predictive accuracy.

**Are any metrics likely to be optimistic for real-world deployment?**

The model is cross-sectional with n = 70 and ~7–8 predictors — adequately parameterised for in-sample fit but not validated for generalisation. The finding that congestion is insignificant is robust across all 4 model specifications (a useful form of internal consistency check), but the AADT elasticity estimates (~1.2–1.9) are specific to the M25 motorway and should not be generalised to mixed road networks.

**Which metric is most relevant to Open Road Risk?**

The AADT elasticity estimates (log(AADT) coefficients ~1.2–1.9 for KSI, ~1.0–1.5 for slight) are the most directly informative for Open Road Risk. They suggest that a fixed-offset model that constrains AADT elasticity to 1.0 may be slightly mis-specified, at least for motorway-class links. The gradient finding is also useful.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Fatal accidents combined with serious injuries because "only few fatal accidents occurred on each segment" (p.5). The model does not use zero-inflated specification; Poisson-lognormal and Poisson-gamma both accommodate zero counts through the random effects structure.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models: Poisson-lognormal (lognormal heterogeneity), Poisson-gamma (= Negative Binomial in the frequentist sense). Zero-heavy counts handled by random effects in both model families, not by explicit zero-inflation. No zero-inflated model tested.
- Whether high-risk locations are evaluated separately: No. All 70 segments included; fatal and serious combined due to low counts.
- Evidence quote or page reference: "Since only few fatal accidents occurred on each segment, these accidents were combined with serious injury accidents." (p.5)
- Practical relevance to my sparse collision link-year dataset: The Poisson-lognormal and Poisson-gamma random-effects structures are relevant to handling over-dispersion in the link-year collision counts. At Open Road Risk's scale (21.7M link-years, ~98–99% zero), the within-segment random effect approach of this paper (n = 70) is structurally incompatible — but the Poisson-gamma (NB) family it validates is already in use or testable in Open Road Risk.

---

## 11. Validation Strategy

- Train/test split method: None — n = 70 segments.
- Spatial holdout used? No
- Temporal holdout used? No
- Grouped holdout used? No
- Cross-validation type: Not performed
- Metrics: DIC for model comparison; posterior credible intervals for coefficient significance.
- External validation: None
- Leakage or generalisation risks: Cross-sectional with n = 70; results specific to M25 motorway. AADT elasticity estimates are particular to a high-volume motorway context and should not be assumed to generalise to rural or urban roads.
- Evidence quote or page reference: "One limitation of this study is that only road segments from the M25 motorway have been included in the analysis." (p.12)
- What I should copy or avoid: Copy the model comparison approach (testing multiple Poisson family specifications, reporting DIC). Copy the WS-based accident snapping method concept. Do not generalise the specific coefficient values to Open Road Risk's mixed-network context. Note that the CAR spatial model finds significant spatial correlation — relevant for understanding whether spatial models are warranted in Open Road Risk, but computationally unrealistic at 2.17M links.

---

## 12. Key Findings Relevant to My Project

**Finding 1**
- Finding: Traffic congestion (measured precisely via a free-flow travel time congestion index) has no statistically significant effect on accident frequency on the M25, in either KSI or slight injury models, across all 4 model specifications. The result is robust to model choice.
- Why it matters: Provides evidence that congestion-related features (e.g., congestion index derived from travel time vs. free-flow) would likely be non-significant in Open Road Risk even if such data were available. Suggests that AADT (volume) and gradient are the dominant structural risk factors for motorway segments, not congestion per se. Does not affect Open Road Risk's current approach but provides negative evidence for adding congestion metrics.
- Evidence: Section 5.1, p.9; Tables 2–3.
- Confidence: High — consistent across all 4 model specifications on a single motorway. Scope is M25 only; result may differ on other road types.

**Finding 2**
- Finding: AADT elasticity of accident frequency is ~1.2–1.9 for KSI and ~1.0–1.5 for slight injury accidents on the M25. These values are above 1.0, meaning accidents grow somewhat faster than traffic volume on this motorway.
- Why it matters: Open Road Risk's Stage 2 uses a fixed log-offset which implicitly constrains AADT elasticity to 1.0. If the true elasticity on motorway-class links is ~1.2–1.9, the fixed-offset model will systematically under-rank high-AADT motorway segments in the risk percentile. This is a diagnostic direction worth testing — specifically, whether fitting log(AADT) as a free predictor rather than a fixed offset changes the motorway-class risk rankings.
- Evidence: Section 5.2, p.10; Tables 2–3.
- Confidence: Medium — result is consistent across 4 specs on M25 motorway; but the paper notes this may reflect motorway-specific conditions and acknowledges that other studies on rural two-lane roads report elasticity 0.6–0.7.

**Finding 3**
- Finding: Segment length coefficient (~0.13–0.16) implies a mean elasticity of ~0.68–0.79, suggesting a sub-linear relationship between road length and accident count. Accidents do not scale proportionally with length.
- Why it matters: Open Road Risk uses a fixed log-offset with coefficient 1 for link length. This paper suggests the true elasticity may be <1.0 on motorway segments. Fitting length as a free predictor (or testing a fixed offset of 1 vs an estimated coefficient) is a diagnostic worth considering. The sub-linear relationship is consistent with Elvik's (2006) "universal law of learning" — higher exposure accumulates safety experience.
- Evidence: Section 5.2, p.10; Tables 2–3.
- Confidence: Medium — consistent result on M25, but may be specific to long motorway segments (mean 5.26 km); unclear whether it holds for short OS Open Roads links (~100–300m).

**Finding 4**
- Finding: Maximum vertical gradient is significantly positively associated with accident frequency in all models and both severity types. The effect is stronger for KSI (coefficient ~0.187–0.210) than for slight (0.190–0.229, though similar). This is consistent with Milton and Mannering (1998).
- Why it matters: OS Terrain 50 derived gradient is already in Open Road Risk as a candidate feature. This UK motorway paper provides additional supporting evidence for its inclusion. Worth prioritising in Stage 2 feature evaluation.
- Evidence: Section 5.3, p.11; Tables 2–3.
- Confidence: High — consistent across all 4 model specs and both severity types on a UK motorway.

**Finding 5**
- Finding: The accident snapping method using a weighted score combining perpendicular distance and angular direction of travel outperforms pure distance-based snapping, particularly for dual-carriageway motorways where an accident on the clockwise carriageway could be mis-assigned to the anticlockwise carriageway by distance alone. About 2% of accidents were unresolvable by this method.
- Why it matters: Open Road Risk's current snap rate is 99.8% but snapping quality and ambiguous matches remain methodological concerns. The STATS19 vehicle direction field is available and could be exploited in a WS-style approach for motorway and dual-carriageway links — the highest-risk link classes in the pipeline. For OS Open Roads links where carriageway separation is small, this method would be most valuable for motorway and A-road dual-carriageway segments.
- Evidence: Section 3.1, pp.5–6; Figure 1.
- Confidence: High for the concept; medium for the specific threshold values (0.32 for WS difference) which are tuned to M25 geometry.

**Finding 6**
- Finding: Spatial autocorrelation (CAR term) is statistically significant in both KSI and slight injury models — accidents on neighbouring M25 segments are correlated after controlling for observed covariates. However, the CAR spatial model produces very similar coefficient estimates to the non-spatial models (DIC differences are small).
- Why it matters: Confirms that spatial correlation exists in motorway accident data even after controlling for AADT and geometry. For Open Road Risk at 2.17M links, a full CAR spatial model is computationally unrealistic. However, the finding that spatial models do not substantially change coefficient estimates relative to non-spatial models (similar DIC, similar coefficients) suggests that the Poisson GLM / XGBoost approach in Open Road Risk may not be critically harmed by ignoring spatial autocorrelation in coefficient estimation — though it would affect uncertainty estimates.
- Evidence: Section 5 (general), p.9; Tables 2–3 (SD u statistically significant but DIC differences small).
- Confidence: Medium — consistent finding for M25 (n = 70 segments); whether spatial autocorrelation is as important at Open Road Risk's finer spatial scale is not testable from this paper.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| WS-based accident snapping (perpendicular distance + angular direction) | Directly addresses Open Road Risk's noted snapping quality concern for dual-carriageway roads; STATS19 vehicle direction field available | STATS19 vehicle direction field (already in data); OS Open Roads segment geometry (already in pipeline) | 70 segments, M25 only | Compatible — most valuable for motorway and dual-carriageway A-road links | Snapping / data engineering (pre-Stage 1a) | Medium | Threshold values (WS > 0.32 for confident assignment) are tuned to M25 geometry; would need recalibration for OS Open Roads link geometry |
| Gradient as significant positive predictor of KSI | Supporting evidence for OS Terrain 50 gradient feature already in pipeline | OS Terrain 50 (already in pipeline) | 70 motorway segments | Compatible | Stage 2 / feature engineering — already present | Already present — document and test | Over-fitting risk if gradient correlated with road class |
| Testing log(AADT) as free predictor vs fixed-offset | Tests whether AADT elasticity ≠ 1 in Open Road Risk data; if elasticity > 1 for motorways, fixed offset mis-ranks high-AADT links | AADT already estimated by Stage 1a | 70 motorway segments | Compatible — implement as diagnostic comparison | Stage 2 / diagnostic | Low — modify existing GLM to free the AADT coefficient | May reveal model mis-specification that complicates interpretation |
| Testing segment length coefficient vs fixed offset = 1 | Tests whether length elasticity ≠ 1; paper finds ~0.7–0.8 on long motorway segments | Link length already in pipeline | 70 motorway segments | Compatible | Stage 2 / diagnostic | Low | Sub-linear length relationship may reflect long-segment averaging artefact not relevant to short OS Open Roads links |
| Poisson-gamma (NB) as alternative to Poisson GLM | Paper finds Poisson-gamma marginally best for slight injuries (DIC); confirms NB as a reasonable alternative | No new data needed | 70 segments | Compatible | Stage 2 — already tested or testable | Low | With 21.7M link-years, NB dispersion parameter estimation is computationally intensive but feasible |
| Separate models for KSI vs slight | Different significant predictors between KSI and slight models (number of lanes significant only for slight); supports severity stratification | STATS19 severity already available | 70 segments | Compatible conceptually; KSI counts at link level will be very sparse | Stage 2 — candidate extension / diagnostic | Medium | KSI count per link-year will be near-zero; model instability expected |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Congestion index (CI = travel time / free-flow travel time − 1) | Requires complete hourly travel time and delay data per segment from a managed motorway network; not available in open-data pipeline | No equivalent of UKHA hourly segment-level travel time data in Open Road Risk | 70 M25 segments | Incompatible — data not available at national scale | Volume/capacity ratio as approximate proxy (AADT / estimated capacity by road class), but this is distant from the precise CI | High |
| Full Bayesian CAR spatial model (WinBUGS MCMC) | Computationally unrealistic at 2.17M links; designed for small-to-medium n (70–15,000) | Computational cost and MCMC convergence at scale | 70 segments | Incompatible at 2.17M link scale | Spatial random effects as approximate correction for grouped spatial units (e.g., police force area fixed effects); or accept non-spatial model with acknowledged limitation | High |
| AADT elasticity values (~1.2–1.9) as production calibration | Derived from M25 motorway only; not generalisable to rural roads, urban streets, or mixed network | Single motorway context; other studies (rural roads) report 0.6–0.7 | 70 motorway segments | Incompatible for national mixed network | Estimate elasticity separately by road class in Open Road Risk; do not apply M25 values globally | High |
| Junction exclusion (15% of accidents removed) | Removes a structurally important crash type; Open Road Risk should model junction-related crashes | Motorway junction exclusion justified by data availability; not appropriate for a general road risk model | 70 segments, junctions excluded | Incompatible — would discard important data | Not applicable; retain junction crashes but add junction complexity features | High |

---

## 14. Pipeline Implications

**Does this paper support using exposure-normalised collision risk?**
Yes — AADT and segment length are the dominant predictors in all models, confirming exposure is essential. The paper's finding that the true AADT elasticity may exceed 1.0 on motorway-class links is a specific concern for Open Road Risk's fixed-offset parameterisation. Worth testing as a diagnostic.

**Does it suggest better handling of AADT/AADF uncertainty?**
Not directly — the paper uses complete UKHA data with no estimation uncertainty. However, the high AADT elasticity finding indirectly implies that uncertainty in AADT estimates (Stage 1a) propagates substantially into Stage 2 risk rankings, particularly for high-volume motorway links.

**Does it suggest useful geometry or road-context features?**
Yes — gradient (maximum vertical grade, %) is confirmed as a significant positive predictor of both KSI and slight accidents on the M25, consistent with OS Terrain 50 grade already in the pipeline. Number of lanes is weakly significant for slight injuries. Radius of curvature was not significant here (possibly due to limited M25 variation) but remains a plausible candidate for roads with greater curvature variation.

**Does it suggest better modelling of junctions?**
Implicitly — by excluding junction accidents (~15%), the paper highlights that junction crashes are a distinct and complicating data category. Open Road Risk should track the proportion of snapped collisions near junctions and consider whether junction proximity features are needed.

**Does it suggest better treatment of severity?**
Yes — KSI and slight models show different significant predictor sets (number of lanes significant for slight but not KSI; gradient slightly more significant for KSI in CAR models). Supports separate severity modelling as a future diagnostic.

**Does it suggest better validation design?**
Not directly — no validation performed. The multiple model specification comparison (4 Poisson variants) is a useful internal robustness check, but not a substitute for external validation.

**Does it expose a weakness in my current approach?**
Yes, two specific points:
1. The fixed log-offset (AADT elasticity = 1.0) may under-rank high-AADT motorway segments if the true elasticity is ~1.2–1.9. Testing log(AADT) as a free predictor vs fixed offset is a low-effort diagnostic.
2. The WS-based snapping method exploits the vehicle direction field in STATS19, which Open Road Risk's current snapping does not. For dual-carriageway and motorway links, this is a concrete improvement direction.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Run a Stage 2 diagnostic comparing the current fixed-offset Poisson GLM against a version where log(AADT) is a free predictor (coefficient estimated rather than fixed to 1.0). Compare coefficient value, model deviance, and whether motorway-class link risk rankings change materially.
- Action type: Diagnostic
- Relevant stage: Stage 2
- Why the paper supports it: Paper finds AADT elasticity ~1.2–1.9 on the M25, consistently above 1.0 across all 4 model specifications. A fixed offset constraining elasticity to 1.0 may systematically mis-rank high-AADT links.
- Evidence: Section 5.2, p.10; Tables 2–3.
- Effort: Low (modify existing GLM code; one additional model run)
- Risk if implemented badly: If elasticity is estimated >1.0, it changes the interpretation of AADT's role — document this carefully. If elasticity is close to 1.0 in Open Road Risk data, the fixed offset is validated.

**Action 2**
- Suggested repo action: Similarly, run a diagnostic testing segment length as a free predictor vs fixed-offset coefficient = 1. The paper finds elasticity ~0.7–0.8 on M25 (sub-linear). If Open Road Risk shows similar sub-linearity for short links, the offset assumption may need revisiting.
- Action type: Diagnostic
- Relevant stage: Stage 2
- Why the paper supports it: Segment length coefficient ~0.13–0.16 implies mean elasticity 0.68–0.79, not 1.0. Consistent with Elvik (2006) law of learning.
- Evidence: Section 5.2, p.10; Tables 2–3.
- Effort: Low (same model run as Action 1 — test jointly)
- Risk if implemented badly: Sub-linear length relationship may be a motorway-segment artefact (average 5.26 km vs ~0.2 km OS Open Roads links); interpret cautiously and segment by road class.

**Action 3**
- Suggested repo action: Document the WS-based snapping concept (perpendicular distance + angular direction from STATS19 vehicle direction field) as a candidate improvement for snapping quality on dual-carriageway and motorway links. Assess what proportion of snapped M25-class links in Open Road Risk are dual-carriageway and whether vehicle direction field is populated in STATS19 records for those accidents.
- Action type: Documentation note / candidate diagnostic for snapping pipeline
- Relevant stage: Data engineering (pre-Stage 1a)
- Why the paper supports it: The WS method directly addresses the dual-carriageway mis-assignment problem; STATS19 vehicle direction field is the required input, already present in the database.
- Evidence: Section 3.1, pp.5–6; Figure 1.
- Effort: Low (documentation); Medium (implementation and assessment)
- Risk if implemented badly: WS thresholds (0.32) are tuned to M25 geometry; re-tuning required for shorter OS Open Roads links. Incorrect re-assignment could worsen snap quality rather than improve it.

**Action 4**
- Suggested repo action: Add documentation note to Stage 2 that gradient (from OS Terrain 50) has UK motorway empirical support (significant positive predictor in this paper, consistent with Milton & Mannering 1998). Prioritise gradient feature in Stage 2 feature evaluation diagnostics.
- Action type: Documentation note
- Relevant stage: Stage 2 / feature engineering — already present
- Why the paper supports it: Gradient significant at 90–95% credible level in all 4 model specs and both severity types on a UK motorway.
- Evidence: Section 5.3, p.11; Tables 2–3.
- Effort: Low
- Risk if implemented badly: None — documentation only; gradient already in pipeline

**Action 5**
- Suggested repo action: Add documentation note recording that a Bayesian CAR spatial model finds statistically significant spatial autocorrelation in M25 accident counts, but that the CAR model produces virtually the same coefficient estimates as the non-spatial Poisson-gamma model (similar DIC). This provides justification for Open Road Risk's non-spatial Poisson GLM approach at national scale — spatial autocorrelation is real but does not materially bias coefficient estimates on this dataset.
- Action type: Documentation note
- Relevant stage: Stage 2 / documentation / validation
- Why the paper supports it: DIC values nearly identical across spatial and non-spatial models (281–284 for KSI; 482–490 for slight); spatial correlation SD significant but coefficients unchanged.
- Evidence: Section 5 (general), p.9; Tables 2–3.
- Effort: Low
- Risk if implemented badly: None — documentation only. Note caveat that this is one motorway at 70 segments; may not hold at Open Road Risk scale.

---

## 16. Query Tags

- Poisson-lognormal
- Poisson-gamma
- negative-binomial
- Bayesian-MCMC
- CAR-spatial-model
- spatial-autocorrelation
- M25-motorway
- UK-motorway
- STATS19
- congestion-index
- AADT-elasticity
- segment-level
- log-AADT-free-predictor
- gradient-significant
- junction-excluded
- accident-snapping
- angular-direction-snap
- WinBUGS
- DIC
- dual-carriageway
- no-validation
- motorway-only

---

## 17. Confidence and Gaps

- Overall confidence in extraction: High
- Important details not stated in the paper:
  - Publication year not stated in PDF (estimated ~2009–2010 from reference dates; verify against published version)
  - Journal name not stated (filename suffix suggests AAP)
  - DOI not stated
  - Whether AADT used is 2006 only or averaged across 2004–2006 not entirely clear; text says traffic data from 2006, accident data from 2004–2006 — this temporal mismatch is a minor methodological concern not discussed in the paper
  - Exact WinBUGS priors and convergence diagnostics beyond what is stated in the text are not fully detailed
- Parts of the paper that need manual checking:
  - Tables 2 and 3: All coefficient values legible and internally consistent. The DIC values (283.56 / 281.02 / 282.36 / 284.04 for KSI; 490.05 / 482.20 / 490.29 / 489.13 for slight) confirm Poisson-gamma marginally best for slight but no dominant model for KSI. These check out.
  - The WS formula: WS = cos(Δθ) / d + 1. With d = 1 minimum (floor) and Δθ = 0: WS_max = 1/1 + 1 = 2. With Δθ = 180° (opposite direction): WS = cos(180°)/d + 1 = −1/d + 1 = 0 (at d = 1 minimum). Range −1 to 2 as stated. Checks out.
  - The paper states "2% such accidents" assigned randomly (WS difference ≤ 0.3) and sensitivity analysis showed no significant difference. This should be verified if the snapping method is adopted.
- Any likely ambiguity or risk of misinterpretation:
  - The paper uses log(AADT) as a free predictor (not a fixed offset). The AADT elasticity values (~1.2–1.9) are specific to a high-volume motorway and should not be extrapolated to Open Road Risk's full mixed network without road-class stratification.
  - The Poisson-gamma model is described as fitting slightly better. In the Bayesian parameterisation used here, Poisson-gamma = Negative Binomial in the frequentist sense; this equivalence should be documented clearly in any Open Road Risk write-up that references this paper.
  - The congestion index (CI) result — no effect — is robust across 4 model specifications. This is strong negative evidence. However, the paper's CI is an annual average from a single year (2006); a time-varying CI matched to the accident year might yield different results. This limitation is acknowledged briefly in the paper.
