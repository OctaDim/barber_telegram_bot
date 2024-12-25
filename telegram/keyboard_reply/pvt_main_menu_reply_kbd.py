from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.buttons_common import SPECIAL_CHARACTERS
from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS
from telegram.params.messages import SELECT_ACTION


def get_pvt_main_menu_reply_kbd():
    builder = ReplyKeyboardBuilder()

    builder.button(text=MAIN_MENU_BUTTONS.SERVICES)
    builder.button(text=MAIN_MENU_BUTTONS.BALANCE)
    builder.button(text=MAIN_MENU_BUTTONS.ASK_QUESTION)
    builder.button(text=MAIN_MENU_BUTTONS.CONTACTS)
    # builder.add(create_empty_no_action_reply_btn())  # No-action common reply btn

    builder.adjust(2, 2, 2)

    keyboard_markup = builder.as_markup(
        input_field_placeholder=SPECIAL_CHARACTERS.UNBROKEN_NON_ZERO_SPACE_u00A0,
        resize_keyboard=True,
        one_time_keyboard=False)

    return keyboard_markup
