import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_categories_ordered_query import (
    get_all_categories_ordered)
from telegram.config.configs import (
    PAGINATION_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.categories_enroll_srcs_inl_kbd import (
    get_categories_enroll_srcs_inl_kbd)
from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
    MethodCategoryToMasterContinueCBData,
    MethodCategoryToServiceContinueCBD)
from telegram.keyboard_inline.submenu_services_inl_kbd import (
    OurServicesInlineMenuCBData)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    NO_AVAILABLE_CATEGORIES,
    SELECT_SERVICES_CATEGORY,
    OR_SELECT_MAIN_MENU)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual, re_open_reply_keyboard_message)
from utilities.pagination_utility import (
    create_paginated_elems)

inline_categories_enroll_srcs_cb_router = Router(name=__name__)
inline_categories_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_categories_enroll_srcs_cb_router.callback_query(OurServicesInlineMenuCBData.filter())
@inline_categories_enroll_srcs_cb_router.callback_query(MethodCategoryToMasterContinueCBData.filter())
@inline_categories_enroll_srcs_cb_router.callback_query(MethodCategoryToServiceContinueCBD.filter())
async def inline_categories_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                               callback_data: CallbackData,
                                               state: FSMContext):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    selected_method_prefix = callback_data.__prefix__
    selected_category_id = None

    current_page_number = 1
    # current_page_number = await get_valid_int_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="current_page_number_of_categories")
    # if not current_page_number:
    #     current_page_number = 1

    categories_records = get_all_categories_ordered(
        active=True,
        order_by_fields="name")

    if not categories_records:
        await callback_query.answer(text=NO_AVAILABLE_CATEGORIES,
                                    show_alert=True)
        return

    paginated_records = create_paginated_elems(
        all_elements=categories_records,
        elements_per_page=PAGINATION_CONFIGS.CATEGORIES_PER_PAGE)

    current_page_records = paginated_records.get(current_page_number)
    total_pages = len(paginated_records)

    categories_reply_markup = get_categories_enroll_srcs_inl_kbd(
        current_page_records=current_page_records,
        total_pages_number=total_pages,
        selected_category_id=selected_category_id,
        current_page_number=current_page_number,
        selected_method_prefix=selected_method_prefix)

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    try:
        cur_message = await callback_query.message.edit_text(
            text=SELECT_SERVICES_CATEGORY,
            reply_markup=categories_reply_markup)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tPrior message was edited to Categories msg successfully :)\n")

    except (TelegramBadRequest, Exception) as exception_info:
        cur_message = await callback_query.message.answer(
            text=SELECT_SERVICES_CATEGORY,
            reply_markup=categories_reply_markup)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tNew Categories message was created, because "
              f"\tprior message is not editable: {exception_info}\n")

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=callback_query,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    await state.update_data(
        selected_category_id=selected_category_id,
        paginated_categories_records=paginated_records,
        selected_method_prefix=selected_method_prefix,
        current_page_number_of_categories=current_page_number)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=True,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
