# Temporal findings

Working document. Updated as analysis progresses.

## Summary

WebTRIS data supports one link-level temporal descriptor (`core_overnight_ratio`)
and two global temporal patterns (monthly seasonal index, weekday/weekend
ratio). Link-level modelling of weekday/weekend or month-of-year variation is
not supported by the data — variation across sites within those axes is too
tight to model meaningfully.

HGV percentage clears the link-specific variation gate. The per-site
within-month std test gives a median across-month std of 7.19 percentage
points, with every month between 6.50 and 8.17 points. That is much wider
than weekday/weekend variation and supports taking HGV% to the collision-model
ablation alongside `core_overnight_ratio`.

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

### 4. HGV percentage has link-specific variation and should be ablated

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

**Per-site within-month spread is wide enough to model.** The step 1b
diagnostic groups raw WebTRIS rows to site × month, then computes the standard
deviation of site-level mean HGV% within each month. This is the same logic
used to park weekday/weekend variation. HGV% is not tight:

| Month | Sites | Mean HGV% | Std, pp | q10 | q90 | Max |
|---|---:|---:|---:|---:|---:|---:|
| Jan | 5,700 | 18.91 | 8.17 | 7.93 | 28.57 | 57.60 |
| Feb | 5,752 | 18.60 | 7.93 | 8.03 | 28.03 | 58.30 |
| Mar | 5,758 | 18.52 | 7.88 | 8.09 | 27.85 | 58.80 |
| Apr | 5,688 | 17.16 | 7.28 | 7.55 | 25.80 | 58.10 |
| May | 5,666 | 16.87 | 7.21 | 7.46 | 25.39 | 69.60 |
| Jun | 5,660 | 16.77 | 7.05 | 7.53 | 25.10 | 63.50 |
| Jul | 5,622 | 16.64 | 6.95 | 7.60 | 24.61 | 67.60 |
| Aug | 5,623 | 15.69 | 6.50 | 7.27 | 23.15 | 69.60 |
| Sep | 5,670 | 16.55 | 6.81 | 7.43 | 24.55 | 58.60 |
| Oct | 5,688 | 17.03 | 7.16 | 7.51 | 25.30 | 69.10 |
| Nov | 5,670 | 17.59 | 7.44 | 7.63 | 26.40 | 62.70 |
| Dec | 5,662 | 15.58 | 6.77 | 6.60 | 23.50 | 62.35 |

Median monthly std is 7.19 percentage points; range is 6.50–8.17. This clears
the temporal plan's 5+ percentage-point threshold for taking HGV% to ablation.

Site-mean HGV% also has a real high-HGV tail. Across 6,003 study-area sites,
the 10th/50th/90th percentiles are 7.68%, 18.02%, and 25.72%; 3.0% of sites
average at least 30% HGV and 0.37% average at least 40%.

| Road type | Sites | Mean HGV% | Std, pp | q10 | q90 | Max |
|---|---:|---:|---:|---:|---:|---:|
| A-road | 802 | 19.97 | 5.97 | 10.48 | 26.07 | 34.82 |
| Motorway | 3,631 | 18.73 | 6.64 | 9.27 | 26.57 | 57.04 |
| Other | 1,570 | 12.64 | 6.88 | 5.49 | 21.82 | 58.28 |

**HGV% vs HGV volume.** HGV% is the more direct feature for a model: a
30%-HGV link is meaningfully different from a 5%-HGV link regardless of
total volume, and severity-relevant features tend to track proportion
rather than absolute count. HGV volume is the cleaner descriptor for
*understanding the data* — it separates "freight-heavy road" from
"low-flow road with a few trucks" — but is more redundant with road
class for modelling. If HGV is taken to ablation, % is the feature; volume
is for diagnostics only.

**Status:** candidate for ablation alongside `core_overnight_ratio`. Use HGV
percentage, not HGV volume, as the modelling descriptor. Supporting CSVs are
`reports/supporting/temporal_hgv_monthly_std.csv`,
`reports/supporting/temporal_hgv_site_month_profile.csv`, and
`reports/supporting/temporal_hgv_road_type_summary.csv`.

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
- **Step 1b (HGV per-site std check):** complete. Finding 4 clears the
  5+ percentage-point threshold, so HGV% joins the ablation candidate set.
- **Step 2 (leakage check for `core_overnight_ratio`):** still required.
- **Step 3 (collision-model ablation):** runs with `core_overnight_ratio`,
  HGV%, and a road-class proxy baseline.
- **Step 4 (month/seasonal at link grain):** parked. Finding 3 is the
  evidence.

The remaining ablation question is narrow: do these descriptors carry
information beyond what road class and existing network features already
give the collision model? Prior is moderate for `core_overnight_ratio`
(real variation but features that drive its prediction overlap with
features already in the collision model) and now moderate for HGV% (real
within-month site variation, but still to be tested against existing road
class and network features).

## Updates

*Add new findings below as analysis continues.*
