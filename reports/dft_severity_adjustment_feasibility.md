# DfT Severity Adjustment Columns - KSI Feasibility Check

**Status:** feasibility report only. No KSI modelling, register edit, diagnostic
rerun, or model-code change.

**Recommendation:** **tighten parking entry only**. The adjusted severity
columns are available locally across the full 2015-2024 study period, so the
old revisit trigger is technically reachable. That does not by itself unpark the
KSI atlas: the Part A force/year test must be rerun on adjusted expected KSI
counts, and the downstream EB/link-year treatment would need explicit
methodological work.

## Sources Checked

- Local processed STATS19:
  - `data/processed/stats19/collision.parquet`
  - `data/processed/stats19/collision_clean.parquet`
  - `data/processed/stats19/casualty.parquet`
  - `data/processed/stats19/casualty_clean.parquet`
- Local raw STATS19:
  - `data/raw/stats19/dft-road-casualty-statistics-collision-1979-latest-published-year.csv`
  - `data/raw/stats19/dft-road-casualty-statistics-casualty-1979-latest-published-year.csv`
  - `data/raw/stats19/dft-road-casualty-statistics-road-safety-open-dataset-data-guide-2024.xlsx`
- Existing ORR KSI artefacts:
  - `reports/ksi_reporting_consistency.md`
  - `reports/preregistration/ksi_diagnostic_preregistration.md`
  - `src/road_risk/diagnostics/ksi_reporting_consistency.py`
  - `src/road_risk/model/eb_shrinkage.py`
  - `src/road_risk/model/collision.py`
- DfT/GOV.UK:
  - [Road safety open data](https://www.gov.uk/government/statistical-data-sets/road-safety-open-data)
  - [Guide to severity adjustments for reported road casualties Great Britain](https://www.gov.uk/government/publications/guide-to-severity-adjustments-for-reported-road-casualty-statistics/guide-to-severity-adjustments-for-reported-road-casualties-great-britain)
  - [Estimating and adjusting for changes in the method of severity reporting for road accidents and casualty data: final report](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/820588/severity-reporting-methodology-final-report.odt)
  - [Annex: update to severity adjustment methodology](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/922708/annex-update-severity-adjustments-methodology.pdf)

## Part 1: Local Data Inventory

The local processed collision files already contain the requested
collision-level adjusted columns:

- `enhanced_severity_collision`: `int64`
- `collision_adjusted_severity_serious`: `float64`
- `collision_adjusted_severity_slight`: `float64`

The local processed casualty files also contain the casualty-level equivalents:

- `enhanced_casualty_severity`: `int64`
- `casualty_adjusted_severity_serious`: `float64`
- `casualty_adjusted_severity_slight`: `float64`
- `casualty_injury_based`: `int64`

The raw collision CSV header also contains
`enhanced_severity_collision`, `collision_adjusted_severity_serious`, and
`collision_adjusted_severity_slight`; the raw casualty CSV contains the
casualty-level adjusted columns. The raw files are named
`1979-latest-published-year`, and local mtimes are March 2026 for raw STATS19
and April 2026 for processed STATS19. The current DfT open data page says the
2024 annual data are the latest final annual files and that the adjustment
figures are now embedded in the main tables rather than supplied only as
separate lookups. This local extract is therefore current for the ORR 2015-2024
study window without downloading any large replacement files.

### Collision-Level Coverage

All three collision-level adjusted severity columns are present and non-null for
every local collision row in 2015-2024.

| year | rows | enhanced severity non-null | adjusted serious non-null | serious range | adjusted slight non-null | slight range |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| 2015 | 56,229 | 56,229 | 56,229 | 0-1 | 56,229 | 0-1 |
| 2016 | 54,712 | 54,712 | 54,712 | 0-1 | 54,712 | 0-1 |
| 2017 | 51,297 | 51,297 | 51,297 | 0-1 | 51,297 | 0-1 |
| 2018 | 48,344 | 48,344 | 48,344 | 0-1 | 48,344 | 0-1 |
| 2019 | 45,473 | 45,473 | 45,473 | 0-1 | 45,473 | 0-1 |
| 2020 | 34,665 | 34,665 | 34,665 | 0-1 | 34,665 | 0-1 |
| 2021 | 39,458 | 39,458 | 39,458 | 0-1 | 39,458 | 0-1 |
| 2022 | 41,122 | 41,122 | 41,122 | 0-1 | 41,122 | 0-1 |
| 2023 | 40,634 | 40,634 | 40,634 | 0-1 | 40,634 | 0-1 |
| 2024 | 40,963 | 40,963 | 40,963 | 0-1 | 40,963 | 0-1 |

### Collision-Level Value Distribution

The adjusted columns are probability / expected-count components, not integer
counts. Fatal collisions receive 0 in both adjusted serious and adjusted slight
columns; a collision-level expected KSI target therefore needs
`fatal_indicator + collision_adjusted_severity_serious`.

| year | serious mean | serious p25 | serious median | serious p75 | serious zeros | serious ones | slight mean | slight p25 | slight median | slight p75 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2015 | 0.213 | 0.020 | 0.065 | 0.159 | 3,848 | 8,628 | 0.773 | 0.831 | 0.931 | 0.978 |
| 2016 | 0.206 | 0.000 | 0.032 | 0.142 | 21,140 | 9,190 | 0.780 | 0.846 | 0.964 | 1.000 |
| 2017 | 0.220 | 0.000 | 0.036 | 0.157 | 19,852 | 9,315 | 0.764 | 0.827 | 0.959 | 1.000 |
| 2018 | 0.233 | 0.000 | 0.042 | 0.176 | 17,921 | 9,320 | 0.750 | 0.805 | 0.953 | 1.000 |
| 2019 | 0.237 | 0.000 | 0.030 | 0.165 | 19,073 | 9,263 | 0.746 | 0.809 | 0.964 | 1.000 |
| 2020 | 0.248 | 0.000 | 0.035 | 0.183 | 14,234 | 7,417 | 0.734 | 0.782 | 0.958 | 1.000 |
| 2021 | 0.251 | 0.000 | 0.000 | 0.181 | 19,861 | 8,968 | 0.731 | 0.734 | 0.989 | 1.000 |
| 2022 | 0.262 | 0.000 | 0.000 | 0.230 | 22,075 | 9,959 | 0.719 | 0.000 | 1.000 | 1.000 |
| 2023 | 0.268 | 0.000 | 0.000 | 0.337 | 21,594 | 10,076 | 0.714 | 0.000 | 1.000 | 1.000 |
| 2024 | 0.271 | 0.000 | 0.000 | 1.000 | 23,825 | 10,434 | 0.711 | 0.000 | 1.000 | 1.000 |

The increasing share of exact 0/1 values is consistent with more records being
reported directly under injury-based systems: for records already assessed under
IBRS, DfT assigns probability 1 to the recorded non-fatal severity category and
0 to the other category.

### Recorded Severity Columns Present

For years where the adjusted columns are present, the unadjusted severity columns
also remain available. `collision_severity` is integer-coded fatal/serious/slight
and `enhanced_severity_collision` is a richer injury-based/enhanced severity
code with values observed locally as `-1`, `1`, `3`, `5`, `6`, and `7`.

The previous KSI diagnostic used `collision_severity in {1, 2}`. A drop-in
adjusted KSI target would not use `enhanced_severity_collision` directly; it
would use recorded fatal plus adjusted serious probability.

## Part 2: Methodology Documentation

DfT's severity adjustment exists because police forces moved at different times
from officer-judgement severity coding to injury-based reporting systems such as
CRASH and COPA. DfT states that injury-based reporting is expected to be more
accurate, but it changes the level and trend of serious injury counts. The 2024
guide lists force-specific adoption dates and notes phased transitions; in the
ORR study area this matters because South Yorkshire, Staffordshire, Cumbria,
Humberside, Suffolk, Cambridgeshire, Lancashire, Greater Manchester,
Nottinghamshire, West Yorkshire, and other forces adopted at different points in
or near the 2015-2024 modelling window.

The ONS/DfT final report considered two approaches: aggregate time-series models
and record-level logistic regression. The chosen approach was the record-level
logistic model, validated against time-series checks. The model estimates the
probability that a non-fatal casualty or collision would be classified as serious
or slight under an injury-based reporting system. It assumes the reporting-system
change affects the split between slight and serious, not the number of total
casualties/collisions or fatalities.

`collision_adjusted_severity_serious` is therefore best read as the modelled
probability / expected contribution that this non-fatal collision would be a
serious collision under IBRS. It is not a deterministic replacement label for an
individual record. `collision_adjusted_severity_slight` is the paired slight
probability. For non-fatal collisions these are complementary expected severity
components; for fatal collisions both adjusted serious and adjusted slight are 0,
because fatal severity is not adjusted.

The adjustment is force/time-sensitive in the practical sense required by the KSI
parking decision. The methodology explicitly includes reporting-system status,
police force, and an interaction between reporting system and force; the DfT
guide and final report both stress that force-level adoption dates and
force-specific pre-IBRS practice are central to the adjustment. For forces with
no or limited IBRS experience, the method necessarily relies on assumptions about
typical IBRS effects, so cross-force comparisons remain more uncertain than
national trends.

DfT's most relevant use cautions are:

- use adjusted severities for trends over time when an area or comparison spans
  mixed IBRS/NIBRS reporting;
- use adjusted severities for comparisons across police forces/geographies when
  some forces use IBRS and some do not;
- use adjusted severities for severity distributions when aggregating around
  1,000 records or more;
- use unadjusted recorded severity for individual records and for small/local
  datasets;
- estimates for NIBRS forces and force-level comparisons carry extra modelling
  uncertainty, and some force-level trends are sensitive to modelling choices.

This is mostly favourable for an ORR Part A rerun at force/year grain, because
force/year cells are aggregate comparisons and most have hundreds to thousands
of collisions. It is less favourable for direct interpretation at individual
link-year grain, where most cells are zero or near zero and many links have very
small exposure.

## Part 3: Integration Assessment

### 3.1 Coverage Gap Handling

The expected partial-coverage problem does not appear in the local 2015-2024
data. Adjusted collision-level and casualty-level columns are present across all
study years. That removes the need to choose among the three fallback strategies
for this study window.

The fallback options remain relevant for reproducibility:

- Use unadjusted severity for pre-coverage years: not needed locally, and would
  reintroduce the heterogeneity that parked KSI.
- Apply published lookup-based adjustments retroactively: not needed locally,
  because the current DfT main tables already embed the adjustment columns.
- Restrict to adjusted-column years: not needed locally, and would unnecessarily
  shrink an already sparse KSI substrate.

### 3.2 Probabilistic Target Handling

At collision level the natural adjusted KSI contribution is:

```text
adjusted_ksi_collision = 1[collision_severity == fatal]
                       + collision_adjusted_severity_serious
```

Aggregated to link-year grain, the target becomes an expected KSI count, not an
integer count. That is acceptable for Poisson GLM-style fitting as a
quasi-likelihood / expected-count target, provided the report is explicit that
the response is expected KSI rather than observed integer KSI.

The EB layer is not a drop-in swap. `src/road_risk/model/eb_shrinkage.py`
currently consumes pooled `collision_count`, checks for observed counts, and
shrinks `predicted_xgb * n_years` toward `collision_count` using a global NB2
dispersion parameter. The current dispersion estimation in
`src/road_risk/model/eb_dispersion.py` is also built around observed
`collision_count`. A KSI version using probabilistic targets would need:

- a new expected-KSI target column at link-year grain;
- a decision on whether the model is estimating expected adjusted KSI collisions
  or integer latent KSI events;
- a re-derived EB variance/dispersion treatment, because NB2 observation noise
  for integer counts is not the same as uncertainty in summed record-level
  probabilities;
- revised validation language for top-k ranking, because observed zero KSI
  becomes expected KSI very close to zero, not a clean binary no-event signal.

The original sparsity concern improves only marginally. Expected counts soften
some hard zeros, but the underlying signal remains rare at link-year grain.

### 3.3 Diagnostic Re-Run Question

The adjusted columns are directly relevant to the Part A parking verdict. The
existing diagnostic explicitly says the 2016-2019 flag concentration is
consistent with staggered CRASH/COPA rollout and that DfT adjustment factors were
not applied. Because the local data now has all-year collision-level adjusted
severity, a defensible next diagnostic would rerun the same force/year
heterogeneity test using adjusted expected KSI.

The outcome is not knowable without that rerun. The adjustment should reduce the
reform-driven discontinuity, but two cautions keep this from immediately
unparking KSI:

- the existing diagnostic found residual heterogeneity outside a clean national
  transition window, including repeated Staffordshire flags and post-2020
  variation;
- DfT/ONS explicitly warn that force-level estimates and cross-force comparisons
  remain sensitive to modelling assumptions, especially where force-specific
  trends or limited IBRS experience matter.

So adjusted columns materially change feasibility, but they do not by themselves
prove that Part A would pass.

### 3.4 Effort Estimate

The most consistent path is the **medium path**, though nearer the lower end
because full adjusted-column coverage already exists locally.

Estimated credible effort: **3-4 weeks**.

- 2-3 days: build and audit adjusted expected KSI target in the snapped
  collision/link-year pipeline.
- 2-3 days: rerun Part A on adjusted force/year expected KSI and compare against
  the original unadjusted flags.
- 3-5 days: adapt GLM/XGBoost target construction and validation reports for
  expected KSI counts.
- 4-6 days: rework EB shrinkage assumptions for probabilistic expected counts,
  or explicitly defer EB from the first adjusted-KSI pass.
- 3-5 days: write methodology notes, caveats, and sensitivity checks, especially
  for link-year sparsity and force-level uncertainty.

This is not the quick path because EB is not a small target-name change and
because Part A may still fail after adjustment. It is not the slowest path
because local coverage is complete for 2015-2024 and lookup reconstruction is
not required.

## Part 4: Recommendation

**Choose option 2: tighten parking entry only.**

Adjusted severity columns exist locally for the entire 2015-2024 study window,
and they are DfT's own record-level probability adjustments, not an R-package
wrapper or external guess. That makes the KSI revisit condition more concrete:
the next defensible step is an adjusted Part A diagnostic, not a vague future
methodology dependency.

But the evidence does not justify unparking the KSI atlas today. No adjusted
force/year consistency test has been run; DfT warns that small/local uses and
force-level comparisons carry extra uncertainty; and ORR's EB layer currently
assumes observed integer counts, while adjusted KSI would be an expected-count
target. The underlying rarity of KSI at link-year grain also remains.

A tightened register condition could say, in substance:

> Reopen only after rerunning Part A using
> `fatal_indicator + collision_adjusted_severity_serious` as adjusted expected
> KSI and showing force/year consistency clears the pre-registered threshold; if
> Part B proceeds, specify whether EB is re-derived for expected counts or
> deferred from the KSI ranking.

That keeps the parking decision intact while replacing a broad external trigger
with the concrete local prerequisite now made possible by the data.
