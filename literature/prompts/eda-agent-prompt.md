# Agent prompt — bounded shallow EDA across three datasets

You are running a bounded, mechanical exploratory data analysis across three public datasets for the `openbotrisk` project. The repo already exists with PROJECT.md and REPO.md committed. Read both before starting — they set the project's scope and constraints.

This task is **familiarity-building only**, not methodology investigation. The output is a short structured EDA report per dataset, written so a human reader (the project owner) can quickly understand what each dataset contains. You are **not** evaluating fit, comparing datasets, or recommending which to use. Those are downstream human judgments.

---

## DATASETS

Download all three into the local `data/` directory of the repo. Note that `data/` is gitignored per REPO.md — do not commit the raw data.

| Dataset | Access method | Approximate size |
|---|---|---|
| TalkingData AdTracking Fraud Detection | Kaggle CLI: `kaggle competitions download -c talkingdata-adtracking-fraud-detection` | ~7 GB compressed |
| IEEE-CIS Fraud Detection | Kaggle CLI: `kaggle competitions download -c ieee-fraud-detection` | ~1 GB |
| CTU-13 | Direct download: `https://mcfp.felk.cvut.cz/publicDatasets/CTU-13-Dataset/CTU-13-Dataset.tar.bz2` | ~1.9 GB |

Kaggle CLI requires the user to have `~/.kaggle/kaggle.json` configured with API token and to have accepted competition rules on the Kaggle website. If Kaggle access fails, stop and report — do not invent workarounds.

---

## CONSTRAINTS

| Do | Don't |
|---|---|
| Run mechanical descriptive analysis | Run any modelling, even baselines |
| Use streaming/chunked reads if needed for memory | Hold entire TalkingData in memory unless trivial |
| Report dataset structure and signal inventory | Compare datasets to each other |
| Note obvious quirks (missing values, label imbalance, time spans) | Make judgments about which dataset is "good" |
| Use DuckDB or polars where pandas would struggle | Add new Python dependencies beyond the minimal set in `environment.yml` plus DuckDB and polars if not already present |
| Stop and ask if something is ambiguous | Invent answers to questions REPO.md doesn't address |
| Produce one short markdown file per dataset | Write a synthesis or recommendation document |
| Keep total runtime reasonable (hours not days) | Run anything that takes overnight without checking |

---

## PER-DATASET OUTPUT

For each dataset, produce a markdown file at `working/eda/<dataset-slug>.md` with the following structure. Keep each section tight — a paragraph or a short table, not an essay.

```
# EDA: <Dataset name>

## Access
- Where downloaded from
- Total size on disk
- File format(s)
- Date downloaded

## Structure
- File or table layout
- Record granularity (click, session, transaction, flow)
- Total row count per file
- Date range / temporal coverage
- Join keys between files (if multiple)

## Schema
- Table of: column name, dtype, nullable, brief description (from official documentation), example value
- Mark columns whose meaning is anonymised or unclear

## Label
- Which column is the label
- Label definition (from official documentation)
- Class balance
- Any notes on label semantics (e.g. proxy labels, time-delayed labels)

## Identifier inventory
- List columns that could serve as actor identifiers or weak identifiers (IPs, device IDs, user IDs, IP-derived signals, browser/device fingerprints, etc.)
- For each: cardinality, missingness rate
- Note explicitly if no such identifiers are present

## Temporal structure
- Time column(s) present
- Time range covered
- Granularity (millisecond, second, minute, day)
- Any obvious temporal patterns in record density (e.g. weekday/weekend, time-of-day bursts) — describe in one or two sentences, do not plot

## Missing data
- Overall missingness rate
- Columns with high missingness (>20%)
- Any patterns of missingness worth noting (entire columns missing for certain time windows, etc.)

## Quirks and observations
- Anything unusual encountered during inspection
- Inconsistencies between official documentation and actual data
- Memory or processing issues encountered

## Reproduction
- The exact commands or script used to generate this report
- Any preprocessing applied (e.g. chunked reading parameters)
- How long the analysis took to run
```

---

## CODE ORGANISATION

Create a small EDA module at `src/openbotrisk/eda/` containing:

- `loaders.py` — functions to load each dataset with sensible chunking
- `descriptive.py` — reusable functions for the descriptive stats (cardinality, missingness, etc.)
- `report.py` — function that takes a dataset and produces the markdown structure above

The actual EDA runs go in `notebooks/eda/<dataset-slug>.ipynb` — one notebook per dataset, calling functions from `src/openbotrisk/eda/`. The notebooks should be reproducible: someone running them top-to-bottom should produce the same markdown report (assuming the data is in place).

The markdown reports are committed to `working/eda/`. The notebooks are committed to `notebooks/eda/`. The raw data stays in `data/` and is gitignored.

---

## DEFINITION OF DONE

| Criterion | Verification |
|---|---|
| All three datasets downloaded successfully | Files present in `data/` |
| One markdown report per dataset in `working/eda/` | Three files exist, follow the structure above |
| One notebook per dataset in `notebooks/eda/` | Three notebooks, each runs top-to-bottom without error |
| EDA module exists in `src/openbotrisk/eda/` | Importable, basic tests pass |
| No raw data committed | `git status` shows no files under `data/` |
| pre-commit passes | `pre-commit run --all-files` exits clean |
| The reports contain no judgments about dataset fit | Reports describe what is present; do not interpret |

When done, report back with:
- The tree of files created
- A one-line summary per dataset of its scale (rows, columns, time span)
- Any blockers encountered (failed downloads, ambiguous schemas, etc.)
- Confirmation that no data was committed and no remote operations were performed

---

## OPERATING RULES

- **Do not push to any remote.** Local work only. The user pushes manually after reviewing.
- **Do not open PRs or interact with GitHub.**
- **Do not modify PROJECT.md or REPO.md.**
- **Do not add new files outside the directories named in this prompt.**
- **Stop and ask** if a dataset's schema is unclear from official documentation, if downloads fail, if memory is insufficient, or if anything else is ambiguous. Do not invent.
- **No synthesis, no comparison, no recommendation.** The reports describe each dataset independently. Cross-dataset analysis is a separate downstream task.
