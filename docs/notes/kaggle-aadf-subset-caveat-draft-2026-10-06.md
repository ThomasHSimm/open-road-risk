# DRAFT — Kaggle dataset description update (not yet published)

Drafted 2026-10-06. For the "Open Road Risk GB link risk + exposure GIS" dataset
description, describing the new full-GB version. Do **not** publish until reviewed.

---

**Version note — full-GB exposure rebuild (2026-10-06).**

An earlier release trained the Stage 1a traffic-exposure (AADT) model on a
**52.0–55.2°N subset** of the DfT AADF count network (central England), because
of a stale ingest cache. In that version, estimated AADT and HGV share outside
that band (about half the links and most recorded collisions) were model
extrapolations, and exposure was systematically under-estimated — worst in Wales,
Scotland and London.

This has been fixed. The AADF ingest now covers the **full GB** count network
(~29,400 count points; ~26,100 directly counted used for training), and Stage 1a
and the Stage 2 collision model have been rebuilt on it. Changes you will see:

- HGV-proportion coverage rose from ~40% to ~80% of links (Scotland ~0.6%→69%,
  Wales ~10%→71%).
- Estimated AADT rose substantially outside central England (median +80–85% in
  Wales/Scotland, +54% London), so the exposure-adjusted collision **rate per
  vehicle-km** fell most in those regions.
- Link **rankings are highly stable** (Spearman ≈ 0.99 vs the previous version;
  ~80% of the top-1% links unchanged).
- Stage 1a is validated GB-wide; the weakest region under spatial holdout is
  London (mean signed log bias +0.090).

**Reminder on interpretation:** the `risk_percentile` field ranks each link by
its *expected collision count* (burden), which scales with traffic — not by
collision rate per vehicle-km. Treat it as a screening layer, not causal proof
or an engineering audit.
