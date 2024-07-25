import datetime


def get_time_delta(time_list):
    hours = int(time_list[0].replace('h', ''))
    minutes = int(time_list[1].replace('m', ''))
    return datetime.timedelta(hours=hours, minutes=minutes)


def get_service_times(start_time: list, time_duration: list, block_hour: list, block_minutes: list):
    start_time_delta = get_time_delta(start_time)
    duration_delta = get_time_delta(time_duration)

    today = datetime.datetime.now().date()
    start_datetime = datetime.datetime.combine(today, datetime.time(0)) + start_time_delta
    end_datetime = start_datetime + duration_delta

    start_time = start_datetime.time()
    end_time = end_datetime.time()

    block_minute = [end_time.hour]

    for hour in range(start_time.hour, end_time.hour):
        block_hour.append(hour)

    for minute in range(0, end_time.minute, 5):
        block_minute.append(minute)

    block_minutes.append(block_minute)

    data = {
        'start_time': start_time,
        'end_time': end_time,
        'block_minute': block_minutes,
        'block_hour': block_hour,
    }

    return data
