from datetime import datetime
import pytest

from traffic_counter.parser import TrafficLog
from traffic_counter.processor import TrafficProcessor


class TestTrafficProcessor:
    @pytest.mark.parametrize(
        ["logs", "expected_count"],
        [
            [[], 0],
            [[TrafficLog(timestamp=datetime(2023, 1, 1, 12, 0), count=5)], 5],
            [
                [
                    TrafficLog(timestamp=datetime(2023, 1, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2023, 1, 1, 12, 0), count=10),
                ],
                15,
            ],
        ],
    )
    def test_get_total_count(self, logs, expected_count):
        processor = TrafficProcessor(logs)
        total_count = processor.get_total_count()
        assert total_count == expected_count


    @pytest.mark.parametrize(
        ["logs", "expected_daily_count"],
        [
            [[], []],
            [
                [TrafficLog(timestamp=datetime(2023, 1, 1, 12, 0), count=5)],
                [(datetime(2023, 1, 1).date(), 5)],
            ],
            [
                [
                    TrafficLog(timestamp=datetime(2023, 1, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2023, 1, 1, 13, 0), count=7),
                    TrafficLog(timestamp=datetime(2023, 1, 2, 14, 0), count=10),
                ],
                [(datetime(2023, 1, 1).date(), 12), (datetime(2023, 1, 2).date(), 10)],
            ],
        ],
    )
    def test_get_daily_count(self, logs, expected_daily_count):
        processor = TrafficProcessor(logs)
        daily_count = processor.get_daily_aggregated_count()
        assert list(daily_count.items()) == expected_daily_count
