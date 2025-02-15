import copy
import inspect

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_slots_from_now_for_date_query import (
    get_slots_from_now_for_date_query)
from database.db_queries.masters_ids_common_for_services import (
    get_masters_ids_common_for_services)
from database.db_queries_hepers.enrollment_intervals_for_date_helper import (
    get_enrollment_intervals_helper)
from database.db_queries_hepers.remove_intervals_by_time_loss import (
    remove_intervals_over_time_loss_limit)
from database.db_queries_hepers.same_time_start_slots_random_master_id import (
    get_time_start_unique_random_intervals)
from telegram.config.configs import (
    LANGUAGE_CONFIGS,
    DB_SLOTS_CONFIGS,
    PAGINATION_CONFIGS,
    SLOTS_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.calendar_enroll_srcs_inl_kbd import (
    MonthContinueCBData)
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    get_enrollment_intervals_inl_kbd)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import get_pvt_main_menu_reply_kbd
from telegram.params.icons_calendar import (
    CALENDAR_ICONS)
from telegram.params.messages import (
    SELECT_ENROLLMENT_SLOT,
    NO_FREE_ENROLLMENT_SLOTS, OR_SELECT_MAIN_MENU)
from telegram.params.messages_inserts import MSG
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_float_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key,
    get_valid_datetime_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_selected_services_summary)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual, re_open_reply_keyboard_message)
from utilities.calendar_utils import (
    get_date_with_month_name, get_hours_minutes_secs_timedelta)
from utilities.numeric_utils import (
    number_or_str_to_integer)
from utilities.pagination_utility import (
    create_paginated_elems)

# from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
#     MethodCategoryToServiceContinueCBD)

continue_calendar_enroll_srcs_cb_router = Router(name=__name__)
continue_calendar_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@continue_calendar_enroll_srcs_cb_router.callback_query(MonthContinueCBData.filter())
async def inline_intervals_slots_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                                    callback_data: CallbackData,
                                                    bot: Bot,
                                                    state: FSMContext):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    # selected_method_prefix = await get_valid_str_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="selected_method_prefix")

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    total_cost_selected = await get_valid_float_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_cost_state")

    total_duration_selected = await get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_duration_state")

    total_duration_txt = get_hours_minutes_secs_timedelta(
        timedelta_value=total_duration_selected,
        language=LANGUAGE_CONFIGS.LANGUAGE,
        abbrev_symbols=3,
        separator=' ',
        space_before_note=True,
        hide_zero_values=True)

    summary_text = get_selected_services_summary(
        services_count=len(selected_services_ids),
        total_cost=total_cost_selected,
        total_duration=total_duration_txt)

    selected_date = await get_valid_datetime_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_date_enroll_srcs_calendar")

    date_text = get_date_with_month_name(
        selected_date,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    selected_master_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_master_id")

    if selected_master_id:
        all_slots_records = get_slots_from_now_for_date_query(
            required_date=selected_date,
            master_id=selected_master_id,
            order_by_fields=("time_start",),
            reserved=False, active=True, admin_only=False)
    else:
        intersecting_masters_ids = get_masters_ids_common_for_services(
            services_ids_list=selected_services_ids)

        all_slots_records = get_slots_from_now_for_date_query(
            required_date=selected_date,
            masters_ids_list=intersecting_masters_ids,
            order_by_fields=("master_id", "time_start"),
            reserved=False, active=True, admin_only=False)

    enrollment_intervals = get_enrollment_intervals_helper(
        slots_records=all_slots_records,
        selected_services_duration=total_duration_selected)

    if DB_SLOTS_CONFIGS.HIDE_SLOTS_OVER_TIME_LOSS_MAX_LIMIT:
        time_loss_max_limit = number_or_str_to_integer(
            DB_SLOTS_CONFIGS.TIME_LOSS_MAX_LIMIT_FOR_HIDE_SLOTS,
            positive=True)

        remove_intervals_over_time_loss_limit(
            enrollment_intervals=enrollment_intervals,
            time_loss_max_limit=time_loss_max_limit)

    if not enrollment_intervals:
        await callback_query.answer(text=NO_FREE_ENROLLMENT_SLOTS,
                                    show_alert=True)
        return

    intervals_dicts_list = [value for value in enrollment_intervals.values()]
    # if selected_method_prefix == MethodCategoryToServiceContinueCBD.__prefix__:
    if not selected_master_id:
        intervals_dicts_list.sort(key=lambda interval_item: (
            interval_item.get("slot time start"),
            # Sorting kbd slots by masters fullname
            interval_item.get("slot master fullname"),
            # Sorting inl slots by master id semi-randomly
            interval_item.get("slot master id")))

    if SLOTS_CONFIGS.ONLY_TIME_START_UNIQUE_RANDOM_SLOTS:
        intervals_dicts_list = get_time_start_unique_random_intervals(
            time_start_non_unique_intervals=intervals_dicts_list)

    paginated_intervals = create_paginated_elems(
        all_elements=intervals_dicts_list,
        elements_per_page=PAGINATION_CONFIGS.TIME_SLOTS_PER_PAGE)

    cur_page_number = 1
    # cur_page_number = await get_valid_int_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="current_page_number_of_intervals")
    # cur_page_number = 1 if not cur_page_number else cur_page_number

    current_page_intervals = paginated_intervals.get(cur_page_number)
    total_pages = len(paginated_intervals)

    summary_msg_text = (f"{CALENDAR_ICONS.CALENDAR} "
                        f"<b>{MSG.SELECTED_DATE}:</b>\n"
                        f"{date_text}\n\n"
                        f"{summary_text}")

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
            text=summary_msg_text,
            message_id=prior_inline_message_id,
            chat_id=callback_query.message.chat.id)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tPrior msg was edited to 'Selected Services Summary' "
              f"\tmsg successfully\n")

    except (TelegramBadRequest, Exception) as exception_info:
        cur_message = await callback_query.message.answer(
            text=summary_msg_text,
            disable_notification=True)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tNew 'Selected Services Summary' message was created, because "
              f"\tprior message is not editable: {exception_info}\n")

    cur_message = await callback_query.message.answer(
        text=SELECT_ENROLLMENT_SLOT,
        reply_markup=get_enrollment_intervals_inl_kbd(
            current_page_intervals=current_page_intervals,
            total_pages_number=total_pages,
            selected_date=selected_date))
    cur_handler_messages_ids.append(cur_message.message_id)

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=callback_query,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=True,
        open_reply_kbd_msg_anyway=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    await state.update_data(
        paginated_intervals_dicts_list=paginated_intervals,
        enrollment_intervals_state=enrollment_intervals,
        current_page_number_of_intervals=cur_page_number)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=True,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
