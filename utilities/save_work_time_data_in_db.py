from datetime import datetime, timedelta

from database.db_queries.work_time_queries import create_work_time, create_break_time


def save_work_time_data_in_db(
        time_start: timedelta,
        time_end: timedelta,
        interval: timedelta,
        days: list,
        master_id: int,
        month,
        year,
        start_break: timedelta = None,
        end_break: timedelta = None,
        master_obj=None
):
    time_intervals = []

    month_dict = {
        "Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4, "Май": 5, "Июнь": 6,
        "Июль": 7, "Август": 8, "Сентябрь": 9, "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12
    }

    for day in days:
        start_datetime = datetime(year=int(year), month=month_dict.get(month), day=int(day)) + time_start
        end_datetime = datetime(year=int(year), month=month_dict.get(month), day=int(day)) + time_end

        if start_break:
            start_break_datetime = datetime(year=int(year), month=month_dict.get(month), day=int(day)) + start_break
            end_break_datetime = datetime(year=int(year), month=month_dict.get(month), day=int(day)) + end_break

            create_break_time(
                start_break=start_break_datetime,
                end_break=end_break_datetime,
                master_obj=master_obj
            )

        current_time = start_datetime
        while current_time < end_datetime:
            next_time = current_time + interval

            if next_time > end_datetime:
                next_time = end_datetime

            if start_break:
                if current_time <= start_break_datetime < next_time:
                    if current_time != start_break_datetime:
                        time_intervals.append((current_time, start_break_datetime))

                    if end_break_datetime == next_time:
                        current_time = next_time
                        continue

                    if next_time > end_break_datetime:
                        time_intervals.append((end_break_datetime, next_time))
                        current_time = next_time
                        continue

                    while True:
                        next_time = next_time + interval

                        if next_time == end_break_datetime:
                            current_time = next_time
                            break

                        if next_time > end_break_datetime:
                            time_intervals.append((end_break_datetime, next_time))
                            current_time = next_time
                            break

                    continue

            time_intervals.append((current_time, next_time))
            current_time = next_time

    for time_interval in time_intervals:
        slot_duration = time_interval[1] - time_interval[0]

        create_work_time(
            time_start=time_interval[0],
            time_end=time_interval[1],
            slot_duration=slot_duration,
            master_id=master_id
        )
