from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.buttons_add_services import BUTTONS_ADD_SERVICES
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL


class AddNewAddressCbData(CallbackData, prefix='add-new-address'):
    pass


class RemoveAddressCbData(CallbackData, prefix='remove-address'):
    pass


class ReturnToContactsCbData(CallbackData, prefix='return-to=contacts'):
    pass


def get_action_by_address():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text=f'{BUTTONS_ADD_SERVICES.ADD} | '
             f'{BUTTONS_ADD_SERVICES.CHANGE_SERVICE}',
        callback_data=AddNewAddressCbData().pack()
    ))

    builder.row(InlineKeyboardButton(
        text=BUTTONS_ADD_SERVICES.REMOVE_SERVICE,
        callback_data=RemoveAddressCbData().pack()
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
