from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import CONTINUED, hours_label, minutes_label, hour_step_label_template, \
    minute_step_label_template, minutes_step_label_template, hours_step_label_template


class EndWorkTimeCbData(CallbackData, prefix='work-time-end'):
    time_end: str


class NextStepEndWorkTimeCbData(CallbackData, prefix='work-time-end-next-step'):
    next_step: bool


def add_end_time_work_inl_kbd():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=hours_label, callback_data='Hour'))

    hours_buttons = []

    for hour_step in range(0, 24):
        if len(str(hour_step)) == 2:
            callback_data = EndWorkTimeCbData(
                time_end=hours_step_label_template.format(hour_step))
            hours_buttons.append(InlineKeyboardButton(
                text=hours_step_label_template.format(hour_step),
                callback_data=callback_data.pack()))
            continue

        callback_data = EndWorkTimeCbData(
            time_end=hour_step_label_template.format(hour_step))
        hours_buttons.append(InlineKeyboardButton(
            text=hour_step_label_template.format(hour_step),
            callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 5):
        builder.row(*hours_buttons[i:i+5])

    builder.row(InlineKeyboardButton(text=minutes_label, callback_data='Minutes'))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        if len(str(minutes_step)) == 2:
            callback_data = EndWorkTimeCbData(
                time_end=minutes_step_label_template.format(minutes_step))
            minutes_buttons.append(InlineKeyboardButton(
                text=minutes_step_label_template.format(minutes_step),
                callback_data=callback_data.pack()))
            continue

        callback_data = EndWorkTimeCbData(
            time_end=minute_step_label_template.format(minutes_step))
        minutes_buttons.append(InlineKeyboardButton(
            text=minute_step_label_template.format(minutes_step),
            callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    callback_data = NextStepEndWorkTimeCbData(next_step=True)
    builder.row(InlineKeyboardButton(text=CONTINUED, callback_data=callback_data.pack()))

    return builder.as_markup()

