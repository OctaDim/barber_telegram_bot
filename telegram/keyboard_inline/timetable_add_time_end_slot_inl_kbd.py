from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import CONTINUED


class NewTimeEndSlotTimetableCbData(CallbackData, prefix='time-end-slot-timetable'):
    time_end: str


class NextStepEndTimeSlotTimetableCbData(CallbackData, prefix='next-step-time-end'):
    next_step: bool


def add_new_time_end_slot():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='hours', callback_data='Hour'))

    hours_buttons = []

    for hour_step in range(0, 24):
        if len(str(hour_step)) == 2:
            callback_data = NewTimeEndSlotTimetableCbData(time_end=f'{hour_step}h')
            hours_buttons.append(InlineKeyboardButton(text=f'{hour_step}h', callback_data=callback_data.pack()))
            continue

        callback_data = NewTimeEndSlotTimetableCbData(time_end=f'0{hour_step}h')
        hours_buttons.append(InlineKeyboardButton(text=f'0{hour_step}h', callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 5):
        builder.row(*hours_buttons[i:i + 5])

    builder.row(InlineKeyboardButton(text='minutes', callback_data='Minutes'))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        if len(str(minutes_step)) == 2:
            callback_data = NewTimeEndSlotTimetableCbData(time_end=f"{minutes_step}m")
            minutes_buttons.append(InlineKeyboardButton(text=f"{minutes_step}m", callback_data=callback_data.pack()))
            continue

        callback_data = NewTimeEndSlotTimetableCbData(time_end=f"0{minutes_step}m")
        minutes_buttons.append(InlineKeyboardButton(text=f"0{minutes_step}m", callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    callback_data = NextStepEndTimeSlotTimetableCbData(next_step=True)
    builder.row(InlineKeyboardButton(text=CONTINUED, callback_data=callback_data.pack()))

    return builder.as_markup()
