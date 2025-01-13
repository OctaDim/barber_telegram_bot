from datetime import datetime, date, timedelta
from typing import Literal
from dateutil.relativedelta import relativedelta
from babel.dates import get_month_names, get_day_names, format_date, format_time, format_timedelta
import locale
import calendar

def get_next_12_months_nums_from_now(required_months_number: int) -> list:
    datetime_now = datetime.now()
    next_months_numbers = []

    for month_step in range(required_months_number):
        future_datetime = datetime_now + relativedelta(months=month_step)
        next_months_numbers.append(future_datetime.month)

    return next_months_numbers


def get_today_weekday_index() -> int:
    return datetime.now().weekday()


def get_weekday_index_by_date(date_value: date | datetime) -> int:
    return date_value.weekday()


def get_weekday_index_by_year_month_day(year: int, month: int, day: int) -> int:
    return datetime(year=year, month=month, day=day).weekday()


def get_weekdays_flex_abbr_list(language: Literal["EN", "RU"] = "EN",
                                symbols_max: Literal[1, 2, 3, 100] = 3,
                                upper_case: bool = False) -> list:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    weekdays_abbr_list = [
        get_day_names(width="abbreviated", context="stand-alone", locale=locale_name)[i]
        for i in range(7)
    ]
    if upper_case:
        weekdays_abbr_list = [wd.upper() for wd in weekdays_abbr_list]
    return weekdays_abbr_list


def get_weekday_flex_abbr_by_index(weekday_index: int,
                                   language: Literal["EN", "RU"] = "EN",
                                   symbols_max: Literal[1, 2, 3, 100] = 3,
                                   upper_case: bool = False) -> str:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    weekday_abbr = get_day_names(width="abbreviated", context="stand-alone", locale=locale_name)[weekday_index]
    if upper_case:
        weekday_abbr = weekday_abbr.upper()
    return weekday_abbr


def get_weekday_flex_abbr_by_date(date_value: date | datetime,
                                  language: Literal["EN", "RU"] = "EN",
                                  symbols_max: Literal[1, 2, 3, 100] = 3,
                                  upper_case: bool = False) -> str:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    weekday_abbr = format_date(date_value, "E", locale=locale_name)
    if upper_case:
        weekday_abbr = weekday_abbr.upper()
    return weekday_abbr


def get_days_quantity_in_month(year: int, month: int) -> int:
    return (datetime(year=year, month=month + 1, day=1) - timedelta(days=1)).day


def get_month_start_weekday_index(year: int, month: int) -> int:
    return datetime(year=year, month=month, day=1).weekday()


def get_month_names_dict(abbreviation: bool = False,
                         language: Literal["EN", "RU"] = "EN",
                         upper_case: bool = False) -> dict:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    month_names = {
        i: get_month_names(width="abbreviated" if abbreviation else "wide", context="stand-alone", locale=locale_name)[i]
        for i in range(1, 13)
    }
    month_names[0] = ""
    if upper_case:
        month_names = {k: v.upper() for k, v in month_names.items()}
    return month_names


def get_month_name_by_number(month_number: int,
                             abbreviation: bool = False,
                             language: Literal["EN", "RU"] = "EN",
                             upper_case: bool = False) -> str:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    month_name = get_month_names(width="abbreviated" if abbreviation else "wide", context="stand-alone", locale=locale_name)[month_number]
    if upper_case:
        month_name = month_name.upper()
    return month_name


def get_weekdays_names_dict(abbreviation: bool = False,
                            language: Literal["EN", "RU"] = "EN",
                            upper_case: bool = False) -> dict:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    weekdays_names = {
        i: get_day_names(width="abbreviated" if abbreviation else "wide", context="stand-alone", locale=locale_name)[i]
        for i in range(7)
    }
    if upper_case:
        weekdays_names = {k: v.upper() for k, v in weekdays_names.items()}
    return weekdays_names


def get_weekday_name_by_index(weekday_index: int,
                              abbreviation: bool = False,
                              language: Literal["EN", "RU"] = "EN",
                              upper_case: bool = False) -> str:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    weekday_name = get_day_names(width="abbreviated" if abbreviation else "wide", context="stand-alone", locale=locale_name)[weekday_index]
    if upper_case:
        weekday_name = weekday_name.upper()
    return weekday_name


def get_numeric_month_calendar_list(year: int, month: int) -> list[list]:
    first_day_weekday = datetime(year=year, month=month, day=1).weekday()
    days_in_month = get_days_quantity_in_month(year=year, month=month)
    calendar_list = []
    week = [0] * 7
    for day in range(1, days_in_month + 1):
        week[(first_day_weekday + day - 1) % 7] = day
        if (first_day_weekday + day) % 7 == 0 or day == days_in_month:
            calendar_list.append(week)
            week = [0] * 7
    return calendar_list


def check_day_is_weekend(year: int, month: int, day: int) -> bool:
    weekday_index = get_weekday_index_by_year_month_day(year=year, month=month, day=day)
    return weekday_index in [5, 6]


def get_date_with_month_name(date_value: datetime | date,
                             language: Literal["EN", "RU"] = "EN",
                             upper_case: bool = False) -> str:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    date_string = format_date(date_value, format="long", locale=locale_name)
    if upper_case:
        date_string = date_string.upper()
    return date_string


def get_time_flex_from_datetime(date_value: datetime,
                                language: Literal["EN", "RU"] = "EN",
                                with_seconds: bool = False,
                                separator: str = ":",
                                hrs_and_mns_notation: bool = False,
                                upper_case: bool = False) -> str:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    time_format = "HH:mm:ss" if with_seconds else "HH:mm"
    time_string = format_time(date_value, format=time_format, locale=locale_name)
    if upper_case:
        time_string = time_string.upper()
    return time_string


def get_date_flex_from_datetime(date_value: datetime | date,
                                language: Literal["EN", "RU"] = "EN",
                                separator: str = "-",
                                month_as_name: bool = False,
                                year_abbreviated: bool = False,
                                upper_case: bool = False) -> str:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    date_format = "short" if not month_as_name else "long"
    date_string = format_date(date_value, format=date_format, locale=locale_name)
    if upper_case:
        date_string = date_string.upper()
    return date_string


def get_hours_minutes_secs_timedelta(timedelta_value: timedelta,
                                     language: Literal["EN", "RU"] = "EN",
                                     abbrev_symbols: Literal[1, 3, "1", "3", "full"] = 1,
                                     show_seconds: bool = False,
                                     hide_zero_values: bool = False,
                                     separator: str = ":",
                                     space_before_note: bool = False,
                                     show_period_after_note: bool = False,
                                     upper_case: bool = False) -> str:
    locale_name = "en_US" if language == "EN" else "ru_RU"
    total_seconds = timedelta_value.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    time_parts = []
    if hours or not hide_zero_values:
        time_parts.append(f"{hours}{separator}")
    if minutes or not hide_zero_values:
        time_parts.append(f"{minutes}{separator}")
    if show_seconds and (seconds or not hide_zero_values):
        time_parts.append(f"{seconds}")

    time_string = "".join(time_parts)
    if upper_case:
        time_string = time_string.upper()
    return time_string


def get_weekdays_names_list(abbreviation: bool = False,
                            language: Literal["EN", "RU"] = "EN",
                            upper_case: bool = False) -> list:
    origin_locale = locale.getlocale(locale.LC_TIME)
    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("ru_RU"))

    if abbreviation:
        weekdays_names = dict(enumerate(calendar.day_abbr))
    else:
        weekdays_names = dict(enumerate(calendar.day_name))

    if upper_case:
        result_weekdays_names = []
        for month_key, month_name in weekdays_names.items():
            result_weekdays_names.append(month_name.upper())
    else:
        result_weekdays_names = []
        for month_key, month_name in weekdays_names.items():
            result_weekdays_names.append(month_name)

    locale.setlocale(locale.LC_TIME, locale=origin_locale)
    return result_weekdays_names
