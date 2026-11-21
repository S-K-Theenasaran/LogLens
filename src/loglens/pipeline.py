
import pandas as pd

from loglens.ingest.parser import parse_log_file
from loglens.ingest.hdfs_parser import parse_hdfs_file
from loglens.parsing.template_miner import (
    fit_template_miner,
    transform_log_templates,
)
from loglens.features.window_features import build_window_features
from loglens.models.isolation_forest import (
    train_isolation_forest,
    predict_anomalies,
)
from loglens.models.local_outlier_factor import (
    train_lof,
    predict_lof,
)
from loglens.incidents.incident_grouper import group_incidents
from loglens.explainability.explainer import explain_anomalies


def load_and_parse_logs(file_path: str) -> pd.DataFrame:
    """Load a server log file and return valid parsed records."""

    if "HDFS" in str(file_path).upper():
        parsed_logs, failed_logs = parse_hdfs_file(file_path)
    else:
        parsed_logs, failed_logs = parse_log_file(file_path)

    if parsed_logs.empty:
        raise ValueError("No valid log entries found in the file.")

    if not failed_logs.empty:
        print(
            f"Warning: {len(failed_logs)} log lines "
            "could not be parsed."
        )

    return parsed_logs.sort_values("timestamp").reset_index(drop=True)


def split_logs_by_time(
    logs: pd.DataFrame,
    train_ratio: float = 0.8,
    window_size: str = "5min",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split logs chronologically without sharing time windows."""

    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1.")

    if logs.empty:
        raise ValueError("Logs cannot be empty.")

    sorted_logs = logs.sort_values("timestamp").reset_index(drop=True)

    window_ids = sorted_logs["timestamp"].dt.floor(window_size)
    unique_windows = window_ids.drop_duplicates().sort_values()

    if len(unique_windows) < 2:
        raise ValueError("At least two time windows are required.")

    split_index = int(len(unique_windows) * train_ratio)
    split_index = max(
        1,
        min(split_index, len(unique_windows) - 1),
    )

    cutoff = unique_windows.iloc[split_index]

    train_logs = sorted_logs[window_ids < cutoff].copy()
    test_logs = sorted_logs[window_ids >= cutoff].copy()

    return train_logs, test_logs


def run_pipeline(file_path: str) -> dict:
    """Run the LogLens anomaly detection pipeline."""

    # Step 1: Load and split logs chronologically.
    logs = load_and_parse_logs(file_path)

    train_logs, test_logs = split_logs_by_time(
        logs,
        train_ratio=0.8,
        window_size="5min",
    )

    # Step 2: Learn templates from training data only.
    miner = fit_template_miner(train_logs)

    train_logs = transform_log_templates(train_logs, miner)
    test_logs = transform_log_templates(test_logs, miner)

    # Step 3: Build consistent features.
    template_ids = sorted(
        cluster.cluster_id
        for cluster in miner.drain.clusters
    )

    if not template_ids:
        raise ValueError("No log templates were learned.")

    train_features = build_window_features(
        train_logs,
        window_size="5min",
        template_ids=template_ids,
    )

    test_features = build_window_features(
        test_logs,
        window_size="5min",
        template_ids=template_ids,
    )

    if train_features.empty or test_features.empty:
        raise ValueError("Training or testing features are empty.")

    if len(train_features) < 3:
        raise ValueError(
            "At least three training windows are required for LOF."
        )

    # Step 4: Isolation Forest.
    isolation_model = train_isolation_forest(
        train_features,
        contamination=0.05,
        random_state=42,
    )

    isolation_results = predict_anomalies(
        isolation_model,
        test_features,
    )

    # Step 5: Local Outlier Factor.
    lof_model, lof_scaler = train_lof(
        train_features,
        n_neighbors=20,
        contamination=0.05,
    )

    lof_results = predict_lof(
        lof_model,
        lof_scaler,
        test_features,
    )

    # Step 6: Incident grouping.
    isolation_incidents = group_incidents(isolation_results)
    lof_incidents = group_incidents(lof_results)

    # Step 7: Explain detected anomalies.
    isolation_explanations = explain_anomalies(
        train_features,
        isolation_results,
    )

    lof_explanations = explain_anomalies(
        train_features,
        lof_results,
    )

    # Step 8: Return results.
    return {
        "train_logs": train_logs,
        "test_logs": test_logs,
        "train_features": train_features,
        "test_features": test_features,
        "isolation_results": isolation_results,
        "lof_results": lof_results,
        "isolation_incidents": isolation_incidents,
        "lof_incidents": lof_incidents,
        "isolation_explanations": isolation_explanations,
        "lof_explanations": lof_explanations,
    }
