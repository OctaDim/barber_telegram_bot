from datetime import datetime

from aiogram import Router
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from aiogram.filters.callback_data import CallbackData

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.keyboard_inline.calendar_inl_kbd import (
    MonthDayCBData,
    MonthContinueCBData, get_enroll_srcs_calendar_inl_kbd)
from telegram.params.messages import CHOOSE_SERVICES_DAY
from telegram.telegram_utils.handlers_stack_utils import get_handler_answer_flag_dict

from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    cannot_modify_obsolete_inl_kbd)
from utilities.json_utils import create_json_file_from_event

month_day_enroll_srcs_calendar_cb_router = Router(name=__name__)
month_day_enroll_srcs_calendar_cb_router.message.filter(ChatTypesFilter(["private"]))


@month_day_enroll_srcs_calendar_cb_router.callback_query(MonthDayCBData.filter())
async def month_day_enroll_srcs_calendar_cb_hdr(callback_query: CallbackQuery,
                                                callback_data: CallbackData,
                                                state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        await cannot_modify_obsolete_inl_kbd(callback_query)
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    selected_day = callback_data.month_day
    selected_month = state_data.get("cur_month_enroll_srcs_calendar")
    selected_year = state_data.get("cur_year_enroll_srcs_calendar")

    selected_date = datetime(selected_year, selected_month, selected_day)
    await state.update_data(selected_date_enroll_srcs_calendar=selected_date)

    await callback_query.message.edit_text(
        text=CHOOSE_SERVICES_DAY,
        reply_markup=get_enroll_srcs_calendar_inl_kbd(calendar_year=selected_year,
                                                      calendar_month=selected_month,
                                                      selected_date=selected_date))

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
