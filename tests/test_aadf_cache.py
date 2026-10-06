"""Guard tests for the AADF ingest cache (stale-subset bug).

The original cache was keyed only on the study-area name, so widening the
configured bbox silently reused a narrower build (filters can only shrink a
cache, never re-add dropped points). These tests pin the fix: the cache key
depends on the bbox/filters, and a narrower-than-configured cache raises.
"""

import json

import pandas as pd
import pytest

from road_risk.config import cfg
from road_risk.ingest.ingest_aadf import (
    STUDY_AREA_NAME,
    _assert_cache_covers_bbox,
    _cache_key,
    _cache_settings,
    load_aadf,
)

FULL_GB = dict(cfg["study_area"]["bbox_wgs84"])
SUBSET = {"min_lat": 52.0, "max_lat": 55.2, "min_lon": -3.4, "max_lon": 1.9}


def test_cache_key_changes_with_bbox_and_filters():
    base = _cache_settings([2024], None, None, None, None, None)
    key = _cache_key(base)
    # Different bbox -> different key (the core of the stale-cache bug).
    wider = {**base, "bbox_wgs84": {**base["bbox_wgs84"], "max_lat": 70.0}}
    assert _cache_key(wider) != key
    # Different lat_bounds / years / directions also change the key.
    assert _cache_key(_cache_settings([2024], (52, 55), None, None, None, None)) != key
    assert _cache_key(_cache_settings([2023], None, None, None, None, None)) != key
    assert _cache_key(_cache_settings([2024], None, None, None, ["N"], None)) != key


def test_assert_cache_covers_bbox_raises_when_smaller():
    # Cache built under the subset bbox, configured for full GB -> raise.
    with pytest.raises(RuntimeError, match="Stale AADF cache"):
        _assert_cache_covers_bbox(SUBSET, FULL_GB, "aadf_filtered_gb_abc.parquet")
    # Cache that covers the configured bbox is fine.
    _assert_cache_covers_bbox(FULL_GB, FULL_GB, "ok.parquet")
    _assert_cache_covers_bbox(FULL_GB, SUBSET, "ok.parquet")


def _write_fake_cache(folder, bbox_in_meta):
    """Place a fake cache + sidecar at the path the current config hashes to."""
    settings = _cache_settings(
        [2024],
        (FULL_GB["min_lat"], FULL_GB["max_lat"]),
        (FULL_GB["min_lon"], FULL_GB["max_lon"]),
        None,
        None,
        None,
    )
    key = _cache_key(settings)
    pq = folder / f"aadf_filtered_{STUDY_AREA_NAME}_{key}.parquet"
    pd.DataFrame(
        {
            "count_point_id": ["1"],
            "year": [2024],
            "latitude": [53.0],
            "longitude": [0.0],
            "direction_of_travel": ["C"],
            "all_motor_vehicles": [1000],
            "all_HGVs": [50],
        }
    ).to_parquet(pq, index=False)
    (pq.with_suffix(".meta.json")).write_text(json.dumps({**settings, "bbox_wgs84": bbox_in_meta}))
    return pq


def test_stale_narrower_cache_raises(tmp_path):
    _write_fake_cache(tmp_path, bbox_in_meta=SUBSET)
    with pytest.raises(RuntimeError, match="Stale AADF cache"):
        load_aadf(
            raw_folder=tmp_path,
            years=[2024],
            lat_bounds=(FULL_GB["min_lat"], FULL_GB["max_lat"]),
            lon_bounds=(FULL_GB["min_lon"], FULL_GB["max_lon"]),
        )


def test_cache_with_covering_bbox_is_reused(tmp_path):
    _write_fake_cache(tmp_path, bbox_in_meta=FULL_GB)
    df = load_aadf(
        raw_folder=tmp_path,
        years=[2024],
        lat_bounds=(FULL_GB["min_lat"], FULL_GB["max_lat"]),
        lon_bounds=(FULL_GB["min_lon"], FULL_GB["max_lon"]),
    )
    assert len(df) == 1 and int(df["year"].iloc[0]) == 2024
