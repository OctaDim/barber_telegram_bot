import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeChat

# ######################################################################
# ## Very necessary import to initialize DB models without cycle imports
# ######################################################################
import database.db_imports_initialization
# ######################################################################

from telegram.config.settings import BOT_CREDENTIALS
from telegram.handlers_admin.timetable_btn_admin import timetable_admin_btn_router
from telegram.handlers_admin.work_time_btn_time import work_time_admin_btn_router
from telegram.handlers_callback_admin.timetable_cb_data import timetable_cb_query
from telegram.handlers_callback_admin.work_time_cb_data import work_time_cb_query
from telegram.handlers_callback_pvt.clicked_cancell_reservation_client_cb_hdr import \
    clicked_cancel_reservation_cb_router
from telegram.handlers_callback_pvt.clicked_reservation_cancelled_completed_cb_hdr import \
    clicked_reservation_cancd_completed_rtr
from telegram.handlers_callback_pvt.clicked_reservation_date_time_cb_hdr import clicked_reservation_date_time_cb_router
from telegram.handlers_callback_pvt.inline_ask_administrator_cb_hdr import inline_ask_administrator_cb_router
from telegram.handlers_callback_pvt.inline_balance_client_cb_hdr import inline_balance_client_router
from telegram.handlers_callback_pvt.inline_contacts_our_cb_hdr import inline_our_contacts_cb_router
from telegram.handlers_callback_pvt.inline_frequent_questions_cb_hdr import inline_frequent_questions_cb_router
from telegram.handlers_callback_pvt.inline_geo_map_cb_hdr import inline_geo_map_router
from telegram.handlers_callback_pvt.inline_methods_enroll_srcs_cb_hdr import inline_methods_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.inline_payments_history_cb_hdr import inline_payments_history_router
from telegram.handlers_callback_pvt.inline_promotions_our_cb_hdr import inline_promotions_our_cb_router
from telegram.handlers_callback_pvt.inline_reservations_client_cb_hdr import inline_client_reservations_cb_router
from telegram.handlers_callback_pvt.inline_services_our_detail_info_cb_hdr import (
    inline_our_services_by_category_cb_router)
from telegram.handlers_callback_pvt.next_prev_page_reservation_cb_hdr import next_prev_page_reservation_client_cb_router
from telegram.handlers_callback_pvt.return_intervals_slots_to_calendar_cb_hdr import \
    return_interval_slots_to_calendar_cb_router
from telegram.handlers_callback_pvt.selected_category_cb_hdr import category_selected_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.inline_intervals_slots_enroll_srcs_cb_hdr import \
    continue_calendar_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.inline_services_filtered_cb_hdr import \
    inline_services_filtered_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.selected_master_cb_hdr import master_selected_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.inline_categories_enroll_srcs_cb_hdr import inline_categories_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.inline_masters_enroll_srcs_cb_hdr import inline_masters_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.selected_method_cb_hdr import method_selected_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.next_prev_month_calend_cb_hdr import next_prev_month_services_cb_router
from telegram.handlers_callback_pvt.next_prev_page_category_cb_hdr import next_prev_page_category_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.next_prev_page_master_cb_hdr import next_prev_page_master_enroll_srcs_cb_router
from telegram.handlers_callback_pvt.next_prev_page_slot_cb_hdr import next_prev_page_slot_enroll_srcs_cb_router
from telegram.handlers_private.no_action_common_reply_hdr_pvt import reply_no_action_common_router
from telegram.handlers_private.return_to_masters_btn_reply_hdr_pvt import return_to_masters_button_router
from telegram.handlers_private.submenu_on_ask_question_btn_reply_hdr_pvt import submenu_ask_question_pvt_router
from telegram.handlers_private.submenu_on_balance_btn_reply_hdr_pvt import submenu_balance_pvt_router
from telegram.handlers_private.submenu_on_contacts_btn_reply_hdr_pvt import submenu_contacts_pvt_router
from telegram.handlers_private.submenu_on_services_btn_reply_hdr_pvt import submenu_services_pvt_router
from telegram.keyboard_inline.inline_deposit_balance_cb_hdr import inline_deposit_balance_router
from telegram.middlewares.all_updates_middleware import AllUpdatesMiddleware
from telegram.params.commands import COMMANDS_PARAMS

from telegram.handlers_private.start_stop_bot_hds_pvt import on_start_stop_router
from telegram.handlers_private.commands_pvt import on_start_router
from telegram.handlers_admin.commands_admin import admin_panel
from telegram.handlers_admin.services_btn_admin import services_admin_btn_router
from telegram.handlers_callback_admin.services_add_time_duration_cb_data import services_add_time_duration_cb_query
from telegram.handlers_callback_admin.services_change_cb_data import services_change_cb_query
from telegram.handlers_callback_admin.services_remove_cb_data import services_remove_cb_query
from telegram.handlers_callback_pvt.selected_service_unselected_cb_hdr import \
    service_selected_unselected_enroll_srcs_cb_router
from telegram.handlers_private.main_menu_btn_reply_hdr_pvt import return_main_menu_pvt_router
from telegram.handlers_private.return_btn_reply_hdr_pvt import return_button_router
from telegram.handlers_private.unhandled_update_hdr_pvt import unhandled_update_router
from telegram.handlers_private.calendar_on_cont_enroll_srcs_btn_rep_hdr_pvt import continue_enroll_srcs_pvt_router
from telegram.handlers_callback_pvt.selected_month_day_calendar_cb_hdr import (
    month_day_selected_calendar_enroll_srcs_cb_router)
from telegram.handlers_callback_pvt.inline_main_menu_common_cb_hdr import inline_main_menu_common_cb_router
from telegram.handlers_callback_pvt.inline_no_action_common_cb_hdr import no_action_common_cb_router
from telegram.handlers_callback_pvt.return_common_cb_hdr import return_common_cb_router
from telegram.handlers_private.cancel_all_services_btn_reply_hdr_pvt import cancel_all_services_pvt_router
from telegram.handlers_callback_pvt.clicked_slot_advising_icons_cb_hdr import clicked_slot_advising_icons_cb_router
from telegram.handlers_callback_pvt.selected_slot_enroll_srcs_cb_hdr import slot_selected_enroll_services_cb_router
from telegram.handlers_callback_pvt.continue_slot_saving_cb_hdr import continue_slot_saving_enroll_srcs_cb_router

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
dp.include_router(timetable_cb_query)
dp.include_router(work_time_cb_query)
dp.include_router(work_time_admin_btn_router)
dp.include_router(return_button_router)
dp.include_router(services_add_time_duration_cb_query)
dp.include_router(services_remove_cb_query)
dp.include_router(services_change_cb_query)
dp.include_router(service_selected_unselected_enroll_srcs_cb_router)
dp.include_router(month_day_selected_calendar_enroll_srcs_cb_router)
dp.include_router(continue_calendar_enroll_srcs_cb_router)
dp.include_router(next_prev_month_services_cb_router)
dp.include_router(inline_main_menu_common_cb_router)
dp.include_router(return_common_cb_router)
dp.include_router(admin_panel)
dp.include_router(timetable_admin_btn_router)
dp.include_router(services_admin_btn_router)
dp.include_router(on_start_stop_router)
dp.include_router(on_start_router)
dp.include_router(return_main_menu_pvt_router)
dp.include_router(continue_enroll_srcs_pvt_router)
dp.include_router(cancel_all_services_pvt_router)
dp.include_router(clicked_slot_advising_icons_cb_router)
dp.include_router(slot_selected_enroll_services_cb_router)
dp.include_router(continue_slot_saving_enroll_srcs_cb_router)
dp.include_router(inline_categories_enroll_srcs_cb_router)
dp.include_router(next_prev_page_category_enroll_srcs_cb_router)
dp.include_router(category_selected_enroll_srcs_cb_router)
dp.include_router(inline_masters_enroll_srcs_cb_router)
dp.include_router(master_selected_enroll_srcs_cb_router)
dp.include_router(next_prev_page_master_enroll_srcs_cb_router)
dp.include_router(inline_services_filtered_enroll_srcs_cb_router)
dp.include_router(next_prev_page_slot_enroll_srcs_cb_router)
dp.include_router(method_selected_enroll_srcs_cb_router)
dp.include_router(inline_our_services_by_category_cb_router)
dp.include_router(clicked_reservation_date_time_cb_router)
dp.include_router(next_prev_page_reservation_client_cb_router)
dp.include_router(clicked_reservation_cancd_completed_rtr)
dp.include_router(clicked_cancel_reservation_cb_router)
dp.include_router(reply_no_action_common_router)
dp.include_router(submenu_services_pvt_router)
dp.include_router(inline_methods_enroll_srcs_cb_router)
dp.include_router(inline_client_reservations_cb_router)
dp.include_router(inline_our_contacts_cb_router)
dp.include_router(submenu_contacts_pvt_router)
dp.include_router(submenu_ask_question_pvt_router)
dp.include_router(submenu_balance_pvt_router)
dp.include_routers(inline_promotions_our_cb_router)
dp.include_router(inline_ask_administrator_cb_router)
dp.include_router(inline_frequent_questions_cb_router)
dp.include_router(inline_geo_map_router)
dp.include_router(inline_balance_client_router)
dp.include_router(inline_deposit_balance_router)
dp.include_router(inline_payments_history_router)
dp.include_router(return_to_masters_button_router)
dp.include_router(return_interval_slots_to_calendar_cb_router)

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
