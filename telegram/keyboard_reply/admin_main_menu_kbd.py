from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.messages import SELECT_ACTION
from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS


def get_admin_main_menu_kbd():
    builder = ReplyKeyboardBuilder()

    builder.button(text=MAIN_MANU_ADMIN_PARAMS.TIMETABLE)
    builder.button(text=MAIN_MANU_ADMIN_PARAMS.WORK_TIME)
    builder.button(text=MAIN_MANU_ADMIN_PARAMS.SERVICES)
    builder.button(text=MAIN_MANU_ADMIN_PARAMS.CONTACTS)

    builder.adjust(2, 2)

    keyboard_markup = builder.as_markup(
        input_field_placeholder=SELECT_ACTION,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    return keyboard_markup
