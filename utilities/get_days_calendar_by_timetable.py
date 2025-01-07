import calendar
from datetime import datetime

from babel.dates import get_month_names

from utilities.get_days_calendar import get_short_weekday_name


def get_days_in_month_by_logbook(
        month,
        year,
        days,
        locale: str = 'ru_RU'
):
    month_name = get_month_names(context='stand-alone',
                                 locale=locale)[month].capitalize()

    _, num_days = calendar.monthrange(year, month)

    days_in_month = {}

    for day in range(1, num_days + 1):
        date = datetime(year, month, day)
        day_of_week_short = get_short_weekday_name(date, locale="ru_RU")

        if date.day in days:
            days_in_month[date.strftime('%d')] = day_of_week_short
            continue

        days_in_month[f'-{date.strftime('%d')}'] = day_of_week_short

    return days_in_month, month_name



