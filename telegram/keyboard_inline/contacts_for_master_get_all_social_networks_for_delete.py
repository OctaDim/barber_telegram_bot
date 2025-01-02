from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.contacts_for_master_cb_data_message import remove


class SocialNetworkForDeleteCbData(CallbackData, prefix='sn-delete', sep='|'):
    social_network_id: int


def get_all_social_networks_for_delete_inl_kbd(
        social_network_id: int
):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=remove,
            callback_data=SocialNetworkForDeleteCbData(
                social_network_id=social_network_id).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
