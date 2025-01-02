from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.buttons_contacts_by_master import CONTACTS_BY_MASTER_PARAMS


class ContactAdminCbData(CallbackData, prefix='contact-admin'):
    contact: str


def contacts_by_admin_inl_kbd():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text=CONTACTS_BY_MASTER_PARAMS.SOCIAL_NETWORKS,
        callback_data=ContactAdminCbData(contact=CONTACTS_BY_MASTER_PARAMS.SOCIAL_NETWORKS).pack()
    ))

    builder.row(InlineKeyboardButton(
        text=CONTACTS_BY_MASTER_PARAMS.ADDRESS,
        callback_data=ContactAdminCbData(contact=CONTACTS_BY_MASTER_PARAMS.ADDRESS).pack()
    ))

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
