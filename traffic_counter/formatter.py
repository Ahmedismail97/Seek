from traffic_counter.models import TrafficRecord


def format_total(total: int) -> str:
    return str(total)


def format_daily(daily: list[tuple[str, int]]) -> str:
    return "\n".join(f"{date} {count}" for date, count in daily)


def format_records(records: list[TrafficRecord]) -> str:
    return "\n".join(
        f"{r.timestamp.isoformat()} {r.count}" for r in records
    )


def format_report(
    total: int,
    daily: list[tuple[str, int]],
    top: list[TrafficRecord],
    least: list[TrafficRecord],
) -> str:
    sections = [
        "Total cars seen:\n" + format_total(total),
        "Cars per day:\n" + format_daily(daily),
        "Top 3 half-hours:\n" + format_records(top),
        "Least busy 1.5-hour period:\n" + format_records(least),
    ]
    return "\n\n".join(sections) + "\n"
