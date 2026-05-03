"""
Compute balanced accuracy on pooled rank-stability predictions.

The available rank-stability seed outputs are pooled to one row per link.
This diagnostic expands a chosen seed's annual prediction back across link-years
using `aadt_estimates.parquet` and scores 0 vs >=1 observed collisions per
link-year against thresholded `predicted_xgb`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from road_risk.config import _ROOT

SEED_PATH = _ROOT / "data/models/rank_stability/seed_42.parquet"
AADT_PATH = _ROOT / "data/models/aadt_estimates.parquet"
RLA_PATH = _ROOT / "data/features/road_link_annual.parquet"
OUT_CSV = _ROOT / "reports/supporting/balanced_accuracy_threshold_sweep.csv"
OUT_MD = _ROOT / "reports/supporting/balanced_accuracy_notes.md"
THRESHOLD_PCTS = [50.0, 75.0, 90.0, 95.0, 97.5, 99.0, 99.5]


def build_link_year_frame() -> pd.DataFrame:
    seed = pd.read_parquet(SEED_PATH, columns=["link_id", "predicted_xgb"])
    aadt = pd.read_parquet(AADT_PATH, columns=["link_id", "year"])
    rla = pd.read_parquet(RLA_PATH, columns=["link_id", "year", "collision_count"])

    df = aadt.merge(seed, on="link_id", how="left")
    df = df.merge(rla, on=["link_id", "year"], how="left")
    df["collision_count"] = df["collision_count"].fillna(0).astype(int)
    df["y_true"] = df["collision_count"].gt(0)
    return df


def run_sweep(df: pd.DataFrame) -> pd.DataFrame:
    seed_scores = pd.read_parquet(SEED_PATH, columns=["predicted_xgb"])["predicted_xgb"].to_numpy()
    threshold_values = np.percentile(seed_scores, THRESHOLD_PCTS)

    rows: list[dict[str, float | int]] = []
    y_true = df["y_true"].to_numpy(dtype=bool)
    scores = df["predicted_xgb"].to_numpy(dtype=float)

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
    positive_rate = float(df["y_true"].mean())
    positive_n = int(df["y_true"].sum())
    total_n = int(len(df))

    notes = f"""# Balanced Accuracy Notes

Seed file used: `data/models/rank_stability/seed_42.parquet`

Method used here:
The available rank-stability seed output is pooled to one row per link, with
`predicted_xgb` representing the pooled annual prediction. To score a
link-year 0 vs >=1 benchmark without retraining, this analysis expands the
seed-42 prediction back across link-years by joining it to
`data/models/aadt_estimates.parquet` and observed `collision_count` from
`data/features/road_link_annual.parquet`. Each link therefore carries the same
predicted score in every year.

Best balanced accuracy:

- Threshold percentile: `{best["threshold_pct"]}`
- Threshold value: `{best["threshold_value"]:.10f}`
- Balanced accuracy: `{best["balanced_accuracy"]:.6f}`
- Sensitivity: `{best["sensitivity"]:.6f}`
- Specificity: `{best["specificity"]:.6f}`
- Predicted positive link-years: `{int(best["n_pred_pos"]):,}`

Approximate comparison to Gilardi et al. (2022) JRSSA:

- Gilardi severe benchmark: `0.675`
- Gilardi slight benchmark: `0.720`
- This pooled-all-crashes model: `{best["balanced_accuracy"]:.6f}`

This comparison is approximate rather than apples-to-apples because Gilardi
reported severity-stratified models, while the present model predicts all
crashes pooled.

Caveats:

- Positive rate here is `{positive_rate:.4%}` ({positive_n:,} positive
  link-years out of {total_n:,}), versus roughly 20% in the Gilardi setup
  over 8 years.
- These are point predictions from a fitted XGBoost model, not posterior
  samples.
- The network here is much larger, about 2.17 million links and 21.68 million
  link-years, roughly 600x the size discussed in the benchmark prompt.
- Because the available seed output is pooled to one row per link, the same
  annual predicted score is repeated across years for a given link in this
  benchmark.
"""
    OUT_MD.write_text(notes)


def main() -> None:
    df = build_link_year_frame()
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
