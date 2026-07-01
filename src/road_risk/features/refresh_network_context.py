"""
Refresh lightweight context columns in network_features.parquet.

This module updates population, deprivation, and RUC fields without recomputing
the expensive graph/topology features in road_risk.features.network.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd

from road_risk.features.deprivation import (
    LINK_DEPRIVATION_PATH,
    assign_deprivation_to_links,
    write_deprivation_provenance,
)
from road_risk.features.network import (
    OPENROADS_PATH,
    OUTPUT_PATH,
    apply_speed_limit_effective_lookup,
    compute_population_density_oa,
    write_population_assignment_provenance,
    write_speed_limit_effective_provenance,
)
from road_risk.features.rural_urban import (
    LINK_RURAL_URBAN_PATH,
    load_or_build_link_rural_urban,
    write_ruc_provenance,
)

logger = logging.getLogger(__name__)

CONTEXT_COLUMNS_TO_DROP = [
    # Old and new population context.
    "pop_density_per_km2",
    "population_area_code",
    "population_area_type",
    "population_nation",
    "population_assignment_method",
    "population_assignment_distance_m",
    # GB deprivation context.
    "deprivation_area_code",
    "deprivation_area_type",
    "deprivation_country",
    "deprivation_source",
    "deprivation_assignment_method",
    "deprivation_assignment_distance_m",
    "overall_decile_within_country",
    "income_decile_within_country",
    "employment_decile_within_country",
    "deprivation_country_england",
    "deprivation_country_wales",
    "deprivation_country_scotland",
    # GB rural-urban context.
    "ruc_country",
    "ruc_source",
    "ruc_area_code",
    "ruc_area_type",
    "ruc_class",
    "ruc_urban_rural",
    "ruc_assignment_method",
    "ruc_assignment_distance_m",
]

SPEED_LIMIT_EFFECTIVE_COLUMNS = [
    "speed_limit_mph_effective",
    "speed_limit_mph_imputed",
    "speed_limit_source",
]


def _assert_same_link_universe(features: pd.DataFrame, openroads: pd.DataFrame) -> None:
    """Fail fast if cached features and Open Roads are not the same link universe."""
    if features["link_id"].duplicated().any():
        raise ValueError("network_features.parquet contains duplicate link_id values.")
    if openroads["link_id"].duplicated().any():
        raise ValueError("openroads.parquet contains duplicate link_id values.")

    feature_links = pd.Index(features["link_id"])
    openroad_links = pd.Index(openroads["link_id"])
    missing_from_features = openroad_links.difference(feature_links)
    missing_from_openroads = feature_links.difference(openroad_links)

    if len(missing_from_features) or len(missing_from_openroads):
        raise ValueError(
            "network_features.parquet and openroads.parquet have different link_id sets: "
            f"{len(missing_from_features):,} openroads links missing from features; "
            f"{len(missing_from_openroads):,} feature links missing from openroads. "
            "Do a full rebuild or create a fresh graph-feature cache."
        )


def _load_or_build_deprivation(openroads: gpd.GeoDataFrame) -> pd.DataFrame:
    if LINK_DEPRIVATION_PATH.exists():
        logger.info("Loading link deprivation assignments from %s", LINK_DEPRIVATION_PATH)
        return pd.read_parquet(LINK_DEPRIVATION_PATH)

    logger.info("Link deprivation assignments not found; building them.")
    return assign_deprivation_to_links(openroads)


def _load_or_build_ruc(openroads: gpd.GeoDataFrame) -> pd.DataFrame:
    if LINK_RURAL_URBAN_PATH.exists():
        logger.info("Loading link rural-urban assignments from %s", LINK_RURAL_URBAN_PATH)
        return pd.read_parquet(LINK_RURAL_URBAN_PATH)

    logger.info("Link rural-urban assignments not found; building them.")
    return load_or_build_link_rural_urban(openroads)


def _refresh_speed_limit_if_possible(
    features: pd.DataFrame,
    openroads: gpd.GeoDataFrame,
) -> pd.DataFrame:
    if "speed_limit_mph" not in features.columns:
        logger.info("No raw speed_limit_mph column present; leaving speed-limit context absent.")
        return features

    required_openroads_cols = {"link_id", "road_classification", "form_of_way", "is_trunk"}
    missing = required_openroads_cols.difference(openroads.columns)
    if missing:
        logger.warning(
            "Skipping speed-limit effective refresh; openroads missing columns: %s",
            sorted(missing),
        )
        return features

    logger.info("Refreshing effective speed-limit columns after RUC update")
    features = features.drop(columns=SPEED_LIMIT_EFFECTIVE_COLUMNS, errors="ignore")
    return apply_speed_limit_effective_lookup(features, openroads)


def _context_columns_to_drop(features: pd.DataFrame) -> list[str]:
    legacy_prefix = "imd"
    retired_deprivation_cols = [
        col
        for col in features.columns
        if col == f"{legacy_prefix}_decile"
        or (col.startswith(f"{legacy_prefix}_") and col.endswith("_decile"))
    ]
    return [
        col
        for col in [*CONTEXT_COLUMNS_TO_DROP, *retired_deprivation_cols]
        if col in features.columns
    ]


def refresh_network_context(
    network_features_path: Path = OUTPUT_PATH,
    openroads_path: Path = OPENROADS_PATH,
) -> pd.DataFrame:
    """Refresh context features while preserving expensive graph/geometry columns."""
    logger.info("Loading cached network features from %s", network_features_path)
    features = pd.read_parquet(network_features_path)

    logger.info("Loading OS Open Roads from %s", openroads_path)
    openroads = gpd.read_parquet(openroads_path)
    _assert_same_link_universe(features, openroads)

    base = features.drop(columns=_context_columns_to_drop(features), errors="ignore")

    logger.info("Refreshing GB OA population context")
    population = compute_population_density_oa(openroads)
    deprivation = _load_or_build_deprivation(openroads)
    ruc = _load_or_build_ruc(openroads)

    refreshed = (
        base.merge(population, on="link_id", how="left", validate="one_to_one")
        .merge(deprivation, on="link_id", how="left", validate="one_to_one")
        .merge(ruc, on="link_id", how="left", validate="one_to_one")
    )
    refreshed = _refresh_speed_limit_if_possible(refreshed, openroads)

    logger.info("Writing refreshed network features to %s", network_features_path)
    network_features_path.parent.mkdir(parents=True, exist_ok=True)
    refreshed.to_parquet(network_features_path, index=False)

    write_population_assignment_provenance(refreshed)
    write_ruc_provenance(refreshed)
    write_deprivation_provenance(refreshed)
    write_speed_limit_effective_provenance(refreshed)

    return refreshed


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--network-features-path",
        type=Path,
        default=OUTPUT_PATH,
        help=f"Network feature parquet to refresh (default: {OUTPUT_PATH})",
    )
    parser.add_argument(
        "--openroads-path",
        type=Path,
        default=OPENROADS_PATH,
        help=f"Open Roads parquet used for context assignment (default: {OPENROADS_PATH})",
    )
    args = parser.parse_args()

    refreshed = refresh_network_context(
        network_features_path=args.network_features_path,
        openroads_path=args.openroads_path,
    )
    print("\n=== Refreshed network context ===")
    print(f"Rows: {len(refreshed):,}")
    print(f"Columns: {len(refreshed.columns):,}")
    print(f"Saved to: {args.network_features_path}")


if __name__ == "__main__":
    main()
