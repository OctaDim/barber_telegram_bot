from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.contacts_for_master_cb_data_message import confirm, change


class ChangePreviewAddressCbData(CallbackData, prefix='change-preview-address'):
    pass


class ConfirmPreviewAddressCbData(CallbackData, prefix='confirm-preview-address'):
    pass


def preview_address_inl_kbd():
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=confirm,
            callback_data=ConfirmPreviewAddressCbData().pack()
        ),
        InlineKeyboardButton(
            text=change,
            callback_data=ChangePreviewAddressCbData().pack()
        )
    ]

    builder.row(*buttons)

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
