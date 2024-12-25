import inspect

from aiogram import Router, F, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.params.buttons_common import (
    COMMON_BUTTONS_PARAMS)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handler_answer_flag_dict)

return_button_router = Router(name=__name__)
return_button_router.message.filter(ChatTypesFilter(["private"]))


@return_button_router.message(F.text == COMMON_BUTTONS_PARAMS.RETURN)
async def return_button_reply_hdr_pvt(message: Message,
                                      state: FSMContext,
                                      bot: Bot,
                                      callback_data: CallbackData = None):
    state_data = await state.get_data()

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="handlers_stack")
    print(f"\tOrigin handler stack: len(handlers_list)={len(handlers_list)}\n")

    if len(handlers_list) > 0:
        prior_handler_dict = handlers_list[-1]
        prior_handler_msgs_ids = prior_handler_dict.get("handler_messages_ids")
        print(f"\tOrigin delete list: "
              f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n")

        if callback_data and callback_data.delete_inline_msg_on_return is True:
            # Stay inline message id in messages ids list to be deleted
            print(f"\tInline msg (callback_query.message.message_id) stayed in "
                  f"\tdelete list, because from inline return cb hdr passed:\n"
                  f"\tcallback_data: {callback_data}\n"
                  f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n")

        elif callback_data and callback_data.delete_inline_msg_on_return is False:
            # Remove inline message id from messages ids list to be deleted
            # to be able to edit by the next handler message
            prior_handler_msgs_ids.remove(message.message_id)
            print(f"\tInline msg (callback_query.message.message_id) removed from "
                  f"delete list, because from inline return cb hdr passed:\n"
                  f"\tcallback_data: {callback_data}\n"
                  f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n")

        if prior_handler_msgs_ids:
            prior_handler_msgs_ids = list(filter(
                lambda msg_id: msg_id is not None, prior_handler_msgs_ids))
            print(f"\tNone values removed from delete list: "
                  f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n")

        if prior_handler_msgs_ids:
            cur_chat_id = message.chat.id
            await bot.delete_messages(chat_id=cur_chat_id,
                                      message_ids=prior_handler_msgs_ids)
            print(f"\tPrior messages were deleted successfully\n"
                  f"\tprior_handler_msgs_ids (deleted ids) = "
                  f"\t{prior_handler_msgs_ids}\n")

        else:
            print(f"\tPrior messages were not deleted, because "
                  f"\tprior_handler_msgs_ids = {prior_handler_msgs_ids}\n")

        handlers_list.pop()
        print(f"\tHandlers list reduced (-1): "
              f"\tlen(handlers_list)={len(handlers_list)}\n")

        await execute_last_stack_handler(handlers_list)
        print(f"\tPrior handler (-1) was executed: "
              f"\tlen(handlers_list)={len(handlers_list)}\n")

        await state.update_data(handlers_stack=handlers_list)
        print(f"\tHandler stack updated: "
              f"\tlen(handlers_list)={len(handlers_list)}\n")

    else:
        print(f"\tReturn operations skipped, because "
              f"\tlen(handlers_list)={len(handlers_list)}\n")

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
