
import pandas as pd

from loglens.models.isolation_forest import (
    train_isolation_forest,
    predict_anomalies,
)
import numpy as np

# Simulate normal server activity over 200 time windows.



rng = np.random.default_rng(42)

normal_windows = pd.DataFrame({
    "template_1": rng.poisson(lam=12, size=200),
    "template_2": rng.poisson(lam=3, size=200),
    "template_3": rng.poisson(lam=1, size=200),
})


# Train only on normal activity.
model = train_isolation_forest(
    normal_windows,
    contamination=0.05,
)

# Create new windows, including an unusual spike.
test_windows = pd.DataFrame({
    "template_1": [11, 12, 10, 150],
    "template_2": [2, 3, 4, 80],
    "template_3": [0, 0, 0, 40],
})

results = predict_anomalies(model, test_windows)

print(results.to_string(index=False))

assert len(results) == 4
assert "is_anomaly" in results.columns
assert "anomaly_score" in results.columns
assert results["is_anomaly"].isin([0, 1]).all()
assert results["anomaly_score"].notna().all()

print("\nAll Isolation Forest checks passed!")

# Check whether the extreme spike receives a high anomaly score.
normal_scores = results["anomaly_score"].iloc[:3]
spike_score = results["anomaly_score"].iloc[3]

assert spike_score >= normal_scores.max(), (
    "The extreme spike should score at least as unusual "
    "as the normal test windows."
)

print("\nExtreme spike score:", spike_score)
print("Spike scoring check passed!")
