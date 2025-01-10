from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.admin_categories_message import CHANGE


class AdminCategoryForChangeCbData(CallbackData, prefix='admin-category-for-cahnge'):
    category_id: int


def get_category_for_change_inl_kbd(category_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=CHANGE,
            callback_data=AdminCategoryForChangeCbData(
                category_id=category_id).pack()
        )
    )

    inline_markup = builder.as_markup()

    return inline_markup
