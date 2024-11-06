from datetime import datetime
from time import sleep

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from database.db_queries.all_slots_from_now_for_month import get_slots_from_now_for_month
from database.db_queries_hepers.enrollment_days_for_month import get_available_enrollment_days
from telegram.config.configs import PAUSE_CONFIGS
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_inline.calendar_inl_kbd import get_enroll_srcs_calendar_inl_kbd
from telegram.params.buttons_enroll_service import ENROLL_SERVICE_BUTTONS
from telegram.params.messages import (
    SELECT_MIN_ONE_SERVICE,
    CHOOSE_SERVICES_DAY)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_float_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key, get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import get_selected_services_summary
from utilities.numeric_utils import number_or_str_to_float

continue_enroll_srcs_pvt_router = Router(name=__name__)
continue_enroll_srcs_pvt_router.message.filter(ChatTypesFilter(["private"]))


@continue_enroll_srcs_pvt_router.message(
    F.text == ENROLL_SERVICE_BUTTONS.CONTINUE_ENROLL_SERVICES)
async def continue_enroll_services_btn_handler(message: Message,
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

    await state.update_data(
        cur_month_enroll_srcs_calendar=month_now,
        cur_year_enroll_srcs_calendar=year_now)

    selected_master_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_master_id")
    if not selected_master_id:
        selected_master_id = "all"

    all_slots_records = get_slots_from_now_for_month(
        year=year_now, month=month_now,
        master_id=selected_master_id,
        reserved=False, active=True, admin_only=False)

    enrollment_days = get_available_enrollment_days(
        slots_records=all_slots_records,
        services_duration=total_duration_selected)

    await message.answer(
        text=CHOOSE_SERVICES_DAY,
        reply_markup=get_enroll_srcs_calendar_inl_kbd(
            calendar_year=year_now,
            calendar_month=month_now,
            enrollment_days=enrollment_days))
