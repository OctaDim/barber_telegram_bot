import inspect

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_services_ordered_queries import (
    get_all_services_ordered)
from database.db_queries.category_obj_by_id_query import (
    get_category_obj_by_id)
from database.db_queries_hepers.masters_fullnames_by_service_obj import (
    get_masters_names_by_service_obj)
from telegram.config.configs import (
    LANGUAGE_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.categories_enroll_srcs_inl_kbd import (
    CategoryToOurServicesInfoContinueCBdata)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    NO_SERVICES_FOR_CATEGORY,
    OR_SELECT_MAIN_MENU)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_service_detailed_info)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    re_open_reply_keyboard_message)
from utilities.calendar_utils import (
    get_hours_minutes_secs_timedelta)


# from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
#     MethodCategoryToServiceContinueCBD)

inline_our_services_by_category_cb_router = Router(name=__name__)
inline_our_services_by_category_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_our_services_by_category_cb_router.callback_query(CategoryToOurServicesInfoContinueCBdata.filter())
async def inline_our_services_detail_info_srcs_cb_hdr(callback_query: CallbackQuery,
                                                      callback_data: CallbackData,
                                                      state: FSMContext):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    selected_category_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_category_id")

    srcs_recs_by_category = get_all_services_ordered(
        category_id=selected_category_id,
        active=True,
        order_by_fields=("sort_index", "name", "price",))

    if not srcs_recs_by_category:
        await callback_query.answer(text=NO_SERVICES_FOR_CATEGORY,
                                    show_alert=True)
        return

    selected_category_obj = get_category_obj_by_id(
        category_id=selected_category_id)
    selected_category_name = selected_category_obj.name

    for service_idx in range(len(srcs_recs_by_category)):
        masters_names = get_masters_names_by_service_obj(
            service_obj=srcs_recs_by_category[service_idx])

        service_duration_time = get_hours_minutes_secs_timedelta(
            timedelta_value=srcs_recs_by_category[service_idx].time_duration,
            language=LANGUAGE_CONFIGS.LANGUAGE,
            hide_zero_values=True,
            space_before_note=True,
            separator=" ",
            abbrev_symbols="3")

        service_detailed_info = get_service_detailed_info(
            service_obj=srcs_recs_by_category[service_idx],
            masters_info=masters_names,
            category_name=selected_category_name,
            service_duration=service_duration_time)

        if service_idx == 0:
            cur_message = await callback_query.message.edit_text(
                text=f"{service_detailed_info}")
            cur_handler_messages_ids.append(cur_message.message_id)
            print(f"\tPrior msg was edited to first 'Service Detailed Info' msg "
                  f"\tsuccessfully, because first service record: service_idx == 0\n")
        else:
            cur_message = await callback_query.message.answer(
                text=f"{service_detailed_info}")
            cur_handler_messages_ids.append(cur_message.message_id)
            print(f"\tNew 'Service Detailed Info' msg was created, because it is"
                  f"\tnot first first service record: service_idx == {service_idx}\n")

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=callback_query,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=True,
        open_reply_kbd_msg_anyway=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    # await state.update_data()

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=True,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
