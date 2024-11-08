from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.handlers_private.return_btn_reply_hdr_pvt import return_button_reply_hdr_pvt
from telegram.keyboard_inline.common_buttons_inline import ReturnInlineBtnCBData
from telegram.telegram_utils.handlers_stack_utils import get_handler_answer_flag_dict
from telegram.telegram_utils.messages_utils import inline_keyboard_is_actual

return_common_cb_router = Router(name=__name__)
return_common_cb_router.message.filter(ChatTypesFilter(["private"]))


@return_common_cb_router.callback_query(ReturnInlineBtnCBData.filter())
async def inline_return_common_cb_hdr(callback_query: CallbackQuery,
                                      state: FSMContext,
                                      current_handler_data: dict):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    await callback_query.answer()

    message = callback_query.message

    # Call the same functionality handler of the reply keyboard button
    await return_button_reply_hdr_pvt(message=message,
                                      state=state,
                                      current_handler_data=current_handler_data)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True,
                                        upd_actual_msg_min_id=True)
