import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from telegram.config.settings import BOT_CREDENTIALS
from telegram.params.commands import COMMANDS_PARAMS
from telegram.handlers_private.commands_pvt import on_start_router


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - "
                           "%(message)s")

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=BOT_CREDENTIALS.TG_BOT_TOKEN)
dp = Dispatcher()
dp["bot_started"] = datetime.now().strftime("%Y-%m-%d %H:%M")

dp.include_router(on_start_router)

private_chat_commands = [
    BotCommand(command=COMMANDS_PARAMS.START_CMD.TEXT,
               description=COMMANDS_PARAMS.START_CMD.DESCRIPTION),
    # BotCommand(command=COMMANDS_PARAMS.MENU_CMD.TEXT,
    #            description=COMMANDS_PARAMS.MENU_CMD.DESCRIPTION),
]


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_chat_commands)

    try:
        await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
