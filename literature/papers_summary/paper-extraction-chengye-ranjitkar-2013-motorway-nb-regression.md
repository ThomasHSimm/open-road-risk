# Paper Extraction — Chengye & Ranjitkar 2013

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: Modelling_Motorway_Accidents_using_Negative_Binomial_Regression.pdf
- Suggested Markdown filename: paper-extraction-chengye-ranjitkar-2013-motorway-nb-regression.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered in context as text + page images)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Conference proceedings paper (Eastern Asia Society for Transportation Studies, Vol.9, 2013); fully accessible. No supplementary material referenced.

---

## 1. Citation

- Title: Modelling Motorway Accidents using Negative Binomial Regression
- Authors: Pan Chengye, Prakash Ranjitkar
- Year: 2013
- DOI or URL, if present: Not stated. Published in Proceedings of the Eastern Asia Society for Transportation Studies, Vol. 9, 2013.
- Country / region studied: New Zealand (Auckland motorway network, State Highway 1N)
- Study setting: motorway only (urban and rural motorway sections, State Highway 1N, 74 km)

---

## 2. Core Objective

- One-sentence description: The paper develops negative binomial regression accident prediction models for a 74 km Auckland motorway section, relating annual accident frequency per segment-year to traffic, geometric, operational, and weather variables, and tests predictive performance on a held-out 2-year dataset.
- Main purpose: safety performance function / accident prediction model / feature importance analysis
- Evidence quote: "The main objective of this paper is to develop accident prediction models for Auckland motorway… the association between motorway accident frequency and non-behavioural contributing factors" (Section 1, p. 2)

---

## 3. Response Variable

- Target variable: Annual accident count per road segment (all recorded crashes on the motorway mainline; ramp accidents excluded)
- Collision type: all crashes (injury + property damage; severity not disaggregated in modelling). The source is New Zealand's CAS (Crash Analysis System), which includes injury and fatal crashes; PDO inclusion not explicitly confirmed but implied by total count of 10,149 crashes across 7 years.
- Severity handling: Not modelled separately. All crash severities combined into a single count.
- Count, binary, rate, risk score, severity class, or other: count (accident frequency per segment per year)
- Time window used for outcomes: annual; 2004–2010 (7 years); model fitted on 2004–2008, validated on 2009–2010
- Evidence quote: "Each year data from a segment was treated as a sample giving a total of 959 data samples" (Section 4, p. 5)

---

## 4. Exposure Handling

- Exposure variable used: AADT per lane (in thousands of vehicles/day), used as a log-transformed predictor variable (ln AADT per lane). Segment length (ln L) is also included as a log-transformed covariate.
- Traffic count source: Traffic Monitoring System (TMS) operated by New Zealand Transport Agency; vehicle sensors and detectors installed along State Highway. Observed AADT data available for the study corridor; some missing values noted in Table 1.
- Whether exposure is modelled, observed, assumed, or ignored: observed (AADT directly available from TMS for the study corridor). No estimation step required.
- Treatment of missing or sparse traffic counts: Missing AADT and heavy vehicle percentage values noted in Table 1 footnote ("Segment number N is 959 except for AADT and Percentage of heavy traffic with some missing figures"). No imputation method described.
- Whether offset terms, rates, denominators, or normalisation are used: No formal offset term. Segment length and AADT per lane are both included as log-transformed predictor variables with freely estimated coefficients (not constrained to 1.0 as a formal offset). This is an important distinction from my Stage 2 pipeline. The model form is: E(yi) = exp(β0 + β1×ln L + β1×ln AADT_per_lane + Σβi×xi). Length coefficient estimated as 0.806–1.578 depending on model (not constrained to 1.0).
- Evidence quote: "E(yi) = exp(β0 + β1×ln L + β1×ln AADT per lane + Σβi×xi)" (equation 10, p. 9)
- Transferability to my AADF/WebTRIS setup: medium
- Notes:
  - The use of AADT per lane rather than total AADT is a modelling choice that implicitly adjusts for the number of lanes. It is not a formal exposure offset; it is a feature in the linear predictor.
  - The paper does not use a formal log offset (log(AADT × length × days)), unlike my Stage 2. Including ln(L) as a free coefficient rather than a constrained offset is a weaker approach theoretically; it allows the model to partially compensate for poor exposure specification but makes interpretation less clean.
  - Observed AADT available for every link in this study. My pipeline estimates AADT via Stage 1a for unobserved links, which is a more complex setup not addressed here.
  - Ramp AADT is included as a separate predictor for segments near ramps, capturing the additional traffic conflict volume — this is a candidate feature for my motorway-class links.

---

## 5. Spatial Unit of Analysis

- Unit: homogeneous road segment (motorway mainline only; ramp accidents excluded)
- Segment length or segmentation rule: Variable length; segments defined as homogeneous in traffic features and key road design characteristics (number of lanes, lane width, horizontal alignment). Ramp presence was the primary segmentation criterion: segments classified as with on-ramp (1,000 m total, 500 m either side of ramp), with off-ramp (500 m), or without ramp. Segments without ramp further subdivided on changes in lanes or curvature. Length range: 0.27–2.94 km (mean 0.97 km, SD 0.53 km). Minimum length 0.2 km and maximum 3 km imposed to mitigate heteroscedasticity and excess zeros from very short segments.
- How crashes are assigned to the network: Direct assignment via CAS spatial location to the motorway segment record. No snapping methodology described; crashes apparently already georeferenced to the motorway network in CAS.
- Treatment of junctions/intersections: Ramps explicitly included as a segment-type category (on-ramp, off-ramp, no ramp). Grade-separated intersections are inherent to motorway design; at-grade intersections not present. Ramp AADT included as a predictor for segments near ramps.
- Spatial aggregation risks: Northbound and southbound carriageways treated as separate segments. Segments sharing a rainfall station may have identical weather variables. Some segments near the CBD have closely spaced ramps; the paper notes these as a cluster of high-accident segments.
- Evidence quote: "These segments were homogeneous in terms of traffic features and key roadway design characteristics including number of lanes, lane width and horizontal alignments" (Section 4, p. 5); "Segments shorter than 0.2 km or longer than 3 km were avoided to mitigate the heteroskedasticity problem" (Section 4, p. 5)
- Relevance to OS Open Roads link-based pipeline: Moderate. My OS Open Roads links are not defined by homogeneity rules or ramp presence; they are defined by OS topology (junction-to-junction). The paper's segmentation approach (homogeneous segments with ramp-based splitting) is more granular and purposeful than OS link geometry. The paper's finding that ramp-split models significantly outperform overall models is relevant context for my motorway-class links, but implementing ramp-aware segmentation on OS Open Roads would require additional data sources (OSM or OS-specific ramp tags).

---

## 6. Temporal Unit of Analysis

- Years covered: 2004–2010 (7 years total; 5 years fitting, 2 years prediction)
- Temporal resolution: annual (each segment-year is one observation)
- Whether seasonality or time-of-day is modelled: No. Annual totals for accidents and annual average values for all predictors. No sub-annual or time-of-day structure.
- Whether before-after or panel structure is used: Panel (segment × year), but temporal dependence between observations from the same segment across years is not explicitly modelled. The paper notes that Caliendo et al. (2007) and GEE (Abdel-Aty and Abdalla 2004; Lord and Persaud 2000) address temporal dependence, and the paper tests a GEE model as a comparison (Table 6), but the primary models are standard negative binomial without panel correction.
- Evidence quote: "A 5-year period (2004 to 2008) dataset was employed in the model development, and a 2-year period (2009 and 2010) dataset was used for testing the prediction performance" (Section 6, p. 10)
- Relevance to WebTRIS-style time profiles: None direct. Annual resolution only.

---

## 7. Engineered Features

Features actually used in at least one reported model (Tables 3, 4, 5).

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| ln(segment length) | Road network geometry | Natural log of segment length in km | Controls for segment length in accident count model; coefficient ~0.8–1.6 across models | Already present — ln(link_length_km) effectively enters via my exposure offset; compare implementation |
| ln(AADT per lane) | TMS traffic sensors | AADT / number of lanes; log-transformed | Dominant predictor; accounts for both volume and lane dilution of conflicts | Partially present — my Stage 2 uses total AADT in offset; AADT per lane as a feature is a candidate for motorway links |
| Percentage of heavy vehicles | TMS | % HGV or heavy vehicle in traffic stream | Positive effect on accident frequency; trucks cause speed variance | Already present as candidate feature — HGV proportion in my Stage 2 feature set |
| On-ramp AADT | TMS | AADT of on-ramp, 0 for non-ramp segments | Positive effect on urban mainline accidents (increased merging conflicts) | Low transferability — ramp-level AADT not available from AADF/OS Open Roads; ramp presence flag may be derivable from OS data |
| Off-ramp AADT | TMS | AADT of off-ramp, 0 for non-ramp segments | Positive effect on accident frequency near diverge zones | Low transferability — same as above |
| Presence of on-ramp (binary) | Road inventory (RAMM) | 1 = segment has on-ramp, 0 = no ramp | Positive effect on rural motorway segments | Medium — form of way / junction type in OS Open Roads may enable a ramp-presence indicator |
| Number of lanes | RAMM road inventory | Count of through lanes | Positive effect in all models; more lanes = more lane-change conflicts | Partially present — lane count sparse in OSM; not in OS Open Roads directly |
| Lane width (m) | RAMM road inventory | Binary: 3.5 m or 3.6 m | Wider lanes associated with more accidents on rural segments (possible risk compensation) | Low — lane width not available in OS Open Roads; sparse in OSM |
| Median type (steel/concrete) | RAMM road inventory | Binary indicator | Concrete median associated with higher accident frequency; functions as urban/rural proxy | Not present — no direct equivalent in OS Open Roads or OSM for UK motorways |
| Width of median (m) | RAMM road inventory | Continuous measurement in metres | Wider median beneficial on rural segments and off-ramp segments | Not present — not available in open UK data |
| Width of shoulder (m) | RAMM road inventory | Continuous measurement in metres | Mixed effects: reduces accidents on non-ramp segments but increases on ramp segments | Not present — not available in OS Open Roads; very sparse in OSM |
| Average curvature (1/m) | RAMM road inventory | Average of 1/radius for all horizontal curves in segment | Negative effect on accident frequency (risk compensation at curves) | Partially present — my pipeline has curvature as a candidate feature; compare implementation |
| Maximum curvature (1/m) | RAMM road inventory | Maximum 1/radius in segment | Used for rural and off-ramp models | Partially present — same as above |
| Average vertical up-grade (%) | RAMM road inventory | Average uphill gradient in segment | Positive effect on accidents without ramps (speed variance from trucks) | Partially present — grade from OS Terrain 50 is in my pipeline; compare implementation |
| Maximum vertical down-grade (%) | RAMM road inventory | Maximum downhill gradient in segment | Positive effect on non-ramp segments (braking distance) | Partially present — same as above |
| Speed limit (km/h) | Highway Information Sheets | Binary: 80 km/h or 100 km/h | Higher accident frequency at 80 km/h zones (confounded: lower limits applied at known high-risk locations) | Partially present — OSM speed limit is a candidate feature in my pipeline; note confounding risk |
| Annual rainfall (mm) | National Climate Database | Annual total precipitation assigned from nearest of 7 weather stations | Negative effect (counterintuitive; likely traffic volume reduction in rain) | Not present — weather data not in my pipeline; low priority given likely confounding |
| Annual wet days | National Climate Database | Count of days with ≥1 mm rain | Negative effect on non-ramp segment accidents | Not present — same as above |

---

## 8. Model Architecture

- Algorithms/models used: Negative binomial regression (primary); Poisson regression (tested, rejected due to overdispersion); zero-inflated negative binomial (tested, rejected; not many zero-accident segments); GEE model (tested as panel correction comparison)
- Baseline model: Poisson regression (rejected); overall negative binomial model (Table 3)
- Final/preferred model: Ramp-type-specific negative binomial models (Table 5: separate models for segments without ramp, with on-ramp, with off-ramp) — best MAD and MSPE on both fitting and prediction datasets
- Loss function or likelihood: Maximum likelihood estimation; negative binomial log-likelihood (equation 8)
- Offset/exposure term: None formal. Segment length enters as ln(L) with freely estimated coefficient (0.806 overall; 0.536–1.578 across sub-models). AADT per lane enters as ln(AADT per lane) with freely estimated coefficient (1.111–2.311 across models).
- Spatial autocorrelation handling: Not addressed. Standard negative binomial treats each segment-year independently.
- Temporal dependence handling: Not formally modelled in primary models. GEE is tested as comparison (Table 6) but negative binomial marginally outperforms on MAD/MSPE. No segment-grouped split or random effects for repeated years.
- Interpretability method: Coefficient signs and t-statistics reported; direction and magnitude of effects discussed in text.
- Goodness of fit: Pseudo-R² (ρ²) as defined in equation 9: ρ² = 1 − LL(β)/LL(0). Values range from 0.088 (urban model) to 0.194 (on-ramp model). Overall model ρ² = 0.119. Overdispersion parameter α reported (0.106–0.183 across models).
- Evidence quote: "After evaluating the predictive performances of all of the above mentioned models, it was found that the negative binomial model is the most desirable approach for this case" (Section 5, p. 7)

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model fit | Pseudo-R² (ρ²) | 0.119 | Overall NB model (N=652) | Low-moderate in-sample fit | Table 3, p. 11 |
| Model fit | Pseudo-R² (ρ²) | 0.163 | Rural NB model (N=227) | Better fit for rural segments | Table 4, p. 12 |
| Model fit | Pseudo-R² (ρ²) | 0.088 | Urban NB model (N=425) | Weakest in-sample fit | Table 4, p. 12 |
| Model fit | Pseudo-R² (ρ²) | 0.131 | Non-ramp NB model (N=241) | Improved over overall | Table 5, p. 14 |
| Model fit | Pseudo-R² (ρ²) | 0.194 | On-ramp NB model (N=192) | Best in-sample fit among all models | Table 5, p. 14 |
| Model fit | Pseudo-R² (ρ²) | 0.110 | Off-ramp NB model (N=190) | Moderate | Table 5, p. 14 |
| Overdispersion | α parameter | 0.183 | Overall model | Significant overdispersion; NB preferred over Poisson | Table 3, p. 11 |
| Overdispersion | α parameter | 0.106–0.130 | Ramp-split models | Lower overdispersion in sub-models than overall model | Table 5, p. 14 |
| Predictive accuracy (held-out) | MAD | 4.07 | Overall NB model | Mean absolute prediction error on 2009–2010 holdout | Table 6, p. 16 |
| Predictive accuracy (held-out) | MAD | 3.98 | Rural+urban models | Marginal improvement | Table 6, p. 16 |
| Predictive accuracy (held-out) | MAD | 3.70 | Ramp-split models (preferred) | Best predictive MAD | Table 6, p. 16 |
| Predictive accuracy (held-out) | MSPE | 36.60 | Overall NB model | Mean squared prediction error on holdout | Table 6, p. 16 |
| Predictive accuracy (held-out) | MSPE | 34.23 | Rural+urban models | Marginal improvement | Table 6, p. 16 |
| Predictive accuracy (held-out) | MSPE | 27.87 | Ramp-split models (preferred) | Best predictive MSPE; ~24% reduction vs overall | Table 6, p. 16 |
| Predictive accuracy (fit data) | MAD / MSPE | 3.21 / 24.92 | Ramp-split models, fitting data | In-sample fit for reference | Table 6, p. 16 |
| GEE comparison | MAD / MSPE | 3.74 / 34.46 | GEE overall model, fitting data | NB slightly outperforms GEE | Table 6, p. 16 |
| Coefficient | ln(AADT per lane) | 2.006 (t=19.3) | Overall model | Dominant traffic predictor; elasticity ~2 | Table 3, p. 11 |
| Coefficient | ln(length) | 0.806 (t=12.2) | Overall model | Sub-proportional length effect (not 1.0) | Table 3, p. 11 |
| Coefficient | Number of lanes | 0.634 (t=15.9) | Overall model | More lanes → more accidents | Table 3, p. 11 |

**Metric qualification:**

- Pseudo-R² (ρ²) values are **in-sample model comparison metrics** relative to a constants-only model. They do not measure predictive accuracy on unseen data. Values of 0.088–0.194 are typical for count regression models on road accident data and do not indicate poor model fit in the field-specific sense.
- MAD and MSPE on the 2-year holdout (2009–2010) are **out-of-sample temporal holdout metrics** — this is the strongest validation in the paper. The holdout is temporal, not spatial; the same 137 segments appear in both fitting and prediction datasets. There is no spatial holdout.
- The temporal holdout is a genuine test of predictive performance (though not spatial generalisation). It is the most relevant metric for my pipeline.
- Overdispersion parameter α is an in-sample fit diagnostic, not a predictive metric.
- The mean accident frequency in this study is 8.77/year per segment (Table 1), which is much higher than my link-year data (~0.01–0.02/year per link-year). MAD and MSPE values are not directly comparable across studies at different mean counts.
- Most relevant metric to Open Road Risk: the temporal holdout MAD/MSPE comparison across model specifications (Table 6), which shows the value of facility-family splitting (ramp-type models reduce MSPE by ~24% over the overall model).

---

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled: Zero-heavy counts handled using negative binomial regression, which accommodates overdispersion relative to Poisson. The paper notes that zero-inflated Poisson is inappropriate "as there are not many sections with zero accident frequency" (Section 5, p. 7). The minimum segment length constraint (≥0.2 km) is also noted to mitigate excess zeros from very short segments.
- Use of Poisson / negative binomial / zero-inflated models / hurdle models: Negative binomial used. Zero-inflated NB was explicitly tested and rejected. The paper notes that zero-inflated models are appropriate "when considerable zeros and extremely low mean value are observed" (p. 3), which does not apply here (mean = 8.77 accidents/year per segment).
- Whether high-risk locations are evaluated separately: No formal treatment of high-risk locations. Sub-model stratification (by ramp type, urban/rural) is the primary approach to handling heterogeneity.
- Evidence quote: "Zero-inflated Poisson model is inappropriate as there are not many sections with zero accident frequency" (Section 5, p. 7)
- Practical relevance: **Low direct relevance to my pipeline.** This paper operates in a high-count regime (mean 8.77 accidents/segment/year; 0% zeros not explicitly stated but very few given Table 1 min=0). My pipeline has ~98–99% zeros at link-year level. The paper's zero-inflated model discussion is background only; the NB model used here would face much more severe zero inflation at my scale. The paper explicitly rejects zero-inflated models because the data are not sparse enough — the opposite of my situation.

---

## 11. Validation Strategy

- Train/test split method: Temporal split. 5 years (2004–2008) for model fitting; 2 years (2009–2010) for prediction testing. Same 137 segments appear in both.
- Spatial holdout used: No
- Temporal holdout used: Yes — 2009–2010 held out from fitting
- Grouped holdout used: No — segments present in both fitting and holdout periods
- Cross-validation type: None
- Metrics: MAD and MSPE computed on both fitting and prediction datasets for all model variants (Table 6)
- External validation: None
- Leakage or generalisation risks:
  - The same physical road segments appear in both fitting and prediction periods. The model learns segment-specific characteristics (geometry, lane count, etc.) from the fitting period and these are unchanged in the prediction period. This is not classical leakage (there is no direct use of holdout outcomes during training), but it means the model is tested on the same roads, not on new roads. Spatial generalisation is not tested.
  - The 2-year holdout is short relative to the 5-year fitting period; road conditions, traffic patterns, and accident frequencies may have changed systematically, but the paper does not discuss this.
  - Variable selection used 80% confidence level (not 95%). This is a weak significance threshold that increases the risk of retaining spurious variables that reduce out-of-sample performance.
- Evidence quote: "A 5-year period (2004 to 2008) dataset was employed in the model development, and a 2-year period (2009 and 2010) dataset was used for testing the prediction performance" (Section 6, p. 10)
- What I should copy or avoid:
  - **Copy**: the temporal holdout design (MAD and MSPE on held-out years) is a simple and useful complement to my grouped-link cross-validation. Adding a temporal holdout (e.g. holding out 2023–2024) would test temporal generalisation independently of my existing grouped link split.
  - **Avoid**: accepting 80% significance as a threshold for variable selection — this will retain noise variables and inflate reported pseudo-R². My pipeline's feature selection should use standard 95% threshold or cross-validated importance.
  - **Avoid**: treating pseudo-R² as evidence of predictive performance. The paper's ρ² values are in-sample only.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: In this case study on a 74 km Auckland motorway, stratifying models by ramp type (no ramp / on-ramp / off-ramp) produced substantially better predictive performance on the 2-year holdout than either the overall model or the rural/urban split (MSPE reduced from 36.60 to 27.87; MAD from 4.07 to 3.70). All ramp-type sub-models had lower overdispersion parameters than the overall model.
- Why it matters: This provides support for facility-family splitting in my Stage 2 model, specifically for motorway-class links. Splitting by ramp presence (or form of way in OS Open Roads terms: slip roads, motorway mainline, etc.) may improve predictive accuracy. This is consistent with the motorway overfitting noted in my v1 facility-family split.
- Evidence: Table 6 MAD/MSPE comparison; Section 8 conclusion p. 16: "applying different models for motorway segments without ramp, with on-ramp and with off-ramp can obtain more precise accident frequency prediction"
- Confidence: medium (single motorway corridor; New Zealand context; temporal holdout only, not spatial)

**Finding 2:**
- Finding: ln(AADT per lane) is the dominant traffic predictor across all models (coefficient ~1.1–2.3, t-statistic 5–19). The number of lanes has a separate significant positive effect (coefficient ~0.5–1.1 across models). This suggests that both total volume and lane-structure should be included for motorway links, not just total AADT.
- Why it matters: My Stage 2 currently uses total AADT in the exposure offset. For motorway-class links, the number of lanes modifies the per-lane traffic intensity and conflict dynamics. Lane count is sparse in OSM but might be derivable for motorways where OSM coverage is better than for minor roads.
- Evidence: Tables 3, 4, 5; Section 6 discussion of AADT per lane and number of lanes, pp. 10–11
- Confidence: medium (consistent across all sub-models; motorway-specific; lane count required)

**Finding 3:**
- Finding: Both on-ramp and off-ramp AADT have significant positive effects on accident frequency for urban motorway segments, while only ramp presence (not AADT volume) matters for rural segments. The paper interprets this as reflecting the density and speed differential of merging/diverging traffic.
- Why it matters: My pipeline does not currently include any ramp-proximity or junction-type features for motorway links. For the motorway-class subset of my data, a ramp-presence indicator (derivable from OS Open Roads form-of-way or OSM tags) may be a useful binary feature even without exact ramp AADT data.
- Evidence: Table 4 rural vs urban coefficients; Section 6 discussion, p. 10–11
- Confidence: medium (plausible mechanism; single corridor; ramp AADT not available in my open data)

**Finding 4:**
- Finding: Horizontal curvature has a consistently negative effect on accident frequency across all models where it appears (coefficient −0.133 to −0.448). The paper attributes this to risk compensation — drivers become more cautious on visible curves. The paper notes this is consistent with Shankar et al. (1995), Anderson et al. (1999), and Chang (2005).
- Why it matters: My pipeline has curvature as a candidate feature, and the expected direction (more curvature → more accidents) differs from what this paper finds for motorways. The paper's finding — that curvature reduces accidents on motorways via visual warning — suggests the curvature effect may be road-type-specific. I should not assume a uniform positive curvature effect across all facility families.
- Evidence: Table 3 coefficient −0.200 (t=−2.49); Tables 4, 5; Section 6 discussion p. 11: "A possible interpretation of this result is that visual effect created by curves becomes stronger as the curvature increases and drivers tend to be more cautious"
- Confidence: medium (consistent across all motorway sub-models; direction opposite to rural roads in other literature; risk compensation is plausible but not confirmed)

**Finding 5:**
- Finding: Maximum vertical up-grade has a significant positive effect on non-ramp motorway segments (coefficient 0.107–0.154), while average and maximum down-grade effects vary by segment type. The paper attributes up-grade effects to speed variance from trucks.
- Why it matters: Grade from OS Terrain 50 is already in my pipeline as a candidate feature. The paper provides directional support for including grade, particularly maximum rather than average grade, and for distinguishing up-grade from down-grade effects for motorway-class links.
- Evidence: Tables 3 and 5; Section 6 discussion p. 11–13
- Confidence: low-medium (limited to one corridor; direction consistent with physics of truck speed variance)

**Finding 6:**
- Finding: The negative binomial slightly outperformed GEE on in-sample MAD/MSPE (NB: 3.71/33.25 vs GEE: 3.74/34.46). The GEE approach (which accounts for temporal correlation of repeated segment observations) did not offer a meaningful improvement.
- Why it matters: This provides weak evidence that explicitly modelling within-segment temporal autocorrelation does not materially improve predictions for annual accident counts on motorways. My grouped link split already addresses leakage, but this finding suggests temporal correlation is not a dominant concern in annual count models.
- Evidence: Table 6, p. 16
- Confidence: low (single corridor; marginal difference; GEE only applied to overall model, not ramp-split models)

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| Negative binomial GLM with ln(L) and ln(AADT) as free covariates | Direct alternative to Poisson GLM with fixed offset; provides overdispersion parameter α; coefficient on length can be tested for deviation from 1.0 | AADT per link, link length, collision counts | 137 segments × 7 years = 959 obs | High — implementable at link-year scale | Stage 2 / diagnostic | Low | Freely estimated length coefficient deviates from theoretical exposure-offset formulation; α must be extracted for EB weighting |
| Temporal holdout validation (MAD and MSPE on held-out years) | Tests temporal generalisation independently of grouped link split; complementary to existing validation | No new data needed; use existing 2015–2024 panel | 137 segments × 2 years | High | Stage 2 / validation | Low | Does not test spatial generalisation; same links in fitting and holdout |
| Facility-family / ramp-type sub-models for motorway class | Paper shows ~24% MSPE reduction from ramp-type splitting; supports motorway-specific sub-model | Form of way from OS Open Roads; ramp presence indicator | 3 sub-models over 137 segments | Medium — requires ramp-presence identification for motorway links | Stage 2 / facility-family v2 | Medium | Ramp AADT not available; ramp presence flag requires OS/OSM derivation |
| Number of lanes as motorway-specific feature | Significant positive predictor across all models; captures lane-change conflict dynamics beyond AADT | OSM lanes tag (better coverage on motorways than minor roads) | 137 segments | Medium — lane count sparse generally but better for motorways | Stage 2 / feature engineering | Low (feature engineering) | OSM lane coverage still incomplete; may need imputation |
| Curvature sign interpretation (negative for motorways) | Paper suggests risk compensation on motorways contradicts naive positive-curvature assumption; supports road-type-specific feature treatment | Curvature already in pipeline | 137 segments | High | Stage 2 / feature validation | Low (documentation/diagnostic) | Effect may be confounded with rural/urban or speed limit in broader dataset |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| On-ramp / off-ramp AADT as continuous predictor | Ramp-level AADT not available from AADF or OS Open Roads open data | Ramp AADT from dedicated sensor network (NZ TMS) | 137 segments | Low — data not available | Binary ramp-presence indicator as proxy; ramp AADT not feasible | High |
| Median width, shoulder width, lane width as continuous predictors | These dimensions not available in OS Open Roads or AADF; sparse/absent in OSM for UK roads | RAMM road inventory (NZ proprietary) | 137 segments | Low — data not available | Not feasible without a UK equivalent of RAMM; median type could potentially be inferred from motorway classification | High |
| Annual rainfall / wet days as predictors | Weather data not currently in my pipeline; paper finds counterintuitive negative effect likely confounded with traffic volume reduction in rain | Nearest-station annual totals | 74 km corridor | Low priority — confounded effect, limited explanatory value demonstrated | Not recommended given confounding; if added, use spatial interpolation from Met Office open data | Medium |
| Applying NZ SPF coefficients to UK motorways | New Zealand motorway geometry, design standards, driver behaviour, and speed limits differ from UK; coefficients are not transferable | NZ road inventory (RAMM), NZ traffic system | 74 km NZ motorway | Not applicable | My Stage 2 re-estimates all coefficients from UK data | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Partially. The paper does not use a formal exposure offset; it uses ln(L) and ln(AADT per lane) as free predictors. This is a weaker theoretical form but produces reasonable empirical results. The paper provides no direct argument against the offset approach used in my Stage 2; it simply follows a different convention. The freely estimated length coefficient (0.806 overall, deviating from 1.0) suggests exposure is not strictly proportional to length for motorways, which is worth noting.

- **Does it suggest better handling of AADT/AADF uncertainty?** No. The study uses directly observed AADT from a sensor network for a single corridor. AADT estimation uncertainty is not addressed.

- **Does it suggest useful geometry or road-context features?** Yes, specifically for motorway-class links: number of lanes, curvature (with a sign reversal vs. non-motorway roads), maximum up-grade, ramp presence, and potentially median/shoulder width (if data were available). The first three are actionable with existing or obtainable data.

- **Does it suggest better modelling of junctions?** Partly. Ramp segments are treated as a separate facility type, not as junctions per se. The ramp treatment is relevant to motorway entry/exit points but not to at-grade junctions on other road types.

- **Does it suggest better treatment of severity?** No. Severity is not disaggregated in this paper.

- **Does it suggest better validation design?** Marginally. The 2-year temporal holdout with MAD and MSPE is a useful addition to the validation toolkit, complementing my existing grouped link split. The MAD metric is also more interpretable than MSPE for count data with rare events because it is not dominated by high-count outliers.

- **Does it expose a weakness in my current approach?** Two minor points:
  1. My Stage 2 does not currently distinguish motorway mainline from motorway slip roads (on/off ramp segments). The paper suggests this split meaningfully improves prediction for motorway-class data.
  2. My current feature set does not include number of lanes as a standalone feature for motorway links, despite it being one of the most consistently significant predictors in this paper.

---

## 15. Repo Actionability

**Action 1:**
- Suggested repo action: Add a temporal holdout diagnostic to Stage 2 validation: hold out the most recent 2 years (e.g. 2023–2024), fit on 2015–2022, compute MAD and MSPE on the holdout. Compare across model variants (GLM vs XGBoost vs EB-smoothed). This complements the grouped link split by testing temporal generalisation.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why the paper supports it: Paper uses 5-year fit / 2-year prediction split; MAD and MSPE show ramp-split models clearly outperform overall model on held-out data
- Evidence: Section 7, Table 6, pp. 15–16
- Effort: low
- Risk if implemented badly: COVID years (2020–2021) fall in the fitting period; their anomalous accident counts may distort the fitted model, making the 2023–2024 holdout evaluation misleading if COVID exposure is handled incorrectly

**Action 2:**
- Suggested repo action: For motorway-class links in Stage 2, add a ramp-presence binary feature (derived from OS Open Roads form-of-way "Slip Road" category or OSM motorway_link tag). Test whether including this feature improves held-out MAD/MSPE for motorway links specifically.
- Action type: candidate feature / small pilot
- Relevant stage: Stage 2 / feature engineering / facility-family v2
- Why the paper supports it: Paper shows ramp-type split reduces MSPE by ~24% on holdout; even a binary ramp indicator without AADT captures part of this effect
- Evidence: Table 6; Section 8 conclusion p. 16
- Effort: low (feature engineering); medium (evaluation)
- Risk if implemented badly: OS Open Roads form-of-way classification of slip roads may not align with ramp influence zones used in this paper (±500 m from ramp); misclassification will add noise

**Action 3:**
- Suggested repo action: For motorway-class links, test number of lanes (from OSM) as an additional feature in Stage 2, separate from its role in computing AADT per lane. Document OSM lane coverage for motorway links specifically (expected to be better than for minor roads) before deciding whether to include it.
- Action type: candidate feature
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Number of lanes is significant across all models (t = 5–16); partial independence from AADT per lane confirmed by simultaneous inclusion of both
- Evidence: Tables 3, 4, 5
- Effort: low
- Risk if implemented badly: OSM lane count for motorways is likely better than for minor roads but still incomplete; imputed values for missing lanes will introduce noise

**Action 4:**
- Suggested repo action: Add a documentation note to Stage 2 feature engineering documenting that the curvature feature may have a road-type-dependent sign: positive (more curvature → more accidents) for rural non-motorway roads and negative (more curvature → fewer accidents, via risk compensation) for motorway-class links. Flag this interaction as a reason to include curvature × road class interaction terms when testing motorway facility-family models.
- Action type: documentation note / candidate feature
- Relevant stage: Stage 2 / feature engineering / documentation
- Why the paper supports it: Consistent negative curvature coefficient across all motorway sub-models; paper cites multiple prior studies confirming the risk compensation effect on motorways
- Evidence: Tables 3, 4, 5; Section 6 discussion p. 11
- Effort: low
- Risk if implemented badly: None (documentation only); interaction term testing has low risk as diagnostic

**Action 5:**
- Suggested repo action: When fitting the negative binomial GLM variant for Stage 2, extract the α (overdispersion) parameter per facility family. Check whether α decreases when models are stratified by facility family (as seen in this paper: α falls from 0.183 overall to 0.106–0.130 for ramp-split sub-models). This would confirm that facility-family stratification is absorbing heterogeneity, and provide the per-family φ needed for correct EB weighting (linking to the gap identified in the Hauer 2001 extraction).
- Action type: diagnostic
- Relevant stage: Stage 2 / EB shrinkage / facility-family v2
- Why the paper supports it: α consistently lower in sub-models than overall model; connects to Hauer 2001 requirement for per-family φ estimation
- Evidence: Tables 3, 4, 5 overdispersion rows
- Effort: low (already requires NB refitting per Hauer 2001 action 1)
- Risk if implemented badly: Low; purely diagnostic

---

## 16. Query Tags

- negative-binomial
- motorway
- motorway-specific-features
- AADT-per-lane
- number-of-lanes
- ramp-presence
- ramp-AADT
- segment-level
- horizontal-curvature
- vertical-grade
- HGV-proportion
- facility-family-split
- temporal-holdout
- MAD-MSPE
- pseudo-R2
- overdispersion-parameter
- risk-compensation
- New-Zealand
- no-spatial-holdout
- free-length-coefficient

---

## 17. Confidence and Gaps

- Overall confidence in extraction: high
- Important details not stated in the paper:
  - Crash severity mix not reported (proportion injury vs PDO in the 10,149 total crashes); the paper analyses all crashes combined without specifying the STATS19-equivalent severity breakdown
  - Imputation method for missing AADT and heavy vehicle values not described
  - Temporal correlation between years for the same segment is acknowledged (citing Caliendo 2007 and GEE) but the NB models do not formally address this; the degree of within-segment temporal autocorrelation in residuals is not reported
  - The variable selection threshold of 80% confidence (p < 0.20) is unusually weak; the paper does not discuss how many candidate variables were tested before selection, making it difficult to assess the severity of multiple testing concerns
  - The paper does not report the zero rate (proportion of segment-years with zero accidents). From Table 1 (min=0, mean=8.77, SD=9.85), the proportion of zeros can be estimated as small but is not stated
- Parts of the paper that need manual checking:
  - Table 5 coefficients for off-ramp AADT (0.065, t=5.804) appear much larger than the equivalent in Table 3 (0.018, t=3.673); this is plausible given the off-ramp sub-model isolates the effect but should be noted if using these coefficients as qualitative direction indicators
  - The MAD and MSPE for the ramp-split models are reported as a combined metric for all three sub-models pooled (Table 6); individual sub-model prediction performance is not reported separately
- Any likely ambiguity or risk of misinterpretation:
  - The negative curvature coefficient is counterintuitive and the paper acknowledges this; it should not be generalised to non-motorway road types where curvature effects are typically positive. This is explicitly a motorway-specific finding.
  - The negative rainfall coefficient is noted as contradicting common sense; the paper attributes it to reduced traffic volume and increased driver caution in rain but does not formally test this. It is likely a confounded effect (volume × weather interaction) and should not be used as a basis for including weather variables in my pipeline without further investigation.
  - The paper uses an 80% significance threshold for variable inclusion. Several variables with t-statistics between 1.7 and 2.0 are retained that would be excluded at 95% confidence. When comparing effect directions with other studies, these marginal variables should be noted as uncertain.
  - The speed limit positive coefficient (80 km/h zones have more accidents than 100 km/h zones) is explicitly flagged by the authors as a policy endogeneity problem — lower limits are applied at already-risky locations. This is a classic post-event confounding issue analogous to my concern about collision-derived context columns. Any speed limit variable in my pipeline faces the same risk.
