from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import code

from telegram.filters.chat_types_filter import IsAdmin
from telegram.keyboard_inline.work_time_add_month_inl_kbd import work_time_month_inl_kbd
from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS
from telegram.params.work_time_cb_data_message import SELECT_A_MONTH

work_time_admin_btn_router = Router(name=__name__)
work_time_admin_btn_router.message.filter(IsAdmin())


class WorkTimes(StatesGroup):
    year = State()
    month = State()
    days = State()
    interval = State()
    time_start = State()
    time_end = State()


@work_time_admin_btn_router.message(F.text == MAIN_MANU_ADMIN_PARAMS.WORK_TIME)
async def get_inl_kbd_add_work_time(message: Message):
    await message.answer(
        text=SELECT_A_MONTH,
        reply_markup=work_time_month_inl_kbd(month=message.date.month, year=message.date.year),
        parse_mode=ParseMode.MARKDOWN
    )

