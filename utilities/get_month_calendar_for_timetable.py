import calendar

from babel.dates import get_month_names


def get_month_dict_for_timetable(
        month: list,
        current_month: int,
        locale: str = 'ru_RU'
):
    month_dict = {}

    for m in range(1, 13):
        if m in month:
            if m == current_month:
                month_dict[f'🔹{get_month_names(
                    context='stand-alone',
                    locale=locale)[m].capitalize()}'] = m
                continue

            month_dict[get_month_names(
                context='stand-alone',
                locale=locale)[m].capitalize()] = m
            continue

        month_dict[calendar.month_name[m]] = None

    return month_dict
