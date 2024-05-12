from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.params.messages import SELECT_ACTION

from database.db_queries.admin_queries import get_btn_admin_panel


def get_admin_main_menu_kbd():
    btn_text = get_btn_admin_panel()

    builder = ReplyKeyboardBuilder()

    builder.button(text=btn_text.get('services'))
    builder.button(text=btn_text.get('contacts'))


    builder.adjust(1, 1)

    keyboard_markup = builder.as_markup(
        input_field_placeholder=SELECT_ACTION,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard_markup
