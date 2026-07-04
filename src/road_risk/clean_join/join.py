"""
join.py
-------
Spatial and attribute joins across all four data sources.

The final output is a road_link × year table — one row per OS Open Roads
link per year — with collision counts, traffic volume, and vehicle mix
aggregated onto each link.

Pipeline
--------
1. snap_collisions_to_roads()
      Stage 1 — attribute match: reconstruct road name from
      first_road_class + first_road_number, match to OpenRoads road_name_clean.
      Then nearest-neighbour *within that named road only*.

      Stage 2 — spatial fallback: pure nearest-neighbour for collisions
      that didn't match in Stage 1 (unclassified roads, bad road numbers).
      Applies a 100m distance cap; beyond that snap_distance_m is still
      recorded but snap_method = 'unmatched'.

2. build_road_features()
      Joins AADF count point data onto OS Open Roads links via spatial
      nearest-neighbour. WebTRIS sensor data joined to AADF count points
      via spatial nearest-neighbour (no shared key).

3. build_road_link_annual()
      Aggregates snapped collisions onto road links per year.
      Joins road features (AADF + WebTRIS) onto the collision aggregates.
      Returns the final analysis table at road_link × year grain.

Key join columns
----------------
OpenRoads road_name_clean  -> STATS19 road_name_clean  (Stage 1)
OpenRoads geometry         -> STATS19 lat/lon          (Stage 2 spatial)
AADF      lat/lon          -> OpenRoads link centroid  (spatial, nearest)
AADF      lat/lon          -> WebTRIS lat/lon          (spatial, nearest)
"""

import argparse
import logging
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from road_risk.config import _ROOT, cfg

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# CRS
WGS84 = "EPSG:4326"

# Maximum distance for WebTRIS → AADF spatial join.
# Beyond this, a WebTRIS sensor is too far to represent the count point's
# road type. 5km is generous for motorway corridors; most valid matches
# are < 2km.
WEBTRIS_MAX_DIST_M = 5_000
BNG = "EPSG:27700"  # British National Grid — metres, used for distance calcs

# Stage 2 spatial fallback distance cap (metres)
SPATIAL_CAP_M = 100

# Minimum collision count per link-year to include in model features
MIN_COLLISIONS = 1

# AADF columns to carry through to the road features table
AADF_FEATURE_COLS = [
    "count_point_id",
    "year",
    "road_name",
    "road_type",
    "latitude",
    "longitude",
    "link_length_km",
    "all_motor_vehicles",
    "all_hgvs",
    "hgv_proportion",
    "lgv_proportion",
    "cars_proportion",
    "heavy_vehicle_prop",
    "estimation_method",
    "is_covid",
]

# WebTRIS columns to carry through to road_link_annual
WEBTRIS_FEATURE_COLS = [
    "site_id",
    "year",
    # 24-hour totals
    "all_flow",
    "weekday_flow",
    "weekend_flow",
    "hgv_pct",
    "hgv_weekday_pct",
    # Time-zone per-hour flow rates (all-days basis)
    "flow_ph_core_daytime",
    "flow_ph_shoulder",
    "flow_ph_late_evening",
    "flow_ph_overnight",
    # Time-zone HGV per-hour rates
    "hgv_ph_core_daytime",
    "hgv_ph_shoulder",
    "hgv_ph_late_evening",
    "hgv_ph_overnight",
    # Derived ratio
    "core_overnight_ratio",
]

ROAD_FEATURE_AUDIT_COLS = [
    "aadf_snap_distance_m",
    "aadf_join_method",
    "webtris_snap_distance_m",
]

EXPECTED_MODEL_YEARS = list(range(2015, 2025))


# ---------------------------------------------------------------------------
# 1. Snap collisions to road links
# ---------------------------------------------------------------------------


def snap_collisions_to_roads(
    collisions: pd.DataFrame,
    openroads: gpd.GeoDataFrame,
    spatial_cap_m: float = SPATIAL_CAP_M,
) -> gpd.GeoDataFrame:
    """
    Snap STATS19 collisions to OS Open Roads links using a two-stage approach.

    OS Open Roads covers ALL classified roads in GB, giving full coverage
    for collisions on B-roads and minor roads that MRDB misses.

    Stage 1 — Attribute match (high confidence)
        Match collision road_name_clean to OpenRoads road_name_clean.
        Then find the nearest link *on that named road* to the collision
        coordinates. Prevents snapping an M62 collision to a nearby A-road.

    Stage 2 — Spatial fallback
        For unmatched collisions (unclassified roads, missing road numbers),
        find the nearest OpenRoads link overall within spatial_cap_m.

    Parameters
    ----------
    collisions  : cleaned collision DataFrame from clean_stats19()
                  Must have: latitude, longitude, road_name_clean, coords_valid
    openroads   : OS Open Roads GeoDataFrame from load_openroads()
                  Must have: link_id, road_name_clean, geometry (WGS84)
    spatial_cap_m : distance cap for Stage 2 in metres (default 100m)

    Returns
    -------
    GeoDataFrame at collision grain with added columns:
      link_id          : matched OpenRoads link ID
      snap_distance_m  : distance from collision to snapped link (metres)
      snap_method      : 'attribute', 'spatial', or 'unmatched'
    """
    logger.info(
        f"Snapping {len(collisions):,} collisions to {len(openroads):,} OS Open Roads links"
    )

    # --- Prepare collisions GeoDataFrame ------------------------------------
    # Only snap collisions with valid coordinates
    valid = (
        collisions["coords_valid"].fillna(False)
        if "coords_valid" in collisions.columns
        else pd.Series(True, index=collisions.index)
    )

    coll_gdf = gpd.GeoDataFrame(
        collisions[valid].copy(),
        geometry=gpd.points_from_xy(
            collisions.loc[valid, "longitude"],
            collisions.loc[valid, "latitude"],
        ),
        crs=WGS84,
    )

    # Project to BNG for distance calculations in metres
    coll_bng = coll_gdf.to_crs(BNG)
    roads_bng = openroads.to_crs(BNG)

    # Output columns
    coll_bng["link_id"] = pd.NA
    coll_bng["snap_distance_m"] = np.nan
    coll_bng["snap_method"] = "unmatched"

    # --- Stage 1: Attribute match -------------------------------------------
    named = coll_bng[coll_bng["road_name_clean"].notna() & (coll_bng["road_name_clean"] != "")]
    logger.info(f"  Stage 1: {len(named):,} collisions have a named road")

    stage1_matched = 0
    for road_name, group in named.groupby("road_name_clean"):
        road_links = roads_bng[roads_bng["road_name_clean"] == road_name]
        if road_links.empty:
            continue
        matched = _nearest_link(group, road_links)
        coll_bng.loc[matched.index, "link_id"] = matched["link_id"].values
        coll_bng.loc[matched.index, "snap_distance_m"] = matched["snap_distance_m"].values
        coll_bng.loc[matched.index, "snap_method"] = "attribute"
        stage1_matched += len(matched)

    logger.info(
        f"  Stage 1 matched: {stage1_matched:,} / {len(named):,} "
        f"({stage1_matched / max(len(named), 1):.1%})"
    )

    # --- Stage 2: Spatial fallback ------------------------------------------
    unmatched = coll_bng[coll_bng["snap_method"] == "unmatched"]
    logger.info(f"  Stage 2: {len(unmatched):,} collisions for spatial fallback")

    if not unmatched.empty:
        matched2 = _nearest_link(unmatched, roads_bng)
        within_cap = matched2["snap_distance_m"] <= spatial_cap_m
        n_within = within_cap.sum()

        coll_bng.loc[matched2.index, "link_id"] = matched2["link_id"].values
        coll_bng.loc[matched2.index, "snap_distance_m"] = matched2["snap_distance_m"].values
        coll_bng.loc[matched2[within_cap].index, "snap_method"] = "spatial"

        logger.info(
            f"  Stage 2 matched within {spatial_cap_m}m: {n_within:,} / {len(unmatched):,} "
            f"({n_within / max(len(unmatched), 1):.1%})"
        )

    # --- Reproject back to WGS84 and add invalid-coord rows ----------------
    coll_out = coll_bng.to_crs(WGS84)

    # Append rows with invalid coordinates (unsnappable — no link_id)
    if (~valid).any():
        invalid_rows = collisions[~valid].copy()
        invalid_rows["link_id"] = pd.NA
        invalid_rows["snap_distance_m"] = np.nan
        invalid_rows["snap_method"] = "invalid_coords"
        invalid_gdf = gpd.GeoDataFrame(invalid_rows, geometry=[None] * len(invalid_rows), crs=WGS84)
        coll_out = pd.concat([coll_out, invalid_gdf], ignore_index=True)

    # Summary
    method_counts = coll_out["snap_method"].value_counts()
    logger.info(f"  Snap summary:\n{method_counts.to_string()}")

    return coll_out


def _nearest_link(
    points: gpd.GeoDataFrame,
    links: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """
    For each point, find the nearest link and return link_id + distance.

    Uses geopandas sjoin_nearest which builds an STRtree index internally —
    efficient for large datasets.

    Both inputs must be in the same projected CRS (BNG recommended for metres).

    Returns
    -------
    DataFrame indexed like `points` with columns: link_id, snap_distance_m
    """
    if points.empty or links.empty:
        return pd.DataFrame(
            {"link_id": pd.NA, "snap_distance_m": np.nan},
            index=points.index,
        )

    joined = gpd.sjoin_nearest(
        points[["geometry"]],
        links[["link_id", "geometry"]],
        how="left",
        distance_col="snap_distance_m",
    )

    # sjoin_nearest can produce duplicates if equidistant — keep first
    joined = joined[~joined.index.duplicated(keep="first")]

    return joined[["link_id", "snap_distance_m"]]


# ---------------------------------------------------------------------------
# 2. Build road features (AADF + WebTRIS per OS Open Roads link per year)
# ---------------------------------------------------------------------------


def build_road_features(
    openroads: gpd.GeoDataFrame,
    aadf: pd.DataFrame,
    webtris: pd.DataFrame | None = None,
    aadf_snap_cap_m: float = 2000,
) -> pd.DataFrame:
    """
    Join AADF traffic features onto OS Open Roads links via spatial
    nearest-neighbour, then attach WebTRIS sensor features where available.

    AADF snap cap of 2km applied — links further than this from any count
    point get NaN traffic features rather than a meaningless distant match.

    Parameters
    ----------
    openroads      : OS Open Roads GeoDataFrame (link_id, geometry in WGS84)
    aadf           : cleaned AADF DataFrame (count_point_id, year, flow cols, lat/lon)
    webtris        : cleaned WebTRIS DataFrame (site_id, year, flow cols, lat/lon)
    aadf_snap_cap_m: max distance (metres) for AADF→road spatial join (default 2km)

    Returns
    -------
    DataFrame at link_id × year grain with traffic features.
    """
    logger.info("Building road features (OpenRoads × AADF × WebTRIS) — spatial joins")

    # --- WebTRIS → AADF spatial join ----------------------------------------
    if webtris is not None and not webtris.empty:
        aadf = _attach_webtris_to_aadf(aadf, webtris)
        logger.info("  WebTRIS features attached to AADF count points")

    # Trim AADF to feature columns — include any WebTRIS columns that were
    # attached by _attach_webtris_to_aadf() (matched by WEBTRIS_FEATURE_COLS).
    # Deduplicate while preserving order (year/site_id appear in both lists).
    webtris_cols = [c for c in WEBTRIS_FEATURE_COLS if c in aadf.columns]
    seen: set[str] = set()
    aadf_keep = []
    for c in AADF_FEATURE_COLS + webtris_cols:
        if c in aadf.columns and c not in seen:
            aadf_keep.append(c)
            seen.add(c)
    aadf_trim = aadf[aadf_keep].copy()

    # --- AADF → OpenRoads: spatial join per year ----------------------------
    logger.info(
        f"  Spatial AADF join: {len(openroads):,} links × "
        f"{aadf_trim['year'].nunique()} years (cap: {aadf_snap_cap_m}m)"
    )

    aadf_gdf = gpd.GeoDataFrame(
        aadf_trim,
        geometry=gpd.points_from_xy(aadf_trim["longitude"], aadf_trim["latitude"]),
        crs=WGS84,
    ).to_crs(BNG)

    roads_bng = openroads.to_crs(BNG).copy()
    roads_centroids = roads_bng[["link_id"]].copy()
    roads_centroids["geometry"] = roads_bng.geometry.centroid
    roads_centroids = gpd.GeoDataFrame(roads_centroids, geometry="geometry", crs=BNG)

    spatial_rows = []
    for year in sorted(aadf_trim["year"].unique()):
        aadf_yr = aadf_gdf[aadf_gdf["year"] == year].copy()
        if aadf_yr.empty:
            continue

        aadf_yr = aadf_yr.drop(columns=["link_id"], errors="ignore")

        joined = gpd.sjoin_nearest(
            roads_centroids,
            aadf_yr,
            how="left",
            distance_col="aadf_snap_distance_m",
        )
        joined = joined[~joined.index.duplicated(keep="first")]

        # Nullify features beyond snap cap — distant match is not meaningful
        feature_cols = [c for c in aadf_keep if c not in ["latitude", "longitude", "year"]]
        beyond_cap = joined["aadf_snap_distance_m"] > aadf_snap_cap_m
        n_beyond = beyond_cap.sum()
        if n_beyond:
            # Cast bool columns to object first to avoid FutureWarning
            for fc in feature_cols:
                if fc in joined.columns and joined[fc].dtype == bool:
                    joined[fc] = joined[fc].astype(object)
            joined.loc[beyond_cap, feature_cols] = np.nan
            logger.info(
                f"    {year}: {n_beyond:,} links beyond {aadf_snap_cap_m}m cap → "
                f"AADF features set to NaN"
            )

        # --- Street name fallback for links still beyond cap ----------------
        # For OpenRoads links with a street_name_clean, try matching to AADF
        # road_name_clean (normalised) — recovers named roads without numbers.
        if "street_name_clean" in openroads.columns and "road_name_clean" in aadf_trim.columns:
            still_beyond = (
                beyond_cap
                & (
                    openroads.set_index("link_id")
                    .loc[joined["link_id"].values, "street_name_clean"]
                    .values
                    != ""
                )
                if "link_id" in joined.columns
                else beyond_cap
            )

            aadf_named = (
                aadf_yr[aadf_yr.get("road_name_clean", pd.Series("", index=aadf_yr.index)) != ""]
                if "road_name_clean" in aadf_yr.columns
                else pd.DataFrame()
            )

            if still_beyond.any() and not aadf_named.empty:
                # Normalise AADF road_name for matching
                aadf_name_map = aadf_yr.assign(
                    aadf_name_norm=aadf_yr.get(
                        "road_name_clean", pd.Series("", index=aadf_yr.index)
                    )
                    .str.upper()
                    .str.replace(r"[^A-Z0-9]", "", regex=True)
                ).set_index("aadf_name_norm")
                links_beyond = joined[still_beyond]["link_id"]
                or_streets = openroads.set_index("link_id")["street_name_clean"]
                n_name_matched = 0
                for lid in links_beyond:
                    street = or_streets.get(lid, "")
                    if street and street in aadf_name_map.index:
                        row = aadf_name_map.loc[street]
                        if isinstance(row, pd.DataFrame):
                            row = row.iloc[0]
                        for fc in feature_cols:
                            if fc in row.index:
                                joined.loc[joined["link_id"] == lid, fc] = row[fc]
                        joined.loc[joined["link_id"] == lid, "aadf_snap_distance_m"] = 0
                        joined.loc[joined["link_id"] == lid, "aadf_join_method"] = "name_match"
                        n_name_matched += 1
                if n_name_matched:
                    logger.info(
                        f"    {year}: {n_name_matched:,} additional links matched via street name"
                    )

        joined["aadf_join_method"] = joined.get(
            "aadf_join_method", pd.Series("spatial", index=joined.index)
        ).fillna("spatial")

        n_matched = (~beyond_cap).sum()
        logger.info(
            f"    {year}: {n_matched:,} / {len(roads_centroids):,} links matched "
            f"(mean dist: {joined.loc[~beyond_cap, 'aadf_snap_distance_m'].mean():.0f}m)"
        )
        spatial_rows.append(joined.drop(columns=["geometry", "index_right"], errors="ignore"))

    if not spatial_rows:
        logger.error("No AADF data joined — check aadf_clean.parquet exists and has rows")
        return pd.DataFrame()

    road_features = pd.concat(spatial_rows, ignore_index=True)
    logger.info(
        f"Road features built: {len(road_features):,} link × year rows | "
        f"links: {road_features['link_id'].nunique():,}"
    )
    return road_features


def _attach_webtris_to_aadf(
    aadf: pd.DataFrame,
    webtris: pd.DataFrame,
) -> pd.DataFrame:
    """
    Spatially match WebTRIS sites to AADF count points (nearest neighbour
    per year), then left-join WebTRIS features onto AADF.

    Both datasets have lat/lon. The join is done per year so a 2019 WebTRIS
    reading only attaches to the 2019 AADF row.
    """
    if "latitude" not in webtris.columns or "longitude" not in webtris.columns:
        logger.warning(
            "WebTRIS data has no lat/lon — cannot spatial-join to AADF. "
            "WebTRIS features will be missing."
        )
        return aadf

    wt_cols = [c for c in WEBTRIS_FEATURE_COLS if c in webtris.columns]

    wt_gdf = gpd.GeoDataFrame(
        webtris,
        geometry=gpd.points_from_xy(webtris["longitude"], webtris["latitude"]),
        crs=WGS84,
    ).to_crs(BNG)

    aadf_gdf = gpd.GeoDataFrame(
        aadf,
        geometry=gpd.points_from_xy(aadf["longitude"], aadf["latitude"]),
        crs=WGS84,
    ).to_crs(BNG)

    result_frames = []
    for year in aadf["year"].unique():
        aadf_yr = aadf_gdf[aadf_gdf["year"] == year].copy()
        wt_yr = (
            wt_gdf[wt_gdf["year"] == year][wt_cols + ["geometry"]]
            if "year" in wt_gdf.columns
            else wt_gdf[wt_cols + ["geometry"]]
        )

        if wt_yr.empty:
            result_frames.append(aadf_yr.drop(columns=["geometry"]))
            continue

        joined = gpd.sjoin_nearest(
            aadf_yr,
            wt_yr.drop(columns=["year"] if "year" in wt_yr.columns else []),
            how="left",
            max_distance=WEBTRIS_MAX_DIST_M,
            distance_col="webtris_snap_distance_m",
        )
        joined = joined[~joined.index.duplicated(keep="first")]

        # Null out WebTRIS features for AADF points beyond the distance cap.
        # sjoin_nearest with max_distance sets index_right=NaN for unmatched
        # rows but may still carry stale column values — explicitly null them.
        wt_feature_cols = [c for c in wt_cols if c not in ["year", "latitude", "longitude"]]
        far = joined["webtris_snap_distance_m"].isna()
        if far.any():
            joined.loc[far, wt_feature_cols] = float("nan")
            logger.info(
                f"  WebTRIS year {year}: {far.sum():,} / {len(joined):,} "
                f"AADF points beyond {WEBTRIS_MAX_DIST_M / 1000:.0f}km cap "
                f"— WebTRIS features set to NaN"
            )

        result_frames.append(joined.drop(columns=["geometry", "index_right"], errors="ignore"))

    return pd.concat(result_frames, ignore_index=True)


# ---------------------------------------------------------------------------
# 3. Build road_link × year final table
# ---------------------------------------------------------------------------


def build_road_link_annual(
    collisions_snapped: gpd.GeoDataFrame,
    road_features: pd.DataFrame | None,
    openroads: gpd.GeoDataFrame,
    road_features_path: str | Path | None = None,
) -> pd.DataFrame:
    """
    Aggregate snapped collisions onto OS Open Roads links per year,
    then join road features to produce the final analysis table.

    Output grain: road_link × year
    """
    logger.info("Building road_link × year table")

    col = collisions_snapped.copy()

    if "collision_year" in col.columns:
        col["year"] = col["collision_year"]
    elif "date" in col.columns:
        col["year"] = pd.to_datetime(col["date"], errors="coerce").dt.year

    snapped = col[col["snap_method"].isin(["attribute", "spatial", "weighted"])].copy()

    # Snap quality filter — remove low-confidence matches that add noise to the model.
    # With correct coordinates, the snap distance distribution has a natural break
    # at score ~0.6 / distance ~100m. Below this threshold snaps are likely landing
    # on the wrong road (parallel minor road, opposite carriageway, etc).
    # Threshold chosen so retained count (~40k) matches historical high-quality baseline.
    # Analysis (April 2026): score>0.6 retains 51.8% of matches, score<0.6 are
    # predominantly far snaps (>100m) on Unclassified/Unknown roads.
    if "snap_score" in snapped.columns:
        n_before = len(snapped)
        snapped = snapped[snapped["snap_score"] >= 0.6]
        n_after = len(snapped)
        logger.info(
            f"  Snap quality filter (score>=0.6): "
            f"{n_after:,} / {n_before:,} collisions retained "
            f"({n_after / n_before:.1%})"
        )

    logger.info(
        f"  Using {len(snapped):,} / {len(col):,} snapped collisions "
        f"({len(snapped) / len(col):.1%})"
    )

    if "vehicle_type" in snapped.columns:
        hgv_codes = {19, 20, 21}
        snapped["involves_hgv"] = snapped["vehicle_type"].isin(hgv_codes)
    else:
        snapped["involves_hgv"] = False

    # Derive binary flags for contextual aggregation before groupby.
    # light_conditions: 1=daylight, 4/5/6/7=darkness variants.
    if "light_conditions" in snapped.columns:
        snapped["_is_dark"] = snapped["light_conditions"].isin([4, 5, 6, 7])
    else:
        snapped["_is_dark"] = False

    # urban_or_rural_area: 1=urban, 2=rural, 3=unallocated.
    if "urban_or_rural_area" in snapped.columns:
        snapped["_is_urban"] = snapped["urban_or_rural_area"] == 1
    else:
        snapped["_is_urban"] = False

    # junction_detail: 0=not at junction; any other positive value = at junction.
    if "junction_detail" in snapped.columns:
        snapped["_at_junction"] = snapped["junction_detail"].gt(0)
    else:
        snapped["_at_junction"] = False

    # pedestrian_crossing: 0 or -1 = none within 50m; positive = crossing present.
    if "pedestrian_crossing" in snapped.columns:
        snapped["_near_crossing"] = snapped["pedestrian_crossing"].gt(0)
    else:
        snapped["_near_crossing"] = False

    agg = (
        snapped.groupby(["link_id", "year"])
        .agg(
            collision_count=("collision_index", "count"),
            fatal_count=("collision_severity", lambda x: (x == 1).sum()),
            serious_count=("collision_severity", lambda x: (x == 2).sum()),
            slight_count=("collision_severity", lambda x: (x == 3).sum()),
            casualty_count=("number_of_casualties", "sum"),
            hgv_collision_count=("involves_hgv", "sum"),
            mean_vehicles_per_collision=("number_of_vehicles", "mean"),
            pct_dark=("_is_dark", "mean"),
            pct_urban=("_is_urban", "mean"),
            pct_junction=("_at_junction", "mean"),
            pct_near_crossing=("_near_crossing", "mean"),
            mean_speed_limit=("speed_limit", lambda x: x[x > 0].mean()),
        )
        .reset_index()
    )

    logger.info(
        f"  Collision aggregates: {len(agg):,} link × year rows | "
        f"links: {agg['link_id'].nunique():,} | years: {sorted(agg['year'].unique())}"
    )

    # --- Join road features -------------------------------------------------
    if road_features is None:
        if road_features_path is None:
            raise ValueError("road_features or road_features_path is required")
        road_feat = _load_road_features_for_annual_keys(road_features_path, agg)
    else:
        road_feat = _filter_road_features_for_annual(road_features, agg)

    result = agg.merge(road_feat, on=["link_id", "year"], how="left", validate="one_to_one")

    # Attach OpenRoads road metadata — single road_name, no duplicates
    or_meta = openroads[
        [
            "link_id",
            "road_name",
            "road_name_clean",
            "road_classification",
            "road_function",
            "form_of_way",
            "link_length_km",
            "is_trunk",
            "is_primary",
        ]
    ].copy()
    # Drop link_length_km from result if already there from AADF to avoid dupe
    if "link_length_km" in result.columns:
        or_meta = or_meta.drop(columns=["link_length_km"])

    result = result.merge(or_meta, on="link_id", how="left")

    # Drop AADF road_name if it exists — OpenRoads road_name is the canonical one
    for col_name in ["road_name_x", "road_name_y"]:
        if col_name in result.columns:
            result = result.drop(columns=[col_name])

    # --- Derived rate -------------------------------------------------------
    if "all_motor_vehicles" in result.columns and "link_length_km" in result.columns:
        vehicle_km = result["all_motor_vehicles"] * result["link_length_km"] * 365
        result["collision_rate_per_mvkm"] = (
            result["collision_count"] / (vehicle_km / 1e6)
        ).replace([np.inf, -np.inf], np.nan)

    # --- COVID flag ---------------------------------------------------------
    if "is_covid" not in result.columns:
        from road_risk.clean_join.clean import COVID_YEARS

        result["is_covid"] = result["year"].isin(COVID_YEARS)

    logger.info(f"Final road_link × year table: {len(result):,} rows × {result.shape[1]} cols")
    if "collision_rate_per_mvkm" in result.columns:
        median_rate = result["collision_rate_per_mvkm"].median()
        logger.info(f"  Collision rate (median): {median_rate:.4f} per M veh-km")

    _validate_road_link_annual(result, snapped, openroads)

    return result


def _road_feature_columns_for_annual(columns: pd.Index | list[str]) -> list[str]:
    """Columns from the all-link traffic table needed by road_link_annual."""
    desired = ["link_id", "year"]
    for col in AADF_FEATURE_COLS + WEBTRIS_FEATURE_COLS + ROAD_FEATURE_AUDIT_COLS:
        if col not in desired:
            desired.append(col)
    return [col for col in desired if col in columns]


def _filter_road_features_for_annual(
    road_features: pd.DataFrame,
    agg: pd.DataFrame,
) -> pd.DataFrame:
    """
    Keep only traffic rows needed by positive collision link-years.

    ``road_features`` is the all Open Roads × year table. At full GB scale this
    is ~39M rows, while ``agg`` is only positive collision link-years. Avoid a
    full-frame copy before the merge.
    """
    keep_cols = _road_feature_columns_for_annual(road_features.columns)
    missing = {"link_id", "year"}.difference(keep_cols)
    if missing:
        raise ValueError(f"road_features is missing required join columns: {sorted(missing)}")

    keys = agg[["link_id", "year"]].drop_duplicates().copy()
    try:
        keys["link_id"] = keys["link_id"].astype(road_features["link_id"].dtype)
    except (TypeError, ValueError):
        logger.warning("Could not cast annual keys to road_features link_id dtype")

    logger.info(
        "  Filtering road features to %s positive collision link-years",
        f"{len(keys):,}",
    )
    filtered = road_features[keep_cols].merge(keys, on=["link_id", "year"], how="inner")

    if filtered.duplicated(["link_id", "year"]).any():
        dupes = filtered.loc[filtered.duplicated(["link_id", "year"], keep=False)]
        raise ValueError(
            "Filtered road_features has duplicate link_id/year rows; first examples:\n"
            f"{dupes[['link_id', 'year']].head(10).to_string(index=False)}"
        )

    logger.info(
        "  Road features retained for annual table: %s / %s rows",
        f"{len(filtered):,}",
        f"{len(road_features):,}",
    )
    return filtered


def _load_road_features_for_annual_keys(
    path: str | Path,
    agg: pd.DataFrame,
) -> pd.DataFrame:
    """Read cached road traffic features one year at a time for annual keys."""
    path = Path(path)
    import pyarrow.parquet as pq

    parquet = pq.ParquetFile(path)
    keep_cols = _road_feature_columns_for_annual(parquet.schema_arrow.names)
    missing = {"link_id", "year"}.difference(keep_cols)
    if missing:
        raise ValueError(f"{path} is missing required road traffic columns: {sorted(missing)}")

    keys = agg[["link_id", "year"]].drop_duplicates().copy()
    years = sorted(int(y) for y in keys["year"].dropna().unique())
    frames = []

    logger.info(
        "  Loading cached road features for annual keys from %s by year",
        path,
    )
    for year in years:
        keys_yr = keys[keys["year"] == year].copy()
        traffic_yr = pd.read_parquet(
            path,
            columns=keep_cols,
            filters=[("year", "=", year)],
        )
        try:
            keys_yr["link_id"] = keys_yr["link_id"].astype(traffic_yr["link_id"].dtype)
        except (TypeError, ValueError):
            logger.warning("Could not cast %s annual keys to road traffic link_id dtype", year)

        if traffic_yr.duplicated(["link_id", "year"]).any():
            dupes = traffic_yr.loc[traffic_yr.duplicated(["link_id", "year"], keep=False)]
            raise ValueError(
                f"{path} has duplicate link_id/year rows for {year}; first examples:\n"
                f"{dupes[['link_id', 'year']].head(10).to_string(index=False)}"
            )

        matched = keys_yr.merge(traffic_yr, on=["link_id", "year"], how="left")
        if len(matched) != len(keys_yr):
            raise ValueError(
                f"Road traffic key merge changed row count for {year}: "
                f"{len(keys_yr):,} -> {len(matched):,}"
            )

        frames.append(matched)
        logger.info(
            "    %s: retained %s annual road-feature rows from %s cached rows",
            year,
            f"{len(matched):,}",
            f"{len(traffic_yr):,}",
        )
        del traffic_yr, matched, keys_yr

    filtered = pd.concat(frames, ignore_index=True)
    if filtered.duplicated(["link_id", "year"]).any():
        raise ValueError("Filtered cached road features has duplicate link_id/year rows")

    logger.info(
        "  Cached road features retained for annual table: %s rows",
        f"{len(filtered):,}",
    )
    return filtered


def _validate_road_link_annual(
    result: pd.DataFrame,
    retained_snapped: pd.DataFrame,
    openroads: gpd.GeoDataFrame,
) -> None:
    """Validate the positive-only road_link_annual contract."""
    if result.empty:
        raise ValueError("road_link_annual is empty")

    if result.duplicated(["link_id", "year"]).any():
        dupes = result.loc[result.duplicated(["link_id", "year"], keep=False)]
        raise ValueError(
            "road_link_annual has duplicate link_id/year rows; first examples:\n"
            f"{dupes[['link_id', 'year']].head(10).to_string(index=False)}"
        )

    years = sorted(int(y) for y in result["year"].dropna().unique())
    if years != EXPECTED_MODEL_YEARS:
        raise ValueError(f"road_link_annual years are {years}; expected {EXPECTED_MODEL_YEARS}")

    if (result["collision_count"] < MIN_COLLISIONS).any():
        raise ValueError("road_link_annual must be positive-only by design")

    expected_collision_sum = int(len(retained_snapped))
    actual_collision_sum = int(result["collision_count"].sum())
    if actual_collision_sum != expected_collision_sum:
        raise ValueError(
            "road_link_annual collision_count sum does not match retained snapped "
            f"collisions: {actual_collision_sum:,} != {expected_collision_sum:,}"
        )

    openroad_links = pd.Index(openroads["link_id"].dropna().astype(str).unique())
    annual_links = pd.Index(result["link_id"].dropna().astype(str).unique())
    outside = annual_links.difference(openroad_links)
    if len(outside):
        raise ValueError(
            "road_link_annual contains link_ids outside Open Roads; first examples: "
            f"{outside[:10].tolist()}"
        )

    logger.info(
        "  road_link_annual validation passed: %s rows, %s links, collision_count sum %s",
        f"{len(result):,}",
        f"{result['link_id'].nunique():,}",
        f"{actual_collision_sum:,}",
    )


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------


def save_road_link_annual(
    df: pd.DataFrame,
    output_folder: str | Path = None,
) -> None:
    """Save the final road_link × year table to parquet."""
    if output_folder is None:
        output_folder = _ROOT / cfg["paths"]["features"]
    out = Path(output_folder)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "road_link_annual.parquet"
    df.to_parquet(path, index=False)
    logger.info(f"Saved road_link_annual to {path} ({len(df):,} rows)")


def save_road_traffic_features(
    df: pd.DataFrame,
    output_folder: str | Path = None,
) -> None:
    """Save the all-link × year pre-collision traffic feature table."""
    if output_folder is None:
        output_folder = _ROOT / cfg["paths"]["features"]
    out = Path(output_folder)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "road_traffic_features.parquet"
    df.to_parquet(path, index=False)
    logger.info(f"Saved road_traffic_features to {path} ({len(df):,} rows)")


def validate_existing_road_traffic_features(
    path: str | Path,
    openroads: gpd.GeoDataFrame,
    aadf: pd.DataFrame,
) -> None:
    """Validate metadata for an existing all-link traffic table."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    import pyarrow.parquet as pq

    parquet = pq.ParquetFile(path)
    available_cols = parquet.schema_arrow.names
    keep_cols = _road_feature_columns_for_annual(available_cols)
    missing = {"link_id", "year"}.difference(keep_cols)
    if missing:
        raise ValueError(f"{path} is missing required road traffic columns: {sorted(missing)}")

    expected_years = sorted(int(y) for y in aadf["year"].dropna().unique())
    expected_rows = len(openroads) * len(expected_years)
    if parquet.metadata.num_rows != expected_rows:
        raise ValueError(
            f"{path} has {parquet.metadata.num_rows:,} rows; expected {expected_rows:,}"
        )

    logger.info(
        "Existing road_traffic_features metadata validation passed: %s rows, "
        "%s Open Roads links, expected years %s",
        f"{parquet.metadata.num_rows:,}",
        f"{len(openroads):,}",
        expected_years,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(skip_road_features_if_valid: bool = False) -> None:
    """
    Load all cleaned parquets, run the full join pipeline, and save
    the road_link × year feature table to data/features/.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )

    processed = _ROOT / cfg["paths"]["processed"]

    # --- Load cleaned data --------------------------------------------------
    logger.info("Loading cleaned data ...")

    collisions = pd.read_parquet(processed / "stats19/collision_clean.parquet")
    aadf = pd.read_parquet(processed / "aadf/aadf_clean.parquet")

    # OS Open Roads — load from processed cache or raw GeoPackage
    or_path = processed / "shapefiles/openroads.parquet"
    if or_path.exists():
        openroads = gpd.read_parquet(or_path)
        logger.info(f"Loaded OS Open Roads from cache ({len(openroads):,} links)")
    else:
        logger.info("OS Open Roads cache not found — loading from GeoPackage ...")
        from road_risk.ingest.ingest_openroads import load_openroads, save_openroads

        openroads = load_openroads()
        save_openroads(openroads, processed / "shapefiles")

    webtris_path = processed / "webtris/webtris_clean.parquet"
    webtris = pd.read_parquet(webtris_path) if webtris_path.exists() else None
    if webtris is None:
        logger.warning("WebTRIS clean parquet not found — proceeding without sensor features")

    # --- Run pipeline -------------------------------------------------------
    # Prefer clean_join/snap.py weighted output if it exists — it uses multi-criteria
    # scoring (spatial + road class + junction + road number) and is more
    # accurate than the attribute+spatial fallback in snap_collisions_to_roads().
    snapped_w_path = processed / "stats19/snapped_weighted.parquet"
    if snapped_w_path.exists():
        logger.info(
            "Step 1: Loading pre-computed snapped_weighted.parquet "
            "(run clean_join/snap.py to regenerate)"
        )
        collisions_snapped = pd.read_parquet(snapped_w_path)
    else:
        logger.info("Step 1: Snapping collisions to OS Open Roads links ...")
        collisions_snapped = snap_collisions_to_roads(collisions, openroads)

    traffic_features_path = _ROOT / cfg["paths"]["features"] / "road_traffic_features.parquet"
    road_features = None
    road_features_path = None
    if skip_road_features_if_valid:
        try:
            logger.info("Step 2: Validating existing road features ...")
            validate_existing_road_traffic_features(
                traffic_features_path,
                openroads,
                aadf,
            )
            road_features_path = traffic_features_path
            logger.info("Step 2: Reusing existing road features")
        except Exception as e:
            logger.warning(
                "Existing road_traffic_features could not be reused (%s); rebuilding",
                e,
            )

    if road_features is None and road_features_path is None:
        logger.info("Step 2: Building road features ...")
        road_features = build_road_features(openroads, aadf, webtris)
        save_road_traffic_features(road_features)

    logger.info("Step 3: Building road_link × year table ...")
    result = build_road_link_annual(
        collisions_snapped,
        road_features,
        openroads,
        road_features_path=road_features_path,
    )

    # --- Summary ------------------------------------------------------------
    print("\n=== road_link_annual ===")
    print(f"  Rows    : {len(result):,}")
    print(f"  Links   : {result['link_id'].nunique():,}")
    print(f"  Years   : {sorted(result['year'].unique())}")
    print(f"  Columns : {result.columns.tolist()}")
    if "collision_rate_per_mvkm" in result.columns:
        print(f"  Collision rate (median): {result['collision_rate_per_mvkm'].median():.4f}")
    if "road_classification" in result.columns:
        print("\n  Road classification breakdown:")
        print(result.groupby("road_classification")["collision_count"].sum().to_string())

    save_road_link_annual(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build clean joined road-risk features")
    parser.add_argument(
        "--skip-road-features-if-valid",
        action="store_true",
        help=(
            "Reuse an existing validated road_traffic_features.parquet and rebuild only "
            "road_link_annual.parquet. Falls back to rebuilding road features if invalid."
        ),
    )
    args = parser.parse_args()
    main(skip_road_features_if_valid=args.skip_road_features_if_valid)
