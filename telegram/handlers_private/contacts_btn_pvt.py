from aiogram import Router, F
from aiogram.types import Message

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd

from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS_PARAMS
from telegram.params.messages import NO_CONTACTS
from telegram.config.configs import CONTACTS_CONFIGS, LANGUAGE_CONFIGS

from database.db_queries.contacts_queries import get_company_contacts

from telegram.telegram_utils.handlers_stack_utils import get_handler_answer_flag_dict
from telegram.telegram_utils.messages_helpers import get_contacts_text

contacts_btn_router = Router(name=__name__)
contacts_btn_router.message.filter(ChatTypesFilter(["private"]))


@contacts_btn_router.message(F.text == MAIN_MENU_BUTTONS_PARAMS.CONTACTS)
async def get_contacts(message: Message):
    contacts_data = get_company_contacts()

    if not contacts_data:
        await message.answer(text=NO_CONTACTS,
                             reply_markup=get_pvt_main_menu_kbd())

        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    contacts_text = get_contacts_text(
        **contacts_data,
        phones_international=CONTACTS_CONFIGS.PHONES_INTERNATIONAL)

    await message.answer(
        text=contacts_text,
        disable_web_page_preview=CONTACTS_CONFIGS.DISABLE_PREVIEW,
        reply_markup=get_pvt_main_menu_kbd())

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
