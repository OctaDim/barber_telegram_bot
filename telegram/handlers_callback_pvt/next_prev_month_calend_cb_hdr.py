from datetime import datetime

from aiogram import Router
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from aiogram.filters.callback_data import CallbackData
from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.keyboard_inline.calendar_inl_kbd import (
    NextMonthCBData,
    PreviousMonthCBData,
    get_enroll_srcs_calendar_inl_kbd)

from telegram.telegram_utils.handlers_stack_utils import get_handler_answer_flag_dict
from telegram.telegram_utils.messages_utils import inline_keyboard_is_actual

from telegram.params.messages import CHOOSE_SERVICES_DAY


next_prev_month_services_cb_router = Router(name=__name__)
next_prev_month_services_cb_router.message.filter(ChatTypesFilter(["private"]))

@next_prev_month_services_cb_router.callback_query(PreviousMonthCBData.filter())
@next_prev_month_services_cb_router.callback_query(NextMonthCBData.filter())
async def next_prev_month_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                             callback_data: CallbackData,
                                             state: FSMContext):

    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    await callback_query.answer()

    calendar_month = state_data.get("cur_month_enroll_srcs_calendar")
    calendar_year = state_data.get("cur_year_enroll_srcs_calendar")

    if callback_data.__prefix__ == "next_month_enroll_srcs":
        calendar_month += 1

        if calendar_month > 12:
            calendar_month = 1
            calendar_year += 1

    elif callback_data.__prefix__ == "prev_month_enroll_srcs":
        calendar_month -= 1

        if calendar_month < 1:
            calendar_month = 12
            calendar_year -= 1

    else:
        calendar_month = datetime.now().month
        calendar_year = datetime.now().year

    await callback_query.message.edit_text(
        text=CHOOSE_SERVICES_DAY,
        reply_markup=get_enroll_srcs_calendar_inl_kbd(calendar_year=calendar_year,
                                                      calendar_month=calendar_month))

    await state.update_data(
        cur_month_enroll_srcs_calendar=calendar_month,
        cur_year_enroll_srcs_calendar=calendar_year,
        selected_date_enroll_srcs_calendar=None)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
