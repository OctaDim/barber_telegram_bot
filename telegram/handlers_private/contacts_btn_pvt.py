from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message


from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS_PARAMS
from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd
from telegram.params.messages import NO_CONTACTS

from database.db_queries.user_queries import get_about_info_company


contacts_btn_router = Router(name=__name__)
contacts_btn_router.message.filter(ChatTypesFilter(["private"]))


@contacts_btn_router.message(F.text == MAIN_MENU_BUTTONS_PARAMS.CONTACTS)
async def get_contacts(message: Message):
    data = get_about_info_company()

    if data:
        await message.answer(text='📱 Socials:\n'
                                  f'{", ".join(data.get("socials"))}\n'
                                  '📞 Telephone:\n'
                                  f'{", ".join(data.get("phone"))}\n\n'
                                  f'📍 Address: \n'
                                  f'{", ".join(data.get("address"))}',
                             parse_mode=ParseMode.HTML,
                             disable_web_page_preview=True,
                             reply_markup=get_pvt_main_menu_kbd()
                             )

        return

    await message.answer(text=NO_CONTACTS, reply_markup=get_pvt_main_menu_kbd())
