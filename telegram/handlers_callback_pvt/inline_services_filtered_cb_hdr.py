import asyncio
import inspect
from datetime import timedelta

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.all_services_ordered_queries import (
    get_all_services_ordered)
from database.db_queries_hepers.masters_fullnames_by_service_obj import (
    get_masters_names_by_service_obj)
from telegram.config.configs import (
    PAUSE_CONFIGS,
    SERVICES_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.handler_helpers.return_calendar_to_services_filtered_inl_inl import (
    delete_calendar_msgs_before_srcs_filtered)
from telegram.keyboard_inline.calendar_enroll_srcs_inl_kbd import (
    ReturnCalendarToSrcsFilteredCBData)
from telegram.keyboard_inline.categories_enroll_srcs_inl_kbd import (
    CategoryToServiceContinueCBData)
from telegram.keyboard_inline.enroll_services_inl_kbd import (
    get_enroll_service_inl_kbd)
from telegram.keyboard_inline.masters_enroll_srcs_inl_kbd import (
    MasterToServiceContinueCBData)
from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
    MethodToServiceDirectlyContinueCBD)
from telegram.keyboard_inline.submenu_services_inl_kbd import (
    EnrollSingleMasterServicesCBData)
from telegram.keyboard_reply.pvt_enroll_services_action_reply_kbd import (
    get_enroll_services_reply_kbd)
from telegram.params.icons_services import (
    SERVICES_ICONS)
from telegram.params.messages import (
    SELECT_SERVICES_BELLOW,
    OR_SELECT_ENROLL_SRCS_MENU_BTN,
    NO_SERVICES_FOR_SELECTED_OPTIONS)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_service_brief_info,
    get_service_brief_info_with_master)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    re_open_reply_keyboard_message)
from utilities.numeric_utils import (
    number_or_str_to_float)

inline_services_filtered_enroll_srcs_cb_router = Router(name=__name__)
inline_services_filtered_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_services_filtered_enroll_srcs_cb_router.callback_query(EnrollSingleMasterServicesCBData.filter())
@inline_services_filtered_enroll_srcs_cb_router.callback_query(MethodToServiceDirectlyContinueCBD.filter())
@inline_services_filtered_enroll_srcs_cb_router.callback_query(MasterToServiceContinueCBData.filter())
@inline_services_filtered_enroll_srcs_cb_router.callback_query(CategoryToServiceContinueCBData.filter())
@inline_services_filtered_enroll_srcs_cb_router.callback_query(ReturnCalendarToSrcsFilteredCBData.filter())
async def inline_enroll_srcs_filtered_cb_hdr(callback_query: CallbackQuery,
                                             callback_data: CallbackData,
                                             bot: Bot,
                                             state: FSMContext):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    callback_prefix = callback_data.__prefix__

    # ##################################################################
    # Delete next calendar hdr msgs on return btn to enroll srcs filtered
    # ##################################################################
    if callback_prefix == ReturnCalendarToSrcsFilteredCBData.__prefix__:
        await delete_calendar_msgs_before_srcs_filtered(
            callback_query=callback_query, state=state, bot=bot)
    # ##################################################################

    # If inline button 'Enroll Master Services' (no criteria for services)
    if callback_prefix == EnrollSingleMasterServicesCBData.__prefix__:
        selected_category_id = []
        selected_master_id = []
    else:
        selected_category_id = await get_valid_int_by_fsm_state_key(
            fsm_state_or_dict_from=state_data,
            fsm_state_literal_key="selected_category_id")

        selected_master_id = await get_valid_int_by_fsm_state_key(
            fsm_state_or_dict_from=state_data,
            fsm_state_literal_key="selected_master_id")

    if selected_category_id and selected_master_id:
        all_services_records = get_all_services_ordered(
            category_id=selected_category_id,
            master_id=selected_master_id,
            active=True,
            order_by_fields=("name", "price",))
    elif selected_master_id:
        all_services_records = get_all_services_ordered(
            master_id=selected_master_id,
            active=True,
            order_by_fields=("name", "price",))
    elif selected_category_id:
        all_services_records = get_all_services_ordered(
            category_id=selected_category_id,
            active=True,
            order_by_fields=("name", "price",))
    else:  # elif not selected_category_id and not selected_master_id
        all_services_records = get_all_services_ordered(
            active=True,
            order_by_fields=("name", "price",))

    if not all_services_records:
        await callback_query.answer(text=NO_SERVICES_FOR_SELECTED_OPTIONS,
                                    show_alert=True)
        return

    try:
        cur_message = await callback_query.message.edit_text(
            text=SELECT_SERVICES_BELLOW)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tPrior message was edited to 'Select services bellow' "
              f"\tmessage successfully\n")
    except (TelegramBadRequest, Exception) as exception_info:
        cur_message = await callback_query.message.answer(
            text=SELECT_SERVICES_BELLOW)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tNew 'Select services bellow' msg was created, because "
              f"\tprior message is not editable: {exception_info}\n")

    selected_services_ids = []
    total_cost_selected = 0
    total_duration_selected = timedelta(0)
    # selected_services_ids = await get_valid_list_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="selected_services_ids_state")

    # selected_method_prefix = await get_valid_str_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="selected_method_prefix")

    all_services_info_dict = {}
    for service_record in all_services_records:
        # if (selected_method_prefix == MethodCategoryToServiceContinueCBD.__prefix__
        #         and SERVICES_CONFIGS.SHOW_MASTERS_NAMES_WHEN_BY_CATEGORY):
        if (not selected_master_id
                and SERVICES_CONFIGS.SHOW_MASTERS_NAMES_WHEN_BY_CATEGORY):
            masters_full_names = get_masters_names_by_service_obj(
                service_obj=service_record)
            service_brief_text = get_service_brief_info_with_master(
                service_record=service_record,
                masters_info=masters_full_names)
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

        cur_message = await callback_query.message.answer(
            text=f"{cur_service_icon} "
                 f"{service_brief_text}\n",
            reply_markup=get_enroll_service_inl_kbd(
                service_id=service_record.id,
                button_selected=button_selected,
                one_more_service_btn=one_more_service_btn))
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tCurrent service message id added to msgs ids list to delete:\n"
              f"\tcur_message.message_id = {cur_message.message_id}\n"
              f"\tcur_handler_messages_ids = {cur_handler_messages_ids}\n")

        delay_seconds = number_or_str_to_float(PAUSE_CONFIGS.LIST_MESSAGES_DELAY)
        if delay_seconds:
            await asyncio.sleep(delay_seconds)

        all_services_info_dict[service_record.id] = {
            "text": service_brief_text,
            "price": service_record.price,
            "duration": service_record.time_duration}

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=callback_query,
        re_open_reply_msg_text=OR_SELECT_ENROLL_SRCS_MENU_BTN,
        re_open_reply_keyboard=get_enroll_services_reply_kbd(
            show_continue_button=False),
        reply_kbd_opened_state_after_open=False,
        open_reply_kbd_msg_anyway=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tEnroll services [no continue] reply kbd opened, "
              f"because open_reply_kbd_msg_anyway = True\n"
              f"\tcur_handler_messages_ids = {cur_handler_messages_ids}\n")

    await state.update_data(
        selected_services_ids_state=selected_services_ids,
        selected_services_cost_state=total_cost_selected,
        selected_services_duration_state=total_duration_selected,
        all_services_info_state=all_services_info_dict)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=True,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
