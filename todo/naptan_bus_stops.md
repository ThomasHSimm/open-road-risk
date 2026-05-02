### NaPTAN bus stops — buffer features

**Context:** Bus stops are conflict generators — braking, overtaking,
pedestrian density. DfT NaPTAN is open, point data, GB-wide. Simple buffer-
count feature per link.

**Decisions already made:**
- Features: `n_bus_stops_50m` (count in 50m buffer), `has_bus_stop`
  (binary flag).
- Buffer distance tunable; 50m is literature-informed starting point.
- Straightforward computation; no licensing or coverage issues.

**Prompt:**
[Draft. Download NaPTAN bus stop data, compute per-link buffer counts at
50m (and optionally 100m for comparison), add features to
network_features.parquet. Retrain Stage 2 and report.]

**Expected outcomes:**
- Modest pseudo-R² improvement (0.005–0.02).
- Likely higher feature importance on urban A-roads and B-roads than on
  motorways or rural classes.

---

