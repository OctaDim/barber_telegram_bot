import re

from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State

from aiogram.filters import StateFilter

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import IsAdmin
from telegram.keyboard_inline.contacts_for_master_inl_kbd import contacts_by_admin_inl_kbd
from telegram.keyboard_inline.contacts_for_master_preview_social_network_inl_kbd import preview_social_network_inl_kbd
from telegram.params.button_social_networks import PreviewSocialNetwork

from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS
from telegram.params.contacts_for_master_cb_data_message import ADD_USERNAME, ENTER_ADDITIONAL_SOCIAL_NETWORK
from telegram.params.messages import SELECT_ACTION

contacts_admin_social_network_btn_router = Router(name=__name__)
contacts_admin_social_network_btn_router.message.filter(IsAdmin())


class ContactsAdminSocialNetwork(StatesGroup):
    social_network = State()
    username_social_network = State()
    url_social_network = State()
    social_network_id = State()


@contacts_admin_social_network_btn_router.message(F.text == MAIN_MANU_ADMIN_PARAMS.CONTACTS)
async def get_contacts_by_admin(message: Message):
    await message.answer(text=SELECT_ACTION, reply_markup=contacts_by_admin_inl_kbd())


@contacts_admin_social_network_btn_router.message(StateFilter(ContactsAdminSocialNetwork.social_network))
async def add_username_social_network(
        message: Message,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    if state_data.get('social_network') is None:
        await state.update_data(social_network=message.text)

        await message.answer(text=ADD_USERNAME)

        await state.set_state(ContactsAdminSocialNetwork.username_social_network)

        return
    elif state_data.get('social_network_id') and state_data.get('username_social_network'):
        preview_text = PreviewSocialNetwork(social_network=message.text,
                                            username=state_data.get(
                                                'username_social_network')
                                            ).generate_preview()

        await message.answer(
            text=preview_text,
            reply_markup=preview_social_network_inl_kbd()
        )

        await state.update_data(social_network=message.text)

        return

    await bot.edit_message_text(
        message_id=message.message_id,
        chat_id=message.chat.id,
        text=ADD_USERNAME
    )

    await state.set_state(ContactsAdminSocialNetwork.username_social_network)


async def add_other_social_network(
        message: Message,
        state: FSMContext,
        bot: Bot
):
    await bot.edit_message_text(
        message_id=message.message_id,
        chat_id=message.chat.id,
        text=ENTER_ADDITIONAL_SOCIAL_NETWORK
    )

    await state.set_state(ContactsAdminSocialNetwork.social_network)


@contacts_admin_social_network_btn_router.message(StateFilter(ContactsAdminSocialNetwork.username_social_network))
async def preview_social_network(
        message: Message,
        state: FSMContext
):
    username = message.text.lower()

    username = re.sub(r'\s|@', '', username)

    await state.update_data(username_social_network=username)

    state_data = await state.get_data()

    preview_text = PreviewSocialNetwork(social_network=state_data.get('social_network'),
                                        username=state_data.get('username_social_network')).generate_preview()

    await message.answer(
        text=preview_text,
        reply_markup=preview_social_network_inl_kbd()
    )

    await state.set_state(None)
