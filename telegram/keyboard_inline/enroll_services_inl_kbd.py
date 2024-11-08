from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardMarkup)

from telegram.params.buttons_enroll_service import ENROLL_SERVICE_BUTTONS


class EnrollServiceCallbackData(CallbackData, prefix="enroll_cancel_services"):
    service_id: int


class OneMoreServiceCallbackData(CallbackData, prefix="one_more_same_service"):
    service_id: int


def get_enroll_service_inl_kbd(service_id: int,
                               button_selected: bool = False,
                               one_more_service_btn: bool = False) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if button_selected:
        inl_button_text = ENROLL_SERVICE_BUTTONS.CANCEL_SERVICE
        callback_data = EnrollServiceCallbackData(service_id=service_id)
        builder_inl_kbd.button(text=inl_button_text,
                               callback_data=callback_data.pack())

        if one_more_service_btn:
            callback_data = OneMoreServiceCallbackData(service_id=service_id)
            builder_inl_kbd.button(text=ENROLL_SERVICE_BUTTONS.ENROLL_ONE_MORE,
                                   callback_data=callback_data.pack())

    else:
        inl_button_text = ENROLL_SERVICE_BUTTONS.ENROLL_SERVICE
        callback_data = EnrollServiceCallbackData(service_id=service_id)
        builder_inl_kbd.button(text=inl_button_text,
                               callback_data=callback_data.pack())

    builder_inl_kbd.adjust(3)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
