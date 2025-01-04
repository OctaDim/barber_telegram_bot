from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.keyboard_inline.timetable_get_day_inl_kbd import NextStepDaysTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL, CONTINUE_BUTTON_TXT


class CurrentTimeStartWorkTimeCbData(CallbackData, prefix='new-time-start-work-time'):
    pass


class CurrentTimeEndWorkTimeCbData(CallbackData, prefix='new-end-time-work-time'):
    pass


class NextStepAddNewWorkTimeCbData(CallbackData, prefix='next-step-add-new-work-time'):
    pass


def add_more_work_time_inl_kbd(time_start: datetime, time_end: datetime):
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=time_start.time().strftime('%H:%M'),
            callback_data=CurrentTimeStartWorkTimeCbData().pack()
        ),
        InlineKeyboardButton(
            text='-',
            callback_data='-'
        ),
        InlineKeyboardButton(
            text=time_end.time().strftime('%H:%M'),
            callback_data=CurrentTimeEndWorkTimeCbData().pack()
        )
    ]

    builder.row(*buttons)

    buttons = [
        InlineKeyboardButton(
            text=RETURN,
            callback_data=NextStepDaysTimetableCbData(
                next_step=True).pack()
        ),
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    ]

    builder.row(InlineKeyboardButton(
            text=CONTINUE_BUTTON_TXT,
            callback_data=NextStepAddNewWorkTimeCbData().pack()
        ))

    builder.row(*buttons)

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
