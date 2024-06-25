from datetime import timedelta
from random import randrange

from aiogram import Router, Bot
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from telegram.params.messages import NONE_SERVICES_SELECTED
from telegram.params.messages_helpers import get_service_brief_info_from_record, get_service_brief_info_from_dict
from telegram.params.messages_inserts import MSG
from telegram.params.messages_variants import SERVICE_SELECTED_VARIANTS
from telegram.params.select_services_icons import SELECT_SERVICES_ICONS
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_inline.enroll_services_inl_kbd import (
    EnrollServiceCallbackData,
    get_enroll_service_inl_kbd)


enroll_services_cb_router = Router(name=__name__)
enroll_services_cb_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_cb_router.callback_query(EnrollServiceCallbackData.filter())
async def select_service_callback_hdr(callback_query: CallbackQuery,
                                      callback_data: EnrollServiceCallbackData,
                                      state: FSMContext):

    data = await state.get_data()
    all_services_info = data.get("all_services_info_state")
    cur_service_info = all_services_info.get(callback_data.service_id)

    cur_service_text = cur_service_info.get("text")
    cur_service_price = cur_service_info.get("price")
    cur_service_duration = cur_service_info.get("duration")

    selected_services_ids = data.get("selected_services_ids_state", [])
    total_cost_selected = data.get("selected_services_cost_state", 0.0)
    total_duration_selected = data.get("selected_services_duration_state",
                                       timedelta(0))

    if not callback_data.inl_button_selected:
        button_state_icon = SELECT_SERVICES_ICONS.SELECTED
        new_service_text = f"{button_state_icon} {cur_service_text}"
        inline_keyboard = get_enroll_service_inl_kbd(
            callback_data.service_id,
            button_selected=True)

        selected_services_ids.append(callback_data.service_id)
        total_cost_selected = round(total_cost_selected + cur_service_price, 2)
        total_duration_selected += cur_service_duration

    else:
        button_state_icon = SELECT_SERVICES_ICONS.NO_ICON
        new_service_text = f"{button_state_icon} {cur_service_text}"
        inline_keyboard = get_enroll_service_inl_kbd(
            callback_data.service_id,
            button_selected=False)

        selected_services_ids.remove(callback_data.service_id)
        total_cost_selected = round(total_cost_selected - cur_service_price, 2)
        total_duration_selected -= cur_service_duration


    await callback_query.message.edit_text(text=new_service_text,
                                           reply_markup=inline_keyboard)

    await state.update_data(
        selected_services_ids_state=selected_services_ids,
        selected_services_cost_state=total_cost_selected,
        selected_services_duration_state=total_duration_selected)

    await state.update_data()

    if len(selected_services_ids):
        await callback_query.answer(
        text=f"{MSG.SERVICES_TOTAL_COUNT} {len(selected_services_ids)}\n"
             f"{MSG.SERVICES_TOTAL_COST} {total_cost_selected} {MSG.CURRENCY_BRIEF}\n"
             f"{MSG.SERVICES_TOTAL_DURATION} {total_duration_selected}",
        show_alert=True)
    else:
        await callback_query.answer(text=NONE_SERVICES_SELECTED,
                                    show_alert=True)
