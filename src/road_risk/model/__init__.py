"""
road_risk.model
---------------
Road risk modelling pipeline.

  Stage 1a — AADT estimator   : aadt.py
  Stage 1b — Time-zone profile : timezone_profile.py
  Stage 1b — Temporal context  : temporal.py
  Stage 2  — Collision model   : collision.py

Entrypoint: python -m road_risk.model --stage traffic|profile|temporal|collision|all
"""

__all__ = [
    "train_aadt_estimator",
    "apply_aadt_estimator",
    "build_collision_dataset",
    "run_collision_stage",
    "run_collision_smoke",
    "run_profile_stage",
]


def __getattr__(name):
    if name in {"train_aadt_estimator", "apply_aadt_estimator"}:
        from road_risk.model.aadt import apply_aadt_estimator, train_aadt_estimator

        return {
            "train_aadt_estimator": train_aadt_estimator,
            "apply_aadt_estimator": apply_aadt_estimator,
        }[name]
    if name in {"build_collision_dataset", "run_collision_stage", "run_collision_smoke"}:
        from road_risk.model.collision import (
            build_collision_dataset,
            run_collision_smoke,
            run_collision_stage,
        )

        return {
            "build_collision_dataset": build_collision_dataset,
            "run_collision_stage": run_collision_stage,
            "run_collision_smoke": run_collision_smoke,
        }[name]
    if name == "run_profile_stage":
        from road_risk.model.timezone_profile import run_profile_stage

        return run_profile_stage
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
