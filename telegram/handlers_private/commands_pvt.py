import inspect

from aiogram import Router
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.db_queries.create_user_on_start_query import (
    create_user_on_start)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.commands import (
    COMMANDS_PARAMS)
from telegram.params.images_params import (
    IMAGES_LINKS)
from telegram.params.messages import (
    SELECT_MAIN_MENU)
from telegram.params.messages_multiline import (
    MAIN_GREETING_RICH_TXT)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    re_open_reply_keyboard_message,
    re_open_photo_reply_message)

on_start_router = Router(name=__name__)
on_start_router.message.filter(ChatTypesFilter(["private"]))


@on_start_router.message(CommandStart())
async def start_command(message: Message,
                        state: FSMContext):
    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    await state.clear()
    handlers_list = []
    await state.update_data(handlers_stack=handlers_list)
    print(f"\tFSM state cleared. Handler stack is empty list []: "
          f"\tlen(handlers_list): {len(handlers_list)}\n")

    cur_handler_messages_ids = []

    # Comment if main greetings msg with reply keyboard at once
    cur_message = await re_open_photo_reply_message(
        telegram_update_obj=message,
        image_path=IMAGES_LINKS.MAIN_GREETING_IMG,
        image_caption_text=MAIN_GREETING_RICH_TXT,
        keyboard=None)
    if not cur_message:
        await message.answer(text=MAIN_GREETING_RICH_TXT)

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=message,
        re_open_reply_msg_text=SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        # Set reply_kbd_opened_state_after_open=True
        # if main greetings message with reply keyboard at once
        reply_kbd_opened_state_after_open=False)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    # await state.update_data()

    data = message.from_user.dict()
    create_user_on_start(data=data, master=False)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)


@on_start_router.message(Command(COMMANDS_PARAMS.MENU_CMD.TEXT))
async def menu_command(message: Message,
                       state: FSMContext):
    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    await state.clear()
    handlers_list = []
    await state.update_data(handlers_stack=handlers_list)
    print(f"\tFSM state cleared. Handler stack is empty list []: "
          f"\tlen(handlers_list): {len(handlers_list)}\n")

    cur_handler_messages_ids = []

    # Comment if main greetings msg with reply keyboard at once
    cur_message = await re_open_photo_reply_message(
        telegram_update_obj=message,
        image_path=IMAGES_LINKS.MAIN_GREETING_IMG,
        image_caption_text=MAIN_GREETING_RICH_TXT,
        keyboard=None)
    if not cur_message:
        await message.answer(text=MAIN_GREETING_RICH_TXT)

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=message,
        re_open_reply_msg_text=SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        # Set reply_kbd_opened_state_after_open=True
        # if main greetings message with reply keyboard at once
        reply_kbd_opened_state_after_open=False)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    # await state.update_data()

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
