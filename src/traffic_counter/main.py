import argparse
from pathlib import Path

from traffic_counter.parser import TrafficParser
from traffic_counter.processor import TrafficProcessor


def analyse():
    parser = argparse.ArgumentParser(description="Traffic Counter analysis tool")
    parser.add_argument(
        "--input", "-i", type=Path, help="Path to the input traffic log file"
    )
    args = parser.parse_args()

    traffic_parser = TrafficParser()
    traffic_data = traffic_parser.parse_file(args.input)

    traffic_processor = TrafficProcessor(traffic_data)

    print("1. Total traffic count:", traffic_processor.get_total_count())
    print("2. Daily aggregated traffic counts:")
    daily_counts = traffic_processor.get_daily_aggregated_count()
    for day, count in daily_counts.items():
        print(f"  {day}: {count}")
    top_3_half_hours = traffic_processor.get_top_n_traffic_logs(3)
    print("3. Top 3 half-hour slots with highest traffic:")
    for log in top_3_half_hours:
        print(f"  {log.timestamp}: {log.count}")
    least_one_and_half = traffic_processor.get_least_traffic_in_contiguous_period(3)
    print("4. 3 contiguous half-hour slots with least traffic:")
    print(f"  Starting {least_one_and_half.timestamp}: {least_one_and_half.count}")
