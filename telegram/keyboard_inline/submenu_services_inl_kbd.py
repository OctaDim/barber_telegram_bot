from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.config.configs import (
    ENROLL_METHODS_CONFIGS)
from telegram.keyboard_inline.common_buttons_inline import (
    create_main_menu_inline_button)
from telegram.params.buttons_services import (
    SERVICES_BUTTONS)


class EnrollServicesInlineMenuCBData(CallbackData, prefix="enroll services inline menu"):
    pass


class EnrollServicesWithoutMethodsCBD(CallbackData, prefix="enroll services without methods"):
    pass


class MyReservationsInlineMenuCBData(CallbackData, prefix="my reservations inline menu"):
    pass


class OurServicesInlineMenuCBData(CallbackData, prefix="our services inline menu"):
    pass


class OurPromotionsInlineMenuCBData(CallbackData, prefix="our promotions inline menu"):
    pass


def get_submenu_services_inl_kbd_pvt() -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if not ENROLL_METHODS_CONFIGS.ENROLL_SERVICES_WITHOUT_METHODS:
        enroll_srcs_callback_data = EnrollServicesInlineMenuCBData()
    else:
        enroll_srcs_callback_data = EnrollServicesWithoutMethodsCBD()

    builder_inl_kbd.button(
        text=SERVICES_BUTTONS.ENROLL_SERVICES,
        callback_data=enroll_srcs_callback_data)

    builder_inl_kbd.button(text=SERVICES_BUTTONS.OUR_PROMOTIONS,
                           callback_data=OurPromotionsInlineMenuCBData())

    builder_inl_kbd.button(text=SERVICES_BUTTONS.MY_RESERVATIONS,
                           callback_data=MyReservationsInlineMenuCBData())

    builder_inl_kbd.button(text=SERVICES_BUTTONS.OUR_SERVICES,
                           callback_data=OurServicesInlineMenuCBData())

    # builder_inl_kbd.add(create_return_inline_button(
    #     delete_inline_msg_on_return=True))
    builder_inl_kbd.add(create_main_menu_inline_button())
    # builder_inl_kbd.add(create_empty_no_action_inl_btn())

    # builder_inl_kbd.adjust(1, 1, 1, 1, 2)
    builder_inl_kbd.adjust(1, 1, 1, 1, 1)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
