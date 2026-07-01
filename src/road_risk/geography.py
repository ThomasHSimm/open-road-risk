"""
Shared study-area helpers.

The configured bbox is only a fast pre-filter. For GB-scale runs, use the
configured boundary polygon as the final geographic filter so Ireland, NI,
Isle of Man, and water-edge false positives do not leak into the pipeline.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import pandas as pd

from road_risk.config import _ROOT, cfg

logger = logging.getLogger(__name__)

STUDY_AREA_NAME = str(cfg["study_area"].get("name", "study_area")).lower()

_wgs84 = cfg["study_area"]["bbox_wgs84"]
STUDY_AREA_BBOX_WGS84 = {
    "min_lat": _wgs84["min_lat"],
    "max_lat": _wgs84["max_lat"],
    "min_lon": _wgs84["min_lon"],
    "max_lon": _wgs84["max_lon"],
}

_bng = cfg["study_area"]["bbox_bng"]
STUDY_AREA_BBOX_BNG = (
    _bng["min_easting"],
    _bng["min_northing"],
    _bng["max_easting"],
    _bng["max_northing"],
)


def _project_path(value: str | Path | None) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    return path if path.is_absolute() else _ROOT / path


def study_area_boundary_path() -> Path | None:
    """Return the configured study-area boundary path, if one is configured."""
    return _project_path(cfg["study_area"].get("boundary"))


@lru_cache(maxsize=8)
def load_study_area_boundary(
    target_crs: str = "EPSG:4326",
    required: bool = True,
):
    """
    Load and dissolve the configured study-area boundary.

    Returns a one-row GeoDataFrame, or None when no boundary is configured and
    required=False.
    """
    import geopandas as gpd

    boundary_path = study_area_boundary_path()
    if boundary_path is None:
        if required:
            raise FileNotFoundError("study_area.boundary is not configured")
        return None

    if not boundary_path.exists():
        message = (
            f"Study-area boundary not found: {boundary_path}\n"
            "Create it with: python scripts/download_gb_boundary.py"
        )
        if required:
            raise FileNotFoundError(message)
        logger.warning(message)
        return None

    layer = cfg["study_area"].get("boundary_layer")
    try:
        boundary = (
            gpd.read_file(boundary_path, layer=layer) if layer else gpd.read_file(boundary_path)
        )
    except Exception:
        # Some user-provided files may not have the configured layer name.
        boundary = gpd.read_file(boundary_path)

    if boundary.empty:
        raise ValueError(f"Study-area boundary is empty: {boundary_path}")

    nation_codes = set(cfg["study_area"].get("nation_codes", []))
    if nation_codes:
        code_col = next(
            (
                col
                for col in boundary.columns
                if col.upper() in {"CTRY23CD", "CTRY24CD", "CTRY22CD", "COUNTRY_CODE"}
            ),
            None,
        )
        if code_col is not None:
            boundary = boundary[boundary[code_col].isin(nation_codes)]
            if boundary.empty:
                raise ValueError(
                    f"Boundary file {boundary_path} has no features matching {sorted(nation_codes)}"
                )

    if boundary.crs is None:
        logger.warning("Study-area boundary has no CRS; assuming EPSG:4326")
        boundary = boundary.set_crs("EPSG:4326")

    if target_crs and str(boundary.crs).upper() != target_crs.upper():
        boundary = boundary.to_crs(target_crs)

    invalid = ~boundary.geometry.is_valid
    if invalid.any():
        boundary = boundary.copy()
        boundary.loc[invalid, "geometry"] = boundary.loc[invalid, "geometry"].buffer(0)

    geom = boundary.geometry.unary_union
    return gpd.GeoDataFrame(
        {"study_area": [STUDY_AREA_NAME]},
        geometry=[geom],
        crs=boundary.crs,
    )


def filter_points_to_study_area(
    df: pd.DataFrame,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    require_boundary: bool | None = None,
) -> pd.DataFrame:
    """
    Filter a lat/lon DataFrame to valid coordinates, configured bbox, and boundary.
    """
    if df.empty:
        return df.copy()
    if lat_col not in df.columns or lon_col not in df.columns:
        raise ValueError(f"Missing coordinate columns: {lat_col!r}, {lon_col!r}")

    lat = pd.to_numeric(df[lat_col], errors="coerce")
    lon = pd.to_numeric(df[lon_col], errors="coerce")

    bbox = STUDY_AREA_BBOX_WGS84
    mask = (
        lat.notna()
        & lon.notna()
        & lat.between(bbox["min_lat"], bbox["max_lat"])
        & lon.between(bbox["min_lon"], bbox["max_lon"])
    )
    filtered = df.loc[mask].copy()
    filtered[lat_col] = lat.loc[mask]
    filtered[lon_col] = lon.loc[mask]
    logger.info(
        "  Coordinate/bbox filter (%s): %s -> %s rows",
        STUDY_AREA_NAME,
        f"{len(df):,}",
        f"{len(filtered):,}",
    )

    if require_boundary is None:
        require_boundary = study_area_boundary_path() is not None

    boundary = load_study_area_boundary("EPSG:4326", required=require_boundary)
    if boundary is None or filtered.empty:
        return filtered

    import geopandas as gpd

    points = gpd.GeoSeries(
        gpd.points_from_xy(filtered[lon_col], filtered[lat_col]),
        crs="EPSG:4326",
        index=filtered.index,
    )
    geom = boundary.geometry.iloc[0]
    try:
        in_boundary = points.covered_by(geom)
    except AttributeError:
        in_boundary = points.within(geom) | points.touches(geom)

    result = filtered.loc[in_boundary].copy()
    logger.info(
        "  Boundary filter (%s): %s -> %s rows",
        STUDY_AREA_NAME,
        f"{len(filtered):,}",
        f"{len(result):,}",
    )
    return result


def filter_geodataframe_to_study_area(
    gdf,
    require_boundary: bool | None = None,
    predicate: str = "intersects",
):
    """Filter a GeoDataFrame to the configured study-area boundary."""
    if require_boundary is None:
        require_boundary = study_area_boundary_path() is not None

    boundary = load_study_area_boundary(str(gdf.crs), required=require_boundary)
    if boundary is None or gdf.empty:
        return gdf

    geom = boundary.geometry.iloc[0]
    if predicate == "within":
        mask = gdf.geometry.within(geom)
    elif predicate == "covered_by":
        try:
            mask = gdf.geometry.covered_by(geom)
        except AttributeError:
            mask = gdf.geometry.within(geom) | gdf.geometry.touches(geom)
    elif predicate == "intersects":
        mask = gdf.geometry.intersects(geom)
    else:
        raise ValueError(f"Unsupported boundary predicate: {predicate}")

    filtered = gdf.loc[mask].copy()
    logger.info(
        "  Boundary filter (%s): %s -> %s features",
        STUDY_AREA_NAME,
        f"{len(gdf):,}",
        f"{len(filtered):,}",
    )
    return filtered
