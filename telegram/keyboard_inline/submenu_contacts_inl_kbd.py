from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.keyboard_inline.common_buttons_inline import (
    create_main_menu_inline_button,
    create_return_inline_button)
from telegram.params.buttons_submenu_contacts import (
    CONTACTS_BUTTONS)


class OurContactsInlineMenuCBData(CallbackData, prefix="our contacts inline menu"):
    pass


class OurMapInlineMenuCBData(CallbackData, prefix="our map inline menu"):
    pass


def get_submenu_contacts_inl_kbd_pvt() -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    builder_inl_kbd.button(text=CONTACTS_BUTTONS.OUR_CONTACTS,
                           callback_data=OurContactsInlineMenuCBData())

    builder_inl_kbd.button(text=CONTACTS_BUTTONS.OUR_MAP,
                           callback_data=OurMapInlineMenuCBData())

    # builder_inl_kbd.add(create_return_inline_button(
    #     delete_inline_msg_on_return=True))
    builder_inl_kbd.add(create_main_menu_inline_button())
    # builder_inl_kbd.add(create_empty_no_action_inl_btn())


    # builder_inl_kbd.adjust(1, 1, 2)
    builder_inl_kbd.adjust(1, 1, 1)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
