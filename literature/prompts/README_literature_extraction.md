# Literature Extraction Workflow

This folder contains prompts and guidance for extracting structured methodological metadata from road-safety literature.

The purpose is to turn academic PDFs into consistent, searchable Markdown records that can be compared against the Open Road Risk pipeline.

## Files

| File | Purpose |
|---|---|
| `road_safety_literature_extraction_prompt.md` | Main prompt used with a paper PDF to produce a structured extraction. |
| `literature_extraction_additional_prompts.md` | Companion prompts for cross-audit, reconciliation, quality control, and metadata indexing. |
| `README_literature_extraction.md` | This usage guide. |

## Core Principle

Do not ask one AI to produce the final answer in one pass and trust it.

Use independent extraction first, then audit, then reconcile.

This reduces the risk of:
- hallucinated methodology,
- overconfident transferability claims,
- missed caveats,
- polished but unsupported summaries,
- one model copying another model's mistake.

The paper PDF is always the source of truth.

## Recommended Workflow

### Step 1 — Independent Extraction

Run the same paper through two AIs independently.

Use:

`road_safety_literature_extraction_prompt.md`

Inputs:
- paper PDF,
- main extraction prompt.

Outputs:
- `extraction_ai1.md`
- `extraction_ai2.md`

Do not show either AI the other AI's output during this step.

Suggested names:

- `extraction_chatgpt.md`
- `extraction_claude.md`
- `extraction_gemini.md`

Use model names that make sense for the tools used.

### Step 2 — Cross-Audit

Use a different AI to audit each extraction against the original PDF.

Use the cross-audit prompt in:

`literature_extraction_additional_prompts.md`

Inputs:
- paper PDF,
- one extraction produced by another AI.

The project context is embedded in `literature_extraction_additional_prompts.md`. You do not need to attach the main extraction prompt separately.

Outputs:
- `audit_ai1_on_ai2.md`
- `audit_ai2_on_ai1.md`

The audit should not rewrite the extraction. It should identify:
- unsupported claims,
- missing details,
- overstatements,
- fields that should be `Not stated`,
- weak transferability judgements.

### Step 3 — Reconciliation

Use the reconciliation prompt in:

`literature_extraction_additional_prompts.md`

This prompt has two modes.

**Mode A — Two extractions:** produces a new `final.md` by combining both extractions. Audit notes are optional; if present, attach them. If not, the AI works directly from the PDF and the two extractions.

Inputs:
- paper PDF,
- both independent extractions,
- audit notes (if available).

Output: `final.md`

**Mode B — One extraction:** edits the single extraction in place and returns a corrected version. Use this when a second independent extraction is not available.

Inputs:
- paper PDF,
- the single extraction.

Output: `extraction-edited.md` (same schema, corrected)

Rules for both modes:
- the paper PDF is the source of truth,
- if support is unclear, write `Not stated`,
- do not include a claim just because multiple AIs included it.

### Step 4 — Optional Metadata Index

For important papers, create a small YAML metadata file or front matter block.

Use the metadata-index prompt in:

`literature_extraction_additional_prompts.md`

Output:
- `metadata.yaml`, or
- YAML front matter at the top of `final.md`.

This makes later search, filtering, spreadsheet import, or RAG indexing easier.

## Chat Interfaces That Render Markdown

Some AI tools render Markdown in chat and do not make it easy to copy the raw `.md` source.

For those tools, use the fallback in the main prompt:

```text
Fallback A — Raw Markdown Copy Block
```

This asks the model to put the entire extraction inside an outer four-backtick raw copy block, with:

```text
RAW_MARKDOWN_START
...
RAW_MARKDOWN_END
```

When saving the file:

1. copy only the content between `RAW_MARKDOWN_START` and `RAW_MARKDOWN_END`,
2. do not include the start/end markers,
3. do not include the outer backticks,
4. save the result as `.md`.

This is especially useful for tools that render headings, tables, and bullets in chat rather than exposing the raw Markdown source.

For tools that can create downloadable files, prefer file output instead.


## Suggested Folder Structure

Use one folder per paper.

Example:

```text
literature/
  001-smith-2021-road-safety/
    paper.pdf
    extraction_chatgpt.md
    extraction_claude.md
    audit_chatgpt_on_claude.md
    audit_claude_on_chatgpt.md
    final.md
    metadata.yaml
```

For lower-priority papers, the lightweight version is acceptable:

```text
literature/
  014-example-paper/
    paper.pdf
    extraction_chatgpt.md
    final.md
```

## When to Use Two AIs vs Three

Use two AIs for most papers.

Use three AIs when the paper is:
- central to the project,
- methodologically complex,
- likely to change the modelling strategy,
- making claims about exposure, severity, zero-inflation, spatial validation, or empirical Bayes,
- difficult to read due to equations, poor OCR, or dense tables.

Do not automatically use three AIs for all papers unless the extra effort is justified.

## Backup Workflow When Multiple AIs Are Not Available

The preferred workflow uses two independent AI extractions, but that may not always be practical.

If only one AI/model is available, do **not** try to fake independence by running the same chat repeatedly with full prior context. Instead, use separated passes with different roles and as little carry-over as possible.

### Option A — One AI, Fresh Chats

Use separate chats or sessions:

```text
Fresh chat 1:
  Paper PDF + main extraction prompt
  → extraction_pass_1.md

Fresh chat 2:
  Paper PDF + main extraction prompt
  → extraction_pass_2.md

Fresh chat 3:
  Paper PDF + extraction_pass_1.md + extraction_pass_2.md + cross-audit/reconciliation prompt
  → final.md
```

This is weaker than using different models, but still better than a single-pass extraction.

Rules:
- start each extraction in a fresh chat where possible,
- do not show pass 2 the output from pass 1,
- use the paper PDF as the source of truth during reconciliation,
- if the two passes disagree and the paper does not clearly resolve it, write `Not stated`.

### Option B — One AI, One Extraction Plus Edit

For lower-priority papers, use the single-extraction mode directly.

Use **Mode B** of the reconciliation prompt in `literature_extraction_additional_prompts.md`:

```text
Paper PDF + main extraction prompt
→ extraction.md

Fresh chat:
  Paper PDF + extraction.md + reconciliation prompt (Mode B)
  → extraction-edited.md

Manual fixes if needed
→ final.md
```

This is the minimum acceptable workflow.

Use it when:
- the paper is peripheral,
- it does not affect modelling choices,
- the method is simple,
- time is limited.

### Option C — Manual Review Only

If model access is limited or the paper is short, use one AI extraction and manually check the high-risk fields.

Manually verify:

- response variable,
- exposure handling,
- spatial unit,
- temporal unit,
- model family,
- validation design,
- transferability judgement,
- repo actionability.

Do not mark the extraction as final until these are checked.

### Priority Rule

Use more review effort for papers that could influence:

- Stage 1a AADT estimation,
- exposure uncertainty,
- Stage 2 count modelling,
- zero-inflated or rare-event modelling,
- empirical Bayes/shrinkage,
- severity handling,
- spatial validation,
- segmentation choices,
- junction modelling.

For low-priority papers, one extraction plus a sanity check is acceptable.


## What Counts as a Good Extraction

A good extraction is:

- evidence-led,
- conservative,
- clear about what is not stated,
- useful for repo decisions,
- honest about data constraints,
- searchable later.

A poor extraction is:

- a generic abstract,
- too polished,
- vague about exposure,
- full of unsupported transferability claims,
- missing validation details,
- pretending that missing paper details are known.

## Quality Checklist

Before accepting `final.md`, check:

- Does it clearly state the response variable?
- Does it state how exposure is handled?
- Does it identify the spatial unit of analysis?
- Does it identify temporal resolution?
- Does it describe validation design?
- Does it distinguish observed traffic counts from estimated exposure?
- Does it flag sparse or missing data?
- Does it avoid unsupported claims?
- Does it include evidence/page references where possible?
- Does it say `Not stated` where needed?
- Does the transferability assessment actually compare against Open Road Risk?

## Common Failure Modes

### Consensus Hallucination

One AI invents or overstates something. Another AI then treats it as plausible because it appears in the first extraction.

Mitigation:
- keep first-pass extractions independent,
- audit against the PDF,
- reconcile only after audit.

### Over-Transferability

The paper uses data that Open Road Risk does not have, but the extraction says the method is transferable.

Mitigation:
- check required data carefully,
- distinguish `high`, `medium`, and `low` transferability,
- mark methods as medium if they require substantial new data engineering.

### Hidden Leakage

A paper may use features that are only known after a collision or are derived from collision events.

Mitigation:
- flag post-event variables,
- compare against the project's leakage guard,
- avoid recommending leakage-prone features for Stage 2.

### Output Wrapped in Code Blocks

Some AIs wrap the whole Markdown output in a code block, which creates broken `.md` files when copied.

Mitigation:
- the main prompt explicitly says not to wrap the whole output in a fenced code block,
- remove stray opening or closing fences before committing.

## Suggested Git Workflow

Create a branch for the literature extraction framework.

Example:

```bash
git checkout -b literature-extraction-workflow
mkdir -p docs/literature/prompts
```

Suggested file locations:

```text
docs/literature/prompts/road_safety_literature_extraction_prompt.md
docs/literature/prompts/literature_extraction_additional_prompts.md
docs/literature/prompts/README_literature_extraction.md
```

Then commit:

```bash
git add docs/literature/prompts/
git commit -m "Add literature extraction prompts and workflow"
```

## Notes for Future Use

The main extraction prompt is intentionally self-contained.

It does not require uploading the repository files.

The repo files were used to create the project dossier inside the prompt, but each literature extraction should only need:

- the paper PDF,
- the main prompt,
- optional companion prompts for audit/reconciliation.