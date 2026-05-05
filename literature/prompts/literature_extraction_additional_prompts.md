# Literature Extraction Additional Prompts

This file contains companion prompts for use after the main extraction prompt.

Use these when checking, reconciling, or indexing AI-generated literature extractions.

The main extraction prompt is:

`road_safety_literature_extraction_prompt.md`

---

# 1. Cross-Audit Prompt

Use this after one AI has produced an extraction.

Attach:
- the original paper PDF,
- the extraction to audit,
- the main project context or main extraction prompt if useful.

Do not ask the auditing AI to rewrite the whole extraction. Its job is to check evidence quality.

## Prompt

You are auditing another AI's extraction of the attached academic paper.

Inputs:
1. The original paper PDF.
2. A Markdown extraction produced by another AI.
3. The Open Road Risk project context.

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

# 2. Reconciliation Prompt

Use this after two or more independent extractions and audit notes exist.

Attach:
- the original paper PDF,
- independent extractions,
- audit notes.

The output should be the final `final.md` record.

## Prompt

You are producing a final methodological metadata extraction for one academic paper.

Inputs:
1. The original paper PDF.
2. Two or more independent AI extractions.
3. Audit notes identifying unsupported claims, missing details, and overstatements.
4. The Open Road Risk project context.

Task:
Create one final Markdown extraction using the same schema as the main extraction prompt.

Rules:
- The paper PDF is the source of truth.
- If extractions disagree, use the version best supported by the paper.
- If no version is clearly supported, write `Not stated`.
- Do not include a claim just because multiple AIs included it.
- Remove unsupported transferability claims.
- Keep evidence quotes or page references where possible.
- Preserve useful disagreement as a caveat where relevant.
- Prefer conservative, searchable metadata over polished prose.

Output requirement:
- If your interface supports file creation, create a `.md` file.
- Suggested filename: `final.md`.
- If file creation is not supported and the chat renders Markdown, use the raw Markdown copy-block fallback from the main prompt.
- If raw source copying works correctly, output plain Markdown directly in chat.
- Do not add commentary before or after the final extraction.

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
