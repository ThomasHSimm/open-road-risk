"""
CLI entry point for the model package.

Usage:
    python -m road_risk.model --stage traffic
    python -m road_risk.model --stage profile
    python -m road_risk.model --stage temporal
    python -m road_risk.model --stage collision
    python -m road_risk.model --stage all
"""

import argparse
import logging

import geopandas as gpd
import pandas as pd

from road_risk.config import _ROOT, cfg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
logger = logging.getLogger(__name__)

PROCESSED = _ROOT / cfg["paths"]["processed"]
AADF_PATH = PROCESSED / "aadf/aadf_clean.parquet"
OPENROADS_PATH = PROCESSED / "shapefiles/openroads.parquet"
MODELS = _ROOT / cfg["paths"]["models"]


def main(stage: str = "all") -> None:
    openroads = gpd.read_parquet(OPENROADS_PATH)

    if stage in ("traffic", "all"):
        from road_risk.model.aadt import run_traffic_stage

        logger.info("=== Stage 1a: AADT estimator ===")
        aadf = pd.read_parquet(AADF_PATH)

        estimates, model, metrics, features = run_traffic_stage(aadf, openroads)

        print("\n=== AADT estimator results ===")
        print(f"  CV R²  : {metrics['cv_r2_mean']:.3f} (±{metrics['cv_r2_std']:.3f})")
        print(
            f"  CV MAE : {metrics['cv_mae_mean']:.3f} log-units "
            f"≈ ×{__import__('numpy').expm1(metrics['cv_mae_mean']):.2f} "
            "multiplicative error"
        )
        if "external_validation" in metrics:
            print("\n  External validation (log scale):")
            for scheme, res in metrics["external_validation"].items():
                print(
                    f"    {scheme:8s}: R²={res['r2']:.3f} | "
                    f"MAE={res['mae']:.3f} | RMSE={res['rmse']:.3f} "
                    f"(n={res['n']:,})"
                )
        print(
            f"\n  Links  : {estimates['link_id'].nunique():,} × {estimates['year'].nunique()} years"
        )
        print("\n  Estimated AADT distribution:")
        print(estimates["estimated_aadt"].describe().round(0).to_string())

    if stage in ("profile", "all"):
        from road_risk.model.timezone_profile import run_profile_stage

        logger.info("=== Stage 1b: Time-zone profile estimator ===")
        profiles, prof_metrics = run_profile_stage(openroads)

        print("\n=== Time-zone profile results ===")
        for target, m in prof_metrics.items():
            print(
                f"  {target:20s}: CV R²={m['cv_r2_mean']:.3f} "
                f"(±{m['cv_r2_std']:.3f}) | MAE={m['cv_mae_mean']:.4f} "
                f"(n={m['n_train']:,})"
            )
        print(
            f"\n  Median core_daytime_frac         : {profiles['core_daytime_frac'].median():.3f}"
        )
        print(f"  Median core_overnight_ratio: {profiles['core_overnight_ratio'].median():.2f}")

    if stage in ("temporal", "all"):
        from road_risk.model.temporal import build_temporal_profiles, plot_temporal_profiles

        logger.info("=== Stage 1b: Temporal profiles ===")
        profiles = build_temporal_profiles()
        plot_temporal_profiles(profiles)

        print("\n=== Temporal profiles ===")
        print(f"  Road types: {sorted(profiles['road_prefix'].unique())}")

    if stage in ("collision", "all"):
        from road_risk.model.collision import run_collision_stage

        run_collision_stage()

    if stage == "all":
        logger.info("=== All stages complete ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Road risk model pipeline")
    parser.add_argument(
        "--stage",
        choices=["traffic", "profile", "temporal", "collision", "all"],
        default="all",
        help="Which stage to run (default: all)",
    )
    args = parser.parse_args()
    main(stage=args.stage)
