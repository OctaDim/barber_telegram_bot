import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat

from telegram.config.settings import BOT_CREDENTIALS
from telegram.params.commands import COMMANDS_PARAMS

from telegram.handlers_private.commands_pvt import on_start_router
from telegram.handlers_private.services_btn_pvt import services_btn_router
from telegram.handlers_private.contacts_btn_pvt import contacts_btn_router
from telegram.handlers_admin.commands_admin import admin_panel
from telegram.handlers_admin.services_btn_admin import services_admin_btn_router


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - "
                           "%(message)s")

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=BOT_CREDENTIALS.TG_BOT_TOKEN)
dp = Dispatcher()
dp["bot_started"] = datetime.now().strftime("%Y-%m-%d %H:%M")

dp.include_router(admin_panel)
dp.include_router(on_start_router)
dp.include_router(services_btn_router)
dp.include_router(contacts_btn_router)
dp.include_router(services_admin_btn_router)


private_chat_commands = [
    BotCommand(command=COMMANDS_PARAMS.MENU_CMD.TEXT,
               description=COMMANDS_PARAMS.MENU_CMD.DESCRIPTION),
    # BotCommand(command=COMMANDS_PARAMS.MENU_CMD.TEXT,
    #            description=COMMANDS_PARAMS.MENU_CMD.DESCRIPTION),
]

admin_chat_commands = [
    BotCommand(command=COMMANDS_PARAMS.ADMIN_PANEL.TEXT,
               description=COMMANDS_PARAMS.ADMIN_PANEL.DESCRIPTION),
    BotCommand(command=COMMANDS_PARAMS.MENU_CMD.TEXT,
               description=COMMANDS_PARAMS.MENU_CMD.DESCRIPTION),
]

scope = BotCommandScopeChat(chat_id=int(BOT_CREDENTIALS.TG_BOT_ADMIN_ID))


async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_my_commands(commands=private_chat_commands)
    await bot.set_my_commands(commands=admin_chat_commands, scope=scope)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types())

    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
