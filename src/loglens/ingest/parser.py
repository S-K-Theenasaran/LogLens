
import re
from datetime import datetime

import pandas as pd


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} "
    r"\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>INFO|WARNING|WARN|ERROR|DEBUG|CRITICAL)\s+"
    r"(?P<component>\S+)\s+"
    r"(?P<message>.*)$"
)


def parse_log_line(line):
    """Parse one server log line into structured fields."""

    match = LOG_PATTERN.match(line.strip())

    if not match:
        return None

    result = match.groupdict()

    try:
        result["timestamp"] = datetime.strptime(
            result["timestamp"], "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return None

    return result


def parse_log_file(file_path):
    """Parse a log file and preserve failed lines."""

    parsed_logs = []
    failed_logs = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            parsed = parse_log_line(line)

            if parsed is not None:
                parsed["line_number"] = line_number
                parsed_logs.append(parsed)
            else:
                failed_logs.append({
                    "line_number": line_number,
                    "raw_line": line.rstrip("\n")
                })

    return pd.DataFrame(parsed_logs), pd.DataFrame(failed_logs)
