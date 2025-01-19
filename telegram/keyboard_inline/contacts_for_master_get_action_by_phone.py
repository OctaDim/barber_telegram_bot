from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.keyboard_inline.contacts_for_master_get_action_by_address import ReturnToContactsCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.buttons_add_services import BUTTONS_ADD_SERVICES
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL


class AddNewPhoneCbData(CallbackData, prefix='add-phone'):
    pass


class ChangePhoneCbData(CallbackData, prefix='change-phone'):
    pass


class RemovePhoneCbData(CallbackData, prefix='remove-phone'):
    pass


def get_action_by_phone():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text=BUTTONS_ADD_SERVICES.ADD,
        callback_data=AddNewPhoneCbData().pack()
    ))

    builder.row(InlineKeyboardButton(
        text=BUTTONS_ADD_SERVICES.CHANGE_SERVICE,
        callback_data=ChangePhoneCbData().pack()
    ))

    builder.row(InlineKeyboardButton(
        text=BUTTONS_ADD_SERVICES.REMOVE_SERVICE,
        callback_data=RemovePhoneCbData().pack()
    ))

    builder.row(
        InlineKeyboardButton(
            text=RETURN,
            callback_data=ReturnToContactsCbData().pack()
        ),
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
