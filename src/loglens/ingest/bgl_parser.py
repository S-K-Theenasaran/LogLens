
from datetime import datetime, timezone

import pandas as pd


def parse_bgl_line(line):
    """Parse one BGL log line, preserving its ground-truth label."""
    parts = line.strip().split(maxsplit=9)

    if len(parts) < 10:
        return None

    label, unix_time, date, node, full_time, location, source, component, level, message = parts

    try:
        timestamp = datetime.fromtimestamp(
            int(unix_time), tz=timezone.utc
        ).replace(tzinfo=None)
    except (ValueError, OverflowError, OSError):
        return None

    return {
        "timestamp": timestamp,
        "level": level,
        "component": component,
        "message": message,
        "is_anomaly": label != "-",
        "anomaly_label": label,
    }


def parse_bgl_file(file_path):
    """Parse BGL logs and preserve invalid lines."""
    parsed_logs = []
    failed_logs = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            parsed = parse_bgl_line(line)

            if parsed is not None:
                parsed["line_number"] = line_number
                parsed_logs.append(parsed)
            else:
                failed_logs.append({
                    "line_number": line_number,
                    "raw_line": line.rstrip("\r\n"),
                })

    return pd.DataFrame(parsed_logs), pd.DataFrame(failed_logs)
