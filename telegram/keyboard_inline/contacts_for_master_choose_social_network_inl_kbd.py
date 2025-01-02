import json

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.button_social_networks import SOCIAL_NETWORK


class NameSocialNetworkCbData(CallbackData, prefix='name-social-network', sep='|'):
    data: str


class OtherSocialNetworkCbData(CallbackData, prefix='other-social-network'):
    pass


def choose_social_network_inl_kbd():
    builder = InlineKeyboardBuilder()

    for attr_name, attr_value in vars(SOCIAL_NETWORK).items():
        if attr_name.startswith('__'):
            continue

        if isinstance(attr_value, tuple):
            name, url = attr_value

            callback_data = json.dumps((name, url))
            builder.row(InlineKeyboardButton(
                text=name,
                callback_data=NameSocialNetworkCbData(
                                            data=callback_data).pack()
            ))

        elif isinstance(attr_value, str):
            builder.row(InlineKeyboardButton(
                text=attr_value,
                callback_data=OtherSocialNetworkCbData().pack()
            ))

    inline_keyboard_markup = builder.as_markup()
    return inline_keyboard_markup
