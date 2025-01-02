from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.params.buttons_add_services import BUTTONS_ADD_SERVICES


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

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
