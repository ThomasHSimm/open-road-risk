# Paper Extraction: Road Safety Factors — Initial Analysis

> **Note on template adaptation:** This is a DfT official statistics analysis document, not a research or modelling paper. Sections covering model architecture, engineered features, validation strategy, and transferability of methods are not applicable. The document provides: the CF→RSF mapping structure, illustrative analysis of factor distributions under the two systems, and early data on directly-recorded RSFs. Sections are adapted accordingly.

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-12
- Source PDF filename: Road_safety_factors__initial_analysis_-_GOV_UK.pdf
- Suggested Markdown filename: paper-extraction-dft-2024-rsf-initial-analysis.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered as text in context window)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Figure 1 (Sankey diagram of CF→RSF mapping flows) is described in text but the image itself is not extractable. Chart images (Charts 1–4) are rendered as data tables in the text, which are extractable.

---

## 1. Citation

- Title: Road Safety Factors: Initial Analysis
- Authors: Department for Transport (no individual authors named)
- Year: Published 30 May 2024
- URL: https://www.gov.uk/government/statistics/road-safety-factors-initial-analysis/road-safety-factors-initial-analysis
- Country / region: Great Britain
- Status: Official Statistics

---

## 2. Purpose and Scope

This document analyses the transition from STATS19 contributory factors (CFs) to road safety factors (RSFs). It covers:
- The structural differences between the CF and RSF categorisation systems
- An illustrative mapping analysis using 2022 fatal collision data
- Early data from directly-recorded RSFs in late 2023

Its value to Open Road Risk is as:
- a **provenance reference** for understanding what the RSF categories mean and how they relate to CFs
- a **quantitative reference** for the distribution of factors under both systems in fatal collisions
- a **risk documentation** source confirming that CF→RSF mapping introduces categorical reclassification, not just relabelling

---

## 3. RSF Category Structure

| RSF code | RSF category name | Safe system pillar alignment |
|---|---|---|
| B | Behaviour or inexperience | Safer road users |
| D | Distraction or impairment | Safer road users |
| P | Non-motorised road users (pedestrian, cyclist, horse rider, PPT) | Safer road users |
| R | Road | Safer roads and roadsides |
| S | Speed | Safer speeds |
| V | Vehicles | Safer vehicles |

Total RSFs: 37 (reduced from 79 CFs).

Key structural change: In the CF system, equivalent behaviours for drivers and pedestrians were separate factors (e.g. CF 405 "driver failed to look properly" vs CF 802 "pedestrian failed to look properly"). In RSFs, these are merged (e.g. B4 "ineffective observation" applies to all road user types). The P category now covers only factors specific to non-motorised road users.

---

## 4. CF→RSF Mapping: Quantitative Distribution (Fatal Collisions, Great Britain 2022)

### 4.1 By RSF section (mapped from CFs)

Source: Chart 1

| RSF section | % of fatal collisions with factor assigned |
|---|---|
| S: Speed | 56% |
| B: Behaviour or inexperience | 45% |
| D: Distraction or impairment | 34% |
| R: Road | 11% |
| P: Non-motorised road users | 8% |
| X: Not coded | 6% |
| V: Vehicles | 4% |

### 4.2 By CF section (original recording, same data)

Source: Chart 2

| CF section | % of fatal collisions with factor assigned |
|---|---|
| 400: Driver/rider error or reaction | 56% |
| 300: Injudicious action | 29% |
| 500: Impairment or distraction | 29% |
| 600: Behaviour or inexperience | 28% |
| 800: Pedestrian only | 15% |
| 100: Road environment | 7% |
| 900: Special codes | 7% |
| 700: Vision affected by external factors | 6% |
| 200: Vehicle defects | 2% |

**Key reclassification effect:** Speed (RSF-S) becomes the single largest category at 56%, substantially higher than its closest CF equivalent (CF 306 "exceeding speed limit" was around 19%). This is because:
- CF 410 "loss of control" (24% of fatal collisions) maps to S
- CF 602 "driver/rider careless, reckless or in a hurry" (21%) maps to S
- CF 601 "aggressive driving" (8%) maps to S

These were previously distributed across CF sections 400 and 600. The reclassification is not a change in road safety; it is a categorical restructuring.

**Open Road Risk implication:** Any prior analysis or literature citing "speed as a contributory factor in X% of fatal collisions" based on CFs is not directly comparable to RSF speed figures. The apparent prominence of speed under RSFs is partly an artefact of the broader RSF-S definition.

### 4.3 Top 10 individual RSFs (mapped from CFs, fatal collisions, 2022)

Source: Chart 3

| RSF | Description | % of fatal collisions |
|---|---|---|
| B4 | Ineffective observation (driver, rider, or pedestrian) | 32% |
| S2 | Driver/rider travelling too fast for conditions (incl. loss of control/swerving) | 30% |
| S4 | Driver/rider being aggressive, dangerous, or reckless | 26% |
| S1 | Driver/rider exceeding speed limit | 19% |
| D1 | Affected by alcohol | 13% |
| B3 | Driver/rider overshot junction or poor turn/manoeuvre | 12% |
| D5 | Illness or disability | 10% |
| D2 | Affected by drugs | 7% |
| D7 | Distraction to driver/rider from inside/outside/on vehicle | 6% |
| B1 | Driver/rider illegal turn/direction or failed to comply with sign/signal | 4% |

### 4.4 Top 10 individual CFs (original recording, fatal collisions, 2022)

Source: Chart 4

| CF code | Description | % of fatal collisions |
|---|---|---|
| 410 | Loss of control | 24% |
| 405 | Driver/rider failed to look properly | 23% |
| 602 | Driver/rider careless, reckless or in a hurry | 21% |
| 306 | Exceeding speed limit | 19% |
| 406 | Driver/rider failed to judge other person's path or speed | 11% |
| 403 | Poor turn or manoeuvre | 11% |
| 501 | Driver/rider impaired by alcohol | 10% |
| 307 | Travelling too fast for conditions | 8% |
| 505 | Driver/rider illness or disability | 8% |
| 601 | Aggressive driving | 8% |

---

## 5. CFs That Cannot Be Mapped to Individual RSFs

Source: Table 2. These 16 CFs have no direct RSF equivalent and can only be assigned to an RSF section at most.

| CF code | CF label | RSF section assignment |
|---|---|---|
| 104 | Inadequate or masked signs or road markings | Road |
| 105 | Defective traffic signals | Road |
| 106 | Traffic calming (road humps, chicane) | Road |
| 107 | Temporary road layout (contraflow) | Road |
| 108 | Road layout (bend, hill, narrow road) | Road |
| 109 | Animal or object in carriageway | Road |
| 205 | Defective or missing mirrors | Vehicles |
| 309 | Vehicle travelling along pavement | Behaviour or inexperience |
| 402 | Junction restart (moving off at junction) | Behaviour or inexperience |
| 404 | Failed to signal or misleading signal | Behaviour or inexperience |
| 709 | Visor or windscreen dirty/scratched/frosted | Vehicles |
| 801 | Crossing road masked by stationary/parked vehicle | Non-motorised road users |
| 901 | Stolen vehicle | Speed |
| 903 | Emergency vehicle on a call | Distraction or impairment |
| 999 | Other | Not coded |

**Open Road Risk implication:** CF 108 (road layout: bend, hill, narrow road) and CF 104 (inadequate signs/markings) are the CFs most directly related to road infrastructure features that Open Road Risk models. Both are unmappable to individual RSFs and collapse into the R (Road) category only. Any use of these specific CFs as collision context would be lost in the RSF system. This is documented here as a data scope limitation, not a modelling recommendation.

---

## 6. Early RSF Direct Recording Data (Late 2023)

Approximately 2,300 collisions in late 2023 had RSFs directly recorded. Findings:
- Average 2.6 RSFs per collision vs ~2 CFs per collision in comparable data
- ~two-thirds of directly-recorded RSF collisions had 3 or more factors (aligned to the STATS19 review recommendation of 3–6 factors)
- The document states it is "too early to draw any firm conclusions" from this sample

This was a November–December 2023 subset from CRASH-system forces only. It is not representative of the 2024 full year.

---

## 7. DfT Planned Approach

- 2023 statistics (published September 2024): RSF tables (mapped from CFs) published alongside CF tables
- 2024 statistics (published September 2025): RSFs used as default presentation; CF historic tables retained for reference; CF data likely discontinued beyond 2023 in terms of active updates
- 2025 statistics: expecting RSFs to cover a majority of data directly

---

## 8. Repo Actionability

**1.**
- Suggested repo action: Add a documentation note recording the CF→RSF category mapping, specifically flagging that CF 108 (road layout) and CF 104 (inadequate signs) — the CFs most relevant to road infrastructure features — are unmappable to individual RSFs. If the pipeline ever uses these CF fields as collision-context labels, their coverage terminates effectively at 2023.
- Action type: documentation note
- Relevant stage: documentation / feature engineering
- Why: These CFs cover road geometry and signing features that are directly relevant to Open Road Risk's road-context modelling. Losing them in the RSF transition is a data scope reduction, not merely a relabelling.
- Effort: low
- Risk if implemented badly: none — documentation only

**2.**
- Suggested repo action: Document that the "speed" RSF category (S) is not comparable to the old CF 306/307 speed factors and should not be used as a like-for-like replacement in any time-series analysis. The RSF-S category is substantially broader, incorporating loss of control, aggressive driving, and reckless behaviour that were previously in CF sections 400 and 600.
- Action type: documentation note
- Relevant stage: documentation
- Why: The document explicitly demonstrates this reclassification: speed-attributed collisions jump from ~19% (CF 306 only) to 56% (RSF-S) for fatal collisions due to categorical restructuring, not real change. Treating RSF-S as equivalent to CF 306/307 would be analytically incorrect.
- Effort: low
- Risk if implemented badly: if not documented, any contextual analysis of "speed-related" collisions in STATS19 will produce a spurious trend at the CF/RSF transition.

**3.**
- Suggested repo action: Note in the data quality documentation that CF 108 (road layout: bend, hill, narrow road) existed as a recorded field in STATS19 until ~2023. If a future EDA page examines collision-level context, this field provides a data-quality-limited but available signal for geometry-related collisions in the 2015–2023 window. Coverage is partial (see CF guide for force-level rates).
- Action type: documentation note
- Relevant stage: documentation / EDA
- Why: CF 108 is the closest STATS19 field to road geometry context. It is imperfect and subjectively assigned, but it exists and may be informative as a diagnostic cross-check against Open Road Risk's curvature/grade features.
- Effort: low
- Risk if implemented badly: low if treated as a diagnostic signal only, not a model feature

---

## 9. Query Tags

- STATS19-RSF
- STATS19-CF
- CF-RSF-mapping
- road-layout-CF108
- speed-RSF-reclassification
- fatal-collision-factors
- contributory-factors-distribution
- RSF-category-structure
- structural-break-2024
- data-scope-limitation
- DfT-official-statistics
- CF-unmappable
- time-series-comparability

---

## 10. Confidence and Gaps

- Overall confidence in extraction: high — official statistics document with explicit tables; figures taken directly
- Important details not stated:
  - The full RSF→individual factor list (37 factors) is in a linked ODS spreadsheet, not in this document. Individual factor codes (e.g. B4, S2) are referenced but the complete list is not reproduced here.
  - The mapping table ODS file is linked but not accessible in this extraction. It would be needed to fully assess which specific CFs map to which RSFs beyond what is discussed in the text.
  - Analysis is restricted to fatal collisions for the illustrative section; it is not stated whether the same distributions hold for serious or slight collisions.
- Parts needing manual checking:
  - The ODS mapping table (linked in document) for the complete CF→RSF mapping
  - Whether the 2024 RSF initial analysis (updated September 2025 in the guide document) supersedes or extends the figures in this May 2024 publication
- Any likely ambiguity:
  - The document is dated May 2024 and covers only data to 2022 for the main analysis, with 2023 late-year RSF data as early indicator. The updated CF/RSF guide (September 2025) contains more recent 2024 data and should be treated as the more current reference for transition status.
