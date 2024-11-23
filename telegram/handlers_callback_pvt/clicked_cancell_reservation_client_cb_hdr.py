from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_queries.reservation_obj_by_id_query import (
    get_reservation_obj_by_id_session)
from database.db_queries.service_worktime_asc_objs_by_wt_srcs_ids import (
    get_service_worktime_asc_objs)
from database.db_queries.user_obj_by_telegram_id import (
    get_user_by_telegram_id_in_session)
from database.db_queries.worktime_obj_by_id_query import (
    get_worktime_obj_by_id_session)
from database.db_utilities.merge_object_transaction_update import (
    merge_obj_to_session_group_update)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.reservations_client_user_inl_kbd import (
    CancelReservationCBData,
    get_reservation_client_user_inl_kbd)
from telegram.params.messages import (
    ALL_RESERVATIONS_HERE)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key,
    get_valid_dict_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

clicked_cancel_reservation_client_cbr = Router(name=__name__)
clicked_cancel_reservation_client_cbr.message.filter(ChatTypesFilter(["private"]))


@clicked_cancel_reservation_client_cbr.callback_query(CancelReservationCBData.filter())
async def clicked_cancel_reservation_client_cb_hdr(callback_query: CallbackQuery,
                                                   callback_data: CallbackData,
                                                   state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    clicked_reservation_id = callback_data.reservation_id

    # ########### Transaction start (with group updating) ##############
    with DBConnection(db_url=db_engine_url) as session_ongoing:
        current_user_telegram_id = callback_query.from_user.id
        current_user_obj = get_user_by_telegram_id_in_session(
            telegram_id=current_user_telegram_id,
            ongoing_session=session_ongoing)
        current_user_id = current_user_obj.id

        reservation_obj = get_reservation_obj_by_id_session(
            reservation_id=clicked_reservation_id,
            ongoing_session=session_ongoing)

        reservation_new_update = {"cancelled_by_client": True}
        merge_obj_to_session_group_update(
            object_to_merge=reservation_obj,
            new_update_data=reservation_new_update,
            ongoing_session=session_ongoing)

        reserved_slots_ids = reservation_obj.reserved_slots_ids
        for slot_id in reserved_slots_ids:
            worktime_obj = get_worktime_obj_by_id_session(
                worktime_slot_id=slot_id,
                ongoing_session=session_ongoing)

            if worktime_obj and not worktime_obj.is_group:
                slot_new_update_data = {"selected_services": None,
                                        # enrolled_users: None,  # For future
                                        "reserved": False,
                                        "editor_id": current_user_id}

                merge_obj_to_session_group_update(
                    object_to_merge=worktime_obj,
                    new_update_data=slot_new_update_data,
                    ongoing_session=session_ongoing)

                work_time_clients = worktime_obj.work_time_clients
                work_time_clients.clear()

                services_objs = worktime_obj.work_time_services
                services_ids = [service.id for service in services_objs]
                service_worktime_asc_objects = get_service_worktime_asc_objs(
                    worktime_id=worktime_obj.id,
                    services_ids=services_ids,
                    ongoing_session=session_ongoing)

                for service_worktime_obj in service_worktime_asc_objects:
                    session_ongoing.delete(service_worktime_obj)

        # Transaction end (with group updating)
        session_ongoing.commit()

    cur_page_number = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="current_page_number_of_reservations")
    cur_page_number = 1 if not cur_page_number else cur_page_number

    paginated_reservations = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="paginated_reservations_records")

    current_page_reservations = paginated_reservations.get(cur_page_number)

    for reservation_obj in current_page_reservations:
        if reservation_obj.id == clicked_reservation_id:
            reservation_obj.cancelled_by_client = True
    paginated_reservations[cur_page_number] = current_page_reservations

    total_pages = len(paginated_reservations)

    await callback_query.message.edit_text(
        text=ALL_RESERVATIONS_HERE,
        reply_markup=get_reservation_client_user_inl_kbd(
            current_page_reservations=current_page_reservations,
            total_pages_number=total_pages,
            current_page_number=cur_page_number))

    await state.update_data(
        paginated_reservations_records=paginated_reservations)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
