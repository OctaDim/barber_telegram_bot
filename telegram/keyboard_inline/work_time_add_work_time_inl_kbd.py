from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from datetime import timedelta

from telegram.params.work_time_cb_data_message import CONTINUED


class StartWorkCbData(CallbackData, prefix='start-work'):
    time: str


class EndWorkCbData(CallbackData, prefix='end-work'):
    time: str


class NextStepAddWorkTime(CallbackData, prefix='Next-Step-Add-Work-Time'):
    next_step: bool


def add_work_time_inl_kbd(time_start=timedelta(hours=00, minutes=00), time_end=timedelta(hours=00, minutes=00)):
    builder = InlineKeyboardBuilder()

    time_start = f"{time_start.seconds // 3600:02}:{(time_start.seconds // 60) % 60:02}"
    time_end = f"{time_end.seconds // 3600:02}:{(time_end.seconds // 60) % 60:02}"

    callback_data = StartWorkCbData(time=f'time_start')
    builder.button(text=f'{time_start}', callback_data=callback_data.pack())

    builder.button(text='-', callback_data='-')

    callback_data = EndWorkCbData(time=f'time_end')
    builder.button(text=f'{time_end}', callback_data=callback_data.pack())

    builder.adjust(3)

    callback_data = NextStepAddWorkTime(next_step=True)
    builder.row(InlineKeyboardButton(text=CONTINUED, callback_data=callback_data.pack()))

    return builder.as_markup()
