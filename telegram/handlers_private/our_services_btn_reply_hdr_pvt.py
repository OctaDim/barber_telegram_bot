from aiogram import Router, F
from aiogram.types import Message

from database.db_queries.all_services_ordered_queries import (
    get_all_services_ordered)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.buttons_main_menu import (
    MAIN_MENU_BUTTONS_PARAMS)
from telegram.params.messages import (
    NO_SERVICES)
from telegram.telegram_utils.messages_helpers import (
    get_service_detailed_info)

services_btn_router = Router(name=__name__)
services_btn_router.message.filter(ChatTypesFilter(["private"]))


@services_btn_router.message(F.text == MAIN_MENU_BUTTONS_PARAMS.OUR_SERVICES)
async def our_services_btn_reply_hdr_pvt(message: Message):
    data = get_all_services_ordered(
        active=True,
        order_by_fields=("name", "price",))

    if data:
        for service in data:
            await message.answer(
                text=f"{get_service_detailed_info(service)}",
                reply_markup=get_pvt_main_menu_reply_kbd())
        return

    await message.answer(text=NO_SERVICES, reply_markup=get_pvt_main_menu_reply_kbd())
