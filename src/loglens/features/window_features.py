
import pandas as pd


def build_window_features(
    logs: pd.DataFrame,
    window_size: str = "5min",
    template_ids=None,
) -> pd.DataFrame:
    """Count log templates within fixed time windows."""

    required = {"timestamp", "template_id"}
    missing = required - set(logs.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if logs.empty:
        raise ValueError("Cannot build features from empty logs.")

    data = logs[["timestamp", "template_id"]].copy()
    data["timestamp"] = pd.to_datetime(
        data["timestamp"], errors="raise"
    )

    if data["template_id"].isna().any():
        raise ValueError("Template IDs must not contain missing values.")

    if template_ids is None:
        template_ids = sorted(data["template_id"].unique())

    # Count each template in each time window.
    counts = (
        data.groupby(
            [pd.Grouper(key="timestamp", freq=window_size), "template_id"]
        )
        .size()
        .unstack(fill_value=0)
    )

    # Keep a consistent feature set across datasets.
    counts = counts.reindex(columns=template_ids, fill_value=0)
    counts.columns = [f"template_{tid}" for tid in counts.columns]

    return counts.sort_index()
