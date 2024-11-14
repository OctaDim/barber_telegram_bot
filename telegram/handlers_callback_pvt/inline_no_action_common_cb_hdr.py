from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.calendar_enroll_srcs_inl_kbd import (
    MonthNameCBData,
    YearNameCBData)
from telegram.keyboard_inline.categories_enroll_srcs_inl_kbd import (
    CategoryPageNumberCBData)
from telegram.keyboard_inline.common_buttons_inline import (
    NoActionEmptyCBData)
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    SlotPageNumberCBData)
from telegram.keyboard_inline.masters_enroll_srcs_inl_kbd import (
    MasterPageNumberCBData)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

no_action_common_cb_router = Router(name=__name__)
no_action_common_cb_router.message.filter(ChatTypesFilter(["private"]))


@no_action_common_cb_router.callback_query(NoActionEmptyCBData.filter())
@no_action_common_cb_router.callback_query(MonthNameCBData.filter())
@no_action_common_cb_router.callback_query(YearNameCBData.filter())
@no_action_common_cb_router.callback_query(CategoryPageNumberCBData.filter())
@no_action_common_cb_router.callback_query(MasterPageNumberCBData.filter())
@no_action_common_cb_router.callback_query(SlotPageNumberCBData.filter())
async def inline_no_action_common_cb_hdr(callback_query: CallbackQuery,
                                         state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    await callback_query.answer()

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
