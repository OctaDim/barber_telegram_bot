from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from utilities.get_months_calendar import month_list


class MonthWorkTimeCbData(CallbackData, prefix='month-work-time'):
    mount: str


def work_time_month_inl_kbd(date):
    builder = InlineKeyboardBuilder()

    months = month_list(date=date)

    for month in months:
        callback_data = MonthWorkTimeCbData(mount=month)
        builder.button(text=month, callback_data=callback_data.pack())

    builder.adjust(3, 3, 3, 3)
    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
