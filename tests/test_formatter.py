from datetime import datetime

from traffic_counter.formatter import format_daily, format_records, format_report, format_total
from traffic_counter.models import TrafficRecord


class TestFormatTotal:
    def test_format(self):
        assert format_total(398) == "398"


class TestFormatDaily:
    def test_format(self):
        daily = [("2021-12-01", 179), ("2021-12-05", 81)]
        result = format_daily(daily)
        assert result == "2021-12-01 179\n2021-12-05 81"


class TestFormatRecords:
    def test_format(self):
        records = [
            TrafficRecord(datetime(2021, 12, 1, 7, 30), 46),
            TrafficRecord(datetime(2021, 12, 1, 8, 0), 42),
        ]
        result = format_records(records)
        assert result == "2021-12-01T07:30:00 46\n2021-12-01T08:00:00 42"


class TestFormatReport:
    def test_sections_separated_by_blank_lines(self):
        report = format_report(
            total=100,
            daily=[("2021-12-01", 100)],
            top=[TrafficRecord(datetime(2021, 12, 1, 7, 30), 46)],
            least=[TrafficRecord(datetime(2021, 12, 1, 8, 0), 10)],
        )
        sections = report.strip().split("\n\n")
        assert len(sections) == 4

    def test_ends_with_newline(self):
        report = format_report(
            total=0,
            daily=[],
            top=[],
            least=[],
        )
        assert report.endswith("\n")
