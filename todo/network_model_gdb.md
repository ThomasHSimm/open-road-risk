### Network Model GDB integration (SRN-only)

**Context:** National Highways Network Model Public download provides
authoritative lane counts and structural attributes for ~42,960 SRN links
(motorways + trunk A-roads), covering ~14,000 of the 21,676 top-1% risk
links. Open Government Licence; no friction. Speed limit removed pending
validation — not available here. SRN-only coverage means this is
facility-family-conditional by construction; integrating it well means
using it *within* a facility-family split, not as a global feature with
NaN-everywhere-else.

**Decisions already made:**
- Queue as dependency of facility-family split, not independent retrain.
  Integrating before the split means wrestling with 95%-missing features
  — the same bias problem OSM had.
- Join via TOID where available (96.45% complete); spatial-join fallback
  for the ~3.5% missing (~1,500 links).
- Useful features: `numberoflanes`, `carriageway`, `srn` flag,
  `startgradeseparation`, `endgradeseparation`, turn/access/vehicle
  restriction counts per link.
- Skip empty columns: `smartmotorway`, `parentlinkref`, `enddate`, and
  `Speed_Limit` layer (0 rows).
- Validity dates: Network Model startdates only go back to 2020 (~75 links)
  with most from 2022 onwards. Do NOT use as evidence of physical road
  presence for pre-2020 modelling years. Use OS Open Roads as truth for
  pre-2020 link existence.

**Prompt:**
[Draft when ready. Should depend on facility-family split work being done
first. Should include: join via TOID with spatial-join fallback, feature
extraction from Link layer + Lane-summary aggregation, exclusion of empty
columns, join quality diagnostics (how many of the expected ~14k top-1%
links got enriched), methodology-page update describing the authoritative
SRN feature set.]

**Expected outcomes:**
- Clean authoritative lane counts on motorway + trunk A model in the
  facility-family split.
- Modest predictive improvement on the SRN model; no impact on other classes.
- Methodology story: "authoritative lanes on SRN, imputed defaults elsewhere."

---

