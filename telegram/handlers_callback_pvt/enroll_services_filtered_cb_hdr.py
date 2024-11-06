from time import sleep

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.orm import joinedload

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.master_model import Master
from database.db_models.service_model import Service
from database.db_queries.services_filtered_by_method_queries import get_services_filtered_by_category_master, \
    get_services_filtered_by_master, get_services_filtered_by_category
from telegram.config.configs import PAUSE_CONFIGS
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enroll_categories_inl_kbd import (
    CategoryToServiceContinueCBData)
from telegram.keyboard_inline.enroll_masters_inl_kbd import (
    MasterToServiceContinueCBData)
from telegram.keyboard_inline.enroll_services_inl_kbd import (
    get_enroll_service_inl_kbd)
from telegram.keyboard_reply.pvt_enroll_service_actions_kbd import (
    get_pvt_enroll_services_actions_reply_kbd)
from telegram.keyboard_reply.pvt_main_menu_kbd import (
    get_pvt_main_menu_kbd)
from telegram.params.messages import (
    NO_SERVICES,
    SELECT_SERVICES_BELLOW,
    SELECT_OTHER_ACTIONS)
from telegram.params.select_services_icons import (
    SELECT_SERVICES_ICONS)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_service_brief_info)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)
from utilities.numeric_utils import number_or_str_to_float

enroll_services_filtered_cb_router = Router(name=__name__)
enroll_services_filtered_cb_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_filtered_cb_router.callback_query(MasterToServiceContinueCBData.filter())
@enroll_services_filtered_cb_router.callback_query(CategoryToServiceContinueCBData.filter())
async def select_service_callback_hdr(callback_query: CallbackQuery,
                                      callback_data: CallbackData,
                                      state: FSMContext):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    message = callback_query.message

    callback_prefix = callback_data.__prefix__

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
        await message.answer(
            text=NO_SERVICES,
            reply_markup=get_pvt_main_menu_kbd())
        return

    await message.answer(text=SELECT_SERVICES_BELLOW)

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    all_services_info_dict = {}
    for service_record in all_services_records:
        service_brief_text = get_service_brief_info(
            service_record=service_record)

        if service_record.id in selected_services_ids:
            same_id_count = selected_services_ids.count(service_record.id)
            inline_button_icon = f"{SELECT_SERVICES_ICONS.SELECTED} " * same_id_count
            button_selected = True
            one_more_service_btn = True
        else:
            inline_button_icon = SELECT_SERVICES_ICONS.NO_ICON
            button_selected = False
            one_more_service_btn = False

        await message.answer(
            text=f"{inline_button_icon} {service_brief_text}",
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

    await message.answer(
        text=SELECT_OTHER_ACTIONS,
        reply_markup=get_pvt_enroll_services_actions_reply_kbd())

    return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)
