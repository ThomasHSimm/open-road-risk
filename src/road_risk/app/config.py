"""
config.py
---------
Paths, constants, palette and display mappings for the Yorkshire Road Risk app.
No Streamlit dependency — safe to import anywhere.
"""

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root resolution
# ---------------------------------------------------------------------------
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from road_risk.config import _ROOT  # noqa: F401
except ImportError:
    _ROOT = None
    for _candidate in [
        Path(__file__).parent.parent,
        Path.home() / "Documents/GitHub/road-risk-analysis",
        Path.home() / "road-risk-analysis",
    ]:
        if (_candidate / "data/models/risk_scores.parquet").exists():
            _ROOT = _candidate
            break

# ---------------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------------
RISK_PATH = _ROOT / "data/models/risk_scores.parquet" if _ROOT else None
OR_PATH = _ROOT / "data/processed/shapefiles/openroads.parquet" if _ROOT else None
NET_PATH = _ROOT / "data/features/network_features.parquet" if _ROOT else None
TEMPORAL_PATH = _ROOT / "data/models/temporal_profiles.parquet" if _ROOT else None

# ---------------------------------------------------------------------------
# Colour palette (blue → red, 7 stops over 0-100)
# ---------------------------------------------------------------------------
RISK_PALETTE: list[tuple[float, str]] = [
    (0, "#2166ac"),
    (20, "#74add1"),
    (40, "#e0f3f8"),
    (60, "#fee090"),
    (80, "#f46d43"),
    (95, "#d73027"),
    (100, "#a50026"),
]

# ---------------------------------------------------------------------------
# Map tile options
# ---------------------------------------------------------------------------
TILE_OPTIONS: dict[str, str] = {
    "CartoDB Voyager": "CartoDB voyager",  # neutral — best contrast for overlays
    "CartoDB Positron": "CartoDB positron",  # light/minimal
    "OpenStreetMap": "OpenStreetMap",
    "CartoDB Dark": "CartoDB dark_matter",
}

# ---------------------------------------------------------------------------
# Road classification → line weight
# ---------------------------------------------------------------------------
ROAD_WEIGHTS: dict[str, float] = {
    "Motorway": 4.0,
    "A Road": 3.0,
    "B Road": 2.0,
}
DEFAULT_ROAD_WEIGHT = 1.5

# ---------------------------------------------------------------------------
# Colour-by variable options
# (label) → (column_name, description, rank_based)
# rank_based=True  → rank-normalise within displayed dataset
# rank_based=False → value is already an absolute 0-100 percentile
# ---------------------------------------------------------------------------
COLOUR_OPTIONS: dict[str, tuple[str, str, bool]] = {
    "Risk Percentile": (
        "risk_percentile",
        "Collision risk vs traffic volume",
        False,
    ),
    "Excess Risk (residual)": (
        "residual_glm",
        "Observed minus model-predicted collisions",
        True,
    ),
    "Traffic Volume (AADT)": (
        "estimated_aadt",
        "Annual avg daily traffic",
        True,
    ),
    "HGV Proportion": (
        "hgv_pct",
        "Heavy goods vehicle share of traffic",
        True,
    ),
    "Speed Limit": (
        "speed_limit",
        "Posted speed limit (mph)",
        True,
    ),
    "Network Betweenness": (
        "betweenness_relative",
        "Relative betweenness centrality",
        True,
    ),
    "Distance to Major Road": (
        "dist_to_major_km",
        "km to nearest A-road / motorway",
        True,
    ),
    "Population Density": (
        "pop_density_per_km2",
        "People per km²",
        True,
    ),
}

# ---------------------------------------------------------------------------
# Tooltip field → display alias
# ---------------------------------------------------------------------------
TOOLTIP_ALIASES: dict[str, str] = {
    "road_name": "Road",
    "road_classification": "Class",
    "risk_percentile": "Risk %ile",
    "estimated_aadt": "AADT (veh/day)",
    "collision_count": "Collisions",
    "fatal_count": "Fatals",
    "serious_count": "Serious",
    "hgv_pct": "HGV %",
    "speed_limit": "Speed Limit (mph)",
    "residual_glm": "Excess risk",
    "link_length_km": "Length (km)",
    "form_of_way": "Form",
    "betweenness_relative": "Betweenness (rel.)",
    "degree_mean": "Node degree",
    "betweenness": "Betweenness (abs.)",
    "dist_to_major_km": "Dist to major (km)",
    "pop_density_per_km2": "Pop density (/km²)",
}

# ---------------------------------------------------------------------------
# Year options available in the risk model
# ---------------------------------------------------------------------------
YEAR_OPTIONS = [2019, 2021, 2023]
