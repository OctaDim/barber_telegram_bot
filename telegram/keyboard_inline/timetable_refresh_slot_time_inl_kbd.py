from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class TimeStartSlotTimetableCbData(CallbackData, prefix='time-start-slot'):
    action: bool


class TimeEndSlotTimetableCbData(CallbackData, prefix='time-end-slot'):
    action: bool


class ContinueRefreshSlotTimeCbData(CallbackData, prefix='continue-refresh-slot-time'):
    active: bool


def refresh_slot_time_inl_kbd(time_start: datetime = None, time_end: datetime = None):
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=f'{time_start.time().isoformat(timespec='minutes')}',
            callback_data=TimeStartSlotTimetableCbData(action=True).pack()
        ),
        InlineKeyboardButton(
            text='-',
            callback_data='-'
        ),
        InlineKeyboardButton(
            text=f'{time_end.time().isoformat(timespec='minutes')}',
            callback_data=TimeEndSlotTimetableCbData(action=True).pack()
        )
    ]

    builder.row(*buttons)

    callback_data = ContinueRefreshSlotTimeCbData(active=True).pack()
    builder.row(
        InlineKeyboardButton(text='Continue', callback_data=callback_data)
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
