from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.db_queries.create_user_on_start_query import create_user_on_start
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.fsm_states.register_new_client_user import RegisterNewClientState
from telegram.handlers_private.commands_pvt import menu_command
from telegram.params.register_user import ONLY_SPACES_USER_NAME, LESS_2_SYMBOLS_USER_NAME


client_enter_name_state_router = Router(name=__name__)
client_enter_name_state_router.message.filter(ChatTypesFilter(["private"]))


@client_enter_name_state_router.message(StateFilter(RegisterNewClientState.new_client_name))
async def client_enter_name_state_hdr_pvt(message: Message,
                                          state: FSMContext):
    await state.set_state(None)

    if len(message.text) < 2:
        await message.answer(text=LESS_2_SYMBOLS_USER_NAME)
        await state.update_data(new_client_name=None)
        await state.set_state(RegisterNewClientState.new_client_name)
        return

    data = message.from_user.dict()
    data['first_name'] = message.text
    result = create_user_on_start(data=data, master=False)
    if not result:
        await message.answer(text=ONLY_SPACES_USER_NAME)
        await state.update_data(new_client_name=None)
        await state.set_state(RegisterNewClientState.new_client_name)
        return

    await menu_command(message=message, state=state)
