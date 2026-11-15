
import pandas as pd

from loglens.ingest.parser import parse_log_line
from loglens.parsing.template_miner import mine_log_templates


sample_logs = [
    "2026-11-15 10:00:00 INFO Auth User 123 logged in",
    "2026-11-15 10:01:00 INFO Auth User 456 logged in",
    "2026-11-15 10:02:00 INFO Auth User 789 logged in",
    "2026-11-15 10:03:00 ERROR Database Connection failed",
    "2026-11-15 10:04:00 ERROR Database Connection failed",
    "2026-11-15 10:05:00 WARNING API Request 100 timed out",
    "2026-11-15 10:06:00 WARNING API Request 200 timed out",
    "2026-11-15 10:07:00 INFO Auth User 321 logged in",
]

parsed = [parse_log_line(line) for line in sample_logs]

assert all(log is not None for log in parsed), "Log parsing failed"

df = pd.DataFrame(parsed)
result = mine_log_templates(df)

assert len(result) == len(sample_logs), "Log count mismatch"
assert result["template_id"].notna().all(), "Missing template IDs"
assert result["template"].notna().all(), "Missing templates"

# All login messages should share one template.
login_ids = result.loc[
    result["component"] == "Auth", "template_id"
]
assert login_ids.nunique() == 1, "Login messages were not grouped"

# Identical database errors should share one template.
database_ids = result.loc[
    result["component"] == "Database", "template_id"
]
assert database_ids.nunique() == 1, "Database errors were not grouped"

print(result[
    ["level", "component", "template_id", "template"]
].to_string(index=False))

print("\nAll template mining checks passed!")
