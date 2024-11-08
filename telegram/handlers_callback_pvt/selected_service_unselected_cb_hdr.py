from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.errors_api_telegram.telegram_exception_errors import (
    TG_EXCEPT_ERRORS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enroll_services_inl_kbd import (
    EnrollServiceCallbackData,
    OneMoreServiceCallbackData,
    get_enroll_service_inl_kbd)
from telegram.params.messages import (
    NONE_SERVICES_SELECTED)
from telegram.params.services_icons import (
    SERVICES_ICONS)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_dict_by_fsm_state_key,
    get_valid_timedelta_by_fsm_state_key,
    get_valid_list_by_fsm_state_key,
    get_valid_float_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_selected_services_summary)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)
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

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    callback_prefix = callback_data.__prefix__

    all_services_info = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="all_services_info_state")

    cur_service_info = all_services_info.get(callback_data.service_id)

    cur_service_id = callback_data.service_id
    cur_service_text = cur_service_info.get("text")
    cur_service_price = cur_service_info.get("price")
    cur_service_duration = cur_service_info.get("duration")

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    total_cost_selected = await get_valid_float_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_cost_state")

    total_duration_selected = await get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_duration_state")

    new_service_text = ""
    inline_keyboard = None

    # If service is not selected at all
    if cur_service_id not in selected_services_ids:
        selected_services_ids.append(cur_service_id)

        total_cost_selected += cur_service_price
        total_cost_selected = round(total_cost_selected, 2)
        total_duration_selected += cur_service_duration

        button_txt_icon = SERVICES_ICONS.SELECTED
        new_service_text = f"{button_txt_icon} {cur_service_text}"
        inline_keyboard = get_enroll_service_inl_kbd(
            service_id=cur_service_id,
            button_selected=True,
            one_more_service_btn=True)

    else:  # If service is selected at least one time or several times
        if callback_prefix == EnrollServiceCallbackData.__prefix__:  # Cancel this service entirely
            same_id_count = selected_services_ids.count(cur_service_id)
            selected_services_ids = remove_same_list_elms_by_value(
                old_list=selected_services_ids,
                value_to_remove=cur_service_id)

            total_cost_selected -= cur_service_price * same_id_count
            total_cost_selected = round(total_cost_selected, 2)
            total_duration_selected -= cur_service_duration * same_id_count

            button_txt_icon = SERVICES_ICONS.SERVICE_POINT
            new_service_text = f"{button_txt_icon} {cur_service_text}"
            inline_keyboard = get_enroll_service_inl_kbd(
                service_id=cur_service_id,
                button_selected=False)

        elif callback_prefix == OneMoreServiceCallbackData.__prefix__:  # Enrol the same service again
            selected_services_ids.append(cur_service_id)
            total_cost_selected += cur_service_price
            total_cost_selected = round(total_cost_selected, 2)
            total_duration_selected += cur_service_duration

            same_id_count = selected_services_ids.count(cur_service_id)
            button_txt_icon = f"{SERVICES_ICONS.SELECTED} " * same_id_count

            new_service_text = f"{button_txt_icon} {cur_service_text}"
            inline_keyboard = get_enroll_service_inl_kbd(
                service_id=cur_service_id,
                button_selected=True,
                one_more_service_btn=True)

    try:
        await callback_query.message.edit_text(
            text=new_service_text,
            reply_markup=inline_keyboard)
    except TelegramBadRequest as error:
        if error.message == TG_EXCEPT_ERRORS.MSG_NOT_MODIFIED:
            print("\tLOG INFO: 'Message not modified' tg exception was intercepted\n")
            pass

    await state.update_data(
        selected_services_ids_state=selected_services_ids,
        selected_services_cost_state=total_cost_selected,
        selected_services_duration_state=total_duration_selected)

    summary_text = get_selected_services_summary(
        services_count=len(selected_services_ids),
        total_cost=total_cost_selected,
        total_duration=total_duration_selected)

    if selected_services_ids:
        await callback_query.answer(text=summary_text,
                                    show_alert=True)
    else:
        await callback_query.answer(text=NONE_SERVICES_SELECTED,
                                    show_alert=True)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
