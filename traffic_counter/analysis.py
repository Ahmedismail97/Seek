from collections import defaultdict

from traffic_counter.models import TrafficRecord


def total_count(records: list[TrafficRecord]) -> int:
    return sum(r.count for r in records)


def daily_counts(records: list[TrafficRecord]) -> list[tuple[str, int]]:
    totals: dict[str, int] = defaultdict(int)
    for r in records:
        totals[r.timestamp.date().isoformat()] += r.count
    return sorted(totals.items())


def top_half_hours(records: list[TrafficRecord], n: int = 3) -> list[TrafficRecord]:
    return sorted(records, key=lambda r: r.count, reverse=True)[:n]


def least_traffic_period(
    records: list[TrafficRecord], window: int = 3
) -> list[TrafficRecord]:
    if len(records) < window:
        return list(records)

    min_sum = sum(r.count for r in records[:window])
    min_idx = 0
    current_sum = min_sum

    for i in range(window, len(records)):
        current_sum += records[i].count - records[i - window].count
        if current_sum < min_sum:
            min_sum = current_sum
            min_idx = i - window + 1

    return records[min_idx : min_idx + window]
