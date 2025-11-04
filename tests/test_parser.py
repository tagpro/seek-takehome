from datetime import datetime
from traffic_counter.parser import TrafficLog, TrafficParser


sample_traffic = """
2021-12-01T05:00:00 5
2021-12-01T05:30:00 12
2021-12-01T06:00:00 14
2021-12-01T06:30:00 15
2021-12-01T07:00:00 25
"""


class TestParser:
    def test_parse_file(self, temp_traffic_file):
        expected: list[TrafficLog] = [
            TrafficLog(
                timestamp=datetime.fromisoformat("2021-12-01T05:00:00"), count=5
            ),
            TrafficLog(
                timestamp=datetime.fromisoformat("2021-12-01T05:30:00"), count=12
            ),
            TrafficLog(
                timestamp=datetime.fromisoformat("2021-12-01T06:00:00"), count=14
            ),
            TrafficLog(
                timestamp=datetime.fromisoformat("2021-12-01T06:30:00"), count=15
            ),
            TrafficLog(
                timestamp=datetime.fromisoformat("2021-12-01T07:00:00"), count=25
            ),
        ]

        file_path = temp_traffic_file(sample_traffic.strip())
        parser = TrafficParser()
        result = parser.parse_file(file_path)
        assert result == expected
