from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.db_queries.all_categories_ordered_query import (
    get_all_categories_ordered)
from telegram.config.configs import (
    PAGINATION_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.categories_enroll_srcs_inl_kbd import (
    get_categories_enroll_srcs_inl_kbd)
from telegram.params.buttons_main_menu import (
    MAIN_MENU_BUTTONS_PARAMS)
from telegram.params.messages import (
    NO_AVAILABLE_CATEGORIES,
    SELECT_CATEGORY_SEE_OUR_SERVICES)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from utilities.pagination_utility import (
    create_paginated_elems)

services_btn_router = Router(name=__name__)
services_btn_router.message.filter(ChatTypesFilter(["private"]))


@services_btn_router.message(F.text == MAIN_MENU_BUTTONS_PARAMS.OUR_SERVICES)
async def our_services_btn_reply_hdr_pvt(message: Message,
                                         state: FSMContext):
    state_data = await state.get_data()

    selected_method_prefix = "our services reply btn private handler"

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
        await message.answer(text=NO_AVAILABLE_CATEGORIES)
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    paginated_records = create_paginated_elems(
        all_elements=categories_records,
        elements_per_page=PAGINATION_CONFIGS.CATEGORIES_PER_PAGE)

    current_page_records = paginated_records.get(current_page_number)
    total_pages = len(paginated_records)

    await message.answer(
        text=SELECT_CATEGORY_SEE_OUR_SERVICES,
        reply_markup=get_categories_enroll_srcs_inl_kbd(
            current_page_records=current_page_records,
            total_pages_number=total_pages,
            selected_category_id=selected_category_id,
            current_page_number=current_page_number,
            selected_method_prefix=selected_method_prefix))

    await state.update_data(
        selected_category_id=selected_category_id,
        paginated_categories_records=paginated_records,
        selected_method_prefix=selected_method_prefix)

    return
