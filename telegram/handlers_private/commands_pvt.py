from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command

from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.params.commands import COMMANDS_PARAMS
from telegram.params.messages import MAIN_GREETING


on_start_router = Router()
on_start_router.message.filter(ChatTypesFilter(["private"]))


@on_start_router.message(CommandStart())
@on_start_router.message(Command(COMMANDS_PARAMS.MENU_CMD.TEXT))
async def start_command(message: Message):
    await message.answer(text=MAIN_GREETING,
                         reply_markup=get_pvt_main_menu_kbd())
