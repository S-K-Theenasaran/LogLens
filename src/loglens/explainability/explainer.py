import pandas as pd


def explain_anomalies(
    train_features: pd.DataFrame,
    anomaly_results: pd.DataFrame,
    top_n: int = 3,
) -> pd.DataFrame:
    """
    Explain anomalous windows by comparing their
    template counts against training averages.
    """

    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    if "is_anomaly" not in anomaly_results.columns:
        raise ValueError("Missing is_anomaly column.")

    feature_columns = list(train_features.columns)

    missing = set(feature_columns) - set(anomaly_results.columns)
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")

    if train_features.empty:
        raise ValueError("Training features cannot be empty.")

    baseline = train_features[feature_columns].mean()

    explanations = []

    anomalies = anomaly_results[
        anomaly_results["is_anomaly"] == 1
    ]

    for timestamp, row in anomalies.iterrows():
        differences = (
            row[feature_columns] - baseline
        ).abs().sort_values(ascending=False)

        for feature in differences.head(top_n).index:
            actual = float(row[feature])
            expected = float(baseline[feature])

            explanations.append({
                "timestamp": timestamp,
                "feature": feature,
                "observed_count": actual,
                "baseline_average": round(expected, 2),
                "difference": round(actual - expected, 2),
                "explanation": (
                    f"{feature}: observed {actual:g} "
                    f"versus training average {expected:.2f}"
                ),
            })

    return pd.DataFrame(
        explanations,
        columns=[
            "timestamp",
            "feature",
            "observed_count",
            "baseline_average",
            "difference",
            "explanation",
        ],
    )