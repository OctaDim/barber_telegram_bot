from aiogram import Router, F
from aiogram.types import Message

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd
from telegram.keyboard_inline.enroll_services_inl_kbd import get_enroll_services_inl_kbd
from telegram.keyboard_reply.pvt_return_main_menu_kbd import get_pvt_return_main_menu_kbd

from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS_PARAMS
from telegram.params.messages_multiline import SELECT_SERVICES_MULTI
from telegram.params.messages import (NO_SERVICES,
                                      SELECT_OTHER_ACTIONS)

from database.db_queries.user_queries import get_services_list


enroll_services_pvt_router = Router(name=__name__)
enroll_services_pvt_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_pvt_router.message(
    F.text == MAIN_MENU_BUTTONS_PARAMS.ENROLL_SERVICES)
async def enroll_services_btn_handler(message: Message):
    all_services_records = get_services_list()

    if not all_services_records:
        await message.answer(
            text=NO_SERVICES,
            reply_markup=get_pvt_main_menu_kbd())
        return

    await message.answer(
        text=SELECT_SERVICES_MULTI,
        reply_markup=get_enroll_services_inl_kbd(all_services_records))

    await message.answer(
        text=SELECT_OTHER_ACTIONS,
        reply_markup=get_pvt_return_main_menu_kbd())
