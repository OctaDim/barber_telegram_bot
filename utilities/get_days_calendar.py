import calendar
from datetime import datetime


def get_days_in_month(month_name, year):
    month_number = list(calendar.month_name).index(month_name.capitalize())

    _, num_days = calendar.monthrange(year, month_number)

    days_in_month = {}
    for day in range(1, num_days + 1):
        date = datetime(year, month_number, day)
        day_of_week_short = date.strftime('%a')

        days_in_month[date.strftime('%d')] = day_of_week_short

    return days_in_month, month_name
