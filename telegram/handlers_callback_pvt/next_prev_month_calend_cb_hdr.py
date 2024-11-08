from datetime import datetime

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_slots_from_now_for_month import (
    get_slots_from_now_for_month)
from database.db_queries_hepers.enrollment_days_for_month import (
    get_available_enrollment_days)
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
    get_valid_timedelta_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

next_prev_month_services_cb_router = Router(name=__name__)
next_prev_month_services_cb_router.message.filter(ChatTypesFilter(["private"]))


@next_prev_month_services_cb_router.callback_query(PreviousMonthCBData.filter())
@next_prev_month_services_cb_router.callback_query(NextMonthCBData.filter())
async def next_prev_month_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                             callback_data: CallbackData,
                                             state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

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

    selected_services_duration = await get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_duration_state")

    selected_master_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_master_id")
    if not selected_master_id:
        selected_master_id = "all"

    all_slots_records = get_slots_from_now_for_month(
        year=calendar_year, month=calendar_month,
        master_id=selected_master_id,
        reserved=False, active=True, admin_only=False)

    enrollment_days = get_available_enrollment_days(
        slots_records=all_slots_records,
        services_duration=selected_services_duration)

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

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
