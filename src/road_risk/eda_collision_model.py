"""
eda_collision_model.py
----------------------
Targeted EDA to stress-test collision model assumptions and inform
model architecture decisions.

Each section answers a specific modelling question:

  Section 1  — Exposure backbone: does vehicle-km predict collisions as expected?
  Section 2  — Road type stratification: are motorways / duals / singles different regimes?
  Section 3  — Frequency vs severity decoupling: two-target justification
  Section 4  — Lane / flow intensity: does distributing flow across lanes change risk?
  Section 5  — Residual diagnostics: where does the pooled model under/over-predict?

Usage:
    python eda_collision_model.py
    python eda_collision_model.py --output-dir quarto/analysis/figures/eda
"""

import argparse
import logging
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from road_risk.config import _ROOT as ROOT

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)-8s  %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths (relative to project root)
# ---------------------------------------------------------------------------
# ROOT = Path(__file__).parent.parent.parent  # src/road_risk/ -> src/ -> project root

RISK_PATH    = ROOT / "data/models/risk_scores.parquet"
RLA_PATH     = ROOT / "data/features/road_link_annual.parquet"
NET_PATH     = ROOT / "data/features/network_features.parquet"
OR_PATH      = ROOT / "data/processed/shapefiles/openroads.parquet"

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor":  "white",
    "axes.facecolor":    "#f8f8f8",
    "axes.grid":          True,
    "grid.alpha":         0.4,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "font.size":          11,
})

ROAD_COLOURS = {
    "Motorway":              "#2563eb",
    "A Road":                "#16a34a",
    "B Road":                "#ca8a04",
    "Classified Unnumbered": "#9333ea",
    "Unclassified":          "#64748b",
    "Unknown":               "#94a3b8",
    "Not Classified":        "#cbd5e1",
}

FORM_COLOURS = {
    "Motorway":                    "#2563eb",
    "Dual Carriageway":            "#1d4ed8",
    "Collapsed Dual Carriageway":  "#3b82f6",
    "Single Carriageway":          "#16a34a",
    "Roundabout":                  "#f59e0b",
    "Slip Road":                   "#ef4444",
    "Shared Use Carriageway":      "#94a3b8",
    "Guided Busway":               "#cbd5e1",
}


def savefig(fig, output_dir: Path, name: str) -> None:
    path = output_dir / f"{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    logger.info(f"  Saved {path}")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data() -> dict:
    logger.info("Loading data ...")
    data = {}

    if RISK_PATH.exists():
        data["risk"] = pd.read_parquet(RISK_PATH)
        logger.info(f"  risk_scores: {len(data['risk']):,} links")

    if RLA_PATH.exists():
        data["rla"] = pd.read_parquet(RLA_PATH)
        logger.info(f"  road_link_annual: {len(data['rla']):,} link-years")

    if NET_PATH.exists():
        data["net"] = pd.read_parquet(NET_PATH)
        logger.info(f"  network_features: {len(data['net']):,} links")

    if OR_PATH.exists():
        import geopandas as gpd
        data["or"] = gpd.read_parquet(OR_PATH).drop(columns=["geometry"])
        logger.info(f"  openroads: {len(data['or']):,} links")

    return data


def build_analysis_table(data: dict) -> pd.DataFrame:
    """Merge risk, openroads, network features into one flat table."""
    if "risk" not in data:
        return pd.DataFrame()

    df = data["risk"].copy()

    if "or" in data:
        or_cols = ["link_id", "road_classification", "form_of_way",
                   "link_length_km", "is_trunk", "is_primary"]
        avail = [c for c in or_cols if c in data["or"].columns]
        # Always merge missing columns from openroads — risk_scores has
        # road_classification but not link_length_km or form_of_way
        missing = [c for c in avail if c != "link_id" and c not in df.columns]
        if missing:
            df = df.merge(data["or"][["link_id"] + missing],
                          on="link_id", how="left")

    if "net" in data:
        net_cols = ["link_id", "degree_mean", "betweenness_relative",
                    "dist_to_major_km", "pop_density_per_km2",
                    "speed_limit_mph", "lanes"]
        avail = [c for c in net_cols if c in data["net"].columns]
        df = df.merge(data["net"][avail], on="link_id", how="left")

    return df


# ---------------------------------------------------------------------------
# Section 1 — Exposure backbone
# ---------------------------------------------------------------------------

def section1_exposure(data: dict, output_dir: Path) -> None:
    logger.info("Section 1: Exposure backbone")

    if "rla" not in data:
        logger.warning("  road_link_annual.parquet not found — skipping")
        return

    rla = data["rla"].copy()
    if "estimated_aadt" not in rla.columns and "risk" in data:
        aadt_map = data["risk"].set_index("link_id")["estimated_aadt"]
        rla["estimated_aadt"] = rla["link_id"].map(aadt_map)

    if "link_length_km" not in rla.columns and "or" in data:
        len_map = data["or"].set_index("link_id")["link_length_km"]
        rla["link_length_km"] = rla["link_id"].map(len_map)

    if "road_classification" not in rla.columns and "or" in data:
        rc_map = data["or"].set_index("link_id")["road_classification"]
        rla["road_classification"] = rla["link_id"].map(rc_map)

    needed = ["collision_count", "estimated_aadt", "link_length_km"]
    if not all(c in rla.columns for c in needed):
        logger.warning(f"  Missing columns for exposure analysis: "
                       f"{[c for c in needed if c not in rla.columns]}")
        return

    rla = rla.dropna(subset=needed)
    rla["vehicle_km"] = rla["estimated_aadt"] * rla["link_length_km"] * 365
    rla["vehicle_km_M"] = rla["vehicle_km"] / 1e6
    rla["log_vkm"] = np.log(rla["vehicle_km_M"].clip(lower=1e-6))

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Section 1 — Exposure backbone", fontsize=13, fontweight="bold")

    # 1a: vehicle-km vs collision count (log-log, binned means)
    ax = axes[0]
    bins = np.percentile(rla["log_vkm"], np.linspace(5, 95, 20))
    rla["vkm_bin"] = pd.cut(rla["log_vkm"], bins=bins)
    binned = rla.groupby("vkm_bin", observed=True).agg(
        mean_count=("collision_count", "mean"),
        mean_vkm=("log_vkm", "mean"),
        n=("collision_count", "count")
    ).dropna()
    ax.scatter(binned["mean_vkm"], binned["mean_count"],
               s=binned["n"] / binned["n"].max() * 200 + 20,
               alpha=0.7, color="#2563eb")
    ax.set_xlabel("Log(vehicle-km/M)")
    ax.set_ylabel("Mean collision count")
    ax.set_title("Exposure vs collision count\n(bin size = circle area)")

    # 1b: collision rate per M vehicle-km distribution
    ax = axes[1]
    with_collisions = rla[rla["collision_count"] > 0].copy()
    with_collisions["rate_per_Mvkm"] = (
        with_collisions["collision_count"] / with_collisions["vehicle_km_M"]
    )
    if "road_classification" in with_collisions.columns:
        for rc, grp in with_collisions.groupby("road_classification"):
            colour = ROAD_COLOURS.get(rc, "#94a3b8")
            rates = grp["rate_per_Mvkm"].clip(upper=grp["rate_per_Mvkm"].quantile(0.99))
            ax.hist(np.log1p(rates), bins=30, alpha=0.5,
                    color=colour, label=rc, density=True)
        ax.legend(fontsize=8, loc="upper right")
    else:
        ax.hist(np.log1p(with_collisions["rate_per_Mvkm"]), bins=40, color="#2563eb", alpha=0.7)
    ax.set_xlabel("Log(1 + collision rate per M veh-km)")
    ax.set_ylabel("Density")
    ax.set_title("Collision rate distribution\nby road class (positive links only)")

    # 1c: zero rates by road type
    ax = axes[2]
    if "road_classification" in rla.columns:
        zero_rates = (
            rla.groupby("road_classification")["collision_count"]
            .apply(lambda x: (x == 0).mean())
            .sort_values()
        )
        colours = [ROAD_COLOURS.get(r, "#94a3b8") for r in zero_rates.index]
        bars = ax.barh(zero_rates.index, zero_rates.values, color=colours)
        ax.set_xlabel("Proportion of zero-collision link-years")
        ax.set_title("Zero-collision rate by road class")
        for bar, val in zip(bars, zero_rates.values):
            ax.text(val + 0.005, bar.get_y() + bar.get_height() / 2,
                    f"{val:.1%}", va="center", fontsize=9)

    plt.tight_layout()
    savefig(fig, output_dir, "01_exposure_backbone")


# ---------------------------------------------------------------------------
# Section 2 — Road type stratification
# ---------------------------------------------------------------------------

def section2_road_types(data: dict, output_dir: Path) -> None:
    logger.info("Section 2: Road type stratification")

    df = build_analysis_table(data)
    if df.empty or "collision_count" not in df.columns:
        logger.warning("  Insufficient data — skipping")
        return

    needed2 = ["road_classification", "estimated_aadt", "link_length_km"]
    missing2 = [c for c in needed2 if c not in df.columns]
    if missing2:
        logger.warning(f"  Missing columns: {missing2} — skipping")
        return

    df = df.dropna(subset=["road_classification", "estimated_aadt", "link_length_km"])
    df["vehicle_km_M"] = df["estimated_aadt"] * df["link_length_km"] * 365 / 1e6
    df["collision_rate"] = df["collision_count"] / df["vehicle_km_M"].clip(lower=1e-6)

    # KSI if available
    if "fatal_count" in df.columns and "serious_count" in df.columns:
        df["ksi_count"] = df["fatal_count"].fillna(0) + df["serious_count"].fillna(0)
        df["ksi_rate"] = df["ksi_count"] / df["vehicle_km_M"].clip(lower=1e-6)
        df["severity_ratio"] = df["ksi_count"] / df["collision_count"].replace(0, np.nan)
        has_ksi = True
    else:
        has_ksi = False

    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("Section 2 — Road type stratification", fontsize=13, fontweight="bold")
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

    road_order = ["Motorway", "A Road", "B Road",
                  "Classified Unnumbered", "Unclassified", "Unknown", "Not Classified"]
    road_order = [r for r in road_order if r in df["road_classification"].unique()]

    def boxplot_by_road(ax, col, label, log=True):
        data_by_road = [
            df.loc[(df["road_classification"] == rc) & (df[col] > 0), col].clip(
                upper=df.loc[df[col] > 0, col].quantile(0.99)
            ).values
            for rc in road_order
        ]
        colours = [ROAD_COLOURS.get(r, "#94a3b8") for r in road_order]
        bp = ax.boxplot(data_by_road, patch_artist=True, showfliers=False,
                        medianprops={"color": "black", "linewidth": 1.5})
        for patch, colour in zip(bp["boxes"], colours):
            patch.set_facecolor(colour)
            patch.set_alpha(0.7)
        ax.set_xticks(range(1, len(road_order) + 1))
        ax.set_xticklabels([r.replace(" ", "\n") for r in road_order], fontsize=8)
        if log:
            ax.set_yscale("log")
        ax.set_ylabel(label)

    # 2a: collision rate by road type
    ax = fig.add_subplot(gs[0, 0])
    boxplot_by_road(ax, "collision_rate", "Collision rate\n(per M veh-km)")
    ax.set_title("Collision frequency by road type")

    # 2b: KSI rate by road type
    if has_ksi:
        ax = fig.add_subplot(gs[0, 1])
        boxplot_by_road(ax, "ksi_rate", "KSI rate\n(per M veh-km)")
        ax.set_title("KSI rate by road type")

        # 2c: severity ratio
        ax = fig.add_subplot(gs[0, 2])
        boxplot_by_road(ax, "severity_ratio", "KSI / total collisions", log=False)
        ax.set_title("Severity ratio by road type\n(motorway effect)")

    # 2d: mean AADT by road type (to contextualise)
    ax = fig.add_subplot(gs[1, 0])
    mean_aadt = df.groupby("road_classification")["estimated_aadt"].median()
    mean_aadt = mean_aadt.reindex(road_order).dropna()
    colours = [ROAD_COLOURS.get(r, "#94a3b8") for r in mean_aadt.index]
    ax.barh(mean_aadt.index, mean_aadt.values, color=colours)
    ax.set_xlabel("Median estimated AADT")
    ax.set_title("Traffic volume by road type")

    # 2e: form of way breakdown
    if "form_of_way" in df.columns:
        ax = fig.add_subplot(gs[1, 1])
        fow_rate = df.groupby("form_of_way")["collision_rate"].median().sort_values()
        fow_rate = fow_rate[fow_rate.index != "Unknown"].dropna()
        colours = [FORM_COLOURS.get(f, "#94a3b8") for f in fow_rate.index]
        ax.barh(fow_rate.index, fow_rate.values, color=colours)
        ax.set_xlabel("Median collision rate (per M veh-km)")
        ax.set_title("Collision rate by form of way")

    # 2f: link count by road type (sample size context)
    ax = fig.add_subplot(gs[1, 2])
    counts = df["road_classification"].value_counts().reindex(road_order).dropna()
    colours = [ROAD_COLOURS.get(r, "#94a3b8") for r in counts.index]
    ax.barh(counts.index, counts.values, color=colours)
    ax.set_xlabel("Number of links")
    ax.set_title("Sample size by road type")

    savefig(fig, output_dir, "02_road_type_stratification")


# ---------------------------------------------------------------------------
# Section 3 — Frequency vs severity decoupling
# ---------------------------------------------------------------------------

def section3_severity(data: dict, output_dir: Path) -> None:
    logger.info("Section 3: Frequency vs severity decoupling")

    df = build_analysis_table(data)
    if df.empty:
        return

    if not all(c in df.columns for c in ["fatal_count", "serious_count",
                                          "collision_count", "estimated_aadt"]):
        logger.warning("  Missing severity columns — skipping")
        return

    needed = ["estimated_aadt", "link_length_km", "fatal_count",
               "serious_count", "collision_count"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        logger.warning(f"  Missing columns for severity analysis: {missing} — skipping")
        return
    df = df.dropna(subset=["estimated_aadt", "link_length_km"])
    df["vehicle_km_M"] = df["estimated_aadt"] * df["link_length_km"] * 365 / 1e6
    df["collision_rate"] = df["collision_count"] / df["vehicle_km_M"].clip(lower=1e-6)
    df["ksi_count"]  = df["fatal_count"].fillna(0) + df["serious_count"].fillna(0)
    df["ksi_rate"]   = df["ksi_count"] / df["vehicle_km_M"].clip(lower=1e-6)

    # Only links with at least one collision
    pos = df[df["collision_count"] > 0].copy()
    pos["severity_ratio"] = pos["ksi_count"] / pos["collision_count"]
    pos_sev = pos[pos["collision_count"] >= 5].copy()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Section 3 — Frequency vs severity decoupling\n"
                 "(justification for two-target model)", fontsize=13, fontweight="bold")

    # 3a: frequency vs KSI rate scatter (coloured by road type)
    ax = axes[0, 0]
    if "road_classification" in pos.columns:
        for rc, grp in pos.groupby("road_classification"):
            colour = ROAD_COLOURS.get(rc, "#94a3b8")
            cap_freq = grp["collision_rate"].clip(upper=grp["collision_rate"].quantile(0.99))
            cap_ksi  = grp["ksi_rate"].clip(upper=grp["ksi_rate"].quantile(0.99))
            ax.scatter(np.log1p(cap_freq), np.log1p(cap_ksi),
                       alpha=0.15, s=6, color=colour, label=rc)
        ax.legend(fontsize=7, markerscale=2, loc="upper left")
    else:
        ax.scatter(np.log1p(pos["collision_rate"]), np.log1p(pos["ksi_rate"]),
                   alpha=0.1, s=5, color="#2563eb")
    ax.set_xlabel("Log(1 + collision rate)")
    ax.set_ylabel("Log(1 + KSI rate)")
    ax.set_title("Frequency vs KSI rate\n(where they diverge = different risk character)")

    # Add identity line
    lim = max(ax.get_xlim()[1], ax.get_ylim()[1])
    ax.plot([0, lim], [0, lim], "k--", alpha=0.3, linewidth=0.8, label="y=x")

    # 3b: severity ratio by road type (key plot)
    ax = axes[0, 1]
    road_order = ["Motorway", "A Road", "B Road",
                  "Classified Unnumbered", "Unclassified"]
    if "road_classification" in pos.columns:
        median_sev = pos_sev.groupby("road_classification")["severity_ratio"].median()
        median_sev = median_sev.reindex(road_order).dropna()
        colours = [ROAD_COLOURS.get(r, "#94a3b8") for r in median_sev.index]
        bars = ax.barh(median_sev.index, median_sev.values, color=colours)
        ax.set_xlabel("Median KSI / total collisions")
        ax.set_title("Severity ratio by road type\n"
                     "(links with 5+ collisions for stability)")
        for bar, val in zip(bars, median_sev.values):
            ax.text(val + 0.002, bar.get_y() + bar.get_height() / 2,
                    f"{val:.2f}", va="center", fontsize=9)

    # 3c: links ranking differently on frequency vs severity
    ax = axes[1, 0]
    q75_freq = pos["collision_rate"].quantile(0.75)
    q75_ksi  = pos["ksi_rate"].quantile(0.75)
    pos["high_freq"] = pos["collision_rate"] > q75_freq
    pos["high_ksi"]  = pos["ksi_rate"]  > q75_ksi
    quadrants = {
        "High freq,\nHigh KSI":   (pos["high_freq"] & pos["high_ksi"]).sum(),
        "High freq,\nLow KSI":    (pos["high_freq"] & ~pos["high_ksi"]).sum(),
        "Low freq,\nHigh KSI":    (~pos["high_freq"] & pos["high_ksi"]).sum(),
        "Low freq,\nLow KSI":     (~pos["high_freq"] & ~pos["high_ksi"]).sum(),
    }
    colours_q = ["#ef4444", "#f97316", "#3b82f6", "#94a3b8"]
    bars = ax.barh(list(quadrants.keys()), list(quadrants.values()), color=colours_q)
    ax.set_xlabel("Number of links")
    ax.set_title("Frequency vs KSI quadrants\n(top quartile threshold)")
    for bar, val in zip(bars, quadrants.values()):
        ax.text(val + 50, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", fontsize=9)

    # 3d: weighted severity score options
    ax = axes[1, 1]
    # Show how rankings shift under different weight schemes
    weights = [
        ("KSI only",        lambda d: d["ksi_count"]),
        ("1·slight + 3·serious + 10·fatal",
         lambda d: d.get("slight_count", d["collision_count"] - d["ksi_count"]) +
                   3 * d["serious_count"].fillna(0) + 10 * d["fatal_count"].fillna(0)),
        ("1·slight + 5·serious + 20·fatal",
         lambda d: d.get("slight_count", d["collision_count"] - d["ksi_count"]) +
                   5 * d["serious_count"].fillna(0) + 20 * d["fatal_count"].fillna(0)),
    ]
    if "road_classification" in pos.columns:
        road_order2 = ["Motorway", "A Road", "B Road", "Classified Unnumbered", "Unclassified"]
        x = np.arange(len(road_order2))
        width = 0.25
        for i, (label, fn) in enumerate(weights[:3]):
            try:
                scores = pos.copy()
                scores["w_score"] = fn(scores)
                scores["w_rate"] = scores["w_score"] / scores["vehicle_km_M"].clip(lower=1e-6)
                medians = scores.groupby("road_classification")["w_rate"].median()
                medians = medians.reindex(road_order2).fillna(0)
                ax.bar(x + i * width, medians.values, width, label=label, alpha=0.8)
            except Exception:
                pass
        ax.set_xticks(x + width)
        ax.set_xticklabels([r.replace(" ", "\n") for r in road_order2], fontsize=8)
        ax.set_ylabel("Median weighted rate per M veh-km")
        ax.set_title("Severity-weighted rates by road type\n(sensitivity to weight scheme)")
        ax.legend(fontsize=8)

    plt.tight_layout()
    savefig(fig, output_dir, "03_severity_decoupling")


# ---------------------------------------------------------------------------
# Section 4 — Lane / flow intensity
# ---------------------------------------------------------------------------

def section4_lanes(data: dict, output_dir: Path) -> None:
    logger.info("Section 4: Lane/flow intensity")

    df = build_analysis_table(data)
    if "lanes" not in df.columns:
        logger.warning("  lanes column not found (OSM coverage ~5%) — skipping")
        return

    df = df.dropna(subset=["lanes", "estimated_aadt", "link_length_km", "collision_count"])
    df = df[df["lanes"] > 0]
    df["vehicle_km_M"]   = df["estimated_aadt"] * df["link_length_km"] * 365 / 1e6
    df["collision_rate"] = df["collision_count"] / df["vehicle_km_M"].clip(lower=1e-6)
    df["aadt_per_lane"]  = df["estimated_aadt"] / df["lanes"]
    baseline_rate = df["collision_count"].sum() / df["vehicle_km_M"].sum()
    df["expected_count_baseline"] = baseline_rate * df["vehicle_km_M"]
    df["log_excess_risk"] = np.log(
        (df["collision_count"] + 1) / (df["expected_count_baseline"] + 1)
    )

    if len(df) < 100:
        logger.warning(f"  Only {len(df)} links with lane data — results may be unstable")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"Section 4 — Lane/flow intensity (n={len(df):,} links with lane data)",
                 fontsize=13, fontweight="bold")

    # 4a: AADT per lane vs excess risk after simple exposure adjustment
    ax = axes[0]
    pos = df[df["collision_count"] > 0]
    ax.scatter(np.log1p(pos["aadt_per_lane"]),
               pos["log_excess_risk"],
               alpha=0.15, s=8, color="#2563eb")
    if len(pos) > 10:
        r, p = stats.pearsonr(np.log1p(pos["aadt_per_lane"]),
                               pos["log_excess_risk"])
        ax.set_title(f"AADT per lane vs excess risk\nr={r:.2f}, p={p:.3f}")
    else:
        ax.set_title("AADT per lane vs excess risk")
    ax.set_xlabel("Log(1 + AADT per lane)")
    ax.set_ylabel("Log(observed+1 / expected+1)")

    # 4b: collision rate by lane count (box)
    ax = axes[1]
    lane_vals = sorted(df["lanes"].unique())
    lane_vals = [
        lane for lane in lane_vals
        if df[df["lanes"] == lane]["collision_count"].sum() > 0
    ]
    data_by_lane = [
        df.loc[(df["lanes"] == lane) & (df["collision_count"] > 0), "collision_rate"]
        .clip(upper=df["collision_rate"].quantile(0.99)).values
        for lane in lane_vals
    ]
    if data_by_lane:
        bp = ax.boxplot(data_by_lane, patch_artist=True, showfliers=False,
                        medianprops={"color": "black", "linewidth": 1.5})
        for patch in bp["boxes"]:
            patch.set_facecolor("#3b82f6")
            patch.set_alpha(0.7)
        ax.set_xticks(range(1, len(lane_vals) + 1))
        ax.set_xticklabels([str(int(lane)) for lane in lane_vals])
        ax.set_yscale("log")
    ax.set_xlabel("Number of lanes")
    ax.set_ylabel("Collision rate (per M veh-km)")
    ax.set_title("Collision rate by lane count")

    # 4c: compare total AADT vs per-lane AADT against excess risk rather than a
    # collision rate that already uses AADT in the denominator.
    ax = axes[2]
    pos2 = df[(df["collision_count"] > 0) & df["estimated_aadt"].notna()]
    if len(pos2) > 10:
        r_total, _ = stats.pearsonr(
            np.log1p(pos2["estimated_aadt"]), pos2["log_excess_risk"])
        r_lane, _  = stats.pearsonr(
            np.log1p(pos2["aadt_per_lane"]),  pos2["log_excess_risk"])
        ax.barh(["Total AADT", "AADT per lane"],
                [abs(r_total), abs(r_lane)],
                color=["#2563eb", "#16a34a"])
        ax.set_xlabel("|r| with excess risk")
        ax.set_title("Association with excess risk\n(after simple exposure baseline)")
        ax.set_xlim(0, 1)
        for i, val in enumerate([abs(r_total), abs(r_lane)]):
            ax.text(val + 0.01, i, f"{val:.2f}", va="center")

    plt.tight_layout()
    savefig(fig, output_dir, "04_lane_flow_intensity")


# ---------------------------------------------------------------------------
# Section 5 — Residual diagnostics
# ---------------------------------------------------------------------------

def section5_residuals(data: dict, output_dir: Path) -> None:
    logger.info("Section 5: Residual diagnostics")

    df = build_analysis_table(data)
    if "predicted_glm" not in df.columns or "collision_count" not in df.columns:
        logger.warning("  predicted_glm not in risk_scores — skipping")
        return

    df = df.dropna(subset=["predicted_glm", "road_classification"])
    df["residual_raw"] = df["collision_count"] - df["predicted_glm"]
    df["residual_ratio"] = (df["collision_count"] + 1) / (df["predicted_glm"] + 1)
    df["log_residual"] = np.log(df["residual_ratio"])

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle("Section 5 — Residual diagnostics\n"
                 "(where does the pooled model under/over-predict?)",
                 fontsize=13, fontweight="bold")

    road_order = ["Motorway", "A Road", "B Road",
                  "Classified Unnumbered", "Unclassified", "Unknown", "Not Classified"]
    road_order = [r for r in road_order if r in df["road_classification"].unique()]

    # 5a: mean log-residual by road type
    ax = axes[0, 0]
    mean_resid = df.groupby("road_classification")["log_residual"].mean()
    mean_resid = mean_resid.reindex(road_order).dropna()
    colours = ["#ef4444" if v > 0 else "#3b82f6" for v in mean_resid.values]
    ax.barh(mean_resid.index, mean_resid.values, color=colours)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Mean log(observed+1 / predicted+1)")
    ax.set_title("Residuals by road type\n(red = under-predicted, blue = over-predicted)")

    # 5b: residuals vs predicted (fitted vs residual)
    ax = axes[0, 1]
    sample = df.sample(min(10000, len(df)), random_state=42)
    ax.scatter(np.log1p(sample["predicted_glm"]), sample["log_residual"],
               alpha=0.08, s=4, color="#64748b")
    ax.axhline(0, color="red", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Log(1 + predicted GLM)")
    ax.set_ylabel("Log residual")
    ax.set_title("Fitted vs residual\n(heteroscedasticity check)")

    # 5c: residuals by form of way
    if "form_of_way" in df.columns:
        ax = axes[1, 0]
        fow_resid = df.groupby("form_of_way")["log_residual"].mean().sort_values()
        colours = ["#ef4444" if v > 0 else "#3b82f6" for v in fow_resid.values]
        ax.barh(fow_resid.index, fow_resid.values, color=colours)
        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_xlabel("Mean log residual")
        ax.set_title("Residuals by form of way\n(red = under-predicted)")

    # 5d: XGBoost vs GLM predictions comparison
    if "predicted_xgb" in df.columns:
        ax = axes[1, 1]
        sample2 = df.sample(min(10000, len(df)), random_state=42)
        ax.scatter(np.log1p(sample2["predicted_glm"]),
                   np.log1p(sample2["predicted_xgb"]),
                   alpha=0.08, s=4, color="#7c3aed")
        lim = max(ax.get_xlim()[1], ax.get_ylim()[1])
        ax.plot([0, lim], [0, lim], "r--", alpha=0.5, linewidth=0.8)
        ax.set_xlabel("Log(1 + predicted GLM)")
        ax.set_ylabel("Log(1 + predicted XGBoost)")
        ax.set_title("GLM vs XGBoost predictions\n(should align post base_margin fix)")

    plt.tight_layout()
    savefig(fig, output_dir, "05_residuals")


# ---------------------------------------------------------------------------
# Section 7 — Top/bottom risk links profile
# ---------------------------------------------------------------------------

def section7_risk_profile(data: dict, output_dir: Path) -> None:
    logger.info("Section 7: Risk percentile profiles")

    df = build_analysis_table(data)
    if df.empty or "risk_percentile" not in df.columns:
        return

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Section 7 — Risk percentile profiles",
                 fontsize=13, fontweight="bold")

    df["risk_tier"] = pd.cut(df["risk_percentile"],
                              bins=[-1e-9, 50, 75, 90, 99, 100],
                              labels=["Low (<50)", "Med (50-75)",
                                      "High (75-90)", "Very high (90-99)",
                                      "Top 1%"],
                              include_lowest=True)

    # 7a: road class composition by risk tier
    ax = axes[0]
    if "road_classification" in df.columns:
        tier_rc = (df.groupby(["risk_tier", "road_classification"], observed=True)
                   .size().unstack(fill_value=0))
        tier_rc = tier_rc.div(tier_rc.sum(axis=1), axis=0)
        bottom = np.zeros(len(tier_rc))
        for rc in tier_rc.columns:
            colour = ROAD_COLOURS.get(rc, "#94a3b8")
            ax.bar(range(len(tier_rc)), tier_rc[rc].values,
                   bottom=bottom, label=rc, color=colour, alpha=0.85)
            bottom += tier_rc[rc].values
        ax.set_xticks(range(len(tier_rc)))
        ax.set_xticklabels(tier_rc.index, rotation=20, ha="right", fontsize=8)
        ax.set_ylabel("Proportion")
        ax.set_title("Road class mix by risk tier")
        ax.legend(fontsize=7, loc="upper left")

    # 7b: mean AADT by risk tier
    ax = axes[1]
    mean_aadt = df.groupby("risk_tier", observed=True)["estimated_aadt"].median()
    ax.bar(range(len(mean_aadt)), mean_aadt.values,
           color=["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#991b1b"])
    ax.set_xticks(range(len(mean_aadt)))
    ax.set_xticklabels(mean_aadt.index, rotation=20, ha="right", fontsize=8)
    ax.set_ylabel("Median estimated AADT")
    ax.set_title("Traffic volume by risk tier")

    # 7c: degree mean by risk tier (junction density)
    ax = axes[2]
    if "degree_mean" in df.columns:
        mean_deg = df.groupby("risk_tier", observed=True)["degree_mean"].median()
        ax.bar(range(len(mean_deg)), mean_deg.values,
               color=["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#991b1b"])
        ax.set_xticks(range(len(mean_deg)))
        ax.set_xticklabels(mean_deg.index, rotation=20, ha="right", fontsize=8)
        ax.set_ylabel("Median node degree (junction complexity)")
        ax.set_title("Junction complexity by risk tier")

    plt.tight_layout()
    savefig(fig, output_dir, "07_risk_profiles")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_dir}")

    data = load_data()

    if not data:
        logger.error("No data loaded — check paths")
        return

    section1_exposure(data, output_dir)
    section2_road_types(data, output_dir)
    section3_severity(data, output_dir)
    section4_lanes(data, output_dir)
    section5_residuals(data, output_dir)
    section7_risk_profile(data, output_dir)

    logger.info(f"Done — {len(list(output_dir.glob('*.png')))} figures in {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="quarto/analysis/figures/eda",
                        help="Directory to save PNG figures")
    args = parser.parse_args()
    main(Path(args.output_dir))
