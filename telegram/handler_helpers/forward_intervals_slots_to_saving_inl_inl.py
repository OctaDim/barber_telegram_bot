import copy
import inspect

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key)


async def delete_intervals_slots_msgs_before_saving_slots(
        callback_query: CallbackQuery,
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
              f"\thandlers_list={handlers_list}\n")
        return
    elif not len(handlers_list) > 0:
        print(f"\tReturn operations skipped, because\n"
              f"\tlen(handlers_list)={len(handlers_list)}\n")
        return

    prior_handler_dict = handlers_list[-1]
    prior_handler_msgs_ids = prior_handler_dict.get("handler_messages_ids")
    messages_ids_to_delete = copy.copy(prior_handler_msgs_ids)
    print(f"\tOrigin lists:\n"
          f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

    # Remove first message (editable) id from messages ids list to be deleted
    # to be able to edit by the next handler message
    messages_ids_to_delete.pop(0)
    print(f"\tFirst Inline Message removed from delete list, because\n"
          f"\tcallback_query.message.caption = {callback_query.message.caption}\n"
          f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

    # Remove last enroll services msg id from msgs ids list to be deleted
    # (to exclude opening telegram text keyboard on reply return button)
    messages_ids_to_delete.pop(-1)
    print(f"\tLast Reply Message removed from delete list, because\n"
          f"\tcallback_query.message.caption = {callback_query.message.caption}\n"
          f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
          f"\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

    if messages_ids_to_delete:
        messages_ids_to_delete = list(filter(
            lambda msg_id: msg_id is not None, messages_ids_to_delete))
        print(f"\tNone values removed from delete list:\n"
              f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
              f"\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

        cur_chat_id = callback_query.message.chat.id
        await bot.delete_messages(chat_id=cur_chat_id,
                                  message_ids=messages_ids_to_delete)
        print(f"\tPrior messages deleted successfully:\n"
              f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
              f"\tmessages_ids_to_delete (deleted ids) = {messages_ids_to_delete}\n")

    else:
        print(f"\tPrior messages not deleted, because\n"
              f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n"
              f"\tmessages_ids_to_delete = {messages_ids_to_delete}\n")

    handlers_list.pop()
    print(f"\t'Calendar' handler removed from handlers list (reduced -1):\n"
          f"\tlen(handlers_list)={len(handlers_list)}\n")

    await state.update_data(
        handlers_stack=handlers_list)
    print(f"\tHandler stack updated:\n"
          f"\tlen(handlers_list)={len(handlers_list)}\n")
