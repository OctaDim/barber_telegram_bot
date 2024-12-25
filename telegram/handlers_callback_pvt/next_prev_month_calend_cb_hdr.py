import inspect
from datetime import datetime

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_slots_from_now_for_month_query import (
    get_slots_from_now_for_month_query)
from database.db_queries.masters_ids_common_for_services import (
    get_masters_ids_common_for_services)
from database.db_queries_hepers.enrollment_days_for_month_helper import (
    get_enrollment_days_helper)
from telegram.config.configs import (
    DB_SLOTS_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.calendar_enroll_srcs_inl_kbd import (
    NextMonthCBData,
    PreviousMonthCBData,
    get_calendar_enroll_srcs_inl_kbd)
from telegram.params.messages import (
    CHOOSE_SERVICES_DAY)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key,
    get_valid_list_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)
from utilities.numeric_utils import (
    number_or_str_to_integer)

next_prev_month_services_cb_router = Router(name=__name__)
next_prev_month_services_cb_router.message.filter(ChatTypesFilter(["private"]))


@next_prev_month_services_cb_router.callback_query(PreviousMonthCBData.filter())
@next_prev_month_services_cb_router.callback_query(NextMonthCBData.filter())
async def next_prev_month_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                             callback_data: CallbackData,
                                             state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    await callback_query.answer()

    callback_prefix = callback_data.__prefix__

    calendar_month = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="cur_month_enroll_srcs_calendar")

    calendar_year = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="cur_year_enroll_srcs_calendar")

    if callback_prefix == NextMonthCBData.__prefix__:
        calendar_month += 1
        if calendar_month > 12:
            calendar_month = 1
            calendar_year += 1
    elif callback_prefix == PreviousMonthCBData.__prefix__:
        calendar_month -= 1
        if calendar_month < 1:
            calendar_month = 12
            calendar_year -= 1
    else:
        calendar_month = datetime.now().month
        calendar_year = datetime.now().year

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    selected_services_duration = await get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_duration_state")

    selected_master_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_master_id")

    if not selected_master_id:
        intersecting_masters_ids = get_masters_ids_common_for_services(
            services_ids_list=selected_services_ids)

        all_slots_records = get_slots_from_now_for_month_query(
            year=calendar_year, month=calendar_month,
            masters_ids_list=intersecting_masters_ids,
            order_by_fields=("master_id", "time_start"),
            reserved=False, active=True, admin_only=False)
    else:
        all_slots_records = get_slots_from_now_for_month_query(
            year=calendar_year, month=calendar_month,
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
        selected_services_duration=selected_services_duration,
        time_loss_max_limit=time_loss_max_limit)

    await callback_query.message.edit_text(
        text=CHOOSE_SERVICES_DAY,
        reply_markup=get_calendar_enroll_srcs_inl_kbd(
            calendar_year=calendar_year,
            calendar_month=calendar_month,
            enrollment_days=enrollment_days))

    await state.update_data(
        cur_month_enroll_srcs_calendar=calendar_month,
        cur_year_enroll_srcs_calendar=calendar_year,
        selected_date_enroll_srcs_calendar=None)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
