from datetime import datetime
from time import sleep

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from database.db_queries.all_slots_from_now_for_month_query import (
    get_slots_from_now_for_month_query)
from database.db_queries.masters_ids_common_for_services import (
    get_masters_ids_common_for_services)
from database.db_queries_hepers.enrollment_days_for_month_helper import (
    get_enrollment_days_helper)
from telegram.config.configs import (
    PAUSE_CONFIGS,
    DB_SLOTS_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.calendar_enroll_srcs_inl_kbd import (
    get_calendar_enroll_srcs_inl_kbd)
from telegram.params.buttons_enroll_service import (
    ENROLL_SERVICE_BUTTONS)
from telegram.params.messages import (
    SELECT_MIN_ONE_SERVICE,
    CHOOSE_SERVICES_DAY)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_float_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_selected_services_summary)
from utilities.numeric_utils import (
    number_or_str_to_float,
    number_or_str_to_integer)

continue_enroll_srcs_pvt_router = Router(name=__name__)
continue_enroll_srcs_pvt_router.message.filter(ChatTypesFilter(["private"]))


@continue_enroll_srcs_pvt_router.message(
    F.text == ENROLL_SERVICE_BUTTONS.CONTINUE_ENROLL_SERVICES)
async def continue_enroll_srcs_btn_reply_hdr_pvt(message: Message,
                                                 state: FSMContext):
    state_data = await state.get_data()

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    if not selected_services_ids:
        await message.answer(text=SELECT_MIN_ONE_SERVICE)
        sleep(number_or_str_to_float(PAUSE_CONFIGS.SHORT_MSG_DELAY))

        handlers_list = await get_valid_list_by_fsm_state_key(
            fsm_state_or_dict_from=state_data,
            fsm_state_literal_key="handlers_stack")
        await execute_last_stack_handler(handlers_list=handlers_list)

        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

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

    await message.answer(text=summary_text,
                         reply_markup=ReplyKeyboardRemove())

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

    await message.answer(
        text=CHOOSE_SERVICES_DAY,
        reply_markup=get_calendar_enroll_srcs_inl_kbd(
            calendar_year=year_now,
            calendar_month=month_now,
            enrollment_days=enrollment_days))

    await state.update_data(
        cur_month_enroll_srcs_calendar=month_now,
        cur_year_enroll_srcs_calendar=year_now)

    return
