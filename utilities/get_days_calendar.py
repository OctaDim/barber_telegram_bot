import calendar
from datetime import datetime

from babel.dates import get_month_names, format_date

from database.db_queries.work_time_queries import get_work_time_by_month


def get_short_weekday_name(date: datetime, locale: str = "ru_RU") -> str:
    return format_date(date, "E", locale=locale).capitalize()


def get_days_in_month(month_name, year, current_date: datetime, master_id: int):
    for i in range(1, 13):
        month = get_month_names(
            context="stand-alone",
            locale='ru_RU')[i].capitalize()

        if month == month_name:
            month_number = i
            break

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
        day_of_week_short = get_short_weekday_name(date, locale="ru_RU")

        days_in_month[date.strftime('%d')] = day_of_week_short

    return days_in_month, month_name
