import pandas as pd

from loglens.incidents.incident_grouper import group_incidents


def test_group_incidents():
    timestamps = pd.to_datetime([
        "2026-11-20 13:40:00",
        "2026-11-20 13:45:00",
        "2026-11-20 13:50:00",
        "2026-11-20 14:00:00",
    ])

    results = pd.DataFrame(
        {
            "is_anomaly": [1, 1, 0, 1],
            "anomaly_score": [0.4, 0.8, 0.1, 0.6],
        },
        index=timestamps,
    )

    incidents = group_incidents(results)

    assert len(incidents) == 2
    assert incidents.iloc[0]["anomaly_windows"] == 2
    assert incidents.iloc[0]["peak_anomaly_score"] == 0.8
    assert incidents.iloc[1]["anomaly_windows"] == 1

    print("All incident grouping checks passed!")


if __name__ == "__main__":
    test_group_incidents()