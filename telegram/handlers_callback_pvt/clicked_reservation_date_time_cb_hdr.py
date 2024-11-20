from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.reservation_obj_by_id_query import (
    get_reservation_obj_by_id)
from telegram.config.configs import (
    LANGUAGE_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.reservations_client_user_inl_kbd import (
    ReservationClickedCBData)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_reservation_detailed_info)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)
from utilities.calendar_utils import (
    get_date_flex_from_datetime,
    get_weekday_flex_abbr_by_date,
    get_time_flex_from_datetime,
    get_hours_minutes_secs_timedelta)

clicked_reservation_date_time_cb_router = Router(name=__name__)
clicked_reservation_date_time_cb_router.message.filter(ChatTypesFilter(["private"]))


@clicked_reservation_date_time_cb_router.callback_query(ReservationClickedCBData.filter())
async def clicked_slot_advising_icon_hint_cb_hdr(callback_query: CallbackQuery,
                                                 callback_data: CallbackData,
                                                 state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    clicked_reservation_id = callback_data.reservation_id
    reservation_obj = get_reservation_obj_by_id(clicked_reservation_id)

    reservation_date = reservation_obj.reservation_date
    reservation_date_txt = get_date_flex_from_datetime(
        date_value=reservation_date,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    reservation_weekday = get_weekday_flex_abbr_by_date(
        date_value=reservation_date,
        language=LANGUAGE_CONFIGS.LANGUAGE,
        symbols_max=2)

    reservation_time_start = reservation_obj.reserved_interval_time_start
    time_start_txt = get_time_flex_from_datetime(
        date_value=reservation_time_start,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    client_time_end = reservation_obj.client_interval_time_end
    time_end_txt = get_time_flex_from_datetime(
        date_value=client_time_end,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    services_total_duration = reservation_obj.reserved_services_total_duration
    srcs_total_duration_txt = get_hours_minutes_secs_timedelta(
        timedelta_value=services_total_duration,
        language=LANGUAGE_CONFIGS.LANGUAGE,
        abbrev_symbols="1",
        separator=" : ")

    services_total_cost = reservation_obj.reserved_services_total_cost

    masters_ids = reservation_obj.reserved_masters_ids
    masters_names_dict = reservation_obj.archive_name_per_master
    masters_names_list = [
        str(masters_names_dict[str(mst_id)]) for mst_id in masters_ids]
    masters_names_txt = ", ".join(masters_names_list)

    services_ids = reservation_obj.reserved_services_ids
    service_name_by_id = reservation_obj.archive_name_per_service
    services_names_list = [
        str(service_name_by_id[str(src_id)]) for src_id in services_ids]
    services_names_txt = ", ".join(services_names_list)

    reservation_detail_info = get_reservation_detailed_info(
        reservation_weekday=reservation_weekday,
        reservation_date=reservation_date_txt,
        reservation_time_start=time_start_txt,
        reservation_time_end=time_end_txt,
        selected_services_duration=srcs_total_duration_txt,
        selected_services_cost=services_total_cost,
        reserved_masters_names=masters_names_txt,
        reserved_services_names=services_names_txt)

    # TG callback query alert message limit max 200 symbols
    if len(reservation_detail_info) <= 200:
        await callback_query.answer(text=reservation_detail_info,
                                    show_alert=True)
    else:
        tg_len_validated_text = reservation_detail_info[0:197] + "..."
        await callback_query.answer(text=tg_len_validated_text,
                                    show_alert=True)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
