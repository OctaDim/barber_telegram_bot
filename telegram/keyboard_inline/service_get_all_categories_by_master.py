from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.admin_categories_message import SELECT


class AdminCategoryForServiceCbData(CallbackData,
                                    prefix='admin-category-for-service'):
    category_id: int


def get_category_for_service_inl_kbd(category_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=SELECT,
            callback_data=AdminCategoryForServiceCbData(
                category_id=category_id).pack()
        )
    )

    inline_markup = builder.as_markup()

    return inline_markup
