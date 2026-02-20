from datetime import datetime

from traffic_counter.analysis import (
    daily_counts,
    least_traffic_period,
    top_half_hours,
    total_count,
)
from traffic_counter.models import TrafficRecord


class TestTotalCount:
    def test_sample_data(self, sample_records):
        assert total_count(sample_records) == 398

    def test_empty(self):
        assert total_count([]) == 0


class TestDailyCounts:
    def test_sample_data(self, sample_records):
        result = daily_counts(sample_records)
        assert result == [
            ("2021-12-01", 179),
            ("2021-12-05", 81),
            ("2021-12-08", 134),
            ("2021-12-09", 4),
        ]

    def test_empty(self):
        assert daily_counts([]) == []


class TestTopHalfHours:
    def test_sample_data(self, sample_records):
        result = top_half_hours(sample_records)
        assert len(result) == 3
        assert result[0].count == 46
        assert result[1].count == 42
        assert result[2].count == 33

    def test_empty(self):
        assert top_half_hours([]) == []

    def test_fewer_than_n(self):
        records = [TrafficRecord(datetime(2021, 1, 1, 0, 0), 10)]
        assert len(top_half_hours(records)) == 1

    def test_custom_n(self, sample_records):
        result = top_half_hours(sample_records, n=5)
        assert len(result) == 5


class TestLeastTrafficPeriod:
    def test_sample_data(self, sample_records):
        result = least_traffic_period(sample_records)
        assert len(result) == 3
        counts = [r.count for r in result]
        assert counts == [9, 11, 0]

    def test_empty(self):
        assert least_traffic_period([]) == []

    def test_fewer_than_window(self):
        records = [
            TrafficRecord(datetime(2021, 1, 1, 0, 0), 10),
            TrafficRecord(datetime(2021, 1, 1, 0, 30), 20),
        ]
        result = least_traffic_period(records)
        assert len(result) == 2

    def test_custom_window(self, sample_records):
        result = least_traffic_period(sample_records, window=2)
        assert len(result) == 2
