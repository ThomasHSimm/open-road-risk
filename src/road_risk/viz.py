"""Shared map-rendering helpers for the Quarto site and notebooks.

Centralises the GB WGS84 map frame, the latitude-aware aspect used by the
Stage 2 maps in ``analysis/model-results.qmd``, and an optional thin GB
coastline outline. Keeping these in one place avoids re-defining the extent
logic on every page and gives basemap-free maps a consistent look.

The outline is a tracked, pre-simplified GeoJSON (``data/boundaries``) so that
every map renders identically without depending on the gitignored source
GeoPackage. Attribution for the outline (ONS / OGL v3) is in ``GB_OUTLINE_ATTRIBUTION``.
"""

from __future__ import annotations

import os
import warnings

import numpy as np

from road_risk.config import _ROOT, cfg

_GB_BBOX = cfg["study_area"]["bbox_wgs84"]

# Stable GB frame, padded outward so the coastline is never clipped at the edge.
GB_MAP_EXTENT = {
    "min_lon": min(_GB_BBOX["min_lon"], -8.7),
    "max_lon": max(_GB_BBOX["max_lon"], 2.1),
    "min_lat": min(_GB_BBOX["min_lat"], 49.8),
    "max_lat": max(_GB_BBOX["max_lat"], 60.9),
}

# Tracked, pre-simplified (~1 km) GB coastline. Committed so renders are
# reproducible without the gitignored data/raw GeoPackage.
GB_OUTLINE_PATH = _ROOT / "data" / "boundaries" / "gb_outline_1km.geojson"

# Required attribution: ONS Countries (Dec 2023) BGC, Open Government Licence v3.
GB_OUTLINE_ATTRIBUTION = (
    "Boundary: Office for National Statistics; contains OS data "
    "© Crown copyright and database right 2023; Open Government Licence v3.0"
)


def set_gb_wgs84_extent(ax, extent=None):
    """Apply a stable GB frame and latitude-aware WGS84 aspect to ``ax``."""
    extent = extent or GB_MAP_EXTENT
    ax.set_xlim(extent["min_lon"], extent["max_lon"])
    ax.set_ylim(extent["min_lat"], extent["max_lat"])
    mid_lat = (extent["min_lat"] + extent["max_lat"]) / 2
    ax.set_aspect(1 / np.cos(np.deg2rad(mid_lat)), adjustable="box")
    ax.set_anchor("C")


def load_gb_outline():
    """Return the tracked GB outline as a WGS84 GeoDataFrame.

    Warns loudly if the file is missing (maps then render without a coastline),
    and raises in CI so a dropped tracked asset cannot pass silently.
    """
    if not GB_OUTLINE_PATH.exists():
        msg = (
            f"GB outline not found at {GB_OUTLINE_PATH}. Maps will render without a "
            "coastline. Regenerate it from data/raw/boundaries/gb_boundary.gpkg."
        )
        if os.environ.get("CI", "").lower() == "true":
            raise FileNotFoundError(msg)
        warnings.warn(msg, stacklevel=2)
        return None

    import geopandas as gpd

    outline = gpd.read_file(GB_OUTLINE_PATH)
    if outline.crs is not None and outline.crs.to_epsg() != 4326:
        outline = outline.to_crs(4326)
    return outline


def add_gb_outline(ax, outline=None, color="#9aa0a6", linewidth=0.6, zorder=1):
    """Draw a thin GB coastline on ``ax`` (WGS84). No-op if the boundary is absent.

    Returns ``True`` if an outline was drawn, ``False`` otherwise.
    """
    if outline is None:
        outline = load_gb_outline()
    if outline is None:
        return False
    outline.boundary.plot(ax=ax, color=color, linewidth=linewidth, zorder=zorder)
    return True
