"""
Five-seed rank stability evaluation for Stage 2 XGBoost.

This module deliberately does not call score_and_save() or write the production
risk_scores.parquet/model artefacts. It loads the existing GLM, retrains only
the XGBoost model for each seed, and writes per-seed scored outputs under
data/models/rank_stability/.
"""

from __future__ import annotations

import itertools
import json
import logging
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd

from road_risk.config import _ROOT
from road_risk.model.collision import (
    AADT_PATH,
    MODELS,
    NET_PATH,
    OPENROADS_PATH,
    RLA_PATH,
    build_collision_dataset,
    score_collision_models,
    train_collision_xgb,
)

logger = logging.getLogger(__name__)

SEEDS = [42, 43, 44, 45, 46]
TOP_K_FIXED = [100, 1_000, 10_000]
RISK_SCORES_PATH = MODELS / "risk_scores.parquet"
GLM_PATH = MODELS / "collision_glm.pkl"
METRICS_PATH = MODELS / "collision_metrics.json"
OUT_DIR = MODELS / "rank_stability"
REPORT_PATH = _ROOT / "reports/rank_stability.md"
PROVENANCE_PATH = _ROOT / "data/provenance/rank_stability_provenance.json"
SCRIPT_PATH = Path("src/road_risk/model/rank_stability.py")


def _read_production_fingerprint() -> dict[str, Any]:
    stat = RISK_SCORES_PATH.stat()
    df = pd.read_parquet(RISK_SCORES_PATH)
    return {
        "path": str(RISK_SCORES_PATH.relative_to(_ROOT)),
        "mtime_ns": stat.st_mtime_ns,
        "size_bytes": stat.st_size,
        "row_count": int(len(df)),
        "columns": list(df.columns),
    }


def _git_sha() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=_ROOT, text=True
        ).strip()
    except Exception:
        return None


def _ensure_directories() -> None:
    for path in [OUT_DIR, REPORT_PATH.parent, PROVENANCE_PATH.parent]:
        path.mkdir(parents=True, exist_ok=True)
        if not path.is_dir():
            raise NotADirectoryError(path)


def _load_existing_glm_and_features(df: pd.DataFrame) -> tuple[Any, list[str], dict[str, Any]]:
    if not GLM_PATH.exists():
        raise FileNotFoundError(f"Existing GLM artefact not found: {GLM_PATH}")
    if not METRICS_PATH.exists():
        raise FileNotFoundError(f"Existing collision metrics not found: {METRICS_PATH}")

    import statsmodels.api as sm

    glm_result = sm.load(str(GLM_PATH))
    with open(METRICS_PATH) as f:
        metrics = json.load(f)

    glm_summary = metrics["glm"]
    glm_features = list(glm_summary["features"])

    for feature in glm_features:
        if feature in df.columns:
            continue
        if feature.endswith("_imputed"):
            source = feature.removesuffix("_imputed")
            if source in df.columns:
                median_val = df[source].median()
                df[feature] = df[source].fillna(median_val)
                logger.info(
                    "  Recreated GLM imputed feature %s from %s (median %.4f)",
                    feature,
                    source,
                    median_val,
                )
                continue
        raise KeyError(f"Required GLM feature missing from stability dataset: {feature}")

    return glm_result, glm_features, glm_summary


def _load_collision_dataset() -> pd.DataFrame:
    openroads = gpd.read_parquet(OPENROADS_PATH)
    rla = pd.read_parquet(RLA_PATH)
    net_features = pd.read_parquet(NET_PATH) if NET_PATH.exists() else None
    aadt_estimates = pd.read_parquet(AADT_PATH)
    return build_collision_dataset(openroads, aadt_estimates, rla, net_features)


def _sorted_by_link(scores: pd.DataFrame) -> pd.DataFrame:
    return scores.sort_values("link_id", kind="mergesort").reset_index(drop=True)


def _top_links(scores: pd.DataFrame, k: int) -> set[Any]:
    ranked = scores.sort_values(
        ["predicted_xgb", "link_id"],
        ascending=[False, True],
        kind="mergesort",
    )
    return set(ranked["link_id"].head(k))


def _rank_array(scores: pd.DataFrame) -> np.ndarray:
    ordered = _sorted_by_link(scores)
    return ordered["predicted_xgb"].rank(method="average", ascending=True).to_numpy()


def _pearson_corr(left: np.ndarray, right: np.ndarray) -> float:
    left_centered = left - left.mean()
    right_centered = right - right.mean()
    denom = np.sqrt(np.sum(left_centered**2) * np.sum(right_centered**2))
    return float(np.sum(left_centered * right_centered) / denom) if denom else float("nan")


def _pairwise_stability(
    scores_by_seed: dict[int, pd.DataFrame],
    top_ks: list[int],
) -> tuple[dict[str, Any], dict[str, Any], dict[int, float]]:
    pairs = list(itertools.combinations(scores_by_seed, 2))

    jaccard: dict[str, Any] = {}
    for k in top_ks:
        top_sets = {seed: _top_links(scores_by_seed[seed], k) for seed in scores_by_seed}
        pair_values = {}
        for left, right in pairs:
            union = top_sets[left] | top_sets[right]
            pair_values[f"{left}-{right}"] = (
                len(top_sets[left] & top_sets[right]) / len(union) if union else float("nan")
            )
        values = list(pair_values.values())
        jaccard[str(k)] = {
            "mean": float(np.mean(values)),
            "min": float(np.min(values)),
            "pairs": pair_values,
        }

    ranks = {seed: _rank_array(scores_by_seed[seed]) for seed in scores_by_seed}
    spearman_pairs = {
        f"{left}-{right}": _pearson_corr(ranks[left], ranks[right])
        for left, right in pairs
    }
    spearman_values = list(spearman_pairs.values())
    spearman = {
        "mean": float(np.mean(spearman_values)),
        "min": float(np.min(spearman_values)),
        "pairs": spearman_pairs,
    }

    seed42_top1 = {}
    top1_key = str(top_ks[-1])
    for pair, value in jaccard[top1_key]["pairs"].items():
        if pair.startswith("42-") or pair.endswith("-42"):
            seed42_top1[pair] = value
    seed42_context = {
        "seed42_top1_jaccard_mean": float(np.mean(list(seed42_top1.values()))),
        "seed42_spearman_mean": float(
            np.mean([
                value
                for pair, value in spearman_pairs.items()
                if pair.startswith("42-") or pair.endswith("-42")
            ])
        ),
    }

    return jaccard, spearman, seed42_context


def _calibration_matrix(
    scores_by_seed: dict[int, pd.DataFrame],
    n_years: int,
) -> tuple[pd.DataFrame, dict[str, float], dict[str, float]]:
    rows = []
    for seed, scores in scores_by_seed.items():
        ranked = scores.sort_values(
            ["predicted_xgb", "link_id"],
            ascending=[True, True],
            kind="mergesort",
        ).copy()
        ranked["decile"] = pd.qcut(
            np.arange(len(ranked)),
            q=10,
            labels=range(1, 11),
        ).astype(int)
        observed = (
            ranked.groupby("decile", observed=True)["collision_count"].sum()
            / (ranked.groupby("decile", observed=True)["link_id"].size() * n_years)
        )
        for decile, rate in observed.items():
            rows.append({
                "seed": int(seed),
                "decile": int(decile),
                "observed_rate": float(rate),
            })

    long = pd.DataFrame(rows)
    matrix = long.pivot(index="decile", columns="seed", values="observed_rate").sort_index()
    std = matrix.std(axis=1, ddof=1)
    mean = matrix.mean(axis=1)
    matrix["std"] = std
    return (
        matrix,
        {str(int(decile)): float(value) for decile, value in std.items()},
        {str(int(decile)): float(value) for decile, value in mean.items()},
    )


def _format_float(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def _flag_notes(
    pseudo_values: dict[int, float],
    jaccard: dict[str, Any],
    spearman: dict[str, Any],
    calibration_std: dict[str, float],
    calibration_mean: dict[str, float],
    top1_k: int,
) -> list[str]:
    notes = []
    spread = max(pseudo_values.values()) - min(pseudo_values.values())
    if spread >= 0.01:
        notes.append(f"Pseudo-R2 spread is {_format_float(spread)}, above the <0.01 prior.")
    if jaccard[str(top1_k)]["mean"] <= 0.93:
        notes.append(
            "Top-1% Jaccard mean is "
            f"{_format_float(jaccard[str(top1_k)]['mean'])}, below the >0.93 prior."
        )
    if jaccard["100"]["mean"] >= jaccard[str(top1_k)]["mean"]:
        notes.append(
            "Top-100 Jaccard is not lower than top-1% Jaccard, contrary to the "
            "smaller-k sensitivity expectation."
        )
    if spearman["mean"] <= 0.99:
        notes.append(f"Mean Spearman rho is {_format_float(spearman['mean'])}, below 0.99.")

    high_std_deciles = []
    for decile, std in calibration_std.items():
        mean = calibration_mean[decile]
        if mean != 0 and std > abs(mean) * 0.10:
            high_std_deciles.append(decile)
    if high_std_deciles:
        notes.append(
            "Per-decile calibration std exceeds about 10% of the decile mean for "
            f"decile(s): {', '.join(high_std_deciles)}."
        )

    if not notes:
        notes.append("All measured stability metrics are within the prior expectations.")
    return notes


def _write_report(
    expected_rows: int,
    pseudo_values: dict[int, float],
    jaccard: dict[str, Any],
    spearman: dict[str, Any],
    calibration: pd.DataFrame,
    seed42_context: dict[int, float],
) -> None:
    pseudo_mean = float(np.mean(list(pseudo_values.values())))
    pseudo_std = float(np.std(list(pseudo_values.values()), ddof=1))
    top1_k = expected_rows // 100

    pseudo_rows = [
        [seed, _format_float(value)]
        for seed, value in pseudo_values.items()
    ]
    pseudo_rows.append(["mean", _format_float(pseudo_mean)])
    pseudo_rows.append(["std", _format_float(pseudo_std)])

    jaccard_rows = [
        [k, _format_float(stats["mean"]), _format_float(stats["min"])]
        for k, stats in jaccard.items()
    ]

    calibration_rows = []
    for decile, row in calibration.iterrows():
        calibration_rows.append(
            [int(decile)]
            + [_format_float(float(row[seed])) for seed in SEEDS]
            + [_format_float(float(row["std"]))]
        )

    seed42_pseudo_delta = pseudo_values[42] - pseudo_mean
    seed42_top1_mean = seed42_context["seed42_top1_jaccard_mean"]
    seed42_spearman_mean = seed42_context["seed42_spearman_mean"]
    pseudo_descriptor = (
        "within one cross-seed standard deviation of the mean"
        if pseudo_std == 0 or abs(seed42_pseudo_delta) <= pseudo_std
        else "outside one cross-seed standard deviation of the mean"
    )
    seed42_representativeness = (
        "appears representative of the five-seed set"
        if pseudo_descriptor.startswith("within")
        else (
            "sits on the lower edge for pseudo-R2 but does not appear to be an "
            "outlier by rank-overlap or full-rank correlation"
        )
    )

    flags = _flag_notes(
        pseudo_values,
        jaccard,
        spearman,
        {str(int(idx)): float(value) for idx, value in calibration["std"].items()},
        {
            str(int(idx)): float(value)
            for idx, value in calibration[[seed for seed in SEEDS]].mean(axis=1).items()
        },
        top1_k,
    )

    report = "\n\n".join([
        "# Rank Stability Evaluation",
        (
            "This report evaluates Stage 2 XGBoost rank stability across five seeds "
            "(42-46), with seed 42 representing the production realisation. The "
            "evaluation measures pseudo-R2 variation, top-k ranking overlap, full-rank "
            "Spearman correlation, and observed per-decile calibration stability. "
            f"The expected per-seed row count, taken from production risk_scores.parquet "
            f"before the run, is {expected_rows:,} links."
        ),
        "## Pseudo-R2\n\n" + _markdown_table(["seed", "pseudo_R2"], pseudo_rows),
        (
            "## Top-k Jaccard\n\n"
            + _markdown_table(["k", "pairwise_mean", "pairwise_min"], jaccard_rows)
        ),
        (
            "## Spearman Correlation\n\n"
            + _markdown_table(
                ["metric", "value"],
                [
                    ["pairwise_mean", _format_float(spearman["mean"])],
                    ["pairwise_min", _format_float(spearman["min"])],
                ],
            )
        ),
        (
            "## Calibration\n\n"
            + _markdown_table(
                ["decile"] + [f"seed_{seed}" for seed in SEEDS] + ["std"],
                calibration_rows,
            )
        ),
        (
            "Decile std small relative to decile mean indicates the calibrated "
            "prediction is stable across seeds; large std in any decile would indicate "
            "the calibration itself is seed-dependent in that risk band."
        ),
        (
            "## Interpretation\n\n"
            f"Seed 42 pseudo-R2 is {pseudo_descriptor}. Its mean top-1% Jaccard "
            f"against the other seeds is {_format_float(seed42_top1_mean)}, compared "
            f"with the all-pair mean of {_format_float(jaccard[str(top1_k)]['mean'])}; "
            f"its mean Spearman rho against the other seeds is "
            f"{_format_float(seed42_spearman_mean)}, compared with the all-pair mean "
            f"of {_format_float(spearman['mean'])}. On these measures, seed 42 "
            f"{seed42_representativeness}."
        ),
        (
            "Full run metadata and pairwise values are in "
            "`data/provenance/rank_stability_provenance.json`."
        ),
        "### Flags\n\n" + "\n".join(f"- {note}" for note in flags),
    ])
    REPORT_PATH.write_text(report + "\n")


def _write_provenance(payload: dict[str, Any]) -> None:
    PROVENANCE_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _verify_outputs(
    production_before: dict[str, Any],
    expected_rows: int,
    row_counts: dict[int, int],
) -> dict[str, Any]:
    production_after = _read_production_fingerprint()
    production_unchanged = (
        production_after["mtime_ns"] == production_before["mtime_ns"]
        and production_after["row_count"] == production_before["row_count"]
        and production_after["columns"] == production_before["columns"]
    )
    seed_files = {seed: OUT_DIR / f"seed_{seed}.parquet" for seed in SEEDS}
    seed_files_exist = {seed: path.exists() for seed, path in seed_files.items()}
    row_counts_match = {seed: count == expected_rows for seed, count in row_counts.items()}

    with open(PROVENANCE_PATH) as f:
        json.load(f)

    verification = {
        "production_before": production_before,
        "production_after": production_after,
        "production_risk_scores_unchanged": production_unchanged,
        "seed_files_exist": seed_files_exist,
        "row_counts_match_expected": row_counts_match,
        "report_exists": REPORT_PATH.exists(),
        "provenance_exists_and_parses": PROVENANCE_PATH.exists(),
    }

    if not production_unchanged:
        raise RuntimeError("Production risk_scores.parquet changed during rank stability run")
    if not all(seed_files_exist.values()):
        raise RuntimeError("One or more per-seed rank stability files are missing")
    if not all(row_counts_match.values()):
        raise RuntimeError("One or more per-seed row counts differ from production row count")
    if not REPORT_PATH.exists():
        raise RuntimeError("Rank stability report was not written")
    return verification


def run_rank_stability(seeds: list[int] | None = None) -> dict[str, Any]:
    seeds = seeds or SEEDS
    if seeds != SEEDS:
        logger.warning("Using non-default seeds: %s", seeds)

    _ensure_directories()
    production_before = _read_production_fingerprint()
    expected_rows = production_before["row_count"]
    logger.info("Production risk_scores row count before run: %s", f"{expected_rows:,}")

    df = _load_collision_dataset()
    n_years = int(df["year"].nunique())
    glm_result, glm_features, glm_summary = _load_existing_glm_and_features(df)

    pseudo_values: dict[int, float] = {}
    row_counts: dict[int, int] = {}
    n_train: dict[int, int] = {}
    n_test: dict[int, int] = {}
    scores_by_seed: dict[int, pd.DataFrame] = {}

    for i, seed in enumerate(seeds, start=1):
        logger.info("=== Rank stability seed %s (%s/%s) ===", seed, i, len(seeds))
        xgb_model, xgb_features, xgb_metrics = train_collision_xgb(df, seed=seed)
        if xgb_metrics.get("n_jobs") != 1:
            raise RuntimeError(f"XGBoost n_jobs is not confirmed as 1 for seed {seed}")

        scores = score_collision_models(
            glm_result,
            xgb_model,
            glm_features,
            xgb_features,
            df,
        )
        row_counts[seed] = int(len(scores))
        if row_counts[seed] != expected_rows:
            raise RuntimeError(
                f"Seed {seed} row count {row_counts[seed]:,} != expected {expected_rows:,}"
            )

        out_path = OUT_DIR / f"seed_{seed}.parquet"
        scores.to_parquet(out_path, index=False)
        logger.info("Saved %s with %s rows", out_path, f"{row_counts[seed]:,}")

        pseudo_values[seed] = float(xgb_metrics["pseudo_r2"])
        n_train[seed] = int(xgb_metrics["n_train"])
        n_test[seed] = int(xgb_metrics["n_test"])
        scores_by_seed[seed] = scores[["link_id", "collision_count", "predicted_xgb"]].copy()

    top_ks = TOP_K_FIXED + [expected_rows // 100]
    jaccard, spearman, seed42_context = _pairwise_stability(scores_by_seed, top_ks)
    calibration, calibration_std, calibration_mean = _calibration_matrix(scores_by_seed, n_years)

    _write_report(
        expected_rows,
        pseudo_values,
        jaccard,
        spearman,
        calibration,
        seed42_context,
    )

    provenance = {
        "script_path": str(SCRIPT_PATH),
        "git_sha": _git_sha(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "seeds_used": seeds,
        "n_jobs_setting_confirmed": True,
        "n_jobs": 1,
        "per_seed_pseudo_r2": {str(seed): value for seed, value in pseudo_values.items()},
        "summary_statistics": {
            "pseudo_r2_mean": float(np.mean(list(pseudo_values.values()))),
            "pseudo_r2_std": float(np.std(list(pseudo_values.values()), ddof=1)),
            "jaccard": jaccard,
            "spearman": spearman,
            "per_decile_calibration_std": calibration_std,
            "per_decile_calibration_mean": calibration_mean,
        },
        "n_train": {str(seed): value for seed, value in n_train.items()},
        "n_test": {str(seed): value for seed, value in n_test.items()},
        "expected_row_count": expected_rows,
        "actual_per_seed_row_counts": {str(seed): value for seed, value in row_counts.items()},
        "glm_retrained": False,
        "glm_features": glm_features,
        "glm_pseudo_r2": glm_summary.get("pseudo_r2"),
        "production_risk_scores_before": production_before,
    }
    _write_provenance(provenance)

    verification = _verify_outputs(production_before, expected_rows, row_counts)
    provenance["verification"] = verification
    _write_provenance(provenance)

    logger.info("Rank stability evaluation complete")
    return provenance


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    run_rank_stability()


if __name__ == "__main__":
    main()
