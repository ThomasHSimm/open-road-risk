import pandas as pd

from road_risk.features.network import apply_speed_limit_effective_lookup


def test_apply_speed_limit_effective_lookup_covers_all_rules_in_priority_order():
    features = pd.DataFrame(
        {
            "link_id": [f"l{i}" for i in range(1, 11)],
            "speed_limit_mph": pd.array(
                [20, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
                dtype="Int64",
            ),
            "ruc_urban_rural": pd.array(
                [
                    "Urban",
                    "Urban",
                    "Urban",
                    "Urban",
                    "Urban",
                    "Urban",
                    "Rural",
                    "Urban",
                    "Rural",
                    pd.NA,
                ],
                dtype="string",
            ),
        }
    )

    openroads = pd.DataFrame(
        {
            "link_id": [f"l{i}" for i in range(1, 11)],
            "road_classification": [
                "Motorway",
                "Motorway",
                "A Road",
                "A Road",
                "A Road",
                "B Road",
                "B Road",
                "Unclassified",
                "Unknown",
                "Classified Unnumbered",
            ],
            "form_of_way": [
                "Single Carriageway",
                "Single Carriageway",
                "Dual Carriageway",
                "Single Carriageway",
                "Single Carriageway",
                "Single Carriageway",
                "Single Carriageway",
                "Single Carriageway",
                "Single Carriageway",
                "Single Carriageway",
            ],
            "is_trunk": [
                False,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
            ],
        }
    )

    out = apply_speed_limit_effective_lookup(features, openroads).set_index("link_id")

    expected_effective = {
        "l1": 20,
        "l2": 70,
        "l3": 70,
        "l4": 70,
        "l5": 60,
        "l6": 30,
        "l7": 60,
        "l8": 30,
        "l9": 60,
        "l10": pd.NA,
    }
    expected_source = {
        "l1": "osm",
        "l2": "lookup_motorway",
        "l3": "lookup_a_road_dual",
        "l4": "lookup_a_road_trunk",
        "l5": "lookup_a_road_single",
        "l6": "lookup_b_road_urban",
        "l7": "lookup_b_road_rural",
        "l8": "lookup_minor_urban",
        "l9": "lookup_minor_rural",
        "l10": "null_no_ruc",
    }
    expected_imputed = {
        "l1": False,
        "l2": True,
        "l3": True,
        "l4": True,
        "l5": True,
        "l6": True,
        "l7": True,
        "l8": True,
        "l9": True,
        "l10": False,
    }

    for link_id, expected in expected_effective.items():
        actual = out.loc[link_id, "speed_limit_mph_effective"]
        if expected is pd.NA:
            assert pd.isna(actual)
        else:
            assert actual == expected

    assert out["speed_limit_source"].to_dict() == expected_source
    assert out["speed_limit_mph_imputed"].to_dict() == expected_imputed
    assert out.loc["l1", "speed_limit_mph"] == 20
