from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    InlineKeyboardMarkup)

from telegram.params.select_services_icons import SELECT_SERVICES_ICONS


def get_select_services_inl_kbd(services_buttons_data: list[dict]) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    for service in services_buttons_data:
        service_icon = service.get("icon")
        service_text = service.get("text")
        builder_inl_kbd.button(text=f"{service_icon} {service_text}",
                               callback_data=service.get("callback_data"))

    builder_inl_kbd.adjust(1)
    all_services_inl_kbd_markup = builder_inl_kbd.as_markup()

    return all_services_inl_kbd_markup
