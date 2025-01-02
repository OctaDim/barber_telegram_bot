from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.address_create_obj_query import create_address_db_obj
from database.db_queries.address_remove import remove_address_obj
from telegram.handlers_admin.contacts_admin_address_btn_admin import add_address
from telegram.keyboard_inline.contacts_for_master_get_action_by_address import AddNewAddressCbData, RemoveAddressCbData
from telegram.keyboard_inline.contacts_for_master_preview_address import ConfirmPreviewAddressCbData, \
    ChangePreviewAddressCbData
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.params.button_admin_panel_or_main_menu import ButtonAdminPanelOrMainMenu
from telegram.params.messages import SUCCESSFULLY

contacts_for_master_address_master_cb_query = Router(name=__name__)


@contacts_for_master_address_master_cb_query.callback_query(AddNewAddressCbData.filter())
async def select_add_new_address(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    await add_address(
        message=callback_query.message,
        state=state,
        bot=bot
    )


@contacts_for_master_address_master_cb_query.callback_query(ConfirmPreviewAddressCbData.filter())
async def confirm_address(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    url = state_data.get('address_url')
    street = state_data.get('address')

    await callback_query.answer(text=SUCCESSFULLY, show_alert=True)

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

    create_address_db_obj(street=street, url=url)


@contacts_for_master_address_master_cb_query.callback_query(ChangePreviewAddressCbData.filter())
async def change_address(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    await add_address(
        message=callback_query.message,
        state=state,
        bot=bot
    )


@contacts_for_master_address_master_cb_query.callback_query(RemoveAddressCbData.filter())
async def remove_address(
        callback_query: CallbackQuery,
        bot: Bot
):
    await callback_query.answer(text=SUCCESSFULLY, show_alert=True)

    await bot.delete_message(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id
    )

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=ButtonAdminPanelOrMainMenu.ADMIN_PANEL,
        reply_markup=get_admin_main_menu_kbd()
    )

    remove_address_obj()
