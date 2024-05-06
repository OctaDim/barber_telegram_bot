from aiogram.filters import Filter
from aiogram.types import Message


class ChatTypesFilter(Filter):
    def __init__(self, chat_types: list[str]):
        self.chat_types = chat_types

    async def __call__(self, message: Message, *args, **kwargs) -> bool:
        chat_type_matches = message.chat.type in self.chat_types
        return chat_type_matches
