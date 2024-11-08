from datetime import datetime

from aiogram import Router, Bot

from telegram.config.settings import BOT_CREDENTIALS
from telegram.filters.chat_types_filter import ChatTypesFilter

on_start_stop_router = Router(name=__name__)
on_start_stop_router.message.filter(ChatTypesFilter(["private"]))


@on_start_stop_router.startup()
async def start_bot_handler(bot: Bot, bot_started: str):
    await bot.send_message(
        chat_id=6079930879,
        # chat_id=BOT_CREDENTIALS.TG_BOT_ADMIN_ID,
        text=f"➡️ {bot_started} ⬅️   Telegram bot started   🟢")


@on_start_stop_router.shutdown()
async def shutdown_bot_handler(bot: Bot):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    await bot.send_message(
        chat_id=6079930879,
        # chat_id=BOT_CREDENTIALS.TG_BOT_ADMIN_ID,
        text=f"➡️ {current_datetime} ⬅️   Telegram bot stopped 🔴")
