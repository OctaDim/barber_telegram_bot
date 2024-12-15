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
from telegram.params.icons_methods import (
    METHODS_ICONS)


class MethodCategoryToMasterCBData(CallbackData, prefix="method_category_to_master"):
    pass


class MethodCategoryToServiceCBData(CallbackData, prefix="method_category_to_service"):
    pass


class MethodMasterToServiceCBData(CallbackData, prefix="method_master_to_services"):
    pass


class MethodCategoryToMasterContinueCBData(CallbackData, prefix="method_category_to_master_continue"):
    pass


class MethodCategoryToServiceContinueCBD(CallbackData, prefix="method_category_to_service_continue"):
    pass


class MethodMasterToServiceContinueCBD(CallbackData, prefix="method_master_to_service_continue"):
    pass


def get_methods_enroll_srcs_inl_kbd(selected_method_prefix: Union[str, None]
                                    ) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if ENROLL_METHODS_CONFIGS.ENROLL_SERVICES_BY_CATEGORY_AND_MASTER:
        if selected_method_prefix == MethodCategoryToMasterCBData.__prefix__:
            selected_icon = METHODS_ICONS.SELECTED
        else:
            selected_icon = METHODS_ICONS.UNSELECTED

        builder_inl_kbd.button(
            text=f"{selected_icon} "
                 f"{ENROLL_METHODS_BUTTONS.ENROLL_CATEGORY_TO_MASTER}",
            callback_data=MethodCategoryToMasterCBData())

    if ENROLL_METHODS_CONFIGS.ENROLL_SERVICES_BY_MASTER:
        if selected_method_prefix == MethodMasterToServiceCBData.__prefix__:
            selected_icon = METHODS_ICONS.SELECTED
        else:
            selected_icon = METHODS_ICONS.UNSELECTED

        builder_inl_kbd.button(
            text=f"{selected_icon} "
                 f"{ENROLL_METHODS_BUTTONS.ENROLL_MASTER_TO_SERVICE}",
            callback_data=MethodMasterToServiceCBData())

    if ENROLL_METHODS_CONFIGS.ENROLL_SERVICES_BY_CATEGORY:
        if selected_method_prefix == MethodCategoryToServiceCBData.__prefix__:
            selected_icon = METHODS_ICONS.SELECTED
        else:
            selected_icon = METHODS_ICONS.UNSELECTED

        builder_inl_kbd.button(
            text=f"{selected_icon} "
                 f"{ENROLL_METHODS_BUTTONS.ENROLL_CATEGORY_TO_SERVICE}",
            callback_data=MethodCategoryToServiceCBData())

    # builder_inl_kbd.add(create_return_inline_button())

    if selected_method_prefix:
        continue_adjust = [1]
        # return_continue_adjust = [2]

        match selected_method_prefix:
            case MethodCategoryToMasterCBData.__prefix__:
                callback_data = MethodCategoryToMasterContinueCBData()
            case MethodCategoryToServiceCBData.__prefix__:
                callback_data = MethodCategoryToServiceContinueCBD()
            case MethodMasterToServiceCBData.__prefix__:
                callback_data = MethodMasterToServiceContinueCBD()
            case _:
                callback_data = None

        builder_inl_kbd.button(
            text=ENROLL_METHODS_BUTTONS.CONTINUE,
            callback_data=callback_data)
    else:
        continue_adjust = []
        # return_continue_adjust = [1]

    builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    adjust = [1, 1, 1] + continue_adjust + [2]
    # adjust = [1, 1, 1] + return_continue_adjust + [1]
    # adjust = [1, 1, 1] + continue_adjust + [1]


    builder_inl_kbd.adjust(*adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
