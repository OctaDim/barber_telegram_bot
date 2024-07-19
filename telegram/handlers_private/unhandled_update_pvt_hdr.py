from time import sleep

from aiogram import Router
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.config.configs import PAUSE_CONFIGS

from telegram.params.messages import UNKNOWN_COMMAND_ENTERED

from utilities.numeric_utils import number_or_str_to_float
from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handlers_stack_list,
    get_handler_answer_flag_dict)


unhandled_update_router = Router(name=__name__)
unhandled_update_router.message.filter(ChatTypesFilter(["private"]))


@unhandled_update_router.message()
async def unhandled_update_handler(message: Message, state: FSMContext):
    await message.reply(text=UNKNOWN_COMMAND_ENTERED)

    delay_seconds = number_or_str_to_float(PAUSE_CONFIGS.SHORT_MSG_DELAY)
    sleep(delay_seconds)

    handlers_list = await get_handlers_stack_list(state=state)
    await execute_last_stack_handler(handlers_list=handlers_list)

    print("\tTEST INFO: Unhandled_update_handler. Handler answer = skip_add_handler_stack")
    print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
