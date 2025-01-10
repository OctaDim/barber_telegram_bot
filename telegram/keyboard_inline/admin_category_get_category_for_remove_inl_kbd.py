from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.admin_categories_message import REMOVE


class AdminCategoryForRemoveCbData(CallbackData, prefix='admin-category-for-remove'):
    category_id: int


def get_category_for_remove_inl_kbd(category_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=REMOVE,
            callback_data=AdminCategoryForRemoveCbData(
                category_id=category_id).pack()
        )
    )

    inline_markup = builder.as_markup()

    return inline_markup
