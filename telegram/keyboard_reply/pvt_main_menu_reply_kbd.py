from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS_PARAMS
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS
from telegram.params.messages import SELECT_ACTION


def get_pvt_main_menu_reply_kbd():
    builder = ReplyKeyboardBuilder()

    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.ENROLL_SERVICES)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.RESERVATIONS)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.OUR_SERVICES)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.FAQ)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.ASK_ADMINISTRATOR)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.MAP)
    builder.button(text=MAIN_MENU_BUTTONS_PARAMS.CONTACTS)
    builder.button(text=COMMON_BUTTONS_PARAMS.RETURN)


    builder.adjust(2, 2, 2, 2)

    keyboard_markup = builder.as_markup(
        input_field_placeholder=SELECT_ACTION,
        resize_keyboard=True,
        one_time_keyboard=True)

    return keyboard_markup
