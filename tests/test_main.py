from pathlib import Path

from traffic_counter.main import main


EXPECTED_OUTPUT = """\
398

2021-12-01 179
2021-12-05 81
2021-12-08 134
2021-12-09 4

2021-12-01T07:30:00 46
2021-12-01T08:00:00 42
2021-12-08T17:00:00 33

2021-12-01T15:00:00 9
2021-12-01T15:30:00 11
2021-12-01T23:30:00 0
"""

SAMPLE_FILE = Path(__file__).resolve().parent.parent / "data" / "sample.txt"


class TestMainIntegration:
    def test_end_to_end(self, capsys):
        main([str(SAMPLE_FILE)])
        captured = capsys.readouterr()
        assert captured.out == EXPECTED_OUTPUT

    def test_missing_file(self, tmp_path):
        import pytest

        with pytest.raises(SystemExit):
            main([str(tmp_path / "nonexistent.txt")])
