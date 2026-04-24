"""
network_features.py
-------------------
Computes network topology and population demand features for all OS Open Roads
links. These are the "Big 3" features that replace lat/lon as spatial signal
in the AADT estimator, giving the model genuine causal structure.

Feature 1 — Node degree (junction complexity)
    Mean degree of start/end nodes of each link.
    High = urban junction-heavy road.
    Low = long uninterrupted rural link.

Feature 2 — Betweenness centrality (network importance)
    Approximate betweenness using sampled shortest paths (k=500).
    High = this road is on many shortest paths = likely through-traffic corridor.
    Low = cul-de-sac or genuinely local road.
    Computed on simplified graph (major roads only for speed), then propagated
    to all links via nearest major-road node.

Feature 3 — Distance to nearest major road (node)
    Graph-distance (in km) from each link's nearest node to the nearest
    Motorway or A Road node.
    Small = feeder road, close to trunk network.
    Large = genuinely isolated local road.

Feature 4 — Population density (LSOA join)
    Population per km² of the LSOA whose centroid is nearest to the road link
    centroid, within 2km. Proxy for local demand.
    Requires: data/raw/stats19/lsoa_population.csv
    Download from: https://www.ons.gov.uk/peoplepopulationandcommunity/
                   populationandmigration/populationestimates/datasets/
                   lowersuperoutputareamidyearpopulationestimates

Feature 5 — Rural-Urban Classification (LSOA join)
    ONS 2021 Rural-Urban Classification attached via the same nearest-centroid
    LSOA assignment used for population density. Adds the raw class code and a
    derived Urban/Rural split.

Usage
-----
    python src/road_risk/features/network.py

    Or from model.py:
        from road_risk.features.network import build_network_features
        features_df = build_network_features(openroads)
"""

import gc
import json
import logging
import shutil
import subprocess
import threading
import time
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from road_risk.config import _ROOT

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Heartbeat — logs progress every N seconds for long-running steps
# ---------------------------------------------------------------------------

class _Heartbeat:
    """
    Context manager that logs a 'still running' message every interval_s
    seconds in a background thread. Useful for long NetworkX computations
    that have no built-in progress callbacks.

    Usage:
        with _Heartbeat("Computing betweenness", interval_s=30):
            result = nx.betweenness_centrality(G, k=200)
    """
    def __init__(self, label: str, interval_s: int = 30):
        self.label     = label
        self.interval  = interval_s
        self._stop     = threading.Event()
        self._thread   = threading.Thread(target=self._run, daemon=True)
        self._started  = None

    def _run(self):
        while not self._stop.wait(self.interval):
            elapsed = int(time.time() - self._started)
            logger.info(
                f"  ... {self.label} still running "
                f"({elapsed}s elapsed, be patient)"
            )

    def __enter__(self):
        self._started = time.time()
        self._thread.start()
        return self

    def __exit__(self, *args):
        self._stop.set()
        self._thread.join()
        elapsed = int(time.time() - self._started)
        logger.info(f"  ... {self.label} finished in {elapsed}s")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROCESSED      = _ROOT / "data/processed"
OPENROADS_PATH = PROCESSED / "shapefiles/openroads_yorkshire.parquet"
LSOA_CENT_PATH = _ROOT / "data/raw/stats19/lsoa_centroids.csv"
LSOA_POP_PATH  = _ROOT / "data/raw/stats19/lsoa_population.csv"
RUC_PATH       = _ROOT / "data/raw/ons/ruc_2021_lsoa_ew.csv"
OUTPUT_PATH    = _ROOT / "data/features/network_features.parquet"
RUC_PROV_PATH  = _ROOT / "data/features/ruc_provenance.json"

# Betweenness centrality sample size — higher = more accurate, slower
# 500 gives a good approximation in ~2-3 minutes for Yorkshire
BETWEENNESS_K = 200

# Max distance for population density join (metres)
POP_JOIN_CAP_M = 2000

# Road classifications that count as "major"
MAJOR_CLASSES = {"Motorway", "A Road"}
RUC_REQUIRED_COLUMNS = ["LSOA21CD", "RUC21CD", "RUC21NM"]


def get_script_git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def load_ruc_lookup(ruc_path: Path = RUC_PATH) -> pd.DataFrame:
    """
    Load the ONS 2021 Rural-Urban Classification lookup keyed by LSOA21CD.

    Fails fast with a clear message if the source file is missing or malformed.
    """
    if not ruc_path.exists():
        raise FileNotFoundError(
            f"RUC CSV not found at {ruc_path}. Expected columns: "
            f"{', '.join(RUC_REQUIRED_COLUMNS)}."
        )

    header = pd.read_csv(ruc_path, nrows=0, encoding="utf-8-sig")
    missing = [col for col in RUC_REQUIRED_COLUMNS if col not in header.columns]
    if missing:
        raise ValueError(
            f"RUC CSV at {ruc_path} is missing required columns: {missing}. "
            f"Found columns: {header.columns.tolist()}."
        )

    ruc = pd.read_csv(
        ruc_path,
        usecols=RUC_REQUIRED_COLUMNS,
        encoding="utf-8-sig",
    ).copy()
    ruc["LSOA21CD"] = ruc["LSOA21CD"].astype("string").str.strip()
    ruc["RUC21CD"] = ruc["RUC21CD"].astype("string").str.strip().str.upper()
    ruc["RUC21NM"] = ruc["RUC21NM"].astype("string").str.strip()

    dupes = int(ruc["LSOA21CD"].duplicated().sum())
    if dupes:
        raise ValueError(
            f"RUC CSV at {ruc_path} contains {dupes:,} duplicate LSOA21CD rows; "
            "expected one row per LSOA."
        )

    logger.info(
        "  Loaded %s RUC rows with %s unique classes",
        f"{len(ruc):,}",
        f"{ruc['RUC21CD'].nunique(dropna=True):,}",
    )
    return ruc


def derive_ruc_urban_rural(ruc_class: pd.Series) -> pd.Series:
    """
    Collapse detailed RUC codes into an Urban/Rural top-level split.

    Supports both the 8-class A1..E2 coding described in the task brief and the
    2021 source variant observed in the supplied ONS CSV (UN1/UF1/RSN1/...).
    """
    urban_8 = {"A1", "B1", "C1", "C2"}
    rural_8 = {"D1", "D2", "E1", "E2"}

    def _map_one(value):
        if pd.isna(value):
            return pd.NA
        code = str(value).strip().upper()
        if code in urban_8 or code.startswith("U"):
            return "Urban"
        if code in rural_8 or code.startswith("R"):
            return "Rural"
        return pd.NA

    return ruc_class.map(_map_one).astype("string")


def write_ruc_provenance(features: pd.DataFrame) -> None:
    def _counts(series: pd.Series) -> dict[str, int]:
        counts = (
            series.astype("object")
            .where(series.notna(), "NaN")
            .value_counts(dropna=False)
            .sort_index()
        )
        return {str(k): int(v) for k, v in counts.items()}

    n_links_total = int(len(features))
    n_links_with_ruc = int(features["ruc_class"].notna().sum())
    coverage_pct = (100.0 * n_links_with_ruc / n_links_total) if n_links_total else 0.0

    provenance = {
        "script_path": str(Path(__file__).resolve()),
        "git_sha": get_script_git_sha(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "ruc_source": "ONS 2021 RUC at LSOA grain, E+W, geoportal.statistics.gov.uk",
        "n_links_total": n_links_total,
        "n_links_with_ruc": n_links_with_ruc,
        "coverage_pct": coverage_pct,
        "ruc_urban_rural_distribution": _counts(features["ruc_urban_rural"]),
        "ruc_class_distribution": _counts(features["ruc_class"]),
    }

    RUC_PROV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RUC_PROV_PATH, "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)
    logger.info(f"Wrote RUC provenance to {RUC_PROV_PATH}")


# ---------------------------------------------------------------------------
# Graph building
# ---------------------------------------------------------------------------

def build_graph(openroads: gpd.GeoDataFrame) -> nx.Graph:
    """
    Build an undirected NetworkX graph from OS Open Roads links.

    Nodes = start_node / end_node TOIDs
    Edges = road links with weight = link_length_km

    Parameters
    ----------
    openroads : GeoDataFrame with link_id, start_node, end_node,
                link_length_km, road_classification columns
    """
    logger.info(f"Building graph from {len(openroads):,} road links ...")

    G = nx.Graph()

    # Add edges with progress logging
    n = len(openroads)
    for i, (_, row) in enumerate(openroads.iterrows()):
        if i % 100_000 == 0 and i > 0:
            logger.info(f"  ... graph build {i:,} / {n:,} links ({i/n:.0%})")
        u = row["start_node"]
        v = row["end_node"]
        if pd.isna(u) or pd.isna(v):
            continue
        G.add_edge(
            u, v,
            link_id=row["link_id"],
            weight=max(row.get("link_length_km", 0.1) or 0.1, 0.001),
            road_classification=row.get("road_classification", "Unknown"),
        )

    logger.info(
        f"  Graph: {G.number_of_nodes():,} nodes, "
        f"{G.number_of_edges():,} edges"
    )
    return G


# ---------------------------------------------------------------------------
# Feature 1: Node degree
# ---------------------------------------------------------------------------

def compute_node_degree(
    G: nx.Graph,
    openroads: gpd.GeoDataFrame,
) -> pd.Series:
    """
    Compute mean node degree for each road link.

    Returns
    -------
    Series indexed by link_id with degree_mean values.
    """
    logger.info("Computing node degree ...")
    degree = dict(G.degree())

    results = {}
    for _, row in openroads.iterrows():
        u = row["start_node"]
        v = row["end_node"]
        deg_u = degree.get(u, 1)
        deg_v = degree.get(v, 1)
        results[row["link_id"]] = (deg_u + deg_v) / 2

    s = pd.Series(results, name="degree_mean")
    logger.info(
        f"  degree_mean: median={s.median():.1f}, "
        f"max={s.max():.0f} (high = complex junction area)"
    )
    return s


# ---------------------------------------------------------------------------
# Feature 2: Betweenness centrality
# ---------------------------------------------------------------------------

def compute_betweenness(
    G: nx.Graph,
    openroads: gpd.GeoDataFrame,
    k: int = BETWEENNESS_K,
) -> pd.Series:
    """
    Compute approximate betweenness centrality for each road link.

    Uses NODE betweenness (faster than edge betweenness) with k-sampled
    shortest paths, then aggregates to links as the mean of endpoint values.

    Node betweenness is O(k × V) vs edge betweenness O(k × V × E/V) —
    much faster on large graphs like OS Open Roads (700k+ edges).

    Returns
    -------
    Series indexed by link_id with betweenness values.
    """
    logger.info(
        f"Computing node betweenness centrality (k={k}, ~1-3 mins) ..."
    )

    # Node betweenness — faster than edge betweenness on large graphs
    with _Heartbeat("betweenness centrality", interval_s=30):
        node_bc = nx.betweenness_centrality(G, k=k, seed=42, weight="weight")

    # Aggregate to links: mean betweenness of start/end nodes
    results = {}
    for _, row in openroads.iterrows():
        u, v = row["start_node"], row["end_node"]
        bc_u = node_bc.get(u, 0.0)
        bc_v = node_bc.get(v, 0.0)
        results[row["link_id"]] = (bc_u + bc_v) / 2

    s = pd.Series(results, name="betweenness").reindex(
        openroads["link_id"], fill_value=0.0
    )

    logger.info(
        f"  betweenness: median={s.median():.6f}, "
        f"p99={s.quantile(0.99):.6f} | "
        f"{(s > 0).sum():,} links with non-zero betweenness"
    )
    return s


# ---------------------------------------------------------------------------
# Feature 3: Distance to nearest major road
# ---------------------------------------------------------------------------

def compute_dist_to_major(
    G: nx.Graph,
    openroads: gpd.GeoDataFrame,
) -> pd.Series:
    """
    Compute graph-distance (km) from each link to the nearest
    Motorway or A Road node.

    Uses multi-source Dijkstra from all major-road nodes simultaneously.

    Returns
    -------
    Series indexed by link_id with dist_to_major_km values.
    """
    logger.info("Computing distance to nearest major road ...")

    # Identify major road nodes
    major_links = openroads[
        openroads["road_classification"].isin(MAJOR_CLASSES)
    ]
    major_nodes = set()
    for _, row in major_links.iterrows():
        if pd.notna(row["start_node"]):
            major_nodes.add(row["start_node"])
        if pd.notna(row["end_node"]):
            major_nodes.add(row["end_node"])

    major_nodes = major_nodes & set(G.nodes())
    logger.info(f"  {len(major_nodes):,} major road nodes as sources")

    if not major_nodes:
        logger.warning("No major road nodes found — returning zeros")
        return pd.Series(0.0, index=openroads["link_id"], name="dist_to_major_km")

    # Multi-source Dijkstra — distance from each node to nearest major node
    with _Heartbeat("dist_to_major Dijkstra", interval_s=15):
        node_dist = nx.multi_source_dijkstra_path_length(
            G, sources=major_nodes, weight="weight"
        )

    # Assign to links: use minimum of start/end node distances
    results = {}
    for _, row in openroads.iterrows():
        u, v = row["start_node"], row["end_node"]
        d_u = node_dist.get(u, np.nan)
        d_v = node_dist.get(v, np.nan)
        if pd.notna(d_u) and pd.notna(d_v):
            results[row["link_id"]] = min(d_u, d_v)
        elif pd.notna(d_u):
            results[row["link_id"]] = d_u
        elif pd.notna(d_v):
            results[row["link_id"]] = d_v
        else:
            results[row["link_id"]] = np.nan

    s = pd.Series(results, name="dist_to_major_km")
    logger.info(
        f"  dist_to_major_km: median={s.median():.2f}km, "
        f"p90={s.quantile(0.9):.2f}km"
    )
    return s


# ---------------------------------------------------------------------------
# Feature 4: Population density
# ---------------------------------------------------------------------------

def compute_population_density(
    openroads: gpd.GeoDataFrame,
    lsoa_cent_path: Path = LSOA_CENT_PATH,
    lsoa_pop_path: Path = LSOA_POP_PATH,
    cap_m: float = POP_JOIN_CAP_M,
    return_lsoa_assignment: bool = False,
):
    """
    Compute population density (people/km²) for each road link by joining
    to the nearest LSOA centroid within cap_m metres.

    Requires two files:
      lsoa_centroids.csv  — LSOA21CD, x, y (BNG) — already downloaded
      lsoa_population.*   — ONS LSOA mid-year population estimates
                            Excel: "Mid-2024 LSOA 2021" sheet, data from row 4
                            Columns: LAD 2023 Code, LAD 2023 Name,
                                     LSOA 2021 Code, LSOA 2021 Name, Total, ...
                            Save as data/raw/stats19/lsoa_population.xlsx
                            or      data/raw/stats19/lsoa_population.csv

    Returns
    -------
    Series indexed by link_id with pop_density_per_km2 values.
    NaN where no LSOA centroid within cap_m metres.

    If return_lsoa_assignment=True, also returns a second Series containing the
    assigned LSOA21CD from the same nearest-centroid join.
    """
    if not lsoa_cent_path.exists():
        logger.warning(
            f"LSOA centroids not found at {lsoa_cent_path} — "
            "population density feature will be NaN"
        )
        density = pd.Series(
            np.nan,
            index=openroads["link_id"],
            name="pop_density_per_km2",
        )
        if return_lsoa_assignment:
            assignment = pd.Series(
                pd.array([pd.NA] * len(openroads), dtype="string"),
                index=openroads["link_id"],
                name="lsoa21cd_assigned",
            )
            return density, assignment
        return density

    # --- Load LSOA centroids (BNG x, y) ------------------------------------
    lsoa_cent = pd.read_csv(
        lsoa_cent_path,
        usecols=["LSOA21CD", "x", "y"],
        encoding="utf-8-sig",
    )

    # --- Load population ----------------------------------------------------
    # Try Excel first, then CSV fallback
    pop_loaded = False
    lsoa_pop = None

    # Check for Excel file
    xl_path = lsoa_pop_path.with_suffix(".xlsx")
    if xl_path.exists():
        logger.info(f"  Reading population from Excel: {xl_path.name}")
        try:
            raw = pd.read_excel(
                xl_path,
                sheet_name="Mid-2024 LSOA 2021",
                header=3,          # row 4 = index 3 is the header
                usecols=[2, 4],    # LSOA 2021 Code, Total
            )
            raw.columns = ["LSOA21CD", "population"]
            raw = raw.dropna(subset=["LSOA21CD", "population"])
            # Remove comma formatting e.g. "1,898" → 1898
            raw["population"] = (
                raw["population"]
                .astype(str)
                .str.replace(",", "", regex=False)
                .pipe(pd.to_numeric, errors="coerce")
            )
            raw = raw.dropna(subset=["population"])
            lsoa_pop = raw
            pop_loaded = True
            logger.info(f"  Loaded {len(lsoa_pop):,} LSOA population records")
        except Exception as e:
            logger.warning(f"  Failed to read Excel: {e}")

    # CSV fallback
    if not pop_loaded and lsoa_pop_path.with_suffix(".csv").exists():
        csv_path = lsoa_pop_path.with_suffix(".csv")
        logger.info(f"  Reading population from CSV: {csv_path.name}")
        raw = pd.read_csv(csv_path, encoding="utf-8-sig")
        raw.columns = raw.columns.str.strip()
        # Find LSOA code and total columns
        code_col = next(
            (c for c in raw.columns if "lsoa" in c.lower() and "code" in c.lower()),
            None
        )
        tot_col = next(
            (c for c in raw.columns if c.lower() in ("total", "population", "all ages")),
            None
        )
        if code_col and tot_col:
            raw = raw.rename(columns={code_col: "LSOA21CD", tot_col: "population"})
            raw["population"] = (
                raw["population"]
                .astype(str)
                .str.replace(",", "", regex=False)
                .pipe(pd.to_numeric, errors="coerce")
            )
            lsoa_pop = raw[["LSOA21CD", "population"]].dropna()
            pop_loaded = True
            logger.info(f"  Loaded {len(lsoa_pop):,} LSOA population records from CSV")

    # --- Merge population onto centroids ------------------------------------
    if pop_loaded and lsoa_pop is not None:
        lsoa_cent = lsoa_cent.merge(lsoa_pop, on="LSOA21CD", how="left")
        n_matched = lsoa_cent["population"].notna().sum()
        logger.info(
            f"  Population matched for {n_matched:,} / {len(lsoa_cent):,} LSOAs"
        )

        # Load actual LSOA area from ONS Standard Area Measurements file
        area_path = _ROOT / "data/raw/stats19/lsoa_area.csv"
        if area_path.exists():
            lsoa_area = pd.read_csv(
                area_path,
                usecols=["LSOA21CD", "Clipped to the Coastline (Area in KM2)"],
                encoding="utf-8-sig",
            ).rename(columns={"Clipped to the Coastline (Area in KM2)": "area_km2"})
            lsoa_cent = lsoa_cent.merge(lsoa_area, on="LSOA21CD", how="left")
            n_area = lsoa_cent["area_km2"].notna().sum()
            logger.info(
                f"  LSOA area joined from SAM file: {n_area:,} / "
                f"{len(lsoa_cent):,} LSOAs | "
                f"median area={lsoa_cent['area_km2'].median():.3f} km²"
            )
        else:
            logger.warning(
                f"  LSOA area file not found at {area_path} — "
                f"using fixed 2.9 km² (underestimates urban density)\n"
                f"  Save SAM_LSOA_DEC_2021_EW_in_KM.csv as data/raw/stats19/lsoa_area.csv"
            )
            lsoa_cent["area_km2"] = 2.9

        lsoa_cent["pop_density"] = (
            lsoa_cent["population"] /
            lsoa_cent["area_km2"].replace(0, np.nan)
        )
        use_density = True
    else:
        logger.warning(
            f"Population file not found. Looked for:\n"
            f"  {xl_path}\n"
            f"  {lsoa_pop_path.with_suffix('.csv')}\n"
            f"Falling back to LSOA count proxy.\n"
            f"Download ONS LSOA mid-year estimates Excel and save as:\n"
            f"  {xl_path}"
        )
        use_density = False

    # --- Spatial join -------------------------------------------------------
    lsoa_xy  = lsoa_cent[["x", "y"]].values
    or_bng   = openroads.to_crs("EPSG:27700").copy()
    road_xy  = np.column_stack([
        or_bng.geometry.centroid.x,
        or_bng.geometry.centroid.y,
    ])

    tree = cKDTree(lsoa_xy)
    dists, indices = tree.query(road_xy, k=1, distance_upper_bound=cap_m)
    valid = dists < cap_m
    assigned_codes = np.full(len(road_xy), pd.NA, dtype=object)
    assigned_codes[valid] = lsoa_cent["LSOA21CD"].values[indices[valid]]

    if use_density:
        pop_values = lsoa_cent["pop_density"].values
        result = np.full(len(road_xy), np.nan)
        result[valid] = pop_values[indices[valid]]
        s = pd.Series(result, index=openroads["link_id"], name="pop_density_per_km2")
    else:
        # Fallback: count LSOAs within 1km as urbanisation proxy
        dists_5, _ = tree.query(road_xy, k=5, distance_upper_bound=1000)
        lsoa_count = (dists_5 < 1000).sum(axis=1).astype(float)
        lsoa_count[~valid] = np.nan
        s = pd.Series(
            lsoa_count, index=openroads["link_id"],
            name="pop_density_per_km2"
        )

    n_valid = s.notna().sum()
    logger.info(
        f"  pop_density_per_km2: {n_valid:,} / {len(openroads):,} links matched "
        f"(median={s.median():.0f})"
    )
    if return_lsoa_assignment:
        assignment = pd.Series(
            assigned_codes,
            index=openroads["link_id"],
            name="lsoa21cd_assigned",
            dtype="string",
        )
        return s, assignment
    return s


# ---------------------------------------------------------------------------
# Feature 5: Betweenness relative to road class
# ---------------------------------------------------------------------------

def compute_betweenness_relative(
    features: pd.DataFrame,
    openroads: gpd.GeoDataFrame,
) -> pd.Series:
    """
    Compute betweenness centrality normalised within road classification.

    Raw betweenness is highly correlated with road_class_ord (major roads
    have high betweenness by definition). This removes that confound, leaving
    only "is this road more central than other roads of the same type?"

    betweenness_relative = betweenness / mean(betweenness for road class)

    A value of 2.0 = twice as central as average road of same type.
    A value of 0.5 = half as central as peers.
    Log-transformed to handle right skew.

    Returns
    -------
    Series indexed by link_id.
    """
    logger.info("Computing betweenness_relative (within road class) ...")

    df = features[["link_id", "betweenness"]].merge(
        openroads[["link_id", "road_classification"]], on="link_id", how="left"
    )

    # Mean betweenness per road class
    class_mean = df.groupby("road_classification")["betweenness"].transform("mean")
    df["betweenness_relative"] = df["betweenness"] / (class_mean + 1e-9)

    # Log transform — heavily right-skewed
    s = np.log1p(df["betweenness_relative"])
    s.index = df["link_id"]
    s.name = "betweenness_relative"

    logger.info(
        f"  betweenness_relative: median={s.median():.3f}, "
        f"p75={s.quantile(0.75):.3f}, "
        f"p99={s.quantile(0.99):.3f}"
    )
    return s


# ---------------------------------------------------------------------------
# Feature 6: OSM attributes (speed limit, lanes, lighting, surface)
# ---------------------------------------------------------------------------

def _rss_mb() -> float:
    """Return current process RSS in MB (Linux /proc/self/status)."""
    try:
        for line in Path("/proc/self/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) / 1024
    except Exception:
        pass
    return float("nan")


def fetch_osm_features(
    openroads: gpd.GeoDataFrame,
    osm_dir: Path | None = None,
    force_recompute: bool = False,
) -> pd.DataFrame:
    """
    Fetch road attributes from OpenStreetMap pbf files and join to OS Open
    Roads links.

    Reads multiple county-level pbf files from data/raw/osm/ and merges them.
    Uses osmnx.graph_from_xml() which reads pbf directly.

    Attributes fetched:
        speed_limit_mph  : posted speed limit (integer mph)
        lanes            : number of lanes
        lit              : street lighting present (bool)
        is_unpaved       : non-tarmac surface (bool)

    Per-county results are written to data/features/_osm_partial/{county}.parquet
    immediately after extraction so progress survives OOM. Existing partials are
    reused unless force_recompute=True, which wipes the partial directory first.

    Download county pbf files from Geofabrik:
        https://download.geofabrik.de/europe/great-britain/england/
    Save to data/raw/osm/ and convert with osmium before running.

    Requires: pip install osmnx

    Returns
    -------
    DataFrame with link_id and OSM feature columns.
    """
    try:
        import osmnx as ox
    except ImportError:
        logger.warning("osmnx not installed — skipping OSM features. pip install osmnx")
        return pd.DataFrame({"link_id": openroads["link_id"]})

    if osm_dir is None:
        osm_dir = _ROOT / "data/raw/osm"

    partial_dir = _ROOT / "data/features/_osm_partial"

    if force_recompute and partial_dir.exists():
        logger.info(f"--force: removing stale OSM partials from {partial_dir}")
        shutil.rmtree(partial_dir)
    partial_dir.mkdir(parents=True, exist_ok=True)

    pbf_files = sorted(osm_dir.glob("*.osm.pbf"))
    osm_files = sorted(osm_dir.glob("*.osm"))
    if osm_files:
        read_files = osm_files
        logger.info(f"Found {len(read_files)} converted .osm files — using these")
    elif pbf_files:
        logger.warning(
            f"Found {len(pbf_files)} .osm.pbf files but osmnx cannot read pbf directly.\n"
            f"Convert first with osmium:\n"
            "  for f in data/raw/osm/*.osm.pbf; do\n"
            "      osmium cat \"$f\" -o \"${f%.osm.pbf}.osm\"\n"
            "  done"
        )
        return pd.DataFrame({"link_id": openroads["link_id"]})
    else:
        logger.warning(
            f"No .osm or .osm.pbf files found in {osm_dir}\n"
            f"Download from: https://download.geofabrik.de/europe/great-britain/england/\n"
            "Then convert .osm.pbf files with osmium before rerunning."
        )
        return pd.DataFrame({"link_id": openroads["link_id"]})

    logger.info(f"Reading {len(read_files)} OSM files from {osm_dir} ...")

    ox.settings.useful_tags_way = list(set(
        ox.settings.useful_tags_way + ["lit", "surface", "lanes", "maxspeed"]
    ))

    # --- Attribute parsers --------------------------------------------------

    def parse_speed(val):
        if isinstance(val, list):
            val = val[0]
        if pd.isna(val):
            return np.nan
        s = str(val).split(";")[0].replace("mph", "").replace("km/h", "").strip()
        try:
            v = float(s)
            return round(v) if v <= 130 else round(v * 0.621371)
        except ValueError:
            return np.nan

    def parse_lanes(val):
        if isinstance(val, list):
            val = val[0]
        if pd.isna(val):
            return np.nan
        try:
            return int(str(val).split(";")[0].strip())
        except (ValueError, AttributeError):
            return np.nan

    def parse_lit(val):
        if isinstance(val, list):
            val = val[0]
        if pd.isna(val):
            return np.nan
        s = str(val).lower()
        if s in ("yes", "1", "true"):
            return True
        if s in ("no", "0", "false"):
            return False
        return np.nan

    def parse_surface(val):
        if isinstance(val, list):
            val = val[0]
        if pd.isna(val):
            return np.nan
        v = str(val).lower().split(";")[0].strip()
        return float(
            v in ("unpaved", "gravel", "dirt", "grass", "ground", "sand", "compacted")
        )

    # --- Per-county loop ----------------------------------------------------

    partial_paths = []
    for osm_file in read_files:
        partial_path = partial_dir / f"{osm_file.stem}.parquet"
        if partial_path.exists():
            logger.info(f"  [{osm_file.name}] partial exists — skipping (RSS {_rss_mb():.0f} MB)")
            partial_paths.append(partial_path)
            continue

        logger.info(f"  [{osm_file.name}] starting load — RSS {_rss_mb():.0f} MB")
        try:
            with _Heartbeat(f"osmnx {osm_file.stem}", interval_s=20):
                G = ox.graph_from_xml(str(osm_file), retain_all=False)
                G = ox.add_edge_speeds(G)
                _, edges = ox.graph_to_gdfs(G)
                edges = edges.reset_index()

            logger.info(
                f"  [{osm_file.name}] graph loaded — {len(edges):,} edges, "
                f"RSS {_rss_mb():.0f} MB"
            )

            # Parse attributes into slim columns while edges is still available
            if "speed_kph" in edges.columns:
                speed = (
                    pd.to_numeric(edges["speed_kph"], errors="coerce") * 0.621371
                ).round().astype("Int64")
            else:
                speed = edges.get(
                    "maxspeed", pd.Series(dtype=object, index=edges.index)
                ).apply(parse_speed)

            slim = gpd.GeoDataFrame(
                {
                    "speed_limit_mph": speed,
                    "lanes_parsed": edges.get(
                        "lanes",
                        pd.Series(dtype=object, index=edges.index),
                    ).apply(parse_lanes),
                    "lit": edges.get(
                        "lit",
                        pd.Series(dtype=object, index=edges.index),
                    ).apply(parse_lit),
                    "is_unpaved": edges.get(
                        "surface",
                        pd.Series(dtype=object, index=edges.index),
                    ).apply(parse_surface),
                    "geometry": edges["geometry"].values,
                },
                geometry="geometry",
                crs="EPSG:4326",
            )

            # Free the full graph and raw edge table before writing
            del G, edges
            gc.collect()
            logger.info(
                f"  [{osm_file.name}] graph freed — RSS {_rss_mb():.0f} MB — "
                f"writing partial ({len(slim):,} rows)"
            )

            slim.to_parquet(partial_path)
            partial_paths.append(partial_path)
            del slim
            gc.collect()

        except Exception as e:
            logger.warning(f"  [{osm_file.name}] FAILED: {e} — skipping county")
            try:
                del G
            except NameError:
                pass
            gc.collect()

    if not partial_paths:
        logger.warning("No OSM partials produced — returning empty OSM features")
        return pd.DataFrame({"link_id": openroads["link_id"]})

    # --- Concatenate slim partials and spatial join -------------------------

    logger.info(
        f"Concatenating {len(partial_paths)} county partials — RSS {_rss_mb():.0f} MB"
    )
    all_slim = pd.concat(
        [gpd.read_parquet(p) for p in partial_paths], ignore_index=True
    )
    logger.info(
        f"  Combined: {len(all_slim):,} OSM edges — RSS {_rss_mb():.0f} MB"
    )

    osm_gdf = gpd.GeoDataFrame(all_slim, geometry="geometry", crs="EPSG:4326").to_crs("EPSG:27700")
    del all_slim
    gc.collect()

    or_centroids = gpd.GeoDataFrame(
        openroads[["link_id"]],
        geometry=openroads.to_crs("EPSG:27700").geometry.centroid,
        crs="EPSG:27700",
    )

    logger.info(f"  Spatial joining OSM → OS Open Roads — RSS {_rss_mb():.0f} MB")
    with _Heartbeat("spatial join OSM→OpenRoads", interval_s=15):
        joined = gpd.sjoin_nearest(
            or_centroids, osm_gdf,
            how="left",
            max_distance=50,
            distance_col="osm_dist",
        )

    joined = joined.sort_values("osm_dist").drop_duplicates(subset="link_id")

    result = joined[["link_id", "speed_limit_mph", "lanes_parsed",
                      "lit", "is_unpaved"]].rename(
        columns={"lanes_parsed": "lanes"}
    )

    n_speed = result["speed_limit_mph"].notna().sum()
    n_lanes = result["lanes"].notna().sum()
    n_lit = result["lit"].fillna(False).sum()
    logger.info(
        f"  OSM features matched: "
        f"speed={n_speed:,} ({n_speed/len(result):.1%}), "
        f"lanes={n_lanes:,} ({n_lanes/len(result):.1%}), "
        f"lit={n_lit:,} ({n_lit/len(result):.1%})"
    )
    return result


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def build_network_features(
    openroads: gpd.GeoDataFrame = None,
    openroads_path: Path = OPENROADS_PATH,
    output_path: Path = OUTPUT_PATH,
    betweenness_k: int = BETWEENNESS_K,
    force_recompute: bool = False,
    include_osm: bool = False,
) -> pd.DataFrame:
    """
    Compute all network and population features for OS Open Roads links.

    Caches result to data/features/network_features.parquet so subsequent
    runs are instant. Use force_recompute=True to regenerate.

    Parameters
    ----------
    openroads       : pre-loaded GeoDataFrame (optional)
    openroads_path  : path to openroads_yorkshire.parquet
    output_path     : where to cache the feature table
    betweenness_k   : sample size for betweenness
    force_recompute : if True, ignores cache
    include_osm     : if True, fetches OSM attributes (requires osmnx,
                      adds ~10 mins). Default False — run separately with
                      --osm flag once satisfied with other features.

    Returns
    -------
    DataFrame with columns:
        degree_mean, betweenness, betweenness_relative,
        dist_to_major_km, pop_density_per_km2,
        ruc_class, ruc_urban_rural,
        [speed_limit_mph, lanes, lit, is_unpaved]  ← if include_osm=True
    """
    required_cols = {"ruc_class", "ruc_urban_rural"}
    if output_path.exists() and not force_recompute:
        cached = pd.read_parquet(output_path)
        osm_cols = {"speed_limit_mph", "lanes", "lit", "is_unpaved"}
        missing_required = required_cols.difference(cached.columns)
        if missing_required:
            logger.info(
                "Cache exists but is missing required RUC columns %s — recomputing.",
                sorted(missing_required),
            )
        elif include_osm and not osm_cols.intersection(cached.columns):
            logger.info(
                "Cache exists but has no OSM columns — recomputing with OSM features."
            )
        else:
            logger.info(f"Loading cached network features from {output_path}")
            return cached

    if openroads is None:
        logger.info(f"Loading OS Open Roads from {openroads_path}")
        openroads = gpd.read_parquet(openroads_path)
        logger.info(f"  {len(openroads):,} links loaded")

    logger.info(f"Loading RUC lookup from {RUC_PATH}")
    ruc_lookup = load_ruc_lookup()
    ruc_by_lsoa = ruc_lookup.set_index("LSOA21CD")["RUC21CD"]

    # Build graph
    G = build_graph(openroads)

    # Compute features
    degree      = compute_node_degree(G, openroads)
    betweenness = compute_betweenness(G, openroads, k=betweenness_k)
    dist_major  = compute_dist_to_major(G, openroads)
    pop_density, lsoa_assignment = compute_population_density(
        openroads,
        return_lsoa_assignment=True,
    )
    ruc_class = lsoa_assignment.map(ruc_by_lsoa).astype("string")
    ruc_urban_rural = derive_ruc_urban_rural(ruc_class)

    # Combine base features
    features = pd.DataFrame({
        "link_id":             openroads["link_id"].values,
        "degree_mean":         degree.values,
        "betweenness":         betweenness.values,
        "dist_to_major_km":    dist_major.values,
        "pop_density_per_km2": pop_density.values,
        "ruc_class":           ruc_class.values,
        "ruc_urban_rural":     ruc_urban_rural.values,
    })

    # Betweenness relative to road class
    bc_rel = compute_betweenness_relative(features, openroads)
    features["betweenness_relative"] = bc_rel.values

    # OSM features (optional — slow)
    if include_osm:
        osm = fetch_osm_features(openroads, force_recompute=force_recompute)
        features = features.merge(osm, on="link_id", how="left")
    else:
        logger.info(
            "  OSM features skipped (use --osm flag to include). "
            "Adds speed_limit_mph, lanes, lit, is_unpaved."
        )

    # Log feature summaries
    logger.info("\n=== Network feature summary ===")
    summary_cols = [c for c in features.columns if c != "link_id"]
    for col in summary_cols:
        vals = features[col].dropna()
        if len(vals) == 0:
            continue
        if vals.dtype == bool or set(vals.unique()).issubset({0, 1, True, False}):
            logger.info(
                f"  {col:28s}: "
                f"True={vals.sum():.0f} ({vals.mean():.1%}), "
                f"nulls={features[col].isna().sum():,}"
            )
        elif pd.api.types.is_numeric_dtype(vals):
            logger.info(
                f"  {col:28s}: median={vals.median():.4f}, "
                f"p25={vals.quantile(0.25):.4f}, "
                f"p75={vals.quantile(0.75):.4f}, "
                f"nulls={features[col].isna().sum():,}"
            )
        else:
            top_counts = vals.astype(str).value_counts().head(3)
            top_text = ", ".join(
                f"{label}={count:,}" for label, count in top_counts.items()
            )
            logger.info(
                f"  {col:28s}: top={top_text}, "
                f"nulls={features[col].isna().sum():,}"
            )

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_parquet(output_path, index=False)
    logger.info(f"Saved network features to {output_path} ({len(features):,} rows)")
    write_ruc_provenance(features)

    return features



def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force", action="store_true",
        help="Recompute even if cache exists"
    )
    parser.add_argument(
        "--k", type=int, default=BETWEENNESS_K,
        help=f"Betweenness sample size (default: {BETWEENNESS_K})"
    )
    parser.add_argument(
        "--osm", action="store_true",
        help=(
            "Include OSM features (speed limit, lanes, lit, surface). "
            "Requires osmnx. Adds ~10 mins."
        )
    )
    args = parser.parse_args()

    try:
        features = build_network_features(
            betweenness_k=args.k,
            force_recompute=args.force,
            include_osm=args.osm,
        )
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc

    print("\n=== Network features ===")
    print(features.describe().round(4).to_string())
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
