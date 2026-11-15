
from loglens.ingest.parser import parse_log_line
from loglens.parsing.template_miner import mine_log_templates

import pandas as pd


sample_logs = [
    "2026-11-15 10:00:00 INFO Auth User 123 logged in",
    "2026-11-15 10:01:00 INFO Auth User 456 logged in",
    "2026-11-15 10:02:00 ERROR Database Connection failed",
    "2026-11-15 10:03:00 INFO Auth User 789 logged in",
]

parsed = [parse_log_line(line) for line in sample_logs]

df = pd.DataFrame([log for log in parsed if log is not None])

result = mine_log_templates(df)

print(result[["timestamp", "level", "component", "template_id", "template"]].to_string(index=False))
