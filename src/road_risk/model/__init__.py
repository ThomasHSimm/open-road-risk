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

from road_risk.model.aadt import train_aadt_estimator, apply_aadt_estimator
from road_risk.model.collision import build_collision_dataset, run_collision_stage
from road_risk.model.timezone_profile import run_profile_stage

__all__ = [
    "train_aadt_estimator",
    "apply_aadt_estimator",
    "build_collision_dataset",
    "run_collision_stage",
    "run_profile_stage",
]
