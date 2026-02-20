from datetime import datetime

import pytest

from traffic_counter.models import TrafficRecord


@pytest.fixture
def sample_records() -> list[TrafficRecord]:
    return [
        TrafficRecord(datetime(2021, 12, 1, 5, 0), 5),
        TrafficRecord(datetime(2021, 12, 1, 5, 30), 12),
        TrafficRecord(datetime(2021, 12, 1, 6, 0), 14),
        TrafficRecord(datetime(2021, 12, 1, 6, 30), 15),
        TrafficRecord(datetime(2021, 12, 1, 7, 0), 25),
        TrafficRecord(datetime(2021, 12, 1, 7, 30), 46),
        TrafficRecord(datetime(2021, 12, 1, 8, 0), 42),
        TrafficRecord(datetime(2021, 12, 1, 15, 0), 9),
        TrafficRecord(datetime(2021, 12, 1, 15, 30), 11),
        TrafficRecord(datetime(2021, 12, 1, 23, 30), 0),
        TrafficRecord(datetime(2021, 12, 5, 9, 30), 18),
        TrafficRecord(datetime(2021, 12, 5, 10, 30), 15),
        TrafficRecord(datetime(2021, 12, 5, 11, 30), 7),
        TrafficRecord(datetime(2021, 12, 5, 14, 0), 6),
        TrafficRecord(datetime(2021, 12, 5, 15, 30), 9),
        TrafficRecord(datetime(2021, 12, 5, 16, 0), 11),
        TrafficRecord(datetime(2021, 12, 5, 16, 30), 15),
        TrafficRecord(datetime(2021, 12, 8, 17, 0), 33),
        TrafficRecord(datetime(2021, 12, 8, 17, 30), 25),
        TrafficRecord(datetime(2021, 12, 8, 18, 0), 33),
        TrafficRecord(datetime(2021, 12, 8, 18, 30), 21),
        TrafficRecord(datetime(2021, 12, 8, 19, 0), 22),
        TrafficRecord(datetime(2021, 12, 9, 0, 0), 4),
    ]


@pytest.fixture
def sample_file(tmp_path):
    content = (
        "2021-12-01T05:00:00 5\n"
        "2021-12-01T05:30:00 12\n"
        "2021-12-01T06:00:00 14\n"
    )
    path = tmp_path / "test_data.txt"
    path.write_text(content)
    return path
