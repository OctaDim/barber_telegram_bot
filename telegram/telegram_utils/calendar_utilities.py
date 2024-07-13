import calendar
import locale

from typing import Literal

from datetime import datetime, date

from dateutil.relativedelta import relativedelta


def get_next_months_numbers_from_now(required_months_number: int) -> list:
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


def get_weekdays_eng_abbr_list() -> list:
    weekdays_abbr_list = calendar.weekheader(3).split()
    return weekdays_abbr_list


def get_weekday_eng_abbr_by_index(weekday_index: int) -> str:
    weekdays_abbr_list = get_weekdays_eng_abbr_list()
    weekday_abbr = weekdays_abbr_list[weekday_index]
    return weekday_abbr


def get_weekday_eng_abbr_by_date(date_value: date|datetime) -> str:
    weekdays_abbr_list = get_weekdays_eng_abbr_list()
    weekday_number = get_weekday_index_by_date(date_value)
    weekday_abbr = weekdays_abbr_list[weekday_number]
    return weekday_abbr


def get_month_days_quantity(year: int, month: int) -> int:
    month_days_quantity = calendar.monthrange(year=year, month=month)[1]
    return month_days_quantity


def get_month_start_weekday_index(year: int, month: int) -> int:
    month_start_weekday = calendar.monthrange(year=year, month=month)[0]
    return month_start_weekday


def get_month_names_dict(abbreviation: bool = False,
                         language: Literal["EN","RU"] = "EN") -> dict:

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
                             language: Literal["EN","RU"] = "EN") -> str:

    origin_locale = locale.getlocale(locale.LC_TIME)

    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    if abbreviation:
        month_name = calendar.month_abbr[month_number]
    else:
        month_name = calendar.month_name[month_number]

    locale.setlocale(locale.LC_TIME, locale=origin_locale)

    return month_name


def get_weekdays_names_dict(abbreviation: bool = False,
                            language: Literal["EN","RU"] = "EN") -> dict:

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
                              language: Literal["EN","RU"] = "EN") -> str:

    origin_locale = locale.getlocale(locale.LC_TIME)

    if language == "RU":
        locale.setlocale(locale.LC_TIME, locale=("Russian_Russia", "1251"))

    if abbreviation:
        weekday_name = calendar.day_abbr[weekday_index]
    else:
        weekday_name = calendar.day_name[weekday_index]

    locale.setlocale(locale.LC_TIME, locale=origin_locale)

    return weekday_name


def get_month_calendar_list(year: int, month: int) -> list[list]:
    month_calendar_list = calendar.monthcalendar(year=year, month=month)
    return month_calendar_list


def get_first_weekday_index():
    return calendar.firstweekday()


def check_day_is_weekend(year: int, month: int, day: int) -> bool:
    weekday_index = get_weekday_index_by_year_month_day(year, month, day)
    day_is_weekend: bool = weekday_index in [5, 6]
    return day_is_weekend
