from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


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
            text='Return',
            callback_data='dsa'
        ),
        InlineKeyboardButton(
            text='Continue',
            callback_data=NextStepAddNewWorkTimeCbData().pack()
        )
    ]

    builder.row(*buttons)

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
