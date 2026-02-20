import argparse
import sys
from pathlib import Path

from traffic_counter.analysis import (
    daily_counts,
    least_traffic_period,
    top_half_hours,
    total_count,
)
from traffic_counter.formatter import format_report
from traffic_counter.parser import parse_file


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Analyse traffic counter data.")
    parser.add_argument("file", type=Path, help="Path to the traffic data file")
    args = parser.parse_args(argv)

    if not args.file.exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    records = parse_file(args.file)

    report = format_report(
        total=total_count(records),
        daily=daily_counts(records),
        top=top_half_hours(records),
        least=least_traffic_period(records),
    )
    print(report, end="")


if __name__ == "__main__":
    main()
