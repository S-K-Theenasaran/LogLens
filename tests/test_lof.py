
import numpy as np
import pandas as pd

from loglens.models.local_outlier_factor import (
    train_lof,
    predict_lof,
)

# Generate reproducible normal server activity.
rng = np.random.default_rng(42)

normal_windows = pd.DataFrame({
    "template_1": rng.poisson(lam=12, size=200),
    "template_2": rng.poisson(lam=3, size=200),
    "template_3": rng.poisson(lam=1, size=200),
})

# Train LOF on normal activity.
model, scaler = train_lof(
    normal_windows,
    n_neighbors=20,
    contamination=0.05,
)

# Test on unseen windows, including an extreme spike.
test_windows = pd.DataFrame({
    "template_1": [11, 12, 10, 150],
    "template_2": [2, 3, 4, 80],
    "template_3": [0, 0, 0, 40],
})

results = predict_lof(model, scaler, test_windows)

print(results.to_string(index=False))

assert len(results) == 4
assert results["is_anomaly"].isin([0, 1]).all()
assert results["anomaly_score"].notna().all()

# The extreme spike should be detected.
assert results["is_anomaly"].iloc[3] == 1, (
    "LOF failed to detect the extreme spike."
)

# The spike should score higher than normal windows.
assert results["anomaly_score"].iloc[3] > (
    results["anomaly_score"].iloc[:3].max()
)

print("\nAll LOF checks passed!")
