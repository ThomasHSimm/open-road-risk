"""
dtc/routes.py
-------------
Process driving test routes from two sources:
  1. GPX files (crowdsourced from plotaroute etc)
  2. Google Maps waypoint URLs (from the UK Driving Test Routes app)

Both are converted to a sequence of OS Open Roads link_ids by routing
through the NetworkX graph we already have from network_features.py.

This replaces the KD-tree snapping approach in ingest_test_routes.py for
Google Maps waypoints, which only gave sparse control points rather than
the full route. NetworkX shortest-path routing between waypoints gives
a complete link sequence consistent with the road network.

Key design
----------
- Load the NetworkX graph once, cache it for batch processing
- For each pair of consecutive waypoints: find nearest graph nodes,
  run Dijkstra shortest path, collect edge link_ids
- GPX files: extract track points, reduce to waypoints via RDP
  simplification, then route the same way
- Output: one row per route with dtc_name, link_ids (list), route stats

Usage
-----
    python src/road_risk/dtc/routes.py
    python src/road_risk/dtc/routes.py --gmaps urls.txt
    python src/road_risk/dtc/routes.py --gpx   # processes data/raw/test_routes/*.gpx
"""

import logging
import re
import time
import json
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import pyproj
from scipy.spatial import cKDTree

from road_risk.config import _ROOT

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
OPENROADS_PATH  = _ROOT / "data/processed/shapefiles/openroads_yorkshire.parquet"
DTC_PATH        = _ROOT / "data/raw/dvsa/dtc_summary.csv"
GPX_DIR         = _ROOT / "data/raw/test_routes"
GMAPS_URLS_PATH = _ROOT / "data/raw/test_routes/gmaps_urls.txt"
OUTPUT_PATH     = _ROOT / "data/processed/test_routes/routed_routes.parquet"
GMAPS_CACHE_DIR = _ROOT / "data/processed/test_routes/gmaps_cache"

# ---------------------------------------------------------------------------
# Coordinate transformer (WGS84 → BNG, shared)
# ---------------------------------------------------------------------------
_WGS_TO_BNG = pyproj.Transformer.from_crs(
    "EPSG:4326", "EPSG:27700", always_xy=True
)

GB_LAT = (49.5, 61.0)
GB_LON = (-8.5,  2.0)
DTC_MAX_DIST_M = 1500   # start/end must be within 1.5km of a DTC
MIN_KM = 3.0
MAX_KM = 50.0


# ---------------------------------------------------------------------------
# Graph loading
# ---------------------------------------------------------------------------

def build_routing_graph(
    openroads: gpd.GeoDataFrame,
) -> tuple[nx.MultiGraph, np.ndarray, np.ndarray, dict]:
    """
    Build a NetworkX graph from OS Open Roads for shortest-path routing.

    Returns
    -------
    G                 : nx.MultiGraph with link_id on each edge
    node_xy           : (N, 2) BNG coordinates for each node (for KD-tree lookup)
    node_ids          : (N,) node ID array aligned with node_xy rows
    start_node_lookup : dict mapping link_id → start_node for direction detection
    """
    logger.info(f"Building routing graph from {len(openroads):,} links ...")

    or_bng = openroads.to_crs("EPSG:27700")

    # MultiGraph preserves parallel links between same node pair
    G = nx.MultiGraph()
    for _, row in or_bng.iterrows():
        u = row["start_node"]
        v = row["end_node"]
        if pd.isna(u) or pd.isna(v):
            continue
        G.add_edge(u, v,
                   link_id=row["link_id"],
                   weight=float(row.get("link_length_m",
                                        row.get("link_length_km", 0.5) * 1000)))

    logger.info(f"  Graph: {G.number_of_nodes():,} nodes, "
                f"{G.number_of_edges():,} edges")

    # Build KD-tree of node positions for nearest-node lookup
    # Node positions: centroid of connected edge geometries
    # Faster approximation: use link endpoint coordinates from geometry
    node_pos = {}
    for _, row in or_bng.iterrows():
        geom = row.geometry
        if geom is None:
            continue
        coords = list(geom.coords)
        if len(coords) < 2:
            continue
        u, v = row["start_node"], row["end_node"]
        if pd.notna(u):
            node_pos[u] = coords[0]
        if pd.notna(v):
            node_pos[v] = coords[-1]

    node_ids = np.array(list(node_pos.keys()))
    node_xy  = np.array(list(node_pos.values()))

    start_node_lookup = {
        row["link_id"]: row["start_node"]
        for _, row in or_bng.iterrows()
        if pd.notna(row.get("start_node")) and pd.notna(row.get("link_id"))
    }
    logger.info(f"  Node positions mapped: {len(node_ids):,}")
    return G, node_xy, node_ids, start_node_lookup


def nearest_node(bng_xy: tuple[float, float],
                 tree: cKDTree,
                 node_ids: np.ndarray,
                 max_dist_m: float = 500) -> str | None:
    """Find the nearest graph node to a BNG coordinate pair."""
    dist, idx = tree.query(bng_xy, k=1, distance_upper_bound=max_dist_m)
    if dist == np.inf:
        return None
    return node_ids[idx]


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def route_waypoints(
    waypoints_latlon: list[tuple[float, float]],
    G: nx.MultiGraph,
    tree: cKDTree,
    node_ids: np.ndarray,
    start_node_lookup: dict | None = None,
) -> list[tuple[int, bool]]:
    """
    Route through a list of (lat, lon) waypoints on the graph.

    Projects each waypoint to BNG, finds nearest graph node, runs
    Dijkstra between consecutive nodes, collects link_ids.

    Returns
    -------
    List of link_ids in traversal order (deduplicated consecutive).
    Empty list if routing fails for all segments.
    """
    # Project waypoints to BNG
    lons = [w[1] for w in waypoints_latlon]
    lats = [w[0] for w in waypoints_latlon]
    eastings, northings = _WGS_TO_BNG.transform(lons, lats)
    bng_waypoints = list(zip(eastings, northings))

    # Find nearest graph node for each waypoint
    nodes = []
    for i, bng in enumerate(bng_waypoints):
        node = nearest_node(bng, tree, node_ids)
        if node is None:
            logger.warning(f"  Waypoint {i} ({waypoints_latlon[i]}) — "
                           f"no graph node within 500m, skipping")
        nodes.append(node)

    # Remove consecutive None or duplicate nodes
    valid_nodes = []
    for n in nodes:
        if n is not None and (not valid_nodes or n != valid_nodes[-1]):
            valid_nodes.append(n)

    if len(valid_nodes) < 2:
        logger.warning("  Too few valid nodes to route")
        return []

    # Route between consecutive nodes
    link_sequence: list[tuple[int, bool]] = []
    n_segments_ok = 0

    for i in range(len(valid_nodes) - 1):
        u, v = valid_nodes[i], valid_nodes[i + 1]
        try:
            path_nodes = nx.shortest_path(G, u, v, weight="weight")
        except nx.NetworkXNoPath:
            logger.debug(f"  No path between nodes {u} → {v}, skipping segment")
            continue
        except nx.NodeNotFound:
            logger.debug(f"  Node not found: {u} or {v}")
            continue

        # Extract (link_id, forward) from path edges
        # MultiGraph returns {key: attr_dict} — pick lightest edge
        for j in range(len(path_nodes) - 1):
            u_n, v_n = path_nodes[j], path_nodes[j + 1]
            edges = G.get_edge_data(u_n, v_n)
            if not edges:
                continue
            best = min(edges.values(), key=lambda e: e.get("weight", 9999))
            if "link_id" not in best:
                continue
            lid = best["link_id"]
            if start_node_lookup is not None:
                forward = (start_node_lookup.get(lid) == u_n)
            else:
                forward = True
            item = (lid, forward)
            if not link_sequence or link_sequence[-1][0] != lid:
                link_sequence.append(item)

        n_segments_ok += 1

    logger.debug(f"  Routed {n_segments_ok}/{len(valid_nodes)-1} segments, "
                 f"{len(link_sequence)} unique links")
    return link_sequence


# ---------------------------------------------------------------------------
# DTC matching
# ---------------------------------------------------------------------------

def load_dtc_lookup() -> gpd.GeoDataFrame:
    df = pd.read_csv(DTC_PATH)
    df = df[df["latitude"].between(*GB_LAT) &
            df["longitude"].between(*GB_LON)].copy()
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs="EPSG:4326",
    ).to_crs("EPSG:27700")
    return gdf


def match_dtc(
    waypoints_latlon: list[tuple[float, float]],
    dtc_gdf: gpd.GeoDataFrame,
) -> dict | None:
    """
    Match start/end of route to nearest DTC.
    Returns dict with dtc_id, dtc_name, distances, or None if no match.
    """
    import geopandas as gpd
    from shapely.geometry import Point

    start_e, start_n = _WGS_TO_BNG.transform(
        waypoints_latlon[0][1], waypoints_latlon[0][0]
    )
    end_e, end_n = _WGS_TO_BNG.transform(
        waypoints_latlon[-1][1], waypoints_latlon[-1][0]
    )

    start_pt = gpd.GeoDataFrame(
        geometry=[Point(start_e, start_n)], crs="EPSG:27700"
    ).iloc[0].geometry

    dists = dtc_gdf.distance(start_pt)
    nearest_idx = dists.idxmin()
    min_dist    = dists.min()

    if min_dist > DTC_MAX_DIST_M:
        logger.warning(f"  Start {min_dist:.0f}m from nearest DTC "
                       f"(cap {DTC_MAX_DIST_M}m)")
        return None

    dtc = dtc_gdf.loc[nearest_idx]
    end_dist = dtc.geometry.distance(Point(end_e, end_n))

    if end_dist > DTC_MAX_DIST_M:
        logger.warning(f"  End {end_dist:.0f}m from '{dtc['name']}' "
                       f"(cap {DTC_MAX_DIST_M}m)")
        return None

    return {
        "dtc_name":           dtc["name"],
        "dtc_id":             dtc.get("id", nearest_idx),
        "start_dist_to_dtc_m": round(min_dist, 1),
        "end_dist_to_dtc_m":   round(end_dist, 1),
    }


# ---------------------------------------------------------------------------
# Google Maps URL source
# ---------------------------------------------------------------------------

def resolve_gmaps_url(url: str, timeout: int = 10) -> str:
    """Follow redirects to get the full Google Maps URL with coordinates."""
    req = Request(url.strip(), headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.url
    except URLError as e:
        raise ValueError(f"Could not resolve {url}: {e}")


def extract_gmaps_waypoints(resolved_url: str) -> list[tuple[float, float]]:
    """Extract (lat, lon) waypoints from a resolved Google Maps URL."""
    coords = re.findall(r'(-?\d+\.\d+),(-?\d+\.\d+)', resolved_url)
    waypoints = [
        (float(lat), float(lon)) for lat, lon in coords
        if GB_LAT[0] <= float(lat) <= GB_LAT[1]
        and GB_LON[0] <= float(lon) <= GB_LON[1]
    ]
    if not waypoints:
        raise ValueError(f"No valid GB coordinates in URL: {resolved_url[:120]}")
    return waypoints


def process_gmaps_urls(
    urls_file: Path,
    G: nx.MultiGraph,
    tree: cKDTree,
    node_ids: np.ndarray,
    dtc_gdf: gpd.GeoDataFrame,
    start_node_lookup: dict | None = None,
    delay_s: float = 1.0,
) -> list[dict]:
    """
    Process a text file of Google Maps URLs.

    File format (tab-separated, name optional):
        https://maps.app.goo.gl/XXX    doncaster_route_01
        https://maps.app.goo.gl/YYY    doncaster_route_02

    Returns list of route dicts ready for DataFrame.
    """
    lines = [l.strip() for l in urls_file.read_text().splitlines()
             if l.strip() and not l.startswith("#")]

    # Cache directory — one JSON file per named route
    GMAPS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for i, line in enumerate(lines, 1):
        parts = line.split("\t")
        url   = parts[0].strip()
        name  = parts[1].strip() if len(parts) > 1 else f"route_{i:03d}"

        # Check cache — skip URL fetch if already processed
        cache_file = GMAPS_CACHE_DIR / f"{name}.json"
        if cache_file.exists():
            import json
            cached = json.loads(cache_file.read_text())
            results.append(cached)
            logger.info(f"[{i}/{len(lines)}] {name} — from cache")
            continue

        logger.info(f"[{i}/{len(lines)}] {name}")
        try:
            resolved  = resolve_gmaps_url(url)
            waypoints = extract_gmaps_waypoints(resolved)

            length_km = _estimate_length_km(waypoints)
            if not (MIN_KM <= length_km <= MAX_KM):
                logger.warning(f"  Invalid length ({length_km:.1f}km) — skipped")
                continue

            dtc_match = match_dtc(waypoints, dtc_gdf)
            if dtc_match is None:
                logger.warning(f"  No DTC match — skipped")
                continue

            links = route_waypoints(waypoints, G, tree, node_ids, start_node_lookup)
            if not links:
                logger.warning(f"  Routing failed — skipped")
                continue

            route_dict = {
                "file_name":       name,
                "source":          "gmaps",
                "n_waypoints":     len(waypoints),
                "route_length_km": round(length_km, 2),
                "n_unique_links":  len(links),
                "link_sequence":   links,
                **dtc_match,
            }
            # Save to cache — convert numpy int64 to native int for JSON
            import json

            def _json_safe(obj):
                if isinstance(obj, (list, tuple)):
                    return [_json_safe(x) for x in obj]
                if hasattr(obj, "item"):  # numpy scalar
                    return obj.item()
                return obj

            cache_safe = {k: _json_safe(v) for k, v in route_dict.items()}
            cache_file.write_text(json.dumps(cache_safe))
            results.append(route_dict)
            logger.info(f"  ✓ {dtc_match['dtc_name']} — "
                        f"{len(links)} links, {length_km:.1f}km")

        except Exception as e:
            logger.warning(f"  ERROR: {e}")

        if i < len(lines):
            time.sleep(delay_s)

    return results


# ---------------------------------------------------------------------------
# GPX source
# ---------------------------------------------------------------------------

def _rdp_simplify(points: list[tuple], epsilon: float = 0.001) -> list[tuple]:
    """
    Ramer-Douglas-Peucker simplification.
    Reduces a dense GPS track to key waypoints.

    epsilon in degrees — 0.001 ≈ 111m, keeps enough waypoints for routing
    without over-simplifying. Previous 0.0001 (~11m) was collapsing loop
    routes (start == end) to a single point.

    Loop routes (start == end) are handled by finding the furthest point
    from start as the midpoint, then recursing on each half.
    """
    if len(points) <= 2:
        return points

    start, end = np.array(points[0]), np.array(points[-1])
    line_vec   = end - start
    line_len   = np.linalg.norm(line_vec)

    if line_len == 0:
        # Loop route: start == end. Find furthest point as midpoint.
        pts   = np.array(points)
        dists = np.sqrt(((pts - start) ** 2).sum(axis=1))
        idx   = int(np.argmax(dists))
        left  = _rdp_simplify(points[:idx + 1], epsilon)
        right = _rdp_simplify(points[idx:], epsilon)
        return left[:-1] + right

    pts   = np.array(points)
    dists = np.abs(np.cross(line_vec, start - pts)) / line_len
    idx   = int(np.argmax(dists))

    if dists[idx] > epsilon:
        left  = _rdp_simplify(points[:idx + 1], epsilon)
        right = _rdp_simplify(points[idx:], epsilon)
        return left[:-1] + right
    return [points[0], points[-1]]


def process_gpx_files(
    gpx_dir: Path,
    G: nx.MultiGraph,
    tree: cKDTree,
    node_ids: np.ndarray,
    dtc_gdf: gpd.GeoDataFrame,
    start_node_lookup: dict | None = None,
    skip_names: set | None = None,
) -> list[dict]:
    """
    Process all GPX files in gpx_dir using NetworkX routing.

    Each GPX track is simplified to key waypoints using RDP, then
    routed through the graph to produce a complete link sequence.
    """
    try:
        import gpxpy
    except ImportError:
        raise ImportError("pip install gpxpy")

    gpx_files = sorted(gpx_dir.glob("*.gpx"))
    if not gpx_files:
        logger.warning(f"No GPX files found in {gpx_dir}")
        return []

    logger.info(f"Processing {len(gpx_files)} GPX files ...")
    results = []

    for gpx_path in gpx_files:
        if skip_names and gpx_path.stem in skip_names:
            logger.debug(f"  {gpx_path.name} — already processed, skipping")
            continue
        logger.info(f"  {gpx_path.name}")
        try:
            with open(gpx_path) as f:
                gpx = gpxpy.parse(f)

            points = []
            for track in gpx.tracks:
                for segment in track.segments:
                    for pt in segment.points:
                        if (GB_LAT[0] <= pt.latitude  <= GB_LAT[1] and
                            GB_LON[0] <= pt.longitude <= GB_LON[1]):
                            points.append((pt.latitude, pt.longitude))

            if len(points) < 5:
                logger.warning(f"    Too few points ({len(points)}) — skipped")
                continue

            # Simplify to key waypoints
            simplified = _rdp_simplify(points, epsilon=0.0002)
            logger.debug(f"    RDP: {len(points)} → {len(simplified)} waypoints")

            length_km = _estimate_length_km(points)
            if not (MIN_KM <= length_km <= MAX_KM):
                logger.warning(f"    Invalid length ({length_km:.1f}km) — skipped")
                continue

            dtc_match = match_dtc(simplified, dtc_gdf)
            if dtc_match is None:
                logger.warning(f"    No DTC match — skipped")
                continue

            links = route_waypoints(simplified, G, tree, node_ids, start_node_lookup)
            if not links:
                logger.warning(f"    Routing failed — skipped")
                continue

            results.append({
                "file_name":       gpx_path.stem,
                "source":          "gpx",
                "n_waypoints":     len(simplified),
                "n_gps_points":    len(points),
                "route_length_km": round(length_km, 2),
                "n_unique_links":  len(links),
                "link_sequence":   links,
                **dtc_match,
            })
            logger.info(f"    ✓ {dtc_match['dtc_name']} — "
                        f"{len(links)} links, {length_km:.1f}km")

        except Exception as e:
            logger.warning(f"    ERROR: {e}")

    return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _estimate_length_km(waypoints_latlon: list[tuple[float, float]]) -> float:
    """Haversine sum of waypoint-to-waypoint distances."""
    if len(waypoints_latlon) < 2:
        return 0.0
    R = 6371.0
    total = 0.0
    for i in range(len(waypoints_latlon) - 1):
        lat1, lon1 = np.radians(waypoints_latlon[i])
        lat2, lon2 = np.radians(waypoints_latlon[i + 1])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
        total += 2 * R * np.arcsin(np.sqrt(a))
    return total


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(process_gpx: bool = True, process_gmaps: bool = True) -> pd.DataFrame:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )

    # Load shared infrastructure once
    logger.info("Loading OS Open Roads ...")
    openroads = gpd.read_parquet(OPENROADS_PATH)

    G, node_xy, node_ids, start_node_lookup = build_routing_graph(openroads)
    tree = cKDTree(node_xy)
    dtc_gdf  = load_dtc_lookup()

    # Load existing results so we can skip already-processed routes
    existing = set()
    if OUTPUT_PATH.exists():
        prev = pd.read_parquet(OUTPUT_PATH)
        existing = set(prev["file_name"].tolist())
        logger.info(f"Found {len(existing)} previously processed routes — will skip")
        all_results = prev.to_dict("records")
    else:
        all_results = []

    # GPX routes
    if process_gpx and GPX_DIR.exists():
        gpx_results = process_gpx_files(
            GPX_DIR, G, tree, node_ids, dtc_gdf, start_node_lookup,
            skip_names=existing
        )
        all_results.extend(gpx_results)
        existing.update(r["file_name"] for r in gpx_results)
        logger.info(f"GPX: {len(gpx_results)} new routes processed")

    # Google Maps URLs
    if process_gmaps and GMAPS_URLS_PATH.exists():
        gmaps_results = process_gmaps_urls(
            GMAPS_URLS_PATH, G, tree, node_ids, dtc_gdf, start_node_lookup
        )
        all_results.extend(gmaps_results)
        logger.info(f"Google Maps: {len(gmaps_results)} routes processed")

    if not all_results:
        logger.warning("No routes processed. Check input files.")
        return pd.DataFrame()

    df = pd.DataFrame(all_results)

    # Normalise link_sequence to consistent [[link_id, forward], ...] format.
    # New GPX routes store (link_id, forward) tuples; cached gmaps routes from
    # JSON store plain ints. PyArrow requires a uniform type to serialise.
    # Serialise link_sequence as JSON string to avoid PyArrow mixed-type issues.
    # Each entry is [[link_id, forward_bool], ...] encoded as a JSON string.
    # analysis.py deserialises with json.loads().
    def _serialise_seq(seq):
        if not seq:
            return "[]"
        if isinstance(seq[0], (list, tuple)):
            return json.dumps([[item[0], bool(item[1])] for item in seq])
        return json.dumps([[lid, True] for lid in seq])

    df["link_sequence"] = df["link_sequence"].apply(_serialise_seq)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    print(f"\n=== Route processing complete ===")
    print(f"  Total routes: {len(df)}")
    print(f"  Centres covered: {df['dtc_name'].nunique()}")
    print(f"\n  Routes per centre:")
    print(df["dtc_name"].value_counts().to_string())
    print(f"\n  Mean links per route: {df['n_unique_links'].mean():.0f}")
    print(f"  Mean route length: {df['route_length_km'].mean():.1f}km")
    print(f"\n  Saved to {OUTPUT_PATH}")

    return df


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpx",    action="store_true", default=True,
                        help="Process GPX files (default: on)")
    parser.add_argument("--gmaps",  action="store_true", default=True,
                        help="Process Google Maps URL file (default: on)")
    parser.add_argument("--no-gpx",   dest="gpx",   action="store_false")
    parser.add_argument("--no-gmaps", dest="gmaps", action="store_false")
    args = parser.parse_args()
    main(process_gpx=args.gpx, process_gmaps=args.gmaps)