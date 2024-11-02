from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.work_time_queries import get_work_time_by_month, get_day_work_time, get_break_time_by_day, \
    get_working_time_month_by_month_by_year
from telegram.keyboard_inline.timetable_get_day_inl_kbd import timetable_get_day_inl_kbd, DaysTimetableCbData, \
    BackToMonthTimetableCbData, NextStepDaysTimetableCbData
from telegram.keyboard_inline.timetable_get_info_about_work_day_inl_kbd import get_info_about_work_day, \
    SelectDayTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import MonthTimetableCbData, BackToAdminMenuTimetableCbData, \
    timetable_get_month_inl_kbd
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.params.button_admin_panel_or_main_menu import ButtonAdminPanelOrMainMenu
from telegram.params.timetable_cb_data_message import SELECT_A_DAYS, SELECT_A_MONTH, SELECT_A_DAYS_SHOW_ALERT
from utilities.get_callback_data_of_day_timetable import get_cb_data_of_day_timetable
from utilities.get_the_previous_or_next_day_timetable import get_previous_or_next_int, get_other_month
from utilities.tick_the_button_timetable import tick_the_button_timetable

timetable_cb_query = Router(name=__name__)


@timetable_cb_query.callback_query(MonthTimetableCbData.filter())
async def get_days_by_month(
        callback_query: CallbackQuery,
        callback_data: MonthTimetableCbData,
        bot: Bot
):
    month = callback_data.month
    year = callback_data.year

    days = get_work_time_by_month(month=month, year=year)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=SELECT_A_DAYS,
        reply_markup=timetable_get_day_inl_kbd(
            month=month,
            year=year,
            date_days=days,
            current_day=callback_query.message.date.day,
            current_month=callback_query.message.date.month
        )
    )


@timetable_cb_query.callback_query(BackToAdminMenuTimetableCbData.filter())
async def back_to_admin_menu_timetable(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=ButtonAdminPanelOrMainMenu.ADMIN_PANEL,
        reply_markup=get_admin_main_menu_kbd()
    )


@timetable_cb_query.callback_query(DaysTimetableCbData.filter())
async def mark_the_day(
        callback_query: CallbackQuery,
        callback_data: DaysTimetableCbData,
        bot: Bot
):
    date_day = callback_data.to_date()

    old_keyboard = callback_query.message.reply_markup.inline_keyboard
    target_text = str(date_day.day)

    current_month = callback_query.message.date.month
    if current_month == date_day.month:
        current_day = callback_query.message.date.day
    else:
        current_day = None

    if len(target_text) == 1:
        target_text = '0' + target_text

    new_keyboard = tick_the_button_timetable(keyboard=old_keyboard, target_text=target_text, current_day=current_day)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=SELECT_A_DAYS,
        reply_markup=new_keyboard
    )


@timetable_cb_query.callback_query(BackToMonthTimetableCbData.filter())
async def back_to_select_month(
        callback_query: CallbackQuery,
        callback_data: BackToMonthTimetableCbData,
        bot: Bot
):
    year = callback_data.year
    current_month = callback_query.message.date.month

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=SELECT_A_MONTH,
        reply_markup=timetable_get_month_inl_kbd(month=current_month, year=year)
    )


@timetable_cb_query.callback_query(NextStepDaysTimetableCbData.filter())
async def get_day_work_time_timetable(
        callback_query: CallbackQuery,
        bot: Bot
):
    keyboard = callback_query.message.reply_markup.inline_keyboard

    date_day = get_cb_data_of_day_timetable(keyboard=keyboard)

    if date_day is None:
        return await callback_query.answer(text=SELECT_A_DAYS_SHOW_ALERT, show_alert=True)

    work_time = get_day_work_time(date_day=date_day)
    break_time = get_break_time_by_day(date_day=date_day)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Тру тру',
        reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
    )


@timetable_cb_query.callback_query(SelectDayTimetableCbData.filter())
async def get_the_previous_or_next_day(
        callback_query: CallbackQuery,
        callback_data: SelectDayTimetableCbData,
        bot: Bot
):
    cb_data = callback_data.to_date()

    month = cb_data.get('date_day').month
    year = cb_data.get('date_day').year
    day = cb_data.get('date_day').day

    days = get_work_time_by_month(month=month, year=year, list_checker=True)

    previous_number, next_number = get_previous_or_next_int(list_integers=days, select_integer=day)

    if cb_data.get('action') == 'back':
        if previous_number:
            work_time = get_day_work_time(date_day=cb_data.get('date_day').replace(day=previous_number))
            break_time = get_break_time_by_day(date_day=cb_data.get('date_day').replace(day=previous_number))

            return await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text='Тру тру',
                reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
            )

        data_previous_month = get_other_month(
            select_year=cb_data.get('date_day').year,
            select_month=cb_data.get('date_day').month,
            action=False
        )

        if data_previous_month:
            work_time = get_day_work_time(date_day=cb_data.get('date_day').replace(
                day=data_previous_month.get('day'),
                month=data_previous_month.get('month'),
                year=data_previous_month.get('year')
            ))
            break_time = get_break_time_by_day(date_day=cb_data.get('date_day').replace(
                day=data_previous_month.get('day'),
                month=data_previous_month.get('month'),
                year=data_previous_month.get('year')
            ))

            return await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text='Тру тру',
                reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
            )

        return await callback_query.answer(text='Нет предыдущих записей.', show_alert=True)

    if cb_data.get('action') == 'next':
        if next_number:
            work_time = get_day_work_time(date_day=cb_data.get('date_day').replace(day=next_number))
            break_time = get_break_time_by_day(date_day=cb_data.get('date_day').replace(day=next_number))

            return await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text='Тру тру',
                reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
            )

        data_next_month = get_other_month(
            select_year=cb_data.get('date_day').year,
            select_month=cb_data.get('date_day').month,
            action=True
        )

        if data_next_month:
            work_time = get_day_work_time(date_day=cb_data.get('date_day').replace(
                day=data_next_month.get('day'),
                month=data_next_month.get('month'),
                year=data_next_month.get('year')
            ))
            break_time = get_break_time_by_day(date_day=cb_data.get('date_day').replace(
                day=data_next_month.get('day'),
                month=data_next_month.get('month'),
                year=data_next_month.get('year')
            ))

            return await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text='Тру тру',
                reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
            )

        return await callback_query.answer(text='Нет сдедующих записей.', show_alert=True)
