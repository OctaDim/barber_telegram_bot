from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.buttons_admin_categories import CHOOSE_SERVICE_OR_CATEGORIES


def get_choose_service_or_categories_replay_kbd():
    builder = ReplyKeyboardBuilder()

    builder.button(text=CHOOSE_SERVICE_OR_CATEGORIES.CATEGORIES)
    builder.button(text=CHOOSE_SERVICE_OR_CATEGORIES.SERVICE)

    builder.adjust(1)

    keyboard_markup = builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard_markup
