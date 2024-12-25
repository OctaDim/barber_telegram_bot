from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData



class GetBreakIdTimeTableCbData(CallbackData, prefix='get-break_id'):
    break_id: int


def get_action_break_time_inl_kbd(break_id):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text='Сделай время активным',
        callback_data=GetBreakIdTimeTableCbData(break_id=break_id).pack()
    ))

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
