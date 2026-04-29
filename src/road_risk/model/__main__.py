import argparse

from road_risk.model.main import main

parser = argparse.ArgumentParser(description="Road risk model pipeline")
parser.add_argument(
    "--stage",
    choices=["traffic", "profile", "temporal", "collision", "all"],
    default="all",
    help="Which stage to run (default: all)",
)
args = parser.parse_args()
main(stage=args.stage)
