import math

import geopandas as gpd
import numpy as np
import pandas as pd
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from shapely.geometry import Point

from road_risk.road_terrain import (
    apply_structure_fallback,
    bilinear_sample_band,
    compute_grade_features,
)


def test_bilinear_sample_band_uses_pixel_centres():
    data = np.array([[0.0, 10.0], [20.0, 30.0]], dtype="float32")
    profile = {
        "driver": "GTiff",
        "height": 2,
        "width": 2,
        "count": 1,
        "dtype": "float32",
        "transform": from_origin(0, 2, 1, 1),
    }

    with MemoryFile() as memfile:
        with memfile.open(**profile) as dataset:
            dataset.write(data, 1)
        with memfile.open() as src:
            sampled = bilinear_sample_band(
                src,
                np.array([0.5, 1.0], dtype="float64"),
                np.array([1.5, 1.0], dtype="float64"),
            )

    assert np.allclose(sampled, np.array([0.0, 15.0], dtype="float32"))


def test_compute_grade_features_uses_45m_baseline():
    points = gpd.GeoDataFrame(
        {
            "link_id": ["a"] * 5,
            "point_sequence": [0, 1, 2, 3, 4],
            "distance_m": [0.0, 15.0, 30.0, 45.0, 60.0],
            "elevation_m": [0.0, 1.5, 3.0, 4.5, 6.0],
            "geometry": [Point(x, 0) for x in [0, 15, 30, 45, 60]],
        },
        geometry="geometry",
        crs="EPSG:27700",
    )

    features = compute_grade_features(points, "link_id").set_index("link_id")

    assert math.isclose(features.loc["a", "mean_grade"], 10.0)
    assert math.isclose(features.loc["a", "max_grade"], 10.0)
    assert math.isclose(features.loc["a", "grade_change"], 6.0)
    assert features.loc["a", "valid_grade_segments"] == 2


def test_structure_fallback_replaces_profile_with_endpoint_grade():
    features = pd.DataFrame(
        {
            "link_id": ["a", "b"],
            "mean_grade": [99.0, 3.0],
            "max_grade": [99.0, 4.0],
            "grade_change": [99.0, 5.0],
            "start_elev_m": [100.0, 20.0],
            "end_elev_m": [110.0, 23.0],
            "profile_length_m": [200.0, 100.0],
            "is_bridge_proxy": [True, False],
            "is_tunnel_proxy": [False, False],
            "is_covered_proxy": [False, False],
        }
    )

    out = apply_structure_fallback(features).set_index("link_id")

    assert math.isclose(out.loc["a", "mean_grade"], 5.0)
    assert math.isclose(out.loc["a", "max_grade"], 5.0)
    assert math.isclose(out.loc["a", "grade_change"], 10.0)
    assert out.loc["a", "grade_method"] == "endpoint_fallback"
    assert out.loc["b", "grade_method"] == "profile"
