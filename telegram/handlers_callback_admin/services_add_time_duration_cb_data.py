from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.admin_queries import add_services
from telegram.handlers_admin.services_btn_admin import (add_price_service,
                                                        preview_service)
from telegram.keyboard_inline.service_get_all_categories_by_master import AdminCategoryForServiceCbData
from telegram.keyboard_inline.services_time_duration_add_inl_kbd import (
    HoursCallbackData,
    MinutesCallbackData
)

from telegram.keyboard_inline.services_time_duration_add_inl_kbd import (
    add_hours_time_duration_services_inl_kbd,
    add_minutes_time_duration_services_inl_kbd
)
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.params.add_time_duration_cb_data_message import (
    ZERO_DURATION_NOT_ALLOWED,
    HOURS,
    MINUTES_SIGN_UP,
    YOU_CHOSEN_HOURS,
    HOURS_SIGN_UP,
    MINUTES,
    YOU_CHOSEN_MINUTES
)
from telegram.params.button_admin_panel_or_main_menu import ButtonAdminPanelOrMainMenu
from telegram.params.messages import SUCCESSFULLY

services_add_time_duration_cb_query = Router(name=__name__)


@services_add_time_duration_cb_query.callback_query(HoursCallbackData.filter())
async def add_hours_callback_query(callback_query: CallbackQuery,
                                   bot: Bot,
                                   callback_data: HoursCallbackData,
                                   state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    data = await state.get_data()
    if data.get("duration_minutes") == 0 and callback_data.hours == 0:
        await callback_query.answer(text=ZERO_DURATION_NOT_ALLOWED,
                                    show_alert=True)
        return

    await state.update_data(duration_hours=callback_data.hours)

    data = await state.get_data()

    await callback_query.message.edit_text(
        text=HOURS,
        reply_markup=add_hours_time_duration_services_inl_kbd(callback_data.hours))

    if data.get("duration_minutes") is None:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id + 1,
            text=MINUTES_SIGN_UP,
            reply_markup=add_minutes_time_duration_services_inl_kbd())

        # await bot.send_message(chat_id=chat_id, text=YOU_CHOSEN_HOURS)

    elif data.get('duration_entered'):
        return await preview_service(message=callback_query.message, state=state)

    else:
        # await bot.delete_message(chat_id=chat_id, message_id=message_id+1)
        await add_price_service(message=callback_query.message, state=state)


@services_add_time_duration_cb_query.callback_query(MinutesCallbackData.filter())
async def add_minutes_callback_query(callback_query: CallbackQuery,
                                     bot: Bot,
                                     callback_data: MinutesCallbackData,
                                     state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    data = await state.get_data()
    if data.get("duration_hours") == 0 and callback_data.minutes == 0:
        await callback_query.answer(text=ZERO_DURATION_NOT_ALLOWED,
                                    show_alert=True)
        return

    await state.update_data(duration_minutes=callback_data.minutes)

    data = await state.get_data()

    await callback_query.message.edit_text(
        text=MINUTES,
        reply_markup=add_minutes_time_duration_services_inl_kbd(callback_data.minutes))

    if data.get("duration_hours") is None:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id - 1,
            text=HOURS_SIGN_UP,
            reply_markup=add_hours_time_duration_services_inl_kbd())

        # await bot.send_message(chat_id=chat_id, text=YOU_CHOSEN_MINUTES)

    elif data.get('duration_entered'):
        return await preview_service(message=callback_query.message, state=state)

    else:
        # await bot.delete_message(chat_id=chat_id, message_id=message_id+2)
        await add_price_service(message=callback_query.message, state=state)


@services_add_time_duration_cb_query.callback_query(AdminCategoryForServiceCbData.filter())
async def add_select_category_for_service(
        callback_query: CallbackQuery,
        callback_data: AdminCategoryForServiceCbData,
        state: FSMContext,
        bot: Bot
):
    category_id = callback_data.category_id
    user_telegram_id = callback_query.from_user.id

    state_data = await state.get_data()

    messages_id = state_data.get('messages_id')

    await bot.delete_messages(message_ids=messages_id,
                              chat_id=callback_query.message.chat.id)

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=SUCCESSFULLY,
        reply_markup=get_admin_main_menu_kbd()
    )

    add_services(
        data=state_data,
        user_telegram_id=user_telegram_id,
        category_id=category_id
    )


    await state.clear()
