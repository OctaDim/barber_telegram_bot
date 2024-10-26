import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeChat

from telegram.config.settings import BOT_CREDENTIALS
# from telegram.handlers_admin.logbook_btn_admin import logbook_admin_btn_router
from telegram.handlers_admin.work_time_btn_time import work_time_admin_btn_router
# from telegram.handlers_callback_admin.logbook_cb_data import logbook_cb_query
from telegram.handlers_callback_admin.work_time_cb_data import work_time_cb_query
from telegram.handlers_callback_pvt.continue_srcs_calendar_cb_hdr import continue_enroll_srcs_calendar_cb_router
from telegram.handlers_callback_pvt.next_prev_month_calend_cb_hdr import next_prev_month_services_cb_router
from telegram.middlewares.all_updates_middleware import AllUpdatesMiddleware
from telegram.params.commands import COMMANDS_PARAMS

from telegram.handlers_private.start_stop_bot_pvt_hds import on_start_stop_router
from telegram.handlers_private.commands_pvt import on_start_router
from telegram.handlers_private.services_btn_pvt import services_btn_router
from telegram.handlers_private.contacts_btn_pvt import contacts_btn_router
from telegram.handlers_admin.commands_admin import admin_panel
from telegram.handlers_admin.services_btn_admin import services_admin_btn_router
from telegram.handlers_private.enroll_services_btn_pvt_hdr import enroll_services_pvt_router
from telegram.handlers_callback_admin.services_add_time_duration_cb_data import services_add_time_duration_cb_query
from telegram.handlers_callback_admin.services_change_cb_data import services_change_cb_query
from telegram.handlers_callback_admin.services_remove_cb_data import services_remove_cb_query
from telegram.handlers_callback_pvt.enroll_services_cb_hdr import enroll_services_cb_router
from telegram.handlers_private.main_menu_btn_pvt_hdr import return_main_menu_pvt_router
from telegram.handlers_private.return_btn_pvt_hdr import return_button_router
from telegram.handlers_private.unhandled_update_pvt_hdr import unhandled_update_router
from telegram.handlers_private.continue_enroll_services_btn_pvt import continue_enroll_srcs_pvt_router
from telegram.handlers_callback_pvt.month_day_enroll_srcs_calendar_cb_hdr import \
    month_day_enroll_srcs_calendar_cb_router
from telegram.handlers_callback_pvt.main_menu_common_cb_hdr import main_menu_common_cb_router
from telegram.handlers_callback_pvt.no_action_common_cb_hdr import no_action_common_cb_router
from telegram.handlers_callback_pvt.return_common_cb_hdr import return_common_cb_router
from telegram.handlers_private.cancel_all_services_btn_pvt import cancel_all_services_pvt_router
from telegram.handlers_callback_pvt.slots_advising_note_cb_hdr import slots_advising_note_cb_router
from telegram.handlers_callback_pvt.slot_selected_cb_hdr import slot_selected_cb_router
from telegram.handlers_callback_pvt.continue_slot_saving_cb_hdr import continue_slot_saving_cb_router

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - "
                           "%(message)s")

# ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=BOT_CREDENTIALS.TG_BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp["bot_started"] = datetime.now().strftime("%Y-%m-%d %H:%M")

# Outer Middlewares:
dp.update.outer_middleware(AllUpdatesMiddleware())

# Routers:
dp.include_router(no_action_common_cb_router)
# dp.include_router(logbook_cb_query)
dp.include_router(work_time_cb_query)
dp.include_router(work_time_admin_btn_router)
dp.include_router(return_button_router)
dp.include_router(services_add_time_duration_cb_query)
dp.include_router(services_remove_cb_query)
dp.include_router(services_change_cb_query)
dp.include_router(enroll_services_cb_router)
dp.include_router(month_day_enroll_srcs_calendar_cb_router)
dp.include_router(continue_enroll_srcs_calendar_cb_router)
dp.include_router(next_prev_month_services_cb_router)
dp.include_router(main_menu_common_cb_router)
dp.include_router(return_common_cb_router)
dp.include_router(admin_panel)
# dp.include_router(logbook_admin_btn_router)
dp.include_router(services_admin_btn_router)
dp.include_router(on_start_stop_router)
dp.include_router(on_start_router)
dp.include_router(return_main_menu_pvt_router)
dp.include_router(enroll_services_pvt_router)
dp.include_router(continue_enroll_srcs_pvt_router)
dp.include_router(cancel_all_services_pvt_router)
dp.include_router(services_btn_router)
dp.include_router(contacts_btn_router)
dp.include_router(slots_advising_note_cb_router)
dp.include_router(slot_selected_cb_router)
dp.include_router(continue_slot_saving_cb_router)
# All unhandled update router:
dp.include_router(unhandled_update_router)

private_chat_commands = [
    BotCommand(command=COMMANDS_PARAMS.MENU_CMD.TEXT,
               description=COMMANDS_PARAMS.MENU_CMD.DESCRIPTION),
    # BotCommand(command=COMMANDS_PARAMS.START_CMD.TEXT,
    #            description=COMMANDS_PARAMS.START_CMD.DESCRIPTION),
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
