from datetime import timedelta

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.params.work_time_cb_data_message import CONTINUE_BUTTON_TXT, YES_LABEL, NO_LABEL


class AddBreakResponseWorkTimeCbData(CallbackData, prefix='add-break-response-work-time'):
    response: str


class AddStartBreakWorkTime(CallbackData, prefix='add-start-break-work-time'):
    action: bool


class AddEndBreakWorkTime(CallbackData, prefix='add-end-break-work-time'):
    action: bool


class NextStepAddBreakWorkTime(CallbackData, prefix='next-step-add-break-work-time'):
    next_step: bool


def add_break_or_not_inl_kbd():
    builder = InlineKeyboardBuilder()

    cb_data = AddBreakResponseWorkTimeCbData(response=YES_LABEL)
    builder.button(text=YES_LABEL, callback_data=cb_data.pack())

    cb_data = AddBreakResponseWorkTimeCbData(response=NO_LABEL)
    builder.button(text=NO_LABEL, callback_data=cb_data.pack())

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup


def add_break_work_time_inl_kbd(time_start_break=timedelta(hours=00, minutes=00),
                                time_end_break=timedelta(hours=00, minutes=00)):
    builder = InlineKeyboardBuilder()

    time_start = f"{time_start_break.seconds // 3600:02}:{(time_start_break.seconds // 60) % 60:02}"
    time_end = f"{time_end_break.seconds // 3600:02}:{(time_end_break.seconds // 60) % 60:02}"

    callback_data = AddStartBreakWorkTime(action=True)
    builder.button(text=f'{time_start}', callback_data=callback_data.pack())

    builder.button(text='-', callback_data='-')

    callback_data = AddEndBreakWorkTime(action=True)
    builder.button(text=f'{time_end}', callback_data=callback_data.pack())

    builder.adjust(3)

    callback_data = NextStepAddBreakWorkTime(next_step=True)
    builder.row(InlineKeyboardButton(text=CONTINUE_BUTTON_TXT, callback_data=callback_data.pack()))

    return builder.as_markup()
