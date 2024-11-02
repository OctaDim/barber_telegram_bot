from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enroll_categories_inl_kbd import (
    get_enroll_categories_inl_kbd,
    PreviousCategoryPageCBData,
    NextCategoryPageCBData)
from telegram.params.messages import (
    SELECT_CATEGORY)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key,
    get_valid_dict_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

next_prev_enroll_category_cb_router = Router(name=__name__)
next_prev_enroll_category_cb_router.message.filter(ChatTypesFilter(["private"]))


@next_prev_enroll_category_cb_router.callback_query(PreviousCategoryPageCBData.filter())
@next_prev_enroll_category_cb_router.callback_query(NextCategoryPageCBData.filter())
async def next_prev_enroll_category_cb_hdr(callback_query: CallbackQuery,
                                           callback_data: CallbackData,
                                           state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    message = callback_query.message

    selected_category_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state,
        fsm_state_literal_key="selected_category_id")

    current_page_number = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state,
        fsm_state_literal_key="current_page_number_of_categories")
    if not current_page_number:
        current_page_number = 1

    paginated_records = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state,
        fsm_state_literal_key="paginated_categories_records")

    if callback_data.__prefix__ == PreviousCategoryPageCBData.__prefix__:
        if not paginated_records.get(current_page_number - 1):
            current_page_number = len(paginated_records)
        else:
            current_page_number -= 1

    if callback_data.__prefix__ == NextCategoryPageCBData.__prefix__:
        if not paginated_records.get(current_page_number + 1):
            current_page_number = 1
        else:
            current_page_number += 1

    current_page_records = paginated_records.get(current_page_number)
    total_pages = len(paginated_records)

    await callback_query.message.edit_text(
        text=SELECT_CATEGORY,
        reply_markup=get_enroll_categories_inl_kbd(
            current_page_records=current_page_records,
            total_pages_number=total_pages,
            selected_category_id=selected_category_id,
            current_page_number=current_page_number))

    await state.update_data(
        current_page_number_of_categories=current_page_number)

    return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)
