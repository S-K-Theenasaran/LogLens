
import pandas as pd

from loglens.explainability.explainer import explain_anomalies


def test_explain_anomalies():
    train_features = pd.DataFrame(
        {
            "template_1": [4, 5, 6],
            "template_2": [2, 2, 2],
        }
    )

    timestamps = pd.to_datetime([
        "2026-11-20 13:45:00",
        "2026-11-20 13:50:00",
    ])

    anomaly_results = pd.DataFrame(
        {
            "template_1": [100, 5],
            "template_2": [2, 2],
            "is_anomaly": [1, 0],
            "anomaly_score": [0.8, 0.1],
        },
        index=timestamps,
    )

    explanations = explain_anomalies(
        train_features,
        anomaly_results,
        top_n=1,
    )

    assert len(explanations) == 1
    assert explanations.iloc[0]["feature"] == "template_1"
    assert explanations.iloc[0]["observed_count"] == 100
    assert explanations.iloc[0]["baseline_average"] == 5.0
    assert explanations.iloc[0]["difference"] == 95.0

    print("All anomaly explanation checks passed!")


if __name__ == "__main__":
    test_explain_anomalies()
