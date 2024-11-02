from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup)

from telegram.config.configs import (
    ENROLL_METHODS_CONFIGS)
from telegram.keyboard_inline.common_buttons_inline import (
    create_return_inline_button,
    create_main_menu_inline_button)
from telegram.params.buttons_enroll_methods import ENROLL_METHODS_BUTTONS


class EnrollByCategoryCBData(CallbackData, prefix="enroll_by_services_category"):
    pass


class EnrollByMasterCBData(CallbackData, prefix="enroll_by_services_master"):
    pass


class EnrollByCategoryThenMasterCBData(CallbackData, prefix="enroll_by_category_then_master"):
    pass


class EnrollMethodContinueCBD(CallbackData, prefix="enroll_services_method_continue"):
    pass


def get_enroll_methods_inl_kbd() -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if ENROLL_METHODS_CONFIGS.SHOW_ENROLL_BY_CATEGORY_AND_MASTER:
        builder_inl_kbd.button(
            text=f"{ENROLL_METHODS_BUTTONS.ENROLL_BY_CATEGORY_AND_MASTER}",
            callback_data=EnrollByCategoryThenMasterCBData())

    if ENROLL_METHODS_CONFIGS.SHOW_ENROLL_BY_CATEGORY:
        builder_inl_kbd.button(
            text=f"{ENROLL_METHODS_BUTTONS.ENROLL_BY_CATEGORY}",
            callback_data=EnrollByCategoryCBData())

    if ENROLL_METHODS_CONFIGS.SHOW_ENROLL_BY_MASTER:
        builder_inl_kbd.button(
            text=f"{ENROLL_METHODS_BUTTONS.ENROLL_BY_MASTER}",
            callback_data=EnrollByMasterCBData())

    builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    adjust = [1, 1, 1] + [2]

    builder_inl_kbd.adjust(*adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
