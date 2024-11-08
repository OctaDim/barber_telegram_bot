from time import sleep

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.masters_names_by_service_id_query import (
    get_masters_full_names_by_service_id)
from database.db_queries.services_filtered_by_method_queries import (
    get_services_filtered_by_category_master,
    get_services_filtered_by_master,
    get_services_filtered_by_category)
from telegram.config.configs import (
    PAUSE_CONFIGS, SERVICES_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.categories_enroll_srcs_inl_kbd import (
    CategoryToServiceContinueCBData)
from telegram.keyboard_inline.masters_enroll_srcs_inl_kbd import (
    MasterToServiceContinueCBData)
from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
    MethodCategoryToServiceContinueCBD)
from telegram.keyboard_inline.enroll_services_inl_kbd import (
    get_enroll_service_inl_kbd)
from telegram.keyboard_reply.pvt_enroll_services_action_reply_kbd import (
    get_pvt_enroll_services_action_reply_kbd)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    NO_SERVICES,
    SELECT_SERVICES_BELLOW,
    SELECT_OTHER_ACTIONS)
from telegram.params.services_icons import (
    SERVICES_ICONS)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_int_by_fsm_state_key, get_valid_str_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_service_brief_info, get_service_brief_info_with_master)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)
from utilities.numeric_utils import (
    number_or_str_to_float)

inline_services_filtered_enroll_srcs_cb_router = Router(name=__name__)
inline_services_filtered_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_services_filtered_enroll_srcs_cb_router.callback_query(MasterToServiceContinueCBData.filter())
@inline_services_filtered_enroll_srcs_cb_router.callback_query(CategoryToServiceContinueCBData.filter())
async def inline_services_filtered_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                                      callback_data: CallbackData,
                                                      state: FSMContext):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    selected_category_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_category_id")

    selected_master_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_master_id")

    all_services_records = []
    if selected_category_id and selected_master_id:
        all_services_records = get_services_filtered_by_category_master(
            selected_category_id=selected_category_id,
            selected_master_id=selected_master_id)
    elif selected_master_id:
        all_services_records = get_services_filtered_by_master(
            selected_master_id=selected_master_id)
    elif selected_category_id:
        all_services_records = get_services_filtered_by_category(
            selected_category_id=selected_category_id)

    if not all_services_records:
        await callback_query.answer(
            text=NO_SERVICES,
            reply_markup=get_pvt_main_menu_reply_kbd())
        return

    await callback_query.message.answer(text=SELECT_SERVICES_BELLOW)

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    selected_method_prefix = await get_valid_str_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_method_prefix")

    all_services_info_dict = {}
    for service_record in all_services_records:
        if (selected_method_prefix == MethodCategoryToServiceContinueCBD.__prefix__
                and SERVICES_CONFIGS.MASTERS_NAMES_WHEN_BY_CATEGORY):
            masters_full_names = get_masters_full_names_by_service_id(
                service_id=service_record.id)
            service_brief_text = get_service_brief_info_with_master(
                service_record=service_record,
                master_info=masters_full_names)
        else:
            service_brief_text = get_service_brief_info(
                service_record=service_record)

        if service_record.id in selected_services_ids:
            same_id_count = selected_services_ids.count(service_record.id)
            cur_service_icon = f"{SERVICES_ICONS.SELECTED} " * same_id_count
            button_selected = True
            one_more_service_btn = True
        else:
            cur_service_icon = SERVICES_ICONS.SERVICE_POINT
            button_selected = False
            one_more_service_btn = False

        await callback_query.message.answer(
            text=f"{cur_service_icon} {service_brief_text}\n",
            reply_markup=get_enroll_service_inl_kbd(service_record.id,
                                                    button_selected,
                                                    one_more_service_btn))

        delay_seconds = number_or_str_to_float(PAUSE_CONFIGS.LIST_DELAY)
        sleep(delay_seconds)

        all_services_info_dict[service_record.id] = {
            "text": service_brief_text,
            "price": service_record.price,
            "duration": service_record.time_duration}

    await state.update_data(all_services_info_state=all_services_info_dict)

    await callback_query.message.answer(
        text=SELECT_OTHER_ACTIONS,
        reply_markup=get_pvt_enroll_services_action_reply_kbd())

    return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)
