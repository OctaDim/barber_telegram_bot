import calendar
import locale
from datetime import datetime, date, timedelta
from typing import Literal

from dateutil.relativedelta import relativedelta


def get_next_12_months_nums_from_now(required_months_number: int) -> list:
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
                                symbols_max: Literal[1, 2, 3, 100] = 3,
                                upper_case: bool = False) -> list:
    origin_locale = locale.getlocale(locale.LC_TIME)

    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    weekdays_abbr_list = calendar.weekheader(symbols_max).split()
    if upper_case:
        weekdays_abbr_list = [wd.upper() for wd in weekdays_abbr_list]

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
                         language: Literal["EN", "RU"] = "EN",
                         upper_case: bool = False) -> dict:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    if abbreviation:
        month_names = dict(enumerate(calendar.month_abbr))
    else:
        month_names = dict(enumerate(calendar.month_name))

    if upper_case:
        result_month_names = {}
        for month_key, month_name in month_names.items():
            result_month_names[month_key] = month_name.upper()
    else:
        result_month_names = month_names

    locale.setlocale(locale.LC_TIME, locale=origin_locale)
    return result_month_names


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
                            language: Literal["EN", "RU"] = "EN",
                            upper_case: bool = False) -> dict:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    if abbreviation:
        weekdays_names = dict(enumerate(calendar.day_abbr))
    else:
        weekdays_names = dict(enumerate(calendar.day_name))

    if upper_case:
        result_weekdays_names = {}
        for month_key, month_name in weekdays_names.items():
            result_weekdays_names[month_key] = month_name.upper()
    else:
        result_weekdays_names = weekdays_names

    locale.setlocale(locale.LC_TIME, locale=origin_locale)
    return result_weekdays_names


def get_weekday_name_by_index(weekday_index: int,
                              abbreviation: bool = False,
                              language: Literal["EN", "RU"] = "EN",
                              upper_case: bool = False) -> str:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    if abbreviation:
        weekday_name = calendar.day_abbr[weekday_index]
    else:
        weekday_name = calendar.day_name[weekday_index]

    weekday_name = weekday_name.upper() if upper_case else weekday_name

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
            month_name = get_month_name_by_number(date_value.month,
                                                  language="RU")

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
                                     abbrev_symbols: Literal[
                                         1, 3, "1", "3", "full"] = 1,
                                     show_seconds: bool = False,
                                     hide_zero_values: bool = False,
                                     separator: str = ":",
                                     space_before_note: bool = False,
                                     show_period_after_note: bool = False,
                                     upper_case: bool = False) -> str:
    hours_note, minutes_note, seconds_note = ("", "", "")

    total_seconds = timedelta_value.total_seconds()
    hrs_value = int(total_seconds // 3600)
    min_value = int((total_seconds % 3600) // 60)
    seconds_value = int(total_seconds % 60)

    if language == "EN":
        match abbrev_symbols:
            case 1 | "1":
                hours_note, minutes_note, seconds_note = ("h", "m", "s")
            case 3 | "3":
                hours_note, minutes_note, seconds_note = ("hrs", "min", "sec")
            case _:  # case "full" or any
                hours_note = "hours" if hrs_value > 1 else "hour"
                minutes_note = "minutes" if min_value > 1 else "minute"
                seconds_note = "seconds" if seconds_value > 1 else "second"

    elif language == "RU":
        match abbrev_symbols:
            case 1 | "1":
                hours_note, minutes_note, seconds_note = ("ч", "м", "с")
            case 3 | "3":
                hours_note, minutes_note, seconds_note = ("час", "мин", "сек")
            case _:  # case "full" or any
                if hrs_value % 10 == 1 and hrs_value % 100 != 11:
                    hours_note = "час"
                elif (2 <= hrs_value % 10 <= 4
                      and (hrs_value % 100 < 10 or hrs_value % 100 >= 20)):
                    hours_note = "часа"
                else:
                    hours_note = "часов"

                if min_value % 10 == 1 and min_value % 100 != 11:
                    minutes_note = "минута"
                elif (2 <= min_value % 10 <= 4
                      and (min_value % 100 < 10 or min_value % 100 >= 20)):
                    minutes_note = "минуты"
                else:
                    minutes_note = "минут"

                if seconds_value % 10 == 1 and seconds_value % 100 != 11:
                    seconds_note = "секунда"
                elif (2 <= seconds_value % 10 <= 4
                      and (seconds_value % 100 < 10
                           or seconds_value % 100 >= 20)):
                    seconds_note = "секунды"
                else:
                    seconds_note = "секунд"

    space = " " if space_before_note else ""

    if show_period_after_note and abbrev_symbols in (1, 3, "1", "3"):
        period_after_note = "."
    else:
        period_after_note = ""

    if not hrs_value and hide_zero_values:
        hours_str = ""
    else:
        hours_str = (f"{hrs_value}"
                     f"{space}"
                     f"{hours_note}"
                     f"{period_after_note}"
                     f"{separator}")

    if not min_value and hide_zero_values:
        minutes_str = ""
    else:
        before_seconds_separator = separator if show_seconds else ""
        minutes_str = (f"{min_value}"
                       f"{space}"
                       f"{minutes_note}"
                       f"{period_after_note}"
                       f"{before_seconds_separator}")

    if show_seconds:
        if not seconds_value and hide_zero_values:
            seconds_str = ""
        else:
            seconds_str = (f"{seconds_value}"
                           f"{space}"
                           f"{seconds_note}"
                           f"{period_after_note}")
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
# print(get_month_names_dict(
#     language="RU",
#     upper_case=True,
#     abbreviation=True))
#
# print(get_weekdays_flex_abbr_list(
#     language="EN",
#     upper_case=True,
#     symbols_max=3))
#
#
# print(get_numeric_month_calendar_list(
#     year=2024, month=12))
#
# print(get_next_12_months_nums_from_now(required_months_number=12))
#
# print(get_weekdays_names_dict(
#     language="RU",
#     upper_case=True,
#     abbreviation=True))
#
# print(get_weekday_name_by_index(
#     weekday_index=0))

# print(get_weekday_flex_abbr_by_date(
#     date_value=datetime.now(),
#     language="RU",
#     symbols_max=
# ))
#
# print(get_hours_minutes_secs_timedelta(
#     timedelta_value=timedelta(hours=1024, minutes=123, seconds=159),
#     language="RU",
#     abbrev_symbols="full",
#     show_period_after_note=True,
#     show_seconds=True,
#     separator=" ",
#     space_before_note=True
# ))
# ######################################################################
