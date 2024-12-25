import inspect

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
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
from telegram.keyboard_inline.common_yes_no_dialog_inl_kbd import (
    open_yes_no_dialog_and_get_answer)
from telegram.keyboard_inline.reservations_client_inl_kbd import (
    CancelReservationCBData,
    get_reservation_client_user_inl_kbd)
from telegram.params.buttons_reservations_client import (
    RESERVATIONS_BUTTONS)
from telegram.params.messages import (
    ALL_RESERVATIONS_HERE,
    CONFIRM_CANCEL_RESERVATION)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key,
    get_valid_dict_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

clicked_cancel_reservation_cb_router = Router(name=__name__)
clicked_cancel_reservation_cb_router.message.filter(ChatTypesFilter(["private"]))


class YesNoCancelReservationCBData(CallbackData, prefix="yes no answer confirm dlg"):
    yes_no_dialog_answer: str


@clicked_cancel_reservation_cb_router.callback_query(CancelReservationCBData.filter())
@clicked_cancel_reservation_cb_router.callback_query(YesNoCancelReservationCBData.filter())
async def clicked_cancel_reservation_cb_hdr(callback_query: CallbackQuery,
                                            callback_data: CallbackData,
                                            state: FSMContext,
                                            bot: Bot):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    callback_prefix = callback_data.__prefix__

    # ########### Dialog yes-no open and get answer ####################
    yes_no_dialog_answer = await open_yes_no_dialog_and_get_answer(
        initial_trigger_callback_data_cls=CancelReservationCBData,
        yes_no_answer_callback_data_cls=YesNoCancelReservationCBData,
        yes_no_dialog_msg_text=CONFIRM_CANCEL_RESERVATION,
        yes_button_text=RESERVATIONS_BUTTONS.CANCEL_RESERVATION_YES,
        no_button_text=RESERVATIONS_BUTTONS.CANCEL_RESERVATION_NO,
        callback_query=callback_query,
        callback_data=callback_data,
        state=state)

    if not yes_no_dialog_answer:
        print(f"\tDialog yes-no inl msg opened, answer not received yet:\n"
              f"\tcallback_prefix = {callback_prefix}\n"
              f"\tyes_no_dialog_answer = {yes_no_dialog_answer}\n")
        return
    elif yes_no_dialog_answer == "no":
        print(f"\tAnswer 'no' received from yes-no dialog:\n"
              f"\tcallback_prefix = {callback_prefix}\n"
              f"\tyes_no_dialog_answer = {yes_no_dialog_answer}\n")
        return
    else:
        print(f"\tAnswer 'yes' received from yes-no dialog:\n"
              f"\tcallback_prefix = {callback_prefix}\n"
              f"\tyes_no_dialog_answer = {yes_no_dialog_answer}\n")

    clicked_reservation_id = callback_data.reservation_id

    # ##################################################################
    # ### Reservation and WorkTime operations start (group updating) ###
    # ##################################################################
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
        print(f"\tDB SESSION: Reservation and WorkTime ongoing session\n"
              f"\twas commit (with group records updating)\n")
    # ##################################################################
    # #### Reservation and WorkTime operations end (group updating) ####
    # ##################################################################

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

    prior_reservation_msg_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="reservation_message_id_state")

    try:
        cur_chat_id = callback_query.message.chat.id
        await bot.edit_message_text(
            text=ALL_RESERVATIONS_HERE,
            message_id=prior_reservation_msg_id,
            chat_id=cur_chat_id,
            reply_markup=get_reservation_client_user_inl_kbd(
                current_page_reservations=current_page_reservations,
                total_pages_number=total_pages,
                current_page_number=cur_page_number))
    except (TelegramBadRequest, Exception) as exception_info:
        print(f"\tMessage not modified, tg exception intercepted: {exception_info}\n")

    await state.update_data(
        paginated_reservations_records=paginated_reservations)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
