from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.handlers_admin.services_btn_admin import add_price_service, preview_service
from telegram.keyboard_inline.services_time_duration_add_inl_kbd import (
    HoursCallbackData,
    MinutesCallbackData
)

from telegram.keyboard_inline.services_time_duration_add_inl_kbd import (
    add_hours_time_duration_services_inl_kbd,
    add_minutes_time_duration_services_inl_kbd
)
from telegram.params.add_time_duration_cb_data_message import (
    ZERO_DURATION_NOT_ALLOWED,
    HOURS,
    MINUTES_SIGN_UP,
    YOU_CHOSEN_HOURS,
    HOURS_SIGN_UP,
    MINUTES,
    YOU_CHOSEN_MINUTES
)


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
        await bot.send_message(
            chat_id=chat_id,
            text=ZERO_DURATION_NOT_ALLOWED)
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

        await bot.send_message(chat_id=chat_id, text=YOU_CHOSEN_HOURS)

    elif data.get('duration_entered'):
        return await preview_service(message=callback_query.message, state=state)

    else:
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
        await bot.send_message(
            chat_id=chat_id,
            text=ZERO_DURATION_NOT_ALLOWED)
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

        await bot.send_message(chat_id=chat_id, text=YOU_CHOSEN_MINUTES)

    elif data.get('duration_entered'):
        return await preview_service(message=callback_query.message, state=state)

    else:
        await add_price_service(message=callback_query.message, state=state)
