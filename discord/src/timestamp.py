import os
from datetime import datetime, timezone, timedelta

TIMESTAMP_FILE = ".timestamp.txt"
IST = timezone(timedelta(hours=5, minutes=30))


def read_stored_timestamp() -> datetime | None:
    if not os.path.exists(TIMESTAMP_FILE):
        return None
    with open(TIMESTAMP_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return None
        return datetime.fromisoformat(content)


def write_stored_timestamp(timestamp: str):
    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(parsed.isoformat())


def parse_timestamp(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def format_timestamp(timestamp: str) -> str:
    return parse_timestamp(timestamp).astimezone(IST).strftime("%B %d, %Y at %I:%M %p")
