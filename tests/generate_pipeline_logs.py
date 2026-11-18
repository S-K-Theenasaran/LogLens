
from datetime import datetime, timedelta
from pathlib import Path
import random

random.seed(42)

output = Path("data/pipeline_test.log")
output.parent.mkdir(parents=True, exist_ok=True)

start = datetime(2026, 11, 18, 10, 0)
lines = []

for window in range(50):
    window_start = start + timedelta(minutes=5 * window)

    # Simulate normal activity in each five-minute window.
    count = random.randint(8, 15)

    # Inject unusual activity into the final test windows.
    if window in (45, 48):
        count = 100

    for i in range(count):
        timestamp = window_start + timedelta(seconds=i * 2)

        message = random.choice([
            "User 123 logged in",
            "User 456 logged in",
            "Database connection successful",
            "Request completed",
        ])

        lines.append(
            f"{timestamp:%Y-%m-%d %H:%M:%S} "
            f"INFO Server {message}\n"
        )

output.write_text("".join(lines), encoding="utf-8")

print(f"Created {output} with {len(lines)} log entries.")
