from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.keyboard_inline.timetable_get_day_inl_kbd import BackToMonthTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import MonthTimetableCbData
from utilities.get_select_date_for_timetable import get_select_date


class SelectDayTimetableCbData(CallbackData, prefix='select-day-timetable'):
    action: str
    date_day: str

    @classmethod
    def from_date(cls, date_day: datetime.date, action: str):
        return cls(date_day=date_day.isoformat(), action=action)

    def to_date(self) -> dict:
        data = {
            'date_day': datetime.fromisoformat(self.date_day).date(),
            'action': self.action
        }
        return data


class WorkTimeSlotTimetableCbData(CallbackData, prefix='work-time-slot-timetable', sep='|'):
    id_work_time: int


class BreakTimeSlotTimetableCbData(CallbackData, prefix='break-time-slot-timetable', sep='|'):
    id_break_time: int


def get_info_about_work_day(work_time: list, break_time):
    builder = InlineKeyboardBuilder()
    date = work_time[0].time_start
    date_data = get_select_date(date=date)

    if break_time:
        break_time_start_str = break_time.start_break.strftime('%H:%M')
        break_time_end_str = break_time.end_break.strftime('%H:%M')

    builder.row(InlineKeyboardButton(
        text=date_data.get('month'),
        callback_data=BackToMonthTimetableCbData(year=date.year).pack()))

    second_row = [
        InlineKeyboardButton(text='<<', callback_data=SelectDayTimetableCbData.from_date(action='back',
                                                                                         date_day=date.date()).pack()),
        InlineKeyboardButton(text=f'{date_data.get('weekday')}',
                             callback_data=MonthTimetableCbData(year=date.year, month=date.month).pack()),
        InlineKeyboardButton(text='>>', callback_data=SelectDayTimetableCbData.from_date(action='next',
                                                                                         date_day=date.date()).pack())
    ]

    builder.row(*second_row)

    for slot in work_time:
        time_start_str = slot.time_start.strftime('%H:%M')
        time_end_str = slot.time_end.strftime('%H:%M')

        if slot.reserved is False:
            reserved_text = 'Свободно'

        else:
            reserved_text = 'Павел Наркевич'

        buttons = [
            InlineKeyboardButton(
                text=f'{time_start_str}-{time_end_str}',
                callback_data=WorkTimeSlotTimetableCbData(id_work_time=slot.id).pack()),
            InlineKeyboardButton(text=reserved_text, callback_data='Свободно')
        ]

        builder.row(*buttons)

        if time_end_str == break_time_start_str:
            buttons = [
                InlineKeyboardButton(
                    text=f'{break_time_start_str}-{break_time_end_str}',
                    callback_data=BreakTimeSlotTimetableCbData(id_break_time=break_time.id).pack()
                ),
                InlineKeyboardButton(text='Перерыв', callback_data='break_time')
            ]

            builder.row(*buttons)

    button = InlineKeyboardButton(
        text='return',
        callback_data=MonthTimetableCbData(year=date.year, month=date.month).pack()
    )

    builder.row(button)

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
