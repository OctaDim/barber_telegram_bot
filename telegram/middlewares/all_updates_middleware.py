from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import show_handlers_stack_logs
from utilities.dict_utils import (
    empty_dict_if_none)


class AllUpdatesMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable,
                       event: TelegramObject,
                       data: Dict) -> Any:

        # Getting FSM state from the data parameter
        state: FSMContext = data.get("state")
        state_data = await state.get_data()

        current_handler_data = {"handler": handler,
                                "event": event,
                                "data": data}

        # Passing current_handler_data to the handler through data, for future
        data["current_handler_data"] = current_handler_data

        # Executing and getting answer, dict or None, from the handler
        handler_answer = await handler(event, data)
        handler_answer = empty_dict_if_none(handler_answer)
        handlers_list = await get_valid_list_by_fsm_state_key(
            fsm_state_or_state_dict=state_data,
            fsm_state_literal_key="handlers_stack")

        print(f"{'-' * 115}\n\tMiddleWare: AllUpdatesMiddleware\n")

        if not handler_answer:
            print(f"\tAdding to handlers stack skipped, because "
                  f"\thandler_answer = {handler_answer}\n"
                  f"\tlen(handlers_list): {len(handlers_list)}\n")
            return

        add_handler_to_stack_answer = handler_answer.get("add_handler_to_return_stack")
        cur_handler_msgs_ids = handler_answer.get("handler_messages_ids")
        executed_handler_name = handler_answer.get("executed_handler_name")

        if executed_handler_name:
            print(f"\tExecuted handler name = {executed_handler_name}\n")

        if add_handler_to_stack_answer:
            if cur_handler_msgs_ids:
                current_handler_data["handler_messages_ids"] = cur_handler_msgs_ids
                current_handler_data["handler_name"] = executed_handler_name

                print(f"\tCurrent Handler messages ids added to cur handler info:\n"
                      f"\thandler_messages_ids = {cur_handler_msgs_ids}\n")

            else:
                print(f"\tCurrent Handler messages ids is empty: "
                      f"\thandler_messages_ids = {cur_handler_msgs_ids}\n")

            handlers_list.append(current_handler_data)
            await state.update_data(handlers_stack=handlers_list)
            print(f"\tHandlers stack incremented +1, because "
                  f"\tflag add_handler_to_stack_answer = {add_handler_to_stack_answer}\n"
                  f"\tlen(handlers_list)={len(handlers_list)}\n")
        else:
            print(f"\tAdding to handlers stack skipped, because "
                  f"\tflag add_handler_to_stack_answer={add_handler_to_stack_answer}\n"
                  f"\tlen(handlers_list)={len(handlers_list)}\n")

        update_min_actual_msg_id_answer = handler_answer.get("update_min_actual_msg_id")
        if update_min_actual_msg_id_answer:
            if event.message:
                new_actual_msg_min_id = event.message.message_id
            elif event.callback_query.message:
                new_actual_msg_min_id = event.callback_query.message.message_id
            else:
                new_actual_msg_min_id = None

            await state.update_data(
                actual_message_min_id=new_actual_msg_min_id)
            print(f"\tMin actual message id updated, because "
                  f"\tflag update_min_actual_msg_id = {update_min_actual_msg_id_answer}\n"
                  f"\tactual_message_min_id = {new_actual_msg_min_id}\n")
        else:
            actual_message_min_id = await get_valid_int_by_fsm_state_key(
                fsm_state_or_dict_from=state_data,
                fsm_state_literal_key="actual_message_min_id")
            print(f"\tMin actual msg id not updated, because "
                  f"\tflag update_min_actual_msg_id = {update_min_actual_msg_id_answer}\n"
                  f"\tactual_message_min_id = {actual_message_min_id}\n")

        if event.message:
            print(f"\tUpdate from Non-Callback Query (reply kbd or other non-inline)\n"
                  f"\tevent.message id={event.message.message_id}\n")
        elif event.callback_query.message:
            print(f"\tUpdate from Callback Query (inline keyboard action)\n"
                  f"\tevent.callback_query.message id = "
                  f"{event.callback_query.message.message_id}\n")

        await show_handlers_stack_logs(state=state)
