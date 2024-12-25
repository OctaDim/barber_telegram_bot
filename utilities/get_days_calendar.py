import calendar
from datetime import datetime

from database.db_queries.work_time_queries import get_work_time_by_month


def get_days_in_month(month_name, year, current_date: datetime, master_id: int):
    month_number = list(calendar.month_name).index(month_name.capitalize())

    _, num_days = calendar.monthrange(year, month_number)

    days_in_month = {}

    work_time_days = get_work_time_by_month(month=month_number, year=year, master_id=master_id)

    for day in range(1, num_days + 1):
        if month_number == current_date.month and year == current_date.year:
            if day < current_date.day:
                continue

        if day in work_time_days:
            continue

        date = datetime(year, month_number, day)
        day_of_week_short = date.strftime('%a')

        days_in_month[date.strftime('%d')] = day_of_week_short

    return days_in_month, month_name
