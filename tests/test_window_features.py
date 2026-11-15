
import pandas as pd

from loglens.features.window_features import build_window_features


logs = pd.DataFrame({
    "timestamp": [
        "2026-11-15 10:00:00",
        "2026-11-15 10:01:00",
        "2026-11-15 10:04:00",
        "2026-11-15 10:05:00",
        "2026-11-15 10:07:00",
        "2026-11-15 10:09:00",
    ],
    "template_id": [1, 1, 2, 1, 2, 2],
})

features = build_window_features(
    logs,
    window_size="5min",
    template_ids=[1, 2, 3],
)

print(features.to_string())

# Verify that both five-minute windows are present.
assert len(features) == 2, "Expected two time windows"

# Verify the exact template counts.
assert features["template_1"].tolist() == [2, 1]
assert features["template_2"].tolist() == [1, 2]

# Template 3 is absent but must still have a column.
assert features["template_3"].tolist() == [0, 0]

# No missing values are allowed.
assert not features.isna().any().any()

print("\nAll time-window feature checks passed!")
