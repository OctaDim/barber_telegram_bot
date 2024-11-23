from typing import List

from aiogram.filters.callback_data import (
    CallbackData)
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup)

from database.db_models.master_model import (
    Master)
from telegram.keyboard_inline.common_buttons_inline import (
    create_return_inline_button,
    create_main_menu_inline_button)
from telegram.params.buttons_enroll_masters import (
    ENROLL_MASTERS_BUTTONS)
from telegram.params.icons_masters import (
    MASTERS_ICONS)


class PreviousMasterPageCBData(CallbackData, prefix="previous_master_page"):
    pass


class MasterPageNumberCBData(CallbackData, prefix="master_page"):
    page_number: int


class NextMasterPageCBData(CallbackData, prefix="next_master_page"):
    pass


class CurrentMasterCBData(CallbackData, prefix="current_master"):
    master_id: int


class MasterToServiceContinueCBData(CallbackData, prefix="master_to_service_continue"):
    pass


def get_masters_enroll_srcs_inl_kbd(current_page_records: List[Master],
                                    total_pages_number: int,
                                    selected_master_id: int = None,
                                    current_page_number: int = 1
                                    ) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if total_pages_number > 1:
        builder_inl_kbd.button(
            text=MASTERS_ICONS.PREVIOUS_PAGE,
            callback_data=PreviousMasterPageCBData())

        builder_inl_kbd.button(
            text=f"{ENROLL_MASTERS_BUTTONS.PAGE}  "
                 f"{current_page_number} / {total_pages_number}",
            callback_data=MasterPageNumberCBData(
                page_number=current_page_number).pack())

        builder_inl_kbd.button(
            text=MASTERS_ICONS.NEXT_PAGE,
            callback_data=NextMasterPageCBData())

    for master_record in current_page_records:
        if master_record.id == selected_master_id:
            selected_icon = MASTERS_ICONS.SELECTED
        else:
            selected_icon = MASTERS_ICONS.UNSELECTED

        builder_inl_kbd.button(
            text=f"{selected_icon} "
                 f"{master_record.full_name} ",
            callback_data=CurrentMasterCBData(
                master_id=master_record.id).pack())

    if selected_master_id:
        continue_adjust = [1]
        builder_inl_kbd.button(
            text=ENROLL_MASTERS_BUTTONS.CONTINUE,
            callback_data=MasterToServiceContinueCBData())
    else:
        continue_adjust = []

    builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    pagination_adjust = [3] if total_pages_number > 1 else []

    masters_number = len(current_page_records)

    dynamic_adjust = pagination_adjust + [1] * masters_number + continue_adjust + [2]
    builder_inl_kbd.adjust(*dynamic_adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
