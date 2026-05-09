# Paper Extraction: Al-Omari 2021 — Crash Analysis and Development of Safety Performance Functions for Florida Roads in the Framework of the Context Classification System

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Crash_Analysis_And_Development_Of_Safety_Performance_Functions_Fo.pdf
- Suggested Markdown filename: paper-extraction-al-omari-2021-florida-context-classification-spf.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (full thesis rendered in context as document)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: All 49 pages rendered as text. Figures 4, 5, 8, and 9 are referenced but not directly viewable; their content is adequately described in text and tables. This is a masters thesis, not a peer-reviewed journal article — evidence standards and methodological scrutiny are accordingly lower. No supplementary material. The thesis was supervised by Mohamed Abdel-Aty (University of Central Florida).

---

## 1. Citation

- Title: Crash Analysis and Development of Safety Performance Functions for Florida Roads in the Framework of the Context Classification System
- Authors: Ma'en Mohammad Ali Al-Omari
- Year: 2021
- DOI or URL: https://stars.library.ucf.edu/etd2020/633
- Country / region studied: United States — Florida statewide
- Study setting: mixed — all road context classes from rural/natural (C1, C2) to suburban commercial (C3C, C3R) to urban (C4, C5, C6); road segments only (intersections excluded from analysis)

---

## 2. Core Objective

- One-sentence description: The thesis develops negative binomial safety performance functions (SPFs) for Florida road segments at three levels of specificity — context-class-specific, area-type-specific, and statewide — and applies EB-adjusted network screening to identify the most problematic road segments.
- Main purpose: safety performance function / hotspot detection (network screening)
- Evidence quote or page reference: "SPFs have been developed in the framework of the FDOT roadway context classification system at three levels of modeling" (Abstract, p.iii); "network screening to determine the most problematic road segments has been accomplished" (Abstract, p.iii)

---

## 3. Response Variable

- Target variable: Annual crash frequency per road segment; modelled separately for total crashes (KABCO), fatal-and-injury crashes (KABC), and property-damage-only crashes (PDO) — the last two specifically for network screening
- Collision type: all crash types modelled in SPFs; injury (KABC) and PDO separated for network screening EPDO-PSI calculation
- Severity handling: SPFs developed for total crashes; separate simple SPFs for FI and PDO crashes used in network screening. No joint severity model.
- Count, binary, rate, risk score, severity class, or other: count (annual crash frequency per segment); DVMT-SPFs implicitly model a rate (DVMT = AADT × length, so ln(DVMT) as predictor with free coefficient is equivalent to a near-rate model)
- Time window used for outcomes: 5-year aggregate (2015–2019); crash frequency expressed as annual average (total crashes / 5 years per segment)
- Evidence quote or page reference: "Crash and traffic data of 2015-2019 years have been obtained" (Abstract, p.iii); Tables 1–2 show "T (total annual crash frequency)" as the response variable

---

## 4. Exposure Handling

- Exposure variable used: two alternatives tested — (1) AADT alone with ln(L) as a fixed offset (segment length in miles entered as ln(L) in model equation), and (2) DVMT = AADT × length, entered as ln(DVMT) as a single combined exposure predictor
- Traffic count source: FDOT average AADT data, 2015–2019 average per segment; segments split and merged based on consistent AADT and road identification
- Whether exposure is modelled, observed, assumed, or ignored: observed FDOT AADT; no imputation or uncertainty propagation described
- Treatment of missing or sparse traffic counts: not explicitly described; segments with reliable AADT appear to have been retained; no discussion of estimation for segments without direct counts
- Whether offset terms, rates, denominators, or normalisation are used:
  - AADT-SPFs: Np = exp(α + β·ln(AADT) + Σγ_i·X_i + ln(L)) — ln(L) as fixed offset, ln(AADT) as covariate with estimated coefficient β
  - DVMT-SPFs: Np = exp(α + β·ln(DVMT) + Σγ_i·X_i) — no separate offset; DVMT = AADT × length so this is a near-offset form with free coefficient on combined exposure
- Evidence quote or page reference: Equations 1 and 2, p.19; "Two exposure variables have been used in this study; the annual average daily traffic (AADT) as the traditional approach and the daily vehicle miles traveled (DVMT) since it accounts for the segment length" (p.18)

### Transferability to my AADF/WebTRIS setup

- Mathematical structure of AADT-SPF with ln(L) offset: **high transferability** — directly analogous to Open Road Risk Stage 2 Poisson GLM offset structure. Estimated AADT coefficients (β ranging 0.39–1.07 across road classes) confirm near-proportionality between traffic and crashes; some urban classes (C5, C6) show sub-linear AADT coefficients (~0.39–0.63) which is worth noting.
- DVMT as combined ln(AADT × length) predictor: **high transferability** for mathematical structure — equivalent to Open Road Risk's existing offset when coefficient is constrained to 1.0; estimated free coefficients (0.50–0.93 across classes) show DVMT-SPFs perform better than AADT-SPFs in most cases, and coefficients are closer to 1.0 than AADT-only coefficients are.
- Specific FDOT AADT data source: **medium transferability** — Open Road Risk uses AADF-based AADT estimates which are comparable in concept; neither paper propagates traffic-count uncertainty.
- Notes: The sub-linear AADT coefficients on urban C5/C6 roads (0.39–0.63 for AADT-SPFs; 0.50–0.70 for DVMT-SPFs) suggest traffic exposure explains less variance in urban cores — possibly due to pedestrian/cyclist crashes, intersection dominance, or congestion effects. Open Road Risk should investigate whether AADT coefficient varies by road class.

---

## 5. Spatial Unit of Analysis

- Unit: road segment with uniform characteristics — segments derived from FDOT context classification map merged with AADT data; consecutive segments with same road ID, context class, and AADT merged into longer homogeneous units
- Segment length or segmentation rule: weighted average or weighted majority of road characteristics within merged segment; minimum length threshold applied to "avoid very short road segments" (exact threshold not stated; described as applied but value not specified). Average lengths range from 0.41 miles (C6) to 2.81 miles (C2) — considerably longer than OS Open Roads links.
- How crashes are assigned to the network: crash records geocoded and matched to road segments via FDOT road identification system; annual crash totals aggregated per segment over 2015–2019
- Treatment of junctions/intersections: intersections not explicitly excluded from collision data (unlike the Washington dataset in Pan et al. 2017), but the study focuses on road segments; access point density (APD) and signalized intersection density (SID) are included as segment-level features rather than modelling intersections separately
- Spatial aggregation risks: not discussed. Long segment averaging (mean 0.41–2.81 miles) will smooth local variation. Weighted-average feature assignment introduces approximation for heterogeneous segments.
- Evidence quote or page reference: "Roadway segments in the context classification map have been split according to average AADT value of 2015 to 2019 years. Consecutive road segments that have the same road identification (RID), CC, and AADT information have been merged" (p.10); "road and environment information was determined for every roadway segment by calculating the weighted average or the weighted majority values within the segment" (p.10)
- Relevance to OS Open Roads link-based pipeline: partial — OS Open Roads links are shorter and more numerous than the FDOT merged segments (mean ~118 m vs 0.41–2.81 miles). The access-point density and signalized intersection density features are conceptually useful but represent a different spatial aggregation scale. The feature engineering approach (weighted averaging of characteristics within longer segments) is not directly transferable to Open Road Risk's shorter link geometry.

---

## 6. Temporal Unit of Analysis

- Years covered: 2015–2019 (5 years)
- Temporal resolution: annual — crash counts expressed as annual averages (total / 5) per segment; no panel structure used (cross-sectional model on 5-year averages)
- Whether seasonality or time-of-day is modelled: no
- Whether before-after or panel structure is used: no — cross-sectional only; 5-year data collapsed to annual averages
- Evidence quote or page reference: "Crash and traffic data of 2015-2019 years have been obtained" (Abstract); descriptive tables show mean annual crash frequency per segment
- Relevance to WebTRIS-style time profiles: not relevant — no time-of-day or temporal analysis performed

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| AADT (annual average daily traffic) | FDOT traffic data | 5-year average per segment; weighted assignment within merged segment | Primary exposure variable | Already present — Open Road Risk uses AADF-derived AADT. Compare coefficient values. |
| DVMT (daily vehicle miles travelled) | Derived | AADT × segment length (miles) | Combined exposure variable; DVMT-SPFs outperform AADT-SPFs in this study | Already present implicitly in exposure offset (AADT × length_km × 365 / 1e6). Compare. |
| Segment length (miles) | FDOT geometry | Direct measurement; used as ln(L) offset in AADT-SPFs | Exposure component | Already present in exposure offset |
| SID — signalized intersection density (per mile) | FDOT data | Count of signalised intersections per segment length | Consistently significant positive predictor across all road classes and all models | Candidate feature — not currently in Open Road Risk; derivable from OS data or OSM |
| APD — access point density (per mile) | FDOT data | Count of access points (driveways, side roads) per segment length | Consistently significant positive predictor across almost all models | Candidate feature — partially derivable from OS Open Roads network topology or OSM; coverage uncertain |
| Speed limit (mph) | FDOT inventory | Direct field; posted speed limit | Consistently significant negative predictor across all road classes (higher speed limit → fewer crashes per segment, after controlling for AADT — likely reflects lower intersection density) | Already a candidate feature in Open Road Risk (OSM speed limit with imputed coverage) |
| Number of lanes | FDOT inventory | Direct count | Significant in some models; positive in DVMT models (more lanes → more crashes after controlling for DVMT) | Derivable from OS Open Roads / OSM; lane count available in Open Road Risk candidate features |
| Shoulder width (feet) | FDOT inventory | Direct measurement | Significant in several CC-SPFs; sign varies by road class — negative (safer) on C3C, C5, C6; positive (less safe) on C4 | Candidate feature; low UK open-data coverage for accurate values |
| Paved shoulder (binary) | FDOT inventory | Indicator variable | Significant negative predictor (safer) on multiple road classes | Low transferability — shoulder type classification not available in UK open data |
| Raised median (binary) | FDOT inventory | Indicator variable | Significant positive predictor (less safe) on C2, C3R, C4 — raised median associated with more crashes (rollover risk noted) | Low direct transferability — median type not in OS Open Roads; partially in OSM |
| Paved median (binary) | FDOT inventory | Indicator variable | Significant negative predictor (safer) on multiple classes | Low transferability |
| Vegetation median (binary) | FDOT inventory | Indicator variable | Significant negative predictor (safer) on C3C and rural roads | Low transferability |
| Median width (feet) | FDOT inventory | Direct measurement | Significant in some models; positive coefficient in some DVMT models (wider median → more crashes on some road types) — counterintuitive, possibly collinear with divided high-speed roads | Candidate but uncertain direction; not readily available in UK open data |
| Pavement condition (1–5 scale) | FDOT inventory | Numeric rating; 1=worst, 5=best | Significant positive predictor in some models (better pavement → more crashes); authors attribute to higher speeds on smooth roads | Not available in UK open data; not a transferable feature |
| Surface width (feet) | FDOT inventory | Total road surface width | Significant in some models | Not directly available; partially derivable from lane count × lane width estimate |
| Asphalt surface (binary) | FDOT inventory | Indicator | Significant negative predictor on natural roads (C1) — paved asphalt safer than unpaved; not significant elsewhere | Not relevant in UK context where virtually all roads are paved |
| Sidewalk width (feet) | FDOT inventory | Direct measurement | Significant negative predictor on suburban residential (C3R) | Not available in UK open data |
| Presence of bike lane (binary) | FDOT inventory | Indicator | Significant negative predictor on C3R, C4 | Partially available from OSM (sparse in UK) |
| Presence of shared path (binary) | FDOT inventory | Indicator | Significant negative predictor on C4 | Low UK coverage |
| Context class (C1–C6) | FDOT classification | Categorical classification based on geography, land use, demographics | Defines model stratification; CC-SPFs outperform area-type and statewide SPFs | Conceptual analogue: Open Road Risk uses rural/urban classification + road type; direct FDOT system not transferable but stratification principle is |

---

## 8. Model Architecture

- Algorithms/models used: negative binomial (NB) generalised linear model; overdispersion confirmed by variance > mean for all road classes
- Baseline model: simple SPF — only exposure variable (ln(AADT) or ln(DVMT)) and, for AADT-SPFs, ln(L) as fixed offset
- Final/preferred model: full context-class-specific DVMT-SPFs (CC-SPFs with all significant variables); DVMT-SPFs marginally outperform AADT-SPFs; CC-SPFs outperform area-type and statewide SPFs
- Loss function or likelihood: negative binomial maximum likelihood; overdispersion parameter k estimated per model; backward selection retaining variables significant at 95% confidence level
- Offset/exposure term: ln(L) as fixed offset in AADT-SPFs; no formal fixed offset in DVMT-SPFs (ln(DVMT) used as free-coefficient covariate — coefficient estimated, not constrained to 1)
- Spatial autocorrelation handling: none — road segments treated as independent observations
- Temporal dependence handling: none — 5-year average cross-section; no panel structure
- Interpretability method: NB coefficients with standard errors and significance; overdispersion parameter reported; MAE and RMSE used as performance metrics
- Correlation screening: variables with correlation > 0.5 excluded prior to model development (Figure 7 shows correlation matrix); backward selection then retains only significant variables
- Evidence quote or page reference: Section 5.1, pp.18–19; "the generalized linear model with negative binomial distribution has been used in this study" (p.18); "variance is much larger than the mean for all road classes" (p.18)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| In-sample goodness of fit | MAE | 8.9 | Simple AADT CC-SPF, C1 (natural) | Lowest-traffic road class | Table 3, p.26 |
| In-sample goodness of fit | MAE | 6.5 | Simple AADT CC-SPF, C2 (rural) | | Table 3, p.26 |
| In-sample goodness of fit | MAE | 28.8 | Simple AADT CC-SPF, C3C (suburban commercial) | Highest absolute MAE among rural/suburban | Table 3, p.26 |
| In-sample goodness of fit | MAE | 30.6 | Simple AADT CC-SPF, C4 (urban general) | Highest absolute MAE in urban class | Table 3, p.26 |
| In-sample goodness of fit | MAE | 20.4 | Full AADT CC-SPF, C3C | Improvement vs simple; ~29% reduction | Table 3, p.27 |
| In-sample goodness of fit | MAE | 26.5 | Full AADT CC-SPF, C4 | Improvement vs simple | Table 3, p.27 |
| In-sample goodness of fit | MAE | 6.0 | Simple DVMT CC-SPF, C1 | Better than AADT simple SPF (8.9) | Table 5, p.30 |
| In-sample goodness of fit | MAE | 5.4 | Simple DVMT CC-SPF, C2 | Better than AADT (6.5) | Table 5, p.30 |
| In-sample goodness of fit | MAE | 24.2 | Simple DVMT CC-SPF, C3C | Better than AADT simple (28.8) | Table 5, p.30 |
| In-sample goodness of fit | MAE | 29.0 | Simple DVMT CC-SPF, C4 | Slight improvement vs AADT simple (30.6) | Table 5, p.30 |
| In-sample goodness of fit | MAE | 37.5 | SW-SPF (statewide), C1 | Much worse than CC-SPF (8.9) — confirms stratification value | Table 4, p.28 |
| In-sample goodness of fit | MAE | >100 | Full statewide DVMT-SPF, C6 | Statewide model completely fails for urban core | Table 6, p.33 |
| NB coefficient | ln(AADT) | 0.97 (SE 0.023) | Simple CC-SPF, C2 rural | Near-unity — consistent with proportionality assumption | Table 3, p.26 |
| NB coefficient | ln(AADT) | 0.39 (SE 0.084) | Simple CC-SPF, C5 urban centre | Sub-linear — traffic explains less variance in dense urban context | Table 3, p.26 |
| NB coefficient | ln(DVMT) | 0.74–0.93 | Full CC-SPFs, C2–C4 | Closer to 1.0 than AADT-only models | Table 5, p.30 |
| NB coefficient | SID (signalised intersection density) | 0.10–0.48 (positive) | Full CC-SPFs and AT-SPFs | Consistent positive effect across all road classes | Tables 3–6 |
| NB coefficient | APD (access point density) | 0.01–0.08 (positive) | Full CC-SPFs | Consistent positive effect; smaller magnitude than SID | Tables 3–6 |
| NB coefficient | Speed limit | −0.02 to −0.05 (negative) | Full CC-SPFs and AT-SPFs, most classes | Higher speed limit → fewer crashes per segment (likely reflects low-conflict road types) | Tables 3–6 |
| Overdispersion parameter | k | 0.29–1.37 | All models | Wide range; higher k on rural/natural roads indicating more overdispersion | Tables 3–6 |
| Network screening | EPDO-PSI ranking | Top 20 segments identified | C3C and C4 roads, Miami area | Practical output; highest PSI in suburban commercial and urban general roads | Table 7 / Figure 9, pp.35–36 |

**Metric qualification:**

- All MAE and RMSE values are **in-sample goodness of fit** — computed on the same data used to fit the models. No train/test split, no temporal holdout, no spatial holdout, and no cross-validation is described.
- These metrics measure in-sample fit adequacy, not predictive generalisation. They cannot be used as benchmarks for out-of-sample prediction performance.
- The comparison between CC-SPFs, AT-SPFs, and SW-SPF is valid as a relative model comparison (the same in-sample data is used for all), but the absolute MAE values overstate predictive accuracy.
- Log-likelihood values (LLV) are reported per model and can be used for in-sample likelihood-ratio tests but are not cross-validated.
- No AIC, BIC, or cross-validation metrics reported.
- Most relevant metric for Open Road Risk: the relative pattern (CC-SPFs outperform statewide; DVMT-SPFs slightly outperform AADT-SPFs) is informative for design decisions, even though absolute MAE values are in-sample only.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: negative binomial distribution used to handle overdispersion. The 5-year temporal aggregation substantially reduces the zero proportion compared to Open Road Risk's annual link-year data — many segments have non-zero 5-year totals even when annual counts are zero.
- Use of Poisson / negative binomial / zero-inflated models: negative binomial only; overdispersion confirmed (variance >> mean for all classes). No zero-inflated model.
- Zero-heavy counts handled using: 5-year temporal aggregation (reduces zero proportion); negative binomial distribution (handles overdispersion but not structural zeros); note that Tables 1–2 show minimum crash counts of 0.0 per year for most classes, confirming residual zero presence even after 5-year aggregation
- Whether high-risk locations are evaluated separately: network screening identifies the top 20 highest EPDO-PSI segments explicitly
- Evidence quote or page reference: "It was found that the variance is much larger than the mean for all road classes. This means that the crash data are over dispersed, and the negative binomial distribution is appropriate" (p.18)
- Practical relevance: Open Road Risk's ~1–2% annual collision rate on link-years is more extreme than this study's segment-level data (where 5-year aggregation substantially fills in zeros). The NB model is appropriate for both, but the threshold between NB adequacy and potential need for zero-inflation is more relevant to Open Road Risk's link-year panel than to this study's 5-year aggregated segments. The paper does not address this distinction.

---

## 11. Validation Strategy

- Train/test split method: none — no train/test split performed
- Spatial holdout used: no
- Temporal holdout used: no
- Grouped holdout used: no
- Cross-validation type: none
- Metrics: MAE and RMSE computed on the same dataset used for model fitting (in-sample)
- External validation: none
- Leakage or generalisation risks: all reported performance metrics are in-sample. The comparison between CC-SPFs, AT-SPFs, and SW-SPF is a valid relative comparison on the same data, but none of these values represents predictive accuracy on unseen data. The network screening EPDO-PSI output is also in-sample (uses the same fitted SPFs applied to the same segments).
- Evidence quote or page reference: Section 5.1, pp.18–19; no holdout or cross-validation described
- What I should copy: the relative model comparison structure (context-class-specific vs area-type vs statewide) is informative as a design principle — evaluate whether road-type-stratified SPFs outperform a single global model. The EPDO-PSI network screening procedure with EB adjustment is a well-documented method directly applicable to Open Road Risk.
- What I should avoid: treating the in-sample MAE/RMSE values as predictive benchmarks.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: Context-class-specific SPFs (CC-SPFs) outperform area-type SPFs (AT-SPFs) and statewide SPFs for most road classes in Florida. The statewide model fails completely for urban core (C6) roads (MAE > 100). Simple DVMT-SPFs generally outperform simple AADT-SPFs, and DVMT coefficients are closer to 1.0 than AADT-only coefficients.
- Why it matters: Provides evidence that road-type stratification of SPFs improves in-sample fit, supporting the case for road-class-stratified modelling or road-class-specific features in Open Road Risk Stage 2. The DVMT (AADT × length) finding reinforces the use of combined exposure in the log-offset. Note: this is in-sample comparison only — external validation was not performed.
- Evidence: Figure 8, p.34; Tables 3–6; "CC-SPFs outperform AT-SPFs and SW-SPF for most road classes" (p.25)
- Confidence: medium — in-sample comparison only; the performance advantage of stratification may partly reflect overfitting to context-class-specific data distributions rather than improved generalisation.

**Finding 2:**
- Finding: Signalised intersection density (SID) and access point density (APD) are the most consistently significant positive predictors of crash frequency across all road classes and all model variants in this study. SID coefficients range 0.10–0.48; APD coefficients range 0.01–0.08. Both remain significant after controlling for AADT/DVMT, road geometry, and other features.
- Why it matters: Open Road Risk does not currently include intersection density or access point density as features. This study provides Florida-specific evidence (across 8 road context classes, ~10,500 segments, 5 years) that these are important predictors. They are conceptually derivable for UK roads from OS Open Roads network topology or OSM. This finding is consistent across multiple road types and exposure specifications, increasing confidence in the direction.
- Evidence: Tables 3–6, all full SPF results; "intersections and access points densities are one of the most influential factors on crash occurrence" (p.37–38)
- Confidence: medium-high for direction within this Florida dataset — consistent finding across all road classes. Transferability to UK road context requires testing; access point density definitions may differ.

**Finding 3:**
- Finding: Speed limit is a consistently significant negative predictor of crash frequency per segment across almost all road classes (higher speed limit → fewer crashes per segment after controlling for AADT). This counterintuitive direction is attributed to the fact that high speed limits occur on roads with fewer access points and intersections (lower conflict density), not to speed being genuinely protective. Coefficients range −0.02 to −0.05.
- Why it matters: Open Road Risk includes OSM speed limit as a candidate feature with imputed coverage. This finding warns that a negative coefficient on speed limit in an SPF is a well-known confound (speed limit proxies for road type/access density rather than independently reducing crash risk). Interpreting a negative speed limit coefficient as causal would be incorrect. This is a diagnostic consideration for feature interpretation in Stage 2.
- Evidence: Tables 3–6; Section 6.1, p.24: "High posted speed limits are only placed on roads with a low intersection and access point densities, therefore maintaining continuous traffic without many interruptions"
- Confidence: high for the confounding interpretation — consistent with general SPF literature and mechanistically plausible.

**Finding 4:**
- Finding: Simple SPFs (exposure only) and full SPFs (exposure + road geometry) show no significant difference in prediction performance (in-sample MAE/RMSE) for most road classes. The authors interpret this as validating the quality of the FDOT context classification system. An alternative interpretation is that the additional geometric variables add little explanatory power beyond what is already captured by road class membership — and/or that the in-sample MAE is an insufficient metric to distinguish model complexity.
- Why it matters: For Open Road Risk, this suggests that simple Poisson exposure models stratified by road class may already capture a substantial fraction of variance, and that adding many road geometry features may not improve prediction substantially. However, the null result on in-sample MAE does not exclude the possibility that geometry features improve ranking of high-risk segments, which is the relevant metric for Open Road Risk's purpose.
- Evidence: Table 3–6; "there was no significant difference in prediction performance of the developed simple and full SPFs for all road classes" (p.37)
- Confidence: medium — in-sample metric with no holdout; the comparison may have insufficient power to detect modest predictive improvements from geometry features at this sample size and with this metric.

**Finding 5:**
- Finding: The EB-adjusted EPDO-PSI network screening identified the most problematic segments as suburban commercial (C3C) and urban general (C4) roads in the Miami area. This confirms that urban roads have higher crash rates per VMT than rural roads despite lower absolute crash counts on rural roads.
- Why it matters: Open Road Risk includes empirical Bayes shrinkage as a diagnostic variant. The EB network screening procedure described in detail here (Equations 5–10) is methodologically mature, uses the NB overdispersion parameter from the fitted SPF, and is directly consistent with the HSM procedure. This provides a well-documented reference for Open Road Risk's EB shrinkage implementation.
- Evidence: Section 5.2 (pp.20–21), Equations 5–10; Table 7 / Figure 9 (pp.35–36)
- Confidence: high as a methodological reference — well-documented HSM procedure.

**Finding 6:**
- Finding: Sub-linear AADT coefficients for urban core roads (C5: 0.39; C6: 0.63 for AADT-SPFs) suggest that crash frequency scales less than proportionally with traffic volume in dense urban environments. This pattern is less pronounced in DVMT-SPFs (C5: 0.50; C6: 0.70) but still present.
- Why it matters: Open Road Risk's Stage 2 Poisson GLM uses a fixed offset (coefficient constrained to 1.0). If the relationship between crashes and exposure is genuinely sub-linear in urban areas, this constraint may cause the GLM to systematically underpredict crashes on high-AADT urban links or overpredict on low-AADT urban links. This deserves investigation in Open Road Risk's GLM residuals stratified by urban/rural classification.
- Evidence: Table 3, p.26 (C5 simple AADT-SPF: β = 0.39, SE 0.084; C6: β = 0.63, SE 0.104); Table 5, p.30
- Confidence: medium — specific to Florida urban context; may also reflect confounding with pedestrian/intersection crash contributions in dense urban areas rather than a genuine sub-linear exposure relationship.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| NB/Poisson GLM with ln(DVMT) = ln(AADT × length) as exposure | Confirms DVMT-SPFs outperform AADT-only SPFs; DVMT coefficients closer to 1.0 — supports current exposure offset design | AADT + link length — both present | ~10,500 segments, Florida statewide | High — already implemented as log-offset | Stage 2 — documentation / validation | Low (already implemented) | Coefficient sub-linearity in urban context warrants checking |
| Road-class-stratified SPF comparison (context-class vs statewide) | Tests whether road-type stratification improves model fit — directly applicable to Open Road Risk's multi-road-type dataset | Road classification — already present | ~10,500 segments | High | Stage 2 — diagnostic / small pilot | Low | In-sample comparison only; needs holdout validation for Open Road Risk |
| EB-adjusted EPDO-PSI network screening with overdispersion parameter from fitted NB/Poisson | Documented EB procedure for hotspot ranking; Equations 5–10 provide a complete methodological reference consistent with HSM | Observed crash counts + predicted counts + overdispersion parameter from Stage 2 GLM | Statewide | High — already partially implemented in Open Road Risk EB variant | Stage 2 — validation / documentation | Low (methodology documented; EB already present) | Open Road Risk's EB currently uses GLM predictions; ensure overdispersion parameter k is correctly estimated and used |
| Signalised intersection density (SID) as Stage 2 feature candidate | Consistently the most significant predictor across all 8 road classes and all models in this study | OS road network graph — count of signalised junctions derivable from OS Open Roads node types or OSM | Segment level | High — derivable from existing OS / OSM data; resolution differs from Florida FDOT data | Stage 2 — candidate feature | Medium (requires deriving junction density from OS/OSM) | OSM signalisation coverage in UK is incomplete; intersection density per km more reliable than signalised intersection density |
| Access point density (APD) as Stage 2 feature candidate | Consistently significant positive predictor; represents side-road and driveway conflict frequency | OS road network topology — count of connected minor links per segment length | Segment level | Medium — derivable from OS Open Roads adjacency; definition may differ from FDOT access points | Stage 2 — candidate feature | Medium | Definition mismatch: FDOT "access points" include driveways not captured in OS Open Roads |
| Sub-linear AADT coefficient diagnostic for urban links | Test whether Stage 2 GLM Poisson residuals show systematic bias by urban/rural class, suggesting fixed offset may be inappropriate for urban areas | Road link classification + GLM residuals — both present | Statewide | High | Stage 2 — diagnostic | Low | Single dataset in Florida; UK urban road crash patterns may differ |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| FDOT context classification system (C1–C6) | Florida-specific administrative classification based on FDOT criteria; no UK equivalent | Florida FDOT data | Florida statewide | Not applicable | UK rural/urban + road class + IMD deprivation is an approximate analogue; document as concept | High |
| Shoulder type (paved/lawn/curb-gutter), median type (raised/paved/vegetation), pavement condition score | Not available in UK open data at segment level | FDOT road inventory | Segment level | Low | OSM partially covers some of these at poor coverage | High |
| Bicycle slot presence, sidewalk spacing, shared path presence | Pedestrian/cyclist infrastructure features not available in UK national open data | FDOT inventory | Segment level | Low | OSM has some pedestrian/cycling features but coverage is sparse and inconsistent for modelling | High |
| Cross-sectional 5-year average model (no panel structure) | Open Road Risk uses link-year panel; averaging across years loses temporal variation and inflates effective sample size | Methodological choice | — | Low — Open Road Risk's panel structure is a design strength; reverting to cross-sectional average would lose temporal validation capability | Not recommended; retain panel structure | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?**
  Yes — NB coefficients on ln(AADT) and ln(DVMT) are near-unity for most road classes, with the notable exception of dense urban classes (C5, C6) where sub-linear coefficients suggest the fixed-offset constraint may be imprecise.

- **Does it suggest better handling of AADT/AADF uncertainty?**
  No — FDOT AADT is used directly without uncertainty propagation, same as Open Road Risk's current approach. Not addressed.

- **Does it suggest useful geometry or road-context features?**
  Yes — signalised intersection density and access point density are the most strongly and consistently supported new candidates for Open Road Risk. Speed limit is already present but its negative coefficient should be interpreted as a road-type confound, not a direct safety effect.

- **Does it suggest better modelling of junctions?**
  Indirectly — SID and APD capture junction conflict density at the segment level rather than modelling individual junctions. This is a practical alternative to explicit junction modelling at Open Road Risk's scale.

- **Does it suggest better treatment of severity?**
  Partially — separate SPFs for FI and PDO crashes used in network screening (EPDO-PSI) provide a severity-weighted ranking approach. This is simpler than Gilardi et al.'s bivariate joint model but more practical for large-scale production use.

- **Does it suggest better validation design?**
  No — the thesis uses no holdout validation. All metrics are in-sample. This is a weakness of the thesis relative to Open Road Risk's needs.

- **Does it expose a weakness in my current approach?**
  Yes — two weaknesses:
  1. Open Road Risk does not currently include intersection/access density features. This study provides consistent evidence across 8 road classes that these are the strongest predictors after exposure.
  2. Open Road Risk's fixed offset (coefficient = 1.0) may be inappropriate for dense urban links. The sub-linear AADT coefficients on C5/C6 suggest investigating GLM residual bias by urban/rural class.

---

## 15. Repo Actionability

**Action 1:**
- Suggested repo action: Add intersection density (junctions per km) as a candidate Stage 2 feature. Derive from OS Open Roads network topology — count of connected nodes per link or per km of road length within a road corridor buffer. Test correlation with AADT and road classification before including in model.
- Action type: candidate feature → small pilot
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: SID is the most consistently significant predictor across all 8 road context classes and all model variants in this study (Tables 3–6); conceptually captures traffic conflict density at access points
- Evidence: Tables 3–6; "intersections and access points densities are one of the most influential factors on crash occurrence" (p.37–38)
- Effort: medium (requires deriving junction density from OS Open Roads; check against OSM for signalised-only variant)
- Risk if implemented badly: collinearity with road classification and AADT; may not add value over existing features if road type already proxies for junction density. Run VIF check before including.

**Action 2:**
- Suggested repo action: Run a diagnostic of Stage 2 GLM Poisson residuals stratified by rural/urban classification (and ideally by road classification). Test whether residuals show systematic positive or negative bias on urban links — which would indicate the fixed exposure offset is inappropriate for urban roads where sub-linear AADT coefficients are expected.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: AADT coefficients on C5/C6 urban core roads are 0.39–0.63, substantially below 1.0; fixed offset assumes coefficient = 1.0 for all road types (Table 3, p.26)
- Evidence: Table 3, p.26
- Effort: low
- Risk if implemented badly: low — this is a diagnostic, not a production change. If bias is found, the appropriate response is a small pilot of road-class-stratified models, not immediate architecture change.

**Action 3:**
- Suggested repo action: Document the EB-adjusted EPDO-PSI network screening procedure (Equations 5–10 in the thesis) as a methodological reference for Open Road Risk's EB shrinkage implementation. Verify that the overdispersion parameter k from the fitted Stage 2 NB/Poisson GLM is correctly used in the EB weight calculation.
- Action type: documentation note / validation of existing feature
- Relevant stage: Stage 2 / documentation
- Why the paper supports it: Equations 5–10 provide a complete, HSM-consistent EB procedure; the EPDO-PSI approach accounts for crash severity weighting and regression-to-the-mean
- Evidence: Section 5.2, pp.20–21
- Effort: low
- Risk if implemented badly: low

**Action 4:**
- Suggested repo action: Run a model comparison diagnostic testing whether road-class-stratified models outperform a single global model on a held-out validation set (temporal or spatial). The Florida thesis shows CC-SPFs outperform statewide SPFs in-sample; Open Road Risk should test whether this holds on a grouped or temporal holdout before making stratification a production design choice.
- Action type: diagnostic / small pilot
- Relevant stage: Stage 2 / validation
- Why the paper supports it: In-sample MAE improvement from stratification is substantial (e.g., statewide AADT-SPF MAE for C1 = 37.5 vs CC-SPF MAE = 8.9), but no holdout validation means the advantage may partly reflect overfitting; this needs verification on Open Road Risk data
- Evidence: Figure 8, p.34; Tables 3–6
- Effort: medium
- Risk if implemented badly: stratified models on small road-class subsets may have insufficient data for some minor road types in Open Road Risk's coverage area

**Action 5:**
- Suggested repo action: Add a documentation note flagging that speed limit's negative coefficient in crash models is a known confound with access density and road type — higher speed limits on less-conflicted roads — rather than a direct safety effect. This applies to Open Road Risk's Stage 2 OSM speed limit feature and should be noted in feature interpretation documentation to avoid causal misreading of coefficient sign.
- Action type: documentation note
- Relevant stage: Stage 2 / feature engineering / documentation
- Why the paper supports it: Consistent negative speed limit coefficients across all Florida road classes explicitly attributed to road-type confounding (p.24); consistent with general SPF literature
- Evidence: Tables 3–6; p.24 discussion
- Effort: low
- Risk if implemented badly: low

---

## 16. Query Tags

- negative-binomial
- safety-performance-function
- SPF
- DVMT-exposure
- AADT-exposure
- near-offset
- road-class-stratification
- intersection-density
- access-point-density
- speed-limit-confound
- EB-network-screening
- EPDO-PSI
- empirical-bayes
- sub-linear-AADT-urban
- Florida
- cross-sectional
- no-holdout-validation
- segment-level
- in-sample-only
- US-transferable-with-caveats

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high for model coefficients, feature significance patterns, and SPF comparison results; medium for generalisability claims (thesis, no peer review, no holdout validation)
- Important details not stated in the thesis:
  - Exact minimum segment length threshold not stated (described only as applied to "avoid very short road segments")
  - No description of how AADT was assigned for segments without nearby counting stations
  - No temporal or spatial holdout validation — all metrics are in-sample
  - Number of total observations per model varies (94–3065 for CC-SPFs) due to correlation-based variable exclusion — smaller subsets for full models raise concerns about overfitting in some road classes
  - Network screening output is at segment level using FDOT road IDs and post mile — not directly mappable to OS Open Roads
- Parts of the thesis that need manual checking:
  - Figure 7 (correlation matrix) was not viewable; the variable exclusion decisions based on correlations > 0.5 are described but not fully verifiable
  - Figures 4, 5, 8, 9 not viewable; results described from tables and text
  - The DVMT full SPF for C3R (Table 5) includes a PSP (shared path) coefficient of +0.25, which is counterintuitive and contradicts the AADT full SPF where PSP has a negative coefficient; this inconsistency is not discussed in the thesis and warrants manual checking
- Any likely ambiguity or risk of misinterpretation:
  - The headline finding that "CC-SPFs outperform AT-SPFs and SW-SPF" is based entirely on in-sample MAE comparison. Without holdout validation, this comparison cannot be used as evidence that CC-SPFs generalise better to new data — only that they fit the training data better.
  - The near-zero difference between simple and full SPF performance is described as validating the FDOT classification system, but it could equally reflect that in-sample MAE is an insensitive metric for detecting modest improvements from geometry features.
  - This is a master's thesis, not a peer-reviewed journal article. The methodological rigour is lower than Gilardi et al. 2022 or Pan et al. 2017. Findings should be treated as directional evidence rather than strong empirical support.