from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.errors_api_telegram.telegram_exception_errors import (
    TG_EXCEPT_ERRORS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.categories_enroll_srcs_inl_kbd import (
    CurrentCategoryCBData,
    get_categories_enroll_srcs_inl_kbd)
from telegram.params.messages import (
    SELECT_CATEGORY)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_dict_by_fsm_state_key,
    get_valid_int_by_fsm_state_key,
    get_valid_str_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

category_selected_enroll_srcs_cb_router = Router(name=__name__)
category_selected_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@category_selected_enroll_srcs_cb_router.callback_query(CurrentCategoryCBData.filter())
async def category_selected_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                               callback_data: CallbackData,
                                               state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    selected_method_prefix = await get_valid_str_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_method_prefix")

    selected_category_id = callback_data.category_id

    # Unselecting category if clicked the same category
    # new_category_id = callback_data.category_id
    # old_category_id = await get_valid_int_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="selected_category_id")
    # if new_category_id == old_category_id:
    #     selected_category_id = None

    current_page_number = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="current_page_number_of_categories")
    if not current_page_number:
        current_page_number = 1

    paginated_records = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="paginated_categories_records")

    current_page_records = paginated_records.get(current_page_number)
    total_pages = len(paginated_records)

    try:
        await callback_query.message.edit_text(
            text=SELECT_CATEGORY,
            reply_markup=get_categories_enroll_srcs_inl_kbd(
                current_page_records=current_page_records,
                total_pages_number=total_pages,
                selected_category_id=selected_category_id,
                current_page_number=current_page_number,
                selected_method_prefix=selected_method_prefix))
    except TelegramBadRequest as error:
        if error.message == TG_EXCEPT_ERRORS.MSG_NOT_MODIFIED:
            print("\tLOG INFO: 'Message not modified' tg exception was intercepted\n")
            pass

    await state.update_data(selected_category_id=selected_category_id)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
