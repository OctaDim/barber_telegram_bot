import calendar
import locale
from datetime import datetime, date, timedelta
from typing import Literal

from dateutil.relativedelta import relativedelta


def get_next_months_list_from_now(required_months_number: int) -> list:
    datetime_now = datetime.now()
    next_months_numbers = []

    for month_step in range(required_months_number):
        future_datetime = datetime_now + relativedelta(months=month_step)
        next_months_numbers.append(future_datetime.month)

    return next_months_numbers


def get_today_weekday_index() -> int:
    weekday_number = datetime.now().weekday()
    return weekday_number


def get_weekday_index_by_date(date_value: date | datetime) -> int:
    weekday_number = date_value.weekday()
    return weekday_number


def get_weekday_index_by_year_month_day(year: int, month: int, day: int) -> int:
    weekday_number = calendar.weekday(year, month, day)
    return weekday_number


def get_weekdays_flex_abbr_list(language: Literal["EN", "RU"] = "EN",
                                symbols_max: Literal[1, 2, 3, 100] = 3) -> list:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    weekdays_abbr_list = calendar.weekheader(symbols_max).split()

    locale.setlocale(locale.LC_TIME, locale=origin_locale)
    return weekdays_abbr_list


def get_weekday_flex_abbr_by_index(weekday_index: int,
                                   language: Literal["EN", "RU"] = "EN",
                                   symbols_max: Literal[1, 2, 3, 100] = 3,
                                   upper_case: bool = False) -> str:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    weekdays_abbr_list = calendar.weekheader(symbols_max).split()
    weekday_abbr = weekdays_abbr_list[weekday_index]

    locale.setlocale(locale.LC_TIME, locale=origin_locale)

    weekday_abbr = weekday_abbr.upper() if upper_case else weekday_abbr
    return weekday_abbr


def get_weekday_flex_abbr_by_date(date_value: date | datetime,
                                  language: Literal["EN", "RU"] = "EN",
                                  symbols_max: Literal[1, 2, 3, 100] = 3,
                                  upper_case: bool = False) -> str:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    weekdays_abbr_list = calendar.weekheader(symbols_max).split()
    weekday_number = date_value.weekday()
    weekday_abbr = weekdays_abbr_list[weekday_number]

    locale.setlocale(locale.LC_TIME, locale=origin_locale)

    weekday_abbr = weekday_abbr.upper() if upper_case else weekday_abbr
    return weekday_abbr


def get_days_quantity_in_month(year: int, month: int) -> int:
    month_days_quantity = calendar.monthrange(year=year, month=month)[1]
    return month_days_quantity


# print(get_days_quantity_in_month(2024, 7))

def get_month_start_weekday_index(year: int, month: int) -> int:
    month_start_weekday = calendar.monthrange(year=year, month=month)[0]
    return month_start_weekday


def get_month_names_dict(abbreviation: bool = False,
                         language: Literal["EN", "RU"] = "EN") -> dict:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    if abbreviation:
        month_names_dict = dict(enumerate(calendar.month_abbr))
    else:
        month_names_dict = dict(enumerate(calendar.month_name))

    locale.setlocale(locale.LC_TIME, locale=origin_locale)
    return month_names_dict


def get_month_name_by_number(month_number: int,
                             abbreviation: bool = False,
                             language: Literal["EN", "RU"] = "EN",
                             upper_case: bool = False) -> str:

    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    if abbreviation:
        month_name = calendar.month_abbr[month_number]
    else:
        month_name = calendar.month_name[month_number]

    month_name = month_name.upper() if upper_case else month_name

    locale.setlocale(locale.LC_TIME, locale=origin_locale)
    return month_name


def get_weekdays_names_dict(abbreviation: bool = False,
                            language: Literal["EN", "RU"] = "EN") -> dict:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    if abbreviation:
        weekdays_names = dict(enumerate(calendar.day_abbr))
    else:
        weekdays_names = dict(enumerate(calendar.day_name))

    locale.setlocale(locale.LC_TIME, locale=origin_locale)
    return weekdays_names


def get_weekday_name_by_index(weekday_index: int,
                              abbreviation: bool = False,
                              language: Literal["EN", "RU"] = "EN") -> str:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    if abbreviation:
        weekday_name = calendar.day_abbr[weekday_index]
    else:
        weekday_name = calendar.day_name[weekday_index]

    locale.setlocale(locale.LC_TIME, locale=origin_locale)
    return weekday_name


def get_numeric_month_calendar_list(year: int, month: int) -> list[list]:
    month_calendar_list = calendar.monthcalendar(year=year, month=month)
    return month_calendar_list


def get_first_weekday_index():
    return calendar.firstweekday()


def check_day_is_weekend(year: int, month: int, day: int) -> bool:
    weekday_index = get_weekday_index_by_year_month_day(year, month, day)
    day_is_weekend: bool = weekday_index in [5, 6]
    return day_is_weekend


def get_date_with_month_name(date_value: datetime | date,
                             language: Literal["EN", "RU"] = "EN",
                             upper_case: bool = False) -> str:
    if language == "EN":
        month_name = get_month_name_by_number(date_value.month, language="EN")
        date_string = f"{month_name} {date_value.day}, {date_value.year}"

    elif language == "RU":
        month_name = get_month_name_by_number(date_value.month, language="RU")
        if date_value.month in [1, 2, 4, 5, 6, 7, 9, 10, 11, 12]:
            month_name = month_name[:-1] + "я"
        else:
            month_name += "а"

        date_string = f"{date_value.day} {month_name} {date_value.year}"

    else:
        date_string = str(date_value.replace(
            hour=0, minute=0, second=0, microsecond=0))

    date_string = date_string.upper() if upper_case else date_string
    return date_string


def get_time_flex_from_datetime(date_value: datetime,
                                language: Literal["EN", "RU"] = "EN",
                                with_seconds: bool = False,
                                separator: str = ":",
                                hrs_and_mns_notation: bool = False,
                                upper_case: bool = False) -> str:
    time_pattern = ""

    if not hrs_and_mns_notation:
        if not with_seconds:
            time_pattern = f"%H{separator}%M"
        else:
            time_pattern = f"%H{separator}%M{separator}%S"
    else:
        if language == "EN":
            if not with_seconds:
                time_pattern = f"{'%H'}h{separator}{'%M'}m"
            else:
                time_pattern = f"{'%H'}h{separator}{'%M'}m{separator}{'%S'}s"
        elif language == "RU":
            if not with_seconds:
                time_pattern = f"{'%H'}ч{separator}{'%M'}м"
            else:
                time_pattern = f"{'%H'}ч{separator}{'%M'}м{separator}{'%S'}c"

    time_result = date_value.strftime(time_pattern)
    time_result = time_result.upper() if upper_case else time_result
    return time_result


def get_date_flex_from_datetime(date_value: datetime | date,
                                language: Literal["EN", "RU"] = "EN",
                                separator: str = "-",
                                month_as_name: bool = False,
                                year_abbreviated: bool = False,
                                upper_case: bool = False) -> str:
    date_pattern = ""

    year_pattern = "%y" if year_abbreviated else "%Y"
    month_pattern = "%B" if month_as_name else "%m"

    if language == "EN":
        date_pattern = f"{year_pattern}{separator}{month_pattern}{separator}%d"

    elif language == "RU":
        if month_as_name:
            month_name = get_month_name_by_number(date_value.month, language="RU")

            if date_value.month in [1, 2, 4, 5, 6, 7, 9, 10, 11, 12]:
                month_name = month_name[:-1] + "я"
            else:
                month_name += "а"
            date_pattern = f"%d{separator}{month_name}{separator}{year_pattern}"

        else:
            date_pattern = f"%d{separator}%m{separator}{year_pattern}"

    date_result = date_value.strftime(date_pattern)
    date_result = date_result.upper() if upper_case else date_result

    return date_result


def get_hours_minutes_secs_timedelta(timedelta_value: timedelta,
                                     language: Literal["EN", "RU"] = "EN",
                                     abbrev_symbols: Literal["1", "3", "F"] = "1",
                                     show_seconds: bool = False,
                                     hide_zero_values: bool = False,
                                     separator: str = ":",
                                     space_before_note: bool = False,
                                     upper_case: bool = False) -> str:
    hrs_note, min_note, sec_note = ("", "", "")

    if language == "EN":
        if abbrev_symbols == "1":
            hrs_note = "h"
            min_note = "m"
            sec_note = "s"
        elif abbrev_symbols == "3":
            hrs_note = "hrs"
            min_note = "min"
            sec_note = "sec"
        elif abbrev_symbols == "F":
            hrs_note = "hours"
            min_note = "minutes"
            sec_note = "seconds"
    elif language == "RU":
        if abbrev_symbols == "1":
            hrs_note = "ч"
            min_note = "м"
            sec_note = "с"
        elif abbrev_symbols == "3":
            hrs_note = "час"
            min_note = "мин"
            sec_note = "сек"
        elif abbrev_symbols == "F":
            hrs_note = "часов"
            min_note = "минут"
            sec_note = "секунд"

    total_seconds = timedelta_value.total_seconds()
    hrs_value = int(total_seconds // 3600)
    min_value = int((total_seconds % 3600) // 60)
    seconds_value = int(total_seconds % 60)

    space = " " if space_before_note else ""

    if not hrs_value and hide_zero_values:
        hours_str = ""
    else:
        hours_str = f"{hrs_value}{space}{hrs_note}{separator}"

    if not min_value and hide_zero_values:
        minutes_str = ""
    else:
        before_seconds_separator = separator if show_seconds else ""
        minutes_str = f"{min_value}{space}{min_note}{before_seconds_separator}"

    if show_seconds:
        if not seconds_value and hide_zero_values:
            seconds_str = ""
        else:
            seconds_str = f"{seconds_value}{space}{sec_note}"
    else:
        seconds_str = ""

    timedelta_str = f"{hours_str}{minutes_str}{seconds_str}"
    timedelta_str = timedelta_str.upper() if upper_case else timedelta_str
    return timedelta_str

# ############################### TEST CODE ############################
# test_date = datetime(year=2024, month=10, day=12,
#                      hour=2, minute=7,
#                      second=5, microsecond=23545)
#
# test_timedelta = timedelta(weeks=2, days=1,
#                            hours=3, minutes=7, seconds=2,
#                            microseconds=15, milliseconds=1000)
# ######################################################################
