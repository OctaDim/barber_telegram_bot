from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from utilities.get_months_calendar import get_month_dict


class MonthWorkTimeCbData(CallbackData, prefix='month-work-time'):
    mount: str
    year: int


class YearWorkTimeCbData(CallbackData, prefix='year-work-time'):
    year: int
    action: str


def work_time_month_inl_kbd(month, year):
    builder = InlineKeyboardBuilder()

    first_row = [
        InlineKeyboardButton(text='<<', callback_data=YearWorkTimeCbData(year=year, action='back').pack()),
        InlineKeyboardButton(text=f'{year}', callback_data=f'{year}'),
        InlineKeyboardButton(text='>>', callback_data=YearWorkTimeCbData(year=year, action='next').pack()),
    ]

    builder.row(*first_row)

    months = get_month_dict(month=month)

    for key, value in months.items():
        if value:
            callback_data = MonthWorkTimeCbData(mount=key, year=year)
            builder.button(text=key, callback_data=callback_data.pack())

            continue

        builder.button(text='-', callback_data='-')

    callback_data = BackToAdminMenuTimetableCbData(active=True).pack()
    builder.row(InlineKeyboardButton(text='Return', callback_data=callback_data))

    builder.adjust(3, 3, 3, 3)
    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
