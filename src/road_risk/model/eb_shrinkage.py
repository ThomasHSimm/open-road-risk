"""
EB-style shrinkage utilities for Stage 2 risk scores.

This module applies a previously estimated NB2 dispersion parameter to pooled
Stage 2 scores. It does not train or modify GLM/XGBoost artefacts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from road_risk.config import _ROOT

EB_PROVENANCE_PATH = _ROOT / "data/provenance/eb_dispersion_provenance.json"


def load_eb_k_values(path: Path = EB_PROVENANCE_PATH) -> dict[str, float]:
    """Load the three session-1 k aggregations from provenance JSON."""
    with open(path) as f:
        provenance = json.load(f)

    required = ["k", "k_alt_positive_weighted", "k_alt_median"]
    missing = [key for key in required if key not in provenance]
    if missing:
        raise KeyError(f"Missing k value(s) in {path}: {missing}")

    return {
        "link_year_weighted": float(provenance["k"]),
        "positive_weighted": float(provenance["k_alt_positive_weighted"]),
        "median": float(provenance["k_alt_median"]),
    }


def compute_eb_scores(
    pooled: pd.DataFrame,
    n_years_by_link: pd.DataFrame,
    k: float,
) -> pd.DataFrame:
    """
    Add EB-adjusted scores to pooled one-row-per-link risk scores.

    Missing or zero n_years means the pooled dataframe contains a link with no
    underlying link-year rows, which points to an upstream pooling/scoring bug.
    """
    if k <= 0:
        raise ValueError(f"EB dispersion k must be positive; got {k}")
    for col in ["link_id", "predicted_xgb", "collision_count"]:
        if col not in pooled.columns:
            raise KeyError(f"Required pooled column missing: {col}")
    if "n_years" not in n_years_by_link.columns:
        raise KeyError("n_years_by_link must contain an n_years column")
    if pooled["predicted_xgb"].isna().any():
        raise ValueError("predicted_xgb contains missing values")
    if (pooled["predicted_xgb"] < 0).any():
        raise ValueError("predicted_xgb contains negative predictions")
    if pooled["collision_count"].isna().any():
        raise ValueError("collision_count contains missing values")

    result = pooled.merge(n_years_by_link, on="link_id", how="left", validate="one_to_one")
    if result["n_years"].isna().any():
        missing = int(result["n_years"].isna().sum())
        raise ValueError(
            f"{missing:,} pooled links have no n_years. This indicates unexpected "
            "pooled dataframe contents: links should not appear in pooled scores "
            "without link-year rows."
        )
    if (result["n_years"] <= 0).any():
        bad = int((result["n_years"] <= 0).sum())
        raise ValueError(
            f"{bad:,} pooled links have n_years <= 0. This indicates unexpected "
            "pooled dataframe contents, not a normal EB input edge case."
        )

    n_pred = result["predicted_xgb"] * result["n_years"]
    result["eb_weight"] = 1 / (1 + k * n_pred)
    n_eb = result["eb_weight"] * n_pred + (1 - result["eb_weight"]) * result["collision_count"]
    result["predicted_eb"] = n_eb / result["n_years"]
    result["risk_percentile_eb"] = result["predicted_eb"].rank(method="average", pct=True) * 100
    return result


def provenance_fingerprint(path: Path = EB_PROVENANCE_PATH) -> dict[str, Any]:
    """Small helper for downstream reports."""
    stat = path.stat()
    return {
        "path": str(path.relative_to(_ROOT)),
        "mtime_ns": stat.st_mtime_ns,
        "size_bytes": stat.st_size,
    }
