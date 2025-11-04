from traffic_counter.parser import TrafficLog
from datetime import date


class TrafficProcessor:
    """
    TrafficProcessor can be used to process parsed traffic data.
    It does the following operations:
    - Get daily counts
    - Get total count

    It expects a list of TrafficLog objects as input which is ordered by timestamp.
    """

    total_count: int

    def __init__(self, traffic_data: list[TrafficLog]) -> None:
        self.traffic_data = traffic_data
        self.total_count = sum(log.count for log in traffic_data)
        self._daily_aggregated: dict[date, int] | None = None

    def get_total_count(self) -> int:
        return self.total_count

    def get_daily_aggregated_count(self) -> dict[date, int]:
        if self._daily_aggregated is None:
            self._daily_aggregated = {}
            for log in self.traffic_data:
                day = log.timestamp.date()
                self._daily_aggregated[day] = (
                    self._daily_aggregated.get(day, 0) + log.count
                )
        return self._daily_aggregated
