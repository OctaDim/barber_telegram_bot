import json
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from telegram.telegram_utils.dict_utils import empty_dict_if_none
from telegram.telegram_utils.handlers_stack_utils import get_handlers_stack_list


class AllUpdatesMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable,
                       event: TelegramObject,
                       data: Dict) -> Any:

        # Use to see event content in a convenient form in a file
        # event_dict = event.model_dump(mode="json")
        # with open("TestJSON.json", "w") as json_file:
        #     json.dump(event_dict, json_file, indent=4, ensure_ascii=True)

        current_handler_data = {"handler": handler,
                                "event": event,
                                "data": data}

        # Passing current_handler_data to the handler through data
        data["current_handler_data"] = current_handler_data

        # Executing and getting answer from the handler, dict or none
        handler_answer = await handler(event, data)
        handler_answer = empty_dict_if_none(handler_answer)

        # Getting fsm state from the data dictionary
        state = data.get("state")

        # Saving last message id if not inline kbd, to check inline kbd is actual thereafter
        if not event.callback_query :
            await state.update_data(
                last_not_inline_msg_id_state=event.message.message_id)

        # Skip adding handler to stack if inline kbd callback query
        if event.callback_query and not handler_answer.get("add_handler_stack"):
            print("\tTEST INFO: All updates middleware. Handlers stack skipped "
                  "because inline kbd cb query answer and add_handler_stack was not returned\n")
            return

        # Skip adding handler to stack if handler returns dict {"skip_handler_stack": True}
        if handler_answer.get("skip_handler_stack"):
            print("\tTEST INFO: All updates middleware. Handlers stack skipped "
                  "because skip_handler_stack key was returned from handler\n")
            return

        # Adding current executed handler data to the handler stack
        handlers_list = await get_handlers_stack_list(state=state)
        handlers_list.append(current_handler_data)
        await state.update_data(handlers_stack=handlers_list)

        print("\tTEST INFO: All updates middleware. Handlers stack incremented +1")
        print(f"\tTEST INFO: len(handlers_list): {len(handlers_list)}\n")
