from aiogram import Router
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import ChatTypesFilter


unhandled_update_router = Router(name=__name__)
unhandled_update_router.message.filter(ChatTypesFilter(["private"]))


@unhandled_update_router.message()
async def unhandled_update_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    handlers_list = state_data.get("handlers_stack")

    print("\tTEST INFO: len(handlers_list): ", len(handlers_list))
    handlers_list.pop()
    print("\tTEST INFO: Unhandled update. Handlers stack reduced by 1 records")
    print("\tTEST INFO: len(handlers_list): ", len(handlers_list))
    print()

    await state.update_data(handlers_stack=handlers_list)
