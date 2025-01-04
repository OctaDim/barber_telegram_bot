from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import CONTINUED, minutes_step_label_template, \
    minute_step_label_template, continue_button_text, hour_step_label_template, minutes_label, \
    hours_step_label_template, hour_label


class NewTimeStartSlotTimetableCbData(CallbackData, prefix='time-start-slot-timetable'):
    time_start: str


class NextStepStartTimeSlotTimetableCbData(CallbackData, prefix='next-step-time-start'):
    next_step: bool


def add_new_time_start_slot():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=hour_label, callback_data='Hour'))

    hours_buttons = []

    for hour_step in range(0, 24):
        if len(str(hour_step)) == 2:
            time_start = hours_step_label_template.format(hour_step)
            callback_data = NewTimeStartSlotTimetableCbData(time_start=time_start)
            hours_buttons.append(InlineKeyboardButton(text=time_start, callback_data=callback_data.pack()))
            continue

        time_start = hour_step_label_template.format(hour_step)
        callback_data = NewTimeStartSlotTimetableCbData(time_start=time_start)
        hours_buttons.append(InlineKeyboardButton(text=time_start, callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 5):
        builder.row(*hours_buttons[i:i + 5])

    builder.row(InlineKeyboardButton(text=minutes_label, callback_data='Minutes'))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        if len(str(minutes_step)) == 2:
            time_start = minutes_step_label_template.format(minutes_step)
            callback_data = NewTimeStartSlotTimetableCbData(time_start=time_start)
            minutes_buttons.append(InlineKeyboardButton(text=time_start, callback_data=callback_data.pack()))
            continue

        time_start = minute_step_label_template.format(minutes_step)
        callback_data = NewTimeStartSlotTimetableCbData(time_start=time_start)
        minutes_buttons.append(InlineKeyboardButton(text=time_start, callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    callback_data = NextStepStartTimeSlotTimetableCbData(next_step=True)
    builder.row(InlineKeyboardButton(text=continue_button_text, callback_data=callback_data.pack()))

    return builder.as_markup()
