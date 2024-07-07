from aiogram import Router, Bot
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.telegram_utils.execute_last_handler import execute_last_handler
from telegram.telegram_utils.list_utils import empty_list_if_none
from telegram.telegram_utils.handler_answer_utils import get_handler_answer_flag_dict

from telegram.params.messages import UNKNOWN_COMMAND_ENTERED


unhandled_update_router = Router(name=__name__)
unhandled_update_router.message.filter(ChatTypesFilter(["private"]))


@unhandled_update_router.message()
async def unhandled_update_handler(message: Message, state: FSMContext):
    await message.reply(text=UNKNOWN_COMMAND_ENTERED)

    state_data = await state.get_data()

    handlers_list = state_data.get("handlers_stack")
    handlers_list = empty_list_if_none(original_list=handlers_list)

    await execute_last_handler(handlers_list=handlers_list)

    print("\tTEST INFO: Unhandled_update_handler. Handler answer = skip_handler_stack")
    print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    return get_handler_answer_flag_dict(skip_handler_stack=True)
