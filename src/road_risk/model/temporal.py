"""
temporal.py
-----------
Stage 1b: Monthly traffic profiles from WebTRIS sensor data.

Computes seasonal multipliers and weekday/weekend ratios per road corridor.
Used for context and potential future temporal exposure weighting.
Not required for the core collision model — which uses pooled AADT.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from road_risk.config import _ROOT
from road_risk.model.constants import MONTH_ORDER

logger = logging.getLogger(__name__)

WEBTRIS_RAW = _ROOT / "data/raw/webtris"
SITES_PATH  = _ROOT / "data/raw/webtris/sites.parquet"
MODELS      = _ROOT / "data/models"


def build_temporal_profiles(
    raw_folder: Path = WEBTRIS_RAW,
    sites_path: Path = SITES_PATH,
) -> pd.DataFrame:
    """
    Build monthly traffic profiles from WebTRIS raw chunk parquets.

    Returns DataFrame at road_prefix × month with:
    - seasonal_index       : monthly flow relative to annual mean
    - weekday_weekend_ratio: awt24hour / adt24hour
    - mean_large_pct       : large vehicle percentage by month
    """
    logger.info("Building temporal traffic profiles from WebTRIS ...")

    sites = pd.read_parquet(sites_path)[
        ["site_id", "description", "latitude", "longitude"]
    ]
    sites["road_prefix"] = sites["description"].str[:4].str.strip()

    chunks = sorted(raw_folder.glob("site_*_*.parquet"))
    if not chunks:
        raise FileNotFoundError(f"No WebTRIS chunks in {raw_folder}")

    # Filter to study area — read from config if available, else use full dataset
    try:
        from road_risk.config import _ROOT
        import yaml
        cfg_path = _ROOT / "config/settings.yaml"
        if cfg_path.exists():
            cfg = yaml.safe_load(cfg_path.read_text())
            bbox = cfg.get("study_area", {}).get("bbox_wgs84", {})
            lat_min = bbox.get("min_lat", 50.0)
            lat_max = bbox.get("max_lat", 56.0)
            lon_min = bbox.get("min_lon", -4.0)
            lon_max = bbox.get("max_lon", 2.0)
        else:
            lat_min, lat_max, lon_min, lon_max = 50.0, 56.0, -4.0, 2.0
    except Exception:
        lat_min, lat_max, lon_min, lon_max = 50.0, 56.0, -4.0, 2.0

    study_sites = set(
        sites[
            sites["latitude"].between(lat_min, lat_max) &
            sites["longitude"].between(lon_min, lon_max)
        ]["site_id"]
    )

    frames = []
    for chunk in chunks:
        site_id = chunk.stem.split("_")[1]
        if site_id not in study_sites:
            continue
        df = pd.read_parquet(chunk)
        df["site_id"] = site_id
        frames.append(df)

    if not frames:
        raise ValueError("No WebTRIS chunks found in study area")

    raw = pd.concat(frames, ignore_index=True)
    logger.info(f"  Loaded {len(raw):,} rows from {len(study_sites):,} sites")

    for col in ["adt24hour", "awt24hour", "adt24largevehiclepercentage"]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")

    raw = raw.merge(sites[["site_id", "road_prefix"]], on="site_id", how="left")
    raw["month_num"] = (
        pd.Categorical(raw["monthname"], categories=MONTH_ORDER, ordered=True).codes + 1
    )
    raw["monthname"] = pd.Categorical(
        raw["monthname"], categories=MONTH_ORDER, ordered=True
    )

    profile = (
        raw.groupby(["road_prefix", "monthname", "month_num"])
        .agg(
            mean_adt24=("adt24hour", "mean"),
            mean_awt24=("awt24hour", "mean"),
            mean_large_pct=("adt24largevehiclepercentage", "mean"),
            n_site_months=("site_id", "count"),
        )
        .reset_index()
        .sort_values(["road_prefix", "month_num"])
    )

    annual_mean = profile.groupby("road_prefix")["mean_adt24"].transform("mean")
    profile["seasonal_index"] = profile["mean_adt24"] / annual_mean.replace(0, np.nan)
    profile["weekday_weekend_ratio"] = (
        profile["mean_awt24"] / profile["mean_adt24"].replace(0, np.nan)
    )

    logger.info(
        f"  Profiles built: {profile['road_prefix'].nunique()} road types × 12 months"
    )

    out = MODELS / "temporal_profiles.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    profile.to_parquet(out, index=False)
    logger.info(f"  Saved to {out}")

    return profile


def plot_temporal_profiles(profiles: pd.DataFrame) -> None:
    """Plot seasonal profiles for top road corridors."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning("matplotlib not available — skipping plot")
        return

    top_roads = (
        profiles.groupby("road_prefix")["n_site_months"]
        .sum().nlargest(6).index.tolist()
    )

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for ax, road in zip(axes.flatten(), top_roads):
        data = profiles[profiles["road_prefix"] == road].sort_values("month_num")
        ax.bar(data["monthname"], data["seasonal_index"],
               color="steelblue", alpha=0.8)
        ax2 = ax.twinx()
        ax2.plot(data["monthname"], data["mean_large_pct"],
                 color="crimson", marker="o", linewidth=2, markersize=4)
        ax2.set_ylabel("Large vehicle %", color="crimson")
        ax.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
        ax.set_title(f"{road} (n={data['n_site_months'].sum():,})")
        ax.set_ylabel("Seasonal index")
        ax.tick_params(axis="x", rotation=45)

    plt.suptitle(
        "WebTRIS seasonal traffic profiles — study area motorways/trunk roads",
        fontsize=13, y=1.02,
    )
    plt.tight_layout()

    out = MODELS / "temporal_profiles.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    logger.info(f"  Saved plot to {out}")
    plt.close()


if __name__ == "__main__":
    # profiles = build_temporal_profiles()
    out = MODELS / "temporal_profiles.parquet"
    if out.exists():
        profiles = pd.read_parquet(out)
    else:
        logger.error(f"Temporal profiles not found at {out} — run build_temporal_profiles() first")
        profiles = build_temporal_profiles()
    plot_temporal_profiles(profiles)