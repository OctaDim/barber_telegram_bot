from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import HOURS_LABEL, MINUTES_LABEL, CONTINUE_BUTTON_TXT


class TimeServicesWorkTimeCbData(CallbackData, prefix='start-time-work-time'):
    time_start: str


class AddServiceDurationWorkTimeCbData(CallbackData, prefix='add-duration-time'):
    next_step: bool


def add_duration_services_work_time_services_inl_kbd(time_start: list = None):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=HOURS_LABEL, callback_data="hour"))

    hours_buttons = []
    for hours_step in range(1, 17):
        callback_data = TimeServicesWorkTimeCbData(time_start=f"{hours_step}h")

        hours_buttons.append(InlineKeyboardButton(text=f"{hours_step}h", callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 4):
        builder.row(*hours_buttons[i:i+4])

    builder.row(InlineKeyboardButton(text=MINUTES_LABEL, callback_data="minutes"))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        callback_data = TimeServicesWorkTimeCbData(time_start=f"{minutes_step}m")

        minutes_buttons.append(InlineKeyboardButton(text=f"{minutes_step}m", callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i+4])

    callback_data = AddServiceDurationWorkTimeCbData(next_step=True)
    builder.row(InlineKeyboardButton(text=CONTINUE_BUTTON_TXT, callback_data=callback_data.pack()))

    return builder.as_markup()
