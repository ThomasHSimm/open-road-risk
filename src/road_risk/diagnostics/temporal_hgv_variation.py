"""
HGV percentage within-month site variation diagnostic.

Implements temporal plan step 1b. The diagnostic checks whether WebTRIS
`adt24largevehiclepercentage` has enough link/site-specific spread within each
month to justify testing HGV percentage as a collision-model descriptor.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

from road_risk.config import _ROOT
from road_risk.model.constants import MONTH_ORDER

logger = logging.getLogger(__name__)

WEBTRIS_RAW = _ROOT / "data/raw/webtris"
SITES_PATH = WEBTRIS_RAW / "sites.parquet"
SETTINGS_PATH = _ROOT / "config/settings.yaml"
SUPPORTING_DIR = _ROOT / "reports/supporting"

MONTHLY_STD_OUT = SUPPORTING_DIR / "temporal_hgv_monthly_std.csv"
SITE_MONTH_OUT = SUPPORTING_DIR / "temporal_hgv_site_month_profile.csv"
ROAD_TYPE_OUT = SUPPORTING_DIR / "temporal_hgv_road_type_summary.csv"


def _load_study_sites(sites_path: Path = SITES_PATH) -> pd.DataFrame:
    """Load WebTRIS sites and filter to the configured study-area bbox."""
    sites = pd.read_parquet(sites_path)[["site_id", "description", "latitude", "longitude"]]
    sites["site_id"] = sites["site_id"].astype(str)
    sites["road_prefix"] = sites["description"].str[:4].str.strip()
    sites["road_type"] = np.select(
        [
            sites["road_prefix"].str.startswith("M", na=False),
            sites["road_prefix"].str.startswith("A", na=False),
        ],
        ["Motorway", "A-road"],
        default="Other",
    )

    cfg = yaml.safe_load(SETTINGS_PATH.read_text())
    bbox = cfg.get("study_area", {}).get("bbox_wgs84", {})
    required = ["min_lat", "max_lat", "min_lon", "max_lon"]
    missing = [key for key in required if key not in bbox]
    if missing:
        raise ValueError(f"Missing bbox_wgs84 keys in {SETTINGS_PATH}: {missing}")

    study = sites[
        sites["latitude"].between(bbox["min_lat"], bbox["max_lat"])
        & sites["longitude"].between(bbox["min_lon"], bbox["max_lon"])
    ].copy()
    if study.empty:
        raise ValueError("No WebTRIS sites found in configured study area")
    return study


def _read_hgv_raw(raw_folder: Path, study_site_ids: set[str]) -> pd.DataFrame:
    """Read monthly HGV percentage values for study-area WebTRIS chunks."""
    chunks = sorted(raw_folder.glob("site_*_*.parquet"))
    if not chunks:
        raise FileNotFoundError(f"No WebTRIS site-year chunks found in {raw_folder}")

    frames: list[pd.DataFrame] = []
    columns = ["site_id", "monthname", "year", "adt24largevehiclepercentage", "adt24hour"]
    for chunk in chunks:
        site_id = chunk.stem.split("_")[1]
        if site_id not in study_site_ids:
            continue
        data = pd.read_parquet(chunk, columns=columns)
        # The chunk name is authoritative: each file is one site-year.
        data["site_id"] = site_id
        frames.append(data)

    if not frames:
        raise ValueError("No WebTRIS chunks found for study-area sites")

    raw = pd.concat(frames, ignore_index=True)
    raw["hgv_pct"] = pd.to_numeric(raw["adt24largevehiclepercentage"], errors="coerce")
    raw["adt24hour"] = pd.to_numeric(raw["adt24hour"], errors="coerce")
    raw["year"] = pd.to_numeric(raw["year"], errors="coerce").astype("Int64")
    raw["monthname"] = pd.Categorical(raw["monthname"], categories=MONTH_ORDER, ordered=True)
    raw = raw.dropna(subset=["site_id", "monthname", "hgv_pct"])
    return raw[["site_id", "year", "monthname", "hgv_pct", "adt24hour"]]


def build_hgv_site_month_profile(
    raw_folder: Path = WEBTRIS_RAW,
    sites_path: Path = SITES_PATH,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return per-site/month HGV profile and the study-area site lookup."""
    sites = _load_study_sites(sites_path)
    raw = _read_hgv_raw(raw_folder, set(sites["site_id"]))
    logger.info(
        "Loaded %s monthly rows from %s study-area sites",
        f"{len(raw):,}",
        f"{raw['site_id'].nunique():,}",
    )

    profile = (
        raw.groupby(["site_id", "monthname"], observed=True)
        .agg(
            mean_hgv_pct=("hgv_pct", "mean"),
            mean_adt24=("adt24hour", "mean"),
            n_site_years=("year", "nunique"),
            n_records=("hgv_pct", "size"),
        )
        .reset_index()
        .merge(sites[["site_id", "road_prefix", "road_type"]], on="site_id", how="left")
        .sort_values(["site_id", "monthname"])
    )
    return profile, sites


def summarise_hgv_variation(profile: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Create monthly, road-type, and headline summaries."""
    monthly = (
        profile.groupby("monthname", observed=True)["mean_hgv_pct"]
        .agg(
            n_sites="count",
            mean_pct="mean",
            std_pct_points="std",
            median_pct="median",
            q10=lambda s: s.quantile(0.10),
            q25=lambda s: s.quantile(0.25),
            q75=lambda s: s.quantile(0.75),
            q90=lambda s: s.quantile(0.90),
            max_pct="max",
        )
        .reset_index()
    )

    site_mean = (
        profile.groupby(["site_id", "road_prefix", "road_type"], observed=True)
        .agg(mean_hgv_pct=("mean_hgv_pct", "mean"), mean_adt24=("mean_adt24", "mean"))
        .reset_index()
    )
    road_type = (
        site_mean.groupby("road_type", observed=True)["mean_hgv_pct"]
        .agg(
            n_sites="count",
            mean_pct="mean",
            std_pct_points="std",
            median_pct="median",
            q10=lambda s: s.quantile(0.10),
            q25=lambda s: s.quantile(0.25),
            q75=lambda s: s.quantile(0.75),
            q90=lambda s: s.quantile(0.90),
            max_pct="max",
        )
        .reset_index()
    )

    monthly_std = monthly["std_pct_points"].dropna()
    headline = pd.DataFrame(
        [
            {
                "n_site_months": int(len(profile)),
                "n_sites": int(profile["site_id"].nunique()),
                "median_monthly_std_pct_points": float(monthly_std.median()),
                "min_monthly_std_pct_points": float(monthly_std.min()),
                "max_monthly_std_pct_points": float(monthly_std.max()),
                "mean_monthly_std_pct_points": float(monthly_std.mean()),
                "site_mean_q10": float(site_mean["mean_hgv_pct"].quantile(0.10)),
                "site_mean_median": float(site_mean["mean_hgv_pct"].median()),
                "site_mean_q90": float(site_mean["mean_hgv_pct"].quantile(0.90)),
                "site_mean_max": float(site_mean["mean_hgv_pct"].max()),
                "share_sites_ge_30pct": float((site_mean["mean_hgv_pct"] >= 30).mean()),
                "share_sites_ge_40pct": float((site_mean["mean_hgv_pct"] >= 40).mean()),
            }
        ]
    )
    return {"monthly": monthly, "road_type": road_type, "headline": headline}


def _format_table(df: pd.DataFrame, cols: list[str], digits: int = 2) -> str:
    rows: list[list[Any]] = []
    for _, row in df[cols].iterrows():
        formatted = []
        for value in row:
            if isinstance(value, (float, np.floating)):
                formatted.append(f"{value:.{digits}f}")
            else:
                formatted.append(str(value))
        rows.append(formatted)

    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def run_hgv_variation_diagnostic() -> dict[str, pd.DataFrame]:
    """Run the diagnostic and write supporting CSV artefacts."""
    SUPPORTING_DIR.mkdir(parents=True, exist_ok=True)
    profile, _sites = build_hgv_site_month_profile()
    summaries = summarise_hgv_variation(profile)

    profile.to_csv(SITE_MONTH_OUT, index=False)
    summaries["monthly"].to_csv(MONTHLY_STD_OUT, index=False)
    summaries["road_type"].to_csv(ROAD_TYPE_OUT, index=False)

    headline = summaries["headline"].iloc[0]
    logger.info("Wrote %s", SITE_MONTH_OUT)
    logger.info("Wrote %s", MONTHLY_STD_OUT)
    logger.info("Wrote %s", ROAD_TYPE_OUT)
    logger.info(
        "Monthly std: median %.2f pp, range %.2f-%.2f pp",
        headline["median_monthly_std_pct_points"],
        headline["min_monthly_std_pct_points"],
        headline["max_monthly_std_pct_points"],
    )
    return {"profile": profile, **summaries}


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    outputs = run_hgv_variation_diagnostic()
    print("\nMonthly HGV% within-month std across sites:")
    print(
        _format_table(
            outputs["monthly"],
            ["monthname", "n_sites", "mean_pct", "std_pct_points", "q10", "q90", "max_pct"],
        )
    )
    print("\nRoad-type site-mean HGV% summary:")
    print(
        _format_table(
            outputs["road_type"],
            ["road_type", "n_sites", "mean_pct", "std_pct_points", "q10", "q90", "max_pct"],
        )
    )
    print("\nHeadline:")
    print(outputs["headline"].to_string(index=False))


if __name__ == "__main__":
    main()
