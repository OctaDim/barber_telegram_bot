import inspect

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.masters_enroll_srcs_inl_kbd import (
    PreviousMasterPageCBData,
    NextMasterPageCBData,
    get_masters_enroll_srcs_inl_kbd)
from telegram.params.messages import (
    SELECT_MASTER)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key,
    get_valid_dict_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

next_prev_page_master_enroll_srcs_cb_router = Router(name=__name__)
next_prev_page_master_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@next_prev_page_master_enroll_srcs_cb_router.callback_query(PreviousMasterPageCBData.filter())
@next_prev_page_master_enroll_srcs_cb_router.callback_query(NextMasterPageCBData.filter())
async def next_prev_page_master_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                                   callback_data: CallbackData,
                                                   state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    callback_prefix = callback_data.__prefix__

    cur_page_number = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="current_page_number_of_masters")
    cur_page_number = 1 if not cur_page_number else cur_page_number

    paginated_records = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="paginated_masters_records")

    total_pages = len(paginated_records)

    if callback_prefix == PreviousMasterPageCBData.__prefix__:
        if (cur_page_number - 1) < 1:
            cur_page_number = total_pages
        else:
            cur_page_number -= 1
    elif callback_prefix == NextMasterPageCBData.__prefix__:
        if (cur_page_number + 1) > total_pages:
            cur_page_number = 1
        else:
            cur_page_number += 1
    else:
        cur_page_number = 1

    # if callback_prefix == PreviousMasterPageCBData.__prefix__:
    #     if not paginated_records.get(cur_page_number - 1):
    #         cur_page_number = len(paginated_records)
    #     else:
    #         cur_page_number -= 1
    # elif callback_prefix == NextMasterPageCBData.__prefix__:
    #     if not paginated_records.get(cur_page_number + 1):
    #         cur_page_number = 1
    #     else:
    #         cur_page_number += 1
    # else:
    #     cur_page_number = 1

    current_page_records = paginated_records.get(cur_page_number)

    await callback_query.message.edit_text(
        text=SELECT_MASTER,
        reply_markup=get_masters_enroll_srcs_inl_kbd(
            current_page_records=current_page_records,
            total_pages_number=total_pages,
            selected_master_id=None,
            current_page_number=cur_page_number))

    await state.update_data(
        selected_master_id=None,
        current_page_number_of_masters=cur_page_number)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
