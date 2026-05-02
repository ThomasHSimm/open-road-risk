"""
Temporal descriptor leakage-geometry diagnostic.

Implements temporal plan Step 2. It checks whether WebTRIS sites used by the
temporal pipelines snap to Open Roads links that fall in the Stage 2 collision
model held-out fold. If they do, temporal descriptors for those links are
in-sample with respect to the temporal model and should be treated as mildly
optimistic in collision-model ablations unless folds are aligned.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
import yaml
from sklearn.model_selection import GroupShuffleSplit

from road_risk.config import _ROOT
from road_risk.model.constants import RANDOM_STATE
from road_risk.model.timezone_profile import FRACTION_TARGETS

logger = logging.getLogger(__name__)

WEBTRIS_CLEAN = _ROOT / "data/processed/webtris/webtris_clean.parquet"
WEBTRIS_RAW = _ROOT / "data/raw/webtris"
WEBTRIS_SITES = WEBTRIS_RAW / "sites.parquet"
OPENROADS_PATH = _ROOT / "data/processed/shapefiles/openroads.parquet"
SETTINGS_PATH = _ROOT / "config/settings.yaml"
SUPPORTING_DIR = _ROOT / "reports/supporting"

SITE_LINK_OUT = SUPPORTING_DIR / "temporal_leakage_site_link_map.csv"
SUMMARY_OUT = SUPPORTING_DIR / "temporal_leakage_summary.csv"
SPLIT_SEED = RANDOM_STATE
SNAP_MAX_DISTANCE_M = 2000


def _load_study_sites() -> pd.DataFrame:
    sites = pd.read_parquet(WEBTRIS_SITES)[["site_id", "description", "latitude", "longitude"]]
    sites["site_id"] = sites["site_id"].astype(str)

    cfg = yaml.safe_load(SETTINGS_PATH.read_text())
    bbox = cfg.get("study_area", {}).get("bbox_wgs84", {})
    required = ["min_lat", "max_lat", "min_lon", "max_lon"]
    missing = [key for key in required if key not in bbox]
    if missing:
        raise ValueError(f"Missing bbox_wgs84 keys in {SETTINGS_PATH}: {missing}")

    return sites[
        sites["latitude"].between(bbox["min_lat"], bbox["max_lat"])
        & sites["longitude"].between(bbox["min_lon"], bbox["max_lon"])
    ].copy()


def _timezone_training_sites() -> pd.DataFrame:
    """Reproduce the site/year filter used by build_profile_training()."""
    wt = pd.read_parquet(WEBTRIS_CLEAN)
    wt["site_id"] = wt["site_id"].astype(str)
    wt = wt[wt["all_flow"] > 0].copy()

    wt["core_daytime_frac"] = (wt["flow_ph_core_daytime"] * 12) / wt["all_flow"]
    wt["shoulder_frac"] = (wt["flow_ph_shoulder"] * 4) / wt["all_flow"]
    wt["late_evening_frac"] = (wt["flow_ph_late_evening"] * 2) / wt["all_flow"]
    wt["overnight_frac"] = (wt["flow_ph_overnight"] * 6) / wt["all_flow"]

    frac_sum = wt[FRACTION_TARGETS].sum(axis=1)
    wt = wt[frac_sum.between(0.98, 1.02)].copy()

    return wt[["site_id", "year", "latitude", "longitude"]].dropna(
        subset=["site_id", "latitude", "longitude"]
    )


def _temporal_raw_sites() -> pd.DataFrame:
    """
    Return study-area raw WebTRIS sites with at least one site-year chunk.

    This represents the site population used by `temporal.py` and by the HGV
    step 1b diagnostic. The actual corridor-level temporal profile is not a
    link-level model, but the shared WebTRIS site geometry is still useful for
    checking potential fold overlap before ablation.
    """
    study_sites = _load_study_sites()
    chunk_site_ids = {chunk.stem.split("_")[1] for chunk in WEBTRIS_RAW.glob("site_*_*.parquet")}
    return study_sites[study_sites["site_id"].isin(chunk_site_ids)].copy()


def _stage2_test_links(link_ids: pd.Series, seed: int = SPLIT_SEED) -> set[Any]:
    """Reproduce the Stage 2 GroupShuffleSplit held-out link set."""
    unique_links = np.unique(link_ids.values)
    dummy_x = np.zeros((len(unique_links), 1))
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    _, test_idx = next(gss.split(dummy_x, groups=unique_links))
    return set(unique_links[test_idx])


def _snap_sites_to_links(sites: pd.DataFrame) -> pd.DataFrame:
    """Snap WebTRIS site coordinates to nearest Open Roads link within 2km."""
    import geopandas as gpd
    import pyproj
    from scipy.spatial import cKDTree

    openroads = gpd.read_parquet(OPENROADS_PATH)[["link_id", "road_classification", "geometry"]]
    openroads_bng = openroads.to_crs("EPSG:27700")
    link_xy = np.column_stack(
        [openroads_bng.geometry.centroid.x, openroads_bng.geometry.centroid.y]
    )
    link_ids = openroads["link_id"].values
    road_class = openroads["road_classification"].values
    tree = cKDTree(link_xy)

    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
    easting, northing = transformer.transform(sites["longitude"].values, sites["latitude"].values)
    dists, idx = tree.query(
        np.column_stack([easting, northing]),
        k=1,
        distance_upper_bound=SNAP_MAX_DISTANCE_M,
    )

    snapped = sites.copy()
    valid = dists < SNAP_MAX_DISTANCE_M
    snapped["snapped_link_id"] = pd.NA
    snapped["snap_distance_m"] = np.nan
    snapped["snapped_road_classification"] = pd.NA
    snapped.loc[valid, "snapped_link_id"] = link_ids[idx[valid]]
    snapped.loc[valid, "snap_distance_m"] = dists[valid]
    snapped.loc[valid, "snapped_road_classification"] = road_class[idx[valid]]
    return snapped


def _summary_row(label: str, site_links: pd.DataFrame, test_links: set[Any]) -> dict[str, Any]:
    valid = site_links[site_links["snapped_link_id"].notna()].copy()
    valid_links = set(valid["snapped_link_id"])
    test_overlap = valid[valid["snapped_link_id"].isin(test_links)]
    overlap_links = set(test_overlap["snapped_link_id"])

    return {
        "site_population": label,
        "n_sites": int(site_links["site_id"].nunique()),
        "n_snapped_sites": int(valid["site_id"].nunique()),
        "n_snapped_links": int(len(valid_links)),
        "n_sites_on_stage2_test_links": int(test_overlap["site_id"].nunique()),
        "n_stage2_test_links_with_sites": int(len(overlap_links)),
        "share_snapped_sites_on_stage2_test_links": (
            float(test_overlap["site_id"].nunique() / valid["site_id"].nunique())
            if valid["site_id"].nunique()
            else np.nan
        ),
        "median_snap_distance_m": float(valid["snap_distance_m"].median())
        if len(valid)
        else np.nan,
        "p90_snap_distance_m": float(valid["snap_distance_m"].quantile(0.9))
        if len(valid)
        else np.nan,
    }


def run_temporal_leakage_diagnostic() -> dict[str, pd.DataFrame]:
    """Run Step 2 and write supporting CSVs."""
    SUPPORTING_DIR.mkdir(parents=True, exist_ok=True)

    openroads = pd.read_parquet(OPENROADS_PATH, columns=["link_id"])
    test_links = _stage2_test_links(openroads["link_id"])

    timezone_sites = _timezone_training_sites()
    raw_temporal_sites = _temporal_raw_sites()
    union_sites = (
        pd.concat(
            [
                timezone_sites[["site_id", "latitude", "longitude"]],
                raw_temporal_sites[["site_id", "latitude", "longitude"]],
            ],
            ignore_index=True,
        )
        .drop_duplicates("site_id")
        .reset_index(drop=True)
    )

    snapped = _snap_sites_to_links(union_sites)
    timezone_snapped = snapped[snapped["site_id"].isin(set(timezone_sites["site_id"]))]
    raw_temporal_snapped = snapped[snapped["site_id"].isin(set(raw_temporal_sites["site_id"]))]

    snapped["used_by_timezone_profile"] = snapped["site_id"].isin(set(timezone_sites["site_id"]))
    snapped["used_by_temporal_raw_profiles"] = snapped["site_id"].isin(
        set(raw_temporal_sites["site_id"])
    )
    snapped["stage2_seed42_test_link"] = snapped["snapped_link_id"].isin(test_links)

    summary = pd.DataFrame(
        [
            _summary_row("timezone_profile_training", timezone_snapped, test_links),
            _summary_row("temporal_raw_profiles", raw_temporal_snapped, test_links),
            _summary_row("union", snapped, test_links),
        ]
    )

    snapped.to_csv(SITE_LINK_OUT, index=False)
    summary.to_csv(SUMMARY_OUT, index=False)

    logger.info("Wrote %s", SITE_LINK_OUT)
    logger.info("Wrote %s", SUMMARY_OUT)
    for row in summary.itertuples(index=False):
        logger.info(
            "%s: %s/%s snapped sites on Stage 2 held-out links (%0.1f%%)",
            row.site_population,
            f"{row.n_sites_on_stage2_test_links:,}",
            f"{row.n_snapped_sites:,}",
            row.share_snapped_sites_on_stage2_test_links * 100,
        )

    return {"site_link_map": snapped, "summary": summary}


def _format_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in df.iterrows():
        cells: list[str] = []
        for value in row:
            if isinstance(value, (float, np.floating)):
                cells.append(f"{value:.4f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    outputs = run_temporal_leakage_diagnostic()
    print(_format_table(outputs["summary"]))


if __name__ == "__main__":
    main()
