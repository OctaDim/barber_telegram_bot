from aiogram.utils.keyboard import (InlineKeyboardBuilder)
from aiogram.filters.callback_data import CallbackData

from database.db_queries.admin_queries import get_one_service


class ChangeServicesCbData(CallbackData, prefix='change-services'):
    id_services: int
    quantity: int


class RemoveServicesCbData(CallbackData, prefix='remove-services'):
    id_services: int


def services_select_inl_kbd(id_service: int, quantity: int = None, action: bool = False):
    builder = InlineKeyboardBuilder()

    service = get_one_service(id_service=id_service)

    if action:
        callback_data = RemoveServicesCbData(id_services=service.id)

    else:
        callback_data = ChangeServicesCbData(id_services=service.id, quantity=quantity)

    builder.button(text='🟩',
                   callback_data=callback_data.pack()
                   )

    builder.adjust(1)
    keyboard = builder.as_markup()

    return keyboard
