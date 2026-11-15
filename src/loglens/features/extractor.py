
import pandas as pd


def extract_log_features(logs: pd.DataFrame) -> pd.DataFrame:
    """Extract numerical features from parsed and templated logs."""

    required = {"timestamp", "level", "component", "template_id"}

    missing = required - set(logs.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    results = logs.copy()

    results["timestamp"] = pd.to_datetime(
        results["timestamp"], errors="raise"
    )

    # Basic numerical features
    results["hour"] = results["timestamp"].dt.hour
    results["minute"] = results["timestamp"].dt.minute

    # Log severity indicators
    results["is_error"] = results["level"].isin(
        ["ERROR", "CRITICAL"]
    ).astype(int)

    results["is_warning"] = results["level"].isin(
        ["WARNING", "WARN"]
    ).astype(int)

    # Message template frequency within this batch
    results["template_frequency"] = (
        results.groupby("template_id")["template_id"]
        .transform("size")
    )

    # Component frequency within this batch
    results["component_frequency"] = (
        results.groupby("component")["component"]
        .transform("size")
    )

    return results
