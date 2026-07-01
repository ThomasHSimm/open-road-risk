"""
Build and assign Great Britain rural-urban context for road links.

England/Wales use the ONS 2021 Rural Urban Classification at LSOA 2021
grain. Scotland uses the Scottish Government Urban Rural Classification 2022
polygon layer.
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from road_risk.config import _ROOT

logger = logging.getLogger(__name__)

BNG = "EPSG:27700"

RAW_RUC = _ROOT / "data/raw/urban_rural_ruc"
EW_RUC_PATH = RAW_RUC / "engwal_2021/ruc_2021_lsoa_ew.csv"
SCOT_RUC_PATH = RAW_RUC / "scot_2022/SG_UrbanRural_2022.shp"
EW_OA_BOUNDARY_DIR = _ROOT / "data/raw/boundaries/eng_output_areas_2021"

OPENROADS_PATH = _ROOT / "data/processed/shapefiles/openroads.parquet"
LINK_RURAL_URBAN_PATH = _ROOT / "data/processed/context/link_rural_urban_gb.parquet"
RUC_PROV_PATH = _ROOT / "data/provenance/ruc_provenance.json"

RUC_FALLBACK_M = 250
EW_REQUIRED_COLUMNS = ["LSOA21CD", "RUC21CD", "RUC21NM", "Urban_rural_flag"]
LINK_COLUMNS = [
    "link_id",
    "ruc_country",
    "ruc_source",
    "ruc_area_code",
    "ruc_area_type",
    "ruc_class",
    "ruc_urban_rural",
    "ruc_assignment_method",
    "ruc_assignment_distance_m",
]
AREA_COLUMNS = [
    "ruc_country",
    "ruc_source",
    "ruc_area_code",
    "ruc_area_type",
    "ruc_class",
    "ruc_urban_rural",
    "geometry",
]


def get_script_git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=8", "HEAD"],
            cwd=_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def repo_display_path(path: Path) -> str:
    return f"{_ROOT.name}/{path.resolve().relative_to(_ROOT)}"


def _find_ew_oa_boundary(path: Path | None = None) -> Path:
    if path is not None:
        return Path(path)

    matches = sorted(EW_OA_BOUNDARY_DIR.glob("*.gpkg"))
    if not matches:
        raise FileNotFoundError(
            f"England/Wales OA boundary file not found. Expected a GPKG in {EW_OA_BOUNDARY_DIR}"
        )
    if len(matches) > 1:
        logger.info("Multiple E/W OA boundary files found; using %s", matches[0].name)
    return matches[0]


def _counts(series: pd.Series) -> dict[str, int]:
    counts = (
        series.astype("object").where(series.notna(), "NaN").value_counts(dropna=False).sort_index()
    )
    return {str(k): int(v) for k, v in counts.items()}


def _load_ew_ruc_lookup(path: Path = EW_RUC_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"England/Wales RUC CSV not found: {path}")

    header = pd.read_csv(path, nrows=0, encoding="utf-8-sig")
    missing = [col for col in EW_REQUIRED_COLUMNS if col not in header.columns]
    if missing:
        raise ValueError(
            f"England/Wales RUC CSV at {path} is missing columns {missing}. "
            f"Found columns: {header.columns.tolist()}."
        )

    ruc = pd.read_csv(path, usecols=EW_REQUIRED_COLUMNS, encoding="utf-8-sig")
    for col in EW_REQUIRED_COLUMNS:
        ruc[col] = ruc[col].astype("string").str.strip()

    if ruc["LSOA21CD"].duplicated().any():
        dupes = int(ruc["LSOA21CD"].duplicated().sum())
        raise ValueError(f"England/Wales RUC contains {dupes:,} duplicate LSOA21CD rows")
    if not ruc["LSOA21CD"].str.startswith(("E", "W")).all():
        raise ValueError("England/Wales RUC contains non-E/W LSOA21CD values")

    ruc["ruc_country"] = np.select(
        [ruc["LSOA21CD"].str.startswith("E"), ruc["LSOA21CD"].str.startswith("W")],
        ["England", "Wales"],
        default=pd.NA,
    )
    ruc["ruc_source"] = "ONS 2021 Rural Urban Classification"
    ruc["ruc_area_code"] = ruc["LSOA21CD"]
    ruc["ruc_area_type"] = "LSOA2021"
    ruc["ruc_class"] = ruc["RUC21NM"]
    ruc["ruc_urban_rural"] = ruc["Urban_rural_flag"]
    ruc.loc[~ruc["ruc_urban_rural"].isin(["Urban", "Rural"]), "ruc_urban_rural"] = pd.NA
    return ruc[
        [
            "ruc_country",
            "ruc_source",
            "ruc_area_code",
            "ruc_area_type",
            "ruc_class",
            "ruc_urban_rural",
        ]
    ].copy()


def _load_ew_lsoa2021_ruc_areas(
    ruc_path: Path = EW_RUC_PATH,
    ew_oa_boundary_path: Path | None = None,
) -> gpd.GeoDataFrame:
    boundary_path = _find_ew_oa_boundary(ew_oa_boundary_path)
    oa = gpd.read_file(boundary_path, columns=["LSOA21CD", "geometry"]).to_crs(BNG)
    if "LSOA21CD" not in oa.columns:
        raise ValueError(f"{boundary_path} is missing LSOA21CD")

    oa["LSOA21CD"] = oa["LSOA21CD"].astype("string").str.strip()
    if not oa["LSOA21CD"].str.startswith(("E", "W")).all():
        raise ValueError("England/Wales OA boundary contains non-E/W LSOA21CD values")

    logger.info("Dissolving E/W OA 2021 polygons to LSOA 2021 for RUC")
    lsoa = oa.dissolve(by="LSOA21CD", as_index=False)
    lsoa = lsoa.rename(columns={"LSOA21CD": "ruc_area_code"})
    if lsoa["ruc_area_code"].duplicated().any():
        raise ValueError("Dissolved E/W LSOA boundary contains duplicate ruc_area_code rows")

    attrs = _load_ew_ruc_lookup(ruc_path)
    areas = attrs.merge(
        lsoa[["ruc_area_code", "geometry"]],
        on="ruc_area_code",
        how="left",
        validate="one_to_one",
    )
    missing_geometry = int(areas["geometry"].isna().sum())
    if missing_geometry:
        raise ValueError(
            f"England/Wales RUC has {missing_geometry:,} rows without LSOA2021 geometry"
        )

    return gpd.GeoDataFrame(areas, geometry="geometry", crs=BNG)[AREA_COLUMNS]


def _load_scotland_ruc_areas(path: Path = SCOT_RUC_PATH) -> gpd.GeoDataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Scotland rural-urban shapefile not found: {path}")

    gdf = gpd.read_file(path).to_crs(BNG)
    required = {"UR8Class", "UR6Name", "UR2Class", "UR2Name", "geometry"}
    missing = required.difference(gdf.columns)
    if missing:
        raise ValueError(f"Scotland rural-urban shapefile is missing columns: {sorted(missing)}")

    result = gdf[["UR8Class", "UR6Name", "UR2Class", "UR2Name", "geometry"]].copy()
    result["ruc_country"] = "Scotland"
    result["ruc_source"] = "Scottish Government Urban Rural Classification 2022"
    result["ruc_area_code"] = "SGUR2022_UR8_" + result["UR8Class"].astype(str)
    result["ruc_area_type"] = "SGUR2022_UR8"
    result["ruc_class"] = result["UR6Name"].astype("string").str.strip()
    result["ruc_urban_rural"] = np.where(result["UR2Class"].astype(int).eq(2), "Rural", "Urban")

    if result["ruc_area_code"].duplicated().any():
        raise ValueError("Scotland rural-urban polygons contain duplicate area codes")
    return gpd.GeoDataFrame(result[AREA_COLUMNS], geometry="geometry", crs=BNG)


def build_gb_rural_urban_areas(
    ew_ruc_path: Path = EW_RUC_PATH,
    ew_oa_boundary_path: Path | None = None,
    scot_ruc_path: Path = SCOT_RUC_PATH,
) -> gpd.GeoDataFrame:
    """Build GB rural-urban polygons with a shared model-ready schema."""
    ew = _load_ew_lsoa2021_ruc_areas(ew_ruc_path, ew_oa_boundary_path)
    scot = _load_scotland_ruc_areas(scot_ruc_path)
    combined = pd.concat([ew, scot], ignore_index=True)
    areas = gpd.GeoDataFrame(combined, geometry="geometry", crs=BNG)
    if areas["ruc_area_code"].duplicated().any():
        dupes = int(areas["ruc_area_code"].duplicated().sum())
        raise ValueError(f"GB rural-urban areas contain {dupes:,} duplicate area codes")
    logger.info(
        "Built GB rural-urban areas: %s",
        areas["ruc_country"].value_counts().sort_index().to_dict(),
    )
    return areas[AREA_COLUMNS]


def assign_rural_urban_to_links(
    openroads: gpd.GeoDataFrame,
    output_path: Path | None = LINK_RURAL_URBAN_PATH,
    fallback_m: float = RUC_FALLBACK_M,
) -> pd.DataFrame:
    """
    Assign GB rural-urban attributes to road links by centroid.

    Primary assignment is road-link centroid within the RUC polygon. Unmatched
    centroids get a nearest-polygon fallback within fallback_m metres.
    """
    areas = build_gb_rural_urban_areas()
    roads = openroads[["link_id", "geometry"]].copy().to_crs(BNG)
    road_centroids = gpd.GeoDataFrame(roads[["link_id"]], geometry=roads.geometry.centroid, crs=BNG)

    within = gpd.sjoin(road_centroids, areas[AREA_COLUMNS], how="left", predicate="within")
    matched = within["ruc_area_code"].notna()
    matched_link_ids = set(within.loc[matched, "link_id"])
    unmatched = road_centroids.loc[~road_centroids["link_id"].isin(matched_link_ids)]

    within = within.loc[matched].copy()
    within["ruc_assignment_method"] = "within"
    within["ruc_assignment_distance_m"] = 0.0

    if not unmatched.empty:
        nearest = gpd.sjoin_nearest(
            unmatched,
            areas[AREA_COLUMNS],
            how="left",
            max_distance=fallback_m,
            distance_col="ruc_assignment_distance_m",
        )
        nearest["ruc_assignment_method"] = np.where(
            nearest["ruc_area_code"].notna(),
            "nearest_fallback",
            pd.NA,
        )
    else:
        nearest = gpd.GeoDataFrame(columns=list(within.columns), crs=BNG)

    assigned = within if nearest.empty else pd.concat([within, nearest], ignore_index=True)
    if not assigned.empty:
        assigned = assigned.sort_values(
            ["link_id", "ruc_assignment_distance_m"], na_position="last"
        ).drop_duplicates(subset="link_id", keep="first")

    result = road_centroids[["link_id"]].merge(
        assigned[LINK_COLUMNS],
        on="link_id",
        how="left",
        validate="one_to_one",
    )
    result["ruc_assignment_method"] = result["ruc_assignment_method"].fillna("unmatched")
    result = pd.DataFrame(result.drop(columns="geometry", errors="ignore"))[LINK_COLUMNS]

    logger.info(
        "  Rural-urban matched for %s / %s links",
        f"{result['ruc_urban_rural'].notna().sum():,}",
        f"{len(result):,}",
    )
    logger.info(
        "  Rural-urban assignment methods: %s",
        result["ruc_assignment_method"].value_counts(dropna=False).to_dict(),
    )

    n_unmatched = int((result["ruc_assignment_method"] == "unmatched").sum())
    n_fallback = int((result["ruc_assignment_method"] == "nearest_fallback").sum())
    if n_unmatched:
        logger.warning(
            "  Rural-urban assignment left %s / %s links unmatched",
            f"{n_unmatched:,}",
            f"{len(result):,}",
        )
    if len(result) and n_fallback / len(result) > 0.05:
        logger.warning(
            "  Rural-urban assignment used nearest fallback for %.1f%% of links; "
            "check CRS/boundary coverage.",
            100 * n_fallback / len(result),
        )

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result.to_parquet(output_path, index=False)
        logger.info("Wrote link rural-urban assignments to %s", output_path)
    return result


def load_or_build_link_rural_urban(
    openroads: gpd.GeoDataFrame,
    path: Path = LINK_RURAL_URBAN_PATH,
    force: bool = False,
) -> pd.DataFrame:
    if path.exists() and not force:
        logger.info("Loading link rural-urban assignments from %s", path)
        return pd.read_parquet(path)
    return assign_rural_urban_to_links(openroads, output_path=path)


def write_ruc_provenance(features: pd.DataFrame) -> None:
    required = {
        "ruc_country",
        "ruc_source",
        "ruc_area_type",
        "ruc_class",
        "ruc_urban_rural",
        "ruc_assignment_method",
        "ruc_assignment_distance_m",
    }
    missing = required.difference(features.columns)
    if missing:
        logger.warning("Skipping RUC provenance; missing columns: %s", sorted(missing))
        return

    fallback_distances = features.loc[
        features["ruc_assignment_method"].eq("nearest_fallback"),
        "ruc_assignment_distance_m",
    ].dropna()
    provenance = {
        "script_path": repo_display_path(Path(__file__)),
        "git_sha": get_script_git_sha(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "output_file": repo_display_path(LINK_RURAL_URBAN_PATH),
        "source_files": {
            "england_wales_ruc": repo_display_path(EW_RUC_PATH),
            "england_wales_boundary": repo_display_path(_find_ew_oa_boundary()),
            "scotland_ruc": repo_display_path(SCOT_RUC_PATH),
        },
        "assignment": "road-link centroid to GB rural-urban polygon; nearest fallback for unmatched centroids",
        "fallback_distance_cap_m": RUC_FALLBACK_M,
        "n_links_total": int(len(features)),
        "n_links_with_ruc": int(features["ruc_urban_rural"].notna().sum()),
        "ruc_country_distribution": _counts(features["ruc_country"]),
        "ruc_area_type_distribution": _counts(features["ruc_area_type"]),
        "ruc_urban_rural_distribution": _counts(features["ruc_urban_rural"]),
        "ruc_class_distribution": _counts(features["ruc_class"]),
        "ruc_assignment_method_distribution": _counts(features["ruc_assignment_method"]),
        "fallback_distance_m": {
            "median": float(fallback_distances.median()) if not fallback_distances.empty else None,
            "p95": (
                float(fallback_distances.quantile(0.95)) if not fallback_distances.empty else None
            ),
            "max": float(fallback_distances.max()) if not fallback_distances.empty else None,
        },
    }

    RUC_PROV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RUC_PROV_PATH, "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)
    logger.info("Wrote RUC provenance to %s", RUC_PROV_PATH)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Rebuild even if output exists")
    parser.add_argument("--output", type=Path, default=LINK_RURAL_URBAN_PATH)
    args = parser.parse_args()

    openroads = gpd.read_parquet(OPENROADS_PATH)
    result = load_or_build_link_rural_urban(openroads, path=args.output, force=args.force)
    write_ruc_provenance(result)
    print("\n=== GB rural-urban assignment ===")
    print(f"Rows: {len(result):,}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
