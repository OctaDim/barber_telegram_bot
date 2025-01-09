import asyncio
import inspect
from time import sleep

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.config.configs import PAUSE_CONFIGS
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.params.messages import UNKNOWN_COMMAND_ENTERED
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import send_warning_message_with_delete_delay, \
    re_open_reply_keyboard_message
from utilities.numeric_utils import number_or_str_to_float

unhandled_update_router = Router(name=__name__)
unhandled_update_router.message.filter(ChatTypesFilter(["private"]))


@unhandled_update_router.message()
async def unhandled_update_handler_pvt(message: Message, state: FSMContext):
    state_data = await state.get_data()

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    await send_warning_message_with_delete_delay(
        message_text=UNKNOWN_COMMAND_ENTERED,
        delete_delay_seconds=PAUSE_CONFIGS.WARNING_MESSAGE_DELAY,
        message=message)

    prior_reply_kbd_markup = state_data.get("prior_reply_kbd_markup_obj_state")
    prior_reply_kbd_text = state_data.get("prior_reply_kbd_text_state")
    prior_reply_kbd_img_path = state_data.get("prior_reply_kbd_img_path_state")
    prior_reply_kbd_img_text = state_data.get("prior_reply_kbd_img_text_state")

    await re_open_reply_keyboard_message(
        telegram_update_obj=message,
        fsm_state=state,
        re_open_reply_keyboard=prior_reply_kbd_markup,
        re_open_reply_msg_text=prior_reply_kbd_text,
        image_path=prior_reply_kbd_img_path,
        image_caption_text=prior_reply_kbd_img_text,
        reply_kbd_opened_state_after_open=True,
        open_reply_kbd_msg_anyway=True)

    # await message.reply(text=UNKNOWN_COMMAND_ENTERED)
    #
    # delay_seconds = number_or_str_to_float(PAUSE_CONFIGS.INFO_MESSAGE_DELAY)
    # if delay_seconds:
    #     await asyncio.sleep(delay_seconds)
    #
    # handlers_list = await get_valid_list_by_fsm_state_key(
    #     fsm_state_or_state_dict=state,
    #     fsm_state_literal_key="handlers_stack")
    #
    # await execute_last_stack_handler(handlers_list=handlers_list)
    #
    # print("\tTEST INFO: Unhandled_update_handler. "
    #       "Handler answer = skip_add_handler_stack")
    # print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

    # await state.update_data()

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
