from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.keyboard_inline.contacts_for_master_get_action_by_address import ReturnToContactsCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.buttons_add_services import BUTTONS_ADD_SERVICES
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL


class AddNewSocialNetworkCbData(CallbackData, prefix='add-social-network'):
    pass


class ChangeSocialNetworkCbData(CallbackData, prefix='change-social-network'):
    pass


class RemoveSocialNetworkCbData(CallbackData, prefix='remove-social-network'):
    pass


def get_action_by_social_networks():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text=BUTTONS_ADD_SERVICES.ADD,
        callback_data=AddNewSocialNetworkCbData().pack()
    ))

    builder.row(InlineKeyboardButton(
        text=BUTTONS_ADD_SERVICES.CHANGE_SERVICE,
        callback_data=ChangeSocialNetworkCbData().pack()
    ))

    builder.row(InlineKeyboardButton(
        text=BUTTONS_ADD_SERVICES.REMOVE_SERVICE,
        callback_data=RemoveSocialNetworkCbData().pack()
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
