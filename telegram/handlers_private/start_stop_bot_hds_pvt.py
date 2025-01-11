from datetime import datetime

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest

from telegram.config.configs import BOT_START_STOP_CONFIG
from telegram.config.settings import BOT_CREDENTIALS
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.telegram_utils.global_menu_button_utils import (
    get_several_roles_ids_list)

on_start_stop_router = Router(name=__name__)
on_start_stop_router.message.filter(ChatTypesFilter(["private"]))


@on_start_stop_router.startup()
async def start_bot_handler(bot: Bot, bot_started: str):
    if not BOT_START_STOP_CONFIG.SEND_BOT_START_STOP_MSG:
        return
    send_start_msg_ids = get_several_roles_ids_list(
        env_ids_string_lists=[BOT_CREDENTIALS.BOT_START_STOP_MSG_IDS, ])

    for send_msg_id in send_start_msg_ids:
        try:
            await bot.send_message(
                chat_id=send_msg_id,
                text=f"{bot_started} 🟢")

        except (TelegramBadRequest, Exception) as exception_error:
            print(f"\tBot 'start' message not sent because "
                  f"\texception_error = {exception_error}\n"
                  f"\tsend_start_msg_ids = '{send_start_msg_ids}'\n"
                  f"\tsend_msg_id = {send_msg_id}\n")


@on_start_stop_router.shutdown()
async def shutdown_bot_handler(bot: Bot):
    if not BOT_START_STOP_CONFIG.SEND_BOT_START_STOP_MSG:
        return

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

    send_stop_msg_for_ids = get_several_roles_ids_list(
        env_ids_string_lists=[BOT_CREDENTIALS.BOT_START_STOP_MSG_IDS, ])

    for send_msg_id in send_stop_msg_for_ids:
        try:
            await bot.send_message(
                chat_id=send_msg_id,
                text=f"{current_datetime} 🔴")

        except (TelegramBadRequest, Exception) as exception_error:
            print(f"\tBot 'stop' message not sent because "
                  f"\texception_error = {exception_error}\n"
                  f"\tsend_stop_msg_for_ids = '{send_stop_msg_for_ids}'\n"
                  f"\tsend_msg_id = {send_msg_id}\n")
