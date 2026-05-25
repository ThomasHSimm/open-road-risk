# Paper Extraction — Methodological Metadata

## 0. Extraction Run Metadata

- Extraction date: 2026-05-11
- Source PDF filename: Comparative_Assessment_Of_Poisson_And_Ne.pdf
- Suggested Markdown filename: paper-extraction-asumadu-2015-poisson-NB-Ghana-road-accidents.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered as document text in context)
- Output mode: downloadable `.md` file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full 5-page paper accessible. Tables 2.1–2.3 fully legible. Figure 2.1 (mean plot) legible from caption and surrounding description.

---

## 1. Citation

- Title: Comparative Assessment Of Poisson And Negative Binomial Regressions As Best Models For Road Count Data
- Authors: Oppong Richard Asumadu, Assuah Charles Kojo, Asiedu-Addo Samuel Kwesi
- Year: 2015
- Journal: International Journal of Scientific Research and Engineering Studies (IJSRES), Volume 2 Issue 11, November 2015, pp.28–32
- ISSN: 2349-8862
- DOI or URL: Not stated. www.ijsres.com
- Country / region studied: Ghana
- Study setting: National-level (whole of Ghana); not road-class-specific; not spatially disaggregated

---

## 2. Core Objective

- One-sentence description: The paper compares Poisson and Negative Binomial regression models fitted to national-level road accident fatality counts in Ghana (aggregated by day of week and year), finding NB fits better due to over-dispersion in the Poisson model.
- Main purpose: Model comparison (Poisson vs NB); descriptive analysis of day-of-week pattern in road fatalities. Not a safety performance function (SPF) in the traditional exposure-adjusted sense.
- Evidence quote: "The ultimate goal of this study was to compare Poisson and Negative binomial regression models using road accident (count) data to assess which of them significantly fit count data." (Abstract, p.28)

---

## 3. Response Variable

- Target variable: Count of people killed in road accidents per day-of-week per year (Ghana national total)
- Collision type: Fatal only (killed); no injury severity breakdown below fatality level
- Severity handling: Fatal casualties only — not KSI or slight injury. Severity is therefore collapsed to the most extreme category.
- Count, binary, rate, risk score, severity class, or other: Count (annual total per day-of-week; no exposure offset or rate normalisation)
- Time window: 2001–2010 (10-year period); data aggregated to 70 observations (7 days × 10 years)
- Evidence quote: "The data for this study was a secondary data obtained from the Building and Road Research Institute... The study considered accident data for a ten year period from 2001 to 2010. The number of people killed by road accident was used as the response variable." (p.30)

---

## 4. Exposure Handling

- Exposure variable used: None. No traffic volume, population, road length, or vehicle-kilometres exposure variable is included as an offset or predictor.
- Traffic count source: Not applicable — no traffic data used.
- Whether exposure is modelled, observed, assumed, or ignored: Ignored. The model predicts raw fatality counts as a function of day of week and year only. There is no exposure normalisation.
- Treatment of missing or sparse traffic counts: Not applicable.
- Whether offset terms, rates, denominators, or normalisation are used: No offset, no rate. Raw count as outcome with no exposure adjustment.
- Evidence quote: "Since this study concentrates on pedestrian casualties, which mainly involve short walking and cycling trips and adjacent land use patterns in the city centre, traffic flows are excluded from the analysis." — **Not stated** in this paper; traffic flows are simply not included, with no stated justification.
- Transferability to my AADF/WebTRIS setup:
  - Mathematical model structure (Poisson vs NB comparison): **Medium** — the statistical comparison of Poisson vs NB is relevant as background for Open Road Risk's model family decision, but the absence of any exposure offset makes this paper's models not transferable as SPFs.
  - Substantive findings: **Low** — the day-of-week result is Ghana-specific, national aggregate, and not exposure-normalised; it has limited applicability to a UK road-link-level pipeline.
- Notes: The absence of an exposure offset is a critical limitation. The fatality counts are influenced by the volume of traffic and road usage on each day, which varies by day of week. Without exposure, the day-of-week coefficients conflate exposure variation with genuine risk variation. This is acknowledged nowhere in the paper.

---

## 5. Spatial Unit of Analysis

- Unit: National aggregate (Ghana national total per day-of-week per year). No spatial disaggregation.
- Segment length or segmentation rule: Not applicable — national aggregate.
- How crashes are assigned to the network: Police Motor Traffic and Transport Unit accident report forms; no spatial assignment or snapping described.
- Treatment of junctions/intersections: Not stated; national aggregate data does not distinguish junction vs mid-link crashes.
- Spatial aggregation risks: Extreme — entire national road network collapsed to a single daily count. All road-class, geographic, and contextual variation is lost. Results have no spatial resolution.
- Evidence quote: "The data for this study was a secondary data obtained from the Building and Road Research Institute of the Council for Scientific and Industrial Research. The data was originally collected using accident report form by the Motor Traffic and Transport Unit of the Ghana Police Service." (p.30)
- Relevance to OS Open Roads link-based pipeline: None. The spatial unit is the antithesis of link-level analysis.

---

## 6. Temporal Unit of Analysis

- Years covered: 2001–2010 (10 years)
- Temporal resolution: Annual total per day-of-week (70 observations = 7 days × 10 years)
- Whether seasonality or time-of-day is modelled: Day of week is the primary explanatory variable. Time of day is not modelled. Seasonality not addressed.
- Whether before-after or panel structure is used: Implicit panel (7 day categories × 10 year observations); year treated as a categorical covariate, not a continuous trend or temporal random effect.
- Evidence quote: "the day the accident occurred in a particular year which resulted in the deaths of the people as the explanatory variables." (p.30)
- Relevance to WebTRIS-style time profiles: Marginal. The finding that day-of-week significantly affects fatality counts is consistent with time-of-day exposure weighting as a concept, but the paper's day-of-week analysis uses raw counts without exposure adjustment, making it methodologically unsuitable as a direct reference for Stage 1b.

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Day of week (Mon–Sun) | Ghana Police accident report forms | Categorical dummy variables (Monday as base) | Primary explanatory variable; Saturday significantly highest fatal count; Wednesday lowest | Not transferable as a causal feature — no exposure adjustment; day-of-week counts reflect both exposure and risk |
| Year (2001–2010) | Ghana Police accident report forms | Categorical dummy variables (2001 as base) | Controls for year-to-year trend; most year dummies significant | Not transferable — year effect in a national Ghana aggregate has no direct application to UK link-level modelling |

No road characteristics, geometric features, traffic volume, population density, or network features are included. The model is a minimal day-of-week × year count model with no road safety SPF structure.

---

## 8. Model Architecture

- Algorithms/models used: Poisson GLM and Negative Binomial GLM, both with log link; estimated using maximum likelihood in R (`glm` function with `family=poisson` and `MASS::glm.nb`).
- Baseline model: Poisson GLM with log link
- Final/preferred model: Negative Binomial GLM (lower AIC, lower deviance, dispersion parameter closer to 1.0)
- Loss function or likelihood: Poisson log-likelihood; NB log-likelihood. MLE estimation.
- Offset/exposure term: None — no offset used.
- Spatial autocorrelation handling: Not addressed.
- Temporal dependence handling: Year treated as categorical dummy — captures year-level mean shifts but does not model autocorrelation or trends formally.
- Interpretability method: Coefficient table (Table 2.3) with z-values and p-values; AIC and deviance comparison (Table 2.2).
- Evidence quote: "The Generalized Linear Model (glm) procedure with both Poisson and Negative Binomial as the distributions specified using the Log link function." (p.31)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Over-dispersion test | Dispersion parameter | 2.297 | Poisson | >> 1; Poisson assumption violated; over-dispersion confirmed | Table 2.2, p.31 |
| Over-dispersion test | Dispersion parameter | 1.290 | Negative Binomial | Closer to 1; substantially reduced over-dispersion | Table 2.2, p.31 |
| Model comparison | AIC | 676.08 (Poisson) vs 663.6 (NB) | Both models | NB has lower AIC by ~12.5 units; preferred model | Table 2.2, p.31 |
| Model comparison | Null deviance | 689.08 (Poisson) vs 384.79 (NB) | Both models; 69 df | NB substantially lower null deviance | Table 2.2, p.31 |
| Model comparison | Residual deviance | 124.05 (Poisson) vs 69.64 (NB) | Both models; 54 df | NB substantially lower residual deviance | Table 2.2, p.31 |
| Coefficient (NB) | Saturday | 0.238 (z = 6.78, p = 1.2e-11) | NB model | exp(0.238) = 1.269 — Saturday fatalities 26.9% higher than Monday | Table 2.3, p.31 |
| Coefficient (NB) | Wednesday | −0.214 (z = −5.71, p = 1.1e-08) | NB model | exp(−0.214) = 0.807 — Wednesday fatalities 19.3% lower than Monday | Table 2.3, p.31 |
| Coefficient (NB) | Tuesday | −0.081 (z = −2.21, p = 0.027) | NB model | Lowest day coefficient; 7.8% reduction vs Monday | Table 2.3, p.31 |
| Coefficient (NB) | Intercept | 5.453 (z = 137, p < 2e-16) | NB model | exp(5.453) = 233.5 — expected Monday 2001 fatalities = 233 | Table 2.3, p.31 |

**Are these metrics in-sample, out-of-sample, cross-validated, or not stated?**

All in-sample. AIC penalises complexity but is not an external validation metric. No train/test split, no temporal holdout, no cross-validation.

**Do these metrics test predictive generalisation?**

No. AIC and deviance are model comparison/fit metrics. No predictive accuracy or generalisation is assessed.

**Are any metrics likely to be optimistic?**

Yes — the dispersion parameter for the NB model (1.290) is close to 1, but this is measured on the same data used to fit the model. The AIC difference (~12.5) is meaningful but small relative to n = 70. The paper does not test whether NB generalises better out-of-sample.

**Which metric is most relevant to Open Road Risk?**

The over-dispersion finding (Poisson dispersion parameter >> 1) is the methodologically relevant result: it confirms what is expected and well-established in the road safety literature — that raw road accident count data typically exhibit over-dispersion. The specific magnitude (2.297 for Ghana national-aggregate fatalities) is not transferable to Open Road Risk's UK link-year context.

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Not addressed. The response variable is Ghana national annual fatality counts by day-of-week — these are aggregate counts ranging from ~2,164 to ~3,410 over 10 years (i.e., ~216–341 per year per day). There are no zeros in this dataset. This is the opposite problem from Open Road Risk's sparse link-year structure.
- Use of Poisson / NB / zero-inflated / hurdle models: Poisson and NB only. Zero-inflated or hurdle models are not discussed and are not needed for this dataset (no zeros).
- Whether high-risk locations are evaluated separately: Not applicable — national aggregate.
- Evidence quote: Not stated; confirmed by Table 2.1 showing minimum annual mean per day = 216.4 (Wednesday), maximum = 341 (Friday).
- Practical relevance to my sparse collision link-year dataset: Very limited. This paper's data has no zero-count problem; Open Road Risk's link-year data is ~98–99% zeros. The over-dispersion finding (NB > Poisson) is a general result well-known in the literature; this paper adds no new methodological insight relevant to zero-heavy data beyond what Khodadadi et al. (2021) provides in much greater depth.

---

## 11. Validation Strategy

- Train/test split method: None
- Spatial holdout used? No
- Temporal holdout used? No
- Grouped holdout used? No
- Cross-validation type: None
- Metrics: AIC, deviance (in-sample); p-values for coefficients
- External validation: None
- Leakage or generalisation risks: n = 70 with ~16 parameters (6 day dummies + 9 year dummies + intercept + dispersion) — moderate parameterisation for the sample size. No validation performed.
- Evidence quote: Not stated.
- What I should copy or avoid: Nothing substantive to copy beyond the basic Poisson vs NB AIC comparison framework, which is already standard practice. Do not use this paper as a primary reference for model family choice in Open Road Risk — Khodadadi et al. (2021) and Wang et al. (M25) both provide more rigorous evidence from road-safety-relevant data.

---

## 12. Key Findings Relevant to My Project

**Finding 1**
- Finding: Poisson regression produced a dispersion parameter of 2.297, substantially exceeding 1.0, confirming over-dispersion in the road accident count data. NB regression reduced this to 1.290 and achieved lower AIC (663.6 vs 676.08), lower null deviance (384.79 vs 689.08), and lower residual deviance (69.64 vs 124.05).
- Why it matters: Provides a further data point (alongside Khodadadi et al. 2021 and Wang et al. M25) that road accident count data exhibit over-dispersion that Poisson does not handle, motivating NB as the baseline SPF family. However, this paper's result is on Ghana national aggregate fatality counts with no exposure adjustment, making it methodologically weaker than the other papers in this review as evidence for Open Road Risk's specific context.
- Evidence: Table 2.2, p.31.
- Confidence: High for the directional finding (NB > Poisson); Low for the specific magnitude or any Open Road Risk application.

**Finding 2**
- Finding: Day-of-week is a statistically significant predictor of road fatality counts in Ghana, with Saturday highest (OR 1.27 vs Monday) and Wednesday/Tuesday lowest. Friday had the highest raw count overall but Saturday emerges as highest when year is controlled.
- Why it matters: Not directly transferable to Open Road Risk's pipeline (no exposure adjustment, Ghana context, national aggregate). However, it provides corroborating context that day-of-week exposure patterns are real and can affect apparent crash counts — consistent with the rationale for Stage 1b's time-of-day profiling. The methodological point is weaker than Wedagama et al. (2008), which models time-of-day effects with exposure adjustment.
- Evidence: Table 2.3; Section II.B, p.31.
- Confidence: Medium for the Ghana-specific day-of-week pattern; Low for any UK or link-level application.

**Finding 3**
- Finding: The paper demonstrates that using AIC to compare Poisson vs NB is a straightforward, standard practice in road safety modelling (both models estimated in R using `glm`/`glm.nb`; AIC extracted directly). This is confirmatory, not novel.
- Why it matters: No new insight; confirms standard practice. The AIC comparison is already used in Open Road Risk's planned NB diagnostic.
- Evidence: Table 2.2; Section II.B, p.31.
- Confidence: High for the method being standard; irrelevant as a standalone finding.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| AIC comparison of Poisson vs NB using R `glm`/`glm.nb` | Confirms standard model comparison workflow; already a Stage 2 TODO | Crash counts (already in pipeline) | 70 national-aggregate observations | Fully compatible as a method | Stage 2 / diagnostic — already planned | Low | Not novel; already planned |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Day-of-week as a predictor of crash fatality counts | No exposure adjustment; national aggregate; Ghana-specific; fatality-only outcome | Traffic volume data absent; spatial disaggregation absent | National aggregate | Incompatible — wrong spatial unit, no exposure, wrong country | Not applicable; WebTRIS Stage 1b addresses time-of-day exposure differently | High |
| Model coefficients (intercept, day dummies, year dummies) | Ghana national fatalities; no exposure; not transferable to UK link-level risk | Different country, road system, units, no normalisation | National aggregate | Incompatible | Not applicable | High |
| No-offset count model | Omitting exposure is a methodological weakness for SPF purposes; explicitly not transferable | No traffic volume data included | National aggregate | Incompatible — Open Road Risk requires exposure normalisation | Not a workaround; retain exposure offset | High |

---

## 14. Pipeline Implications

**Does this paper support using exposure-normalised collision risk?**
By omission — the lack of an exposure offset in this paper is a weakness, not a feature. The paper implicitly illustrates why exposure normalisation is necessary: day-of-week raw counts reflect both traffic volume variation and risk variation, making the coefficients uninterpretable as risk estimates.

**Does it suggest better handling of AADT/AADF uncertainty?**
No.

**Does it suggest useful geometry or road-context features?**
No — no geometry features are used.

**Does it suggest better modelling of junctions?**
No.

**Does it suggest better treatment of severity?**
Not usefully — fatality-only analysis is the response variable; no severity gradient is modelled.

**Does it suggest better validation design?**
No — no validation is performed.

**Does it expose a weakness in my current approach?**
No direct weakness exposed. The paper is confirmatory of well-established points (NB > Poisson for over-dispersed data) that are better evidenced by Khodadadi et al. (2021) in a more relevant context.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: No new repo actions warranted from this paper specifically. The Poisson vs NB comparison is already a documented Stage 2 TODO, better evidenced by Khodadadi et al. (2021). This paper could be cited as further background context for over-dispersion being common in road accident count data, but should not be a primary reference.
- Action type: No action required
- Relevant stage: N/A
- Why: All substantive findings are either (a) already planned in Open Road Risk, (b) better supported by other papers in this review, or (c) not transferable to the pipeline context.
- Effort: N/A
- Risk: N/A

---

## 16. Query Tags

- Poisson-vs-NB
- over-dispersion
- AIC-comparison
- negative-binomial
- road-fatalities
- day-of-week
- national-aggregate
- Ghana
- no-exposure-offset
- no-spatial-disaggregation
- no-validation
- low-transferability
- descriptive-analysis
- maximum-likelihood
- R-statistical-software
- low-volume-analog-absent
- fatality-only
- confirmatory-only

---

## 17. Confidence and Gaps

- Overall confidence in extraction: High (paper is simple and short; findings are clearly stated)
- Important details not stated in the paper:
  - No DOI provided
  - The IJSRES journal (ISSN 2349-8862) is a low-visibility open-access journal; publication quality should be treated accordingly. The paper's methodology is sound at a basic level but does not add to the road safety SPF literature beyond confirming standard textbook knowledge.
  - Whether the dispersion parameter reported (2.297 for Poisson; 1.290 for NB) is the Pearson chi-squared/df statistic or the estimated NB dispersion parameter α is not entirely clear from the text, though context suggests the former for Poisson and the latter for NB.
  - "Saturday significantly had the highest number of people killed in road accidents in Ghana" (Abstract) — this contradicts the raw data (Friday has the most in Table 2.1), and is only true in the NB model when year is controlled. The paper explains this but the Abstract is misleading.
- Parts needing manual checking:
  - Table 2.3: Saturday coefficient 0.238497 → exp(0.238497) = 1.269, described in text as 1.2693340. Checks out. Tuesday coefficient −0.081113 → exp(−0.081113) = 0.922, described as "0.922089 which means the expected number killed on Tuesday was 7.8% lower." Checks out.
  - AIC difference: 676.08 (Poisson) − 663.6 (NB) = 12.48 units. By convention ΔAIC > 10 is considered strong evidence; this just crosses that threshold. Not a large margin.
- Any likely ambiguity or risk of misinterpretation:
  - The paper should not be cited as evidence that NB is preferred over Poisson for Open Road Risk's specific link-year context, which has very different data characteristics (zero-heavy, exposure-adjusted, UK, link-level). Khodadadi et al. (2021) is the appropriate reference for that purpose.
  - The absence of an exposure offset means the day-of-week coefficients are confounded with daily traffic volume variation. Friday's high raw count likely reflects higher traffic volumes (commuting, leisure), not necessarily higher per-vehicle-km risk. The paper does not acknowledge this limitation.
