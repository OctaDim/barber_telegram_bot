from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class AllUpdatesMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:

        current_handler_data = {"handler": handler,
                                "event": event,
                                "data": data}

        state = data.get("state")
        state_data = await state.get_data()

        handlers_list = state_data.get("handlers_stack")

        if handlers_list:
            handlers_list.append(current_handler_data)
        else:
            handlers_list = [current_handler_data]

        await state.update_data(handlers_stack=handlers_list)

        data["current_handler_data"] = current_handler_data

        print("\tTEST INFO: All updates middleware. Handlers stack incremented")
        print("\tTEST INFO: len(handlers_list): ", len(handlers_list))
        print()

        result = await handler(event, data)
        return result
