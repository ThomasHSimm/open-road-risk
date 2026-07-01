"""
Build population lookup tables and context layers.

Preferred GB population-density feature path:
  OA population + OA boundary -> OA density polygon -> road centroid within OA.

Legacy England/Wales path:
  OA population -> aggregate to LSOA -> nearest LSOA centroid.
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from road_risk.config import _ROOT

logger = logging.getLogger(__name__)

RAW_POPULATION = _ROOT / "data/raw/population"
RAW_BOUNDARIES = _ROOT / "data/raw/boundaries"
PROCESSED_CONTEXT = _ROOT / "data/processed/context"
PROVENANCE = _ROOT / "data/provenance"
ENG_WAL_FOLDER = RAW_POPULATION / "eng_wal"
ENG_WAL_BOUNDARIES_FOLDER = RAW_BOUNDARIES / "eng_output_areas_2021"
SCOT_FOLDER = RAW_POPULATION / "scot"
SCOT_BOUNDARIES_FOLDER = RAW_BOUNDARIES / "scot_output_areas_2022"
DEFAULT_EW_OA_POPULATION = ENG_WAL_FOLDER / "census2021-ts001-oa.csv"
DEFAULT_SCOT_OA_POPULATION = SCOT_FOLDER / "outputarea2022_usualresidentpopulation.csv"
DEFAULT_SCOT_OA_BOUNDARY = SCOT_BOUNDARIES_FOLDER / "OutputArea2022_MHW.shp"
DEFAULT_LSOA_OUTPUT = RAW_POPULATION / "lsoa_population.csv"
DEFAULT_GB_OA_DENSITY_OUTPUT = PROCESSED_CONTEXT / "oa_population_density_gb.parquet"
POPULATION_DENSITY_GB_PROV_PATH = PROVENANCE / "population_density_gb_provenance.json"

OA_CODE_COL = "geography code"
OA_CODE_FALLBACK_COL = "geography"
OA_POPULATION_COL = "Residence type: Total; measures: Value"
LSOA_OUTPUT_COLUMNS = ["LSOA21CD", "population"]
GB_OA_DENSITY_COLUMNS = [
    "oa_code",
    "nation",
    "population_area_type",
    "population_year",
    "population",
    "area_km2",
    "pop_density_per_km2",
    "geometry",
]
MISSING_POPULATION_RATE_THRESHOLD = 0.005


def _find_ew_oa_lookup(path: Path | None = None) -> Path:
    if path is not None:
        return Path(path)

    matches = sorted(ENG_WAL_FOLDER.glob("Output_Areas_2021_EW_BGC_V2_*.xlsx"))
    if not matches:
        matches = sorted(ENG_WAL_BOUNDARIES_FOLDER.glob("Output_Areas_2021_EW_BGC_V2_*.gpkg"))
    if not matches:
        matches = sorted(ENG_WAL_FOLDER.glob("Output_Areas_2021_EW_BGC_V2_*.gpkg"))
    if not matches:
        raise FileNotFoundError(
            "England/Wales OA lookup not found. Expected a file like:\n"
            f"  {ENG_WAL_FOLDER / 'Output_Areas_2021_EW_BGC_V2_*.xlsx'}\n"
            "or:\n"
            f"  {ENG_WAL_BOUNDARIES_FOLDER / 'Output_Areas_2021_EW_BGC_V2_*.gpkg'}"
        )
    if len(matches) > 1:
        logger.info("Multiple OA lookup files found; using %s", matches[0].name)
    return matches[0]


def _find_ew_oa_boundary(path: Path | None = None) -> Path:
    if path is not None:
        return Path(path)

    matches = sorted(ENG_WAL_BOUNDARIES_FOLDER.glob("Output_Areas_2021_EW_BGC_V2_*.gpkg"))
    if not matches:
        matches = sorted(ENG_WAL_FOLDER.glob("Output_Areas_2021_EW_BGC_V2_*.gpkg"))
    if not matches:
        raise FileNotFoundError(
            "England/Wales OA boundary file not found. Expected a file like:\n"
            f"  {ENG_WAL_BOUNDARIES_FOLDER / 'Output_Areas_2021_EW_BGC_V2_*.gpkg'}"
        )
    if len(matches) > 1:
        logger.info("Multiple England/Wales OA boundary files found; using %s", matches[0].name)
    return matches[0]


def _repo_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(_ROOT))
    except ValueError:
        return str(path)


def _git_sha() -> str:
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


def _assert_unique_codes(df: pd.DataFrame, code_col: str, label: str) -> None:
    dupes = df[code_col][df[code_col].duplicated()].dropna().unique()
    if len(dupes):
        sample = ", ".join(map(str, dupes[:5]))
        raise ValueError(f"{label} contains duplicate {code_col} values; sample: {sample}")


def _assert_code_prefix(
    codes: pd.Series,
    prefixes: tuple[str, ...],
    label: str,
    forbidden_prefixes: tuple[str, ...] = (),
) -> None:
    values = codes.dropna().astype(str).str.strip()
    bad = values[~values.str.startswith(prefixes)]
    if not bad.empty:
        raise ValueError(
            f"{label} has {len(bad):,} code(s) outside expected prefixes {prefixes}; "
            f"sample: {bad.head().tolist()}"
        )
    forbidden = (
        values[values.str.startswith(forbidden_prefixes)] if forbidden_prefixes else values[:0]
    )
    if not forbidden.empty:
        raise ValueError(
            f"{label} has {len(forbidden):,} forbidden code(s) with prefixes "
            f"{forbidden_prefixes}; sample: {forbidden.head().tolist()}"
        )


def _validate_missing_population(gdf, label: str) -> None:
    missing = int(gdf["population"].isna().sum())
    rate = missing / len(gdf) if len(gdf) else 0.0
    if rate > MISSING_POPULATION_RATE_THRESHOLD:
        raise ValueError(
            f"{label} missing population for {missing:,} / {len(gdf):,} areas "
            f"({rate:.2%}), above threshold {MISSING_POPULATION_RATE_THRESHOLD:.2%}"
        )
    if missing:
        logger.warning(
            "%s missing population for %s / %s areas (%.2f%%)",
            label,
            f"{missing:,}",
            f"{len(gdf):,}",
            rate * 100,
        )


def _summary_by_nation(df: pd.DataFrame, value_col: str) -> dict[str, dict[str, float | int]]:
    summary: dict[str, dict[str, float | int]] = {}
    for nation, group in df.groupby("nation", dropna=False):
        values = pd.to_numeric(group[value_col], errors="coerce").dropna()
        summary[str(nation)] = {
            "count": int(values.size),
            "min": float(values.min()) if not values.empty else float("nan"),
            "median": float(values.median()) if not values.empty else float("nan"),
            "mean": float(values.mean()) if not values.empty else float("nan"),
            "max": float(values.max()) if not values.empty else float("nan"),
        }
    return summary


def load_england_wales_oa_population(path: Path = DEFAULT_EW_OA_POPULATION) -> pd.DataFrame:
    """Load OA-level England/Wales Census 2021 usual-resident population."""
    if not path.exists():
        raise FileNotFoundError(f"England/Wales OA population file not found: {path}")

    header = pd.read_csv(path, nrows=0, encoding="utf-8-sig").columns
    code_col = OA_CODE_COL if OA_CODE_COL in header else OA_CODE_FALLBACK_COL

    raw = pd.read_csv(
        path,
        usecols=[code_col, OA_POPULATION_COL],
        dtype={code_col: "string"},
        encoding="utf-8-sig",
    ).rename(columns={code_col: "OA21CD", OA_POPULATION_COL: "population"})

    raw["population"] = pd.to_numeric(raw["population"], errors="coerce")
    result = raw.dropna(subset=["OA21CD", "population"]).copy()
    result["population"] = result["population"].astype("int64")
    return result


def load_england_wales_oa_to_lsoa(path: Path | None = None) -> pd.DataFrame:
    """Load the OA21CD -> LSOA21CD lookup from the ONS OA boundary workbook/GPKG."""
    import geopandas as gpd

    lookup_path = _find_ew_oa_lookup(path)
    if lookup_path.suffix.lower() in {".xlsx", ".xls"}:
        lookup = pd.read_excel(lookup_path, usecols=["OA21CD", "LSOA21CD"], dtype="string")
    else:
        layers = gpd.list_layers(lookup_path)
        layer = layers.iloc[0]["name"] if len(layers) else None
        lookup = gpd.read_file(lookup_path, layer=layer, ignore_geometry=True)

    required = {"OA21CD", "LSOA21CD"}
    missing = required - set(lookup.columns)
    if missing:
        raise ValueError(f"{lookup_path} is missing required columns: {sorted(missing)}")

    return lookup[["OA21CD", "LSOA21CD"]].dropna().drop_duplicates()


def build_oa_area_table(boundary_path: str | Path, code_col: str):
    """Utility: build an OA area table from a boundary file, calculating area in BNG."""
    import geopandas as gpd

    boundary_path = Path(boundary_path)
    oa = gpd.read_file(boundary_path)
    oa = oa.to_crs("EPSG:27700")
    oa = oa.rename(columns={code_col: "oa_code"})
    oa["oa_code"] = oa["oa_code"].astype(str).str.strip()
    oa["area_km2"] = oa.geometry.area / 1_000_000
    return oa[["oa_code", "area_km2", "geometry"]]


def _load_england_wales_oa_density_inputs(
    population_path: Path,
    boundary_path: Path | None,
):
    import geopandas as gpd

    boundary_path = _find_ew_oa_boundary(boundary_path)
    population = load_england_wales_oa_population(population_path)
    _assert_unique_codes(population, "OA21CD", "England/Wales OA population")
    _assert_code_prefix(population["OA21CD"], ("E", "W"), "England/Wales OA population")

    boundary = gpd.read_file(boundary_path).to_crs("EPSG:27700")
    if "OA21CD" not in boundary.columns:
        raise ValueError(f"{boundary_path} is missing OA21CD")
    boundary = boundary[["OA21CD", "geometry"]].copy()
    boundary["OA21CD"] = boundary["OA21CD"].astype("string").str.strip()
    _assert_unique_codes(boundary, "OA21CD", "England/Wales OA boundary")
    _assert_code_prefix(boundary["OA21CD"], ("E", "W"), "England/Wales OA boundary")

    merged = boundary.merge(population, on="OA21CD", how="left", validate="one_to_one")
    _validate_missing_population(merged, "England/Wales OA boundary")

    merged = merged.rename(columns={"OA21CD": "oa_code"})
    merged["nation"] = merged["oa_code"].str[0].map({"E": "England", "W": "Wales"})
    merged["population_area_type"] = "OA2021"
    merged["population_year"] = 2021
    return merged, boundary_path


def load_scotland_oa_population(path: Path = DEFAULT_SCOT_OA_POPULATION) -> pd.DataFrame:
    """Load OA-level Scotland Census 2022 usual-resident population."""
    if not path.exists():
        raise FileNotFoundError(f"Scotland OA population file not found: {path}")

    raw = pd.read_csv(
        path,
        usecols=["OutputArea2022", "UsualResidentPopulation"],
        dtype={"OutputArea2022": "string"},
        encoding="utf-8-sig",
    ).rename(columns={"OutputArea2022": "oa_code", "UsualResidentPopulation": "population"})

    raw["oa_code"] = raw["oa_code"].astype("string").str.strip()
    raw["population"] = pd.to_numeric(raw["population"], errors="coerce")
    result = raw.dropna(subset=["oa_code", "population"]).copy()
    result["population"] = result["population"].astype("int64")
    return result


def _load_scotland_oa_density_inputs(
    population_path: Path,
    boundary_path: Path,
):
    import geopandas as gpd

    if not boundary_path.exists():
        raise FileNotFoundError(f"Scotland OA boundary file not found: {boundary_path}")

    population = load_scotland_oa_population(population_path)
    _assert_unique_codes(population, "oa_code", "Scotland OA population")
    _assert_code_prefix(
        population["oa_code"],
        ("S001",),
        "Scotland OA population",
        forbidden_prefixes=("S010",),
    )

    boundary = gpd.read_file(boundary_path).to_crs("EPSG:27700")
    if "code" not in boundary.columns:
        raise ValueError(f"{boundary_path} is missing Scotland OA code column 'code'")
    boundary = boundary[["code", "geometry"]].rename(columns={"code": "oa_code"})
    boundary["oa_code"] = boundary["oa_code"].astype("string").str.strip()
    _assert_unique_codes(boundary, "oa_code", "Scotland OA boundary")
    _assert_code_prefix(
        boundary["oa_code"],
        ("S001",),
        "Scotland OA boundary",
        forbidden_prefixes=("S010",),
    )

    merged = boundary.merge(population, on="oa_code", how="left", validate="one_to_one")
    _validate_missing_population(merged, "Scotland OA boundary")

    merged["nation"] = "Scotland"
    merged["population_area_type"] = "OA2022"
    merged["population_year"] = 2022
    return merged


def _write_gb_population_density_provenance(
    data,
    output_path: Path,
    ew_population_path: Path,
    ew_boundary_path: Path,
    scot_population_path: Path,
    scot_boundary_path: Path,
) -> None:
    provenance = {
        "script_path": _repo_path(Path(__file__)),
        "git_sha": _git_sha(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "output_path": _repo_path(output_path),
        "missing_population_rate_threshold": MISSING_POPULATION_RATE_THRESHOLD,
        "sources": {
            "england_wales": {
                "source_population_file": _repo_path(ew_population_path),
                "source_boundary_file": _repo_path(ew_boundary_path),
                "boundary_type": "ONS OA 2021 EW BGC V2",
                "population_year": 2021,
                "population_area_type": "OA2021",
            },
            "scotland": {
                "source_population_file": _repo_path(scot_population_path),
                "source_boundary_file": _repo_path(scot_boundary_path),
                "boundary_type": "Scotland Output Area 2022 MHW",
                "population_year": 2022,
                "population_area_type": "OA2022",
            },
        },
        "n_areas": int(len(data)),
        "n_missing_population": int(data["population"].isna().sum()),
        "n_areas_by_nation": {
            str(k): int(v)
            for k, v in data["nation"].value_counts(dropna=False).sort_index().items()
        },
        "duplicate_code_checks": {
            "oa_code_duplicates": int(data["oa_code"].duplicated().sum()),
        },
        "area_summary_by_nation": _summary_by_nation(data, "area_km2"),
        "density_summary_by_nation": _summary_by_nation(data, "pop_density_per_km2"),
        "population_summary_by_nation": _summary_by_nation(data, "population"),
    }

    POPULATION_DENSITY_GB_PROV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(POPULATION_DENSITY_GB_PROV_PATH, "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)
    logger.info("Wrote provenance to %s", POPULATION_DENSITY_GB_PROV_PATH)


def build_gb_oa_population_density(
    output_path: Path = DEFAULT_GB_OA_DENSITY_OUTPUT,
    ew_oa_population_path: Path = DEFAULT_EW_OA_POPULATION,
    ew_oa_boundary_path: Path | None = None,
    scot_oa_population_path: Path = DEFAULT_SCOT_OA_POPULATION,
    scot_oa_boundary_path: Path = DEFAULT_SCOT_OA_BOUNDARY,
):
    """
    Build a GB OA population-density polygon layer.

    Output columns:
      oa_code, nation, population_area_type, population_year, population,
      area_km2, pop_density_per_km2, geometry.
    """
    import geopandas as gpd

    ew, ew_boundary_path = _load_england_wales_oa_density_inputs(
        Path(ew_oa_population_path),
        ew_oa_boundary_path,
    )
    scot = _load_scotland_oa_density_inputs(
        Path(scot_oa_population_path),
        Path(scot_oa_boundary_path),
    )

    combined = pd.concat([ew, scot], ignore_index=True)
    gdf = gpd.GeoDataFrame(combined, geometry="geometry", crs="EPSG:27700")
    if gdf.crs is None or gdf.crs.to_epsg() != 27700:
        gdf = gdf.to_crs("EPSG:27700")

    _assert_unique_codes(gdf, "oa_code", "GB OA population-density layer")
    gdf["area_km2"] = gdf.geometry.area / 1_000_000
    if (gdf["area_km2"] <= 0).any():
        bad = gdf.loc[gdf["area_km2"] <= 0, "oa_code"].head().tolist()
        raise ValueError(f"GB OA population-density layer has non-positive areas; sample: {bad}")

    gdf["pop_density_per_km2"] = gdf["population"] / gdf["area_km2"].replace(0, pd.NA)
    gdf = gdf[GB_OA_DENSITY_COLUMNS].sort_values("oa_code").reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_parquet(output_path, index=False)
    logger.info("Wrote %s GB OA population-density rows to %s", f"{len(gdf):,}", output_path)

    _write_gb_population_density_provenance(
        gdf,
        output_path,
        Path(ew_oa_population_path),
        Path(ew_boundary_path),
        Path(scot_oa_population_path),
        Path(scot_oa_boundary_path),
    )
    return gdf


def build_lsoa_population(
    output_path: Path = DEFAULT_LSOA_OUTPUT,
    ew_oa_population_path: Path = DEFAULT_EW_OA_POPULATION,
    ew_oa_lookup_path: Path | None = None,
) -> pd.DataFrame:
    """
    Legacy England/Wales helper for the old LSOA-centroid network feature path.

    Do not use this for GB population-density features. Prefer
    build_gb_oa_population_density().

    Returns a DataFrame with the same columns expected by network.py:
    LSOA21CD, population.
    """
    oa_population = load_england_wales_oa_population(ew_oa_population_path)
    oa_lookup = load_england_wales_oa_to_lsoa(ew_oa_lookup_path)

    merged = oa_lookup.merge(oa_population, on="OA21CD", how="left", validate="one_to_one")
    missing_pop = merged["population"].isna().sum()
    if missing_pop:
        logger.warning(
            "Missing OA population for %s / %s England/Wales OAs",
            f"{missing_pop:,}",
            f"{len(merged):,}",
        )

    lsoa_population = (
        merged.dropna(subset=["population"])
        .groupby("LSOA21CD", as_index=False)["population"]
        .sum()
        .sort_values("LSOA21CD")
    )
    lsoa_population["population"] = lsoa_population["population"].round().astype("int64")
    lsoa_population = lsoa_population[LSOA_OUTPUT_COLUMNS]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    lsoa_population.to_csv(output_path, index=False)
    logger.info(
        "Wrote %s LSOA population rows to %s",
        f"{len(lsoa_population):,}",
        output_path,
    )
    return lsoa_population


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GB OA population-density context layer")
    parser.add_argument(
        "--legacy-lsoa", action="store_true", help="Build legacy E/W LSOA CSV instead"
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--ew-oa-population", type=Path, default=DEFAULT_EW_OA_POPULATION)
    parser.add_argument("--ew-oa-boundary", type=Path, default=None)
    parser.add_argument("--ew-oa-lookup", type=Path, default=None)
    parser.add_argument("--scot-oa-population", type=Path, default=DEFAULT_SCOT_OA_POPULATION)
    parser.add_argument("--scot-oa-boundary", type=Path, default=DEFAULT_SCOT_OA_BOUNDARY)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    if args.legacy_lsoa:
        build_lsoa_population(
            output_path=args.output or DEFAULT_LSOA_OUTPUT,
            ew_oa_population_path=args.ew_oa_population,
            ew_oa_lookup_path=args.ew_oa_lookup,
        )
    else:
        build_gb_oa_population_density(
            output_path=args.output or DEFAULT_GB_OA_DENSITY_OUTPUT,
            ew_oa_population_path=args.ew_oa_population,
            ew_oa_boundary_path=args.ew_oa_boundary,
            scot_oa_population_path=args.scot_oa_population,
            scot_oa_boundary_path=args.scot_oa_boundary,
        )


if __name__ == "__main__":
    main()
