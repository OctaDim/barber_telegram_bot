from datetime import datetime
from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardMarkup)

from database.db_models.reservation_model import (
    Reservation)
from telegram.config.configs import (
    LANGUAGE_CONFIGS,
    RESERVATIONS_CONFIGS)
from telegram.keyboard_inline.common_buttons_inline import (
    create_return_inline_button,
    create_main_menu_inline_button)
from telegram.params.buttons_reservations_client import (
    RESERVATIONS_BUTTONS)
from telegram.params.icons_reservations import (
    RESERVATIONS_ICONS)
from utilities.calendar_utils import (
    get_date_flex_from_datetime,
    get_weekday_flex_abbr_by_date,
    get_time_flex_from_datetime)


class PreviousReservationPageCBData(CallbackData, prefix="previous reservation page"):
    pass


class ReservationPageNumberCBData(CallbackData, prefix="reservation page number"):
    page_number: int


class NextReservationPageCBData(CallbackData, prefix="next reservation page"):
    pass


class ReservationClickedDateTimeCBData(CallbackData, prefix="reservation date time clicked"):
    reservation_id: int


class CancelReservationCBData(CallbackData, prefix="cancel reservation callback"):
    reservation_id: int


class ReservationCompletedCBData(CallbackData, prefix="reservation already completed"):
    pass


class ReservationCancelledByAdminCBData(CallbackData, prefix="reservation cancelled by admin"):
    pass


class ReservationCancelledByClientCBData(CallbackData, prefix="reservation cancelled by client"):
    pass


def get_reservation_client_user_inl_kbd(
        current_page_reservations: List[Reservation],
        total_pages_number: int,
        current_page_number: int = 1
) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    if total_pages_number > 1:
        builder_inl_kbd.button(
            text=RESERVATIONS_ICONS.PREVIOUS_PAGE,
            callback_data=PreviousReservationPageCBData())

        builder_inl_kbd.button(
            text=f"{RESERVATIONS_BUTTONS.PAGE}  "
                 f"{current_page_number} / {total_pages_number}",
            callback_data=ReservationPageNumberCBData(
                page_number=current_page_number).pack())

        builder_inl_kbd.button(
            text=RESERVATIONS_ICONS.NEXT_PAGE,
            callback_data=NextReservationPageCBData())

    for reservation_obj in current_page_reservations:
        reservation_id = reservation_obj.id
        # for future, to reverse reservation cancel
        reservation_slots_ids = reservation_obj.reserved_slots_ids

        reservation_date = reservation_obj.reservation_date
        reservation_date_text = get_date_flex_from_datetime(
            date_value=reservation_date,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        reservation_weekday = get_weekday_flex_abbr_by_date(
            date_value=reservation_date,
            language=LANGUAGE_CONFIGS.LANGUAGE,
            symbols_max=2)

        reservation_time_start = reservation_obj.reserved_interval_time_start
        time_start_text = get_time_flex_from_datetime(
            date_value=reservation_time_start,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        client_time_end = reservation_obj.client_interval_time_end
        time_end_text = get_time_flex_from_datetime(
            date_value=client_time_end,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        cur_reservation_cb_data = ReservationClickedDateTimeCBData(
            reservation_id=reservation_id).pack()

        if RESERVATIONS_CONFIGS.SHOW_RESERVATION_WEEKDAY:
            builder_inl_kbd.button(
                text=f"{reservation_date_text} {reservation_weekday}",
                callback_data=cur_reservation_cb_data)
        else:
            builder_inl_kbd.button(
                text=f"{reservation_date_text}",
                callback_data=cur_reservation_cb_data)

        builder_inl_kbd.button(
            text=f"{time_start_text}  -  {time_end_text}",
            callback_data=cur_reservation_cb_data)

        if reservation_obj.cancelled_by_client:
            action_btn_cb_data = ReservationCancelledByClientCBData()
            action_btn_caption = RESERVATIONS_BUTTONS.CANCELLED_BY_USER
        elif reservation_obj.cancelled_by_admin:
            action_btn_cb_data = ReservationCancelledByAdminCBData()
            action_btn_caption = RESERVATIONS_BUTTONS.CANCELLED_BY_ADMIN
        else:
            if reservation_time_start <= datetime.now():
                action_btn_cb_data = ReservationCompletedCBData()
                action_btn_caption = RESERVATIONS_BUTTONS.COMPLETED_RESERVATION
            else:
                action_btn_cb_data = CancelReservationCBData(
                    reservation_id=reservation_id).pack()
                action_btn_caption = RESERVATIONS_BUTTONS.CANCEL_RESERVATION

        builder_inl_kbd.button(
            text=action_btn_caption,
            callback_data=action_btn_cb_data)

    builder_inl_kbd.add(create_return_inline_button())
    builder_inl_kbd.add(create_main_menu_inline_button())

    pagination_adjust = [3] if total_pages_number > 1 else []
    # return_main_menu_bts_adjust = [1]  # Without Return button
    return_main_menu_bts_adjust = [2]  # With Return button

    dynamic_adjust = (pagination_adjust
                      + [3] * len(current_page_reservations)
                      + return_main_menu_bts_adjust)

    builder_inl_kbd.adjust(*dynamic_adjust)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
