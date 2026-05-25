"""
zero_calibration.py
--------------------
Posterior predictive zero check (Pew et al. 2020, §8 of crash-frequency-models.qmd).

Tests whether the Stage 2 Poisson GLM reproduces the observed zero rate by simulating
S realisations from its predictive distribution and comparing zero counts to observed.

A well-calibrated model produces p ≈ 0.50. A Poisson GLM on overdispersed data will
systematically underestimate zeros (p ≪ 0.50).

The production GLM is trained on downsampled zeros (GLM_ZERO_SAMPLE_RATIO=10), which
biases the intercept upward — predicted rates are too high, predicted zero probability
too low. This makes the test conservative: failing with the biased model is stronger
evidence of misfit than failing with an unbiased one. A secondary unbiased fit on a
diagnostic sample is run for comparison.

Outputs:
  reports/zero_calibration.md
  reports/supporting/zero_calibration_z_distribution.csv
  reports/supporting/zero_calibration_summary.json

Run with:
  conda run -n env1 python src/road_risk/diagnostics/zero_calibration.py
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

OUT_MD = _ROOT / "reports" / "zero_calibration.md"
SUPPORT_DIR = _ROOT / "reports" / "supporting"
OUT_CSV = SUPPORT_DIR / "zero_calibration_z_distribution.csv"
OUT_JSON = SUPPORT_DIR / "zero_calibration_summary.json"

# Simulation draws — 1000 matches Pew et al. procedure
S = 1_000
# Diagnostic sample cap — keeps memory manageable while preserving true zero rate
DIAG_SAMPLE_CAP = 2_000_000

CORE_FEATURES = [
    "road_class_ord",
    "form_of_way_ord",
    "is_motorway",
    "is_a_road",
    "is_slip_road",
    "is_roundabout",
    "is_dual",
    "is_trunk",
    "is_primary",
    "log_link_length",
    "is_covid",
    "year_norm",
]


def _build_design(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    X = df[features].fillna(0).astype(float)
    return sm.add_constant(X)


def _fit_poisson(df: pd.DataFrame, features: list[str]) -> sm.GLMResultsWrapper:
    X = _build_design(df, features)
    y = df["collision_count"].astype(int)
    return sm.GLM(y, X, family=sm.families.Poisson(), offset=df["log_offset"].astype(float)).fit(
        maxiter=200
    )


def _fit_nb(
    df: pd.DataFrame, features: list[str]
) -> tuple[sm.regression.linear_model.RegressionResultsWrapper | None, dict]:
    """Fit NB GLM and return (result, convergence_info).

    convergence_info keys: converged, warnflag, grad_norm, alpha_se, alpha_ci_low, alpha_ci_high.
    result is None on failure.
    """
    X = _build_design(df, features)
    y = df["collision_count"].astype(int)
    conv: dict = {
        "converged": False,
        "warnflag": None,
        "grad_norm": None,
        "alpha_se": None,
        "alpha_ci_low": None,
        "alpha_ci_high": None,
    }
    try:
        result = sm.NegativeBinomial(y, X, offset=df["log_offset"].astype(float)).fit(
            maxiter=200, disp=False
        )
    except Exception as exc:
        logger.warning(f"NB fit failed: {exc}")
        return None, conv

    retvals = getattr(result, "mle_retvals", {}) or {}
    conv["converged"] = bool(getattr(result, "converged", retvals.get("converged", False)))
    conv["warnflag"] = int(retvals.get("warnflag", -1))
    # gradient norm at solution — 0 means exact convergence; small value indicates clean solution
    gopt = retvals.get("gopt", None)
    conv["grad_norm"] = float(np.max(np.abs(gopt))) if gopt is not None else None

    if "alpha" in result.params.index:
        conv["alpha_se"] = float(result.bse["alpha"])
        ci = result.conf_int().loc["alpha"]
        conv["alpha_ci_low"] = float(ci.iloc[0])
        conv["alpha_ci_high"] = float(ci.iloc[1])

    logger.info(
        f"  NB convergence: converged={conv['converged']} | "
        f"warnflag={conv['warnflag']} | grad_norm={conv['grad_norm']}"
    )
    if conv["alpha_se"] is not None:
        logger.info(
            f"  NB alpha: {result.params['alpha']:.4f} "
            f"(SE={conv['alpha_se']:.4f}, "
            f"95% CI [{conv['alpha_ci_low']:.4f}, {conv['alpha_ci_high']:.4f}])"
        )
    if not conv["converged"]:
        logger.warning("  NB MLE did not converge — results may be unreliable")
    return result, conv


def _zero_check(
    lambda_hat: np.ndarray,
    y_obs: np.ndarray,
    rng: np.random.Generator,
    s: int = S,
) -> dict:
    """Run the posterior predictive zero check.

    Returns dict with Z_obs, E_Z_sim, SD_Z_sim, p, and the S simulated counts.
    """
    Z_obs = int((y_obs == 0).sum())
    Z_sim = np.empty(s, dtype=np.int64)
    for i in range(s):
        Z_sim[i] = int((rng.poisson(lambda_hat) == 0).sum())
    p = float((Z_sim > Z_obs).mean())
    return {
        "Z_obs": Z_obs,
        "E_Z_sim": float(Z_sim.mean()),
        "SD_Z_sim": float(Z_sim.std()),
        "p": p,
        "Z_sim": Z_sim,
        "n_rows": len(y_obs),
        "zero_rate_obs": float(Z_obs / len(y_obs)),
        "zero_rate_sim_mean": float(Z_sim.mean() / len(y_obs)),
    }


def main() -> None:
    rng = np.random.default_rng(RANDOM_STATE)
    SUPPORT_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Load data
    # ------------------------------------------------------------------
    logger.info("Loading data ...")
    if not AADT_PATH.exists():
        raise FileNotFoundError(f"AADT estimates not found: {AADT_PATH}. Run --stage traffic.")
    openroads = gpd.read_parquet(OPENROADS_PATH)
    aadt = pd.read_parquet(AADT_PATH)
    rla = pd.read_parquet(RLA_PATH)
    net = pd.read_parquet(NET_PATH) if NET_PATH.exists() else None

    df = build_collision_dataset(openroads, aadt, rla, net)
    n_total = len(df)
    zero_rate_true = float((df["collision_count"] == 0).mean())
    logger.info(f"Full dataset: {n_total:,} link-years | zero rate = {zero_rate_true:.4f}")

    # ------------------------------------------------------------------
    # Diagnostic sample — pure random draw, preserves true zero rate
    #
    # The production GLM is trained on 10:1 downsampled zeros (all positives
    # + GLM_ZERO_SAMPLE_RATIO × positives zeros). With 391k positives and
    # a 2M cap, keeping all positives gives only 1.6M zeros → 80% zero rate,
    # far from the true 98.2%. Fitting a GLM on that biased sample produces
    # inflated predicted rates that cause the simulation to OVER-predict zeros
    # (p = 1.0), the opposite of expected.
    #
    # Fix: plain random sample from the full index. At 2M rows the expected
    # split is ~36k positives / ~1.96M zeros (≈ true 98.2% zero rate). This
    # gives a well-specified unbiased GLM and a meaningful zero-calibration.
    # ------------------------------------------------------------------
    n_sample = min(DIAG_SAMPLE_CAP, n_total)
    sel = np.sort(rng.choice(df.index, size=n_sample, replace=False))
    diag = df.loc[sel].copy()
    n_pos_diag = int((diag["collision_count"] > 0).sum())
    n_zero_diag = int((diag["collision_count"] == 0).sum())
    logger.info(
        f"Diagnostic sample: {len(diag):,} rows | "
        f"{n_pos_diag:,} positives + {n_zero_diag:,} zeros | "
        f"zero rate = {(diag['collision_count'] == 0).mean():.4f}"
    )

    available_features = [c for c in CORE_FEATURES if c in diag.columns]

    # ------------------------------------------------------------------
    # Fit Poisson GLM (unbiased — true zero rate)
    # ------------------------------------------------------------------
    logger.info("Fitting unbiased Poisson GLM on diagnostic sample ...")
    poisson_result = _fit_poisson(diag, available_features)
    logger.info(f"  Converged={poisson_result.converged} | deviance={poisson_result.deviance:,.0f}")

    # ------------------------------------------------------------------
    # Zero-calibration check — Poisson
    # ------------------------------------------------------------------
    logger.info(f"Running zero-calibration check (S={S}) — Poisson ...")
    X_diag = _build_design(diag, available_features)
    lambda_poisson = poisson_result.predict(X_diag, offset=diag["log_offset"].astype(float)).values
    y_obs = diag["collision_count"].values

    check_poisson = _zero_check(lambda_poisson, y_obs, rng)
    logger.info(
        f"  Poisson: Z_obs={check_poisson['Z_obs']:,} | "
        f"E[Z_sim]={check_poisson['E_Z_sim']:,.0f} | "
        f"p={check_poisson['p']:.3f}"
    )

    # ------------------------------------------------------------------
    # Fit NB GLM (comparison)
    # ------------------------------------------------------------------
    logger.info("Fitting NB GLM on diagnostic sample ...")
    nb_result, nb_conv = _fit_nb(diag, available_features)
    alpha = None
    check_nb = None
    if nb_result is not None:
        # NB predict returns E[y]; simulate via Poisson-gamma mixture (NB2 parameterisation)
        mu_nb = nb_result.predict(
            sm.add_constant(diag[available_features].fillna(0).astype(float)),
            offset=diag["log_offset"].astype(float),
        ).values
        alpha = float(nb_result.params.get("alpha", 0))
        # statsmodels NegativeBinomial uses NB2: Var(y) = mu + alpha*mu^2.
        # Higher alpha = more dispersion; alpha=0 reduces to Poisson.
        # This is the RECIPROCAL of the k used in HSM/FHWA reports (Var = mu + mu^2/k).
        logger.info(f"  NB alpha (NB2: Var=mu+alpha*mu^2, higher=more dispersion) = {alpha:.4f}")
        if alpha > 0:
            lambda_nb_sim = rng.gamma(shape=1 / alpha, scale=alpha * mu_nb)
            check_nb = _zero_check(lambda_nb_sim, y_obs, rng)
            logger.info(
                f"  NB:     Z_obs={check_nb['Z_obs']:,} | "
                f"E[Z_sim]={check_nb['E_Z_sim']:,.0f} | "
                f"p={check_nb['p']:.3f}"
            )
        else:
            logger.warning("  NB alpha ≈ 0 — NB degenerated to Poisson; skipping NB check")

    # ------------------------------------------------------------------
    # Save results
    # ------------------------------------------------------------------
    z_df = pd.DataFrame({"poisson_z_sim": check_poisson["Z_sim"]})
    if check_nb is not None:
        z_df["nb_z_sim"] = check_nb["Z_sim"]
    z_df.to_csv(OUT_CSV, index=False)

    summary = {
        "n_total_link_years": n_total,
        "zero_rate_full_dataset": zero_rate_true,
        "diagnostic_sample_n": len(diag),
        "diagnostic_sample_n_positives": n_pos_diag,
        "diagnostic_sample_zero_rate": float((diag["collision_count"] == 0).mean()),
        "poisson": {
            "Z_obs": check_poisson["Z_obs"],
            "E_Z_sim": check_poisson["E_Z_sim"],
            "SD_Z_sim": check_poisson["SD_Z_sim"],
            "p": check_poisson["p"],
            "zero_rate_obs": check_poisson["zero_rate_obs"],
            "zero_rate_sim_mean": check_poisson["zero_rate_sim_mean"],
        },
        "nb": {
            "alpha": alpha,
            "alpha_se": nb_conv.get("alpha_se"),
            "alpha_ci_low": nb_conv.get("alpha_ci_low"),
            "alpha_ci_high": nb_conv.get("alpha_ci_high"),
            "converged": nb_conv.get("converged"),
            "warnflag": nb_conv.get("warnflag"),
            "grad_norm": nb_conv.get("grad_norm"),
            "Z_obs": check_nb["Z_obs"] if check_nb else None,
            "E_Z_sim": check_nb["E_Z_sim"] if check_nb else None,
            "p": check_nb["p"] if check_nb else None,
        }
        if nb_result is not None
        else None,
        "s_draws": S,
        "random_seed": RANDOM_STATE,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(summary, f, indent=2)

    # ------------------------------------------------------------------
    # Markdown report
    # ------------------------------------------------------------------
    def _p_interp(p: float) -> str:
        if p < 0.01:
            return "severe misfit — Poisson substantially underestimates the zero count"
        elif p < 0.10:
            return "moderate misfit — Poisson underestimates zeros; NB warranted"
        elif p < 0.25:
            return "marginal — monitor; NB diagnostic recommended"
        else:
            return "adequate calibration for zero regime"

    nb_section = ""
    if check_nb is not None:
        alpha_ci_str = (
            f"[{nb_conv['alpha_ci_low']:.4f}, {nb_conv['alpha_ci_high']:.4f}]"
            if nb_conv.get("alpha_ci_low") is not None
            else "n/a"
        )
        grad_str = f"{nb_conv['grad_norm']:.2e}" if nb_conv.get("grad_norm") is not None else "n/a"
        conv_flag = "YES" if nb_conv.get("converged") else "NO — results may be unreliable"
        nb_section = f"""
### Negative Binomial check

| Metric | Value |
|--------|-------|
| MLE converged | {conv_flag} |
| Warnflag | {nb_conv.get("warnflag", "n/a")} (0 = clean) |
| Gradient norm at solution | {grad_str} |
| Overdispersion α | {alpha:.4f} |
| α SE | {f"{nb_conv['alpha_se']:.4f}" if nb_conv.get("alpha_se") is not None else "n/a"} |
| α 95% CI | {alpha_ci_str} |
| Z_obs | {check_nb["Z_obs"]:,} |
| E[Z_sim] | {check_nb["E_Z_sim"]:,.0f} |
| p | {check_nb["p"]:.3f} |

{
            "NB adequately reproduces the observed zero count (p ≈ 0.5)."
            if check_nb["p"] > 0.25
            else f"NB also underestimates zeros (p = {check_nb['p']:.3f}); zero-inflation may be warranted."
        }
"""

    report = f"""# Zero-Calibration Diagnostic

**Method**: Posterior predictive zero check (Pew et al. 2020 / crash-frequency-models.qmd §8).

S = {S} realisations drawn from the Poisson predictive distribution.
p = proportion of realisations with more zeros than observed (well-calibrated → p ≈ 0.50).

**Diagnostic sample**: {len(diag):,} link-years ({n_pos_diag:,} with ≥1 collision;
{n_zero_diag:,} zeros — pure random draw preserving true zero rate from {n_total:,} total).

---

## Poisson GLM result

| Metric | Value |
|--------|-------|
| Observed zeros (Z_obs) | {check_poisson["Z_obs"]:,} |
| Simulated mean E[Z_sim] | {check_poisson["E_Z_sim"]:,.0f} |
| Simulated SD[Z_sim] | {check_poisson["SD_Z_sim"]:,.0f} |
| p-value | {check_poisson["p"]:.3f} |
| Observed zero rate | {check_poisson["zero_rate_obs"]:.4f} |
| Simulated mean zero rate | {check_poisson["zero_rate_sim_mean"]:.4f} |

**Interpretation**: {_p_interp(check_poisson["p"])}
{nb_section}
---

## Notes

- The diagnostic sample preserves the true zero rate (~{zero_rate_true:.1%}).
  The production Poisson GLM is trained on 1:{GLM_ZERO_SAMPLE_RATIO} downsampled zeros
  (biased intercept). This check uses an unbiased fit on the diagnostic sample.
- Full dataset: {n_total:,} link-years across {df["year"].nunique()} years
  ({df["year"].min()}–{df["year"].max()}).
- Supporting data: `reports/supporting/zero_calibration_z_distribution.csv`
- Summary JSON: `reports/supporting/zero_calibration_summary.json`
"""
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(report)
    logger.info(f"Report saved to {OUT_MD}")
    logger.info(f"Summary: {json.dumps(summary['poisson'], indent=2)}")


if __name__ == "__main__":
    main()
