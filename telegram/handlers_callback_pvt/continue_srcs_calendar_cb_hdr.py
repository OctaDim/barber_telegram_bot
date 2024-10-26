from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_slots_from_now_for_date import (
    get_slots_from_now_for_date)
from database.db_queries_hepers.enrollment_intervals_for_date import (
    get_available_enrollment_intervals)
from database.db_queries_hepers.remove_intervals_by_time_loss import (
    remove_intervals_over_time_loss_limit)
from telegram.config.configs import (LANGUAGE_CONFIGS,
                                     DB_SLOTS_CONFIGS)
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_inline.calendar_inl_kbd import MonthContinueCBData
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    get_enrollment_intervals_inl_kbd)
from telegram.params.calendar_icons import CALENDAR_ICONS
from telegram.params.messages import (
    SELECT_ENROLLMENT_SLOTS,
    NO_FREE_ENROLLMENT_SLOTS)
from telegram.params.messages_inserts import MSG
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_float_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key,
    get_valid_dict_by_fsm_state_key, get_valid_datetime_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import get_handler_answer_flag_dict
from telegram.telegram_utils.messages_helpers import get_selected_services_summary
from telegram.telegram_utils.messages_utils import inline_keyboard_is_actual
from utilities.calendar_utils import get_date_with_month_name

continue_enroll_srcs_calendar_cb_router = Router(name=__name__)
continue_enroll_srcs_calendar_cb_router.message.filter(ChatTypesFilter(["private"]))


@continue_enroll_srcs_calendar_cb_router.callback_query(MonthContinueCBData.filter())
async def continue_enroll_srcs_calendar_cb_hdr(callback_query: CallbackQuery,
                                               callback_data: CallbackData,
                                               state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    await callback_query.answer()

    message = callback_query.message

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_ids_state")

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

    selected_date = await get_valid_datetime_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_date_enroll_srcs_calendar")

    date_text = get_date_with_month_name(
        selected_date,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    master_id = None  # For the future, to define master_id selected by user/client
    all_slots_records = get_slots_from_now_for_date(
        required_date=selected_date,
        master_id=None)

    enrollment_intervals = get_available_enrollment_intervals(
        slots_records=all_slots_records,
        selected_services_duration=total_duration_selected)

    if not enrollment_intervals:
        await message.answer(text=NO_FREE_ENROLLMENT_SLOTS)
        return get_handler_answer_flag_dict(upd_actual_msg_min_id=True,
                                            skip_add_handler_stack=True)

    if DB_SLOTS_CONFIGS.LIMIT_SLOTS_BY_TIME_LOSS:
        remove_intervals_over_time_loss_limit(
            enrollment_intervals=enrollment_intervals,
            time_loss_max_limit=DB_SLOTS_CONFIGS.SLOT_TIME_LOSS_MAX_LIMIT)

    await message.answer(
        text=f"{CALENDAR_ICONS.CALENDAR} {MSG.SELECTED_DATE}:\n"
             f"{date_text}\n\n"
             f"{summary_text}")

    await message.answer(
        text=SELECT_ENROLLMENT_SLOTS,
        reply_markup=get_enrollment_intervals_inl_kbd(
            selected_date=selected_date,
            enrollment_intervals=enrollment_intervals))

    await state.update_data(
        enrollment_intervals_state=enrollment_intervals)

    return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)
