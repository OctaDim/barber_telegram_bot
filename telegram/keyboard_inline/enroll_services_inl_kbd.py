from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardMarkup)

from telegram.params.messages_helpers import get_service_brief_info
from telegram.params.select_services_icons import SELECT_SERVICES_ICONS


class EnrollServicesCallbackData(CallbackData, prefix="enroll_services"):
    service_id: int
    service_icon: str
    selected_state: bool


def get_enroll_services_inl_kbd(all_services_records: list) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    for service_record in all_services_records:
        service_icon = SELECT_SERVICES_ICONS.UNSELECTED
        service_text = get_service_brief_info(service_record)

        callback_data = EnrollServicesCallbackData(service_id=service_record.id,
                                                   service_icon=service_icon,
                                                   selected_state=False)

        service_btn_text = f"{service_icon}  {service_text}"
        builder_inl_kbd.button(text=service_btn_text,
                               callback_data=callback_data)

    builder_inl_kbd.adjust(1)
    inline_keyboard_markup = builder_inl_kbd.as_markup()
    return inline_keyboard_markup
