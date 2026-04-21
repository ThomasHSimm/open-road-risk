"""
dtc/analysis.py
---------------
Correlate per-route road network features with DVSA test centre pass rates
and fault category rates.

Extended feature set covers:
  - Speed environment (high/low speed proportions)
  - Junction character (roundabouts, T-junctions, crossroads, complexity)
  - Turn analysis (left/right/straight from link geometry bearing changes)
  - Road character (dual carriageway, link length, road class mix)
  - Risk scores (percentile, excess risk, AADT)
  - Source quality flag (gpx vs gmaps)

Usage
-----
    python src/road_risk/dtc/analysis.py
    python src/road_risk/dtc/analysis.py --min-routes 2
"""

import argparse
import logging
from pathlib import Path

import json
import numpy as np
import pandas as pd
from scipy import stats

from road_risk.config import _ROOT

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROUTED_PATH  = _ROOT / "data/processed/test_routes/routed_routes.parquet"
SNAPPED_PATH = _ROOT / "data/processed/test_routes/snapped_routes.parquet"
RISK_PATH    = _ROOT / "data/models/risk_scores.parquet"
NET_PATH     = _ROOT / "data/features/network_features.parquet"
OR_PATH      = _ROOT / "data/processed/shapefiles/openroads_yorkshire.parquet"
DTC_PATH     = _ROOT / "data/raw/dvsa/dtc_summary.csv"
FAILS_PATH     = _ROOT / "data/raw/dvsa/agg_2023_fails_pivot.csv"
REL_PATH       = _ROOT / "data/raw/dvsa/agg_2023_fails_relative_pivot.csv"
ANNEX_D_RATES  = _ROOT / "data/raw/dvsa/annex_d_fault_rates.csv"
MANOEUVRE_PATH = _ROOT / "data/raw/dvsa/manoeuvre_fail_rates.csv"
OUTPUT_PATH    = _ROOT / "data/features/dtc_route_features.parquet"
CORR_PATH      = _ROOT / "data/features/dtc_correlations.csv"

HIGH_SPEED_MPH = 40
LOW_SPEED_MPH  = 30

_CLASS_SPEED_PROXY = {
    "Motorway": 70, "A Road": 50, "B Road": 40,
    "Classified Unnumbered": 30, "Not Classified": 30,
    "Unclassified": 25, "Unknown": 30,
}

KEY_FAULTS = [
    "Junctions - turning right",
    "Junctions - turning left",
    "Junctions - observation",
    "Response to signs - traffic lights",
    "Maintain progress - undue hesitation",
    "Use of speed",
    "Mirrors - change direction",
    "Awareness/planning",
    "Positioning - normal driving",
    "Judgement - crossing",
]

# Fault categories linked to road/route environment
ROAD_LINKED_FAULTS = [
    "junctions_turning_right", "junctions_turning_left",
    "junctions_observation", "junctions_approach_speed",
    "response_to_signs_traffic_lights", "use_of_speed",
    "maintain_progress_undue_hesitation", "positioning_normal_driving",
    "mirrors_change_direction", "judgement_crossing", "judgement_meeting",
    "response_to_signs_traffic_signs", "response_to_signs_road_markings",
]

# Fault categories reflecting general candidate aptitude (levellers)
APTITUDE_FAULTS = [
    "control_clutch", "control_gears", "control_steering",
    "move_off_control", "move_off_safely",
    "signals_necessary", "signals_correctly",
    "vehicle_checks", "eyesight", "precautions",
]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_routes() -> pd.DataFrame:
    for path in [ROUTED_PATH, SNAPPED_PATH]:
        if path.exists():
            df = pd.read_parquet(path)
            logger.info(f"Loaded {len(df)} routes from {path.name}, "
                        f"{df['dtc_name'].nunique()} centres")
            return df
    raise FileNotFoundError(f"No routes found. Run dtc/routes.py first.")


def load_link_features():
    import geopandas as gpd

    or_cols = ["link_id", "road_classification", "form_of_way",
               "road_function", "link_length_km", "is_trunk",
               "is_primary", "geometry"]
    openroads = gpd.read_parquet(OR_PATH)[or_cols]
    link_df = openroads.drop(columns=["geometry"]).copy()

    if RISK_PATH.exists():
        risk = pd.read_parquet(RISK_PATH).drop(
            columns=[c for c in ["road_classification", "link_length_km",
                                  "form_of_way"] if c in
                     pd.read_parquet(RISK_PATH).columns],
            errors="ignore",
        )
        link_df = link_df.merge(risk, on="link_id", how="left")

    if NET_PATH.exists():
        net = pd.read_parquet(NET_PATH)
        want = ["link_id", "degree_mean", "betweenness_relative",
                "dist_to_major_km", "pop_density_per_km2",
                "speed_limit_mph", "is_unpaved"]
        link_df = link_df.merge(
            net[[c for c in want if c in net.columns]],
            on="link_id", how="left"
        )

    # Speed estimate: OSM where available, else road class proxy
    proxy = link_df["road_classification"].map(_CLASS_SPEED_PROXY).fillna(30)
    if "speed_limit_mph" in link_df.columns:
        link_df["speed_est_mph"] = link_df["speed_limit_mph"].fillna(proxy)
    else:
        link_df["speed_est_mph"] = proxy

    logger.info(f"Link features: {len(link_df):,} links")
    return link_df, openroads


# ---------------------------------------------------------------------------
# Turn analysis from geometry
# ---------------------------------------------------------------------------

def _bearing(p1, p2) -> float:
    return np.degrees(np.arctan2(p2[0] - p1[0], p2[1] - p1[1])) % 360


def _bearing_change(b1: float, b2: float) -> float:
    return (b2 - b1 + 180) % 360 - 180


def _link_bearings(
    link_id: int,
    forward: bool,
    geom_lookup: dict,
) -> tuple[float, float] | None:
    """Return (entry_bearing, exit_bearing) accounting for traversal direction."""
    if link_id not in geom_lookup:
        return None
    entry_b, exit_b = geom_lookup[link_id]
    if forward:
        return entry_b, exit_b
    return (exit_b + 180) % 360, (entry_b + 180) % 360


def compute_turn_features(link_sequence: list, openroads_gdf) -> dict:
    """
    Classify each junction in the route as right turn, left turn,
    straight, or U-turn based on bearing change between consecutive links.
    """
    empty = {"pct_right_turns": np.nan, "pct_left_turns": np.nan,
             "pct_straight": np.nan, "n_junctions": 0,
             "right_left_ratio": np.nan}

    if len(link_sequence) < 2:
        return empty

    # Normalise to (link_id, forward) tuples.
    # Three possible formats:
    #   [int, ...]                  legacy plain link_ids (assume forward)
    #   [(link_id, fwd), ...]       tuples from in-memory routing
    #   [[link_id, fwd], ...]       lists after parquet round-trip (tuples → lists)
    first = link_sequence[0]
    if isinstance(first, (tuple, list)):
        seq = [(item[0], bool(item[1])) for item in link_sequence]
    else:
        seq = [(item, True) for item in link_sequence]

    link_ids = {lid for lid, _ in seq}
    or_bng = openroads_gdf[
        openroads_gdf["link_id"].isin(link_ids)
    ].to_crs("EPSG:27700")

    geom_lookup = {}
    for _, row in or_bng.iterrows():
        coords = list(row.geometry.coords)
        if len(coords) >= 2:
            geom_lookup[row["link_id"]] = (
                _bearing(coords[0], coords[1]),
                _bearing(coords[-2], coords[-1]),
            )

    right = left = straight = u_turn = 0
    n = 0

    for i in range(len(seq) - 1):
        lid_a, fwd_a = seq[i]
        lid_b, fwd_b = seq[i + 1]
        ba = _link_bearings(lid_a, fwd_a, geom_lookup)
        bb = _link_bearings(lid_b, fwd_b, geom_lookup)
        if ba is None or bb is None:
            continue
        change = _bearing_change(ba[1], bb[0])
        n += 1
        if 30 <= change <= 150:
            right += 1
        elif -150 <= change <= -30:
            left += 1
        elif abs(change) > 150:
            u_turn += 1
        else:
            straight += 1

    if n == 0:
        return empty

    return {
        "pct_right_turns":   right    / n,
        "pct_left_turns":    left     / n,
        "pct_straight":      straight / n,
        "pct_u_turns":       u_turn   / n,
        "n_junctions":       n,
        "right_left_ratio":  right / left if left > 0 else np.nan,
    }


# ---------------------------------------------------------------------------
# Per-route features
# ---------------------------------------------------------------------------

def compute_route_features(
    routes: pd.DataFrame,
    link_df: pd.DataFrame,
    openroads_gdf,
) -> pd.DataFrame:

    logger.info("Computing per-route features ...")
    rows = []

    for _, row in routes.iterrows():
        links = row["link_sequence"]
        # Deserialise JSON string (from parquet storage)
        if isinstance(links, str):
            links = json.loads(links)
        if not isinstance(links, (list, np.ndarray)) or len(links) == 0:
            continue

        # Unpack link_ids — handles plain ints, tuples, or lists (parquet round-trip)
        if len(links) > 0 and isinstance(links[0], (tuple, list)):
            plain_ids = [item[0] for item in links]
        else:
            plain_ids = list(links)
        rl = link_df[link_df["link_id"].isin(plain_ids)].copy()
        if len(rl) == 0:
            continue

        feat = {
            "dtc_name":        row["dtc_name"],
            "file_name":       row.get("file_name", ""),
            "source":          row.get("source", "unknown"),
            "n_links":         len(rl),
            "route_length_km": row.get("route_length_km", np.nan),
        }

        # Speed environment
        spd = rl["speed_est_mph"].dropna()
        feat["mean_speed_est"]  = spd.mean()
        feat["pct_high_speed"]  = (spd >= HIGH_SPEED_MPH).mean()
        feat["pct_low_speed"]   = (spd <= LOW_SPEED_MPH).mean()
        feat["pct_urban_speed"] = (spd <= 20).mean()

        # Junction character
        if "form_of_way" in rl.columns:
            fow = rl["form_of_way"]
            feat["pct_roundabout"] = (fow == "Roundabout").mean()
            feat["n_roundabouts"]  = int((fow == "Roundabout").sum())
            feat["pct_dual"]       = fow.isin(
                ["Dual Carriageway", "Collapsed Dual Carriageway"]
            ).mean()

        if "degree_mean" in rl.columns:
            deg = rl["degree_mean"].dropna()
            feat["degree_mean_mean"]     = deg.mean()
            feat["pct_t_junction"]       = ((deg >= 2.5) & (deg < 3.5)).mean()
            feat["pct_crossroads"]       = ((deg >= 3.5) & (deg < 4.5)).mean()
            feat["pct_complex_junction"] = (deg >= 4.5).mean()

        # Road class mix
        if "road_classification" in rl.columns:
            counts = rl["road_classification"].value_counts(normalize=True)
            for rc in ["Motorway", "A Road", "B Road",
                       "Classified Unnumbered", "Unclassified"]:
                feat[f"pct_{rc.lower().replace(' ', '_')}"] = counts.get(rc, 0.0)

        # Road character
        if "link_length_km" in rl.columns:
            ll = rl["link_length_km"].dropna()
            feat["mean_link_length_km"] = ll.mean()
            feat["pct_short_links"]     = (ll < 0.1).mean()
            feat["pct_long_links"]      = (ll > 0.5).mean()

        # Network features
        for src, dst in [
            ("betweenness_relative", "betweenness_rel_mean"),
            ("dist_to_major_km",     "dist_to_major_mean"),
            ("pop_density_per_km2",  "pop_density_mean"),
        ]:
            if src in rl.columns:
                feat[dst] = rl[src].dropna().mean()

        # Risk scores
        if "risk_percentile" in rl.columns:
            rp = rl["risk_percentile"].dropna()
            feat["risk_percentile_mean"] = rp.mean()
            feat["risk_percentile_p90"]  = rp.quantile(0.9)
            feat["pct_high_risk"]        = (rp >= 90).mean()

        if "estimated_aadt" in rl.columns:
            feat["estimated_aadt_mean"] = rl["estimated_aadt"].dropna().mean()

        if "residual_glm" in rl.columns:
            feat["residual_glm_mean"] = rl["residual_glm"].dropna().mean()

        # Turn analysis — pass links directly (JSON string or list handled inside)
        try:
            feat.update(compute_turn_features(links, openroads_gdf))
        except Exception as e:
            logger.debug(f"  Turn analysis failed for {row.get('file_name')}: {e}")

        rows.append(feat)

    result = pd.DataFrame(rows)
    logger.info(f"Per-route features: {len(result)} routes, "
                f"{result.shape[1]} cols")
    return result


def aggregate_to_dtc(route_features: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = route_features.select_dtypes(include=[np.number]).columns.tolist()
    agg = {c: "mean" for c in numeric_cols}
    agg["file_name"] = "count"
    agg["source"]    = lambda x: "/".join(sorted(x.unique()))

    out = (
        route_features.groupby("dtc_name").agg(agg)
        .reset_index()
        .rename(columns={"file_name": "n_routes"})
    )

    src = (
        route_features.groupby(["dtc_name", "source"])
        .size().unstack(fill_value=0)
        .rename(columns=lambda c: f"n_{c}")
        .reset_index()
    )
    out = out.merge(src, on="dtc_name", how="left")
    out["mixed_sources"] = (
        out.get("n_gpx", pd.Series(0, index=out.index)) > 0
    ) & (
        out.get("n_gmaps", pd.Series(0, index=out.index)) > 0
    )

    logger.info(f"Per-DTC features: {len(out)} centres")
    return out


# ---------------------------------------------------------------------------
# Outcomes
# ---------------------------------------------------------------------------

def load_dtc_outcomes() -> pd.DataFrame:
    dtc = pd.read_csv(DTC_PATH).rename(columns={
        "pass": "overall_pass_rate",
        "isFirstAttempt": "first_attempt_pass_rate",
        "name": "dtc_name",
    })

    # Annex D: SD + minor fault rates per test, 110 columns
    if ANNEX_D_RATES.exists():
        ann = pd.read_csv(ANNEX_D_RATES)
        ann["name"] = ann["name"].str.strip()
        rate_cols = [c for c in ann.columns if c.endswith("_rate")]
        dtc = dtc.merge(
            ann[["name"] + rate_cols],
            left_on="dtc_name", right_on="name", how="left"
        ).drop(columns=["name"], errors="ignore")
        logger.info(f"Annex D rates joined: {len(rate_cols)} cols")
        # Composite indices
        road_sd    = [f"sd_{f}_rate"    for f in ROAD_LINKED_FAULTS if f"sd_{f}_rate"    in dtc.columns]
        apt_sd     = [f"sd_{f}_rate"    for f in APTITUDE_FAULTS    if f"sd_{f}_rate"    in dtc.columns]
        road_minor = [f"minor_{f}_rate" for f in ROAD_LINKED_FAULTS if f"minor_{f}_rate" in dtc.columns]
        apt_minor  = [f"minor_{f}_rate" for f in APTITUDE_FAULTS    if f"minor_{f}_rate" in dtc.columns]
        if road_sd:
            dtc["road_fault_index_sd"]    = dtc[road_sd].mean(axis=1)
            dtc["aptitude_index_sd"]      = dtc[apt_sd].mean(axis=1) if apt_sd else np.nan
            dtc["adjusted_difficulty_sd"] = dtc["road_fault_index_sd"] - dtc["aptitude_index_sd"]
        if road_minor:
            dtc["road_fault_index_minor"]    = dtc[road_minor].mean(axis=1)
            dtc["aptitude_index_minor"]      = dtc[apt_minor].mean(axis=1) if apt_minor else np.nan
            dtc["adjusted_difficulty_minor"] = dtc["road_fault_index_minor"] - dtc["aptitude_index_minor"]
    else:
        logger.warning(f"Annex D rates not found at {ANNEX_D_RATES}")

    # Manoeuvre fail rates
    if MANOEUVRE_PATH.exists():
        man = pd.read_csv(MANOEUVRE_PATH)
        man["name"] = man["name"].str.strip()
        man_cols = [c for c in man.columns if c.endswith("_fail_rate")]
        dtc = dtc.merge(
            man[["name"] + man_cols],
            left_on="dtc_name", right_on="name", how="left"
        ).drop(columns=["name"], errors="ignore")
        logger.info(f"Manoeuvre fail rates joined: {len(man_cols)} cols")
    else:
        logger.warning(f"Manoeuvre rates not found at {MANOEUVRE_PATH}")

    logger.info(f"DTC outcomes: {len(dtc)} centres, {dtc.shape[1]} cols")
    return dtc


# ---------------------------------------------------------------------------
# Correlations
# ---------------------------------------------------------------------------

def run_correlations(
    dtc_features: pd.DataFrame,
    dtc_outcomes: pd.DataFrame,
    min_routes: int = 2,
    gpx_only: bool = False,
) -> pd.DataFrame:

    df = dtc_features[dtc_features["n_routes"] >= min_routes].copy()

    if gpx_only:
        n_gmaps = df.get("n_gmaps", pd.Series(0, index=df.index))
        df = df[n_gmaps == 0]
        logger.info(f"GPX-only: {len(df)} centres")

    if len(df) < 4:
        logger.warning(f"Too few centres ({len(df)}) for meaningful correlations")
        return pd.DataFrame()

    outcome_cols = ["first_attempt_pass_rate", "overall_pass_rate"]
    for col in ["road_fault_index_sd", "road_fault_index_minor",
                "adjusted_difficulty_sd", "adjusted_difficulty_minor"]:
        if col in dtc_outcomes.columns:
            outcome_cols.append(col)
    for f in ROAD_LINKED_FAULTS:
        for pfx in ["sd_", "minor_"]:
            col = f"{pfx}{f}_rate"
            if col in dtc_outcomes.columns:
                outcome_cols.append(col)
    for col in [c for c in dtc_outcomes.columns if c.endswith("_fail_rate")]:
        outcome_cols.append(col)

    merged = df.merge(
        dtc_outcomes[["dtc_name"] + [c for c in outcome_cols
                                     if c in dtc_outcomes.columns]],
        on="dtc_name", how="inner",
    )

    if len(merged) == 0:
        logger.warning("No centres matched between routes and outcomes")
        return pd.DataFrame()

    logger.info(f"Correlation analysis: {len(merged)} centres")

    feat_cols = [
        c for c in df.columns
        if c not in {"dtc_name", "n_routes", "source", "file_name",
                     "mixed_sources"}
        and not c.startswith("n_")
    ]

    rows = []
    for fc in feat_cols:
        if fc not in merged.columns:
            continue
        x = merged[fc].dropna()
        if len(x) < 4:
            continue
        for oc in outcome_cols:
            if oc not in merged.columns:
                continue
            y = merged.loc[x.index, oc].dropna()
            idx = x.index.intersection(y.index)
            if len(idx) < 4:
                continue
            r, p = stats.pearsonr(x[idx], y[idx])
            rows.append({
                "feature": fc, "outcome": oc,
                "r": round(r, 3), "p": round(p, 3),
                "n": len(idx),
                "sig": "**" if p < 0.01 else ("*" if p < 0.05 else ""),
            })

    if not rows:
        return pd.DataFrame()

    out = pd.DataFrame(rows)
    out["abs_r"] = out["r"].abs()
    return out.sort_values(["outcome", "abs_r"], ascending=[True, False])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(min_routes: int = 2) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )

    routes       = load_routes()
    link_df, or_gdf = load_link_features()
    dtc_outcomes = load_dtc_outcomes()

    route_features = compute_route_features(routes, link_df, or_gdf)
    dtc_features   = aggregate_to_dtc(route_features)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dtc_features.to_parquet(OUTPUT_PATH, index=False)

    # Summary
    print("\n=== Per-DTC route features ===")
    show = [c for c in [
        "dtc_name", "n_routes", "source",
        "risk_percentile_mean", "degree_mean_mean",
        "pct_roundabout", "pct_right_turns", "pct_left_turns",
        "pct_high_speed", "pct_t_junction", "mixed_sources",
    ] if c in dtc_features.columns]
    print(dtc_features[show].sort_values(
        "risk_percentile_mean", ascending=False
    ).to_string(index=False))

    # All-source correlations
    print(f"\n=== Correlations — all sources (min {min_routes} routes) ===")
    corr = run_correlations(dtc_features, dtc_outcomes, min_routes)
    if not corr.empty:
        fa = corr[corr["outcome"] == "first_attempt_pass_rate"].head(15)
        print("\n--- vs first-attempt pass rate ---")
        print(fa[["feature", "r", "p", "sig", "n"]].to_string(index=False))

        key_outcomes = [
            "road_fault_index_sd", "road_fault_index_minor",
            "adjusted_difficulty_sd",
            "sd_junctions_turning_right_rate", "sd_junctions_turning_left_rate",
            "sd_response_to_signs_traffic_lights_rate",
            "minor_junctions_turning_right_rate",
            "reverse_right_fail_rate", "reverse_park_fail_rate",
        ]
        for oc in key_outcomes:
            top = corr[corr["outcome"] == oc].head(5)
            if not top.empty:
                print(f"\n--- vs '{oc}' ---")
                print(top[["feature", "r", "p", "sig", "n"]].to_string(
                    index=False))

        corr.to_csv(CORR_PATH, index=False)
        logger.info(f"Saved to {CORR_PATH}")

    # GPX-only for quality check
    print("\n=== GPX-only correlations ===")
    corr_gpx = run_correlations(dtc_features, dtc_outcomes,
                                min_routes, gpx_only=True)
    if not corr_gpx.empty:
        fa_gpx = corr_gpx[
            corr_gpx["outcome"] == "first_attempt_pass_rate"
        ].head(10)
        print(fa_gpx[["feature", "r", "p", "sig", "n"]].to_string(index=False))
        corr_gpx.to_csv(
            CORR_PATH.with_name("dtc_correlations_gpx_only.csv"), index=False
        )

    print(f"\nCentres in analysis: {len(dtc_features)}")
    print("Note: small N — all findings exploratory.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-routes", type=int, default=2)
    args = parser.parse_args()
    main(min_routes=args.min_routes)