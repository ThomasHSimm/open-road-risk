"""
Method-of-moments dispersion estimate for EB-style risk shrinkage.

This module estimates a single global NB2 dispersion parameter from existing
Stage 2 link-year predictions. It does not train models, apply EB scores, or
modify production risk score artefacts.
"""

from __future__ import annotations

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
)

logger = logging.getLogger(__name__)

METRICS_PATH = MODELS / "collision_metrics.json"
XGB_MODEL_PATH = MODELS / "collision_xgb.json"
PROVENANCE_PATH = _ROOT / "data/provenance/eb_dispersion_provenance.json"
REPORT_PATH = _ROOT / "reports/eb_dispersion.md"
SCRIPT_PATH = Path("src/road_risk/model/eb_dispersion.py")

N_QUANTILE_BINS = 20
MIN_LINK_YEARS_PER_BIN = 10_000
MIN_POSITIVE_ROWS_PER_BIN = 100
NEGATIVE_BIN_FAIL_FRACTION = 0.25


def _git_sha() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=_ROOT, text=True).strip()
    except Exception:
        return None


def _fingerprint_dataframe(path: Path, df: pd.DataFrame) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": str(path.relative_to(_ROOT)),
        "mtime_ns": stat.st_mtime_ns,
        "size_bytes": stat.st_size,
        "row_count": int(len(df)),
        "columns": list(df.columns),
    }


def _fingerprint_file(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": str(path.relative_to(_ROOT)),
        "mtime_ns": stat.st_mtime_ns,
        "size_bytes": stat.st_size,
    }


def _load_stage2_dataset() -> tuple[pd.DataFrame, dict[str, Any]]:
    logger.info("Loading Stage 2 inputs and rebuilding link-year table ...")
    openroads = gpd.read_parquet(OPENROADS_PATH)
    rla = pd.read_parquet(RLA_PATH)
    net_features = pd.read_parquet(NET_PATH) if NET_PATH.exists() else None
    aadt_estimates = pd.read_parquet(AADT_PATH)

    fingerprints = {
        "openroads": _fingerprint_dataframe(OPENROADS_PATH, openroads),
        "road_link_annual": _fingerprint_dataframe(RLA_PATH, rla),
        "aadt_estimates": _fingerprint_dataframe(AADT_PATH, aadt_estimates),
        "network_features": (
            _fingerprint_dataframe(NET_PATH, net_features) if net_features is not None else None
        ),
        "collision_xgb_model": _fingerprint_file(XGB_MODEL_PATH),
        "collision_metrics": _fingerprint_file(METRICS_PATH),
    }

    df = build_collision_dataset(openroads, aadt_estimates, rla, net_features)
    fingerprints["constructed_link_year_table"] = {
        "row_count": int(len(df)),
        "columns": list(df.columns),
        "n_links": int(df["link_id"].nunique()),
        "years": [int(year) for year in sorted(df["year"].unique())],
    }
    return df, fingerprints


def _load_xgb_features() -> list[str]:
    with open(METRICS_PATH) as f:
        metrics = json.load(f)
    return list(metrics["xgb"]["features"])


def _score_link_year_predictions(df: pd.DataFrame, feature_cols: list[str]) -> np.ndarray:
    try:
        from xgboost import XGBRegressor
    except ImportError as e:
        raise ImportError("pip install xgboost") from e

    missing = [col for col in feature_cols if col not in df.columns]
    if missing:
        raise KeyError(f"XGBoost feature(s) missing from link-year table: {missing}")

    logger.info("Loading existing XGBoost model from %s", XGB_MODEL_PATH)
    model = XGBRegressor()
    model.load_model(str(XGB_MODEL_PATH))
    model.set_params(n_jobs=1)

    logger.info("Scoring %s link-years with existing XGBoost model ...", f"{len(df):,}")
    X = df[feature_cols].fillna(0).astype("float32")
    base_margin = df["log_offset"].fillna(0).to_numpy(dtype=np.float32)
    predictions = model.predict(X, base_margin=base_margin)
    if np.any(predictions < 0):
        raise ValueError("XGBoost produced negative count predictions")
    return predictions.astype(np.float64, copy=False)


def _initial_bin_ids(predicted: np.ndarray, n_bins: int) -> tuple[np.ndarray, list[dict[str, Any]]]:
    quantiles = np.linspace(0, 1, n_bins + 1)
    edges = np.quantile(predicted, quantiles)
    unique_edges = np.unique(edges)
    if len(unique_edges) < 2:
        raise ValueError("Cannot form prediction bins: predicted_xgb is constant")
    bin_ids = np.searchsorted(unique_edges[1:-1], predicted, side="right")

    definitions = []
    for bin_index in range(len(unique_edges) - 1):
        definitions.append(
            {
                "initial_bin_index": int(bin_index),
                "predicted_xgb_lower": float(unique_edges[bin_index]),
                "predicted_xgb_upper": float(unique_edges[bin_index + 1]),
            }
        )
    return bin_ids.astype(np.int16, copy=False), definitions


def _summarize_bin(
    predicted: np.ndarray,
    observed: np.ndarray,
    member_indices: list[int],
    bin_index: int,
    source_bins: list[int],
) -> dict[str, Any]:
    idx = np.asarray(member_indices, dtype=np.int64)
    y = observed[idx]
    pred = predicted[idx]
    mean_y = float(np.mean(y))
    var_y = float(np.var(y, ddof=1)) if len(y) > 1 else float("nan")
    k_bin = (
        float((var_y - mean_y) / (mean_y**2)) if mean_y > 0 and np.isfinite(var_y) else float("nan")
    )
    return {
        "bin_index": int(bin_index),
        "source_initial_bins": [int(value) for value in source_bins],
        "predicted_xgb_lower": float(np.min(pred)),
        "predicted_xgb_upper": float(np.max(pred)),
        "n_link_years": int(len(y)),
        "n_positive": int(np.sum(y > 0)),
        "mean_y": mean_y,
        "var_y": var_y,
        "k_bin": k_bin,
    }


def _make_retained_bins(
    predicted: np.ndarray,
    observed: np.ndarray,
    bin_ids: np.ndarray,
    n_initial_bins: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_bins: list[int] = []
    member_indices: list[int] = []
    merge_actions: list[dict[str, Any]] = []
    retained: list[dict[str, Any]] = []

    for initial_bin in range(n_initial_bins):
        idx = np.flatnonzero(bin_ids == initial_bin)
        source_bins.append(initial_bin)
        member_indices.extend(idx.tolist())
        n_positive = int(np.sum(observed[idx] > 0))
        merge_actions.append(
            {
                "initial_bin": int(initial_bin),
                "n_link_years": int(len(idx)),
                "n_positive": n_positive,
                "action": "accumulated",
            }
        )

        if (
            len(member_indices) >= MIN_LINK_YEARS_PER_BIN
            and int(np.sum(observed[np.asarray(member_indices, dtype=np.int64)] > 0))
            >= MIN_POSITIVE_ROWS_PER_BIN
        ):
            retained.append(
                _summarize_bin(
                    predicted,
                    observed,
                    member_indices,
                    len(retained),
                    source_bins,
                )
            )
            if len(source_bins) > 1:
                merge_actions[-1]["action"] = "closed_merged_retained_bin"
                merge_actions[-1]["retained_bin_index"] = int(len(retained) - 1)
                merge_actions[-1]["source_initial_bins"] = [int(v) for v in source_bins]
            else:
                merge_actions[-1]["action"] = "closed_retained_bin"
                merge_actions[-1]["retained_bin_index"] = int(len(retained) - 1)
            source_bins = []
            member_indices = []

    if member_indices:
        if retained:
            logger.info(
                "Merging trailing low-count bin(s) %s into previous retained bin",
                source_bins,
            )
            previous = retained.pop()
            combined_sources = previous["source_initial_bins"] + source_bins
            combined_members: list[int] = []
            for source in combined_sources:
                combined_members.extend(np.flatnonzero(bin_ids == source).tolist())
            retained.append(
                _summarize_bin(
                    predicted,
                    observed,
                    combined_members,
                    len(retained),
                    combined_sources,
                )
            )
            merge_actions.append(
                {
                    "action": "merged_trailing_bins_into_previous",
                    "source_initial_bins": [int(v) for v in source_bins],
                    "retained_bin_index": int(len(retained) - 1),
                }
            )
        else:
            retained.append(
                _summarize_bin(
                    predicted,
                    observed,
                    member_indices,
                    0,
                    source_bins,
                )
            )
            merge_actions.append(
                {
                    "action": "single_retained_bin_from_all_initial_bins",
                    "source_initial_bins": [int(v) for v in source_bins],
                    "retained_bin_index": 0,
                }
            )

    return retained, merge_actions


def _aggregate_k(retained_bins: list[dict[str, Any]]) -> dict[str, Any]:
    n_bins_after_merge = len(retained_bins)
    kept = [
        row
        for row in retained_bins
        if np.isfinite(row["k_bin"]) and row["var_y"] > row["mean_y"] and row["k_bin"] >= 0
    ]
    dropped = [
        row
        for row in retained_bins
        if not (np.isfinite(row["k_bin"]) and row["var_y"] > row["mean_y"] and row["k_bin"] >= 0)
    ]
    dropped_fraction = len(dropped) / n_bins_after_merge if n_bins_after_merge else 0.0
    if dropped_fraction > NEGATIVE_BIN_FAIL_FRACTION:
        raise RuntimeError(
            "Method-of-moments dispersion failed: "
            f"{len(dropped)} / {n_bins_after_merge} bins "
            f"({dropped_fraction:.1%}) had Var(y) <= E(y), exceeding the "
            f"{NEGATIVE_BIN_FAIL_FRACTION:.0%} threshold."
        )
    if not kept:
        raise RuntimeError("No retained bins had positive NB2 dispersion")

    n_link_years = np.asarray([row["n_link_years"] for row in kept], dtype=np.float64)
    n_positive = np.asarray([row["n_positive"] for row in kept], dtype=np.float64)
    k_values = np.asarray([row["k_bin"] for row in kept], dtype=np.float64)

    k = float(np.sum(n_link_years * k_values) / np.sum(n_link_years))
    k_alt_positive = (
        float(np.sum(n_positive * k_values) / np.sum(n_positive))
        if np.sum(n_positive) > 0
        else float("nan")
    )
    k_alt_median = float(np.median(k_values))

    return {
        "k": k,
        "k_alt_positive_weighted": k_alt_positive,
        "k_alt_median": k_alt_median,
        "kept_bins": kept,
        "dropped_bins": dropped,
        "dropped_negative_k_bin_count": int(len(dropped)),
        "dropped_negative_k_bin_fraction": float(dropped_fraction),
    }


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


def _write_report(
    aggregation: dict[str, Any],
    n_bins_initial: int,
    n_bins_after_merge: int,
    merge_actions: list[dict[str, Any]],
) -> None:
    kept_bins = aggregation["kept_bins"]
    dropped_count = aggregation["dropped_negative_k_bin_count"]
    dropped_fraction = aggregation["dropped_negative_k_bin_fraction"]

    bin_rows = [
        [
            row["bin_index"],
            f"{_format_float(row['predicted_xgb_lower'])}-"
            f"{_format_float(row['predicted_xgb_upper'])}",
            f"{row['n_link_years']:,}",
            f"{row['n_positive']:,}",
            _format_float(row["mean_y"]),
            _format_float(row["var_y"]),
            _format_float(row["k_bin"]),
        ]
        for row in kept_bins
    ]
    k_rows = [
        ["link-year weighted (primary)", _format_float(aggregation["k"])],
        [
            "positive-event weighted (diagnostic)",
            _format_float(aggregation["k_alt_positive_weighted"]),
        ],
        ["median of retained k_bin (diagnostic)", _format_float(aggregation["k_alt_median"])],
    ]

    k_values = np.asarray([row["k_bin"] for row in kept_bins], dtype=np.float64)
    if len(k_values) > 1:
        spread = float(np.max(k_values) / np.min(k_values)) if np.min(k_values) > 0 else np.inf
        spread_sentence = (
            "The retained k_bin values vary by "
            f"about {spread:.1f}x across the predicted-risk range."
        )
    else:
        spread_sentence = "Only one retained k_bin value is available after merging."
    divergence = max(
        abs(aggregation["k_alt_positive_weighted"] - aggregation["k"]),
        abs(aggregation["k_alt_median"] - aggregation["k"]),
    )
    divergence_sentence = (
        "The diagnostic aggregations are close to the primary k."
        if divergence <= max(abs(aggregation["k"]) * 0.25, 1e-12)
        else "The diagnostic aggregations diverge materially from the primary k."
    )
    dropped_sentence = (
        "No bins were dropped for non-physical negative dispersion."
        if dropped_count == 0
        else f"{dropped_count} bins were dropped for non-physical negative dispersion."
    )

    merge_summary = (
        "No adjacent-bin merges were needed beyond the 20 initial quantile bins."
        if n_bins_after_merge == n_bins_initial
        else (
            f"Initial {n_bins_initial} quantile bins were merged into "
            f"{n_bins_after_merge} retained bins before negative-k filtering."
        )
    )

    report = "\n\n".join(
        [
            "# EB Dispersion Method-of-Moments Estimate",
            (
                "This report estimates a global NB2 dispersion parameter k for "
                "EB-style shrinkage using method-of-moments. Link-years are binned "
                "by existing Stage 2 XGBoost predicted collision count, and each "
                "bin's observed mean and variance imply k_bin = (Var(y) - E(y)) / "
                "E(y)^2."
            ),
            "## k_bin Values\n\n"
            + _markdown_table(
                [
                    "bin",
                    "predicted_xgb_range",
                    "n_link_years",
                    "n_positive",
                    "E(y)",
                    "Var(y)",
                    "k_bin",
                ],
                bin_rows,
            ),
            "## k Aggregations\n\n" + _markdown_table(["aggregation", "k"], k_rows),
            (
                "Divergence between the primary link-year weighted k and the "
                "diagnostic alternatives indicates non-constant dispersion and a "
                "potentially fragile global-k assumption."
            ),
            (
                "## Dropped Bins\n\n"
                f"Dropped bins: {dropped_count} of {n_bins_after_merge} after merging "
                f"({_format_float(dropped_fraction * 100)}%)."
            ),
            "## Bin Merges\n\n" + merge_summary,
            (
                "Merge rule: start with 20 quantile bins by predicted_xgb, walk bins "
                "from low to high prediction, and accumulate adjacent bins until the "
                f"candidate bin has at least {MIN_LINK_YEARS_PER_BIN:,} link-years "
                f"and {MIN_POSITIVE_ROWS_PER_BIN:,} positive-collision link-years; "
                "any trailing low-count bin is merged into the previous retained bin."
            ),
            (
                "## Interpretation\n\n"
                f"{dropped_sentence} {spread_sentence} {divergence_sentence} "
                "These diagnostics describe the MoM estimate only; they do not decide "
                "whether EB shrinkage should be adopted."
            ),
            (
                "Full provenance, bin definitions, and merge actions are in "
                "`data/provenance/eb_dispersion_provenance.json`."
            ),
        ]
    )
    REPORT_PATH.write_text(report + "\n")


def estimate_dispersion_mom() -> dict[str, Any]:
    PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df, fingerprints = _load_stage2_dataset()
    feature_cols = _load_xgb_features()
    predicted = _score_link_year_predictions(df, feature_cols)
    observed = df["collision_count"].to_numpy(dtype=np.float64, copy=False)

    logger.info("Forming %s quantile bins by predicted_xgb ...", N_QUANTILE_BINS)
    bin_ids, initial_definitions = _initial_bin_ids(predicted, N_QUANTILE_BINS)
    retained_bins, merge_actions = _make_retained_bins(
        predicted,
        observed,
        bin_ids,
        len(initial_definitions),
    )
    aggregation = _aggregate_k(retained_bins)

    kept_bins = aggregation["kept_bins"]
    provenance = {
        "method": "method_of_moments",
        "script_path": str(SCRIPT_PATH),
        "k": aggregation["k"],
        "k_alt_positive_weighted": aggregation["k_alt_positive_weighted"],
        "k_alt_median": aggregation["k_alt_median"],
        "k_bin": kept_bins,
        "dropped_negative_k_bins": aggregation["dropped_bins"],
        "bin_merge_rule_applied": (
            "Started with quantile bins by predicted_xgb; walked adjacent bins "
            "from low to high prediction, accumulating until each retained bin "
            f"had at least {MIN_LINK_YEARS_PER_BIN} link-years and "
            f"{MIN_POSITIVE_ROWS_PER_BIN} positive-collision link-years; "
            "merged any trailing low-count bin into the previous retained bin."
        ),
        "bin_merge_actions": merge_actions,
        "initial_bin_definitions": initial_definitions,
        "n_bins_initial": len(initial_definitions),
        "n_bins_after_merge": len(retained_bins),
        "n_bins_after_negative_drop": len(kept_bins),
        "dropped_negative_k_bin_count": aggregation["dropped_negative_k_bin_count"],
        "dropped_negative_k_bin_fraction": aggregation["dropped_negative_k_bin_fraction"],
        "negative_k_bin_fail_threshold": NEGATIVE_BIN_FAIL_FRACTION,
        "n_link_years_total": int(len(df)),
        "n_positive_total": int(np.sum(observed > 0)),
        "data_fingerprint": fingerprints,
        "git_sha": _git_sha(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
    }

    PROVENANCE_PATH.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    _write_report(
        aggregation,
        len(initial_definitions),
        len(retained_bins),
        merge_actions,
    )
    logger.info("Wrote %s", PROVENANCE_PATH)
    logger.info("Wrote %s", REPORT_PATH)
    return provenance


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    provenance = estimate_dispersion_mom()
    print(f"k={provenance['k']:.10g}")
    print(f"k_alt_positive_weighted={provenance['k_alt_positive_weighted']:.10g}")
    print(f"k_alt_median={provenance['k_alt_median']:.10g}")
    print(f"dropped_negative_k_bins={provenance['dropped_negative_k_bin_count']}")


if __name__ == "__main__":
    main()
