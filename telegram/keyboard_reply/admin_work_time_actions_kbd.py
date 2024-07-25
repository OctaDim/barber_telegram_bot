from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.button_work_time_actions import BUTTON_WORK_TIME_ACTIONS


def get_work_time_action_kbd():
    builder = ReplyKeyboardBuilder()

    builder.button(text=BUTTON_WORK_TIME_ACTIONS.ADD)
    builder.button(text=BUTTON_WORK_TIME_ACTIONS.CHANGE)

    builder.adjust(1, 1)

    keyboard_markup = builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard_markup
