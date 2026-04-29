"""
family_split.py
---------------
Session 1: per-family XGBoost training and stitching for Stage 2.

Trains one XGBoost Poisson model per facility family:
  motorway | trunk_a | other_urban | other_rural

Produces data/models/risk_scores_family.parquet with both a global-stitched
ranking (risk_percentile_family) and a within-family ranking
(risk_percentile_within_family). Does not modify production
risk_scores.parquet or any existing model artefacts.

Family assignment uses:
  road_function, is_trunk  — from OS Open Roads (build_collision_dataset
                             extracts is_trunk but not road_function, so
                             road_function is joined here from openroads)
  ruc_urban_rural          — from data/features/network_features.parquet,
                             already present in the df returned by
                             build_collision_dataset when net_features is passed

Design doc: quarto/methodology/facility-family-split.qmd §5
"""

from __future__ import annotations

import hashlib
import json
import logging
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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
    train_collision_xgb,
)

logger = logging.getLogger(__name__)

SCRIPT_PATH = Path("src/road_risk/model/family_split.py")
PROVENANCE_PATH = _ROOT / "data/provenance/family_split_provenance.json"
OUT_PATH = MODELS / "risk_scores_family.parquet"
RISK_SCORES_PATH = MODELS / "risk_scores.parquet"

FAMILIES = ["motorway", "trunk_a", "other_urban", "other_rural"]

# Active-network family link counts from design doc §2 (road_link_annual.parquet
# distinct link_ids). Any family differing by more than _TOLERANCE halts the run.
_EXPECTED_ACTIVE_COUNTS: dict[str, int] = {
    "motorway": 2_279,
    "trunk_a": 5_465,
    "other_urban": 177_296,
    "other_rural": 48_564,
}
_FAMILY_COUNT_TOLERANCE = 0.01  # 1 %


# ── Family assignment ──────────────────────────────────────────────────────────


def assign_family(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'family' column.  Raises ValueError if any row cannot be assigned.

    Required columns: road_function (str), is_trunk (int/bool), ruc_urban_rural (str).

    Precedence (first matching condition wins):
      1. road_function == "Motorway"               → motorway
      2. road_function == "A Road"  &  is_trunk    → trunk_a
      3. ruc_urban_rural == "Urban"                → other_urban
      4. ruc_urban_rural == "Rural"                → other_rural
    """
    is_trunk_bool = df["is_trunk"].astype(bool)
    conditions = [
        df["road_function"] == "Motorway",
        (df["road_function"] == "A Road") & is_trunk_bool,
        df["ruc_urban_rural"] == "Urban",
        df["ruc_urban_rural"] == "Rural",
    ]
    family_arr = np.select(conditions, FAMILIES, default="")
    n_unknown = int((family_arr == "").sum())
    if n_unknown > 0:
        unknown_mask = family_arr == ""
        bad_cols = ["link_id", "road_function", "is_trunk", "ruc_urban_rural"]
        bad = df.loc[unknown_mask, bad_cols].head(10)
        raise ValueError(
            f"{n_unknown:,} rows could not be assigned to a facility family.\n"
            f"First examples:\n{bad.to_string()}"
        )
    df = df.copy()
    df["family"] = family_arr
    return df


def _verify_family_counts(active_family_counts: dict[str, int]) -> None:
    """Compare observed active-network family counts against design-doc §2."""
    for family, expected in _EXPECTED_ACTIVE_COUNTS.items():
        observed = active_family_counts.get(family, 0)
        delta = abs(observed - expected) / expected
        if delta > _FAMILY_COUNT_TOLERANCE:
            raise ValueError(
                f"Family '{family}' count mismatch: observed {observed:,}, "
                f"expected {expected:,} ({delta:.2%} > {_FAMILY_COUNT_TOLERANCE:.0%} "
                "tolerance). Data has changed since the design doc was written."
            )
    logger.info(
        "Family counts verified against design doc §2 (all within %.0f%% tolerance)",
        _FAMILY_COUNT_TOLERANCE * 100,
    )


# ── Per-family training ────────────────────────────────────────────────────────


def train_family_xgb(df: pd.DataFrame, family: str, seed: int = 42) -> tuple:
    """
    Filter df to family and delegate to train_collision_xgb unchanged.

    Returns (model, feature_list, metrics) exactly as train_collision_xgb does.
    Raises RuntimeError if the family has fewer than 50 unique link_ids —
    too few for a stable GroupShuffleSplit(test_size=0.2).
    """
    family_df = df[df["family"] == family].copy()
    n_links = int(family_df["link_id"].nunique())
    n_rows = len(family_df)
    logger.info("Training %s: %s links, %s link-year rows", family, f"{n_links:,}", f"{n_rows:,}")
    if n_links < 50:
        raise RuntimeError(
            f"Family '{family}' has only {n_links} unique link_ids — too few "
            "for a stable GroupShuffleSplit(test_size=0.2). Stopping as requested."
        )
    return train_collision_xgb(family_df, seed=seed)


# ── Scoring and pooling ────────────────────────────────────────────────────────


def score_family_xgb(
    df: pd.DataFrame,
    models_by_family: dict[str, tuple],
) -> pd.DataFrame:
    """
    Score every family's link-year rows with its per-family XGBoost model.

    models_by_family: {family: (model, feature_list, metrics)}

    Returns a pooled one-row-per-link DataFrame with predicted_xgb_family,
    family, collision_count, estimated_aadt, and optional count/audit columns.
    """
    parts: list[pd.DataFrame] = []
    for family, (model, feature_list, _metrics) in models_by_family.items():
        fam_df = df[df["family"] == family].copy()
        X = fam_df[feature_list].fillna(0).astype(float)
        offsets = fam_df["log_offset"].fillna(0).values.astype(float)
        fam_df["predicted_xgb_family"] = model.predict(X, base_margin=offsets)
        parts.append(fam_df)
        logger.info(
            "Scored %s: %s rows, mean predicted_xgb_family = %.5f",
            family,
            f"{len(fam_df):,}",
            float(fam_df["predicted_xgb_family"].mean()),
        )

    scored = pd.concat(parts, ignore_index=True)

    # Verify family constant per link_id before pooling
    multi = (scored.groupby("link_id")["family"].nunique() > 1).sum()
    if multi > 0:
        raise ValueError(
            f"{multi:,} link_ids appear in more than one family after scoring. "
            "Family assignment is not unique per link."
        )

    agg: dict[str, str] = {
        "collision_count": "sum",
        "estimated_aadt": "mean",
        "predicted_xgb_family": "mean",
        "family": "first",
    }
    for col in ("fatal_count", "serious_count"):
        if col in scored.columns:
            agg[col] = "sum"
    for col in ("ruc_imputed", "ruc_fill_method"):
        if col in scored.columns:
            agg[col] = "first"

    pooled = scored.groupby("link_id", sort=False).agg(agg).reset_index()
    logger.info("Pooled %s link-year rows → %s links", f"{len(scored):,}", f"{len(pooled):,}")
    return pooled


def compute_family_rankings(pooled: pd.DataFrame) -> pd.DataFrame:
    """
    Add risk_percentile_family (global stitched) and
    risk_percentile_within_family (per-family) columns.
    """
    pooled = pooled.copy()
    pooled["risk_percentile_family"] = (
        pooled["predicted_xgb_family"].rank(method="average", pct=True) * 100
    )
    pooled["risk_percentile_within_family"] = (
        pooled.groupby("family")["predicted_xgb_family"].rank(method="average", pct=True) * 100
    )
    return pooled


# ── Provenance helpers ─────────────────────────────────────────────────────────


def _read_fingerprint(path: Path) -> dict[str, Any]:
    stat = path.stat()
    df = pd.read_parquet(path)
    return {
        "path": str(path.relative_to(_ROOT)),
        "mtime_ns": stat.st_mtime_ns,
        "size_bytes": stat.st_size,
        "row_count": int(len(df)),
        "columns": list(df.columns),
    }


def _file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_sha() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=_ROOT, text=True).strip()
    except Exception:
        return None


def _write_provenance(payload: dict[str, Any]) -> None:
    PROVENANCE_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


# ── Main run ───────────────────────────────────────────────────────────────────


def run_family_split(seed: int = 42) -> dict[str, Any]:
    """
    Session 1 orchestration: family assignment → per-family training →
    stitched scoring → risk_scores_family.parquet.

    Does not modify production risk_scores.parquet or rank_stability files.
    Stops and raises on any verification failure.
    """
    PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)

    # Snapshot production file before any work
    production_before = _read_fingerprint(RISK_SCORES_PATH)
    expected_rows = production_before["row_count"]
    logger.info(
        "Production risk_scores.parquet: %s rows, mtime_ns=%s",
        f"{expected_rows:,}",
        production_before["mtime_ns"],
    )

    # ── Load inputs ───────────────────────────────────────────────────────────
    import geopandas as gpd

    t0 = time.time()
    logger.info("Loading input data ...")
    openroads = gpd.read_parquet(OPENROADS_PATH)
    rla = pd.read_parquet(RLA_PATH)
    net_features = pd.read_parquet(NET_PATH)
    aadt_estimates = pd.read_parquet(AADT_PATH)
    logger.info("Input data loaded in %.0f s", time.time() - t0)

    net_fp = {
        "path": str(NET_PATH.relative_to(_ROOT)),
        "mtime_ns": NET_PATH.stat().st_mtime_ns,
        "size_bytes": NET_PATH.stat().st_size,
        "row_count": int(len(net_features)),
    }
    rla_fp = {
        "path": str(RLA_PATH.relative_to(_ROOT)),
        "mtime_ns": RLA_PATH.stat().st_mtime_ns,
        "size_bytes": RLA_PATH.stat().st_size,
        "row_count": int(len(rla)),
    }

    # ── Build collision dataset ───────────────────────────────────────────────
    t1 = time.time()
    logger.info("Building collision dataset ...")
    df = build_collision_dataset(openroads, aadt_estimates, rla, net_features)
    logger.info("Collision dataset built in %.0f s: %s rows", time.time() - t1, f"{len(df):,}")

    # ── Join road_function and assign families ────────────────────────────────
    # build_collision_dataset extracts is_trunk but not road_function from openroads.
    # ruc_urban_rural is already in df via the net_features merge.
    if "road_function" not in df.columns:
        road_func = pd.DataFrame(openroads[["link_id", "road_function"]]).drop_duplicates("link_id")
        df = df.merge(road_func, on="link_id", how="left")

    n_missing_rf = int(df["road_function"].isna().sum())
    if n_missing_rf > 0:
        raise ValueError(
            f"{n_missing_rf:,} rows have no road_function after joining from openroads. "
            "Check that openroads.parquet covers all link_ids in the dataset."
        )

    df = assign_family(df)
    logger.info(
        "Families assigned:\n%s",
        df.groupby("family")["link_id"].nunique().sort_values(ascending=False).to_string(),
    )

    # ── Verify active-network family counts against design doc §2 ─────────────
    active_ids = set(rla["link_id"].unique())
    active_families = (
        df[df["link_id"].isin(active_ids)]
        .drop_duplicates("link_id")["family"]
        .value_counts()
        .to_dict()
    )
    logger.info("Active-network family counts: %s", active_families)
    _verify_family_counts(active_families)

    # ── Per-family training ───────────────────────────────────────────────────
    models_by_family: dict[str, tuple] = {}
    per_family_metrics: dict[str, dict[str, Any]] = {}

    for family in FAMILIES:
        t_fam = time.time()
        logger.info("=== Training family: %s ===", family)
        try:
            model, feature_list, metrics = train_family_xgb(df, family, seed=seed)
        except RuntimeError as exc:
            raise RuntimeError(f"Training halted for family '{family}': {exc}") from exc

        elapsed = round(time.time() - t_fam, 1)

        if metrics["pseudo_r2"] < 0:
            logger.warning(
                "Family '%s' pseudo-R2 = %.4f is negative — worse than a null model. "
                "Session 2 will diagnose; proceeding as instructed.",
                family,
                metrics["pseudo_r2"],
            )
        elif metrics["pseudo_r2"] < 0.3:
            logger.warning(
                "Family '%s' pseudo-R2 = %.4f is below 0.3. "
                "This may indicate overfitting on a small family. Session 2 will diagnose.",
                family,
                metrics["pseudo_r2"],
            )

        per_family_metrics[family] = {
            "n_train": int(metrics["n_train"]),
            "n_test": int(metrics["n_test"]),
            "pseudo_r2": float(metrics["pseudo_r2"]),
            "seed": int(seed),
            "features": list(feature_list),
            "training_time_s": elapsed,
        }
        models_by_family[family] = (model, feature_list, metrics)
        logger.info(
            "%s: n_train=%s  n_test=%s  pseudo_R2=%.4f  time=%.0f s",
            family,
            f"{metrics['n_train']:,}",
            f"{metrics['n_test']:,}",
            metrics["pseudo_r2"],
            elapsed,
        )

    # ── Score all families, pool, rank ────────────────────────────────────────
    t_score = time.time()
    logger.info("Scoring all families and pooling ...")
    pooled = score_family_xgb(df, models_by_family)
    pooled = compute_family_rankings(pooled)
    logger.info("Scoring + ranking done in %.0f s", time.time() - t_score)

    # ── Row-count guard ───────────────────────────────────────────────────────
    if len(pooled) != expected_rows:
        raise RuntimeError(
            f"Output row count {len(pooled):,} ≠ production "
            f"risk_scores.parquet row count {expected_rows:,}. "
            "Investigate before saving."
        )

    # ── Join production risk_percentile for side-by-side comparison ───────────
    prod_pct = pd.read_parquet(RISK_SCORES_PATH, columns=["link_id", "risk_percentile"])
    pooled = pooled.merge(prod_pct, on="link_id", how="left")
    n_missing_prod = int(pooled["risk_percentile"].isna().sum())
    if n_missing_prod > 0:
        logger.warning(
            "%s links in family output have no production risk_percentile "
            "(should be zero; these links are absent from risk_scores.parquet).",
            f"{n_missing_prod:,}",
        )

    # ── Column selection and ordering ─────────────────────────────────────────
    save_cols = [
        "link_id",
        "family",
        "collision_count",
        "fatal_count",
        "serious_count",
        "estimated_aadt",
        "predicted_xgb_family",
        "risk_percentile_family",
        "risk_percentile_within_family",
        "risk_percentile",
        "ruc_imputed",
        "ruc_fill_method",
    ]
    out_df = pooled[[c for c in save_cols if c in pooled.columns]]

    # ── Verification assertions ───────────────────────────────────────────────
    assert out_df["risk_percentile_family"].between(0, 100).all(), (
        "risk_percentile_family contains values outside [0, 100]"
    )
    assert out_df["risk_percentile_within_family"].between(0, 100).all(), (
        "risk_percentile_within_family contains values outside [0, 100]"
    )
    assert out_df["predicted_xgb_family"].notna().all(), "predicted_xgb_family contains NaN"
    assert (out_df["predicted_xgb_family"] >= 0).all(), (
        "predicted_xgb_family contains negative values"
    )
    assert out_df["family"].isin(FAMILIES).all(), "Unknown values in family column"

    # ── Save ──────────────────────────────────────────────────────────────────
    out_df.to_parquet(OUT_PATH, index=False)
    logger.info("Saved %s: %s rows", OUT_PATH, f"{len(out_df):,}")

    # ── Output fingerprint ────────────────────────────────────────────────────
    out_fp = {
        "path": str(OUT_PATH.relative_to(_ROOT)),
        "sha256": _file_hash(OUT_PATH),
        "mtime_ns": OUT_PATH.stat().st_mtime_ns,
        "size_bytes": OUT_PATH.stat().st_size,
        "row_count": int(len(out_df)),
    }

    # ── Verify production file unchanged ──────────────────────────────────────
    production_after = _read_fingerprint(RISK_SCORES_PATH)
    prod_unchanged = production_after["mtime_ns"] == production_before["mtime_ns"]
    if not prod_unchanged:
        raise RuntimeError(
            "Production risk_scores.parquet mtime changed during family split run. "
            "This should not happen — investigate immediately."
        )

    # ── Verify rank stability seed files not disturbed ────────────────────────
    rs_dir = MODELS / "rank_stability"
    rs_files: dict[str, bool] = {}
    if rs_dir.exists():
        for s in [42, 43, 44, 45, 46]:
            p = rs_dir / f"seed_{s}.parquet"
            rs_files[str(s)] = p.exists()

    # ── Output family link counts ─────────────────────────────────────────────
    output_family_counts = {
        k: int(v) for k, v in out_df.groupby("family")["link_id"].count().items()
    }

    # ── Provenance ────────────────────────────────────────────────────────────
    provenance: dict[str, Any] = {
        "script_path": str(SCRIPT_PATH),
        "git_sha": _git_sha(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "seed": int(seed),
        "n_jobs": 1,
        "families_trained": FAMILIES,
        "per_family_metrics": per_family_metrics,
        "active_network_family_counts": {k: int(v) for k, v in active_families.items()},
        "output_family_counts": output_family_counts,
        "feature_list": per_family_metrics[FAMILIES[0]]["features"],
        "input_fingerprints": {
            "network_features": net_fp,
            "road_link_annual": rla_fp,
        },
        "output_fingerprint": out_fp,
        "production_risk_scores_before": production_before,
        "production_risk_scores_unchanged": prod_unchanged,
        "rank_stability_seed_files_exist": rs_files,
        "missing_prod_risk_percentile_count": n_missing_prod,
    }
    _write_provenance(provenance)
    logger.info("Provenance written to %s", PROVENANCE_PATH)

    # ── Stdout summary ────────────────────────────────────────────────────────
    print("\n=== Family Split — Session 1 Summary ===")
    print(f"\nPer-family training (seed={seed}):")
    print(f"  {'family':<15} {'n_train':>10} {'n_test':>8} {'pseudo_R2':>10} {'time_s':>8}")
    print(f"  {'-' * 15} {'-' * 10} {'-' * 8} {'-' * 10} {'-' * 8}")
    for family in FAMILIES:
        m = per_family_metrics[family]
        print(
            f"  {family:<15} {m['n_train']:>10,} {m['n_test']:>8,} "
            f"{m['pseudo_r2']:>10.4f} {m['training_time_s']:>8.1f}"
        )

    print(f"\nFamily link counts in scored output ({len(out_df):,} total links):")
    for family, count in sorted(output_family_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {family:<15}: {count:>10,}")

    print(f"\nOutput: {OUT_PATH}")
    print(f"Production risk_scores.parquet unchanged: {prod_unchanged}")
    print()

    return provenance


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    run_family_split(seed=42)


if __name__ == "__main__":
    main()
