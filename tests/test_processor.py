from datetime import datetime
import pytest

from traffic_counter.parser import TrafficLog
from traffic_counter.processor import TrafficProcessor


class TestTrafficProcessor:
    @pytest.mark.parametrize(
        ["logs", "expected_count"],
        [
            [[], 0],
            [[TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5)], 5],
            [
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=10),
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
                [TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5)],
                [(datetime(2025, 10, 1).date(), 5)],
            ],
            [
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 13, 0), count=7),
                    TrafficLog(timestamp=datetime(2025, 10, 2, 14, 0), count=10),
                ],
                [
                    (datetime(2025, 10, 1).date(), 12),
                    (datetime(2025, 10, 2).date(), 10),
                ],
            ],
        ],
    )
    def test_get_daily_count(self, logs, expected_daily_count):
        processor = TrafficProcessor(logs)
        daily_count = processor.get_daily_aggregated_count()
        assert list(daily_count.items()) == expected_daily_count

    @pytest.mark.parametrize(
        ["logs", "n", "expected_top_n"],
        [
            [[], 3, []],
            [
                [TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5)],
                1,
                [TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5)],
            ],
            [
                [TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5)],
                5,
                [TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5)],
            ],
            [
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 13, 0), count=10),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 14, 0), count=7),
                ],
                2,
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 13, 0), count=10),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 14, 0), count=7),
                ],
            ],
            [
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 13, 0), count=10),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 14, 0), count=7),
                ],
                0,
                [],
            ],
        ],
    )
    def test_get_top_n_traffic_logs(self, logs, n, expected_top_n):
        processor = TrafficProcessor(logs)
        top_n = processor.get_top_n_traffic_logs(n)
        assert top_n == expected_top_n

    @pytest.mark.parametrize(
        ["logs", "contiguous_count", "expected_least_traffic"],
        [
            # empty logs
            [[], 3, TrafficLog(timestamp=datetime.min, count=0)],
            # only create group of one log
            [
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 30), count=10),
                ],
                1,
                TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
            ],
            # least traffic for two contiguous logs.
            # Multiple options possible, returns the first one
            [
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 30), count=10),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 13, 0), count=8),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 13, 30), count=7),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 14, 0), count=15),
                ],
                2,
                TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=15),
            ],
            # least traffic for two contiguous logs.
            # there is a gap between 10:00 and 12:00, so only returns the 10:00 log
            [
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 10, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 30), count=10),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 13, 0), count=10),
                ],
                2,
                TrafficLog(timestamp=datetime(2025, 10, 1, 10, 0), count=5),
            ],
            # least traffic for three contiguous logs
            [
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 30), count=10),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 13, 0), count=7),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 13, 30), count=25),
                ],
                3,
                TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=25),
            ],
            # least traffic for three contiguous logs with only 2 contiguous logs available
            [
                [
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 0), count=5),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 12, 30), count=10),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 14, 0), count=7),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 14, 30), count=1),
                    TrafficLog(timestamp=datetime(2025, 10, 1, 15, 30), count=30),
                ],
                3,
                TrafficLog(timestamp=datetime(2025, 10, 1, 14, 0), count=8),
            ],
        ],
    )
    def test_get_least_traffic_in_contiguous_period(
        self, logs, contiguous_count, expected_least_traffic
    ):
        processor = TrafficProcessor(logs)
        least_traffic = processor.get_least_traffic_in_contiguous_period(
            contiguous_count
        )
        assert least_traffic == expected_least_traffic
