from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command

from aiogram.fsm.context import FSMContext

from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd
from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.params.commands import COMMANDS_PARAMS
from telegram.params.messages_multiline import MAIN_GREETING_MULTI


on_start_router = Router(name=__name__)
on_start_router.message.filter(ChatTypesFilter(["private"]))


@on_start_router.message(CommandStart())
async def start_command(state: FSMContext):
    await state.update_data(handlers_stack=None)


@on_start_router.message(Command(COMMANDS_PARAMS.MENU_CMD.TEXT))
async def menu_command(message: Message):
    await message.answer(text=MAIN_GREETING_MULTI,
                         reply_markup=get_pvt_main_menu_kbd())
