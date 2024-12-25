from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from utilities.get_days_calendar import get_days_in_month


class DaysWorkTimeCbData(CallbackData, prefix='days-work-time'):
    days: str


class NextStepTimeWorkTimeCbData(CallbackData, prefix='continue-work-time'):
    mount: str
    year: int
    active_return: bool


class ReturnStepToMonthWorkTimeCbData(CallbackData, prefix='return-to-month-work-time'):
    active: bool


def work_time_days_inl_kbd(mount: str, year: int, current_date, master_id):
    builder = InlineKeyboardBuilder()

    data, month_name = get_days_in_month(month_name=mount, year=year, current_date=current_date, master_id=master_id)
    data_copy = data.copy()

    week_row = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    calendar_data = []

    builder.button(text=month_name, callback_data=month_name)

    for week_day in week_row:
        builder.button(text=week_day, callback_data=week_day)

    for i in range(6):
        if data_copy:
            for day in week_row:
                if data_copy:
                    for key, value in data_copy.items():
                        if day == value:
                            calendar_data.append(key)
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
            callback_data = DaysWorkTimeCbData(days=day)
            builder.button(text=day, callback_data=callback_data)

            continue

        builder.button(text=day, callback_data=day)

    buttons = [
        InlineKeyboardButton(
            text='Return',
            callback_data=ReturnStepToMonthWorkTimeCbData(active=True).pack()
        ),
        InlineKeyboardButton(
            text='Продолжить',
            callback_data=NextStepTimeWorkTimeCbData(mount=mount, year=year, active_return=False).pack()
        )
    ]

    builder.row(*buttons)

    builder.adjust(1, 7)

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
