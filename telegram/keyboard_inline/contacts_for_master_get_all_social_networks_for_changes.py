from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.contacts_for_master_cb_data_message import change


class SocialNetworkForChangesCbData(CallbackData, prefix='sn-change', sep='|'):
    social_network_id: int


def get_all_social_networks_for_changes_inl_kbd(
        social_network_id: int
):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=change,
            callback_data=SocialNetworkForChangesCbData(
                social_network_id=social_network_id).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
