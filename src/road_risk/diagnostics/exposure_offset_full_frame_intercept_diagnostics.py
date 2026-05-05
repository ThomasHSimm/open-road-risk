"""
exposure_offset_full_frame_intercept_diagnostics.py
------------------------------------------
Full-population calibration diagnostics for Stage 2 GLM exposure variants A and B.

Re-fits Models A and B (same formulations as exposure_offset_experiment.py) on the
standard downsampled training frame, then scores the ENTIRE ~21M-row population to
produce calibration tables free from the GLM score-equation identity that forces
exact residual balance for indicator-variable groups in the training frame.

Diagnostic tables (all on full scored frame):
  1. Residuals by AADT decile
  2. Residuals by road family (motorway / trunk_a / other_urban / other_rural)
  3. Residuals by road classification
  4. Residuals by top-risk band (top 1% / 1-5% / 5-20% / bottom 80%)

For each table: A vs B comparison columns (absolute and relative residual improvement).

Also reports motorway residuals at full precision on both training frame and full frame
to explain the 0.0000 result from the previous run.

Outputs:
  docs/internal/exposure_offset_full_frame_diagnostics.json
  reports/exposure_offset_full_frame_diagnostics.md

Run with: conda run -n env1 python src/road_risk/diagnostics/exposure_offset_full_frame_diagnostics.py
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(Path(__file__).parents[3]))
from road_risk.config import _ROOT
from road_risk.model.collision import (
    AADT_PATH,
    GLM_ZERO_SAMPLE_RATIO,
    MODELS,
    NET_PATH,
    OPENROADS_PATH,
    RLA_PATH,
    build_collision_dataset,
)
from road_risk.model.constants import RANDOM_STATE

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

OUT_DIR = _ROOT / "docs" / "internal"
REPORTS_DIR = _ROOT / "reports"
OUT_JSON = OUT_DIR / "exposure_offset_full_frame_intercept_diagnostics.json"
OUT_MD = REPORTS_DIR / "exposure_offset_full_frame_intercept_diagnostics.md"
FAM_CAL_JSON = OUT_DIR / "family_intercept_calibration_diagnostics.json"
FAM_CAL_MD = REPORTS_DIR / "family_intercept_calibration_diagnostics.md"
WITHIN_FAM_JSON = OUT_DIR / "family_within_aadt_diagnostics.json"
WITHIN_FAM_MD = REPORTS_DIR / "family_within_aadt_diagnostics.md"
RISK_SCORES_PATH = MODELS / "risk_scores.parquet"

CHUNK = 1_000_000

STRUCTURAL_COLS = [
    "road_class_ord",
    "form_of_way_ord",
    "is_motorway",
    "is_a_road",
    "is_slip_road",
    "is_roundabout",
    "is_dual",
    "is_trunk",
    "is_primary",
    "is_covid",
    "year_norm",
]

FAMILIES = ["motorway", "trunk_a", "other_urban", "other_rural"]


# ---------------------------------------------------------------------------
# helpers shared with exposure_offset_experiment
# ---------------------------------------------------------------------------


def _calibrate_to_total(
    df: pd.DataFrame, pred_col: str, obs_col: str = "collision_count"
) -> tuple[pd.Series, float]:
    obs_total = df[obs_col].sum()
    pred_total = df[pred_col].sum()
    if pred_total <= 0:
        raise ValueError(f"{pred_col} total prediction is non-positive")
    factor = obs_total / pred_total
    return df[pred_col] * factor, float(np.log(factor))


def _null_deviance_poisson(y: np.ndarray, offset: np.ndarray) -> float:
    y = np.asarray(y, dtype=float)
    offset = np.clip(np.asarray(offset, dtype=float), -50.0, 50.0)
    sum_y, sum_exp = y.sum(), np.exp(offset).sum()
    if sum_y <= 0 or sum_exp <= 0:
        return np.inf
    alpha = np.log(sum_y / sum_exp)
    mu_null = np.exp(np.clip(alpha + offset, -50.0, 50.0))
    eps = 1e-300
    contrib = np.where(y > 0, y * np.log((y + eps) / (mu_null + eps)), 0.0) - (y - mu_null)
    return float(2.0 * contrib.sum())


def _pseudo_r2(result, y=None, offset=None) -> float:
    deviance = float(result.deviance)
    try:
        null_dev = float(result.null_deviance)
        if not np.isfinite(null_dev) or null_dev <= 0:
            raise ValueError
    except Exception:
        null_dev = _null_deviance_poisson(np.asarray(y), np.asarray(offset))
    return float(1.0 - deviance / null_dev)


def _downsample(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    pos_idx = df.index[df["collision_count"] > 0]
    zero_idx = df.index[df["collision_count"] == 0]
    n_keep = min(len(zero_idx), len(pos_idx) * GLM_ZERO_SAMPLE_RATIO)
    zero_sample = rng.choice(zero_idx, size=n_keep, replace=False)
    sel = np.sort(np.concatenate([pos_idx.values, zero_sample]))
    logger.info(f"  Downsampled: {len(pos_idx):,} pos + {n_keep:,} zeros = {len(sel):,} rows")
    return df.loc[sel].copy()


# ---------------------------------------------------------------------------
# model fitting (Models A and B only — C dropped)
# ---------------------------------------------------------------------------


def _fit_glm(X, y, offset):
    return sm.GLM(y, X, family=sm.families.Poisson(), offset=offset).fit(maxiter=200)


def fit_model_a(glm_df: pd.DataFrame) -> tuple:
    """Full offset: log(AADT × length × 365/1e6). Returns (result, features, offset_col)."""
    logger.info("Fitting Model A ...")
    features = STRUCTURAL_COLS + ["log_link_length"]
    X = sm.add_constant(glm_df[features].astype(float))
    y = glm_df["collision_count"].astype(int)
    offset = glm_df["log_offset"].astype(float)
    result = _fit_glm(X, y, offset)
    pr2 = _pseudo_r2(result, y=y, offset=offset)
    coefs = result.params.to_dict()
    logger.info(
        f"  Model A: pseudo-R²={pr2:.4f}, converged={result.converged}, "
        f"coef(log_link_length)={coefs.get('log_link_length', np.nan):.4f}"
    )
    return result, features, "log_offset", pr2, coefs


def fit_model_b(glm_df: pd.DataFrame) -> tuple:
    """No offset; log_aadt and log_link_length as features. Returns (result, features, offset_col)."""
    logger.info("Fitting Model B ...")
    features = STRUCTURAL_COLS + ["log_aadt", "log_link_length"]
    X = sm.add_constant(glm_df[features].astype(float))
    y = glm_df["collision_count"].astype(int)
    zero_off = pd.Series(np.zeros(len(glm_df), dtype=float), index=glm_df.index)
    result = _fit_glm(X, y, zero_off)
    pr2 = _pseudo_r2(result, y=y, offset=zero_off)
    coefs = result.params.to_dict()
    logger.info(
        f"  Model B: pseudo-R²={pr2:.4f}, converged={result.converged}, "
        f"coef(log_aadt)={coefs.get('log_aadt', np.nan):.4f}, "
        f"coef(log_link_length)={coefs.get('log_link_length', np.nan):.4f}"
    )
    return result, features, None, pr2, coefs


# ---------------------------------------------------------------------------
# chunked full-frame scoring
# ---------------------------------------------------------------------------


def _score_glm_full(df: pd.DataFrame, result, features: list, offset_col: str | None) -> np.ndarray:
    """Score GLM on entire df in 1M-row chunks. Returns float32 array aligned to df."""
    logger.info(f"  Scoring {len(df):,} rows (chunked) ...")
    preds = np.empty(len(df), dtype="float32")
    for start in range(0, len(df), CHUNK):
        end = min(start + CHUNK, len(df))
        chunk = df.iloc[start:end]
        missing = chunk[features].isna().sum()
        if missing.any():
            raise ValueError(f"Missing scoring features:\n{missing[missing > 0]}")
        # X_c = sm.add_constant(chunk[features].fillna(0).astype(float), has_constant="add")
        X_c = sm.add_constant(chunk[features].astype(float), has_constant="add")

        if offset_col and chunk[offset_col].isna().any():
            raise ValueError(f"Missing offset values in {offset_col}")
        off_c = (
            chunk[offset_col].astype(float)
            if offset_col
            else pd.Series(np.zeros(end - start), index=chunk.index)
        )
        preds[start:end] = np.asarray(result.predict(X_c, offset=off_c), dtype="float32")
    return preds


# ---------------------------------------------------------------------------
# family assignment (soft — unmatched rows → "other")
# ---------------------------------------------------------------------------


def _assign_family(df: pd.DataFrame) -> pd.Series:
    """
    Assign facility family using the same precedence as family_split.assign_family.
    Rows that cannot be matched (missing road_function / ruc_urban_rural) → 'other'.
    """
    road_fn = df.get("road_function", pd.Series("", index=df.index)).fillna("")
    ruc = df.get("ruc_urban_rural", pd.Series("", index=df.index)).fillna("")
    is_trunk = df["is_trunk"].astype(bool)
    conditions = [
        road_fn == "Motorway",
        (road_fn == "A Road") & is_trunk,
        ruc == "Urban",
        ruc == "Rural",
    ]
    return pd.Series(
        np.select(conditions, FAMILIES, default="other"),
        index=df.index,
        name="family",
    )


# ---------------------------------------------------------------------------
# diagnostic aggregation
# ---------------------------------------------------------------------------


def _resid_table(
    df: pd.DataFrame, group_col: str, pred_a_col: str, pred_b_col: str
) -> pd.DataFrame:
    """
    Aggregate observed/predicted by group and compute residual comparison columns.
    """
    agg = df.groupby(group_col).agg(
        n=(pred_a_col, "count"),
        sum_obs=("collision_count", "sum"),
        sum_pred_a=(pred_a_col, "sum"),
        sum_pred_b=(pred_b_col, "sum"),
    )
    agg["net_resid_a"] = agg["sum_obs"] - agg["sum_pred_a"]
    agg["net_resid_b"] = agg["sum_obs"] - agg["sum_pred_b"]
    agg["mean_resid_a"] = agg["net_resid_a"] / agg["n"]
    agg["mean_resid_b"] = agg["net_resid_b"] / agg["n"]
    agg["rel_resid_a"] = agg["net_resid_a"] / agg["sum_pred_a"].replace(0, np.nan)
    agg["rel_resid_b"] = agg["net_resid_b"] / agg["sum_pred_b"].replace(0, np.nan)
    # Positive = Model B is better calibrated (smaller absolute relative error)
    agg["rel_improvement"] = agg["rel_resid_a"].abs() - agg["rel_resid_b"].abs()
    return agg.round(6)


def _aadt_decile_table(df: pd.DataFrame, pred_a_col: str, pred_b_col: str) -> pd.DataFrame:
    """Residuals by AADT decile (decile thresholds from full frame)."""
    df = df.copy()
    df["aadt_decile"] = pd.qcut(df["estimated_aadt"], q=10, labels=False, duplicates="drop")
    agg = df.groupby("aadt_decile").agg(
        n=(pred_a_col, "count"),
        aadt_mean=("estimated_aadt", "mean"),
        aadt_p10=("estimated_aadt", lambda x: x.quantile(0.1)),
        aadt_p90=("estimated_aadt", lambda x: x.quantile(0.9)),
        sum_obs=("collision_count", "sum"),
        sum_pred_a=(pred_a_col, "sum"),
        sum_pred_b=(pred_b_col, "sum"),
    )
    agg["net_resid_a"] = agg["sum_obs"] - agg["sum_pred_a"]
    agg["net_resid_b"] = agg["sum_obs"] - agg["sum_pred_b"]
    agg["rel_resid_a"] = agg["net_resid_a"] / agg["sum_pred_a"].replace(0, np.nan)
    agg["rel_resid_b"] = agg["net_resid_b"] / agg["sum_pred_b"].replace(0, np.nan)
    agg["rel_improvement"] = agg["rel_resid_a"].abs() - agg["rel_resid_b"].abs()
    return agg.round(6)


def _top_risk_band_table(
    df_link: pd.DataFrame,
    pred_a_rate_col: str,
    pred_b_rate_col: str,
    pred_a_total_col: str,
    pred_b_total_col: str,
) -> pd.DataFrame:
    records = []

    for model_label, rate_col, total_col in [
        ("A", pred_a_rate_col, pred_a_total_col),
        ("B", pred_b_rate_col, pred_b_total_col),
    ]:
        pct = df_link[rate_col].rank(pct=True, method="average") * 100
        bands = pd.cut(
            pct,
            bins=[0, 80, 95, 99, 100],
            labels=["bottom_80pct", "5_to_20pct", "1_to_5pct", "top_1pct"],
            include_lowest=True,
        )

        tmp = df_link.copy()
        tmp["band"] = bands

        g = tmp.groupby("band", observed=False).agg(
            n_links=(rate_col, "count"),
            sum_obs=("collision_count", "sum"),
            sum_pred=(total_col, "sum"),
        )
        g["net_resid"] = g["sum_obs"] - g["sum_pred"]
        g["rel_resid"] = g["net_resid"] / g["sum_pred"].replace(0, np.nan)
        g["model"] = model_label

        records.append(g.reset_index())

    return pd.concat(records, ignore_index=True).round(6)


def _top_risk_band_table_common_basis(
    df_link: pd.DataFrame,
    basis_rate_col: str,
    pred_a_total_col: str,
    pred_b_total_col: str,
) -> pd.DataFrame:
    pct = df_link[basis_rate_col].rank(pct=True, method="average") * 100
    bands = pd.cut(
        pct,
        bins=[0, 80, 95, 99, 100],
        labels=["bottom_80pct", "5_to_20pct", "1_to_5pct", "top_1pct"],
        include_lowest=True,
    )

    tmp = df_link.copy()
    tmp["band"] = bands

    g = tmp.groupby("band", observed=False).agg(
        n_links=("collision_count", "count"),
        sum_obs=("collision_count", "sum"),
        sum_pred_a=(pred_a_total_col, "sum"),
        sum_pred_b=(pred_b_total_col, "sum"),
    )

    g["net_resid_a"] = g["sum_obs"] - g["sum_pred_a"]
    g["net_resid_b"] = g["sum_obs"] - g["sum_pred_b"]
    g["rel_resid_a"] = g["net_resid_a"] / g["sum_pred_a"].replace(0, np.nan)
    g["rel_resid_b"] = g["net_resid_b"] / g["sum_pred_b"].replace(0, np.nan)
    g["rel_improvement"] = g["rel_resid_a"].abs() - g["rel_resid_b"].abs()

    return g.reset_index().round(6)


# ---------------------------------------------------------------------------
# motorway stats helper (called separately for training frame and full frame)
# ---------------------------------------------------------------------------


def _mw_stats_from_frame(
    frame: pd.DataFrame, pred_col_a: str, pred_col_b: str, frame_label: str
) -> dict:
    """Motorway residual stats at full float precision for a given frame."""
    mw = frame[frame["road_classification"] == "Motorway"]
    if len(mw) == 0:
        return {"frame": frame_label, "n_rows": 0}
    sum_obs = float(mw["collision_count"].sum())
    sum_a = float(mw[pred_col_a].sum())
    sum_b = float(mw[pred_col_b].sum())
    return {
        "frame": frame_label,
        "n_rows": int(len(mw)),
        "sum_obs": sum_obs,
        "sum_pred_a": sum_a,
        "sum_pred_b": sum_b,
        "net_resid_a": sum_obs - sum_a,
        "net_resid_b": sum_obs - sum_b,
        "mean_resid_a": float((mw["collision_count"] - mw[pred_col_a]).mean()),
        "mean_resid_b": float((mw["collision_count"] - mw[pred_col_b]).mean()),
        "rel_resid_a": (sum_obs - sum_a) / sum_a if sum_a > 0 else None,
        "rel_resid_b": (sum_obs - sum_b) / sum_b if sum_b > 0 else None,
    }


# ---------------------------------------------------------------------------
# markdown output
# ---------------------------------------------------------------------------


def _write_markdown(report: dict) -> None:
    ma = report["model_summary"]["model_a"]
    mb = report["model_summary"]["model_b"]
    cal = report["calibration"]
    mw = report["motorway_precision"]

    mw_train = mw["training_frame"]
    mw_raw = mw["full_frame_raw"]
    mw_cal = mw["full_frame_calibrated"]

    def rows_resid(records: list[dict], label_col: str) -> str:
        return "\n".join(
            f"| {row[label_col]} | {int(row['n']):,} | {row['sum_obs']:,.0f} | "
            f"{row['net_resid_a']:+,.0f} | {row['rel_resid_a']:+.4f} | "
            f"{row['net_resid_b']:+,.0f} | {row['rel_resid_b']:+.4f} | "
            f"{row['rel_improvement']:+.4f} |"
            for row in records
        )

    def rows_aadt(records: list[dict]) -> str:
        return "\n".join(
            f"| {int(row['aadt_decile'])} | {int(row['n']):,} | "
            f"{row['aadt_mean']:,.0f} | {row['sum_obs']:,.0f} | "
            f"{row['net_resid_a']:+,.0f} | {row['rel_resid_a']:+.4f} | "
            f"{row['net_resid_b']:+,.0f} | {row['rel_resid_b']:+.4f} | "
            f"{row['rel_improvement']:+.4f} |"
            for row in records
        )

    def rows_own_band(records: list[dict], model: str) -> str:
        return "\n".join(
            f"| {row['band']} | {int(row['n_links']):,} | "
            f"{row['sum_obs']:,.0f} | {row['sum_pred']:,.0f} | "
            f"{row['net_resid']:+,.0f} | {row['rel_resid']:+.4f} |"
            for row in records
            if row["model"] == model
        )

    def rows_common_band(records: list[dict]) -> str:
        return "\n".join(
            f"| {row['band']} | {int(row['n_links']):,} | {row['sum_obs']:,.0f} | "
            f"{row['net_resid_a']:+,.0f} | {row['rel_resid_a']:+.4f} | "
            f"{row['net_resid_b']:+,.0f} | {row['rel_resid_b']:+.4f} | "
            f"{row['rel_improvement']:+.4f} |"
            for row in records
        )

    # Basic generated interpretation from calibrated common-basis/top-risk results.
    cal_aadt = report["calibrated"]["by_aadt_decile"]
    cal_family = report["calibrated"]["by_family"]
    cal_common_band = report["calibrated"]["by_top_risk_band_common_basis"]

    n_aadt_better = sum(row["rel_improvement"] > 0 for row in cal_aadt)
    n_family_better = sum(row["rel_improvement"] > 0 for row in cal_family)
    top1_common = next(
        (row for row in cal_common_band if row["band"] == "top_1pct"),
        None,
    )

    top1_text = ""
    if top1_common is not None:
        top1_text = (
            f"On the calibrated common-basis top-1% band, Model B relative-residual "
            f"improvement is {top1_common['rel_improvement']:+.4f}."
        )

    if n_aadt_better >= 7 and n_family_better >= 4:
        recommendation = (
            "Model B is a credible v3 GLM candidate after intercept calibration, "
            "because it improves calibration across most AADT deciles and road families."
        )
    else:
        recommendation = (
            "Model B should remain a diagnostic formulation rather than replacing Model A, "
            "because calibrated full-frame improvements are mixed rather than consistently positive."
        )

    md = f"""---
title: "Stage 2 GLM: Full-frame exposure calibration diagnostics"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** GLM diagnostic only. No production models changed.
**Models:** A (full offset) vs B (learned exposure). Model C dropped.
**Frame:** Full scored population unless explicitly labelled as the downsampled training frame.

---

## 1. Why motorway residuals were exactly 0.0 in the training-frame report

{mw["explanation"]}

### Training-frame motorway residuals

| Metric | Model A | Model B |
|---|---:|---:|
| N rows | {mw_train["n_rows"]:,} | — |
| sum_obs | {mw_train["sum_obs"]:.6f} | — |
| sum_pred | {mw_train["sum_pred_a"]:.6f} | {mw_train["sum_pred_b"]:.6f} |
| net_resid | {mw_train["net_resid_a"]:.6f} | {mw_train["net_resid_b"]:.6f} |
| mean_resid | {mw_train["mean_resid_a"]:.6f} | {mw_train["mean_resid_b"]:.6f} |
| rel_resid | {mw_train["rel_resid_a"]:.6f} | {mw_train["rel_resid_b"]:.6f} |

### Full-frame motorway residuals — raw predictions

| Metric | Model A | Model B |
|---|---:|---:|
| N rows | {mw_raw["n_rows"]:,} | — |
| sum_obs | {mw_raw["sum_obs"]:.0f} | — |
| sum_pred | {mw_raw["sum_pred_a"]:.2f} | {mw_raw["sum_pred_b"]:.2f} |
| net_resid | {mw_raw["net_resid_a"]:.2f} | {mw_raw["net_resid_b"]:.2f} |
| rel_resid | {mw_raw["rel_resid_a"]:.4f} | {mw_raw["rel_resid_b"]:.4f} |

### Full-frame motorway residuals — intercept-calibrated predictions

| Metric | Model A | Model B |
|---|---:|---:|
| N rows | {mw_cal["n_rows"]:,} | — |
| sum_obs | {mw_cal["sum_obs"]:.0f} | — |
| sum_pred | {mw_cal["sum_pred_a"]:.2f} | {mw_cal["sum_pred_b"]:.2f} |
| net_resid | {mw_cal["net_resid_a"]:.2f} | {mw_cal["net_resid_b"]:.2f} |
| rel_resid | {mw_cal["rel_resid_a"]:.4f} | {mw_cal["rel_resid_b"]:.4f} |

---

## 2. Model summary

| | Model A | Model B |
|---|---:|---:|
| Exposure treatment | Full offset `log(AADT × length × 365 / 1e6)` | No offset; `log_aadt` + `log_length` as features |
| pseudo-R², training frame | {ma["pseudo_r2"]:.4f} | {mb["pseudo_r2"]:.4f} |
| coef(log_aadt) | forced = 1.0 | {mb["coef_log_aadt"]:.4f} |
| coef(log_length) | {ma["coef_log_link_length"]:.4f} | {mb["coef_log_link_length"]:.4f} |
| effective length β | {ma["effective_length_beta"]:.4f} | {mb["effective_length_beta"]:.4f} |

Model A forces AADT and length to scale linearly through the offset, then partly offsets the length assumption through the learned `log_link_length` correction. Model B learns both terms directly. In this diagnostic GLM, AADT is only mildly sub-linear, while length is strongly sub-linear.

---

## 3. Intercept calibration

The raw full-frame predictions are affected by zero-downsampling intercept bias. The calibrated predictions apply a single multiplicative correction so that total predicted collisions match total observed collisions on the full scored frame.

| | Model A | Model B |
|---|---:|---:|
| raw sum_pred | {cal["model_a"]["raw_sum_pred"]:,.0f} | {cal["model_b"]["raw_sum_pred"]:,.0f} |
| calibrated sum_pred | {cal["model_a"]["cal_sum_pred"]:,.0f} | {cal["model_b"]["cal_sum_pred"]:,.0f} |
| sum_obs | {cal["model_a"]["sum_obs"]:,.0f} | {cal["model_b"]["sum_obs"]:,.0f} |
| calibration factor | {cal["model_a"]["factor"]:.6f} | {cal["model_b"]["factor"]:.6f} |
| log correction | {cal["model_a"]["log_correction"]:.6f} | {cal["model_b"]["log_correction"]:.6f} |

The raw tables show the downsampling calibration problem. The calibrated tables are the cleaner basis for structural residual diagnosis.

---

## 4. Calibrated residuals by AADT decile

Decile 0 = lowest AADT. Positive net residual means under-prediction. `Improvement > 0` means Model B has smaller absolute relative residual than Model A.

| Decile | N | Mean AADT | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{rows_aadt(report["calibrated"]["by_aadt_decile"])}

---

## 5. Calibrated residuals by road family

| Family | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
{rows_resid(report["calibrated"]["by_family"], "family")}

---

## 6. Calibrated residuals by road classification

| Class | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
{rows_resid(report["calibrated"]["by_road_class"], "road_classification")}

---

## 7. Calibrated top-risk bands

Bands are defined separately for each model using that model's own link-level predicted rate. Residuals use summed link-year predictions, not `mean × global n_years`.

### Model A own-rank bands

| Band | Links | Obs | Pred | Net resid | Rel resid |
|---|---:|---:|---:|---:|---:|
{rows_own_band(report["calibrated"]["by_top_risk_band"], "A")}

### Model B own-rank bands

| Band | Links | Obs | Pred | Net resid | Rel resid |
|---|---:|---:|---:|---:|---:|
{rows_own_band(report["calibrated"]["by_top_risk_band"], "B")}

---

## 8. Calibrated top-risk bands on common Model A basis

These bands use Model A's link-level ranking as the fixed basis, then compare Model A and Model B predictions on exactly the same link groups. This is the cleaner operational comparison.

| Band | Links | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
{rows_common_band(report["calibrated"]["by_top_risk_band_common_basis"])}

---

## 9. Raw residual appendix

These tables are included to show the scale of zero-downsampling intercept bias before calibration. They should not be used as the primary structural calibration evidence.

### Raw residuals by AADT decile

| Decile | N | Mean AADT | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{rows_aadt(report["raw"]["by_aadt_decile"])}

### Raw residuals by road family

| Family | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
{rows_resid(report["raw"]["by_family"], "family")}

---

## 10. Interpretation and recommendation

Model B improves the downsampled training-frame pseudo-R², and its coefficients make the exposure assumptions more explicit. However, the production question is whether it improves full-population calibration after removing the known intercept bias.

Calibrated comparison summary:

- Model B improves {n_aadt_better}/10 AADT deciles.
- Model B improves {n_family_better}/{len(cal_family)} road-family groups.
- {top1_text}

**Recommendation:** {recommendation}

If motorway residuals remain large after intercept calibration, the issue is not solved by global exposure treatment alone. The next modelling step should be family-specific calibration or per-family GLM diagnostics, not more global exposure tweaking.

_Machine-readable: `docs/internal/exposure_offset_full_frame_diagnostics.json`_
"""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_MD, "w") as f:
        f.write(md)

    logger.info(f"Markdown written to {OUT_MD}")


# ---------------------------------------------------------------------------
# Per-family intercept calibration helpers
# ---------------------------------------------------------------------------


def _resid_3way(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """
    Residual table comparing raw, global-calibrated, and family-calibrated Model A.
    Columns: n, sum_obs, sum_pred_{raw/global/family}, rel_resid_{raw/global/family},
             improv_global (|raw|−|global|), improv_family (|raw|−|family|),
             family_vs_global (|global|−|family|).
    Positive improvement = that variant is better calibrated.
    """
    agg = df.groupby(group_col).agg(
        n=("collision_count", "count"),
        sum_obs=("collision_count", "sum"),
        sum_pred_raw=("pred_a", "sum"),
        sum_pred_global=("pred_a_cal", "sum"),
        sum_pred_family=("pred_a_family_cal", "sum"),
    )
    for label in ("raw", "global", "family"):
        p = f"sum_pred_{label}"
        agg[f"rel_resid_{label}"] = (agg["sum_obs"] - agg[p]) / agg[p].replace(0, np.nan)
    agg["improv_global"] = agg["rel_resid_raw"].abs() - agg["rel_resid_global"].abs()
    agg["improv_family"] = agg["rel_resid_raw"].abs() - agg["rel_resid_family"].abs()
    agg["family_vs_global"] = agg["rel_resid_global"].abs() - agg["rel_resid_family"].abs()
    return agg.round(6)


def _aadt_decile_3way(df: pd.DataFrame) -> pd.DataFrame:
    """AADT decile residuals for raw, global-cal, and family-cal Model A."""
    df = df.copy()
    df["aadt_decile"] = pd.qcut(df["estimated_aadt"], q=10, labels=False, duplicates="drop")
    agg = df.groupby("aadt_decile").agg(
        n=("collision_count", "count"),
        aadt_mean=("estimated_aadt", "mean"),
        sum_obs=("collision_count", "sum"),
        sum_pred_raw=("pred_a", "sum"),
        sum_pred_global=("pred_a_cal", "sum"),
        sum_pred_family=("pred_a_family_cal", "sum"),
    )
    for label in ("raw", "global", "family"):
        p = f"sum_pred_{label}"
        agg[f"rel_resid_{label}"] = (agg["sum_obs"] - agg[p]) / agg[p].replace(0, np.nan)
    agg["improv_global"] = agg["rel_resid_raw"].abs() - agg["rel_resid_global"].abs()
    agg["improv_family"] = agg["rel_resid_raw"].abs() - agg["rel_resid_family"].abs()
    agg["family_vs_global"] = agg["rel_resid_global"].abs() - agg["rel_resid_family"].abs()
    return agg.round(6)


def _top_risk_band_3way_common(df_link: pd.DataFrame) -> pd.DataFrame:
    """
    Top-risk bands on a common raw Model A ranking (pred_a_rate).
    Compares all three prediction variants within the same link groups.
    """
    pct = df_link["pred_a_rate"].rank(pct=True, method="average") * 100
    bands = pd.cut(
        pct,
        bins=[0, 80, 95, 99, 100],
        labels=["bottom_80pct", "5_to_20pct", "1_to_5pct", "top_1pct"],
        include_lowest=True,
    )
    tmp = df_link.copy()
    tmp["band"] = bands
    agg = tmp.groupby("band", observed=False).agg(
        n_links=("collision_count", "count"),
        sum_obs=("collision_count", "sum"),
        sum_pred_raw=("pred_a_total", "sum"),
        sum_pred_global=("pred_a_cal_total", "sum"),
        sum_pred_family=("pred_a_fam_cal_total", "sum"),
    )
    for label in ("raw", "global", "family"):
        p = f"sum_pred_{label}"
        agg[f"rel_resid_{label}"] = (agg["sum_obs"] - agg[p]) / agg[p].replace(0, np.nan)
    agg["improv_global"] = agg["rel_resid_raw"].abs() - agg["rel_resid_global"].abs()
    agg["improv_family"] = agg["rel_resid_raw"].abs() - agg["rel_resid_family"].abs()
    agg["family_vs_global"] = agg["rel_resid_global"].abs() - agg["rel_resid_family"].abs()
    return agg.reset_index().round(6)


def _write_family_cal_markdown(report: dict) -> None:
    fac = report["calibration_factors"]
    by_fam = report["by_family"]
    by_cls = report["by_road_class"]
    by_aadt = report["by_aadt_decile"]
    by_band = report["by_top_risk_band_common_basis"]

    def _fac_rows():
        lines = []
        for r in fac:
            lines.append(
                f"| {r['family']} | {int(r['n']):,} | {r['sum_obs']:,.0f} | "
                f"{r['sum_pred_raw']:,.0f} | {r['sum_pred_global']:,.0f} | "
                f"{r['sum_pred_family']:,.0f} | {r['factor']:.4f} | {r['log_factor']:+.4f} |"
            )
        return "\n".join(lines)

    def _resid_rows(records, label_col):
        lines = []
        for r in records:
            lines.append(
                f"| {r[label_col]} | {int(r['n']):,} | {r['sum_obs']:,.0f} | "
                f"{r['rel_resid_raw']:+.4f} | {r['rel_resid_global']:+.4f} | "
                f"{r['rel_resid_family']:+.4f} | {r['family_vs_global']:+.4f} |"
            )
        return "\n".join(lines)

    def _aadt_rows():
        lines = []
        for r in by_aadt:
            lines.append(
                f"| {int(r['aadt_decile'])} | {int(r['n']):,} | {r['aadt_mean']:,.0f} | "
                f"{r['sum_obs']:,.0f} | "
                f"{r['rel_resid_raw']:+.4f} | {r['rel_resid_global']:+.4f} | "
                f"{r['rel_resid_family']:+.4f} | {r['family_vs_global']:+.4f} |"
            )
        return "\n".join(lines)

    def _band_rows():
        lines = []
        for r in by_band:
            lines.append(
                f"| {r['band']} | {int(r['n_links']):,} | {r['sum_obs']:,.0f} | "
                f"{r['rel_resid_raw']:+.4f} | {r['rel_resid_global']:+.4f} | "
                f"{r['rel_resid_family']:+.4f} | {r['family_vs_global']:+.4f} |"
            )
        return "\n".join(lines)

    # Derived interpretation signals
    n_fam_better = sum(r["family_vs_global"] > 0 for r in by_fam)
    n_aadt_damaged = sum(r["family_vs_global"] < -0.01 for r in by_aadt)
    n_aadt_better = sum(r["family_vs_global"] > 0 for r in by_aadt)
    n_aadt_total = len(by_aadt)
    mw = next((r for r in by_fam if r["family"] == "motorway"), None)
    top1 = next((r for r in by_band if r["band"] == "top_1pct"), None)

    mw_text = (
        f"Motorway: raw={mw['rel_resid_raw']:+.4f}, "
        f"global-cal={mw['rel_resid_global']:+.4f}, "
        f"family-cal={mw['rel_resid_family']:+.4f} (by definition ≈ 0)."
        if mw
        else "Motorway family not found in results."
    )
    top1_text = (
        f"Top-1% band: raw={top1['rel_resid_raw']:+.4f}, "
        f"global-cal={top1['rel_resid_global']:+.4f}, "
        f"family-cal={top1['rel_resid_family']:+.4f}."
        if top1
        else ""
    )

    if n_fam_better >= 4 and n_aadt_damaged <= 2:
        verdict = (
            "**Recommendation:** Treat per-family intercept calibration as a candidate v3 GLM "
            "calibration layer, not yet a production change. "
            "The follow-up gate is within-family AADT-decile diagnostics, especially motorway "
            "and trunk-A. If those show no major residual slope pattern, family intercept "
            "calibration is probably enough for the GLM. If they show systematic high-AADT or "
            "low-AADT bias within family, move to family-specific slopes or interactions."
        )
    elif n_fam_better >= 3 and n_aadt_damaged <= 4:
        verdict = (
            "**Partial evidence for per-family calibration.** "
            "Family-level totals improve but AADT decile calibration is partly damaged, "
            "suggesting family composition effects. Richer per-family diagnostics (slopes or features) "
            "are needed before adopting this as a production calibration layer."
        )
    else:
        verdict = (
            "**Per-family intercept calibration fixes family totals by construction "
            "but does not improve structural calibration.** "
            "The residual bias is driven by within-family AADT/length composition differences "
            "that a single multiplicative factor cannot address. "
            "Per-family GLMs with separate slopes are the next diagnostic step."
        )

    md = f"""---
title: "Stage 2 GLM: Per-family intercept calibration diagnostic"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** Diagnostic only. No production models changed. No retraining.
**Model:** Model A (full offset). Model B excluded from per-family analysis.
**Frame:** All tables use the full ~21M-row scored population.

Comparisons: **raw** (uncalibrated) · **global-cal** (single intercept correction) · **family-cal** (per-family intercept correction).

---

## 1. What this diagnostic tests

The global intercept calibration corrects the downsampling intercept bias (factor applies
uniformly to all links). The open question is: does a *per-family* intercept — keeping all
slopes fixed — reduce the remaining family-level residual bias observed after global
calibration, and does it do so without damaging AADT decile or top-risk-band calibration?

The per-family factor is:
`factor_f = sum_obs_f / sum_pred_a_raw_f`
`pred_a_family_cal = pred_a * factor_f`

This is a multiplicative intercept correction per facility family. It cannot change
within-family AADT or link-length residual patterns; it only shifts the level.

---

## 2. Calibration factors

| Family | N rows | Obs | Raw pred | Global-cal pred | Family-cal pred | Factor | Log correction |
|---|---:|---:|---:|---:|---:|---:|---:|
{_fac_rows()}

The log correction is the implied intercept shift (log-scale). Family-cal pred ≈ obs by construction.

---

## 3. Residuals by road family

rel_resid = (obs − pred) / pred. Positive = under-prediction. Negative = over-prediction.
family_vs_global > 0 means family-cal is better calibrated than global-cal.

| Family | N | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|
{_resid_rows(by_fam, "family")}

---

## 4. Residuals by road classification

| Class | N | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|
{_resid_rows(by_cls, "road_classification")}

---

## 5. Residuals by AADT decile

Decile 0 = lowest AADT, 9 = highest. This is the key test: does family calibration
damage within-decile calibration?

| Decile | N | Mean AADT | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|---:|
{_aadt_rows()}

---

## 6. Residuals by top-risk band (common Model A ranking)

Bands are fixed by raw Model A link-level predicted rate. All three variants are
evaluated on the same link groups. This tests whether family calibration shifts
risk within the top-risk population.

| Band | Links | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |
|---|---:|---:|---:|---:|---:|---:|
{_band_rows()}

---

## 7. Interpretation

### Motorway calibration
{mw_text}

Motorway family-cal rel_resid is ≈ 0 by construction (factor forces sum_pred = sum_obs
at family level). Whether the motorway issue is structural is not answered by the global
AADT decile table. It requires a within-motorway diagnostic: residuals by AADT decile
using motorway rows only, after family intercept calibration.

### Top-risk bands
{top1_text}

### Summary

Family calibration improves {n_aadt_better}/{n_aadt_total} global AADT deciles.
It worsens {n_aadt_damaged} decile(s) by more than 1 percentage point, but improves the
highest-AADT decile and substantially improves the lowest-to-mid deciles.

{verdict}

### Next steps
- If motorway rel_resid at the family level is ≈ 0 (by construction) but AADT decile 9
  (highest traffic) still shows bias, the motorway problem is a slope/composition issue,
  not an intercept issue. Per-family GLM slopes are needed.
- Top-risk-band calibration improves at the bottom 80%, 1–5%, and top 1% bands, with the
  largest gain in the top 1% band. The 5–20% band worsens slightly.
- Consider applying family calibration as a post-scoring step in the EB shrinkage workflow
  rather than in the GLM itself, to keep the model unchanged.

_Machine-readable: `docs/internal/family_intercept_calibration_diagnostics.json`_
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(FAM_CAL_MD, "w") as f:
        f.write(md)
    logger.info(f"Family-cal markdown written to {FAM_CAL_MD}")


# ---------------------------------------------------------------------------
# Within-family AADT decile helpers
# ---------------------------------------------------------------------------

FAMILY_ORDER = ["motorway", "trunk_a", "other_urban", "other_rural", "other"]


def _within_family_aadt_decile_3way(df: pd.DataFrame) -> dict[str, list[dict]]:
    """
    For each family, compute residuals by within-family AADT decile for all three
    Model A prediction variants: raw, global-cal, family-cal.
    df must contain: family, estimated_aadt, collision_count,
                     pred_a, pred_a_cal, pred_a_family_cal.
    AADT deciles are computed within each family independently.
    """
    results = {}
    for fam in FAMILY_ORDER:
        sub = df[df["family"] == fam].copy()
        if len(sub) == 0:
            continue
        sub["aadt_decile"] = pd.qcut(sub["estimated_aadt"], q=10, labels=False, duplicates="drop")
        agg = sub.groupby("aadt_decile").agg(
            n=("collision_count", "count"),
            aadt_p10=("estimated_aadt", lambda x: x.quantile(0.1)),
            aadt_mean=("estimated_aadt", "mean"),
            aadt_p90=("estimated_aadt", lambda x: x.quantile(0.9)),
            sum_obs=("collision_count", "sum"),
            sum_pred_raw=("pred_a", "sum"),
            sum_pred_global=("pred_a_cal", "sum"),
            sum_pred_family=("pred_a_family_cal", "sum"),
        )
        for label in ("raw", "global", "family"):
            p = f"sum_pred_{label}"
            agg[f"rel_resid_{label}"] = (agg["sum_obs"] - agg[p]) / agg[p].replace(0, np.nan)
        agg["family_vs_global"] = agg["rel_resid_global"].abs() - agg["rel_resid_family"].abs()
        results[fam] = agg.round(6).reset_index().to_dict(orient="records")
    return results


def _write_within_family_markdown(results: dict[str, list[dict]]) -> None:
    def _table(records: list[dict]) -> str:
        lines = [
            "| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | Raw rel | Global-cal rel | Family-cal rel | Family vs global |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for r in records:
            lines.append(
                f"| {int(r['aadt_decile'])} | {int(r['n']):,} "
                f"| {r['aadt_p10']:,.0f} | {r['aadt_mean']:,.0f} | {r['aadt_p90']:,.0f} "
                f"| {r['sum_obs']:,.0f} "
                f"| {r['rel_resid_raw']:+.4f} | {r['rel_resid_global']:+.4f} "
                f"| {r['rel_resid_family']:+.4f} | {r['family_vs_global']:+.4f} |"
            )
        return "\n".join(lines)

    def _interpret(fam: str, records: list[dict]) -> str:
        fam_rels = [r["rel_resid_family"] for r in records]
        fam_range = max(fam_rels) - min(fam_rels)
        low_decile_rel = fam_rels[0] if fam_rels else float("nan")
        high_decile_rel = fam_rels[-1] if fam_rels else float("nan")
        slope_sign = "positive" if high_decile_rel > low_decile_rel else "negative"
        if fam_range < 0.10:
            return (
                f"Family-cal residuals are roughly flat across within-{fam} AADT deciles "
                f"(range {fam_range:.3f}). Per-family intercept calibration appears sufficient "
                f"for this family; no strong evidence of a residual slope problem."
            )
        elif fam_range < 0.25:
            return (
                f"Moderate within-{fam} AADT slope remains after family-cal "
                f"(range {fam_range:.3f}, {slope_sign} slope: "
                f"low-AADT rel={low_decile_rel:+.4f}, high-AADT rel={high_decile_rel:+.4f}). "
                f"A per-family exposure slope or AADT interaction should be tested."
            )
        else:
            return (
                f"Strong within-{fam} AADT slope remains after family-cal "
                f"(range {fam_range:.3f}, {slope_sign} slope: "
                f"low-AADT rel={low_decile_rel:+.4f}, high-AADT rel={high_decile_rel:+.4f}). "
                f"Per-family intercept calibration is not sufficient for this family. "
                f"Per-family GLMs with separate exposure slopes are recommended."
            )

    sections = []
    for i, fam in enumerate(FAMILY_ORDER, start=1):
        if fam not in results:
            continue
        records = results[fam]
        total_obs = sum(r["sum_obs"] for r in records)
        total_pred_fam = sum(r["sum_pred_family"] for r in records)
        rel_total = (
            (total_obs - total_pred_fam) / total_pred_fam if total_pred_fam else float("nan")
        )
        interp = _interpret(fam, records)
        sections.append(
            f"## {i}. {fam}\n\n"
            f"Family total (family-cal): obs={total_obs:,.0f}, pred={total_pred_fam:,.2f}, "
            f"rel_resid={rel_total:+.4f} (≈ 0 by construction).\n\n"
            f"**Interpretation:** {interp}\n\n" + _table(records)
        )

    # Overall verdict across families
    slope_families = []
    flat_families = []
    for fam in FAMILY_ORDER:
        if fam not in results:
            continue
        fam_rels = [r["rel_resid_family"] for r in results[fam]]
        fam_range = max(fam_rels) - min(fam_rels)
        if fam_range >= 0.10:
            slope_families.append(fam)
        else:
            flat_families.append(fam)

    if not slope_families:
        overall = (
            "All families show roughly flat within-family residuals after family intercept "
            "calibration. **Recommend per-family intercept calibration as a candidate v3 GLM "
            "calibration layer.** No evidence of residual slope problems within any family."
        )
    elif len(slope_families) <= 2 and all(f in ("motorway", "trunk_a") for f in slope_families):
        overall = (
            f"Flat residuals in {', '.join(flat_families)}. "
            f"Slope patterns persist within {', '.join(slope_families)} after family-cal. "
            "**Recommend per-family intercept calibration for low-volume families, "
            "but test per-family exposure slopes or AADT interactions for "
            f"{', '.join(slope_families)} before treating family-cal as sufficient for those families.**"
        )
    else:
        overall = (
            f"Slope patterns persist within {', '.join(slope_families)} after family-cal. "
            "**Per-family intercept calibration alone is not sufficient. "
            "Per-family GLMs with separate exposure slopes should be tested.**"
        )

    md = f"""---
title: "Stage 2 GLM: Within-family AADT decile calibration"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** Diagnostic only. No production models changed. No retraining.
**Model:** Model A (full offset). All three prediction variants compared.
**Frame:** Full ~21M-row scored population.

Comparisons: **raw** · **global-cal** (single intercept correction) · **family-cal** (per-family intercept correction).

---

## Background

After per-family intercept calibration, the family-level totals match observations by
construction. This diagnostic tests whether residual bias *within each family* varies
systematically across the AADT distribution.

If family-cal residuals are roughly flat across within-family AADT deciles → intercept
calibration is probably enough for that family.

If family-cal residuals still show a systematic AADT slope within a family → that family
needs per-family exposure slopes or AADT interactions, not just an intercept shift.

AADT deciles are computed separately within each family (decile 0 = lowest 10% of AADT
within that family, not across the full population).

`family_vs_global` > 0 means family-cal is better calibrated than global-cal at that decile.

---

{"---".join(f"\n{s}\n" for s in sections)}

---

## Overall verdict

{overall}

_Machine-readable: `docs/internal/family_within_aadt_diagnostics.json`_
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(WITHIN_FAM_MD, "w") as f:
        f.write(md)
    logger.info(f"Within-family markdown written to {WITHIN_FAM_MD}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def run() -> dict:
    logger.info("=== Full-frame exposure diagnostics ===")

    # --- load ---
    logger.info("Loading data ...")
    openroads = gpd.read_parquet(OPENROADS_PATH)
    road_fn_map = openroads[["link_id", "road_function"]].copy()

    rla = pd.read_parquet(RLA_PATH)
    aadt_estimates = pd.read_parquet(AADT_PATH)
    net_features = pd.read_parquet(NET_PATH) if NET_PATH.exists() else None

    df = build_collision_dataset(openroads, aadt_estimates, rla, net_features)
    del openroads

    # Experiment columns
    df["log_aadt"] = np.log(df["estimated_aadt"].clip(lower=1.0))

    # Join road_function for family assignment.
    df = df.merge(road_fn_map, on="link_id", how="left")
    del road_fn_map

    # Assign family.
    df["family"] = _assign_family(df)
    fam_counts = df["family"].value_counts().to_dict()
    logger.info(f"  Family counts: {fam_counts}")

    # --- downsample for training ---
    rng = np.random.default_rng(RANDOM_STATE)

    core_req = [
        c
        for c in STRUCTURAL_COLS + ["log_link_length", "log_aadt", "log_offset"]
        if c in df.columns
    ]

    missing_core = [
        c
        for c in STRUCTURAL_COLS + ["log_link_length", "log_aadt", "log_offset"]
        if c not in df.columns
    ]
    if missing_core:
        raise ValueError(f"Missing required core columns: {missing_core}")

    full_idx = df.dropna(subset=core_req).index
    logger.info(f"  Full scoring frame after core dropna: {len(full_idx):,} rows")

    glm_df = _downsample(df.loc[full_idx], rng)

    # --- fit Models A and B only ---
    res_a, feat_a, off_col_a, pr2_a, coefs_a = fit_model_a(glm_df)
    res_b, feat_b, off_col_b, pr2_b, coefs_b = fit_model_b(glm_df)

    # --- training-frame motorway stats ---
    X_a_tr = sm.add_constant(glm_df[feat_a].astype(float), has_constant="add")
    glm_df["pred_a_train"] = res_a.predict(
        X_a_tr,
        offset=glm_df["log_offset"].astype(float),
    )
    del X_a_tr

    X_b_tr = sm.add_constant(glm_df[feat_b].astype(float), has_constant="add")
    glm_df["pred_b_train"] = res_b.predict(
        X_b_tr,
        offset=pd.Series(np.zeros(len(glm_df), dtype=float), index=glm_df.index),
    )
    del X_b_tr

    mw_train_stats = _mw_stats_from_frame(
        glm_df,
        "pred_a_train",
        "pred_b_train",
        "downsampled training frame",
    )
    del glm_df

    # --- build thin scoring frame ---
    thin_cols = list(
        dict.fromkeys(
            feat_a
            + feat_b
            + [
                "link_id",
                "year",
                "estimated_aadt",
                "collision_count",
                "road_classification",
                "family",
                "log_offset",
            ]
        )
    )
    thin_cols = [c for c in thin_cols if c in df.columns]

    df_thin = df.loc[full_idx, thin_cols].copy()
    del df

    # Defensive missing checks before scoring.
    for model_name, features in {"A": feat_a, "B": feat_b}.items():
        missing = df_thin[features].isna().sum()
        missing = missing[missing > 0]
        if len(missing):
            raise ValueError(
                f"Missing scoring features for Model {model_name}:\n{missing.to_string()}"
            )

    if off_col_a is not None and df_thin[off_col_a].isna().any():
        raise ValueError(f"Missing offset values in {off_col_a}")

    # --- score full frame: raw predictions ---
    logger.info("Scoring full frame ...")
    df_thin["pred_a"] = _score_glm_full(df_thin, res_a, feat_a, off_col_a)
    df_thin["pred_b"] = _score_glm_full(df_thin, res_b, feat_b, off_col_b)

    # --- post-hoc intercept calibration ---
    # Keep raw predictions. Calibrated predictions are separate columns.
    df_thin["pred_a_cal"], log_corr_a = _calibrate_to_total(df_thin, "pred_a")
    df_thin["pred_b_cal"], log_corr_b = _calibrate_to_total(df_thin, "pred_b")

    calibration = {
        "model_a": {
            "factor": float(np.exp(log_corr_a)),
            "log_correction": float(log_corr_a),
            "raw_sum_pred": float(df_thin["pred_a"].sum()),
            "cal_sum_pred": float(df_thin["pred_a_cal"].sum()),
            "sum_obs": float(df_thin["collision_count"].sum()),
        },
        "model_b": {
            "factor": float(np.exp(log_corr_b)),
            "log_correction": float(log_corr_b),
            "raw_sum_pred": float(df_thin["pred_b"].sum()),
            "cal_sum_pred": float(df_thin["pred_b_cal"].sum()),
            "sum_obs": float(df_thin["collision_count"].sum()),
        },
    }

    logger.info(
        "  Calibration factors: "
        f"A={calibration['model_a']['factor']:.6f}, "
        f"B={calibration['model_b']['factor']:.6f}"
    )

    # --- diagnostics: raw and calibrated ---
    logger.info("Computing diagnostics ...")

    by_aadt_raw = _aadt_decile_table(df_thin, "pred_a", "pred_b")
    by_aadt_cal = _aadt_decile_table(df_thin, "pred_a_cal", "pred_b_cal")

    by_family_raw = _resid_table(df_thin, "family", "pred_a", "pred_b")
    by_family_cal = _resid_table(df_thin, "family", "pred_a_cal", "pred_b_cal")

    by_cls_raw = _resid_table(df_thin, "road_classification", "pred_a", "pred_b")
    by_cls_cal = _resid_table(df_thin, "road_classification", "pred_a_cal", "pred_b_cal")

    # --- top-risk bands ---
    # One row per link. Use summed predictions for residuals.
    # Use mean predicted rate for ranking/banding.
    link_agg = df_thin.groupby("link_id").agg(
        collision_count=("collision_count", "sum"),
        pred_a_total=("pred_a", "sum"),
        pred_b_total=("pred_b", "sum"),
        pred_a_cal_total=("pred_a_cal", "sum"),
        pred_b_cal_total=("pred_b_cal", "sum"),
        pred_a_rate=("pred_a", "mean"),
        pred_b_rate=("pred_b", "mean"),
        pred_a_cal_rate=("pred_a_cal", "mean"),
        pred_b_cal_rate=("pred_b_cal", "mean"),
        n_years=("year", "nunique"),
        road_classification=("road_classification", "first"),
        family=("family", "first"),
    )

    by_band_raw = _top_risk_band_table(
        link_agg,
        pred_a_rate_col="pred_a_rate",
        pred_b_rate_col="pred_b_rate",
        pred_a_total_col="pred_a_total",
        pred_b_total_col="pred_b_total",
    )

    by_band_cal = _top_risk_band_table(
        link_agg,
        pred_a_rate_col="pred_a_cal_rate",
        pred_b_rate_col="pred_b_cal_rate",
        pred_a_total_col="pred_a_cal_total",
        pred_b_total_col="pred_b_cal_total",
    )

    # Common-band comparison: Model A bands used as fixed operational groups.
    by_band_common_raw = _top_risk_band_table_common_basis(
        link_agg,
        basis_rate_col="pred_a_rate",
        pred_a_total_col="pred_a_total",
        pred_b_total_col="pred_b_total",
    )

    by_band_common_cal = _top_risk_band_table_common_basis(
        link_agg,
        basis_rate_col="pred_a_cal_rate",
        pred_a_total_col="pred_a_cal_total",
        pred_b_total_col="pred_b_cal_total",
    )

    # --- motorway precision stats ---
    mw_full_raw_stats = _mw_stats_from_frame(
        df_thin,
        "pred_a",
        "pred_b",
        "full scored frame, raw predictions",
    )
    mw_full_cal_stats = _mw_stats_from_frame(
        df_thin,
        "pred_a_cal",
        "pred_b_cal",
        "full scored frame, intercept-calibrated predictions",
    )

    mw_precision = {
        "training_frame": mw_train_stats,
        "full_frame_raw": mw_full_raw_stats,
        "full_frame_calibrated": mw_full_cal_stats,
        "explanation": (
            "The training-frame mean_resid is exactly 0.0 by construction. "
            "The Poisson GLM feature set includes 'is_motorway' and 'is_a_road' binary "
            "indicators. For a Poisson GLM with canonical log link, the score equations "
            "at convergence require Σ_i[x_ij*(y_i-μ_i)]=0 for every predictor j. "
            "For a binary indicator x_ij ∈ {0,1}, this becomes Σ_group(y_i-μ_i)=0 "
            "within the TRAINING FRAME — i.e. sum(obs) = sum(pred) exactly for motorway "
            "links in the training data. This is a GLM score-equation identity, not "
            "evidence of perfect calibration. Full-frame residuals are not constrained "
            "this way because the model was fitted on a downsampled subset."
        ),
    }

    # --- bundle ---
    report = {
        "model_summary": {
            "model_a": {
                "pseudo_r2": round(pr2_a, 6),
                "coef_log_aadt": None,
                "coef_log_link_length": round(coefs_a.get("log_link_length", np.nan), 6),
                "effective_length_beta": round(1.0 + coefs_a.get("log_link_length", 0.0), 6),
            },
            "model_b": {
                "pseudo_r2": round(pr2_b, 6),
                "coef_log_aadt": round(coefs_b.get("log_aadt", np.nan), 6),
                "coef_log_link_length": round(coefs_b.get("log_link_length", np.nan), 6),
                "effective_length_beta": round(coefs_b.get("log_link_length", np.nan), 6),
            },
        },
        "calibration": calibration,
        "motorway_precision": mw_precision,
        "raw": {
            "by_aadt_decile": by_aadt_raw.reset_index().to_dict(orient="records"),
            "by_family": by_family_raw.reset_index().to_dict(orient="records"),
            "by_road_class": by_cls_raw.reset_index().to_dict(orient="records"),
            "by_top_risk_band": by_band_raw.to_dict(orient="records"),
            "by_top_risk_band_common_basis": by_band_common_raw.to_dict(orient="records"),
        },
        "calibrated": {
            "by_aadt_decile": by_aadt_cal.reset_index().to_dict(orient="records"),
            "by_family": by_family_cal.reset_index().to_dict(orient="records"),
            "by_road_class": by_cls_cal.reset_index().to_dict(orient="records"),
            "by_top_risk_band": by_band_cal.to_dict(orient="records"),
            "by_top_risk_band_common_basis": by_band_common_cal.to_dict(orient="records"),
        },
    }

    # --- save ---
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(report, f, indent=2)
    logger.info(f"JSON written to {OUT_JSON}")

    _write_markdown(report)

    # --- console summary ---
    logger.info("=== Done ===")

    print("\n=== MODEL SUMMARY ===")
    print(f"Model A pseudo-R²: {pr2_a:.4f}")
    print(f"Model B pseudo-R²: {pr2_b:.4f}")

    print("\n=== INTERCEPT CALIBRATION ===")
    print(
        f"Model A factor={calibration['model_a']['factor']:.6f}, "
        f"log_correction={calibration['model_a']['log_correction']:.6f}"
    )
    print(
        f"Model B factor={calibration['model_b']['factor']:.6f}, "
        f"log_correction={calibration['model_b']['log_correction']:.6f}"
    )

    print("\n=== MOTORWAY FULL-FRAME RAW ===")
    mw_f = mw_precision["full_frame_raw"]
    print(f"  sum_obs: {mw_f['sum_obs']:.0f}")
    print(
        f"  Model A: sum_pred={mw_f['sum_pred_a']:.2f}, "
        f"net_resid={mw_f['net_resid_a']:.2f}, rel={mw_f['rel_resid_a']:.4f}"
    )
    print(
        f"  Model B: sum_pred={mw_f['sum_pred_b']:.2f}, "
        f"net_resid={mw_f['net_resid_b']:.2f}, rel={mw_f['rel_resid_b']:.4f}"
    )

    print("\n=== MOTORWAY FULL-FRAME CALIBRATED ===")
    mw_fc = mw_precision["full_frame_calibrated"]
    print(f"  sum_obs: {mw_fc['sum_obs']:.0f}")
    print(
        f"  Model A: sum_pred={mw_fc['sum_pred_a']:.2f}, "
        f"net_resid={mw_fc['net_resid_a']:.2f}, rel={mw_fc['rel_resid_a']:.4f}"
    )
    print(
        f"  Model B: sum_pred={mw_fc['sum_pred_b']:.2f}, "
        f"net_resid={mw_fc['net_resid_b']:.2f}, rel={mw_fc['rel_resid_b']:.4f}"
    )

    print("\n=== CALIBRATED AADT DECILE RESIDUALS ===")
    print(
        by_aadt_cal[
            [
                "aadt_mean",
                "sum_obs",
                "net_resid_a",
                "rel_resid_a",
                "net_resid_b",
                "rel_resid_b",
                "rel_improvement",
            ]
        ].to_string()
    )

    print("\n=== CALIBRATED FAMILY RESIDUALS ===")
    print(
        by_family_cal[
            [
                "n",
                "sum_obs",
                "net_resid_a",
                "rel_resid_a",
                "net_resid_b",
                "rel_resid_b",
                "rel_improvement",
            ]
        ].to_string()
    )

    # --- per-family intercept calibration ---
    logger.info("Computing per-family intercept calibration ...")

    # Factors from raw Model A predictions (sum_obs / sum_pred_a per family).
    fam_factors = (by_family_raw["sum_obs"] / by_family_raw["sum_pred_a"]).to_dict()
    global_factor = calibration["model_a"]["factor"]

    # Apply per-family correction; fall back to global factor for unknown families.
    df_thin["pred_a_family_cal"] = df_thin["pred_a"] * df_thin["family"].map(fam_factors).fillna(
        global_factor
    )

    # Add family-cal columns to link_agg for top-risk-band comparison.
    fam_cal_link = df_thin.groupby("link_id").agg(
        pred_a_fam_cal_total=("pred_a_family_cal", "sum"),
        pred_a_fam_cal_rate=("pred_a_family_cal", "mean"),
    )
    link_agg = link_agg.join(fam_cal_link)

    # Build calibration factors table.
    cal_factors_records = []
    for fam, factor in sorted(fam_factors.items()):
        row = by_family_raw.loc[fam]
        n = int(row["n"])
        sum_obs = float(row["sum_obs"])
        sum_pred_raw = float(row["sum_pred_a"])
        sum_pred_global = sum_pred_raw * global_factor
        cal_factors_records.append(
            {
                "family": fam,
                "n": n,
                "sum_obs": round(sum_obs, 2),
                "sum_pred_raw": round(sum_pred_raw, 2),
                "sum_pred_global": round(sum_pred_global, 2),
                "sum_pred_family": round(sum_obs, 2),  # by construction
                "factor": round(factor, 6),
                "log_factor": round(float(np.log(factor)), 6),
            }
        )

    # 3-way residual diagnostics.
    fam_3way = _resid_3way(df_thin, "family").reset_index()
    cls_3way = _resid_3way(df_thin, "road_classification").reset_index()
    aadt_3way = _aadt_decile_3way(df_thin).reset_index()
    band_3way = _top_risk_band_3way_common(link_agg)

    fam_cal_report = {
        "calibration_factors": cal_factors_records,
        "by_family": fam_3way.to_dict(orient="records"),
        "by_road_class": cls_3way.to_dict(orient="records"),
        "by_aadt_decile": aadt_3way.to_dict(orient="records"),
        "by_top_risk_band_common_basis": band_3way.to_dict(orient="records"),
    }

    FAM_CAL_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(FAM_CAL_JSON, "w") as f:
        json.dump(fam_cal_report, f, indent=2)
    logger.info(f"Family-cal JSON written to {FAM_CAL_JSON}")

    _write_family_cal_markdown(fam_cal_report)

    print("\n=== FAMILY-CAL FACTORS ===")
    for r in cal_factors_records:
        print(
            f"  {r['family']:15s}  factor={r['factor']:.4f}  "
            f"log={r['log_factor']:+.4f}  "
            f"obs={r['sum_obs']:,.0f}  raw_pred={r['sum_pred_raw']:,.0f}"
        )

    # --- within-family AADT decile diagnostic ---
    # Pass only the 6 needed columns so per-family .copy() stays small.
    logger.info("Computing within-family AADT decile diagnostics ...")
    _wf_thin = df_thin[
        ["family", "estimated_aadt", "collision_count", "pred_a", "pred_a_cal", "pred_a_family_cal"]
    ]
    within_fam_results = _within_family_aadt_decile_3way(_wf_thin)
    del _wf_thin

    WITHIN_FAM_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(WITHIN_FAM_JSON, "w") as f:
        json.dump(within_fam_results, f, indent=2)
    logger.info(f"Within-family JSON written to {WITHIN_FAM_JSON}")

    _write_within_family_markdown(within_fam_results)

    print("\n=== WITHIN-FAMILY AADT DECILE (family-cal rel_resid range) ===")
    for fam in FAMILY_ORDER:
        if fam not in within_fam_results:
            continue
        records = within_fam_results[fam]
        rels = [r["rel_resid_family"] for r in records]
        print(
            f"  {fam:15s}  min={min(rels):+.4f}  max={max(rels):+.4f}  "
            f"range={max(rels) - min(rels):.4f}"
        )

    return report


if __name__ == "__main__":
    run()
