
import re
from datetime import datetime

import pandas as pd


HDFS_PATTERN = re.compile(
    r"^(?P<date>\d{6})\s+"
    r"(?P<time>\d{6})\s+"
    r"(?P<process_id>\d+)\s+"
    r"(?P<level>INFO|WARN|WARNING|ERROR|DEBUG|FATAL)\s+"
    r"(?P<component>\S+):\s*"
    r"(?P<message>.*)$"
)


def parse_hdfs_line(line):
    """Convert an HDFS log line into LogLens fields."""
    match = HDFS_PATTERN.match(line.strip())

    if not match:
        return None

    fields = match.groupdict()

    try:
        timestamp = datetime.strptime(
            fields["date"] + fields["time"],
            "%y%m%d%H%M%S"
        )
    except ValueError:
        return None

    return {
        "timestamp": timestamp,
        "level": fields["level"],
        "component": fields["component"],
        "message": fields["message"],
    }


def parse_hdfs_file(file_path):
    """Parse HDFS logs and preserve invalid lines."""
    parsed_logs = []
    failed_logs = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            parsed = parse_hdfs_line(line)

            if parsed is not None:
                parsed["line_number"] = line_number
                parsed_logs.append(parsed)
            else:
                failed_logs.append({
                    "line_number": line_number,
                    "raw_line": line.rstrip("\r\n"),
                })

    return pd.DataFrame(parsed_logs), pd.DataFrame(failed_logs)
