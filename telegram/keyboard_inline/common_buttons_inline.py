from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from telegram.params.buttons_common import (
    COMMON_BUTTONS_PARAMS,
    SPECIAL_CHARACTERS)


class NoActionEmptyCBData(CallbackData, prefix="no_action_empty_inl_common"):
    pass


class ReturnInlineBtnCBData(CallbackData, prefix="return_inl_common"):
    delete_inline_msg_on_return: bool


class MainMenuInlineBtnCBData(CallbackData, prefix="main_menu_inl_common"):
    pass


def create_return_inline_button(
        delete_inline_msg_on_return: bool = False
):
    callback_data = ReturnInlineBtnCBData(
        delete_inline_msg_on_return=delete_inline_msg_on_return)

    inline_button = InlineKeyboardButton(
        text=COMMON_BUTTONS_PARAMS.RETURN,
        callback_data=callback_data.pack())

    return inline_button


def create_main_menu_inline_button():
    inline_button = InlineKeyboardButton(
        text=COMMON_BUTTONS_PARAMS.MAIN_MENU,
        callback_data=MainMenuInlineBtnCBData().pack())

    return inline_button


def create_empty_no_action_inl_btn():
    inline_button = InlineKeyboardButton(
        text=SPECIAL_CHARACTERS.NO_ACTION_EMPTY_u200B,
        callback_data=NoActionEmptyCBData().pack())

    return inline_button
