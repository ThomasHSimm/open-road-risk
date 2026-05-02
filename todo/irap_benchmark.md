### External iRAP-class benchmark (Victoria first, NZ/NSW second)

**Context:** Current validation is strong internally but still mostly within the
open-data stack. To make a stakeholder-facing claim that the model is more than
an interesting predictor, it needs an external benchmark against a recognised
road-infrastructure safety framework. The cleanest use of iRAP-class data is
not as a Stage 2 feature, but as a held-out benchmark for convergent validity.
This tests whether the open-data risk ranking agrees with accepted surveyed-road
safety ratings on the subset of roads where those ratings exist.

**Decisions already made:**
- Use iRAP / AusRAP / KiwiRAP **as benchmark only**, not as a production
  feature in Stage 2 v1. Avoids circularity and patchy-coverage bias.
- Benchmark against **vehicle Star Rating first**, not crash risk maps or FSI
  estimates. Star rating is the cleaner infrastructure-oriented label.
- Victoria is the first proving ground because the public AusRAP dataset appears
  machine-readable and pairs with open crash and traffic data.
- New South Wales is the next replication if the goal is low-friction external
  replication; New Zealand is the next replication if the goal is closest
  UK-like policy / institutional analogue.
- Compare on a **common benchmark section table** — do not join native OS Open
  Roads links directly to RAP segments and pretend they are the same unit.
- Report this as **convergent validity** / external benchmark evidence, not as
  proof the model "replaces iRAP".
- Keep internal validation work (future-years holdout, naïve `AADT × length`
  baseline, 5-seed stability, EB shrinkage) separate. External benchmark adds
  evidence; it does not rescue weak internal validity.

**Prompt:**

Draft a Quarto design doc at
`quarto/methodology/external-benchmark-irap.qmd`, NOT code.
I will review before any implementation.

The doc should cover:

1. Why iRAP-class data is a benchmark and not a training feature:
   - coverage mismatch on unsurveyed roads
   - circularity risk
   - distinction between infrastructure audit and realised-harm prediction

2. Benchmark geography choice:
   - Victoria as first benchmark
   - NSW as second benchmark for within-country replication
   - New Zealand as second benchmark for closest UK-like analogue
   - what exact public datasets are expected for each (RAP layer, crash data,
     traffic / AADT backbone)

3. Unit-of-analysis design:
   - define a common benchmark section table
   - options: provider section IDs vs fixed 100 m segmentation
   - length-weighted aggregation of link-year predictions onto benchmark sections
   - note that the benchmark must use surveyed-road geometry as reference, not
     raw OS Open Roads links as-if equivalent

4. Metrics to report:
   - Spearman or Kendall rank agreement between predicted risk and inverse star score
   - AUROC / PR-AUC for identifying 1–2 star sections
   - Quadratic-weighted kappa after binning predicted risk into 5 bands
   - share of top-x% predicted-risk length falling on 1–2 star roads
   - disagreement audit by quadrant:
     high predicted / low star,
     high predicted / high star,
     low predicted / low star,
     low predicted / high star

5. Diagnostic outputs:
   - map of true positives
   - map of informative disagreements
   - table of representative sections in each disagreement quadrant
   - note whether audited geometric fields (e.g. curvature, grade, lane width if
     present in the benchmark) broadly agree with model signal

6. Reporting and claims discipline:
   - exact wording for README / Quarto / slides
   - explicitly avoid “replacement for iRAP”
   - record RAP programme name, publication date, and model version so the
     comparison is robust to methodology drift

7. Dependency / execution note:
   - benchmark should be run alongside, not before, future-years holdout,
     naïve baseline, 5-seed stability, and EB shrinkage review
   - stop after the design doc; do not download data or implement joins yet

**Expected outcomes:**
- A credible external-validation story for surveyed roads without weakening the
  open-data positioning of the core model.
- Agreement should be meaningful but not perfect; informative disagreement is a
  feature, not necessarily a failure.
- Strongest likely public claim: the model aligns with an accepted
  infrastructure-safety framework on surveyed roads and can then be used as a
  network-wide triage layer on roads that are not routinely surveyed.
- If agreement is weak even after sensible benchmarking design, that is a real
  signal to revisit feature set / geometry / exposure assumptions before making
  stronger stakeholder claims.

---
