from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardMarkup)

from database.db_models.services_model import Services
from telegram.params.messages_helpers import get_service_brief_info_from_record
from telegram.params.buttons_enroll_service import ENROLL_SERVICE_BUTTONS
from telegram.params.select_services_icons import SELECT_SERVICES_ICONS


class EnrollServiceCallbackData(CallbackData, prefix="enroll_service"):
    service_id: int
    # service_text: str
    inl_button_selected: bool


def get_enroll_service_inl_kbd(service_id: int, button_selected=False) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if not button_selected:
        inl_button_text = ENROLL_SERVICE_BUTTONS.ENROLL_SERVICE
        callback_data = EnrollServiceCallbackData(
            service_id=service_id,
            inl_button_selected=False)

    else:
        inl_button_text = ENROLL_SERVICE_BUTTONS.CANCEL_SERVICE
        callback_data = EnrollServiceCallbackData(
            service_id=service_id,
            inl_button_selected=True)

    builder_inl_kbd.button(text=inl_button_text,
                           callback_data=callback_data.pack())

    builder_inl_kbd.adjust(1)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
