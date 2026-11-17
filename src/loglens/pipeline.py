
import pandas as pd

from loglens.ingest.parser import parse_log_file
from loglens.parsing.template_miner import mine_log_templates
from loglens.features.window_features import build_window_features

from loglens.models.isolation_forest import (
    train_isolation_forest,
    predict_anomalies,
)

from loglens.models.local_outlier_factor import (
    train_lof,
    predict_lof,
)

def load_and_parse_logs(file_path: str) -> pd.DataFrame:
    """Load a server log file and return valid parsed records."""

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
    split_index = max(1, min(split_index, len(unique_windows) - 1))

    cutoff = unique_windows.iloc[split_index]

    train_logs = sorted_logs[window_ids < cutoff].copy()
    test_logs = sorted_logs[window_ids >= cutoff].copy()

    return train_logs, test_logs
