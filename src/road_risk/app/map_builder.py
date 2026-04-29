"""
map_builder.py
--------------
Constructs and returns a folium.Map from a filtered GeoDataFrame.
No Streamlit calls — pure folium logic, fully testable in isolation.
"""

import folium
import geopandas as gpd
import pandas as pd

from config import RISK_PALETTE, TOOLTIP_ALIASES
from road_risk.app.colours import compute_colour_column, road_weight

# Scored roads (have collision model output) — coloured by chosen variable
# Total rendering budget — motorways + A roads always included fully,
# B roads and others fill the remainder up to this cap.
MAX_LINKS_SCORED = 60_000
# Columns shown in the hover tooltip, in display order.
# Only columns that are actually present in the GDF are included at runtime.
_BASE_TOOLTIP_COLS = [
    "road_name",
    "road_classification",
    "risk_percentile",
    "estimated_aadt",
    "collision_count",
    "fatal_count",
    "serious_count",
    "hgv_pct",
    "speed_limit",
    "residual_glm",
    "link_length_km",
    "form_of_way",
]

_NET_TOOLTIP_COLS = [
    "betweenness_relative",
    "degree_mean",
    "dist_to_major_km",
    "pop_density_per_km2",
]

# Integer rounding for these columns before serialisation
_INT_COLS = {"risk_percentile", "collision_count", "fatal_count", "serious_count", "estimated_aadt"}
# 1 dp
_ONE_DP = {"hgv_pct", "speed_limit"}
# 3 dp
_THREE_DP = {
    "residual_glm",
    "link_length_km",
    "betweenness_relative",
    "degree_mean",
    "dist_to_major_km",
    "pop_density_per_km2",
}


def _legend_html(
    colour_label: str,
    scale_min: float,
    scale_max: float,
    rank_based: bool,
) -> str:
    if rank_based:
        entries = [
            (RISK_PALETTE[-1][1], f"High {colour_label}"),
            (RISK_PALETTE[4][1], ""),
            (RISK_PALETTE[2][1], ""),
            (RISK_PALETTE[0][1], f"Low {colour_label}"),
        ]
    else:
        entries = [
            ("#a50026", "Top 1%"),
            ("#d73027", "Top 1–5%"),
            ("#f46d43", "Top 5–20%"),
            ("#fee090", "Mid 40–80%"),
            ("#74add1", "Low 20–40%"),
            ("#2166ac", "Lowest 20%"),
        ]

    rows = "".join(
        f'<div style="display:flex;align-items:center;margin:3px 0;">'
        f'  <div style="width:18px;height:8px;background:{col};'
        f'              border-radius:2px;margin-right:8px;flex-shrink:0;"></div>'
        f'  <span style="font-size:11px;">{label}</span>'
        f"</div>"
        for col, label in entries
    )

    scale_note = (
        f'<div style="font-size:10px;color:#aaa;margin-top:5px;">'
        f"Scale: {scale_min}–{scale_max}th pct.</div>"
        if (scale_min != 0 or scale_max != 99)
        else ""
    )

    no_data_row = ""  # All links scored — no 'no data' legend entry needed

    return f"""
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
                background:rgba(20,22,35,0.90);padding:12px 16px;
                border-radius:8px;border:1px solid #555;color:#ddd;
                min-width:160px;pointer-events:none;">
        <div style="font-size:13px;font-weight:600;margin-bottom:8px;">{colour_label}</div>
        {rows}
        {no_data_row}
        {scale_note}
    </div>
    """


def build_folium_map(
    map_gdf: gpd.GeoDataFrame,
    colour_col: str,
    colour_label: str,
    rank_based: bool,
    scale_min: float,
    scale_max: float,
    map_tile: str,
    show_legend: bool,
) -> tuple[folium.Map, int, int]:
    """
    Build and return (folium.Map, n_shown, n_total).

    Single GeoJson layer — all links are scored (risk_scores covers full network).
    Sampled to MAX_LINKS_SCORED for performance.
    """
    m = folium.Map(
        location=[53.95, -1.3],
        zoom_start=9,
        tiles=map_tile,
        control_scale=True,
    )

    # All links are scored — single layer, no grey skeleton needed.
    # risk_scores.parquet now covers all ~998k network links.
    scored_gdf = map_gdf.copy()
    n_total = len(scored_gdf)

    if n_total > MAX_LINKS_SCORED:
        # Priority sampling: motorways + A roads always rendered fully.
        # B roads and others fill the remaining budget.
        motorways = scored_gdf[scored_gdf["road_classification"] == "Motorway"]
        a_roads = scored_gdf[scored_gdf["road_classification"] == "A Road"]
        b_roads = scored_gdf[scored_gdf["road_classification"] == "B Road"]
        other = scored_gdf[
            ~scored_gdf["road_classification"].isin(["Motorway", "A Road", "B Road"])
        ]

        budget = max(0, MAX_LINKS_SCORED - len(motorways) - len(a_roads))
        b_sample = b_roads.sample(min(len(b_roads), budget // 2), random_state=42)
        oth_sample = other.sample(min(len(other), budget // 2), random_state=42)
        scored_gdf = pd.concat([motorways, a_roads, b_sample, oth_sample], ignore_index=True)

    n_shown = len(scored_gdf)

    # ---- Scored roads ----
    if len(scored_gdf) > 0:
        # Colour column may be absent if network features haven't been generated
        if colour_col in scored_gdf.columns:
            scored_gdf["_colour"] = compute_colour_column(
                scored_gdf, colour_col, rank_based, scale_min, scale_max
            )
        else:
            scored_gdf["_colour"] = "#888888"

        scored_gdf["_weight"] = scored_gdf["road_classification"].map(road_weight)

        all_wanted = _BASE_TOOLTIP_COLS + _NET_TOOLTIP_COLS
        tooltip_cols = [c for c in all_wanted if c in scored_gdf.columns]
        active_aliases = [TOOLTIP_ALIASES.get(c, c) for c in tooltip_cols]

        scored_gdf["road_name"] = scored_gdf["road_name"].fillna("Unnamed")
        scored_gdf["form_of_way"] = scored_gdf["form_of_way"].fillna("Unknown")

        for col in tooltip_cols:
            if col not in scored_gdf.columns:
                continue
            if col in _INT_COLS:
                scored_gdf[col] = scored_gdf[col].fillna(0).round(0).astype(int)
            elif col in _ONE_DP:
                scored_gdf[col] = scored_gdf[col].fillna(0).round(1)
            elif col in _THREE_DP:
                scored_gdf[col] = scored_gdf[col].fillna(0).round(3)

        geojson_cols = tooltip_cols + ["_colour", "_weight", "geometry"]
        folium.GeoJson(
            scored_gdf[geojson_cols],
            style_function=lambda f: {
                "color": f["properties"]["_colour"],
                "weight": f["properties"]["_weight"],
                "opacity": 0.85,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=tooltip_cols,
                aliases=active_aliases,
                sticky=True,
                style="font-size:12px;font-family:sans-serif;",
            ),
            name="Road risk",
        ).add_to(m)

    # ---- Legend ----
    if show_legend:
        m.get_root().html.add_child(
            folium.Element(_legend_html(colour_label, scale_min, scale_max, rank_based))
        )

    folium.LayerControl().add_to(m)
    return m, n_shown, n_total
