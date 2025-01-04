from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import CONTINUED, HOURS_LABEL, HOUR_LABEL, MINUTES_STEP_LABEL_TEMPLATE, \
    HOURS_STEP_LABEL_TEMPLATE, MINUTES_LABEL, HOUR_STEP_LABEL_TEMPLATE, MINUTE_STEP_LABEL_TEMPLATE


class StartWorkTimeCbData(CallbackData, prefix='work-time-start'):
    time_start: str


class NextStepStartWorkTimeCbData(CallbackData, prefix='work-time-start-next-step'):
    next_step: bool


def add_start_time_work_inl_kbd():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=HOURS_LABEL, callback_data=HOUR_LABEL))

    hours_buttons = []

    for hour_step in range(0, 24):
        if len(str(hour_step)) == 2:
            callback_data = StartWorkTimeCbData(time_start=HOURS_STEP_LABEL_TEMPLATE.format(hour_step))
            hours_buttons.append(InlineKeyboardButton(
                text=HOURS_STEP_LABEL_TEMPLATE.format(hour_step), callback_data=callback_data.pack()))
            continue

        callback_data = StartWorkTimeCbData(time_start=HOUR_STEP_LABEL_TEMPLATE.format(hour_step))
        hours_buttons.append(InlineKeyboardButton(text=HOUR_STEP_LABEL_TEMPLATE.format(hour_step), callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 5):
        builder.row(*hours_buttons[i:i+5])

    builder.row(InlineKeyboardButton(
        text=MINUTES_LABEL, callback_data=MINUTES_LABEL))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        if len(str(minutes_step)) == 2:
            callback_data = StartWorkTimeCbData(time_start=MINUTES_STEP_LABEL_TEMPLATE.format(minutes_step))
            minutes_buttons.append(InlineKeyboardButton(
                text=MINUTES_STEP_LABEL_TEMPLATE.format(minutes_step), callback_data=callback_data.pack()))
            continue

        callback_data = StartWorkTimeCbData(time_start=MINUTE_STEP_LABEL_TEMPLATE.format(minutes_step))
        minutes_buttons.append(InlineKeyboardButton(text=MINUTE_STEP_LABEL_TEMPLATE.format(minutes_step), callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    callback_data = NextStepStartWorkTimeCbData(next_step=True)
    builder.row(InlineKeyboardButton(text=CONTINUED, callback_data=callback_data.pack()))

    return builder.as_markup()
