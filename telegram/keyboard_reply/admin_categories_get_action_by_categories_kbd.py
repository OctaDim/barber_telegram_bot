from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.buttons_admin_categories import ADMIN_CATEGORIES_ACTION


def get_action_by_categories_replay_kbd():
    builder = ReplyKeyboardBuilder()

    builder.button(text=ADMIN_CATEGORIES_ACTION.ADD)
    builder.button(text=ADMIN_CATEGORIES_ACTION.CHANGE)
    builder.button(text=ADMIN_CATEGORIES_ACTION.REMOVE)

    builder.adjust(1)

    keyboard_markup = builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard_markup
