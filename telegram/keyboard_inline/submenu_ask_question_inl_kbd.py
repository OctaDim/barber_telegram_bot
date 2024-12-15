from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.keyboard_inline.common_buttons_inline import (
    create_main_menu_inline_button)
from telegram.params.buttons_ask_question import (
    ASK_QUESTION_BUTTONS)


class AskAdministratorInlineMenuCBData(CallbackData, prefix="ask administrator inline menu"):
    pass


class FrequentQuestionsInlineMenuCBData(CallbackData, prefix="faq questions inline menu"):
    pass


def get_ask_question_inl_kbd_pvt() -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    builder_inl_kbd.button(text=ASK_QUESTION_BUTTONS.ASK_ADMINISTRATOR,
                           callback_data=AskAdministratorInlineMenuCBData())

    builder_inl_kbd.button(text=ASK_QUESTION_BUTTONS.FREQUENT_QUESTIONS,
                           callback_data=FrequentQuestionsInlineMenuCBData())

    # builder_inl_kbd.add(create_return_inline_button(
    #     delete_inline_msg_on_return=True))
    builder_inl_kbd.add(create_main_menu_inline_button())
    # builder_inl_kbd.add(create_empty_no_action_inl_btn())

    # builder_inl_kbd.adjust(1, 1, 2)
    builder_inl_kbd.adjust(1, 1, 1)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
