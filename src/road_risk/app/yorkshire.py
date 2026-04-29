"""
Yorkshire Road Risk Explorer
-----------------------------
Streamlit app for exploring road risk scores across the Yorkshire network.

Run with:
    streamlit run app/yorkshire.py
    python -m streamlit run app/yorkshire.py

Or directly (calls main() which IS the app — no subprocess):
    python app/yorkshire.py

Requires:
    pip install streamlit folium streamlit-folium geopandas
"""

import sys
from pathlib import Path

# Ensure app/ directory is on sys.path so sibling modules resolve
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from streamlit_folium import st_folium

from config import COLOUR_OPTIONS, RISK_PATH, TILE_OPTIONS, YEAR_OPTIONS
from data import build_map_gdf, load_temporal
from road_risk.app.map_builder import build_folium_map

# ---------------------------------------------------------------------------
# Page config — must be the first Streamlit call in the module
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Yorkshire Road Risk Explorer",
    page_icon="🛣",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
_CSS = """
<style>
    [data-testid="stSidebar"] { background: #0f1117; }
    [data-testid="stSidebar"] * { color: #e8e8e8 !important; }
    .metric-card {
        background: #1a1d27;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        border-left: 3px solid #e05252;
    }
    .metric-card .label {
        font-size: 11px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card .value { font-size: 22px; font-weight: 600; color: #f0f0f0; }
    .metric-card .sub   { font-size: 12px; color: #aaa; margin-top: 2px; }
    h1 { font-size: 1.6rem !important; }
    .stSelectbox label, .stMultiSelect label, .stSlider label { font-size: 12px !important; }
</style>
"""


def _metric_card(label: str, value: str, sub: str) -> str:
    return (
        f'<div class="metric-card">'
        f'  <div class="label">{label}</div>'
        f'  <div class="value">{value}</div>'
        f'  <div class="sub">{sub}</div>'
        f"</div>"
    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def _build_sidebar() -> dict:
    """Render sidebar controls and return a dict of current values."""
    with st.sidebar:
        st.title("🛣 Yorkshire Road Risk")
        st.caption("Exposure-adjusted collision risk · OS Open Roads · 2015–2024")
        st.divider()

        st.subheader("Filters")

        road_classes = st.multiselect(
            "Road classification",
            ["Motorway", "A Road", "B Road", "Classified Unnumbered", "Unclassified"],
            default=["Motorway", "A Road", "B Road"],
        )

        risk_tier = st.select_slider(
            "Show risk tier",
            options=["Top 1%", "Top 5%", "Top 10%", "Top 25%", "All roads"],
            value="Top 10%",
        )
        tier_map = {"Top 1%": 99, "Top 5%": 95, "Top 10%": 90, "Top 25%": 75, "All roads": 0}
        min_percentile = tier_map[risk_tier]

        selected_years = st.multiselect(
            "Model years",
            YEAR_OPTIONS,
            default=[YEAR_OPTIONS[-1]],
            help=(
                "Multiple years: risk_percentile = max (worst year), "
                "collision_count = sum, AADT / HGV / darkness = mean."
            ),
        )

        st.divider()
        st.subheader("Appearance")

        map_tile_label = st.selectbox("Map style", list(TILE_OPTIONS.keys()), index=0)
        map_tile = TILE_OPTIONS[map_tile_label]

        colour_by_label = st.selectbox(
            "Colour roads by",
            list(COLOUR_OPTIONS.keys()),
            index=0,
            help=(
                "Non-percentile variables are rank-normalised within the "
                "currently displayed links so the full colour range is used."
            ),
        )
        colour_col, colour_desc, rank_based = COLOUR_OPTIONS[colour_by_label]

        color_range = st.slider(
            "Colour scale range (percentile)",
            min_value=0,
            max_value=100,
            value=(0, 99),
            help="Narrow to e.g. 80–99 to maximise contrast at the high-risk end.",
        )
        scale_min, scale_max = color_range

        st.divider()
        show_legend = st.toggle("Show legend", value=True)

        st.divider()
        st.caption("**About the model**")
        st.caption(
            "Risk scores from a Poisson GLM + XGBoost trained on 452k collisions "
            "across 23 police forces, 2015–2024, pooled to one row per link. "
            "Exposure offset = log(AADT × length × 365 / 1M veh-km). "
            "Higher percentile = more collisions than expected given traffic volume."
        )

    return dict(
        road_classes=road_classes,
        min_percentile=min_percentile,
        risk_tier=risk_tier,
        selected_years=selected_years,
        map_tile=map_tile,
        colour_by_label=colour_by_label,
        colour_col=colour_col,
        colour_desc=colour_desc,
        rank_based=rank_based,
        scale_min=scale_min,
        scale_max=scale_max,
        show_legend=show_legend,
    )


# ---------------------------------------------------------------------------
# Info panel helper — shows clicked road details + seasonality chart
# ---------------------------------------------------------------------------
def _render_info_panel(map_data: dict, map_gdf) -> None:
    st.subheader("Road details")

    temporal_df = load_temporal()
    clicked = map_data and map_data.get("last_object_clicked")

    if clicked:
        props = clicked.get("properties") or {}

        road_name = props.get("road_name", "Unnamed")
        road_class = props.get("road_classification", "Unknown")
        risk_pct = props.get("risk_percentile", "—")
        aadt = props.get("estimated_aadt", 0)
        collisions = props.get("collision_count", 0)
        fatals = props.get("fatal_count", "—")
        hgv = props.get("hgv_pct", None)
        speed = props.get("speed_limit", None)
        excess = props.get("residual_glm", None)

        st.markdown(f"### {road_name}")
        st.write(f"**Class:** {road_class} &nbsp;|&nbsp; **Risk %ile:** {risk_pct}")
        st.write(
            f"**AADT:** {int(aadt):,} veh/day &nbsp;|&nbsp; "
            f"**Collisions:** {int(collisions)} &nbsp;|&nbsp; "
            f"**Fatals:** {fatals}"
        )

        if hgv is not None:
            st.write(f"**HGV:** {float(hgv) * 100:.1f}% &nbsp;|&nbsp; **Speed limit:** {speed} mph")

        if excess is not None:
            st.write(f"**Excess risk:** {float(excess):+.3f}")

        # ---- Seasonality chart ----
        if temporal_df is not None and road_name != "Unnamed":
            # Extract road prefix (up to 4 chars, e.g. "A1(M)" → "A1(M", "M62" → "M62")
            prefix = str(road_name)[:4].strip()
            road_season = temporal_df[temporal_df["road_prefix"] == prefix]

            if not road_season.empty:
                st.divider()
                st.caption(f"Seasonal traffic index — {prefix}")
                # Support both monthname and month columns
                idx_col = "monthname" if "monthname" in road_season.columns else "month"
                chart_data = road_season.set_index(idx_col)[["seasonal_index"]]
                st.bar_chart(chart_data, height=160)
    else:
        st.caption("Click a road link to see details and seasonality.")

    st.divider()

    # Top 10 table
    st.subheader("Top 10 highest risk")
    top10 = (
        map_gdf[
            [
                "road_name",
                "road_classification",
                "risk_percentile",
                "estimated_aadt",
                "collision_count",
            ]
        ]
        .sort_values("risk_percentile", ascending=False)
        .head(10)
        .copy()
    )
    top10["road_name"] = top10["road_name"].fillna("Unnamed")
    top10["risk_percentile"] = top10["risk_percentile"].round(0).astype(int)
    top10["estimated_aadt"] = top10["estimated_aadt"].round(0).astype(int)
    st.dataframe(
        top10.rename(
            columns={
                "road_name": "Road",
                "road_classification": "Class",
                "risk_percentile": "Pct",
                "estimated_aadt": "AADT",
                "collision_count": "Cols",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------------------------
# Main application function
# ---------------------------------------------------------------------------
def main() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)

    # ---- Sidebar ----
    cfg = _build_sidebar()

    if not cfg["selected_years"]:
        st.warning("Select at least one year in the sidebar.")
        return

    st.title("Yorkshire Road Risk Explorer")

    # ---- Load data ----
    years_tuple = tuple(sorted(cfg["selected_years"]))
    map_gdf = build_map_gdf(years_tuple, tuple(cfg["road_classes"]), cfg["min_percentile"])

    if map_gdf is None:
        st.error(
            "Could not load model outputs. Run `model.py --stage collision` "
            "and ensure `_ROOT` resolves to the project root."
        )
        st.info(f"Expected risk scores at: `{RISK_PATH}`")
        return

    if len(map_gdf) == 0:
        st.warning(
            "No links match the current filters. "
            "Try loosening the risk tier or road class selection."
        )
        return

    # Graceful fallback if chosen colour column isn't in the data yet
    colour_col = cfg["colour_col"]
    rank_based = cfg["rank_based"]
    colour_label = cfg["colour_by_label"]
    if colour_col not in map_gdf.columns:
        st.sidebar.warning(
            f"'{colour_label}' not in data — falling back to Risk Percentile. "
            "Re-run model.py to generate the missing column."
        )
        colour_col, rank_based, colour_label = "risk_percentile", False, "Risk Percentile"

    # ---- Summary metrics ----
    years_label = ", ".join(str(y) for y in years_tuple)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            _metric_card(
                "Road links shown", f"{len(map_gdf):,}", f"{cfg['risk_tier']} · {years_label}"
            ),
            unsafe_allow_html=True,
        )

    with col2:
        med_pct = map_gdf["risk_percentile"].median()
        st.markdown(
            _metric_card("Median risk percentile", f"{med_pct:.0f}", "of all Yorkshire links"),
            unsafe_allow_html=True,
        )

    with col3:
        n_collisions = int(map_gdf["collision_count"].sum())
        st.markdown(
            _metric_card("Total collisions", f"{n_collisions:,}", f"summed across {years_label}"),
            unsafe_allow_html=True,
        )

    with col4:
        if "hgv_pct" in map_gdf.columns:
            avg_hgv = map_gdf["hgv_pct"].mean() * 100
            st.markdown(
                _metric_card("Avg HGV exposure", f"{avg_hgv:.1f}%", "across visible links"),
                unsafe_allow_html=True,
            )
        else:
            mean_aadt = map_gdf["estimated_aadt"].median()
            st.markdown(
                _metric_card("Median AADT", f"{mean_aadt:,.0f}", "vehicles/day"),
                unsafe_allow_html=True,
            )

    st.divider()

    # ---- Map + info panel ----
    map_col, info_col = st.columns([3, 1])

    with map_col:
        folium_map, n_shown, n_total = build_folium_map(
            map_gdf=map_gdf,
            colour_col=colour_col,
            colour_label=colour_label,
            rank_based=rank_based,
            scale_min=cfg["scale_min"],
            scale_max=cfg["scale_max"],
            map_tile=cfg["map_tile"],
            show_legend=cfg["show_legend"],
        )

        if n_total > n_shown:
            st.caption(
                f"⚠ Showing {n_shown:,} of {n_total:,} links. Tighten filters to reduce sampling."
            )

        # returned_objects="last_object_clicked" returns the full feature
        # properties dict on click, which we need for road name / seasonality.
        # Pan and zoom do NOT trigger a rerun.
        map_data = st_folium(
            folium_map,
            height=600,
            use_container_width=True,
            returned_objects=["last_object_clicked"],
            key="road_risk_map",
        )

    with info_col:
        _render_info_panel(map_data, map_gdf)

    # ---- Road classification breakdown ----
    st.divider()
    st.subheader("Risk distribution by road class")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        by_class = (
            map_gdf.groupby("road_classification")["risk_percentile"]
            .agg(["median", "count"])
            .reset_index()
            .sort_values("median", ascending=False)
            .rename(
                columns={
                    "road_classification": "Road class",
                    "median": "Median risk percentile",
                    "count": "Links",
                }
            )
        )
        st.dataframe(by_class, use_container_width=True, hide_index=True)

    with chart_col2:
        st.caption(f"""
        **Colour dimension: {colour_label}**

        {cfg["colour_desc"]}

        A road in the **top 1%** has more collisions than 99% of all roads
        *given its traffic volume*. Quiet B-roads with disproportionate
        collisions can outrank busy motorways.

        **Excess risk** = observed minus model-predicted. Positive = worse
        than the model expects.

        Multi-year: percentile = max (worst year), collisions = total.
        """)


# ---------------------------------------------------------------------------
# Entry point
# Streamlit re-runs this module top-to-bottom on each interaction,
# so main() is called directly — no subprocess needed.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
