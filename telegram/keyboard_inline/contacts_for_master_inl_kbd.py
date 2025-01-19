from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.buttons_contacts_by_master import CONTACTS_BY_MASTER_PARAMS
from telegram.params.work_time_cb_data_message import RETURN


class ContactAdminCbData(CallbackData, prefix='contact-admin'):
    contact: str


def contacts_by_admin_inl_kbd():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text=CONTACTS_BY_MASTER_PARAMS.SOCIAL_NETWORKS,
        callback_data=ContactAdminCbData(
            contact=CONTACTS_BY_MASTER_PARAMS.SOCIAL_NETWORKS).pack()
    ))

    builder.row(InlineKeyboardButton(
        text=CONTACTS_BY_MASTER_PARAMS.ADDRESS,
        callback_data=ContactAdminCbData(
            contact=CONTACTS_BY_MASTER_PARAMS.ADDRESS).pack()
    ))

    builder.row(InlineKeyboardButton(
        text=CONTACTS_BY_MASTER_PARAMS.PHONE,
        callback_data=ContactAdminCbData(
            contact=CONTACTS_BY_MASTER_PARAMS.PHONE).pack()
    ))

    builder.row(InlineKeyboardButton(
        text=RETURN,
        callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
