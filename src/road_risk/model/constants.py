"""
Shared constants for the model package.
"""

ROAD_CLASS_ORDER = [
    "Motorway",
    "A Road",
    "B Road",
    "Classified Unnumbered",
    "Not Classified",
    "Unclassified",
    "Unknown",
]

ROAD_CLASS_ORDINAL = {
    "Motorway":             6,
    "A Road":               5,
    "B Road":               4,
    "Classified Unnumbered": 3,
    "Not Classified":       2,
    "Unclassified":         1,
    "Unknown":              0,
}

FORM_OF_WAY_ORDER = [
    "Dual Carriageway",
    "Collapsed Dual Carriageway",
    "Motorway",
    "Slip Road",
    "Roundabout",
    "Single Carriageway",
    "Shared Use Carriageway",
    "Guided Busway",
]

FORM_OF_WAY_ORDINAL = {
    "Dual Carriageway":           4,
    "Collapsed Dual Carriageway": 3,
    "Slip Road":                  2,
    "Roundabout":                 2,
    "Single Carriageway":         1,
    "Shared Use Carriageway":     1,
    "Guided Busway":              0,
}

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Duplicated from cfg["years"]["covid"] pending model.yaml migration.
# Keep in sync with config/settings.yaml until then.
COVID_YEARS = {2020, 2021}
RANDOM_STATE = 42