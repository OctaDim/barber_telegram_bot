from aiogram import Router
from aiogram.types import CallbackQuery

from telegram.keyboard_inline.services_change_select_inl_kbd import RemoveServicesCbData
from telegram.params.messages import SUCCESSFULLY

from database.db_queries.admin_queries import services_remove


services_remove_cb_query = Router(name=__name__)


@services_remove_cb_query.callback_query(RemoveServicesCbData.filter())
async def remove_service(callback_query: CallbackQuery, callback_data: RemoveServicesCbData):
    services_remove(id_service=callback_data.id_services)

    await callback_query.message.edit_text(text=SUCCESSFULLY)

    return
