"""
Temporal feature ablation against the post-fix Stage 2 collision model.

Configurations:
  A. Baseline
  B. Baseline + core_overnight_ratio
  C. Baseline + core_overnight_ratio + WebTRIS HGV%

The runner retrains XGBoost across seeds 42-46 using the same held-out split
logic as rank_stability, records full and primary (leakage-excluded) metrics,
and compares B/C against the baseline under the pre-registered decision rule.
"""

from __future__ import annotations

import logging
from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

from road_risk.config import _ROOT
from road_risk.model.collision import (
    AADT_PATH,
    MODELS,
    NET_PATH,
    OPENROADS_PATH,
    RLA_PATH,
    TRAFFIC_FEATURES_PATH,
    build_collision_dataset,
    score_collision_models,
)
from road_risk.model.rank_stability import _load_existing_glm_and_features

logger = logging.getLogger(__name__)

SEEDS = [42, 43, 44, 45, 46]
OUTPUT_CSV = _ROOT / "reports/supporting/temporal_ablation_results.csv"
OUTPUT_MD = _ROOT / "reports/supporting/temporal_ablation_summary.md"
TIMEZONE_PROFILES = _ROOT / "data/models/timezone_profiles.parquet"
LEAKAGE_MAP = _ROOT / "reports/supporting/temporal_leakage_site_link_map.csv"
BASELINE_OUT_DIR = MODELS / "rank_stability"
ABLATION_OUT_DIR = MODELS / "rank_stability_temporal_ablation"

CONFIGS = {
    "A": {"extra_features": [], "label": "Baseline"},
    "B": {"extra_features": ["core_overnight_ratio"], "label": "Baseline + core_overnight_ratio"},
    "C": {
        "extra_features": ["core_overnight_ratio", "webtris_hgv_pct"],
        "label": "Baseline + core_overnight_ratio + WebTRIS HGV%",
    },
}

DECISION_RULE = """A new feature configuration earns adoption if BOTH:
- Pseudo-R² improvement > 0.009 over the baseline (1.5x noise floor of 0.006), AND
- Test deviance reduction > 0.6% (1.5x noise floor of ~0.4%).

Improvement must be observed on at least 4 of 5 seeds. Mixed seed outcomes (passes on 1-3 seeds) count as null result.

Anything below those thresholds counts as null result, regardless of sign of the change."""


def _load_base_dataset() -> pd.DataFrame:
    openroads = gpd.read_parquet(OPENROADS_PATH)
    rla = pd.read_parquet(RLA_PATH)
    net_features = pd.read_parquet(NET_PATH) if NET_PATH.exists() else None
    aadt_estimates = pd.read_parquet(AADT_PATH)
    df = build_collision_dataset(openroads, aadt_estimates, rla, net_features)
    return df


def _attach_temporal_features(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    tz = pd.read_parquet(
        TIMEZONE_PROFILES,
        columns=["link_id", "core_overnight_ratio"],
    )
    core = (
        tz.groupby("link_id", observed=True)
        .agg(core_overnight_ratio=("core_overnight_ratio", "mean"))
        .reset_index()
    )

    traffic = pd.read_parquet(TRAFFIC_FEATURES_PATH, columns=["link_id", "year", "hgv_pct"])
    webtris_hgv = (
        traffic.groupby("link_id", observed=True)
        .agg(webtris_hgv_pct=("hgv_pct", "mean"))
        .reset_index()
    )

    out = df.merge(core, on="link_id", how="left")
    out = out.merge(webtris_hgv, on="link_id", how="left")

    coverage = {
        "core_overnight_ratio": float(out["core_overnight_ratio"].notna().mean()),
        "webtris_hgv_pct": float(out["webtris_hgv_pct"].notna().mean()),
    }
    return out, coverage


def _leakage_link_ids() -> set[Any]:
    leakage = pd.read_csv(LEAKAGE_MAP)
    return set(
        leakage.loc[leakage["stage2_seed42_test_link"].fillna(False), "snapped_link_id"].dropna()
    )


def _xgb_feature_cols(df: pd.DataFrame, extra_features: list[str]) -> list[str]:
    feature_cols = [
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
        "estimated_aadt",
        "is_covid",
        "year_norm",
    ]
    optional = [
        "hgv_proportion",
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
    ] + list(extra_features)
    for col in optional:
        if col in df.columns:
            feature_cols.append(col)
    return feature_cols


def _train_and_evaluate(
    df: pd.DataFrame,
    glm_result: Any,
    glm_features: list[str],
    config: str,
    seed: int,
    leakage_links: set[Any],
) -> tuple[dict[str, Any], pd.DataFrame]:
    try:
        from xgboost import XGBRegressor
    except ImportError as e:
        raise ImportError("pip install xgboost") from e

    extra_features = CONFIGS[config]["extra_features"]
    feature_cols = _xgb_feature_cols(df, extra_features)

    model_df = df[["link_id", "year", "collision_count", "log_offset"] + feature_cols].copy()
    model_df[feature_cols] = model_df[feature_cols].fillna(0)
    model_df["log_offset"] = model_df["log_offset"].fillna(0)

    X = model_df[feature_cols].astype("float32")
    y = model_df["collision_count"].astype(int)
    offsets = model_df["log_offset"].to_numpy(dtype="float32", copy=False)
    groups = model_df["link_id"].to_numpy()

    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    idx_train, idx_test = next(gss.split(X, y, groups=groups))
    X_train, X_test = X.iloc[idx_train], X.iloc[idx_test]
    y_train, y_test = y.iloc[idx_train], y.iloc[idx_test]
    off_train, off_test = offsets[idx_train], offsets[idx_test]

    model = XGBRegressor(
        objective="count:poisson",
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=seed,
        n_jobs=1,
        verbosity=0,
    )
    model.fit(
        X_train,
        y_train,
        base_margin=off_train,
        eval_set=[(X_test, y_test)],
        base_margin_eval_set=[off_test],
        verbose=False,
    )

    y_pred = model.predict(X_test, base_margin=off_test)
    test_df = model_df.iloc[idx_test][["link_id", "year", "collision_count"]].copy()
    test_df["y_pred"] = y_pred.astype("float64", copy=False)

    importance = pd.Series(model.feature_importances_, index=feature_cols)

    logger.info("Scoring pooled outputs for config %s seed %s ...", config, seed)
    scores = score_collision_models(
        glm_result,
        model,
        glm_features,
        feature_cols,
        df,
    )
    logger.info("Pooled scoring complete for config %s seed %s", config, seed)
    ABLATION_OUT_DIR.mkdir(parents=True, exist_ok=True)
    scores.to_parquet(ABLATION_OUT_DIR / f"config_{config}_seed_{seed}.parquet", index=False)

    metrics_rows: list[dict[str, Any]] = []
    for leakage_handling, sub in [
        ("full", test_df),
        ("primary", test_df[~test_df["link_id"].isin(leakage_links)].copy()),
    ]:
        eps = 1e-6
        y_obs = sub["collision_count"].to_numpy(dtype="float64", copy=False)
        y_hat = sub["y_pred"].to_numpy(dtype="float64", copy=False)
        deviance = 2.0 * float(
            np.sum(
                np.where(y_obs > 0, y_obs * np.log((y_obs + eps) / (y_hat + eps)), 0.0)
                - (y_obs - y_hat)
            )
        )
        null_pred = np.full_like(y_hat, y_obs.mean(), dtype="float64")
        null_dev = 2.0 * float(
            np.sum(
                np.where(y_obs > 0, y_obs * np.log((y_obs + eps) / (null_pred + eps)), 0.0)
                - (y_obs - null_pred)
            )
        )
        pseudo_r2 = float(1.0 - deviance / null_dev) if null_dev > 0 else float("nan")
        metrics_rows.append(
            {
                "config": config,
                "seed": seed,
                "leakage_handling": leakage_handling,
                "pseudo_r2": pseudo_r2,
                "test_deviance": deviance,
                "n_eval_links": int(sub["link_id"].nunique()),
                "hgv_proportion_importance": float(importance.get("hgv_proportion", np.nan)),
                "core_overnight_ratio_importance": float(
                    importance.get("core_overnight_ratio", np.nan)
                ),
                "webtris_hgv_pct_importance": float(importance.get("webtris_hgv_pct", np.nan)),
            }
        )

    summary = {
        "config": config,
        "seed": seed,
        "n_train": int(len(idx_train)),
        "n_test": int(len(idx_test)),
        "feature_cols": feature_cols,
        "importance": importance.to_dict(),
        "metrics_rows": metrics_rows,
    }
    return summary, scores


def _load_baseline_scores(seed: int) -> pd.DataFrame:
    return pd.read_parquet(
        BASELINE_OUT_DIR / f"seed_{seed}.parquet",
        columns=["link_id", "collision_count", "predicted_xgb"],
    )


def _top1_jaccard_vs_baseline(config_scores: pd.DataFrame, baseline_scores: pd.DataFrame) -> float:
    k = max(1, len(baseline_scores) // 100)
    base_top = set(
        baseline_scores.sort_values(
            ["predicted_xgb", "link_id"],
            ascending=[False, True],
            kind="mergesort",
        )["link_id"].head(k)
    )
    cfg_top = set(
        config_scores.sort_values(
            ["predicted_xgb", "link_id"],
            ascending=[False, True],
            kind="mergesort",
        )["link_id"].head(k)
    )
    union = base_top | cfg_top
    return float(len(base_top & cfg_top) / len(union)) if union else float("nan")


def _decision_flags(primary_df: pd.DataFrame) -> pd.DataFrame:
    baseline = (
        primary_df[primary_df["config"] == "A"][["seed", "pseudo_r2", "test_deviance"]]
        .rename(
            columns={
                "pseudo_r2": "baseline_pseudo_r2",
                "test_deviance": "baseline_test_deviance",
            }
        )
        .copy()
    )
    merged = primary_df.merge(baseline, on="seed", how="left")
    merged["pseudo_r2_improvement"] = merged["pseudo_r2"] - merged["baseline_pseudo_r2"]
    merged["deviance_reduction_pct"] = (
        merged["baseline_test_deviance"] - merged["test_deviance"]
    ) / merged["baseline_test_deviance"]
    merged["passes_rule"] = (
        (merged["config"] != "A")
        & (merged["pseudo_r2_improvement"] > 0.009)
        & (merged["deviance_reduction_pct"] > 0.006)
    )
    return merged


def _verdict(config_df: pd.DataFrame) -> str:
    passes = int(config_df["passes_rule"].sum())
    if passes >= 4:
        return "adopt"
    if passes in (1, 2, 3):
        return "mixed"
    return "null"


def _format_float(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}" if np.isfinite(value) else "nan"


def _markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in df.iterrows():
        cells = []
        for value in row:
            if isinstance(value, (float, np.floating)):
                cells.append(_format_float(float(value)))
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def run_temporal_ablation() -> pd.DataFrame:
    df = _load_base_dataset()
    df, coverage = _attach_temporal_features(df)
    leakage_links = _leakage_link_ids()
    glm_result, glm_features, _glm_summary = _load_existing_glm_and_features(df)

    rows: list[dict[str, Any]] = []
    jaccard_rows: list[dict[str, Any]] = []
    for config in ["A", "B", "C"]:
        logger.info("=== Temporal ablation config %s: %s ===", config, CONFIGS[config]["label"])
        for i, seed in enumerate(SEEDS, start=1):
            logger.info("Config %s seed %s (%s/%s)", config, seed, i, len(SEEDS))
            summary, scores = _train_and_evaluate(
                df, glm_result, glm_features, config, seed, leakage_links
            )
            rows.extend(summary["metrics_rows"])
            if config in {"B", "C"}:
                baseline_scores = _load_baseline_scores(seed)
                jaccard_rows.append(
                    {
                        "config": config,
                        "seed": seed,
                        "top1pct_jaccard_vs_baseline": _top1_jaccard_vs_baseline(
                            scores, baseline_scores
                        ),
                    }
                )
            pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False)

    results = pd.DataFrame(rows)
    decision_df = _decision_flags(results[results["leakage_handling"] == "primary"].copy())
    jaccard_df = pd.DataFrame(jaccard_rows)
    _write_summary(results, decision_df, jaccard_df, coverage)
    return results


def _write_summary(
    results: pd.DataFrame,
    decision_df: pd.DataFrame,
    jaccard_df: pd.DataFrame,
    coverage: dict[str, float],
) -> None:
    lines: list[str] = []
    lines.append("# Temporal Ablation Summary\n")
    lines.append("## Pre-Registered Decision Rule\n")
    lines.append(DECISION_RULE + "\n")

    lines.append("## Feature Source Note\n")
    lines.append(
        "Configuration C uses `webtris_hgv_pct` from `data/features/road_traffic_features.parquet` "
        "rather than `timezone_profiles.parquet`, because `timezone_profiles.parquet` does not contain "
        "a plain WebTRIS HGV percentage column. This is the literal WebTRIS HGV% descriptor.\n"
    )

    lines.append("## Coverage Rates\n")
    lines.append(
        f"- `core_overnight_ratio` non-missing share: {_format_float(coverage['core_overnight_ratio'], 4)}\n"
    )
    lines.append(
        f"- `webtris_hgv_pct` non-missing share: {_format_float(coverage['webtris_hgv_pct'], 4)}\n"
    )

    lines.append("## Config Summary\n")
    for leakage in ["primary", "full"]:
        lines.append(f"### {leakage.title()} Evaluation\n")
        sub = results[results["leakage_handling"] == leakage].copy()
        summary_rows = []
        for config in ["A", "B", "C"]:
            cfg = sub[sub["config"] == config]
            summary_rows.append(
                {
                    "config": config,
                    "pseudo_r2_mean": cfg["pseudo_r2"].mean(),
                    "pseudo_r2_min": cfg["pseudo_r2"].min(),
                    "pseudo_r2_max": cfg["pseudo_r2"].max(),
                    "deviance_mean": cfg["test_deviance"].mean(),
                    "deviance_min": cfg["test_deviance"].min(),
                    "deviance_max": cfg["test_deviance"].max(),
                }
            )
        lines.append(_markdown_table(pd.DataFrame(summary_rows)) + "\n")

    lines.append("## Primary Rule Check\n")
    pass_rows = []
    for config in ["B", "C"]:
        cfg = decision_df[decision_df["config"] == config].copy()
        for _, row in cfg.sort_values("seed").iterrows():
            pass_rows.append(
                {
                    "config": config,
                    "seed": int(row["seed"]),
                    "pseudo_r2_improvement": row["pseudo_r2_improvement"],
                    "deviance_reduction_pct": row["deviance_reduction_pct"],
                    "passes_rule": bool(row["passes_rule"]),
                }
            )
    lines.append(_markdown_table(pd.DataFrame(pass_rows)) + "\n")

    lines.append("## Verdicts\n")
    for config in ["B", "C"]:
        cfg = decision_df[decision_df["config"] == config].copy()
        lines.append(f"- Config {config}: `{_verdict(cfg)}`\n")

    lines.append("## Top-1% Rank Jaccard vs Baseline\n")
    if not jaccard_df.empty:
        jacc_summary = (
            jaccard_df.groupby("config", observed=True)["top1pct_jaccard_vs_baseline"]
            .agg(["mean", "min", "max"])
            .reset_index()
        )
        lines.append(_markdown_table(jacc_summary) + "\n")

    OUTPUT_MD.write_text("\n".join(lines))


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    results = run_temporal_ablation()
    print(results.to_string(index=False))
    print(f"Wrote {OUTPUT_CSV}")
    print(f"Wrote {OUTPUT_MD}")


if __name__ == "__main__":
    main()
