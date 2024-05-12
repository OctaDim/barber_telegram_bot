from aiogram.filters import Filter
from aiogram.types import Message
from aiogram import types, Bot

from telegram.config.settings import BOT_CREDENTIALS


class ChatTypesFilter(Filter):
    def __init__(self, chat_types: list[str]):
        self.chat_types = chat_types

    async def __call__(self, message: Message, *args, **kwargs) -> bool:
        chat_type_matches = message.chat.type in self.chat_types
        return chat_type_matches


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, *args, **kwargs) -> bool:
        admin_id = BOT_CREDENTIALS.TG_BOT_ADMIN_ID
        is_amin = message.from_user.id == int(admin_id)
        return is_amin
