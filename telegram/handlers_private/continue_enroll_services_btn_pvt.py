import asyncio

from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from telegram.filters.chat_types_filter import ChatTypesFilter

from aiogram.fsm.context import FSMContext

from telegram.keyboard_inline.calendar_inl_kbd import get_enroll_srcs_calendar_inl_kbd

from telegram.params.buttons_enroll_service import ENROLL_SERVICE_BUTTONS
from telegram.params.messages_helpers import get_selected_services_summary
from telegram.params.messages import (SELECT_MIN_ONE_SERVICE,
                                      CHOOSE_SERVICE_DAY)

from telegram.telegram_utils.enroll_services_utils import (
    get_selected_services_ids,
    get_selected_services_cost,
    get_selected_services_duration)

from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handlers_stack_list,
    get_handler_answer_flag_dict)

continue_enroll_srcs_pvt_router = Router(name=__name__)
continue_enroll_srcs_pvt_router.message.filter(ChatTypesFilter(["private"]))


@continue_enroll_srcs_pvt_router.message(
    F.text == ENROLL_SERVICE_BUTTONS.CONTINUE_ENROLL_SERVICES)
async def continue_enroll_services_btn_handler(message: Message,
                                               state: FSMContext):
    state_data = await state.get_data()
    selected_services_ids = await get_selected_services_ids(state=state_data)

    if not selected_services_ids:
        await message.answer(text=SELECT_MIN_ONE_SERVICE)
        await asyncio.sleep(2.5)

        handlers_list = await get_handlers_stack_list(state=state)
        await execute_last_stack_handler(handlers_list=handlers_list)

        return get_handler_answer_flag_dict(skip_handler_stack=True)

    total_cost_selected = await get_selected_services_cost(state=state_data)
    total_duration_selected = await get_selected_services_duration(state=state_data)

    await message.answer(
        text=get_selected_services_summary(
            services_count=len(selected_services_ids),
            total_cost=total_cost_selected,
            total_duration=total_duration_selected,
            salutation_flag=True),
        reply_markup=ReplyKeyboardRemove())

    await message.answer(
        text=CHOOSE_SERVICE_DAY,
        reply_markup=get_enroll_srcs_calendar_inl_kbd(date_value=datetime.now()))
