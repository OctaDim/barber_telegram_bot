from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.keyboard_inline.contacts_for_master_get_action_by_social_network import AddNewSocialNetworkCbData
from telegram.keyboard_inline.contacts_for_master_inl_kbd import ContactAdminCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.buttons_contacts_by_master import CONTACTS_BY_MASTER_PARAMS
from telegram.params.contacts_for_master_cb_data_message import confirm, change
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL


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
