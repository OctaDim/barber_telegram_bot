from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.keyboard_inline.common_cb_data_all_inl_kbds import NoActionCommonCBData


no_action_common_cb_router = Router(name=__name__)
no_action_common_cb_router.message.filter(ChatTypesFilter(["private"]))


@no_action_common_cb_router.callback_query(NoActionCommonCBData.filter())
async def no_action_common_callback_hdr(callback_query: CallbackQuery):
    await callback_query.answer()
