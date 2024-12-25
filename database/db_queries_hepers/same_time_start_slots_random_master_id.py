import random
from typing import List


def get_time_start_unique_random_intervals(
        time_start_non_unique_intervals: List[dict]
) -> List[dict]:
    same_time_start_intervals_dict = {}
    for cur_interval in time_start_non_unique_intervals:
        slot_time_start = cur_interval.get("slot time start")
        intervals_list = same_time_start_intervals_dict.setdefault(slot_time_start, [])
        intervals_list.append(cur_interval)
        same_time_start_intervals_dict[slot_time_start] = intervals_list

    time_start_unique_intervals = []
    for time_start, intervals_list in same_time_start_intervals_dict.items():
        same_time_start_random_interval = random.choice(intervals_list)
        time_start_unique_intervals.append(same_time_start_random_interval)

    return time_start_unique_intervals
