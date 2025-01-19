from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class AddServiceTimetableCbData(CallbackData, prefix='add-service-timetable'):
    service_id: int
    quantity: int


def get_all_services(id_service: int, quantity: int):
    builder = InlineKeyboardBuilder()

    callback_data = AddServiceTimetableCbData(service_id=id_service, quantity=quantity)

    builder.button(text='Выбрать',
                   callback_data=callback_data.pack()
                   )

    builder.adjust(1)
    keyboard = builder.as_markup()

    return keyboard




