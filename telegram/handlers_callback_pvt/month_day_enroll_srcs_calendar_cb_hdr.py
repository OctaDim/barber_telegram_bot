from datetime import datetime

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_slots_from_now_for_month import (
    get_slots_from_now_for_month)
from database.db_queries_hepers.enrollment_days_for_month import (
    get_available_enrollment_days)
from telegram.errors_api_telegram.telegram_exception_errors import (
    TG_EXCEPT_ERRORS)
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_inline.calendar_inl_kbd import (
    MonthDayCBData,
    get_enroll_srcs_calendar_inl_kbd)
from telegram.params.messages import CHOOSE_SERVICES_DAY
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

month_day_enroll_srcs_calendar_cb_router = Router(name=__name__)
month_day_enroll_srcs_calendar_cb_router.message.filter(ChatTypesFilter(["private"]))


@month_day_enroll_srcs_calendar_cb_router.callback_query(MonthDayCBData.filter())
async def month_day_enroll_srcs_calendar_cb_hdr(callback_query: CallbackQuery,
                                                callback_data: CallbackData,
                                                state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    selected_day = callback_data.month_day

    selected_month = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="cur_month_enroll_srcs_calendar")

    selected_year = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="cur_year_enroll_srcs_calendar")

    selected_date = datetime(selected_year, selected_month, selected_day)
    await state.update_data(selected_date_enroll_srcs_calendar=selected_date)

    selected_services_duration = await get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_duration_state")

    selected_master_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_master_id")
    if not selected_master_id:
        selected_master_id = "all"

    all_slots_records = get_slots_from_now_for_month(
        year=selected_year, month=selected_month,
        master_id=selected_master_id,
        reserved=False, active=True, admin_only=False)

    enrollment_days = get_available_enrollment_days(
        slots_records=all_slots_records,
        services_duration=selected_services_duration)

    try:
        await callback_query.message.edit_text(
            text=CHOOSE_SERVICES_DAY,
            reply_markup=get_enroll_srcs_calendar_inl_kbd(
                calendar_year=selected_year,
                calendar_month=selected_month,
                selected_date=selected_date,
                enrollment_days=enrollment_days))
    except TelegramBadRequest as error:
        if error.message == TG_EXCEPT_ERRORS.MSG_NOT_MODIFIED:
            print("\tLOG INFO: 'Message not modified' tg exception was intercepted\n")
            pass

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
