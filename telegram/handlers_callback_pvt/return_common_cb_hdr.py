from aiogram import Router

from aiogram.fsm.context import FSMContext


from aiogram.filters.callback_data import CallbackData

from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.handlers_private.return_btn_pvt_hdr import return_button_handler

from telegram.keyboard_inline.common_cb_data_all_inl_kbds import ReturnInlineBtnCBData


return_common_cb_router = Router(name=__name__)
return_common_cb_router.message.filter(ChatTypesFilter(["private"]))


@return_common_cb_router.callback_query(ReturnInlineBtnCBData.filter())
async def return_common_callback_hdr(callback_query: CallbackQuery,
                                     state: FSMContext,
                                     current_handler_data: dict):
    await callback_query.answer()
    message = callback_query.message

    # Call the same functionality handler of the reply keyboard button
    await return_button_handler(message=message,
                                state=state,
                                current_handler_data=current_handler_data)
