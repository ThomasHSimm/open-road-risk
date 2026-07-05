"""Build static worked examples of STATS19 collision snapping.

This consumes existing processed parquet outputs only. It does not rerun
ingest, snapping, joining, traffic estimation, or modelling.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import sys
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "open-road-risk-mpl"))

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import pyarrow.parquet as pq
import shapely
from matplotlib.lines import Line2D
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points

try:
    from road_risk.config import _ROOT
except ModuleNotFoundError:  # Allows direct execution as python src/.../script.py
    _ROOT = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(_ROOT / "src"))

from road_risk.clean_join.snap import (
    HALF_LIFE_M,
    K_CANDIDATES,
    SEARCH_RADIUS,
    W_CLASS,
    W_JUNCTION,
    W_NUMBER,
    W_SPATIAL,
    _junction_score,
    _road_class_score,
    _road_number_score,
    _spatial_score,
)

logger = logging.getLogger(__name__)

SNAPPED_PATH = _ROOT / "data/processed/stats19/snapped_weighted.parquet"
COLLISION_PATH = _ROOT / "data/processed/stats19/collision_clean.parquet"
OPENROADS_PATH = _ROOT / "data/processed/shapefiles/openroads.parquet"
OUTPUT_DIR = _ROOT / "quarto/outputs/figures"
MANIFEST_PATH = OUTPUT_DIR / "snap-examples-manifest.json"

COLLISION_ID_CANDIDATES = ["collision_index", "accident_index", "collision_ref_no"]
LINK_ID_CANDIDATES = ["link_id", "id", "road_link_id"]
SNAP_METHOD_CANDIDATES = ["snap_method", "method"]
SNAP_SCORE_CANDIDATES = ["snap_score", "score"]
SNAP_DISTANCE_CANDIDATES = ["snap_distance_m", "distance_m"]

COLLISION_COLUMNS = [
    "collision_index",
    "collision_year",
    "collision_ref_no",
    "date",
    "time",
    "longitude",
    "latitude",
    "collision_severity",
    "number_of_vehicles",
    "number_of_casualties",
    "local_authority_highway",
    "first_road_class",
    "first_road_number",
    "road_type",
    "speed_limit",
    "junction_detail",
    "junction_control",
    "second_road_class",
    "second_road_number",
    "weather_conditions",
    "road_surface_conditions",
    "urban_or_rural_area",
    "road_name_clean",
    "coords_valid",
]

SNAPPED_COLUMNS = [
    "collision_index",
    "link_id",
    "snap_distance_m",
    "snap_score",
    "score_spatial",
    "score_class",
    "score_junction",
    "score_number",
    "snap_method",
]

OPENROADS_ATTR_COLUMNS = [
    "link_id",
    "road_classification",
    "form_of_way",
    "road_number",
    "road_name_clean",
    "link_length_m",
]

OPENROADS_FIGURE_COLUMNS = OPENROADS_ATTR_COLUMNS + ["geometry"]

STATS19_LABELS = {
    "collision_severity": {
        1: "Fatal",
        2: "Serious",
        3: "Slight",
    },
    "first_road_class": {
        1: "Motorway",
        2: "A(M)",
        3: "A",
        4: "B",
        5: "C",
        6: "Unclassified",
    },
    "second_road_class": {
        0: "Not at junction or within 20 metres",
        1: "Motorway",
        2: "A(M)",
        3: "A",
        4: "B",
        5: "C",
        6: "Unclassified",
        -1: "Data missing or out of range",
    },
    "road_type": {
        1: "Roundabout",
        2: "One way street",
        3: "Dual carriageway",
        6: "Single carriageway",
        7: "Slip road",
        9: "Unknown",
        12: "One way street / slip road",
        -1: "Data missing or out of range",
    },
    "junction_detail": {
        0: "Not at junction or within 20 metres",
        1: "Roundabout",
        2: "Mini-roundabout",
        3: "T or staggered junction",
        5: "Slip road",
        6: "Crossroads",
        7: "More than four arms",
        8: "Private drive or entrance",
        9: "Other junction",
        99: "Unknown",
        -1: "Data missing or out of range",
    },
    "junction_control": {
        0: "Not at junction or within 20 metres",
        1: "Authorised person",
        2: "Auto traffic signal",
        3: "Stop sign",
        4: "Give way or uncontrolled",
        -1: "Data missing or out of range",
    },
    "weather_conditions": {
        1: "Fine no high winds",
        2: "Raining no high winds",
        3: "Snowing no high winds",
        4: "Fine + high winds",
        5: "Raining + high winds",
        6: "Snowing + high winds",
        7: "Fog or mist",
        8: "Other",
        9: "Unknown",
        -1: "Data missing or out of range",
    },
    "road_surface_conditions": {
        1: "Dry",
        2: "Wet or damp",
        3: "Snow",
        4: "Frost or ice",
        5: "Flood over 3cm deep",
        6: "Oil or diesel",
        7: "Mud",
        -1: "Data missing or out of range",
    },
    "urban_or_rural_area": {
        1: "Urban",
        2: "Rural",
        3: "Unallocated",
    },
}

EXAMPLES = [
    {
        "key": "simple",
        "title": "Simple road segment",
        "file": "snap-example-simple.png",
        "buffer_m": 170.0,
        "reason": "High-score snap to a single-carriageway A/B road away from a recorded junction.",
        "summary": "One nearby link clearly fits the point and road attributes.",
        "ambiguity": "Limited ambiguity; alternatives are farther away or weaker matches.",
    },
    {
        "key": "junction",
        "title": "Junction or roundabout",
        "file": "snap-example-junction.png",
        "buffer_m": 210.0,
        "reason": "High-score snap where junction form-of-way is part of the decision.",
        "summary": "Near a junction, several short links can be plausible.",
        "ambiguity": "The nearest road is not always the most plausible junction link.",
    },
    {
        "key": "parallel-links",
        "title": "Dual carriageway / parallel links",
        "file": "snap-example-parallel-links.png",
        "buffer_m": 260.0,
        "reason": "High-score snap on a dual-carriageway or motorway-style local network.",
        "summary": "Parallel carriageways make distance-only snapping ambiguous.",
        "ambiguity": "Nearby parallel and junction links have very similar geometry.",
    },
    {
        "key": "dense-urban",
        "title": "Dense urban network",
        "file": "snap-example-dense-urban.png",
        "buffer_m": 230.0,
        "reason": "Urban junction case with many nearby links in a compact search window.",
        "summary": "Dense urban networks create many nearby candidates.",
        "ambiguity": "Multiple short links sit inside the same compact search window.",
    },
    {
        "key": "low-confidence",
        "title": "Lower-confidence retained snap",
        "file": "snap-example-low-confidence.png",
        "buffer_m": 360.0,
        "reason": "Retained weighted snap close to the 0.6 score threshold.",
        "summary": "Retained because it passes the threshold; uncertainty is higher.",
        "ambiguity": "The selected score is close to the retained/filtered boundary.",
    },
    {
        "key": "filtered-low-score",
        "title": "Filtered low-score snap",
        "file": "snap-example-filtered-low-score.png",
        "buffer_m": 420.0,
        "reason": "Weighted snap below the 0.6 score threshold, excluded before link-year aggregation.",
        "summary": "Filtered example: below the retained score threshold.",
        "ambiguity": "Distance and attribute evidence are not strong enough to retain.",
    },
]

WORKED_SCORING_EXAMPLE_KEYS = {"simple", "dense-urban"}


@dataclass(frozen=True)
class Example:
    key: str
    title: str
    filename: str
    buffer_m: float
    reason: str
    summary: str
    ambiguity: str
    row: pd.Series


def _schema_columns(path: Path) -> list[str]:
    return pq.ParquetFile(path).schema_arrow.names


def _first_existing(path: Path, candidates: list[str]) -> str | None:
    available = set(_schema_columns(path))
    for candidate in candidates:
        if candidate in available:
            return candidate
    return None


def _read_existing_columns(path: Path, wanted: list[str]) -> pd.DataFrame:
    available = set(_schema_columns(path))
    columns = [col for col in wanted if col in available]
    missing = sorted(set(wanted) - available)
    if missing:
        logger.warning("Skipping missing columns from %s: %s", path.relative_to(_ROOT), missing)
    return pd.read_parquet(path, columns=columns)


def _read_openroads_attrs(link_ids: set[str]) -> pd.DataFrame:
    """Read Open Roads attributes for matched links without loading geometry."""
    frames: list[pd.DataFrame] = []
    parquet_file = pq.ParquetFile(OPENROADS_PATH)
    for batch in parquet_file.iter_batches(columns=OPENROADS_ATTR_COLUMNS, batch_size=500_000):
        df = batch.to_pandas()
        df = df[df["link_id"].isin(link_ids)]
        if not df.empty:
            frames.append(df)
    if not frames:
        return pd.DataFrame(columns=OPENROADS_ATTR_COLUMNS)
    return pd.concat(frames, ignore_index=True)


def _normalise_snap_rows() -> tuple[pd.DataFrame, dict[str, str | None]]:
    snap_schema = set(_schema_columns(SNAPPED_PATH))
    collision_id_col = _first_existing(SNAPPED_PATH, COLLISION_ID_CANDIDATES)
    link_id_col = _first_existing(SNAPPED_PATH, LINK_ID_CANDIDATES)
    method_col = _first_existing(SNAPPED_PATH, SNAP_METHOD_CANDIDATES)
    score_col = _first_existing(SNAPPED_PATH, SNAP_SCORE_CANDIDATES)
    distance_col = _first_existing(SNAPPED_PATH, SNAP_DISTANCE_CANDIDATES)

    if collision_id_col is None or link_id_col is None:
        raise KeyError("Could not identify collision identifier and matched link columns.")

    snapped_cols = [col for col in SNAPPED_COLUMNS if col in snap_schema]
    snapped = pd.read_parquet(SNAPPED_PATH, columns=snapped_cols)

    collision_schema = set(_schema_columns(COLLISION_PATH))
    collision_cols = [col for col in COLLISION_COLUMNS if col in collision_schema]
    collisions = pd.read_parquet(COLLISION_PATH, columns=collision_cols)

    rows = collisions.merge(snapped, on=collision_id_col, how="inner", validate="one_to_one")
    rows = rows.rename(
        columns={
            collision_id_col: "collision_id",
            link_id_col: "matched_link_id",
            method_col or "snap_method": "snap_method",
            score_col or "snap_score": "snap_score",
            distance_col or "snap_distance_m": "snap_distance_m",
        }
    )

    link_ids = set(rows["matched_link_id"].dropna().astype(str))
    attrs = _read_openroads_attrs(link_ids).rename(
        columns={
            "link_id": "matched_link_id",
            "road_name_clean": "matched_road_name_clean",
        }
    )
    rows["matched_link_id"] = rows["matched_link_id"].astype("string")
    attrs["matched_link_id"] = attrs["matched_link_id"].astype("string")
    rows = rows.merge(attrs, on="matched_link_id", how="left", validate="many_to_one")

    for col in ["snap_score", "snap_distance_m", "longitude", "latitude", "link_length_m"]:
        if col in rows.columns:
            rows[col] = pd.to_numeric(rows[col], errors="coerce")

    columns_used = {
        "collision_id": collision_id_col,
        "link_id": link_id_col,
        "snap_method": method_col,
        "snap_score": score_col,
        "snap_distance_m": distance_col,
    }
    return rows, columns_used


def _matched_base(rows: pd.DataFrame) -> pd.DataFrame:
    base = rows[
        rows["matched_link_id"].notna()
        & rows["longitude"].notna()
        & rows["latitude"].notna()
        & rows["snap_method"].isin(["weighted", "attribute", "spatial"])
    ].copy()
    if "coords_valid" in base.columns:
        base = base[base["coords_valid"].fillna(False)]
    if "snap_score" in base.columns:
        base = base[base["snap_score"].notna()]
    return base


def _pick_first(candidates: pd.DataFrame, used: set[Any], sort_by: list[str]) -> pd.Series | None:
    candidates = candidates[~candidates["collision_id"].isin(used)].copy()
    if candidates.empty:
        return None
    ascending = [col not in {"snap_score", "score_spatial"} for col in sort_by]
    candidates = candidates.sort_values(sort_by, ascending=ascending)
    row = candidates.iloc[0]
    used.add(row["collision_id"])
    return row


def _select_examples(rows: pd.DataFrame) -> tuple[list[Example], list[str]]:
    base = _matched_base(rows)
    used: set[Any] = set()
    missing: list[str] = []
    selected: list[Example] = []

    simple = base[
        (base["snap_score"] >= 0.82)
        & (base["snap_distance_m"].between(5, 25))
        & (base["junction_detail"].fillna(0).astype("Int64") == 0)
        & (base["urban_or_rural_area"].fillna(0).astype("Int64") == 2)
        & (base["form_of_way"].fillna("").str.contains("Single", case=False))
        & (base["road_classification"].fillna("").isin(["A Road", "B Road"]))
        & (base["link_length_m"].fillna(0) >= 300)
    ]
    junction_roundabout = base[
        (base["snap_score"] >= 0.8)
        & base["form_of_way"].fillna("").str.contains("Roundabout", case=False)
    ]
    junction = junction_roundabout
    if junction.empty:
        junction = base[
            (base["snap_score"] >= 0.8) & (base["junction_detail"].fillna(0).astype("Int64") > 0)
        ]
    parallel = base[
        (base["snap_score"] >= 0.8)
        & (
            base["form_of_way"].fillna("").str.contains("Dual", case=False)
            | base["road_classification"].fillna("").isin(["Motorway"])
        )
    ]
    dense = base[
        (base["snap_score"] >= 0.75)
        & (base["urban_or_rural_area"].fillna(0).astype("Int64") == 1)
        & (base["junction_detail"].fillna(0).astype("Int64") > 0)
        & (base["road_classification"].fillna("").isin(["A Road", "B Road", "Unclassified"]))
    ]
    low_confidence = base[
        (base["snap_score"] >= 0.6) & (base["snap_score"] <= 0.68) & base["snap_distance_m"].notna()
    ]
    filtered_low_score = base[
        (base["snap_score"] >= 0.55)
        & (base["snap_score"] < 0.6)
        & (base["snap_distance_m"].between(25, 150))
    ]

    pools = {
        "simple": (simple, ["snap_distance_m", "snap_score"]),
        "junction": (junction, ["snap_distance_m", "snap_score"]),
        "parallel-links": (parallel, ["snap_distance_m", "snap_score"]),
        "dense-urban": (dense, ["snap_distance_m", "snap_score"]),
        "low-confidence": (low_confidence, ["snap_score", "snap_distance_m"]),
        "filtered-low-score": (filtered_low_score, ["snap_distance_m", "snap_score"]),
    }

    fallback = base[base["snap_score"] >= 0.6]
    for spec in EXAMPLES:
        pool, sort_by = pools[spec["key"]]
        row = _pick_first(pool, used, sort_by)
        if row is None:
            missing.append(spec["key"])
            row = _pick_first(fallback, used, ["snap_distance_m", "snap_score"])
        if row is None:
            continue
        selected.append(
            Example(
                key=spec["key"],
                title=spec["title"],
                filename=spec["file"],
                buffer_m=spec["buffer_m"],
                reason=spec["reason"],
                summary=spec["summary"],
                ambiguity=spec["ambiguity"],
                row=row,
            )
        )
    return selected, missing


def _wgs84_bbox(lon: float, lat: float, buffer_m: float) -> tuple[float, float, float, float]:
    lat_delta = buffer_m / 111_320
    lon_delta = buffer_m / (111_320 * max(math.cos(math.radians(lat)), 0.2))
    return lon - lon_delta, lat - lat_delta, lon + lon_delta, lat + lat_delta


def _bbox_mask(bounds: Any, bbox: tuple[float, float, float, float]) -> Any:
    minx, miny, maxx, maxy = bounds[:, 0], bounds[:, 1], bounds[:, 2], bounds[:, 3]
    xmin, ymin, xmax, ymax = bbox
    return (maxx >= xmin) & (minx <= xmax) & (maxy >= ymin) & (miny <= ymax)


def _read_nearby_openroads(examples: list[Example]) -> dict[str, gpd.GeoDataFrame]:
    boxes = {
        example.key: _wgs84_bbox(
            float(example.row["longitude"]),
            float(example.row["latitude"]),
            _display_buffer_m(example),
        )
        for example in examples
    }
    frames: dict[str, list[gpd.GeoDataFrame]] = {example.key: [] for example in examples}

    parquet_file = pq.ParquetFile(OPENROADS_PATH)
    for batch in parquet_file.iter_batches(columns=OPENROADS_FIGURE_COLUMNS, batch_size=300_000):
        df = batch.to_pandas()
        geoms = shapely.from_wkb(df["geometry"].to_numpy())
        bounds = shapely.bounds(geoms)
        for key, bbox in boxes.items():
            mask = _bbox_mask(bounds, bbox)
            if mask.any():
                local = df.loc[mask].drop(columns=["geometry"]).copy()
                frames[key].append(gpd.GeoDataFrame(local, geometry=geoms[mask], crs="EPSG:4326"))

    nearby: dict[str, gpd.GeoDataFrame] = {}
    for key, parts in frames.items():
        if parts:
            nearby[key] = pd.concat(parts, ignore_index=True)
        else:
            nearby[key] = gpd.GeoDataFrame(columns=OPENROADS_FIGURE_COLUMNS, geometry=[], crs=4326)
    return nearby


def _metric_text(row: pd.Series) -> str:
    bits = [f"method={row['snap_method']}"]
    if pd.notna(row.get("snap_score")):
        bits.append(f"score={row['snap_score']:.3f}")
    if pd.notna(row.get("snap_distance_m")):
        bits.append(f"distance={row['snap_distance_m']:.1f} m")
    return " | ".join(bits)


def _retained_status(row: pd.Series) -> str:
    method = str(row.get("snap_method", ""))
    score = row.get("snap_score")
    if method not in {"weighted", "attribute", "spatial"}:
        return "filtered"
    if pd.isna(score):
        return "retained"
    return "retained" if float(score) >= 0.6 else "filtered"


def _json_value(value: Any, *, decimals: int | None = None) -> Any:
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.date().isoformat()
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float):
        return round(value, decimals) if decimals is not None else value
    return value


def _code_label(column: str, value: Any) -> str | None:
    if pd.isna(value):
        return None
    code = int(value)
    label = STATS19_LABELS.get(column, {}).get(code)
    if label is None:
        return f"code {code}"
    return f"{label} (code {code})"


def _road_number(row: pd.Series, class_col: str, number_col: str) -> str | None:
    road_class = row.get(class_col)
    number = row.get(number_col)
    if pd.isna(road_class) or pd.isna(number):
        return None
    if int(number) <= 0:
        return None
    prefix = {
        1: "M",
        2: "A",
        3: "A",
        4: "B",
        5: "C",
    }.get(int(road_class), "")
    return f"{prefix}{int(number)}" if prefix else str(int(number))


def _string_or_none(value: Any) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def _format_number(value: Any) -> str:
    if value is None or pd.isna(value):
        return "unknown"
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:g}"


def _count_phrase(value: Any, singular: str, plural: str) -> str:
    if value is None or pd.isna(value):
        return f"unknown {plural}"
    count = int(value)
    label = singular if count == 1 else plural
    return f"{count} {label}"


def _stats19_source_record(row: pd.Series) -> dict[str, Any]:
    return {
        "collision_index": str(row.get("collision_index", row.get("collision_id"))),
        "collision_ref_no": _string_or_none(row.get("collision_ref_no")),
        "collision_year": _json_value(row.get("collision_year")),
        "date": _json_value(row.get("date")),
        "time": _string_or_none(row.get("time")),
        "longitude": _json_value(row.get("longitude"), decimals=6),
        "latitude": _json_value(row.get("latitude"), decimals=6),
        "local_authority_highway": _string_or_none(row.get("local_authority_highway")),
        "collision_severity": _code_label("collision_severity", row.get("collision_severity")),
        "number_of_vehicles": _json_value(row.get("number_of_vehicles")),
        "number_of_casualties": _json_value(row.get("number_of_casualties")),
        "first_road_class": _code_label("first_road_class", row.get("first_road_class")),
        "first_road_number": _json_value(row.get("first_road_number")),
        "first_road": _road_number(row, "first_road_class", "first_road_number"),
        "road_type": _code_label("road_type", row.get("road_type")),
        "speed_limit_mph": _json_value(row.get("speed_limit")),
        "junction_detail": _code_label("junction_detail", row.get("junction_detail")),
        "junction_control": _code_label("junction_control", row.get("junction_control")),
        "second_road_class": _code_label("second_road_class", row.get("second_road_class")),
        "second_road_number": _json_value(row.get("second_road_number")),
        "second_road": _road_number(row, "second_road_class", "second_road_number"),
        "weather_conditions": _code_label("weather_conditions", row.get("weather_conditions")),
        "road_surface_conditions": _code_label(
            "road_surface_conditions",
            row.get("road_surface_conditions"),
        ),
        "urban_or_rural_area": _code_label("urban_or_rural_area", row.get("urban_or_rural_area")),
        "road_name_clean": _string_or_none(row.get("road_name_clean")),
        "coords_valid": _json_value(row.get("coords_valid")),
    }


def _stats19_plain_text(row: pd.Series) -> str:
    source = _stats19_source_record(row)
    road = source["first_road"] or source["first_road_class"] or "road not numbered"
    vehicles = _count_phrase(source["number_of_vehicles"], "vehicle", "vehicles")
    casualties = _count_phrase(source["number_of_casualties"], "casualty", "casualties")
    return (
        f"{source['date']} {source['time']}; severity {source['collision_severity']}; "
        f"{vehicles}, {casualties}; "
        f"first road {road}; road type {source['road_type']}; "
        f"speed limit {_format_number(source['speed_limit_mph'])} mph; "
        f"junction {source['junction_detail']}; weather {source['weather_conditions']}; "
        f"surface {source['road_surface_conditions']}; "
        f"point ({source['longitude']}, {source['latitude']})."
    )


def _display_buffer_m(example: Example) -> float:
    snap_distance = float(example.row["snap_distance_m"] or 0)
    return min(SEARCH_RADIUS, max(example.buffer_m, snap_distance * 2.5 + 80))


def _score_local_candidates(
    row: pd.Series,
    roads_27700: gpd.GeoDataFrame,
    point_geom: Point,
) -> gpd.GeoDataFrame:
    """Rank nearby links for explanation; this is not the persisted snap candidate list."""
    candidates = roads_27700.copy()
    if candidates.empty:
        return candidates

    distances = candidates.geometry.distance(point_geom).to_numpy()
    s_spatial = _spatial_score(distances, HALF_LIFE_M)
    s_class = _road_class_score(
        int(row.get("first_road_class", 0) or 0),
        candidates["road_classification"].fillna(""),
    )
    s_junction = _junction_score(
        int(row.get("junction_detail", -1) or -1),
        candidates["form_of_way"].fillna(""),
    )
    s_number = _road_number_score(
        str(row.get("road_name_clean", "") or ""),
        candidates["road_name_clean"].fillna(""),
    )
    candidates["candidate_distance_m"] = distances
    candidates["candidate_score"] = (
        W_SPATIAL * s_spatial + W_CLASS * s_class + W_JUNCTION * s_junction + W_NUMBER * s_number
    )
    candidates["candidate_score_spatial"] = s_spatial
    candidates["candidate_score_class"] = s_class
    candidates["candidate_score_junction"] = s_junction
    candidates["candidate_score_number"] = s_number
    candidates = candidates.sort_values(
        ["candidate_score", "candidate_distance_m"],
        ascending=[False, True],
    ).copy()
    candidates["local_candidate_rank"] = range(1, len(candidates) + 1)
    return candidates


def _candidate_role(display_rank: int, selected: bool) -> str:
    if selected:
        return "Selected link"
    return f"Alternative {display_rank}"


def _candidate_why_it_matters(candidate: pd.Series, selected: bool) -> str:
    if selected:
        return "Saved snap target; compare its component scores with nearby alternatives."

    reasons: list[str] = []
    if float(candidate["candidate_score_spatial"]) >= 0.9:
        reasons.append("very close spatially")
    elif float(candidate["candidate_score_spatial"]) >= 0.6:
        reasons.append("spatially plausible")
    else:
        reasons.append("weaker on distance")

    if float(candidate["candidate_score_class"]) < 1.0:
        reasons.append("road class is less supportive")
    if float(candidate["candidate_score_junction"]) < 1.0:
        reasons.append("junction/form context is weaker")
    if float(candidate["candidate_score_number"]) < 1.0:
        reasons.append("road-number evidence is not exact")

    return "; ".join(reasons) + "."


def _candidate_records(candidates: gpd.GeoDataFrame, selected_link_id: str) -> list[dict[str, Any]]:
    if candidates.empty:
        return []
    selected = candidates[candidates["link_id"].astype(str) == selected_link_id].head(1)
    competitors = candidates[candidates["link_id"].astype(str) != selected_link_id].head(2)
    display = pd.concat([selected, competitors], ignore_index=False)
    records: list[dict[str, Any]] = []
    for display_rank, (_, candidate) in enumerate(display.iterrows(), start=1):
        is_selected = str(candidate["link_id"]) == selected_link_id
        role = _candidate_role(display_rank, is_selected)
        records.append(
            {
                "display_rank": display_rank,
                "candidate_rank": int(candidate["local_candidate_rank"]),
                "local_candidate_rank": int(candidate["local_candidate_rank"]),
                "role": role,
                "link_id": str(candidate["link_id"]),
                "selected": is_selected,
                "distance_m": round(float(candidate["candidate_distance_m"]), 2),
                "candidate_distance_m": round(float(candidate["candidate_distance_m"]), 2),
                "score_spatial": round(float(candidate["candidate_score_spatial"]), 4),
                "score_class": round(float(candidate["candidate_score_class"]), 4),
                "score_junction": round(float(candidate["candidate_score_junction"]), 4),
                "score_number": round(float(candidate["candidate_score_number"]), 4),
                "composite_score": round(float(candidate["candidate_score"]), 4),
                "candidate_score": round(float(candidate["candidate_score"]), 4),
                "road_classification": None
                if pd.isna(candidate.get("road_classification"))
                else str(candidate["road_classification"]),
                "form_of_way": None
                if pd.isna(candidate.get("form_of_way"))
                else str(candidate["form_of_way"]),
                "road_name_clean": _string_or_none(candidate.get("road_name_clean")),
                "why_it_matters": _candidate_why_it_matters(candidate, is_selected),
            }
        )
    return records


def _label_line_near_point(
    ax: Any,
    point_geom: Point,
    line_geom: Any,
    label: str,
    color: str,
    offset_m: tuple[float, float],
) -> None:
    _, line_point = nearest_points(point_geom, line_geom)
    ax.annotate(
        label,
        xy=(line_point.x, line_point.y),
        xytext=offset_m,
        textcoords="offset points",
        ha="center",
        va="center",
        fontsize=7,
        color="white",
        bbox={"boxstyle": "round,pad=0.18", "fc": color, "ec": "white", "lw": 0.6},
        zorder=6,
    )


def _plot_example(example: Example, roads: gpd.GeoDataFrame, output_path: Path) -> dict[str, Any]:
    row = example.row
    lon = float(row["longitude"])
    lat = float(row["latitude"])
    point = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326").to_crs(27700)
    point_geom = point.geometry.iloc[0]
    buffer_m = _display_buffer_m(example)
    point_buffer = point_geom.buffer(buffer_m)

    roads = roads.drop_duplicates("link_id").copy()
    roads_27700 = roads.to_crs(27700)
    if not roads_27700.empty:
        roads_27700 = roads_27700[roads_27700.geometry.intersects(point_buffer)]

    selected_link_id = str(row["matched_link_id"])
    candidates = _score_local_candidates(row, roads_27700, point_geom)
    selected = candidates[candidates["link_id"].astype(str) == selected_link_id]
    competitors = candidates[candidates["link_id"].astype(str) != selected_link_id].head(2)
    competitor_ids = set(competitors["link_id"].astype(str))
    other = candidates[
        (candidates["link_id"].astype(str) != selected_link_id)
        & (~candidates["link_id"].astype(str).isin(competitor_ids))
    ]

    fig, ax = plt.subplots(figsize=(5.8, 4.65), dpi=180)
    if not other.empty:
        other.plot(ax=ax, color="#b8b8b8", linewidth=1.0, alpha=0.75, zorder=1)
    competitor_colours = ["#d89c25", "#6a62b7"]
    for rank, ((_, competitor), colour) in enumerate(
        zip(competitors.iterrows(), competitor_colours, strict=False),
        start=2,
    ):
        gpd.GeoDataFrame([competitor], geometry="geometry", crs=27700).plot(
            ax=ax,
            color=colour,
            linewidth=2.3,
            alpha=0.95,
            zorder=2,
        )
        _label_line_near_point(
            ax,
            point_geom,
            competitor.geometry,
            f"{rank}",
            colour,
            offset_m=(9, 8 if rank == 2 else -10),
        )
    if not selected.empty:
        selected.plot(ax=ax, color="#d64b3c", linewidth=3.2, zorder=3)
        target = selected.geometry.union_all()
        _, snap_point = nearest_points(point_geom, target)
        gpd.GeoSeries([LineString([point_geom, snap_point])], crs=27700).plot(
            ax=ax,
            color="#1f6fb2",
            linewidth=1.6,
            linestyle="--",
            zorder=4,
        )
        _label_line_near_point(
            ax,
            point_geom,
            target,
            "S",
            "#d64b3c",
            offset_m=(-10, -9),
        )

    point.plot(ax=ax, color="#1f6fb2", markersize=68, edgecolor="white", linewidth=1.0, zorder=5)

    minx, miny, maxx, maxy = point_buffer.bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{example.title}\n{_metric_text(row)}", fontsize=10, pad=8)
    fig.text(
        0.5,
        0.025,
        example.summary,
        ha="center",
        va="bottom",
        fontsize=8,
        color="#333333",
    )
    fig.subplots_adjust(bottom=0.12)
    ax.legend(
        handles=[
            Line2D([0], [0], color="#b8b8b8", lw=2, label="Other nearby links"),
            Line2D([0], [0], color="#d64b3c", lw=3, label="Selected snapped link"),
            Line2D([0], [0], color="#d89c25", lw=2.3, label="Candidate 2"),
            Line2D([0], [0], color="#6a62b7", lw=2.3, label="Candidate 3"),
            Line2D(
                [0], [0], marker="o", color="w", markerfacecolor="#1f6fb2", label="STATS19 point"
            ),
            Line2D([0], [0], color="#1f6fb2", lw=1.5, linestyle="--", label="Snap offset"),
        ],
        loc="lower left",
        fontsize=7,
        frameon=True,
        framealpha=0.92,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    candidate_records = _candidate_records(candidates, selected_link_id)
    selected_rank = None
    if not selected.empty:
        selected_rank = int(selected.iloc[0]["local_candidate_rank"])
    is_worked_scoring_example = example.key in WORKED_SCORING_EXAMPLE_KEYS

    return {
        "key": example.key,
        "example_type": example.title,
        "title": example.title,
        "file": str(output_path.relative_to(_ROOT)),
        "plain_language_summary": example.summary,
        "ambiguity_reason": example.ambiguity,
        "reason_selected": example.reason,
        "collision_id": str(row["collision_id"]),
        "year": int(row["collision_year"]) if pd.notna(row.get("collision_year")) else None,
        "stats19_source_record": _stats19_source_record(row),
        "stats19_plain_text": _stats19_plain_text(row),
        "selected_link_id": str(row["matched_link_id"]),
        "link_id": str(row["matched_link_id"]),
        "snap_method": str(row["snap_method"]),
        "snap_score": round(float(row["snap_score"]), 4) if pd.notna(row["snap_score"]) else None,
        "snap_distance_m": (
            round(float(row["snap_distance_m"]), 2) if pd.notna(row["snap_distance_m"]) else None
        ),
        "road_classification": None
        if pd.isna(row.get("road_classification"))
        else str(row["road_classification"]),
        "form_of_way": None if pd.isna(row.get("form_of_way")) else str(row["form_of_way"]),
        "matched_road_name_clean": _string_or_none(row.get("matched_road_name_clean")),
        "candidate_count_shown": int(len(candidates)),
        "retained_status": _retained_status(row),
        "nearby_candidate_links": int(len(candidates)),
        "nearby_links_plotted": int(len(candidates)),
        "selected_local_candidate_rank": selected_rank,
        "top_nearby_candidates": candidate_records,
        "candidate_scoring_table": candidate_records if is_worked_scoring_example else [],
        "candidate_scoring_is_worked_example": is_worked_scoring_example,
        "candidate_scoring_source": "reconstructed_explanatory",
        "candidate_scoring_note": (
            "Candidate scores are reconstructed for explanation from nearby Open Roads "
            "links in the figure window using the weighted snap scoring functions. "
            "The final snapped parquet stores exact component scores only for the "
            "selected link, not for losing candidates."
        ),
        "selected_link_found_in_window": bool(not selected.empty),
    }


def build_snap_example_figures(
    output_dir: Path = OUTPUT_DIR,
    manifest_path: Path = MANIFEST_PATH,
) -> dict[str, Any]:
    rows, columns_used = _normalise_snap_rows()
    examples, missing_types = _select_examples(rows)
    nearby = _read_nearby_openroads(examples)

    figure_records = []
    for example in examples:
        output_path = output_dir / example.filename
        figure_records.append(_plot_example(example, nearby[example.key], output_path))

    manifest = {
        "created_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_files": {
            "snapped": str(SNAPPED_PATH.relative_to(_ROOT)),
            "collisions": str(COLLISION_PATH.relative_to(_ROOT)),
            "openroads": str(OPENROADS_PATH.relative_to(_ROOT)),
        },
        "columns_used": columns_used,
        "examples_created": len(figure_records),
        "example_types_requested": [spec["key"] for spec in EXAMPLES],
        "example_types_not_found_automatically": missing_types,
        "worked_scoring_example_types": sorted(WORKED_SCORING_EXAMPLE_KEYS),
        "candidate_link_logic": (
            "Figures reconstruct nearby candidate links from OS Open Roads within the "
            "display buffer, capped at the 500 m snap search radius. Distances are "
            "line-to-point distances and scores reuse the weighted snap scoring rules; "
            "the persisted parquet does not contain the exact internal candidate list."
        ),
        "snap_parameters": {
            "k_candidates": K_CANDIDATES,
            "search_radius_m": SEARCH_RADIUS,
            "spatial_half_life_m": HALF_LIFE_M,
            "weights": {
                "spatial": W_SPATIAL,
                "class": W_CLASS,
                "junction": W_JUNCTION,
                "number": W_NUMBER,
            },
            "retained_score_threshold": 0.6,
        },
        "figures": figure_records,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    logger.info("Wrote %s snap example figures", len(figure_records))
    logger.info("Wrote %s", manifest_path.relative_to(_ROOT))
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    args = parse_args()
    manifest = build_snap_example_figures(output_dir=args.output_dir, manifest_path=args.manifest)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
