from aiogram import Router
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_inline.enroll_services_inl_kbd import EnrollServicesCallbackData
from telegram.keyboard_reply.pvt_enroll_service_actions_kbd import get_enroll_service_actions_reply_kbd
from telegram.params.messages_helpers import get_service_detailed_info
from telegram.telegram_utils.delete_messages import delete_inline_msg_and_next_msgs

from database.db_queries.service_by_id_query import get_service_by_id

enroll_services_cb_router = Router(name=__name__)
enroll_services_cb_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_cb_router.callback_query(EnrollServicesCallbackData.filter())
async def select_services_callback_hdr(callback_query: CallbackQuery,
                                       callback_data: EnrollServicesCallbackData):
    # await delete_inline_msg_and_next_msgs(callback_query=callback_query,
    #                                       messages_number_to_delete=1)

    service_record_id = get_service_by_id(callback_data.service_id)
    service_detailed_info = get_service_detailed_info(service_record_id)

    await callback_query.message.answer(
        text=service_detailed_info,
        reply_markup=get_enroll_service_actions_reply_kbd())
