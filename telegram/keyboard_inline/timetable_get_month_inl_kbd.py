from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from database.db_queries.work_time_queries import get_working_time_month_by_month_by_year
from telegram.params.work_time_cb_data_message import RETURN, PRIOR_PAGE, NEXT_PAGE
from utilities.get_month_calendar_for_timetable import get_month_dict_for_timetable


class YearTimetableCbData(CallbackData, prefix='year-timetable'):
    year: int
    action: str


class MonthTimetableCbData(CallbackData, prefix='month-timetable'):
    month: int
    year: int


class BackToAdminMenuTimetableCbData(CallbackData, prefix='back-admin-menu-timetable'):
    active: bool


def timetable_get_month_inl_kbd(
        year: int,
        month: int,
        telegram_id: int
):
    builder = InlineKeyboardBuilder()

    first_row = [
        InlineKeyboardButton(text='<<', callback_data=YearTimetableCbData(year=year, action=PRIOR_PAGE).pack()),
        InlineKeyboardButton(text=f'{year}', callback_data=f'{year}'),
        InlineKeyboardButton(text='>>', callback_data=YearTimetableCbData(year=year, action=NEXT_PAGE).pack()),
    ]

    builder.row(*first_row)

    months = get_month_dict_for_timetable(
        month=get_working_time_month_by_month_by_year(
                                            year=year,
                                            telegram_id=telegram_id),
        current_month=month)

    for key, value in months.items():
        if value:
            callback_data = MonthTimetableCbData(month=int(value), year=year)
            builder.button(text=key, callback_data=callback_data.pack())

            continue

        builder.button(text='-', callback_data=str(value))

    builder.adjust(3, 3, 3, 3)

    callback_data = BackToAdminMenuTimetableCbData(active=True).pack()
    builder.row(InlineKeyboardButton(text=RETURN, callback_data=callback_data))

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
