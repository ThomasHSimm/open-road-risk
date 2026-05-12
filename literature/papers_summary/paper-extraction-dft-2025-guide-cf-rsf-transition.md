# Paper Extraction: Guide to Road Safety and Contributory Factors for Reported Road Casualties Great Britain

> **Note on template adaptation:** This is a methodological guidance document, not a research or modelling paper. Sections covering model architecture, engineered features, validation strategy, and transferability of methods are not applicable and have been replaced with sections more relevant to this document type: data quality mechanics, CF/RSF transition structure, per-force coverage, and implications for Open Road Risk feature engineering.

---

## 0. Extraction Run Metadata

- Extraction date: 2026-05-12
- Source PDF filename: Guide_to_road_safety_and_contributory_factors_for_reported_road_casualties_Great_Britain_-_GOV_UK.pdf
- Suggested Markdown filename: paper-extraction-dft-2025-guide-cf-rsf-transition.md
- AI tool used: Claude
- Model name, if visible: Claude Sonnet 4.6
- Model version, if visible: not stated
- Interface used: web chat
- Input type: PDF upload (rendered as text in context window)
- Output mode: downloadable .md file
- Was the full paper accessible to the model? yes
- Notes on access limitations: Embedded charts are described in text; chart image data is not extractable. Table 6a (per-force CF coverage 2015–2022) is truncated in the rendered version — later year columns are cut off. Table 7 (2024 force RSF status) appears complete.

---

## 1. Citation

- Title: Guide to Road Safety and Contributory Factors for Reported Road Casualties Great Britain
- Authors: Department for Transport (no individual authors named)
- Year: Updated 25 September 2025 (original publication date not stated; document updated annually)
- URL: https://www.gov.uk/government/publications/guide-to-contributory-factors-for-reported-road-casualty-statistics/guide-to-contributory-factors-for-reported-road-casualties-great-britain
- Country / region: Great Britain (England, Scotland, Wales)
- Status: Official DfT guidance document, updated alongside annual STATS19 release

---

## 2. Purpose and Scope

This is a methodological guidance document explaining the structure, limitations, and transition mechanics of the contributory factor (CF) and road safety factor (RSF) data fields within the STATS19 road collision dataset. It is aimed at analysts and data users, not at modellers or researchers.

Its value to Open Road Risk is as:
- a **data quality reference** documenting what CF and RSF fields mean, how they are recorded, and how reliable they are
- a **transition risk reference** documenting the structural break between CF and RSF recording from 2024 onwards
- a **per-force coverage reference** documenting which Yorkshire, NW England, and Midlands forces were using RSFs vs CFs in 2024

---

## 3. CF and RSF System Structure

### 3.1 What CFs and RSFs are

CFs and RSFs are fields recorded by the attending police officer at a collision scene. They indicate up to 6 factors the officer believes contributed to the collision. They are subjective officer judgements, not the result of formal investigation. The officer also records whether each factor was "very likely" or had only a "possible" link to the collision.

Key limitations stated explicitly in the document:
- Not all collisions are included: only those where police attended and recorded at least one CF or RSF. In 2024, this was 66% of all reported collisions.
- Factors can be assigned to vehicles, casualties, or uninjured pedestrians — one collision can have multiple factors across multiple road users.
- Factors should not be summed across collisions because one collision can be counted multiple times.
- Some factors (e.g. exceeding speed limit) may not be obvious at the scene and are subject to under-reporting.
- Subsequent investigation may change the recorded factors, but the STATS19 record is not typically updated.

### 3.2 CF structure

- 77 CFs grouped into 9 sections
- Collected from 2005; consistently recorded through to late 2023
- Sections: road environment, vehicle defects, driver/rider injudicious action, driver/rider error or reaction, driver/rider impairment or distraction, driver/rider behaviour or inexperience, driver/rider vision affected, pedestrian factors, special codes

### 3.3 RSF structure

- 37 RSFs grouped into 6 sections aligned to safe system pillars
- Sections: B (Behaviour or inexperience), D (Distraction or impairment), P (Non-motorised road users), R (Road), S (Speed), V (Vehicles)
- STATS19 review recommendation from 2018; CRASH system forces began recording RSFs from November 2023

### 3.4 CF coverage rate (collisions included in CF analysis, by severity)

Based on Table 3a (CF specification):

| Severity | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---|---|---|---|---|---|
| Fatal | 91% | 85% | 87% | 87% | 86% | 84% |
| Fatal or Serious (adjusted) | 86% | 82% | 82% | 81% | 80% | 79% |
| All collisions | 77% | 73% | 72% | 69% | 67% | 66% |

Based on Table 3b (RSF specification):

| Severity | 2023 | 2024 |
|---|---|---|
| Fatal | 97% | 99% |
| Fatal or Serious (adjusted) | 81% | 86% |
| All collisions | 61% | 70% |

**Important for Open Road Risk:** CF coverage for all collisions has been declining (77% in 2015 to ~66% by 2020). RSF coverage for all collisions is 70% in 2024. Approximately 30–34% of all collisions in any given year have no CF or RSF recorded. Any analysis using CF/RSF fields as features implicitly excludes or treats missing values for this subset.

### 3.5 CF coverage by road class (Table 4a, CF specification)

| Road class | 2015 | 2016 | 2022 |
|---|---|---|---|
| Motorways | 84% | 80% | ~77% |
| A Roads | 80% | 77% | ~69% |
| B Roads | 79% | 74% | ~69% |
| Other roads | 73% | 69% | ~62% |

Motorways have consistently higher CF coverage than minor roads. If Open Road Risk ever uses CF-derived features, minor road links will have a structurally higher missing rate than motorway links, which could bias any model using those features.

---

## 4. The CF→RSF Transition: Mechanics and Risks

### 4.1 Timeline

| Year | CF/RSF mix |
|---|---|
| Up to 2022 | 100% CFs |
| 2023 | ~97% CFs, ~3% RSFs |
| 2024 | ~69% CFs (converted to RSF categories), ~31% RSFs directly recorded |
| 2025 | Expected majority RSFs |
| 2026 | Expected most, but not all, RSFs |

### 4.2 Mapping approach

DfT has published a CF→RSF mapping table. The mapping is many-to-one (multiple CFs map to a single RSF). Key constraints:
- 16 CFs cannot be mapped to any individual RSF (e.g. CF 104 inadequate signs, CF 105 defective traffic signals, CF 108 road layout such as bend/hill/narrow road, CF 109 animal/object in carriageway). These can be mapped to the RSF section level only.
- The mapping was derived before any directly-recorded RSF data existed — it reflects theoretical alignment, not observed officer behaviour.
- Reverse mapping (RSF → CF) is not generally possible.

### 4.3 Observed step change in recording

DfT's September 2025 analysis shows that directly-recorded RSF data produces measurably different factor distributions from CF-converted data:

| RSF section | % collisions (2024, converted from CFs) | % collisions (2024, directly recorded as RSFs) | Relative change |
|---|---|---|---|
| Speed | 41% | 36% | 0.88 |
| Behaviour or inexperience | 63% | 75% | 1.18 |
| Distraction or impairment | 19% | 28% | 1.48 |
| Road | 16% | 22% | 1.40 |
| Non-motorised road users | 6% | 14% | 2.21 |
| Vehicles | 4% | 6% | 1.60 |

The document states explicitly: "the change in system appears to have led to a break in the time series for some factors." Tables RAS0704 to RAS0706 have been withdrawn pending further analysis. The "fatal 4" factsheet has been paused.

**Open Road Risk implication:** If the pipeline ever ingests STATS19 data from 2024 onwards and uses any CF-derived field as a feature (or contextual label), the step change in recording means 2024+ CF values are not comparable to 2015–2023 values. This is a structural break in any time-series use of those fields.

### 4.4 Average factors per collision

- CF system: ~1.9 factors per collision (converted)
- RSF system (directly recorded): ~2.5 factors per collision
- STATS19 review recommended 3–6 factors per collision; ~60% of directly-recorded RSF collisions meet this threshold

The increase in factors per collision under RSFs is relevant: it means individual RSF flags will be more common per collision in future data, not because more factors actually existed, but because reporting changed.

---

## 5. Per-Force RSF Status in 2024 (Table 7)

This is directly relevant to Open Road Risk's police force codes.

### Forces in Open Road Risk's study area (Yorkshire, NW England, NE England, Midlands)

| Police force | Open Road Risk force code | 2024 RSF data status |
|---|---|---|
| West Yorkshire | 13 | Some data collected as RSFs |
| South Yorkshire | 12 | All data collected as CFs |
| North Yorkshire | 14 (approx) | All data collected as CFs |
| Humberside | 16 (approx) | All data collected as CFs |
| Lancashire | 4 | Some data collected as RSFs |
| Merseyside | 5 (approx) | All data collected as CFs |
| Greater Manchester | 6 (approx) | Some data collected as RSFs |
| Cheshire | 7 (approx) | All data collected as CFs |
| Northumbria | — | All data collected as RSFs |
| Durham | — | All data collected as RSFs |
| West Midlands | — | Some data collected as RSFs |
| Staffordshire | — | Some data collected as RSFs |
| West Mercia | — | Some data collected as RSFs |
| Warwickshire | — | All data collected as CFs |
| Derbyshire | — | Some data collected as RSFs |
| Nottinghamshire | — | All data collected as RSFs |
| Leicestershire | — | All data collected as RSFs |
| Northamptonshire | — | All data collected as RSFs |

**Note:** Force code mapping is approximate; the document does not use numeric force codes. Open Road Risk should verify code↔force mapping against the STATS19 force lookup table.

**Key finding for 2024 STATS19 data:** Within the Yorkshire cluster, South Yorkshire, North Yorkshire, and Humberside recorded 100% CFs in 2024; West Yorkshire had partial RSF recording. Within NW England, Lancashire and Greater Manchester had partial RSF recording; Merseyside and Cheshire remained CF-only. This means that any 2024 STATS19 data ingested into Open Road Risk will have a mixed CF/RSF landscape across its own study area, even before considering forces outside the study area.

---

## 6. Data Access Constraints on CF/RSF Fields

RSF data is not available at record level in the standard STATS19 download or the Collision Analysis Tool (CAT). It is published only as aggregated tables (RAS07 series). Individual collision-level RSF data requires an end-user agreement application to DfT (roadacc.stats@dft.gov.uk).

CF data at record level is available in the standard STATS19 download (available from data.gov.uk), but the document notes it is treated as sensitive and that local authority breakdowns (RAS0706) have been paused during the CF→RSF transition.

**Open Road Risk implication:** If the pipeline currently uses STATS19 record-level CF fields (e.g. as contextual labels or diagnostic features), those fields are available in the download. Record-level RSF fields are not in the standard download. Future ingestion of 2024+ STATS19 data will not include record-level RSFs unless DfT releases them or a data agreement is in place.

---

## 7. DfT Guidance on Analysis Approach

DfT explicitly recommends (Section 6.1):
- Do not directly compare CF-converted data with directly-recorded RSF data to avoid implying trends that do not exist.
- For time-series analysis, use proportions of collisions assigned a given factor, not raw counts, because the reduced scope of CF collection means raw counts will artificially decline as RSF coverage grows.
- Treat directly-recorded RSF data with caution until more analysis is done.

---

## 8. Repo Actionability

**1.**
- Suggested repo action: Document the per-force CF/RSF status for 2024 in the repo's data quality notes. Specifically flag that South Yorkshire (12), North Yorkshire, and Humberside were 100% CF in 2024; West Yorkshire was partial RSF; and that several Midlands forces (Nottinghamshire, Leicestershire, Northamptonshire) were 100% RSF.
- Action type: documentation note
- Relevant stage: documentation / feature engineering
- Why: If CF-derived fields are ever used as features or diagnostic labels, their recording basis differs across the study area in 2024. This is not a model error but a data provenance issue that should be documented.
- Effort: low
- Risk if implemented badly: none — documentation only

**2.**
- Suggested repo action: Add a note to the STATS19 ingestion pipeline that CF fields from 2024 STATS19 data are not comparable to 2015–2023 CF fields for any force that transitioned to RSF recording in 2024. Flag the structural break explicitly in data provenance.
- Action type: documentation note
- Relevant stage: documentation / feature engineering
- Why: The document explicitly states a step change in factor recording under RSFs. Using CF fields in a time-series feature across the 2024 boundary is unreliable for transitioning forces.
- Effort: low
- Risk if implemented badly: if not flagged, any trend analysis using CF-derived features across 2024 will conflate the recording change with real collision factor trends

**3.**
- Suggested repo action: Check whether the pipeline currently ingests or uses any STATS19 CF fields (e.g. speed-related, road-related CFs) as features or contextual labels. If so, document the coverage rate (66–77% of collisions, lower for minor roads) and note that CF absence does not mean CF did not apply.
- Action type: diagnostic
- Relevant stage: feature engineering / documentation
- Why: The document confirms that 30–34% of collisions have no CF recorded in any given year, and minor road coverage is lower than motorway coverage. A CF field used as a binary feature would conflate "not recorded" with "not applicable."
- Effort: low
- Risk if implemented badly: low — diagnostic only

**4.**
- Suggested repo action: Note that record-level RSF data is not in the standard STATS19 download and requires a DfT data agreement. If the pipeline is extended to 2024+ data, do not assume RSF fields will be available from the standard open-data source.
- Action type: documentation note
- Relevant stage: documentation
- Why: The document explicitly states RSF data is not released at record level in the standard tools; only aggregated RAS07 tables are published.
- Effort: low
- Risk if implemented badly: none — documentation only

---

## 9. Query Tags

- STATS19-CF
- STATS19-RSF
- contributory-factors
- road-safety-factors
- CF-RSF-transition
- structural-break-2024
- police-force-coverage
- Yorkshire-force-codes
- data-quality
- STATS19-field-coverage
- missing-data-CF
- minor-road-CF-bias
- record-level-RSF-unavailable
- time-series-break
- DfT-guidance

---

## 10. Confidence and Gaps

- Overall confidence in extraction: high — guidance document with explicit tables and stated figures
- Important details not stated:
  - The exact force numeric codes are not in this document; Table 7 uses force names only. Force code↔name mapping must be verified against the STATS19 force lookup.
  - Table 6a (per-force CF coverage percentages 2015–2022) was truncated in the rendered PDF; later year columns were cut off and are not fully extractable here. The published tables (RAS07 series) should be checked for complete figures.
  - The document does not state what proportion of 2024 Open Road Risk study-area collisions specifically have CFs vs RSFs — that requires joining force coverage data to the STATS19 download.
- Parts needing manual checking:
  - Table 6a later-year columns (2021, 2022, 2023 per-force CF coverage)
  - The mapping table ODS file (linked but not in this document) — needed to assess which specific CFs map to which RSFs
  - Whether the standard STATS19 open-data download for 2024 includes any RSF fields or only CF fields
- Any likely ambiguity:
  - "Some data collected as RSFs" for forces like West Yorkshire and Lancashire means a portion of 2024 collisions use RSFs, but the document does not state the proportion for each force. The RAS07 tables or Table 6b (which was partially visible) would give this.
