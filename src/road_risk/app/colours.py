"""
colours.py
----------
Palette helpers for the Yorkshire Road Risk app.
No Streamlit dependency.
"""

import pandas as pd

from config import DEFAULT_ROAD_WEIGHT, RISK_PALETTE, ROAD_WEIGHTS


def _palette_lookup(normalised: float) -> str:
    """Map a value already in [0, 100] to a hex colour via RISK_PALETTE."""
    for i, (thresh, _) in enumerate(RISK_PALETTE):
        if normalised <= thresh:
            return RISK_PALETTE[max(0, i - 1)][1]
    return RISK_PALETTE[-1][1]


def make_colour_fn(scale_min: float, scale_max: float):
    """
    Return a function mapping a value → hex colour, rescaled via
    [scale_min, scale_max] → [0, 100] before palette lookup.
    """
    span = max(float(scale_max - scale_min), 1.0)

    def colour(val):
        if pd.isna(val):
            return "#555555"
        rescaled = (float(val) - scale_min) / span * 100.0
        rescaled = max(0.0, min(100.0, rescaled))
        return _palette_lookup(rescaled)

    return colour


def compute_colour_column(
    gdf,
    colour_col: str,
    rank_based: bool,
    scale_min: float,
    scale_max: float,
) -> pd.Series:
    """
    Compute a hex-colour Series for each row in gdf.

    rank_based=False  — value is already an absolute 0-100 percentile
                        (only risk_percentile). scale_min/max let the
                        user stretch the gradient.
    rank_based=True   — convert to percentile rank within displayed
                        dataset first, then apply scale_min/max. Makes
                        AADT, HGV %, betweenness etc. comparable on the
                        same colour scale without unit conversion.
    """
    series = gdf[colour_col].copy()

    if rank_based:
        normalised = series.rank(pct=True, na_option="bottom") * 100.0
    else:
        normalised = series.astype(float)

    colour_fn = make_colour_fn(scale_min, scale_max)
    return normalised.map(colour_fn)


def road_weight(road_class: str) -> float:
    return ROAD_WEIGHTS.get(road_class, DEFAULT_ROAD_WEIGHT)
