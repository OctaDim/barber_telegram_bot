import asyncio
import inspect
import os
from typing import Union

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, Message, ReplyKeyboardMarkup,
                           FSInputFile)

from telegram.params.messages import (
    CANNOT_USE_OBSOLETE_MSG)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key,
    get_valid_state_data_from_fsm_state,
    get_valid_bool_by_fsm_state_key,
    get_valid_list_by_fsm_state_key)
from utilities.numeric_utils import (
    number_or_str_to_float)


async def inline_keyboard_is_actual(state: FSMContext | dict,
                                    callback_query: CallbackQuery) -> bool:
    async def message_inline_kbd_is_obsolete():
        await callback_query.answer(
            text=CANNOT_USE_OBSOLETE_MSG,
            show_alert=True)

    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from=state)

    # ##### Check inline keyboard is obsolete because server was restarted
    if not state_data and "actual_message_min_id" not in state_data:
        await message_inline_kbd_is_obsolete()
        return False

    # ##### Check inline keyboard is obsolete because new inl kbd was called
    minimal_actual_msg_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="actual_message_min_id")

    if callback_query.message.message_id < minimal_actual_msg_id:
        await message_inline_kbd_is_obsolete()
        return False

    return True


async def re_open_reply_keyboard_message(
        fsm_state: FSMContext,
        telegram_update_obj: Union[Message, CallbackQuery],
        re_open_reply_msg_text: str,
        re_open_reply_keyboard: ReplyKeyboardMarkup,
        reply_kbd_opened_state_after_open: bool = False,
        open_reply_kbd_msg_anyway: bool = False,
        image_path: str = None
) -> Message | None:
    print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

    reply_kbd_opened_state = await get_valid_bool_by_fsm_state_key(
        fsm_state_or_dict_from=fsm_state,
        fsm_state_literal_key="reply_keyboard_opened_state")

    if reply_kbd_opened_state and not open_reply_kbd_msg_anyway:
        print(f"\tNew Reply keyboard Message was not created, "
              f"\tbecause reply_kbd_opened_state = {reply_kbd_opened_state}\n")
        return

    prior_reply_message_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=fsm_state,
        fsm_state_literal_key="prior_reply_message_id_state")
    print(f"\tprior_reply_message_id_state = {prior_reply_message_id}\n")

    match telegram_update_obj:
        case CallbackQuery() as telegram_update_obj:
            telegram_message_obj = telegram_update_obj.message
        case Message() as telegram_update_obj:
            telegram_message_obj = telegram_update_obj
        case _:
            telegram_message_obj = None

    try:
        # Call new reply kbd till deleting prior reply to exclude opening text kbd
        if image_path:
            # image_path = os.path.join(BASE_DIR, image_path)
            image_path = os.path.normpath(image_path)
            img_path_exists_flag = os.path.exists(image_path)
            img_file_exists_flag = os.path.isfile(image_path)
        else:
            img_path_exists_flag, img_file_exists_flag = False, False

        if image_path and img_path_exists_flag and img_file_exists_flag:
            image_obj = FSInputFile(path=image_path)
            new_reply_message = await telegram_message_obj.answer_photo(
                photo=image_obj,
                # caption=re_open_reply_msg_text,
                reply_markup=re_open_reply_keyboard)
            new_reply_message_id = new_reply_message.message_id

            print(f"\tNew Reply keyboard Message (with photo) was created, "
                  f"\tbecause main_menu_opened_state = {reply_kbd_opened_state}\n"
                  f"\tnew_reply_message_id = {new_reply_message_id}\n"
                  f"\timage_path = {image_path}\n")
        else:
            new_reply_message = await telegram_message_obj.answer(
                text=re_open_reply_msg_text,
                reply_markup=re_open_reply_keyboard)
            new_reply_message_id = new_reply_message.message_id

            print(f"\tNew Reply keyboard Message (without photo) was created, "
                  f"\tbecause main_menu_opened_state = {reply_kbd_opened_state}\n"
                  f"\tnew_reply_message_id = {new_reply_message_id}\n"
                  f"\timage_path = {image_path}\n"
                  f"\timg_path_exists_flag = {img_path_exists_flag}\n"
                  f"\timg_file_exists_flag = {img_file_exists_flag}\n")

    except (TelegramBadRequest, Exception) as exception_info:
        print(f"\tNew Reply keyboard Message was not created: {exception_info}\n")
    else:
        try:
            # Deleting to remove repeated above reply keyboard text message
            cur_chat_id = telegram_message_obj.chat.id
            bot = telegram_message_obj.bot
            await bot.delete_message(message_id=prior_reply_message_id,
                                     chat_id=cur_chat_id)
            print(f"\tPrior Reply keyboard Message was deleted successfully\n")

        except (TelegramBadRequest, Exception) as exception_info:
            print(f"\tPrior Reply keyboard Message was not deleted: {exception_info}\n")

        await fsm_state.update_data(
            reply_keyboard_opened_state=reply_kbd_opened_state_after_open,
            prior_reply_message_id_state=new_reply_message_id)
        print(f"\tFSM state updated:\n"
              f"\treply_keyboard_opened_state = {reply_kbd_opened_state}\n"
              f"\tprior_reply_message_id_state = {new_reply_message_id}\n")

        return new_reply_message


async def send_warning_message_with_delete_delay(
        message_text: str,
        message: Message,
        delete_delay_seconds: Union[float, int, str] = 0
) -> list[int] | None:
    print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

    if not message_text.strip() or len(message_text.strip()) == 0:
        print(f"\tWarning message not displayed, because empty text\n"
              f"\tmessage_text = {message_text}\n")
        return

    reply_message = await message.answer(
        text=message_text)

    reply_message_id = reply_message.message_id
    cur_chat_id = reply_message.chat.id
    messages_ids_to_delete = [reply_message_id, reply_message_id - 1]

    delay_seconds = number_or_str_to_float(
        number_or_str_number=delete_delay_seconds,
        positive=True)
    if delay_seconds:
        await asyncio.sleep(delay_seconds)

    try:
        await message.bot.delete_messages(
            message_ids=messages_ids_to_delete,
            chat_id=cur_chat_id)
        print(f"\tWarning messages deleted successfully:\n"
              f"\tdeleted_messages = {messages_ids_to_delete}\n")
    except (TelegramBadRequest, Exception) as exception_info:
        print(f"\tWarning messages not deleted, because: {exception_info}\n"
              f"\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

        return messages_ids_to_delete


async def remove_previous_msgs_before_main_btn(state: FSMContext,
                                               message: Message):
    print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state,
        fsm_state_literal_key="handlers_stack")
    print(f"\tOrigin handler stack: len(handlers_list)={len(handlers_list)}\n")

    if len(handlers_list) > 0:
        prior_handler_dict = handlers_list[-1]
        prior_handler_msgs_ids = prior_handler_dict.get("handler_messages_ids")
        print(f"\tOrigin delete list: "
              f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n")

        if prior_handler_msgs_ids:
            prior_handler_msgs_ids = list(filter(
                lambda msg_id: msg_id is not None, prior_handler_msgs_ids))
            print(f"\tNone values removed from delete list: "
                  f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n")

        if prior_handler_msgs_ids:
            bot = message.bot
            cur_chat_id = message.chat.id
            await bot.delete_messages(chat_id=cur_chat_id,
                                      message_ids=prior_handler_msgs_ids)
            print(f"\tPrior messages were deleted successfully\n"
                  f"\tprior_handler_msgs_ids (deleted ids) = {prior_handler_msgs_ids}\n")

            await state.update_data(main_menu_opened_state=False)
            print(f"\tMain Menu opened state updated to False\n")

        else:
            print(f"\tPrior messages were not deleted, because "
                  f"\tprior_handler_msgs_ids = {prior_handler_msgs_ids}\n")

    # Saving the first handler only (Main Menu) before clearing state
    new_handlers_list = handlers_list[:1]

    # Saving reply message id (Reply Menu) before clearing state
    prior_reply_message_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state,
        fsm_state_literal_key="prior_reply_message_id_state")

    await state.clear()

    await state.update_data(
        handlers_stack=new_handlers_list,
        prior_reply_message_id_state=prior_reply_message_id)
    print(f"\tFirst handler saved. Prior reply msg id saved\n"
          f"\tFSM state cleared. FSM state updated:\n"
          f"\tprior_reply_message_id_state = {prior_reply_message_id}"
          f"\tlen(handlers_list) = {len(new_handlers_list)}\n")
