import re

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from telegram.keyboard_inline.work_time_add_days_inl_kbd import (
    work_time_days_inl_kbd,
    DaysWorkTimeCbData,
    NextStepTimeWorkTimeCbData
)

from telegram.keyboard_inline.work_time_add_duration_services_inl_kbd import (
    add_duration_services_work_time_services_inl_kbd,
    TimeServicesWorkTimeCbData, AddServiceDurationWorkTimeCbData,
)

from telegram.keyboard_inline.work_time_add_month_inl_kbd import MonthWorkTimeCbData
from telegram.keyboard_inline.work_time_add_timetable_inl_kbd import (
    add_hours_work_time_services_inl_kbd,
    HoursWorkTimeCbData,
    ServiceDurationTimeWorkTimeCbData,
)

from utilities.get_service_times import get_service_times


work_time_cb_query = Router(name=__name__)


@work_time_cb_query.callback_query(MonthWorkTimeCbData.filter())
async def get_inl_kdb_add_days_work_time(
        callback_query: CallbackQuery,
        callback_data: MonthWorkTimeCbData,
        bot: Bot,
        state: FSMContext):
    month = callback_data.mount

    await state.update_data(month=month)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выбери день или несколко дней',
        reply_markup=work_time_days_inl_kbd(mount=callback_data.mount)
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
        text='Выбери день или несколко дней',
        reply_markup=new_keyboard
    )


@work_time_cb_query.callback_query(NextStepTimeWorkTimeCbData.filter())
async def get_inl_kbd_add_time(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext):
    keyboard = callback_query.message.reply_markup.inline_keyboard

    active_days = []

    for row in keyboard:
        for button in row:
            if '✅' in button.text:
                active_days.append(re.sub('[^0-9]', '', button.text))

    if len(active_days) == 0:
        return await callback_query.answer(text='Выбери что то из дней', show_alert=True)

    await state.update_data(
        days=active_days,
        time=list(),
        time_start=list(),
        time_end=list(),
        delta=list(),
        block_hours=list(),
        block_minutes=list()
    )

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Добавьте время начало услуги.',
        reply_markup=add_hours_work_time_services_inl_kbd()
    )


@work_time_cb_query.callback_query(HoursWorkTimeCbData.filter())
async def add_start_time_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        callback_data: HoursWorkTimeCbData):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    target_text = callback_data.time
    new_text = '✅' + target_text

    for row in old_keyboard:
        for button in row:
            if target_text[-1] in button.text:
                if target_text == button.text:
                    button.text = new_text
                    cb_data = HoursWorkTimeCbData(time=target_text)
                    button.callback_data = cb_data.pack()

                else:
                    button.text = button.text.replace('✅', '')
                    cb_data = HoursWorkTimeCbData(time=button.text.replace('✅', ''))
                    button.callback_data = cb_data.pack()

    new_keyboard = InlineKeyboardMarkup(inline_keyboard=old_keyboard)

    message_text = 'Добавьте время начало услуги.'

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=message_text,
        reply_markup=new_keyboard
    )


@work_time_cb_query.callback_query(ServiceDurationTimeWorkTimeCbData.filter())
async def add_end_time_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext):

    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    time = []

    for row in old_keyboard:
        for button in row:
            if '✅' in button.text:
                time.append(button.text.replace('✅', ''))

                button.text = button.text.replace('✅', '')
                cb_data = HoursWorkTimeCbData(time=button.text)
                button.callback_data = cb_data.pack()

    state_data = await state.get_data()

    time_start: list = state_data.get('time_start')
    time_start.append(time)

    await state.update_data(time_start=time_start)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Введите продолжительность услуги',
        reply_markup=add_duration_services_work_time_services_inl_kbd()
    )


@work_time_cb_query.callback_query(TimeServicesWorkTimeCbData.filter())
async def get_duration_services_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        callback_data: TimeServicesWorkTimeCbData):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    cb_data = callback_data.time_start.split()
    target_text = cb_data[-1]

    new_text = '✅' + target_text

    for row in old_keyboard:
        for button in row:
            if target_text[-1] in button.text:
                if target_text == button.text:
                    button.text = new_text

                else:
                    button.text = button.text.replace('✅', '')

    new_keyboard = InlineKeyboardMarkup(inline_keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Введите продолжительность услуги',
        reply_markup=new_keyboard
    )


@work_time_cb_query.callback_query(AddServiceDurationWorkTimeCbData.filter())
async def add_duration_services_work_time(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext,):

    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    time_duration = []

    for row in old_keyboard:
        for button in row:
            if '✅' in button.text:
                btn_cb_data = button.callback_data.split(':')
                time_duration.append(btn_cb_data[-1])

    if len(time_duration) != 2:
        return await callback_query.answer(text='Выбери что то из времени', show_alert=True)

    state_data = await state.get_data()

    state_time_duration: list = state_data.get('time')
    state_time_duration.append(time_duration)

    state_block_minutes: list = state_data.get('block_minutes')

    data = get_service_times(
        start_time=state_data.get('time_start')[-1],
        time_duration=state_time_duration[-1],
        block_hour=state_data.get('block_hours'),
        block_minutes=state_block_minutes
    )

    state_time_start: list = state_data.get('time_start')
    state_time_start.append(data.get('start_time'))

    state_time_end: list = state_data.get('time_end')
    state_time_end.append(data.get('end_time'))

    await state.update_data(
        time_duration_service=state_time_duration,
        block_hours=data.get('block_hour'),
        block_minutes=data.get('block_minute'),
        time_start=state_time_start,
        time_end=state_time_end

    )

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f'Начало {data.get('start_time')}, конец {data.get('end_time')}',
    )

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text='Отлично, давай еще',
        reply_markup=add_hours_work_time_services_inl_kbd(block_hour=data.get('block_hour'))
    )
