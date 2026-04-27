## TODO.md:

[ ] Stage 1b integration decision — keep timezone_profiles.parquet as a separate temporal output for now, then run an ablation before using time-zone fractions as Stage 2 exposure weights. This prevents the current all-day risk ranking and future temporal-risk ranking from being mixed accidentally.

## README.md

**Stage 1b — Time-zone profiles**  
Uses WebTRIS National Highways sensor reports to learn within-day traffic
shape (peak / pre-peak / off-peak fractions). The cleaned WebTRIS table is
sparse by design: current local data has 15,011 site × year rows from 5,948
sensor sites for 2019, 2021, and 2023. The profile model then applies those
learned fractions to all links using estimated AADT and network features,
producing `timezone_profiles.parquet`. These profiles are currently a
separate output for temporal analysis and future exposure weighting; they are
not part of the current Stage 2 collision feature set.

## Future-work.qmd

### Temporal disaggregation of Stage 2

**What it is:** Move Stage 2 from link × year grain to link × year ×
time-bucket grain (e.g. month, day-of-week × hour block). Would use
Stage 1b temporal profiles as exposure-modifier infrastructure. Major
refactor of the collision model; not a feature addition.

**Why it's interesting:** Crash risk varies sharply by time of day
and day of week in ways the current annual model cannot represent.
Friday evenings and Saturday nights carry disproportionate risk; peak
commute hours concentrate motorway collisions; school-run windows
concentrate urban collisions near schools. A temporally disaggregated
model would produce rankings that identify *when* a link is risky,
not just which links are risky overall.

**Why not now:** Multi-session refactor requiring (a) Stage 1b to
move from diagnostic to production output, (b) temporal joins to be
rebuilt in Stage 2, (c) potentially different modelling approach
entirely (hierarchical Poisson with time random effects, or
stratified per time-bucket model). Also: today's rank stability work
suggests the current model has largely saturated what link-level
features can explain — temporal is a plausible candidate for
meaningful predictive lift beyond the current ceiling, but sizing
that claim requires research.

**Good starting point for someone else:**

- Deep-research pass on temporal disaggregation approaches in UK
  road safety literature. Specifically: how other STATS19-based
  analyses have handled time-of-day effects at link grain; whether
  hierarchical modelling or stratified models are preferred; what
  sample-size constraints per time-bucket apply.
- Scope out what Stage 1b would need to produce to feed temporal
  Stage 2.
- Design doc before implementation. Temporal work is methodology-
  heavy enough that a prompt can't carry it.

**Related:** Would pair naturally with weather warning analysis
(above) — temporal grain is the natural level for weather effects
to manifest.

## Chat Claude

7. The WebTRIS time-zone profile asset is oddly under-used. Stage 1b is built and runs but is labelled "diagnostic / future temporal weighting." Time-of-day exposure structure is exactly the kind of covariate that could meaningfully improve risk ranking on motorway/trunk sections where it's actually available. Neither ChatGPT nor I have flagged this — worth considering whether it earns its place in production rather than sitting parked.

Probably worth doing but with caveats
GIAS schools — Real signal but your current model is annual-grain. School-proximity effects are time-of-day (school-run windows) and calendar (term vs holiday). Without temporal disaggregation the feature becomes a static "near a school" flag, which partly duplicates urban/population-density signal you already have. Useful, but less additive than the source suggests until your Stage 1b temporal work is further along.