from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.contacts_for_master_cb_data_message import remove


class PhoneForDeleteCbData(CallbackData, prefix='ph-delete', sep='|'):
    phone_id: int


def get_all_phone_for_delete_inl_kbd(
        phone_id: int
):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=remove,
            callback_data=PhoneForDeleteCbData(
                phone_id=phone_id).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
