# Temporal features plan

## Problem

The collision model produces per-link annual risk scores. Crash timestamps
from STATS19 are already used on the collision side. The question is whether
the temporal traffic models (currently producing time-zone fractions per
link, plus a corridor-level monthly profile) earn a place in the production
collision model.

The previous framing — "use temporal fractions as exposure weights" —
overcommits. Producing flow conditional on time-of-day × day-of-week × month
× year per link is a combinatorial blowup with stacked prediction error,
and WebTRIS coverage (motorways and major A-roads only) means most of those
conditional flows would be extrapolated.

The collision model already has crash timestamps. It does not need a
conditional exposure denominator to learn time-conditioned effects. It needs
to know the *shape* of each link's traffic distribution.

## Approach

Rescope the temporal work from "produce conditional flows" to "produce
link-level shape descriptors."

- Exposure denominator stays as annual AADT. Unchanged.
- Each temporal model produces one number per link summarising one axis
  of temporal distribution.
- Collision model takes those numbers as features alongside its existing
  features and learns time-conditioned risk against the annual denominator.

Bounds the consequence of WebTRIS coverage error: a noisy feature can be
downweighted by the collision model; a biased denominator cannot.

## Existing state

Two temporal pipelines are already built:

- `timezone_profile.py` — link-level model, predicts four time-of-day
  fractions per OS Open Roads link × year, trained on WebTRIS, output
  `timezone_profiles.parquet`. Produces `peak_offpeak_ratio` directly.
- `temporal.py` — corridor-level model, aggregates to road-prefix × month,
  produces `seasonal_index` and `weekday_weekend_ratio`. Output
  `temporal_profiles.parquet`. Not at link grain.

Two known problems with the existing state:

1. **Band labels are wrong in `timezone_profile.py`.** The differencing of
   cumulative WebTRIS windows (12h/16h/18h/24h) does not produce the time
   periods the column names claim. WebTRIS windows are not nested at a
   common start point — they have different start times (00, 06, 06, 07).
   Actual bands produced by current differencing logic:

   | Code label | True period | Hours |
   |------------|-------------|------:|
   | `peak_frac` | 07:00–18:59 | 12 |
   | `prepeak_frac` | 06–07 + 19–22 (mixed shoulder) | 4 |
   | `preoffpeak_frac` | 22:00–24:00 | 2 |
   | `offpeak_frac` | 00:00–06:00 | 6 |

   `peak_frac` is correct; the other three are mislabelled. The "evening
   pre-peak" band is actually a mix of early morning and evening shoulder,
   which is information-destroying for any commuter-vs-leisure narrative.

2. **Weekday/weekend is at corridor grain, not link grain.** `temporal.py`
   produces `weekday_weekend_ratio` per road prefix, defined as
   `awt24hour / adt24hour` (bounded ~1 to 1.4). Not directly usable as a
   link feature.

## Sequence

### Step 0 — Fix band labels and re-run time-of-day model

**Complete.** Time-of-day bands renamed in cleaning code and
`timezone_profile.py`: `core_daytime_frac` (07:00–18:59), `shoulder_frac`
(06–07 + 19–22), `late_evening_frac` (22:00–24:00), `overnight_frac`
(00:00–06:00). `peak_offpeak_ratio` renamed to `core_overnight_ratio`.
Model re-run; CV R² values consistent with pre-rename: 0.65 / 0.63 /
0.46 / 0.54 for the four fractions.

### Step 1 — Build link-level weekday/weekend model

**Parked.** Per-site within-month standard deviation of weekday/weekend
ratio is ~0.03 across all months around a mean of 1.08. Mean is
essentially identical across road types (motorway 1.073, A-road 1.076,
other 1.085). 90% of sites fall between 1.045 and 1.125. The descriptor
has no link-specific variation a model could recover. See temporal_findings.md
finding 2 for evidence. Same logic parks seasonal/month at link grain
(finding 3).

### Step 1b — HGV per-site within-month std check

**Complete.** This step replaces the original step 1.

Boxplot evidence in the temporal exploration qmd showed substantial
within-road-class spread in HGV percentage (IQRs ~10pp, outliers
40–70%). The follow-up diagnostic confirmed that the spread is not just a
plotting artefact.

The diagnostic ran the same per-site within-month std check on
`adt24largevehiclepercentage` that settled weekday/weekend:

```python
profile = (
    raw.groupby(["site_id", "monthname"], observed=True)
    .agg(mean_hgv_pct=("adt24largevehiclepercentage", "mean"))
    .reset_index()
)
print(profile.groupby("monthname", observed=True)["mean_hgv_pct"].std())
```

Result:

- 6,003 study-area WebTRIS sites; 68,159 site-month rows.
- Median monthly within-month-across-sites std: 7.19 percentage points.
- Monthly std range: 6.50–8.17 percentage points.
- Site-mean HGV% 10th/50th/90th percentiles: 7.68%, 18.02%, 25.72%.
- 3.0% of sites average at least 30% HGV; 0.37% average at least 40%.

Decision rule and outcome:
- **Tight (<2 percentage points within-month-across-sites):** park.
  Variation is dominated by road class, which is already in the
  collision model.
- **Wide (5+ percentage points):** candidate for ablation alongside
  `core_overnight_ratio`. **This is the observed outcome.**
- **In between:** judgement call — examine the distribution shape and
  whether it has a heavy tail of genuinely freight-heavy sites that
  carry signal road class can't capture.

Note on feature choice for ablation if HGV clears: use HGV % rather than
HGV volume. % captures "freight-heavy character of this link" which is
what would matter for collision risk; volume is more redundant with road
class (motorways carry more freight in absolute terms by definition) and
useful mainly as a diagnostic for understanding the data.

Supporting artefacts:

- `src/road_risk/diagnostics/temporal_hgv_variation.py`
- `reports/supporting/temporal_hgv_monthly_std.csv`
- `reports/supporting/temporal_hgv_site_month_profile.csv`
- `reports/supporting/temporal_hgv_road_type_summary.csv`

### Step 2 — Confirm leakage geometry

Check whether any links in the collision model's evaluation folds
correspond to WebTRIS sites used to train either temporal model. If so,
descriptors for those links are in-sample predictions and will inflate
collision-model CV results.

Either align folds by site or document the optimism explicitly.

### Step 3 — Run the collision-model ablation

Three configurations, same folds, same seed:

- Post-grade collision model, scored with the chunked path.
- Post-grade + `core_overnight_ratio` + HGV%.
- Post-grade + cheap proxy (e.g. road class × urban density interaction, or
  whatever the existing feature set can encode of the same idea).

Compare headline CV metric with confidence intervals from resampling.

Decision rule: pre-registered, TBD — to be set before results are seen.
The threshold needs to sit above the noise floor of the post-grade collision
model's CV. Re-measure that noise floor on the post-fix training population
before setting the decision threshold, because the IMD/grade imputation
refactor changed the GLM estimation sample and the chunked scoring path
changed the operational scoring implementation.

Three possible verdicts:

- Descriptors clearly beat both baselines → adopt in production.
- Descriptors match the cheap proxy → do not adopt; the information was
  already available from existing features.
- Descriptors do not beat the post-grade baseline → do not adopt; park the
  temporal models honestly.

### Step 4 — Month / seasonality

Only if step 3 passes for the time-of-day and weekday/weekend descriptors,
and there is headroom.

`temporal.py` already produces `seasonal_index` at corridor grain. Lower
priority per project goals. Two paths:

- Coarse: spatial-join the corridor-level `seasonal_index` to OS Open Roads
  links by road name. Every link on a corridor gets the same value. Weak
  but cheap.
- Link-level: build a third model mirroring step 1 for a per-link seasonal
  amplitude target. More work; defer unless step 3 results suggest seasonal
  signal is worth pursuing.

Defer the choice until step 3 results are in.

## Out of scope

- Conditional exposure flows (peak × weekday × month × year per link). The
  combinatorial blowup is the reason this plan exists.
- Changing the collision model's grain or architecture.
- Changes to the AADT exposure model.
- School proximity, weather, or any non-temporal features.

## Risks and unknowns

- **Band-labelling fix has cascading effects.** Column names change,
  `timezone_profiles.parquet` schema changes, the qmd narrative changes,
  any downstream code consuming `prepeak_frac` etc. needs updating. Larger
  scope than a renaming.
- **Leakage between WebTRIS sites and collision-model test folds is
  unverified.** Step 2 is a real gate.
- **Cheap-proxy baseline is loosely specified.** Whatever proxy is chosen
  determines whether the comparison is meaningful. If the proxy is too
  weak, descriptors will appear to add value they do not.
- **IMD/grade features may absorb urban-character signal.** Those features
  may capture part of the same spatial/urban structure that previously gave
  `core_overnight_ratio` apparent lift. Check feature overlap before running
  the ablation.
- **Pre-registered decision rule is not yet set.** Must be set before
  step 3 results are inspected.
- **R² values currently quoted in `timezone-profile.qmd` are stale and
  attached to mislabelled targets.** They should not be cited in the plan
  or anywhere else until step 0 is complete.

## Effort

Step 0: one focused session. Mostly mechanical (rename, re-run, update
narrative), but the cascade through dependent code is the unknown.

Step 1: one focused session. New target, existing architecture, no new
data pulls.

Step 2: short check, possibly extending if leakage is real.

Step 3: one focused session given a working evaluation harness.

Step 4: deferred decision.

Total: probably 3–4 focused sessions to a go/no-go verdict on the
descriptors.

## What this plan replaces

The previous file mixed three different scopes — keep-as-diagnostic,
adopt-as-features, full temporal disaggregation. This plan is one scope:
measure whether link-level shape descriptors earn a place in the existing
annual collision model, with the band-labelling bug fixed first as a
prerequisite. Other scopes (conditional exposure, temporal grain change,
additional non-temporal features) are not addressed here and should be
decided separately.
