"""
Export full-GB link-level exposure and modelled risk as a QGIS-ready GeoPackage.

This module consumes existing scored/model output parquet files only. It does
not run STATS19 processing, snapping, joining, traffic estimation, AADT
modelling, or collision model scoring.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
from pathlib import Path
from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import pyogrio
import shapely

from road_risk.config import _ROOT
from road_risk.outputs.top_risk_segments import (
    _calibration_caveat,
    _derive_family,
    _derive_road_archetype,
)

logger = logging.getLogger(__name__)

RISK_PATH = _ROOT / "data/models/risk_scores.parquet"
RISK_EB_PATH = _ROOT / "data/models/risk_scores_eb.parquet"
OPENROADS_PATH = _ROOT / "data/processed/shapefiles/openroads.parquet"
NETWORK_PATH = _ROOT / "data/features/network_features.parquet"

DEFAULT_OUTPUT = _ROOT / "data/exports/gis/open-road-risk-gb-link-risk-exposure.gpkg"
DEFAULT_LAYER = "gb_link_risk_exposure"
EXPECTED_FULL_ROWS = 3_941_299

RISK_COLUMNS = [
    "link_id",
    "risk_percentile",
    "predicted_xgb",
    "predicted_glm",
    "collision_count",
    "fatal_count",
    "serious_count",
    "estimated_aadt",
]

OPENROADS_COLUMNS = [
    "link_id",
    "road_classification",
    "road_function",
    "family",
    "road_archetype",
    "form_of_way",
    "link_length_km",
    "is_trunk",
    "geometry",
]

NETWORK_COLUMNS = [
    "link_id",
    "ruc_urban_rural",
    "deprivation_country",
]

OUTPUT_COLUMNS = [
    "link_id",
    "risk_percentile",
    "risk_decile",
    "global_risk_rank",
    "predicted_xgb",
    "predicted_eb",
    "estimated_aadt",
    "link_length_km",
    "exposure_vehicle_km_year",
    "collision_count",
    "fatal_count",
    "serious_count",
    "crude_rate_per_million_vkm",
    "road_classification",
    "road_function",
    "family",
    "road_archetype",
    "form_of_way",
    "deprivation_country",
    "calibration_caveat",
    "is_top_1pct",
    "is_top_5pct",
    "is_top_decile",
    "geometry",
]

KEY_NON_NULL_FIELDS = [
    "link_id",
    "risk_percentile",
    "risk_decile",
    "global_risk_rank",
    "predicted_xgb",
    "predicted_eb",
    "estimated_aadt",
    "link_length_km",
    "exposure_vehicle_km_year",
    "collision_count",
    "fatal_count",
    "serious_count",
    "crude_rate_per_million_vkm",
    "road_classification",
    "road_function",
    "family",
    "road_archetype",
    "form_of_way",
    "deprivation_country",
    "calibration_caveat",
    "geometry",
]


def _schema_columns(path: Path) -> list[str]:
    return pq.ParquetFile(path).schema_arrow.names


def _existing_columns(path: Path, wanted: list[str]) -> list[str]:
    available = set(_schema_columns(path))
    return [col for col in wanted if col in available]


def _read_indexed(path: Path, columns: list[str]) -> pd.DataFrame:
    existing = _existing_columns(path, columns)
    missing = sorted(set(columns).difference(existing))
    if missing:
        logger.info("Skipping unavailable columns in %s: %s", _display_path(path), missing)
    if "link_id" not in existing:
        raise KeyError(f"{path} has no link_id column")
    df = pd.read_parquet(path, columns=existing).set_index("link_id", drop=False)
    df.index.name = None
    return df


def _risk_decile(risk_percentile: pd.Series) -> pd.Series:
    values = pd.to_numeric(risk_percentile, errors="coerce")
    decile = np.floor(values / 10.0).add(1).clip(lower=1, upper=10)
    return decile.astype("Int64")


def _safe_crude_rate(collision_count: pd.Series, exposure: pd.Series) -> pd.Series:
    collisions = pd.to_numeric(collision_count, errors="coerce")
    exposure_num = pd.to_numeric(exposure, errors="coerce")
    valid = np.isfinite(exposure_num) & (exposure_num > 0)
    rate = pd.Series(np.nan, index=collision_count.index, dtype="float64")
    rate.loc[valid] = collisions.loc[valid] / exposure_num.loc[valid] * 1_000_000
    return rate


def _load_risk_scores(risk_path: Path) -> pd.DataFrame:
    risk = _read_indexed(risk_path, RISK_COLUMNS)
    ranking_field = "risk_percentile" if "risk_percentile" in risk.columns else "predicted_xgb"
    risk[ranking_field] = pd.to_numeric(risk[ranking_field], errors="coerce")
    if risk[ranking_field].isna().any():
        missing = int(risk[ranking_field].isna().sum())
        raise ValueError(f"{missing:,} risk rows have missing {ranking_field}")

    ranked_ids = (
        risk[[ranking_field, "link_id"]]
        .sort_values([ranking_field, "link_id"], ascending=[False, True], kind="mergesort")
        .index
    )
    ranks = pd.Series(np.arange(1, len(ranked_ids) + 1), index=ranked_ids, name="global_risk_rank")
    risk = risk.join(ranks)
    risk["risk_decile"] = _risk_decile(risk["risk_percentile"])
    risk["is_top_1pct"] = pd.to_numeric(risk["risk_percentile"], errors="coerce").ge(99)
    risk["is_top_5pct"] = pd.to_numeric(risk["risk_percentile"], errors="coerce").ge(95)
    risk["is_top_decile"] = pd.to_numeric(risk["risk_percentile"], errors="coerce").ge(90)
    return risk


def _load_predicted_eb(risk_eb_path: Path | None) -> pd.DataFrame:
    if risk_eb_path is None or not risk_eb_path.exists():
        return pd.DataFrame(columns=["link_id", "predicted_eb"]).set_index("link_id")
    columns = _existing_columns(risk_eb_path, ["link_id", "predicted_eb"])
    if "predicted_eb" not in columns:
        return pd.DataFrame(columns=["link_id", "predicted_eb"]).set_index("link_id")
    eb = pd.read_parquet(risk_eb_path, columns=columns)
    eb = eb.drop_duplicates("link_id").set_index("link_id", drop=False)
    eb.index.name = None
    return eb


def _add_export_fields(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    if "family" not in result.columns or result["family"].isna().all():
        result["family"] = _derive_family(result)
    else:
        result["family"] = result["family"].fillna(_derive_family(result))
    if "road_archetype" not in result.columns or result["road_archetype"].isna().all():
        result["road_archetype"] = _derive_road_archetype(result)
    else:
        result["road_archetype"] = result["road_archetype"].fillna(_derive_road_archetype(result))

    road_classification = result.get(
        "road_classification", pd.Series("", index=result.index)
    ).fillna("")
    road_function = result.get("road_function", pd.Series("", index=result.index)).fillna("")
    result["is_motorway"] = road_classification.eq("Motorway") | road_function.eq("Motorway")
    result["low_exposure_flag"] = pd.to_numeric(result["estimated_aadt"], errors="coerce").lt(500)
    result["sparse_collision_history_flag"] = pd.to_numeric(
        result["collision_count"], errors="coerce"
    ).le(1)
    result["calibration_caveat"] = result.apply(_calibration_caveat, axis=1)

    result["exposure_vehicle_km_year"] = (
        pd.to_numeric(result["estimated_aadt"], errors="coerce")
        * pd.to_numeric(result["link_length_km"], errors="coerce")
        * 365
    )
    result["crude_rate_per_million_vkm"] = _safe_crude_rate(
        result["collision_count"], result["exposure_vehicle_km_year"]
    )
    return result


def _write_qgis_styles(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    risk_qml = """<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34" styleCategories="Symbology">
  <renderer-v2 type="graduatedSymbol" attr="risk_decile" graduatedMethod="GraduatedColor" symbollevels="0">
    <ranges>
      <range lower="1" upper="1" symbol="0" label="1 lowest"/>
      <range lower="2" upper="2" symbol="1" label="2"/>
      <range lower="3" upper="3" symbol="2" label="3"/>
      <range lower="4" upper="4" symbol="3" label="4"/>
      <range lower="5" upper="5" symbol="4" label="5"/>
      <range lower="6" upper="6" symbol="5" label="6"/>
      <range lower="7" upper="7" symbol="6" label="7"/>
      <range lower="8" upper="8" symbol="7" label="8"/>
      <range lower="9" upper="9" symbol="8" label="9"/>
      <range lower="10" upper="10" symbol="9" label="10 highest"/>
    </ranges>
    <symbols>
      <symbol name="0" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="255,247,236,255"/><Option name="line_width" value="0.18"/></Option></layer></symbol>
      <symbol name="1" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="254,232,200,255"/><Option name="line_width" value="0.18"/></Option></layer></symbol>
      <symbol name="2" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="253,212,158,255"/><Option name="line_width" value="0.20"/></Option></layer></symbol>
      <symbol name="3" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="253,187,132,255"/><Option name="line_width" value="0.20"/></Option></layer></symbol>
      <symbol name="4" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="252,141,89,255"/><Option name="line_width" value="0.22"/></Option></layer></symbol>
      <symbol name="5" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="239,101,72,255"/><Option name="line_width" value="0.22"/></Option></layer></symbol>
      <symbol name="6" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="215,48,31,255"/><Option name="line_width" value="0.25"/></Option></layer></symbol>
      <symbol name="7" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="179,0,0,255"/><Option name="line_width" value="0.28"/></Option></layer></symbol>
      <symbol name="8" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="127,0,0,255"/><Option name="line_width" value="0.32"/></Option></layer></symbol>
      <symbol name="9" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="80,0,0,255"/><Option name="line_width" value="0.42"/></Option></layer></symbol>
    </symbols>
  </renderer-v2>
</qgis>
"""
    rate_qml = """<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34" styleCategories="Symbology">
  <renderer-v2 type="graduatedSymbol" attr="crude_rate_per_million_vkm" graduatedMethod="GraduatedColor" symbollevels="0">
    <ranges>
      <range lower="0" upper="1" symbol="0" label="0-1"/>
      <range lower="1" upper="5" symbol="1" label="1-5"/>
      <range lower="5" upper="10" symbol="2" label="5-10"/>
      <range lower="10" upper="25" symbol="3" label="10-25"/>
      <range lower="25" upper="50" symbol="4" label="25-50"/>
      <range lower="50" upper="1000000000" symbol="5" label="50+"/>
    </ranges>
    <symbols>
      <symbol name="0" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="241,245,249,255"/><Option name="line_width" value="0.18"/></Option></layer></symbol>
      <symbol name="1" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="186,230,253,255"/><Option name="line_width" value="0.20"/></Option></layer></symbol>
      <symbol name="2" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="125,211,252,255"/><Option name="line_width" value="0.22"/></Option></layer></symbol>
      <symbol name="3" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="56,189,248,255"/><Option name="line_width" value="0.25"/></Option></layer></symbol>
      <symbol name="4" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="2,132,199,255"/><Option name="line_width" value="0.30"/></Option></layer></symbol>
      <symbol name="5" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="12,74,110,255"/><Option name="line_width" value="0.38"/></Option></layer></symbol>
    </symbols>
  </renderer-v2>
</qgis>
"""
    (output_dir / "risk_decile.qml").write_text(risk_qml, encoding="utf-8")
    (output_dir / "crude_collision_rate.qml").write_text(rate_qml, encoding="utf-8")


def _format_size(path: Path) -> str:
    size = path.stat().st_size
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} B"


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(_ROOT))
    except ValueError:
        return str(path)


def _update_bounds(current: list[float] | None, bounds: np.ndarray) -> list[float]:
    if bounds is None or len(bounds) != 4 or not np.isfinite(bounds).all():
        return current if current is not None else [math.nan, math.nan, math.nan, math.nan]
    if current is None or not np.isfinite(current).all():
        return [float(bounds[0]), float(bounds[1]), float(bounds[2]), float(bounds[3])]
    return [
        min(float(current[0]), float(bounds[0])),
        min(float(current[1]), float(bounds[1])),
        max(float(current[2]), float(bounds[2])),
        max(float(current[3]), float(bounds[3])),
    ]


def export_gis(
    risk_scores: Path = RISK_PATH,
    openroads: Path = OPENROADS_PATH,
    network_features: Path = NETWORK_PATH,
    risk_scores_eb: Path | None = RISK_EB_PATH,
    output: Path = DEFAULT_OUTPUT,
    layer: str = DEFAULT_LAYER,
    batch_size: int = 200_000,
    overwrite: bool = True,
    limit: int | None = None,
) -> dict[str, Any]:
    if not risk_scores.exists():
        raise FileNotFoundError(risk_scores)
    if not openroads.exists():
        raise FileNotFoundError(openroads)
    if not network_features.exists():
        raise FileNotFoundError(network_features)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and overwrite:
        output.unlink()
    elif output.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {output}")

    logger.info("Loading full risk score index")
    risk = _load_risk_scores(risk_scores)
    logger.info("Loading EB predictions where available")
    predicted_eb = _load_predicted_eb(risk_scores_eb)
    logger.info("Loading compact network context")
    network = _read_indexed(network_features, NETWORK_COLUMNS)

    openroads_cols = _existing_columns(openroads, OPENROADS_COLUMNS)
    if "geometry" not in openroads_cols:
        raise KeyError(f"{openroads} has no geometry column")

    non_null_counts = dict.fromkeys(KEY_NON_NULL_FIELDS, 0)
    country_counts: dict[str, int] = {}
    total_rows = 0
    bounds: list[float] | None = None
    first_chunk = True
    parquet_file = pq.ParquetFile(openroads)

    logger.info("Writing %s layer %s", _display_path(output), layer)
    for batch in parquet_file.iter_batches(columns=openroads_cols, batch_size=batch_size):
        roads = batch.to_pandas()
        if limit is not None:
            remaining = limit - total_rows
            if remaining <= 0:
                break
            roads = roads.head(remaining)

        merged = roads.merge(risk, on="link_id", how="inner", validate="one_to_one")
        if predicted_eb is not None and not predicted_eb.empty:
            merged = merged.merge(
                predicted_eb[["link_id", "predicted_eb"]],
                on="link_id",
                how="left",
                validate="one_to_one",
            )
        else:
            merged["predicted_eb"] = np.nan
        merged = merged.merge(
            network[[c for c in NETWORK_COLUMNS if c in network.columns]],
            on="link_id",
            how="left",
            validate="one_to_one",
        )
        merged = _add_export_fields(merged)

        geometry = shapely.from_wkb(merged.pop("geometry"))
        gdf = gpd.GeoDataFrame(merged, geometry=geometry, crs="EPSG:4326")
        gdf = gdf[OUTPUT_COLUMNS]

        pyogrio.write_dataframe(
            gdf,
            output,
            layer=layer,
            driver="GPKG",
            append=not first_chunk,
            use_arrow=True,
        )
        first_chunk = False

        rows = len(gdf)
        total_rows += rows
        bounds = _update_bounds(bounds, gdf.total_bounds)
        for field in KEY_NON_NULL_FIELDS:
            if field == "geometry":
                non_null_counts[field] += int(gdf.geometry.notna().sum())
            elif field in gdf.columns:
                non_null_counts[field] += int(gdf[field].notna().sum())
        if "deprivation_country" in gdf.columns:
            for key, value in gdf["deprivation_country"].fillna("missing").value_counts().items():
                country_counts[str(key)] = country_counts.get(str(key), 0) + int(value)
        logger.info("  wrote %s rows", f"{total_rows:,}")

    if limit is None and total_rows != len(risk):
        raise RuntimeError(
            f"Export row count {total_rows:,} does not match risk rows {len(risk):,}"
        )
    if limit is None and total_rows != EXPECTED_FULL_ROWS:
        raise RuntimeError(
            f"Export row count {total_rows:,} does not match expected {EXPECTED_FULL_ROWS:,}"
        )

    _write_qgis_styles(output.parent)
    info = pyogrio.read_info(output, layer=layer)
    validation = {
        "output": _display_path(output),
        "layer": layer,
        "row_count": total_rows,
        "bounds": bounds,
        "crs": "EPSG:4326",
        "geometry_type": info.get("geometry_type"),
        "non_null_counts": non_null_counts,
        "deprivation_country_counts": country_counts,
        "wales_present": country_counts.get("Wales", 0) > 0,
        "scotland_present": country_counts.get("Scotland", 0) > 0,
        "file_size": _format_size(output),
        "qgis_styles": [
            _display_path(output.parent / "risk_decile.qml"),
            _display_path(output.parent / "crude_collision_rate.qml"),
        ],
    }
    return validation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--risk-scores", type=Path, default=RISK_PATH)
    parser.add_argument("--risk-scores-eb", type=Path, default=RISK_EB_PATH)
    parser.add_argument("--openroads", type=Path, default=OPENROADS_PATH)
    parser.add_argument("--network-features", type=Path, default=NETWORK_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--layer", default=DEFAULT_LAYER)
    parser.add_argument("--batch-size", type=int, default=200_000)
    parser.add_argument("--limit", type=int, default=None, help="Write only the first N rows")
    parser.add_argument(
        "--smoke-rows",
        type=int,
        default=None,
        help="Alias for --limit, intended for small external packaging smoke tests",
    )
    parser.add_argument("--no-overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    args = parse_args()
    if args.limit is not None and args.smoke_rows is not None and args.limit != args.smoke_rows:
        raise ValueError("--limit and --smoke-rows were both provided with different values")
    limit = args.smoke_rows if args.smoke_rows is not None else args.limit
    validation = export_gis(
        risk_scores=args.risk_scores,
        risk_scores_eb=args.risk_scores_eb,
        openroads=args.openroads,
        network_features=args.network_features,
        output=args.output,
        layer=args.layer,
        batch_size=args.batch_size,
        overwrite=not args.no_overwrite,
        limit=limit,
    )
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
