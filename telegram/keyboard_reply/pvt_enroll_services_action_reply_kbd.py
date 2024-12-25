from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup

from telegram.config.configs import SERVICES_CONFIGS
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS, SPECIAL_CHARACTERS
from telegram.params.buttons_enroll_service import ENROLL_SRCS_BUTTONS


def get_enroll_services_reply_kbd(
        show_continue_button: bool = False
) -> ReplyKeyboardMarkup:
    builder_reply_kbd = ReplyKeyboardBuilder()

    if show_continue_button:
        builder_reply_kbd.button(text=ENROLL_SRCS_BUTTONS.CONTINUE_ENROLL_SERVICES)
        continue_adjust = [1]
    else:
        continue_adjust = []

    if SERVICES_CONFIGS.SHOW_CANCEL_ALL_SERVICES_BUTTON:
        builder_reply_kbd.button(text=ENROLL_SRCS_BUTTONS.CANCEL_ALL_SERVICES)
        cancel_all_srcs_adjust = [1]
    else:
        cancel_all_srcs_adjust = []

    builder_reply_kbd.button(text=ENROLL_SRCS_BUTTONS.RETURN_TO_MASTERS)
    builder_reply_kbd.button(text=COMMON_BUTTONS_PARAMS.MAIN_MENU)

    dynamic_adjust = (continue_adjust
                      + cancel_all_srcs_adjust
                      + [2])

    builder_reply_kbd.adjust(*dynamic_adjust)

    place_holder = SPECIAL_CHARACTERS.UNBROKEN_NON_ZERO_SPACE_u00A0
    reply_keyboard_markup = builder_reply_kbd.as_markup(
        input_field_placeholder=place_holder,
        resize_keyboard=True,
        one_time_keyboard=False)

    return reply_keyboard_markup
