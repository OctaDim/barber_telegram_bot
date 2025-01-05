from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command

from database.db_queries.create_user_on_start_query import create_user_on_start
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.filters.chat_types_filter import IsAdmin
from telegram.params.commands import COMMANDS_PARAMS
from telegram.params.register_user import WRITE_NAME

admin_panel = Router()
admin_panel.message.filter(IsAdmin())


class AdminPanelState(StatesGroup):
    first_name_new_user = State()


@admin_panel.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()

    data = message.from_user.dict()

    result = create_user_on_start(data=data, master=True)
    if result:
        await message.answer(text=f'Добро пожаловать!',
                             reply_markup=get_admin_main_menu_kbd())

        return

    await register_first_name_master(message=message, state=state)


@admin_panel.message(Command(COMMANDS_PARAMS.ADMIN_PANEL.TEXT))
async def start_command(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(text=f'Добро пожаловать!',
                         reply_markup=get_admin_main_menu_kbd())


async def register_first_name_master(message: Message, state: FSMContext):
    await message.answer(text=WRITE_NAME)

    await state.set_state(AdminPanelState.first_name_new_user)


@admin_panel.message(StateFilter(AdminPanelState.first_name_new_user))
async def create_master_on_start(message: Message):
    data = message.from_user.dict()
    data['first_name'] = message.text

    await message.answer(text=f'Добро пожаловать!',
                         reply_markup=get_admin_main_menu_kbd())

    create_user_on_start(data=data, master=True)
