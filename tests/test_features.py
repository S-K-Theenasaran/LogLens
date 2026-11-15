
import pandas as pd

from loglens.ingest.parser import parse_log_line
from loglens.parsing.template_miner import mine_log_templates
from loglens.features.extractor import extract_log_features


sample_logs = [
    "2026-11-15 10:00:00 INFO Auth User 123 logged in",
    "2026-11-15 10:01:00 INFO Auth User 456 logged in",
    "2026-11-15 10:02:00 ERROR Database Connection failed",
    "2026-11-15 10:03:00 WARNING API Request 100 timed out",
    "2026-11-15 10:04:00 WARNING API Request 200 timed out",
]

parsed = [parse_log_line(line) for line in sample_logs]

assert all(log is not None for log in parsed), "Log parsing failed"

df = pd.DataFrame(parsed)
templated = mine_log_templates(df)
features = extract_log_features(templated)

expected_columns = {
    "hour",
    "minute",
    "is_error",
    "is_warning",
    "template_frequency",
    "component_frequency",
}

assert expected_columns.issubset(features.columns)
assert len(features) == len(sample_logs)

# Check error and warning indicators.
assert features["is_error"].tolist() == [0, 0, 1, 0, 0]
assert features["is_warning"].tolist() == [0, 0, 0, 1, 1]

# Check component frequencies.
assert features["component_frequency"].tolist() == [2, 2, 1, 2, 2]

# Check that extracted features contain no missing values.
assert features[list(expected_columns)].notna().all().all()

print(features[
    [
        "component",
        "template_id",
        "hour",
        "minute",
        "is_error",
        "is_warning",
        "template_frequency",
        "component_frequency",
    ]
].to_string(index=False))

print("\nAll feature extraction checks passed!")
