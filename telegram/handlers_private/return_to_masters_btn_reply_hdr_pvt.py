import inspect

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.handler_helpers.return_services_filtered_to_masters_rep_inl import (
    delete_services_filtered_msgs_before_masters)
from telegram.params.buttons_enroll_service import (
    ENROLL_SRCS_BUTTONS)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)

return_to_masters_button_router = Router(name=__name__)
return_to_masters_button_router.message.filter(ChatTypesFilter(["private"]))


@return_to_masters_button_router.message(F.text == ENROLL_SRCS_BUTTONS.RETURN_TO_MASTERS)
async def return_to_masters_on_reply_btn_hdr_pvt(message: Message,
                                                 state: FSMContext,
                                                 bot: Bot):
    state_data = await state.get_data()

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    # ##################################################################
    # Delete services filtered messages on return btn to masters handler
    # ##################################################################
    await delete_services_filtered_msgs_before_masters(
        message=message, state=state, bot=bot)
    # ##################################################################

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
