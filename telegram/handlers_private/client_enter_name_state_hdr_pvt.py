from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.db_queries.create_user_on_start_query import create_user_on_start
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.fsm_states.register_new_client_user import RegisterNewClientState
from telegram.handlers_private.commands_pvt import menu_command

client_enter_name_state_router = Router(name=__name__)
client_enter_name_state_router.message.filter(ChatTypesFilter(["private"]))


@client_enter_name_state_router.message(StateFilter(RegisterNewClientState.new_client_name))
async def client_enter_name_state_hdr_pvt(message: Message,
                                          state: FSMContext):
    data = message.from_user.dict()
    data['first_name'] = message.text

    await menu_command(message=message, state=state)

    create_user_on_start(data=data, master=True)
