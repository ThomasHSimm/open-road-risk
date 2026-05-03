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

The temporal ablation is now complete. Two configurations were tested against
the post-fix baseline using a pre-registered adoption rule:

- pseudo-R² improvement > `0.009` over baseline, and
- test deviance reduction > `0.6%`,

with improvement required on at least `4/5` seeds.

Verdict: both temporal descriptors are **real but below threshold**. Both
configurations produce small, consistent improvements. Config C
(`core_overnight_ratio` + WebTRIS HGV%) improves pseudo-R² by about `0.006`
and reduces test deviance by about `0.85%` across all 5 seeds. Those gains are
statistically detectable and reproducible, but they do not clear the
pre-registered adoption bar because pseudo-R² improvement stays below `0.009`
on every seed. Config C narrowly clears the deviance criterion but fails the
pseudo-R² criterion on every seed. Config B is smaller again. The descriptors
therefore carry real but marginal signal: not redundant with the existing
feature set, but not large enough to justify additional pipeline complexity at
the pre-registered threshold.

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

**Status:** real but below threshold. The descriptor adds small, consistent
signal in the collision-model ablation, but not enough to clear the
pre-registered adoption rule. Parked unless project priorities or the
underlying time-zone model change.

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

### 4. HGV percentage has link-specific variation and was worth ablating

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

**Status:** real but below threshold. Stage 2 already includes AADF-derived
`hgv_proportion`, so the ablation only remained meaningful if it used a
genuinely distinct WebTRIS-derived HGV descriptor. That check was passed, and
the WebTRIS HGV descriptor produced small reproducible lift in config C, but
not enough to meet the pre-registered adoption rule. If revisited in future,
use HGV percentage rather than HGV volume. Supporting
CSVs are `reports/supporting/temporal_hgv_monthly_std.csv`,
`reports/supporting/temporal_hgv_site_month_profile.csv`, and
`reports/supporting/temporal_hgv_road_type_summary.csv`.

### 5. Temporal descriptor leakage geometry is real but bounded

Step 2 checked whether WebTRIS sites used by the temporal pipelines snap to
Open Roads links that are in the Stage 2 collision-model held-out fold. The
diagnostic reproduces the seed-42 `GroupShuffleSplit` over `link_id`, then
snaps WebTRIS sites to their nearest Open Roads link within 2 km.

| Site population | Sites | Snapped links | Sites on held-out links | Held-out links with sites | Share |
|---|---:|---:|---:|---:|---:|
| `timezone_profile.py` training | 5,946 | 3,625 | 1,246 | 736 | 21.0% |
| Raw temporal/HGV profiles | 6,003 | 3,640 | 1,255 | 737 | 20.9% |
| Union | 6,003 | 3,640 | 1,255 | 737 | 20.9% |

The overlap is close to the expected 20% from a random link split, but it is
still leakage geometry: for those held-out collision links, temporal
descriptors would be predictions from a temporal model trained on the
corresponding WebTRIS site. The temporal ablation should either align folds,
exclude the 737 WebTRIS-snapped held-out links from the score comparison, or
report the result as mildly optimistic for that subset.

Supporting CSVs are `reports/supporting/temporal_leakage_summary.csv` and
`reports/supporting/temporal_leakage_site_link_map.csv`.

### 6. Existing post-grade features partly explain `core_overnight_ratio`

Step 3 prep checked whether the temporal descriptor mostly duplicates the
current Stage 2 feature surface. A `HistGradientBoostingRegressor` was trained
to predict link-level mean `core_overnight_ratio` from existing non-temporal
features, using a 300k-link sample.

| Feature set | Features | R² | MAE | Target std |
|---|---:|---:|---:|---:|
| Road context | 12 | 0.066 | 2.053 | 2.799 |
| Urban/IMD/grade | 9 | 0.232 | 1.864 | 2.799 |
| Full post-grade Stage 2 feature surface | 25 | 0.363 | 1.682 | 2.799 |

The overlap is material but not saturating. Current features can recover about
36% of the variation in `core_overnight_ratio`, which supports keeping a
cheap-proxy/overlap baseline in the ablation. It does not by itself prove the
temporal descriptor is redundant.

Top single-feature Spearman correlations are modest: `degree_mean` 0.151,
`speed_limit_mph_effective` 0.148, `lanes` −0.133, `hgv_proportion` −0.082,
`is_primary` −0.060, and `mean_grade` −0.050. The descriptor is therefore not
just a one-column proxy, but it does encode some urban/network character.

The prep also audited the rank-stability artefacts. At prep time, the existing
files were stale for the post-grade noise floor: `rank_stability_provenance.json`
recorded GLM pseudo-R² 0.301 and 20 GLM features, while the current post-grade
model recorded GLM pseudo-R² 0.347 and 32 GLM features. That issue was
subsequently resolved by the post-fix rank-stability rerun used for the final
ablation threshold.

Supporting CSVs are
`reports/supporting/temporal_feature_overlap_summary.csv`,
`reports/supporting/temporal_feature_overlap_correlations.csv`, and
`reports/supporting/temporal_noise_floor_artifact_audit.csv`.

### 7. Collision-model ablation result

The post-fix Stage 2 model was re-run across seeds `42-46` under three
configurations:

- `A`: baseline
- `B`: baseline + `core_overnight_ratio`
- `C`: baseline + `core_overnight_ratio` + WebTRIS HGV%

Primary comparison excluded the `737` held-out links that snap to WebTRIS
sites. A full-fold sensitivity comparison was also reported separately.

Pre-registered decision rule:

- pseudo-R² improvement > `0.009` over baseline, and
- test deviance reduction > `0.6%`,

with improvement required on at least `4/5` seeds. Mixed results across only
`1-3` seeds count as null.

Observed result:

- Config `B`: pseudo-R² improvement `0.0036-0.0045`; deviance reduction
  `0.53%-0.66%`; verdict `null`
- Config `C`: pseudo-R² improvement `0.0056-0.0063`; deviance reduction
  `0.82%-0.92%`; verdict `null`

Both configurations produce small, consistent improvements. Config C is the
stronger of the two: about `0.006` pseudo-R² and `0.85%` deviance reduction
across all 5 seeds. The gains are reproducible, so the descriptors are not
redundant with the existing feature surface, but they still fall below the
pre-registered adoption threshold. Config C narrowly clears the deviance
criterion and fails the pseudo-R² criterion on every seed.

Operationally, the descriptors move rankings but not dramatically enough to
justify production complexity at the agreed bar. Top-1% Jaccard versus the
baseline is about `0.764` for config B and `0.751` for config C, indicating
real reshuffling without enough headline lift to warrant adoption.

Supporting outputs:

- `reports/supporting/temporal_ablation_results.csv`
- `reports/supporting/temporal_ablation_summary.md`

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

Worth investigating before relying on link-level predictions for any future
temporal revisit. Not blocking for the completed ablation, but still a known
limitation.

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
  5+ percentage-point variation threshold, but Stage 2 already includes
  AADF-derived `hgv_proportion`; only a distinct WebTRIS-derived HGV
  descriptor should join the ablation.
- **Step 2 (leakage check for `core_overnight_ratio`):** complete. Finding 5
  confirms fold overlap, so Step 3 must align/exclude affected links or
  document the optimism.
- **Step 3 prep:** complete. Feature-overlap check ran; post-fix
  rank-stability rerun established the honest baseline and noise floor.
- **Step 3 (collision-model ablation):** complete. Both descriptor
  configurations produced small, reproducible lift but failed the
  pre-registered adoption rule. Verdict: parked as "real but below
  threshold."
- **Step 4 (month/seasonal at link grain):** parked. Finding 3 is the
  evidence.

Temporal work is therefore complete for the current scope. The descriptors
may be worth revisiting only if the adoption threshold is intentionally reset
because project priorities change, or if the underlying time-zone/HGV models
improve materially. They should not be revisited at the same threshold based
on the current results.

## Updates

*Add new findings below as analysis continues.*
