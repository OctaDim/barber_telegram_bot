import asyncio
import logging

from aiogram import Bot, Dispatcher

from telegram.config.settings import BOT_CREDENTIALS
from telegram.handlers_private.commands_pvt import on_start_router


ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=BOT_CREDENTIALS.TG_BOT_TOKEN)
dp = Dispatcher()

dp.include_router(on_start_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
