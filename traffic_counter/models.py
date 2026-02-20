from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class TrafficRecord:
    timestamp: datetime
    count: int
