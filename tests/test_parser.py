from datetime import datetime

from traffic_counter.models import TrafficRecord
from traffic_counter.parser import parse_file, parse_line


class TestParseLine:
    def test_normal_line(self):
        record = parse_line("2021-12-01T05:00:00 5")
        assert record == TrafficRecord(datetime(2021, 12, 1, 5, 0), 5)

    def test_zero_count(self):
        record = parse_line("2021-12-01T23:30:00 0")
        assert record.count == 0

    def test_whitespace_handling(self):
        record = parse_line("  2021-12-01T05:00:00 5  \n")
        assert record == TrafficRecord(datetime(2021, 12, 1, 5, 0), 5)


class TestParseFile:
    def test_parse_file(self, sample_file):
        records = parse_file(sample_file)
        assert len(records) == 3
        assert records[0].count == 5
        assert records[2].count == 14

    def test_blank_lines_skipped(self, tmp_path):
        path = tmp_path / "blanks.txt"
        path.write_text("2021-12-01T05:00:00 5\n\n2021-12-01T06:00:00 14\n\n")
        records = parse_file(path)
        assert len(records) == 2
