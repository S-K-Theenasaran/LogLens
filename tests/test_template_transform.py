
import pandas as pd

from loglens.parsing.template_miner import (
    fit_template_miner,
    transform_log_templates,
)

train_logs = pd.DataFrame({
    "message": [
        "User 123 logged in",
        "User 456 logged in",
        "User 789 logged in",
    ]
})

test_logs = pd.DataFrame({
    "message": [
        "User 999 logged in",
        "Database connection failed",
    ]
})

miner = fit_template_miner(train_logs)
cluster_count_before = len(miner.drain.clusters)

results = transform_log_templates(test_logs, miner)

print(results.to_string(index=False))

assert results.iloc[0]["template_id"] is not None
assert pd.isna(results.iloc[1]["template_id"])
assert len(miner.drain.clusters) == cluster_count_before

print("\nTraining-only template matching checks passed!")
