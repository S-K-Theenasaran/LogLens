
import pandas as pd


SEVERITY_LEVELS = (
    "INFO",
    "WARNING",
    "ERROR",
    "SEVERE",
    "FATAL",
    "DEBUG",
)


def build_window_features(
    logs: pd.DataFrame,
    window_size: str = "5min",
    template_ids=None,
    include_empty_windows: bool = True,
) -> pd.DataFrame:
    """Build template and severity counts per time window."""

    required = {"timestamp", "template_id"}
    missing = required - set(logs.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if logs.empty:
        raise ValueError(
            "Cannot build features from empty logs."
        )

    data = logs.copy()
    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="raise",
    )

    if template_ids is None:
        template_ids = sorted(
            data["template_id"].dropna().unique()
        )

    unknown_id = -1

    if unknown_id in template_ids:
        raise ValueError(
            "Unknown template ID conflicts with known IDs."
        )

    data["template_id"] = data["template_id"].fillna(
        unknown_id
    )

    # Count templates in each time window.
    counts = (
        data.groupby(
            [
                pd.Grouper(
                    key="timestamp",
                    freq=window_size,
                ),
                "template_id",
            ]
        )
        .size()
        .unstack(fill_value=0)
    )

    feature_ids = list(template_ids) + [unknown_id]

    counts = counts.reindex(
        columns=feature_ids,
        fill_value=0,
    )

    counts.columns = [
        "unknown_template_count"
        if template_id == unknown_id
        else f"template_{template_id}"
        for template_id in counts.columns
    ]

    # Count log severity levels.
    if "level" in data.columns:
        levels = (
            data["level"]
            .fillna("")
            .astype(str)
            .str.upper()
            .replace({"WARN": "WARNING"})
        )

        severity_data = data[["timestamp"]].copy()
        severity_data["level"] = levels

        severity_counts = (
            severity_data.groupby(
                [
                    pd.Grouper(
                        key="timestamp",
                        freq=window_size,
                    ),
                    "level",
                ]
            )
            .size()
            .unstack(fill_value=0)
        )

        severity_counts = severity_counts.reindex(
            columns=SEVERITY_LEVELS,
            fill_value=0,
        )

        severity_counts.columns = [
            f"level_{level.lower()}_count"
            for level in severity_counts.columns
        ]

        counts = counts.join(
            severity_counts,
            how="left",
        )

    # Include empty time windows if requested.
    if include_empty_windows:
        all_windows = pd.date_range(
            start=data["timestamp"].min().floor(window_size),
            end=data["timestamp"].max().floor(window_size),
            freq=window_size,
        )

        counts = counts.reindex(
            index=all_windows,
            fill_value=0,
        )

    counts = counts.fillna(0)
    counts.index.name = "timestamp"

    return counts.sort_index()
