from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class HoursWorkTimeCbData(CallbackData, prefix='hours-work-time'):
    time: str


class ServiceDurationTimeWorkTimeCbData(CallbackData, prefix='service-end-time'):
    next_step: bool


def add_hours_work_time_services_inl_kbd(block_hour: list = None):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Часы", callback_data="hour"))

    hours_buttons = []
    for hours_step in range(7, 23):
        if block_hour:
            if hours_step in block_hour:
                hours_buttons.append(InlineKeyboardButton(text='-', callback_data='-'))
                continue

        callback_data = HoursWorkTimeCbData(time=f"{hours_step}h")

        hours_buttons.append(InlineKeyboardButton(text=f"{hours_step}h", callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 4):
        builder.row(*hours_buttons[i:i+4])

    builder.row(InlineKeyboardButton(text="Минуты", callback_data="minutes"))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        callback_data = HoursWorkTimeCbData(time=f"{minutes_step}m")

        minutes_buttons.append(InlineKeyboardButton(text=f"{minutes_step}m", callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i+4])

    callback_data = ServiceDurationTimeWorkTimeCbData(next_step=True)
    builder.row(InlineKeyboardButton(text='Продолжить', callback_data=callback_data.pack()))

    return builder.as_markup()
