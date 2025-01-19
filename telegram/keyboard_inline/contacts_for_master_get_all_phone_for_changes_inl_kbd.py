from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.contacts_for_master_cb_data_message import change


class PhoneForChangesCbData(CallbackData, prefix='ph-change', sep='|'):
    phone_id: int


def get_all_phone_for_changes_inl_kbd(
        phone_id: int
):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=change,
            callback_data=PhoneForChangesCbData(
                phone_id=phone_id).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
