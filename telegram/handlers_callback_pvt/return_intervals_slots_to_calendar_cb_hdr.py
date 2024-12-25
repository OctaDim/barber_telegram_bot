import inspect

from aiogram import Router, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.handler_helpers.return_intervals_slots_to_calendar_inl_rep import \
    delete_intervals_slots_msgs_before_calendar
from telegram.handlers_private.return_btn_reply_hdr_pvt import (
    return_button_reply_hdr_pvt)
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    ReturnIntervalsSlotsToCalendarCBData)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

return_interval_slots_to_calendar_cb_router = Router(name=__name__)
return_interval_slots_to_calendar_cb_router.message.filter(ChatTypesFilter(["private"]))


@return_interval_slots_to_calendar_cb_router.callback_query(ReturnIntervalsSlotsToCalendarCBData.filter())
async def return_intervals_slots_to_calendar_inl_hdr(callback_query: CallbackQuery,
                                                     callback_data: CallbackData,
                                                     state: FSMContext,
                                                     bot: Bot):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    # ##################################################################
    # Delete intervals slots msgs on return button to calendar handler
    # ##################################################################
    await delete_intervals_slots_msgs_before_calendar(
        callback_query=callback_query, state=state, bot=bot)
    # ##################################################################

    message = callback_query.message

    # Call the same functionality handler of the reply keyboard button
    await return_button_reply_hdr_pvt(message=message,
                                      state=state,
                                      bot=bot,
                                      callback_data=callback_data)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
