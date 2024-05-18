from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    InlineKeyboardMarkup)

from aiogram import types

def get_select_services_inl_kbd(all_services: list) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    for service in all_services:
        button_text = (f"🟩  {service.name} - \n"
                       f"{service.price} руб   (service.duration)")
        builder_inl_kbd.button(text=button_text,
                               callback_data=f"{service.id}_{service.name}")

    builder_inl_kbd.adjust(1)
    all_services_inl_kbd_markup = builder_inl_kbd.as_markup()

    return all_services_inl_kbd_markup
