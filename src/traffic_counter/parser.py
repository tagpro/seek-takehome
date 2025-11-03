from dataclasses import dataclass, field


@dataclass
class TrafficData:
    """
    This is a simple data structure to hold traffic data.
    Traffic data is a simple list of (timestamp, count) tuples.
    """
    data: list[tuple[str, int]] = field(default_factory=list)

    def add_entry(self, timestamp: str, count: int):
        self.data.append((timestamp, count))

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
    def parse_file(self, file_path: str) -> TrafficData:
        result: TrafficData = TrafficData()
        with open(file_path, 'r') as f:
            for line in f:
                timestamp, count = line.strip().split()
                result.add_entry(timestamp, int(count))
        return result
