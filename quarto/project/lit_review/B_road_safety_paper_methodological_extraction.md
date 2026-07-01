# Methodological extraction for road-link injury-collision risk modelling

**Paper:** Retallack, A. E. and Ostendorf, B. (2020), *Relationship Between Traffic Volume and Accident Frequency at Intersections*, International Journal of Environmental Research and Public Health, 17(4), 1393.  
**Source file:** `ijerph-17-01393.pdf`  
**Relevance to your project:** Moderate. The paper is useful for thinking about exposure normalisation, congestion/non-linearity, rainfall interaction, and sparse-event modelling. It is less directly transferable because it models **urban intersections in Adelaide**, not UK road links, and uses **hourly SCATS intersection counts**, not AADF-style link exposure.

---

## 1. What the paper models

The paper models the relationship between **traffic volume / congestion** and **motor-vehicle accident frequency** at urban intersections.

It has three linked analyses:

1. **Accident frequency vs traffic volume / congestion**
   - Main analysis.
   - Tests whether accident frequency rises linearly or non-linearly with traffic volume.
   - Separate models are fitted for low-, middle-, and high-volume intersections.

2. **Accident severity vs congestion**
   - Compares property-damage-only and minor-injury accidents across congestion levels.
   - Serious injury and fatal accidents are not modelled because of low or zero counts.

3. **Rainfall risk vs congestion**
   - Estimates accident risk during raining and not-raining periods.
   - Calculates relative risk of rainfall at each congestion level.

The paper is not a network screening or road-risk ranking study. It does not estimate “unusually high observed collisions relative to exposure” for individual sites in the way your project does. It is more of an exposure-response study focused on how accident frequency changes with short-term traffic volume and rain.

---

## 2. Response variable

### Main accident-frequency model

**Response variable:** accident frequency.

More specifically:

- accidents are counted after grouping by:
  - intersection size rank: low-, middle-, or high-volume intersections;
  - congestion index level: 1 to 15.
- This gives **45 grouped observations**:
  - 3 intersection volume ranks × 15 congestion levels.
- The count in each group is the dependent variable in the Poisson / negative-binomial models.

The paper uses **all eligible motor-vehicle accidents** for the main frequency analysis.

### Severity analysis

The severity analysis uses counts or normalised counts for:

- **PDO:** property damage only;
- **MI:** minor injury.

**Serious injury accidents:** excluded from the severity comparison because only 20 serious-injury accidents had matched traffic-volume data.  
**Fatal accidents:** none occurred at the studied intersections during the study period.

### Rainfall analysis

The rainfall analysis uses accident counts and accident risks split by:

- raining;
- not raining;
- congestion index level.

Risk is defined as:

```text
accident risk = number of accidents in condition / number of hourly periods in condition
```

Relative risk is defined as:

```text
RR = raining accident risk / not-raining accident risk
```

### Injury-only response?

Not used as the main response. The main model includes motor-vehicle accidents generally, including property-damage-only and minor-injury accidents. For your injury-collision project, that is a limitation because the paper’s main count model is not injury-collision-specific.

---

## 3. Spatial unit

**Spatial unit:** intersection.

Details:

- Study area: Adelaide City Council area, South Australia.
- Initial traffic dataset: 122 intersections.
- Final processed traffic dataset: 120 intersections after removing two problematic sites with unrealistic zero-volume patterns.
- Accident records were spatially joined to intersections using a **20 m distance parameter**.
- The paper does not model road links, carriageway sections, approaches, arms, or route segments.

### Transferability issue for your project

Your project uses road-network links in Great Britain. This paper’s spatial unit is therefore not directly aligned. The strongest transferable idea is not the intersection unit itself, but the exposure-normalisation logic: comparing traffic levels relative to each site’s own traffic distribution when absolute traffic volume is not directly comparable across sites.

---

## 4. Temporal unit

**Temporal unit:** one hour.

Details:

- Traffic volumes are hourly SCATS measurements.
- Accident times are rounded **down to the nearest hour** before matching to traffic volume.
- Rounding down is used so the traffic volume measurement is less likely to be affected by the accident itself.
- Study period: 2010–2014.
- Accident data originally available for South Australia from 2010–2017, but filtered to Adelaide City Council and 2010–2014 to match traffic-volume coverage.
- Rainfall data has 30-minute resolution and is joined to hourly traffic periods.

### Implication for AADF-style projects

The paper uses short-term hourly exposure, not annualised exposure. Its findings about congestion and rainfall are therefore about within-site, within-hour variation. AADF-style exposure is much coarser and may not capture the high-congestion tail that drives the paper’s non-linear result.

---

## 5. How traffic exposure is handled

The paper does **not** use AADT or AADF as a conventional model offset.

Instead, it handles exposure in two ways:

### 5.1 Hourly traffic volume as explanatory variable

Traffic volume is the main explanatory variable in the accident-frequency models.

- Data source: City of Adelaide traffic intersection volumes.
- Measurement: total number of vehicles passing through an intersection in each hour.
- Directional traffic counts were not available.
- Each hourly traffic count is corrected using a provided error ratio / valid ratio.

### 5.2 Site-normalised congestion index

Because intersections have different capacities, absolute traffic volumes are not assumed to be comparable across sites.

The authors avoid formal volume/capacity ratios because they lacked:

- signal timing data;
- detailed intersection geometry;
- directional traffic counts;
- lane-group-level data.

Instead, they create a **congestion index**:

- for each intersection, all hourly traffic-volume observations are divided into **15 quantile bins**;
- bin 1 represents the lowest traffic-volume periods at that intersection;
- bin 15 represents the highest traffic-volume periods at that intersection;
- the bin is interpreted as a relative congestion level.

This is a pragmatic normalisation strategy when site capacity is hard to measure.

### 5.3 Median traffic volume per congestion bin

The paper notes that plotting accident frequency directly against bin number can distort the exposure-response curve because quantile bins are not evenly spaced in actual vehicle/hour terms.

To avoid this, the authors:

- calculate the **median traffic volume** for each congestion level;
- do this separately for low-, middle-, and high-volume intersection groups;
- plot/model accident frequency against these median traffic volumes.

### 5.4 No explicit log-exposure offset

The paper does not state that it uses a log traffic-volume offset, vehicle-kilometre offset, vehicle-entering-intersection offset, or exposure-adjusted expected collision framework.

For your project, this is important: the paper models accident frequency as a function of volume/congestion, but it is not a direct template for an exposure-adjusted empirical-Bayes or residual-risk ranking model.

---

## 6. Accident-data processing

The accident data came from South Australia’s Department of Planning, Transport and Infrastructure road crash dataset.

Key processing steps:

- accidents outside Adelaide City Council were removed;
- accidents outside 2010–2014 were removed;
- accident records were matched to traffic volumes by location and hour;
- accidents involving cyclists, pedestrians, wheelchairs, and animals were removed;
- accident times were rounded down to the previous hour;
- spatial join used a 20 m radius around intersections;
- final matched accident-volume dataset contained **1,629 accidents**.

The exclusion of pedestrians and cyclists is a major transferability limitation for a UK injury-risk model if your response includes all police-reported injury collisions involving vulnerable road users.

---

## 7. Traffic-data processing

Traffic-volume data:

- source: City of Adelaide traffic intersection volumes;
- technology: Sydney Coordinated Adaptive Traffic System;
- period: 2010–2014;
- raw observations: 5,369,323 hourly traffic-volume measurements;
- processed observations: 5,213,580;
- raw intersections: 122;
- processed intersections: 120.

Cleaning steps:

- two intersections with unrealistic median traffic volumes of zero were removed;
- groups of traffic-volume measurements that stayed identical for more than five consecutive hourly periods were removed;
- hourly counts were adjusted using the valid ratio derived from the error ratio.

This is relevant to your project because AADF-style open traffic data may also contain implausible zeros, flatlined observations, or inconsistent estimates. The paper gives a concrete example of pre-model exposure cleaning, but the exact rule is specific to high-frequency SCATS data and should not be copied blindly into AADF processing.

---

## 8. Model types

### 8.1 Main count models

The paper fits count models to accident frequency:

1. **Poisson GLM**
2. **Negative binomial model**
3. Candidate functional forms:
   - linear:
     ```text
     accident frequency ~ traffic volume
     ```
   - quadratic:
     ```text
     accident frequency ~ traffic volume + traffic volume²
     ```
   - natural spline:
     ```text
     accident frequency ~ natural spline(traffic volume, 4 d.f.)
     ```

### 8.2 Overdispersion handling

The authors first fit Poisson models and test for overdispersion.

Results:

| Intersection group | Dispersion ratio | Pearson chi-square p-value | Model implication |
|---|---:|---:|---|
| Low-volume | 1.37 | 0.164 | Poisson considered acceptable |
| Middle-volume | 3.77 | <0.001 | Overdispersed; negative binomial used |
| High-volume | 3.25 | <0.001 | Overdispersed; negative binomial used |

### 8.3 Model selection

Model selection uses **AICc**.

Reported model-selection results:

| Intersection group | Best-supported model | Key result |
|---|---|---|
| Low-volume | Quadratic Poisson | AICc 69.3; evidence ratio 17.7 over next model |
| Middle-volume | Quadratic negative binomial | AICc 108.1; evidence ratio 11.5 over next model |
| High-volume | Quadratic negative binomial narrowly ahead of natural spline | quadratic AICc 119.1; natural spline AICc 120.3; linear much worse |

The practical modelling message is that the paper found little support for a purely linear volume-frequency relationship once high-congestion observations were included.

### 8.4 Machine-learning models

Not used.

### 8.5 Spatial random effects, hierarchical models, empirical Bayes, or residual ranking

Not stated / not used.

The paper does not appear to estimate intersection-specific random effects, spatial autocorrelation, empirical Bayes expected counts, excess-risk residuals, or ranked high-risk locations.

---

## 9. Quantitative results

### 9.1 Sample sizes

| Quantity | Value |
|---|---:|
| Raw accident records | 146,718 |
| Processed accidents in ACC, 2010–2014 | 2,336 |
| Accidents matched to traffic-volume data | 1,629 |
| Raw traffic-volume observations | 5,369,323 |
| Processed traffic-volume observations | 5,213,580 |
| Raw intersections | 122 |
| Processed intersections | 120 |
| Serious-injury accidents with traffic-volume data | 20 |
| Fatal accidents at studied intersections | 0 |

### 9.2 Traffic volume and accident frequency

Main finding:

- accident frequency increases with traffic volume;
- the relationship is approximately linear at lower and middle traffic volumes;
- accident frequency increases faster at the highest congestion levels;
- quadratic terms are supported over linear-only models.

The paper says the relationship is approximately linear until:

- congestion level 12 for low-volume intersections;
- congestion level 13 for middle- and high-volume intersections.

After that, accident frequency rises more sharply.

### 9.3 Rainfall

Key rainfall results:

- accident risk increases with congestion under both raining and not-raining conditions;
- raining-period risk is higher than not-raining risk at most congestion levels;
- rainfall relative risk declines as congestion increases;
- at congestion level 1, accident risk is approximately **five times greater** when raining than when not raining;
- by congestion level 15, relative risk approaches **1**, meaning rainfall no longer appears to elevate risk relative to not-raining periods at the highest congestion level.

### 9.4 Severity

Key severity result:

- no clear relationship was found between congestion and accident severity.
- The ratio of minor-injury to property-damage-only accidents does not show a meaningful change across congestion levels.
- Serious-injury and fatal severity modelling was not possible due to sparse counts.

---

## 10. Validation approach

**Formal predictive validation:** Not stated.

The paper does not report:

- train/test split;
- cross-validation;
- out-of-sample predictive performance;
- calibration plots;
- holdout-year validation;
- site-level ranking validation;
- comparison against observed future collisions;
- ROC / precision-recall / top-decile capture metrics;
- spatial transfer validation.

What it does include:

- overdispersion checks for Poisson models;
- AICc-based model comparison;
- loess curves and confidence bands for visual assessment;
- comparison of linear, quadratic, and natural-spline functional forms;
- sensitivity-style reasoning in Appendix A for choosing 15 congestion bins.

For your road-risk modelling project, this means the paper is more useful for feature/exposure design than for validation design.

---

## 11. Limitations stated or evident from the method

### 11.1 Spatial-unit limitation

The analysis is intersection-based, not link-based. Transfer to road links is not direct.

### 11.2 Geographic limitation

The study area is small and highly urban: Adelaide City Council. It may be more homogeneous than a large Great Britain model covering urban, suburban, rural, A-road, B-road, motorway, and local-road contexts.

### 11.3 Exposure limitation

The paper has high-resolution hourly traffic volume. Your project uses AADF-style exposure, which cannot observe hourly congestion states unless supplemented with time-of-day profiles or speed/congestion data.

### 11.4 Capacity limitation

The congestion index is a workaround for missing capacity data. It is useful, but it is not a formal volume/capacity ratio.

### 11.5 Directionality limitation

Directional traffic data was unavailable. The paper uses total intersection volume per hour.

### 11.6 Accident-type limitation

Pedestrians, cyclists, wheelchairs, and animals were removed. That limits relevance to injury-risk models that include vulnerable road users.

### 11.7 Severity limitation

The paper could not model fatal or serious-injury outcomes meaningfully because there were no fatal crashes and only 20 serious-injury crashes with matched traffic data.

### 11.8 Covariate limitation

The main models are intentionally parsimonious. They do not include many variables that may matter for your project, such as:

- road geometry;
- speed limit, except discussed indirectly;
- road class;
- junction form beyond being intersections;
- land use;
- deprivation;
- lighting;
- traffic control;
- turning flows;
- vulnerable road-user exposure;
- speed variation;
- enforcement;
- temporal seasonality;
- spatial correlation.

### 11.9 Validation limitation

No out-of-sample validation is reported.

### 11.10 Causality limitation

The study shows associations between traffic volume/congestion, rain, and accident frequency. It should not be treated as proving that reducing congestion will necessarily reduce collisions everywhere.

---

## 12. Transferability to a large open-data UK road-link risk model

### Useful and transferable

#### A. Exposure-response may be non-linear

The paper supports testing non-linear exposure effects rather than assuming a simple linear relationship between traffic volume and collision count.

For your project, this suggests that when modelling collision counts against AADF or vehicle-km exposure, it may be worth comparing:

- log-linear exposure offset only;
- exposure as an offset plus flexible AADF terms;
- splines for AADF;
- road-class-specific exposure effects;
- interactions between exposure and junction density / urbanicity.

This is a modelling consideration, not a production recommendation from this paper alone.

#### B. Check overdispersion explicitly

The paper’s low-volume group was acceptable under Poisson, while middle- and high-volume groups were overdispersed and needed negative binomial models. This is directly relevant to injury-collision count modelling, where overdispersion is common.

#### C. Avoid assuming traffic exposure is comparable across site types

The paper normalises traffic relative to each intersection because absolute volume means different things at different sites. For UK links, this maps to a broader point: AADF on a motorway, rural A-road, urban distributor, and minor urban link does not imply the same operational condition or risk mechanism.

#### D. Consider rainfall / weather as an interaction, not only a main effect

The paper finds rainfall relative risk is highest at low congestion and declines at high congestion. This suggests weather effects may interact with traffic state. With AADF data alone, that exact interaction may be hard to model, but weather-region or wet-day exposure adjustments could be explored in research mode.

#### E. Clean exposure data before modelling

The paper removed impossible or suspicious traffic-volume patterns before modelling. For your project, analogous checks are important for AADF and network exposure joins.

### Weakly transferable or not directly transferable

#### A. Hourly congestion index

The paper’s 15-bin within-site congestion index requires repeated traffic observations per site. A single AADF value per link does not support the same method.

Possible analogue:

- percentile-rank AADF within road class, local authority, urban/rural class, or functional road class.

But that would measure relative annual traffic intensity, not hourly congestion.

#### B. Intersection accident matching

The 20 m spatial join to intersections is not directly applicable to links. A link model needs collision-to-link assignment rules, junction handling, and treatment of collisions near nodes.

#### C. Exclusion of vulnerable road users

If your project’s police-reported injury collisions include pedestrians and cyclists, the paper’s vehicle-only filtering makes its response population narrower than yours.

#### D. Adelaide-specific operating conditions

The study area has a dense urban intersection network and mostly low speeds around 50 km/h. This does not cover many UK link contexts.

#### E. No site ranking

The paper does not evaluate methods for ranking unusually risky sites. It cannot tell you whether a given UK road-link ranking method is best.

---

## 13. Practical actions you might take

These are research/design actions suggested by the paper’s methods. They are not production changes justified by this paper alone.

### 13.1 In the modelling specification

- Test whether collision counts are overdispersed relative to Poisson expectations.
- Include negative binomial models as a baseline candidate, especially for grouped or high-flow links.
- Test non-linear exposure terms rather than assuming traffic volume has only a proportional log-offset relationship.
- Compare linear, quadratic, and spline forms for AADF or log-AADF.
- Consider interactions between traffic exposure and road type, urban/rural context, junction density, or speed environment.
- Keep a pure exposure-offset model as a benchmark so you can see whether flexible exposure terms materially improve validation.

### 13.2 In exposure engineering

- Audit AADF values for implausible zeros, missingness, sharp discontinuities, and inconsistent values across adjacent links.
- Distinguish “traffic exposure” from “congestion.” AADF gives exposure but not necessarily congestion.
- Consider deriving relative exposure ranks within comparable strata, such as road class and urban/rural category, as an exploratory feature.
- Avoid interpreting a high AADF percentile as equivalent to the paper’s hourly congestion index unless you have repeated traffic observations or speed/congestion data.

### 13.3 In spatial assignment

- Treat junction and near-junction collisions carefully. This paper is intersection-only; a link model needs explicit rules for node-proximate collisions.
- Consider whether to build separate features for junction density, signalised junction proximity, or intersection influence zones.

### 13.4 In response-variable design

- Be clear whether your response includes:
  - all injury collisions;
  - killed or seriously injured only;
  - slight injury only;
  - vehicle-only injury collisions;
  - pedestrian/cyclist collisions.
- Do not transfer this paper’s vehicle-only exclusions unless they match your research question.

### 13.5 In validation

- Add validation procedures that the paper does not provide:
  - temporal holdout;
  - spatial holdout;
  - calibration by exposure band;
  - top-ranked-link capture rate;
  - comparison of observed vs expected collisions by road class;
  - sensitivity to collision-to-link matching choices.

### 13.6 In interpretation

- If your model finds high risk on high-flow roads, separate:
  - high collision counts because of high exposure;
  - unusually high collision counts after exposure adjustment;
  - high congestion or operational stress, if measured.
- Avoid using this paper alone to justify intervention priorities. It supports testing certain model forms, not deciding production policy.

---

## 14. Direct mapping to your project

| Your project component | What this paper contributes | Caveat |
|---|---|---|
| Police-reported injury collisions | Uses police-style crash records with time, location, weather, severity | Main model is not injury-only; vulnerable road users removed |
| Road-network links | Not directly applicable | Paper uses intersections, not links |
| AADF-style traffic exposure | Strong conceptual relevance on exposure-response | Paper uses hourly traffic counts, not annual average exposure |
| Road/context features | Limited | Few context covariates included |
| Count models | Directly relevant | Uses grouped counts, not link-level expected-risk ranking |
| Machine learning | Not applicable | No ML models used |
| Ranking unusually risky links | Indirect only | No ranking or empirical-Bayes framework |
| Validation | Limited | No out-of-sample validation reported |
| Great Britain transfer | Methodological ideas only | Different country, unit, traffic data, road environment |

---

## 15. Bottom-line methodological takeaways

1. The most useful idea is to **test non-linear exposure-risk relationships**, especially at high traffic volumes.
2. The paper supports checking **Poisson vs negative-binomial** behaviour rather than assuming equidispersion.
3. The site-normalised congestion index is a clever workaround for missing capacity data, but it depends on repeated traffic observations and is not directly available from single-value AADF.
4. The rainfall analysis is useful because it treats weather risk as varying by traffic state, but the exact method needs hourly exposure and weather periods.
5. The paper does not provide a validation or ranking framework for open-data UK road-link risk modelling.
6. For your project, use this paper as support for exploratory model specification and exposure diagnostics, not as a basis for production changes on its own.
