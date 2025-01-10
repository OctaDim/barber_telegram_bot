from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.category_remove_by_id import remove_category_by_id
from telegram.handlers_admin.categories_btn_admin import change_category
from telegram.keyboard_inline.admin_categories_get_categories_for_cahnge_inl_kbd import AdminCategoryForChangeCbData
from telegram.keyboard_inline.admin_category_get_category_for_remove_inl_kbd import AdminCategoryForRemoveCbData
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.params.button_admin_panel_or_main_menu import ButtonAdminPanelOrMainMenu
from telegram.params.timetable_cb_data_message import SUCCESSFULLY

admin_change_category_cb_router = Router(name=__name__)


@admin_change_category_cb_router.callback_query(AdminCategoryForChangeCbData.filter())
async def select_category_for_change(
        callback_query: CallbackQuery,
        callback_data: AdminCategoryForChangeCbData,
        state: FSMContext,
        bot: Bot
):
    category_id = callback_data.category_id

    state_data = await state.get_data()
    messages_id = state_data.get('messages_id')

    await bot.delete_messages(
        chat_id=callback_query.message.chat.id,
        message_ids=messages_id)

    await change_category(message=callback_query.message, state=state)

    await state.update_data(category_id=category_id)


@admin_change_category_cb_router.callback_query(AdminCategoryForRemoveCbData.filter())
async def remove_select_category(
        callback_query: CallbackQuery,
        callback_data: AdminCategoryForRemoveCbData,
        state: FSMContext,
        bot: Bot
):
    category_id = callback_data.category_id

    state_data = await state.get_data()
    messages_id = state_data.get('messages_id')

    await bot.delete_messages(
        chat_id=callback_query.message.chat.id,
        message_ids=messages_id)

    await state.update_data(category_id=category_id)

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=SUCCESSFULLY,
        reply_markup=get_admin_main_menu_kbd()
    )

    remove_category_by_id(category_id=category_id)

    await state.clear()
