---
title: "Open Road Risk: an open-data pipeline for exposure-adjusted collision risk across the road network of Northern and Central England"
subtitle: "Methodology and findings as of May 2026 — an active, ongoing project"
author: "Thomas Simm"
date: "May 2026"
---

# Open Road Risk: an open-data pipeline for exposure-adjusted collision risk across the road network of Northern and Central England

**Author:** Thomas Simm (independent research)
**Project site:** https://openroadrisk.org/
**Repository:** https://github.com/ThomasHSimm/open-road-risk

Open Road Risk is an active, ongoing project. This document reports its methodology and findings at a single point in that work — the model run dated 2026-05-03 (git SHA `301a766b`). Numbers and conclusions will move as the project develops; the project site and repository are authoritative for the current state. The accompanying public site and code repository sit alongside this document rather than being summarised by it.

*To cite this work, please use the Zenodo archive: https://doi.org/10.5281/zenodo.20451731 (see [How to cite](#how-to-cite)).*

---

## Abstract

Open Road Risk (ORR) estimates how dangerous each road is *relative to how much traffic it carries*, rather than ranking roads by raw collision counts — a busy motorway and a quiet lane with the same number of collisions are not equally risky. It does this for roughly 2.1 million road links across Northern and Central England, using only open data and an open, reproducible code base. As far as I can tell, no other public system combines national collision data, full-network coverage, exposure-adjusted modelling, open methods, and a reproducible implementation at once; that combination, rather than any single technique, is the contribution.

The pipeline has three stages: estimate traffic volume for every road (most roads have no traffic counter), profile within-day traffic patterns, and model collision counts against that estimated exposure. The collision model is the headline output. On held-out data its predictive fit is modest — as expected for a problem where ~99% of road-years have zero recorded collisions — and the work's value is in the ranking it produces and the openness of how it gets there, not in a high fit statistic.

This is a research prototype, not a tool for operational safety decisions. It is most useful for network screening, prioritisation, and hypothesis generation. The methodology below is written to be honest about where it is strong and where it is not:

- **Strengths** — exposure-adjusted framing, training only on directly-counted traffic data, exclusion of features that would leak information from observed collisions, and grouped cross-validation that prevents the same road appearing in both training and test.
- **Open questions and limitations** (covered in Sections 10 and 12) — the traffic-estimation step's uncertainty is not yet carried into the collision model; the two collision models are not yet compared on a common evaluation surface; the cross-validation is not fully spatial; and several diagnostics (a negative-binomial comparator, road-family-stratified exposure, an external benchmark) are identified but not yet run.

```{=latex}
\newpage
```

## 1. Introduction

### 1.1 Motivation

Road collision risk is routinely misrepresented by raw collision counts. A road link with twenty recorded collisions may be unusually dangerous if it carries little traffic, or unremarkable if it is the busiest corridor in the region. Correctly comparing links requires normalising observed outcomes by exposure — typically vehicle-kilometres or vehicle-days of travel — a principle that underlies the Highway Safety Manual (HSM) approach (Harwood et al., 2000; Srinivasan and Harkey, 2013) and is the basis of official UK casualty rate reporting (National Highways, 2022; DfT, 2025).

In practice, this normalisation is difficult to apply at full-network scale because direct traffic measurements are sparse. The Department for Transport's Annual Average Daily Flow (AADF) data records vehicle counts at fixed count points — directional totals averaged to a daily figure — but these points are concentrated on major roads. Most minor and unclassified roads, which account for the large majority of the roughly 2.1 million links in the study area, have no nearby count point and therefore no measured traffic at all.

Open Road Risk's response is a two-step move that needs its two key terms kept distinct. **AADF** is the *observed* count data described above — the training signal, available only at count points. **AADT** (Annual Average Daily Traffic) is the *estimated* per-link traffic volume that Stage 1a produces for every road in the network, including the millions that have no count point. ORR trains a model on the observed AADF counts, uses it to estimate AADT everywhere, and then uses that estimated AADT as the exposure denominator in the collision model. The aim is not the most accurate possible safety model; it is to show that exposure-adjusted safety analysis can be done at full-network scale using only open data, open methods, and a public repository.

### 1.2 Related work

Crash-frequency modelling has a long methodological tradition, and ORR sits at the intersection of four substantively distinct lines of work. Sketching them is necessary because the design choices in later sections — Poisson with log-offset, Empirical Bayes shrinkage, feature exclusion rules, grouped cross-validation — only make sense against this background.

**The SPF/HSM tradition.** A Safety Performance Function (SPF) is, in plain terms, a regression that predicts the expected number of crashes on a road from its traffic volume and a few road characteristics — the engineering standard for "how many crashes should we expect here, given how busy it is?" SPFs emerged from US highway safety research in the 1990s and were codified in the FHWA Highway Safety Manual (Harwood et al., 2000; Srinivasan and Harkey, 2013). The canonical form is a Negative Binomial regression in which traffic volume enters as `log(AADT × length)`, either as a free covariate or as a fixed offset (the difference matters and is discussed in Section 6.1), fitted separately for each road type — rural two-lane, urban arterial, signalised junction, and so on. Local calibration factors adjust national SPFs to specific areas, and Empirical Bayes shrinkage (Hauer et al., 2001) blends the SPF's prediction with a site's own observed history. The tradition is mature, interpretable, and embedded in US engineering practice. Its main constraint is data: facility-specific calibration needs manual road inventory and segmentation that does not extend naturally to a 2.1-million-link network. The choices it makes — Poisson/NB likelihood, exposure offset, EB combination — are nonetheless the standard against which any new approach should be measured. Lord and Mannering (2010) review why these choices are made and what the alternatives are; Khodadadi et al. (2021) extend the model-family question into the very zero-heavy, low-mean regime ORR occupies, finding that NB-Lindley parameterisations outperform standard NB-2 when the zero proportion is high.

**The UK spatial-Bayesian tradition.** A separate strand of work has applied Bayesian hierarchical models to UK crash data at network scale. Wang et al. (2009) fit spatial Poisson-lognormal and NB models to the M25 motorway, treating AADT and length as free covariates and reporting sub-linear AADT elasticity — below the unity a fixed offset implies. Boulieri et al. (2016) extend the approach to ward-level data across England with a space-time Bayesian model and AADF-derived exposure. Gilardi et al. (2022) is the closest methodological predecessor to ORR: a Bayesian hierarchical Poisson model fitted to OS road segments in Leeds, with ICAR spatial random effects, multivariate severity outcomes, and a `log(length × estimated commuter flow)` offset. This tradition is stronger than ORR in several respects — explicit spatial random effects, joint severity modelling, properly quantified posterior uncertainty — but the published work is restricted either to single cities (Gilardi) or to coarser spatial units (Boulieri, ward grain). No published Bayesian model in this tradition has been applied at full-network grain across multiple regions.

**The ML-based tradition.** A more recent strand uses machine learning models in place of GLMs, with mixed results. Pan et al. (2017) benchmark a Deep Belief Network against NB regression for a cross-country global SPF and report worse out-of-sample performance for the deep model on sparse-count data — providing useful negative evidence against assuming that more expressive models automatically perform better on the zero-heavy distributions typical of road safety. Gao et al. (2024) is the most relevant recent comparator: a spatio-temporal probabilistic graph neural network (STZITD-GNN) with zero-inflated Tweedie likelihoods for daily road-level crash prediction in London. The architecture is considerably more expressive than ORR's Stage 2 and produces explicit uncertainty estimates, but it uses no exposure offset (so cannot distinguish high-risk from high-traffic roads), validates only temporally rather than spatially, and does not scale to 2.17M links in its current form. The AccHR@k metric introduced in that paper — the fraction of actual crash links captured in the top-k% of predicted risk — is directly applicable to ORR and is a planned addition to the evaluation stack. ORR's use of XGBoost with a Poisson objective sits between the GLM and GNN approaches: more flexible than a Poisson GLM in feature interactions, more interpretable and computationally tractable than a spatial GNN.

**The AADT estimation literature.** Stage 1a places ORR in a parallel literature on traffic-volume estimation for unmeasured road segments. Jayasinghe et al. (2019) show that betweenness centrality in a dual road graph substantially improves AADT prediction on low-count roads relative to location-and-classification models — a finding that directly motivates ORR's feature set. More recent work has shifted toward interval prediction, using Quantile Random Forests or conformal prediction with high-dimensional spatial covariates to produce calibrated prediction intervals rather than point estimates. This is the most important methodological advance ORR has not yet adopted: Stage 1a currently produces point predictions only, and Stage 2 treats them as exact, which understates total uncertainty in the final risk scores.

**Adjacent work worth noting briefly.** The iRAP methodology (iRAP, 2023) is the largest non-academic comparator, but it scores roads by built-in attributes (lane width, junction frequency, roadside hazards) rather than by observed collision history — a fundamentally different question. Network kernel density estimation, reviewed by Ziakopoulos and Yannis (2020), provides a non-model-based alternative for hotspot identification but does not adjust for exposure. Severity-focused modelling (Savolainen et al., 2011; Michalaki et al., 2015) addresses what conditions predict severity *given* a crash, which is conditional on the frequency model ORR fits and is a candidate for parallel future work.

### 1.3 Contribution

As far as I can determine from a public-source scan, no other publicly available system combines national STATS19 collision data, full-network coverage across multiple regions, exposure-adjusted SPF-style modelling, open methods, and a reproducible public code base simultaneously. The closest comparators each lack at least one of these properties: iRAP lacks open methods and collision-based modelling; Gilardi et al. (2022) is restricted to a single city; DfT's own Road Safety Framework (DfT, 2024) is national but not link-level; the ML-based comparators either lack exposure adjustment (Gao et al., 2024) or operate at a different scale (Pan et al., 2017). ORR's contribution is not methodological novelty in any single component — the offset structure is from the HSM tradition, the centrality features are from Jayasinghe et al., XGBoost with a Poisson objective is standard — but the combination, applied at full-network grain on open UK data, with a reproducible public implementation.

The document is structured as follows. Section 2 describes the data sources. Section 3 gives the pipeline architecture. Sections 4–6 describe the methodology of each stage. Section 7 covers Empirical Bayes shrinkage. Section 8 describes the evaluation design. Section 9 gives current results. Section 10 lists known limitations. Section 11 situates the work in more detail relative to specific comparators. Section 12 outlines future methodological directions.

---

## 2. Data sources

| Source | Role in pipeline | Licence |
|--------|-----------------|---------|
| DfT STATS19 (2015–2024) | Collision outcomes for Stage 2 | Open Government Licence |
| DfT AADF by direction (2015–2024) | Observed traffic counts for Stage 1a training | Open Government Licence |
| National Highways WebTRIS | Within-day traffic profiles for Stage 1b | Open data; reuse terms to confirm before redistribution |
| OS Open Roads | Network backbone and link geometry | Open Government Licence |
| OpenStreetMap | Road attributes: speed limits, lanes, surface | ODbL (share-alike applies to derived databases) |
| ONS LSOA boundaries and population | Population density; deprivation indices (IMD) | Open Government Licence |
| OS Terrain 50 | Elevation and road gradient | Open Government Licence |

STATS19 records injury collisions reported to police in Great Britain. For the current study area, 203,928 collision records spanning 2015–2024 were loaded; 99.8% were successfully snapped to OS Open Roads links using a weighted multi-criteria matching procedure (mean snap score 0.860). The pipeline applies COVID flags for 2020 and part of 2021 but retains those years in training.

The AADF dataset contains both directly observed count-point measurements and DfT-interpolated estimates. Stage 1a uses only rows where `estimation_method == "Counted"`. Of the 14,193 count points in the 2015–2024 window, 12,905 have at least one directly counted observation and form the training set. The drop rate is approximately twice as high on Major roads (11.2%) as on Minor roads (4.6%), which means the training set is modestly less representative of major-road conditions; this is accepted as preferable to contaminating the target with DfT's own interpolation model.

WebTRIS data covers only the National Highways strategic road network. The current pull contains 15,011 site × year rows from 5,948 sensor sites for 2019, 2021, and 2023. This sparsity — both in site coverage and in year availability — means Stage 1b is confined to the motorway and major A-road network and cannot be extended to the wider network without additional sensor data.

OSM attribute coverage is partial. Raw speed limits are available for 56.4% of links; a tiered imputation from OS road classifications provides `speed_limit_mph_effective` for 91.27% of links. Lane counts (7.3%), lighting status (9.3%), and surface type (16.2%) are much sparser and are median-imputed where included.

*Supporting material: [data-quality-notes.md](../docs/internal/data-quality-notes.md); [Stage 1a — AADT model page](../quarto/methodology/exposure-model.qmd); [AADF counted-only filter investigation](../quarto/investigations/aadf-counted-only-filter.qmd)*

---

## 3. Pipeline architecture

The pipeline has three modelling stages followed by an output layer. Inputs feed two parallel Stage 1 models; Stage 1a's output becomes the exposure denominator for Stage 2, which produces the risk scores:

```
INPUTS                  STAGE 1            STAGE 2         OUTPUT

DfT AADF counts     -> Stage 1a: AADT  --+
OS Open Roads          estimation        |
OSM/ONS/Terrain        (HGBR)            +-> Stage 2:   -> risk_scores
                                         |   collision     .parquet
DfT STATS19         ---------------------+   model         (+ EB and
collisions                               |   (Poisson       family
                                         |   GLM +          variants)
National Highways   -> Stage 1b:      ---+   XGBoost)
WebTRIS                time-zone
                       profiles
                       [diagnostic;
                       not in score]
```

Stage 1b is shown dashed-in because it is diagnostic only: it is built but does not currently feed the Stage 2 production score (Section 5). Each stage is a separate scikit-learn-compatible model that can be retrained independently. The CLI entrypoint is `python -m road_risk.model --stage <traffic|profile|collision|all>`. Stage 1a must precede Stage 2 because Stage 2 consumes Stage 1a's AADT estimates as the exposure denominator.

*Supporting material: [Modelling approach overview](../quarto/methodology/modelling.qmd); [Model inventory](../quarto/methodology/model-inventory.qmd); [CODE_README.md](../CODE_README.md)*

---

## 4. Stage 1a: AADT estimation

Stage 1a estimates Annual Average Daily Traffic (AADT) for every OS Open Roads link × year, using AADF count points as the training signal and network + road attributes as predictors.

### 4.1 Model family

The estimator is scikit-learn's `HistGradientBoostingRegressor` (HGBR). HGBR was chosen for three reasons: it scales to the 2.1M-link inference set efficiently, handles missing values natively without requiring imputation, and captures non-linear interactions between road type, location, and network position that a linear model would miss. The target variable is `log(AADT)` after year de-meaning within each count point, which removes the long-term trend from what the cross-sectional predictors need to explain. At inference, the year mean is added back.

### 4.2 Features

Features included in Stage 1a are road classification, trunk-road indicator, geographic centroid coordinates, link length, distance to the nearest major road, betweenness centrality in the OS Open Roads graph, population density from ONS LSOA data, HGV proportion where directly measured by AADF, and selected OSM attributes. WebTRIS time-profile features are explicitly excluded from Stage 1a because they are not available at full-network inference time.

Jayasinghe et al. (2019) demonstrate that betweenness centrality in a dual road graph predicts AADT substantially better than location alone, and that models using centrality features outperform both pure-location and pure-classification models on low-count roads. The feature set used here follows that principle.

### 4.3 Cross-validation

Stage 1a uses `GroupKFold` grouped by `count_point_id`, so that every observation from a given count point is in either train or validation, never both. This prevents spatial leakage from repeated observations at the same physical location. Two external holdout schemes are evaluated after the primary CV:

- **Local holdout** (Scheme 1): 20% of count point IDs withheld at random. Tests within-region generalisation.
- **Spatial holdout** (Scheme 2): all count points north of the 75th-percentile latitude withheld. Tests north-south extrapolation.

Mahoney et al. (2023) show that standard random k-fold cross-validation is severely optimistically biased for spatially autocorrelated data, and that the degree of bias is proportional to the spatial autocorrelation range. Grouped-by-point CV is better than random splitting but does not enforce a spatial buffer between train and validation; adjacent roads at different count points may remain correlated. The spatial block holdout partially addresses this, but variogram-based buffer sizing (as recommended by Mahoney et al., 2023) has not been implemented.

### 4.4 Holdout performance

At the most recent recorded run (git SHA `301a766b`, 2026-05-03):

| Holdout scheme | R² |
|---|---|
| Local (20% of count points withheld) | 0.832 |
| Spatial (northern block withheld) | 0.788 |

The lower spatial R² is expected: the northern spatial block tests out-of-distribution extrapolation rather than within-distribution interpolation. This gap may also reflect the absence of explicit spatial error terms in the HGBR model.

*Note: These R² values are on the counted-only holdout. The R² increase from ~0.72 (estimated-rows-included baseline) to ~0.83 (counted-only) partly reflects a cleaner target rather than an intrinsically stronger model; see [AADF counted-only filter investigation](../quarto/investigations/aadf-counted-only-filter.qmd) for the controlled comparison.*

AADT estimates are not interval-valued: Stage 1a produces a point prediction only. Propagating Stage 1a uncertainty into Stage 2 is the highest-priority methodological gap and is discussed in Section 10.

*Supporting material: [Stage 1a methodology page](../quarto/methodology/exposure-model.qmd); [AADF counted-only filter investigation](../quarto/investigations/aadf-counted-only-filter.qmd); [aadt.py source](../src/road_risk/model/aadt.py)*

---

## 5. Stage 1b: time-zone profiles

Stage 1b estimates within-day traffic fractions (peak, pre-peak, off-peak) using National Highways WebTRIS sensor reports. One `HistGradientBoostingRegressor` is fitted per time-band fraction, grouped by `site_id` in cross-validation. Predictions are combined with Stage 1a AADT estimates to reconstruct reconstructed hourly flows for each link in the study area.

Stage 1b is currently diagnostic and does not feed the Stage 2 production score. The main reasons for deferring integration are: (1) WebTRIS sensor coverage is confined to the strategic road network, so time-zone profiles are unavailable for the large majority of the 2.17M links; (2) integrating profiles into Stage 2 would require rebuilding the collision count model at link × year × time-band grain, which is a substantial refactor. The Stage 1b output (`timezone_profiles.parquet`) provides material for temporal robustness checks (see [Temporal exploration analysis](../quarto/analysis/temporal-exploration.qmd)) but does not currently affect risk rankings.

Mensah and Hauer (1998) give a theoretical basis for why averaging temporal flows before entering them into an SPF introduces bias: the expected crash rate under variable flow is not the same as the crash rate under average flow unless the SPF is linear in flow. At annual grain, this bias is a known accepted limitation.

*Supporting material: [Stage 1b methodology page](../quarto/methodology/timezone-profile.qmd); [Temporal exploration](../quarto/analysis/temporal-exploration.qmd)*

---

## 6. Stage 2: collision risk modelling

Stage 2 models annual injury collision counts per link-year using the Stage 1a AADT estimates as the exposure denominator. Two models are fitted in parallel.

### 6.1 Poisson formulation and the exposure offset

The canonical form for a crash-frequency model on a road segment is a Poisson GLM with the log of vehicle-kilometres as an offset:

$$\log(\mu_{it}) = \log(\text{AADT}_{it} \times L_i \times 365 / 10^6) + \beta_0 + \sum_k \beta_k X_{itk}$$

where $\mu_{it}$ is the expected collision count for link $i$ in year $t$, $L_i$ is link length in km, and $X_{itk}$ are road and contextual features. The division by $10^6$ expresses exposure in millions of vehicle-kilometres; as a constant it shifts only the intercept and does not affect the model otherwise. The offset is a fixed term with coefficient 1, not an estimated coefficient. This forces the model to predict a collision *rate* per vehicle-kilometre rather than a raw count, and is the standard SPF form recommended by Hauer et al. (2001) and used by Gilardi et al. (2022) on OS road segments in Leeds.

The offset forces an elasticity of exactly 1.0 between AADT and expected crashes. Several SPF studies report sub-linear AADT elasticity rather than unity: Khodadadi et al. (2021) estimate AADT elasticities of roughly 0.63–0.74 across NB parameterisations for low-volume US roads, and Wang et al. (2009) and Aguero-Valverde and Jovanis (2008) similarly fit AADT as a free covariate rather than a unit-elasticity offset. This constraint was tested directly in ORR. A diagnostic GLM (Model B) was fitted with `log(AADT)` and `log(length)` as free covariates rather than a fixed offset; it estimated an AADT coefficient of 0.93 — close to unity and well above the sub-linear values some of the literature reports for other road types. Model B improved the downsampled training-frame pseudo-R² but did **not** improve calibrated full-frame residuals: it was better on 0 of 10 AADT deciles and 2 of 5 road families, and worse on the calibrated common-basis top-1% band. The fixed-offset model (Model A) was therefore retained for production. The remaining open question is not whether the global elasticity is unity — the global test was run — but whether a *road-family-stratified* free-elasticity model would behave differently; that diagnostic has not been run.

The exposure is currently a *point estimate* from Stage 1a. National Highways (2022) uses the same offset structure in official UK rate-comparison guidance, but assumes vehicle miles are known rather than estimated. The uncertainty in Stage 1a AADT estimates flows unreported into Stage 2.

### 6.2 Model family choice

**Why not OLS?** Lord and Mannering (2010) are explicit: crash-frequency data are non-negative integers and OLS regression is generally inappropriate. OLS produces non-integer and potentially negative predictions and violates variance assumptions for zero-heavy count data.

**Why Poisson over Negative Binomial?** Poisson and Negative Binomial (NB) are both standard families for crash count data. NB is the canonical extension for overdispersion, adding a dispersion parameter $\alpha$ such that $\text{Var}(y) = \mu + \alpha\mu^2$; when $\alpha = 0$, NB reduces to Poisson (Lord and Mannering, 2010). Pew et al. (2020) show in a Bayesian intersection study that the improvement of ZINB over Poisson is driven primarily by the dispersion parameter $\alpha$ rather than by zero-inflation itself (estimated zero-inflation probability $\pi \approx 0$ in both ZIP and ZINB models). This supports running a Poisson GLM as the primary model and testing for overdispersion as a diagnostic step rather than defaulting to NB.

The current Poisson dispersion ratio is approximately 1.401 (see [exposure offset diagnostics report](../reports/exposure_offset_full_frame_diagnostics.md)), below the pre-set 1.5 threshold at which a NB diagnostic run was planned, so NB has not yet been fitted. Two caveats apply. First, this is a single *global* dispersion ratio; facility-specific overdispersion (motorway vs minor road) has not been decomposed, and Chengye and Ranjitkar (2013) find that stratifying a motorway NB model by ramp type reduces overdispersion, suggesting a pooled ratio can mask family-level heterogeneity. Second, Khodadadi et al. (2021) show that for very zero-heavy, low-mean count data, NB-Lindley (NB-L) models substantially outperform standard NB-2 — and ORR's ~98–99% link-year zero rate is more extreme than the regime in which they found that advantage. The dispersion ratio being below threshold is therefore weaker evidence against fitting NB than it first appears; an explicit NB GLM comparator remains a priority diagnostic (see Section 10.4).

Zero-inflated models (ZIP, ZINB) are a natural concern given that ~98–99% of link-years have zero recorded collisions. Pew et al. (2020) find at signalised intersections that the zero-inflation probability is negligible once overdispersion is properly accounted for. At link grain, the situation is different: most zeros are structural (a residential side-street with 50 vehicles/day will have essentially zero expected collisions), not due to a separate zero-generating process. The current implementation does not include a zero-inflation component; this is an accepted limitation.

**GLM and XGBoost in parallel.** Stage 2 fits two models:

- A **Poisson GLM** (`statsmodels.GLM` with `family=Poisson`, log link, and explicit exposure offset). The GLM is trained on a downsampled table — all collision-positive link-years plus zero-collision rows sampled to 10× the positive count — giving roughly 4M training rows (about 391k positives plus ~10× zeros). The downsampling exists to keep the dense `statsmodels` design matrix within memory, not for statistical reasons; the full 17.3M-row table would be ~2GB+ of float64. The GLM is used diagnostically for coefficient interpretation, SHAP analysis, and residual inspection.
- A **Poisson XGBoost regressor** (`XGBRegressor(objective="count:poisson")` with `base_margin=log_exposure`). XGBoost trains on the full link × year table (17.3M rows per seed) via its own chunking. It is the production ranker.

The GLM and XGBoost pseudo-R² values are **not directly comparable**: the GLM figure is in-sample on the ~4M-row downsampled balanced table, while the XGBoost figure is out-of-sample on the held-out link split (about 4.3M test rows) with the real zero-heavy distribution. This asymmetry is a known limitation documented publicly in the model status page; a common evaluation surface is the highest-priority short-term evaluation task.

### 6.3 Feature set and the post-event exclusion policy

Stage 2 features include: `speed_limit_mph_effective` (tiered-imputed speed limit), road classification, `betweenness_relative` (network centrality, normalised), link length, `hgv_proportion`, ONS rural-urban classification (RUC), IMD deprivation deciles, `mean_grade` (from OS Terrain 50), `road_curvature` features (from OS Open Roads geometry), population density, and estimated AADT.

Variables that are computable only from the circumstances of *observed* collisions are explicitly excluded from Stage 2. These include: `pct_dark` (proportion of historical collisions in darkness), `pct_urban`, `pct_junction`, `pct_near_crossing`, and `mean_speed_limit` derived from collision records. These post-event variables are useful diagnostics of *what conditions are associated with past crashes* but would contaminate a model intended to score links *before* future collisions occur — they encode information about where crashes happened, not about the inherent properties of roads. This exclusion boundary is enforced in the feature construction code and documented at [feature-engineering.qmd](../quarto/methodology/feature-engineering.qmd).

Michalaki et al. (2015) demonstrate a similar distinction for motorway severity modelling: variables like number-of-vehicles or casualty counts are legitimately informative about conditional severity (given a crash, what factors predict severity?) but must not be used in a forward-looking frequency model.

Note on `mean_grade`: the current Stage 2 GLM produces a small negative coefficient on mean road gradient (−0.0202), which is opposite to the SPF literature prior. Huda and Al-Kaisy (2024) report grade as a risk factor in low-volume road screening, and the broader SPF literature generally finds steeper roads associated with higher risk. The negative sign in ORR is most likely a confounding effect with road class (steep rural minor roads may carry very little traffic and have low collision rates), but this has not been tested.

### 6.4 Grouped cross-validation

Stage 2 holds out complete link identifiers: all link-year rows for a given `link_id` are in either train or test. This prevents the model from learning from one year of a link and predicting another year of the same link. It does not prevent leakage across spatially adjacent links, which is a weaker guarantee than buffered spatial CV (Mahoney et al., 2023).

The evaluation uses five fixed random seeds and reports mean and range of pseudo-R² across seeds. The top-1% link stability across seeds (Jaccard similarity) is 0.904, providing a practical lower bound on how stable the ranking is under seed variation.

### 6.5 Facility-family split (diagnostic)

A facility-family variant splits Stage 2 training into groups defined by OS road classification and network context (motorway, A-road, B-road, Minor, Unclassified), fitting separate XGBoost models per family. The motivation follows Chengye and Ranjitkar (2013), who show that stratification by ramp type absorbs overdispersion in a motorway NB model, and the broader SPF tradition (Harwood et al., 2000; Hauer et al., 2001) of using facility-specific calibration rather than a single global model.

The family-split variant is currently flagged as overfitting on the motorway family (held-out residuals larger than the pooled model, reversals in family-wise predictions). This is likely due to the relatively small number of motorway link-years. The family-split v2 is deferred pending further investigation.

*Supporting material: [Rank stability investigation](../quarto/investigations/rank-stability.qmd); [rank_stability.md](../reports/rank_stability.md); [collision.py source](../src/road_risk/model/collision.py); [feature-engineering.qmd](../quarto/methodology/feature-engineering.qmd); [Facility-family split page](../quarto/methodology/facility-family-split.qmd); [family_validation.md](../reports/family_validation.md)*

---

## 7. Empirical Bayes shrinkage

An Empirical Bayes (EB) shrinkage layer is implemented as a diagnostic variant (`risk_scores_eb.parquet`). EB shrinkage combines the model's prediction with the link's observed collision history to produce a history-adjusted estimate, following the HSM combining form (Hauer et al., 2001). On links with little observed history the model prediction is trusted more; on links with a long observed history the observed counts are trusted more.

The shrinkage operates in *total-count space* over each link's observed period. For a link with per-year XGBoost prediction $\mu$ and $n$ observed years, let $N_\text{pred} = \mu \cdot n$ be the total predicted count and $N_\text{obs}$ the total observed count. Then:

$$w = \frac{1}{1 + k \cdot N_\text{pred}}$$

$$N_\text{EB} = w \cdot N_\text{pred} + (1 - w) \cdot N_\text{obs}$$

$$\hat{\lambda} = N_\text{EB} / n$$

where $w$ is the weight on the *model prediction* (not the observation), and $\hat{\lambda}$ is the EB-adjusted per-year rate used for ranking. The dispersion parameter $k$ is a single global value estimated by method-of-moments from binned prediction/observation summaries under the NB2 relation $\text{Var}(y) = E(y) + k\,E(y)^2$; the production run uses the positive-event-weighted aggregation, $k = 3.451$.

A note on parameterisation: this is the standard HSM combining form, with $k$ in the NB2 dispersion convention $\text{Var} = E + kE^2$. An equivalent NB2 can be written with $k$ as a *size* parameter in the form $k/(k+N_\text{pred})$, and the two conventions are not interchangeable — at $k = 3.451$ they give very different weights. The code is correct and internally consistent, but the methodology page does not currently spell out which convention $k$ follows, so anyone comparing $k = 3.451$ against a literature NB2 size parameter would draw the wrong conclusion. This is a documentation gap rather than a modelling error.

The EB top-1% intersection with the non-EB ranking is 38.85% (8,421 of 21,675 links), meaning EB substantially reshuffles the top-1% list. This reflects the combination of a global (not facility-family) $k$ and the zero-heavy distribution: links with high raw model predictions but no collision history are sharply downweighted. The Hauer et al. (2001) method recommends facility-specific calibration rather than a global $k$, and the facility-family split (Section 6.5) is partly motivated by this.

The EB layer is currently diagnostic only and is not used to generate the production ranking. The main reason is that the EB and non-EB rankings converge to near-identical lists only at very high percentiles (Jaccard at top-1%: 0.3885; at top-5%: higher, though not yet reported). Whether this instability is desirable (EB is removing false positives on sparse links) or problematic (EB is suppressing genuinely dangerous links with sparse history) is unresolved.

*Supporting material: [EB shrinkage page](../quarto/methodology/empirical-bayes-shrinkage.qmd); [eb_validation.md](../reports/eb_validation.md); [eb_shrinkage.py source](../src/road_risk/model/eb_shrinkage.py)*

---

## 8. Evaluation design

### 8.1 Pseudo-R²

Stage 2 model performance is reported as McFadden's pseudo-R² for Poisson models:

$$\text{pseudo-}R^2 = 1 - \frac{\ell(\hat{\beta})}{\ell(\bar{y})}$$

where $\ell(\hat{\beta})$ is the fitted log-likelihood and $\ell(\bar{y})$ is the null-model (intercept-only) log-likelihood. Pseudo-R² is the standard diagnostic for Poisson GLMs, but it does not have a direct analogue in terms of explained variance and is not directly comparable across differently-sampled datasets. The GLM figure (0.347) is in-sample on a downsampled table; the XGBoost figure (0.323) is out-of-sample on the full link × year distribution.

### 8.2 Rank stability

Because the primary output is a percentile ranking rather than calibrated count estimates, rank stability is a more operationally relevant metric than fit statistics. The 5-seed stability harness trains and scores the production XGBoost model under five different random seeds and reports:

- **Spearman rank correlation** of the full percentile vector across seed pairs
- **Top-1% Jaccard similarity**: fraction of the 21,675 top-ranked links that appear in the top-1% ranking across all five seed pairs

Current values: Spearman 0.999; top-1% Jaccard 0.904. These indicate that the ranking is very stable overall, and that approximately 90% of the top-1% list is consistent across all seeds. The Jaccard noise floor is 0.904; feature additions that change the ranking by less than this are within seed noise and cannot be claimed as genuine improvements.

*Supporting material: [Rank stability investigation](../quarto/investigations/rank-stability.qmd); [rank_stability.md](../reports/rank_stability.md)*

### 8.3 Zero-calibration

The zero-calibration diagnostic checks whether the model is systematically miscalibrated on zero-collision links. If the proportion of zero-collision links in the top-k% of predicted risk is much higher than expected, the model is assigning high risk scores to links with no collision history — plausibly correct (they may simply be lucky so far) or a sign of exposure-denominator errors. See [zero-calibration investigation](../quarto/investigations/zero-calibration.qmd) and [zero_calibration.md](../reports/zero_calibration.md).

### 8.4 Evaluation limitations

The current evaluation has three important limitations:

1. **No common holdout surface.** The GLM and XGBoost are not evaluated on the same held-out rows against the same null model, so the published figures cannot be used to determine which model performs better.
2. **Grouped CV is not spatial CV.** Adjacent links remain correlated across the train/test split. Mahoney et al. (2023) show, in a simulation study, that standard V-fold CV is severely optimistically biased for spatially autocorrelated data and that the appropriate spatial-CV exclusion buffer scales with the autocorrelation range. The magnitude of this bias for ORR has not been quantified, and the buffer sizes in that study are simulation-specific and do not transfer directly to a road network.
3. **No external benchmark.** All evaluation is internal holdout. No independent safety screening scheme has been compared against the ORR ranking on overlapping geography.

---

## 9. Current results

The most recent model run (git SHA `301a766b`, 2026-05-03):

| Stage | Metric | Value |
|------|--------|-------|
| Stage 1a (AADT) | Local holdout R² | 0.832 |
| Stage 1a (AADT) | Spatial holdout R² | 0.788 |
| Stage 2 GLM | Pseudo-R² (in-sample, downsampled) | 0.347 |
| Stage 2 XGBoost | Pseudo-R² (held-out, grouped by link, 5 seeds) | 0.323 |
| Stage 2 XGBoost | Top-1% Jaccard (5 seeds) | 0.904 |
| Stage 2 XGBoost | Spearman rank correlation (5 seeds) | 0.999 |
| Top-1% link count | — | 21,675 |
| EB shrinkage parameter | k (production, positive-event weighted) | 3.451 |
| EB top-1% intersection with non-EB ranking | — | 38.85% |

The XGBoost pseudo-R² of 0.323 is an out-of-sample estimate under grouped-link CV. It should not be read as low without context: on a target where ~99% of link-years are zero, held-out pseudo-R² in this range is unremarkable, and cross-study comparison is in any case unreliable because reported fit statistics differ by zero-rate, spatial unit, and evaluation design (Gilardi et al. (2022) report Bayesian DIC rather than held-out pseudo-R²; Chengye and Ranjitkar (2013) report NB deviance and squared Pearson correlation). The figure earlier documented at ~0.86 was a pre-fix artefact inflated by feature-table leakage in the `hgv_proportion` join; it was corrected during normal development and is noted here only because the stale value still appears in some repository documents (see Section 10.9).

An interactive map of the top-1% highest-risk links is published at [Top-risk map](../quarto/outputs/top-risk-map.qmd). The map uses May 2026 production scores with an EB refresh.

---

## 10. Known limitations

These limitations are listed in roughly the order I would address them.

### 10.1 Unpropagated Stage 1a uncertainty

Stage 1a produces point predictions only. Stage 2 treats those predictions as exact exposure, so the downstream risk scores understate total uncertainty: the pseudo-R² of 0.323 is conditional on Stage 1a being correct. The right fix is interval prediction at Stage 1a — for example, using a Quantile Random Forest (QRF) or conformal prediction — propagated into Stage 2 via repeated draws from the Stage 1a predictive distribution or via analytic approximation. Until this is implemented, any stated confidence interval on a Stage 2 risk score is conditional on Stage 1a, which it should not be.

### 10.2 Fixed log-offset: global test done, family-stratified test open

The exposure offset fixes the AADT elasticity at 1.0. As described in Section 6.1, this was tested directly: a diagnostic GLM with `log(AADT)` and `log(length)` as free covariates estimated an AADT coefficient of 0.93 — close to unity — and did not improve calibrated full-frame residuals over the fixed-offset model, which was therefore retained. So the *global* elasticity question has been answered. What remains open is whether a road-family-stratified free-elasticity model would behave differently: some of the SPF literature (Khodadadi et al., 2021; Wang et al., 2009) reports sub-linear AADT elasticity that varies by road type, and the global ORR test cannot rule out family-level departures from unity. The family-stratified diagnostic has not been run.

### 10.3 Grouped CV is not spatial CV

The grouped-link holdout does not enforce a spatial buffer between train and validation. Road links adjacent to held-out links are available for training, and the model can learn local spatial patterns that generalise to held-out links not because of the features but because of spatial proximity. Mahoney et al. (2023) recommend variogram-based buffer sizing estimated from Stage 2 residuals. A regional holdout pilot (hold out one force area entirely) would quantify the magnitude of this optimism.

### 10.4 Poisson overdispersion: tested globally, NB comparator still open

Overdispersion was tested. With ~98–99% zero link-years the Poisson mean-variance equality assumption is at risk (Lord and Mannering, 2010, identify this as the primary methodological challenge in crash-frequency modelling), and the measured global dispersion ratio is 1.401 — below the pre-set 1.5 threshold at which an NB run was planned, so NB was not fitted. The limitation is that this decision rests on a *single global* ratio. Facility-specific overdispersion (motorway vs minor road) has not been decomposed, and Khodadadi et al. (2021) show that NB-Lindley models outperform standard NB-2 precisely in the extreme-zero, low-mean regime ORR occupies — which means a sub-threshold global ratio is weaker evidence against NB than it appears. Fitting an NB GLM with the existing exposure offset as a comparator, and a posterior predictive zero check on the current Poisson GLM, remain priority diagnostics.

### 10.5 EB parameterisation is a documentation gap, not an error

The EB weight `w = 1/(1 + k·N_pred)` is the standard HSM combining form with $k$ in the NB2 dispersion convention $\text{Var} = E + kE^2$ (Section 7). It is correct and internally consistent with the reported weights. The only issue is that the methodology page does not state which NB2 convention $k$ follows, so a reader comparing $k = 3.451$ against a literature NB2 *size* parameter (the $k/(k+N_\text{pred})$ form) would misread it. The fix is a one-paragraph note on the methodology page, not a modelling change.

### 10.6 Negative gradient coefficient

The current Stage 2 GLM produces a negative coefficient on `mean_grade` (−0.0202, significant). This is opposite to the SPF literature prior: Huda and Al-Kaisy (2024) report grade as a positive risk factor in low-volume road screening, and steeper roads are generally associated with higher crash rates in the literature. The most likely explanation is a confounding effect with road class — steep rural minor roads carry very little traffic and have low collision rates even on steep gradients — but this has not been tested through stratified analysis or interaction terms.

### 10.7 No external benchmark

All evaluation is against internal holdouts from the same data source (STATS19). No independent screening scheme or field survey has been compared against the ORR ranking on overlapping geography. The closest planned external comparison is against iRAP-style data, but this is still in the design stage. Without external validation, the ranking cannot be claimed to identify genuinely dangerous links beyond what STATS19 and the model together imply.

### 10.8 OSM licensing

OSM attributes are incorporated under the Open Database Licence (ODbL), which has a share-alike provision: databases that materially incorporate ODbL data are themselves subject to ODbL. This applies to `risk_scores.parquet` if OSM-derived features are materially part of the risk computation. An explicit ODbL attribution and licensing note is needed before output files are circulated.

### 10.9 A stale pre-fix model artefact remains in the repository

The repository still contains `collision_xgb.json`, an XGBoost model produced before a data-leakage bug in the `hgv_proportion` feature was identified and fixed (the feature was joined after collision aggregation and so was non-zero only on collision-positive link-years). Post-fix XGBoost pseudo-R² dropped from ~0.86 to ~0.32, confirming the earlier figure was leakage-inflated. The pre-fix artefact should not be used; it is retained pending a retraining step and removal. This is the one item that should be resolved before the repository is presented as a reproducible reference, because a casual reader could pick up the stale artefact or the stale metric.

### 10.10 Historical Yorkshire terminology in code

The project began as a Yorkshire pilot. Variable, module, and constant names still reference Yorkshire even though the study area now covers Northern and Central England. This is harmless to anyone who knows the history but confusing to a reader encountering the code cold; a short README note would resolve it.

---

## 11. Detailed comparison with selected approaches

This section expands the brief survey in Section 1.2 with more detail on the four approaches most directly comparable to ORR.

### 11.1 SPF-based approaches (FHWA/HSM)

The FHWA Highway Safety Manual (Harwood et al., 2000; Srinivasan and Harkey, 2013) is the engineering-standard approach. It prescribes: (a) facility-specific SPFs trained on observed crash counts with AADT and length as predictors; (b) jurisdiction-specific calibration factors to adjust national-average SPFs to local conditions; (c) EB combination of SPF predictions with site history. This is more interpretable and more directly actionable for intervention planning than ORR's current design. The tradeoffs are scale and data requirements: the HSM approach requires manual road inventory segmentation by facility type and junction configuration, which is feasible for major-road networks but does not scale naturally to 2.1M links. ORR's machine-learning approach trades some interpretability for scalability.

*Supporting material: [Hauer et al. (2001) extraction](../literature/papers_summary/paper-extraction-hauer-2001-eb-spf-tutorial.md); [Srinivasan (2013) extraction](../literature/papers_summary/paper-extraction-srinivasan-2013-spf-decision-guide.md)*

### 11.2 UK academic spatial-Bayesian work

Gilardi et al. (2022) is the closest methodological predecessor for UK full-network segment-level crash modelling. They fit a Bayesian hierarchical Poisson model with ICAR spatial random effects to OS road segments in Leeds, using an offset of `log(length × estimated commuter flow)` and reporting multivariate severity outcomes. Their approach is stronger than ORR in several respects: it includes spatial random effects, models severity jointly, and uses Bayesian inference to quantify uncertainty. The trade-off is computational complexity and restriction to a single city with available Census-routed traffic estimates.

Boulieri et al. (2016) take a similar approach at ward level across England with a Bayesian space-time model and AADF-derived exposure. Their ward grain is coarser than ORR but demonstrates the offset structure at UK scale. Wang et al. (2009) model M25 motorway collision counts with spatial Poisson-lognormal and NB variants, fitting AADT and length as free covariates rather than a fixed offset and reporting sub-linear AADT elasticity for the corridor — one of the results motivating the fixed-offset sensitivity check in Section 10.2.

*Supporting material: [Gilardi et al. (2022) extraction](../literature/papers_summary/paper-extraction-gilardi-2022-network-lattice-crashes.md); [Spatial methods page](../quarto/literature/spatial-methods-and-network-risk.qmd)*

### 11.3 Machine-learning comparators

Pan et al. (2017) benchmark a Deep Belief Network against NB regression for a cross-country global SPF, reporting worse out-of-sample performance for the deep model on sparse-count data — useful negative evidence against jumping to complex neural architectures.

Gao et al. (2024) implement a spatio-temporal probabilistic GNN (STZITD-GNN) with zero-inflated Tweedie likelihoods for daily road-level crash prediction in London. The architecture is considerably more expressive than ORR's current Stage 2 and provides explicit uncertainty estimates. However, it uses no exposure offset and cannot distinguish high-risk from high-traffic roads; validation is within-year temporal only (no spatial holdout); and the GNN architecture does not scale to 2.17M links. The AccHR@k metric introduced in that paper — the fraction of actual crash links captured in the top-k% of predicted risk — is directly applicable to ORR and a planned addition to the evaluation stack.

*Supporting material: [Gao et al. (2024) extraction](../literature/papers_summary/paper-extraction-gao-2024-stzitdgnn.md); [Pan et al. (2017) extraction](../literature/papers_summary/paper-extraction-pan-2017-global-road-safety-performance-function-dbn.md)*

### 11.4 Spatial methods review

Ziakopoulos and Yannis (2020) survey spatial approaches in road safety, covering network kernel density estimation, spatial regression, Bayesian hierarchical models, and the modifiable areal unit problem (MAUP). Their key caution — that the choice of spatial unit (link, intersection, zone, grid) materially affects both the model structure and the results — applies directly to ORR's choice of OS Open Roads links as the spatial grain. MAUP sensitivity analysis has not been conducted.

*Supporting material: [Ziakopoulos and Yannis (2020) extraction](../literature/papers_summary/paper-extraction-ziakopoulos-yannis-2020-COMBINED.md)*

---

## 12. Future directions

Listed by priority.

### 12.1 Common evaluation surface (short-term)

The single most important near-term task is computing GLM and XGBoost pseudo-R² on the same held-out link set, against the same null model, with the same row distribution. Until this is done, the relative performance of the two models is unknown.

### 12.2 Interval-valued Stage 1a (medium-term)

Replacing point AADT predictions with calibrated intervals — via Quantile Random Forest, conformal prediction, or gradient-boosted quantile regression — and propagating the resulting uncertainty into Stage 2 via repeated draws is the most important methodological extension. This would produce risk *intervals* rather than point rankings and allow links with high AADT uncertainty to be flagged as such.

### 12.3 Road-family-stratified AADT elasticity (medium-term)

The global free-elasticity test has been run (Section 6.1, Section 10.2): a free-covariate GLM estimated an AADT coefficient near unity and did not beat the fixed offset on calibrated full-frame residuals. The remaining work is to fit the free-covariate model *with road-family interactions*, since Aguero-Valverde and Jovanis (2008) and Al-Omari (2021) both suggest the elasticity departs from unity for some road classes even where a pooled estimate does not. This would confirm whether a single global offset is adequate across families or whether motorway and minor-road links need different exposure treatment.

### 12.4 Spatial cross-validation (medium-term)

Implementing variogram-based buffer sizing and reporting a regionally held-out R² would quantify the magnitude of the current CV optimism. A starting point is estimating the spatial autocorrelation range from Stage 2 residuals and using that as the exclusion buffer radius (Mahoney et al., 2023).

### 12.5 Family-specific or hierarchical Stage 2 (medium-term)

Making the facility-family split operational — with per-family dispersion estimation and family-specific holdout evaluation — would bring ORR closer to the calibration discipline of the HSM approach. A hierarchical Poisson model (partially pooled across families) is a natural generalisation that shares strength across families while allowing family-specific parameters.

### 12.6 External benchmark (medium-term)

A first external convergent-validity check against an independent safety screening surface on overlapping geography — whether iRAP data, local authority screening outputs, or a regional safety scheme — is necessary before any operational claim is made. The iRAP benchmark design is in the active task queue; practical execution requires data access or a collaborating organisation with overlapping geography.

### 12.7 Severity-aware and mode-specific variants (longer-term)

Fitting parallel Stage 2 models with KSI-weighted, fatal-only, motorcycle-specific, or VRU-weighted targets would produce decision-useful outputs for specific stakeholder groups. These are straightforward modifications of the Stage 2 training pipeline (the change is in the target variable and exposure denominator, not the model architecture) but require policy input on severity weighting before implementation.

---

## 13. Conclusions

Open Road Risk demonstrates that exposure-adjusted safety performance modelling at full-network scale is feasible using only open data, across the road network of Northern and Central England. The pipeline's key methodological contributions are the counted-only AADF filter, the grouped cross-validation design, the post-event feature exclusion policy, and the explicit documentation of where the model's assumptions may be wrong. The headline out-of-sample XGBoost pseudo-R² of 0.323 is modest by construction, given a target that is ~99% zeros; the work's value is in the ranking and the openness, not the fit statistic.

The pipeline is a research prototype, not a decision-grade operational product. Its value is as a transparent reference implementation and a substrate for methodological experimentation. The work required to move it toward operational use — uncertainty-aware exposure estimation, spatial cross-validation, external benchmarking, and common evaluation surfaces for GLM and XGBoost — is described in Sections 10 and 12.

---

## How to cite

This work is archived on Zenodo, which mints a persistent DOI for each release. Please cite the Zenodo record:

> Simm, T. (2026). *Open Road Risk: an open-data pipeline for exposure-adjusted collision risk across the road network of Northern and Central England.* Zenodo. https://doi.org/10.5281/zenodo.20451731

The DOI above resolves to the latest version. The project site (https://openroadrisk.org/) and code repository (https://github.com/ThomasHSimm/open-road-risk) are authoritative for the current state of the work.

---

## References

Citations are given in author-year format. Full extraction notes, quality flags, and per-paper traceability are held in the repository under `literature/papers_summary/` and on the project site's literature pages.

**Aguero-Valverde and Jovanis (2008)**
Analysis of Road Crash Frequency with Spatial Models. *Accident Analysis and Prevention*.

**Al-Omari (2021)**
Crash Analysis and Development of Safety Performance Functions for Florida Roads in the Framework of the Context Classification System. PhD thesis, Florida.

**Boulieri et al. (2016)**
A space-time multivariate Bayesian model to analyse road traffic accidents by severity. *Journal of the Royal Statistical Society, Series A*.

**Chengye and Ranjitkar (2013)**
Modelling Motorway Accidents using Negative Binomial Regression.

**DfT (2024)**
Road Safety Framework: Initial Analysis.

**DfT (2025)**
Reported Road Casualties Great Britain: 2024 Annual Report.

**Gao et al. (2024)**
Uncertainty-Aware Probabilistic Graph Neural Networks for Road-Level Traffic Crash Prediction. *Transportation Research Part C*.

**Gilardi et al. (2022)**
Multivariate hierarchical analysis of car crashes data considering a spatial network lattice. *Journal of the Royal Statistical Society, Series A*, 185(3), 1150–1177.

**Harwood et al. (2000)**
Prediction of the Expected Safety Performance of Rural Two-Lane Highways. FHWA-RD-99-207.

**Hauer et al. (2001)**
Estimating Safety by the Empirical Bayes Method: A Tutorial.

**Huda and Al-Kaisy (2024)**
Network Screening on Low-Volume Roads Using Risk Factors.

**Jayasinghe et al. (2019)**
A novel approach to model traffic on road segments of large-scale urban road networks.

**Khodadadi et al. (2021)**
Application of different negative binomial parameterizations to develop safety performance functions for non-federal aid system roads.

**Lord and Mannering (2010)**
The Statistical Analysis of Crash-Frequency Data: A Review and Assessment of Methodological Alternatives. *Transportation Research Part A*, 44(5), 291–305.

**Mahoney et al. (2023)**
Assessing the Performance of Spatial Cross-Validation Approaches for Models of Spatially Structured Data.

**Mensah and Hauer (1998)**
Two Problems of Averaging Arising in the Estimation of the Relationship Between Accidents and Traffic Flow.

**Michalaki et al. (2015)**
Exploring the factors affecting motorway accident severity in England using the generalised ordered logistic regression model. *Journal of Safety Research*.

**National Highways (2022)**
Comparing Collision and Casualty Rates.

**Pan et al. (2017)**
Development of a global road safety performance function using deep neural networks. *International Journal of Transportation Science and Technology*.

**Pew et al. (2020)**
Justification for considering zero-inflated models in crash frequency analysis. *Analytic Methods in Accident Research*.

**Poch and Mannering (1996)**
Negative Binomial Analysis of Intersection-Accident Frequencies. *Journal of Transportation Engineering*.

**Savolainen et al. (2011)**
The Statistical Analysis of Highway Crash-Injury Severities: A Review and Assessment of Methodological Alternatives. *Accident Analysis and Prevention*.

**Srinivasan and Harkey (2013)**
Selecting a Safety Performance Function for a Project-Level Analysis. FHWA-SA-14-004.

**Wang et al. (2009)**
Impact of Traffic Congestion on Road Safety: A Spatial Analysis of the M25 Motorway in England.

**Ziakopoulos and Yannis (2020)**
A review of spatial approaches in road safety.

---

*This document reflects the project state at git SHA `301a766b` (2026-05-03). Project site, repository, and methodology pages are authoritative for the current state. Internal notes and reports linked above are supporting material and may contain stale metrics from pre-fix model runs; the consistency review at [`docs/internal/consistency-review-2026-05-23.md`](../docs/internal/consistency-review-2026-05-23.md) documents which internal documents contain superseded figures.*