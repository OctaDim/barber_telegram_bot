from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.keyboard_inline.work_time_add_month_inl_kbd import MonthWorkTimeCbData
from telegram.params.work_time_cb_data_message import CONTINUED, RETURN


class HoursIntervalWorkTimeCbData(CallbackData, prefix='hours-work-time-interval'):
    time: str


class IntervalNextStepTimeWorkTimeCbData(CallbackData, prefix='service-end-time-interval'):
    next_step: bool


def add_interval_work_time_services_inl_kbd(mount: str, year: int):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Часы", callback_data="hour"))

    hours_buttons = []
    for hours_step in range(0, 12):
        callback_data = HoursIntervalWorkTimeCbData(time=f"{hours_step}h")

        hours_buttons.append(InlineKeyboardButton(text=f"{hours_step}h", callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 4):
        builder.row(*hours_buttons[i:i + 4])

    builder.row(InlineKeyboardButton(text="Минуты", callback_data="minutes"))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        callback_data = HoursIntervalWorkTimeCbData(time=f"{minutes_step}m")

        minutes_buttons.append(InlineKeyboardButton(text=f"{minutes_step}m", callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    buttons = [
        InlineKeyboardButton(
            text=RETURN,
            callback_data=MonthWorkTimeCbData(mount=mount, year=year).pack()
        ),
        InlineKeyboardButton(
            text=CONTINUED,
            callback_data=IntervalNextStepTimeWorkTimeCbData(next_step=True).pack()
        )
    ]

    builder.row(*buttons)

    return builder.as_markup()
