from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup

from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS
from telegram.params.messages import CHOOSE_AN_ACTION


def get_pvt_return_and_main_menu_reply_kbd() -> ReplyKeyboardMarkup:
    builder_reply_kbd = ReplyKeyboardBuilder()

    builder_reply_kbd.button(text=COMMON_BUTTONS_PARAMS.MAIN_MENU)
    builder_reply_kbd.button(text=COMMON_BUTTONS_PARAMS.RETURN)

    builder_reply_kbd.adjust(1)

    reply_keyboard_markup = builder_reply_kbd.as_markup(
        input_field_placeholder=CHOOSE_AN_ACTION,
        resize_keyboard=True,
        one_time_keyboard=True)

    return reply_keyboard_markup
