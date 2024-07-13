from aiogram import Router, F
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.telegram_utils.list_utils import empty_list_if_none
from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handlers_stack_list,
    get_handler_answer_flag_dict)

from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS
from telegram.params.messages import CAN_USE_LEFT_MENU


return_button_router = Router(name=__name__)
return_button_router.message.filter(ChatTypesFilter(["private"]))


@return_button_router.message(F.text == COMMON_BUTTONS_PARAMS.RETURN)
async def return_button_handler(message: Message,
                                state: FSMContext,
                                current_handler_data: dict):

    handlers_list = await get_handlers_stack_list(state=state)

    if len(handlers_list) <= 1:
        await message.answer(text=CAN_USE_LEFT_MENU)
        handlers_list = None

        print("\tTEST INFO: Return handler. Handlers stack cleared")
        handlers_list = empty_list_if_none(handlers_list)
        print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    else:
        del handlers_list[-1]
        await execute_last_stack_handler(handlers_list)

        # current_hdr_function = current_handler_data.get("handler")
        # current_hdr_event = current_handler_data.get("event")
        # current_hdr_data = current_handler_data.get("data")
        # print(f"\t{current_hdr_function}\n")
        # print(f"\t{current_hdr_event}\n")
        # print(f"\t{current_hdr_data}\n")

        print("\tTEST INFO: Return handler. Handlers stack reduced -1 and executed")
        print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    await state.update_data(handlers_stack=handlers_list)

    print("\tTEST INFO: Return handler. Handler answer = skip_handler_stack")
    print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    return get_handler_answer_flag_dict(skip_handler_stack=True)
