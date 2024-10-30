from datetime import timedelta, datetime

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.association_service_worktime import (
    ServiceWorkTimeAssociation)
from database.db_models.work_time_model import WorkTime
from database.db_queries.get_user_obj_by_telegram_id import (
    get_user_obj_by_telegram_id)
from database.db_queries.worktime_slot_by_id_query import (
    get_worktime_slot_by_id_in_session)
from database.db_utilities.merge_object_transaction_update import (
    merge_obj_to_session_group_update)
from database.db_utilities.slot_taken_msg_rollback_main_menu import (
    slot_taken_msg_rollback_main_menu)
from telegram.config.configs import (
    LANGUAGE_CONFIGS,
    DB_SLOTS_CONFIGS)
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    ContinueSlotSavingCBData)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_dict_by_fsm_state_key,
    get_valid_float_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_selected_services_summary,
    get_summary_services_with_slot)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)
from utilities.calendar_utils import (
    get_date_with_month_name,
    get_time_flex_from_datetime)
from utilities.numeric_utils import number_or_str_to_integer

continue_slot_saving_cb_router = Router(name=__name__)
continue_slot_saving_cb_router.message.filter(ChatTypesFilter(["private"]))


@continue_slot_saving_cb_router.callback_query(ContinueSlotSavingCBData.filter())
async def continue_slot_saving_cb_hdr(callback_query: CallbackQuery,
                                      callback_data: CallbackData,
                                      state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    message = callback_query.message

    current_user_telegram_id = callback_query.from_user.dict().get("id")
    current_user_obj = get_user_obj_by_telegram_id(
        telegram_id=current_user_telegram_id)
    current_user_id = current_user_obj.id

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    selected_interval_first_slot_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_interval_first_slot_id")

    enrollment_intervals = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="enrollment_intervals_state")

    selected_interval = enrollment_intervals.get(
        selected_interval_first_slot_id)
    selected_slots_ids = selected_interval.get("all slots ids")

    selected_slots_ids_except_last_id = selected_slots_ids[:-1]
    last_selected_slot_id = selected_slots_ids[-1]
    last_slot_time_loss = selected_interval.get("slot time loss")

    # ##################################################################
    # Slots group saving and updating Transaction start
    # ##################################################################
    with DBConnection(db_url=db_engine_url) as ongoing_session:
        for slot_id in selected_slots_ids:
            slot_obj = get_worktime_slot_by_id_in_session(
                worktime_slot_id=slot_id,
                ongoing_session=ongoing_session)

            # #################################################################
            # Checking if any slot of selected ones is reserved or not active
            # #################################################################
            if not slot_obj or slot_obj.reserved or not slot_obj.active:
                await slot_taken_msg_rollback_main_menu(
                    message=message,
                    ongoing_session=ongoing_session,
                    state=state)
                return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)

            # #################################################################
            # Checking if any slot of selected ones is defined as admin only
            # #################################################################
            if (DB_SLOTS_CONFIGS.NEW_SLOT_FROM_TIME_LOSS_FOR_ADMIN_ONLY
                    and slot_obj.admin_only):
                await slot_taken_msg_rollback_main_menu(
                    message=message,
                    ongoing_session=ongoing_session,
                    state=state)
                return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)

            new_update_data = {"client_user_id": current_user_id,
                               "reserved": True,
                               "editor_id": current_user_id}

            # #################################################################
            # Ordinary updating all slots except last one with optional time loss
            # #################################################################
            if slot_id in selected_slots_ids_except_last_id:
                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=ongoing_session)
                print(f"\tTEST INFO: Ordinary updating all slots "
                      "(except last slot with optional time loss)\n")

            # #################################################################
            # Ordinary updating last slot if not time loss (effective slot)
            # #################################################################
            if slot_id == last_selected_slot_id and not last_slot_time_loss:
                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=ongoing_session)
                print(f"\tTEST INFO: Ordinary updating last slot "
                      f"if not time loss (slot is very effective)\n")

            time_loss_min_limit = number_or_str_to_integer(
                DB_SLOTS_CONFIGS.MIN_TIME_LOSS_FOR_CREATING_NEW_SLOT,
                positive=True)
            time_loss_min_limit = timedelta(minutes=time_loss_min_limit)

            # #################################################################
            # Ordinary updating last slot (because tyme loss is less min limit)
            # #################################################################
            if (slot_id == last_selected_slot_id and last_slot_time_loss
                    and last_slot_time_loss < time_loss_min_limit):
                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=ongoing_session)
                print(f"\tTEST INFO: Ordinary updating last slot "
                      f"if not time loss (slot is very effective slot)\n")

            # #################################################################
            # Ordinary updating last slot if time loss, but NOT make split flag
            # #################################################################
            if (slot_id == last_selected_slot_id and last_slot_time_loss
                    and last_slot_time_loss >= time_loss_min_limit
                    and not DB_SLOTS_CONFIGS.MAKE_SPLIT_NEW_SLOTS_IF_TIME_LOSS):
                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=ongoing_session)
                print(f"\tTEST INFO: Ordinary updating last slot "
                      f"if not time loss (slot is very effective slot)\n")

            # #################################################################
            # Last slot splitting into effective parts (time loss and make split flag)
            # #################################################################
            if (slot_id == last_selected_slot_id and last_slot_time_loss
                    and last_slot_time_loss >= time_loss_min_limit
                    and DB_SLOTS_CONFIGS.MAKE_SPLIT_NEW_SLOTS_IF_TIME_LOSS):
                client_time_end = selected_interval.get("client time end")

                # getting values before slot object will be updated
                new_update_data = {
                    "client_user_id": current_user_id,
                    "time_start": slot_obj.time_start,
                    "time_end": client_time_end,
                    "slot_duration": client_time_end - slot_obj.time_start,
                    "reserved": True,
                    "editor_id": current_user_id}

                new_slot_obj_from_loss_time = WorkTime(
                    master_id=slot_obj.master_id,
                    client_user_id=None,
                    time_start=client_time_end,
                    time_end=slot_obj.time_end,
                    slot_duration=slot_obj.time_end - client_time_end,
                    reserved=False,
                    admin_only=DB_SLOTS_CONFIGS.NEW_SLOT_FROM_TIME_LOSS_FOR_ADMIN_ONLY,
                    creator_id=current_user_id)

                # Updating split slot with new values
                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=ongoing_session)

                # Adding new effective slot from time loss
                ongoing_session.add(new_slot_obj_from_loss_time)

                print(f"\tTEST INFO: Last slot split into reserved part"
                      f" and effective free part because time loss\n")

            # #################################################################
            # Explicit adding assoc to save repeated services for each work time
            # #################################################################
            for service_id in selected_services_ids:
                service_worktime_assoc = ServiceWorkTimeAssociation(
                    service_id=service_id,
                    work_time_id=slot_id,
                    updated=datetime.now(),
                    creator_id=current_user_id)

                ongoing_session.add(service_worktime_assoc)

        ongoing_session.commit()  # Slot group saving and updating Transaction end

        # #################################################################
        # Info block displaying selected services and time interval summary
        # #################################################################
        selected_date = state_data.get("selected_date_enroll_srcs_calendar")

        selected_services_cost = await get_valid_float_by_fsm_state_key(
            fsm_state_or_dict_from=state_data,
            fsm_state_literal_key="selected_services_cost_state")

        selected_services_duration = await get_valid_timedelta_by_fsm_state_key(
            fsm_state_or_dict_from=state_data,
            fsm_state_literal_key="selected_services_duration_state")

        date_text = get_date_with_month_name(
            selected_date,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        summary_text = get_selected_services_summary(
            services_count=len(selected_services_ids),
            total_cost=selected_services_cost,
            total_duration=selected_services_duration)

        slot_time_start = selected_interval.get("slot time start")
        slot_time_start_text = get_time_flex_from_datetime(
            date_value=slot_time_start,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        client_time_end = selected_interval.get("client time end")
        client_time_end_text = get_time_flex_from_datetime(
            date_value=client_time_end,
            language=LANGUAGE_CONFIGS.LANGUAGE)

        complete_summary_text = get_summary_services_with_slot(
            date_text=date_text,
            summary_text=summary_text,
            slot_time_start=slot_time_start_text,
            slot_time_end=client_time_end_text)

        await message.answer(text=complete_summary_text)

        await state.clear()
        return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)
