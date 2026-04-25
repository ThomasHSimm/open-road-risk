"""
Single-run EB shrinkage validation diagnostics.

This script applies EB-style shrinkage to the current pooled production risk
scores using the positive-event weighted k from session 1, writes a separate
`risk_scores_eb.parquet`, and produces a validation report. It does not modify
production `risk_scores.parquet` or any 5-seed artefacts.
"""

from __future__ import annotations

import itertools
import logging
from typing import Any

import numpy as np
import pandas as pd

from road_risk.config import _ROOT
from road_risk.model.collision import AADT_PATH, MODELS
from road_risk.model.eb_shrinkage import compute_eb_scores, load_eb_k_values

logger = logging.getLogger(__name__)

RISK_PATH = MODELS / "risk_scores.parquet"
EB_RISK_PATH = MODELS / "risk_scores_eb.parquet"
RANK_STABILITY_DIR = MODELS / "rank_stability"
REPORT_PATH = _ROOT / "reports/eb_validation.md"
SEEDS = [42, 43, 44, 45, 46]
EXPECTED_CHURN_COUNTS = {100: 21, 1000: 234}


def _format_float(value: float, digits: int = 6) -> str:
    if not np.isfinite(value):
        return "nan"
    if abs(value) < 0.001:
        return f"{value:.8f}"
    return f"{value:.{digits}f}"


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def _n_years_by_link() -> pd.DataFrame:
    logger.info("Computing n_years by link from %s", AADT_PATH)
    aadt = pd.read_parquet(AADT_PATH, columns=["link_id", "year"])
    return (
        aadt.groupby("link_id", sort=False)["year"]
        .nunique()
        .reset_index(name="n_years")
    )


def _top_set(df: pd.DataFrame, score_col: str, k: int) -> set[Any]:
    ranked = df.sort_values(
        [score_col, "link_id"],
        ascending=[False, True],
        kind="mergesort",
    )
    return set(ranked["link_id"].head(k))


def _top_frame(df: pd.DataFrame, score_col: str, k: int) -> pd.DataFrame:
    return df.sort_values(
        [score_col, "link_id"],
        ascending=[False, True],
        kind="mergesort",
    ).head(k)


def _churn_set(k: int) -> set[Any]:
    top_sets = []
    for seed in SEEDS:
        path = RANK_STABILITY_DIR / f"seed_{seed}.parquet"
        scores = pd.read_parquet(path, columns=["link_id", "predicted_xgb"])
        top_sets.append(_top_set(scores, "predicted_xgb", k))
    union = set().union(*top_sets)
    intersection = set.intersection(*top_sets)
    return union - intersection


def _percentile_rows(series: pd.Series, percentiles: list[float]) -> list[list[str]]:
    quantiles = series.quantile(percentiles)
    return [
        [f"p{int(p * 100)}", _format_float(float(quantiles.loc[p]))]
        for p in percentiles
    ]


def _rank_array(df: pd.DataFrame, score_col: str) -> np.ndarray:
    ordered = df.sort_values("link_id", kind="mergesort")
    return ordered[score_col].rank(method="average", ascending=True).to_numpy()


def _pearson_corr(left: np.ndarray, right: np.ndarray) -> float:
    left_centered = left - left.mean()
    right_centered = right - right.mean()
    denom = np.sqrt(np.sum(left_centered**2) * np.sum(right_centered**2))
    return float(np.sum(left_centered * right_centered) / denom) if denom else float("nan")


def _movement_summary(scores: pd.DataFrame, link_ids: set[Any]) -> dict[str, Any]:
    subset = scores[scores["link_id"].isin(link_ids)].copy()
    delta = subset["risk_percentile_eb"] - subset["risk_percentile"]
    abs_delta = delta.abs()
    gt5 = subset[abs_delta > 5]
    gt10 = subset[abs_delta > 10]
    return {
        "n": int(len(subset)),
        "gt5_count": int(len(gt5)),
        "gt10_count": int(len(gt10)),
        "gt5_pct": float(len(gt5) / len(subset) * 100) if len(subset) else 0.0,
        "gt10_pct": float(len(gt10) / len(subset) * 100) if len(subset) else 0.0,
        "gt5_toward_top1": int((gt5["risk_percentile_eb"] > gt5["risk_percentile"]).sum()),
        "gt5_away_top1": int((gt5["risk_percentile_eb"] < gt5["risk_percentile"]).sum()),
        "gt10_toward_top1": int((gt10["risk_percentile_eb"] > gt10["risk_percentile"]).sum()),
        "gt10_away_top1": int((gt10["risk_percentile_eb"] < gt10["risk_percentile"]).sum()),
    }


def _class_breakdown(df: pd.DataFrame, link_ids: set[Any]) -> list[list[Any]]:
    subset = df[df["link_id"].isin(link_ids)]
    if "road_classification" not in subset.columns:
        return [["road_classification missing", len(subset)]]
    counts = subset["road_classification"].fillna("Unknown").value_counts()
    return [[idx, int(value)] for idx, value in counts.items()]


def _qualitative_rows(
    scores: pd.DataFrame,
    entrants: set[Any],
    leavers: set[Any],
) -> list[list[Any]]:
    rows = []
    cols = [
        "link_id",
        "road_classification",
        "estimated_aadt",
        "collision_count",
        "n_years",
        "predicted_xgb",
        "predicted_eb",
        "eb_weight",
        "risk_percentile",
        "risk_percentile_eb",
    ]
    for label, link_ids, ascending in [
        ("entered", entrants, False),
        ("left", leavers, True),
    ]:
        subset = scores[scores["link_id"].isin(link_ids)].copy()
        subset["delta"] = subset["risk_percentile_eb"] - subset["risk_percentile"]
        subset["abs_delta"] = subset["delta"].abs()
        subset = subset.sort_values(
            ["abs_delta", "link_id"],
            ascending=[False, ascending],
            kind="mergesort",
        ).head(5)
        for _, row in subset[cols].iterrows():
            rows.append([
                label,
                row["link_id"],
                row.get("road_classification", ""),
                _format_float(float(row["estimated_aadt"])),
                int(row["collision_count"]),
                int(row["n_years"]),
                _format_float(float(row["predicted_xgb"])),
                _format_float(float(row["predicted_eb"])),
                _format_float(float(row["eb_weight"])),
                _format_float(float(row["risk_percentile"])),
                _format_float(float(row["risk_percentile_eb"])),
            ])
    return rows


def _k_sensitivity(
    base_scores: pd.DataFrame,
    n_years: pd.DataFrame,
    k_values: dict[str, float],
    top_k: int,
) -> tuple[pd.DataFrame, list[list[Any]], list[list[Any]], list[list[Any]], list[list[Any]]]:
    sensitivity = {}
    top_sets = {}
    ranks = {}

    base_cols = [
        "link_id",
        "collision_count",
        "predicted_xgb",
        "risk_percentile",
    ]
    for label, k in k_values.items():
        scored = compute_eb_scores(base_scores[base_cols].copy(), n_years, k)
        score_col = f"predicted_eb_{label}"
        pct_col = f"risk_percentile_eb_{label}"
        sensitivity[score_col] = scored["predicted_eb"]
        sensitivity[pct_col] = scored["risk_percentile_eb"]
        top_sets[label] = _top_set(scored, "predicted_eb", top_k)
        ranks[label] = _rank_array(scored, "predicted_eb")

    sensitivity_df = pd.DataFrame({"link_id": base_scores["link_id"]})
    for col, values in sensitivity.items():
        sensitivity_df[col] = values

    membership_rows = [
        [label, f"{len(top_sets[label]):,}"]
        for label in k_values
    ]
    overlap_rows = []
    spearman_rows = []
    labels = list(k_values)
    for left, right in itertools.combinations(labels, 2):
        inter = len(top_sets[left] & top_sets[right])
        union = len(top_sets[left] | top_sets[right])
        overlap_rows.append([
            f"{left} vs {right}",
            f"{inter:,}",
            f"{union:,}",
            _format_float(inter / union if union else float("nan")),
        ])
        spearman_rows.append([
            f"{left} vs {right}",
            _format_float(_pearson_corr(ranks[left], ranks[right])),
        ])

    production = sensitivity_df["risk_percentile_eb_positive_weighted"]
    movement_rows = []
    for label in ["link_year_weighted", "median"]:
        delta = (sensitivity_df[f"risk_percentile_eb_{label}"] - production).abs()
        movement_rows.append([
            f"{label} vs positive_weighted",
            f"{int((delta > 1).sum()):,}",
            f"{int((delta > 5).sum()):,}",
            f"{int((delta > 10).sum()):,}",
        ])

    return sensitivity_df, membership_rows, overlap_rows, spearman_rows, movement_rows


def _write_report(
    scores: pd.DataFrame,
    k_values: dict[str, float],
    top_stats: dict[str, Any],
    movement: dict[str, Any],
    churn_rows: list[list[Any]],
    sensitivity_membership: list[list[Any]],
    sensitivity_overlap: list[list[Any]],
    sensitivity_spearman: list[list[Any]],
    sensitivity_movement: list[list[Any]],
) -> None:
    n_years = scores["n_years"]
    n_year_rows = [
        ["count", f"{len(n_years):,}"],
        ["min", _format_float(float(n_years.min()))],
        ["median", _format_float(float(n_years.median()))],
        ["max", _format_float(float(n_years.max()))],
    ] + _percentile_rows(n_years, [0.05, 0.25, 0.75, 0.95])

    k_rows = [
        ["positive_weighted (production)", _format_float(k_values["positive_weighted"])],
        ["link_year_weighted", _format_float(k_values["link_year_weighted"])],
        ["median", _format_float(k_values["median"])],
    ]
    weight_rows = _percentile_rows(scores["eb_weight"], [0, 0.05, 0.25, 0.5, 0.75, 0.95, 1])
    move_rows = [
        ["median_abs_delta", _format_float(movement["median_abs_delta"])],
        ["p90_abs_delta", _format_float(movement["p90_abs_delta"])],
        ["p99_abs_delta", _format_float(movement["p99_abs_delta"])],
        [">10 percentile points", f"{movement['gt10_count']:,} ({movement['gt10_pct']:.2f}%)"],
        [">25 percentile points", f"{movement['gt25_count']:,} ({movement['gt25_pct']:.2f}%)"],
    ]

    qualitative = _qualitative_rows(scores, top_stats["entrants"], top_stats["leavers"])
    entrant_class_rows = _class_breakdown(scores, top_stats["entrants"])
    leaver_class_rows = _class_breakdown(scores, top_stats["leavers"])

    observations = [
        (
            "Risk percentiles remain related but not identical: median absolute "
            f"change is {_format_float(movement['median_abs_delta'])} percentile "
            f"points and p99 is {_format_float(movement['p99_abs_delta'])}."
        ),
        (
            "Low-exposure or limited-observation links dropping is assessed in "
            "the entrant/leaver table via AADT, collision counts, and EB weights."
        ),
        (
            "Links rising under EB are visible in the deterministic entrant "
            "sample; repeated observed collisions relative to the prior should "
            "show as lower EB weights and higher predicted_eb."
        ),
        (
            "With positive-weighted k, movement should concentrate where "
            "k * predicted_xgb * n_years is large; the weight distribution above "
            "shows how much shrinkage is applied across the scored population."
        ),
    ]

    report = "\n\n".join([
        "# EB Single-Run Validation",
        (
            "This report applies EB-style shrinkage to the current pooled Stage 2 "
            "risk scores without modifying production `risk_scores.parquet`. The "
            "production EB run uses the positive-event weighted dispersion from "
            "`data/provenance/eb_dispersion_provenance.json`; see "
            "`quarto/methodology/empirical-bayes-shrinkage.qmd` for the design "
            "and `reports/eb_dispersion.md` for the MoM k diagnostics."
        ),
        "## 6.1 Single-Run Ranking Movement\n\n"
        + "### n_years Distribution\n\n"
        + _markdown_table(["metric", "value"], n_year_rows)
        + "\n\n### k Values\n\n"
        + _markdown_table(["k", "value"], k_rows)
        + "\n\n### eb_weight Distribution\n\n"
        + _markdown_table(["percentile", "eb_weight"], weight_rows)
        + "\n\n### Percentile Movement\n\n"
        + _markdown_table(["metric", "value"], move_rows),
        "## 6.2 Top-1% Comparison\n\n"
        + _markdown_table(
            ["metric", "value"],
            [
                ["top_1pct_count", f"{top_stats['top_k']:,}"],
                ["intersection", f"{top_stats['intersection']:,}"],
                ["intersection_pct_of_top1", f"{top_stats['intersection_pct']:.2f}%"],
                ["entering_EB_top1", f"{len(top_stats['entrants']):,}"],
                ["leaving_EB_top1", f"{len(top_stats['leavers']):,}"],
            ],
        )
        + "\n\n### Entrants By Road Class\n\n"
        + _markdown_table(["road_classification", "count"], entrant_class_rows)
        + "\n\n### Leavers By Road Class\n\n"
        + _markdown_table(["road_classification", "count"], leaver_class_rows),
        "## 6.3 Qualitative Link Review\n\n"
        + _markdown_table(
            [
                "direction",
                "link_id",
                "road_classification",
                "estimated_aadt",
                "collision_count",
                "n_years",
                "predicted_xgb",
                "predicted_eb",
                "eb_weight",
                "risk_percentile",
                "risk_percentile_eb",
            ],
            qualitative,
        ),
        (
            "## 6.4 Seed-Churn Intersection Diagnostic\n\n"
            "EB should disproportionately affect borderline links, which should "
            "overlap with the population that seed-churns. If churning links do "
            "not show systematically larger EB movement than the general "
            "population, EB is probably not addressing the source of seed-induced "
            "ranking instability. This is a diagnostic, not a pass/fail criterion.\n\n"
            + _markdown_table(
                [
                    "population",
                    "n_links",
                    "abs_delta_gt5",
                    "abs_delta_gt5_pct",
                    "gt5_toward_top1",
                    "gt5_away_top1",
                    "abs_delta_gt10",
                    "abs_delta_gt10_pct",
                    "gt10_toward_top1",
                    "gt10_away_top1",
                ],
                churn_rows,
            )
        ),
        "## 7 k Sensitivity\n\n"
        + "### Top-1% Membership Count\n\n"
        + _markdown_table(["k", "top_1pct_count"], sensitivity_membership)
        + "\n\n### Pairwise Top-1% Overlap\n\n"
        + _markdown_table(["pair", "intersection", "union", "jaccard"], sensitivity_overlap)
        + "\n\n### Pairwise Spearman\n\n"
        + _markdown_table(["pair", "spearman"], sensitivity_spearman)
        + "\n\n### Percentile Movement Versus Production k\n\n"
        + _markdown_table(
            ["comparison", "abs_delta_gt1", "abs_delta_gt5", "abs_delta_gt10"],
            sensitivity_movement,
        )
        + "\n\nIf top-1% membership or Spearman moves materially across the three k values, "
        "the borrowed-k method is operationally fragile under non-constant dispersion. "
        "Material vs not-material is left for human review from the numbers above.",
        "## Closing Recommendation\n\n"
        "The diagnostics above should be read as evidence for whether EB is useful, "
        "ambiguous, or problematic. This run produces the EB-adjusted scores and "
        "single-run validation only; cross-seed EB stability is reserved for session 3.\n\n"
        "### Observations Against Priors\n\n"
        + "\n".join(f"- {item}" for item in observations),
    ])
    REPORT_PATH.write_text(report + "\n")


def run_validation() -> dict[str, Any]:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    k_values = load_eb_k_values()
    production_k = k_values["positive_weighted"]

    logger.info("Loading pooled production scores from %s", RISK_PATH)
    production = pd.read_parquet(RISK_PATH)
    n_years = _n_years_by_link()

    logger.info("Computing EB scores with positive-event weighted k=%s", production_k)
    scores = compute_eb_scores(production, n_years, production_k)
    scores.to_parquet(EB_RISK_PATH, index=False)
    logger.info("Wrote EB scores to %s", EB_RISK_PATH)

    delta = scores["risk_percentile_eb"] - scores["risk_percentile"]
    abs_delta = delta.abs()
    movement = {
        "median_abs_delta": float(abs_delta.median()),
        "p90_abs_delta": float(abs_delta.quantile(0.9)),
        "p99_abs_delta": float(abs_delta.quantile(0.99)),
        "gt10_count": int((abs_delta > 10).sum()),
        "gt10_pct": float((abs_delta > 10).mean() * 100),
        "gt25_count": int((abs_delta > 25).sum()),
        "gt25_pct": float((abs_delta > 25).mean() * 100),
    }

    top_k = len(scores) // 100
    old_top = _top_set(scores, "predicted_xgb", top_k)
    eb_top = _top_set(scores, "predicted_eb", top_k)
    top_stats = {
        "top_k": top_k,
        "intersection": len(old_top & eb_top),
        "intersection_pct": len(old_top & eb_top) / top_k * 100,
        "entrants": eb_top - old_top,
        "leavers": old_top - eb_top,
    }

    full_summary = _movement_summary(scores, set(scores["link_id"]))
    churn_table_rows = []
    top1000_gt10 = None
    for k in [100, 1000]:
        churn = _churn_set(k)
        expected = EXPECTED_CHURN_COUNTS[k]
        label = f"seed_churn_top_{k}"
        if abs(len(churn) - expected) > max(5, expected * 0.1):
            label += f" (expected approx {expected}, observed {len(churn)})"
        summary = _movement_summary(scores, churn)
        if k == 1000:
            top1000_gt10 = summary["gt10_count"]
        churn_table_rows.append([
            label,
            f"{summary['n']:,}",
            f"{summary['gt5_count']:,}",
            f"{summary['gt5_pct']:.2f}%",
            f"{summary['gt5_toward_top1']:,}",
            f"{summary['gt5_away_top1']:,}",
            f"{summary['gt10_count']:,}",
            f"{summary['gt10_pct']:.2f}%",
            f"{summary['gt10_toward_top1']:,}",
            f"{summary['gt10_away_top1']:,}",
        ])
    churn_table_rows.append([
        "full_scored_population",
        f"{full_summary['n']:,}",
        f"{full_summary['gt5_count']:,}",
        f"{full_summary['gt5_pct']:.2f}%",
        f"{full_summary['gt5_toward_top1']:,}",
        f"{full_summary['gt5_away_top1']:,}",
        f"{full_summary['gt10_count']:,}",
        f"{full_summary['gt10_pct']:.2f}%",
        f"{full_summary['gt10_toward_top1']:,}",
        f"{full_summary['gt10_away_top1']:,}",
    ])

    (
        _,
        sensitivity_membership,
        sensitivity_overlap,
        sensitivity_spearman,
        sensitivity_movement,
    ) = _k_sensitivity(
        production,
        n_years,
        k_values,
        top_k,
    )
    _write_report(
        scores,
        k_values,
        top_stats,
        movement,
        churn_table_rows,
        sensitivity_membership,
        sensitivity_overlap,
        sensitivity_spearman,
        sensitivity_movement,
    )

    return {
        "production_k": production_k,
        "top1_intersection": top_stats["intersection"],
        "top1_intersection_pct": top_stats["intersection_pct"],
        "median_abs_delta": movement["median_abs_delta"],
        "top1000_churn_gt10": top1000_gt10,
    }


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    result = run_validation()
    print(f"production_k_used={result['production_k']:.10g}")
    print(
        "top1_intersection="
        f"{result['top1_intersection']} ({result['top1_intersection_pct']:.2f}%)"
    )
    print(f"median_abs_percentile_change={result['median_abs_delta']:.10g}")
    print(f"top1000_churn_links_eb_change_gt10={result['top1000_churn_gt10']}")


if __name__ == "__main__":
    main()
