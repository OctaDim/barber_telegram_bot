from aiogram.types import KeyboardButton

from telegram.params.buttons_common import SPECIAL_CHARACTERS


def create_empty_no_action_reply_btn():
    reply_button = KeyboardButton(
        text=SPECIAL_CHARACTERS.NO_ACTION_SYMBOL_REPLY)
    return reply_button
