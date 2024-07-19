from aiogram import Router
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from aiogram.filters.callback_data import CallbackData

from telegram.config.configs import LANGUAGE_CONFIGS
from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.keyboard_inline.calendar_inl_kbd import MonthContinueCBData
from telegram.params.calendar_icons import CALENDAR_ICONS

from telegram.telegram_utils.messages_helpers import get_selected_services_summary
from utilities.calendar_utils import get_date_with_month_name

from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)

from telegram.telegram_utils.enroll_services_utils import (
    get_selected_services_ids,
    get_selected_services_cost,
    get_selected_services_duration)

from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    cannot_modify_obsolete_inl_kbd)


continue_enroll_srcs_calendar_cb_router = Router(name=__name__)
continue_enroll_srcs_calendar_cb_router.message.filter(ChatTypesFilter(["private"]))


@continue_enroll_srcs_calendar_cb_router.callback_query(MonthContinueCBData.filter())
async def continue_enroll_srcs_calendar_cb_hdr(callback_query: CallbackQuery,
                                               callback_data: CallbackData,
                                               state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        await cannot_modify_obsolete_inl_kbd(callback_query)
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    message = callback_query.message

    selected_services_ids = await get_selected_services_ids(state=state_data)
    total_cost_selected = await get_selected_services_cost(state=state_data)
    total_duration_selected = await get_selected_services_duration(state=state_data)

    selected_data = state_data.get("selected_date_enroll_srcs_calendar")

    summary_text = get_selected_services_summary(
           services_count=len(selected_services_ids),
           total_cost=total_cost_selected,
           total_duration=total_duration_selected)

    date_string = get_date_with_month_name(
        selected_data,
        language=LANGUAGE_CONFIGS.LANGUAGE)

    await message.answer(
        text=f"{CALENDAR_ICONS.CALENDAR} <b>{date_string}</b>"
             f"{summary_text}")

    return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)
