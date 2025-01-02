from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.buttons_add_services import BUTTONS_ADD_SERVICES


class AddNewAddressCbData(CallbackData, prefix='add-new-address'):
    pass


class RemoveAddressCbData(CallbackData, prefix='remove-address'):
    pass


def get_action_by_address():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text=f'{BUTTONS_ADD_SERVICES.ADD} | '
             f'{BUTTONS_ADD_SERVICES.CHANGE_SERVICE}',
        callback_data=AddNewAddressCbData().pack()
    ))

    builder.row(InlineKeyboardButton(
        text=BUTTONS_ADD_SERVICES.REMOVE_SERVICE,
        callback_data=RemoveAddressCbData().pack()
    ))

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
