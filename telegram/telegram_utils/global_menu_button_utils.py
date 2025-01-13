import inspect

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommandScopeChat, BotCommand

from telegram.config.settings import BOT_CREDENTIALS
from telegram.params.commands import COMMANDS_PARAMS
from utilities.list_utils import (
    get_strs_list_from_env_string,
    convert_str_list_to_int_list)


async def enable_users_global_commands(bot: Bot) -> None:
    private_chat_commands = [
        BotCommand(command=COMMANDS_PARAMS.MENU_CMD.TEXT,
                   description=COMMANDS_PARAMS.MENU_CMD.DESCRIPTION), ]

    await bot.set_my_commands(commands=private_chat_commands)


async def enable_admins_global_commands(bot: Bot) -> None:
    print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

    admins_chat_commands = [
        BotCommand(command=COMMANDS_PARAMS.ADMIN_PANEL.TEXT,
                   description=COMMANDS_PARAMS.ADMIN_PANEL.DESCRIPTION),
        BotCommand(command=COMMANDS_PARAMS.MENU_CMD.TEXT,
                   description=COMMANDS_PARAMS.MENU_CMD.DESCRIPTION), ]

    admins_ids_env_str = BOT_CREDENTIALS.TG_BOT_ADMINS_IDS
    admins_tg_ids = get_strs_list_from_env_string(
        origin_env_string=admins_ids_env_str)

    for admin_tg_id in admins_tg_ids:
        admins_scope = BotCommandScopeChat(chat_id=admin_tg_id)
        try:
            await bot.set_my_commands(commands=admins_chat_commands,
                                      scope=admins_scope)
            print(f"\tAdmin global commands enabled successfully "
                  f"\tadmin_tg_id = {admin_tg_id}\n")

        except (TelegramBadRequest, Exception) as exception_error:
            print(f"\tAdmin global commands not enabled because "
                  f"\texception_error = {exception_error}\n"
                  f"\tadmins_ids_env_str = '{admins_ids_env_str}'\n"
                  f"\tadmin_tg_id = {admin_tg_id}\n")


async def enable_developers_global_commands(bot: Bot) -> None:
    print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

    developers_chat_commands = [
        BotCommand(command=COMMANDS_PARAMS.ADMIN_PANEL.TEXT,
                   description=COMMANDS_PARAMS.ADMIN_PANEL.DESCRIPTION),
        BotCommand(command=COMMANDS_PARAMS.MENU_CMD.TEXT,
                   description=COMMANDS_PARAMS.MENU_CMD.DESCRIPTION), ]

    developers_ids_env_str = BOT_CREDENTIALS.TG_BOT_DEVELOPERS_IDS
    developers_tg_ids = get_strs_list_from_env_string(
        origin_env_string=developers_ids_env_str)

    for developer_tg_id in developers_tg_ids:
        developers_scope = BotCommandScopeChat(chat_id=developer_tg_id)
        try:
            await bot.set_my_commands(commands=developers_chat_commands,
                                      scope=developers_scope)
            print(f"\tDeveloper global commands enabled successfully "
                  f"\tdeveloper_tg_id = {developer_tg_id}\n")

        except (TelegramBadRequest, Exception) as exception_error:
            print(f"\tDeveloper global commands not enabled because "
                  f"\texception_error = {exception_error}\n"
                  f"\tdevelopers_ids_env_str = '{developers_ids_env_str}'\n"
                  f"\tdeveloper_tg_id = {developer_tg_id}\n")


def get_several_roles_ids_list(env_ids_string_lists: list[str]) -> list[int]:
    several_roles_admins_list = []
    for cur_admin_list in env_ids_string_lists:
        admins_ids = cur_admin_list
        admins_ids = get_strs_list_from_env_string(admins_ids)
        admins_ids = convert_str_list_to_int_list(admins_ids)

        several_roles_admins_list.extend(admins_ids)

    return several_roles_admins_list
