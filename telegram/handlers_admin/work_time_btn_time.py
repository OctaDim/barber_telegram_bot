from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import code

from telegram.filters.chat_types_filter import IsAdmin
from telegram.keyboard_inline.work_time_add_month_inl_kbd import work_time_month_inl_kbd
from telegram.keyboard_reply.admin_work_time_actions_kbd import get_work_time_action_kbd
from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS
from telegram.params.button_work_time_actions import BUTTON_WORK_TIME_ACTIONS


work_time_admin_btn_router = Router(name=__name__)
work_time_admin_btn_router.message.filter(IsAdmin())


class WorkTimes(StatesGroup):
    month = State()
    days = State()
    time_duration_service = State()
    time_start = State()
    time_end = State()
    delta = State()
    block_hours = State()
    block_minutes = State()


@work_time_admin_btn_router.message(F.text == MAIN_MANU_ADMIN_PARAMS.WORK_TIME)
async def get_work_time_actions(message: Message):
    await message.answer(text='Выберите действие:', reply_markup=get_work_time_action_kbd())


@work_time_admin_btn_router.message(F.text == BUTTON_WORK_TIME_ACTIONS.ADD)
async def get_inl_kbd_add_work_time(message: Message):
    await message.answer(
        text=code('команда'),
        reply_markup=work_time_month_inl_kbd(date=message.date.date()),
        parse_mode=ParseMode.MARKDOWN
    )

