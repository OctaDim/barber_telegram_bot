import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    SlotSelectedCBData,
    get_enrollment_intervals_inl_kbd)
from telegram.params.messages import (
    SELECT_ENROLLMENT_SLOT)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_dict_by_fsm_state_key,
    get_valid_datetime_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

slot_selected_enroll_services_cb_router = Router(name=__name__)
slot_selected_enroll_services_cb_router.message.filter(ChatTypesFilter(["private"]))


@slot_selected_enroll_services_cb_router.callback_query(SlotSelectedCBData.filter())
async def slot_selected_enroll_services_cb_hdr(callback_query: CallbackQuery,
                                               callback_data: CallbackData,
                                               state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    interval_first_slot_id = callback_data.first_slot_id

    # # Unselecting time interval if clicked the same interval
    # new_interval_first_slot_id = callback_data.first_slot_id
    # old_interval_first_slot_id = await get_valid_int_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="selected_interval_first_slot_id")
    # if new_interval_first_slot_id == old_interval_first_slot_id:
    #     interval_first_slot_id = None

    selected_date = await get_valid_datetime_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_date_enroll_srcs_calendar")

    cur_page_number = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="current_page_number_of_intervals")
    cur_page_number = 1 if not cur_page_number else cur_page_number

    paginated_intervals = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="paginated_intervals_dicts_list")

    current_page_intervals = paginated_intervals.get(cur_page_number)
    total_pages = len(paginated_intervals)

    try:
        await callback_query.message.edit_text(
            text=SELECT_ENROLLMENT_SLOT,
            reply_markup=get_enrollment_intervals_inl_kbd(
                current_page_number=cur_page_number,
                current_page_intervals=current_page_intervals,
                total_pages_number=total_pages,
                selected_date=selected_date,
                selected_slot_id=interval_first_slot_id))
    except (TelegramBadRequest, Exception) as exception_info:
        print(f"\tMessage not modified, tg exception intercepted: {exception_info}\n")

    await state.update_data(
        selected_interval_first_slot_id=interval_first_slot_id)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
