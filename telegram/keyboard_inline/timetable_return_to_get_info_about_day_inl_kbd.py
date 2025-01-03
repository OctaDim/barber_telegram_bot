from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.keyboard_inline.timetable_get_day_inl_kbd import NextStepDaysTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL


def return_to_get_info_about_day():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=RETURN,
            callback_data=NextStepDaysTimetableCbData(
                next_step=True).pack()
        ),
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
