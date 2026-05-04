"""
family_exposure_slope_heldout_diagnostics.py
--------------------------------------------
Held-out evaluation of family-specific exposure slope models vs global GLM variants.

Tests whether family-specific exposure slopes (AADT × family, length × family interactions)
improve held-out calibration versus global Model A and simple intercept-calibration variants.

Split:
  80 % train links / 20 % held-out links (by link_id, seed 42).
  All years for a link stay in the same split.
  GLM fitted on downsampled training link-years only.
  All diagnostics computed on the held-out link-year frame only.

Models compared:
  A      — Global Model A (full offset, STRUCTURAL + log_link_length). Raw.
  A_gcal — Model A + global intercept calibration (factor from training links).
  A_fcal — Model A + per-family intercept calibration (family factors from training links).
  M4     — Pooled interaction GLM (Model A offset + log_aadt×family + log_ll×family interactions).
  M5     — Per-family GLMs (one GLM per family, same offset). Optional; motorway overfit flagged.

Outputs:
  docs/internal/family_exposure_slope_heldout_diagnostics.json
  reports/family_exposure_slope_heldout_diagnostics.md

Run: conda run -n env1 python -m src.road_risk.diagnostics.family_exposure_slope_heldout_diagnostics
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
OUT_JSON = OUT_DIR / "family_exposure_slope_heldout_diagnostics.json"
OUT_MD = REPORTS_DIR / "family_exposure_slope_heldout_diagnostics.md"

TRAIN_FRAC = 0.80
SPLIT_SEED = 42
CHUNK = 1_000_000

FAMILIES = ["motorway", "trunk_a", "other_urban", "other_rural"]
FAMILY_ORDER = ["motorway", "trunk_a", "other_urban", "other_rural", "other"]

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

# Motorway held-out n is small (~8 k link-years).  Flag if train-side n too low.
MOTORWAY_MIN_TRAIN_ROWS = 2_000


# ---------------------------------------------------------------------------
# helpers shared with other diagnostics
# ---------------------------------------------------------------------------


def _assign_family(df: pd.DataFrame) -> pd.Series:
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


def _null_deviance_poisson(y: np.ndarray, offset: np.ndarray) -> float:
    y = np.asarray(y, dtype=float)
    offset = np.clip(np.asarray(offset, dtype=float), -50.0, 50.0)
    s, e = y.sum(), np.exp(offset).sum()
    if s <= 0 or e <= 0:
        return np.inf
    alpha = np.log(s / e)
    mu = np.exp(np.clip(alpha + offset, -50.0, 50.0))
    eps = 1e-300
    contrib = np.where(y > 0, y * np.log((y + eps) / (mu + eps)), 0.0) - (y - mu)
    return float(2.0 * contrib.sum())


def _pseudo_r2(result, y=None, offset=None) -> float:
    deviance = float(result.deviance)
    try:
        nd = float(result.null_deviance)
        if not np.isfinite(nd) or nd <= 0:
            raise ValueError
    except Exception:
        nd = _null_deviance_poisson(np.asarray(y), np.asarray(offset))
    return float(1.0 - deviance / nd)


def _poisson_deviance(y: np.ndarray, mu: np.ndarray) -> float:
    """Held-out Poisson deviance (2 × Σ [y log(y/μ) − (y−μ)])."""
    y = np.asarray(y, dtype=float)
    mu = np.clip(np.asarray(mu, dtype=float), 1e-300, None)
    eps = 1e-300
    contrib = np.where(y > 0, y * np.log((y + eps) / mu), 0.0) - (y - mu)
    return float(2.0 * contrib.sum())


def _downsample(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    pos_idx = df.index[df["collision_count"] > 0]
    zero_idx = df.index[df["collision_count"] == 0]
    n_keep = min(len(zero_idx), len(pos_idx) * GLM_ZERO_SAMPLE_RATIO)
    zero_sample = rng.choice(zero_idx, size=n_keep, replace=False)
    sel = np.sort(np.concatenate([pos_idx.values, zero_sample]))
    logger.info(f"  Downsampled: {len(pos_idx):,} pos + {n_keep:,} zeros = {len(sel):,} rows")
    return df.loc[sel].copy()


def _fit_glm(X, y, offset):
    return sm.GLM(y, X, family=sm.families.Poisson(), offset=offset).fit(maxiter=200)


def _score_chunked(df: pd.DataFrame, result, features: list, offset_col: str | None) -> np.ndarray:
    preds = np.empty(len(df), dtype="float32")
    for start in range(0, len(df), CHUNK):
        end = min(start + CHUNK, len(df))
        chunk = df.iloc[start:end]
        X_c = sm.add_constant(chunk[features].astype(float), has_constant="add")
        off_c = (
            chunk[offset_col].astype(float)
            if offset_col
            else pd.Series(np.zeros(end - start, dtype=float), index=chunk.index)
        )
        preds[start:end] = np.asarray(result.predict(X_c, offset=off_c), dtype="float32")
    return preds


# ---------------------------------------------------------------------------
# model fitting
# ---------------------------------------------------------------------------


def _fit_model_a(glm_df: pd.DataFrame):
    """Global Model A: full offset, STRUCTURAL + log_link_length."""
    feats = STRUCTURAL_COLS + ["log_link_length"]
    X = sm.add_constant(glm_df[feats].astype(float))
    y = glm_df["collision_count"].astype(int)
    off = glm_df["log_offset"].astype(float)
    res = _fit_glm(X, y, off)
    pr2 = _pseudo_r2(res, y=y, offset=off)
    logger.info(f"  Model A  pseudo-R²={pr2:.4f}  converged={res.converged}")
    return res, feats, "log_offset", pr2


def _fit_model_interaction(glm_df: pd.DataFrame):
    """
    Pooled interaction GLM (Model 4).
    Same offset as Model A.  Adds per-family deviations for log_aadt and log_link_length.
    Interaction columns: log_aadt_<fam> and log_ll_<fam> for each non-reference family.
    Reference family = 'other'.
    """
    # Build interaction columns in place on the training df copy.
    df = glm_df.copy()
    _add_interaction_cols(df)
    interaction_feats = _interaction_col_names()
    feats = STRUCTURAL_COLS + ["log_link_length"] + interaction_feats
    X = sm.add_constant(df[feats].astype(float))
    y = df["collision_count"].astype(int)
    off = df["log_offset"].astype(float)
    res = _fit_glm(X, y, off)
    pr2 = _pseudo_r2(res, y=y, offset=off)
    logger.info(f"  Model M4 pseudo-R²={pr2:.4f}  converged={res.converged}")
    return res, feats, "log_offset", pr2


def _fit_per_family_glms(glm_df: pd.DataFrame) -> dict:
    """
    Model 5: one GLM per family with same full offset.
    Returns dict keyed by family name.
    Motorway n is small — overfit risk flagged in output.
    """
    models = {}
    for fam in FAMILY_ORDER:
        sub = glm_df[glm_df["family"] == fam].copy()
        if len(sub) == 0:
            logger.warning(f"  M5: no training rows for family={fam}, skipping")
            continue
        # Drop zero-variance structural features within this family.
        feats_base = STRUCTURAL_COLS + ["log_link_length"]
        feats = [c for c in feats_base if sub[c].nunique() > 1]
        dropped = set(feats_base) - set(feats)
        if dropped:
            logger.info(f"  M5 [{fam}]: dropped constant features {dropped}")
        n_pos = (sub["collision_count"] > 0).sum()
        logger.info(f"  M5 [{fam}]: n={len(sub):,}  positives={n_pos:,}  features={len(feats)}")
        if fam == "motorway" and len(sub) < MOTORWAY_MIN_TRAIN_ROWS:
            logger.warning(f"  M5 [motorway]: only {len(sub):,} train rows — overfit risk HIGH")
        X = sm.add_constant(sub[feats].astype(float))
        y = sub["collision_count"].astype(int)
        off = sub["log_offset"].astype(float)
        res = _fit_glm(X, y, off)
        pr2 = _pseudo_r2(res, y=y, offset=off)
        logger.info(f"  M5 [{fam}]: pseudo-R²={pr2:.4f}  converged={res.converged}")
        models[fam] = {"result": res, "features": feats, "pr2": pr2}
    return models


def _interaction_col_names() -> list[str]:
    cols = []
    for fam in FAMILIES:  # "other" is reference, omitted
        tag = fam.replace("_", "")
        cols += [f"log_aadt_x_{tag}", f"log_ll_x_{tag}"]
    return cols


def _add_interaction_cols(df: pd.DataFrame) -> None:
    """Add log_aadt × family and log_link_length × family columns in-place."""
    for fam in FAMILIES:
        tag = fam.replace("_", "")
        mask = (df["family"] == fam).astype(float)
        df[f"log_aadt_x_{tag}"] = df["log_aadt"] * mask
        df[f"log_ll_x_{tag}"] = df["log_link_length"] * mask


# ---------------------------------------------------------------------------
# calibration
# ---------------------------------------------------------------------------


def _compute_cal_factors(df_train: pd.DataFrame, pred_col: str) -> tuple[float, dict]:
    """
    Estimate global and per-family intercept calibration factors from training links.
    Returns (global_factor, {family: factor}).
    """
    obs_total = df_train["collision_count"].sum()
    pred_total = df_train[pred_col].sum()
    global_factor = float(obs_total / pred_total)

    family_factors = {}
    for fam in FAMILY_ORDER:
        mask = df_train["family"] == fam
        obs_f = df_train.loc[mask, "collision_count"].sum()
        pred_f = df_train.loc[mask, pred_col].sum()
        family_factors[fam] = float(obs_f / pred_f) if pred_f > 0 else global_factor

    return global_factor, family_factors


def _apply_family_cal(
    pred_series: pd.Series, family_series: pd.Series, family_factors: dict, global_factor: float
) -> pd.Series:
    factors = family_series.map(family_factors).fillna(global_factor)
    return pred_series * factors


# ---------------------------------------------------------------------------
# diagnostic aggregation
# ---------------------------------------------------------------------------


def _resid_by_group(df: pd.DataFrame, group_col: str, pred_cols: list[str]) -> pd.DataFrame:
    """Residuals by group for multiple prediction columns."""
    agg_dict = {
        "n": ("collision_count", "count"),
        "sum_obs": ("collision_count", "sum"),
    }
    for c in pred_cols:
        agg_dict[f"sum_pred_{c}"] = (c, "sum")
    agg = df.groupby(group_col).agg(**agg_dict)
    for c in pred_cols:
        p = f"sum_pred_{c}"
        agg[f"rel_resid_{c}"] = (agg["sum_obs"] - agg[p]) / agg[p].replace(0, np.nan)
    return agg.round(6)


def _within_family_aadt_all(df: pd.DataFrame, pred_cols: list[str]) -> dict[str, list[dict]]:
    """
    Within-family AADT decile residuals for all prediction columns.
    AADT deciles are computed within each family independently.
    """
    results = {}
    for fam in FAMILY_ORDER:
        sub = df[df["family"] == fam].copy()
        if len(sub) == 0:
            continue
        sub["aadt_decile"] = pd.qcut(sub["estimated_aadt"], q=10, labels=False, duplicates="drop")
        agg_dict = {
            "n": ("collision_count", "count"),
            "aadt_p10": ("estimated_aadt", lambda x: x.quantile(0.1)),
            "aadt_mean": ("estimated_aadt", "mean"),
            "aadt_p90": ("estimated_aadt", lambda x: x.quantile(0.9)),
            "sum_obs": ("collision_count", "sum"),
        }
        for c in pred_cols:
            agg_dict[f"sum_pred_{c}"] = (c, "sum")
        agg = sub.groupby("aadt_decile").agg(**agg_dict)
        for c in pred_cols:
            p = f"sum_pred_{c}"
            agg[f"rel_resid_{c}"] = (agg["sum_obs"] - agg[p]) / agg[p].replace(0, np.nan)
        results[fam] = agg.round(6).reset_index().to_dict(orient="records")
    return results


def _top_risk_bands_common(
    df_link: pd.DataFrame, basis_rate_col: str, pred_total_cols: list[str]
) -> list[dict]:
    """
    Top-risk bands defined by Model A raw rate on held-out links.
    All prediction variants evaluated on the same link groups.
    """
    pct = df_link[basis_rate_col].rank(pct=True, method="average") * 100
    bands = pd.cut(
        pct,
        bins=[0, 80, 95, 99, 100],
        labels=["bottom_80pct", "5_to_20pct", "1_to_5pct", "top_1pct"],
        include_lowest=True,
    )
    tmp = df_link.copy()
    tmp["band"] = bands
    agg_dict = {
        "n_links": ("collision_count", "count"),
        "sum_obs": ("collision_count", "sum"),
    }
    for c in pred_total_cols:
        agg_dict[f"sum_pred_{c}"] = (c, "sum")
    agg = tmp.groupby("band", observed=False).agg(**agg_dict)
    for c in pred_total_cols:
        p = f"sum_pred_{c}"
        agg[f"rel_resid_{c}"] = (agg["sum_obs"] - agg[p]) / agg[p].replace(0, np.nan)
    return agg.reset_index().round(6).to_dict(orient="records")


# ---------------------------------------------------------------------------
# markdown writer
# ---------------------------------------------------------------------------


def _write_markdown(report: dict) -> None:
    meta = report["metadata"]
    cal = report["calibration_factors"]
    ms = report["model_summary"]
    by_fam = report["heldout_by_family"]
    wf = report["heldout_family_aadt_decile"]
    bands = report["heldout_top_risk_bands"]

    MODELS_LABEL = {
        "raw": "A raw",
        "gcal": "A gcal",
        "fcal": "A fcal",
        "m4": "M4 raw",
        "m4_gcal": "M4 gcal",
        "m4_fcal": "M4 fcal",
        "m5": "M5 raw",
    }
    pred_cols = [c for c in ["raw", "gcal", "fcal", "m4", "m5"] if c in ms]

    def _col_headers(extra=""):
        return " | ".join(f"{MODELS_LABEL[c]}" for c in pred_cols) + extra

    def _fam_table() -> str:
        lines = [
            "| Family | N | Obs | "
            + " | ".join(f"rel {MODELS_LABEL[c]}" for c in pred_cols)
            + " |",
            "|---|---:|---:|" + "|".join(["---:"] * len(pred_cols)) + "|",
        ]
        for r in by_fam:
            fam = r["family"]
            cells = [f"| {fam} | {int(r['n']):,} | {r['sum_obs']:,.0f}"]
            for c in pred_cols:
                cells.append(f"{r.get(f'rel_resid_{c}', float('nan')):+.4f}")
            lines.append(" | ".join(cells) + " |")
        return "\n".join(lines)

    def _band_table() -> str:
        lines = [
            "| Band | Links | Obs | "
            + " | ".join(f"rel {MODELS_LABEL[c]}" for c in pred_cols)
            + " |",
            "|---|---:|---:|" + "|".join(["---:"] * len(pred_cols)) + "|",
        ]
        for r in bands:
            cells = [f"| {r['band']} | {int(r['n_links']):,} | {r['sum_obs']:,.0f}"]
            for c in pred_cols:
                cells.append(f"{r.get(f'rel_resid_{c}', float('nan')):+.4f}")
            lines.append(" | ".join(cells) + " |")
        return "\n".join(lines)

    def _wf_section(fam: str, records: list[dict]) -> str:
        lines = [
            f"### {fam}\n",
            "| Decile | N | AADT p10 | AADT mean | AADT p90 | Obs | "
            + " | ".join(f"rel {MODELS_LABEL[c]}" for c in pred_cols)
            + " |",
            "|---|---:|---:|---:|---:|---:|" + "|".join(["---:"] * len(pred_cols)) + "|",
        ]
        for r in records:
            cells = [
                f"| {int(r['aadt_decile'])} | {int(r['n']):,} "
                f"| {r['aadt_p10']:,.0f} | {r['aadt_mean']:,.0f} | {r['aadt_p90']:,.0f} "
                f"| {r['sum_obs']:,.0f}"
            ]
            for c in pred_cols:
                cells.append(f"{r.get(f'rel_resid_{c}', float('nan')):+.4f}")
            lines.append(" | ".join(cells) + " |")
        return "\n".join(lines)

    def _model_summary_table() -> str:
        lines = [
            "| Model | Train pseudo-R² | Held-out deviance | Notes |",
            "|---|---:|---:|---|",
        ]
        for key, label in MODELS_LABEL.items():
            if key not in ms:
                continue
            m = ms[key]
            pr2 = f"{m.get('pseudo_r2_train', float('nan')):.4f}"
            dev = f"{m.get('deviance_heldout', float('nan')):.1f}"
            notes = m.get("notes", "")
            lines.append(f"| {label} | {pr2} | {dev} | {notes} |")
        return "\n".join(lines)

    def _cal_table() -> str:
        lines = [
            "| Family | Train obs | Train pred A raw | Cal factor | Log factor |",
            "|---|---:|---:|---:|---:|",
        ]
        for r in cal["per_family_detail"]:
            to = r["train_obs"]
            tp = r["train_pred_raw"]
            lines.append(
                f"| {r['family']} | {to:,.0f} | {tp:,.2f} "
                f"| {r['factor']:.4f} | {r['log_factor']:+.4f} |"
            )
        return "\n".join(lines)

    # Derive verdict
    def _verdict() -> str:
        m4_in = "m4" in ms
        m5_in = "m5" in ms

        def _range(key: str) -> float:
            """Max family-cal rel_resid range across families for a given model."""
            ranges = []
            for fam, records in wf.items():
                rels = [r.get(f"rel_resid_{key}", float("nan")) for r in records]
                rels = [r for r in rels if np.isfinite(r)]
                if rels:
                    ranges.append(max(rels) - min(rels))
            return max(ranges) if ranges else float("nan")

        fcal_range = _range("fcal")
        m4_range = _range("m4") if m4_in else float("nan")
        m5_range = _range("m5") if m5_in else float("nan")

        # Primary comparison: M4+fcal vs A+fcal (both calibrated, apples-to-apples).
        m4_fcal_in = "m4_fcal" in ms
        m4_fcal_range = _range("m4_fcal") if m4_fcal_in else float("nan")
        top1 = next((r for r in bands if r["band"] == "top_1pct"), None)
        m4_fcal_top1_ok = (
            top1 is not None
            and m4_fcal_in
            and abs(top1.get("rel_resid_m4_fcal", float("nan")))
            <= abs(top1.get("rel_resid_fcal", float("nan"))) * 1.05  # allow 5% slack
        )

        if m4_fcal_in and np.isfinite(m4_fcal_range) and m4_fcal_range < fcal_range * 0.85:
            if m4_fcal_top1_ok:
                return (
                    "**M4+fcal (pooled interaction GLM + per-family calibration) improves "
                    "held-out within-family AADT calibration vs A+fcal "
                    f"(max range: M4+fcal={m4_fcal_range:.3f} vs A+fcal={fcal_range:.3f}) "
                    "without materially worsening top-1% band calibration. "
                    "Recommend M4 as candidate v3 GLM formulation, to be combined with "
                    "per-family intercept calibration.**"
                )
            else:
                return (
                    "**M4+fcal improves held-out within-family AADT calibration "
                    f"(max range: M4+fcal={m4_fcal_range:.3f} vs A+fcal={fcal_range:.3f}) "
                    "but worsens top-1% band calibration. "
                    "Investigate top-risk-band shift before adopting M4.**"
                )
        elif m4_fcal_in and np.isfinite(m4_fcal_range):
            return (
                "**M4+fcal does not materially improve held-out within-family AADT calibration "
                f"vs A+fcal (max range: M4+fcal={m4_fcal_range:.3f} vs A+fcal={fcal_range:.3f}). "
                "Prefer A + per-family intercept calibration for simplicity.**"
            )
        else:
            return (
                "A + per-family intercept calibration is the best-performing held-out "
                "variant tested. M4 calibrated results not available."
            )

    wf_sections = "\n\n---\n\n".join(
        _wf_section(fam, records) for fam, records in wf.items() if records
    )

    md = f"""---
title: "Stage 2 GLM: Family exposure slope held-out diagnostics"
date: "2026-05-04"
---

**Status:** Complete (2026-05-04).
**Scope:** Held-out diagnostic only. No production models changed. No retraining.
**Split:** 80/20 by link_id (seed {SPLIT_SEED}). Train: {meta["n_train_links"]:,} links ({meta["n_train_link_years"]:,} link-years). Held-out: {meta["n_held_links"]:,} links ({meta["n_held_link_years"]:,} link-years).
**Note:** Intercept calibration factors (global and per-family) are estimated on training links only and applied to held-out links. No information leakage.

---

## 1. Why this diagnostic

Within-family AADT decile diagnostics showed that per-family intercept calibration alone
is insufficient: all families retain structured residual patterns across their own AADT
deciles. This diagnostic tests whether family-specific exposure slopes (AADT × family,
length × family interactions) close that gap on held-out data.

---

## 2. Model summary

{_model_summary_table()}

---

## 3. Intercept calibration factors (estimated on training links)

Global factor: {cal["global_factor"]:.4f} (log {np.log(cal["global_factor"]):+.4f}).

{_cal_table()}

---

## 4. Held-out residuals by family

{_fam_table()}

---

## 5. Held-out residuals by top-risk band (common Model A raw ranking)

Bands fixed by raw Model A held-out link-level predicted rate.
All models evaluated on the same link groups.

{_band_table()}

---

## 6. Held-out within-family AADT decile residuals

AADT deciles are within each family (decile 0 = lowest 10 % of AADT within that family).
This is the primary test of whether interaction slopes fix the residual bias seen in the
family intercept calibration diagnostics.

{wf_sections}

---

## 7. Verdict

{_verdict()}

### Decision rules applied
- M4 improves held-out within-family AADT calibration (max range < 85 % of family-cal
  range) AND does not worsen top-1% band → **Recommend M4 as candidate v3 GLM**.
- M4 improves within-family calibration but worsens top-1% → further investigation needed.
- M4 no better than family-cal → prefer intercept-only for simplicity.
- M5 improves train/full-frame but not held-out → **Reject (overfit)**. Motorway n is
  small enough (~{meta.get("n_train_motorway", "unknown"):,} train link-years) that
  per-family GLM risks learning noise rather than signal.

_Machine-readable: `docs/internal/family_exposure_slope_heldout_diagnostics.json`_
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_MD, "w") as f:
        f.write(md)
    logger.info(f"Markdown written to {OUT_MD}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def run() -> dict:
    logger.info("=== Family exposure slope held-out diagnostics ===")

    # --- load ---
    logger.info("Loading data ...")
    openroads = gpd.read_parquet(OPENROADS_PATH)
    road_fn_map = openroads[["link_id", "road_function"]].copy()

    rla = pd.read_parquet(RLA_PATH)
    aadt_estimates = pd.read_parquet(AADT_PATH)
    net_features = pd.read_parquet(NET_PATH) if NET_PATH.exists() else None

    df = build_collision_dataset(openroads, aadt_estimates, rla, net_features)
    del openroads

    # Compute feature columns.
    df["log_aadt"] = np.log(df["estimated_aadt"].clip(lower=1.0))
    df["log_offset"] = np.log(
        (df["estimated_aadt"] * df["link_length_km"] * 365.0 / 1e6).clip(lower=1e-6)
    )

    # Join road_function and assign family.
    df = df.merge(road_fn_map, on="link_id", how="left")
    del road_fn_map
    df["family"] = _assign_family(df)
    logger.info(f"  Family counts: {df['family'].value_counts().to_dict()}")

    # Required columns check.
    core_req = list(
        dict.fromkeys(
            STRUCTURAL_COLS
            + [
                "log_link_length",
                "log_aadt",
                "log_offset",
                "estimated_aadt",
                "collision_count",
                "family",
                "link_id",
                "year",
            ]
        )
    )
    missing = [c for c in core_req if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    full_idx = df.dropna(subset=core_req).index
    logger.info(f"  Rows after dropna: {len(full_idx):,}")

    # --- 80/20 link-level split ---
    all_links = df["link_id"].unique()
    rng_split = np.random.default_rng(SPLIT_SEED)
    rng_split.shuffle(all_links)
    n_train_links = int(len(all_links) * TRAIN_FRAC)
    train_links = set(all_links[:n_train_links])
    held_links = set(all_links[n_train_links:])

    is_train = df.loc[full_idx, "link_id"].isin(train_links)
    train_idx = full_idx[is_train.values]
    held_idx = full_idx[~is_train.values]

    logger.info(
        f"  Split: {len(train_links):,} train links ({len(train_idx):,} link-years) | "
        f"{len(held_links):,} held-out links ({len(held_idx):,} link-years)"
    )

    n_train_motorway = int((df.loc[train_idx, "family"] == "motorway").sum())
    logger.info(f"  Train motorway link-years: {n_train_motorway:,}")
    if n_train_motorway < MOTORWAY_MIN_TRAIN_ROWS:
        logger.warning(
            f"  Motorway train n={n_train_motorway:,} < {MOTORWAY_MIN_TRAIN_ROWS:,} — "
            "M5 motorway GLM overfit risk HIGH"
        )

    # --- build thin held-out scoring frame (keep only what we need) ---
    interaction_cols = _interaction_col_names()
    thin_cols = list(
        dict.fromkeys(
            STRUCTURAL_COLS
            + [
                "log_link_length",
                "log_aadt",
                "log_offset",
                "estimated_aadt",
                "collision_count",
                "family",
                "link_id",
                "year",
            ]
        )
    )
    thin_cols = [c for c in thin_cols if c in df.columns]

    df_held = df.loc[held_idx, thin_cols].copy()
    _add_interaction_cols(df_held)

    # For training, also keep interaction cols.
    df_train = df.loc[train_idx, thin_cols].copy()
    _add_interaction_cols(df_train)

    del df  # free fat frame

    # --- downsample training frame for GLM fitting ---
    rng_fit = np.random.default_rng(RANDOM_STATE)
    glm_df = _downsample(df_train, rng_fit)

    # --- fit models ---
    res_a, feats_a, off_a, pr2_a = _fit_model_a(glm_df)
    res_m4, feats_m4, off_m4, pr2_m4 = _fit_model_interaction(glm_df)
    m5_models = _fit_per_family_glms(glm_df)

    # --- score full training frame for calibration factor estimation ---
    logger.info("Scoring training frame for calibration factors ...")
    df_train["pred_a_train"] = _score_chunked(df_train, res_a, feats_a, off_a)
    df_train["pred_m4_train"] = _score_chunked(df_train, res_m4, feats_m4, off_m4)

    global_factor_a, fam_factors_a = _compute_cal_factors(df_train, "pred_a_train")
    global_factor_m4, fam_factors_m4 = _compute_cal_factors(df_train, "pred_m4_train")
    # Use Model A factors for A variants; M4 factors for M4 calibrated variants.
    global_factor = global_factor_a
    fam_factors = fam_factors_a
    logger.info(
        f"  A calibration:  global={global_factor_a:.4f}  "
        f"family={{{', '.join(f'{k}: {v:.4f}' for k, v in fam_factors_a.items())}}}"
    )
    logger.info(
        f"  M4 calibration: global={global_factor_m4:.4f}  "
        f"family={{{', '.join(f'{k}: {v:.4f}' for k, v in fam_factors_m4.items())}}}"
    )

    # Store per-family train obs/pred for the calibration table before deleting df_train.
    train_cal_detail = {}
    for fam in FAMILY_ORDER:
        mask = df_train["family"] == fam
        train_cal_detail[fam] = {
            "train_obs": float(df_train.loc[mask, "collision_count"].sum()),
            "train_pred_raw": float(df_train.loc[mask, "pred_a_train"].sum()),
        }
    del df_train

    # --- score held-out frame ---
    logger.info("Scoring held-out frame ...")
    df_held["pred_a_raw"] = _score_chunked(df_held, res_a, feats_a, off_a)
    df_held["pred_a_gcal"] = df_held["pred_a_raw"] * global_factor
    df_held["pred_a_fcal"] = _apply_family_cal(
        df_held["pred_a_raw"], df_held["family"], fam_factors, global_factor
    )
    df_held["pred_m4"] = _score_chunked(df_held, res_m4, feats_m4, off_m4)
    df_held["pred_m4_gcal"] = df_held["pred_m4"] * global_factor_m4
    df_held["pred_m4_fcal"] = _apply_family_cal(
        df_held["pred_m4"], df_held["family"], fam_factors_m4, global_factor_m4
    )

    # M5: score held-out by family using per-family model.
    df_held["pred_m5"] = np.nan
    for fam, m in m5_models.items():
        mask = df_held["family"] == fam
        if mask.sum() == 0:
            continue
        sub = df_held.loc[mask]
        df_held.loc[mask, "pred_m5"] = _score_chunked(sub, m["result"], m["features"], off_a)
    # Fill any missing m5 predictions (families not fitted) with family-cal fallback.
    missing_m5 = df_held["pred_m5"].isna()
    if missing_m5.any():
        df_held.loc[missing_m5, "pred_m5"] = df_held.loc[missing_m5, "pred_a_fcal"]

    # Held-out Poisson deviances.
    y_held = df_held["collision_count"].values
    dev = {}
    for label, col in [
        ("raw", "pred_a_raw"),
        ("gcal", "pred_a_gcal"),
        ("fcal", "pred_a_fcal"),
        ("m4", "pred_m4"),
        ("m4_gcal", "pred_m4_gcal"),
        ("m4_fcal", "pred_m4_fcal"),
        ("m5", "pred_m5"),
    ]:
        dev[label] = _poisson_deviance(y_held, df_held[col].values)

    # --- diagnostics on held-out frame ---
    logger.info("Computing held-out diagnostics ...")
    pred_cols = [
        "pred_a_raw",
        "pred_a_gcal",
        "pred_a_fcal",
        "pred_m4",
        "pred_m4_gcal",
        "pred_m4_fcal",
        "pred_m5",
    ]
    short_cols = ["raw", "gcal", "fcal", "m4", "m4_gcal", "m4_fcal", "m5"]

    # Rename pred columns to short names in a view copy for aggregation.
    df_d = df_held[
        ["family", "estimated_aadt", "collision_count", "link_id", "year"] + pred_cols
    ].copy()
    df_d.rename(columns=dict(zip(pred_cols, short_cols)), inplace=True)

    by_family = _resid_by_group(df_d, "family", short_cols)
    wf_decile = _within_family_aadt_all(df_d, short_cols)

    # Link-level aggregation for top-risk bands.
    link_agg_dict = {"collision_count": ("collision_count", "sum")}
    for c in short_cols:
        link_agg_dict[f"{c}_total"] = (c, "sum")
        link_agg_dict[f"{c}_rate"] = (c, "mean")
    link_agg = df_d.groupby("link_id").agg(**link_agg_dict)

    bands = _top_risk_bands_common(
        link_agg,
        basis_rate_col="raw_rate",
        pred_total_cols=[f"{c}_total" for c in short_cols],
    )
    # Rename sum_pred columns to match short names.
    bands_clean = []
    for r in bands:
        row = {"band": r["band"], "n_links": r["n_links"], "sum_obs": r["sum_obs"]}
        for c in short_cols:
            key = f"sum_pred_{c}_total"
            rr_key = f"rel_resid_{c}_total"
            row[f"rel_resid_{c}"] = r.get(rr_key, float("nan"))
        bands_clean.append(row)

    # --- bundle report ---
    cal_detail = [
        {
            "family": fam,
            "train_obs": round(train_cal_detail[fam]["train_obs"], 2),
            "train_pred_raw": round(train_cal_detail[fam]["train_pred_raw"], 2),
            "factor": round(fam_factors[fam], 6),
            "log_factor": round(float(np.log(fam_factors[fam])), 6),
        }
        for fam in FAMILY_ORDER
    ]

    model_summary = {
        "raw": {
            "pseudo_r2_train": round(pr2_a, 6),
            "deviance_heldout": round(dev["raw"], 2),
            "notes": "Global Model A, no calibration",
        },
        "gcal": {
            "pseudo_r2_train": round(pr2_a, 6),
            "deviance_heldout": round(dev["gcal"], 2),
            "notes": "Model A + global intercept cal (train links)",
        },
        "fcal": {
            "pseudo_r2_train": round(pr2_a, 6),
            "deviance_heldout": round(dev["fcal"], 2),
            "notes": "Model A + per-family intercept cal (train links)",
        },
        "m4": {
            "pseudo_r2_train": round(pr2_m4, 6),
            "deviance_heldout": round(dev["m4"], 2),
            "notes": "Pooled interaction GLM, no calibration",
        },
        "m4_gcal": {
            "pseudo_r2_train": round(pr2_m4, 6),
            "deviance_heldout": round(dev["m4_gcal"], 2),
            "notes": "M4 + global intercept cal (train links)",
        },
        "m4_fcal": {
            "pseudo_r2_train": round(pr2_m4, 6),
            "deviance_heldout": round(dev["m4_fcal"], 2),
            "notes": "M4 + per-family intercept cal (train links) — primary M4 comparison",
        },
        "m5": {
            "pseudo_r2_train": round(float(np.mean([m["pr2"] for m in m5_models.values()])), 6),
            "deviance_heldout": round(dev["m5"], 2),
            "notes": (f"Per-family GLMs, no calibration. Motorway train n={n_train_motorway:,}."),
        },
    }

    report = {
        "metadata": {
            "n_train_links": len(train_links),
            "n_held_links": len(held_links),
            "train_frac": TRAIN_FRAC,
            "split_seed": SPLIT_SEED,
            "n_train_link_years": len(train_idx),
            "n_held_link_years": len(held_idx),
            "n_train_motorway": n_train_motorway,
        },
        "calibration_factors": {
            "global_factor": round(global_factor, 6),
            "global_log_factor": round(float(np.log(global_factor)), 6),
            "per_family": {k: round(v, 6) for k, v in fam_factors.items()},
            "per_family_detail": cal_detail,
        },
        "model_summary": model_summary,
        "heldout_by_family": by_family.reset_index().to_dict(orient="records"),
        "heldout_family_aadt_decile": wf_decile,
        "heldout_top_risk_bands": bands_clean,
    }

    # --- save ---
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(report, f, indent=2)
    logger.info(f"JSON written to {OUT_JSON}")

    _write_markdown(report)

    # --- console summary ---
    print("\n=== HELD-OUT DEVIANCE ===")
    for k, v in dev.items():
        print(f"  {k:10s}  deviance={v:.1f}")

    print("\n=== HELD-OUT FAMILY RESIDUALS (A+fcal vs M4+fcal) ===")
    for fam in FAMILY_ORDER:
        row = by_family.loc[fam] if fam in by_family.index else None
        if row is None:
            continue
        print(
            f"  {fam:15s}  A+fcal={row.get('rel_resid_fcal', float('nan')):+.4f}  "
            f"M4+fcal={row.get('rel_resid_m4_fcal', float('nan')):+.4f}"
        )

    print("\n=== WITHIN-FAMILY AADT RANGE (A+fcal vs M4+fcal) ===")
    for fam in FAMILY_ORDER:
        if fam not in wf_decile:
            continue
        records = wf_decile[fam]
        for key, label in [("fcal", "A+fcal"), ("m4_fcal", "M4+fcal")]:
            rels = [r.get(f"rel_resid_{key}", float("nan")) for r in records]
            rels = [r for r in rels if np.isfinite(r)]
            rng = max(rels) - min(rels) if rels else float("nan")
            print(f"  {fam:15s}  {label:10s}  range={rng:.4f}")

    return report


if __name__ == "__main__":
    run()
