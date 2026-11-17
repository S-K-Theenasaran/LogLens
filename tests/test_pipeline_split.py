
import pandas as pd
from loglens.pipeline import split_logs_by_time

logs = pd.DataFrame({
    "timestamp": pd.to_datetime([
        "2026-11-17 10:06:00",
        "2026-11-17 10:01:00",
        "2026-11-17 10:11:00",
        "2026-11-17 10:03:00",
        "2026-11-17 10:07:00",
        "2026-11-17 10:12:00",
    ]),
    "message": ["D", "A", "F", "B", "C", "E"],
})

train_logs, test_logs = split_logs_by_time(
    logs,
    train_ratio=0.6,
    window_size="5min",
)

print("Training logs:")
print(train_logs.to_string(index=False))

print("\nTesting logs:")
print(test_logs.to_string(index=False))

assert train_logs["message"].tolist() == ["A", "B"]
assert test_logs["message"].tolist() == ["D", "C", "F", "E"]

train_windows = set(train_logs["timestamp"].dt.floor("5min"))
test_windows = set(test_logs["timestamp"].dt.floor("5min"))

assert train_windows.isdisjoint(test_windows)
assert train_logs["timestamp"].max() < test_logs["timestamp"].min()

print("\nAll window-safe chronological split checks passed!")
