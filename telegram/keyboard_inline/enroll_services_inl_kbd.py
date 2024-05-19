from datetime import timedelta

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    InlineKeyboardMarkup)

from telegram.params.select_services_icons import SELECT_SERVICES_ICONS
from telegram.params.messages import CURRENCY_BRIEF, SERVICE_DURATION


class EnrollServicesCallbackData(CallbackData, prefix="enroll_services"):
    service_id: int
    service_icon: str
    selected_state: bool


def get_enroll_services_inl_kbd(all_services_records: list) \
        -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    for service in all_services_records:
        service_icon = SELECT_SERVICES_ICONS.UNSELECTED

        service_text = (f"{service.name} - "
                        f"{service.price}{CURRENCY_BRIEF}  "
                        f"({SERVICE_DURATION}: {service.time_duration})")

        callback_data = EnrollServicesCallbackData(service_id=service.id,
                                                   service_icon=service_icon,
                                                   selected_state=False)


        service_btn_text = f"{service_icon}  {service_text}"
        builder_inl_kbd.button(text=service_btn_text,
                               callback_data=callback_data)

    builder_inl_kbd.adjust(1)

    inline_keyboard_markup = builder_inl_kbd.as_markup()

    return inline_keyboard_markup
