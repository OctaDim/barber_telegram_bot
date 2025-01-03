import json

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.create_social_network import create_social_network
from database.db_queries.get_all_social_networks_by_masters import get_all_social_networks_by_masters
from database.db_queries.social_network_by_id_query import get_social_network_by_id
from database.db_queries.social_network_delete_obj_by_id_query import delete_social_network_by_id
from database.db_queries.social_network_update_data_query import social_network_update_data

from telegram.handlers_admin.contacts_admin_social_network_btn_admin import add_username_social_network, add_other_social_network

from telegram.keyboard_inline.contacts_for_master_choose_social_network_inl_kbd import choose_social_network_inl_kbd, \
    NameSocialNetworkCbData, OtherSocialNetworkCbData
from telegram.keyboard_inline.contacts_for_master_get_action_by_address import get_action_by_address, \
    ReturnToContactsCbData
from telegram.keyboard_inline.contacts_for_master_get_action_by_social_network import get_action_by_social_networks, \
    AddNewSocialNetworkCbData, ChangeSocialNetworkCbData, RemoveSocialNetworkCbData
from telegram.keyboard_inline.contacts_for_master_get_all_social_networks_for_changes import \
    get_all_social_networks_for_changes_inl_kbd, SocialNetworkForChangesCbData
from telegram.keyboard_inline.contacts_for_master_get_all_social_networks_for_delete import \
    get_all_social_networks_for_delete_inl_kbd, SocialNetworkForDeleteCbData
from telegram.keyboard_inline.contacts_for_master_inl_kbd import ContactAdminCbData, contacts_by_admin_inl_kbd
from telegram.keyboard_inline.contacts_for_master_preview_social_network_inl_kbd import \
    ConfirmPreviewSocialNetworkCbData, ChangePreviewSocialNetworkCbData, preview_social_network_inl_kbd
from telegram.keyboard_inline.contacts_for_master_select_change_inl_kbd import \
    change_obtained_social_network_data_inl_kbd, ChangeObtainedSocialNetworkCbData, ChangeObtainedUsernameCbData

from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd

from telegram.params.button_admin_panel_or_main_menu import ButtonAdminPanelOrMainMenu
from telegram.params.button_social_networks import PreviewSocialNetwork
from telegram.params.buttons_contacts_by_master import CONTACTS_BY_MASTER_PARAMS
from telegram.params.contacts_for_master_cb_data_message import choose_a_social_network, select_change
from telegram.params.messages import SELECT_ACTION, SUCCESSFULLY

contacts_for_master_social_network_master_cb_query = Router(name=__name__)


@contacts_for_master_social_network_master_cb_query.callback_query(ContactAdminCbData.filter())
async def get_action_by_selected_contact(
        callback_query: CallbackQuery,
        callback_data: ContactAdminCbData,
        bot: Bot
):
    cb_data = callback_data.contact

    if cb_data == CONTACTS_BY_MASTER_PARAMS.SOCIAL_NETWORKS:
        await bot.edit_message_text(
            message_id=callback_query.message.message_id,
            chat_id=callback_query.message.chat.id,
            text=SELECT_ACTION,
            reply_markup=get_action_by_social_networks()
        )

        return

    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=SELECT_ACTION,
        reply_markup=get_action_by_address()
    )


@contacts_for_master_social_network_master_cb_query.callback_query(AddNewSocialNetworkCbData.filter())
async def choose_social_network(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=choose_a_social_network,
        reply_markup=choose_social_network_inl_kbd()
    )


@contacts_for_master_social_network_master_cb_query.callback_query(NameSocialNetworkCbData.filter())
async def get_selected_social_network(
        callback_query: CallbackQuery,
        state: FSMContext,
        callback_data: NameSocialNetworkCbData,
        bot: Bot
):
    cb_data = callback_data.data

    name, url = json.loads(cb_data)

    state_data = await state.get_data()

    await state.update_data(social_network=name, url_social_network=url)

    username_social_network = state_data.get('username_social_network')

    if state_data.get('username_social_network'):
        preview_text = PreviewSocialNetwork(
            social_network=name,
            username=username_social_network).generate_preview()

        await bot.edit_message_text(
            message_id=callback_query.message.message_id,
            chat_id=callback_query.message.chat.id,
            text=preview_text,
            reply_markup=preview_social_network_inl_kbd()
        )

        return

    await add_username_social_network(
        message=callback_query.message,
        state=state,
        bot=bot
    )


@contacts_for_master_social_network_master_cb_query.callback_query(ConfirmPreviewSocialNetworkCbData.filter())
async def confirm_social_network(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    social_network = state_data.get('social_network')
    username_social_network = state_data.get('username_social_network')
    url_social_network = state_data.get('url_social_network')
    social_network_id = state_data.get('social_network_id')

    if social_network_id:
        social_network_update_data(
            social_network_id=social_network_id,
            social_network_url=url_social_network,
            social_network_name=social_network,
            social_network_username=username_social_network
        )
    else:
        create_social_network(
            url_social_network=url_social_network,
            username_social_network=username_social_network,
            social_network=social_network
        )

    await callback_query.answer(SUCCESSFULLY, show_alert=True)

    await bot.delete_message(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id
    )

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=ButtonAdminPanelOrMainMenu.ADMIN_PANEL,
        reply_markup=get_admin_main_menu_kbd()
    )

    await state.clear()


@contacts_for_master_social_network_master_cb_query.callback_query(ChangePreviewSocialNetworkCbData.filter())
async def change_obtained_social_network_data(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=select_change,
        reply_markup=change_obtained_social_network_data_inl_kbd()
    )


@contacts_for_master_social_network_master_cb_query.callback_query(ChangeObtainedSocialNetworkCbData.filter())
async def change_obtained_social_network(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=choose_a_social_network,
        reply_markup=choose_social_network_inl_kbd()
    )


@contacts_for_master_social_network_master_cb_query.callback_query(ChangeObtainedUsernameCbData.filter())
async def change_obtained_username_social_network(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    await state.update_data(username_social_network=None)

    await add_username_social_network(message=callback_query.message, state=state, bot=bot)


@contacts_for_master_social_network_master_cb_query.callback_query(OtherSocialNetworkCbData.filter())
async def select_other_social_network(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    await add_other_social_network(
        message=callback_query.message,
        state=state,
        bot=bot
    )


@contacts_for_master_social_network_master_cb_query.callback_query(ChangeSocialNetworkCbData.filter())
async def get_social_networks_for_changes(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    await bot.delete_message(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id
    )

    social_networks = get_all_social_networks_by_masters()

    messages_id = []
    for social_network in social_networks:
        preview_text = PreviewSocialNetwork(
            social_network=social_network.name,
            username=social_network.social_username
        ).generate_preview_for_changes()

        message = await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=preview_text,
            reply_markup=get_all_social_networks_for_changes_inl_kbd(
                social_network_id=social_network.id,
            ))

        messages_id.append(message.message_id)

    await state.update_data(messages_id=messages_id)


@contacts_for_master_social_network_master_cb_query.callback_query(SocialNetworkForChangesCbData.filter())
async def change_social_network(
        callback_query: CallbackQuery,
        callback_data: SocialNetworkForChangesCbData,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    social_network_id = callback_data.social_network_id

    social_network_obj = get_social_network_by_id(
        social_network_id=social_network_id
    )

    await bot.delete_messages(
        chat_id=callback_query.message.chat.id,
        message_ids=state_data.get('messages_id')
    )

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=select_change,
        reply_markup=change_obtained_social_network_data_inl_kbd()
    )

    await state.update_data(
        social_network_id=social_network_id,
        social_network=social_network_obj.name,
        url_social_network=social_network_obj.url,
        username_social_network=social_network_obj.social_username
    )


@contacts_for_master_social_network_master_cb_query.callback_query(RemoveSocialNetworkCbData.filter())
async def get_social_network_for_delete(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    await bot.delete_message(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id
    )

    social_networks = get_all_social_networks_by_masters()

    messages_id = []
    for social_network in social_networks:
        preview_text = PreviewSocialNetwork(
            social_network=social_network.name,
            username=social_network.social_username
        ).generate_preview_for_delete()

        message = await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=preview_text,
            reply_markup=get_all_social_networks_for_delete_inl_kbd(
                social_network_id=social_network.id,
            ))

        messages_id.append(message.message_id)

    await state.update_data(messages_id=messages_id)


@contacts_for_master_social_network_master_cb_query.callback_query(SocialNetworkForDeleteCbData.filter())
async def delete_social_network(
        callback_query: CallbackQuery,
        callback_data: SocialNetworkForDeleteCbData,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    social_network_id = callback_data.social_network_id

    delete_social_network_by_id(social_network_id=social_network_id)

    await bot.delete_messages(
        chat_id=callback_query.message.chat.id,
        message_ids=state_data.get('messages_id')
    )

    await callback_query.answer(SUCCESSFULLY, show_alert=True)

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=ButtonAdminPanelOrMainMenu.ADMIN_PANEL,
        reply_markup=get_admin_main_menu_kbd()
    )


@contacts_for_master_social_network_master_cb_query.callback_query(ReturnToContactsCbData.filter())
async def return_to_admin_contacts(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=SELECT_ACTION,
        reply_markup=contacts_by_admin_inl_kbd()
    )
