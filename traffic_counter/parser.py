from datetime import datetime
from pathlib import Path

from traffic_counter.models import TrafficRecord


def parse_line(line: str) -> TrafficRecord:
    timestamp_str, count_str = line.strip().split()
    return TrafficRecord(
        timestamp=datetime.fromisoformat(timestamp_str),
        count=int(count_str),
    )


def parse_file(path: Path) -> list[TrafficRecord]:
    records: list[TrafficRecord] = []
    with open(path) as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                records.append(parse_line(stripped))
    return records
