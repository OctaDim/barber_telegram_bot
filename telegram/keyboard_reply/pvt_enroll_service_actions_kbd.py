from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup

from telegram.params.buttons_enroll_service import ENROLL_SERVICE_BUTTONS
from telegram.params.messages import CHOOSE_AN_ACTION
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS



def get_enroll_service_actions_reply_kbd() -> ReplyKeyboardMarkup:
    builder_reply_kbd = ReplyKeyboardBuilder()

    builder_reply_kbd.button(text=ENROLL_SERVICE_BUTTONS.KEEP_SERVICE)
    builder_reply_kbd.button(text=ENROLL_SERVICE_BUTTONS.CANCEL_SERVICE)
    builder_reply_kbd.button(text=COMMON_BUTTONS_PARAMS.RETURN)


    builder_reply_kbd.adjust(1)
    reply_keyboard_markup = builder_reply_kbd.as_markup(
        input_field_placeholder=CHOOSE_AN_ACTION,
        resize_keyboard=True,
        one_time_keyboard=True)

    return reply_keyboard_markup
