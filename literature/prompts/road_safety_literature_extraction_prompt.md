# Road Safety Literature Extraction Prompt

Use this prompt with each academic paper PDF. Attach the paper and paste the full prompt below.

---

# Role

You are extracting methodological metadata from an academic road-safety paper for a real-world open-data road-risk modelling project.

Do **not** write a general abstract.

Do **not** infer details that are not explicitly stated in the paper.

If something is unclear, absent, or only implied, write: **Not stated**.

Prefer a sparse accurate extraction over a complete-looking but speculative one.

Where possible, include short evidence quotes or page references. If page numbers are unavailable, describe the section/table/figure where the evidence appears.

Before extracting, identify the filename of the paper PDF if it is visible in the interface. If the filename is not visible, write: **not stated**.


Prefer page, table, figure, or section references over internal citation IDs.

Use internal citation IDs only if the interface provides them and no page reference is available.

---

# My Project Context / Repo Dossier

I am building **Open Road Risk**, an open-source road safety pipeline for Northern and Central England.

## Aim

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

---

# Current Modelling Structure

## Stage 1a — AADT Estimator

- Predicts AADT for every road link.
- Trained on counted-only AADF rows.
- Uses gradient boosting style regression.
- Uses grouped validation by count point.
- Current reported CV R² is approximately 0.83, but spatial generalisation and feature consistency remain important concerns.

## Stage 1b — Time-Zone Profile Model

- Learns within-day traffic profile fractions from WebTRIS site-year data.
- Uses grouped validation by WebTRIS site.
- Currently separate from the Stage 2 collision model.

## Stage 2 — Collision Risk Model

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

---

# Important Methodological Guardrails

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

---

# Transferability Rules

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

---

# Evidence Scope Rules

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

unless the paper provides broad evidence across multiple settings and compatible data.

---

# Repo Action Discipline

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

---

# Access Limitation

Do not assume access to my repository code.

Use this project dossier as the full description of my pipeline unless I provide extra files.

If a judgement depends on implementation details not provided here, say so explicitly.

---

# Extraction Task

Read the attached paper and output a structured methodological extraction.

Focus strictly on:

- data engineering,
- mathematical assumptions,
- exposure handling,
- spatial/temporal design,
- model architecture,
- reported quantitative results,
- validation,
- transferability to Open Road Risk.

Do not include generic literature-review prose.

Do not include recommendations unsupported by the paper.

---

# Extraction Run Metadata Requirement

At the start of the extraction, include a short run-metadata section.

If the AI model name or version is visible in the interface, record it.

If it is not visible, write `not stated`.

Do not guess the model version.

Record the source PDF filename if visible. If it is not visible, write `not stated`.

If a downloadable `.md` file is not created, include a `Save this as:` line immediately after `RAW_MARKDOWN_START`.

Suggested filename pattern:

`paper-extraction-author-year-short-title.md`

The `Save this as:` line is for the user and should not be included in the final saved Markdown file unless the user wants to keep it as provenance.

---

## Important for Chat Interfaces That Render Markdown

If you cannot create a downloadable `.md` file, you must use the raw copy-block fallback. Do not provide rendered Markdown directly in chat, because rendered headings, bullets, and tables are not reliable for copy/paste into a Markdown file.

# Output Delivery Requirement

You must provide the extraction in a form that can be saved as a `.md` file without losing the raw Markdown syntax.

## Preferred Output — Downloadable Markdown File

If your interface supports file creation or downloadable artifacts, create a Markdown file with the extraction as the file contents.

Suggested filename pattern:

`paper-extraction-author-year-short-title.md`

Do not also paste a rendered Markdown version in chat unless asked.

## Mandatory Chat Fallback — Raw Markdown Copy Block

If you cannot create a downloadable `.md` file, do **not** output normal rendered Markdown in chat.

Instead, output the entire extraction inside one outer raw Markdown copy block using **four backticks**.

Start exactly with this line:

````text
RAW_MARKDOWN_START
````

Immediately after `RAW_MARKDOWN_START`, add one line:

`Save this as: paper-extraction-author-year-short-title.md`

Then put the Markdown extraction.

End exactly with this line:

````text
RAW_MARKDOWN_END
````

The user will copy the Markdown extraction between `RAW_MARKDOWN_START` and `RAW_MARKDOWN_END`.

Do not include:

- the outer four-backtick fences,
- `RAW_MARKDOWN_START`,
- `RAW_MARKDOWN_END`

in the saved `.md` file.

The `Save this as:` line can either be removed before saving or kept at the top if the user wants filename provenance.

## Markdown Safety Rules

- Do not output ordinary rendered Markdown in chat if no downloadable file is created.
- Do not start the actual extraction with ```markdown.
- Do not wrap sections of the extraction in triple-backtick fences unless absolutely necessary.
- If a code/math block is needed inside the extraction, prefer indented code blocks or inline code.
- Do not add commentary before or after the extraction.
- The saved content must be valid Markdown.

---

# Output Format

Use the exact headings below.

Do not add commentary before or after the extraction.

---

# Paper Metadata

## 0. Extraction Run Metadata

- Extraction date:
- Source PDF filename:
- Suggested Markdown filename:
- AI tool used: ChatGPT / Claude / Gemini / other / not stated
- Model name, if visible:
- Model version, if visible:
- Interface used: web chat / API / desktop app / other / not stated
- Input type: PDF upload / text pasted / OCR / other
- Output mode: downloadable `.md` file / raw Markdown copy block / rendered chat Markdown / other
- Was the full paper accessible to the model? yes / no / uncertain
- Notes on access limitations:

## 1. Citation

- Title:
- Authors:
- Year:
- DOI or URL, if present:
- Country / region studied:
- Study setting: urban / rural / motorway / mixed / not stated

## 2. Core Objective

- One-sentence description of what the paper tries to predict, estimate, explain, or classify:
- Main purpose: prediction / causal inference / hotspot detection / simulation / descriptive analysis / safety performance function / other
- Evidence quote or page reference:

## 3. Response Variable

- Target variable:
- Collision type: injury / fatal / serious / slight / property-damage-only / all crashes / not stated
- Severity handling:
- Count, binary, rate, risk score, severity class, or other:
- Time window used for outcomes:
- Evidence quote or page reference:

## 4. Exposure Handling

- Exposure variable used, if any:
- Traffic count source:
- Whether exposure is modelled, observed, assumed, or ignored:
- Treatment of missing or sparse traffic counts:
- Whether offset terms, rates, denominators, or normalisation are used:
- Evidence quote or page reference:
- Transferability to my AADF/WebTRIS setup: high / medium / low / mixed
- Notes:

Important:

- Separate transferability of the mathematical exposure structure from transferability of the paper's specific data source.
- Do not label exposure handling as high-transferability if the paper relies on traffic data I do not have, unless the transferable part is clearly limited to the model structure.

## 5. Spatial Unit of Analysis

- Unit: road segment / intersection / grid cell / route / area / other
- Segment length or segmentation rule:
- How crashes are assigned to the network:
- Treatment of junctions/intersections:
- Spatial aggregation risks:
- Evidence quote or page reference:
- Relevance to OS Open Roads link-based pipeline:

## 6. Temporal Unit of Analysis

- Years covered:
- Temporal resolution: yearly / monthly / daily / hourly / peak-off-peak / other
- Whether seasonality or time-of-day is modelled:
- Whether before-after or panel structure is used:
- Evidence quote or page reference:
- Relevance to WebTRIS-style time profiles:

## 7. Engineered Features

List the most important engineered features, especially those I could recreate.

| Feature | Raw source | Engineering method | Why it matters | Transferable to my pipeline? |
|---|---|---|---|---|

Only include features actually used in the paper.

If a feature is already part of Open Road Risk, mark it as "already present / compare implementation" rather than suggesting it as new.

## 8. Model Architecture

- Algorithms/models used:
- Baseline model:
- Final/preferred model:
- Loss function or likelihood, if stated:
- Offset/exposure term, if used:
- Spatial autocorrelation handling:
- Temporal dependence handling:
- Interpretability method:
- Evidence quote or page reference:

## 9. Reported Metrics / Quantitative Results

Extract the main quantitative results reported in the paper.

Include:

- model comparison metrics,
- predictive metrics,
- calibration metrics,
- classification metrics,
- uncertainty intervals,
- headline coefficient/effect estimates,
- ranking/hotspot performance,
- sensitivity-analysis results.

Use a table where possible.

| Result type | Metric/statistic | Value | Model/subgroup | Interpretation | Evidence/page |
|---|---|---|---|---|---|

After the table, answer:

- Are these metrics in-sample, out-of-sample, cross-validated, spatially held out, temporally held out, externally validated, or not stated?
- If predictions are evaluated on the same data used for fitting, label the result as **in-sample posterior predictive diagnostic** or **in-sample diagnostic**, not unqualified predictive accuracy.
- Do these metrics test predictive generalisation, model fit, ranking/hotspot usefulness, posterior predictive adequacy, calibration, or something else?
- Are any metrics likely to be optimistic for real-world deployment?
- Which metric, if any, is most relevant to Open Road Risk?

Important:

- Do not invent metrics.
- Do not call a metric "predictive accuracy" without qualification unless the paper uses held-out, cross-validated, temporal, spatial, or external validation data.
- Do not treat DIC, AIC, BIC, WAIC, posterior fit, or in-sample accuracy as equivalent to external predictive validation.
- If the paper reports only model-comparison metrics, say that clearly.
- If the paper reports no usable quantitative validation, write `Not stated`.

## 10. Rare Event / Class Imbalance Handling

- How rare collisions or zero-heavy data are handled:
- Use of Poisson / negative binomial / zero-inflated models / hurdle models / resampling / weighting / focal loss / other:
- Whether high-risk locations are evaluated separately:
- Evidence quote or page reference:
- Practical relevance to my sparse collision link-year dataset:

Important:

- Do not use the tag or phrase `zero-inflated` unless the paper explicitly uses a zero-inflated model.
- If the data are zero-heavy but the model is not zero-inflated, say `zero-heavy counts handled using...`.

## 11. Validation Strategy

- Train/test split method:
- Spatial holdout used? yes/no/not stated
- Temporal holdout used? yes/no/not stated
- Grouped holdout used? yes/no/not stated
- Cross-validation type:
- Metrics:
- External validation:
- Leakage or generalisation risks:
- Evidence quote or page reference:
- What I should copy or avoid:

Important:

- Distinguish classic data leakage from weaker external generalisation.
- If a spatial random-effect model uses neighbouring observed outcomes during fitting, describe this as an in-sample spatial smoothing/generalisation limitation unless the paper makes a true leakage error.
- Do not overstate this as leakage without evidence.

## 12. Key Findings Relevant to My Project

Give 3–6 findings that are directly useful for my road-risk pipeline.

For each finding:

- Finding:
- Why it matters:
- Evidence quote or page reference:
- Confidence: high / medium / low

Important:

- Do not overgeneralise from a small or simplified study area.
- If the finding supports a direction rather than proves a repo decision, say that.
- Preserve the paper's scope. Use phrases like "in this case study" or "this suggests" where appropriate.

## 13. Transferability Assessment Against Open Road Risk

### Techniques I could realistically implement

| Technique | Why useful for this repo | Required data | Paper scale | Open Road Risk scale compatibility | Fits current stage? Stage 1a / Stage 1b / Stage 2 / future feature / validation / documentation | Implementation difficulty | Main risk |
|---|---|---|---|---|---|---|---|

### Techniques that probably do not transfer

| Technique | Why it does not transfer | Missing data or assumption | Paper scale | Open Road Risk scale compatibility | Possible workaround | Confidence |
|---|---|---|---|---|---|---|

Important:

- A technique can be conceptually transferable but practically difficult at Open Road Risk scale.
- Mark computationally unrealistic methods as medium or low transferability even if they are statistically attractive.
- Do not recommend adding features that are already in the repo; instead suggest validation, comparison, or documentation of existing features.
- Include the study scale from the paper where available, such as number of links, intersections, crashes, years, or regions.

## 14. Pipeline Implications

Answer these directly:

- Does this paper support using exposure-normalised collision risk?
- Does it suggest better handling of AADT/AADF uncertainty?
- Does it suggest useful geometry or road-context features?
- Does it suggest better modelling of junctions?
- Does it suggest better treatment of severity?
- Does it suggest better validation design?
- Does it expose a weakness in my current approach?

## 15. Repo Actionability

Give up to 5 concrete implications for my repo.

For each:

- Suggested repo action:
- Action type: documentation note / diagnostic / small pilot / baseline comparison / candidate feature / candidate model extension / production change
- Relevant stage: Stage 1a / Stage 1b / Stage 2 / validation / feature engineering / documentation
- Why the paper supports it:
- Evidence quote or page reference:
- Effort: low / medium / high
- Risk if implemented badly:

Important:

- Suggested actions should be realistic for Open Road Risk.
- Prefer the least disruptive useful action.
- If a feature already exists, suggest testing, documenting, validating, or comparing it rather than "add feature".
- Do not suggest large architecture changes unless the paper gives strong support.
- Prefer diagnostic additions over disruptive model rewrites unless evidence is strong.
- Avoid recommending production changes directly from a single paper.

## 16. Query Tags

Produce 10–20 short tags I can use for search/filtering later.

Examples:

- AADT
- exposure-offset
- negative-binomial
- zero-heavy-counts
- junction-risk
- spatial-holdout
- segment-level
- severity-model
- UK-transferable
- traffic-count-imputation

Important:

- Do not use `zero-inflation` unless the paper explicitly fits a zero-inflated model.
- Prefer precise tags over fashionable ones.

## 17. Confidence and Gaps

- Overall confidence in extraction: high / medium / low
- Important details not stated in the paper:
- Parts of the paper that need manual checking:
- Any likely ambiguity or risk of misinterpretation:

---

# Final Instruction

The output should be useful as a searchable metadata record.

Be strict, evidence-led, and conservative.

Do not make the paper sound more relevant than it is.

Do not add claims merely because they seem plausible from general road-safety knowledge.

Do not add repo actions that are not supported by the paper.

Do not recommend production repo changes from a single paper unless the evidence is unusually strong and directly transferable.
