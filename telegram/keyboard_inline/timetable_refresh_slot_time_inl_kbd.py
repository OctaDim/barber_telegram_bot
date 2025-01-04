from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.keyboard_inline.timetable_get_info_about_work_day_inl_kbd import WorkTimeSlotTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL, CONTINUE_BUTTON_TXT


class TimeStartSlotTimetableCbData(CallbackData, prefix='time-start-slot'):
    action: bool


class TimeEndSlotTimetableCbData(CallbackData, prefix='time-end-slot'):
    action: bool


class ContinueRefreshSlotTimeCbData(CallbackData, prefix='continue-refresh-slot-time'):
    active: bool


def refresh_slot_time_inl_kbd(
        id_work_time: int,
        reserved_slot: bool,
        time_start: datetime = None,
        time_end: datetime = None,
):
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=f'{time_start.time().isoformat(timespec='minutes')}',
            callback_data=TimeStartSlotTimetableCbData(action=True).pack()
        ),
        InlineKeyboardButton(
            text='-',
            callback_data='-'
        ),
        InlineKeyboardButton(
            text=f'{time_end.time().isoformat(timespec='minutes')}',
            callback_data=TimeEndSlotTimetableCbData(action=True).pack()
        )
    ]

    builder.row(*buttons)

    callback_data = ContinueRefreshSlotTimeCbData(active=True).pack()
    builder.row(
        InlineKeyboardButton(
            text=CONTINUE_BUTTON_TXT,
            callback_data=callback_data)
    )

    builder.row(
        InlineKeyboardButton(
            text=RETURN,
            callback_data=WorkTimeSlotTimetableCbData(
                id_work_time=id_work_time,
                reserved_slot=reserved_slot
            ).pack()
        ),
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
