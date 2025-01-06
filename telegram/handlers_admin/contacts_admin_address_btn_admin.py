from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from telegram.filters.chat_types_filter import IsAdmin
from telegram.keyboard_inline.contacts_for_master_preview_address import preview_address_inl_kbd
from telegram.params.button_contacts_for_master_address import PreviewAddress
from telegram.params.contacts_for_master_cb_data_message import ENTER_ADDRESS

contacts_admin_address_btn_router = Router(name=__name__)
contacts_admin_address_btn_router.message.filter(IsAdmin())


class ContactsAdminAddress(StatesGroup):
    address = State()
    address_url = State()


async def add_address(
        message: Message,
        state: FSMContext,
        bot: Bot
):
    await bot.edit_message_text(
        message_id=message.message_id,
        chat_id=message.chat.id,
        text=ENTER_ADDRESS
    )

    await state.set_state(ContactsAdminAddress.address)


@contacts_admin_address_btn_router.message(StateFilter(ContactsAdminAddress.address))
async def preview_address(
        message: Message,
        state: FSMContext
):
    url, preview_text = PreviewAddress(address=message.text).generate_preview()

    await message.answer(
        text=preview_text,
        reply_markup=preview_address_inl_kbd(),
        parse_mode='HTML',
        disable_web_page_preview=True
    )

    await state.update_data(address=message.text, address_url=url)
