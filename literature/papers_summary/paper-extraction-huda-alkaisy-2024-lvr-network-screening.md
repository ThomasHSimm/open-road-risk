# Paper Extraction: Huda & Al-Kaisy — Network Screening on Low-Volume Roads Using Risk Factors

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-09
- Source PDF filename: dot_78279_DS1.pdf
- Suggested Markdown filename: paper-extraction-huda-alkaisy-2024-lvr-network-screening.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (full text in context)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Full text and all tables/figures present. DOI: https://doi.org/10.3390/futuretransp4010013. Published Future Transportation 2024.

---

## 1. Citation

- Title: Network Screening on Low-Volume Roads Using Risk Factors
- Authors: Kazi Tahsin Huda, Ahmed Al-Kaisy
- Year: 2024
- DOI: https://doi.org/10.3390/futuretransp4010013
- Country / region studied: USA (Oregon)
- Study setting: Rural (low-volume rural two-lane roads, AADT ≤ 1000 vpd)

---

## 2. Core Objective

- One-sentence description: The paper proposes a practical network screening method for rural low-volume roads that predicts EB expected crash counts from categorised roadway risk factors, with and without traffic volume, to identify priority sites for safety improvement.
- Main purpose: Hotspot detection / network screening / safety performance function
- Evidence quote or page reference: "The main objective of the current study was to develop a practical and effective method for network screening on rural LVRs which requires a minimal amount of information and technical expertise." (p. 3)

---

## 3. Response Variable

- Target variable: EB expected number of crashes per year per 0.05-mile section
- Collision type: Total injury crashes (all severities combined); property-damage-only not stated
- Severity handling: Not modelled separately; total crashes used
- Count, binary, rate, risk score, severity class, or other: Continuous expected crash count (EB-smoothed), used as both response variable in regression and as the network screening ranking metric
- Time window used for outcomes: Crash data 2004–2013 (10 years)
- Evidence quote or page reference: "Crash data from 2004 to 2013 were also collected for each of the 0.05-mile sections." (p. 4); "The response (dependent) variable in both models was the EB expected number of crashes." (p. 5)

**Important modelling note:** The response variable is not raw observed crash count but the HSM Empirical Bayes expected crash count, which is already a weighted blend of predicted (SPF-based) and observed crashes. Regressing on EB expected crashes rather than raw counts means the model is predicting a smoothed quantity, which inflates R-squared relative to predicting raw counts. This is a notable methodological choice — see Section 9.

---

## 4. Exposure Handling

- Exposure variable used, if any: AADT (exact continuous value) in Model 1; excluded from Model 2
- Traffic count source: Oregon DOT databases; described as measured or estimated AADT, not stated whether observed counts or modelled
- Whether exposure is modelled, observed, assumed, or ignored: Included as a covariate in Model 1; dropped in Model 2
- Treatment of missing or sparse traffic counts: Model 2 explicitly designed for situations where AADT is unavailable; shows only ~1% reduction in R-squared (0.915 → 0.906) from dropping AADT
- Whether offset terms, rates, denominators, or normalisation are used: No exposure offset. AADT enters as a linear covariate in the log-linear OLS model. Segment length fixed at 0.05 miles, so no length-normalisation needed across sections.
- Evidence quote or page reference: Equation 4 (p. 8); "the method could be used with and without traffic data, without compromising the effectiveness of the network screening process" (abstract)
- Transferability to my AADF/WebTRIS setup: Medium for structure; low for direct use
- Notes: The near-identical R-squared with and without AADT on LVRs (≤1000 vpd) is a directly relevant finding for Open Road Risk. It suggests that on very low-volume links, road geometry and roadside features may dominate risk ranking and estimated AADT contributes little incremental predictive signal. This should not be assumed to hold at higher volume ranges. The exposure-as-covariate structure (not offset) is again weaker than Open Road Risk's current offset approach.

---

## 5. Spatial Unit of Analysis

- Unit: Road segment — fixed 0.05-mile (≈80 m) sections
- Segment length or segmentation rule: Fixed-length 0.05-mile sections, chosen to capture changes in roadway/roadside characteristics with reasonable accuracy. Longer segments are formed by aggregating sections for network ranking.
- How crashes are assigned to the network: Not described in detail; implied by Oregon DOT crash database linkage to roadway sections.
- Treatment of junctions/intersections: Intersections explicitly excluded; paper focuses on road segments only. "This research focused solely on roadway segments." (p. 4)
- Spatial aggregation risks: Section-level estimates are summed and divided by segment length to produce crash density for ranking (Figure 5). Aggregation from 0.05-mile sections to longer segments could obscure within-segment variation.
- Evidence quote or page reference: "Data were collected for roadway sections that are 0.05 miles in length." (p. 3)
- Relevance to OS Open Roads link-based pipeline: Moderate. The 0.05-mile (80 m) fixed-length sections are shorter than many OS Open Roads links but closer in scale than the M25 segment papers. The fixed-length segmentation approach contrasts with OS Open Roads variable-length links; this is a known trade-off between capture of geometry changes and link-definition consistency.

---

## 6. Temporal Unit of Analysis

- Years covered: 2004–2013 (10 years of crash data)
- Temporal resolution: Annual aggregate (no sub-annual modelling)
- Whether seasonality or time-of-day is modelled: No
- Whether before-after or panel structure is used: No — cross-sectional (one observation per 0.05-mile section, crashes aggregated over 10 years)
- Evidence quote or page reference: "Crash data from 2004 to 2013 were also collected." (p. 4)
- Relevance to WebTRIS-style time profiles: None

---

## 7. Engineered Features

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|
| Lane width (LW) | Oregon DOT database | Binary: <11 ft (narrower) vs ≥11 ft (wider). CART failed to split; cut-off from descriptive statistics + engineering judgment | Narrower lanes → higher crash risk | Low — lane width available from OSM but sparse in Open Road Risk; OSM lanes field noted as sparse |
| Shoulder width (SW) | Oregon DOT database | Binary: <1.8 ft vs ≥1.8 ft. Cut-off from CART analysis | Narrower shoulder → higher crash risk | Low — shoulder width not in OS Open Roads or OSM with good coverage |
| Degree of horizontal curvature (DC) | Oregon DOT database | 4-category ordinal: 0° (straight), <9° (mild), 9–28° (moderate), ≥28° (sharp). Cut-offs from CART | Sharp curves strongly associated with higher EB expected crashes (avg 0.86 vs 0.067 for straight) | Medium — curvature derivable from OS Open Roads geometry; already flagged as candidate feature. CART-derived thresholds are US-specific; UK equivalents would need re-derivation |
| Vertical grade (G) | Oregon DOT database | Binary: <4% (mild) vs ≥4% (steep). CART uninformative; cut-off from crash rate plot | Steep grade → higher crash rate per mile (1.55 vs 1.50) | Already present as candidate — OS Terrain 50. Paper supports 4% as a defensible threshold but effect size is small (Figure 4) |
| Driveway density (DD) | Oregon DOT video logs / Google Maps aerial | Exact count of driveways per mile | Access points increase conflict points; positive coefficient in both models | Low — driveway density not systematically available for UK road network; no direct OS Open Roads equivalent |
| Side slope (SS) | Oregon DOT video logs | 3-category: steep/moderate/flat (pre-classified from video logs) | Steeper side slope → higher crash risk | Low — not available in open UK data stack |
| Fixed objects (FO) | Oregon DOT video logs | 3-category: many/some/few (pre-classified from video logs) | More fixed objects → higher crash risk | Low — not systematically available in UK open data |
| AADT (V) | Oregon DOT | Exact continuous value | Standard exposure; positive coefficient but near-identical model fit without it on LVRs | Already present — estimated AADT in Open Road Risk Stage 1a |

---

## 8. Model Architecture

- Algorithms/models used: (1) OLS linear regression on log(EB expected crashes) — with AADT; (2) same without AADT. CART used as preprocessing to derive feature category thresholds.
- Baseline model: Not stated; EB expected crash count from HSM SPF used as response variable baseline
- Final/preferred model: Model 1 (with AADT), adjusted R² = 0.915
- Loss function or likelihood: OLS (minimises sum of squared residuals on log-transformed EB expected crashes)
- Offset/exposure term, if used: None — AADT enters as a linear covariate; segment length fixed at 0.05 miles (implicit constant length normalisation, not an offset)
- Spatial autocorrelation handling: None
- Temporal dependence handling: None — cross-sectional
- Interpretability method: Coefficient signs and magnitudes; CART outputs for threshold selection; crash rate plots by category
- Evidence quote or page reference: "Multivariate ordinary least squares linear regression analysis was used." (p. 8); Equations 4–5 (p. 8–9).

**Critical modelling note:** OLS is applied to a log-transformed EB expected crash count, not to raw observed counts. This departs from the standard Poisson/NB count model family used in Open Road Risk. The response variable (EB expected crashes) is a smooth, continuous quantity derived from the HSM SPF + observed crashes, which behaves more like a continuous outcome than a zero-heavy integer count. This explains the unusually high R-squared values (0.91–0.92). It also means the model is essentially predicting a model output from another model, which produces optimistic-looking fit statistics. This is not equivalent to predicting raw crash counts, and the R-squared cannot be compared to Open Road Risk's GLM pseudo-R² or XGBoost R².

---

## 9. Reported Metrics / Quantitative Results

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|
| Model fit (training) | Adjusted R² | 0.915 | Model 1 (with AADT) | Explains 91.5% of variance in log(EB expected crashes) — but see note on response variable | Table 2, p. 9 |
| Model fit (training) | Adjusted R² | 0.905 | Model 2 (no AADT) | Near-identical fit without traffic volume | Table 3, p. 9 |
| Predictive validation | Mean predicted vs actual EB crashes, % difference | <5% (2.3–2.4%) | Model 1, training + testing | Small bias in mean prediction | Table 4, p. 11 |
| Predictive validation | Mean predicted vs actual EB crashes, % difference | ~12% (8–13%) | Model 2 (no AADT), training + testing | Larger but acceptable bias without traffic data | Table 4 |
| Predictive validation | MBE | −0.0015 (training) / 0.0018 (testing) | Model 1 | Near-zero mean bias | Table 4 |
| Predictive validation | RMSE | 0.18 (training) / 0.19 (testing) | Model 1 | Small absolute RMSE consistent with mean EB crashes of ~0.09 | Table 4 |
| Feature finding | CART: curvature threshold | ≥28° → avg EB crashes 0.86 vs 0.067 for straight | CART analysis | Sharp curves have 13× higher expected crash density than straight segments | Figure 1, p. 7 |
| Feature finding | Crash rate by grade | ≥4% grade → 1.55 vs 1.50 crashes/mile | Descriptive | Steep grade increases crash rate, but effect is small | Figure 4 |
| Feature finding | Crash rate by lane width | <11 ft → 1.55 vs 1.49 crashes/mile | Descriptive | Narrower lanes slightly higher crash rate | Figure 3 |
| Coefficient | AADT coefficient | +0.001 | Model 1 | Very small — consistent with near-zero marginal contribution of AADT on LVRs | Table 2 |

**Validation type:** A random 80/20 train/test split was used. This is a held-out test set, but the split is **random** (not spatial, not temporal, not grouped by road corridor). Sections from the same road corridor may appear in both training and testing sets, creating potential spatial leakage — adjacent 0.05-mile sections from the same road will have correlated geometry and EB crash values. This is not acknowledged as a limitation in the paper.

**Are metrics likely to be optimistic?** Yes, for two reasons: (1) the response variable is EB expected crashes (a model output), not raw counts, making OLS R-squared high by construction; (2) random split does not prevent spatial leakage across nearby sections. The R-squared values of 0.91–0.92 should not be compared directly to Open Road Risk's XGBoost R² or GLM pseudo-R² on raw count data.

**Most relevant metric for Open Road Risk:** The near-zero marginal contribution of AADT in Model 2 on LVRs (R² drops only 0.009 without AADT). This is directly relevant to Open Road Risk's minor rural road links where Stage 1a AADT estimates are most uncertain.

---

## 10. Rare Event / Class Imbalance Handling

- How rare events are handled: By using EB expected crashes (rather than observed counts) as the response variable, the paper sidesteps the sparsity problem. The EB shrinkage pulls low-observation sites toward the SPF prediction, effectively regularising sparse crash data.
- Model family: OLS on log-transformed EB expected crashes — not a count model, no zero-inflation, no Poisson/NB. Zero-heavy counts are not a modelling problem here because the EB expected crash value is a continuous positive quantity (minimum 0.0083 in the dataset, Table 1).
- Whether high-risk locations are evaluated separately: No
- Evidence quote or page reference: "The EB expected number of total crashes was selected as a basis for network screening...given the favorable performance of the EB method for LVRs." (p. 4)
- Practical relevance to my sparse collision link-year dataset: High relevance as a design principle. Using EB expected crashes as a ranking metric rather than raw observed counts is already implemented in Open Road Risk as a diagnostic variant. The paper provides empirical support that on low-volume roads specifically, EB-based ranking is more reliable than raw count ranking, and that geometric risk factors dominate the EB estimate.

---

## 11. Validation Strategy

- Train/test split method: Random 80/20 split (680 miles training, 170 miles testing)
- Spatial holdout used? No — random split; spatially adjacent sections likely split across training and testing
- Temporal holdout used? No
- Grouped holdout used? No
- Cross-validation type: None (single random split)
- Metrics: MBE, RMSE, mean and total predicted vs actual EB crashes
- External validation: None — all data from Oregon
- Leakage or generalisation risks: (1) Spatial leakage: random split of 0.05-mile sections means sections from the same road corridor appear in both sets; EB values for adjacent sections are correlated through the SPF (same road type and AADT range) and through observed crashes on nearby sections. This is a weak form of data leakage, not acknowledged in the paper. (2) The response variable (EB expected crashes) is partly derived from observed crashes in the same dataset, so the model is predicting a quantity that contains the observed crash history it was trained on — this circular element is inherent to the method design and inflates apparent fit.
- Evidence quote or page reference: "The data were split randomly into two parts. The first part consisting of 80 percent...was used to develop or train the model while the second part...was used for testing." (p. 8)
- What I should copy or avoid: The use of RMSE and MBE on a held-out random split is a reasonable validation practice for a low-volume-road screening tool. Do not treat R-squared values as comparable to Open Road Risk's metrics on raw count data. A spatial or grouped corridor holdout would be more robust for a future similar application.

---

## 12. Key Findings Relevant to My Project

**Finding 1:**
- Finding: On low-volume roads (AADT ≤ 1000 vpd), dropping AADT from the model reduces adjusted R² from 0.915 to 0.905 — a difference of only 0.009. This suggests that on very low-volume links, road geometry and roadside features explain nearly as much variance in EB expected crash risk as geometry + traffic volume combined.
- Why it matters: Open Road Risk's Stage 1a AADT estimates are least reliable for low-volume rural links (sparse AADF coverage, wider confidence intervals). This finding suggests that for the lowest-volume tier of Open Road Risk links, the Stage 2 risk ranking may be robust to AADT estimation error — geometry features may dominate. This does not generalise beyond the LVR range (≤1000 vpd).
- Evidence: Tables 2–3 comparison; abstract; p. 10.
- Confidence: Medium — finding is internally consistent and supported by a companion paper (Al-Kaisy and Huda, 2022), but study is Oregon rural roads only. UK road geometry effects may differ.

**Finding 2:**
- Finding: Sharp horizontal curvature (degree of curvature ≥28°) is associated with 13× higher average EB expected crash density than straight segments (0.86 vs 0.067 per year per 0.05-mile section). The curvature effect is the largest single predictor in the CART analysis.
- Why it matters: This provides the strongest quantitative evidence across the papers extracted so far for horizontal curvature as a risk factor. The CART-derived thresholds (9° and 28°) give empirically grounded category boundaries, though these are US-specific and would need recalibration for UK geometry conventions.
- Evidence: Figure 1 (CART output), p. 6–7; Table 2 coefficient DC = +0.24.
- Confidence: Medium — very consistent within the Oregon dataset; curvature effect plausible but magnitude likely network-specific.

**Finding 3:**
- Finding: Steep vertical grade (≥4%) is associated with higher crash rates per mile, but the observed effect is small (1.55 vs 1.50 crashes/mile). The grade coefficient in the regression is positive and significant, consistent with the companion M25 frequency paper.
- Why it matters: Adds a second independent dataset supporting grade as a positive predictor of crash frequency. The small magnitude at LVR scale (low speeds, low volumes) is consistent with grade being more important at higher-speed/higher-volume roads (as seen on M25). Supports including grade from OS Terrain 50 but with modest expected effect size at the low end of the speed/volume range.
- Evidence: Figure 4; Table 2 coefficient G not explicitly reported but included in variable set (grade included in the ≥4% binary; see Table 1).
- Confidence: Low-medium — grade significance consistent with other studies but effect size small in this dataset; CART failed to identify a useful cut-off (required engineering judgment).

**Finding 4:**
- Finding: Empirical Bayes expected crash count outperforms raw observed crash count as a network screening metric for low-volume roads, and can be approximated to within ~5% accuracy using simple categorised roadway variables, enabling network screening without detailed traffic or geometry databases.
- Why it matters: Open Road Risk already implements EB shrinkage as a diagnostic variant. This paper provides direct empirical support for EB-based ranking on low-volume rural links — the most challenging segment type in Open Road Risk for both AADT estimation and crash observation reliability.
- Evidence: Abstract; Section 5.1; Table 4 (validation results).
- Confidence: Medium — supported by companion paper and multiple literature references, but Oregon-specific implementation.

**Finding 5:**
- Finding: Driveway density (access point density) is a significant positive predictor of expected crashes on rural LVRs (coefficient +0.016 per driveway/mile in Model 1). The authors suggest this is obtainable from aerial imagery (Google Maps).
- Why it matters: Driveway or access point density is not currently in Open Road Risk's feature set. It is not directly available from OS Open Roads or OSM with good coverage. The paper suggests aerial-derived counts as a feasible data source, but this would require significant effort at 2.1M link scale. Flag as a low-priority future candidate.
- Evidence: Table 2, p. 9; p. 3 (data description).
- Confidence: Medium for the association; low for transferability to UK open-data pipeline at scale.

---

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|
| EB expected crash count as ranking metric for low-volume links | Paper provides empirical support that EB ranking is more reliable than raw counts for sparse-crash links; already a diagnostic variant in Open Road Risk | Already implemented — EB shrinkage available | ~850 miles, 16,514 sections | Compatible — relevant for the rural low-volume tier of Open Road Risk links | Stage 2 / validation / documentation | Low (already present; document the evidence) | EB in Open Road Risk uses different SPF base; direct comparison of k values not transferable |
| CART-derived category thresholds for curvature | Provides empirically derived cut-offs (9° and 28° degree of curvature) separating risk tiers; useful reference when categorising OS Open Roads curvature values | OS Open Roads geometry (curvature derivable) | ~850 miles Oregon rural | Compatible in principle; US thresholds need recalibration for UK geometry | Stage 2 / feature engineering / candidate feature | Medium (curvature calculation + threshold testing) | US degree-of-curvature thresholds not directly applicable to UK; would need CART or percentile-based recalibration on Open Road Risk data |
| 4% grade threshold as binary feature | Two independent datasets (Oregon LVR + M25) find a positive grade–crash association; 4% threshold derived from crash rate plot | OS Terrain 50 (already planned) | ~850 miles Oregon rural | Compatible | Stage 2 / candidate feature | Low once Terrain 50 integrated | Effect size small on low-volume roads; may be more important on high-speed links |
| CART for data-driven feature categorisation | Objective method for setting cut-off values for continuous geometric variables based on their relationship with EB expected crashes | Any continuous feature + EB expected crash response | Any scale | Computationally feasible at 2.1M link scale using sklearn or R | Stage 2 / feature engineering | Low-medium | CART-derived thresholds will differ by road type and volume band; should not use single global thresholds |

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|
| Shoulder width as risk feature | Shoulder width not systematically available in OS Open Roads or OSM for UK roads at national scale | Shoulder width data absent from open UK stack | ~850 miles | Low | Possibly derivable from OS MasterMap or Highways England data for major roads; not feasible at national scale | High |
| Driveway density (access point density) | Not available at national scale in UK open data | No systematic UK access-point inventory | ~850 miles | Low | Manual Google Maps sampling or OSM access=* tags for pilot; not scalable | High |
| Side slope and fixed object ratings | Require video log inspection or roadside audit; not available nationally | Oregon DOT video logs | ~850 miles | Low | No open-data equivalent in UK | High |
| HSM SPF as the EB base model | HSM SPF calibrated for Oregon; not calibrated for UK. UK road geometry conventions and crash recording differ | UK-calibrated HSM SPF not available | ~850 miles | Low for direct use | Open Road Risk's own Poisson GLM can serve as SPF for EB shrinkage — already the approach taken | High |
| OLS on log(EB expected crashes) as the primary model | Predicting a model output (EB) from features is not equivalent to predicting raw crash counts; misleadingly high R-squared. Open Road Risk models raw counts with Poisson/XGBoost | No data gap; methodological mismatch | ~850 miles | Low — different modelling target | Not applicable; maintain Poisson/XGBoost on raw counts | High |

---

## 14. Pipeline Implications

- **Does this paper support using exposure-normalised collision risk?** Indirectly — the near-identical model fit with and without AADT on LVRs suggests that for the lowest-volume tier of Open Road Risk links, AADT estimation uncertainty may not substantially degrade risk ranking quality. Does not argue against the offset; argues that AADT uncertainty matters less at very low volumes.
- **Does it suggest better handling of AADT/AADF uncertainty?** Yes, indirectly — for LVR links (≤1000 vpd), geometric and roadside features dominate EB expected crash risk; AADT has minimal marginal contribution. This suggests Open Road Risk could document a lower sensitivity to Stage 1a AADT error for its lowest-volume rural links.
- **Does it suggest useful geometry or road-context features?** Yes — curvature (strong, CART-quantified), grade (weak but consistent), lane width and shoulder width (moderate, not available in UK open data), driveway/access density (moderate, not available at scale).
- **Does it suggest better modelling of junctions?** No — intersections explicitly excluded.
- **Does it suggest better treatment of severity?** No — total crashes only.
- **Does it suggest better validation design?** Weakly — random train/test split is better than no split (unlike the M25 papers), but a grouped corridor holdout would be more appropriate for spatially correlated sections.
- **Does it expose a weakness in my current approach?** One note: if Open Road Risk currently ranks low-volume rural links primarily by estimated AADT × length exposure (offset), this paper suggests that exposure uncertainty may be less critical for ranking those links than geometric factors. It is worth checking whether the Stage 2 risk percentile for low-AADT links is dominated by the exposure offset term or by geometry features.

---

## 15. Repo Actionability

**Action 1**
- Suggested repo action: Document that on low-volume rural links (AADT ≤ ~1000 vpd), EB-based ranking is empirically supported and Stage 1a AADT estimation error is likely to have lower impact on risk ranking than it does for higher-volume links. Add this as a calibration note in Stage 1a / Stage 2 documentation.
- Action type: Documentation note
- Relevant stage: Stage 1a / Stage 2 / documentation
- Why the paper supports it: R² drop of only 0.009 when removing AADT from LVR model; authors explicitly note "the contribution of crash history and traffic exposure in the estimation of the HSM EB expected number of crashes is not tangible on low-volume roads." (p. 10)
- Effort: Low
- Risk if implemented badly: Could be misread as implying AADT doesn't matter generally; note must be qualified to the LVR range.

**Action 2**
- Suggested repo action: When OS Terrain 50 grade is integrated, consider using CART to derive data-driven binary or multi-class grade thresholds on Open Road Risk's own EB-ranked link-year data, rather than importing the Oregon 4% threshold directly.
- Action type: Diagnostic / candidate feature (once grade is available)
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: CART-derived thresholds for curvature (9°, 28°) are empirically calibrated to the local crash–geometry relationship; the 4% grade threshold was derived from an Oregon-specific crash rate plot. UK geometry effects may produce different optimal thresholds.
- Effort: Low-medium (CART is straightforward in sklearn/R once grade values are available)
- Risk if implemented badly: CART thresholds overfit to training data if applied without cross-validation; use as a starting point, not a final decision rule.

**Action 3**
- Suggested repo action: Prioritise horizontal curvature as a Stage 2 candidate feature based on the strong CART-quantified association in this paper (sharp curves: 13× higher EB crash density than straight segments). Calculate curvature from OS Open Roads geometry and run a diagnostic confirming the direction of association in Open Road Risk data before adding to production model.
- Action type: Candidate feature → diagnostic
- Relevant stage: Stage 2 / feature engineering
- Why the paper supports it: Curvature is the strongest single predictor in CART analysis; consistent with direction found in the companion M25 severity paper.
- Effort: Medium (curvature calculation from polyline geometry + diagnostic)
- Risk if implemented badly: CART-derived thresholds are US/Oregon-specific; do not apply the 9°/28° cut-offs without UK-calibrated equivalents. Effect size on UK roads of mixed classification is unknown.

**Action 4**
- Suggested repo action: Note in documentation that driveway/access density is a significant LVR predictor in this study but has no scalable UK open-data equivalent. Flag as a potential future enrichment if OS AddressBase or OSM access point data are evaluated, but do not prioritise.
- Action type: Documentation note
- Relevant stage: Feature engineering / documentation
- Why the paper supports it: Positive, significant driveway density coefficient in both models (Tables 2–3); coefficient magnitude (+0.016 per driveway/mile) is modest.
- Effort: Low for note
- Risk if implemented badly: None for documentation.

**Action 5**
- Suggested repo action: Add a note to validation documentation flagging that the high R-squared values (0.91–0.92) reported in this paper are not comparable to Open Road Risk's XGBoost R² or Poisson pseudo-R² — they arise from predicting a smooth EB model output, not raw crash counts. This prevents misinterpretation if these metrics are cited in project documentation.
- Action type: Documentation note
- Relevant stage: Documentation / validation
- Why the paper supports it: The OLS model predicts log(EB expected crashes), where EB is already a blended smooth quantity; this artificially inflates R-squared relative to predicting raw observed counts.
- Effort: Low
- Risk if implemented badly: None for documentation.

---

## 16. Query Tags

- low-volume-roads
- network-screening
- empirical-bayes
- CART-thresholds
- curvature-risk-factor
- grade-risk-factor
- lane-width
- shoulder-width
- driveway-density
- rural-roads
- OLS-on-EB-response
- no-exposure-offset
- AADT-optional
- random-train-test-split
- spatial-leakage-risk
- Oregon-USA
- HSM-SPF
- feature-categorisation
- zero-heavy-workaround-EB
- inflated-R-squared-warning

---

## 17. Confidence and Gaps

- Overall confidence in extraction: High — full paper text and all tables present.
- Important details not stated in the paper: Whether AADT is observed counts or modelled estimates (not stated). Whether junction crashes were excluded from the crash count used to construct the EB response (implied yes, but not stated). Number of distinct road corridors in the sample (only total mileage stated — ~850 miles; number of separate roads unknown).
- Parts of the paper that need manual checking: Table 1 shows grade (G) as a variable but Table 2 does not list a grade coefficient separately from the other variables — check whether grade was dropped or absorbed into another term. On review: the variable set in Equation 4 (p. 8) lists LW, SW, DD, V, DC, SS, FO but not G explicitly. Grade may have been excluded from the final regression model despite being discussed in Figure 4. This is ambiguous and should be confirmed.
- Any likely ambiguity or risk of misinterpretation: (1) High R-squared values are artefacts of regressing on EB expected crashes (model output), not raw counts. This must not be interpreted as strong predictive performance on new crash data. (2) The near-zero AADT contribution on LVRs is specific to AADT ≤ 1000 vpd and should not be generalised to higher-volume links. (3) CART thresholds (9°, 28° curvature; 4% grade; 1.8 ft shoulder) are US/Oregon-specific; direct application to UK Open Road Risk would require recalibration.
