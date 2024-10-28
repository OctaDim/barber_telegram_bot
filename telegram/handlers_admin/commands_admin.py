from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command

from database.db_queries.create_user_on_start_query import create_user_on_start
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.filters.chat_types_filter import IsAdmin
from telegram.params.commands import COMMANDS_PARAMS

admin_panel = Router()
admin_panel.message.filter(IsAdmin())


@admin_panel.message(CommandStart())
@admin_panel.message(Command(COMMANDS_PARAMS.ADMIN_PANEL.TEXT))
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    data = message.from_user.dict()

    await message.answer(text=f'Добро пожаловать!',
                         reply_markup=get_admin_main_menu_kbd())

    create_user_on_start(data=data, master=True)
