from aiogram.utils.keyboard import (InlineKeyboardBuilder)
from aiogram.filters.callback_data import CallbackData

from database.db_queries.user_queries import get_services_list

from telegram.params.button_services_action import BUTTON_SERVICES_ACTION


class ChangeServicesCbData(CallbackData, prefix='change-services'):
    id_services: int


class RemoveServicesCbData(CallbackData, prefix='remove-services'):
    id_services: int


def services_select_inl_kbd(action: bool = False):
    builder = InlineKeyboardBuilder()

    services = get_services_list()
    for elem in services:
        if action:
            callback_data = RemoveServicesCbData(id_services=elem.id)

        else:
            callback_data = ChangeServicesCbData(id_services=elem.id)

        builder.button(text=f'{elem.name} - {elem.price}byn',
                       callback_data=callback_data.pack()
                       )

    builder.adjust(1)
    keyboard = builder.as_markup()

    return keyboard
