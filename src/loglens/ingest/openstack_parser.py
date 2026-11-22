
import re
from datetime import datetime

import pandas as pd


OPENSTACK_PATTERN = re.compile(
    r"^(?P<source>\S+)\s+"
    r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+"
    r"(?P<process_id>\d+)\s+"
    r"(?P<level>DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL)\s+"
    r"(?P<component>\S+)\s+"
    r"(?P<message>.*)$"
)


def parse_openstack_line(line):
    """Parse one OpenStack log entry into LogLens fields."""

    match = OPENSTACK_PATTERN.match(line.strip())

    if not match:
        return None

    fields = match.groupdict()

    try:
        timestamp = datetime.fromisoformat(
            f"{fields['date']} {fields['time']}"
        )
    except ValueError:
        return None

    return {
        "timestamp": timestamp,
        "level": fields["level"],
        "component": fields["component"],
        "message": fields["message"],
        "source": fields["source"],
        "process_id": int(fields["process_id"]),
    }


def parse_openstack_file(file_path):
    """Parse OpenStack logs and preserve invalid lines."""

    parsed_logs = []
    failed_logs = []

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="replace",
    ) as file:
        for line_number, line in enumerate(file, start=1):
            parsed = parse_openstack_line(line)

            if parsed is not None:
                parsed["line_number"] = line_number
                parsed_logs.append(parsed)
            else:
                failed_logs.append({
                    "line_number": line_number,
                    "raw_line": line.rstrip("\r\n"),
                })

    return (
        pd.DataFrame(parsed_logs),
        pd.DataFrame(failed_logs),
    )
