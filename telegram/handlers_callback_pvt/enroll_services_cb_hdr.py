from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.telegram_utils.enroll_services_utils import get_selected_services_ids, get_selected_services_cost, \
    get_selected_services_duration

from telegram.telegram_utils.list_utils import remove_same_list_elms_by_value

from telegram.keyboard_inline.enroll_services_inl_kbd import (
    EnrollServiceCallbackData,
    OneMoreServiceCallbackData,
    get_enroll_service_inl_kbd)

from telegram.telegram_utils.messages_utils import cannot_modify_obsolete_list

from telegram.params.select_services_icons import SELECT_SERVICES_ICONS
from telegram.params.messages_helpers import get_selected_services_summary
from telegram.params.messages import NONE_SERVICES_SELECTED


enroll_services_cb_router = Router(name=__name__)
enroll_services_cb_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_cb_router.callback_query(EnrollServiceCallbackData.filter())
@enroll_services_cb_router.callback_query(OneMoreServiceCallbackData.filter())
async def select_service_callback_hdr(callback_query: CallbackQuery,
                                      callback_data: CallbackData,
                                      state: FSMContext):
    data = await state.get_data()
    if not data:
        await cannot_modify_obsolete_list(callback_query)
        return

    # Checking if inline keyboard is not obsolete (not older )
    last_not_inline_msg_id = data.get("last_not_inline_msg_id_state")
    if callback_query.message.message_id < last_not_inline_msg_id:
        await cannot_modify_obsolete_list(callback_query)
        return

    all_services_info = data.get("all_services_info_state")
    cur_service_info = all_services_info.get(callback_data.service_id)

    cur_service_id = callback_data.service_id
    cur_service_text = cur_service_info.get("text")
    cur_service_price = cur_service_info.get("price")
    cur_service_duration = cur_service_info.get("duration")

    selected_services_ids = await get_selected_services_ids(state=data)
    total_cost_selected = await get_selected_services_cost(state=data)
    total_duration_selected = await get_selected_services_duration(state=data)

    if not cur_service_id in selected_services_ids:  # If service is not selected entirely
        selected_services_ids.append(cur_service_id)

        total_cost_selected += cur_service_price
        total_cost_selected = round(total_cost_selected, 2)
        total_duration_selected += cur_service_duration

        button_state_icon = SELECT_SERVICES_ICONS.SELECTED
        new_service_text = f"{button_state_icon} {cur_service_text}"
        inline_keyboard = get_enroll_service_inl_kbd(
            service_id=cur_service_id,
            button_selected=True,
            one_more_service_btn=True)

    else:  # If service is selected at least one time
        if callback_data.__prefix__ == "enroll_cancel_services":  # Cancel this service entirely
            same_id_count = selected_services_ids.count(cur_service_id)
            selected_services_ids = remove_same_list_elms_by_value(
                old_list=selected_services_ids,
                value_to_remove=cur_service_id)

            total_cost_selected -= cur_service_price * same_id_count
            total_cost_selected = round(total_cost_selected, 2)
            total_duration_selected -= cur_service_duration * same_id_count

            button_state_icon = SELECT_SERVICES_ICONS.NO_ICON
            new_service_text = f"{button_state_icon} {cur_service_text}"
            inline_keyboard = get_enroll_service_inl_kbd(
                service_id=cur_service_id,
                button_selected=False)

        if callback_data.__prefix__ == "one_more_same_service":  # Enroll the same service one more time
            selected_services_ids.append(cur_service_id)
            total_cost_selected += cur_service_price
            total_cost_selected = round(total_cost_selected, 2)
            total_duration_selected += cur_service_duration

            same_id_count = selected_services_ids.count(cur_service_id)

            button_state_icon = f"{SELECT_SERVICES_ICONS.SELECTED} " * same_id_count
            new_service_text = f"{button_state_icon} {cur_service_text}"
            inline_keyboard = get_enroll_service_inl_kbd(
                service_id=cur_service_id,
                button_selected=True,
                one_more_service_btn=True)

    await callback_query.message.edit_text(text=new_service_text,
                                           reply_markup=inline_keyboard)

    await state.update_data(
        selected_services_ids_state=selected_services_ids,
        selected_services_cost_state=total_cost_selected,
        selected_services_duration_state=total_duration_selected)

    if selected_services_ids:
        await callback_query.answer(
            text=get_selected_services_summary(
                services_count=len(selected_services_ids),
                total_cost=total_cost_selected,
                total_duration=total_duration_selected),
            show_alert=True)

    else:
        await callback_query.answer(text=NONE_SERVICES_SELECTED,
                                    show_alert=True)
