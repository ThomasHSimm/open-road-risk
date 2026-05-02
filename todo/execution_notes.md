## Notes On Execution Order

The "Queued tasks with prompts" section is now long. Eleven tasks are queued.
Realistic pace is probably one per session, maybe two if things are flowing. This
list documents intent as much as plan.

Dependencies matter more than priority:

- ~~EB shrinkage~~ ✅ done. 5-seed stability is independent of everything else.
- Facility-family split depends on EB shrinkage infrastructure being in place ✅.
- NHNM depends on facility-family split.
- OSM tiered imputation benefits from ONS RUC being done first.
- Curvature/grade are independent but want the 5-seed infrastructure to evaluate
  their contribution honestly.

A rough execution sequence that respects dependencies:

1. ~~AADF filter~~ ✅ done.
2. 5-seed stability — infrastructure for evaluating everything else.
3. ~~EB shrinkage~~ ✅ done (25 April 2026).
4. ~~IMD~~ ✅ + NaPTAN — cheap adds, independent of model structure.
5. ~~ONS RUC~~ ✅ done.
6. ~~OSM tiered imputation~~ ✅ done.
7. Curvature + grade — independent; do when in the mood for geometry work.
8. ~~Facility-family split~~ ✅ sessions 1–2 done (26 April 2026); sessions 3–4 deferred
   pending v2 redesign (motorway overfitting, partial pooling candidate).
9. NHNM integration — depends on facility-family v2 decision.
