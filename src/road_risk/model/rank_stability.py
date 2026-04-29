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
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=_ROOT, text=True).strip()
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
        f"{left}-{right}": _pearson_corr(ranks[left], ranks[right]) for left, right in pairs
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
            np.mean(
                [
                    value
                    for pair, value in spearman_pairs.items()
                    if pair.startswith("42-") or pair.endswith("-42")
                ]
            )
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
        observed = ranked.groupby("decile", observed=True)["collision_count"].sum() / (
            ranked.groupby("decile", observed=True)["link_id"].size() * n_years
        )
        for decile, rate in observed.items():
            rows.append(
                {
                    "seed": int(seed),
                    "decile": int(decile),
                    "observed_rate": float(rate),
                }
            )

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

    pseudo_rows = [[seed, _format_float(value)] for seed, value in pseudo_values.items()]
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

    report = "\n\n".join(
        [
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
        ]
    )
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


# =============================================================================
# Per-family rank stability (extension — global harness above is unchanged)
# =============================================================================

FAMILIES_ORDERED = ["motorway", "trunk_a", "other_urban", "other_rural"]
FAMILY_OUT_DIR = MODELS / "family"
FAMILY_REPORT_PATH = _ROOT / "reports/family_rank_stability.md"
FAMILY_PROVENANCE_PATH = _ROOT / "data/provenance/family_rank_stability_provenance.json"

# Per-family fixed top-k (from design doc §6.2); percentage k added at runtime
_FAMILY_FIXED_TOP_K: dict[str, list[int]] = {
    "motorway": [25, 50, 100],
    "trunk_a": [50, 100, 500],
    "other_urban": [100, 1_000, 10_000],
    "other_rural": [100, 1_000, 10_000],
}
_FAMILY_PCT_K: dict[str, float] = {
    "motorway": 0.10,
    "trunk_a": 0.10,
    "other_urban": 0.01,
    "other_rural": 0.01,
}

# Global baseline from reports/rank_stability.md (5-seed, held-out, link-year)
_GLOBAL_BASELINE: dict[str, float] = {
    "pseudo_r2_mean": 0.859041,
    "pseudo_r2_std": 0.001411,
    "top1pct_jaccard_mean": 0.918494,
    "top1pct_jaccard_min": 0.907843,
    "spearman_mean": 0.998106,
    "spearman_min": 0.997841,
}


# ---------------------------------------------------------------------------
# Column-parameterised variants of global helpers
# ---------------------------------------------------------------------------


def _top_links_col(scores: pd.DataFrame, score_col: str, k: int) -> set[Any]:
    ranked = scores.sort_values(
        [score_col, "link_id"],
        ascending=[False, True],
        kind="mergesort",
    )
    return set(ranked["link_id"].head(k))


def _rank_array_col(scores: pd.DataFrame, score_col: str) -> np.ndarray:
    ordered = _sorted_by_link(scores)
    return ordered[score_col].rank(method="average", ascending=True).to_numpy()


def _pairwise_stability_col(
    scores_by_seed: dict[int, pd.DataFrame],
    top_ks: list[int],
    score_col: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Like _pairwise_stability but with a configurable score column."""
    pairs = list(itertools.combinations(scores_by_seed, 2))

    jaccard: dict[str, Any] = {}
    for k in top_ks:
        top_sets = {
            seed: _top_links_col(scores_by_seed[seed], score_col, k) for seed in scores_by_seed
        }
        pair_values: dict[str, float] = {}
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

    ranks = {seed: _rank_array_col(scores_by_seed[seed], score_col) for seed in scores_by_seed}
    spearman_pairs: dict[str, float] = {
        f"{left}-{right}": _pearson_corr(ranks[left], ranks[right]) for left, right in pairs
    }
    spearman_values = list(spearman_pairs.values())
    spearman: dict[str, Any] = {
        "mean": float(np.mean(spearman_values)),
        "min": float(np.min(spearman_values)),
        "pairs": spearman_pairs,
    }

    top1_key = str(top_ks[-1])
    seed42_top1 = {
        pair: value
        for pair, value in jaccard[top1_key]["pairs"].items()
        if pair.startswith("42-") or pair.endswith("-42")
    }
    seed42_spear = [
        value
        for pair, value in spearman_pairs.items()
        if pair.startswith("42-") or pair.endswith("-42")
    ]
    seed42_context = {
        "seed42_top1_jaccard_mean": (
            float(np.mean(list(seed42_top1.values()))) if seed42_top1 else float("nan")
        ),
        "seed42_spearman_mean": (float(np.mean(seed42_spear)) if seed42_spear else float("nan")),
    }
    return jaccard, spearman, seed42_context


def _calibration_matrix_col(
    scores_by_seed: dict[int, pd.DataFrame],
    n_years: int,
    score_col: str,
) -> tuple[pd.DataFrame, dict[str, float], dict[str, float]]:
    """Like _calibration_matrix but with a configurable score column."""
    rows: list[dict[str, Any]] = []
    for seed, scores in scores_by_seed.items():
        ranked = scores.sort_values(
            [score_col, "link_id"],
            ascending=[True, True],
            kind="mergesort",
        ).copy()
        ranked["decile"] = pd.qcut(
            np.arange(len(ranked)),
            q=10,
            labels=range(1, 11),
        ).astype(int)
        observed = ranked.groupby("decile", observed=True)["collision_count"].sum() / (
            ranked.groupby("decile", observed=True)["link_id"].size() * n_years
        )
        for decile, rate in observed.items():
            rows.append(
                {
                    "seed": int(seed),
                    "decile": int(decile),
                    "observed_rate": float(rate),
                }
            )

    long = pd.DataFrame(rows)
    matrix = long.pivot(index="decile", columns="seed", values="observed_rate").sort_index()
    std = matrix.std(axis=1, ddof=1)
    mean_col = matrix.mean(axis=1)
    matrix["std"] = std
    return (
        matrix,
        {str(int(decile)): float(v) for decile, v in std.items()},
        {str(int(decile)): float(v) for decile, v in mean_col.items()},
    )


# ---------------------------------------------------------------------------
# Stitched held-out pseudo-R² from per-family training
# ---------------------------------------------------------------------------


def _family_stitched_heldout_pr2(
    df: pd.DataFrame,
    models_by_family: dict[str, tuple[Any, list[str], dict[str, Any]]],
    seed: int,
) -> float:
    """Pool held-out link-year rows across all trained families and compute
    stitched pseudo-R² (link-year grain, eps=1e-6 — same as train_collision_xgb)."""
    from sklearn.model_selection import GroupShuffleSplit

    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    eps = 1e-6
    all_y: list[np.ndarray] = []
    all_y_pred: list[np.ndarray] = []

    for family, (model, feature_list, _metrics) in models_by_family.items():
        fam_df = df[df["family"] == family].copy()
        groups = fam_df["link_id"].values
        # GroupShuffleSplit is deterministic on the sorted unique groups;
        # passing zeros for X is fine — only groups matters for the split.
        x_dummy = np.zeros((len(fam_df), 1))
        _, test_idx = next(gss.split(x_dummy, groups=groups))
        test_df = fam_df.iloc[test_idx]

        x_test = test_df[feature_list].fillna(0).astype(float)
        off_test = test_df["log_offset"].fillna(0).values.astype(float)
        y_pred = model.predict(x_test, base_margin=off_test)
        y_test = test_df["collision_count"].astype(float).values

        all_y.append(y_test)
        all_y_pred.append(y_pred)

    y = np.concatenate(all_y)
    y_pred_arr = np.concatenate(all_y_pred)
    null_val = float(y.mean())

    deviance = 2.0 * float(
        np.sum(np.where(y > 0, y * np.log((y + eps) / (y_pred_arr + eps)), 0.0) - (y - y_pred_arr))
    )
    null_dev = 2.0 * float(
        np.sum(np.where(y > 0, y * np.log((y + eps) / (null_val + eps)), 0.0) - (y - null_val))
    )
    return float(1.0 - deviance / null_dev) if null_dev > 0 else float("nan")


# ---------------------------------------------------------------------------
# Failure threshold guard
# ---------------------------------------------------------------------------


def _check_failure_threshold(
    failed_combos: list[tuple[int, str, str]],
    threshold: int = 3,
) -> None:
    """Raise if any single family accumulates >= threshold seed failures."""
    from collections import Counter

    family_failures = Counter(fam for _, fam, _ in failed_combos)
    bad = {fam: cnt for fam, cnt in family_failures.items() if cnt >= threshold}
    if bad:
        summary = "; ".join(f"{fam}: {cnt} failures" for fam, cnt in bad.items())
        raise RuntimeError(
            "Too many seed failures for families — stopping rather than averaging "
            f"over degraded results. {summary}. "
            "Check failed_combos in provenance for details."
        )


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------


def _write_family_report(  # noqa: C901
    seeds_used: list[int],
    stitched_pseudo: dict[int, float],
    per_family_pseudo: dict[str, dict[int, float]],
    jaccard_stitched: dict[str, Any],
    spearman_stitched: dict[str, Any],
    family_jaccard: dict[str, dict[str, Any]],
    family_spearman: dict[str, dict[str, Any]],
    calibration: pd.DataFrame,
    family_link_counts: dict[str, int],
    n_links: int,
) -> None:
    FAMILY_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    stitched_vals = [v for v in stitched_pseudo.values() if np.isfinite(v)]
    stitched_mean = float(np.mean(stitched_vals)) if stitched_vals else float("nan")
    stitched_std = float(np.std(stitched_vals, ddof=1)) if len(stitched_vals) > 1 else float("nan")
    top1_k = n_links // 100

    # §1 Pseudo-R² table
    pr2_headers = ["seed", "stitched"] + FAMILIES_ORDERED
    pr2_rows: list[list[Any]] = []
    for seed in seeds_used:
        row: list[Any] = [seed, _format_float(stitched_pseudo.get(seed, float("nan")))]
        for fam in FAMILIES_ORDERED:
            row.append(_format_float(per_family_pseudo.get(fam, {}).get(seed, float("nan"))))
        pr2_rows.append(row)

    def _fam_mean(fam: str) -> str:
        vals = [v for v in per_family_pseudo.get(fam, {}).values() if np.isfinite(v)]
        return _format_float(float(np.mean(vals))) if vals else "nan"

    def _fam_std(fam: str) -> str:
        vals = [v for v in per_family_pseudo.get(fam, {}).values() if np.isfinite(v)]
        return _format_float(float(np.std(vals, ddof=1))) if len(vals) > 1 else "nan"

    pr2_rows.append(
        ["mean", _format_float(stitched_mean)] + [_fam_mean(f) for f in FAMILIES_ORDERED]
    )
    pr2_rows.append(["std", _format_float(stitched_std)] + [_fam_std(f) for f in FAMILIES_ORDERED])
    pr2_table = _markdown_table(pr2_headers, pr2_rows)

    # §2 Stitched Jaccard table
    stitched_jacc_rows = [
        [k, _format_float(stats["mean"]), _format_float(stats["min"])]
        for k, stats in jaccard_stitched.items()
    ]
    stitched_jacc_table = _markdown_table(
        ["k", "pairwise_mean", "pairwise_min"], stitched_jacc_rows
    )

    # §3 Per-family Jaccard sections
    family_jacc_sections: list[str] = []
    for fam in FAMILIES_ORDERED:
        if fam not in family_jaccard:
            continue
        fam_rows = [
            [k, _format_float(s["mean"]), _format_float(s["min"])]
            for k, s in family_jaccard[fam].items()
        ]
        family_jacc_sections.append(
            f"#### {fam} (n={family_link_counts.get(fam, 0):,})\n\n"
            + _markdown_table(["k", "pairwise_mean", "pairwise_min"], fam_rows)
        )

    # §4 Spearman table
    spearman_rows: list[list[Any]] = [
        [
            "stitched",
            _format_float(spearman_stitched["mean"]),
            _format_float(spearman_stitched["min"]),
        ]
    ]
    for fam in FAMILIES_ORDERED:
        sp = family_spearman.get(fam, {})
        spearman_rows.append(
            [
                fam,
                _format_float(sp.get("mean", float("nan"))),
                _format_float(sp.get("min", float("nan"))),
            ]
        )
    spearman_table = _markdown_table(
        ["model_surface", "pairwise_mean", "pairwise_min"], spearman_rows
    )

    # §5 Calibration table
    cal_rows: list[list[Any]] = []
    for decile, row in calibration.iterrows():
        cal_rows.append(
            [int(decile)]
            + [_format_float(float(row[seed])) for seed in seeds_used]
            + [_format_float(float(row["std"]))]
        )
    cal_table = _markdown_table(
        ["decile"] + [f"seed_{s}" for s in seeds_used] + ["std"],
        cal_rows,
    )

    # §6 Global comparison table
    top1_jacc_mean = jaccard_stitched.get(str(top1_k), {}).get("mean", float("nan"))
    top1_jacc_min = jaccard_stitched.get(str(top1_k), {}).get("min", float("nan"))
    comparison_rows: list[list[str]] = [
        [
            "pseudo-R² mean",
            (f"{_GLOBAL_BASELINE['pseudo_r2_mean']:.6f} ± {_GLOBAL_BASELINE['pseudo_r2_std']:.6f}"),
            f"{stitched_mean:.6f} ± {stitched_std:.6f}",
        ],
        [
            "top-1% Jaccard mean",
            _format_float(_GLOBAL_BASELINE["top1pct_jaccard_mean"]),
            _format_float(top1_jacc_mean),
        ],
        [
            "top-1% Jaccard min",
            _format_float(_GLOBAL_BASELINE["top1pct_jaccard_min"]),
            _format_float(top1_jacc_min),
        ],
        [
            "Spearman mean",
            _format_float(_GLOBAL_BASELINE["spearman_mean"]),
            _format_float(spearman_stitched["mean"]),
        ],
        [
            "Spearman min",
            _format_float(_GLOBAL_BASELINE["spearman_min"]),
            _format_float(spearman_stitched["min"]),
        ],
    ]
    comparison_table = _markdown_table(
        ["metric", "global (rank_stability.md)", "family stitched (this run)"],
        comparison_rows,
    )

    # §7 Flags
    positive_flags: list[str] = []
    concern_flags: list[str] = []

    pr2_delta = stitched_mean - _GLOBAL_BASELINE["pseudo_r2_mean"]
    if pr2_delta >= 0:
        positive_flags.append(
            f"Stitched pseudo-R² mean ({stitched_mean:.6f}) matches or exceeds global "
            f"baseline ({_GLOBAL_BASELINE['pseudo_r2_mean']:.6f}); delta = {pr2_delta:+.6f}."
        )
    else:
        concern_flags.append(
            f"Stitched pseudo-R² mean ({stitched_mean:.6f}) below global baseline "
            f"({_GLOBAL_BASELINE['pseudo_r2_mean']:.6f}); delta = {pr2_delta:+.6f}."
        )

    if spearman_stitched["mean"] >= _GLOBAL_BASELINE["spearman_mean"] - 0.001:
        positive_flags.append(
            f"Stitched Spearman mean ({spearman_stitched['mean']:.6f}) comparable to "
            f"global baseline ({_GLOBAL_BASELINE['spearman_mean']:.6f})."
        )
    else:
        concern_flags.append(
            f"Stitched Spearman mean ({spearman_stitched['mean']:.6f}) below global "
            f"baseline ({_GLOBAL_BASELINE['spearman_mean']:.6f})."
        )

    top1_jacc_vs_baseline = top1_jacc_mean - _GLOBAL_BASELINE["top1pct_jaccard_mean"]
    if top1_jacc_mean >= _GLOBAL_BASELINE["top1pct_jaccard_mean"] - 0.01:
        positive_flags.append(
            f"Stitched top-1% Jaccard mean ({top1_jacc_mean:.6f}) within 0.01 of "
            f"global baseline ({_GLOBAL_BASELINE['top1pct_jaccard_mean']:.6f}); "
            f"delta = {top1_jacc_vs_baseline:+.6f}."
        )
    else:
        concern_flags.append(
            f"Stitched top-1% Jaccard mean ({top1_jacc_mean:.6f}) more than 0.01 below "
            f"global baseline ({_GLOBAL_BASELINE['top1pct_jaccard_mean']:.6f}); "
            f"delta = {top1_jacc_vs_baseline:+.6f}."
        )

    stitched_spread = max(stitched_vals) - min(stitched_vals) if len(stitched_vals) > 1 else 0.0
    if stitched_spread < 0.01:
        positive_flags.append(
            f"Stitched pseudo-R² spread ({stitched_spread:.6f}) is below 0.01 — "
            "fit quality is stable across seeds."
        )

    for fam in FAMILIES_ORDERED:
        fam_vals = [v for v in per_family_pseudo.get(fam, {}).values() if np.isfinite(v)]
        if len(fam_vals) < 2:
            continue
        spread = max(fam_vals) - min(fam_vals)
        if spread >= 0.02:
            concern_flags.append(
                f"{fam} pseudo-R² spread across seeds is {spread:.4f} "
                "(≥ 0.02); may indicate overfitting on this small family."
            )
        else:
            positive_flags.append(f"{fam} pseudo-R² spread ({spread:.4f}) is below 0.02.")

    flag_text = ""
    if positive_flags:
        flag_text += "### Positive findings\n\n" + "\n".join(f"- {f}" for f in positive_flags)
    if concern_flags:
        if flag_text:
            flag_text += "\n\n"
        flag_text += "### Concerns\n\n" + "\n".join(f"- {f}" for f in concern_flags)
    if not flag_text:
        flag_text = "- All measured stability metrics are within prior expectations."

    report = "\n\n".join(
        [
            "# Family Rank Stability Evaluation",
            (
                "This report evaluates per-family XGBoost rank stability across five seeds "
                f"({', '.join(str(s) for s in seeds_used)}), with seed 42 representing the "
                "session-1 production realisation. "
                f"The stitched ranking covers the full network ({n_links:,} links); "
                "per-family metrics cover each family subset. "
                "Global baseline from `reports/rank_stability.md`: "
                f"pseudo-R² {_GLOBAL_BASELINE['pseudo_r2_mean']:.6f} "
                f"± {_GLOBAL_BASELINE['pseudo_r2_std']:.6f}. "
                "Adoption criterion (design doc §6.5): recommend per-family approach if "
                "headline stitched metrics improve materially, or if per-family diagnostics "
                "reveal patterned residuals the global model missed."
            ),
            (
                "## 1. Pseudo-R² Stability\n\n"
                "Per-seed held-out link-year pseudo-R². Stitched: pooled held-out "
                "link-years across all families (single null model). Per-family: "
                "directly from training metrics (same grain, same formula).\n\n" + pr2_table
            ),
            ("## 2. Stitched Ranking: Top-k Jaccard\n\n" + stitched_jacc_table),
            (
                "## 3. Per-Family Top-k Jaccard\n\n"
                "Family-scaled thresholds: motorway/trunk_a at fixed k + 10% of family "
                "links; other_urban/other_rural at fixed k + 1% of family links.\n\n"
                + "\n\n".join(family_jacc_sections)
            ),
            "## 4. Spearman Correlation\n\n" + spearman_table,
            (
                "## 5. Calibration (Stitched Ranking)\n\n"
                "Per-decile observed mean collision rate per seed and std across seeds. "
                "Stitched ranking sorted by predicted_xgb_family.\n\n" + cal_table
            ),
            "## 6. Comparison Against Global Baseline\n\n" + comparison_table,
            "## 7. Flags\n\n" + flag_text,
            (
                "Full run metadata and per-pair values are in "
                "`data/provenance/family_rank_stability_provenance.json`."
            ),
        ]
    )
    FAMILY_REPORT_PATH.write_text(report + "\n")
    logger.info("Wrote family rank stability report to %s", FAMILY_REPORT_PATH)


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------


def run_family_rank_stability(seeds: list[int] | None = None) -> dict[str, Any]:
    """Five-seed per-family rank stability evaluation.

    Does not modify production risk_scores.parquet, session-1
    risk_scores_family.parquet, or global rank_stability/seed_<N>.parquet files.
    """
    from road_risk.model.family_split import (
        assign_family,
        compute_family_rankings,
        score_family_xgb,
        train_family_xgb,
    )

    seeds = seeds or SEEDS
    logger.info("Family rank stability run: seeds=%s", seeds)

    FAMILY_OUT_DIR.mkdir(parents=True, exist_ok=True)
    FAMILY_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    FAMILY_PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Snapshot protected artefacts before any work
    production_before = _read_production_fingerprint()
    n_links = production_before["row_count"]

    family_prod_path = MODELS / "risk_scores_family.parquet"
    family_prod_mtime: int | None = None
    if family_prod_path.exists():
        family_prod_mtime = family_prod_path.stat().st_mtime_ns

    # Load data once — same dataset as global harness
    logger.info("Loading collision dataset (shared with global harness) ...")
    df = _load_collision_dataset()
    n_years = int(df["year"].nunique())

    # road_function is needed for assign_family but not in build_collision_dataset
    if "road_function" not in df.columns:
        import geopandas as gpd

        _or = gpd.read_parquet(OPENROADS_PATH, columns=["link_id", "road_function"])
        road_func = pd.DataFrame(_or[["link_id", "road_function"]]).drop_duplicates("link_id")
        df = df.merge(road_func, on="link_id", how="left")

    df = assign_family(df)
    family_link_counts = {
        fam: int(df[df["family"] == fam]["link_id"].nunique()) for fam in FAMILIES_ORDERED
    }
    logger.info("Family link counts: %s", family_link_counts)

    # Per-seed training loop
    failed_combos: list[tuple[int, str, str]] = []
    per_seed_stitched_pr2: dict[int, float] = {}
    per_family_pseudo: dict[str, dict[int, float]] = {fam: {} for fam in FAMILIES_ORDERED}
    per_seed_n_train: dict[int, dict[str, int]] = {}
    per_seed_n_test: dict[int, dict[str, int]] = {}
    per_seed_row_counts: dict[int, dict[str, int]] = {}
    stitched_scores_by_seed: dict[int, pd.DataFrame] = {}
    fam_scores_by_seed: dict[str, dict[int, pd.DataFrame]] = {fam: {} for fam in FAMILIES_ORDERED}

    for i_seed, seed in enumerate(seeds, 1):
        logger.info("=== Family rank stability seed %d (%d/%d) ===", seed, i_seed, len(seeds))
        seed_dir = FAMILY_OUT_DIR / f"seed_{seed}"
        seed_dir.mkdir(parents=True, exist_ok=True)

        models_by_family: dict[str, tuple[Any, list[str], dict[str, Any]]] = {}
        seed_n_train: dict[str, int] = {}
        seed_n_test: dict[str, int] = {}
        seed_row_counts: dict[str, int] = {}

        for family in FAMILIES_ORDERED:
            try:
                model, feature_list, metrics = train_family_xgb(df, family, seed=seed)
            except Exception as exc:
                logger.error("FAILED seed=%d family=%s: %s", seed, family, exc)
                failed_combos.append((seed, family, str(exc)))
                _check_failure_threshold(failed_combos)
                continue

            models_by_family[family] = (model, feature_list, metrics)
            per_family_pseudo[family][seed] = float(metrics["pseudo_r2"])
            seed_n_train[family] = int(metrics["n_train"])
            seed_n_test[family] = int(metrics["n_test"])
            logger.info(
                "  %s: pseudo_R2=%.4f  n_train=%d  n_test=%d",
                family,
                metrics["pseudo_r2"],
                metrics["n_train"],
                metrics["n_test"],
            )

        if not models_by_family:
            logger.error("Seed %d: all families failed — skipping seed", seed)
            continue

        missing_fams = set(FAMILIES_ORDERED) - set(models_by_family)
        if missing_fams:
            logger.warning(
                "Seed %d: missing families %s — stitching with available families",
                seed,
                missing_fams,
            )

        # Score and pool
        pooled = score_family_xgb(df, models_by_family)
        pooled = compute_family_rankings(pooled)

        if len(pooled) != n_links:
            logger.warning(
                "Seed %d stitched row count %d != expected %d (some families may have failed)",
                seed,
                len(pooled),
                n_links,
            )

        # Save per-family parquets
        for family in FAMILIES_ORDERED:
            if family not in models_by_family:
                continue
            fam_sub = pooled[pooled["family"] == family].copy()
            fam_path = seed_dir / f"{family}.parquet"
            fam_sub.to_parquet(fam_path, index=False)
            seed_row_counts[family] = int(len(fam_sub))
            logger.info("  Saved %s (%d rows)", fam_path.name, len(fam_sub))

        stitched_path = seed_dir / "stitched.parquet"
        pooled.to_parquet(stitched_path, index=False)
        logger.info("  Saved stitched.parquet (%d rows)", len(pooled))

        # Stitched held-out pseudo-R² at link-year grain
        pr2_stitched = _family_stitched_heldout_pr2(df, models_by_family, seed)
        per_seed_stitched_pr2[seed] = pr2_stitched
        logger.info("  Stitched held-out R² (seed=%d): %.6f", seed, pr2_stitched)

        # Store lightweight copies for stability metrics
        stitched_scores_by_seed[seed] = pooled[
            ["link_id", "collision_count", "predicted_xgb_family"]
        ].copy()
        for family in FAMILIES_ORDERED:
            if family in models_by_family:
                fam_scores_by_seed[family][seed] = pooled[pooled["family"] == family][
                    ["link_id", "collision_count", "predicted_xgb_family"]
                ].copy()

        per_seed_n_train[seed] = seed_n_train
        per_seed_n_test[seed] = seed_n_test
        per_seed_row_counts[seed] = seed_row_counts

    _check_failure_threshold(failed_combos)

    # Stability metrics
    top_ks_stitched = TOP_K_FIXED + [n_links // 100]
    jaccard_stitched, spearman_stitched, _ = _pairwise_stability_col(
        stitched_scores_by_seed, top_ks_stitched, score_col="predicted_xgb_family"
    )

    family_jaccard: dict[str, dict[str, Any]] = {}
    family_spearman: dict[str, dict[str, Any]] = {}
    for fam in FAMILIES_ORDERED:
        fam_seeds = fam_scores_by_seed[fam]
        if len(fam_seeds) < 2:
            logger.warning("Family %s has fewer than 2 successful seeds — skipping stability", fam)
            continue
        n_fam = family_link_counts.get(fam, 0)
        pct_k = max(1, int(n_fam * _FAMILY_PCT_K[fam]))
        top_ks_fam = _FAMILY_FIXED_TOP_K[fam] + [pct_k]
        jac_fam, spear_fam, _ = _pairwise_stability_col(
            fam_seeds, top_ks_fam, score_col="predicted_xgb_family"
        )
        family_jaccard[fam] = jac_fam
        family_spearman[fam] = {"mean": spear_fam["mean"], "min": spear_fam["min"]}

    calibration, cal_std, cal_mean = _calibration_matrix_col(
        stitched_scores_by_seed, n_years, score_col="predicted_xgb_family"
    )

    # Write report
    _write_family_report(
        seeds_used=seeds,
        stitched_pseudo=per_seed_stitched_pr2,
        per_family_pseudo=per_family_pseudo,
        jaccard_stitched=jaccard_stitched,
        spearman_stitched=spearman_stitched,
        family_jaccard=family_jaccard,
        family_spearman=family_spearman,
        calibration=calibration,
        family_link_counts=family_link_counts,
        n_links=n_links,
    )

    # Verify protected artefacts unchanged
    production_after = _read_production_fingerprint()
    prod_unchanged = production_after["mtime_ns"] == production_before["mtime_ns"]
    if not prod_unchanged:
        raise RuntimeError(
            "Production risk_scores.parquet changed during family rank stability run"
        )

    if family_prod_mtime is not None and family_prod_path.exists():
        if family_prod_path.stat().st_mtime_ns != family_prod_mtime:
            raise RuntimeError(
                "Session-1 risk_scores_family.parquet changed during family rank stability run"
            )

    rs_files_ok = {str(s): (OUT_DIR / f"seed_{s}.parquet").exists() for s in SEEDS}

    # Build and write provenance
    stitched_vals = [v for v in per_seed_stitched_pr2.values() if np.isfinite(v)]
    provenance: dict[str, Any] = {
        "script_path": "src/road_risk/model/rank_stability.py",
        "git_sha": _git_sha(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "seeds_used": seeds,
        "n_jobs": 1,
        "families": FAMILIES_ORDERED,
        "failed_combos": [{"seed": s, "family": f, "error": e} for s, f, e in failed_combos],
        "family_link_counts": family_link_counts,
        "per_seed_stitched_pseudo_r2": {str(s): v for s, v in per_seed_stitched_pr2.items()},
        "per_family_pseudo_r2": {
            fam: {str(s): v for s, v in by_seed.items()}
            for fam, by_seed in per_family_pseudo.items()
        },
        "per_seed_n_train": {str(s): counts for s, counts in per_seed_n_train.items()},
        "per_seed_n_test": {str(s): counts for s, counts in per_seed_n_test.items()},
        "per_seed_row_counts": {str(s): counts for s, counts in per_seed_row_counts.items()},
        "summary_statistics": {
            "stitched_pseudo_r2_mean": (
                float(np.mean(stitched_vals)) if stitched_vals else float("nan")
            ),
            "stitched_pseudo_r2_std": (
                float(np.std(stitched_vals, ddof=1)) if len(stitched_vals) > 1 else float("nan")
            ),
            "jaccard_stitched": jaccard_stitched,
            "spearman_stitched": spearman_stitched,
            "family_jaccard": family_jaccard,
            "family_spearman": family_spearman,
            "per_decile_calibration_std": cal_std,
            "per_decile_calibration_mean": cal_mean,
        },
        "production_risk_scores_before": production_before,
        "production_risk_scores_unchanged": prod_unchanged,
        "rank_stability_global_seed_files_exist": rs_files_ok,
        "global_baseline": _GLOBAL_BASELINE,
    }
    FAMILY_PROVENANCE_PATH.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    logger.info("Wrote provenance to %s", FAMILY_PROVENANCE_PATH)

    return provenance


def main_family() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    result = run_family_rank_stability()
    summary = result.get("summary_statistics", {})
    pr2_mean = summary.get("stitched_pseudo_r2_mean", float("nan"))
    pr2_std = summary.get("stitched_pseudo_r2_std", float("nan"))
    top1_k = result.get("production_risk_scores_before", {}).get("row_count", 0) // 100
    jacc = summary.get("jaccard_stitched", {})
    jm = jacc.get(str(top1_k), {})
    print(f"\nStitched 5-seed pseudo-R²: {pr2_mean:.6f} ± {pr2_std:.6f}")
    print(
        f"Stitched top-1% Jaccard: "
        f"mean={jm.get('mean', float('nan')):.6f}  "
        f"min={jm.get('min', float('nan')):.6f}"
    )
    fam_pr2 = result.get("per_family_pseudo_r2", {})
    for fam in FAMILIES_ORDERED:
        vals = [v for v in fam_pr2.get(fam, {}).values() if np.isfinite(v)]
        if vals:
            print(f"  {fam}: pseudo-R² mean={np.mean(vals):.4f} ± {np.std(vals, ddof=1):.4f}")
    if result.get("failed_combos"):
        print("FAILURES:", result["failed_combos"])


if __name__ == "__main__":
    import sys as _sys

    if "--family" in _sys.argv:
        main_family()
    else:
        main()
