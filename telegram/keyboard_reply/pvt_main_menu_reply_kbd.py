from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.config.configs import BALANCE_CONFIGS
from telegram.params.buttons_common import SPECIAL_CHARACTERS
from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS
from telegram.params.messages import SELECT_ACTION


def get_pvt_main_menu_reply_kbd():
    builder = ReplyKeyboardBuilder()

    builder.button(text=MAIN_MENU_BUTTONS.SERVICES)
    if BALANCE_CONFIGS.SHOW_BALANCE_MENU:
        builder.button(text=MAIN_MENU_BUTTONS.BALANCE)
    builder.button(text=MAIN_MENU_BUTTONS.ASK_QUESTION)
    builder.button(text=MAIN_MENU_BUTTONS.CONTACTS)
    # builder.add(create_empty_no_action_reply_btn())  # No-action common reply btn

    if BALANCE_CONFIGS.SHOW_BALANCE_MENU:
        builder.adjust(2, 2)
    else:
        builder.adjust(1, 2)

    keyboard_markup = builder.as_markup(
        input_field_placeholder=SPECIAL_CHARACTERS.UNBROKEN_NON_ZERO_SPACE_u00A0,
        resize_keyboard=True,
        one_time_keyboard=False)

    return keyboard_markup
