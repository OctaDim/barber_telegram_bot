from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.keyboard_inline.timetable_get_day_inl_kbd import NextStepDaysTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.timetable_cb_data_message import make_time_active_label
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL


class GetBreakIdTimeTableCbData(CallbackData, prefix='get-break_id'):
    break_id: int


def get_action_break_time_inl_kbd(break_id):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text=make_time_active_label,
        callback_data=GetBreakIdTimeTableCbData(break_id=break_id).pack()
    ))

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
