from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from telegram.config.configs import LANGUAGE_CONFIGS
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    ContinueSlotSavingCBData)
from telegram.params.calendar_icons import CALENDAR_ICONS
from telegram.params.intervals_slots_icons import SLOT_ICONS
from telegram.params.messages_inserts import MSG
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_dict_by_fsm_state_key,
    get_valid_float_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key, get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_selected_services_summary, get_summary_services_with_slot)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)
from utilities.calendar_utils import (
    get_date_with_month_name,
    get_time_flex_from_datetime)

continue_slot_saving_cb_router = Router(name=__name__)
continue_slot_saving_cb_router.message.filter(ChatTypesFilter(["private"]))


@continue_slot_saving_cb_router.callback_query(ContinueSlotSavingCBData.filter())
async def continue_slot_saving_cb_hdr(callback_query: CallbackQuery,
                                      callback_data: CallbackData,
                                      state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    await callback_query.answer()
    message = callback_query.message

    selected_date = state_data.get("selected_date_enroll_srcs_calendar")

    interval_first_slot_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_interval_first_slot_id")

    enrollment_intervals = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="enrollment_intervals_state")

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    all_services_info = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="all_services_info_state")

    selected_services_cost = await get_valid_float_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_cost_state")

    services_services_duration = await get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_duration_state")

    for interval_dict in enrollment_intervals:
        for key, value in interval_dict.items():
            print("#####", key, "#####", value)
        print()

    for interval_dict in enrollment_intervals:
        if interval_dict.get("first slot id") == interval_first_slot_id:
            date_text = get_date_with_month_name(
                selected_date,
                language=LANGUAGE_CONFIGS.LANGUAGE)

            summary_text = get_selected_services_summary(
                services_count=len(selected_services_ids),
                total_cost=selected_services_cost,
                total_duration=services_services_duration)

            for key, value in all_services_info.items():
                print("#####", key, "#####", value)
            print()

            # for service_id in selected_services_ids:
            #     cur_selected_service = all_services_info.get(service_id)
            #     print(cur_selected_service.get(""))
            #     print()

            slot_time_start = interval_dict.get("slot time start")
            slot_time_start_text = get_time_flex_from_datetime(
                date_value=slot_time_start,
                language=LANGUAGE_CONFIGS.LANGUAGE)

            client_time_end = interval_dict.get("client time end")
            client_time_end_text = get_time_flex_from_datetime(
                date_value=client_time_end,
                language=LANGUAGE_CONFIGS.LANGUAGE)

            complete_summary_text = get_summary_services_with_slot(
                date_text=date_text,
                summary_text=summary_text,
                slot_time_start=slot_time_start_text,
                slot_time_end=client_time_end_text)

            await message.answer(text=complete_summary_text)

    # await state.update_data(
    #     enrollment_intervals_state=filtered_intervals_dict)

    await state.clear()

    return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)

    # filtered_intervals_dict = {}
    # for interval in enrollment_intervals:
    #     first_slot_id = interval.get("first slot id")
    #     filtered_intervals_dict[first_slot_id] = {
    #         "first slot id": interval.get("first slot id"),
    #         "all slots ids": interval.get("all slots ids"),
    #         "slot time start": interval.get("slot time start"),
    #         "slot time end": interval.get("slot time end"),
    #         "client time end": interval.get("client time end"),
    #         "all slots duration": interval.get("all slots duration"),
    #         "selected services duration": interval.get("selected services duration"),
    #         "slot time loss": interval.get("slot time loss")}
    #
    # await state.update_data(
    #     enrollment_intervals_state=filtered_intervals_dict)
