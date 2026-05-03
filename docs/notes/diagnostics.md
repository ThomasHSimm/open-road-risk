On the broader checks point
Worth doing, and worth doing properly rather than as ad-hoc grep. A few categories of check that would have caught this one and likely catch the next:
1. Coverage-by-target-stratum sanity checks. For every feature in the Stage 2 dataset, compute the missingness rate broken down by collision history. Any feature where missingness differs by more than a few percentage points between collision and zero-collision links is a leakage suspect. The metric is cheap. The bug is loud once you know to look. Could live as a notebook or a one-shot diagnostic script you run after Stage 2 builds.
2. Row-count assertions at join boundaries. Each join in join.py and collision.py should have an assertion: "after this join, expected row count is X; actual is Y; deviation > threshold means raise." That would catch "we're starting from 21M link-years but only 391k get traffic features" the moment it happens. Cheap to add, hard to add later when you're not sure what the right invariant is.
3. Feature-importance plausibility. Any single feature with importance >0.3 in a tree model with 30+ features deserves a second look. Not because it's automatically wrong — sometimes one feature genuinely dominates — but because that's the visible symptom of the leakage class of bug. A pre-commit check or a CI test that fails if any feature crosses a threshold (configurable) would force a "is this real or is this leakage" conversation each time.
4. The split-population check. For any feature, compute mean and std on the collision-positive vs zero-collision subsets. If they differ by more than X standard deviations, the feature is correlated with the target — which can be legitimate (HGV% really is higher on risky roads) but is also the leakage signature. Worth a glance before training.
These are all post-hoc diagnostics, not preventative ones. They don't stop you writing the bug; they catch it early. That's probably the right level — preventative type systems for data joins exist (Great Expectations, dbt tests, etc.) but they're heavy and the cost-benefit on a research repo is dubious.
What I'd actually add to the project
Single diagnostic notebook or script: diagnostics/feature_audit.py that runs after every Stage 2 build and reports:

Coverage rate for each feature, overall and by collision history
Row count at each major join step vs expected
Top 10 features by importance from a quick fit, flagged if any exceed 0.3
Mean/std of each feature on collision vs zero-collision subsets, flagged if separation exceeds 2σ

Output is a markdown report saved to reports/diagnostics/. Runs in a few minutes. Scan it before trusting any new model run.
This would have caught the HGV bug immediately — coverage rate of 9.67% overall vs 89.72% on collision links is a huge red flag in any of the four checks above.
Worth scoping when there's time, not now.