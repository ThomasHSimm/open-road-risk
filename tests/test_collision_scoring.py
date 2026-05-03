import numpy as np
import pandas as pd

from road_risk.model.collision import score_collision_models


class FakeGlmResult:
    _road_risk_imputed_features = {}
    _road_risk_missing_features = {}

    def predict(self, x, offset):
        return np.exp(offset.to_numpy()) + x["road_class_ord"].to_numpy()


class FakeXgbModel:
    def predict(self, x, base_margin):
        return np.exp(base_margin) + x["estimated_aadt"].to_numpy() / 10_000


def test_score_collision_models_documents_and_applies_input_mutation():
    df = pd.DataFrame(
        {
            "link_id": ["a", "a", "b", "b"],
            "year": [2020, 2021, 2020, 2021],
            "collision_count": [1, 0, 0, 2],
            "fatal_count": [0, 0, 0, 1],
            "serious_count": [1, 0, 0, 0],
            "estimated_aadt": [1_000.0, 1_200.0, 2_000.0, 2_200.0],
            "log_offset": np.log([0.5, 0.6, 1.0, 1.1]),
            "road_class_ord": [1, 1, 2, 2],
            "road_classification": ["A Road", "A Road", "B Road", "B Road"],
        }
    )

    pooled = score_collision_models(
        FakeGlmResult(),
        FakeXgbModel(),
        ["road_class_ord"],
        ["estimated_aadt"],
        df,
    )

    assert {"predicted_glm", "predicted_xgb"}.issubset(df.columns)
    np.testing.assert_allclose(df["predicted_glm"], [1.5, 1.6, 3.0, 3.1])
    np.testing.assert_allclose(df["predicted_xgb"], [0.6, 0.72, 1.2, 1.32])

    assert pooled["link_id"].tolist() == ["a", "b"]
    assert pooled["collision_count"].tolist() == [1, 2]
    assert pooled["fatal_count"].tolist() == [0, 1]
    assert pooled["serious_count"].tolist() == [1, 0]
    np.testing.assert_allclose(pooled["predicted_glm"], [1.55, 3.05])
    np.testing.assert_allclose(pooled["predicted_xgb"], [0.66, 1.26])
    np.testing.assert_allclose(pooled["residual_glm"], [-2.1, -4.1])
    assert pooled.loc[pooled["link_id"] == "b", "risk_percentile"].iloc[0] == 100.0
