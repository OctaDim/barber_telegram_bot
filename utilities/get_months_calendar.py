import calendar

from babel.dates import get_month_names


def get_month_dict(month, locale: str = 'ru_RU'):
    month_dict = {}

    for m in range(1, 13):
        if month > m:
            month_dict[get_month_names(
                context='stand-alone',
                locale=locale)[m].capitalize()] = None
            continue

        month_dict[get_month_names(
                context='stand-alone',
                locale=locale)[m].capitalize()] = True

    return month_dict
