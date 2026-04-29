"""
diagnostics/osm_coverage.py
----------------------------
OSM feature coverage analysis stratified by road class and region.

Loads network_features.parquet and road network geometry, then reports
coverage of OSM-derived columns (speed_limit_mph, lanes, lit, is_unpaved)
broken down by road_classification and a coarse regional band.

Outputs
-------
quarto/analysis/osm-coverage-by-class.csv  — full table (class × column)
quarto/analysis/osm-coverage.qmd           — narrative highlighting usable / noisy columns

Usage
-----
    python src/road_risk/diagnostics/osm_coverage.py

Prerequisites
-------------
Run network_features.py with the --osm flag first:
    python src/road_risk/features/network.py --osm --force

The script will exit early with a clear message if OSM columns are absent.
"""

import sys
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd
from road_risk.config import _ROOT as ROOT

# ROOT = Path(__file__).resolve().parents[3]
NET_PATH    = ROOT / "data/features/network_features.parquet"
OR_PATH     = ROOT / "data/processed/shapefiles/openroads.parquet"
REPORT_DIR  = ROOT / "quarto" / "analysis"
OUT_CSV     = REPORT_DIR / "osm-coverage-by-class.csv"
OUT_QMD     = REPORT_DIR / "osm-coverage.qmd"

OSM_COLUMNS = ["speed_limit_mph", "lanes", "lit", "is_unpaved"]
NUMERIC_OSM = ["speed_limit_mph", "lanes"]

ROAD_CLASS_ORDER = [
    "Motorway", "A Road", "B Road",
    "Classified Unnumbered", "Unclassified",
    "Not Classified", "Unknown",
]


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------

def load_data():
    if not NET_PATH.exists():
        sys.exit(
            f"ERROR: {NET_PATH} not found.\n"
            "Run: python src/road_risk/features/network.py --force first."
        )

    print(f"Loading network features from {NET_PATH.name} ...")
    net = pd.read_parquet(NET_PATH)
    print(f"  {len(net):,} rows × {net.shape[1]} columns")
    print(f"  Columns: {list(net.columns)}")

    # Check OSM columns are present
    present = [c for c in OSM_COLUMNS if c in net.columns]
    absent  = [c for c in OSM_COLUMNS if c not in net.columns]

    if not present:
        sys.exit(
            "\nERROR: No OSM columns found in network_features.parquet.\n"
            "The file has only graph/population features:\n"
            f"  {list(net.columns)}\n\n"
            "Re-run network_features.py with the --osm flag to add OSM enrichment:\n"
            "  python src/road_risk/features/network.py --osm --force\n\n"
            "Source OSM files are present in data/raw/osm/ — the run takes ~15 mins."
        )

    if absent:
        print(f"\n  WARNING: Expected OSM columns not found: {absent}")
        print(f"  Proceeding with available columns: {present}\n")

    # Load road geometry for road_classification and region
    print("Loading OpenRoads for road_classification ...")
    try:
        import geopandas as gpd
        or_gdf = gpd.read_parquet(OR_PATH)
        or_df = pd.DataFrame(or_gdf[["link_id", "road_classification"]].copy())

        # Coarse regional band from link centroid latitude
        centroids = or_gdf.to_crs("EPSG:4326").geometry.centroid
        or_df["latitude"] = centroids.y
    except Exception as e:
        print(f"  WARNING: Could not load geometry ({e}). Road class / region unavailable.")
        or_df = pd.DataFrame(
            {
                "link_id": net["link_id"],
                "road_classification": "Unknown",
                "latitude": np.nan,
            }
        )

    merged = net.merge(or_df, on="link_id", how="left")
    merged["road_classification"] = (
        merged["road_classification"]
        .fillna("Unknown")
        .where(merged["road_classification"].isin(ROAD_CLASS_ORDER), other="Unknown")
    )

    # Coarse regional band: 1° latitude bands (roughly 111 km)
    merged["lat_band"] = merged["latitude"].apply(
        lambda x: f"{int(x):.0f}–{int(x)+1:.0f}°N" if pd.notna(x) else "Unknown"
    )

    return merged, present


# ---------------------------------------------------------------------------
# Coverage by road class
# ---------------------------------------------------------------------------

def coverage_by_class(df: pd.DataFrame, osm_cols: list) -> pd.DataFrame:
    rows = []
    for rc in ROAD_CLASS_ORDER:
        sub = df[df["road_classification"] == rc]
        if len(sub) == 0:
            continue
        for col in osm_cols:
            if col not in df.columns:
                continue
            n_total   = len(sub)
            n_filled  = sub[col].notna().sum()
            pct       = n_filled / n_total * 100

            row = {
                "road_class":  rc,
                "column":      col,
                "n_links":     n_total,
                "n_filled":    int(n_filled),
                "pct_coverage": round(pct, 1),
            }

            # Value distribution for numeric columns
            if col in NUMERIC_OSM:
                vals = sub[col].dropna()
                if len(vals) > 0:
                    q = vals.quantile([0.25, 0.5, 0.75])
                    row["min"]    = round(float(vals.min()), 1)
                    row["q25"]    = round(float(q[0.25]), 1)
                    row["median"] = round(float(q[0.50]), 1)
                    row["q75"]    = round(float(q[0.75]), 1)
                    row["max"]    = round(float(vals.max()), 1)
                    row["n_distinct"] = int(vals.nunique())
                else:
                    row["min"] = row["q25"] = row["median"] = row["q75"] = row["max"] = np.nan
                    row["n_distinct"] = 0

            rows.append(row)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Coverage by region (lat band)
# ---------------------------------------------------------------------------

def coverage_by_region(df: pd.DataFrame, osm_cols: list) -> pd.DataFrame:
    rows = []
    for band in sorted(df["lat_band"].unique()):
        sub = df[df["lat_band"] == band]
        for col in osm_cols:
            if col not in df.columns:
                continue
            n_total  = len(sub)
            n_filled = sub[col].notna().sum()
            rows.append({
                "lat_band":    band,
                "column":      col,
                "n_links":     n_total,
                "n_filled":    int(n_filled),
                "pct_coverage": round(n_filled / n_total * 100, 1),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Markdown summary
# ---------------------------------------------------------------------------

def build_markdown(by_class: pd.DataFrame, by_region: pd.DataFrame, osm_cols: list) -> str:
    lines = [
        "---",
        'title: "OSM Feature Coverage Diagnostic"',
        "format:",
        "  html:",
        "    toc: true",
        "    toc-depth: 3",
        "    number-sections: true",
        "    page-layout: full",
        "---",
        "",
    ]

    # Overall
    lines.append("## Overall coverage\n")
    total = by_class.groupby("column").apply(
        lambda g: pd.Series({
            "n_links":     g["n_links"].sum(),
            "n_filled":    g["n_filled"].sum(),
        })
    ).reset_index()
    total["pct_coverage"] = (total["n_filled"] / total["n_links"] * 100).round(1)
    lines.append(total[["column", "n_links", "n_filled", "pct_coverage"]].to_markdown(index=False))
    lines.append("\n")

    # By road class — pivot
    lines.append("## Coverage by road class (%)\n")
    pivot = by_class.pivot_table(
        index="column", columns="road_class", values="pct_coverage"
    )
    # Reorder columns
    ordered_cols = [c for c in ROAD_CLASS_ORDER if c in pivot.columns]
    pivot = pivot[ordered_cols]
    lines.append(pivot.round(1).fillna("—").to_markdown())
    lines.append("\n")

    # By region — pivot
    if not by_region.empty:
        lines.append("## Coverage by latitude band (%)\n")
        pivot_r = by_region.pivot_table(
            index="column", columns="lat_band", values="pct_coverage"
        )
        lines.append(pivot_r.round(1).fillna("—").to_markdown())
        lines.append("\n")

    # Numeric distributions
    num_cols = [c for c in NUMERIC_OSM if c in osm_cols]
    if num_cols:
        lines.append("## Value distributions (populated rows only)\n")
        for col in num_cols:
            sub = by_class[by_class["column"] == col].copy()
            dist_cols = [
                "road_class",
                "n_filled",
                "n_distinct",
                "min",
                "q25",
                "median",
                "q75",
                "max",
            ]
            available = [c for c in dist_cols if c in sub.columns]
            lines.append(f"### {col}\n")
            lines.append(sub[available].to_markdown(index=False))
            lines.append("\n")

    # --- Highlights ---
    lines.append("## Highlights\n")

    lines.append("### Columns with >80% coverage by road class (usable without imputation)\n")
    high = by_class[by_class["pct_coverage"] >= 80][["road_class", "column", "pct_coverage"]]
    if high.empty:
        lines.append("_No column × road-class combination reaches 80% coverage._\n")
    else:
        lines.append(high.sort_values("pct_coverage", ascending=False).to_markdown(index=False))
    lines.append("\n")

    lines.append(
        "### Columns with <20% coverage by road class "
        "(imputation would invent most values)\n"
    )
    low = by_class[by_class["pct_coverage"] < 20][
        ["road_class", "column", "pct_coverage", "n_links", "n_filled"]
    ]
    if low.empty:
        lines.append("_No column × road-class combination is below 20% coverage._\n")
    else:
        lines.append(low.sort_values("pct_coverage").to_markdown(index=False))
    lines.append("\n")

    lines.append("### Decision guidance\n")
    lines.append(
        textwrap.dedent("""\
        For each column × road-class, coverage determines the right modelling strategy:

        - **≥80%**: Include as-is; drop the small fraction of missing rows.
        - **20–80%**: Median-impute and add an `{col}_imputed` binary flag;
          coefficient reflects the imputed value and should be interpreted with caution.
        - **<20%**: The imputed value is invented for >80% of rows. The coefficient
          will primarily reflect the imputation default, not genuine signal.
          Consider excluding from the model or using road-class median as a proxy
          only if the proxy is defensible.

        Note: coverage on major roads (Motorway, A Road) is typically higher because
        OSM contributors prioritise high-traffic routes. If those columns are included
        in a model trained on all road classes, the signal comes almost entirely from
        major roads and the imputed values for minor roads are close to noise.
        """)
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    df, osm_cols = load_data()

    print(f"\nOSM columns present: {osm_cols}")
    print(f"Total links: {len(df):,}")
    print(f"Road classes: {sorted(df['road_classification'].unique())}\n")

    # Overall coverage printout
    print("=== Overall OSM coverage ===")
    for col in osm_cols:
        pct = df[col].notna().mean() * 100
        n   = df[col].notna().sum()
        print(f"  {col:20s}: {pct:5.1f}%  ({n:,} / {len(df):,} links)")

    # By road class
    print("\n=== Coverage by road class ===")
    by_class = coverage_by_class(df, osm_cols)
    pivot = by_class.pivot_table(
        index="road_class", columns="column", values="pct_coverage"
    )
    print(pivot.round(1).fillna("—").to_string())

    # By region
    by_region = coverage_by_region(df, osm_cols)
    print("\n=== Coverage by latitude band ===")
    pivot_r = by_region.pivot_table(
        index="lat_band", columns="column", values="pct_coverage"
    )
    print(pivot_r.round(1).fillna("—").to_string())

    # Value distributions for numeric columns
    for col in [c for c in NUMERIC_OSM if c in osm_cols]:
        print(f"\n=== {col} value distribution by road class ===")
        dist = by_class[by_class["column"] == col].copy()
        dist_cols = ["road_class", "n_filled", "min", "q25", "median", "q75", "max", "n_distinct"]
        print(dist[[c for c in dist_cols if c in dist.columns]].to_string(index=False))

    # Write CSV
    by_class.to_csv(OUT_CSV, index=False)
    print(f"\nFull table written to: {OUT_CSV}")

    # Write Quarto page
    md = build_markdown(by_class, by_region, osm_cols)
    OUT_QMD.write_text(md)
    print(f"Summary written to: {OUT_QMD}")

    # Highlights
    print("\n=== HIGHLIGHTS ===")
    high = by_class[by_class["pct_coverage"] >= 80]
    if not high.empty:
        print(
            "Usable as-is (≥80%):  ",
            list(high[["column", "road_class"]].itertuples(index=False, name=None)),
        )
    else:
        print("No column × class combination reaches 80%")

    low = by_class[by_class["pct_coverage"] < 20]
    if not low.empty:
        print(f"Noisy when imputed (<20%): {len(low)} combinations")
        print(low[["column","road_class","pct_coverage"]].to_string(index=False))


if __name__ == "__main__":
    main()
