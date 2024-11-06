from typing import Union

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup)

from telegram.config.configs import (
    ENROLL_METHODS_CONFIGS)
from telegram.keyboard_inline.common_buttons_inline import (
    create_return_inline_button,
    create_main_menu_inline_button)
from telegram.params.buttons_enroll_methods import (
    ENROLL_METHODS_BUTTONS)
from telegram.params.methods_icons import (
    METHODS_ICONS)


class MethodCategoryToMasterCBData(CallbackData, prefix="method_category_to_master"):
    pass


class MethodCategoryToServiceCBData(CallbackData, prefix="method_category_to_service"):
    pass


class MethodMasterToServiceCBData(CallbackData, prefix="method_master_to_services"):
    pass


def get_enroll_methods_inl_kbd(
        selected_method_prefix: Union[str, None]) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if ENROLL_METHODS_CONFIGS.SHOW_ENROLL_CATEGORY_TO_MASTER:
        if selected_method_prefix == MethodCategoryToMasterCBData.__prefix__:
            selected_icon = METHODS_ICONS.SELECTED
        else:
            selected_icon = METHODS_ICONS.UNSELECTED

        builder_inl_kbd.button(
            text=f"{selected_icon} "
                 f"{ENROLL_METHODS_BUTTONS.ENROLL_CATEGORY_TO_MASTER}",
            callback_data=MethodCategoryToMasterCBData())

    if ENROLL_METHODS_CONFIGS.SHOW_ENROLL_CATEGORY_TO_SERVICE:
        if selected_method_prefix == MethodCategoryToServiceCBData.__prefix__:
            selected_icon = METHODS_ICONS.SELECTED
        else:
            selected_icon = METHODS_ICONS.UNSELECTED

        builder_inl_kbd.button(
            text=f"{selected_icon} "
                 f"{ENROLL_METHODS_BUTTONS.ENROLL_CATEGORY_TO_SERVICE}",
            callback_data=MethodCategoryToServiceCBData())

    if ENROLL_METHODS_CONFIGS.SHOW_ENROLL_MASTER_TO_SERVICE:
        if selected_method_prefix == MethodMasterToServiceCBData.__prefix__:
            selected_icon = METHODS_ICONS.SELECTED
        else:
            selected_icon = METHODS_ICONS.UNSELECTED

        builder_inl_kbd.button(
            text=f"{selected_icon} "
                 f"{ENROLL_METHODS_BUTTONS.ENROLL_MASTER_TO_SERVICE}",
            callback_data=MethodMasterToServiceCBData())

    # if selected_method_prefix:
    #     continue_adjust = [1]
    #     builder_inl_kbd.button(
    #         text=ENROLL_METHODS_BUTTONS.CONTINUE,
    #         callback_data=EnrollMethodContinueCBD())
    # else:
    #     continue_adjust = []

    builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    adjust = [1, 1, 1] + [2]
    # adjust = [1, 1, 1] + continue_adjust + [2]

    builder_inl_kbd.adjust(*adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
