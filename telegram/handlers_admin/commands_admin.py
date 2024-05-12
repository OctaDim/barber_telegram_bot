from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command

from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.filters.chat_types_filter import IsAdmin
from telegram.params.commands import COMMANDS_PARAMS
from telegram.params.messages import MAIN_GREETING

admin_panel = Router()
admin_panel.message.filter(IsAdmin())


@admin_panel.message(CommandStart())
@admin_panel.message(Command(COMMANDS_PARAMS.ADMIN_PANEL.TEXT))
async def start_command(message: Message):
    await message.answer(text=f'{message.chat.id}',
                         reply_markup=get_admin_main_menu_kbd())
