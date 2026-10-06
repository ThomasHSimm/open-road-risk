# DRAFT — Kaggle dataset description caveat (not yet published)

Drafted 2026-10-06. For the "Open Road Risk GB link risk + exposure GIS" dataset
description. Do **not** publish until reviewed.

---

**Known limitation — traffic exposure is extrapolated outside central England (2026-10-06).**

The Stage 1a AADT (traffic exposure) model was trained on DfT AADF count points
limited to **latitudes 52.0–55.2°N** (roughly central England), because of a
stale ingest cache created under an earlier, smaller study-area bounding box.
The raw DfT AADF data is full-GB (≈40,300 count points); this release used
≈14,200 of them (≈12,900 directly counted), all within that band.

As a result:

- Estimated AADT and HGV share for links **outside 52.0–55.2°N** (about half of
  the ~3.94 M scored links, and the areas containing the majority of recorded
  collisions) are **model extrapolations**, not fits to local counts. HGV share
  is imputed for almost all out-of-band links.
- Risk rankings that depend on exposure inherit this uncertainty and are least
  reliable in Scotland, Wales, and northern/southern England.

Treat out-of-band exposure and rankings as indicative only. A full-GB AADF
rebuild is planned; this notice will be removed once exposure is refit on
national count data.
