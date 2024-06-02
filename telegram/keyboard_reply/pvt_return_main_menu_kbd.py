from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup

from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS


def get_pvt_return_main_menu_kbd(return_btn_prefix: str) -> ReplyKeyboardMarkup:
    builder_reply_kbd = ReplyKeyboardBuilder()

    builder_reply_kbd.button(text=COMMON_BUTTONS_PARAMS.MAIN_MENU)
    builder_reply_kbd.button(text=COMMON_BUTTONS_PARAMS.RETURN,
                             return_prefix=return_btn_prefix)

    builder_reply_kbd.adjust(1)

    reply_keyboard_markup = builder_reply_kbd.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True)

    return reply_keyboard_markup
