from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from telegram.telegram_utils.handlers_stack_utils import get_handlers_stack_list
from utilities.dict_utils import (
    empty_dict_if_none)


class AllUpdatesMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable,
                       event: TelegramObject,
                       data: Dict) -> Any:

        # Getting FSM state from the data parameter
        state_data: FSMContext = data.get("state")

        current_handler_data = {"handler": handler,
                                "event": event,
                                "data": data}

        # Passing current_handler_data to the handler through data
        data["current_handler_data"] = current_handler_data

        # Executing and getting answer, dict or None, from the handler
        handler_answer = await handler(event, data)
        handler_answer = empty_dict_if_none(handler_answer)

        # Automatically adding handler to the handlers stack if not skip_add_handler_stack flag
        if (handler_answer is not None
                and not handler_answer.get("skip_add_handler_stack")):
            handlers_list = await get_handlers_stack_list(state=state_data)
            handlers_list.append(current_handler_data)
            await state_data.update_data(handlers_stack=handlers_list)

            print("\tTEST INFO: All updates middleware. Handlers stack incremented +1")
            print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")

        else:  # Skipping adding handler to the handlers stack if skip_add_handler_stack flag

            print("\tTEST INFO: All updates middleware. Handlers stack skipped "
                  "because skip_add_handler_stack flag was returned from handler\n")

        # Updating message min id if any updates except inline kbd
        if event.message:
            actual_message_min_id = event.message.message_id
            await state_data.update_data(actual_message_min_id=actual_message_min_id)

            print("\tTEST INFO: All updates middleware. Min message id updated "
                  "because any updates from relpy kbd (event.message)\n")

        # Updating message min id if inline kbd and upd_actual_msg_min_id flag
        elif event.callback_query and handler_answer.get("upd_actual_msg_min_id"):
            actual_message_min_id = event.callback_query.message.message_id
            await state_data.update_data(actual_message_min_id=actual_message_min_id)

            print("\tTEST INFO: All updates middleware. Min message id updated "
                  "because inline keyboard (event.callback_query) "
                  "and 'upd_actual_msg_min_id' flag\n")

        else:  # Skipping updating min message id
            print("\tTEST INFO: All updates middleware. Min message id not updated"
                  "because inline keyboard (event.callback_query), "
                  "but not 'upd_actual_msg_min_id' flag\n")
