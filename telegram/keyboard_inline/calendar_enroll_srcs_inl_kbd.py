from datetime import datetime

from aiogram.filters.callback_data import (
    CallbackData)
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup)

from telegram.config.configs import (
    LANGUAGE_CONFIGS, CALENDAR_CONFIGS)
from telegram.keyboard_inline.common_buttons_inline import (
    create_return_inline_button,
    NoActionEmptyCBData,
    create_main_menu_inline_button,
    create_empty_no_action_inl_btn)
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS
from telegram.params.buttons_enroll_calendar import ENROLL_CALENDAR_BUTTONS
from telegram.params.icons_calendar import (
    CALENDAR_ICONS)
from utilities.calendar_utils import (
    get_numeric_month_calendar_list,
    get_month_name_by_number,
    get_weekday_flex_abbr_by_index)


class PreviousMonthCBData(CallbackData, prefix="prev_month_enroll_srcs"):
    pass


class MonthNameCBData(CallbackData, prefix="month_name_enroll_srcs"):
    pass


class YearNameCBData(CallbackData, prefix="year_name_enroll_srcs"):
    pass


class NextMonthCBData(CallbackData, prefix="next_month_enroll_srcs"):
    pass


class MonthDayCBData(CallbackData, prefix="month_day_enroll_srcs"):
    month_day: int


class MonthContinueCBData(CallbackData, prefix="calendar_continue_enroll_srcs"):
    pass


class ReturnCalendarToSrcsFilteredCBData(CallbackData, prefix="return_calendar_to_srcs_filtered"):
    pass


def get_calendar_enroll_srcs_inl_kbd(
        calendar_year: int,
        calendar_month: int,
        enrollment_days: list = None,
        selected_date: datetime = None
) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if not CALENDAR_CONFIGS.MONTH_AND_YEAR_IN_ONE_BUTTON:
        builder_inl_kbd.button(
            text=f"{calendar_year}",
            callback_data=YearNameCBData())

    builder_inl_kbd.button(
        text=CALENDAR_ICONS.TO_PREVIOUS_MONTH,
        callback_data=PreviousMonthCBData())

    month_name = get_month_name_by_number(
        month_number=calendar_month,
        abbreviation=CALENDAR_CONFIGS.MONTH_AND_YEAR_IN_ONE_BUTTON,
        upper_case=CALENDAR_CONFIGS.MONTH_NAME_UPPER_CASE,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    if CALENDAR_CONFIGS.MONTH_AND_YEAR_IN_ONE_BUTTON:
        builder_inl_kbd.button(
            text=f"{month_name}"
                 f"{ENROLL_CALENDAR_BUTTONS.MONTH_YEAR_BTN_SEPARATOR}"
                 f"{calendar_year}",
            callback_data=MonthNameCBData())
    else:
        builder_inl_kbd.button(
            text=f"{month_name}",
            callback_data=MonthNameCBData())

    builder_inl_kbd.button(
        text=CALENDAR_ICONS.TO_NEXT_MONTH,
        callback_data=NextMonthCBData())

    for weekday_index in range(7):
        weekday_abbreviation = get_weekday_flex_abbr_by_index(
            weekday_index=weekday_index,
            language=LANGUAGE_CONFIGS.LANGUAGE,
            symbols_max=2,
            upper_case=CALENDAR_CONFIGS.WEEKDAYS_ABBR_UPPER_CASE)

        if not CALENDAR_CONFIGS.SHOW_WEEKDAY_ICONS:
            month_txt = weekday_abbreviation
        elif weekday_index > 4:
            month_txt = f"{weekday_abbreviation}{CALENDAR_ICONS.WEEKEND}"
        else:
            month_txt = f"{weekday_abbreviation}{CALENDAR_ICONS.WORKDAY}"

        builder_inl_kbd.button(
            text=month_txt,
            callback_data=NoActionEmptyCBData())

    month_calendar_list = get_numeric_month_calendar_list(calendar_year,
                                                          calendar_month)

    # Removing from calendar not available empty weeks before actual date
    # if (calendar_month == datetime.now().month
    #         and calendar_year == datetime.now().year):
    #     month_calendar_truncated = month_calendar_list.copy()
    #     for week_index in range(len(month_calendar_list)):
    #         if datetime.now().day not in month_calendar_list[week_index]:
    #             month_calendar_truncated.pop(0)
    #         else:
    #             month_calendar_list = month_calendar_truncated
    #             break

    month_calendar_flat_list = sum(month_calendar_list, [])

    for loop_day in month_calendar_flat_list:

        if loop_day and loop_day in enrollment_days:
            loop_datetime = datetime(calendar_year, calendar_month, loop_day)
            datetime_now = datetime.now().replace(hour=0, minute=0,
                                                  second=0, microsecond=0)

            if selected_date and loop_datetime == selected_date:
                button_text = (f"{CALENDAR_ICONS.SELECTED}"
                               f"{loop_day}")
                callback_data = MonthDayCBData(month_day=loop_day)
                builder_inl_kbd.button(text=button_text,
                                       callback_data=callback_data.pack())

            elif loop_datetime > datetime_now:
                button_text = (f"{CALENDAR_ICONS.UNSELECTED_DAY}"
                               f"{loop_day}")
                callback_data = MonthDayCBData(month_day=loop_day)
                builder_inl_kbd.button(text=button_text,
                                       callback_data=callback_data.pack())

            elif loop_datetime == datetime_now:
                button_text = (f"{CALENDAR_ICONS.TODAY_DATE}"
                               f"{loop_day}")
                callback_data = MonthDayCBData(month_day=loop_day)
                builder_inl_kbd.button(text=button_text,
                                       callback_data=callback_data.pack())

            else:  # if loop_datetime < datetime_now (empty days before today)
                builder_inl_kbd.add(create_empty_no_action_inl_btn())

        else:
            builder_inl_kbd.add(create_empty_no_action_inl_btn())

    if selected_date:
        continue_adjust = [1]
        builder_inl_kbd.button(
            text=ENROLL_CALENDAR_BUTTONS.CONTINUE,
            callback_data=MonthContinueCBData().pack())
    else:
        continue_adjust = []

    builder_inl_kbd.button(
        text=COMMON_BUTTONS_PARAMS.RETURN,
        callback_data=ReturnCalendarToSrcsFilteredCBData().pack())
    # builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    year_adjust = [] if CALENDAR_CONFIGS.MONTH_AND_YEAR_IN_ONE_BUTTON else [1]

    work_weeks_number = len(month_calendar_flat_list) // 7
    dynamic_adjust = year_adjust + [3, 7] + [7] * work_weeks_number + continue_adjust + [2]
    # dynamic_adjust = [1, 3, 7] + [7] * work_weeks_number + continue_adjust + [2]
    builder_inl_kbd.adjust(*dynamic_adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
