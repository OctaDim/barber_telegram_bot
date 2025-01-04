from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import CONTINUED, minutes_label, hours_step_label_template, \
    hour_step_label_template, hour_label, minutes_step_label_template, minute_step_label_template, continue_button_text


class NewTimeEndSlotTimetableCbData(CallbackData, prefix='time-end-slot-timetable'):
    time_end: str


class NextStepEndTimeSlotTimetableCbData(CallbackData, prefix='next-step-time-end'):
    next_step: bool


def add_new_time_end_slot():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=hour_label, callback_data='Hour'))

    hours_buttons = []

    for hour_step in range(0, 24):
        if len(str(hour_step)) == 2:
            time_end = hours_step_label_template.format(hour_step)
            callback_data = NewTimeEndSlotTimetableCbData(time_end=time_end)
            hours_buttons.append(InlineKeyboardButton(text=time_end, callback_data=callback_data.pack()))
            continue

        time_end = hour_step_label_template.format(hour_step)
        callback_data = NewTimeEndSlotTimetableCbData(time_end=time_end)
        hours_buttons.append(InlineKeyboardButton(text=time_end, callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 5):
        builder.row(*hours_buttons[i:i + 5])

    builder.row(InlineKeyboardButton(text=minutes_label, callback_data='Minutes'))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        if len(str(minutes_step)) == 2:
            time_end = minutes_step_label_template.format(minutes_step)
            callback_data = NewTimeEndSlotTimetableCbData(time_end=time_end)
            minutes_buttons.append(InlineKeyboardButton(text=time_end, callback_data=callback_data.pack()))
            continue

        time_end = minute_step_label_template.format(minutes_step)
        callback_data = NewTimeEndSlotTimetableCbData(time_end=time_end)
        minutes_buttons.append(InlineKeyboardButton(text=time_end, callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    callback_data = NextStepEndTimeSlotTimetableCbData(next_step=True)
    builder.row(InlineKeyboardButton(text=continue_button_text, callback_data=callback_data.pack()))

    return builder.as_markup()
