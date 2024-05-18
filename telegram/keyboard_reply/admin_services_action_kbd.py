from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.button_services_action import BUTTON_SERVICES_ACTION


def get_services_action_kbd():
    builder = ReplyKeyboardBuilder()

    builder.button(text=BUTTON_SERVICES_ACTION.ADD)
    builder.button(text=BUTTON_SERVICES_ACTION.CHANGE)
    builder.button(text=BUTTON_SERVICES_ACTION.Remove)

    builder.adjust(1, 1, 1)

    keyboard_markup = builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard_markup
