import asyncio
from aiogram import (
    Bot,
    Dispatcher,
)
from telegram.core.config.settings import BOT_CREDENTIALS

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=BOT_CREDENTIALS.TG_BOT_TOKEN)

dp = Dispatcher()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
