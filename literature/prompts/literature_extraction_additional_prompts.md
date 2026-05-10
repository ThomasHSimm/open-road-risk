# Literature Extraction Additional Prompts

This file contains companion prompts for use after the main extraction prompt.

Use these when checking, reconciling, or indexing AI-generated literature extractions.

The main extraction prompt is:

`road_safety_literature_extraction_prompt.md`

This file is self-contained. The full Open Road Risk project context is included below in the Project Context section. You do not need to attach the main extraction prompt when using prompts from this file, unless you specifically want the AI to follow the full extraction schema (e.g. during reconciliation).

---

# Project Context

This section is the full Open Road Risk project dossier. Include it when attaching this file to any AI session, so the AI has the context it needs without requiring the main extraction prompt.

## Aim

I am building **Open Road Risk**, an open-source road safety pipeline for Northern and Central England.

The project estimates exposure-adjusted road collision risk for OS Open Roads links.

The purpose is to identify road links where observed injury collisions are unusually high relative to traffic exposure and road/network context.

This is an exploratory decision-support and safety-performance modelling project, not a causal proof that any individual road feature causes collisions.

## Geography, Time, and Scale

- Study area: Yorkshire, North West England, North East England, Midlands, and parts of East England.
- Time range: 2015–2024.
- Network: approximately 2,167,557 OS Open Roads links.
- Main modelling table: road link × year.
- Approximate modelling scale: around 21.7 million link-year rows.
- Collisions are rare: around 1–2% of link-years have one or more recorded injury collision.

## Main Data Sources

### Collision Data

- STATS19-style police-reported injury collision records.
- Damage-only collisions are not included.
- Collisions are spatially snapped to OS Open Roads links.
- Current snap rate is high, around 99.8%, but snapping quality and ambiguous matches remain methodological concerns.
- Collision-derived context columns are treated as diagnostics and excluded from Stage 2 model features to avoid post-event leakage.

### Road Network

- OS Open Roads link geometry.
- Segment definition currently follows OS Open Roads links, not fixed-length 100m segmentation.
- Features include road classification, form of way, trunk/primary indicators, link length, and derived network features.

### Traffic Exposure

- AADF-style annual average daily flow data.
- Stage 1a trains only on directly counted AADF rows, avoiding DfT-interpolated targets.
- AADT is estimated for all road links using road/network/context features.
- Exposure uncertainty is a central concern.

### Time-of-Day Traffic Profiles

- WebTRIS-style National Highways sensor reports are used to learn peak/pre-peak/off-peak time fractions.
- These profiles currently produce a separate output for temporal analysis and future exposure weighting.
- They are not currently part of the Stage 2 collision feature set.

### Contextual / Engineered Features

Current or candidate features include:

- road classification,
- form of way,
- trunk/primary status,
- link length,
- estimated AADT,
- HGV proportion,
- peak/off-peak fractions,
- latitude/longitude,
- degree and betweenness centrality,
- distance to major roads,
- population density,
- OSM speed limits, lanes, lighting, surface,
- IMD deprivation deciles,
- rural/urban classification,
- curvature,
- grade from OS Terrain 50,
- possible future features such as junction complexity, crossings, bus stops, road width, and bridge/tunnel flags.

OSM feature coverage is uneven. Speed limit has usable imputed coverage, but lanes, lighting, and surface are sparse.

## Current Modelling Structure

### Stage 1a — AADT Estimator

- Predicts AADT for every road link.
- Trained on counted-only AADF rows.
- Uses gradient boosting style regression.
- Uses grouped validation by count point.
- Current reported CV R² is approximately 0.83, but spatial generalisation and feature consistency remain important concerns.

### Stage 1b — Time-Zone Profile Model

- Learns within-day traffic profile fractions from WebTRIS site-year data.
- Uses grouped validation by WebTRIS site.
- Currently separate from the Stage 2 collision model.

### Stage 2 — Collision Risk Model

- Main unit: road link-year.
- Outcome: observed injury collision count.
- Uses an exposure offset based on:

`log(AADT × link_length_km × 365 / 1e6)`

- Current model family includes:
  - Poisson GLM for interpretable coefficients and residual diagnostics.
  - XGBoost for risk ranking / predictive benchmark.
- XGBoost currently drives the production risk percentile.
- GLM residuals are used diagnostically.
- Grouped split by road link is used to reduce leakage across repeated years for the same road link.
- Empirical Bayes shrinkage and facility-family split models exist as diagnostic variants, not the main production output.

## Important Methodological Guardrails

When assessing papers, pay special attention to:

1. Whether exposure is handled as an offset, denominator, feature, latent quantity, or ignored.
2. Whether the paper accounts for sparse or estimated traffic counts.
3. Whether validation uses spatial, temporal, grouped, or random splits.
4. Whether the method can handle zero-heavy collision counts.
5. Whether the method relies on post-event variables that would leak collision information.
6. Whether the spatial unit of analysis is compatible with OS Open Roads link geometry.
7. Whether severity is modelled separately or combined with frequency.
8. Whether the method requires data not realistically available in my open-data UK pipeline.
9. Whether reported metrics are in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, or externally validated.
10. Whether a metric supports predictive generalisation or only model comparison / goodness of fit.
11. Whether the paper's study scale is compatible with Open Road Risk's scale.
12. Whether a paper finding supports a diagnostic, a small pilot, or a production change.

## Transferability Rules

A method is **highly transferable** if it can probably be implemented using:

- STATS19-style injury collision data,
- OS Open Roads geometry,
- AADF/WebTRIS-style sparse traffic counts,
- OSM,
- census/geodemographic data,
- OS Terrain 50,
- standard Python geospatial and machine-learning tooling.

A method has **low transferability** if it requires:

- complete observed traffic counts for every road segment,
- lane-level traffic engineering data,
- connected-vehicle trajectories,
- floating-car speed traces,
- detailed signal timings,
- commercial inspection scores,
- proprietary road inventory surveys,
- manual road safety audits at national scale.

For partial matches, say so explicitly. For example:

- The mathematical exposure-offset structure may be highly transferable.
- The paper's particular traffic-flow data source may have low or medium transferability.
- A spatial model may be conceptually useful but computationally unrealistic at 2.1 million links.

Do not collapse these into a single overconfident judgement.

## Evidence Scope Rules

When stating findings, preserve the scope of the paper.

Do not generalise from one case study to all road networks.

Use cautious phrasing such as:

- "In this case study..."
- "The paper provides evidence that..."
- "This suggests..."
- "This may support..."
- "This does not prove..."

Avoid strong phrasing such as:

- "proves",
- "validates the need",
- "should be prioritised",
- "is robust generally",
- "demonstrates this will work in my repo"

Do not generalise to Open Road Risk unless the paper provides broad evidence across multiple settings and compatible data.

## Repo Action Discipline

For repo actions, prefer the least disruptive useful action.

Use this order:

1. documentation note,
2. diagnostic,
3. small pilot,
4. comparison against current baseline,
5. candidate feature,
6. candidate model extension,
7. production change.

Do not recommend production changes directly from a single paper unless the evidence is strong, transferable, and scale-compatible.

If a feature or method is already part of Open Road Risk, suggest testing, validating, documenting, or comparing it rather than adding it.

## Access Limitation

Do not assume access to the repository code.

Use this project dossier as the full description of the pipeline unless extra files are provided.

If a judgement depends on implementation details not provided here, say so explicitly.

---

# 1. Cross-Audit Prompt

Use this after one AI has produced an extraction.

Attach:
- the original paper PDF,
- the extraction to audit.

The Open Road Risk project context is in the Project Context section of this file. You do not need to attach the main extraction prompt separately.

Do not ask the auditing AI to rewrite the whole extraction. Its job is to check evidence quality.

## Prompt

You are auditing another AI's extraction of the attached academic paper.

Inputs:
1. The original paper PDF.
2. A Markdown extraction produced by another AI.
3. The Open Road Risk project context (see Project Context section of this file).

Task:
Check the extraction against the paper.

The paper PDF is the source of truth.

Do not rewrite the whole extraction unless explicitly asked.

Return only the following sections.

## Unsupported Claims

Claims in the extraction that are not supported by the paper.

| Section | Claim | Why unsupported | Corrected version or remove? | Evidence/page |
|---|---|---|---|---|

## Missing Important Details

Important methodological details present in the paper but missing from the extraction.

| Section | Missing detail | Why it matters | Evidence/page |
|---|---|---|---|

## Overstated Transferability

Places where the extraction says a method transfers to Open Road Risk but the evidence is weak.

| Claim | Problem | Better judgement | Evidence/page |
|---|---|---|---|

## Fields That Should Be `Not stated`

Fields where the extraction inferred information that the paper does not clearly state.

| Section | Current text | Replace with | Reason |
|---|---|---|---|

## Methodological Risks Missed

Risks the extraction failed to flag.

Consider:
- exposure uncertainty,
- rare collision counts,
- spatial leakage,
- temporal leakage,
- post-event variable leakage,
- segmentation mismatch,
- unobserved traffic volume,
- proprietary or unavailable data.

| Risk | Why it matters | Evidence/page |
|---|---|---|

## Final Audit Verdict

- Overall reliability of extraction: high / medium / low
- Main corrections needed:
- Whether this extraction is safe to use for metadata search: yes / yes with caveats / no
- Short reason:

Important:
- Do not wrap the whole answer in a code block.
- Do not add general commentary.
- Be conservative.
- If a claim cannot be verified, flag it.

---

# 2. Reconciliation / In-Place Edit Prompt

This prompt has two modes depending on how many extractions you have.

---

## Mode A — Two Extractions: Produce `final.md`

Use this when you have two independent extractions of the same paper, with or without prior audit notes.

Attach:
- the original paper PDF,
- both extractions,
- audit notes if available (omit if not).

The output is a new combined `final.md`. Do not edit either input extraction.

### Prompt

You are producing a final methodological metadata extraction for one academic paper.

Inputs:
1. The original paper PDF.
2. Two independent AI extractions of the same paper.
3. Audit notes identifying unsupported claims, missing details, and overstatements (if provided; if not, work directly from the PDF and the two extractions).
4. The Open Road Risk project context (see Project Context section of this file).

Task:
Create one final Markdown extraction using the same section schema as the main extraction prompt (`road_safety_literature_extraction_prompt.md`).

Rules:
- The paper PDF is the source of truth.
- If the two extractions agree and the paper supports the claim, include it.
- If the two extractions disagree, use the version best supported by the paper.
- If neither version is clearly supported by the paper, write `Not stated`.
- Do not include a claim just because both AIs included it — consensus is not evidence.
- Remove unsupported transferability claims.
- Keep evidence quotes or page references where possible.
- Preserve useful disagreement as a caveat where relevant, e.g. "Extraction A states X; Extraction B states Y; paper text is ambiguous."
- Prefer conservative, searchable metadata over polished prose.
- Flag any section where the paper is unclear or inaccessible.

Output requirement:
- If your interface supports file creation, create a `.md` file named `final.md`.
- If file creation is not supported, output the entire extraction inside one outer raw Markdown copy block using four backticks, starting with `RAW_MARKDOWN_START` and ending with `RAW_MARKDOWN_END`.
- Do not add commentary before or after the final extraction.

---

## Mode B — One Extraction: Edit In Place

Use this when you have only one extraction and want to improve it directly, without producing a separate file.

Attach:
- the original paper PDF,
- the single extraction.

The output is a corrected version of the same extraction, using the same section schema. Do not produce a new separate document — edit the extraction you were given.

### Prompt

You are improving a single AI extraction of the attached academic paper.

Inputs:
1. The original paper PDF.
2. One Markdown extraction to improve.
3. The Open Road Risk project context (see Project Context section of this file).

Task:
Edit the extraction directly. Return a corrected version using the same section schema as the original.

Rules:
- The paper PDF is the source of truth.
- Correct any unsupported claims. Replace with the paper's actual text, or write `Not stated`.
- Add missing methodological details that are present in the paper but absent from the extraction.
- Downgrade or remove transferability claims that are not justified by the paper's data and methods compared against Open Road Risk's data sources.
- Change fields to `Not stated` where the extraction inferred information the paper does not clearly state.
- Add any methodological risks the extraction missed. Consider: exposure uncertainty, rare collision counts, spatial leakage, temporal leakage, post-event variable leakage, segmentation mismatch, unobserved traffic volume, proprietary or unavailable data.
- Add evidence quotes or page references where they are missing and can be found in the paper.
- Do not add claims that are not in the paper.
- Do not rewrite sections that are already accurate and well-supported.
- Prefer conservative, searchable metadata over polished prose.

Output requirement:
- Return the full corrected extraction, not just the changed sections.
- If your interface supports file creation, create a `.md` file. Suggested filename: same as the input file, with `-edited` appended, e.g. `extraction-edited.md`.
- If file creation is not supported, output the entire corrected extraction inside one outer raw Markdown copy block using four backticks, starting with `RAW_MARKDOWN_START` and ending with `RAW_MARKDOWN_END`.
- Do not add commentary before or after the corrected extraction.

---

# 3. Metadata Index Prompt

Use this after a final extraction exists.

Input:
- `final.md`

Output:
- compact YAML metadata for search/filtering.

## Prompt

Create a compact YAML metadata record from the final literature extraction.

The YAML should support search, filtering, spreadsheet import, or later RAG indexing.

Use only information present in the final extraction.

If a field is unknown, use `not_stated`.

Return only valid YAML.

Do not wrap the YAML in a code block.

Required fields:

title:
authors:
year:
doi_or_url:
country_or_region:
study_setting:
paper_type:
response_variable:
collision_type:
severity_handling:
spatial_unit:
temporal_unit:
exposure_used:
exposure_method:
traffic_count_source:
missing_traffic_handling:
model_family:
specific_models:
rare_event_handling:
validation_design:
spatial_holdout:
temporal_holdout:
grouped_holdout:
external_validation:
key_features:
transferability_to_open_road_risk:
relevant_stage:
  - Stage 1a
  - Stage 1b
  - Stage 2
  - validation
  - feature engineering
  - documentation
main_repo_actions:
main_limitations:
tags:

Guidance:
- `paper_type` should be one of: prediction, causal inference, hotspot detection, simulation, descriptive analysis, safety performance function, review, other.
- `transferability_to_open_road_risk` should be: high, medium, low, or mixed.
- `tags` should contain 10–20 short search tags.
- Keep values concise.
- Do not invent fields that are not supported by the extraction.

---

# 4. Lightweight Sanity Check Prompt

Use this for low-priority papers where a full cross-audit is too much.

Input:
- paper PDF,
- one extraction.

## Prompt

Check this literature extraction against the attached paper.

Return only:

## Major Problems

List any serious unsupported claims, missing methods, or incorrect transferability judgements.

## Minor Corrections

List smaller fixes.

## Safe to Use?

- yes / yes with caveats / no

Reason:

Rules:
- The paper is the source of truth.
- Do not rewrite the extraction.
- Do not wrap the answer in a code block.
- Be conservative.

---

# 5. Batch Comparison Prompt

Use this after several final extractions exist.

Input:
- multiple `final.md` records.

Purpose:
Compare papers by method, not by general topic.

## Prompt

Compare the attached final literature extraction records.

Focus on methodological implications for Open Road Risk.

Return:

## Exposure Handling Patterns

Group papers by how they handle exposure:
- offset,
- rate denominator,
- direct feature,
- modelled/latent exposure,
- ignored,
- other.

## Collision Model Families

Group papers by model family:
- Poisson,
- negative binomial,
- zero-inflated,
- hurdle,
- Bayesian,
- tree-based ML,
- graph/network model,
- severity model,
- other.

## Validation Patterns

Group papers by validation design:
- random split,
- spatial holdout,
- temporal holdout,
- grouped holdout,
- external validation,
- not stated.

## Transferable Techniques

List techniques that appear across multiple papers and are realistic for Open Road Risk.

| Technique | Papers | Relevant stage | Why useful | Risk |
|---|---|---|---|---|

## Gaps in the Literature Set

Identify what the current set of papers does not yet cover well.

Consider:
- AADT uncertainty,
- minor roads without counts,
- link-based segmentation,
- STATS19-style injury-only outcomes,
- spatial validation,
- severity modelling,
- empirical Bayes shrinkage,
- temporal traffic profiles.

## Suggested Next Papers to Look For

List search queries or paper types to fill the gaps.

Do not invent citations.

---

# 6. Human Review Checklist

Use this manually before committing a final extraction.

## Required Checks

- Response variable is clear.
- Exposure handling is clear.
- Spatial unit is clear.
- Temporal unit is clear.
- Validation design is clear.
- Missing details are marked `Not stated`.
- Transferability is not overstated.
- Required data sources are realistic for Open Road Risk.
- Evidence/page references are present where possible.
- Repo actionability is specific.
- No whole-file Markdown code fence has been added.
- No stray opening or closing fence remains.
- YAML, if present, is valid.

## Commit Criteria

Commit the extraction if:

- it is conservative,
- it is searchable,
- it would help answer “what have others tried?”,
- it would help decide whether a repo change is worth testing.

Do not commit as final if:

- it reads like a general abstract,
- it contains unsupported model claims,
- it says methods are transferable without checking data requirements,
- it hides uncertainty,
- it omits exposure handling.