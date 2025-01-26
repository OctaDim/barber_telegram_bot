import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_masters_ordered_query import (
    get_all_masters_ordered)
from database.db_queries.all_services_ordered_queries import (
    get_all_services_ordered)
from telegram.config.configs import (
    PAGINATION_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.categories_enroll_srcs_inl_kbd import (
    CategoryToMasterContinueCBData)
from telegram.keyboard_inline.masters_enroll_srcs_inl_kbd import (
    get_masters_enroll_srcs_inl_kbd)
from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
    MethodMasterToServiceContinueCBD)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    NO_AVAILABLE_MASTERS,
    SELECT_MASTER,
    OR_SELECT_MAIN_MENU)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    re_open_reply_keyboard_message)
from utilities.pagination_utility import (
    create_paginated_elems)

inline_masters_enroll_srcs_cb_router = Router(name=__name__)
inline_masters_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_masters_enroll_srcs_cb_router.callback_query(MethodMasterToServiceContinueCBD.filter())
@inline_masters_enroll_srcs_cb_router.callback_query(CategoryToMasterContinueCBData.filter())
async def inline_masters_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                            callback_data: CallbackData,
                                            state: FSMContext):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    callback_prefix = callback_data.__prefix__
    selected_master_id = None

    current_page_number = 1
    # current_page_number = await get_valid_int_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="current_page_number_of_masters")
    # if not current_page_number:
    #     current_page_number = 1

    if callback_prefix == MethodMasterToServiceContinueCBD.__prefix__:
        masters_records = get_all_masters_ordered(
            active=True,
            order_by_fields=("sort_index", "full_name", "category_id"))
    elif callback_prefix == CategoryToMasterContinueCBData.__prefix__:
        selected_category_id = await get_valid_int_by_fsm_state_key(
            fsm_state_or_dict_from=state_data,
            fsm_state_literal_key="selected_category_id")

        # Getting masters by category via services included in category. Option 1
        all_services_by_category = get_all_services_ordered(
            category_id=selected_category_id,
            active=True)
        masters_records_set = set()
        for service_obj in all_services_by_category:
            masters_records_set.update(service_obj.service_masters)
        masters_records = list(masters_records_set)
        masters_records.sort(key=lambda master: master.full_name)

        # Getting masters by category directly. Option 2
        # masters_records = get_all_masters_ordered(
        #     active=True,
        #     category_id=selected_category_id,
        #     order_by_fields=("full_name",))
    else:
        masters_records = []

    if not masters_records:
        await callback_query.answer(text=NO_AVAILABLE_MASTERS,
                                    show_alert=True)
        return

    paginated_records = create_paginated_elems(
        all_elements=masters_records,
        elements_per_page=PAGINATION_CONFIGS.MASTERS_PER_PAGE)

    current_page_records = paginated_records.get(current_page_number)
    total_pages = len(paginated_records)

    masters_reply_markup = get_masters_enroll_srcs_inl_kbd(
        current_page_records=current_page_records,
        total_pages_number=total_pages,
        selected_master_id=selected_master_id,
        current_page_number=current_page_number)

    try:
        cur_message = await callback_query.message.edit_text(
            text=SELECT_MASTER,
            reply_markup=masters_reply_markup)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tPrior message was edited to Masters msg successfully\n")

    except (TelegramBadRequest, Exception) as exception_info:
        cur_message = await callback_query.message.answer(
            text=SELECT_MASTER,
            reply_markup=masters_reply_markup)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tNew Masters message was created, because "
              f"\tprior message is not editable: {exception_info}\n")

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=callback_query,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=False)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    await state.update_data(
        selected_master_id=selected_master_id,
        paginated_masters_records=paginated_records,
        current_page_number_of_masters=current_page_number)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=True,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
