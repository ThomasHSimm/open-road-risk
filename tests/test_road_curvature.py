import math

import numpy as np
from shapely.geometry import LineString, MultiLineString

from road_risk.road_curvature import (
    MAX_CURVATURE_COL,
    MEAN_CURVATURE_COL,
    SINUOSITY_COL,
    normalise_linestring,
    resample_linestring,
    turning_angle_features,
)


def test_straight_line_has_zero_curvature_and_unit_sinuosity():
    features = turning_angle_features(LineString([(0, 0), (30, 0)]), spacing_m=15.0)

    assert features[MEAN_CURVATURE_COL] == 0.0
    assert features[MAX_CURVATURE_COL] == 0.0
    assert features[SINUOSITY_COL] == 1.0


def test_single_right_angle_mean_is_total_turning_per_link_km():
    features = turning_angle_features(LineString([(0, 0), (15, 0), (15, 15)]), spacing_m=15.0)

    assert math.isclose(features[MEAN_CURVATURE_COL], 3000.0)
    assert math.isclose(features[MAX_CURVATURE_COL], 6000.0)
    assert math.isclose(features[SINUOSITY_COL], math.sqrt(2))


def test_sinuosity_is_capped_for_near_closed_links():
    features = turning_angle_features(LineString([(0, 0), (100, 0), (0.1, 0)]), spacing_m=15.0)

    assert features[SINUOSITY_COL] == 5.0


def test_max_curvature_is_capped_for_vertex_artifacts():
    features = turning_angle_features(
        LineString([(0, 0), (0.1, 0), (0.1, 0.1)]),
        spacing_m=15.0,
    )

    assert features[MAX_CURVATURE_COL] == 10_000.0


def test_short_line_is_resampled_with_midpoint():
    points = resample_linestring(LineString([(0, 0), (10, 0)]), spacing_m=15.0)

    assert np.allclose(points, np.array([[0.0, 0.0], [5.0, 0.0], [10.0, 0.0]]))


def test_multilinestring_normalisation_keeps_longest_part_when_disjoint():
    geom = MultiLineString([[(0, 0), (1, 0)], [(10, 0), (13, 0)]])

    normalised = normalise_linestring(geom)

    assert isinstance(normalised, LineString)
    assert math.isclose(normalised.length, 3.0)
