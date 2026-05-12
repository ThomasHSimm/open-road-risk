# Paper Extraction: Reported Road Casualties Great Britain, Annual Report 2024

> **Note on template adaptation:** This is a descriptive statistics report, not a methodology or modelling paper. Sections covering model architecture, engineered features, validation strategy, and transferability of methods are not applicable and have been replaced with sections more relevant to this document type: baseline statistics, data quality caveats, and implications for Open Road Risk calibration and context.

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-12
- Source PDF filename: Reported_road_casualties_Great_Britain__annual_report__2024_-_GOV_UK.pdf
- Suggested Markdown filename: paper-extraction-dft-2025-reported-road-casualties-gb-2024.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: This is the summary report PDF. Full underlying data tables (RAS series) are published separately at gov.uk and are not included in this document.

---

## 1. Citation

- Title: Reported Road Casualties Great Britain, Annual Report: 2024
- Authors: Department for Transport (no individual authors named)
- Year: 2025 (published 25 September 2025; covers calendar year 2024 data)
- DOI or URL: https://www.gov.uk/government/statistics/reported-road-casualties-great-britain-annual-report-2024/reported-road-casualties-great-britain-annual-report-2024
- Country / region: Great Britain (England, Scotland, Wales; Northern Ireland reported separately)
- Status: Accredited Official Statistics (formerly National Statistics)

---

## 2. Purpose and Scope

This is an annual descriptive statistics release, not a research paper. It provides counts and rates of police-reported personal injury road collisions and casualties for 2024, broken down by severity, road user type, vehicle type, age, sex, road type, and contributing factors. It does not propose models, test hypotheses, or generate new methodology.

Its value to Open Road Risk is as:
- a **baseline reference** for national-level collision and casualty rates against which link-level estimates can be contextualised,
- a **data quality reference** documenting known STATS19 limitations,
- a **denominator source** for exposure rates (billion vehicle miles by road type).

---

## 3. Key Headline Statistics for 2024 (Great Britain)

### 3.1 Absolute counts

| Metric | 2024 value | % change from 2023 | % change from 2014 |
|---|---|---|---|
| Fatalities | 1,602 | -1% | -10% |
| KSI casualties (adjusted) | 29,467 | -1% | -14% |
| Seriously injured (adjusted) | 27,865 | 0% | -15% |
| All casualties | 128,272 | -4% | -34% |
| Billion vehicle miles | 340 | +2% | +7% |

### 3.2 Rates per billion vehicle miles

| Metric | 2024 value | % change from 2023 | % change from 2014 |
|---|---|---|---|
| Fatalities per bvm | 4.7 | -3% | -15% |
| KSI per bvm | 86.7 | -2% | -20% |
| All casualties per bvm | 377.6 | -5% | -38% |

### 3.3 By road type (2024)

| Road type | Fatal share | All casualty share | Traffic share | Fatalities per bvm | All casualties per bvm |
|---|---|---|---|---|---|
| Motorways | 6% | 4% | 21% | 1.3 | 72 |
| Rural roads | 60% | 34% | 45% | 6.3 | 287 |
| Urban roads | 35% | 62% | 35% | 4.7 | 675 |

The rural/urban/motorway split is the most directly relevant breakdown for Open Road Risk's road-type stratification.

### 3.4 By road user type (fatalities, 2024)

| Road user | Fatalities | % change from 2023 | Fatality rate per bvm |
|---|---|---|---|
| Car occupants | 692 | -5% | 2.7 |
| Pedestrians | 409 | +1% | 26.4 (per billion miles walked) |
| Motorcyclists | 340 | +8% | 115.2 |
| Pedal cyclists | 82 | -6% | 23.3 |
| LGV occupants | 32 | -16% | 0.5 |
| HGV occupants | 17 | +21% | 1.0 |

Motorcyclist fatality rate (115.2 per bvm) is an order of magnitude above car occupants (2.7). This is relevant if Open Road Risk models link-level risk by road user mix.

### 3.5 Contributing factors (fatal collisions, 2024)

Based on RSF (Road Safety Factors) system — note only ~75% of 2024 collisions were RSF-coded natively; the remainder were converted from the old contributory factor system. Results below are for the CF-converted subset only (consistent with prior years):

| RSF section | % of fatal collisions with factor recorded |
|---|---|
| Speed | 59% |
| Behaviour or inexperience | 52% |
| Distraction or impairment | 34% |
| Road | 13% |
| Non-motorised road users | 9% |
| Vehicles | 3% |

### 3.6 Deprivation (England only, 2024)

Casualties are disproportionately concentrated in more deprived areas. The most deprived IMD decile accounts for 11.8% of casualties; the least deprived accounts for 6.8% — a 4.9 percentage point gap. Open Road Risk already includes IMD deprivation deciles as a candidate feature; this provides national-level context supporting its inclusion.

---

## 4. Data Quality Caveats Relevant to Open Road Risk

These are stated explicitly in the report and are directly relevant to the pipeline.

**Under-reporting of non-fatal casualties:** The report notes that non-fatal (particularly slight) casualties are substantially under-reported to police. Hospital, survey, and compensation claims data all indicate higher totals than STATS19. This is a known and documented limitation — Open Road Risk's collision outcome is also police-reported injury collisions only, so the same caveat applies.

**Severity adjustment:** Figures for serious and slight injuries are adjusted to account for police forces changing to injury-based reporting systems from 2016 onwards. The adjustment model is maintained by ONS Methodology Advisory Service. Raw unadjusted counts and adjusted counts differ, particularly for serious injuries. Open Road Risk should use adjusted figures if comparing to national benchmarks.

**Police force data quality issues:** Some police forces in previous years had recording errors. The report notes this is unlikely to affect national totals but cautions against sub-national breakdowns by police force area. Relevant to Open Road Risk given its use of police force codes 12/13/14/16 for Yorkshire and 4–7 for NW England.

**Online self-reporting:** The introduction of online self-reporting (Single Online Home project) is expected to increase reported slight casualties over time, potentially creating a structural break in the slight casualty trend that is unrelated to actual road safety changes.

**RSF transition (2024 onward):** A new Road Safety Factors coding system replaced the old Contributory Factors system. In 2024, only ~25% of collisions were natively recorded as RSFs; the remainder were converted. The report warns there is a step change in which factors are recorded under RSFs vs CFs, meaning RSF trends pre- and post-transition are not directly comparable. This is a documentation risk if Open Road Risk ever uses contributory factor fields from STATS19 as features.

---

## 5. Specific Numbers Useful for Open Road Risk Calibration

### National fatality rate benchmark
4.7 fatalities per billion vehicle miles (2024). Equivalent to 0.0047 fatalities per million vehicle miles, or approximately 0.0000047 per vehicle mile. This is a useful sanity check for Stage 2 model outputs.

### Rural road overrepresentation
Rural roads account for 45% of traffic but 60% of fatalities — a fatality rate of 6.3 per bvm vs 4.7 on urban roads and 1.3 on motorways. This differential is large and well-established. If Open Road Risk's Stage 2 model does not adequately separate rural vs urban vs motorway risk, it will conflate these structurally different risk profiles.

### Motorway underrepresentation
Motorways carry 21% of traffic but account for only 6% of fatalities and 4% of all casualties. The report confirms the known phenomenon noted in Open Road Risk's own model dossier (motorway overfitting concern). The national data supports treating motorways as a structurally distinct facility family.

### Motorcyclist rate disparity
At 115.2 fatalities per bvm, motorcyclists face a risk ~43x higher than car occupants (2.7 per bvm). If Open Road Risk links are used by mixed road users, this differential is large enough to matter for any severity-weighted outputs.

---

## 6. What This Report Does Not Provide

To avoid over-interpreting the document:

- No link-level or segment-level data. All statistics are at national or road-type aggregate level.
- No AADT or traffic count methodology. Vehicle miles figures come from DfT Road Traffic Statistics, not AADF count points.
- No spatial breakdown below road type (urban/rural/motorway). Police force breakdowns exist in the separate RAS04 tables, not in this report.
- No modelling, SPF, or predictive methodology.
- No data on collision frequency distribution across links (i.e. how many links have zero, one, two collisions — which is what Open Road Risk needs for model design).
- Yorkshire/NW/Midlands-specific rates are not in this report; they would be in RAS04 tables.

---

## 7. Repo Actionability

**1.**
- Suggested repo action: Add a documentation note recording the 2024 national baseline rates (4.7 fatalities per bvm, 86.7 KSI per bvm, 377.6 all casualties per bvm) as a sanity-check reference for Stage 2 model outputs.
- Action type: documentation note
- Relevant stage: Stage 2 / documentation
- Why: Provides an official national denominator against which link-level predictions can be checked for plausibility. If aggregate predicted risk across all Open Road Risk links (summed and normalised by AADT × length) diverges substantially from the national rate, that is a calibration diagnostic signal.
- Effort: low
- Risk if implemented badly: none — documentation only

**2.**
- Suggested repo action: Add a note documenting that Open Road Risk's STATS19 collision outcome inherits the police under-reporting limitation for non-fatal casualties, and that slight casualties are particularly affected. Reference the DfT severity adjustment guidance for context.
- Action type: documentation note
- Relevant stage: documentation / Stage 2
- Why: The report explicitly confirms that non-fatal casualties are substantially under-reported. This is a known limitation but worth formally documenting in the repo as provenance.
- Effort: low
- Risk if implemented badly: none

**3.**
- Suggested repo action: Cross-check the Stage 2 model's road-type risk differentials against the national figures (motorway 1.3 / rural 6.3 / urban 4.7 fatalities per bvm). If the model's facility-family split does not reproduce approximately this ordering, investigate whether the AADT offset or road classification features are functioning correctly.
- Action type: diagnostic
- Relevant stage: Stage 2 / validation
- Why: The rural/urban/motorway differential is large, well-established, and nationally confirmed. It is a basic sanity check for any road risk model using STATS19 data.
- Effort: low-medium
- Risk if implemented badly: low — diagnostic only; findings inform whether road type is being handled correctly

**4.**
- Suggested repo action: Document the RSF/CF transition risk in STATS19 data from 2024 onwards. If Open Road Risk's data pipeline eventually ingests 2024 STATS19 data, contributory factor fields will have a structural break that affects comparability with 2015–2023 data.
- Action type: documentation note
- Relevant stage: documentation / feature engineering
- Why: The report explicitly warns that RSF-coded collisions show a step change in which factors are recorded relative to CF-converted collisions. Using CF-derived features across the 2024 transition year without acknowledging this would introduce a spurious trend.
- Effort: low
- Risk if implemented badly: if not flagged and the pipeline later uses CF fields, trend analyses across the 2024 boundary would be unreliable

---

## 8. Query Tags

- STATS19-2024
- national-baseline-rates
- fatalities-per-billion-vehicle-miles
- rural-urban-motorway-differential
- severity-adjustment
- KSI
- road-user-type
- under-reporting
- IMD-deprivation
- RSF-CF-transition
- contributory-factors
- police-force-data-quality
- UK-official-statistics
- DfT
- exposure-rates
- facility-family-context

---

## 9. Confidence and Gaps

- Overall confidence in extraction: high — this is a straightforward statistics report; figures are taken directly from the tables
- Important details not stated in this report:
  - Sub-national breakdowns (police force, local authority, region) are in separate RAS04 tables, not included here
  - Yorkshire/NW/Midlands-specific rates are not in this document
  - Link-level or segment-level distributional statistics (zero-collision rate, mean collisions per link) are not published anywhere in STATS19 outputs
  - The severity adjustment model parameters are in separate DfT guidance, not here
- Parts needing manual checking:
  - The RSF/CF transition section (Section 9.1) is somewhat compressed; the separate road safety factors data collection report should be checked before using CF fields from 2024 STATS19 data
  - The online self-reporting impact analysis (referenced but not reproduced) should be checked if slight casualty trends matter for the pipeline
- Any likely ambiguity:
  - "Adjusted" serious and slight injury figures are used throughout. If Open Road Risk's STATS19 pipeline uses raw (unadjusted) severity fields, the national benchmark figures in this report are not directly comparable. Clarify which severity field version the pipeline ingests.
