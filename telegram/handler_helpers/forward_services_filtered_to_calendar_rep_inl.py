import copy
import inspect

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.params.buttons_enroll_service import (
    ENROLL_SRCS_BUTTONS)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key)


async def delete_srcs_filtered_msgs_before_calendar(
        message: Message,
        state: FSMContext,
        bot: Bot
) -> None:
    state_data = await state.get_data()

    print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="handlers_stack")
    print(f"\tOrigin handler stack: len(handlers_list)={len(handlers_list)}\n")

    if handlers_list is None:
        print(f"\tReturn operations skipped, because\n"
              f"\t\thandlers_list={handlers_list}\n")
        return
    elif not len(handlers_list) > 0:
        print(f"\tReturn operations skipped, because\n"
              f"\t\tlen(handlers_list)={len(handlers_list)}\n")
        return

    prior_handler_dict = handlers_list[-1]
    prior_handler_msgs_ids = prior_handler_dict.get("handler_messages_ids")
    messages_ids_to_delete = copy.copy(prior_handler_msgs_ids)
    prior_inline_message_id = messages_ids_to_delete[0]
    print(f"\tOrigin data:\n"
          f"\t\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\t\tmessages_ids_to_delete = {messages_ids_to_delete}\n"
          f"\t\tprior_inline_message_id = {prior_inline_message_id}\n")

    # # Remove first message (editable) id from messages ids list to be deleted
    # # to be able to edit by the next handler message
    messages_ids_to_delete.pop(0)
    print(f"\tFirst Inline Message removed from delete list, because\n"
          f"\tmessage.text = {ENROLL_SRCS_BUTTONS.CONTINUE_ENROLL_SERVICES}\n"
          f"\t\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\t\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

    # Remove Enroll Services Reply kbd Menu msg id from msgs ids list to be deleted
    # (to exclude opening telegram text keyboard on reply return button)
    messages_ids_to_delete.pop(-1)
    print(f"\tLast Reply Message removed from delete list, because\n"
          f"\tmessage.text = {ENROLL_SRCS_BUTTONS.CONTINUE_ENROLL_SERVICES}\n"
          f"\t\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\t\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

    # Add "Continue Enroll Services" Reply kbd msg from user to delete list
    messages_ids_to_delete.append(message.message_id)
    print(f"\tReply kbd 'Continue Enroll Services' msg id added to delete list, because\n"
          f"\tmessage.text = {ENROLL_SRCS_BUTTONS.CONTINUE_ENROLL_SERVICES}\n"
          f"\t\tmessage.message_id = {message.message_id}\n"
          f"\t\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\t\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

    if messages_ids_to_delete:
        messages_ids_to_delete = list(filter(
            lambda msg_id: msg_id is not None, messages_ids_to_delete))
        print(f"\tNone values removed from delete list:\n"
              f"\t\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
              f"\t\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

        cur_chat_id = message.chat.id
        await bot.delete_messages(chat_id=cur_chat_id,
                                  message_ids=messages_ids_to_delete)
        print(f"\tPrior messages deleted successfully:\n"
              f"\t\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
              f"\t\tmessages_ids_to_delete (deleted ids) = {messages_ids_to_delete}\n")

        await state.update_data(
            reply_keyboard_opened_state=False)
        print(f"\tReply Menu opened state updated to False:\n"
              f"\t\treply_keyboard_opened_state = False\n")

    else:
        print(f"\tPrior messages not deleted, because\n"
              f"\t\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
              f"\t\tmessages_ids_to_delete = {messages_ids_to_delete}\n")
