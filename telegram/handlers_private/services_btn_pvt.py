from aiogram import Router, F
from aiogram.types import Message


from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS_PARAMS
from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd
from telegram.params.messages import NO_SERVICES

from database.db_queries.user_queries import get_services_list
from telegram.telegram_utils.messages_helpers import get_service_detailed_info

services_btn_router = Router(name=__name__)
services_btn_router.message.filter(ChatTypesFilter(["private"]))


@services_btn_router.message(F.text == MAIN_MENU_BUTTONS_PARAMS.OUR_SERVICES)
async def get_services(message: Message):
    data = get_services_list()

    if data:
        for service in data:
            await message.answer(
                text=f"{get_service_detailed_info(service)}",
                reply_markup=get_pvt_main_menu_kbd())
        return

    await message.answer(text=NO_SERVICES, reply_markup=get_pvt_main_menu_kbd())
