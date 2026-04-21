"""
data.py
-------
Cached data loading and filtered GeoDataFrame construction.

All public functions use @st.cache_data so they only re-execute when their
arguments change. Map pan/zoom no longer trigger reruns (handled by
returned_objects in st_folium), so build_map_gdf only fires on real filter
changes.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd
import streamlit as st

from config import (
    RISK_PATH, OR_PATH, NET_PATH, TEMPORAL_PATH, DTC_PATHS,
    DTC_LON_BOUNDS, DTC_LAT_BOUNDS,
)

# risk_scores.parquet is now one row per link_id (pooled across years).
# No year column, no aggregation needed.


# ---------------------------------------------------------------------------
# Raw loaders
# ---------------------------------------------------------------------------

@st.cache_data
def load_risk() -> pd.DataFrame | None:
    if RISK_PATH is None or not RISK_PATH.exists():
        return None
    return pd.read_parquet(RISK_PATH)


@st.cache_data
def load_openroads() -> gpd.GeoDataFrame | None:
    if OR_PATH is None or not OR_PATH.exists():
        return None
    gdf = gpd.read_parquet(OR_PATH)
    return gdf.to_crs("EPSG:4326")


@st.cache_data
def load_network() -> pd.DataFrame | None:
    if NET_PATH is None or not NET_PATH.exists():
        return None
    return pd.read_parquet(NET_PATH)


@st.cache_data
def load_temporal() -> pd.DataFrame | None:
    """
    Load temporal (seasonal) profiles keyed by road_prefix.
    Expected columns: road_prefix, monthname (or month), seasonal_index.
    Returns None silently if the file doesn't exist yet.
    """
    if TEMPORAL_PATH is None or not TEMPORAL_PATH.exists():
        return None
    return pd.read_parquet(TEMPORAL_PATH)


@st.cache_data
def load_dtc() -> pd.DataFrame | None:
    for p in DTC_PATHS:
        if Path(p).exists():
            dtc = pd.read_csv(p)
            lat_min, lat_max = DTC_LAT_BOUNDS
            lon_min, lon_max = DTC_LON_BOUNDS
            return dtc[
                dtc["latitude"].between(lat_min, lat_max) &
                dtc["longitude"].between(lon_min, lon_max)
            ].copy()
    return None


# ---------------------------------------------------------------------------
# Filtered map GeoDataFrame
# ---------------------------------------------------------------------------

# Columns to pull from risk_scores.parquet (one row per link_id — no year).
# Rename map: {output_col: source_col}. Missing columns are skipped gracefully.
_RISK_COLS = {
    "risk_percentile": "risk_percentile",
    "predicted_glm":   "predicted_glm",
    "residual_glm":    "residual_glm",
    "collision_count": "collision_count",
    "fatal_count":     "fatal_count",
    "serious_count":   "serious_count",
    "estimated_aadt":  "estimated_aadt",
    "hgv_pct":         "hgv_proportion",
    "speed_limit":     "speed_limit_mph",
}


@st.cache_data
def build_map_gdf(
    road_classes_tuple: tuple[str, ...],
    min_percentile: int,
) -> gpd.GeoDataFrame | None:
    """
    Join risk scores (one row per link) + geometry + network features,
    apply UI filters.

    risk_scores.parquet is now pooled — no year dimension.
    Every scored link has risk_percentile, collision_count (pooled total),
    estimated_aadt (mean across years), and residual_glm.

    All ~998k links are scored (including zero-collision links), so no
    two-layer grey-skeleton rendering is needed.
    """
    risk      = load_risk()
    openroads = load_openroads()
    net       = load_network()

    if risk is None or openroads is None:
        return None

    # Rename source columns to app display names
    rename = {v: k for k, v in _RISK_COLS.items() if v in risk.columns and v != k}
    risk_renamed = risk.rename(columns=rename)

    # Drop columns that also exist in openroads to avoid _x/_y suffix collisions.
    # road_classification from openroads is authoritative.
    or_cols = {"road_classification", "road_name", "link_length_km", "form_of_way"}
    drop_from_risk = [c for c in or_cols if c in risk_renamed.columns]
    if drop_from_risk:
        risk_renamed = risk_renamed.drop(columns=drop_from_risk)

    gdf = openroads[
        ["link_id", "geometry", "road_classification",
         "road_name", "link_length_km", "form_of_way"]
    ].merge(risk_renamed, on="link_id", how="left")

    # Join network features
    if net is not None:
        net_want  = ["link_id", "betweenness_relative", "degree_mean",
                     "betweenness", "dist_to_major_km", "pop_density_per_km2"]
        available = [c for c in net_want if c in net.columns]
        gdf = gdf.merge(net[available], on="link_id", how="left")

    # Road-class filter
    if road_classes_tuple:
        gdf = gdf[gdf["road_classification"].isin(road_classes_tuple)]

    # Percentile threshold
    if min_percentile > 0 and "risk_percentile" in gdf.columns:
        gdf = gdf[gdf["risk_percentile"] >= min_percentile]

    return gdf.copy()
