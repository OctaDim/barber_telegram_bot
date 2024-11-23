from datetime import datetime
from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup)

from database.db_queries.master_fullname_by_id_query import (
    get_master_full_name_by_id)
from telegram.config.configs import (
    LANGUAGE_CONFIGS,
    SLOTS_CONFIGS)
from telegram.keyboard_inline.common_buttons_inline import (
    create_return_inline_button,
    create_main_menu_inline_button,
    ReturnInlineBtnCBData)
from telegram.params.buttons_intervals_slots import (
    SLOTS_BUTTONS)
from telegram.params.icons_intervals_slots import (
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
            text=f"{SLOTS_BUTTONS.PAGE}  "
                 f"{current_page_number} / {total_pages_number}",
            callback_data=SlotPageNumberCBData(
                page_number=current_page_number).pack())

        builder_inl_kbd.button(
            text=SLOT_ICONS.NEXT_PAGE,
            callback_data=NextSlotPageCBData())

    time_start_frequency_dict = {}
    cur_page_masters_ids = []
    for interval in current_page_intervals:
        slot_time_start = interval.get("slot time start")
        time_start_frequency_dict[slot_time_start] = (
                time_start_frequency_dict.setdefault(slot_time_start, 0) + 1)

        slot_master_id = interval.get("slot master id")
        if slot_master_id not in cur_page_masters_ids:
            cur_page_masters_ids.append(slot_master_id)

    master_name_by_id = {}
    for master_id in cur_page_masters_ids:
        master_name_by_id[master_id] = get_master_full_name_by_id(master_id)

    interval_number = 1
    prior_interval_time_start = None
    for interval in current_page_intervals:
        first_slot_id = interval.get("first slot id")
        slot_time_start = interval.get("slot time start")
        client_time_end = interval.get("client time end")
        slot_time_loss = interval.get("slot time loss")
        slot_master_id = interval.get("slot master id")

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

        interval_repeat_txt = ""
        slot_masters_number = time_start_frequency_dict.get(slot_time_start)
        if SLOTS_CONFIGS.SHOW_SAME_TIME_START_SLOT_NUMBER:
            if slot_time_start == prior_interval_time_start:
                interval_number += 1
            else:
                if SLOTS_CONFIGS.SHOW_SAME_TIME_START_FIRST_SLOT_NUMBER:
                    interval_number = 1
            interval_repeat_txt = f" {interval_number}/{slot_masters_number}"
            prior_interval_time_start = slot_time_start

        if (not SLOTS_CONFIGS.SHOW_SLOT_MASTER_FULL_NAME
                or not SLOTS_CONFIGS.SHOW_SLOTS_ADVISES_ICONS):
            start_end_time_separator = " - "
        else:
            start_end_time_separator = "-"

        enrolment_slot_text = (f"{selected_left_icon} "
                               f"{slot_time_start_text}"
                               f"{start_end_time_separator}"
                               f"{client_time_end_text} "
                               f"{interval_repeat_txt}"
                               f"{selected_right_icon}")

        builder_inl_kbd.button(text=enrolment_slot_text,
                               callback_data=cur_slot_callback_data)

        if SLOTS_CONFIGS.SHOW_SLOT_MASTER_FULL_NAME:
            slot_master_full_name = master_name_by_id.get(slot_master_id)
            if slot_master_full_name:
                slot_master_full_name = f" {slot_master_full_name} "
            else:
                slot_master_full_name = f""

            builder_inl_kbd.button(text=f"{slot_master_full_name}",
                                   callback_data=cur_slot_callback_data)

    date_info_adjust = [1]
    pagination_adjust = [3] if total_pages_number > 1 else []
    slot_row_columns_number = (1 + SLOTS_CONFIGS.SHOW_SLOTS_ADVISES_ICONS
                               + SLOTS_CONFIGS.SHOW_SLOT_MASTER_FULL_NAME)

    if selected_slot_id:
        continue_btn_adjust = [1]
        builder_inl_kbd.button(
            text=SLOTS_BUTTONS.CONTINUE,
            callback_data=ContinueSlotSavingCBData())
    else:
        continue_btn_adjust = []

    return_main_menu_bts_adjust = [2]
    if slot_row_columns_number == 2 and not selected_slot_id:
        return_main_menu_bts_adjust = [1]

    builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    dynamic_adjust = (
            date_info_adjust
            + pagination_adjust
            + [int(slot_row_columns_number)] * len(current_page_intervals)
            + continue_btn_adjust
            + return_main_menu_bts_adjust)

    builder_inl_kbd.adjust(*dynamic_adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
