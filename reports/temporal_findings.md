# Temporal findings

Working document. Updated as analysis progresses.

## Summary

WebTRIS data supports one link-level temporal descriptor (`core_overnight_ratio`)
and two global temporal patterns (monthly seasonal index, weekday/weekend
ratio). Link-level modelling of weekday/weekend or month-of-year variation is
not supported by the data — variation across sites within those axes is too
tight to model meaningfully.

HGV percentage is the one axis with an unresolved verdict. Boxplot evidence
suggests possible within-road-class variation, but the per-site within-month
std test (the same diagnostic that settled weekday/weekend) has not been run.
Pending.

## Findings

### 1. Time-of-day variation is link-specific and substantial

`core_overnight_ratio` (flow per hour during 07:00–18:59 ÷ flow per hour
during 00:00–06:00) varies by ~3–4× across WebTRIS sites:

| Stat | Value |
|------|------:|
| Median | 7.07 |
| IQR | 5.68 to 9.14 |
| 5th–95th percentile | 4.19 to 15.18 |
| Max | 91.56 |

This is genuine link-specific variation. Site-by-site differences are large
enough that a feature-based model has something to predict. The current
time-of-day model (`timezone_profile.py`) achieves CV R² ≈ 0.65 on
`core_daytime_frac`, suggesting network features capture much of this
variation.

**Status:** worth taking forward to ablation. Question is whether it adds
lift over road class in the collision model.

### 2. Weekday/weekend variation is global, not link-specific

Per-site, per-month standard deviation of `weekday_weekend_ratio`
(`awt24hour / adt24hour`) across the WebTRIS network:

| Month | Std |
|-------|----:|
| Jan | 0.032 |
| Feb | 0.033 |
| Mar | 0.028 |
| Apr | 0.038 |
| May | 0.028 |
| Jun | 0.032 |
| Jul | 0.044 |
| Aug | 0.029 |
| Sep | 0.033 |
| Oct | 0.030 |
| Nov | 0.030 |
| Dec | 0.038 |

Mean across-site std ≈ 0.033. Mean ratio ≈ 1.08.

The mean ratio is approximately constant across road types:

| Road type | Mean | Std |
|-----------|-----:|----:|
| Motorway | 1.073 | 0.022 |
| A-road | 1.076 | 0.014 |
| Other | 1.085 | 0.028 |

90% of sites fall between ratios of 1.045 and 1.125. A link-level model
cannot recover meaningful site-specific signal from this — the variation is
too tight relative to the mean.

**Status:** parked at link grain. The global mean (~1.08) is a usable
constant if needed elsewhere.

### 3. Seasonal variation is global, not link-specific

Monthly `seasonal_index` values (mean monthly flow ÷ annual mean flow), by
road type:

| Month | A-road | Motorway | Other |
|-------|-------:|---------:|------:|
| Jan | 0.829 | 0.837 | 0.837 |
| Feb | 0.910 | 0.923 | 0.913 |
| Mar | 0.947 | 0.941 | 0.948 |
| Apr | 0.976 | 0.964 | 0.985 |
| May | 0.999 | 0.993 | 1.013 |
| Jun | 1.051 | 1.050 | 1.060 |
| Jul | 1.070 | 1.074 | 1.070 |
| Aug | 1.076 | 1.094 | 1.084 |
| Sep | 1.084 | 1.079 | 1.074 |
| Oct | 1.068 | 1.073 | 1.058 |
| Nov | 1.043 | 1.035 | 1.031 |
| Dec | 0.949 | 0.937 | 0.931 |

Road-type values are within ±0.02 of each other in every month. The
seasonal pattern is real (~30% swing from January trough to August peak)
but **the same shape applies to every road type**.

**Status:** parked at link grain. The global monthly multipliers are usable
if temporal collision modelling is ever pursued, but in an annual-grain
collision model a uniform monthly multiplier doesn't change link rankings.

### 4. HGV: unresolved, with a denominator artefact in the seasonal pattern

HGV percentage by road type and month (`mean_large_pct` from
`temporal_profiles.parquet`):

| Month | A-road | Motorway | Other |
|-------|-------:|---------:|------:|
| Jan | 17.51 | 17.10 | 14.41 |
| Apr | 15.63 | 15.34 | 12.97 |
| Aug | 14.37 | 14.26 | 11.88 |
| Dec | 13.89 | 13.86 | 11.55 |

Two patterns:

**Seasonal HGV% drop is largely a denominator artefact, not a freight
pattern.** HGV% drops ~3pp from winter to summer across all road types.
Over the same period, total flow rises ~30% (finding 3 above). HGV
volume is therefore roughly stable across seasons — passenger traffic
surges in summer and dilutes the ratio. This means HGVs are *less*
seasonal than passenger traffic, not more. Useful to know for
interpretation; doesn't on its own suggest link-specific signal.

**Within-road-class spread visible in boxplots is wider than weekday/
weekend showed.** IQRs of HGV% within each road type span ~10 percentage
points; outliers reach 40–70%. Some of this is genuine site differences
(truck-heavy industrial corridors), some is noise from low-flow sites
where the ratio becomes unstable. Whether the genuine variation is large
enough to model — and adds anything beyond road class — is the question
the per-site within-month std test would answer. Not run yet.

**HGV% vs HGV volume.** HGV% is the more direct feature for a model: a
30%-HGV link is meaningfully different from a 5%-HGV link regardless of
total volume, and severity-relevant features tend to track proportion
rather than absolute count. HGV volume is the cleaner descriptor for
*understanding the data* — it separates "freight-heavy road" from
"low-flow road with a few trucks" — but is more redundant with road
class for modelling. If HGV is taken to ablation, % is the feature; volume
is for diagnostics only.

**Status:** pending per-site within-month std check on
`adt24largevehiclepercentage`. If std is tight (say <2 pp), park for the
same reason as weekday/weekend. If wider (5+ pp), candidate for ablation
alongside `core_overnight_ratio`.

## Caveats

### WebTRIS coverage skew

WebTRIS sensors are concentrated on the National Highways network —
motorways and major A-roads. Findings 2 and 3 (no link-specific weekday/
weekend or seasonal variation) reflect the homogeneity of *this network*,
not necessarily of all UK roads. Minor roads, unclassified roads, and
school-route corridors might show different patterns, but they are
unobserved in WebTRIS and therefore unmodellable from this data source.

This means the "park" verdict is conditional: weekday/weekend and seasonal
descriptors at link grain *cannot be modelled from WebTRIS*. If they exist
on minor roads, this data source can't tell you.

### Predicted vs measured `core_overnight_ratio` gap

The applied `timezone_profile.py` model produces a network-wide median
`core_overnight_ratio` of 9.09 across 21M link predictions. Measured WebTRIS
sites have median 7.07. The 30% gap suggests one of:

- Minor roads (most of the predicted population) genuinely are more
  day-concentrated than the WebTRIS-measured network. Plausible — minor
  roads see proportionally less night traffic.
- The model extrapolates upward outside its training distribution. Also
  plausible.
- Some combination.

Worth investigating before relying on link-level predictions for the
collision-model ablation. Not blocking, but a known limitation.

### Latent issue: corridor fragmentation in `temporal.py`

`road_prefix = description[:4]` may fragment corridors when WebTRIS site
descriptions vary in formatting (e.g. "M62 ", "M62/", "M62E" treated as
separate prefixes). This is a pre-existing issue in `temporal.py` not
introduced by this work. Doesn't affect the verdicts above (which are
supported by per-site analysis as well as per-corridor) but should be
fixed if `temporal.py` output is used elsewhere.

## Implications for the temporal plan

- **Step 0 (band-labelling fix):** complete. Time-of-day bands renamed to
  reflect actual time periods.
- **Step 1 (link-level weekday/weekend model):** parked. Finding 2 above is
  the evidence.
- **Step 1b (HGV per-site std check):** new, replaces the original
  weekday/weekend step. Cheap diagnostic to settle finding 4. Outcome
  determines whether HGV joins the ablation.
- **Step 2 (leakage check for `core_overnight_ratio`):** still required.
- **Step 3 (collision-model ablation):** runs with `core_overnight_ratio`
  plus a road-class proxy baseline. HGV% added if step 1b clears.
- **Step 4 (month/seasonal at link grain):** parked. Finding 3 is the
  evidence.

The remaining ablation question is narrow: do these descriptors carry
information beyond what road class and existing network features already
give the collision model? Prior is moderate for `core_overnight_ratio`
(real variation but features that drive its prediction overlap with
features already in the collision model) and uncertain for HGV% (depends
on step 1b outcome).

## Updates

*Add new findings below as analysis continues.*