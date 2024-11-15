from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup)

from database.db_models.category_model import (
    Category)
from telegram.keyboard_inline.common_buttons_inline import (
    create_return_inline_button,
    create_main_menu_inline_button)
from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
    MethodCategoryToServiceContinueCBD,
    MethodCategoryToMasterContinueCBData)
from telegram.params.buttons_enroll_categories import (
    ENROLL_CATEGORIES_BUTTONS)
from telegram.params.categories_icons import (
    CATEGORIES_ICONS)


class PreviousCategoryPageCBData(CallbackData, prefix="previous_category_page"):
    pass


class CategoryPageNumberCBData(CallbackData, prefix="category_page"):
    page_number: int


class NextCategoryPageCBData(CallbackData, prefix="next_category_page"):
    pass


class CurrentCategoryCBData(CallbackData, prefix="current_category"):
    category_id: int


class CategoryToServiceContinueCBData(CallbackData, prefix="category_to_service_continue"):
    pass


class CategoryToMasterContinueCBData(CallbackData, prefix="category_to_master_continue"):
    pass


class CategoryToOurServicesInfoContinueCBdata(CallbackData,
                                              prefix="category_to_our_services_info_continue"):
    pass


def get_categories_enroll_srcs_inl_kbd(
        current_page_records: List[Category],
        total_pages_number: int,
        selected_category_id: int = None,
        current_page_number: int = 1,
        selected_method_prefix: str = None,
) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if total_pages_number > 1:
        builder_inl_kbd.button(
            text=CATEGORIES_ICONS.PREVIOUS_PAGE,
            callback_data=PreviousCategoryPageCBData())

        builder_inl_kbd.button(
            text=f"{ENROLL_CATEGORIES_BUTTONS.PAGE}  "
                 f"{current_page_number} / {total_pages_number}",
            callback_data=CategoryPageNumberCBData(
                page_number=current_page_number).pack())

        builder_inl_kbd.button(
            text=CATEGORIES_ICONS.NEXT_PAGE,
            callback_data=NextCategoryPageCBData())

    for category_record in current_page_records:
        if category_record.id == selected_category_id:
            selected_icon = CATEGORIES_ICONS.SELECTED
        else:
            selected_icon = CATEGORIES_ICONS.UNSELECTED

        builder_inl_kbd.button(
            text=f"{selected_icon} "
                 f"{category_record.name}",
            callback_data=CurrentCategoryCBData(
                category_id=category_record.id).pack())

    if selected_category_id:
        continue_adjust = [1]
        if selected_method_prefix == MethodCategoryToServiceContinueCBD.__prefix__:
            continue_callback_data = CategoryToServiceContinueCBData
        elif selected_method_prefix == MethodCategoryToMasterContinueCBData.__prefix__:
            continue_callback_data = CategoryToMasterContinueCBData
        else:  # elif selected_method_prefix == "our services reply btn private handler"
            continue_callback_data = CategoryToOurServicesInfoContinueCBdata

        builder_inl_kbd.button(
            text=ENROLL_CATEGORIES_BUTTONS.CONTINUE,
            callback_data=continue_callback_data())
    else:
        continue_adjust = []

    builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    pagination_adjust = [3] if total_pages_number > 1 else []

    categories_number = len(current_page_records)
    dynamic_adjust = pagination_adjust + [1] * categories_number + continue_adjust + [2]
    builder_inl_kbd.adjust(*dynamic_adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
