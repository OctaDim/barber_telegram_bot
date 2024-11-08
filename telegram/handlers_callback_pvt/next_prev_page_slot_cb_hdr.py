from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    PreviousSlotPageCBData,
    NextSlotPageCBData, get_enrollment_intervals_inl_kbd)
from telegram.params.messages import (
    SELECT_ENROLLMENT_SLOT)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key,
    get_valid_dict_by_fsm_state_key,
    get_valid_datetime_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

next_prev_page_slot_enroll_srcs_cb_router = Router(name=__name__)
next_prev_page_slot_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@next_prev_page_slot_enroll_srcs_cb_router.callback_query(PreviousSlotPageCBData.filter())
@next_prev_page_slot_enroll_srcs_cb_router.callback_query(NextSlotPageCBData.filter())
async def next_prev_page_slot_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                                 callback_data: CallbackData,
                                                 state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    callback_prefix = callback_data.__prefix__

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

    if callback_prefix == PreviousSlotPageCBData.__prefix__:
        if not paginated_intervals.get(cur_page_number - 1):
            cur_page_number = len(paginated_intervals)
        else:
            cur_page_number -= 1
    elif callback_prefix == NextSlotPageCBData.__prefix__:
        if not paginated_intervals.get(cur_page_number + 1):
            cur_page_number = 1
        else:
            cur_page_number += 1
    else:
        cur_page_number = 1

    current_page_intervals = paginated_intervals.get(cur_page_number)
    total_pages = len(paginated_intervals)

    await callback_query.message.edit_text(
        text=SELECT_ENROLLMENT_SLOT,
        reply_markup=get_enrollment_intervals_inl_kbd(
            current_page_number=cur_page_number,
            current_page_intervals=current_page_intervals,
            total_pages_number=total_pages,
            selected_date=selected_date))

    await state.update_data(
        selected_master_id=None,
        current_page_number_of_intervals=cur_page_number)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
