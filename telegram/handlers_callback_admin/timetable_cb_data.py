from datetime import datetime, timedelta

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.db_queries.create_user_query import create_service_using_the_master
from database.db_queries.get_master_obj_by_telegram_id import get_master_id_by_telegram_id
from database.db_queries.work_time_queries import get_work_time_by_month, get_day_work_time, get_break_time_by_day, \
    get_one_slots, update_time_start_and_time_end, \
    create_break_time, create_work_time_by_break_time, make_slot_inactive_or_active

from telegram.filters.reserved_slot_filter import ReservedSlotFilter
from telegram.handlers_admin.timetable_btn_admin import add_name_new_client

from telegram.keyboard_inline.common_buttons_inline import create_return_inline_button
from telegram.keyboard_inline.timetable_add_interval_work_time_inl_kbd import add_work_time_interval_inl_kbd, \
    AddIntervalWorkTimeCbData, AddIntervalNextStepTimeWorkTimeCbData
from telegram.keyboard_inline.timetable_add_more_work_time_inl_kbd import add_more_work_time_inl_kbd, \
    CurrentTimeStartWorkTimeCbData, CurrentTimeEndWorkTimeCbData, NextStepAddNewWorkTimeCbData
from telegram.keyboard_inline.timetable_add_new_end_work_time_inl_kbd import NewTimeEndWorkTimeTimetableCbData, \
    NextStepEndTimeWorkTimeTimetableCbData, add_new_time_end_work_time_inl_kbd
from telegram.keyboard_inline.timetable_add_new_time_start_slot_inl_kbd import add_new_time_start_slot, \
    NewTimeStartSlotTimetableCbData, NextStepStartTimeSlotTimetableCbData
from telegram.keyboard_inline.timetable_add_new_time_start_work_time_inl_kbd import \
    add_new_time_start_work_time_inl_kbd, NewTimeStartWorkTimeTimetableCbData, NextStepStartTimeWorkTimeTimetableCbData
from telegram.keyboard_inline.timetable_add_time_end_slot_inl_kbd import add_new_time_end_slot, \
    NewTimeEndSlotTimetableCbData, NextStepEndTimeSlotTimetableCbData
from telegram.keyboard_inline.timetable_get_action_break_time import get_action_break_time_inl_kbd, \
    GetBreakIdTimeTableCbData
from telegram.keyboard_inline.timetable_get_actions_for_not_reserved_slot import get_actions_for_not_reserved_slot, \
    BlockOutTimeCbData, ChangeTimeSlot, AddClientToSlot
from telegram.keyboard_inline.timetable_get_all_services_inl_kbd import AddServiceTimetableCbData
from telegram.keyboard_inline.timetable_get_day_inl_kbd import timetable_get_day_inl_kbd, DaysTimetableCbData, \
    BackToMonthTimetableCbData, NextStepDaysTimetableCbData
from telegram.keyboard_inline.timetable_get_info_about_work_day_inl_kbd import get_info_about_work_day, \
    SelectDayTimetableCbData, WorkTimeSlotTimetableCbData, BreakTimeSlotTimetableCbData, PageNumberSlotTimetableCbData, \
    AddMoreWorkTimeTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import MonthTimetableCbData, BackToAdminMenuTimetableCbData, \
    timetable_get_month_inl_kbd
from telegram.keyboard_inline.timetable_refresh_slot_time_inl_kbd import refresh_slot_time_inl_kbd, \
    TimeStartSlotTimetableCbData, TimeEndSlotTimetableCbData, ContinueRefreshSlotTimeCbData
from telegram.keyboard_inline.timetable_return_to_get_info_about_day_inl_kbd import return_to_get_info_about_day

from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd

from telegram.params.button_admin_panel_or_main_menu import ButtonAdminPanelOrMainMenu
from telegram.params.messages import SUCCESSFULLY
from telegram.params.timetable_cb_data_message import SELECT_A_DAYS, SELECT_A_MONTH, SELECT_A_DAYS_SHOW_ALERT, \
    SLOT_MANAGEMENT
from telegram.params.work_time_cb_data_message import CHOOSE_TWO_VALUE, ADD_INTERVAL, INTERVAL_CANNOT_BE_0H_OM, RETURN

from telegram.telegram_utils.fsm_states_utils import get_valid_list_by_fsm_state_key
from utilities.calendar_utils import get_month_name_by_number

from utilities.get_callback_data_of_day_timetable import get_cb_data_of_day_timetable
from utilities.get_info_about_reserved_slot import get_info_about_reserved_slot
from utilities.get_start_or_end_work_time import get_the_time_from_the_inl_keyboard
from utilities.get_the_previous_or_next_day_timetable import get_previous_or_next_int, get_other_month
from utilities.save_work_time_data_in_db import save_work_time_data_in_db
from utilities.tick_the_butthon import tick_the_button
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

    master_id = get_master_id_by_telegram_id(telegram_id=callback_query.from_user.id)

    days = get_work_time_by_month(month=month, year=year, master_id=master_id)

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
        state: FSMContext,
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

    await state.clear()


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
        callback_data: NextStepDaysTimetableCbData,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()
    state_date_day = state_data.get('date_day')
    print(state_date_day)

    if state_date_day is None:
        keyboard = callback_query.message.reply_markup.inline_keyboard

        date_day = get_cb_data_of_day_timetable(keyboard=keyboard)

        if date_day is None:
            return await callback_query.answer(
                text=SELECT_A_DAYS_SHOW_ALERT, show_alert=True)
    else:
        date_day = state_date_day

    work_time = get_day_work_time(date_day=date_day)
    break_time = get_break_time_by_day(date_day=date_day)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=SLOT_MANAGEMENT,
        reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
    )
    print(date_day)
    await state.update_data(date_day=date_day)


@timetable_cb_query.callback_query(SelectDayTimetableCbData.filter())
async def get_the_previous_or_next_day(
        callback_query: CallbackQuery,
        state: FSMContext,
        callback_data: SelectDayTimetableCbData,
        bot: Bot
):
    cb_data = callback_data.to_date()

    month = cb_data.get('date_day').month
    year = cb_data.get('date_day').year
    day = cb_data.get('date_day').day

    master_id = get_master_id_by_telegram_id(telegram_id=callback_query.from_user.id)

    days = get_work_time_by_month(month=month, year=year, list_checker=True, master_id=master_id)

    previous_number, next_number = get_previous_or_next_int(list_integers=days, select_integer=day)

    if cb_data.get('action') == 'back':
        if previous_number:
            work_time = get_day_work_time(date_day=cb_data.get('date_day').replace(day=previous_number))
            break_time = get_break_time_by_day(date_day=cb_data.get('date_day').replace(day=previous_number))

            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=SLOT_MANAGEMENT,
                reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
            )

            return await state.update_data(date_day=cb_data.get('date_day').replace(day=previous_number))

        data_previous_month = get_other_month(
            select_year=cb_data.get('date_day').year,
            select_month=cb_data.get('date_day').month,
            action=False,
            master_id=master_id
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

            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,

                message_id=callback_query.message.message_id,
                text=SLOT_MANAGEMENT,
                reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
            )

            return await state.update_data(date_day=cb_data.get('date_day').replace(
                day=data_previous_month.get('day'),
                month=data_previous_month.get('month'),
                year=data_previous_month.get('year')))

        return await callback_query.answer(text='Нет предыдущих записей.', show_alert=True)

    if cb_data.get('action') == 'next':
        if next_number:
            work_time = get_day_work_time(date_day=cb_data.get('date_day').replace(day=next_number))
            break_time = get_break_time_by_day(date_day=cb_data.get('date_day').replace(day=next_number))

            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=SLOT_MANAGEMENT,
                reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
            )

            return await state.update_data(date_day=cb_data.get('date_day').replace(day=next_number))

        data_next_month = get_other_month(
            select_year=cb_data.get('date_day').year,
            select_month=cb_data.get('date_day').month,
            action=True,
            master_id=master_id
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

            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=SLOT_MANAGEMENT,
                reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
            )

            return await state.update_data(date_day=cb_data.get('date_day').replace(
                day=data_next_month.get('day'),
                month=data_next_month.get('month'),
                year=data_next_month.get('year')))

        return await callback_query.answer(text='Нет сдедующих записей.', show_alert=True)


@timetable_cb_query.callback_query(WorkTimeSlotTimetableCbData.filter(), ReservedSlotFilter())
async def get_about_info_by_slot(
        callback_query: CallbackQuery,
        callback_data: WorkTimeSlotTimetableCbData,
        bot: Bot
):
    cb_data = callback_data.dict()

    if cb_data.get('reserved_slot'):
        slot = get_one_slots(work_time_id=cb_data.get('id_work_time'))
        text = get_info_about_reserved_slot(slot=slot)

        await bot.edit_message_text(
            message_id=callback_query.message.message_id,
            chat_id=callback_query.message.chat.id,
            text=text,
            disable_web_page_preview=True,
            reply_markup=return_to_get_info_about_day()
        )


@timetable_cb_query.callback_query(WorkTimeSlotTimetableCbData.filter())
async def get_action_by_clear_slot(
        callback_query: CallbackQuery,
        callback_data: WorkTimeSlotTimetableCbData,
        state: FSMContext,
        bot: Bot
):
    work_time_id = callback_data.id_work_time
    reserved_slot = callback_data.reserved_slot

    work_time_obj = get_one_slots(work_time_id=work_time_id)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Select action.',
        reply_markup=get_actions_for_not_reserved_slot(
            work_time_id=work_time_id,
            work_time_active=work_time_obj.active,
        )
    )

    await state.update_data(
        work_time_id=work_time_id,
        reserved_slot=reserved_slot
    )


@timetable_cb_query.callback_query(BlockOutTimeCbData.filter())
async def block_out_time_slot(
        callback_query: CallbackQuery,
        callback_data: BlockOutTimeCbData,
        state: FSMContext,
        bot: Bot
):
    work_time_id = callback_data.work_time_id

    make_slot_inactive_or_active(work_time_id=work_time_id)

    await callback_query.answer(text=SUCCESSFULLY, show_alert=True)

    state_data = await state.get_data()

    work_time = get_day_work_time(date_day=state_data.get('date_day'))
    break_time = get_break_time_by_day(date_day=state_data.get('date_day'))

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=SLOT_MANAGEMENT,
        reply_markup=get_info_about_work_day(work_time=work_time, break_time=break_time)
    )


@timetable_cb_query.callback_query(ChangeTimeSlot.filter())
async def change_slot_time(
        callback_query: CallbackQuery,
        callback_data: ChangeTimeSlot,
        state: FSMContext,
        bot: Bot
):
    slot = get_one_slots(work_time_id=callback_data.work_time_id)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Введите новое время',
        reply_markup=refresh_slot_time_inl_kbd(
            time_start=slot.time_start,
            time_end=slot.time_end,
            reserved_slot=slot.reserved,
            id_work_time=slot.id
        )
    )

    await state.update_data(
        work_time_obj=slot,
        time_start_slot=slot.time_start,
        time_end_slot=slot.time_end
    )


@timetable_cb_query.callback_query(TimeStartSlotTimetableCbData.filter())
async def get_inl_kbd_add_new_time_start(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Введите новое время начала слота',
        reply_markup=add_new_time_start_slot()
    )


@timetable_cb_query.callback_query(NewTimeStartSlotTimetableCbData.filter())
async def get_start_time_slot(
        callback_query: CallbackQuery,
        callback_data: NewTimeStartSlotTimetableCbData,
        bot: Bot
):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time_start, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Введите новое время начала слота',
        reply_markup=new_keyboard
    )


@timetable_cb_query.callback_query(NextStepStartTimeSlotTimetableCbData.filter())
async def next_step_start_time_slot(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    cb_data = await state.get_data()
    keyboard = callback_query.message.reply_markup.inline_keyboard

    time_start = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(time_start) != 5:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    time_start = datetime.strptime(time_start, "%H:%M").time()
    work_time_obj = cb_data.get('work_time_obj')

    if time_start <= work_time_obj.time_start.time():
        return await callback_query.answer(text='Новое время не может быть меньше или равно старому', show_alert=True)

    if time_start >= work_time_obj.time_end.time():
        return await callback_query.answer(text='Новое врем не может начинаться позднее чем старое', show_alert=True)

    time_end = cb_data.get('time_end_slot')
    time_start = work_time_obj.time_start.replace(hour=time_start.hour, minute=time_start.minute)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Введите новое время',
        reply_markup=refresh_slot_time_inl_kbd(
            time_start=time_start,
            time_end=time_end,
            id_work_time=work_time_obj.id,
            reserved_slot=work_time_obj.reserved
        )
    )

    await state.update_data(time_start_slot=time_start)


@timetable_cb_query.callback_query(TimeEndSlotTimetableCbData.filter())
async def get_inl_kbd_add_new_time_end(
        callback_query: CallbackQuery,
        bot: Bot
):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Введите новое время конца слота',
        reply_markup=add_new_time_end_slot()
    )


@timetable_cb_query.callback_query(NewTimeEndSlotTimetableCbData.filter())
async def get_end_time_slot(
        callback_query: CallbackQuery,
        callback_data: NewTimeEndSlotTimetableCbData,
        bot: Bot
):
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time_end, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Введите новое время конца слота',
        reply_markup=new_keyboard
    )


@timetable_cb_query.callback_query(NextStepEndTimeSlotTimetableCbData.filter())
async def next_step_end_time_slot(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    cb_data = await state.get_data()
    keyboard = callback_query.message.reply_markup.inline_keyboard

    time_end = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(time_end) != 5:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    time_end = datetime.strptime(time_end, "%H:%M").time()
    work_time_obj = cb_data.get('work_time_obj')

    if time_end >= work_time_obj.time_end.time():
        return await callback_query.answer(text='Новое время не может быть меньше или равно старому', show_alert=True)

    if time_end <= work_time_obj.time_start.time():
        return await callback_query.answer(text='Новое врем не может начинаться позднее чем старое', show_alert=True)

    time_start = cb_data.get('time_start_slot')
    time_end = work_time_obj.time_end.replace(hour=time_end.hour, minute=time_end.minute)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Введите новое время',
        reply_markup=refresh_slot_time_inl_kbd(
            time_start=time_start,
            time_end=work_time_obj.time_end.replace(hour=time_end.hour, minute=time_end.minute),
            id_work_time=work_time_obj.id,
            reserved_slot=work_time_obj.reserved
        )
    )

    await state.update_data(time_end_slot=time_end)


@timetable_cb_query.callback_query(ContinueRefreshSlotTimeCbData.filter())
async def refresh_slot_time(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    work_time_obj = state_data.get('work_time_obj')
    slot_duration = state_data.get('time_end_slot') - state_data.get('time_start_slot')

    data = {
        'time_start': state_data.get('time_start_slot'),
        'time_end': state_data.get('time_end_slot'),
        'slot_duration': slot_duration
    }

    result = update_time_start_and_time_end(
        work_time_obj=work_time_obj,
        data=data
    )

    if result:
        await callback_query.answer(text='Успешно', show_alert=True)

        if work_time_obj.time_end == data.get('time_end'):
            create_break_time(
                end_break=data.get('time_start'),
                start_break=work_time_obj.time_start,
                master_obj=[work_time_obj.work_time_masters]
            )
        elif work_time_obj.time_start == data.get('time_start'):
            create_break_time(
                start_break=data.get('time_end'),
                end_break=work_time_obj.time_end,
                master_obj=[work_time_obj.work_time_masters]
            )
        else:
            create_break_time(
                start_break=work_time_obj.time_start,
                end_break=data.get('time_start'),
                master_obj=[work_time_obj.work_time_masters]
            )

            create_break_time(
                start_break=data.get('time_end'),
                end_break=work_time_obj.time_end,
                master_obj=[work_time_obj.work_time_masters]
            )

        work_time_list = get_day_work_time(date_day=work_time_obj.time_start.date())
        break_time_list = get_break_time_by_day(date_day=work_time_obj.time_start.date())

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите действие',
            reply_markup=get_info_about_work_day(work_time=work_time_list, break_time=break_time_list)
        )


@timetable_cb_query.callback_query(BreakTimeSlotTimetableCbData.filter())
async def get_action_break_time(
        callback_query: CallbackQuery,
        callback_data: BreakTimeSlotTimetableCbData,
        bot: Bot
):
    cb_data = callback_data.id_break_time

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Select action',
        reply_markup=get_action_break_time_inl_kbd(break_id=cb_data)
    )


@timetable_cb_query.callback_query(GetBreakIdTimeTableCbData.filter())
async def create_new_work_time(
        callback_query: CallbackQuery,
        callback_data: GetBreakIdTimeTableCbData,
        bot: Bot
):
    break_id = callback_data.break_id

    date_day = create_work_time_by_break_time(break_id=break_id)

    await callback_query.answer(text='Успешно', show_alert=True)

    work_time_list = get_day_work_time(date_day=date_day)
    break_time_list = get_break_time_by_day(date_day=date_day)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите действие',
        reply_markup=get_info_about_work_day(work_time=work_time_list, break_time=break_time_list)
    )


@timetable_cb_query.callback_query(PageNumberSlotTimetableCbData.filter())
async def get_new_page(
        callback_query: CallbackQuery,
        callback_data: PageNumberSlotTimetableCbData,
        bot: Bot
):
    cb_data = callback_data.to_date()

    work_time_list = get_day_work_time(date_day=cb_data.get('date_day'))
    break_time_list = get_break_time_by_day(date_day=cb_data.get('date_day'))

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите действие',
        reply_markup=get_info_about_work_day(
            work_time=work_time_list,
            break_time=break_time_list,
            page=cb_data.get('page'))
    )


@timetable_cb_query.callback_query(AddMoreWorkTimeTimetableCbData.filter())
async def add_more_work_time(
        callback_query: CallbackQuery,
        callback_data: AddMoreWorkTimeTimetableCbData,
        state: FSMContext,
        bot: Bot
):
    cb_data = callback_data.to_date()

    current_time_start_work_day = cb_data.get('time_start_work_day')
    current_time_end_work_day = cb_data.get('time_end_work_day')

    await state.clear()

    await state.update_data(
        current_time_start_work_day=cb_data.get('time_start_work_day'),
        current_time_end_work_day=cb_data.get('time_end_work_day'),
        date_day=cb_data.get('time_end_work_day')
    )

    text = (f'Текущее время работы составляет: \n'
            f'{current_time_start_work_day.time().strftime("%H:%M")} - '
            f'{current_time_end_work_day.time().strftime("%H:%M")}')

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=add_more_work_time_inl_kbd(
            time_start=current_time_start_work_day,
            time_end=current_time_end_work_day
        ),
        parse_mode='Markdown'
    )


@timetable_cb_query.callback_query(CurrentTimeStartWorkTimeCbData.filter())
async def get_inl_kbd_add_new_time_start_work_time(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    text = (f'Текущее время работы составляет: \n'
            f'{state_data.get("current_time_start_work_day").time().strftime("%H:%M")} - '
            f'{state_data.get("current_time_end_work_day").time().strftime("%H:%M")}')

    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=text,
        reply_markup=add_new_time_start_work_time_inl_kbd(),
        parse_mode='Markdown'
    )


@timetable_cb_query.callback_query(NewTimeStartWorkTimeTimetableCbData.filter())
async def get_selected_time_start_work_time(
        callback_query: CallbackQuery,
        callback_data: NewTimeStartWorkTimeTimetableCbData,
        bot: Bot
):
    text = callback_query.message.text
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time_start, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=new_keyboard
    )


@timetable_cb_query.callback_query(NextStepStartTimeWorkTimeTimetableCbData.filter())
async def add_new_time_start_work_time(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()
    keyboard = callback_query.message.reply_markup.inline_keyboard

    time_start = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(time_start) != 5:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    new_time_start = datetime.strptime(time_start, "%H:%M").time()

    current_time_start = state_data.get('current_time_start_work_day').time()
    current_time_end = state_data.get('current_time_end_work_day').time()

    if current_time_start <= new_time_start < current_time_end or new_time_start == current_time_start:
        return await callback_query.answer(
            text=f'Вы добавили интервал, начинающийся в {new_time_start.strftime('%H:%M')},'
                 f' но он пересекается с основным рабочим временем {current_time_start.strftime('%H:%M')} - '
                 f'{current_time_end.strftime('%H:%M')}',
            show_alert=True)

    if state_data.get('time_end_slot'):
        time_end = state_data.get('time_end_slot').time()

        if new_time_start == time_end:
            return await callback_query.answer(
                text='Время начала и окончания работы не могут совпадать. Пожалуйста, введите корректное время окончания.',
                show_alert=True
            )

        if new_time_start > time_end:
            return await callback_query.answer(
                text=f'Время окончания работы {time_end.strftime('%H:%M')} не может быть раньше времени начала'
                     f' {new_time_start.strftime('%H:%M')}. Пожалуйста, введите корректное время окончания.',
                show_alert=True
            )

    new_time_start_datetime = datetime.combine(state_data.get('current_time_start_work_day').date(), new_time_start)

    await state.update_data(time_start_slot=new_time_start_datetime)

    text = callback_query.message.text

    if state_data.get('time_end_slot'):
        time_end = state_data.get('time_end_slot')
    else:
        time_end = state_data.get('current_time_end_work_day')

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=add_more_work_time_inl_kbd(
            time_start=new_time_start_datetime,
            time_end=time_end
        ),
        parse_mode='Markdown'
    )


@timetable_cb_query.callback_query(CurrentTimeEndWorkTimeCbData.filter())
async def get_inl_kbd_add_new_end_start_work_time(
        callback_query: CallbackQuery,
        bot: Bot
):
    text = callback_query.message.text

    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        reply_markup=add_new_time_end_work_time_inl_kbd(),
        text=text
    )


@timetable_cb_query.callback_query(NewTimeEndWorkTimeTimetableCbData.filter())
async def get_selected_time_end_work_time(
        callback_query: CallbackQuery,
        callback_data: NewTimeEndWorkTimeTimetableCbData,
        bot: Bot
):
    text = callback_query.message.text
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time_start, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=new_keyboard
    )


@timetable_cb_query.callback_query(NextStepEndTimeWorkTimeTimetableCbData.filter())
async def add_new_time_end_work_time(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()
    keyboard = callback_query.message.reply_markup.inline_keyboard

    time_end = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(time_end) != 5:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    time_start = state_data.get('time_start_slot')
    time_end = datetime.strptime(time_end, '%H:%M').time()

    if state_data.get('time_start_slot'):
        if time_start.time() > time_end:
            return await callback_query.answer(
                text=f'Время окончания работы {time_end.strftime('%H:%M')} не может быть раньше времени начала'
                     f' {time_start.strftime('%H:%M')}. Пожалуйста, введите корректное время окончания.',
                show_alert=True)

        if time_start.time() == time_end:
            return await callback_query.answer(
                text='Время начала и окончания работы не могут совпадать. Пожалуйста, введите корректное время окончания.',
                show_alert=True
            )

    new_time_end_datetime = datetime.combine(state_data.get('current_time_start_work_day').date(), time_end)

    await state.update_data(time_end_slot=new_time_end_datetime)

    text = callback_query.message.text

    if time_start is None:
        time_start = state_data.get('current_time_start_work_day')

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=add_more_work_time_inl_kbd(
            time_start=time_start,
            time_end=new_time_end_datetime
        ),
        parse_mode='Markdown'
    )


@timetable_cb_query.callback_query(NextStepAddNewWorkTimeCbData.filter())
async def add_slot_duration_work_time(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    if state_data.get('time_start_slot') is None and state_data.get('time_end_slot') is None:
        await callback_query.answer(text='Так нельзя', show_alert=True)
        return

    work_time = get_day_work_time(date_day=state_data.get('date_day'))

    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=ADD_INTERVAL,
        reply_markup=add_work_time_interval_inl_kbd(work_time=work_time)
    )


@timetable_cb_query.callback_query(AddIntervalWorkTimeCbData.filter())
async def get_selected_slot_duration_work_time(
        callback_query: CallbackQuery,
        callback_data: AddIntervalWorkTimeCbData,
        bot: Bot
):
    text = callback_query.message.text
    old_keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = tick_the_button(target_text=callback_data.time, keyboard=old_keyboard)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=new_keyboard
    )


@timetable_cb_query.callback_query(AddIntervalNextStepTimeWorkTimeCbData.filter())
async def next_step_add_interval_work_time(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    keyboard = callback_query.message.reply_markup.inline_keyboard

    slot_duration = get_the_time_from_the_inl_keyboard(keyboard=keyboard)

    if len(slot_duration) < 4:
        return await callback_query.answer(text=CHOOSE_TWO_VALUE, show_alert=True)

    if slot_duration == '0:00':
        return await callback_query.answer(text=INTERVAL_CANNOT_BE_0H_OM, show_alert=True)

    state_data = await state.get_data()

    slot_duration = datetime.strptime(slot_duration, '%H:%M').time()

    time_start_slot = state_data.get('time_start_slot')
    time_end_slot = state_data.get('time_end_slot')
    current_time_start_work_day = state_data.get('current_time_start_work_day')
    current_time_end_work_day = state_data.get('current_time_end_work_day')

    month = get_month_name_by_number(current_time_start_work_day.month)

    work_time_list = get_day_work_time(date_day=current_time_start_work_day.date())

    if time_start_slot is None and time_end_slot.time() > current_time_end_work_day.time():

        await callback_query.answer(text='SUCCESSFULLY', show_alert=True)

        save_work_time_data_in_db(
            time_start=timedelta(hours=current_time_end_work_day.hour, minutes=current_time_end_work_day.minute),
            time_end=timedelta(hours=time_end_slot.hour, minutes=time_end_slot.minute),
            interval=timedelta(hours=slot_duration.hour, minutes=slot_duration.minute),
            start_break=None,
            end_break=None,
            month=month,
            year=current_time_start_work_day.year,
            days=[current_time_start_work_day.day],
            master_id=work_time_list[0].work_time_masters.id
        )

        work_time_list = get_day_work_time(date_day=current_time_start_work_day.date())
        break_time_list = get_break_time_by_day(date_day=current_time_start_work_day.date())

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите действие',
            reply_markup=get_info_about_work_day(
                work_time=work_time_list,
                break_time=break_time_list
            )
        )

        return

    elif time_end_slot is None or (time_start_slot.time() < current_time_start_work_day.time()) and (
            current_time_start_work_day.time() <= time_end_slot.time() <= current_time_end_work_day.time()):

        await callback_query.answer(text='SUCCESSFULLY', show_alert=True)

        save_work_time_data_in_db(
            time_start=timedelta(hours=time_start_slot.hour, minutes=time_start_slot.minute),
            time_end=timedelta(hours=current_time_start_work_day.hour, minutes=current_time_start_work_day.minute),
            interval=timedelta(hours=slot_duration.hour, minutes=slot_duration.minute),
            start_break=None,
            end_break=None,
            month=month,
            year=current_time_start_work_day.year,
            days=[current_time_start_work_day.day],
            master_id=work_time_list[0].work_time_masters.id,
        )

        work_time_list = get_day_work_time(date_day=current_time_start_work_day.date())
        break_time_list = get_break_time_by_day(date_day=current_time_start_work_day.date())

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите действие',
            reply_markup=get_info_about_work_day(
                work_time=work_time_list,
                break_time=break_time_list
            )
        )

        return

    elif time_end_slot.time() > current_time_end_work_day.time() and (
            time_start_slot.time() < current_time_start_work_day.time()):

        await callback_query.answer(text='SUCCESSFULLY', show_alert=True)

        save_work_time_data_in_db(
            time_start=timedelta(hours=time_start_slot.hour, minutes=time_start_slot.minute),
            time_end=timedelta(hours=current_time_start_work_day.hour, minutes=current_time_start_work_day.minute),
            interval=timedelta(hours=slot_duration.hour, minutes=slot_duration.minute),
            start_break=None,
            end_break=None,
            month=month,
            year=current_time_start_work_day.year,
            days=[current_time_start_work_day.day],
            master_id=work_time_list[0].work_time_masters.id
        )

        save_work_time_data_in_db(
            time_start=timedelta(hours=current_time_end_work_day.hour, minutes=current_time_end_work_day.minute),
            time_end=timedelta(hours=time_end_slot.hour, minutes=time_end_slot.minute),
            interval=timedelta(hours=slot_duration.hour, minutes=slot_duration.minute),
            start_break=None,
            end_break=None,
            month=month,
            year=current_time_start_work_day.year,
            days=[current_time_start_work_day.day],
            master_id=work_time_list[0].work_time_masters.id
        )

        work_time_list = get_day_work_time(date_day=current_time_start_work_day.date())
        break_time_list = get_break_time_by_day(date_day=current_time_start_work_day.date())

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите действие',
            reply_markup=get_info_about_work_day(
                work_time=work_time_list,
                break_time=break_time_list
            )
        )

        return

    elif time_end_slot.time() < current_time_start_work_day.time():
        await callback_query.answer(text='SUCCESSFULLY', show_alert=True)

        master_obj = work_time_list[0].work_time_masters.id

        save_work_time_data_in_db(
            time_start=timedelta(hours=time_start_slot.hour, minutes=time_start_slot.minute),
            time_end=timedelta(hours=time_end_slot.hour, minutes=time_end_slot.minute),
            interval=timedelta(hours=slot_duration.hour, minutes=slot_duration.minute),
            start_break=timedelta(hours=time_end_slot.hour, minutes=time_end_slot.minute),
            end_break=timedelta(hours=current_time_start_work_day.hour, minutes=current_time_start_work_day.minute),
            month=month,
            year=current_time_start_work_day.year,
            days=[current_time_start_work_day.day],
            master_id=work_time_list[0].work_time_masters.id,
            master_obj=master_obj
        )

        work_time_list = get_day_work_time(date_day=current_time_start_work_day.date())
        break_time_list = get_break_time_by_day(date_day=current_time_start_work_day.date())

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите действие',
            reply_markup=get_info_about_work_day(
                work_time=work_time_list,
                break_time=break_time_list
            )
        )

        return

    else:
        await callback_query.answer(text='SUCCESSFULLY', show_alert=True)

        master_obj = work_time_list[0].work_time_masters.id

        save_work_time_data_in_db(
            time_start=timedelta(hours=time_start_slot.hour, minutes=time_start_slot.minute),
            time_end=timedelta(hours=time_end_slot.hour, minutes=time_end_slot.minute),
            interval=timedelta(hours=slot_duration.hour, minutes=slot_duration.minute),
            start_break=timedelta(hours=current_time_end_work_day.hour, minutes=current_time_end_work_day.minute),
            end_break=timedelta(hours=time_start_slot.hour, minutes=time_start_slot.minute),
            month=month,
            year=current_time_start_work_day.year,
            days=[current_time_start_work_day.day],
            master_id=work_time_list[0].work_time_masters.id,
            master_obj=master_obj
        )

        work_time_list = get_day_work_time(date_day=current_time_start_work_day.date())
        break_time_list = get_break_time_by_day(date_day=current_time_start_work_day.date())

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите действие',
            reply_markup=get_info_about_work_day(
                work_time=work_time_list,
                break_time=break_time_list
            )
        )

        return


@timetable_cb_query.callback_query(AddClientToSlot.filter())
async def add_new_client(
        callback_query: CallbackQuery,
        callback_data: AddClientToSlot,
        state: FSMContext,
        bot: Bot
):
    await state.update_data(work_time_id=callback_data.work_time_id)

    await add_name_new_client(message=callback_query.message, state=state, bot=bot)


@timetable_cb_query.callback_query(AddServiceTimetableCbData.filter())
async def add_new_service(
        callback_query: CallbackQuery,
        callback_data: AddServiceTimetableCbData,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()
    messages_id = state_data.get('messages_id')

    await bot.delete_messages(chat_id=callback_query.message.chat.id, message_ids=messages_id)

    data = {
        'first_name': state_data.get('name_new_client'),
        'phone_number': state_data.get('phone_new_client'),
        'service_id': callback_data.service_id,
        'work_time_id': state_data.get('work_time_id')
    }

    date_day = create_service_using_the_master(data=data)

    work_time_list = get_day_work_time(date_day=date_day.date())
    break_time_list = get_break_time_by_day(date_day=date_day.date())

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text='Admin Panel',
        reply_markup=get_info_about_work_day(
            work_time=work_time_list,
            break_time=break_time_list
        )
    )

    await state.clear()
