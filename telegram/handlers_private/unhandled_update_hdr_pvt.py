from time import sleep

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.config.configs import PAUSE_CONFIGS
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.params.messages import UNKNOWN_COMMAND_ENTERED
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handler_answer_flag_dict)
from utilities.numeric_utils import number_or_str_to_float

unhandled_update_router = Router(name=__name__)
unhandled_update_router.message.filter(ChatTypesFilter(["private"]))


@unhandled_update_router.message()
async def unhandled_update_handler_pvt(message: Message, state: FSMContext):
    await message.reply(text=UNKNOWN_COMMAND_ENTERED)

    delay_seconds = number_or_str_to_float(PAUSE_CONFIGS.SHORT_MSG_DELAY)
    sleep(delay_seconds)

    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state,
        fsm_state_literal_key="handlers_stack")

    await execute_last_stack_handler(handlers_list=handlers_list)

    print("\tTEST INFO: Unhandled_update_handler. Handler answer = skip_add_handler_stack")
    print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
