import calendar
from datetime import datetime


def get_days_in_month_by_logbook(month, year, days):
    month_name = calendar.month_name[month]

    _, num_days = calendar.monthrange(year, month)

    days_in_month = {}

    for day in range(1, num_days + 1):
        date = datetime(year, month, day)
        day_of_week_short = date.strftime('%a')

        if date.day in days:
            days_in_month[date.strftime('%d')] = day_of_week_short
            continue

        days_in_month[f'-{date.strftime('%d')}'] = day_of_week_short

    return days_in_month, month_name



