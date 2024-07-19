from aiogram import Router

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.keyboard_inline.common_buttons_inline import NoActionEmptyCBData
from telegram.keyboard_inline.calendar_inl_kbd import (
    MonthNameCBData,
    YearNameCBData)

from telegram.telegram_utils.handlers_stack_utils import get_handler_answer_flag_dict
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    cannot_modify_obsolete_inl_kbd)


no_action_common_cb_router = Router(name=__name__)
no_action_common_cb_router.message.filter(ChatTypesFilter(["private"]))


@no_action_common_cb_router.callback_query(NoActionEmptyCBData.filter())
@no_action_common_cb_router.callback_query(MonthNameCBData.filter())
@no_action_common_cb_router.callback_query(YearNameCBData.filter())
async def no_action_common_callback_hdr(callback_query: CallbackQuery,
                                        state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        await cannot_modify_obsolete_inl_kbd(callback_query)

    else:
        await callback_query.answer()

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
