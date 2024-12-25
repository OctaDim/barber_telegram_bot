import copy
import inspect
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.db_queries.all_slots_from_now_for_month_query import (
    get_slots_from_now_for_month_query)
from database.db_queries.masters_ids_common_for_services import (
    get_masters_ids_common_for_services)
from database.db_queries_hepers.enrollment_days_for_month_helper import (
    get_enrollment_days_helper)
from telegram.config.configs import (
    DB_SLOTS_CONFIGS,
    PAUSE_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.handler_helpers.forward_services_filtered_to_calendar_rep_inl import (
    delete_srcs_filtered_msgs_before_calendar)
from telegram.keyboard_inline.calendar_enroll_srcs_inl_kbd import (
    get_calendar_enroll_srcs_inl_kbd)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.buttons_enroll_service import (
    ENROLL_SRCS_BUTTONS)
from telegram.params.messages import (
    CHOOSE_SERVICES_DAY,
    SELECT_MIN_ONE_SERVICE,
    OR_SELECT_MAIN_MENU_BUTTON)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_float_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_selected_services_summary)
from telegram.telegram_utils.messages_utils import (
    send_warning_message_with_delete_delay, \
    re_open_reply_keyboard_message)
from utilities.numeric_utils import (
    number_or_str_to_integer)

continue_enroll_srcs_pvt_router = Router(name=__name__)
continue_enroll_srcs_pvt_router.message.filter(ChatTypesFilter(["private"]))


@continue_enroll_srcs_pvt_router.message(F.text == ENROLL_SRCS_BUTTONS.CONTINUE_ENROLL_SERVICES)
async def calendar_on_continue_enroll_srcs_btn_rep_hdr(message: Message,
                                                       bot: Bot,
                                                       state: FSMContext):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    if not selected_services_ids:
        await send_warning_message_with_delete_delay(
            message_text=SELECT_MIN_ONE_SERVICE,
            message=message,
            delete_delay_seconds=PAUSE_CONFIGS.WARNING_MESSAGE_DELAY)
        return get_handler_answer_flag_dict(
            executed_handler_name=inspect.currentframe().f_code.co_name)

    total_cost_selected = await get_valid_float_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_cost_state")

    total_duration_selected = await get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_duration_state")

    summary_text = get_selected_services_summary(
        services_count=len(selected_services_ids),
        total_cost=total_cost_selected,
        total_duration=total_duration_selected)

    year_now = datetime.now().year
    month_now = datetime.now().month

    selected_master_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_master_id")

    if not selected_master_id:
        intersecting_masters_ids = get_masters_ids_common_for_services(
            services_ids_list=selected_services_ids)

        all_slots_records = get_slots_from_now_for_month_query(
            year=year_now, month=month_now,
            masters_ids_list=intersecting_masters_ids,
            order_by_fields=("master_id", "time_start"),
            reserved=False, active=True, admin_only=False)
    else:
        all_slots_records = get_slots_from_now_for_month_query(
            year=year_now, month=month_now,
            master_id=selected_master_id,
            order_by_fields=("time_start",),
            reserved=False, active=True, admin_only=False)

    if DB_SLOTS_CONFIGS.HIDE_SLOTS_OVER_TIME_LOSS_MAX_LIMIT:
        time_loss_max_limit = number_or_str_to_integer(
            DB_SLOTS_CONFIGS.TIME_LOSS_MAX_LIMIT_FOR_HIDE_SLOTS,
            positive=True)
    else:
        # Any big minutes value to see slots with any time loss
        time_loss_max_limit = 99999

    enrollment_days = get_enrollment_days_helper(
        slots_records=all_slots_records,
        selected_services_duration=total_duration_selected,
        time_loss_max_limit=time_loss_max_limit)

    # ##################################################################
    # Delete prior handler enroll services msgs before calendar messages
    # ##################################################################
    await delete_srcs_filtered_msgs_before_calendar(
        message=message, state=state, bot=bot)
    # ##################################################################

    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="handlers_stack")
    print(f"\tOrigin handler stack: len(handlers_list)={len(handlers_list)}\n")

    prior_handler_dict = handlers_list[-1]
    prior_handler_msgs_ids = prior_handler_dict.get("handler_messages_ids")
    messages_ids_to_delete_copy = copy.copy(prior_handler_msgs_ids)
    prior_inline_message_id = messages_ids_to_delete_copy[0]
    print(f"\tOrigin data:\n"
          f"\t\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\t\tprior_inline_message_id = {prior_inline_message_id}\n")

    try:
        cur_message = await bot.edit_message_text(
            text=CHOOSE_SERVICES_DAY,
            message_id=prior_inline_message_id,
            chat_id=message.chat.id,
            reply_markup=get_calendar_enroll_srcs_inl_kbd(
                calendar_year=year_now,
                calendar_month=month_now,
                enrollment_days=enrollment_days))
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tPrior message was edited to Calendar message successfully\n")

    except (TelegramBadRequest, Exception) as exception_info:
        cur_message = await message.answer(
            text=CHOOSE_SERVICES_DAY,
            reply_markup=get_calendar_enroll_srcs_inl_kbd(
                calendar_year=year_now,
                calendar_month=month_now,
                enrollment_days=enrollment_days))
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tNew Calendar message was created, because "
              f"\tprior message is not editable: {exception_info}\n")

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=message,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU_BUTTON,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=True,
        open_reply_kbd_msg_anyway=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    await state.update_data(
        cur_month_enroll_srcs_calendar=month_now,
        cur_year_enroll_srcs_calendar=year_now,
        # Addition updates:
        actual_message_min_id=prior_inline_message_id)  # First inl msg in many

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=True,
        handler_messages_ids=cur_handler_messages_ids,
        # update_min_actual_msg_id=False,  # Because first inl msg in many msgs
        executed_handler_name=inspect.currentframe().f_code.co_name)
