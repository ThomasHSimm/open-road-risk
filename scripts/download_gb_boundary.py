"""
Download and build the configured GB boundary.

Source:
  ONS Open Geography Portal / ArcGIS FeatureServer
  Countries (December 2023) Boundaries UK BGC

The source contains four UK country polygons. This script keeps England,
Scotland, and Wales, dissolves them to one GB feature, and writes:
  data/raw/boundaries/gb_boundary.gpkg

BGC is the ONS 20 m generalised, coastline-clipped product. It is small enough
to download reliably and precise enough for national study-area filtering.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import geopandas as gpd
import requests

from road_risk.config import _ROOT, cfg

LOGGER = logging.getLogger(__name__)

SERVICE_URL = (
    "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
    "Countries_December_2023_Boundaries_UK_BGC/FeatureServer/0/query"
)
SOURCE_ITEM_URL = (
    "https://geoportal.statistics.gov.uk/datasets/ons::countries-december-2023-boundaries-uk-bgc"
)


def _output_path(path: str | Path | None) -> Path:
    configured = cfg["study_area"].get("boundary", "data/raw/boundaries/gb_boundary.gpkg")
    out = Path(path or configured)
    return out if out.is_absolute() else _ROOT / out


def download_gb_boundary(output_path: Path, layer: str) -> None:
    nation_codes = cfg["study_area"].get(
        "nation_codes",
        ["E92000001", "S92000003", "W92000004"],
    )
    quoted_codes = ",".join(f"'{code}'" for code in nation_codes)
    params = {
        "where": f"CTRY23CD IN ({quoted_codes})",
        "outFields": "CTRY23CD,CTRY23NM",
        "outSR": "4326",
        "returnGeometry": "true",
        "f": "geojson",
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_geojson = output_path.with_suffix(".source.geojson")

    LOGGER.info("Downloading ONS country boundary features...")
    response = requests.get(SERVICE_URL, params=params, timeout=180)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("features"):
        raise RuntimeError(f"ONS boundary query returned no features: {json.dumps(payload)[:500]}")

    tmp_geojson.write_text(json.dumps(payload), encoding="utf-8")
    try:
        countries = gpd.read_file(tmp_geojson)
        countries = countries[countries["CTRY23CD"].isin(nation_codes)].copy()
        if countries.empty:
            raise RuntimeError(f"No GB countries found in ONS payload for {nation_codes}")

        dissolved = countries.dissolve()
        gb = gpd.GeoDataFrame(
            {
                "study_area": ["gb"],
                "source": ["ONS Countries December 2023 Boundaries UK BGC"],
                "source_url": [SOURCE_ITEM_URL],
                "nation_codes": [",".join(nation_codes)],
            },
            geometry=[dissolved.geometry.iloc[0]],
            crs=countries.crs,
        )

        if output_path.exists():
            output_path.unlink()
        gb.to_file(output_path, layer=layer, driver="GPKG")
        LOGGER.info("Wrote %s (layer=%s)", output_path, layer)
    finally:
        tmp_geojson.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--layer",
        default=cfg["study_area"].get("boundary_layer", "gb_boundary"),
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    download_gb_boundary(_output_path(args.output), args.layer)


if __name__ == "__main__":
    main()
