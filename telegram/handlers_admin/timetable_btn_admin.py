from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State

from telegram.filters.chat_types_filter import IsAdmin
from telegram.keyboard_inline.timetable_get_month_inl_kbd import timetable_get_month_inl_kbd
from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS
from telegram.params.timetable_cb_data_message import SELECT_A_MONTH

timetable_admin_btn_router = Router(name=__name__)
timetable_admin_btn_router.message.filter(IsAdmin())


class Timetable(StatesGroup):
    pass


@timetable_admin_btn_router.message(F.text == MAIN_MANU_ADMIN_PARAMS.TIMETABLE)
async def get_inl_kbd_add_work_time(message: Message):
    await message.answer(
        text=SELECT_A_MONTH,
        reply_markup=timetable_get_month_inl_kbd(month=message.date.month, year=message.date.year),
        parse_mode=ParseMode.MARKDOWN
    )
