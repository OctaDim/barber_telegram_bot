from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardMarkup)

from telegram.config.configs import (LANGUAGE_CONFIGS,
                                     SLOTS_CONFIGS)
from telegram.keyboard_inline.common_buttons_inline import (
    create_return_inline_button,
    create_main_menu_inline_button,
    ReturnInlineBtnCBData)
from telegram.params.buttons_intervals_slots import SLOTS_BUTTONS
from telegram.params.intervals_slots_icons import SLOT_ICONS
from telegram.telegram_utils.messages_helpers import (
    get_slot_advising_icon,
    get_slots_advising_brief_note)
from utilities.calendar_utils import (
    get_date_with_month_name,
    get_time_flex_from_datetime)


class SlotSelectedCBData(CallbackData, prefix="current_slot_selected"):
    first_slot_id: int


class SlotsAdvisingNoteCBData(CallbackData, prefix="slots_advising_note"):
    pass


class ContinueSlotSavingCBData(CallbackData, prefix="continue_slot_saving"):
    pass


def get_enrollment_intervals_inl_kbd(
        selected_date: datetime,
        enrollment_intervals: dict[dict] | dict,
        selected_slot_id: int = None
) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    date_now = get_date_with_month_name(date_value=selected_date,
                                        language=LANGUAGE_CONFIGS.LANGUAGE)
    date_now_text = f"{SLOT_ICONS.DATE_CALENDAR}  {date_now.upper()}"
    builder_inl_kbd.button(text=date_now_text,
                           callback_data=ReturnInlineBtnCBData())

    if SLOTS_CONFIGS.SHOW_SLOTS_ADVISES:
        advising_note_text = get_slots_advising_brief_note()
        builder_inl_kbd.button(text=advising_note_text,
                               callback_data=SlotsAdvisingNoteCBData())

    for interval in enrollment_intervals.values():
        first_slot_id = interval.get("first slot id")
        slot_time_start = interval.get("slot time start")
        client_time_end = interval.get("client time end")
        slot_time_loss = interval.get("slot time loss")

        cur_slot_callback_data = SlotSelectedCBData(
            first_slot_id=first_slot_id).pack()

        if SLOTS_CONFIGS.SHOW_SLOTS_ADVISES:
            advising_icon = get_slot_advising_icon(time_loss=slot_time_loss)
            builder_inl_kbd.button(text=advising_icon,
                                   callback_data=cur_slot_callback_data)

        if selected_slot_id == first_slot_id:
            selected_icon = SLOT_ICONS.SELECTED_SLOT
        else:
            selected_icon = SLOT_ICONS.UNSELECTED_SLOT

        slot_time_start_text = get_time_flex_from_datetime(
            date_value=slot_time_start,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        client_time_end_text = get_time_flex_from_datetime(
            date_value=client_time_end,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        enrolment_slot_text = (f"{selected_icon} "
                               f"{slot_time_start_text} - "
                               f"{client_time_end_text} "
                               f"{selected_icon}")
        builder_inl_kbd.button(text=enrolment_slot_text,
                               callback_data=cur_slot_callback_data)

    if selected_slot_id:
        builder_inl_kbd.button(text=SLOTS_BUTTONS.CONTINUE,
                               callback_data=ContinueSlotSavingCBData())

    builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    date_info_adjust = [1]
    if SLOTS_CONFIGS.SHOW_SLOTS_ADVISES:
        slots_advising_note_adjust = [1]
        slot_row_columns_number = 2
        return_main_meny_bts_adjust = [2] if selected_slot_id else [1]
    else:
        slots_advising_note_adjust = []
        slot_row_columns_number = 1
        return_main_meny_bts_adjust = [2]
    continue_btn_adjust = [1] if selected_slot_id else []

    dynamic_adjust = (
            date_info_adjust
            + slots_advising_note_adjust
            + [int(slot_row_columns_number)] * len(enrollment_intervals)
            + continue_btn_adjust
            + return_main_meny_bts_adjust)

    builder_inl_kbd.adjust(*dynamic_adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
