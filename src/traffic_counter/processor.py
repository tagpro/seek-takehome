import sys
from traffic_counter.parser import TrafficLog
from datetime import date, datetime, timedelta


class TrafficProcessor:
    """
    TrafficProcessor can be used to process parsed traffic data.
    It does the following operations:
    - Get daily counts
    - Get total count

    It expects a list of TrafficLog objects as input which is ordered by timestamp.
    """

    timeslot_minutes = 30

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

    def get_top_n_traffic_logs(self, n: int) -> list[TrafficLog]:
        if n <= 0:
            return []
        return sorted(self.traffic_data, key=lambda log: log.count, reverse=True)[:n]

    def _get_n_contiguous_logs(self, start: int, n: int) -> list[TrafficLog]:
        """
        Get n contiguous logs starting from start of the traffic data.
        The contiguous logs must fall under consecutive half-hour slots.
        """
        if n <= 0:
            return []

        last_timestamp = self.traffic_data[start].timestamp + timedelta(
            minutes=self.timeslot_minutes * (n - 1)
        )
        traffic_len = len(self.traffic_data)
        end = min(start + n, traffic_len)

        return [
            log
            for _, log in enumerate(self.traffic_data[start:end])
            if log.timestamp <= last_timestamp
        ]

    def get_least_traffic_in_contiguous_period(
        self, contiguous_count: int
    ) -> TrafficLog:
        """
        We want to find the n contiguous half-hour slots with the least traffic.
        Because there may be missing half-hour slots in the data, we only consider
        the slots which are contiguous in time.
        Assumption: we consider individual half-hour slots as n contiguous slots even when
        we don't have data for the next n slots.

        contiguous_count: number of contiguous half-hour slots to consider
        returns: TrafficLog with the timestamp of the first slot and the total count of the contiguous slots
        """
        # contiguous_traffic holds the traffic count for n contiguous half-hour slots
        min_contiguous_traffic: TrafficLog = TrafficLog(
            timestamp=datetime.min, count=sys.maxsize
        )
        if contiguous_count <= 0 or len(self.traffic_data) == 0:
            return TrafficLog(timestamp=datetime.min, count=0)

        traffic_len = len(self.traffic_data)
        for i in range(traffic_len - contiguous_count + 1):
            next_logs = self._get_n_contiguous_logs(i, contiguous_count)
            total_count = sum(log.count for log in next_logs)
            if total_count < min_contiguous_traffic.count:
                min_contiguous_traffic = TrafficLog(
                    timestamp=next_logs[0].timestamp, count=total_count
                )
        return min_contiguous_traffic
