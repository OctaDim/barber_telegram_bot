from datetime import datetime, date

from aiogram.filters.callback_data import CallbackData

from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardMarkup)

from telegram.keyboard_inline.common_cb_data_all_inl_kbds import (
    NoActionCommonCBData,
    ReturnInlineBtnCBData,
    MainMenuInlineBtnCBData)

from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS
from telegram.params.buttons_enroll_service import ENROLL_SERVICE_BUTTONS
from telegram.params.calendar_icons import CALENDAR_ICONS

from telegram.telegram_utils.calendar_utilities import (
    get_month_calendar_list,
    get_month_name_by_number)


class MonthDayCallbackData(CallbackData, prefix="month_day"):
    month_day: int


class PreviousMonthCBData(CallbackData, prefix="previous_month"):
    pass


class NextMonthCBData(CallbackData, prefix="next_month"):
    pass


class MonthContinueCBData(CallbackData, prefix="month_continue"):
    pass


def get_enroll_srcs_calendar_inl_kbd(date_value: datetime | date) -> InlineKeyboardMarkup:
    year = date_value.year
    month = date_value.month

    builder_inl_kbd = InlineKeyboardBuilder()

    builder_inl_kbd.button(
        text=CALENDAR_ICONS.PREVIOUS_MONTH,
        callback_data=PreviousMonthCBData().pack())

    month_name = get_month_name_by_number(month_number=month,
                                          language="RU")
    month_name = month_name.upper()

    builder_inl_kbd.button(
        text=month_name,
        callback_data=NoActionCommonCBData().pack())

    builder_inl_kbd.button(
        text=str(year),
        callback_data=NoActionCommonCBData().pack())

    builder_inl_kbd.button(
        text=CALENDAR_ICONS.NEXT_MONTH,
        callback_data=NextMonthCBData().pack())

    for workday_header_index in range(5):
        builder_inl_kbd.button(
            text=CALENDAR_ICONS.WORKDAY,
            callback_data=NoActionCommonCBData().pack())

    for weekday_header_index in range(2):
        builder_inl_kbd.button(
            text=CALENDAR_ICONS.WEEKEND,
            callback_data=NoActionCommonCBData().pack())

    month_calendar_list = get_month_calendar_list(year, month)
    month_calendar_flat_list = sum(month_calendar_list, [])

    for loop_day in month_calendar_flat_list:

        if loop_day:
            loop_datetime = datetime(year, month, loop_day)
            datetime_now = datetime.now().replace(hour=0, minute=0,
                                                  second=0, microsecond=0)
            if loop_datetime > datetime_now:
                button_text = str(loop_day)
                callback_data = MonthDayCallbackData(month_day=loop_day)
            elif loop_datetime == datetime_now:
                button_text = CALENDAR_ICONS.TODAY + str(loop_day)
                callback_data = MonthDayCallbackData(month_day=loop_day)
            else:
                button_text = "\u200B"
                callback_data = NoActionCommonCBData().pack()
        else:
            button_text = "\u200B"
            callback_data = NoActionCommonCBData().pack()

        builder_inl_kbd.button(text=button_text,
                               callback_data=callback_data)

    builder_inl_kbd.button(
        text=ENROLL_SERVICE_BUTTONS.CONTINUE,
        callback_data=MonthContinueCBData().pack())

    builder_inl_kbd.button(
        text=COMMON_BUTTONS_PARAMS.RETURN,
        callback_data=ReturnInlineBtnCBData().pack())

    builder_inl_kbd.button(
        text=COMMON_BUTTONS_PARAMS.MAIN_MENU,
        callback_data=MainMenuInlineBtnCBData().pack())

    builder_inl_kbd.adjust(4, 7, 7, 7, 7, 7, 7, 1, 2)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
