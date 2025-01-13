import copy
import inspect
import random
from datetime import timedelta

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.reservation_model import (
    Reservation)
from database.db_models.work_time_model import (
    WorkTime)
from database.db_queries.masters_objs_by_ids_list import (
    get_unique_masters_objs_by_ids_list)
from database.db_queries.services_objects_by_ids_list import (
    get_unique_services_objs_by_ids_list)
from database.db_queries.user_obj_by_telegram_id import (
    get_user_obj_by_telegram_id)
from database.db_queries.worktime_obj_by_id_query import (
    get_worktime_obj_by_id_session)
from database.db_queries_hepers.add_service_worktime_assoc_explicit import (
    directly_add_service_worktime_association)
from database.db_utilities.merge_object_transaction_update import (
    merge_obj_to_session_group_update)
from telegram.config.configs import (
    LANGUAGE_CONFIGS,
    DB_SLOTS_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.handler_helpers.forward_intervals_slots_to_saving_inl_inl import (
    delete_intervals_slots_msgs_before_saving_slots)
from telegram.handlers_private.main_menu_btn_reply_hdr_pvt import (
    main_menu_btn_reply_hdr_pvt)
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    ContinueSlotSavingCBData)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    SLOT_ALREADY_TAKEN,
    MAX_PERSON_GROUP_LIMIT_REACHED,
    CLIENT_ALREADY_ENROLLED,
    DATE_NOT_SET,
    AFTER_SLOT_SAVING_MAIN_MENU)
from telegram.params.messages_variants import (
    SERVICES_CONGRATS_VARIANTS)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_dict_by_fsm_state_key,
    get_valid_float_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict, show_handlers_stack_logs)
from telegram.telegram_utils.messages_helpers import (
    get_selected_services_summary,
    get_summary_services_with_slot)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    re_open_reply_keyboard_message)
from utilities.calendar_utils import (
    get_date_with_month_name,
    get_hours_minutes_secs_timedelta, get_time_flex_from_datetime)
from utilities.numeric_utils import (
    number_or_str_to_integer)

continue_slot_saving_enroll_srcs_cb_router = Router(name=__name__)
continue_slot_saving_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@continue_slot_saving_enroll_srcs_cb_router.callback_query(ContinueSlotSavingCBData.filter())
async def continue_slot_saving_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                                  callback_data: CallbackData,
                                                  state: FSMContext,
                                                  bot: Bot):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    message = callback_query.message

    # Getting without validation and setting now if None, because certain date
    selected_date = state_data.get("selected_date_enroll_srcs_calendar")
    if not selected_date:
        await callback_query.answer(text=DATE_NOT_SET,
                                    show_alert=True)
        return

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    selected_services_cost = await get_valid_float_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_cost_state")

    selected_services_duration = await get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_duration_state")

    selected_interval_first_slot_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_interval_first_slot_id")

    enrollment_intervals = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="enrollment_intervals_state")

    selected_interval = enrollment_intervals.get(
        selected_interval_first_slot_id)
    selected_slots_ids = selected_interval.get("all slots ids")
    slot_time_start = selected_interval.get("slot time start")
    client_time_end = selected_interval.get("client time end")
    master_time_end = selected_interval.get("slot time end")
    master_id = selected_interval.get("slot master id")

    selected_slots_ids_except_last_id = selected_slots_ids[:-1]
    last_selected_slot_id = selected_slots_ids[-1]
    last_slot_time_loss = selected_interval.get("slot time loss")

    # Transaction start (with group adding and updating)
    with DBConnection(db_url=db_engine_url) as session_ongoing:
        current_user_telegram_id = callback_query.from_user.id
        current_user_obj = get_user_obj_by_telegram_id(
            telegram_id=current_user_telegram_id)
        current_user_id = current_user_obj.id

        # ##############################################################
        # WorkTime operations start (group adding and updating slots) ##
        # ##############################################################
        for slot_id in selected_slots_ids:
            slot_obj = get_worktime_obj_by_id_session(
                worktime_slot_id=slot_id,
                ongoing_session=session_ongoing)

            new_update_data = {"selected_services": selected_services_ids,
                               "reserved": True,
                               "editor_id": current_user_id}

            time_loss_min_limit = number_or_str_to_integer(
                DB_SLOTS_CONFIGS.MIN_TIME_LOSS_FOR_CREATING_NEW_SLOT,
                positive=True)
            time_loss_min_limit = timedelta(minutes=time_loss_min_limit)

            # For the future. Checking group parameters
            if not len(slot_obj.work_time_clients):
                enrolled_clients_number = 0
            else:
                enrolled_clients_number = len(slot_obj.work_time_clients)

            if not slot_obj.max_clients_limit:
                max_person_worktime_limit = 1
            else:
                max_person_worktime_limit = slot_obj.max_clients_limit

            # For the future. Checking if client is already enrolled before
            if (slot_obj.is_group
                    and current_user_obj in slot_obj.work_time_clients):
                await callback_query.answer(text=CLIENT_ALREADY_ENROLLED)
                session_ongoing.rollback()
                # Call the same functionality handler of the reply keyboard button
                await main_menu_btn_reply_hdr_pvt(message=message, state=state)
                # return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)

            # For the future. Checking if clients number >= max client limit
            elif (slot_obj.is_group
                  and enrolled_clients_number >= max_person_worktime_limit):
                await callback_query.answer(text=MAX_PERSON_GROUP_LIMIT_REACHED)
                session_ongoing.rollback()
                # Call the same functionality handler of the reply keyboard button
                await main_menu_btn_reply_hdr_pvt(message=message, state=state)
                # return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)

            # Checking if slot non group and is already reserved
            elif not slot_obj.is_group and slot_obj.reserved:
                await callback_query.answer(text=SLOT_ALREADY_TAKEN)
                session_ongoing.rollback()
                # Call the same functionality handler of the reply keyboard button
                await main_menu_btn_reply_hdr_pvt(message=message, state=state)
                # return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)

            # Checking if not slot obj or not active
            elif not slot_obj or not slot_obj.active:
                await callback_query.answer(text=SLOT_ALREADY_TAKEN)
                session_ongoing.rollback()
                # Call the same functionality handler of the reply keyboard button
                await main_menu_btn_reply_hdr_pvt(message=message, state=state)
                # return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)

            # Checking if any slot of selected ones is defined as admin only
            elif (DB_SLOTS_CONFIGS.NEW_SLOT_FROM_TIME_LOSS_FOR_ADMIN_ONLY
                  and slot_obj.admin_only):
                await callback_query.answer(text=SLOT_ALREADY_TAKEN)
                session_ongoing.rollback()
                # Call the same functionality handler of the reply keyboard button
                await main_menu_btn_reply_hdr_pvt(message=message, state=state)
                # return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)

            # Ordinary updating all slots except last one with optional time loss
            if slot_id in selected_slots_ids_except_last_id:
                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=session_ongoing)
                print(f"\tDB SESSION: Ordinary updating all slots\n"
                      f"\t(except last slot with optional time loss)\n")

            # Ordinary updating last slot if not time loss (effective slot)
            elif slot_id == last_selected_slot_id and not last_slot_time_loss:
                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=session_ongoing)
                print(f"\tDB SESSION: Ordinary updating last slot\n"
                      f"\tif not time loss (slot is very effective)\n")

            # Ordinary updating last slot (because tyme loss is less min limit)
            elif (slot_id == last_selected_slot_id and last_slot_time_loss
                  and last_slot_time_loss < time_loss_min_limit):
                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=session_ongoing)
                print(f"\tDB SESSION: Ordinary updating last slot\n"
                      f"\tif not time loss (slot is very effective slot)\n")

            # Ordinary updating last slot if time loss, but NOT make split flag
            elif (slot_id == last_selected_slot_id and last_slot_time_loss
                  and last_slot_time_loss >= time_loss_min_limit
                  and not DB_SLOTS_CONFIGS.MAKE_SPLIT_NEW_SLOTS_IF_TIME_LOSS):
                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=session_ongoing)
                print(f"\tDB SESSION: Ordinary updating last slot\n"
                      f"\tif not time loss (slot is very effective slot)\n")

            # Last slot splitting into effective parts (time loss and make split flag)
            elif (slot_id == last_selected_slot_id and last_slot_time_loss
                  and last_slot_time_loss >= time_loss_min_limit
                  and DB_SLOTS_CONFIGS.MAKE_SPLIT_NEW_SLOTS_IF_TIME_LOSS):

                client_time_end = selected_interval.get("client time end")
                master_time_end = client_time_end
                slot_time_end_before_update = slot_obj.time_end

                # getting values before existing slot object will be updated
                new_update_data = {
                    "time_start": slot_obj.time_start,
                    "time_end": client_time_end,
                    "slot_duration": client_time_end - slot_obj.time_start,
                    "selected_services": selected_services_ids,
                    "reserved": True,
                    "editor_id": current_user_id}

                merge_obj_to_session_group_update(
                    object_to_merge=slot_obj,
                    new_update_data=new_update_data,
                    ongoing_session=session_ongoing)

                new_slot_obj_from_loss_time = WorkTime(
                    master_id=slot_obj.master_id,
                    time_start=client_time_end,
                    time_end=slot_time_end_before_update,
                    slot_duration=slot_time_end_before_update - client_time_end,
                    reserved=False,
                    admin_only=DB_SLOTS_CONFIGS.NEW_SLOT_FROM_TIME_LOSS_FOR_ADMIN_ONLY,
                    creator_id=current_user_id)

                session_ongoing.add(new_slot_obj_from_loss_time)
                print(f"\tDB SESSION: Last slot split into reserved part\n"
                      f"\tand effective free part because time loss\n")

            # Adding records directly to save non-unique pairs worktime - service
            directly_add_service_worktime_association(
                selected_services_ids=selected_services_ids,
                worktime_slot_id=slot_id,
                current_user_id=current_user_id,
                ongoing_session=session_ongoing)

            slot_obj.work_time_clients.append(current_user_obj)
        # ##############################################################
        # WorkTime operations end (with group adding and updating slots)
        # ##############################################################

        # ##############################################################
        # ### Reservation operations start (adding all statistical info)
        # ##############################################################
        services_objs = get_unique_services_objs_by_ids_list(
            services_ids_list=selected_services_ids,
            ongoing_session=session_ongoing)

        arch_name_per_service = {}
        arch_price_per_service = {}
        arch_duration_per_service = {}

        for service_obj in services_objs:
            service_id = service_obj.id
            arch_name_per_service[service_id] = service_obj.name
            arch_price_per_service[service_id] = service_obj.price
            arch_duration_per_service[
                service_id] = service_obj.time_duration.total_seconds()

        masters_ids = [master_id]  # For the future, when masters many
        masters_objs = get_unique_masters_objs_by_ids_list(
            masters_ids_list=masters_ids,
            ongoing_session=session_ongoing)

        arch_name_per_master = {}
        for master_obj in masters_objs:
            arch_name_per_master[master_obj.id] = master_obj.full_name

        master_interval_duration = master_time_end - slot_time_start
        client_interval_duration = client_time_end - slot_time_start
        interval_time_loss = master_interval_duration - client_interval_duration

        new_user_reservation = Reservation(
            reservation_date=selected_date,
            client_user_id=current_user_id,

            reserved_interval_first_slot_id=selected_interval_first_slot_id,
            reserved_slots_ids=selected_slots_ids,

            reserved_interval_time_start=slot_time_start,
            master_interval_time_end=master_time_end,
            client_interval_time_end=client_time_end,

            master_interval_duration=master_interval_duration,
            client_interval_duration=client_interval_duration,
            interval_time_loss=interval_time_loss,

            reserved_services_ids=selected_services_ids,
            reserved_services_total_cost=selected_services_cost,
            reserved_services_total_duration=selected_services_duration,

            archive_name_per_service=arch_name_per_service,
            archive_price_per_service=arch_price_per_service,
            archive_duration_per_service=arch_duration_per_service,

            reserved_masters_ids=masters_ids,
            archive_name_per_master=arch_name_per_master,

            creator_id=current_user_id)

        session_ongoing.add(new_user_reservation)
        # ##############################################################
        # ##### Reservation operations end (adding all statistical info)
        # ##############################################################

        # Transaction end (with group adding and updating)
        session_ongoing.commit()
        print(f"\tDB SESSION: WorkTime and Reservation ongoing session\n"
              f"\twas commit (with group records adding and updating)\n")

    # ##################################################################
    # Info block showing user selected services and time interval summary
    # ##################################################################
    date_text = get_date_with_month_name(
        selected_date,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    selected_services_txt = get_hours_minutes_secs_timedelta(
        timedelta_value=selected_services_duration,
        language=LANGUAGE_CONFIGS.LANGUAGE,
        abbrev_symbols=3,
        separator=' ',
        space_before_note=True,
        hide_zero_values=True)

    summary_text = get_selected_services_summary(
        services_count=len(selected_services_ids),
        total_cost=selected_services_cost,
        total_duration=selected_services_txt)

    slot_time_start_text = get_time_flex_from_datetime(
        date_value=slot_time_start,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    client_time_end_text = get_time_flex_from_datetime(
        date_value=client_time_end,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    congratulation_txt = random.choice(SERVICES_CONGRATS_VARIANTS)

    complete_summary_text = get_summary_services_with_slot(
        congratulation_text=congratulation_txt,
        date_text=date_text,
        summary_text=summary_text,
        slot_time_start=slot_time_start_text,
        slot_time_end=client_time_end_text)

    # ##################################################################
    # Delete prior handler intervals slots msgs before saving slots msgs
    # ##################################################################
    await delete_intervals_slots_msgs_before_saving_slots(
        callback_query=callback_query, state=state, bot=bot)
    # ##################################################################

    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="handlers_stack")

    prior_handler_dict = handlers_list[-1]
    prior_handler_msgs_ids = prior_handler_dict.get("handler_messages_ids")
    messages_ids_to_delete_copy = copy.copy(prior_handler_msgs_ids)
    prior_inline_message_id = messages_ids_to_delete_copy[0]
    print(f"\tOrigin data:\n"
          f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\tprior_inline_message_id = {prior_inline_message_id}\n")

    try:
        cur_message = await bot.edit_message_text(
            text=complete_summary_text,
            message_id=prior_inline_message_id,
            chat_id=callback_query.message.chat.id)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tPrior msg was edited to 'Complete Summary' message"
              f"\tmsg successfully\n")

    except (TelegramBadRequest, Exception) as exception_info:
        cur_message = await callback_query.message.answer(
            text=complete_summary_text)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tNew 'Complete Summary' message was created, because "
              f"\tprior message is not editable: {exception_info}\n")

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=message,
        re_open_reply_msg_text=AFTER_SLOT_SAVING_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=True,
        open_reply_kbd_msg_anyway=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    await state.update_data(
        handlers_stack=handlers_list)
    print(f"\tFSM state 'handlers_stack' updated:\n"
          f"\tlen(handlers_list)={len(handlers_list)}\n")

    await show_handlers_stack_logs(state=state)

    await state.clear()
    print(f"\tFSM State cleared:\n"
          f"\tlen(handlers_list)={len(handlers_list)}\n")

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
