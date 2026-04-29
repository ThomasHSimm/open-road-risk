"""
model.py — backwards compatibility shim.

The model pipeline has been refactored into src/road_risk/model/
This file delegates to the new package so existing calls still work:
    python src/road_risk/model.py --stage traffic
    python src/road_risk/model.py --stage collision
"""

from road_risk.model.main import main

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Road risk model pipeline")
    parser.add_argument(
        "--stage",
        choices=["traffic", "temporal", "collision", "all"],
        default="all",
    )
    args = parser.parse_args()
    main(stage=args.stage)
