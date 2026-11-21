
import pandas as pd


def build_window_features(
    logs: pd.DataFrame,
    window_size: str = "5min",
    template_ids=None,
) -> pd.DataFrame:
    """Count known and unseen log templates in time windows."""

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

    if template_ids is None:
        template_ids = sorted(
            data["template_id"].dropna().unique()
        )

    # Reserve -1 for unseen templates.
    # Drain3 cluster IDs are positive integers.
    unknown_id = -1

    if unknown_id in template_ids:
        raise ValueError("Unknown template ID conflicts with known IDs.")

    data["template_id"] = data["template_id"].fillna(unknown_id)

    counts = (
        data.groupby(
            [
                pd.Grouper(key="timestamp", freq=window_size),
                "template_id",
            ]
        )
        .size()
        .unstack(fill_value=0)
    )

    # Keep identical columns for training and testing.
    feature_ids = list(template_ids) + [unknown_id]

    counts = counts.reindex(
        columns=feature_ids,
        fill_value=0,
    )

    all_windows = pd.date_range(
        start=data["timestamp"].min().floor(window_size),
        end=data["timestamp"].max().floor(window_size),
        freq=window_size,
    )

    counts = counts.reindex(
        index=all_windows,
        fill_value=0,
    )

    counts.index.name = "timestamp"
    counts.columns = [
        "unknown_template_count" if tid == unknown_id
        else f"template_{tid}"
        for tid in counts.columns
    ]

    return counts.sort_index()
