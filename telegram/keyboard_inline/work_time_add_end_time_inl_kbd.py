from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import CONTINUED, HOURS_LABEL, MINUTES_LABEL, HOUR_STEP_LABEL_TEMPLATE, \
    MINUTE_STEP_LABEL_TEMPLATE, MINUTES_STEP_LABEL_TEMPLATE, HOURS_STEP_LABEL_TEMPLATE


class EndWorkTimeCbData(CallbackData, prefix='work-time-end'):
    time_end: str


class NextStepEndWorkTimeCbData(CallbackData, prefix='work-time-end-next-step'):
    next_step: bool


def add_end_time_work_inl_kbd():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=HOURS_LABEL, callback_data='Hour'))

    hours_buttons = []

    for hour_step in range(0, 24):
        if len(str(hour_step)) == 2:
            callback_data = EndWorkTimeCbData(
                time_end=HOURS_STEP_LABEL_TEMPLATE.format(hour_step))
            hours_buttons.append(InlineKeyboardButton(
                text=HOURS_STEP_LABEL_TEMPLATE.format(hour_step),
                callback_data=callback_data.pack()))
            continue

        callback_data = EndWorkTimeCbData(
            time_end=HOUR_STEP_LABEL_TEMPLATE.format(hour_step))
        hours_buttons.append(InlineKeyboardButton(
            text=HOUR_STEP_LABEL_TEMPLATE.format(hour_step),
            callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 5):
        builder.row(*hours_buttons[i:i+5])

    builder.row(InlineKeyboardButton(text=MINUTES_LABEL, callback_data='Minutes'))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        if len(str(minutes_step)) == 2:
            callback_data = EndWorkTimeCbData(
                time_end=MINUTES_STEP_LABEL_TEMPLATE.format(minutes_step))
            minutes_buttons.append(InlineKeyboardButton(
                text=MINUTES_STEP_LABEL_TEMPLATE.format(minutes_step),
                callback_data=callback_data.pack()))
            continue

        callback_data = EndWorkTimeCbData(
            time_end=MINUTE_STEP_LABEL_TEMPLATE.format(minutes_step))
        minutes_buttons.append(InlineKeyboardButton(
            text=MINUTE_STEP_LABEL_TEMPLATE.format(minutes_step),
            callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    callback_data = NextStepEndWorkTimeCbData(next_step=True)
    builder.row(InlineKeyboardButton(text=CONTINUED, callback_data=callback_data.pack()))

    return builder.as_markup()
