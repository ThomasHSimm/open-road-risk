### Curvature from OS Open Roads geometry

**Context:** Curve geometry correlates with run-off-road crashes and
severity per the literature. OS does not publish curvature as an attribute;
neither does OSM cleanly (OSM node density is unreliable for curvature
derivation). OS Open Roads provides LineString geometry — survey-grade
accuracy, universal coverage — from which curvature can be computed by
resampling. Major win because it's universal coverage, no licensing, no
imputation.

**Decisions already made:**
- Resample geometry to fixed spacing (10–25m, TBD after vertex-density
  check), compute turning angle at each interior point, summarise per link.
- Features: `mean_curvature_deg_per_km`, `max_curvature_deg_per_km`, `sinuosity` (length /
  straight-line distance).
- Before committing: verify vertex density on OS Open Roads per road class.
  If Unclassified is sparsely vertexed, curvature feature will be near-zero
  noise on 1.06M links and should be flagged as minor-road-degraded.
- OS Open Roads simplifies at 1:25,000. Curvature values will be conservative
  relative to survey-grade. Acceptable for ranking purposes; document in
  methodology.

**Prompt:**

Pre-check step first:

1. Load `openroads_yorkshire.parquet` or current network parquet.
2. Compute `vertices_per_km` per link:
   `len(geometry.coords) / (length / 1000)`.
3. Summarise by `road_classification` using `describe()`.
4. Report the distribution.

Based on the vertex density result, propose either:

1. Compute curvature features across all road classes as a universal-coverage
   feature.
2. Compute curvature only on classes where vertex density is adequate
   (threshold TBD from the data); flag as NaN for others.

Then implement the chosen path:

1. Resample each LineString to 15m spacing (tunable).
2. Compute turning angle per interior sample point.
3. Per-link features:
   - `mean_curvature_deg_per_km`
   - `max_curvature_deg_per_km`
   - `sinuosity` (`link_length / straight_line_length`)
4. Add to `network_features.parquet` as new columns.
5. Report how many links get non-null curvature values and distribution.

Do not retrain the collision model yet. This is feature engineering only.

**Expected outcomes:**
- Universal or near-universal coverage depending on vertex density.
- Curvature features rank links sensibly even if absolute values are
  conservative (OS Open Roads simplification).
- Adds the geometric risk signal missing from current feature set.

---

