from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.contacts_for_master_cb_data_message import confirm, change


class ChangePreviewSocialNetworkCbData(CallbackData, prefix='change-preview-social-network'):
    pass


class ConfirmPreviewSocialNetworkCbData(CallbackData, prefix='confirm-preview-social-network'):
    pass


def preview_social_network_inl_kbd():
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=confirm,
            callback_data=ConfirmPreviewSocialNetworkCbData().pack()
        ),
        InlineKeyboardButton(
            text=change,
            callback_data=ChangePreviewSocialNetworkCbData().pack()
        )
    ]

    builder.row(*buttons)

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
