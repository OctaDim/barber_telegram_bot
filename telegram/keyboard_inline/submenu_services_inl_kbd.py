from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.config.configs import (
    ENROLL_METHODS_CONFIGS)
from telegram.keyboard_inline.common_buttons_inline import (
    create_main_menu_inline_button)
from telegram.params.buttons_submenu_services import (
    SERVICES_BUTTONS)


class EnrollServicesInlineMenuCBData(CallbackData, prefix="enroll services inline menu"):
    pass


class EnrollSingleMasterServicesCBData(CallbackData, prefix="enroll services without methods"):
    pass


class MyReservationsInlineMenuCBData(CallbackData, prefix="my reservations inline menu"):
    pass


class OurServicesInlineMenuCBData(CallbackData, prefix="our services inline menu"):
    pass


class OurPromotionsInlineMenuCBData(CallbackData, prefix="our promotions inline menu"):
    pass


def get_submenu_services_inl_kbd_pvt() -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if ENROLL_METHODS_CONFIGS.ENROLL_SINGLE_MASTER_SERVICES:
        builder_inl_kbd.button(
            text=SERVICES_BUTTONS.ENROLL_SINGLE_MASTER_SERVICES,
            callback_data=EnrollSingleMasterServicesCBData().pack())

    any_enroll_services_by_method_flag = any([
        ENROLL_METHODS_CONFIGS.ENROLL_SERVICES_BY_CATEGORY_AND_MASTER,
        ENROLL_METHODS_CONFIGS.ENROLL_SERVICES_BY_CATEGORY,
        ENROLL_METHODS_CONFIGS.ENROLL_SERVICES_BY_SERVICES,
        ENROLL_METHODS_CONFIGS.ENROLL_SERVICES_BY_MASTER])
    if any_enroll_services_by_method_flag:
        builder_inl_kbd.button(
            text=SERVICES_BUTTONS.ENROLL_SERVICES,
            callback_data=EnrollServicesInlineMenuCBData().pack())

    builder_inl_kbd.button(
        text=SERVICES_BUTTONS.OUR_PROMOTIONS,
        callback_data=OurPromotionsInlineMenuCBData().pack())

    builder_inl_kbd.button(
        text=SERVICES_BUTTONS.MY_RESERVATIONS,
        callback_data=MyReservationsInlineMenuCBData().pack())

    builder_inl_kbd.button(
        text=SERVICES_BUTTONS.OUR_SERVICES,
        callback_data=OurServicesInlineMenuCBData().pack())

    # builder_inl_kbd.add(create_return_inline_button(
    #     delete_inline_msg_on_return=True))
    builder_inl_kbd.add(create_main_menu_inline_button())
    # builder_inl_kbd.add(create_empty_no_action_inl_btn())

    # builder_inl_kbd.adjust(1, 1, 1, 1, 2)
    builder_inl_kbd.adjust(1, 1, 1, 1, 1)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
