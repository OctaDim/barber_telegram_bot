from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.keyboard_inline.contacts_for_master_inl_kbd import ContactAdminCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.buttons_contacts_by_master import CONTACTS_BY_MASTER_PARAMS
from telegram.params.contacts_for_master_cb_data_message import confirm, change
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL


class ChangePreviewPhoneCbData(CallbackData, prefix='change-preview-address'):
    pass


class ConfirmPreviewPhoneCbData(CallbackData, prefix='confirm-preview-address'):
    pass


def preview_phone_inl_kbd():
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=confirm,
            callback_data=ConfirmPreviewPhoneCbData().pack()
        ),
        InlineKeyboardButton(
            text=change,
            callback_data=ChangePreviewPhoneCbData().pack()
        )
    ]

    builder.row(*buttons)

    builder.row(
        InlineKeyboardButton(
            text=RETURN,
            callback_data=ContactAdminCbData(contact=CONTACTS_BY_MASTER_PARAMS.ADDRESS).pack()
        ),
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
