from dataclasses import dataclass, field
from datetime import datetime


@dataclass(order=True)
class TrafficLog:
    """
    This is a simple data structure to hold a single traffic entry.
    It contains a timestamp and a count.
    """

    timestamp: datetime
    count: int = field(compare=False)


class TrafficParser:
    """
    TrafficParser can be used to parse traffic file.
    It expects an input like the next 3 lines:
    2021-12-01T05:00:00 5
    2021-12-01T05:30:00 12
    2021-12-01T06:00:00 14

    Each line contains a timestamp and a count separated by space.
    It returns a TrafficData object, which contains the parsed data.
    """

    def parse_file(self, file_path: str) -> list[TrafficLog]:
        result: list[TrafficLog] = []
        with open(file_path, "r") as f:
            for line in f:
                timestamp, count = line.strip().split()
                result.append(TrafficLog(datetime.fromisoformat(timestamp), int(count)))
        return result
