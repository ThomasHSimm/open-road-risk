# Structured methodological extraction: *Relationship Between Traffic Volume and Accident Frequency*

## Source file
- Uploaded PDF: `ijerph-17-01393.pdf`

## 1) Citation metadata
- **Title:** *Relationship Between Traffic Volume and Accident Frequency at Intersections*
- **Authors:** Angus Eugene Retallack; Bertram Ostendorf
- **Journal:** *International Journal of Environmental Research and Public Health*
- **Year:** 2020
- **Volume / Article:** 17 / 1393
- **DOI:** 10.3390/ijerph17041393
- **Received / Accepted / Published:** 31 Jan 2020 / 19 Feb 2020 / 21 Feb 2020
- **Study area:** Adelaide City Council (ACC), South Australia, Australia

**Evidence**
- “Relationship Between Traffic Volume and Accident Frequency at Intersections” (p.1).
- “Angus Eugene Retallack and Bertram Ostendorf” (p.1).
- “Int. J. Environ. Res. Public Health 2020, 17, 1393; doi:10.3390/ijerph17041393” (p.1).
- “Received: 31 January 2020; Accepted: 19 February 2020; Published: 21 February 2020” (p.1).
- “The study is constrained to the Adelaide City Council (ACC) area in South Australia, Australia” (Section 2.1, p.2).

## 2) Study objective
- **Primary objective:** Analyse how traffic volumes affect accident frequency at intersections, specifically to test linear versus non-linear hypotheses.
- **Secondary objectives:** Examine whether congestion affects accident severity, and examine rainfall-related accident risk across congestion levels.

**Evidence**
- “This study aims to analyse how traffic volumes affect accident frequency to address the lack of consensus between the linear and non-linear hypotheses” (Section 1, p.2).
- “Separate analyses look at the effect of congestion on accident severity and the effects of rainfall on accident risk across these congestion levels” (Section 1, p.2).

## 3) Response variable
- **Main response variable:** Accident frequency (count of accidents) within grouped combinations of intersection-size rank and congestion level.
- **Severity analysis response:** Frequency of PDO and MI accidents by congestion level; MI:PDO accident-frequency ratio.
- **Rainfall analysis response:** Accident risk by congestion level under raining vs not-raining conditions, then relative risk (RR).
- **Outcome scale used in modelling:** Count outcome for grouped accident frequencies.

**Evidence**
- “Accidents in the accident volumes dataset were then grouped by the size of the intersection they occurred at and the congestion level at the time of the accident. This results in 45 groups... The number that occurred in each of these 45 groups was counted” (Section 2.10, p.6).
- “The frequency of PDO and MI traffic accidents in each congestion level were then plotted” (Section 2.11, p.7).
- “For each of these filtered datasets, the accident frequency in each congestion level was counted” (Section 2.12, p.7).
- “Accident risk is the probability of an accident occurring within a period” (Section 2.12, p.7).

## 4) Collision type and severity handling
- **Collision population retained:** Motor-vehicle accidents at intersections in the ACC with matched traffic-volume data.
- **Excluded collision/unit types:** Accidents involving cyclists, pedestrians, wheelchairs, and animals were removed.
- **Severity categories considered:** Property damage only (PDO), minor injury (MI), serious injury (SI).
- **Fatal collisions:** None at intersections in the study area during the study period.
- **Severity modelling approach:** No formal count model for severity stated; authors used plots of normalized frequencies and MI:PDO ratio by congestion level.
- **Serious injury handling:** Excluded from severity comparison because only 20 SI accidents had traffic-volume data.

**Evidence**
- “Accidents that included unit types such as cyclists, pedestrians, wheelchairs and animals were removed” (Section 2.4, p.4).
- “The accident volumes dataset was filtered into three subsets, containing property damage only (PDO), minor injury (MI) and serious injury (SI) accidents” (Section 2.11, p.7).
- “there were no fatal accidents at intersections in the ACC during the study period” (Section 2.11, p.7).
- “As there were only 20 SI accidents with traffic volume data, there was too much noise for a clear response to be observed and SI accidents were not considered further” (Section 2.11, p.7).

## 5) Exposure handling
- **Exposure concept used:** Traffic volume immediately before each accident; for rainfall analysis, number of hourly periods under raining or not-raining conditions within each congestion level.
- **Pre-accident timing rule:** Accident times were rounded down to the previous hour so that the traffic volume “was not affected by the accident itself.”
- **Normalization across sites:** Raw traffic volumes were not compared directly across intersections. Instead, each hourly measurement was assigned to one of 15 intersection-specific quantile bins, used as a **congestion index**.
- **Intersection heterogeneity handling:** Intersections were divided into three ranks based on median traffic volume, and median traffic volume for each congestion level was calculated separately by rank.
- **Offset / person-time / vehicle-km exposure term in count model:** Not stated.

**Evidence**
- “it was necessary to know the volume of traffic passing through an intersection immediately before each accident” (Section 2.7, p.5).
- “Accident times were rounded down to the nearest hour... to ensure the traffic volume used was not affected by the accident itself” (Section 2.4, p.4).
- “traffic volumes must be normalised” (Section 2.9, p.6).
- “assigning each measurement into one of 15 bins in a quantile classification based on other measurements at the same intersection” (Section 2.9, p.6).
- “These bins effectively act as an index for congestion by representing traffic volumes relative to the overall range of volumes at an intersection” (Section 2.9, p.6).
- “intersections are divided into three ranks based on their median traffic volumes” (Appendix B / Figure A4 discussion, pp.17–18).

## 6) Traffic count source
- **Source:** Public “Traffic Intersection Volumes” dataset via data.sa.gov.au, attributed to the City of Adelaide.
- **Measurement system:** Sydney Coordinated Adaptive Traffic System (SCATS).
- **Coverage:** 2010–2014, 122 intersections originally, reduced to 120 after removing two problematic sites.
- **Resolution:** Hourly traffic volume measurements; total number of vehicles passing through an intersection each hour.
- **Directionality:** Directional traffic counts were not available.
- **Error correction:** Hourly counts were multiplied by the “valid ratio” derived from the provided error ratio.

**Evidence**
- “Traffic intersection volumes from 2010 to 2014 [42] are publicly available through data.sa.gov.au” (Section 2.5, p.4).
- “recorded using the Sydney Coordinated Adaptive Traffic System (SCATS)” (Section 2.5, p.4).
- “Traffic volumes represent the total number of vehicles to pass through an intersection in each hour. Directional traffic data was not available” (Section 2.5, p.4).
- “The dataset consists of hourly traffic volume measurements for 122 intersections in the ACC” (Section 2.5, p.4).
- “Volume measurements from these two intersections were removed... leaving a total of 120 intersections” (Section 2.6, p.4).
- “Each hourly traffic volume measurement was multiplied by its valid ratio to give a corrected measurement” (Section 2.6, p.5).

## 7) Spatial unit of analysis
- **Raw traffic-data spatial unit:** Intersection.
- **Raw crash-data spatial link rule:** Accident joined to any intersection within 20 m.
- **Analytical unit for main model fitting:** Aggregated cells defined by **intersection-size rank × congestion level** (45 groups total).
- **Study-area extent:** Adelaide City Council intersections.

**Evidence**
- “The dataset consists of hourly traffic volume measurements for 122 intersections in the ACC” (Section 2.5, p.4).
- “the two datasets were spatially joined with a distance parameter of 20 m” (Section 2.7, p.5).
- “This results in 45 groups (three intersection size ranks × 15 congestion levels)” (Section 2.10, p.6).
- Figure 1 maps “intersection sites where high temporal resolution traffic volume data exists” (Figure 1, p.3).

## 8) Temporal unit of analysis
- **Traffic-data temporal unit:** 60 minutes.
- **Crash-data matching unit:** Hourly; accident timestamps rounded down to the previous hour.
- **Study period for matched crash-volume analysis:** 2010–2014.
- **Rainfall-data temporal unit:** 30 minutes, joined to hourly traffic-volume periods.
- **Modelled time index beyond hourly grouping:** Not stated.

**Evidence**
- Table 2 lists “Temporal resolution 60 minutes” (Table 2, p.5).
- “Accident times were rounded down to the nearest hour to match the hourly timestamps of the traffic volume data” (Section 2.4, p.4).
- Table 3 lists accident-volumes dataset “Temporal extent 2010–2014” (Table 3, p.5).
- “Rainfall rates were taken... with a temporal resolution of 30 minutes” (Section 2.8, p.5).

## 9) Engineered features
- **Congestion index:** 15 within-intersection quantile bins of hourly traffic volume.
- **Intersection size rank:** Three classes based on median traffic volume (low / middle / high volume intersections).
- **Median traffic volume for each congestion level:** Used on x-axis to avoid distortion from uneven bin spacing.
- **Weather exposure:** Raining vs not-raining classification from rainfall data.
- **Corrected traffic counts:** Raw SCATS count multiplied by valid ratio.
- **Error filtering rules:** Removal of two implausible sites and removal of runs of unchanged values lasting more than five consecutive hours.
- **Natural spline term:** Natural spline with 4 degrees of freedom, used as one candidate model specification.

**Evidence**
- “assigning each measurement into one of 15 bins in a quantile classification” (Section 2.9, p.6).
- “Intersections were grouped into three different sizes based on their median traffic volumes” (Section 2.10, p.6).
- “the median traffic volumes of each of the congestion levels was calculated” (Section 2.10, p.6).
- “Each hourly traffic volume measurement was multiplied by its valid ratio” (Section 2.6, p.5).
- “groups of traffic volume measurements that remained the same for more than five consecutive hourly periods... were removed” (Section 2.6, p.4).
- “Natural Spline: accident frequency ~ natural spline (traffic volume, 4 d.f.)” (Section 2.10, p.6).

## 10) Model architecture
- **Main model family:** Generalized linear count models for accident frequency.
- **Candidate specifications:** Linear term only; quadratic term; natural spline with 4 d.f.
- **Stratification:** Separate models for low-, middle-, and high-volume intersection ranks.
- **Model selection:** AICc.
- **Software:** R, in RStudio.
- **Severity and rainfall components:** Descriptive/risk-based analyses with plotted loess curves; not presented as multivariable regression models.

**Evidence**
- “Initially, poisson generalized linear models (GLM) were fit with a single linear explanatory term” (Section 2.10, p.6).
- “The following formulae were used for either the poisson or negative binomial models” (Section 2.10, p.6).
- “Linear: accident frequency ~ traffic volume”; “Quadratic: accident frequency ~ traffic volume + (traffic volume)^2”; “Natural Spline: accident frequency ~ natural spline (traffic volume, 4 d.f.)” (Section 2.10, p.6).
- “The most preferable of these three models for each intersection rank were determined using the AICc” (Section 2.10, p.6).
- “Data was processed and analysed using the R programming language... with the RStudio integrated development environment” (Section 2, p.2).

## 11) Poisson / negative-binomial / zero-inflated / other count-model handling
- **Poisson used:** Yes, as initial GLM family.
- **Overdispersion check:** Yes, Poisson models tested for overdispersion using dispersion ratio, Pearson’s Chi-squared, and p-value.
- **Negative binomial used:** Yes, for middle- and high-volume intersections due to overdispersion.
- **Zero-inflated model:** Not stated.
- **Hurdle model:** Not stated.
- **Random effects / hierarchical structure:** Not stated.
- **Spatial autocorrelation handling:** Not stated.
- **Temporal autocorrelation handling:** Not stated.
- **Offset term:** Not stated.

**Evidence**
- “Initially, poisson generalized linear models (GLM) were fit” (Section 2.10, p.6).
- “These models were then tested for overdispersion to determine whether the poisson was appropriate. If the poisson model is overdispersed, the negative binomial model is more appropriate” (Section 2.10, p.6).
- “poisson GLMs were appropriate for the counts of accidents occurring in low-volume intersections. As the poisson is overdispersed for middle- and high-volume intersections, negative binomial models were used for these instead” (Section 3.1, p.8).
- Table 4 reports overdispersion diagnostics by intersection rank (Table 4, p.8).

## 12) Reported quantitative results
### 12.1 Data volumes
- **Processed crash dataset before traffic join:** 2,336 accidents.
- **Matched crash-volume dataset:** 1,629 accidents with associated traffic volumes.
- **Traffic-volume dataset:** 5,369,323 raw hourly measurements; 5,213,580 processed.
- **Intersections:** 122 raw; 120 processed.

**Evidence**
- Table 1: processed accident dataset “n 2336” (Table 1, p.4).
- “This resulted in a total of 1629 accidents... with associated traffic volumes” (Section 2.7, Table 3, p.5).
- Table 2: “n 5,369,323” raw and “5,213,580” processed; “Number of intersections 122 / 120” (Table 2, p.5).

### 12.2 Overdispersion results
- **Low-volume intersections:** dispersion ratio 1.37; Pearson’s Chi² 17.82; p = 0.164; overdispersed = No.
- **Middle-volume intersections:** dispersion ratio 3.77; Pearson’s Chi² 48.99; p < 0.001; overdispersed = Yes.
- **High-volume intersections:** dispersion ratio 3.25; Pearson’s Chi² 42.25; p < 0.001; overdispersed = Yes.

**Evidence**
- Table 4 (p.8).

### 12.3 Model-selection results
- **Low-volume intersections:** Quadratic model AICc 69.3, weight 0.938; natural spline AICc 75.1; linear AICc 78.6.
- **Middle-volume intersections:** Quadratic model AICc 108.1, weight 0.912; natural spline AICc 113.0; linear AICc 117.3.
- **High-volume intersections:** Quadratic model AICc 119.1, weight 0.634; natural spline AICc 120.3, weight 0.352; linear AICc 126.9.
- **Interpretation stated by authors:** Non-linear models outperform linear models, and quadratic is favored for low- and middle-volume intersections; for high-volume intersections quadratic and spline are close.

**Evidence**
- Table 5 (p.8).
- “the quadratic models are favourable for accident counts at low- and middle-volume intersections” (Section 3.1, p.8).
- “The delta AICc between the quadratic and natural spline negative binomial models was only 1.2 for high-volume intersections... the AICc values do not support the choice of one model over the other” (Section 3.1, p.8).

### 12.4 Shape of traffic-volume relationship
- **Authors’ stated pattern:** Approximately linear at lower traffic volumes, with stronger-than-linear increase at highest congestion levels.
- **Linearity range described from Figure 3:** Low-volume intersections appear linear through congestion level 12; middle- and high-volume intersections through congestion level 13.

**Evidence**
- “Figure 3 emphasizes the linearity of the relationship up until the higher levels of congestion” (Section 3.1, p.8).
- “For middle- and high-volume intersections, the relationship is linear up until median traffic volumes relating to congestion level 13. For low-volume intersections, the relationship is linear up until median traffic volumes relating to congestion level 12” (Section 3.1, p.8).

### 12.5 Severity results
- **Stated result:** No clear change in MI:PDO ratio with congestion; no significant effect on severity claimed in abstract/conclusion.
- **Serious injury sample size:** 20 with traffic-volume data; excluded from severity comparison.

**Evidence**
- “no change in the ratio of MI to PDO accidents being apparent” (Section 3.2, p.9).
- “No significant effect of congestion index on accident severity was detected” (Abstract, p.1).
- “no relationship was found, possibly due to the lack of SI and fatal accidents in the data” (Section 5, p.13).

### 12.6 Rainfall results
- **Stated result:** Accident risk increases with congestion in both raining and not-raining conditions.
- **Relative risk trend:** RR decreases as congestion increases.
- **Approximate magnitudes reported in text:** RR ≈ 5 at congestion level 1; RR approaches 1 by congestion level 15.
- **Illustrative risk value:** At congestion level 15, not-raining accident risk is approximately 0.0008 (0.08%).

**Evidence**
- “For both not-raining and raining accidents, the risk of an accident occurring increases with increasing congestion” (Section 3.3, p.10).
- “In congestion level one, a RR of approximately five means that the risk of an accident is five times greater when it is raining than when it is not raining” (Section 3.3, p.11).
- “By congestion level 15, the RR approaches one” (Section 3.3, p.11).
- “the risk of approximately 0.0008 for not-raining accidents means that... there is a 0.08% chance of an accident occurring” (Section 3.3, p.10).

## 13) Validation strategy
- **Formal out-of-sample validation / holdout / cross-validation:** Not stated.
- **Model comparison strategy:** AICc comparison across candidate models.
- **Diagnostic used for count-family choice:** Overdispersion testing for Poisson.
- **Graphical checks:** Comparison of fitted curves, loess curves, and 95% confidence bands in figures.

**Evidence**
- “The most preferable of these three models... were determined using the AICc” (Section 2.10, p.6).
- Table 4 reports dispersion diagnostics (p.8).
- Figure 3 and Appendix Figure A5 show fitted/loess relationships with “95% confidence intervals” or “Error bands... at a 95% confidence level” (pp.9, 18).

## 14) Limitations stated or directly acknowledged by the paper
- **No directional traffic counts:** Prevented conventional v/c calculation by lane group.
- **No readily available signal timing and intersection geometry information:** Limited use of Highway Capacity Manual capacity methods.
- **Parsimonious modelling may omit covariates / unobserved heterogeneity:** Explicitly acknowledged in Introduction.
- **Potential secondary accidents:** Authors state this may affect inference because congestion was estimated from pre-accident traffic volumes.
- **Limited serious-injury and no fatal-intersection cases:** Constrained severity analysis.
- **Highly localized study area:** Used to reduce heterogeneity, but broader transfer is not demonstrated directly.
- **Need for large, high-quality temporally detailed traffic data:** Implied dependency of approach.

**Evidence**
- “Directional traffic data was not available” (Section 2.5, p.4).
- “Signal timing data for each intersection was not easily accessible and intersection geometry information would have been difficult to ascertain and use over 120 intersections” (Section 2.9, p.6).
- “a parsimonious approach could lead to issues relating to unobserved heterogeneity in unincluded factors” (Introduction, p.2).
- “Although we have estimated congestion based on traffic volumes prior to accidents, secondary accidents may occur” (Section 4.1, p.12).
- “SI and fatal accidents were excluded due to limited sample sizes (n = 20 and n = 0, respectively)” (Section 4.2, p.13).

## 15) Transferability to an open road-safety modelling project using open road-network and collision data
### 15.1 Elements that look transferable
- **Intersection-focused framing** is compatible with open road-network data if intersections can be derived from the network.
- **Simple spatial join of crashes to intersections** could be reproduced with open collision point data, subject to positional quality.
- **Within-site normalization of traffic conditions** is conceptually transferable where direct capacity estimates are unavailable.
- **Baseline count-model comparison logic** (Poisson vs negative binomial after overdispersion check; linear vs quadratic/spline comparison) is transferable as a cautious benchmark framework.

**Evidence**
- “This study has demonstrated the ability of high temporal frequency traffic volume data to be used in parsimonious models for predicting accident frequencies at intersections” (Section 5, p.13).
- “a novel approach to standardising traffic conditions was taken” (Section 2.9, p.6).

### 15.2 Elements that are not directly transferable from this paper alone
- **The paper depends on high-frequency traffic counts** from SCATS. Open road-network and collision data alone do not provide that exposure measure.
- **The congestion index is relative within each instrumented intersection**, so it needs repeated counts by site; it cannot be recreated from a static network file alone.
- **The study does not test portability across cities, networks, or data vendors.**
- **The study excludes pedestrians/cyclists/animals**, so it is not directly a general multimodal safety model.
- **The main fitted unit is aggregated rank × congestion cell**, not a network-wide intersection-level predictive deployment setup.

**Evidence**
- “Large datasets of high temporal frequency traffic volumes are used” (Introduction, p.2).
- “recorded using the Sydney Coordinated Adaptive Traffic System (SCATS)” (Section 2.5, p.4).
- “These bins effectively act as an index for congestion by representing traffic volumes relative to the overall range of volumes at an intersection” (Section 2.9, p.6).

### 15.3 Cautious actions suggested by this paper for an open-data project
- **Documentation note:** Record clearly when exposure is based on proxy or relative congestion rather than measured directional counts.
- **Diagnostics:** Compare Poisson and negative binomial baselines and check overdispersion before interpreting shape terms.
- **Small pilot:** Test whether a simple non-linear exposure term improves fit over a linear term on a limited, well-measured subset of intersections.
- **Baseline comparison:** Keep the paper’s parsimonious setup as a benchmark, not as a production assumption.
- **Do not assume severity effects transfer:** This paper found no clear severity relationship and had very limited SI data.
- **Do not assume rain effects transfer uniformly:** The reported rainfall RR varied by congestion level and was estimated in one city only.

**Evidence**
- “The most preferable of these three models... were determined using the AICc” (Section 2.10, p.6).
- “These models were then tested for overdispersion” (Section 2.10, p.6).
- “no relationship was found” for severity (Section 5, p.13).
- “RR becomes smaller... as congestion increases” (Section 3.3, p.11).

## 16) Extraction notes on what is **not stated**
- **Exact software packages/functions used for Poisson, negative binomial, spline, loess, and AICc calculations:** Not stated.
- **Exact regression coefficients, standard errors, p-values, or confidence intervals for the final count models:** Not stated in the provided tables/text.
- **Whether the quadratic term coefficient itself was reported numerically:** Not stated.
- **Any zero-inflated or hurdle model comparison:** Not stated.
- **Any cross-validation or held-out predictive performance metric:** Not stated.
- **Any use of offsets/exposure denominators inside the count GLMs:** Not stated.
- **Any explicit collision-type taxonomy beyond excluded unit types and severity levels:** Not stated.
- **Any open-data reproducibility package or code release:** Not stated.

## 17) Short bottom line for methodology reuse
This paper is most useful as a **parsimonious intersection-count modelling reference** showing that, in one instrumented urban setting, grouped accident counts were better fit by non-linear traffic-volume terms than by a purely linear term, with Poisson adequate in one stratum and negative binomial needed in two others. It is **not** a direct recipe for open-data-only deployment, because the core exposure variable relies on repeated hourly intersection counts from SCATS and on site-specific normalization.