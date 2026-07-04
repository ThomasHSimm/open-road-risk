"""Build the simplified GB reporting-area layer used by the key-figures page.

The reporting-area layer is a display geography only. It is not used by the
model, which remains road-link/link-year based, and it is not a formal
administrative or statistical geography. The dissolve policy below keeps
compact urban and county-style authorities legible on public maps while the
10 km grid remains the primary consistent display geography.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer, datadir

ROOT = Path(__file__).resolve().parents[1]

EW_BOUNDARY = (
    ROOT / "data/raw/boundaries/eng_output_areas_2021/"
    "Output_Areas_2021_EW_BGC_V2_-5587136561181621407.gpkg"
)
EW_LSOA_AREA = ROOT / "data/raw/stats19/lsoa_area.csv"
ENG_IOD = (
    ROOT / "data/raw/imd/eng/File_7_IoD2025_All_Ranks_Scores_Deciles_Population_Denominators.csv"
)
SCOT_BOUNDARY = ROOT / "data/raw/boundaries/scot_output_areas_2022/OutputArea2022_MHW.shp"
SCOT_SIMD = ROOT / "data/raw/imd/scot/SIMD+2020v2+-+datazone+lookup+-+updated+2025.xlsx"
OUTPUT = ROOT / "quarto/outputs/reporting_areas_gb.geojson"
MANIFEST = ROOT / "quarto/outputs/reporting_areas_gb_manifest.json"

# TODO:
# Finalise the explicit GB-wide dissolve policy in DISPLAY_AREA_MERGES_GB and
# keep the output independent of the old partial areas_study.geojson footprint.
# The layer should use one consistent display policy across England, Wales, and
# Scotland.

BNG = "EPSG:27700"
WGS84 = "EPSG:4326"
WEB_SIMPLIFY_M = 100
POLICY_NAME = "gb_display_reporting_area_dissolve_v1"
POLICY_DESCRIPTION = (
    "Simplified GB-wide display geography for key-figure maps. Local authorities "
    "are dissolved into named reporting areas only where compact urban or "
    "county-style groupings improve map legibility. This is not a modelling unit "
    "or a formal reporting/statistical boundary."
)

DISPLAY_AREA_MERGES_GB = {
    "Bedford": "Bedfordshire",
    "Central Bedfordshire": "Bedfordshire",
    "Luton": "Bedfordshire",
    "Burnley": "Lancashire and Blackpool",
    "Chorley": "Lancashire and Blackpool",
    "Fylde": "Lancashire and Blackpool",
    "Hyndburn": "Lancashire and Blackpool",
    "Lancaster": "Lancashire and Blackpool",
    "Pendle": "Lancashire and Blackpool",
    "Preston": "Lancashire and Blackpool",
    "Ribble Valley": "Lancashire and Blackpool",
    "Rossendale": "Lancashire and Blackpool",
    "South Ribble": "Lancashire and Blackpool",
    "West Lancashire": "Lancashire and Blackpool",
    "Wyre": "Lancashire and Blackpool",
    "Blackburn with Darwen": "Lancashire and Blackpool",
    "Blackpool": "Lancashire and Blackpool",
    "Darlington": "Tees Valley",
    "Hartlepool": "Tees Valley",
    "Middlesbrough": "Tees Valley",
    "Redcar and Cleveland": "Tees Valley",
    "Stockton-on-Tees": "Tees Valley",
    "Amber Valley": "Derby and Derbyshire",
    "Bolsover": "Derby and Derbyshire",
    "Chesterfield": "Derby and Derbyshire",
    "Derby": "Derby and Derbyshire",
    "Derbyshire Dales": "Derby and Derbyshire",
    "Erewash": "Derby and Derbyshire",
    "High Peak": "Derby and Derbyshire",
    "North East Derbyshire": "Derby and Derbyshire",
    "South Derbyshire": "Derby and Derbyshire",
    "Kingston upon Hull, City of": "Hull and East Riding",
    "East Riding of Yorkshire": "Hull and East Riding",
    "Blaby": "Leicester, Leicestershire and Rutland",
    "Charnwood": "Leicester, Leicestershire and Rutland",
    "Harborough": "Leicester, Leicestershire and Rutland",
    "Hinckley and Bosworth": "Leicester, Leicestershire and Rutland",
    "Leicester": "Leicester, Leicestershire and Rutland",
    "Melton": "Leicester, Leicestershire and Rutland",
    "North West Leicestershire": "Leicester, Leicestershire and Rutland",
    "Oadby and Wigston": "Leicester, Leicestershire and Rutland",
    "Rutland": "Leicester, Leicestershire and Rutland",
    "Boston": "Greater Lincolnshire",
    "East Lindsey": "Greater Lincolnshire",
    "Lincoln": "Greater Lincolnshire",
    "North Kesteven": "Greater Lincolnshire",
    "North East Lincolnshire": "Greater Lincolnshire",
    "North Lincolnshire": "Greater Lincolnshire",
    "South Holland": "Greater Lincolnshire",
    "South Kesteven": "Greater Lincolnshire",
    "West Lindsey": "Greater Lincolnshire",
    "Ashfield": "Nottingham and Nottinghamshire",
    "Bassetlaw": "Nottingham and Nottinghamshire",
    "Broxtowe": "Nottingham and Nottinghamshire",
    "Gedling": "Nottingham and Nottinghamshire",
    "Mansfield": "Nottingham and Nottinghamshire",
    "Newark and Sherwood": "Nottingham and Nottinghamshire",
    "Nottingham": "Nottingham and Nottinghamshire",
    "Rushcliffe": "Nottingham and Nottinghamshire",
    "Cambridge": "Cambridgeshire and Peterborough",
    "East Cambridgeshire": "Cambridgeshire and Peterborough",
    "Fenland": "Cambridgeshire and Peterborough",
    "Huntingdonshire": "Cambridgeshire and Peterborough",
    "Peterborough": "Cambridgeshire and Peterborough",
    "South Cambridgeshire": "Cambridgeshire and Peterborough",
    "Shropshire": "Shropshire and Telford",
    "Telford and Wrekin": "Shropshire and Telford",
    "Cannock Chase": "Staffordshire and Stoke-on-Trent",
    "East Staffordshire": "Staffordshire and Stoke-on-Trent",
    "Lichfield": "Staffordshire and Stoke-on-Trent",
    "Newcastle-under-Lyme": "Staffordshire and Stoke-on-Trent",
    "South Staffordshire": "Staffordshire and Stoke-on-Trent",
    "Stafford": "Staffordshire and Stoke-on-Trent",
    "Staffordshire Moorlands": "Staffordshire and Stoke-on-Trent",
    "Stoke-on-Trent": "Staffordshire and Stoke-on-Trent",
    "Tamworth": "Staffordshire and Stoke-on-Trent",
    "Cheshire East": "Cheshire and Warrington",
    "Cheshire West and Chester": "Cheshire and Warrington",
    "Halton": "Cheshire and Warrington",
    "Warrington": "Cheshire and Warrington",
    "North Yorkshire": "North Yorkshire and York",
    "York": "North Yorkshire and York",
    "Barking and Dagenham": "Greater London",
    "Barnet": "Greater London",
    "Bexley": "Greater London",
    "Brent": "Greater London",
    "Bromley": "Greater London",
    "Camden": "Greater London",
    "City of London": "Greater London",
    "Croydon": "Greater London",
    "Ealing": "Greater London",
    "Enfield": "Greater London",
    "Greenwich": "Greater London",
    "Hackney": "Greater London",
    "Hammersmith and Fulham": "Greater London",
    "Haringey": "Greater London",
    "Harrow": "Greater London",
    "Havering": "Greater London",
    "Hillingdon": "Greater London",
    "Hounslow": "Greater London",
    "Islington": "Greater London",
    "Kensington and Chelsea": "Greater London",
    "Kingston upon Thames": "Greater London",
    "Lambeth": "Greater London",
    "Lewisham": "Greater London",
    "Merton": "Greater London",
    "Newham": "Greater London",
    "Redbridge": "Greater London",
    "Richmond upon Thames": "Greater London",
    "Southwark": "Greater London",
    "Sutton": "Greater London",
    "Tower Hamlets": "Greater London",
    "Waltham Forest": "Greater London",
    "Wandsworth": "Greater London",
    "Westminster": "Greater London",
    "Bolton": "Greater Manchester",
    "Bury": "Greater Manchester",
    "Manchester": "Greater Manchester",
    "Oldham": "Greater Manchester",
    "Rochdale": "Greater Manchester",
    "Salford": "Greater Manchester",
    "Stockport": "Greater Manchester",
    "Tameside": "Greater Manchester",
    "Trafford": "Greater Manchester",
    "Wigan": "Greater Manchester",
    "Knowsley": "Merseyside",
    "Liverpool": "Merseyside",
    "Sefton": "Merseyside",
    "St. Helens": "Merseyside",
    "Wirral": "Merseyside",
    "Birmingham": "West Midlands",
    "Coventry": "West Midlands",
    "Dudley": "West Midlands",
    "Sandwell": "West Midlands",
    "Solihull": "West Midlands",
    "Walsall": "West Midlands",
    "Wolverhampton": "West Midlands",
    "Bradford": "West Yorkshire",
    "Calderdale": "West Yorkshire",
    "Kirklees": "West Yorkshire",
    "Leeds": "West Yorkshire",
    "Wakefield": "West Yorkshire",
    "Barnsley": "South Yorkshire",
    "Doncaster": "South Yorkshire",
    "Rotherham": "South Yorkshire",
    "Sheffield": "South Yorkshire",
    "Gateshead": "Tyne and Wear",
    "Newcastle upon Tyne": "Tyne and Wear",
    "North Tyneside": "Tyne and Wear",
    "South Tyneside": "Tyne and Wear",
    "Sunderland": "Tyne and Wear",
    "Bath and North East Somerset": "Bristol and West of England",
    "Bristol, City of": "Bristol and West of England",
    "North Somerset": "Bristol and West of England",
    "South Gloucestershire": "Bristol and West of England",
    "East Devon": "Devon, Plymouth and Torbay",
    "Exeter": "Devon, Plymouth and Torbay",
    "Mid Devon": "Devon, Plymouth and Torbay",
    "North Devon": "Devon, Plymouth and Torbay",
    "Plymouth": "Devon, Plymouth and Torbay",
    "South Hams": "Devon, Plymouth and Torbay",
    "Teignbridge": "Devon, Plymouth and Torbay",
    "Torbay": "Devon, Plymouth and Torbay",
    "Torridge": "Devon, Plymouth and Torbay",
    "West Devon": "Devon, Plymouth and Torbay",
    "Bournemouth, Christchurch and Poole": "Dorset and BCP",
    "Dorset": "Dorset and BCP",
    "Ashford": "Kent and Medway",
    "Canterbury": "Kent and Medway",
    "Dartford": "Kent and Medway",
    "Dover": "Kent and Medway",
    "Folkestone and Hythe": "Kent and Medway",
    "Gravesham": "Kent and Medway",
    "Maidstone": "Kent and Medway",
    "Medway": "Kent and Medway",
    "Sevenoaks": "Kent and Medway",
    "Swale": "Kent and Medway",
    "Thanet": "Kent and Medway",
    "Tonbridge and Malling": "Kent and Medway",
    "Tunbridge Wells": "Kent and Medway",
    "Basildon": "Essex, Southend and Thurrock",
    "Braintree": "Essex, Southend and Thurrock",
    "Brentwood": "Essex, Southend and Thurrock",
    "Castle Point": "Essex, Southend and Thurrock",
    "Chelmsford": "Essex, Southend and Thurrock",
    "Colchester": "Essex, Southend and Thurrock",
    "Epping Forest": "Essex, Southend and Thurrock",
    "Harlow": "Essex, Southend and Thurrock",
    "Maldon": "Essex, Southend and Thurrock",
    "Rochford": "Essex, Southend and Thurrock",
    "Southend-on-Sea": "Essex, Southend and Thurrock",
    "Tendring": "Essex, Southend and Thurrock",
    "Thurrock": "Essex, Southend and Thurrock",
    "Uttlesford": "Essex, Southend and Thurrock",
    "Basingstoke and Deane": "Hampshire, Portsmouth and Southampton",
    "East Hampshire": "Hampshire, Portsmouth and Southampton",
    "Eastleigh": "Hampshire, Portsmouth and Southampton",
    "Fareham": "Hampshire, Portsmouth and Southampton",
    "Gosport": "Hampshire, Portsmouth and Southampton",
    "Hart": "Hampshire, Portsmouth and Southampton",
    "Havant": "Hampshire, Portsmouth and Southampton",
    "New Forest": "Hampshire, Portsmouth and Southampton",
    "Portsmouth": "Hampshire, Portsmouth and Southampton",
    "Rushmoor": "Hampshire, Portsmouth and Southampton",
    "Southampton": "Hampshire, Portsmouth and Southampton",
    "Test Valley": "Hampshire, Portsmouth and Southampton",
    "Winchester": "Hampshire, Portsmouth and Southampton",
    "Cumberland": "Cumbria",
    "Westmorland and Furness": "Cumbria",
    "North Northamptonshire": "Northamptonshire",
    "West Northamptonshire": "Northamptonshire",
    "Aberdeen City": "Aberdeen and Aberdeenshire",
    "Aberdeenshire": "Aberdeen and Aberdeenshire",
    "City of Edinburgh": "Edinburgh and Lothians",
    "East Lothian": "Edinburgh and Lothians",
    "Midlothian": "Edinburgh and Lothians",
    "West Lothian": "Edinburgh and Lothians",
    "East Dunbartonshire": "Glasgow City Region",
    "East Renfrewshire": "Glasgow City Region",
    "Glasgow City": "Glasgow City Region",
    "Inverclyde": "Glasgow City Region",
    "North Lanarkshire": "Glasgow City Region",
    "Renfrewshire": "Glasgow City Region",
    "South Lanarkshire": "Glasgow City Region",
    "West Dunbartonshire": "Glasgow City Region",
    "Clackmannanshire": "Forth Valley",
    "Falkirk": "Forth Valley",
    "Stirling": "Forth Valley",
    "Angus": "Tayside",
    "Dundee City": "Tayside",
    "Perth and Kinross": "Tayside",
    "East Ayrshire": "Ayrshire",
    "North Ayrshire": "Ayrshire",
    "South Ayrshire": "Ayrshire",
}


def initialise_pyproj() -> None:
    """Use the conda env PROJ database; env1 otherwise returns inf for EPSG:27700."""
    proj_dir = Path(sys.prefix) / "share/proj"
    if proj_dir.exists():
        datadir.set_data_dir(str(proj_dir))
    sanity = Transformer.from_crs(BNG, WGS84, always_xy=True).transform(400000, 300000)
    if not all(abs(value) < 1_000_000 for value in sanity):
        raise RuntimeError(f"Bad EPSG:27700 transform; got {sanity}")


def build_england_wales_areas() -> gpd.GeoDataFrame:
    ew_oa = gpd.read_file(EW_BOUNDARY, columns=["LSOA21CD", "geometry"]).to_crs(BNG)
    lsoa_area = pd.read_csv(EW_LSOA_AREA, usecols=["LSOA21CD", "LTLA22CD", "LTLA22NM"])
    eng_lookup = pd.read_csv(
        ENG_IOD,
        usecols=[
            "LSOA code (2021)",
            "Local Authority District code (2024)",
            "Local Authority District name (2024)",
        ],
    ).rename(
        columns={
            "LSOA code (2021)": "LSOA21CD",
            "Local Authority District code (2024)": "area_code",
            "Local Authority District name (2024)": "area_name",
        }
    )
    wal_lookup = lsoa_area[lsoa_area["LSOA21CD"].str.startswith("W")].rename(
        columns={"LTLA22CD": "area_code", "LTLA22NM": "area_name"}
    )[["LSOA21CD", "area_code", "area_name"]]
    lookup = pd.concat([eng_lookup, wal_lookup], ignore_index=True)
    lookup["country"] = lookup["area_code"].str[0].map({"E": "England", "W": "Wales"})

    joined = ew_oa.merge(lookup, on="LSOA21CD", how="inner", validate="many_to_one")
    missing = len(ew_oa) - len(joined)
    if missing:
        raise ValueError(f"Missing E/W LSOA lookup rows for {missing:,} output areas")
    return joined.dissolve(by=["area_code", "area_name", "country"], as_index=False)[
        ["area_code", "area_name", "country", "geometry"]
    ]


def build_scotland_areas() -> gpd.GeoDataFrame:
    scot_oa = gpd.read_file(SCOT_BOUNDARY, columns=["council", "geometry"]).to_crs(BNG)
    scot_lookup = pd.read_excel(
        SCOT_SIMD,
        sheet_name="SIMD 2020v2 DZ lookup data",
        usecols=["LAcode", "LAname"],
    )
    scot_lookup = (
        scot_lookup.dropna()
        .drop_duplicates()
        .rename(columns={"LAcode": "area_code", "LAname": "area_name"})
    )
    joined = scot_oa.merge(
        scot_lookup,
        left_on="council",
        right_on="area_code",
        how="left",
        validate="many_to_one",
    )
    missing = joined["area_name"].isna().sum()
    if missing:
        missing_codes = sorted(joined.loc[joined["area_name"].isna(), "council"].dropna().unique())
        raise ValueError(
            f"Missing Scotland council lookup for {missing:,} OAs; codes: {missing_codes}"
        )
    joined["country"] = "Scotland"
    return joined.dissolve(by=["area_code", "area_name", "country"], as_index=False)[
        ["area_code", "area_name", "country", "geometry"]
    ]


def apply_reporting_groups(input_areas: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    input_areas = input_areas.copy()
    missing_group_inputs = sorted(set(DISPLAY_AREA_MERGES_GB) - set(input_areas["area_name"]))
    if missing_group_inputs:
        raise ValueError(f"Reporting group inputs not found: {missing_group_inputs}")
    input_areas["reporting_area"] = (
        input_areas["area_name"].map(DISPLAY_AREA_MERGES_GB).fillna(input_areas["area_name"])
    )
    return input_areas


def dissolve_reporting_areas(input_areas: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    reporting = input_areas.dissolve(
        by="reporting_area",
        as_index=False,
        aggfunc={
            "area_code": lambda s: ";".join(sorted(s.astype(str).unique())),
            "area_name": lambda s: "; ".join(sorted(s.astype(str).unique())),
            "country": lambda s: ";".join(sorted(s.astype(str).unique())),
        },
    )
    reporting = reporting[["area_code", "area_name", "reporting_area", "country", "geometry"]]
    reporting = reporting.to_crs(BNG)
    reporting["geometry"] = reporting.geometry.simplify(WEB_SIMPLIFY_M, preserve_topology=True)
    reporting = reporting.to_crs(WGS84).sort_values("reporting_area").reset_index(drop=True)
    if reporting.geometry.isna().any() or reporting.geometry.is_empty.any():
        raise ValueError("Reporting layer contains null or empty geometries")
    return reporting


def largest_reporting_areas(input_areas: gpd.GeoDataFrame, limit: int = 10) -> str:
    component_counts = (
        input_areas.groupby("reporting_area")["area_code"]
        .nunique()
        .sort_values(ascending=False)
        .head(limit)
    )
    return "; ".join(
        f"{reporting_area}: {count}" for reporting_area, count in component_counts.items()
    )


def write_manifest(input_areas: gpd.GeoDataFrame, reporting: gpd.GeoDataFrame) -> None:
    merged = input_areas[input_areas["area_name"] != input_areas["reporting_area"]]
    merge_members = (
        merged.groupby("reporting_area")["area_name"]
        .apply(lambda values: sorted(values.astype(str).unique()))
        .sort_index()
        .to_dict()
    )
    manifest = {
        "policy_name": POLICY_NAME,
        "policy_description": POLICY_DESCRIPTION,
        "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "output": str(OUTPUT.relative_to(ROOT)),
        "source_authority_count": int(len(input_areas)),
        "reporting_area_count": int(len(reporting)),
        "merged_reporting_area_count": int(len(merge_members)),
        "single_authority_reporting_area_count": int(len(reporting) - len(merge_members)),
        "primary_public_geography": "10 km grid cells generated in key-figures.qmd",
        "display_geography": "Simplified named reporting areas for optional map context",
        "not_used_for": [
            "model fitting",
            "risk-score calculation",
            "validation folds",
            "formal administrative reporting",
        ],
        "merge_members": merge_members,
        "sources": {
            "england_wales_boundary": str(EW_BOUNDARY.relative_to(ROOT)),
            "england_wales_lsoa_lookup": str(EW_LSOA_AREA.relative_to(ROOT)),
            "england_iod_lookup": str(ENG_IOD.relative_to(ROOT)),
            "scotland_boundary": str(SCOT_BOUNDARY.relative_to(ROOT)),
            "scotland_lookup": str(SCOT_SIMD.relative_to(ROOT)),
        },
        "simplification_tolerance_m": WEB_SIMPLIFY_M,
        "crs": WGS84,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def main() -> None:
    initialise_pyproj()
    ew_areas = build_england_wales_areas()
    scot_areas = build_scotland_areas()
    input_areas = gpd.GeoDataFrame(
        pd.concat([ew_areas, scot_areas], ignore_index=True),
        geometry="geometry",
        crs=BNG,
    )
    input_areas = apply_reporting_groups(input_areas)
    reporting = dissolve_reporting_areas(input_areas)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    reporting.to_file(OUTPUT, driver="GeoJSON", coordinate_precision=5)
    write_manifest(input_areas, reporting)

    print(f"policy_name={POLICY_NAME}")
    print(f"source_ew_boundary={EW_BOUNDARY.relative_to(ROOT)}")
    print(f"source_ew_lookup={EW_LSOA_AREA.relative_to(ROOT)}; {ENG_IOD.relative_to(ROOT)}")
    print(f"source_scotland_boundary={SCOT_BOUNDARY.relative_to(ROOT)}")
    print(f"source_scotland_lookup={SCOT_SIMD.relative_to(ROOT)}")
    print(f"input_authority_count={len(input_areas)}")
    print(f"reporting_area_count={len(reporting)}")
    print(f"largest_dissolved_reporting_areas={largest_reporting_areas(input_areas)}")
    print(f"bounds={[float(value) for value in reporting.total_bounds]}")
    print(f"wales_present={bool(reporting['country'].str.contains('Wales', regex=False).any())}")
    print(
        f"scotland_present={bool(reporting['country'].str.contains('Scotland', regex=False).any())}"
    )
    print(f"output={OUTPUT.relative_to(ROOT)}")
    print(f"manifest={MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
