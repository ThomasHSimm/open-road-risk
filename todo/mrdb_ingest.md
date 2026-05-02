### MRDB ingest — confirm and clean up

Status: ingest pipeline runs but output is orphaned.

`ingest_mrdb.py` and `clean_mrdb()` produce `mrdb_clean.parquet` but nothing
downstream reads it. The actual AADF→link join in `join.py` uses
`sjoin_nearest` against OS Open Roads, not MRDB's `count_point_id` hard-link.
The docstring on `join.py` line 23 ("Joins AADF count point data onto MRDB
links via count_point_id") is stale — actual joins are spatial, on OS Open
Roads.

History (likely): OS Open Roads was added after MRDB and superseded it for
network geometry. MRDB-specific code path was deprecated but the ingest step
was never removed. Worth confirming via git log on `clean_join/join.py`.

Action:
- Confirm MRDB is genuinely unused (grep for any read of `mrdb_clean.parquet`
  outside of `clean.py`).
- If unused: remove `ingest_mrdb.py` from the pipeline run order in
  `README.md` and `CODE_README.md`. Delete or archive `ingest_mrdb.py` and
  the `clean_mrdb()` function in `clean.py`. Update the stale docstring
  on `join.py:23`.
- If used somewhere I missed: document the actual usage and update the
  methodology page (`data-joining.qmd`) to reflect it.

Public site has been updated separately to remove the MRDB data source page
(removed from `_quarto.yml`, page deleted). See `docs/internal/site-todo.md`.
---

