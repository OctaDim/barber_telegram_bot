from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.buttons_add_services import BUTTONS_ADD_SERVICES
from telegram.params.buttons_change_services import BUTTONS_CHANGE_SERVICES


def get_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text=BUTTONS_ADD_SERVICES.ADD)
    builder.button(text=BUTTONS_ADD_SERVICES.CHANGE_SERVICE)
    builder.button(text=BUTTONS_ADD_SERVICES.REMOVE_SERVICE)

    builder.adjust(3)

    keyboard_markup = builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard_markup


def get_change_service_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text=BUTTONS_CHANGE_SERVICES.NAME)
    builder.button(text=BUTTONS_CHANGE_SERVICES.DESCRIPTION)
    builder.button(text=BUTTONS_CHANGE_SERVICES.PRICE)

    builder.adjust(3)

    keyboard_markup = builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard_markup
