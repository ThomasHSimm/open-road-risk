### IMD (Index of Multiple Deprivation) LSOA join

> **STATUS: COMPLETED 1 May 2026.**
> See `todo/feature_addition_imd_grade.md` for the writeup.
> Kept here as a record of the original specification and prompt.

- [x] IMD 2025 LSOA join added to `network_features.parquet` (1 May 2026) —
  overall IMD decile, crime decile, and living-environment indoors decile
  included. Indoors sub-domain used instead of the full Living Environment
  domain to avoid leakage from the Outdoors road traffic accidents indicator.
  See `data/provenance/imd_provenance.json`.
- [ ] Persist `lsoa21cd_assigned` to `network_features.parquet` for future
  IMD/RUC coverage diagnostics. Current IMD coverage gap is explained:
  61,313 links without English IMD ≈ the earlier 62k estimate, almost
  certainly Welsh LSOAs picked up at the western edge of the study bounding
  box (Cheshire/Shropshire border and Wirral peninsula reaching toward Wales).
  Not urgent; this would make the diagnostic one-line in future.

**Context:** Deprivation correlates with crash risk via mechanisms not
captured by population density alone — older vehicle fleets, enforcement
gaps, pedestrian exposure, on-street parking density. LSOA-grain open data
from MHCLG. Integration is near-free — same spatial join as existing LSOA
population density feature.

**Decisions already made:**
- Use domain-level scores (crime, living environment) rather than only
  the overall IMD decile; these domains are more directly road-safety-
  relevant.
- Universal England coverage (LSOA is complete).
- No licensing friction.

**Prompt:**
[Draft as a small, well-scoped task. Download IMD 2019 LSOA data, join
via existing LSOA spatial join infrastructure, add as features to Stage 2.
Include overall decile plus crime domain and living environment domain as
separate features. Report before/after CV R² on Stage 2 retrain.]

**Expected outcomes:**
- Modest pseudo-R² improvement (0.01–0.03).
- Crime domain likely carries more distinctive signal than overall decile
  (which correlates heavily with other things already in the model).

---
