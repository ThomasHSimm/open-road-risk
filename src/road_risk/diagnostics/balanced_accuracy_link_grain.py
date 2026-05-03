"""
Compute balanced accuracy on pooled rank-stability predictions at link grain.

This supersedes the earlier link-year expansion benchmark. It compares one
pooled prediction per link against one pooled observed outcome per link:
whether the link had at least one observed crash in 2015-2024.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from road_risk.config import _ROOT

SEED_PATH = _ROOT / "data/models/rank_stability/seed_42.parquet"
OUT_CSV = _ROOT / "reports/supporting/balanced_accuracy_link_grain.csv"
OUT_MD = _ROOT / "reports/supporting/balanced_accuracy_notes_v2.md"
THRESHOLD_PCTS = [50.0, 75.0, 90.0, 95.0, 97.5, 99.0, 99.5]


def build_link_frame() -> pd.DataFrame:
    df = pd.read_parquet(SEED_PATH, columns=["link_id", "predicted_xgb", "collision_count"])
    df["observed_link_outcome"] = df["collision_count"].gt(0)
    return df


def run_sweep(df: pd.DataFrame) -> pd.DataFrame:
    scores = df["predicted_xgb"].to_numpy(dtype=float)
    y_true = df["observed_link_outcome"].to_numpy(dtype=bool)
    threshold_values = np.percentile(scores, THRESHOLD_PCTS)

    rows: list[dict[str, float | int]] = []
    for pct, value in zip(THRESHOLD_PCTS, threshold_values, strict=True):
        y_pred = scores >= value
        tp = int(np.sum(y_pred & y_true))
        fp = int(np.sum(y_pred & ~y_true))
        tn = int(np.sum(~y_pred & ~y_true))
        fn = int(np.sum(~y_pred & y_true))
        sensitivity = tp / (tp + fn) if (tp + fn) else float("nan")
        specificity = tn / (tn + fp) if (tn + fp) else float("nan")
        balanced_accuracy = (
            (sensitivity + specificity) / 2
            if np.isfinite(sensitivity) and np.isfinite(specificity)
            else float("nan")
        )
        rows.append(
            {
                "threshold_pct": pct,
                "threshold_value": float(value),
                "n_pred_pos": int(np.sum(y_pred)),
                "TP": tp,
                "FP": fp,
                "TN": tn,
                "FN": fn,
                "sensitivity": float(sensitivity),
                "specificity": float(specificity),
                "balanced_accuracy": float(balanced_accuracy),
            }
        )
    return pd.DataFrame(rows)


def write_notes(df: pd.DataFrame, sweep: pd.DataFrame) -> None:
    best = sweep.sort_values(
        ["balanced_accuracy", "specificity", "threshold_pct"],
        ascending=[False, False, True],
    ).iloc[0]
    positive_rate = float(df["observed_link_outcome"].mean())
    positive_n = int(df["observed_link_outcome"].sum())
    total_n = int(len(df))

    notes = f"""# Balanced Accuracy Notes V2

Seed file used: `data/models/rank_stability/seed_42.parquet`

Method used here:
This benchmark is computed at the correct link grain. The seed-42 rank-stability
output is already pooled to one row per link, so the observed outcome is also
pooled to one row per link:

- `observed_link_outcome = 1` if `collision_count >= 1`
- `observed_link_outcome = 0` otherwise

This supersedes the prior link-year computation in
`reports/supporting/balanced_accuracy_notes.md`, which expanded pooled
per-link predictions back across link-years and was methodologically flawed.

Best balanced accuracy:

- Threshold percentile: `{best["threshold_pct"]}`
- Threshold value: `{best["threshold_value"]:.10f}`
- Balanced accuracy: `{best["balanced_accuracy"]:.6f}`
- Sensitivity: `{best["sensitivity"]:.6f}`
- Specificity: `{best["specificity"]:.6f}`
- Predicted positive links: `{int(best["n_pred_pos"]):,}`

Approximate comparison to Gilardi et al. (2022) JRSSA:

- Gilardi severe benchmark: `0.675`
- Gilardi slight benchmark: `0.720`
- This pooled-all-crashes link-grain model: `{best["balanced_accuracy"]:.6f}`

This comparison remains approximate rather than apples-to-apples because
Gilardi reported severity-stratified models, while the present model predicts
all crashes pooled.

Caveats:

- Positive rate here is `{positive_rate:.4%}` ({positive_n:,} positive links
  out of {total_n:,}), not Gilardi's outcome definition.
- These are point predictions from a fitted XGBoost model, not posterior
  samples.
- The network here is much larger, about 2.17 million links, roughly 600x the
  size discussed in the benchmark prompt.
- The benchmark uses pooled link-level outcomes over 2015-2024, matching the
  pooled link-level predictions, rather than year-specific outcomes.
"""
    OUT_MD.write_text(notes)


def main() -> None:
    df = build_link_frame()
    sweep = run_sweep(df)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    sweep.to_csv(OUT_CSV, index=False)
    write_notes(df, sweep)
    print(sweep.to_string(index=False))
    best = sweep.sort_values(
        ["balanced_accuracy", "specificity", "threshold_pct"],
        ascending=[False, False, True],
    ).iloc[0]
    print("\nBEST")
    print(best.to_string())


if __name__ == "__main__":
    main()
