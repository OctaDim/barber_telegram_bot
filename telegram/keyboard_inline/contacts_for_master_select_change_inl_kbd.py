from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.button_social_networks import SELECT_SOCIAL_NETWORK_CHANGE


class ChangeObtainedSocialNetworkCbData(CallbackData, prefix='change-obtained-social-network'):
    pass


class ChangeObtainedUsernameCbData(CallbackData, prefix='change-obtained-username'):
    pass


def change_obtained_social_network_data_inl_kbd():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text=SELECT_SOCIAL_NETWORK_CHANGE.SOCIAL_NETWORKS,
        callback_data=ChangeObtainedSocialNetworkCbData().pack()
    ))

    builder.row(InlineKeyboardButton(
        text=SELECT_SOCIAL_NETWORK_CHANGE.USERNAME,
        callback_data=ChangeObtainedUsernameCbData().pack()
    ))

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
