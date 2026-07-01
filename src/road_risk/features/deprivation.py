"""
Build and assign GB deprivation context.

The GB feature surface keeps each national deprivation index separate in
provenance, then exposes only within-country comparable deciles to the model.

England: IoD 2025, LSOA 2021.
Wales: WIMD 2019, LSOA 2011.
Scotland: SIMD 2020v2, Data Zone 2011.
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree as ET

import geopandas as gpd
import numpy as np
import pandas as pd

from road_risk.config import _ROOT

logger = logging.getLogger(__name__)

RAW_IMD = _ROOT / "data/raw/imd"
RAW_BOUNDARIES = _ROOT / "data/raw/boundaries"
PROCESSED_CONTEXT = _ROOT / "data/processed/context"
PROVENANCE = _ROOT / "data/provenance"

ENG_IOD_PATH = RAW_IMD / "eng/File_7_IoD2025_All_Ranks_Scores_Deciles_Population_Denominators.csv"
WAL_WIMD_PATH = (
    RAW_IMD / "wal/welsh-index-multiple-deprivation-2019-index-and-domain-ranks-by-small-area.ods"
)
SCOT_SIMD_PATH = RAW_IMD / "scot/SIMD+2020v2+-+datazone+lookup+-+updated+2025.xlsx"
EW_OA_BOUNDARY_FOLDER = RAW_BOUNDARIES / "eng_output_areas_2021"
WAL_LSOA2011_BOUNDARY_PATH = RAW_BOUNDARIES / "wal_lsoa_2011/lsoa_wales_2011.gpkg"
SCOT_DZ_BOUNDARY_PATH = RAW_BOUNDARIES / "scot_data_zones_2011/SG_DataZone_Bdry_2011.shp"

DEPRIVATION_AREAS_PATH = PROCESSED_CONTEXT / "deprivation_areas_gb.parquet"
LINK_DEPRIVATION_PATH = PROCESSED_CONTEXT / "link_deprivation_gb.parquet"
DEPRIVATION_PROV_PATH = PROVENANCE / "deprivation_gb_provenance.json"

DEPRIVATION_FALLBACK_M = 250
BNG = "EPSG:27700"

ENG_LSOA_COL = "LSOA code (2021)"
ENG_OVERALL_DECILE_COL = (
    "Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"
)
ENG_INCOME_DECILE_COL = "Income Decile (where 1 is most deprived 10% of LSOAs)"
ENG_EMPLOYMENT_DECILE_COL = "Employment Decile (where 1 is most deprived 10% of LSOAs)"

SHARED_DECILE_COLS = [
    "overall_decile_within_country",
    "income_decile_within_country",
    "employment_decile_within_country",
]
AREA_COLUMNS = [
    "deprivation_area_code",
    "deprivation_area_type",
    "deprivation_country",
    "deprivation_source",
    "deprivation_year",
    *SHARED_DECILE_COLS,
    "geometry",
]
LINK_COLUMNS = [
    "link_id",
    "deprivation_area_code",
    "deprivation_area_type",
    "deprivation_country",
    "deprivation_source",
    "deprivation_assignment_method",
    "deprivation_assignment_distance_m",
    *SHARED_DECILE_COLS,
    "deprivation_country_england",
    "deprivation_country_wales",
    "deprivation_country_scotland",
]


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


def _find_ew_oa_boundary(path: Path | None = None) -> Path:
    if path is not None:
        return Path(path)

    matches = sorted(EW_OA_BOUNDARY_FOLDER.glob("Output_Areas_2021_EW_BGC_V2_*.gpkg"))
    if not matches:
        raise FileNotFoundError(
            "England/Wales OA boundary file not found. Expected a file like:\n"
            f"  {EW_OA_BOUNDARY_FOLDER / 'Output_Areas_2021_EW_BGC_V2_*.gpkg'}"
        )
    if len(matches) > 1:
        logger.info("Multiple E/W OA boundary files found; using %s", matches[0].name)
    return matches[0]


def _assert_unique(df: pd.DataFrame, col: str, label: str) -> None:
    dupes = df.loc[df[col].duplicated(), col].dropna().astype(str).head().tolist()
    if dupes:
        raise ValueError(f"{label} contains duplicate {col} values; sample: {dupes}")


def _rank_to_decile(rank: pd.Series, n: int) -> pd.Series:
    numeric = pd.to_numeric(rank, errors="coerce")
    decile = np.ceil(numeric * 10 / n).clip(lower=1, upper=10)
    return decile.astype("Int8")


def _to_int8_decile(series: pd.Series, label: str) -> pd.Series:
    decile = pd.to_numeric(series, errors="coerce")
    bad = decile.notna() & ~decile.between(1, 10)
    if bad.any():
        raise ValueError(f"{label} contains deciles outside 1..10; sample: {decile[bad].head()}")
    return decile.astype("Int8")


def _read_ods_table(path: Path, table_name: str) -> list[list[str]]:
    ns = {
        "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
        "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
        "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    }
    table_name_key = f"{{{ns['table']}}}name"
    repeat_cols_key = f"{{{ns['table']}}}number-columns-repeated"
    repeat_rows_key = f"{{{ns['table']}}}number-rows-repeated"

    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("content.xml"))

    for table in root.findall(".//table:table", ns):
        if table.attrib.get(table_name_key) != table_name:
            continue

        rows: list[list[str]] = []
        for row in table.findall("table:table-row", ns):
            row_repeat = int(row.attrib.get(repeat_rows_key, "1"))
            values: list[str] = []
            for cell in row.findall("table:table-cell", ns):
                col_repeat = int(cell.attrib.get(repeat_cols_key, "1"))
                text = " ".join(
                    "".join(paragraph.itertext()) for paragraph in cell.findall("text:p", ns)
                ).strip()
                values.extend([text] * min(col_repeat, 100))
            for _ in range(min(row_repeat, 100)):
                rows.append(values)
        return rows

    raise ValueError(f"Table {table_name!r} not found in {path}")


def _build_lsoa2021_boundaries(ew_oa_boundary_path: Path | None = None) -> gpd.GeoDataFrame:
    boundary_path = _find_ew_oa_boundary(ew_oa_boundary_path)
    oa = gpd.read_file(boundary_path, columns=["LSOA21CD", "geometry"]).to_crs(BNG)
    if "LSOA21CD" not in oa.columns:
        raise ValueError(f"{boundary_path} is missing LSOA21CD")

    oa["LSOA21CD"] = oa["LSOA21CD"].astype("string").str.strip()
    lsoa = oa.dissolve(by="LSOA21CD", as_index=False)
    lsoa = lsoa.rename(columns={"LSOA21CD": "deprivation_area_code"})
    lsoa["deprivation_area_code"] = lsoa["deprivation_area_code"].astype("string").str.strip()
    _assert_unique(lsoa, "deprivation_area_code", "E/W LSOA2021 boundary")
    return lsoa[["deprivation_area_code", "geometry"]]


def _load_wales_lsoa2011_boundary(
    boundary_path: Path = WAL_LSOA2011_BOUNDARY_PATH,
) -> gpd.GeoDataFrame:
    """Load Welsh LSOA 2011 polygons for WIMD 2019."""
    if not boundary_path.exists():
        raise FileNotFoundError(f"Wales LSOA 2011 boundary file not found: {boundary_path}")

    boundary = gpd.read_file(boundary_path).to_crs(BNG)
    if "LSOA11Code" not in boundary.columns:
        raise ValueError(f"{boundary_path} is missing LSOA11Code")

    boundary = boundary[["LSOA11Code", "geometry"]].rename(
        columns={"LSOA11Code": "deprivation_area_code"}
    )
    boundary["deprivation_area_code"] = (
        boundary["deprivation_area_code"].astype("string").str.strip()
    )
    if not boundary["deprivation_area_code"].str.startswith("W").all():
        raise ValueError("Wales LSOA 2011 boundary contains non-W LSOA codes")
    _assert_unique(boundary, "deprivation_area_code", "Wales LSOA 2011 boundary")
    return boundary[["deprivation_area_code", "geometry"]]


def load_england_iod(path: Path = ENG_IOD_PATH) -> pd.DataFrame:
    """Load England IoD 2025 at LSOA 2021 grain."""
    if not path.exists():
        raise FileNotFoundError(f"England IoD file not found: {path}")

    required = [
        ENG_LSOA_COL,
        ENG_OVERALL_DECILE_COL,
        ENG_INCOME_DECILE_COL,
        ENG_EMPLOYMENT_DECILE_COL,
    ]
    header = pd.read_csv(path, nrows=0, encoding="utf-8-sig").columns
    missing = [col for col in required if col not in header]
    if missing:
        raise ValueError(f"{path} is missing required columns: {missing}")

    df = pd.read_csv(path, usecols=required, encoding="utf-8-sig").rename(
        columns={
            ENG_LSOA_COL: "deprivation_area_code",
            ENG_OVERALL_DECILE_COL: "overall_decile_within_country",
            ENG_INCOME_DECILE_COL: "income_decile_within_country",
            ENG_EMPLOYMENT_DECILE_COL: "employment_decile_within_country",
        }
    )
    df["deprivation_area_code"] = df["deprivation_area_code"].astype("string").str.strip()
    if not df["deprivation_area_code"].str.startswith("E").all():
        raise ValueError("England IoD contains non-E LSOA codes")
    _assert_unique(df, "deprivation_area_code", "England IoD")
    for col in SHARED_DECILE_COLS:
        df[col] = _to_int8_decile(df[col], col)
    df["deprivation_area_type"] = "LSOA2021"
    df["deprivation_country"] = "England"
    df["deprivation_source"] = "IoD 2025"
    df["deprivation_year"] = 2025
    return df[
        [
            "deprivation_area_code",
            "deprivation_area_type",
            "deprivation_country",
            "deprivation_source",
            "deprivation_year",
            *SHARED_DECILE_COLS,
        ]
    ]


def load_wales_wimd(path: Path = WAL_WIMD_PATH) -> pd.DataFrame:
    """Load Wales WIMD 2019 ranks and convert them to within-Wales deciles."""
    if not path.exists():
        raise FileNotFoundError(f"Wales WIMD file not found: {path}")

    rows = _read_ods_table(path, "WIMD_2019_ranks")
    header_idx = next(i for i, row in enumerate(rows) if row and row[0] == "LSOA code")
    header = rows[header_idx]
    data_rows = [row for row in rows[header_idx + 1 :] if row and row[0].startswith("W")]
    df = pd.DataFrame(data_rows, columns=header[: len(data_rows[0])])
    required = ["LSOA code", "WIMD 2019", "Income", "Employment"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{path} WIMD_2019_ranks is missing required columns: {missing}")

    result = df[required].rename(columns={"LSOA code": "deprivation_area_code"}).copy()
    result["deprivation_area_code"] = result["deprivation_area_code"].astype("string").str.strip()
    _assert_unique(result, "deprivation_area_code", "Wales WIMD")
    n = len(result)
    result["overall_decile_within_country"] = _rank_to_decile(result["WIMD 2019"], n)
    result["income_decile_within_country"] = _rank_to_decile(result["Income"], n)
    result["employment_decile_within_country"] = _rank_to_decile(result["Employment"], n)
    result["deprivation_area_type"] = "LSOA2011"
    result["deprivation_country"] = "Wales"
    result["deprivation_source"] = "WIMD 2019"
    result["deprivation_year"] = 2019
    return result[
        [
            "deprivation_area_code",
            "deprivation_area_type",
            "deprivation_country",
            "deprivation_source",
            "deprivation_year",
            *SHARED_DECILE_COLS,
        ]
    ]


def load_scotland_simd(path: Path = SCOT_SIMD_PATH) -> pd.DataFrame:
    """Load Scotland SIMD2020v2 at 2011 Data Zone grain."""
    if not path.exists():
        raise FileNotFoundError(f"Scotland SIMD file not found: {path}")

    df = pd.read_excel(path, sheet_name="SIMD 2020v2 DZ lookup data")
    required = [
        "DZ",
        "SIMD2020v2_Decile",
        "SIMD2020v2_Income_Domain_Rank",
        "SIMD2020_Employment_Domain_Rank",
    ]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{path} is missing required columns: {missing}")

    result = df[required].rename(
        columns={
            "DZ": "deprivation_area_code",
            "SIMD2020v2_Decile": "overall_decile_within_country",
        }
    )
    result["deprivation_area_code"] = result["deprivation_area_code"].astype("string").str.strip()
    if not result["deprivation_area_code"].str.startswith("S010").all():
        raise ValueError("Scotland SIMD contains non-S010 data-zone codes")
    _assert_unique(result, "deprivation_area_code", "Scotland SIMD")
    n = len(result)
    result["overall_decile_within_country"] = _to_int8_decile(
        result["overall_decile_within_country"],
        "Scotland SIMD overall decile",
    )
    result["income_decile_within_country"] = _rank_to_decile(
        result["SIMD2020v2_Income_Domain_Rank"],
        n,
    )
    result["employment_decile_within_country"] = _rank_to_decile(
        result["SIMD2020_Employment_Domain_Rank"],
        n,
    )
    result["deprivation_area_type"] = "DZ2011"
    result["deprivation_country"] = "Scotland"
    result["deprivation_source"] = "SIMD 2020v2"
    result["deprivation_year"] = 2020
    return result[
        [
            "deprivation_area_code",
            "deprivation_area_type",
            "deprivation_country",
            "deprivation_source",
            "deprivation_year",
            *SHARED_DECILE_COLS,
        ]
    ]


def _merge_with_geometry(
    attrs: pd.DataFrame,
    geometry: gpd.GeoDataFrame,
    label: str,
    checks: dict[str, object],
) -> gpd.GeoDataFrame:
    merged = attrs.merge(
        geometry,
        on="deprivation_area_code",
        how="left",
        validate="one_to_one",
    )
    missing_geometry = int(merged["geometry"].isna().sum())
    checks[f"{label}_attribute_rows"] = int(len(attrs))
    checks[f"{label}_rows_missing_geometry"] = missing_geometry
    if missing_geometry:
        logger.warning(
            "%s deprivation lookup has %s / %s rows without available geometry",
            label,
            f"{missing_geometry:,}",
            f"{len(attrs):,}",
        )
    merged = merged.dropna(subset=["geometry"]).copy()
    return gpd.GeoDataFrame(merged, geometry="geometry", crs=BNG)


def build_gb_deprivation_areas(
    output_path: Path = DEPRIVATION_AREAS_PATH,
    ew_oa_boundary_path: Path | None = None,
    wales_boundary_path: Path = WAL_LSOA2011_BOUNDARY_PATH,
    scotland_boundary_path: Path = SCOT_DZ_BOUNDARY_PATH,
) -> gpd.GeoDataFrame:
    """Build the GB deprivation polygon context layer."""
    logger.info("Building GB deprivation area layer")
    checks: dict[str, object] = {}

    lsoa2021 = _build_lsoa2021_boundaries(ew_oa_boundary_path)
    eng_geom = lsoa2021[lsoa2021["deprivation_area_code"].str.startswith("E")].copy()
    checks["england_lsoa2021_boundary_rows"] = int(len(eng_geom))

    england = _merge_with_geometry(load_england_iod(), eng_geom, "england", checks)
    wal_geom = _load_wales_lsoa2011_boundary(wales_boundary_path)
    checks["wales_lsoa2011_boundary_rows"] = int(len(wal_geom))
    wales_attrs = load_wales_wimd()
    wales = _merge_with_geometry(wales_attrs, wal_geom, "wales", checks)
    checks["wales_boundary_rows_without_wimd"] = int(
        len(set(wal_geom["deprivation_area_code"]) - set(wales_attrs["deprivation_area_code"]))
    )

    scot_geom = gpd.read_file(scotland_boundary_path).to_crs(BNG)
    if "DataZone" not in scot_geom.columns:
        raise ValueError(f"{scotland_boundary_path} is missing DataZone")
    scot_geom = scot_geom[["DataZone", "geometry"]].rename(
        columns={"DataZone": "deprivation_area_code"}
    )
    scot_geom["deprivation_area_code"] = (
        scot_geom["deprivation_area_code"].astype("string").str.strip()
    )
    if not scot_geom["deprivation_area_code"].str.startswith("S010").all():
        raise ValueError("Scotland data-zone boundary contains non-S010 codes")
    _assert_unique(scot_geom, "deprivation_area_code", "Scotland data-zone boundary")
    checks["scotland_dz2011_boundary_rows"] = int(len(scot_geom))
    scotland = _merge_with_geometry(load_scotland_simd(), scot_geom, "scotland", checks)

    combined = pd.concat([england, wales, scotland], ignore_index=True)
    gdf = gpd.GeoDataFrame(combined[AREA_COLUMNS], geometry="geometry", crs=BNG)
    if gdf.crs is None or gdf.crs.to_epsg() != 27700:
        gdf = gdf.to_crs(BNG)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_parquet(output_path, index=False)
    logger.info("Wrote GB deprivation areas to %s (%s rows)", output_path, f"{len(gdf):,}")
    write_deprivation_provenance(areas=gdf, area_build_checks=checks)
    return gdf


def assign_deprivation_to_links(
    openroads: gpd.GeoDataFrame,
    areas_path: Path = DEPRIVATION_AREAS_PATH,
    output_path: Path | None = LINK_DEPRIVATION_PATH,
    fallback_m: float = DEPRIVATION_FALLBACK_M,
) -> pd.DataFrame:
    """
    Assign GB deprivation attributes to road links by centroid.

    Primary assignment is road-link centroid within the deprivation polygon.
    Unmatched centroids get a nearest-polygon fallback within fallback_m metres.
    """
    if not areas_path.exists():
        build_gb_deprivation_areas(output_path=areas_path)

    areas = gpd.read_parquet(areas_path).to_crs(BNG)
    roads = openroads[["link_id", "geometry"]].copy().to_crs(BNG)
    road_centroids = gpd.GeoDataFrame(
        roads[["link_id"]],
        geometry=roads.geometry.centroid,
        crs=BNG,
    )

    area_slim = areas[AREA_COLUMNS].copy()
    within = gpd.sjoin(road_centroids, area_slim, how="left", predicate="within")
    matched = within["deprivation_area_code"].notna()
    matched_link_ids = set(within.loc[matched, "link_id"])
    unmatched = road_centroids.loc[~road_centroids["link_id"].isin(matched_link_ids)]

    within = within.loc[matched].copy()
    within["deprivation_assignment_method"] = "within"
    within["deprivation_assignment_distance_m"] = 0.0

    if not unmatched.empty:
        nearest = gpd.sjoin_nearest(
            unmatched,
            area_slim,
            how="left",
            max_distance=fallback_m,
            distance_col="deprivation_assignment_distance_m",
        )
        nearest["deprivation_assignment_method"] = np.where(
            nearest["deprivation_area_code"].notna(),
            "nearest_fallback",
            pd.NA,
        )
    else:
        nearest = gpd.GeoDataFrame(columns=list(within.columns), crs=BNG)

    assigned = within if nearest.empty else pd.concat([within, nearest], ignore_index=True)
    if not assigned.empty:
        assigned = assigned.sort_values(
            ["link_id", "deprivation_assignment_distance_m"], na_position="last"
        ).drop_duplicates(subset="link_id", keep="first")

    result = road_centroids[["link_id"]].merge(
        assigned[
            [
                "link_id",
                "deprivation_area_code",
                "deprivation_area_type",
                "deprivation_country",
                "deprivation_source",
                "deprivation_assignment_method",
                "deprivation_assignment_distance_m",
                *SHARED_DECILE_COLS,
            ]
        ],
        on="link_id",
        how="left",
        validate="one_to_one",
    )
    result["deprivation_assignment_method"] = result["deprivation_assignment_method"].fillna(
        "unmatched"
    )
    country = result["deprivation_country"].astype("string")
    result["deprivation_country_england"] = country.eq("England").fillna(False).astype("int8")
    result["deprivation_country_wales"] = country.eq("Wales").fillna(False).astype("int8")
    result["deprivation_country_scotland"] = country.eq("Scotland").fillna(False).astype("int8")
    result = pd.DataFrame(result.drop(columns="geometry", errors="ignore"))[LINK_COLUMNS]

    logger.info(
        "  Deprivation matched for %s / %s links",
        f"{result['overall_decile_within_country'].notna().sum():,}",
        f"{len(result):,}",
    )
    logger.info(
        "  Deprivation assignment methods: %s",
        result["deprivation_assignment_method"].value_counts(dropna=False).to_dict(),
    )
    n_unmatched = int((result["deprivation_assignment_method"] == "unmatched").sum())
    n_fallback = int((result["deprivation_assignment_method"] == "nearest_fallback").sum())
    if n_unmatched:
        logger.warning(
            "  Deprivation assignment left %s / %s links unmatched",
            f"{n_unmatched:,}",
            f"{len(result):,}",
        )
    if len(result) and n_fallback / len(result) > 0.05:
        logger.warning(
            "  Deprivation assignment used nearest fallback for %.1f%% of links; "
            "check CRS/boundary coverage.",
            100 * n_fallback / len(result),
        )

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result.to_parquet(output_path, index=False)
        logger.info("Wrote link deprivation assignments to %s", output_path)
    return result


def _counts(series: pd.Series) -> dict[str, int]:
    counts = (
        series.astype("object").where(series.notna(), "NaN").value_counts(dropna=False).sort_index()
    )
    return {str(k): int(v) for k, v in counts.items()}


def _decile_distribution_by_country(df: pd.DataFrame, column: str) -> dict[str, dict[str, int]]:
    output: dict[str, dict[str, int]] = {}
    for country, group in df.groupby("deprivation_country", dropna=False):
        output[str(country)] = _counts(group[column])
    return output


def write_deprivation_provenance(
    features: pd.DataFrame | None = None,
    areas: gpd.GeoDataFrame | None = None,
    area_build_checks: dict[str, object] | None = None,
) -> None:
    """Write GB deprivation area and link-assignment provenance."""
    previous: dict[str, object] = {}
    if DEPRIVATION_PROV_PATH.exists():
        try:
            previous = json.loads(DEPRIVATION_PROV_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = {}

    if areas is None and DEPRIVATION_AREAS_PATH.exists():
        areas = gpd.read_parquet(DEPRIVATION_AREAS_PATH)

    provenance: dict[str, object] = {
        "script_path": _repo_path(Path(__file__)),
        "git_sha": _git_sha(),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "warning": (
            "Deciles are within-country relative deprivation measures. "
            "A value of 1 means the most deprived 10% within that country/index, "
            "not the most deprived 10% of Great Britain."
        ),
        "area_output": _repo_path(DEPRIVATION_AREAS_PATH),
        "link_assignment_output": _repo_path(LINK_DEPRIVATION_PATH),
        "fallback_distance_threshold_m": DEPRIVATION_FALLBACK_M,
        "sources": {
            "England": {
                "source": "IoD 2025",
                "source_file": _repo_path(ENG_IOD_PATH),
                "boundary_file": _repo_path(_find_ew_oa_boundary()),
                "geography": "LSOA 2021",
                "year": 2025,
            },
            "Wales": {
                "source": "WIMD 2019",
                "source_file": _repo_path(WAL_WIMD_PATH),
                "boundary_file": _repo_path(WAL_LSOA2011_BOUNDARY_PATH),
                "geography": "LSOA 2011",
                "year": 2019,
            },
            "Scotland": {
                "source": "SIMD 2020v2",
                "source_file": _repo_path(SCOT_SIMD_PATH),
                "boundary_file": _repo_path(SCOT_DZ_BOUNDARY_PATH),
                "geography": "Data Zone 2011",
                "year": 2020,
            },
        },
        "area_build_checks": area_build_checks or previous.get("area_build_checks", {}),
    }

    if areas is not None:
        provenance["area_counts_by_country"] = _counts(areas["deprivation_country"])
        provenance["area_type_counts"] = _counts(areas["deprivation_area_type"])
        provenance["area_decile_distributions_by_country"] = {
            col: _decile_distribution_by_country(areas, col) for col in SHARED_DECILE_COLS
        }

    if features is not None:
        required = {
            "deprivation_country",
            "deprivation_area_type",
            "deprivation_assignment_method",
            "deprivation_assignment_distance_m",
            "overall_decile_within_country",
        }
        missing = required.difference(features.columns)
        if missing:
            logger.warning(
                "Skipping link-level deprivation provenance fields; missing columns: %s",
                sorted(missing),
            )
        else:
            distances = pd.to_numeric(
                features["deprivation_assignment_distance_m"],
                errors="coerce",
            ).dropna()
            provenance["link_assignment"] = {
                "method": (
                    "road-link centroid to deprivation polygon; nearest fallback "
                    "for unmatched centroids"
                ),
                "n_links_total": int(len(features)),
                "n_links_with_deprivation": int(
                    features["overall_decile_within_country"].notna().sum()
                ),
                "assignment_method_counts": _counts(features["deprivation_assignment_method"]),
                "link_counts_by_country": _counts(features["deprivation_country"]),
                "link_area_type_counts": _counts(features["deprivation_area_type"]),
                "unmatched_count": int(
                    (features["deprivation_assignment_method"] == "unmatched").sum()
                ),
                "fallback_distance_m": {
                    "median": float(distances.median()) if not distances.empty else None,
                    "p95": float(distances.quantile(0.95)) if not distances.empty else None,
                    "max": float(distances.max()) if not distances.empty else None,
                },
                "link_decile_distributions_by_country": {
                    col: _decile_distribution_by_country(features, col)
                    for col in SHARED_DECILE_COLS
                    if col in features.columns
                },
            }
        if "link_assignment" not in provenance and "link_assignment" in previous:
            provenance["link_assignment"] = previous["link_assignment"]
    elif "link_assignment" in previous:
        provenance["link_assignment"] = previous["link_assignment"]

    DEPRIVATION_PROV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DEPRIVATION_PROV_PATH, "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)
    logger.info("Wrote deprivation provenance to %s", DEPRIVATION_PROV_PATH)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assign-links", action="store_true", help="Also assign deprivation to links"
    )
    parser.add_argument("--force", action="store_true", help="Rebuild outputs even if they exist")
    args = parser.parse_args()

    if args.force or not DEPRIVATION_AREAS_PATH.exists():
        build_gb_deprivation_areas()
    else:
        logger.info("Deprivation area layer already exists at %s", DEPRIVATION_AREAS_PATH)
        write_deprivation_provenance()

    if args.assign_links:
        openroads = gpd.read_parquet(_ROOT / "data/processed/shapefiles/openroads.parquet")
        assignments = assign_deprivation_to_links(openroads)
        write_deprivation_provenance(features=assignments)


if __name__ == "__main__":
    main()
