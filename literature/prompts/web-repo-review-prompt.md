# Web and Repository Review Prompt

Use this prompt to extract structured methodological notes from websites, online courses,
or GitHub repositories relevant to Open Road Risk.

This prompt is a companion to the paper extraction prompt
(`road_safety_literature_extraction_prompt.md`). Reviews produced by this prompt live in
the same `literature/` folder as paper extractions, with the filename prefix
`web-review-` or `repo-review-` to distinguish them from paper extractions.

**When to use this prompt:**

- Methodology course sites (e.g. Transport Data Science, Spatial Data Science with R)
- GitHub repos implementing methods relevant to the pipeline (e.g. EB shrinkage, SPF
  fitting, spatial CV)
- Online textbooks or reference guides (e.g. Geocomputation with R, Highway Safety Manual
  online resources)
- Do NOT use for data-source catalogues (DfT, AADF, STATS19 bulk downloads) — those
  warrant a separate data-source review schema

**How to use:**

Attach this prompt in a fresh chat. Provide the URL(s) to review. The AI should fetch
and read the pages before producing the extraction. If the site is large, specify which
pages to review rather than the root URL alone.

---

## Prompt

You are producing a structured methodological review of a website or GitHub repository
for the Open Road Risk project.

This is not a paper extraction. Do not use the paper extraction schema. Use the schema
below instead.

The Open Road Risk project context is provided below. Read it before producing the review.

---

### Open Road Risk Project Context

**Aim:** Open Road Risk is an open-source road safety pipeline for Northern and Central
England. It estimates exposure-adjusted road collision risk for OS Open Roads links
(~2.17M links). The purpose is to identify road links where observed injury collisions
are unusually high relative to traffic exposure and road/network context.

**Pipeline stages:**
- Stage 1a — ML-based AADT estimation from sparse DfT AADF counts (~0.4% of links have
  observed counts)
- Stage 1b — WebTRIS-derived time-zone traffic profile estimation (peak/off-peak/overnight
  fractions per link)
- Stage 2 — Poisson GLM + XGBoost collision risk model at link × year grain, with
  log(AADT × length × 365 / 1e6) as exposure offset; XGBoost drives the production
  `risk_percentile`; Empirical Bayes shrinkage available as a diagnostic variant

**Data stack:** STATS19 injury collisions (police-reported), OS Open Roads geometry,
DfT AADF traffic counts, WebTRIS National Highways profiles, OSM features, OS Terrain 50
grade, ONS census/deprivation, rural/urban classification.

**Language and tooling:** Python 3.11/3.14, conda env1, pandas/geopandas/pyarrow,
XGBoost, statsmodels, scikit-learn, Quarto for documentation.

**Key open questions:** AADT elasticity testing, spatial CV (police-force holdout),
temporal holdout, NB GLM vs Poisson, EB shrinkage per facility family, temporal
exposure conditioning (core_overnight_ratio), STATS19 collision timing disaggregation,
zero-calibration diagnostic, CURE plots.

---

### Instructions

Read the pages listed below (or all main methodology pages if no list is provided).

For each section of the schema, answer based only on what the site/repo actually contains.
If a field does not apply or the content is absent, write `Not covered`.

Do not invent content that is not on the site.
Be conservative about transferability — note where methods use R when the pipeline uses
Python, or where examples use different data sources.
Flag where content is pedagogical/illustrative versus production-ready.

---

## Output Schema

### 0. Review Metadata

- Review date:
- Resource name:
- Root URL:
- Resource type: [course site / online textbook / GitHub repo / reference tool / other]
- Primary language(s): [R / Python / both / other]
- Pages reviewed: [list each URL reviewed and the date accessed]
- Pages not reviewed (if site is large): [list any major sections skipped and why]
- Was code executable or only illustrative?
- Overall accessibility: [freely available / login required / partially paywalled]

---

### 1. Resource Description

- One-paragraph description of what this resource is and who it is aimed at.
- Authors or maintainers, if stated.
- Institutional affiliation, if stated.
- Last updated or version, if stated.
- Relationship to any papers already in the Open Road Risk literature register (e.g. same
  author as Gilardi 2022).

---

### 2. Methods Covered

List the methodological topics covered, grouped by category. For each topic note:
- Whether it is covered conceptually only, with illustrative code, or with
  production-quality implementation.
- The programming language used.
- A page URL or section reference.

Use this structure:

| Topic | Coverage depth | Language | Page/section |
|---|---|---|---|

Categories to consider:
- Crash / collision data handling (STATS19, police-reported data)
- Traffic exposure / AADT
- Count models (Poisson, NB, zero-inflated)
- Safety performance functions / SPFs
- Empirical Bayes shrinkage
- Spatial methods (CAR, spatial CV, network analysis)
- Temporal methods (time-series, holdout design)
- Machine learning for transport (XGBoost, random forest)
- Road network analysis (OS Open Roads, OSM, igraph, NetworkX)
- Validation and metrics
- Visualisation and mapping
- Reproducibility and workflow (Quarto, Git, environments)

---

### 3. Code Quality and Reproducibility

- Is code provided? If so, as standalone scripts, notebooks, or a package?
- Is the code runnable as-is, or does it require data not provided?
- What dependencies are required? Are they compatible with Open Road Risk's stack
  (Python 3.11, conda, standard geospatial/ML packages)?
- Is there a clear licence for reuse?
- Any notable code patterns worth adopting (e.g. a clean spatial join approach,
  a well-structured validation loop)?

---

### 4. Relevance to Open Road Risk Pipeline Stages

For each pipeline stage, note whether the resource provides useful guidance, code,
or conceptual framing. Use: high / medium / low / not covered.

| Stage | Relevance | What specifically is useful |
|---|---|---|
| Stage 1a — AADT estimation | | |
| Stage 1b — Time-zone profiles | | |
| Stage 2 — Collision risk model | | |
| Validation and metrics | | |
| Feature engineering | | |
| Documentation and reproducibility | | |

---

### 5. Key Transferable Items

List specific techniques, code patterns, datasets, or conceptual framings that could
be directly useful for Open Road Risk. Be concrete — name the page, function, or
section.

For each item note:
- What it is
- Why it is useful
- Any adaptation needed (language translation, data source substitution, scale adjustment)
- Confidence that it transfers: high / medium / low

| Item | Why useful | Adaptation needed | Confidence |
|---|---|---|---|

---

### 6. What Does Not Transfer

List content that appears relevant but does not transfer to Open Road Risk.
Common reasons: R-only with no Python equivalent, requires data not in the UK open stack,
pedagogical only with no production path, scale incompatible with 2.17M links.

| Item | Why it does not transfer | Possible workaround |
|---|---|---|

---

### 7. Repo Actions

Suggest specific actions for the Open Road Risk repository based on this review.
Follow the repo action discipline: documentation note → diagnostic → small pilot →
candidate feature → production change. Do not recommend production changes from a
single resource unless the evidence is strong and scale-compatible.

For each action:

- **Action:** what to do
- **Type:** documentation note / diagnostic / small pilot / candidate feature / production change
- **Relevant stage:** Stage 1a / Stage 1b / Stage 2 / validation / documentation
- **Why this resource supports it:**
- **Effort:** low / medium / high
- **Risk if implemented badly:**

---

### 8. Gaps This Resource Does Not Cover

Note any Open Road Risk questions this resource was expected to address but does not.
This helps identify what to look for next.

---

### 9. Query Tags

10–20 short tags for search and filtering. Include: language, methods covered, key
authors, relevant pipeline stages, and any notable limitations.

---

### 10. Confidence and Caveats

- Overall confidence in review: high / medium / low
- Pages that should be re-reviewed when updated:
- Any content that was inaccessible (login walls, broken links, incomplete pages):
- Whether a re-review is recommended after a stated update cycle:

---

## Output requirements

- Do not wrap the whole output in a code block.
- Do not add commentary before or after the extraction.
- Use the filename prefix `web-review-` for course/textbook sites and `repo-review-`
  for GitHub repositories.
- Suggested filename format: `web-review-[short-name]-[year].md`
  e.g. `web-review-tds-lovelace-2025.md`
- If your interface supports file creation, create a `.md` file.
- If not, output inside a four-backtick raw copy block with `RAW_MARKDOWN_START` and
  `RAW_MARKDOWN_END` markers.
