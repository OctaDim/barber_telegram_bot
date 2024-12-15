import inspect

from aiogram import Router, F
from aiogram.types import Message

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.buttons_common import (
    SPECIAL_CHARACTERS)
from telegram.params.messages import (
    SELECT_ACTION)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)

reply_no_action_common_router = Router(name=__name__)
reply_no_action_common_router.message.filter(ChatTypesFilter(["private"]))


@reply_no_action_common_router.message(F.text == SPECIAL_CHARACTERS.NO_ACTION_SYMBOL_REPLY)
async def no_action_common_reply_handler(message: Message):
    await message.delete()

    await message.answer(text=SELECT_ACTION,
                         reply_markup=get_pvt_main_menu_reply_kbd())

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
