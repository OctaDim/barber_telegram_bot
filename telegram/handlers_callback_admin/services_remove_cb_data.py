from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.keyboard_inline.services_change_select_inl_kbd import RemoveServicesCbData
from telegram.params.messages import SUCCESSFULLY
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd

from database.db_queries.admin_queries import services_remove


services_remove_cb_query = Router(name=__name__)


@services_remove_cb_query.callback_query(RemoveServicesCbData.filter())
async def remove_service(
        callback_query: CallbackQuery,
        callback_data: RemoveServicesCbData,
        bot: Bot,
        state: FSMContext):

    services_remove(id_service=callback_data.id_services)

    state_data = await state.get_data()
    messages_id = state_data.get('messages_id')

    await bot.delete_messages(chat_id=callback_query.message.chat.id, message_ids=messages_id)

    await callback_query.message.answer(text=SUCCESSFULLY, reply_markup=get_admin_main_menu_kbd())

    return
