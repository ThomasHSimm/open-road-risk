# Facility-family split: family definition

## Decision

V1 of facility-family Stage 2 modelling uses four families:

1. **Motorway** — `road_function == "Motorway"`
2. **Trunk A-road** — `road_function == "A Road"` AND `is_trunk == True`
3. **Other-Urban** — neither of the above, AND ONS RUC indicates urban
4. **Other-Rural** — neither of the above, AND ONS RUC indicates rural

Links with no ONS RUC assignment (~15.5% of the network) are
characterised separately before the v1 spec is finalised and either
assigned by spatial-join fallback or to a default family.

`form_of_way` (single carriageway, dual carriageway, roundabout, slip
road) and `is_primary` are kept as features within each per-family
model. They are not used to define families.

## Source data

OS Open Roads. Each link has:

- `road_function`: principled functional categorisation (Motorway,
  A Road, B Road, Local Road, Minor Road, Restricted Local Access
  Road, Local Access Road, Secondary Access Road).
- `is_trunk`: boolean. National Highways-managed network.
- `is_primary`: boolean. DfT primary route network (green-sign
  through-routes), overlapping but distinct from trunk.
- `form_of_way`: physical form (Single/Dual/Collapsed Dual
  Carriageway, Roundabout, Slip Road, Shared Use, Guided Busway).

Counts below are for the study-area extract (N+C England,
~2.17M links).

## Family populations (study area)

| Family | Definition | Approx. links |
|---|---|---:|
| Motorway | road_function == "Motorway" | ~3,900 |
| Trunk A | "A Road" AND is_trunk | ~16,000 |
| Other-Urban | neither, RUC = urban | bulk of remainder |
| Other-Rural | neither, RUC = rural | bulk of remainder |
| Unknown RUC | neither, RUC null | ~336,000 (15.5%) |

Motorway is the smallest family. 4k links is small for XGBoost but
trainable. Per-family seed stability via the 5-seed harness will
test whether this family size is viable; if not, motorway can be
merged with trunk-A in a follow-up.

GB scaling estimate: ~5,500-6,000 motorway links and ~22,000-25,000
trunk A-road links GB-wide. Other-Urban and Other-Rural will be in
the millions. Family-size concerns are confined to motorway.

## Reasoning for each decision

### Why split on the trunk/non-trunk distinction rather than A/B/below

OS `road_classification` field (A Road / B Road / Classified
Unnumbered / Unclassified / Not Classified / Unknown) has known
unreliability in distinguishing B from unclassified, particularly
for older links. The trunk flag is more reliable: it reflects
National Highways management, which determines design standards,
maintenance regime, and infrastructure quality.

OS `road_function` is more reliable than `road_classification` for
distinguishing functional categories below trunk, but the v1 spec
collapses these into Other-Urban / Other-Rural rather than splitting
by road_function. The reasoning is that the urban/rural distinction
captures more risk-relevant variation than the road_function
distinctions for non-trunk roads — an urban A-road through a town
centre (often 30 mph, with junctions and pedestrians) is functionally
closer to an urban B-road than to a rural A-road. Splitting by
road_function within each RUC class is a v2 candidate if the v1
results show patterned residuals along that dimension.

### Why not add `is_primary` to the trunk family definition

Considered and rejected. Counts:

| Subset | Count |
|---|---:|
| A Road, trunk, primary | 13,873 |
| A Road, trunk, non-primary | 2,138 |
| A Road, non-trunk, primary | 57,182 |
| A Road, non-trunk, non-primary | 82,341 |

Adding primary would expand the Trunk A family from ~16k to ~73k.
Primary route status is administratively about route-network
designation (green signs) rather than design standard. A non-trunk
primary A-road through a small town is structurally still an urban
A-road — pedestrians, side junctions, signal-controlled crossings —
and is better grouped with other urban roads than with motorway-grade
trunk A-roads.

The trunk/non-trunk distinction has a cleaner structural correlate
(national vs local management → divided carriageways, grade-separated
junctions, controlled access). Keeping the family definition aligned
with structural design standard is methodologically clearer than
mixing structural and route-designation criteria.

`is_primary` is retained as a feature; the model can use it within
each family.

### Why not split by `form_of_way` (e.g. dual carriageway as a family)

Considered and rejected for v1. The motivation for facility-family
splitting is structural exposure-to-risk shape — different
traffic environments with different crash mechanisms, following the
HSM safety performance function approach. Form_of_way is a geometric
property, not a traffic-environment property in the same sense.

A dual carriageway B-road and a single carriageway B-road are
structurally similar in most relevant respects (same road class,
similar speed limits and traffic mix). The dual-carriageway flag
predicts higher speeds and different conflict patterns, but those
effects are within-family variation that XGBoost can capture by
splitting on `form_of_way` as a feature. Treating dual carriageway as
a family would prevent the per-family models from sharing information
across single and dual variants of the same road class, losing
statistical power without a clear structural justification.

Dual carriageway across all road_functions adds ~5,100 non-Motorway
non-Trunk-A links to the network. The bulk of these are dual-form
non-trunk A-roads (3,820 of the 5,100) which are functionally
similar to trunk A-roads. If v1 reveals systematic under-prediction
on dual-form non-trunk A-roads, "high-spec A-road" defined by
dual-form regardless of trunk status is a candidate v2 family.

### Why not break out roundabouts or intersections as a separate family

Considered and deferred to v2. OS `form_of_way` flags ~26,000
roundabout links across the network — a trainable population. HSM
treats intersections separately because their crash mechanisms are
distinct (turning conflicts dominate). Methodologically, an
intersection family is well-motivated.

Deferred for v1 because adding it bundles two changes (family
definition + intersection-specific model structure) into one
implementation, increasing the number of decisions that have to be
right. v1 keeps roundabouts within their parent road_function
family (a roundabout on a trunk A-road lands in Trunk A; a
roundabout connecting non-trunk A-roads lands in Other-Urban or
Other-Rural by RUC). XGBoost can split on `form_of_way` within each
family. v2 can promote roundabouts to a separate family if v1
residuals show patterning by form_of_way.

Slip roads (~8,400 motorway, ~1,500 trunk A, plus more on
non-trunk A and below) are handled the same way: assigned to their
parent road_function family, with `form_of_way` available as a
feature within the family.

### Why ONS RUC binary (urban/rural) rather than population density

ONS RUC is an externally-defined classification. Anyone can
reproduce the urban/rural assignment from public ONS data. Using a
population-density threshold introduces an analyst choice (where
to draw the line) that's harder to defend. RUC has the same issue
at one remove (someone at ONS chose the boundaries) but at least
the boundaries are externally settled.

The 6-class RUC scheme (UN1, UF1, RSN1, RSF1, RLN1, RLF1) is
collapsed to binary urban/rural via the existing
`ruc_urban_rural` derived field, currently 74% urban / 26% rural
across non-null study-area links.

## Outstanding decision: handling links with no RUC assignment

15.5% of links (~336,000 in the study area) have no ONS RUC
assignment. The ONS RUC integration uses nearest-LSOA-centroid
lookup, which fails for links far from any LSOA centroid —
typically boundary or coastal locations.

Three options are on the table:

1. **Spatial-join fallback** — expand the LSOA lookup radius or
   use a different join method to assign RUC to most no-RUC links.
   The TODO entry on this gap suggests it's probably resolvable.
   Doing this as a precursor to facility-family split removes a
   known data issue.
2. **Default to Rural** — most boundary/coastal links are likely
   rural. Assign all no-RUC links to Other-Rural with a flag, and
   revisit if the family shows oddly biased residuals.
3. **Separate "Unknown" family** — train a fifth model on the
   no-RUC links specifically. Methodologically cleanest (no
   imputation) but trains a model on a structurally biased
   population (boundary/coastal only).

The decision depends on whether the no-RUC links are geographically
clustered (suggesting structural bias) or scattered (suggesting
the default-to-rural approach is safe), and on the road_function
distribution within the no-RUC population.

A short characterisation analysis is needed before v1 is finalised.

## Validation plan (high level)

Per-family XGBoost models, evaluated against the current single-
model baseline on:

- **Headline metric:** combined ranking (per-family predictions
  stitched into one network-wide ranking) compared against current
  global-model ranking. Pseudo-R² and 5-seed Jaccard at k =
  100 / 1000 / 10000 / top-1%.
- **Per-family metrics:** pseudo-R², 5-seed Jaccard, and
  calibration per family. Identifies where per-family approach
  helps and where it doesn't.
- **Motorway-specific check:** the global model has a known mean
  residual of -3.3 on motorways (under-prediction). The per-family
  motorway model should reduce this. If it doesn't, that's
  evidence the motorway issue is not a family-specification
  problem.
- **Stability check on Motorway family:** with ~4k links, motorway
  per-family training is the stability test for whether v1 family
  sizing is viable.

## Out of scope for v1

- Per-family `k` for EB shrinkage (deferred; current global-k EB
  output stays as-is).
- Hierarchical / partial-pooling models across families.
- Breaking out roundabouts or slip roads as separate families.
- Splitting non-trunk roads by road_function (B vs Local vs
  Restricted, etc.).
- Adding `is_primary` to the trunk family.
- NHNM integration (depends on this work landing first).

## Key references

- TODO entry: "Facility-family split for Stage 2"
- EB session 1 finding: dispersion strongly non-constant across
  predicted-risk range (`reports/eb_dispersion.md`,
  `quarto/methodology/empirical-bayes-shrinkage.qmd` §3.1).
  Independent evidence that one global model leaves structure on
  the table.
- ONS RUC integration: `data/features/ruc_provenance.json`
- Current Stage 2: `quarto/methodology/...stage2 page...`