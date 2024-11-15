from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_services_ordered_queries import (
    get_all_services_ordered)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.categories_enroll_srcs_inl_kbd import (
    CategoryToOurServicesInfoContinueCBdata)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    NO_SERVICES)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_service_detailed_info)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

# from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
#     MethodCategoryToServiceContinueCBD)

inline_our_services_by_category_cb_router = Router(name=__name__)
inline_our_services_by_category_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_our_services_by_category_cb_router.callback_query(CategoryToOurServicesInfoContinueCBdata.filter())
async def inline_our_services_detail_info_srcs_cb_hdr(callback_query: CallbackQuery,
                                                      callback_data: CallbackData,
                                                      state: FSMContext):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    selected_category_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_category_id")

    all_services_records_by_category = get_all_services_ordered(
        category_id=selected_category_id,
        active=True,
        order_by_fields=("price", "name",))

    if not all_services_records_by_category:
        await callback_query.answer(
            text=NO_SERVICES,
            reply_markup=True)

    for service_record in all_services_records_by_category:
        await callback_query.message.answer(
            text=f"{get_service_detailed_info(service_record)}",
            reply_markup=get_pvt_main_menu_reply_kbd())
