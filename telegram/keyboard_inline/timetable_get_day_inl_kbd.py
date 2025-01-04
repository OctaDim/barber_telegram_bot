from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from datetime import datetime

from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL, CONTINUE_BUTTON_TXT
from utilities.get_days_calendar_by_timetable import get_days_in_month_by_logbook


class DaysTimetableCbData(CallbackData, prefix='days-timetable'):
    date_day: str

    @classmethod
    def from_date(cls, date_day: datetime.date):
        return cls(date_day=date_day.isoformat())

    def to_date(self) -> datetime.date:
        return datetime.fromisoformat(self.date_day).date()


class NextStepDaysTimetableCbData(CallbackData, prefix='continue-timetable'):
    next_step: bool


class BackToMonthTimetableCbData(CallbackData, prefix='back-to-month-timetable'):
    year: int


def timetable_get_day_inl_kbd(month: int, year: int, date_days: dict, current_day: int, current_month: int):
    builder = InlineKeyboardBuilder()

    data, month_name = get_days_in_month_by_logbook(month=month, year=year, days=date_days)
    data_copy = data.copy()

    week_row = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    calendar_data = []

    builder.button(text=month_name, callback_data=f'{month_name}')

    for week_day in week_row:
        builder.button(text=week_day, callback_data=f'{week_day}')

    for i in range(6):
        if data_copy:
            for day in week_row:
                if data_copy:
                    for key, value in data_copy.items():
                        if day == value:
                            if '-' not in key:
                                calendar_data.append(key)
                                data_copy.pop(key)
                                break

                            calendar_data.append('-')
                            data_copy.pop(key)
                            break

                        calendar_data.append('-')
                        break
                    else:
                        break

                elif len(calendar_data[-1]) < 7:
                    calendar_data.append('-')

    for day in calendar_data:
        if day != '-':
            if int(day) == current_day:
                if current_month == month:
                    callback_data = DaysTimetableCbData.from_date(date_days.get(int(day)))
                    builder.button(text=f'🔹{day}', callback_data=callback_data.pack())

                    continue

            callback_data = DaysTimetableCbData.from_date(date_days.get(int(day)))
            builder.button(text=day, callback_data=callback_data.pack())

            continue

        builder.button(text=day, callback_data='day')

    callback_data = NextStepDaysTimetableCbData(next_step=True)
    builder.button(text=CONTINUE_BUTTON_TXT, callback_data=callback_data.pack())

    builder.adjust(1, 7)

    callback_data = BackToMonthTimetableCbData(year=year)
    builder.row(
        InlineKeyboardButton(text=RETURN, callback_data=callback_data.pack()),
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
