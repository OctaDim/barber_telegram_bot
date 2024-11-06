from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db_queries.all_categories_ordered_query import (
    get_all_categories_ordered)
from telegram.config.configs import (
    PAGINATION_CONFIGS)
from telegram.errors_api_telegram.telegram_exception_errors import (
    TG_EXCEPT_ERRORS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enroll_categories_inl_kbd import (
    get_enroll_categories_inl_kbd)
from telegram.keyboard_inline.enroll_methods_inl_kbd import (
    MethodCategoryToServiceCBData, get_enroll_methods_inl_kbd, MethodCategoryToMasterCBData)
from telegram.params.messages import (
    NO_AVAILABLE_CATEGORIES,
    SELECT_CATEGORY, HOW_SELECT_SERVICES)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)
from utilities.pagination_utility import (
    create_paginated_elems)

method_by_category_cb_router = Router(name=__name__)
method_by_category_cb_router.message.filter(ChatTypesFilter(["private"]))


@method_by_category_cb_router.callback_query(MethodCategoryToMasterCBData.filter())
@method_by_category_cb_router.callback_query(MethodCategoryToServiceCBData.filter())
async def enroll_methods_by_category_cb_hdr(callback_query: CallbackQuery,
                                            callback_data: CallbackData,
                                            state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    selected_method_prefix = callback_data.__prefix__

    try:
        await callback_query.message.edit_text(
            text=HOW_SELECT_SERVICES,
            reply_markup=get_enroll_methods_inl_kbd(
                selected_method_prefix=selected_method_prefix))
    except TelegramBadRequest as error:
        if error.message == TG_EXCEPT_ERRORS.MSG_NOT_MODIFIED:
            print("\tLOG INFO: 'Message not modified' tg exception was intercepted\n")
            pass

    selected_category_id = None

    current_page_number = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="current_page_number_of_categories")
    if not current_page_number:
        current_page_number = 1

    categories_records = get_all_categories_ordered(
        active=True,
        order_by_fields="name")

    if not categories_records:
        await callback_query.answer(text=NO_AVAILABLE_CATEGORIES,
                                    show_alert=True)
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    paginated_records = create_paginated_elems(
        all_elements=categories_records,
        elements_per_page=PAGINATION_CONFIGS.CATEGORIES_PER_PAGE)

    current_page_records = paginated_records.get(current_page_number)
    total_pages = len(paginated_records)

    await callback_query.message.answer(
        text=SELECT_CATEGORY,
        reply_markup=get_enroll_categories_inl_kbd(
            current_page_records=current_page_records,
            total_pages_number=total_pages,
            selected_category_id=selected_category_id,
            current_page_number=current_page_number,
            selected_method_prefix=selected_method_prefix))

    await state.update_data(
        selected_category_id=selected_category_id,
        paginated_categories_records=paginated_records,
        selected_method_prefix=selected_method_prefix)

    return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)
