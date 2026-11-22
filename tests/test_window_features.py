
import pandas as pd
import pytest

from loglens.features.window_features import build_window_features


@pytest.fixture
def sample_logs():
    return pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2026-11-17 10:00:00",
            "2026-11-17 10:01:00",
            "2026-11-17 10:06:00",
        ]),
        "template_id": [1, 1, None],
        "level": ["INFO", "WARNING", "ERROR"],
    })


def test_template_counts(sample_logs):
    features = build_window_features(
        sample_logs,
        window_size="5min",
        template_ids=[1, 2],
    )

    assert len(features) == 2
    assert features["template_1"].tolist() == [2, 0]
    assert features["template_2"].tolist() == [0, 0]


def test_unknown_templates(sample_logs):
    features = build_window_features(
        sample_logs,
        template_ids=[1, 2],
    )

    assert features["unknown_template_count"].tolist() == [0, 1]


def test_severity_counts(sample_logs):
    features = build_window_features(
        sample_logs,
        template_ids=[1, 2],
    )

    assert features["level_info_count"].tolist() == [1, 0]
    assert features["level_warning_count"].tolist() == [1, 0]
    assert features["level_error_count"].tolist() == [0, 1]


def test_empty_windows():
    logs = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2026-11-17 10:00:00",
            "2026-11-17 10:10:00",
        ]),
        "template_id": [1, 1],
    })

    features = build_window_features(
        logs,
        window_size="5min",
        template_ids=[1],
        include_empty_windows=True,
    )

    assert len(features) == 3
    assert features["template_1"].tolist() == [1, 0, 1]


def test_missing_columns():
    logs = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2026-11-17 10:00:00",
        ])
    })

    with pytest.raises(ValueError):
        build_window_features(logs)
