import json

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.keyboard_inline.contacts_for_master_inl_kbd import ContactAdminCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.button_social_networks import SOCIAL_NETWORK
from telegram.params.buttons_contacts_by_master import CONTACTS_BY_MASTER_PARAMS
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL


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

    builder.row(
        InlineKeyboardButton(
            text=RETURN,
            callback_data=ContactAdminCbData(contact=CONTACTS_BY_MASTER_PARAMS.SOCIAL_NETWORKS).pack()
        ),
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    )

    inline_keyboard_markup = builder.as_markup()
    return inline_keyboard_markup
