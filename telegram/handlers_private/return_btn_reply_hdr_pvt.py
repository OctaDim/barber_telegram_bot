from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.params.buttons_common import (
    COMMON_BUTTONS_PARAMS)
from telegram.params.messages import (
    CAN_USE_LEFT_MENU)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handler_answer_flag_dict)

return_button_router = Router(name=__name__)
return_button_router.message.filter(ChatTypesFilter(["private"]))


@return_button_router.message(F.text == COMMON_BUTTONS_PARAMS.RETURN)
async def return_button_reply_hdr_pvt(message: Message,
                                      state: FSMContext,
                                      current_handler_data: dict):
    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state,
        fsm_state_literal_key="handlers_stack")

    if len(handlers_list) <= 2:
        await state.clear()

    if len(handlers_list) <= 1:
        await message.answer(text=CAN_USE_LEFT_MENU)
        handlers_list = []
        print("\tTEST INFO: Return handler. Handlers stack cleared")
        print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    else:
        del handlers_list[-1]
        await execute_last_stack_handler(handlers_list)

        # #### For the future
        # current_hdr_function = current_handler_data.get("handler")
        # current_hdr_event = current_handler_data.get("event")
        # current_hdr_data = current_handler_data.get("data")
        # print(f"\t{current_hdr_function}\n")
        # print(f"\t{current_hdr_event}\n")
        # print(f"\t{current_hdr_data}\n")

        print("\tTEST INFO: Return handler. Handlers stack reduced -1 and executed")
        print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    await state.update_data(handlers_stack=handlers_list)

    print("\tTEST INFO: Return handler. Handler answer = skip_add_handler_stack")
    print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
