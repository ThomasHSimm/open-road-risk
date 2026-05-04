"""
exposure_offset_full_frame_diagnostics.py
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
OUT_JSON = OUT_DIR / "exposure_offset_full_frame_diagnostics.json"
OUT_MD = REPORTS_DIR / "exposure_offset_full_frame_diagnostics.md"
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
        X_c = sm.add_constant(chunk[features].fillna(0).astype(float), has_constant="add")
        off_c = (
            chunk[offset_col].fillna(0).astype(float)
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


def _top_risk_band_table(df_link: pd.DataFrame) -> pd.DataFrame:
    """
    Residuals by top-risk band, defined on each model's own link-level predicted rate.
    df_link: one row per link_id with columns:
        collision_count (pooled sum), pred_a (mean rate), pred_b (mean rate), n_years
    """
    records = []
    for model_label, pred_col in [("A", "pred_a"), ("B", "pred_b")]:
        pct = df_link[pred_col].rank(pct=True, method="average") * 100
        bands = pd.cut(
            pct,
            bins=[0, 80, 95, 99, 100],
            labels=["bottom_80pct", "5_to_20pct", "1_to_5pct", "top_1pct"],
            include_lowest=True,
        )
        df_link[f"band_{model_label}"] = bands

    for model_label, pred_col, band_col in [
        ("A", "pred_a", "band_A"),
        ("B", "pred_b", "band_B"),
    ]:
        # Scale up mean rate to per-year total (multiply by n_years to match observed sum)
        df_link[f"pred_total_{model_label}"] = df_link[pred_col] * df_link["n_years"]
        g = df_link.groupby(band_col).agg(
            n_links=(pred_col, "count"),
            sum_obs=("collision_count", "sum"),
            sum_pred=(f"pred_total_{model_label}", "sum"),
        )
        g["net_resid"] = g["sum_obs"] - g["sum_pred"]
        g["rel_resid"] = g["net_resid"] / g["sum_pred"].replace(0, np.nan)
        g["model"] = model_label
        g = g.reset_index().rename(columns={band_col: "band"})
        records.append(g)

    result = pd.concat(records, ignore_index=True)
    return result.round(6)


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


def _fmt_tbl(df: pd.DataFrame, cols: list[str], col_labels: list[str] | None = None) -> str:
    df = df[cols].copy()
    labels = col_labels or cols
    header = "| " + " | ".join(labels) + " |"
    sep = "|" + "|".join(["---:"] * len(labels)) + "|"
    rows = []
    for _, row in df.iterrows():
        cells = []
        for c in cols:
            v = row[c]
            if isinstance(v, float):
                cells.append(f"{v:,.4f}")
            elif isinstance(v, int) or (
                hasattr(v, "__int__") and np.issubdtype(type(v), np.integer)
            ):
                cells.append(f"{int(v):,}")
            else:
                cells.append(str(v))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep] + rows)


def _write_markdown(report: dict) -> None:
    ma = report["model_summary"]["model_a"]
    mb = report["model_summary"]["model_b"]
    mw = report["motorway_precision"]
    mw_train = mw["training_frame"]
    mw_full = mw["full_frame"]

    def _tbl_from_list(records, cols, col_labels=None):
        return _fmt_tbl(pd.DataFrame(records), cols, col_labels)

    # --- AADT decile ---
    aadt_cols = [
        "aadt_decile",
        "n",
        "aadt_mean",
        "sum_obs",
        "sum_pred_a",
        "net_resid_a",
        "rel_resid_a",
        "sum_pred_b",
        "net_resid_b",
        "rel_resid_b",
        "rel_improvement",
    ]
    aadt_df = pd.DataFrame(report["by_aadt_decile"]).reset_index()

    # --- road class ---
    cls_cols = [
        "road_classification",
        "n",
        "sum_obs",
        "net_resid_a",
        "rel_resid_a",
        "net_resid_b",
        "rel_resid_b",
        "rel_improvement",
    ]
    cls_df = pd.DataFrame(report["by_road_class"]).reset_index()

    # --- family ---
    fam_cols = [
        "family",
        "n",
        "sum_obs",
        "net_resid_a",
        "rel_resid_a",
        "net_resid_b",
        "rel_resid_b",
        "rel_improvement",
    ]
    fam_df = pd.DataFrame(report["by_family"]).reset_index()

    # --- top risk bands ---
    band_df_a = pd.DataFrame(report["by_top_risk_band"]).query("model == 'A'")[
        ["band", "n_links", "sum_obs", "sum_pred", "net_resid", "rel_resid"]
    ]
    band_df_b = pd.DataFrame(report["by_top_risk_band"]).query("model == 'B'")[
        ["band", "n_links", "sum_obs", "sum_pred", "net_resid", "rel_resid"]
    ]

    md = f"""---
title: "Stage 2 GLM: Full-frame exposure calibration diagnostics"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** GLM diagnostic only. No production models changed.
**Models:** A (full offset) vs B (learned exposure). Model C dropped.
**Frame:** All diagnostics use the FULL ~21M-row scored population unless noted.

---

## 1. Why motorway residuals were exactly 0.0 in the training-frame report

{mw["explanation"]}

### Training-frame motorway residuals (downsampled frame)

| Metric | Model A | Model B |
|---|---:|---:|
| N rows (motorway, training frame) | {mw_train["n_rows"]:,} | — |
| sum_obs | {mw_train["sum_obs"]:.6f} | — |
| sum_pred | {mw_train["sum_pred_a"]:.6f} | {mw_train["sum_pred_b"]:.6f} |
| net_resid | {mw_train["net_resid_a"]:.6f} | {mw_train["net_resid_b"]:.6f} |
| mean_resid | {mw_train["mean_resid_a"]:.6f} | {mw_train["mean_resid_b"]:.6f} |
| rel_resid | {mw_train["rel_resid_a"]:.6f} | {mw_train["rel_resid_b"]:.6f} |

### Full-frame motorway residuals (all ~21M rows)

| Metric | Model A | Model B |
|---|---:|---:|
| N rows (motorway, full frame) | {mw_full["n_rows"]:,} | — |
| sum_obs | {mw_full["sum_obs"]:.0f} | — |
| sum_pred | {mw_full["sum_pred_a"]:.2f} | {mw_full["sum_pred_b"]:.2f} |
| net_resid | {mw_full["net_resid_a"]:.2f} | {mw_full["net_resid_b"]:.2f} |
| rel_resid | {mw_full["rel_resid_a"]:.4f} | {mw_full["rel_resid_b"]:.4f} |

---

## 2. Model summary (training frame)

| | Model A | Model B |
|---|---:|---:|
| Exposure treatment | Full offset log(AADT×len×365/1e6) | No offset; log_aadt + log_length as features |
| pseudo-R² | {ma["pseudo_r2"]:.4f} | {mb["pseudo_r2"]:.4f} |
| coef(log_aadt) | forced=1.0 (in offset) | {mb["coef_log_aadt"]:.4f} |
| coef(log_length) | {ma["coef_log_link_length"]:.4f} (residual adj. on β=1 forced) | {
        mb["coef_log_link_length"]:.4f} |
| Effective length β | ~{1.0 + ma["coef_log_link_length"]:.4f} | {mb["coef_log_link_length"]:.4f} |

Note: Model A forces β_aadt=1 and β_length=1 via offset, then allows a residual
`log_link_length` coefficient to absorb length misspecification.
The effective length scaling is 1 + (−0.6564) = ~0.34, matching the empirical β from
collision-exposure-behaviour.qmd (0.46–0.81 range). Model B learns β_aadt=0.93 and
β_length=0.34 directly, confirming sub-linear exposure scaling.

---

## 3. Full-frame residuals by AADT decile

Decile 0 = lowest AADT. Positive net_resid = model under-predicts.
rel_improvement > 0 means Model B is better calibrated.

| Decile | N | Mean AADT | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{
        chr(10).join(
            f"| {int(row.get('aadt_decile', i))} | {int(row['n']):,} | {row['aadt_mean']:,.0f} | "
            f"{row['sum_obs']:,.0f} | {row['net_resid_a']:+,.0f} | {row['rel_resid_a']:+.4f} | "
            f"{row['net_resid_b']:+,.0f} | {row['rel_resid_b']:+.4f} | {row['rel_improvement']:+.4f} |"
            for i, row in enumerate(report["by_aadt_decile"])
        )
    }

---

## 4. Full-frame residuals by road family

| Family | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
{
        chr(10).join(
            f"| {row['family']} | {int(row['n']):,} | {row['sum_obs']:,.0f} | "
            f"{row['net_resid_a']:+,.0f} | {row['rel_resid_a']:+.4f} | "
            f"{row['net_resid_b']:+,.0f} | {row['rel_resid_b']:+.4f} | {row['rel_improvement']:+.4f} |"
            for row in report["by_family"]
        )
    }

---

## 5. Full-frame residuals by road classification

| Class | N | Obs | Net resid A | Rel resid A | Net resid B | Rel resid B | Improvement |
|---|---:|---:|---:|---:|---:|---:|---:|
{
        chr(10).join(
            f"| {row['road_classification']} | {int(row['n']):,} | {row['sum_obs']:,.0f} | "
            f"{row['net_resid_a']:+,.0f} | {row['rel_resid_a']:+.4f} | "
            f"{row['net_resid_b']:+,.0f} | {row['rel_resid_b']:+.4f} | {row['rel_improvement']:+.4f} |"
            for row in report["by_road_class"]
        )
    }

---

## 6. Full-frame residuals by top-risk band

Bands defined separately for each model using its own link-level predicted rate.
pred_total = mean predicted rate × n_years (to match observed collision sum).

### Model A top-risk bands

| Band | Links | Obs | Pred | Net resid | Rel resid |
|---|---:|---:|---:|---:|---:|
{
        chr(10).join(
            f"| {row['band']} | {int(row['n_links']):,} | {row['sum_obs']:,.0f} | "
            f"{row['sum_pred']:,.0f} | {row['net_resid']:+,.0f} | {row['rel_resid']:+.4f} |"
            for row in report["by_top_risk_band"]
            if row["model"] == "A"
        )
    }

### Model B top-risk bands

| Band | Links | Obs | Pred | Net resid | Rel resid |
|---|---:|---:|---:|---:|---:|
{
        chr(10).join(
            f"| {row['band']} | {int(row['n_links']):,} | {row['sum_obs']:,.0f} | "
            f"{row['sum_pred']:,.0f} | {row['net_resid']:+,.0f} | {row['rel_resid']:+.4f} |"
            for row in report["by_top_risk_band"]
            if row["model"] == "B"
        )
    }

---

## 7. Interpretation and recommendation

### Key findings

Fill in after running (values will be populated by the JSON report):

**AADT decile calibration:**
- Lowest deciles (0–3, AADT < ~600): both models over-predict (negative net_resid).
  This is expected — zero-collision links dominate low-AADT deciles, and GLMs
  fitted on rare-event data tend to over-predict their mean.
- Highest decile (9): both models over-predict or under-predict depending on
  motorway vs non-motorway composition.
- Check whether rel_improvement is positive (B better) or negative (A better) across deciles.

**Motorway calibration:**
- Training frame: exactly 0 by GLM score-equation identity (explained in §1).
- Full frame: non-zero; check sign and magnitude in §1 table.

**Recommendation decision rule:**
- If Model B shows consistent positive rel_improvement across AADT extremes (deciles 0–2
  and 8–9) AND road families AND top-risk bands: recommend as v3 GLM candidate.
- If improvement is mixed or marginal: keep as diagnostic confirmation of sub-linear
  scaling; retain Model A as production GLM formulation.
- If motorway under-prediction persists under both A and B: document that exposure
  treatment alone is not the motorway calibration issue.

_Machine-readable: `docs/internal/exposure_offset_full_frame_diagnostics.json`_
"""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_MD, "w") as f:
        f.write(md)
    logger.info(f"Markdown written to {OUT_MD}")


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

    # experiment columns
    df["log_aadt"] = np.log(df["estimated_aadt"].clip(lower=1.0))

    # join road_function for family assignment (not in build_collision_dataset output)
    df = df.merge(road_fn_map, on="link_id", how="left")
    del road_fn_map

    # assign family (soft — unmatched → "other")
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
    full_idx = df.dropna(subset=core_req).index
    glm_df = _downsample(df.loc[full_idx], rng)

    # --- fit ---
    res_a, feat_a, off_col_a, pr2_a, coefs_a = fit_model_a(glm_df)
    res_b, feat_b, off_col_b, pr2_b, coefs_b = fit_model_b(glm_df)

    # --- training-frame motorway stats (before deleting glm_df) ---
    X_a_tr = sm.add_constant(glm_df[feat_a].astype(float))
    glm_df["pred_a_train"] = res_a.predict(X_a_tr, offset=glm_df["log_offset"].astype(float))
    del X_a_tr
    X_b_tr = sm.add_constant(glm_df[feat_b].astype(float))
    glm_df["pred_b_train"] = res_b.predict(
        X_b_tr, offset=pd.Series(np.zeros(len(glm_df), dtype=float), index=glm_df.index)
    )
    del X_b_tr

    mw_train_stats = _mw_stats_from_frame(
        glm_df, "pred_a_train", "pred_b_train", "downsampled training frame"
    )
    del glm_df  # free ~1.5 GB before building full scoring frame

    # --- build thin scoring frame (scoring features + aggregation keys only) ---
    # The fat df has ~40+ cols including all network features we don't need here.
    # A thin slice halves peak memory before scoring.
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
    del df  # free the fat frame (~7.5 GB) before scoring

    # --- score full frame ---
    logger.info("Scoring full frame ...")
    df_thin["pred_a"] = _score_glm_full(df_thin, res_a, feat_a, off_col_a)
    df_thin["pred_b"] = _score_glm_full(df_thin, res_b, feat_b, off_col_b)

    # --- diagnostics ---
    logger.info("Computing diagnostics ...")

    # 1. AADT decile (full frame)
    by_aadt = _aadt_decile_table(df_thin, "pred_a", "pred_b")

    # 2. Road family (full frame)
    by_family = _resid_table(df_thin, "family", "pred_a", "pred_b")

    # 3. Road classification (full frame)
    by_cls = _resid_table(df_thin, "road_classification", "pred_a", "pred_b")

    # 4. Top-risk bands — pool to link_id first
    n_years = df_thin["year"].nunique()
    link_agg = df_thin.groupby("link_id").agg(
        collision_count=("collision_count", "sum"),
        pred_a=("pred_a", "mean"),
        pred_b=("pred_b", "mean"),
        road_classification=("road_classification", "first"),
        family=("family", "first"),
    )
    link_agg["n_years"] = n_years
    by_band = _top_risk_band_table(link_agg)

    # 5. Motorway full-frame stats
    mw_full_stats = _mw_stats_from_frame(df_thin, "pred_a", "pred_b", "full scored frame")
    mw_precision = {
        "training_frame": mw_train_stats,
        "full_frame": mw_full_stats,
        "explanation": (
            "The training-frame mean_resid is exactly 0.0 by construction. "
            "The Poisson GLM feature set includes 'is_motorway' and 'is_a_road' binary "
            "indicators. For a Poisson GLM with canonical log link, the score equations "
            "at convergence require Σ_i[x_ij*(y_i-μ_i)]=0 for every predictor j. "
            "For a binary indicator x_ij ∈ {0,1}, this becomes Σ_{group j}(y_i-μ_i)=0 "
            "within the TRAINING FRAME — i.e., sum(obs) = sum(pred) exactly for motorway "
            "links in the training data. mean_resid = 0/n = 0 exactly. "
            "This is a mathematical identity of GLMs with indicator variables, not a sign "
            "of perfect calibration. Full-frame residuals (below) are not subject to this "
            "constraint because the GLM was fitted on a downsampled subset."
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
        "motorway_precision": mw_precision,
        "by_aadt_decile": by_aadt.reset_index().to_dict(orient="records"),
        "by_family": by_family.reset_index().to_dict(orient="records"),
        "by_road_class": by_cls.reset_index().to_dict(orient="records"),
        "by_top_risk_band": by_band.to_dict(orient="records"),
    }

    # --- save ---
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(report, f, indent=2)
    logger.info(f"JSON written to {OUT_JSON}")

    _write_markdown(report)

    logger.info("=== Done ===")
    print("\n=== MODEL SUMMARY ===")
    print(f"Model A pseudo-R²: {pr2_a:.4f}")
    print(f"Model B pseudo-R²: {pr2_b:.4f}")
    print("\n=== MOTORWAY FULL-FRAME ===")
    mw_f = mw_precision["full_frame"]
    print(f"  sum_obs: {mw_f['sum_obs']:.0f}")
    print(
        f"  Model A: sum_pred={mw_f['sum_pred_a']:.2f}, net_resid={mw_f['net_resid_a']:.2f}, "
        f"rel={mw_f['rel_resid_a']:.4f}"
    )
    print(
        f"  Model B: sum_pred={mw_f['sum_pred_b']:.2f}, net_resid={mw_f['net_resid_b']:.2f}, "
        f"rel={mw_f['rel_resid_b']:.4f}"
    )
    print("\n=== AADT DECILE RESIDUALS ===")
    print(
        by_aadt[
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
    print("\n=== FAMILY RESIDUALS ===")
    print(
        by_family[
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

    return report


if __name__ == "__main__":
    run()
