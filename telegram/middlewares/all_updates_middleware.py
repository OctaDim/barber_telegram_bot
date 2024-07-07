import json
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from telegram.telegram_utils.list_utils import empty_list_if_none


class AllUpdatesMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable,
                       event: TelegramObject,
                       data: Dict) -> Any:

        # event_dict = event.model_dump(mode="json")
        # with open("TestJSON.json", "w") as json_file:
        #     json.dump(event_dict, json_file, indent=4, ensure_ascii=True)

        current_handler_data = {"handler": handler,
                                "event": event,
                                "data": data}

        data["current_handler_data"] = current_handler_data

        handler_answer = await handler(event, data)

        # Skip adding handler to stack if inline kbd callback query
        if event.callback_query:
            print("\tTEST INFO: All updates middleware. "
                  "Handlers stack skipped because inline keyboard callback query answer\n")
            return

        # Skip adding handler to stack if handler returns dict {"skip_handler_stack": True}
        if handler_answer and handler_answer.get("skip_handler_stack"):
            print("\tTEST INFO: All updates middleware. "
                  "Handlers stack skipped because skip_handler_stack key was returned from handler\n")
            return

        state = data.get("state")  # Getting fsm state from the data
        state_data = await state.get_data()

        handlers_list = state_data.get("handlers_stack")
        handlers_list = empty_list_if_none(original_list=handlers_list)
        handlers_list.append(current_handler_data)

        await state.update_data(handlers_stack=handlers_list)

        print("\tTEST INFO: All updates middleware. Handlers stack incremented +1")
        print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")
