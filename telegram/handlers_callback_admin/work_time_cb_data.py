import datetime
import re

from datetime import timedelta

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from database.db_queries.get_master_obj_by_telegram_id import get_master_id_by_telegram_id
from database.db_queries.work_time_queries import create_work_time
from telegram.keyboard_inline.work_time_add_break_inl_kbd import add_break_or_not_inl_kbd, \
    AddBreakResponseWorkTimeCbData, add_break_work_time_inl_kbd, AddStartBreakWorkTime, AddEndBreakWorkTime, \
    NextStepAddBreakWorkTime
from telegram.keyboard_inline.work_time_add_days_inl_kbd import (
    work_time_days_inl_kbd,
    DaysWorkTimeCbData,
    NextStepTimeWorkTimeCbData, ReturnStepToMonthWorkTimeCbData
)

from telegram.keyboard_inline.work_time_add_end_time_inl_kbd import EndWorkTimeCbData, add_end_time_work_inl_kbd, \
    NextStepEndWorkTimeCbData

from telegram.keyboard_inline.work_time_add_month_inl_kbd import MonthWorkTimeCbData, YearWorkTimeCbData, \
    work_time_month_inl_kbd
from telegram.keyboard_inline.work_time_add_start_and_end_break_inl_kbd import StartBreakWorkTimeCbData, \
    add_start_break_time_work_inl_kbd, EndBreakWorkTimeCbData, NextStepStartBreakWorkTimeCbData, \
    add_end_break_time_work_inl_kbd, NextStepEndBreakWorkTimeCbData
from telegram.keyboard_inline.work_time_add_start_time_work_inl_kbd import add_start_time_work_inl_kbd, \
    StartWorkTimeCbData, NextStepStartWorkTimeCbData

from telegram.keyboard_inline.work_time_add_work_time_inl_kbd import add_work_time_inl_kbd, StartWorkCbData, \
    EndWorkCbData, NextStepAddWorkTime

from telegram.keyboard_inline.work_time_interval_add_inl_kbd import (
    add_interval_work_time_services_inl_kbd,
    HoursIntervalWorkTimeCbData,
    IntervalNextStepTimeWorkTimeCbData
)
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.params.messages import SUCCESSFULLY
from telegram.params.work_time_cb_data_message import SELECT_A_MONTH, PICK_DAY, PICK_ONE_DAY, ADD_INTERVAL, \
    INTERVAL_CANNOT_BE_0H_OM, SELECT_WORKING_DAY, CHOOSE_TWO_VALUE, ADD_START_TIME, ADD_END_TIME, TIME_ADDED, \
    TOTAL_OPERATING_TIME_LESS_INTERVAL, SELECT_START_AND_END_WORKING_DAY, PICK_END_OF_THE_DAY, PICK_START_OF_THE_DAY, \
    ADD_BREAK_QUESTION, ADD_BREAK_ACTION, ADD_BREAK_START_TIME, ADD_BREAK_END_TIME, \
    BREAK_START_LESS_WORK_TIME, BREAK_START_EXCEED_WORK_TIME, \
    BREAK_START_EXCEED_BREAK_END, BREAK_END_LESS_WORK_TIME, BREAK_END_EXCEED_WORK_TIME, \
    BREAK_END_LESS_BREAK_START, NEXT_PAGE, NO_LABEL
from utilities.save_work_time_data_in_db import save_work_time_data_in_db
from utilities.tick_the_butthon import tick_the_button
from utilities.get_start_or_end_work_time import get_the_time_from_the_inl_keyboard

work_time_cb_query = Router(name=__name__)


@work_time_cb_query.callback_query(ReturnStepToMonthWorkTimeCbData.filter())
async def return_to_month(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=SELECT_A_MONTH,
        reply_markup=work_time_month_inl_kbd(
            month=callback_query.message.date.month,
            year=callback_query.message.date.year)
    )


@work_time_cb_query.callback_query(YearWorkTimeCbData.filter())
async def get_another_month(
        callback_query: CallbackQuery,
        callback_data: YearWorkTimeCbData,
        bot: Bot
):
    year = callback_data.year
    month = callback_query.message.date.month

    if callback_data.action == NEXT_PAGE:
        year += 1
        if year != callback_query.message.date.year:
            month = 1

    else:
        year -= 1

        if year == callback_query.message.date.year:
            pass
        elif year < callback_query.message.date.year:
            year += 1
        else:
            month = 1

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=SELECT_A_MONTH,
        reply_markup=work_time_month_inl_kbd(month=month, year=year)
    )


@work_time_cb_query.callback_query(MonthWorkTimeCbData.filter())
async def get_inl_kdb_add_days_work_time(
        callback_query: CallbackQuery,
        callback_data: MonthWorkTimeCbData,
        bot: Bot,
        state: FSMContext):
    month = callback_data.mount
    year = callback_data.year

    current_date = callback_query.message.date

    master_id = get_master_id_by_telegram_id(telegram_id=callback_query.from_user.id)

    await state.update_data(month=month, year=year)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=PICK_DAY,
        reply_markup=work_time_days_inl_kbd(
            mount=callback_data.mount,
            year=year,
            current_date=current_date,
            master_id=master_id)
    )


@work_time_cb_query.callback_query(DaysWorkTimeCbData.filter())
async def save_work_days_work_time(
        callback_query: CallbackQuery,
        callback_data: DaysWorkTimeCbData,
        bot: Bot):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    target_text = callback_data.days

    original_text = target_text.replace('✅', '')

    if '✅' in target_text:
        new_text = original_text

    else:
        new_text = '✅' + original_text

    for row in old_keyboard:
        for button in row:
            if original_text == button.text.replace('✅', ''):
                button.text = new_text
                cb_data = DaysWorkTimeCbData(days=new_text)
                button.callback_data = cb_data.pack()

    new_keyboard = InlineKeyboardMarkup(inline_keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=PICK_DAY,
        reply_markup=new_keyboard
    )


@work_time_cb_query.callback_query(NextStepTimeWorkTimeCbData.filter())
async def get_inl_kbd_add_time(
        callback_query: CallbackQuery,
        callback_data: NextStepTimeWorkTimeCbData,
        bot: Bot,
        state: FSMContext):
    cb_mount = callback_data.mount
    cb_year = callback_data.year
    cb_active_return = callback_data.active_return

    if cb_active_return:
        return await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=ADD_INTERVAL,
            reply_markup=add_interval_work_time_services_inl_kbd(mount=cb_mount, year=cb_year)
        )

    keyboard = callback_query.message.reply_markup.inline_keyboard

    active_days = []

    for row in keyboard:
        for button in row:
            if '✅' in button.text:
                active_days.append(re.sub('[^0-9]', '', button.text))

    if len(active_days) == 0:
        return await callback_query.answer(text=PICK_ONE_DAY, show_alert=True)

    await state.update_data(
        days=active_days,
    )

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_INTERVAL,
        reply_markup=add_interval_work_time_services_inl_kbd(mount=cb_mount, year=cb_year)
    )


@work_time_cb_query.callback_query(HoursIntervalWorkTimeCbData.filter())
async def get_interval_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        callback_data: HoursIntervalWorkTimeCbData
):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_INTERVAL,
        reply_markup=new_keyboard
    )


@work_time_cb_query.callback_query(IntervalNextStepTimeWorkTimeCbData.filter())
async def interval_next_step(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext
):
    cb_data = await state.get_data()
    keyboard = callback_query.message.reply_markup.inline_keyboard

    time_interval = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(time_interval) < 4:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    if time_interval == '0:00':
        return await callback_query.answer(text=INTERVAL_CANNOT_BE_0H_OM, show_alert=True)

    hours, minutes = map(int, time_interval.split(':'))
    interval = timedelta(hours=hours, minutes=minutes)

    await state.update_data(interval=interval)

    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=SELECT_WORKING_DAY,
        reply_markup=add_work_time_inl_kbd(mount=cb_data.get('month'), year=cb_data.get('year'))
    )


@work_time_cb_query.callback_query(StartWorkCbData.filter())
async def create_start_time_work(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=SELECT_WORKING_DAY,
        reply_markup=add_start_time_work_inl_kbd()
    )


@work_time_cb_query.callback_query(StartWorkTimeCbData.filter())
async def get_start_work_time(
        callback_query: CallbackQuery,
        callback_data: StartWorkTimeCbData,
        bot: Bot
):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time_start, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_START_TIME,
        reply_markup=new_keyboard
    )


@work_time_cb_query.callback_query(NextStepStartWorkTimeCbData.filter())
async def next_step_start_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext
):
    cb_data = await state.get_data()
    keyboard = callback_query.message.reply_markup.inline_keyboard

    time_start = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(time_start) != 5:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    hours, minutes = map(int, time_start.split(':'))
    time_start = timedelta(hours=hours, minutes=minutes)

    state_data = await state.get_data()
    await state.update_data(time_start=time_start)

    if state_data.get('time_end'):
        time_end = state_data.get('time_end')

    else:
        time_end = timedelta(hours=00, minutes=00)
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=add_work_time_inl_kbd(
            time_start=time_start, time_end=time_end, mount=cb_data.get('month'), year=cb_data.get('year')),
        text=SELECT_WORKING_DAY,
    )


@work_time_cb_query.callback_query(EndWorkCbData.filter())
async def create_end_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_END_TIME,
        reply_markup=add_end_time_work_inl_kbd()
    )


@work_time_cb_query.callback_query(EndWorkTimeCbData.filter())
async def get_end_work_time(
        callback_query: CallbackQuery,
        callback_data: EndWorkTimeCbData,
        bot: Bot
):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time_end, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_END_TIME,
        reply_markup=new_keyboard
    )


@work_time_cb_query.callback_query(NextStepEndWorkTimeCbData.filter())
async def next_step_end_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext
):
    cb_data = await state.get_data()
    keyboard = callback_query.message.reply_markup.inline_keyboard

    time_end = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(time_end) != 5:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    hours, minutes = map(int, time_end.split(':'))
    time_end = timedelta(hours=hours, minutes=minutes)

    state_data = await state.get_data()
    await state.update_data(time_end=time_end)

    if state_data.get('time_start'):
        time_start = state_data.get('time_start')

    else:
        time_start = timedelta(hours=00, minutes=00)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=add_work_time_inl_kbd(
            time_start=time_start, time_end=time_end, mount=cb_data.get('month'), year=cb_data.get('year')),
        text=SELECT_WORKING_DAY,
    )


@work_time_cb_query.callback_query(NextStepAddWorkTime.filter())
async def next_step_add_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext
):
    state_data = await state.get_data()

    time_start = state_data.get('time_start')
    time_end = state_data.get('time_end')
    interval = state_data.get('interval')

    if time_start is None and time_end is None:
        return await callback_query.answer(
            text=SELECT_START_AND_END_WORKING_DAY, show_alert=True)

    if time_end is None:
        return await callback_query.answer(
            text=PICK_END_OF_THE_DAY, show_alert=True)

    if time_start is None:
        return await callback_query.answer(
            text=PICK_START_OF_THE_DAY, show_alert=True)

    total_operating_time = time_end - time_start

    if total_operating_time.days < 0:
        return await callback_query.answer(
            text=BREAK_START_LESS_WORK_TIME, show_alert=True)

    if total_operating_time < interval:
        return await callback_query.answer(
            text=TOTAL_OPERATING_TIME_LESS_INTERVAL + interval,
            show_alert=True)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_BREAK_QUESTION,
        reply_markup=add_break_or_not_inl_kbd()
    )


@work_time_cb_query.callback_query(AddBreakResponseWorkTimeCbData.filter())
async def get_response_add_break(
        callback_query: CallbackQuery,
        callback_data: AddBreakResponseWorkTimeCbData,
        bot: Bot,
        state: FSMContext
):
    cb_data = callback_data.response
    state_data = await state.get_data()

    if cb_data == NO_LABEL:
        await bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id
        )

        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=TIME_ADDED,
            reply_markup=get_admin_main_menu_kbd()
        )

        master_id = get_master_id_by_telegram_id(telegram_id=callback_query.from_user.id)

        save_work_time_data_in_db(
            time_start=state_data.get('time_start'),
            time_end=state_data.get('time_end'),
            interval=state_data.get('interval'),
            days=state_data.get('days'),
            month=state_data.get('month'),
            year=state_data.get('year'),
            start_break=state_data.get('time_start_break'),
            end_break=state_data.get('time_end_break'),
            master_id=master_id
        )

        await state.clear()

        return

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_BREAK_ACTION,
        reply_markup=add_break_work_time_inl_kbd()
    )


@work_time_cb_query.callback_query(AddStartBreakWorkTime.filter())
async def create_start_break_work_time(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_BREAK_START_TIME,
        reply_markup=add_start_break_time_work_inl_kbd()
    )


@work_time_cb_query.callback_query(AddEndBreakWorkTime.filter())
async def create_end_break_work_time(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_BREAK_END_TIME,
        reply_markup=add_end_break_time_work_inl_kbd()
    )


@work_time_cb_query.callback_query(StartBreakWorkTimeCbData.filter())
async def get_start_break_work_time(
        callback_query: CallbackQuery,
        callback_data: StartBreakWorkTimeCbData,
        bot: Bot
):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time_start, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_BREAK_START_TIME,
        reply_markup=new_keyboard
    )


@work_time_cb_query.callback_query(EndBreakWorkTimeCbData.filter())
async def get_end_break_work_time(
        callback_query: CallbackQuery,
        callback_data: EndBreakWorkTimeCbData,
        bot: Bot
):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time_end, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_BREAK_END_TIME,
        reply_markup=new_keyboard
    )


@work_time_cb_query.callback_query(NextStepStartBreakWorkTimeCbData.filter())
async def next_step_start_break_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext
):
    keyboard = callback_query.message.reply_markup.inline_keyboard

    time_start_break = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(time_start_break) != 5:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    hours, minutes = map(int, time_start_break.split(':'))
    time_start_break = timedelta(hours=hours, minutes=minutes)

    state_data = await state.get_data()

    time_start = state_data.get('time_start')
    time_end = state_data.get('time_end')
    interval = state_data.get('interval')
    time_end_break = state_data.get('time_end_break')

    if time_start > time_start_break:
        return await callback_query.answer(text=BREAK_START_LESS_WORK_TIME,
                                           show_alert=True)

    if time_end < time_start_break:
        return await callback_query.answer(text=BREAK_START_EXCEED_WORK_TIME,
                                           show_alert=True)

    if time_end_break:
        if time_start_break >= time_end_break:
            return await callback_query.answer(
                text=BREAK_START_EXCEED_BREAK_END.format(time_end_break),
                show_alert=True
            )

    await state.update_data(time_start_break=time_start_break)

    if state_data.get('time_end_break'):
        time_end_break = state_data.get('time_end_break')

    else:
        time_end_break = timedelta(hours=00, minutes=00)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=add_break_work_time_inl_kbd(time_start_break=time_start_break, time_end_break=time_end_break),
        text=ADD_BREAK_ACTION,
    )


@work_time_cb_query.callback_query(NextStepEndBreakWorkTimeCbData.filter())
async def next_step_end_break_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext
):
    keyboard = callback_query.message.reply_markup.inline_keyboard

    time_end_break = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(time_end_break) != 5:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    hours, minutes = map(int, time_end_break.split(':'))
    time_end_break = timedelta(hours=hours, minutes=minutes)

    state_data = await state.get_data()

    time_start = state_data.get('time_start')
    time_end = state_data.get('time_end')
    interval = state_data.get('interval')
    time_start_break = state_data.get('time_start_break')

    if time_start > time_end_break:
        return await callback_query.answer(text=BREAK_END_LESS_WORK_TIME,
                                           show_alert=True)

    if time_end < time_end_break:
        return await callback_query.answer(text=BREAK_END_EXCEED_WORK_TIME,
                                           show_alert=True)

    if time_start_break:
        if time_end_break < time_start_break:
            return await callback_query.answer(
                text=BREAK_END_LESS_BREAK_START.format(time_start_break),
                show_alert=True
            )

    await state.update_data(time_end_break=time_end_break)

    if state_data.get('time_start_break'):
        time_start_break = state_data.get('time_start_break')

    else:
        time_start_break = timedelta(hours=00, minutes=00)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=add_break_work_time_inl_kbd(time_start_break=time_start_break, time_end_break=time_end_break),
        text=ADD_BREAK_ACTION,
    )


@work_time_cb_query.callback_query(NextStepAddBreakWorkTime.filter())
async def next_step_add_break_work_time(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    await state.clear()

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=TIME_ADDED,
        reply_markup=get_admin_main_menu_kbd()
    )

    master_id, master_obj = get_master_id_by_telegram_id(telegram_id=callback_query.from_user.id, master_object=True)

    save_work_time_data_in_db(
        time_start=state_data.get('time_start'),
        time_end=state_data.get('time_end'),
        interval=state_data.get('interval'),
        days=state_data.get('days'),
        month=state_data.get('month'),
        year=state_data.get('year'),
        start_break=state_data.get('time_start_break'),
        end_break=state_data.get('time_end_break'),
        master_id=master_id,
        master_obj=[master_obj]
    )
