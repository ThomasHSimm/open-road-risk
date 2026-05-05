"""
exposure_offset_experiment.py
------------------------------
Controlled experiment: exposure-as-offset vs exposure-as-feature in Stage 2 GLM.

Tests three GLM variants:
  A — current production: full offset log(AADT × length × 365/1e6), forces β=1
  B — fully learned: no offset; log_aadt and log_length as free features
  C — hybrid: partial offset log(length × 365/1e6); log_aadt as learned feature

Plus an overdispersion check and optional NegBin sensitivity fit.

Output: JSON results printed to stdout + docs/internal/exposure_offset_experiment.md
        (and a JSON sidecar at same path for machine consumption).

Run with: conda run -n env1 python src/road_risk/diagnostics/exposure_offset_experiment.py
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

# --- project imports --------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parents[3]))  # ensure src/ is on path
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

RISK_SCORES_PATH = MODELS / "risk_scores.parquet"
OUT_DIR = _ROOT / "docs" / "internal"
OUT_MD = OUT_DIR / "exposure_offset_experiment.md"
OUT_JSON = OUT_DIR / "exposure_offset_experiment.json"

# Core structural features shared across all three models (no exposure terms)
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

OVERDISPERSION_THRESHOLD = 1.5


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _downsample(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Downsample zeros to GLM_ZERO_SAMPLE_RATIO × positives (same policy as production)."""
    pos_idx = df.index[df["collision_count"] > 0]
    zero_idx = df.index[df["collision_count"] == 0]
    n_keep = min(len(zero_idx), len(pos_idx) * GLM_ZERO_SAMPLE_RATIO)
    zero_sample = rng.choice(zero_idx, size=n_keep, replace=False)
    sel = np.concatenate([pos_idx.values, zero_sample])
    sel.sort()
    logger.info(f"  Downsampled: {len(pos_idx):,} pos + {n_keep:,} zeros = {len(sel):,} rows")
    return df.loc[sel].copy()


def _fit_glm(X, y, offset, family=None):
    if family is None:
        family = sm.families.Poisson()
    return sm.GLM(y, X, family=family, offset=offset).fit(maxiter=200)


def _null_deviance_poisson(y: np.ndarray, offset: np.ndarray) -> float:
    """Direct Poisson null deviance (intercept-only model with offset).

    Avoids statsmodels' null_deviance property which re-runs IRLS internally
    and overflows when the offset has extreme values (e.g. log(length×365/1e6)
    without AADT terms, producing values around -30 to -20 for short links).

    alpha is chosen so Σ(mu) = Σ(y), i.e. alpha = log(Σy / Σexp(offset)).
    """
    y = np.asarray(y, dtype=float)
    offset = np.clip(np.asarray(offset, dtype=float), -50.0, 50.0)
    sum_y = y.sum()
    sum_exp = np.exp(offset).sum()
    if sum_y <= 0 or sum_exp <= 0:
        return np.inf
    alpha = np.log(sum_y / sum_exp)
    mu_null = np.exp(np.clip(alpha + offset, -50.0, 50.0))
    eps = 1e-300
    contrib = np.where(y > 0, y * np.log((y + eps) / (mu_null + eps)), 0.0) - (y - mu_null)
    return float(2.0 * contrib.sum())


def _pseudo_r2(result, y=None, offset=None) -> float:
    """Pseudo-R² = 1 - deviance/null_deviance.

    Falls back to direct computation when statsmodels' null_deviance property
    fails (it re-fits an intercept-only model internally, which overflows with
    extreme partial offsets). Pass y and offset to enable the fallback.
    """
    deviance = float(result.deviance)
    try:
        null_dev = float(result.null_deviance)
        if not np.isfinite(null_dev) or null_dev <= 0:
            raise ValueError("non-finite null_deviance")
    except Exception:
        if y is None or offset is None:
            raise RuntimeError(
                "null_deviance computation failed; pass y= and offset= to _pseudo_r2"
            )
        null_dev = _null_deviance_poisson(
            np.asarray(y, dtype=float), np.asarray(offset, dtype=float)
        )
        logger.info(f"  Used manual null deviance: {null_dev:.1f}")
    return float(1.0 - deviance / null_dev)


def _residuals_by_group(df_scored: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Mean Pearson residual (observed − predicted) by group."""
    df_scored = df_scored.copy()
    df_scored["pearson_resid"] = df_scored["collision_count"] - df_scored["pred"]
    return (
        df_scored.groupby(group_col)
        .agg(
            n=("collision_count", "count"),
            sum_obs=("collision_count", "sum"),
            sum_pred=("pred", "sum"),
            mean_resid=("pearson_resid", "mean"),
        )
        .round(4)
    )


def _jaccard_top1(pred_series: pd.Series, prod_series: pd.Series) -> float:
    """Jaccard similarity of top-1% sets (by link_id index)."""
    n = len(pred_series)
    k = max(1, int(round(n * 0.01)))
    top_exp = set(pred_series.nlargest(k).index)
    top_prod = set(prod_series.nlargest(k).index)
    inter = len(top_exp & top_prod)
    union = len(top_exp | top_prod)
    return inter / union if union else 0.0


# ---------------------------------------------------------------------------
# model fitting
# ---------------------------------------------------------------------------


def fit_model_a(glm_df: pd.DataFrame) -> dict:
    """
    Model A: production formulation.
    offset = log(AADT × length × 365/1e6); log_link_length also in features.
    """
    logger.info("Fitting Model A (current offset) ...")
    features = STRUCTURAL_COLS + ["log_link_length"]
    X = sm.add_constant(glm_df[features].astype(float))
    y = glm_df["collision_count"].astype(int)
    offset = glm_df["log_offset"].astype(float)

    result = _fit_glm(X, y, offset)
    glm_df["pred_a"] = result.predict(X, offset=offset)

    coefs = result.params.to_dict()
    return {
        "pseudo_r2": _pseudo_r2(result, y=y, offset=offset),
        "deviance": float(result.deviance),
        "aic": float(result.aic),
        "converged": bool(result.converged),
        "n_obs": int(len(glm_df)),
        "coef_log_link_length": float(coefs.get("log_link_length", np.nan)),
        "coef_log_aadt": None,  # absorbed into offset
        "note": "AADT and length both in offset (β=1 forced); log_link_length also as feature",
        "features": features,
        "_result": result,
        "_features": features,
        "_offset_col": "log_offset",
    }


def fit_model_b(glm_df: pd.DataFrame) -> dict:
    """
    Model B: fully learned exposure.
    No offset. log_aadt and log_link_length as free features.
    """
    logger.info("Fitting Model B (learned exposure) ...")
    features = STRUCTURAL_COLS + ["log_aadt", "log_link_length"]
    X = sm.add_constant(glm_df[features].astype(float))
    y = glm_df["collision_count"].astype(int)
    zero_offset = pd.Series(np.zeros(len(glm_df)), index=glm_df.index)

    result = _fit_glm(X, y, zero_offset)
    glm_df["pred_b"] = result.predict(X, offset=zero_offset)

    coefs = result.params.to_dict()
    return {
        "pseudo_r2": _pseudo_r2(result, y=y, offset=zero_offset),
        "deviance": float(result.deviance),
        "aic": float(result.aic),
        "converged": bool(result.converged),
        "n_obs": int(len(glm_df)),
        "coef_log_aadt": float(coefs.get("log_aadt", np.nan)),
        "coef_log_link_length": float(coefs.get("log_link_length", np.nan)),
        "note": "No offset; AADT and length learned freely",
        "features": features,
        "_result": result,
        "_features": features,
        "_offset_col": None,
    }


def fit_model_c(glm_df: pd.DataFrame) -> dict:
    """
    Model C: hybrid.
    offset = log(length × 365/1e6); log_aadt as learned feature.
    Fixes β_length=1, learns β_aadt freely.
    """
    logger.info("Fitting Model C (hybrid offset) ...")
    features = STRUCTURAL_COLS + ["log_aadt"]
    X = sm.add_constant(glm_df[features].astype(float))
    y = glm_df["collision_count"].astype(int)
    # Partial offset: length × days, without AADT
    partial_offset = glm_df["log_length_offset"].astype(float)

    result = _fit_glm(X, y, partial_offset)
    glm_df["pred_c"] = result.predict(X, offset=partial_offset)

    coefs = result.params.to_dict()
    return {
        "pseudo_r2": _pseudo_r2(result, y=y, offset=partial_offset),
        "deviance": float(result.deviance),
        "aic": float(result.aic),
        "converged": bool(result.converged),
        "n_obs": int(len(glm_df)),
        "coef_log_aadt": float(coefs.get("log_aadt", np.nan)),
        "coef_log_link_length": None,  # fixed at β=1 via offset
        "note": "offset=log(length×365/1e6); log_aadt learned",
        "features": features,
        "_result": result,
        "_features": features,
        "_offset_col": "log_length_offset",
    }


def fit_negbin_a(glm_df: pd.DataFrame) -> dict:
    """
    NegBin sensitivity for Model A formulation.
    Only run if overdispersion ratio > OVERDISPERSION_THRESHOLD.
    """
    logger.info("Fitting NegBin sensitivity (Model A formulation) ...")
    features = STRUCTURAL_COLS + ["log_link_length"]
    X = sm.add_constant(glm_df[features].astype(float))
    y = glm_df["collision_count"].astype(int)
    offset = glm_df["log_offset"].astype(float)

    try:
        result = sm.GLM(
            y,
            X,
            family=sm.families.NegativeBinomial(),
            offset=offset,
        ).fit(maxiter=200)
        converged = bool(result.converged)
        pseudo_r2 = _pseudo_r2(result, y=y, offset=offset)
        aic = float(result.aic)
    except Exception as e:
        logger.warning(f"  NegBin failed: {e}")
        return {"error": str(e)}

    return {
        "pseudo_r2": pseudo_r2,
        "deviance": float(result.deviance),
        "aic": aic,
        "converged": converged,
    }


# ---------------------------------------------------------------------------
# Jaccard from downsampled frame (memory-safe approximation)
# ---------------------------------------------------------------------------


def _link_pred_from_sample(glm_df: pd.DataFrame, pred_col: str) -> pd.Series:
    """
    Pool predicted rates to link_id from the downsampled GLM frame.
    Used for Jaccard approximation instead of scoring the full 21M-row dataset,
    which would require ~3 extra copies of the full frame and OOM on <32 GB machines.
    The downsampled frame retains all positive link-years, so top-1% overlap
    is representative for diagnostic purposes.
    """
    return glm_df.groupby("link_id")[pred_col].mean()


# ---------------------------------------------------------------------------
# main experiment
# ---------------------------------------------------------------------------


def run():
    logger.info("=== Exposure offset experiment ===")

    # --- load data ---
    logger.info("Loading data ...")
    openroads = gpd.read_parquet(OPENROADS_PATH)
    rla = pd.read_parquet(RLA_PATH)
    net_features = pd.read_parquet(NET_PATH) if NET_PATH.exists() else None
    aadt_estimates = pd.read_parquet(AADT_PATH)
    prod_scores = pd.read_parquet(RISK_SCORES_PATH).set_index("link_id")

    df = build_collision_dataset(openroads, aadt_estimates, rla, net_features)

    # --- add experiment-specific columns ---
    df["log_aadt"] = np.log(df["estimated_aadt"].clip(lower=1.0))
    # Partial offset for Model C: log(length × 365/1e6)
    df["log_length_offset"] = np.log((df["link_length_km"] * 365 / 1e6).clip(lower=1e-9))

    # --- overdispersion ---
    logger.info("Computing overdispersion ...")
    y_all = df["collision_count"]
    dispersion_ratio = float(y_all.var() / y_all.mean())
    logger.info(f"  Dispersion ratio (var/mean): {dispersion_ratio:.3f}")
    run_negbin = dispersion_ratio > OVERDISPERSION_THRESHOLD

    # --- downsample for GLM fitting ---
    rng = np.random.default_rng(RANDOM_STATE)
    core_required = list(STRUCTURAL_COLS) + [
        "log_link_length",
        "log_aadt",
        "log_offset",
        "log_length_offset",
    ]
    core_required = [c for c in core_required if c in df.columns]
    full_idx = df.dropna(subset=core_required).index
    glm_df = _downsample(df.loc[full_idx], rng)

    # --- fit models ---
    res_a = fit_model_a(glm_df)
    res_b = fit_model_b(glm_df)
    res_c = fit_model_c(glm_df)

    negbin_result = None
    if run_negbin:
        logger.info(
            f"Overdispersion {dispersion_ratio:.2f} > {OVERDISPERSION_THRESHOLD} — fitting NegBin sensitivity"
        )
        negbin_result = fit_negbin_a(glm_df)
    else:
        logger.info(
            f"Overdispersion {dispersion_ratio:.2f} ≤ {OVERDISPERSION_THRESHOLD} — NegBin skipped"
        )

    # --- residuals by road class (on downsampled df) ---
    logger.info("Computing residuals by road class ...")

    def _resid_table(pred_col: str) -> pd.DataFrame:
        tmp = glm_df[["road_classification", "collision_count", pred_col]].copy()
        tmp = tmp.rename(columns={pred_col: "pred"})
        return _residuals_by_group(tmp, "road_classification")

    resid_a_class = _resid_table("pred_a")
    resid_b_class = _resid_table("pred_b")
    resid_c_class = _resid_table("pred_c")

    # --- residuals by AADT decile ---
    logger.info("Computing residuals by AADT decile ...")
    glm_df["aadt_decile"] = pd.qcut(glm_df["estimated_aadt"], q=10, labels=False, duplicates="drop")

    def _resid_aadt(pred_col: str) -> pd.DataFrame:
        tmp = glm_df[["aadt_decile", "estimated_aadt", "collision_count", pred_col]].copy()
        tmp = tmp.rename(columns={pred_col: "pred"})
        g = tmp.groupby("aadt_decile").agg(
            n=("collision_count", "count"),
            aadt_mean=("estimated_aadt", "mean"),
            sum_obs=("collision_count", "sum"),
            sum_pred=("pred", "sum"),
        )
        g["mean_resid"] = g["sum_obs"] - g["sum_pred"]
        return g.round(3)

    resid_a_aadt = _resid_aadt("pred_a")
    resid_b_aadt = _resid_aadt("pred_b")
    resid_c_aadt = _resid_aadt("pred_c")

    # --- top-1% Jaccard vs production (approximate, from downsampled frame) ---
    # Full-dataset scoring would require copying the 21M-row df three times (~OOM).
    # The downsampled frame retains all positive link-years, making it sufficient
    # for top-1% overlap diagnostics.
    logger.info("Computing Jaccard vs production top-1% (from downsampled frame) ...")
    prod_pred = prod_scores["predicted_xgb"]

    link_pred_a = _link_pred_from_sample(glm_df, "pred_a")
    link_pred_b = _link_pred_from_sample(glm_df, "pred_b")
    link_pred_c = _link_pred_from_sample(glm_df, "pred_c")

    # Align to common index (downsampled frame covers subset of all links)
    common_a = prod_pred.index.intersection(link_pred_a.index)
    common_b = prod_pred.index.intersection(link_pred_b.index)
    common_c = prod_pred.index.intersection(link_pred_c.index)
    jac_a = _jaccard_top1(link_pred_a.loc[common_a], prod_pred.loc[common_a])
    jac_b = _jaccard_top1(link_pred_b.loc[common_b], prod_pred.loc[common_b])
    jac_c = _jaccard_top1(link_pred_c.loc[common_c], prod_pred.loc[common_c])
    logger.info(f"  Jaccard A={jac_a:.3f}  B={jac_b:.3f}  C={jac_c:.3f}")

    # --- motorway residuals specifically ---
    def _motorway_mean_resid(pred_col: str) -> float:
        mw = glm_df[glm_df["road_classification"] == "Motorway"]
        return float((mw["collision_count"] - mw[pred_col]).mean())

    mw_a = _motorway_mean_resid("pred_a")
    mw_b = _motorway_mean_resid("pred_b")
    mw_c = _motorway_mean_resid("pred_c")

    # --- bundle results ---
    results = {
        "dispersion_ratio": round(dispersion_ratio, 4),
        "negbin_run": run_negbin,
        "model_a": {
            "exposure": "full offset: log(AADT × length × 365/1e6)",
            "pseudo_r2": round(res_a["pseudo_r2"], 4),
            "deviance": round(res_a["deviance"], 1),
            "aic": round(res_a["aic"], 1),
            "converged": res_a["converged"],
            "coef_log_aadt": res_a["coef_log_aadt"],
            "coef_log_link_length": round(res_a["coef_log_link_length"], 4),
            "jaccard_vs_prod": round(jac_a, 4),
            "motorway_mean_resid": round(mw_a, 4),
        },
        "model_b": {
            "exposure": "no offset; log_aadt and log_link_length as features",
            "pseudo_r2": round(res_b["pseudo_r2"], 4),
            "deviance": round(res_b["deviance"], 1),
            "aic": round(res_b["aic"], 1),
            "converged": res_b["converged"],
            "coef_log_aadt": round(res_b["coef_log_aadt"], 4),
            "coef_log_link_length": round(res_b["coef_log_link_length"], 4),
            "jaccard_vs_prod": round(jac_b, 4),
            "motorway_mean_resid": round(mw_b, 4),
        },
        "model_c": {
            "exposure": "hybrid: offset=log(length×365/1e6); log_aadt learned",
            "pseudo_r2": round(res_c["pseudo_r2"], 4),
            "deviance": round(res_c["deviance"], 1),
            "aic": round(res_c["aic"], 1),
            "converged": res_c["converged"],
            "coef_log_aadt": round(res_c["coef_log_aadt"], 4),
            "coef_log_link_length": res_c["coef_log_link_length"],
            "jaccard_vs_prod": round(jac_c, 4),
            "motorway_mean_resid": round(mw_c, 4),
        },
        "negbin": negbin_result if negbin_result else "not_run",
    }

    # --- residual tables as dicts for JSON ---
    def _df_to_dict(d: pd.DataFrame) -> dict:
        return d.reset_index().to_dict(orient="records")

    residuals = {
        "by_road_class": {
            "model_a": _df_to_dict(resid_a_class),
            "model_b": _df_to_dict(resid_b_class),
            "model_c": _df_to_dict(resid_c_class),
        },
        "by_aadt_decile": {
            "model_a": _df_to_dict(resid_a_aadt),
            "model_b": _df_to_dict(resid_b_aadt),
            "model_c": _df_to_dict(resid_c_aadt),
        },
    }
    full_output = {"summary": results, "residuals": residuals}

    # --- save JSON ---
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(full_output, f, indent=2)
    logger.info(f"JSON written to {OUT_JSON}")

    # --- write markdown report ---
    _write_markdown(
        results,
        residuals,
        resid_a_class,
        resid_b_class,
        resid_c_class,
        resid_a_aadt,
        resid_b_aadt,
        resid_c_aadt,
    )

    print("\n=== EXPERIMENT COMPLETE ===")
    print(json.dumps(results, indent=2))
    return full_output


def _write_markdown(results, residuals, ra_cls, rb_cls, rc_cls, ra_aadt, rb_aadt, rc_aadt):
    r = results
    ma, mb, mc = r["model_a"], r["model_b"], r["model_c"]

    def _nb_row():
        nb = r.get("negbin")
        if nb == "not_run":
            return f"Not run (dispersion ratio {r['dispersion_ratio']:.2f} ≤ {OVERDISPERSION_THRESHOLD})"
        if isinstance(nb, dict) and "error" in nb:
            return f"Failed: {nb['error']}"
        if isinstance(nb, dict):
            return (
                f"pseudo-R²={nb['pseudo_r2']:.4f}, AIC={nb['aic']:.0f}, converged={nb['converged']}"
            )
        return str(nb)

    def _cls_md(df: pd.DataFrame) -> str:
        rows = ["| Road class | N | Obs | Pred | Mean resid |", "|---|---:|---:|---:|---:|"]
        for _, row in df.reset_index().iterrows():
            rows.append(
                f"| {row['road_classification']} | {int(row['n']):,} | "
                f"{row['sum_obs']:.0f} | {row['sum_pred']:.0f} | {row['mean_resid']:.4f} |"
            )
        return "\n".join(rows)

    def _aadt_md(df: pd.DataFrame) -> str:
        rows = ["| Decile | Mean AADT | Obs | Pred | Net resid |", "|---|---:|---:|---:|---:|"]
        for _, row in df.reset_index().iterrows():
            rows.append(
                f"| {int(row['aadt_decile'])} | {row['aadt_mean']:,.0f} | "
                f"{row['sum_obs']:.0f} | {row['sum_pred']:.0f} | {row['mean_resid']:.1f} |"
            )
        return "\n".join(rows)

    md = f"""---
title: "Stage 2 GLM: Exposure offset experiment"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** GLM-only diagnostic. No production models changed.
**Purpose:** Test whether fixed exposure offset (β=1 forced) is misspecified relative to
empirically learned β values, and measure impact on residual bias by road class and AADT extremes.

---

## 1. Background

The current Stage 2 GLM uses `log(AADT × length × 365/1e6)` as a fixed Poisson offset,
which forces the exposure scaling coefficient β=1. The `collision-exposure-behaviour.qmd`
diagnostic showed empirical β values of 0.46–0.81 across road classes, suggesting the offset
is misspecified. This experiment tests three formulations on the same downsampled training
data (ratio 1:{GLM_ZERO_SAMPLE_RATIO} zeros:positives) to isolate the exposure treatment effect.

Production baseline (collision_metrics.json): GLM pseudo-R²=0.351, XGBoost pseudo-R²=0.321.

---

## 2. Overdispersion check

| Statistic | Value |
|---|---:|
| Dispersion ratio (var/mean) | {r["dispersion_ratio"]:.3f} |
| Threshold for NegBin | {OVERDISPERSION_THRESHOLD} |
| NegBin sensitivity | {_nb_row()} |

---

## 3. Model variant summary

| Model | Exposure treatment | pseudo-R² | Deviance | AIC | Converged |
|---|---|---:|---:|---:|---|
| A (production) | Full offset: log(AADT×length×365/1e6) | {ma["pseudo_r2"]:.4f} | {ma["deviance"]:,.0f} | {ma["aic"]:,.0f} | {ma["converged"]} |
| B (learned) | No offset; log_aadt + log_length as features | {mb["pseudo_r2"]:.4f} | {mb["deviance"]:,.0f} | {mb["aic"]:,.0f} | {mb["converged"]} |
| C (hybrid) | Partial offset log(length×365/1e6); log_aadt learned | {mc["pseudo_r2"]:.4f} | {mc["deviance"]:,.0f} | {mc["aic"]:,.0f} | {mc["converged"]} |

### Exposure coefficients

| Model | coef(log_aadt) | coef(log_length) | Note |
|---|---:|---:|---|
| A | — (β=1 forced) | {ma["coef_log_link_length"]} | length residual adjustment |
| B | {mb["coef_log_aadt"]} | {mb["coef_log_link_length"]} | both freely learned |
| C | {mc["coef_log_aadt"]} | — (β=1 via offset) | AADT freely learned |

### Top-1% ranking Jaccard vs production XGBoost

Computed from the downsampled GLM frame (all positive link-years + sampled zeros).
Directionally correct for diagnosis; not a full-population Jaccard.

| Comparison | Jaccard |
|---|---:|
| Model A GLM vs production XGBoost | {ma["jaccard_vs_prod"]:.4f} |
| Model B GLM vs production XGBoost | {mb["jaccard_vs_prod"]:.4f} |
| Model C GLM vs production XGBoost | {mc["jaccard_vs_prod"]:.4f} |

### Motorway mean residual (observed − predicted, downsampled frame)

| Model | Mean residual |
|---|---:|
| A | {ma["motorway_mean_resid"]:.4f} |
| B | {mb["motorway_mean_resid"]:.4f} |
| C | {mc["motorway_mean_resid"]:.4f} |

Positive = model under-predicts (more collisions than expected).
Negative = model over-predicts.

---

## 4. Residuals by road class

### Model A (current offset)

{_cls_md(ra_cls)}

### Model B (learned exposure)

{_cls_md(rb_cls)}

### Model C (hybrid)

{_cls_md(rc_cls)}

---

## 5. Residuals by AADT decile

Decile 0 = lowest traffic, 9 = highest. Net residual = sum(observed) − sum(predicted) across all rows in decile.

### Model A

{_aadt_md(ra_aadt)}

### Model B

{_aadt_md(rb_aadt)}

### Model C

{_aadt_md(rc_aadt)}

---

## 6. Interpretation

**Key diagnostic question:** Does learned exposure reduce systematic residual bias at AADT extremes and by facility family?

Fill in after reviewing the tables above:

- **Model B coef(log_aadt):** {mb["coef_log_aadt"]:.4f} (vs 1.0 forced in A). Sub-linear if < 1, confirming misspecification.
- **Model C coef(log_aadt):** {mc["coef_log_aadt"]:.4f} — isolates AADT scaling with length held fixed.
- **Motorway bias direction:** A={ma["motorway_mean_resid"]:.4f}, B={mb["motorway_mean_resid"]:.4f}, C={mc["motorway_mean_resid"]:.4f}.
  Under-prediction (positive) on motorways was the primary concern; compare sign/magnitude across models.
- **AADT extreme bias:** Review decile 0 and 9 net residuals across models for whether learned exposure
  reduces systematic over/under-prediction at traffic extremes.
- **Ranking stability:** Jaccard A/B/C vs production XGBoost indicates whether exposure
  treatment alone moves the operational top-1% set.

---

## 7. Next steps

Based on findings:
- If Model C shows materially lower residual bias at AADT extremes with comparable or better
  pseudo-R²: consider adopting hybrid offset as the v3 GLM formulation.
- If B and C show similar results: the AADT scaling is the dominant issue; length can stay fixed.
- If motorway under-prediction persists across all variants: the problem is not exposure treatment
  alone — investigate motorway-specific features or per-family GLMs.
- Per-family k values (EB shrinkage v2) remain the recommended next step regardless of outcome.

_Machine-readable results: `docs/internal/exposure_offset_experiment.json`_
"""

    with open(OUT_MD, "w") as f:
        f.write(md)
    logger.info(f"Markdown written to {OUT_MD}")


if __name__ == "__main__":
    run()
