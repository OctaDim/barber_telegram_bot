from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS_PARAMS
from telegram.params.messages import  SELECT_ACTION


def get_pvt_main_menu_kbd():
    builder = ReplyKeyboardBuilder()

    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.FREE_TIME)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.RESERVATIONS)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.SERVICES)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.PRICES)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.FAQ)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.ASK_ADMINISTRATOR)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.MAP)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.CONTACTS)

    builder.adjust(2, 2, 2, 2)

    keyboard_markup = builder.as_markup(
        input_field_placeholder=SELECT_ACTION,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard_markup
