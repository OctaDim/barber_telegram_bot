import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.telegram_utils.enroll_services_utils import get_selected_services_ids

from telegram.params.buttons_enroll_service import ENROLL_SERVICE_BUTTONS
from telegram.params.messages import (ALL_SERVICES_CANCELLED,
                                      NONE_SERVICES_SELECTED)

from telegram.telegram_utils.handlers_stack_utils import (
    get_handlers_stack_list,
    execute_last_stack_handler,
    get_handler_answer_flag_dict)


cancel_all_services_pvt_router = Router(name=__name__)
cancel_all_services_pvt_router.message.filter(ChatTypesFilter(["private"]))


@cancel_all_services_pvt_router.message(
    F.text == ENROLL_SERVICE_BUTTONS.CANCEL_ALL_CERVICES)
async def cancel_all_services_btn_handler(message: Message,
                                          state: FSMContext):
    state_data = await state.get_data()
    selected_services_ids = await get_selected_services_ids(state=state_data)

    if selected_services_ids:
        message_text = ALL_SERVICES_CANCELLED

        # Reset total info of the selected services in a state
        await state.update_data(
            selected_services_ids_state=None,
            selected_services_cost_state=None,
            selected_services_duration_state=None)
    else:
        message_text = NONE_SERVICES_SELECTED

    await message.answer(text=message_text)
    await asyncio.sleep(2)

    handlers_list = await get_handlers_stack_list(state=state)
    await execute_last_stack_handler(handlers_list=handlers_list)

    return get_handler_answer_flag_dict(skip_handler_stack=True)
