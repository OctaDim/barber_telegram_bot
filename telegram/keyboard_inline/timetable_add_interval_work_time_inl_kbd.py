from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import CONTINUED


class AddIntervalWorkTimeCbData(CallbackData, prefix='add-work-time-interval'):
    time: str


class AddIntervalNextStepTimeWorkTimeCbData(CallbackData, prefix='add-service-end-time-interval'):
    next_step: bool



def add_work_time_interval_inl_kbd():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Часы", callback_data="hour"))

    hours_buttons = []
    for hours_step in range(0, 12):
        callback_data = AddIntervalWorkTimeCbData(time=f"{hours_step}h")

        hours_buttons.append(InlineKeyboardButton(text=f"{hours_step}h", callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 4):
        builder.row(*hours_buttons[i:i + 4])

    builder.row(InlineKeyboardButton(text="Минуты", callback_data="minutes"))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        callback_data = AddIntervalWorkTimeCbData(time=f"{minutes_step}m")

        minutes_buttons.append(InlineKeyboardButton(text=f"{minutes_step}m", callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    buttons = [
        InlineKeyboardButton(
            text='Return',
            callback_data='dadsa'
        ),
        InlineKeyboardButton(
            text=CONTINUED,
            callback_data=AddIntervalNextStepTimeWorkTimeCbData(next_step=True).pack()
        )
    ]

    builder.row(*buttons)

    return builder.as_markup()
