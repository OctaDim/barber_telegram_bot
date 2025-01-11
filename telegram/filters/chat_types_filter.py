from aiogram import types
from aiogram.filters import Filter
from aiogram.types import Message

from telegram.config.settings import BOT_CREDENTIALS
from telegram.telegram_utils.global_menu_button_utils import (
    get_several_roles_ids_list)


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
        admins_ids = get_several_roles_ids_list(
            env_ids_string_lists=[
                BOT_CREDENTIALS.TG_BOT_ADMINS_IDS,
                BOT_CREDENTIALS.TG_BOT_DEVELOPERS_IDS],
        )
        is_admin = message.from_user.id in admins_ids
        return is_admin
