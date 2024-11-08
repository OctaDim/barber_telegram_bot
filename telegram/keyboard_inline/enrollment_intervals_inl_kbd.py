from datetime import datetime
from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup)

from telegram.config.configs import (
    LANGUAGE_CONFIGS,
    SLOTS_CONFIGS)
from telegram.keyboard_inline.common_buttons_inline import (
    create_return_inline_button,
    create_main_menu_inline_button,
    ReturnInlineBtnCBData)
from telegram.params.buttons_intervals_slots import (
    SLOTS_BUTTONS)
from telegram.params.intervals_slots_icons import (
    SLOT_ICONS)
from telegram.telegram_utils.messages_helpers import (
    get_slot_advising_icon)
from utilities.calendar_utils import (
    get_date_with_month_name,
    get_time_flex_from_datetime)


class PreviousSlotPageCBData(CallbackData, prefix="previous_slot_page"):
    pass


class SlotPageNumberCBData(CallbackData, prefix="slot_page_number"):
    page_number: int


class NextSlotPageCBData(CallbackData, prefix="next_slot_page"):
    pass


class SlotSelectedCBData(CallbackData, prefix="current_slot_selected"):
    first_slot_id: int


class SlotsAdvisingNoteCBData(CallbackData, prefix="slots_advising_note"):
    pass


class ContinueSlotSavingCBData(CallbackData, prefix="continue_slot_saving"):
    pass


def get_enrollment_intervals_inl_kbd(
        current_page_intervals: List[dict],
        total_pages_number: int,
        selected_date: datetime,
        selected_slot_id: int = None,
        current_page_number: int = 1,
) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    date_now = get_date_with_month_name(date_value=selected_date,
                                        language=LANGUAGE_CONFIGS.LANGUAGE)
    date_now_text = f"{SLOT_ICONS.DATE_CALENDAR}  {date_now.upper()}"
    builder_inl_kbd.button(text=date_now_text,
                           callback_data=ReturnInlineBtnCBData())

    if total_pages_number > 1:
        builder_inl_kbd.button(
            text=SLOT_ICONS.PREVIOUS_PAGE,
            callback_data=PreviousSlotPageCBData())

        builder_inl_kbd.button(
            text=f"{SLOTS_BUTTONS.PAGE} "
                 f"{current_page_number}",
            callback_data=SlotPageNumberCBData(
                page_number=current_page_number).pack())

        builder_inl_kbd.button(
            text=SLOT_ICONS.NEXT_PAGE,
            callback_data=NextSlotPageCBData())

    for interval in current_page_intervals:
        first_slot_id = interval.get("first slot id")
        slot_time_start = interval.get("slot time start")
        client_time_end = interval.get("client time end")
        slot_time_loss = interval.get("slot time loss")

        cur_slot_callback_data = SlotSelectedCBData(
            first_slot_id=first_slot_id).pack()

        if SLOTS_CONFIGS.SHOW_SLOTS_ADVISES_ICONS:
            advising_icon = get_slot_advising_icon(time_loss=slot_time_loss)

            if SLOTS_CONFIGS.SHOW_SLOTS_ADVISING_ICON_HINT:
                advising_callback_data = SlotsAdvisingNoteCBData()
            else:
                advising_callback_data = cur_slot_callback_data

            builder_inl_kbd.button(text=advising_icon,
                                   callback_data=advising_callback_data)

        if selected_slot_id == first_slot_id:
            selected_left_icon = SLOT_ICONS.SELECTED_SLOT_START_ICON
            selected_right_icon = SLOT_ICONS.SELECTED_SLOT_END_ICON
        else:
            selected_left_icon = SLOT_ICONS.UNSELECTED_SLOT
            selected_right_icon = SLOT_ICONS.UNSELECTED_SLOT

        slot_time_start_text = get_time_flex_from_datetime(
            date_value=slot_time_start,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        client_time_end_text = get_time_flex_from_datetime(
            date_value=client_time_end,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        enrolment_slot_text = (f"{selected_left_icon} "
                               f"{slot_time_start_text} - "
                               f"{client_time_end_text} "
                               f"{selected_right_icon}")
        builder_inl_kbd.button(text=enrolment_slot_text,
                               callback_data=cur_slot_callback_data)

    if selected_slot_id:
        continue_btn_adjust = [1]
        builder_inl_kbd.button(
            text=SLOTS_BUTTONS.CONTINUE,
            callback_data=ContinueSlotSavingCBData())
    else:
        continue_btn_adjust = []

    builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    date_info_adjust = [1]
    if SLOTS_CONFIGS.SHOW_SLOTS_ADVISES_ICONS:
        slot_row_columns_number = 2
        return_main_meny_bts_adjust = [2] if selected_slot_id else [1]

    else:
        slot_row_columns_number = 1
        return_main_meny_bts_adjust = [2]

    pagination_adjust = [3] if total_pages_number > 1 else []

    dynamic_adjust = (
            date_info_adjust
            + pagination_adjust
            + [int(slot_row_columns_number)] * len(current_page_intervals)
            + continue_btn_adjust
            + return_main_meny_bts_adjust)

    builder_inl_kbd.adjust(*dynamic_adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
