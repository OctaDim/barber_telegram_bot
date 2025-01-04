from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import CONTINUED, MINUTES_LABEL, HOURS_STEP_LABEL_TEMPLATE, \
    HOUR_STEP_LABEL_TEMPLATE, HOUR_LABEL, MINUTES_STEP_LABEL_TEMPLATE, MINUTE_STEP_LABEL_TEMPLATE, CONTINUE_BUTTON_TXT


class NewTimeEndSlotTimetableCbData(CallbackData, prefix='time-end-slot-timetable'):
    time_end: str


class NextStepEndTimeSlotTimetableCbData(CallbackData, prefix='next-step-time-end'):
    next_step: bool


def add_new_time_end_slot():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=HOUR_LABEL, callback_data='Hour'))

    hours_buttons = []

    for hour_step in range(0, 24):
        if len(str(hour_step)) == 2:
            time_end = HOURS_STEP_LABEL_TEMPLATE.format(hour_step)
            callback_data = NewTimeEndSlotTimetableCbData(time_end=time_end)
            hours_buttons.append(InlineKeyboardButton(text=time_end, callback_data=callback_data.pack()))
            continue

        time_end = HOUR_STEP_LABEL_TEMPLATE.format(hour_step)
        callback_data = NewTimeEndSlotTimetableCbData(time_end=time_end)
        hours_buttons.append(InlineKeyboardButton(text=time_end, callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 5):
        builder.row(*hours_buttons[i:i + 5])

    builder.row(InlineKeyboardButton(text=MINUTES_LABEL, callback_data='Minutes'))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        if len(str(minutes_step)) == 2:
            time_end = MINUTES_STEP_LABEL_TEMPLATE.format(minutes_step)
            callback_data = NewTimeEndSlotTimetableCbData(time_end=time_end)
            minutes_buttons.append(InlineKeyboardButton(text=time_end, callback_data=callback_data.pack()))
            continue

        time_end = MINUTE_STEP_LABEL_TEMPLATE.format(minutes_step)
        callback_data = NewTimeEndSlotTimetableCbData(time_end=time_end)
        minutes_buttons.append(InlineKeyboardButton(text=time_end, callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    callback_data = NextStepEndTimeSlotTimetableCbData(next_step=True)
    builder.row(InlineKeyboardButton(text=CONTINUE_BUTTON_TXT, callback_data=callback_data.pack()))

    return builder.as_markup()
