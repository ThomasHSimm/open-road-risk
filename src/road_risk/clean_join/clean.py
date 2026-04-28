"""
clean.py
--------
Per-source cleaning functions for road risk pipeline.

Each function accepts the raw loaded DataFrame(s) and returns a cleaned
version ready for joining. Cleaning is kept separate from ingest so the
raw data is never overwritten and cleaning rules are testable in isolation.

Functions
---------
clean_stats19(data)   : drop historic cols, flag COVID, validate coords
clean_aadf(df)        : filter to target years, validate flows, add road_name_clean
clean_webtris(df)     : drop duplicates, aggregate monthly → annual
clean_mrdb(gdf)       : add link_id, derive road_name_clean for joining

Note: spatial analysis uses STATS19 latitude/longitude fields throughout.
    A previous investigation suspected a Yorkshire BNG grid-square error, but
    a direct check against the current raw STATS19 CSV found the BNG fields and
    lat/lon-derived BNG positions agree within a few metres. LSOA validation
    uses lat/lon directly.
"""

import logging
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pyproj

from road_risk.config import _ROOT, cfg

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# WebTRIS pull years — read from config/settings.yaml (webtris.target_years)
TARGET_YEARS: list[int] = cfg["webtris"]["target_years"]

# STATS19 collision columns that are historic/superseded — drop these
HISTORIC_COLS = [
    "junction_detail_historic",
    "pedestrian_crossing_human_control_historic",
    "pedestrian_crossing_physical_facilities_historic",
    "carriageway_hazards_historic",
    "local_authority_highway_current",  # superseded by local_authority_highway
]

# STATS19 first_road_class code → road prefix for name reconstruction
ROAD_CLASS_PREFIX = {
    1: "M",   # Motorway
    2: "A",   # A(M) — motorway-standard A road
    3: "A",   # A road
    4: "B",   # B road
    5: "C",   # C road
    6: "",    # Unclassified
}

# GB bounding box for coordinate validation
GB_LAT = (49.9, 60.9)
GB_LON = (-8.2, 2.0)

# COVID years flag
COVID_YEARS = {2020, 2021}


# ---------------------------------------------------------------------------
# STATS19
# ---------------------------------------------------------------------------

def clean_stats19(
    data: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    """
    Clean all three STATS19 tables.

    Changes applied
    ---------------
    Collisions:
      - Drop historic / superseded columns
      - Parse date → datetime, extract year/month/hour
      - Validate lat/lon within GB bounds (flag bad coords, don't drop)
      - Add is_covid boolean flag
      - Reconstruct road_name_clean from first_road_class + first_road_number
        (used as join key to MRDB/AADF in join.py Stage 1)

    Vehicles:
      - No structural changes — column names already normalised by ingest

    Casualties:
      - No structural changes

    Parameters
    ----------
    data : dict returned by load_stats19() — keys collision/vehicle/casualty

    Returns
    -------
    dict with same keys, cleaned DataFrames
    """
    cleaned = {}

    # --- Collisions ---------------------------------------------------------
    if "collision" in data:
        col = data["collision"].copy()
        logger.info(f"Cleaning collisions: {len(col):,} rows")

        # Drop historic columns (only those present — years vary)
        drop = [c for c in HISTORIC_COLS if c in col.columns]
        col = col.drop(columns=drop)
        logger.info(f"  Dropped {len(drop)} historic columns: {drop}")

        # Parse date
        if "date" in col.columns and not pd.api.types.is_datetime64_any_dtype(col["date"]):
            col["date"] = pd.to_datetime(col["date"], dayfirst=True, errors="coerce")

        # Derive time features
        if "date" in col.columns:
            col["month"] = col["date"].dt.month
            col["day_name"] = col["date"].dt.day_name()

        if "time" in col.columns:
            col["hour"] = pd.to_datetime(
                col["time"], format="%H:%M", errors="coerce"
            ).dt.hour

        # Use collision_year if available, else derive from date
        if "collision_year" not in col.columns and "date" in col.columns:
            col["collision_year"] = col["date"].dt.year

        # COVID flag
        if "collision_year" in col.columns:
            col["is_covid"] = col["collision_year"].isin(COVID_YEARS)
            logger.info(
                f"  COVID rows flagged: {col['is_covid'].sum():,} "
                f"({col['is_covid'].mean():.1%})"
            )

        # Coordinate note: spatial work uses lat/lon. Current raw STATS19 BNG
        # fields cross-check cleanly against lat/lon-derived BNG coordinates.

        # --- LSOA coordinate validation --------------------------------------
        # Cross-check collision coordinates against its recorded LSOA centroid.
        # Collisions >10km from their LSOA centroid have suspect coordinates.
        col = _validate_lsoa_coords(col)

        # Final coords_valid flag — False if outside GB bounds OR suspect
        if "latitude" in col.columns and "longitude" in col.columns:
            bad_lat = ~col["latitude"].between(*GB_LAT) | col["latitude"].isna()
            bad_lon = ~col["longitude"].between(*GB_LON) | col["longitude"].isna()
            bad_coords = bad_lat | bad_lon
            if "coords_suspect" in col.columns:
                bad_coords = bad_coords | col["coords_suspect"]
            col["coords_valid"] = ~bad_coords
            n_bad = bad_coords.sum()
            if n_bad:
                logger.warning(
                    f"  {n_bad:,} rows ({n_bad/len(col):.1%}) have invalid/suspect "
                    f"coordinates — flagged as coords_valid=False (not dropped)"
                )

        # Reconstruct road_name_clean for Stage 1 snap in join.py
        col = _add_road_name_clean(col)

        cleaned["collision"] = col
        logger.info(f"  Collisions cleaned: {len(col):,} rows × {col.shape[1]} cols")

    # --- Vehicles -----------------------------------------------------------
    if "vehicle" in data:
        veh = data["vehicle"].copy()
        # No structural changes needed — normalisation done in ingest
        cleaned["vehicle"] = veh
        logger.info(f"Vehicles: {len(veh):,} rows (no changes)")

    # --- Casualties ---------------------------------------------------------
    if "casualty" in data:
        cas = data["casualty"].copy()
        cleaned["casualty"] = cas
        logger.info(f"Casualties: {len(cas):,} rows (no changes)")

    return cleaned



# ---------------------------------------------------------------------------
# Coordinate correction helpers
# ---------------------------------------------------------------------------

# LSOA centroid file — place in data/raw/stats19/
LSOA_CENTROIDS_PATH = _ROOT / "data/raw/stats19/lsoa_centroids.csv"

# Distance threshold for LSOA validation (metres)
LSOA_DIST_THRESHOLD_M = 10000


def _validate_lsoa_coords(col: pd.DataFrame) -> pd.DataFrame:
    """
    Validate collision coordinates against recorded LSOA population centroid.

    Uses lat/lon (WGS84) haversine distance. This avoids dependence on local
    EPSG:27700 transform behaviour and matches the coordinate source used by
    the snapping pipeline.

    Collisions more than LSOA_DIST_THRESHOLD_M (10km) from their LSOA centroid
    are flagged as coords_suspect=True.

    If the LSOA centroids file is not found, validation is skipped with a warning.
    """
    col["coords_suspect"] = False
    col["coords_corrected"] = False  # No BNG correction applied — lat/lon used directly

    if "lsoa_of_accident_location" not in col.columns:
        logger.warning("  lsoa_of_accident_location not found — LSOA validation skipped")
        return col

    if not LSOA_CENTROIDS_PATH.exists():
        logger.warning(
            f"  LSOA centroids file not found at {LSOA_CENTROIDS_PATH} — "
            "LSOA validation skipped. Download from ONS Open Geography Portal."
        )
        return col

    # Load LSOA centroids — expect WGS84 lat/lon columns
    # ONS file has BNG x/y — convert to lat/lon for consistent comparison
    lsoa = pd.read_csv(
        LSOA_CENTROIDS_PATH,
        usecols=["LSOA21CD", "x", "y"],
        encoding="utf-8-sig",
    )

    # Convert LSOA centroids from BNG to lat/lon
    _bng_to_wgs84 = pyproj.Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)
    lsoa_lon, lsoa_lat = _bng_to_wgs84.transform(lsoa["x"].values, lsoa["y"].values)
    lsoa["lsoa_lat"] = lsoa_lat
    lsoa["lsoa_lon"] = lsoa_lon

    col = col.merge(
        lsoa[["LSOA21CD", "lsoa_lat", "lsoa_lon"]],
        left_on="lsoa_of_accident_location",
        right_on="LSOA21CD",
        how="left"
    )

    has_both = (
        col["latitude"].notna() & col["longitude"].notna() &
        col["lsoa_lat"].notna()
    )

    # Haversine distance (metres) between collision and LSOA centroid
    R = 6_371_000.0
    lat1 = np.radians(col.loc[has_both, "latitude"].values)
    lat2 = np.radians(col.loc[has_both, "lsoa_lat"].values)
    dlat = lat2 - lat1
    dlon = np.radians(
        col.loc[has_both, "longitude"].values -
        col.loc[has_both, "lsoa_lon"].values
    )
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    dist_m = 2 * R * np.arcsin(np.sqrt(a))

    col.loc[has_both, "lsoa_dist_m"] = dist_m
    col.loc[has_both, "coords_suspect"] = dist_m > LSOA_DIST_THRESHOLD_M

    col = col.drop(columns=["LSOA21CD", "lsoa_lat", "lsoa_lon"], errors="ignore")

    n_suspect = col["coords_suspect"].sum()
    logger.info(
        f"  LSOA validation: {n_suspect:,} collisions flagged as coords_suspect "
        f"({n_suspect/len(col):.1%}) | using haversine lat/lon distance"
    )
    return col


def _add_road_name_clean(col: pd.DataFrame) -> pd.DataFrame:
    """
    Reconstruct road name string from first_road_class + first_road_number.

    Examples: class=1, number=62 → 'M62'
              class=3, number=64 → 'A64'
              class=4, number=1234 → 'B1234'
              class=6            → '' (unclassified — no name)

    The result is stored in road_name_clean and used as the Stage 1
    join key in join.py to snap collisions to MRDB/AADF road links
    without relying on spatial proximity alone.
    """
    if "first_road_class" not in col.columns or "first_road_number" not in col.columns:
        logger.warning(
            "first_road_class / first_road_number not found — "
            "road_name_clean will be empty; join.py will fall back to Stage 2 spatial"
        )
        col["road_name_clean"] = ""
        return col

    prefix = col["first_road_class"].map(ROAD_CLASS_PREFIX).fillna("")
    number = col["first_road_number"].fillna(0).astype(int).astype(str)
    number = number.replace("0", "")  # 0 means no road number

    col["road_name_clean"] = (prefix + number).where(
        col["first_road_class"].isin(ROAD_CLASS_PREFIX) & (number != ""),
        other="",
    )

    n_named = (col["road_name_clean"] != "").sum()
    logger.info(
        f"  road_name_clean: {n_named:,} / {len(col):,} collisions have a named road "
        f"({n_named/len(col):.1%}) — remainder will use Stage 2 spatial snap"
    )
    return col


# ---------------------------------------------------------------------------
# AADF
# ---------------------------------------------------------------------------

def clean_aadf(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the AADF bidirectional aggregate.

    Changes applied
    ---------------
    - Filter to full_range years (all study years, not WebTRIS sparse sample)
    - Validate flow columns are non-negative
    - Add road_name_clean (standardised road name for joining to MRDB)
    - Add is_covid flag

    Parameters
    ----------
    df : DataFrame from aggregate_bidirectional() in ingest_aadf.py

    Returns
    -------
    Cleaned DataFrame at count_point_id × year grain.
    """
    logger.info(f"Cleaning AADF: {len(df):,} rows")

    # Keep all study years — AADF is a static download, no API cost to retain
    # all years. TARGET_YEARS (webtris sparse sample) must NOT be used here.
    full_years = cfg["years"]["full_range"]
    before = len(df)
    df = df[df["year"].isin(full_years)].copy()
    logger.info(f"  Year filter → {len(df):,} rows (from {before:,})")

    # Validate flow columns non-negative
    flow_cols = ["all_motor_vehicles", "all_hgvs", "pedal_cycles"]
    for col in flow_cols:
        if col in df.columns:
            n_neg = (df[col] < 0).sum()
            if n_neg:
                logger.warning(f"  {col}: {n_neg} negative values → set to NaN")
                df.loc[df[col] < 0, col] = np.nan

    # Validate proportions are in [0, 1]
    prop_cols = ["hgv_proportion", "lgv_proportion", "cars_proportion", "heavy_vehicle_prop"]
    for col in prop_cols:
        if col in df.columns:
            n_bad = (~df[col].between(0, 1) & df[col].notna()).sum()
            if n_bad:
                logger.warning(f"  {col}: {n_bad} values outside [0,1] → set to NaN")
                df.loc[~df[col].between(0, 1), col] = np.nan

    # Standardise road name for Stage 1 join
    if "road_name" in df.columns:
        df["road_name_clean"] = (
            df["road_name"]
            .str.strip()
            .str.upper()
            .str.replace(r"\s+", "", regex=True)  # 'A 64' → 'A64'
        )
    else:
        df["road_name_clean"] = ""

    # COVID flag
    df["is_covid"] = df["year"].isin(COVID_YEARS)

    logger.info(
        f"AADF cleaned: {len(df):,} rows | "
        f"years: {sorted(df['year'].unique())} | "
        f"count points: {df['count_point_id'].nunique():,}"
    )
    return df


# ---------------------------------------------------------------------------
# WebTRIS
# ---------------------------------------------------------------------------

def clean_webtris(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and aggregate WebTRIS monthly data to annual grain.

    Changes applied
    ---------------
    - Drop duplicate columns: site_id (= siteid), _pull_year (= year)
    - Aggregate 12 monthly rows → 1 annual row per site per year
      (mean of flow metrics, mean of large vehicle percentage)
    - Keep only TARGET_YEARS [2019, 2021, 2023]
    - Add is_covid flag

    Parameters
    ----------
    df : Combined DataFrame from combine_raw() in ingest_webtris.py
         Grain: site × year × month (12 rows per site-year)

    Returns
    -------
    DataFrame at site_id × year grain.
    """
    logger.info(f"Cleaning WebTRIS: {len(df):,} rows")

    # Rename siteid → site_id for consistency
    if "siteid" in df.columns:
        df = df.rename(columns={"siteid": "site_id"})

    # Use _pull_year as authoritative year — always an int set by our code.
    # The API 'year' column may be string or wrong type; drop it after promoting.
    if "_pull_year" in df.columns:
        if "year" in df.columns:
            df = df.drop(columns=["year"])
        df = df.rename(columns={"_pull_year": "year"})
    elif "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # Drop duplicate site_id (siteid already renamed above)
    if "site_id" in df.columns and df.columns.tolist().count("site_id") > 1:
        df = df.loc[:, ~df.columns.duplicated(keep="first")]

    years = sorted(df["year"].dropna().unique()) if "year" in df.columns else "missing"
    logger.info(f"  Year column set — unique years: {years}")

    # Filter to target years
    year_col = "year" if "year" in df.columns else None
    if year_col:
        before = len(df)
        df = df[df[year_col].isin(TARGET_YEARS)].copy()
        logger.info(f"  Year filter → {len(df):,} rows (from {before:,})")

    # Identify flow and percentage columns
    flow_cols = [c for c in df.columns if c.startswith("adt") or c.startswith("awt")]
    pct_cols  = [c for c in flow_cols if "percentage" in c]
    vol_cols  = [c for c in flow_cols if "percentage" not in c]

    if not flow_cols:
        logger.warning("No adt/awt columns found in WebTRIS data — check column names")

    # Coerce flow/percentage columns to numeric — pytris returns them as strings
    for c in vol_cols + pct_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Aggregate monthly → annual
    # Volumes: mean daily flow across months (already a daily average)
    # Percentages: mean across months
    group_cols = ["site_id", "year"] if year_col else ["site_id"]
    non_numeric = [c for c in df.columns if c not in flow_cols + group_cols
                   and df[c].dtype == object and c != "monthname"]

    agg_dict = {c: "mean" for c in vol_cols + pct_cols if c in df.columns}

    # For non-numeric metadata — take first value (stable within site-year)
    for c in non_numeric:
        agg_dict[c] = "first"

    annual = df.groupby(group_cols).agg(agg_dict).reset_index()

    # Rename to project-standard names
    #   adt (all days) → all_*   |   awt (weekdays) → weekday_*
    #   large_vehicle → hgv      |   hour window kept as suffix _Nh
    rename_map = {
        # 24-hour (all-day totals)
        "adt24hour":                    "all_flow",
        "adt24largevehiclepercentage":  "hgv_pct",
        "awt24hour":                    "weekday_flow",
        "awt24largevehiclepercentage":  "hgv_weekday_pct",
        # Sub-day windows used for time-zone derivation
        "adt18hour":                    "all_flow_18h",
        "adt18largevehiclepercentage":  "hgv_pct_18h",
        "awt18hour":                    "weekday_flow_18h",
        "awt18largevehiclepercentage":  "hgv_weekday_pct_18h",
        "adt16hour":                    "all_flow_16h",
        "adt16largevehiclepercentage":  "hgv_pct_16h",
        "awt16hour":                    "weekday_flow_16h",
        "awt16largevehiclepercentage":  "hgv_weekday_pct_16h",
        "adt12hour":                    "all_flow_12h",
        "adt12largevehiclepercentage":  "hgv_pct_12h",
        "awt12hour":                    "weekday_flow_12h",
        "awt12largevehiclepercentage":  "hgv_weekday_pct_12h",
    }
    annual = annual.rename(columns={k: v for k, v in rename_map.items() if k in annual.columns})

    # Derived weekend flow: (7 × all_flow - 5 × weekday_flow) / 2
    # Guard: negative values indicate data inconsistency → set to NaN
    if "all_flow" in annual.columns and "weekday_flow" in annual.columns:
        annual["weekend_flow"] = (
            7 * annual["all_flow"] - 5 * annual["weekday_flow"]
        ) / 2
        n_neg = (annual["weekend_flow"] < 0).sum()
        if n_neg:
            logger.warning(
                f"  weekend_flow: {n_neg} negative rows set to NaN "
                f"(weekday_flow > all_flow — likely data artefact)"
            )
            annual.loc[annual["weekend_flow"] < 0, "weekend_flow"] = np.nan

    # COVID flag
    if "year" in annual.columns:
        annual["is_covid"] = annual["year"].isin(COVID_YEARS)

    # Time-zone per-hour flow features
    annual = _derive_time_zones(annual)

    logger.info(
        f"WebTRIS cleaned: {len(annual):,} rows "
        f"(site × year) | sites: {annual['site_id'].nunique():,} | "
        f"years: {sorted(annual['year'].unique()) if 'year' in annual.columns else 'n/a'}"
    )
    return annual


def _derive_time_zones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive per-hour flow rates for four time zones by differencing the
    12/16/18/24-hour window columns in the WebTRIS annual reports.

    Zone definitions (stacked outward from core daytime)
    ─────────────────────────────────────────────────────
    Zone            Hours  Derivation                      Approx clock
    Peak              12   all_flow_12h / 12               07:00–19:00
    Pre-peak           4   (all_flow_16h − 12h) / 4        05–07 + 19–21
    Pre-offpeak        2   (all_flow_18h − 16h) / 2        04–05 + 21–22
    Offpeak            6   (all_flow   − 18h) / 6          22:00–04:00

    Output columns (vehicles per hour, all-days basis)
    ───────────────────────────────────────────────────
    flow_ph_core_daytime, flow_ph_shoulder, flow_ph_late_evening, flow_ph_overnight
    hgv_ph_core_daytime,  hgv_ph_shoulder,  hgv_ph_late_evening,  hgv_ph_overnight
    core_overnight_ratio  — flow_ph_core_daytime / flow_ph_overnight
    """
    df = df.copy()

    needed = ["all_flow", "all_flow_18h", "all_flow_16h", "all_flow_12h"]
    if any(c not in df.columns for c in needed):
        logger.warning(
            "Time-zone derivation skipped — missing columns: "
            + str([c for c in needed if c not in df.columns])
        )
        return df

    # Zone vehicle totals (full window, not per-hour)
    zone_peak       = df["all_flow_12h"]
    zone_prepeak    = df["all_flow_16h"] - df["all_flow_12h"]
    zone_preoffpeak = df["all_flow_18h"] - df["all_flow_16h"]
    zone_offpeak    = df["all_flow"]     - df["all_flow_18h"]

    # Per-hour flow rates
    df["flow_ph_core_daytime"]       = zone_peak       / 12
    df["flow_ph_shoulder"]    = zone_prepeak     / 4
    df["flow_ph_late_evening"] = zone_preoffpeak  / 2
    df["flow_ph_overnight"]    = zone_offpeak     / 6

    # HGV per-hour — derive by differencing *cumulative HGV counts*, not by
    # applying cumulative HGV% to marginal flow bands (which mixes cumulative
    # percentages with incremental flows and under-counts by ~7%).
    #
    # Correct method:
    #   cumulative_hgv_Xh = all_flow_Xh × hgv_pct_Xh / 100
    #   zone_hgv_band     = cumulative_hgv_Xh − cumulative_hgv_prev
    #   hgv_ph_band       = zone_hgv_band / hours_in_band
    hgv_needed = ["hgv_pct", "hgv_pct_18h", "hgv_pct_16h", "hgv_pct_12h"]
    if all(c in df.columns for c in hgv_needed):
        cum_hgv_12h = df["all_flow_12h"] * df["hgv_pct_12h"] / 100
        cum_hgv_16h = df["all_flow_16h"] * df["hgv_pct_16h"] / 100
        cum_hgv_18h = df["all_flow_18h"] * df["hgv_pct_18h"] / 100
        cum_hgv_24h = df["all_flow"]     * df["hgv_pct"]     / 100

        zone_hgv_peak       = cum_hgv_12h
        zone_hgv_prepeak    = cum_hgv_16h - cum_hgv_12h
        zone_hgv_preoffpeak = cum_hgv_18h - cum_hgv_16h
        zone_hgv_offpeak    = cum_hgv_24h - cum_hgv_18h

        df["hgv_ph_core_daytime"]       = zone_hgv_peak       / 12
        df["hgv_ph_shoulder"]    = zone_hgv_prepeak     / 4
        df["hgv_ph_late_evening"] = zone_hgv_preoffpeak  / 2
        df["hgv_ph_overnight"]    = zone_hgv_offpeak     / 6

        # Sanity check: reconstructed daily HGV should equal cum_hgv_24h
        recon = zone_hgv_peak + zone_hgv_prepeak + zone_hgv_preoffpeak + zone_hgv_offpeak
        recon_ratio = (recon / cum_hgv_24h.replace(0, np.nan)).dropna()
        n_bad = ((recon_ratio < 0.98) | (recon_ratio > 1.02)).sum()
        if n_bad:
            logger.warning(
                f"  HGV time-zone: {n_bad} rows outside 98–102% reconciliation band"
            )
    else:
        logger.warning("HGV time-zone columns skipped — missing: "
                       + str([c for c in hgv_needed if c not in df.columns]))

    # Peakiness ratio — how much more intense is peak vs night
    df["core_overnight_ratio"] = (
        df["flow_ph_core_daytime"] / df["flow_ph_overnight"].replace(0, np.nan)
    )

    new_cols = [c for c in df.columns
                if c.startswith(("flow_ph_", "hgv_ph_", "peak_offpeak"))]
    logger.info(
        f"  Time-zone features derived: {len(new_cols)} columns | "
        f"{df[new_cols].notna().all(axis=1).sum():,} / {len(df):,} rows fully populated"
    )
    return df


# ---------------------------------------------------------------------------
# MRDB
# ---------------------------------------------------------------------------

def clean_mrdb(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Clean the MRDB GeoDataFrame and prepare for spatial joining.

    Changes applied
    ---------------
    - Add link_id: stable integer ID for each road link
    - Add road_name_clean: standardised road name for Stage 1 attribute join
    - Validate geometry (drop null/invalid geometries)

    Note: the MRDB shapefile only contains CP_Number, RoadNumber, geometry.
    Road type and link length are sourced from AADF in join.py.

    Parameters
    ----------
    gdf : GeoDataFrame from load_mrdb() in ingest_mrdb.py

    Returns
    -------
    GeoDataFrame with link_id and road_name_clean added.
    """
    logger.info(f"Cleaning MRDB: {len(gdf):,} road links")

    gdf = gdf.copy()

    # Validate geometry
    null_geom = gdf.geometry.isna()
    if null_geom.any():
        logger.warning(f"  {null_geom.sum()} null geometries — dropping")
        gdf = gdf[~null_geom]

    invalid_geom = ~gdf.geometry.is_valid
    if invalid_geom.any():
        logger.info(f"  Fixing {invalid_geom.sum()} invalid geometries with buffer(0)")
        gdf.loc[invalid_geom, "geometry"] = gdf.loc[invalid_geom, "geometry"].buffer(0)

    # Stable integer link ID (index-based, 1-indexed)
    gdf = gdf.reset_index(drop=True)
    gdf["link_id"] = gdf.index + 1

    # Standardise road name: 'M62', 'A64', 'B1234' etc.
    road_col = "road_name" if "road_name" in gdf.columns else (
        "RoadNumber" if "RoadNumber" in gdf.columns else None
    )
    if road_col:
        gdf["road_name_clean"] = (
            gdf[road_col]
            .fillna("")
            .str.strip()
            .str.upper()
            .str.replace(r"\s+", "", regex=True)
        )
        # Ensure road_name column exists with standard name
        if road_col != "road_name":
            gdf = gdf.rename(columns={road_col: "road_name"})
    else:
        logger.warning("No road name column found in MRDB")
        gdf["road_name_clean"] = ""

    # count_point_id — normalise to string for joining to AADF
    cp_col = "count_point_id" if "count_point_id" in gdf.columns else (
        "CP_Number" if "CP_Number" in gdf.columns else None
    )
    if cp_col:
        gdf["count_point_id"] = gdf[cp_col].astype(str).str.strip()
        gdf["count_point_id"] = gdf["count_point_id"].replace("nan", np.nan)
        if cp_col != "count_point_id":
            gdf = gdf.drop(columns=[cp_col])
        n_with_cp = gdf["count_point_id"].notna().sum()
        logger.info(
            f"  count_point_id: {n_with_cp:,} / {len(gdf):,} links have a CP number"
        )

    logger.info(
        f"MRDB cleaned: {len(gdf):,} links | "
        f"road names: {gdf['road_name_clean'].nunique():,} unique"
    )
    return gdf


# ---------------------------------------------------------------------------
# Save helpers
# ---------------------------------------------------------------------------

def save_cleaned(
    data: dict | pd.DataFrame | gpd.GeoDataFrame,
    name: str,
    output_folder: str | Path = None,
) -> None:
    """
    Save cleaned data to data/processed/<name>/.

    Parameters
    ----------
    data : dict of DataFrames (stats19), single DataFrame (aadf/webtris),
           or GeoDataFrame (mrdb)
    name : source name — 'stats19', 'aadf', 'webtris', 'mrdb'
    output_folder : defaults to data/processed/<name>/
    """
    if output_folder is None:
        output_folder = _ROOT / cfg["paths"]["processed"] / name
    out = Path(output_folder)
    out.mkdir(parents=True, exist_ok=True)

    if isinstance(data, dict):
        for table, df in data.items():
            path = out / f"{table}_clean.parquet"
            df.to_parquet(path, index=False)
            logger.info(f"  Saved {name}/{table}_clean.parquet ({len(df):,} rows)")
    elif isinstance(data, gpd.GeoDataFrame):
        path = out / f"{name}_clean.parquet"
        data.to_parquet(path, index=False)
        logger.info(f"  Saved {name}_clean.parquet ({len(data):,} rows)")
    else:
        path = out / f"{name}_clean.parquet"
        data.to_parquet(path, index=False)
        logger.info(f"  Saved {name}_clean.parquet ({len(data):,} rows)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Load all processed parquets, clean each source, and save to
    data/processed/<source>/  as *_clean.parquet files.
    """

    from road_risk.ingest.ingest_aadf import aggregate_bidirectional, load_aadf
    from road_risk.ingest.legacy_ingest_mrdb import load_mrdb
    from road_risk.ingest.ingest_stats19 import load_stats19

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )

    # --- STATS19 ------------------------------------------------------------
    logger.info("=== STATS19 ===")
    stats19_raw = load_stats19(
        _ROOT / "data/raw/stats19",
        years=list(range(2015, 2025)),   # 2015-2024 only — pre-2015 has unreliable coords
    )
    stats19_clean = clean_stats19(stats19_raw)
    save_cleaned(stats19_clean, "stats19")

    # --- AADF ---------------------------------------------------------------
    logger.info("=== AADF ===")
    aadf_raw = load_aadf(_ROOT / "data/raw/aadf")
    aadf_agg = aggregate_bidirectional(aadf_raw)
    aadf_clean = clean_aadf(aadf_agg)
    save_cleaned(aadf_clean, "aadf")

    # --- WebTRIS ------------------------------------------------------------
    logger.info("=== WebTRIS ===")
    webtris_chunks = sorted(
        (_ROOT / "data/raw/webtris").glob("site_*_*.parquet")
    )
    if webtris_chunks:
        from road_risk.ingest.ingest_webtris import combine_raw
        webtris_raw = combine_raw(_ROOT / "data/raw/webtris")
        webtris_clean = clean_webtris(webtris_raw)

        # Attach site coordinates — lat/lon lives in sites.parquet,
        # not in the per-site traffic chunks that combine_raw() loads.
        sites_path = _ROOT / "data/raw/webtris/sites.parquet"
        if sites_path.exists():
            sites = pd.read_parquet(sites_path, columns=["site_id", "latitude", "longitude"])
            sites["site_id"] = sites["site_id"].astype(webtris_clean["site_id"].dtype)
            webtris_clean = webtris_clean.merge(sites, on="site_id", how="left")
            n_with_coords = webtris_clean["latitude"].notna().sum()
            logger.info(
                f"  Site coordinates attached: {n_with_coords:,} / "
                f"{len(webtris_clean):,} rows"
            )
        else:
            logger.warning("sites.parquet not found — WebTRIS lat/lon will be missing")

        save_cleaned(webtris_clean, "webtris")
    else:
        logger.warning("No WebTRIS chunks found — skipping")

    # --- MRDB ---------------------------------------------------------------
    logger.info("=== MRDB ===")
    mrdb_raw = load_mrdb(_ROOT / "data/raw/shapefiles")
    mrdb_clean = clean_mrdb(mrdb_raw)
    save_cleaned(mrdb_clean, "mrdb")

    logger.info("=== Cleaning complete ===")


if __name__ == "__main__":
    main()
