from aiogram import Router
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.db_queries.create_user_on_start_query import (
    create_user_on_start)
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.commands import COMMANDS_PARAMS
from telegram.params.messages import (
    SELECT_ACTION,
    WELCOME_ON_START)

on_start_router = Router(name=__name__)
on_start_router.message.filter(ChatTypesFilter(["private"]))


@on_start_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.update_data(handlers_stack=None)
    data = message.from_user.dict()

    await message.answer(text=f'{WELCOME_ON_START}',
                         reply_markup=get_pvt_main_menu_reply_kbd())

    create_user_on_start(data=data, master=False)


@on_start_router.message(Command(COMMANDS_PARAMS.MENU_CMD.TEXT))
async def menu_command(message: Message):
    await message.answer(text=SELECT_ACTION,
                         reply_markup=get_pvt_main_menu_reply_kbd())
