from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.keyboard_inline.services_change_select_inl_kbd import ChangeServicesCbData
from telegram.handlers_admin.services_btn_admin import preview_service

from database.db_queries.admin_queries import get_one_service, services_remove
from telegram.params.messages import SUCCESSFULLY

services_change_cb_query = Router(name=__name__)


@services_change_cb_query.callback_query(ChangeServicesCbData.filter())
async def get_service(callback_query: CallbackQuery, callback_data: ChangeServicesCbData, state: FSMContext):
    service = get_one_service(id_service=callback_data.id_services)

    data = {
        'name': service.name,
        'description': service.description,
        'price': service.price,
        'id': service.id
    }

    await preview_service(message=callback_query.message, cb_data=data, state=state)
