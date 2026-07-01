# Open Road Risk AI Literature Extraction Case Study

## Purpose

This is a small prompt-ablation case study, not a full benchmark.

The aim is to show how evidence access, project context, and prompt constraints affect AI-assisted literature extraction. Each run should be done in a fresh temporary ChatGPT chat so that context from one run does not contaminate another.

## Recommended paper

**Retallack, A. E., & Ostendorf, B. (2020). _Relationship Between Traffic Volume and Accident Frequency at Intersections_. International Journal of Environmental Research and Public Health, 17(4), 1393.**

DOI: `10.3390/ijerph17041393`

Suggested source PDF: publisher PDF from MDPI.

## Why this paper is a good case-study paper

- It is open access and around 20–22 pages, so it is practical for repeated temporary-chat runs.
- It is road-safety modelling, not just a generic transport paper.
- It has concrete quantitative claims that can be missed, flattened, or overstated:
  - 120 intersections.
  - 1,629 motor-vehicle accidents.
  - More than five million hourly traffic-volume measurements.
  - Poisson and negative-binomial models.
  - A significant quadratic term at high traffic volumes.
  - Rainfall relative risk changes by congestion level.
  - No significant effect of congestion index on accident severity.
- It is close enough to Open Road Risk to be relevant, but not a perfect match:
  - It is intersection-level, not OS Open Roads link-year level.
  - It uses observed traffic-volume data, not sparse AADF estimation.
  - It tests congestion/rainfall relationships, not national-scale road-link risk ranking.

That makes it useful because a good extraction should preserve both relevance and limits.

---

# Run matrix

| Run | Inputs given to ChatGPT | Prompt condition | Purpose |
|---|---|---|---|
| A | Paper PDF + your full Open Road Risk extraction prompt/readme | Full structured prompt | Best-case structured extraction |
| B | Paper PDF only | Generic project-aware extraction prompt | Tests value of full structured prompt |
| C | Paper reference only, no PDF | Reference-only extraction prompt | Tests hallucination and false certainty risk |
| D | Paper reference + Open Road Risk project context, no PDF | Context but no source artefact | Tests whether project context creates plausible but unsupported specificity |
| E | Paper PDF + vague summary prompt | Weak prompt | Shows flattening and premature synthesis |
| F | Paper PDF + structured extraction fields but no Open Road Risk dossier | Structured but not project-specific | Tests value of repo/project context |

---

# Common run rules

Use these rules for every run:

1. Start each run in a fresh temporary ChatGPT chat.
2. Use the same model if possible.
3. Do not correct the model mid-run.
4. Save the output exactly as returned, except for filename cleanup.
5. Record whether ChatGPT created a downloadable Markdown file or required raw Markdown copy-paste.
6. Do not paste outputs from one run into another run.
7. Do not tell ChatGPT what happened in the other runs.
8. Use the same target paper/reference in every condition.

---

# Suggested filenames

- `retallack-ostendorf-2020-run-a-pdf-plus-full-prompt.md`
- `retallack-ostendorf-2020-run-b-pdf-plus-generic-project-prompt.md`
- `retallack-ostendorf-2020-run-c-reference-only.md`
- `retallack-ostendorf-2020-run-d-reference-plus-project-context-no-pdf.md`
- `retallack-ostendorf-2020-run-e-pdf-plus-vague-summary.md`
- `retallack-ostendorf-2020-run-f-pdf-plus-structured-no-dossier.md`

---

# Run A prompt

## Inputs

Attach:

1. The Retallack & Ostendorf paper PDF.
2. Your existing full Open Road Risk literature extraction prompt.

## Prompt to paste

Use the attached Open Road Risk extraction prompt exactly.

Read the attached paper PDF and produce the extraction as a downloadable Markdown file if possible.

Do not use information from outside the attached paper unless the prompt explicitly asks for citation metadata and the metadata is visible in the paper.

---

# Run B prompt: PDF + generic project-aware extraction

## Inputs

Attach:

1. The Retallack & Ostendorf paper PDF only.

Do not attach the full Open Road Risk extraction prompt.

## Prompt to paste

Please read the attached road-safety paper and extract the methodological information that would be useful for my road-risk modelling project.

My project estimates exposure-adjusted injury-collision risk for road links in Great Britain. It uses police-reported injury collisions, road-network links, AADF-style traffic exposure, road/context features, and count models or machine-learning models to rank road links by unusually high observed collisions relative to exposure.

Focus on:

- what the paper models,
- the response variable,
- the spatial and temporal unit,
- how traffic exposure is handled,
- model types,
- quantitative results,
- validation approach,
- limitations,
- transferability to a large open-data UK road-link risk model,
- practical actions I might take.

Do not write a general abstract. Be specific. Where the paper does not state something, say “Not stated”. Do not recommend production changes from this single paper.

Create the output as a Markdown file if possible.

---

# Run C prompt: reference only, no PDF

## Inputs

Do not attach the paper PDF.

Only paste the paper reference below.

## Prompt to paste

I am testing what happens when an AI literature extraction is attempted without the source PDF.

Paper reference:

Retallack, A. E., & Ostendorf, B. (2020). Relationship Between Traffic Volume and Accident Frequency at Intersections. International Journal of Environmental Research and Public Health, 17(4), 1393. https://doi.org/10.3390/ijerph17041393

My project estimates exposure-adjusted injury-collision risk for road links in Great Britain. It uses police-reported injury collisions, road-network links, AADF-style traffic exposure, road/context features, and count models or machine-learning models to rank road links by unusually high observed collisions relative to exposure.

Produce a methodological extraction for this paper.

Important constraints:

- You do not have the paper PDF unless it is available to you through the interface.
- Do not invent page references.
- Do not invent tables, coefficients, sample sizes, methods, or validation details.
- If a detail is not available from the reference alone, write “Not available from reference only”.
- Separate what can be inferred from the title/reference from what would require access to the full paper.
- Include a section listing the risks of using this extraction in an evidence register.

Create the output as a Markdown file if possible.

---

# Run D prompt: reference + project context, no PDF

## Inputs

Do not attach the paper PDF.

Paste the paper reference and the project context below.

## Prompt to paste

I am testing what happens when an AI literature extraction has strong project context but does not have the source PDF.

Paper reference:

Retallack, A. E., & Ostendorf, B. (2020). Relationship Between Traffic Volume and Accident Frequency at Intersections. International Journal of Environmental Research and Public Health, 17(4), 1393. https://doi.org/10.3390/ijerph17041393

Project context:

I am building Open Road Risk, an open-source road safety pipeline for Great Britain.

The project estimates exposure-adjusted road collision risk for OS Open Roads links. The purpose is to identify road links where observed injury collisions are unusually high relative to traffic exposure and road/network context.

The project uses STATS19-style police-reported injury collision records, OS Open Roads geometry, AADF-style annual average daily flow data, WebTRIS-style time-of-day profiles, OSM-derived road features where coverage allows, population/geodemographic context, road classification, link length, estimated AADT, HGV proportion, rural/urban indicators, curvature, grade, and network measures.

The main modelling unit is road link × year. The Stage 2 outcome is observed injury collision count. The current exposure offset is:

log(AADT × link_length_km × 365 / 1e6)

Current models include a Poisson GLM for interpretable diagnostics and XGBoost for risk ranking / predictive benchmarking. Grouped split by road link is used to reduce leakage across repeated years for the same road link. Empirical Bayes shrinkage and negative-binomial escalation are diagnostic or candidate extensions.

Task:

Produce a conservative methodological extraction for the referenced paper, focused on transferability to Open Road Risk.

Important constraints:

- You do not have the paper PDF unless it is available to you through the interface.
- Do not invent paper-specific details.
- If a detail would require the full paper, write “Not available without source PDF”.
- You may explain why the paper sounds relevant from the reference, but clearly separate that from verified extraction.
- Include a section called “Unsupported details that would require checking”.
- Include a section called “Risk of false confidence from project context”.

Create the output as a Markdown file if possible.

---

# Run E prompt: PDF + vague summary prompt

## Inputs

Attach:

1. The Retallack & Ostendorf paper PDF only.

## Prompt to paste

Please summarise this paper and explain how it is useful for my Open Road Risk project.

My project estimates road collision risk using open road, collision, and traffic data.

Tell me the main findings, useful methods, and what I should do in my project based on this paper.

Create the output as a Markdown file if possible.

---

# Run F prompt: PDF + structured fields but no Open Road Risk dossier

## Inputs

Attach:

1. The Retallack & Ostendorf paper PDF only.

Do not attach the full Open Road Risk project dossier.

## Prompt to paste

Read the attached road-safety paper and produce a structured methodological extraction.

Do not write a general abstract.

Do not infer details that are not explicitly stated in the paper. If something is unclear, absent, or only implied, write “Not stated”.

Focus on:

- citation metadata,
- study objective,
- response variable,
- collision type and severity handling,
- exposure handling,
- traffic count source,
- spatial unit of analysis,
- temporal unit of analysis,
- engineered features,
- model architecture,
- Poisson, negative-binomial, zero-inflated, or other count-model handling,
- reported quantitative results,
- validation strategy,
- limitations,
- transferability to a road-safety modelling project using open road-network and collision data.

For each important claim, include a short evidence quote, page reference, section reference, table reference, or figure reference where possible.

Do not recommend production changes from a single paper. Prefer cautious actions such as documentation notes, diagnostics, small pilots, or baseline comparisons.

Create the output as a Markdown file if possible.

---

# Comparison checklist

After all outputs are saved, assess each run against the same checklist.

| Check | Run A | Run B | Run C | Run D | Run E | Run F |
|---|---:|---:|---:|---:|---:|---:|
| Correct citation metadata |  |  |  |  |  |  |
| Correct sample size / study scale |  |  |  |  |  |  |
| Correct response variable |  |  |  |  |  |  |
| Correct spatial unit |  |  |  |  |  |  |
| Correct temporal unit |  |  |  |  |  |  |
| Correct exposure handling |  |  |  |  |  |  |
| Correct model family |  |  |  |  |  |  |
| Captured key quantitative findings |  |  |  |  |  |  |
| Correct validation description |  |  |  |  |  |  |
| Preserved intersection-vs-link limitation |  |  |  |  |  |  |
| Preserved observed-traffic-vs-estimated-AADF limitation |  |  |  |  |  |  |
| Avoided unsupported repo actions |  |  |  |  |  |  |
| Included useful limitations |  |  |  |  |  |  |
| Avoided invented details |  |  |  |  |  |  |
| Clearly stated uncertainty/access limits |  |  |  |  |  |  |

Suggested scoring:

- 2 = correct and useful
- 1 = partially correct or too vague
- 0 = missing, wrong, or unsupported

---

# Commentary points for the methods note

Use the results to comment on questions like:

1. Did the full prompt improve extraction quality, or mainly improve formatting?
2. Did the project dossier make the output more transferable, or did it encourage overfitting to the repo?
3. Did the reference-only run correctly refuse unsupported specificity?
4. Did the vague prompt produce premature synthesis or unsupported recommendations?
5. Did the structured-but-no-dossier run capture paper facts but miss project-specific transferability?
6. Which fields most often prevented overclaiming?
7. Which details still required manual checking even in the best run?

Suggested wording:

> This was not a benchmark of ChatGPT or a proof that one prompt is optimal. It was a small worked example showing how the same paper changes when the model is given different combinations of source access, project context, and extraction constraints. The outputs are published as artefacts so readers can inspect the differences rather than relying only on my description of the workflow.
