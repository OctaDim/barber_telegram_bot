from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_masters_ordered_query import (
    get_all_masters_ordered)
from telegram.config.configs import (
    PAGINATION_CONFIGS)
from telegram.errors_api_telegram.telegram_exception_errors import (
    TG_EXCEPT_ERRORS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enroll_categories_inl_kbd import (
    CategoryToMasterContinueCBData)
from telegram.keyboard_inline.enroll_masters_inl_kbd import (
    get_enroll_masters_inl_kbd)
from telegram.keyboard_inline.enroll_methods_inl_kbd import (
    get_enroll_methods_inl_kbd,
    MethodMasterToServiceCBData)
from telegram.params.messages import (
    HOW_SELECT_SERVICES,
    NO_AVAILABLE_MASTERS,
    SELECT_MASTER)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)
from utilities.pagination_utility import (
    create_paginated_elems)

enroll_method_by_master_cb_router = Router(name=__name__)
enroll_method_by_master_cb_router.message.filter(ChatTypesFilter(["private"]))


@enroll_method_by_master_cb_router.callback_query(MethodMasterToServiceCBData.filter())
@enroll_method_by_master_cb_router.callback_query(CategoryToMasterContinueCBData.filter())
async def enroll_method_by_master_cb_hdr(callback_query: CallbackQuery,
                                         callback_data: CallbackData,
                                         state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    callback_prefix = callback_data.__prefix__

    if callback_prefix == MethodMasterToServiceCBData.__prefix__:
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
        await state.update_data(selected_method_prefix=selected_method_prefix)

    message = callback_query.message

    selected_master_id = None
    # selected_master_id = await get_valid_int_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="selected_master_id")

    current_page_number = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="current_page_number_of_masters")
    if not current_page_number:
        current_page_number = 1

    masters_records = None
    if callback_prefix == MethodMasterToServiceCBData.__prefix__:
        masters_records = get_all_masters_ordered(
            active=True,
            order_by_fields=(
                "full_name", "category_id"))

    elif callback_prefix == CategoryToMasterContinueCBData.__prefix__:
        selected_category_id = await get_valid_int_by_fsm_state_key(
            fsm_state_or_dict_from=state_data,
            fsm_state_literal_key="selected_category_id")

        masters_records = get_all_masters_ordered(
            active=True,
            category_id=selected_category_id,
            order_by_fields=("full_name",))

    if not masters_records:
        await callback_query.answer(text=NO_AVAILABLE_MASTERS,
                                    show_alert=True)
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    paginated_records = create_paginated_elems(
        all_elements=masters_records,
        elements_per_page=PAGINATION_CONFIGS.MASTERS_PER_PAGE)

    current_page_records = paginated_records.get(current_page_number)
    total_pages = len(paginated_records)

    await callback_query.message.answer(
        text=SELECT_MASTER,
        reply_markup=get_enroll_masters_inl_kbd(
            current_page_records=current_page_records,
            total_pages_number=total_pages,
            selected_master_id=selected_master_id,
            current_page_number=current_page_number))

    await state.update_data(
        selected_master_id=selected_master_id,
        paginated_masters_records=paginated_records)

    return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)
