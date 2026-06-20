### Stage 3 — Conditional severity model (frequency–severity decomposition)

**Context:** Stage 2 predicts collision counts per link-year. A direct KSI
count model at link grain is not viable: ~7,400 fatals and a modest serious
count over 21.7M link-year rows is a zeros-on-zeros target with worse rank
stability than the current top-1% churn, and the pre-registered KSI atlas
diagnostic (`reports/ksi_reporting_consistency*.md`, parked) found
force/year severity-reporting instability that failed the adoption gate.

Instead: decompose. Keep Stage 2 unchanged as the frequency model and add a
**Stage 3 severity model at collision grain** — P(KSI | collision occurred) —
combined multiplicatively:

```
E[KSI per link-year] = E[collisions per link-year]  ×  P(KSI | collision on link)
        (Stage 2, unchanged)            (Stage 3, new)
```

This moves severity modelling from 21.7M sparse link-years to ~200k
collision rows with a ~15–25% positive rate, and separates where each known
data problem bites: slight under-reporting affects frequency level (ranking
already robust — exposure-adjusted, rank-based); CRaSH/COPA severity
misclassification affects only Stage 3, where the IBRS-only target (below)
addresses it.

**Cancellation property (supported by the adjusted Part A by-year table —
ratio drifts 0.226 → 0.289 over 2015–2024, partly growing slight
under-reporting):** slight under-reporting deflates E[N reported] and
inflates P(KSI | reported) by the same mechanism, so their product —
expected reported KSI — is approximately invariant to it, and reported
KSI ≈ true KSI because KSI (especially fatal) reporting is near-complete.
The combined target is therefore more robust to the dominant reporting
problem than either factor alone. Limit: this holds for network-wide
reporting trends, not force-specific under-reporting (neither model
carries force terms at inference) — hence the Staffordshire exclusion.

**This is not the parked KSI atlas and must not be positioned as having
passed the gate the atlas failed.** It is a different object — a conditional
severity propensity with explicit nuisance handling. Cite the parked
diagnostic as the design motivation in the writeup.

**Decisions already made:**

- **Precedent:** this is the HSM SPF + severity-distribution-function (SDF)
  two-stage structure. Comparison literature finds two-stage SDF accuracy
  similar to univariate per-severity SPFs and superior to fixed proportions,
  and specifically recommends it where severity samples are too small for
  direct severity-count models (our case). Known assumption to state in the
  methodology page: severity is conditionally independent of frequency given
  features; joint frequency-severity models exist but are out of scope for v1.
- **Target — primary spec: injury-based rows only.** The DfT adjusted
  probabilities are themselves outputs of a DfT logistic regression: for
  injury-based (IBRS) force-years the published adjusted values are the
  observed labels (exactly 0/1); for NIBRS force-years they are model
  predictions. Training on adjusted values across all rows means partially
  regressing on DfT's adjustment model rather than real-world severity —
  a circularity that distorts infrastructure coefficients invisibly.
  Primary spec therefore trains on `injury_based == 1` rows with observed
  KSI labels; adjusted-target-all-rows and recorded-target-all-rows are
  sensitivity runs. Session-1 check: IBRS share of study-area collisions
  2019–2024 (full GB adoption expected during 2026, so the share should be
  high but is not 100%).
- **Data note:** from the 2024 DfT publication, adjustment figures and the
  `injury_based` flag are included in the main collision/casualty tables
  rather than separate lookup files — the existing STATS19 ingest may
  already carry `collision_adjusted_severity_serious` / `_slight` and
  `collision_injury_based`. Verify before building anything.
- **Binary KSI vs slight,** not ordinal 3-class. The fatal/serious boundary
  is the least reliably recorded; fatal-only is too thin to model. Fatals
  are however the most completely reported outcome — use observed fatal
  share vs model-implied as an external consistency check, not a target.
- **Nuisance handling:** force (or force×year) effects in Stage 3,
  estimated but NEVER used for link prediction. Caveat to carry into the
  design: fixed effects absorb genuine geographic severity differences
  (rural forces really do have more severe collisions) along with reporting
  artefacts, and zeroing them at inference biases regional predictions.
  Candidates: (a) force FE, zeroed at inference — clean nuisance removal,
  accepts the regional bias; (b) force random effects / partial pooling —
  shrinks force effects toward zero in proportion to evidence, less signal
  destruction. Decide in session 1 after inspecting between-force severity
  variance on IBRS-only data; LOFO transfer is the arbiter either way.
  Note the IBRS-only primary target already removes the largest reporting
  artefact, so the nuisance term's job is smaller than in the atlas design.
- **Staffordshire: whole-force exclusion as primary spec.** The DfT-
  acknowledged under-reporting covers 2017–2023
  (`reports/staffordshire_data_quality.md`), but the adjusted Part A flags
  extend into 2024 because the recovery transient (506 → 883 → 1,493
  collisions) breaks year-on-year ratios on the way back up, and the
  severity mix of the reported subset during under-reporting is unknown.
  Matches the report's own recommendation that future KSI work exclude
  Staffordshire by default. 2017–2024-only exclusion as sensitivity.
- **Training window:** 2019–2024 primary; full-window-adjusted as
  sensitivity. Mirrors the reopening condition written in `todo/parked.md`,
  applied to a conditional model rather than the atlas.
- **Features: pre-event link features ONLY.** `FORBIDDEN_POST_EVENT_COLS`
  discipline applies with full force and is more tempting to violate here —
  the strong severity predictors (number_of_vehicles, light_conditions,
  vehicle types, casualty class) are all event attributes. None may enter
  the production model. Assert feature-list cleanliness pre-training, as
  Stage 2 does.
- **Expected performance:** infrastructure-only severity models show modest
  discrimination in the literature. The acceptable AUC band is NOT asserted
  here — setting it, with citations, is a session-1 pre-registration task
  (an earlier draft asserted 0.60–0.68 from general knowledge; treat that
  as unverified). The principle stands regardless: pre-register the band
  before fitting and do not let a leaky event feature rescue the headline.
  Speed-limit-effective and rural/urban expected to carry most of the
  signal (kinetic-energy story). Include `is_covid` — severity composition
  shifted in 2020–21 and the window includes it.
- **The deliverable is the re-ranking:** rural single-carriageway A-roads
  should rise in expected-KSI rank relative to urban links while collision
  frequency rank stays put. If expected-KSI top-1% ≈ collision top-1%, the
  model adds nothing — report that honestly.
- **Validation:** leave-one-force-out alongside the usual 5-seed harness.
  Cross-force transfer of P(KSI | collision) is the demonstration that the
  per-force nuisance handling worked — the claim a reviewer will probe.
- **Output:** new columns on a separate parquet
  (`risk_scores_severity.parquet`), production `risk_scores.parquet`
  unchanged — same pattern as EB and family-split. Adoption into production
  ranking is a separate, later decision with its own gate.

**Pre-registration (write before implementation, same discipline as the
KSI atlas and temporal-descriptor work):**

- Primary metric: held-out AUC (link-grouped split) against a band set with
  citations during pre-registration, plus calibration (reliability curve,
  slope/intercept) on the IBRS observed-label target.
- Leave-one-force-out AUC spread — pre-set an acceptable range.
- Rank-divergence report: Jaccard and Spearman between collision top-1%
  and expected-KSI top-1%; composition shift by road class and RUC.
  Divergence is expected and desired — pre-state the direction
  (rural high-speed up, urban low-speed down) so the result is a test,
  not a story fitted afterwards.
- Sensitivity grid: {IBRS-only observed vs adjusted-all-rows vs
  recorded-all-rows target} × {Staffordshire whole-force excluded vs
  2017–2024 excluded} × {2019–2024 vs full window}. Conclusions must be
  stable across the grid or the instability reported.

**Prompt:**

[Draft when ready. Session 1 should be design-doc + data-prep only, no
model: verify whether the current STATS19 ingest already carries
`collision_injury_based` and the adjusted-severity columns (in main tables
since the 2024 publication); build the collision-grain training table
(snapped collisions with score ≥ 0.6, joined to link features via link_id);
report IBRS share by force/year for the study area; cross-check positive
rate by force/year against the atlas diagnostic's flagged rows; set the
AUC band with citations; choose FE vs partial pooling from between-force
variance on IBRS data; write the pre-registration. Session 2: fit (logistic
GLM for interpretability + gradient boosting comparison, same dual-model
pattern as Stage 2), LOFO validation, rank-divergence report. Session 3:
Quarto methodology page + writeup. Memory note: collision-grain table is
small (~200k rows); no chunking needed for training, but scoring P(KSI)
onto 2.17M links reuses the Stage 2 chunked-scoring path.]

**Expected outcomes:**

- A defensible expected-KSI ranking layer without claiming the parked KSI
  atlas gate was passed.
- Meaningful but modest discrimination, assessed against the pre-registered
  AUC band set with citations before fitting.
- Top-1% re-ranking toward rural high-speed single carriageways — the
  substantive output.
- If LOFO transfer fails or sensitivity-grid conclusions flip, that is a
  real signal the force-level reporting problems leak into the conditional
  model too — park again with the evidence, same as the atlas.

**Dependencies / sequencing:**

- Independent of facility-family v2, NHNM, and the memory-strategy decision
  (training table is small; scoring reuses existing chunked path).
- Wants the `mean_grade` sign investigation done first or alongside —
  grade enters Stage 3 as a candidate feature and an unexplained
  wrong-sign coefficient in Stage 2 will resurface in review of both.
- Uses published DfT severity-adjustment data. The separate lookup files
  used for the adjusted Part A rerun may no longer be needed if the ingest
  already carries the in-table columns — verify in session 1.
- **EB layer incompatibility** (per the adjusted Part A report's caveats):
  the current EB shrinkage assumes observed integer counts. If expected-KSI
  output ever gets an EB treatment, it must be re-derived for an
  expected-count target, not applied as a drop-in. Out of scope for v1;
  noted so it is not done casually later.
- **Gate question resolved (13 June 2026), with one condition.** The 15
  flags surviving the adjusted Part A diagnostic decompose as: 6 in
  2016–2018 (CRaSH/COPA transition era — outside the 2019–2024 window);
  5 in 2019–2020 (Cumbria, Durham, Humberside, Suffolk, Cambridgeshire —
  upward steps consistent with IBRS adoption-year boundaries, which an
  IBRS-only training set never compares across; Humberside's downward
  step is the anomaly to inspect); 4 Staffordshire 2021–2024 (collision
  under-reporting + recovery transient — handled by exclusion, see below).
  **Session-1 verification and kill condition:** tabulate
  `collision_injury_based` by force/year, overlay the 15 flags. If any
  flag sits within a continuous IBRS period (Humberside 2019 the prime
  suspect), the IBRS-only design fails its premise — stop and revisit
  before any fitting.

---
