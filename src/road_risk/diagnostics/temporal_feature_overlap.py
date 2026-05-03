"""
Temporal feature-overlap diagnostic.

This is the Step 3 prep check for the temporal plan. It asks whether
`core_overnight_ratio` is mostly recoverable from the existing post-grade
Stage 2 feature surface before adding temporal descriptors to the collision
model. If so, temporal ablation needs a higher bar because apparent lift may
be urban-character signal already represented by IMD, grade, road class,
centrality, population density, speed, lanes, AADT, and vehicle mix.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from road_risk.config import _ROOT
from road_risk.model.constants import FORM_OF_WAY_ORDINAL, RANDOM_STATE, ROAD_CLASS_ORDINAL

logger = logging.getLogger(__name__)

TIMEZONE_PROFILES = _ROOT / "data/models/timezone_profiles.parquet"
RISK_SCORES = _ROOT / "data/models/risk_scores.parquet"
NET_FEATURES = _ROOT / "data/features/network_features.parquet"
OPENROADS = _ROOT / "data/processed/shapefiles/openroads.parquet"
COLLISION_METRICS = _ROOT / "data/models/collision_metrics.json"
RANK_STABILITY_PROVENANCE = _ROOT / "data/provenance/rank_stability_provenance.json"
SUPPORTING_DIR = _ROOT / "reports/supporting"

SUMMARY_OUT = SUPPORTING_DIR / "temporal_feature_overlap_summary.csv"
CORRELATION_OUT = SUPPORTING_DIR / "temporal_feature_overlap_correlations.csv"
NOISE_FLOOR_AUDIT_OUT = SUPPORTING_DIR / "temporal_noise_floor_artifact_audit.csv"

SAMPLE_ROWS = 300_000


def _load_link_level_temporal() -> pd.DataFrame:
    tz = pd.read_parquet(
        TIMEZONE_PROFILES,
        columns=["link_id", "core_overnight_ratio", "hgv_core_daytime_frac"],
    )
    return (
        tz.groupby("link_id", observed=True)
        .agg(
            core_overnight_ratio=("core_overnight_ratio", "mean"),
            hgv_core_daytime_frac=("hgv_core_daytime_frac", "mean"),
        )
        .reset_index()
    )


def _build_feature_frame() -> pd.DataFrame:
    temporal = _load_link_level_temporal()
    risk = pd.read_parquet(
        RISK_SCORES,
        columns=[
            "link_id",
            "estimated_aadt",
            "road_classification",
            "hgv_proportion",
            "speed_limit_mph_effective",
            "betweenness_relative",
        ],
    )
    net_cols = [
        "link_id",
        "degree_mean",
        "betweenness",
        "dist_to_major_km",
        "pop_density_per_km2",
        "ruc_urban_rural",
        "imd_decile",
        "imd_crime_decile",
        "imd_living_indoor_decile",
        "lanes",
        "is_unpaved",
        "mean_grade",
    ]
    net = pd.read_parquet(NET_FEATURES, columns=[c for c in net_cols if c != ""])
    openroads = pd.read_parquet(
        OPENROADS,
        columns=[
            "link_id",
            "form_of_way",
            "road_function",
            "is_trunk",
            "is_primary",
            "link_length_km",
        ],
    )

    df = temporal.merge(risk, on="link_id", how="left")
    df = df.merge(net, on="link_id", how="left")
    df = df.merge(openroads, on="link_id", how="left")
    df = df.replace([np.inf, -np.inf], np.nan)

    df["road_class_ord"] = df["road_classification"].map(ROAD_CLASS_ORDINAL).fillna(0)
    df["form_of_way_ord"] = df["form_of_way"].map(FORM_OF_WAY_ORDINAL).fillna(1)
    df["is_motorway"] = (df["road_classification"] == "Motorway").astype("int8")
    df["is_a_road"] = (df["road_classification"] == "A Road").astype("int8")
    df["is_slip_road"] = (df["form_of_way"] == "Slip Road").astype("int8")
    df["is_roundabout"] = (df["form_of_way"] == "Roundabout").astype("int8")
    df["is_dual"] = (
        df["form_of_way"].isin(["Dual Carriageway", "Collapsed Dual Carriageway"])
    ).astype("int8")
    df["is_trunk"] = df["is_trunk"].fillna(False).astype("int8")
    df["is_primary"] = df["is_primary"].fillna(False).astype("int8")
    df["log_link_length"] = np.log(df["link_length_km"].clip(lower=0.001))
    df["log_estimated_aadt"] = np.log1p(df["estimated_aadt"])
    df["is_urban"] = (df["ruc_urban_rural"].fillna("") == "Urban").astype("int8")
    return df


def _feature_sets() -> dict[str, list[str]]:
    road_context = [
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
        "log_estimated_aadt",
        "hgv_proportion",
    ]
    post_grade = road_context + [
        "degree_mean",
        "betweenness",
        "betweenness_relative",
        "dist_to_major_km",
        "pop_density_per_km2",
        "speed_limit_mph_effective",
        "lanes",
        "is_unpaved",
        "imd_decile",
        "imd_crime_decile",
        "imd_living_indoor_decile",
        "mean_grade",
        "is_urban",
    ]
    urban_imd_grade = [
        "road_class_ord",
        "form_of_way_ord",
        "log_estimated_aadt",
        "pop_density_per_km2",
        "imd_decile",
        "imd_crime_decile",
        "imd_living_indoor_decile",
        "mean_grade",
        "is_urban",
    ]
    return {
        "road_context": road_context,
        "urban_imd_grade": urban_imd_grade,
        "post_grade_stage2_feature_surface": post_grade,
    }


def _fit_overlap_model(df: pd.DataFrame, feature_cols: list[str]) -> dict[str, Any]:
    model_df = df[["core_overnight_ratio"] + feature_cols].dropna(subset=["core_overnight_ratio"])
    if len(model_df) > SAMPLE_ROWS:
        model_df = model_df.sample(SAMPLE_ROWS, random_state=RANDOM_STATE)

    x = model_df[feature_cols].astype("float32")
    y = model_df["core_overnight_ratio"].astype("float32")
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=RANDOM_STATE
    )
    model = HistGradientBoostingRegressor(
        max_iter=200,
        learning_rate=0.05,
        l2_regularization=0.01,
        random_state=RANDOM_STATE,
    )
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    return {
        "n_rows": int(len(model_df)),
        "n_features": int(len(feature_cols)),
        "r2": float(r2_score(y_test, pred)),
        "mae": float(mean_absolute_error(y_test, pred)),
        "target_mean": float(y_test.mean()),
        "target_std": float(y_test.std()),
    }


def _correlations(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in columns:
        pair = df[[col, "core_overnight_ratio"]].dropna()
        if len(pair) < 100 or pair[col].nunique(dropna=True) < 2:
            continue
        rho, p_val = spearmanr(pair[col], pair["core_overnight_ratio"])
        rows.append(
            {
                "feature": col,
                "spearman_rho": float(rho),
                "p_value": float(p_val),
                "n": int(len(pair)),
                "feature_missing_share": float(df[col].isna().mean()),
            }
        )
    corr = pd.DataFrame(rows)
    if corr.empty:
        return corr
    corr["abs_spearman_rho"] = corr["spearman_rho"].abs()
    return corr.sort_values("abs_spearman_rho", ascending=False)


def _audit_noise_floor_artifacts() -> pd.DataFrame:
    import json

    rows: list[dict[str, Any]] = []
    current_metrics = (
        json.loads(COLLISION_METRICS.read_text()) if COLLISION_METRICS.exists() else {}
    )
    rank_prov = (
        json.loads(RANK_STABILITY_PROVENANCE.read_text())
        if RANK_STABILITY_PROVENANCE.exists()
        else {}
    )

    current_glm_features = set(current_metrics.get("glm", {}).get("features", []))
    rank_glm_features = set(rank_prov.get("glm_features", []))
    rows.append(
        {
            "artifact": "rank_stability_provenance",
            "usable_for_post_grade_noise_floor": bool(
                current_glm_features
                and rank_glm_features
                and current_glm_features == rank_glm_features
                and abs(
                    current_metrics.get("glm", {}).get("pseudo_r2", np.nan)
                    - rank_prov.get("glm_pseudo_r2", np.nan)
                )
                < 1e-9
            ),
            "current_glm_pseudo_r2": current_metrics.get("glm", {}).get("pseudo_r2"),
            "artifact_glm_pseudo_r2": rank_prov.get("glm_pseudo_r2"),
            "current_n_glm_features": len(current_glm_features),
            "artifact_n_glm_features": len(rank_glm_features),
            "reason": (
                "matches current post-grade GLM feature surface"
                if current_glm_features == rank_glm_features
                else "stale: GLM feature surface/pseudo-R2 differs from current post-grade model"
            ),
        }
    )
    return pd.DataFrame(rows)


def run_temporal_feature_overlap() -> dict[str, pd.DataFrame]:
    SUPPORTING_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Building link-level temporal feature overlap frame ...")
    df = _build_feature_frame()

    feature_sets = _feature_sets()
    summary_rows = []
    for label, features in feature_sets.items():
        present = [col for col in features if col in df.columns]
        metrics = _fit_overlap_model(df, present)
        metrics["feature_set"] = label
        summary_rows.append(metrics)
        logger.info("%s: R2=%.3f MAE=%.3f", label, metrics["r2"], metrics["mae"])

    summary = pd.DataFrame(summary_rows)[
        ["feature_set", "n_rows", "n_features", "r2", "mae", "target_mean", "target_std"]
    ]
    corr_cols = sorted(set().union(*feature_sets.values()))
    correlations = _correlations(df, [col for col in corr_cols if col in df.columns])
    audit = _audit_noise_floor_artifacts()

    summary.to_csv(SUMMARY_OUT, index=False)
    correlations.to_csv(CORRELATION_OUT, index=False)
    audit.to_csv(NOISE_FLOOR_AUDIT_OUT, index=False)
    logger.info("Wrote %s", SUMMARY_OUT)
    logger.info("Wrote %s", CORRELATION_OUT)
    logger.info("Wrote %s", NOISE_FLOOR_AUDIT_OUT)
    return {"summary": summary, "correlations": correlations, "noise_floor_audit": audit}


def _format_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in df.iterrows():
        cells = []
        for value in row:
            if isinstance(value, (float, np.floating)):
                cells.append(f"{value:.4f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    outputs = run_temporal_feature_overlap()
    print("\nOverlap model summary:")
    print(_format_table(outputs["summary"]))
    print("\nTop Spearman correlations:")
    print(_format_table(outputs["correlations"].head(12)))
    print("\nNoise-floor artifact audit:")
    print(_format_table(outputs["noise_floor_audit"]))


if __name__ == "__main__":
    main()
