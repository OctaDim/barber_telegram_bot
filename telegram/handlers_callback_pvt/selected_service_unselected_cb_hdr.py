import copy
import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enroll_services_inl_kbd import (
    EnrollServiceCallbackData,
    OneMoreServiceCallbackData,
    get_enroll_service_inl_kbd)
from telegram.keyboard_reply.pvt_enroll_services_action_reply_kbd import (
    get_enroll_services_reply_kbd)
from telegram.params.icons_services import (
    SERVICES_ICONS)
from telegram.params.messages import (
    NONE_SERVICES_SELECTED,
    OR_SELECT_ENROLL_SERVICES_MENU)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_dict_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key,
    get_valid_list_by_fsm_state_key,
    get_valid_float_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_selected_services_summary)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    re_open_reply_keyboard_message)
from utilities.dict_utils import (
    empty_dict_if_none)
from utilities.list_utils import (
    remove_same_list_elms_by_value)

service_selected_unselected_enroll_srcs_cb_router = Router(name=__name__)
service_selected_unselected_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@service_selected_unselected_enroll_srcs_cb_router.callback_query(EnrollServiceCallbackData.filter())
@service_selected_unselected_enroll_srcs_cb_router.callback_query(OneMoreServiceCallbackData.filter())
async def service_selected_unselected_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                                         callback_data: CallbackData,
                                                         state: FSMContext):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    callback_prefix = callback_data.__prefix__

    all_services_info = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="all_services_info_state")

    cur_service_info = all_services_info.get(callback_data.service_id)
    cur_service_info = empty_dict_if_none(cur_service_info)

    cur_service_id = callback_data.service_id
    cur_service_text = cur_service_info.get("text")
    cur_service_price = cur_service_info.get("price")
    cur_service_duration = cur_service_info.get("duration")

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    total_cost_selected = await get_valid_float_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_cost_state")

    total_duration_selected = await get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_duration_state")

    new_service_text = None
    enroll_services_inline_kbd = None

    # If service is not selected at all
    if cur_service_id not in selected_services_ids:
        selected_services_ids.append(cur_service_id)

        total_cost_selected += cur_service_price
        total_cost_selected = round(total_cost_selected, 2)
        total_duration_selected += cur_service_duration

        button_txt_icon = SERVICES_ICONS.SELECTED
        new_service_text = f"{button_txt_icon} {cur_service_text}"
        enroll_services_inline_kbd = get_enroll_service_inl_kbd(
            service_id=cur_service_id,
            button_selected=True,
            one_more_service_btn=True)

    else:  # If service is selected at least one time or several times
        if callback_prefix == EnrollServiceCallbackData.__prefix__:
            # Cancel this service entirely
            same_id_count = selected_services_ids.count(cur_service_id)
            selected_services_ids = remove_same_list_elms_by_value(
                old_list=selected_services_ids,
                value_to_remove=cur_service_id)

            total_cost_selected -= cur_service_price * same_id_count
            total_cost_selected = round(total_cost_selected, 2)
            total_duration_selected -= cur_service_duration * same_id_count

            button_txt_icon = SERVICES_ICONS.SERVICE_POINT
            new_service_text = f"{button_txt_icon} {cur_service_text}"
            enroll_services_inline_kbd = get_enroll_service_inl_kbd(
                service_id=cur_service_id,
                button_selected=False)

        elif callback_prefix == OneMoreServiceCallbackData.__prefix__:
            # Enroll the same service again
            selected_services_ids.append(cur_service_id)
            total_cost_selected += cur_service_price
            total_cost_selected = round(total_cost_selected, 2)
            total_duration_selected += cur_service_duration

            same_id_count = selected_services_ids.count(cur_service_id)
            button_txt_icon = f"{SERVICES_ICONS.SELECTED} " * same_id_count

            new_service_text = f"{button_txt_icon} {cur_service_text}"
            enroll_services_inline_kbd = get_enroll_service_inl_kbd(
                service_id=cur_service_id,
                button_selected=True,
                one_more_service_btn=True)

    try:
        await callback_query.message.edit_text(
            text=new_service_text,
            reply_markup=enroll_services_inline_kbd)
    except (TelegramBadRequest, Exception) as exception_info:
        print(f"\tMessage not modified, tg exception intercepted: "
              f"{exception_info}\n")

    summary_text = get_selected_services_summary(
        services_count=len(selected_services_ids),
        total_cost=total_cost_selected,
        total_duration=total_duration_selected)

    prior_reply_message_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="prior_reply_message_id_state")

    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="handlers_stack")
    print(f"\tOrigin handler stack: len(handlers_list)={len(handlers_list)}\n")

    prior_handler_dict = handlers_list[-1]
    prior_handler_msgs_ids = prior_handler_dict["handler_messages_ids"]
    messages_ids_to_change = copy.copy(prior_handler_msgs_ids)
    print(f"\tOrigin data (handler [-1]):\n"
          f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\tmessages_ids_to_change = {messages_ids_to_change}\n")

    if selected_services_ids:
        await callback_query.answer(text=summary_text,
                                    show_alert=True)

        cur_message = await re_open_reply_keyboard_message(
            fsm_state=state,
            telegram_update_obj=callback_query,
            re_open_reply_msg_text=OR_SELECT_ENROLL_SERVICES_MENU,
            re_open_reply_keyboard=get_enroll_services_reply_kbd(
                show_continue_button=True),
            reply_kbd_opened_state_after_open=True)
        if cur_message:
            messages_ids_to_change.remove(prior_reply_message_id)
            messages_ids_to_change.append(cur_message.message_id)
            prior_handler_dict["handler_messages_ids"] = messages_ids_to_change
            handlers_list.pop()
            handlers_list.append(prior_handler_dict)
            print(f"\tEnroll services [with continue] reply kbd opened, because\n"
                  f"\tselected_services_ids = {selected_services_ids}\n"
                  f"\treply_kbd_opened_state_after_open = False\n"
                  f"\tprior_reply_message_id = {prior_reply_message_id}\n"
                  f"\tcur_message.message_id = {cur_message.message_id}\n"
                  f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
                  f"\tmessages_ids_to_change = {messages_ids_to_change}\n")
    else:
        await callback_query.answer(text=NONE_SERVICES_SELECTED,
                                    show_alert=True)
        cur_message = await re_open_reply_keyboard_message(
            fsm_state=state,
            telegram_update_obj=callback_query,
            re_open_reply_msg_text=OR_SELECT_ENROLL_SERVICES_MENU,
            re_open_reply_keyboard=get_enroll_services_reply_kbd(
                show_continue_button=False),
            reply_kbd_opened_state_after_open=False,
            open_reply_kbd_msg_anyway=True)
        if cur_message:
            messages_ids_to_change.remove(prior_reply_message_id)
            messages_ids_to_change.append(cur_message.message_id)
            prior_handler_dict["handler_messages_ids"] = messages_ids_to_change
            handlers_list.pop()
            handlers_list.append(prior_handler_dict)
            print(f"\tEnroll services [no continue] reply kbd opened, because\n"
                  f"\tselected_services_ids = {selected_services_ids}\n"
                  f"\treply_kbd_opened_state_after_open = False\n"
                  f"\tprior_reply_message_id = {prior_reply_message_id}\n"
                  f"\tcur_message.message_id = {cur_message.message_id}\n"
                  f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
                  f"\tmessages_ids_to_change = {messages_ids_to_change}\n")

    await state.update_data(
        selected_services_ids_state=selected_services_ids,
        selected_services_cost_state=total_cost_selected,
        selected_services_duration_state=total_duration_selected,
        # Additional update
        handlers_stack=handlers_list)
    print(f"\tState updated when selected-unselected services:\n"
          f"\tlen(handlers_stack) = {len(handlers_list)}\n")

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
