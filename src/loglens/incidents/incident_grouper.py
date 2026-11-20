import pandas as pd


def group_incidents(
    anomaly_results: pd.DataFrame,
    max_gap: str = "5min"
) -> pd.DataFrame:
    """
    Group consecutive anomalous time windows into incidents.

    Each incident receives a unique ID, start time,
    end time, number of anomalous windows, and peak score.
    """

    required_columns = {"is_anomaly", "anomaly_score"}
    missing = required_columns - set(anomaly_results.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    anomalies = anomaly_results[
        anomaly_results["is_anomaly"] == 1
    ].copy()

    if anomalies.empty:
        return pd.DataFrame(
            columns=[
                "incident_id",
                "start_time",
                "end_time",
                "anomaly_windows",
                "peak_anomaly_score",
            ]
        )

    anomalies = anomalies.sort_index()

    max_gap = pd.Timedelta(max_gap)
    incidents = []
    current_group = []

    for timestamp, row in anomalies.iterrows():
        if current_group:
            previous_time = current_group[-1][0]

            if timestamp - previous_time > max_gap:
                incidents.append(current_group)
                current_group = []

        current_group.append((timestamp, row))

    if current_group:
        incidents.append(current_group)

    summaries = []

    for incident_number, group in enumerate(incidents, start=1):
        summaries.append(
            {
                "incident_id": incident_number,
                "start_time": group[0][0],
                "end_time": group[-1][0],
                "anomaly_windows": len(group),
                "peak_anomaly_score": max(
                    row["anomaly_score"] for _, row in group
                ),
            }
        )

    return pd.DataFrame(summaries)