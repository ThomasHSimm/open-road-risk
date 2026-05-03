"""
Compare current Stage 2 HGV share with WebTRIS HGV percentage.

This diagnostic answers whether the model-facing `hgv_proportion` is
effectively the same descriptor as WebTRIS `adt24largevehiclepercentage` on
sites snapped to Open Roads links.
"""

from __future__ import annotations

import matplotlib
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

from road_risk.config import _ROOT

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

SUPPORTING = _ROOT / "reports/supporting"
SNAP_MAP = SUPPORTING / "temporal_leakage_site_link_map.csv"
SITE_MONTH_PROFILE = SUPPORTING / "temporal_hgv_site_month_profile.csv"
RISK_SCORES = _ROOT / "data/models/risk_scores.parquet"

OUT_CSV = SUPPORTING / "hgv_aadf_vs_webtris_correlation.csv"
OUT_PNG = SUPPORTING / "hgv_aadf_vs_webtris_correlation.png"


def _weighted_site_hgv(profile: pd.DataFrame) -> pd.DataFrame:
    """Average raw-derived site-month HGV% across months/years."""
    profile = profile.copy()
    profile["site_id"] = profile["site_id"].astype(str)
    profile["weighted_hgv"] = profile["mean_hgv_pct"] * profile["n_records"]
    site = (
        profile.groupby("site_id", as_index=False, observed=True)
        .agg(
            weighted_hgv=("weighted_hgv", "sum"),
            webtris_hgv_records=("n_records", "sum"),
            webtris_n_months=("monthname", "nunique"),
            webtris_road_type=(
                "road_type",
                lambda x: x.mode().iat[0] if not x.mode().empty else np.nan,
            ),
        )
        .reset_index(drop=True)
    )
    site["webtris_hgv_pct"] = site["weighted_hgv"] / site["webtris_hgv_records"]
    return site.drop(columns=["weighted_hgv"])


def build_comparison() -> tuple[pd.DataFrame, pd.DataFrame]:
    site_map = pd.read_csv(SNAP_MAP)
    site_map["site_id"] = site_map["site_id"].astype(str)
    site_hgv = _weighted_site_hgv(pd.read_csv(SITE_MONTH_PROFILE))

    risk = pd.read_parquet(
        RISK_SCORES,
        columns=["link_id", "hgv_proportion", "road_classification", "collision_count"],
    ).rename(
        columns={
            "link_id": "snapped_link_id",
            "hgv_proportion": "aadf_hgv_proportion",
        }
    )
    risk["aadf_hgv_pct"] = risk["aadf_hgv_proportion"] * 100

    rows = site_map.merge(site_hgv, on="site_id", how="left").merge(
        risk, on="snapped_link_id", how="left"
    )
    rows["hgv_pct_abs_diff"] = (rows["aadf_hgv_pct"] - rows["webtris_hgv_pct"]).abs()
    rows["hgv_pct_signed_diff"] = rows["aadf_hgv_pct"] - rows["webtris_hgv_pct"]
    valid = rows.dropna(subset=["aadf_hgv_pct", "webtris_hgv_pct"])

    if len(valid) >= 2:
        pearson_r, pearson_p = pearsonr(valid["aadf_hgv_pct"], valid["webtris_hgv_pct"])
        spearman_r, spearman_p = spearmanr(valid["aadf_hgv_pct"], valid["webtris_hgv_pct"])
    else:
        pearson_r = pearson_p = spearman_r = spearman_p = np.nan

    all_hgv = pd.read_parquet(RISK_SCORES, columns=["hgv_proportion"])["hgv_proportion"]
    summary = pd.DataFrame(
        [
            {
                "row_type": "summary",
                "n_sites_in_snap_map": len(rows),
                "n_sites_with_webtris_hgv": int(rows["webtris_hgv_pct"].notna().sum()),
                "n_sites_with_aadf_hgv": int(rows["aadf_hgv_pct"].notna().sum()),
                "n_sites_compared": int(len(valid)),
                "pearson_r": float(pearson_r) if np.isfinite(pearson_r) else np.nan,
                "pearson_p": float(pearson_p) if np.isfinite(pearson_p) else np.nan,
                "spearman_r": float(spearman_r) if np.isfinite(spearman_r) else np.nan,
                "spearman_p": float(spearman_p) if np.isfinite(spearman_p) else np.nan,
                "median_abs_diff_pct_points": (
                    float(valid["hgv_pct_abs_diff"].median()) if len(valid) else np.nan
                ),
                "mean_signed_diff_pct_points": (
                    float(valid["hgv_pct_signed_diff"].mean()) if len(valid) else np.nan
                ),
                "risk_scores_aadf_hgv_missing_share_all_links": float(all_hgv.isna().mean()),
            }
        ]
    )
    return rows, summary


def write_outputs(rows: pd.DataFrame, summary: pd.DataFrame) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    rows_out = rows.copy()
    rows_out.insert(0, "row_type", "site")
    for col in summary.columns:
        if col not in rows_out.columns:
            rows_out[col] = np.nan
    for col in rows_out.columns:
        if col not in summary.columns:
            summary[col] = np.nan
    pd.concat([summary[rows_out.columns], rows_out], ignore_index=True).to_csv(OUT_CSV, index=False)

    valid = rows.dropna(subset=["aadf_hgv_pct", "webtris_hgv_pct"]).copy()
    pearson_r = summary.loc[0, "pearson_r"]
    spearman_r = summary.loc[0, "spearman_r"]
    median_abs_diff = summary.loc[0, "median_abs_diff_pct_points"]

    fig, ax = plt.subplots(figsize=(7, 6), dpi=160)
    if len(valid):
        classes = valid["road_classification"].fillna("Unknown")
        labels = sorted(classes.unique())
        cmap = plt.get_cmap("tab10")
        for i, label in enumerate(labels):
            sub = valid[classes == label]
            ax.scatter(
                sub["aadf_hgv_pct"],
                sub["webtris_hgv_pct"],
                s=18,
                alpha=0.55,
                color=cmap(i % 10),
                label=str(label),
                edgecolors="none",
            )
        max_val = float(np.nanmax([valid["aadf_hgv_pct"].max(), valid["webtris_hgv_pct"].max(), 1]))
        ax.plot(
            [0, max_val],
            [0, max_val],
            color="black",
            linewidth=1,
            linestyle="--",
            label="1:1",
        )
        ax.set_xlim(left=0, right=max_val * 1.05)
        ax.set_ylim(bottom=0, top=max_val * 1.05)
        ax.legend(loc="lower right", fontsize=8, frameon=True)

    ax.set_xlabel("AADF hgv_proportion from risk_scores (%)")
    ax.set_ylabel("WebTRIS mean adt24largevehiclepercentage (%)")
    ax.set_title("AADF vs WebTRIS HGV share on snapped WebTRIS sites")
    ax.text(
        0.02,
        0.98,
        (
            f"n={len(valid):,}\n"
            f"Pearson r={pearson_r:.3f}\n"
            f"Spearman r={spearman_r:.3f}\n"
            f"Median abs diff={median_abs_diff:.2f} pp"
        ),
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "#cccccc"},
    )
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT_PNG)
    plt.close(fig)


def main() -> None:
    rows, summary = build_comparison()
    write_outputs(rows, summary)
    print(summary.to_string(index=False))
    print(f"Wrote {OUT_CSV.relative_to(_ROOT)}")
    print(f"Wrote {OUT_PNG.relative_to(_ROOT)}")


if __name__ == "__main__":
    main()
