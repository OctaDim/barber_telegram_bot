from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.keyboard_inline.timetable_get_day_inl_kbd import BackToMonthTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import MonthTimetableCbData, BackToAdminMenuTimetableCbData
from telegram.params.timetable_cb_data_message import available_label, overlapped_label, break_label, \
    add_work_time_label, page_label_template
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL, PRIOR_PAGE, NEXT_PAGE
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
    reserved_slot: bool


class BreakTimeSlotTimetableCbData(CallbackData, prefix='break-time-slot-timetable', sep='|'):
    id_break_time: int


class PageNumberSlotTimetableCbData(CallbackData, prefix='page-number-slot-timetable', sep='|'):
    page: int
    date_day: str

    @classmethod
    def from_date(cls, date_day: datetime.date, page: int):
        return cls(date_day=date_day.isoformat(), page=page)

    def to_date(self) -> dict:
        data = {
            'date_day': datetime.fromisoformat(self.date_day).date(),
            'page': self.page
        }
        return data



class AddMoreWorkTimeTimetableCbData(CallbackData, prefix='add-more-work-time', sep='|'):
    time_start_work_day: str
    time_end_work_day: str

    @classmethod
    def from_date(cls, time_start_work_day: datetime, time_end_work_day: datetime):
        return cls(time_start_work_day=time_start_work_day.isoformat(), time_end_work_day=time_end_work_day.isoformat())

    def to_date(self) -> dict:
        data = {
            'time_start_work_day': datetime.fromisoformat(self.time_start_work_day),
            'time_end_work_day': datetime.fromisoformat(self.time_end_work_day)
        }
        return data


def get_info_about_work_day(work_time: list, break_time: list, page: int = 0):
    builder = InlineKeyboardBuilder()

    date = work_time[0].time_start
    date_data = get_select_date(date=date)

    work_time = [work_time[i:i + 6] for i in range(0, len(work_time), 6)]

    break_times = []
    for break_item in break_time:
        break_time_start_str = break_item.start_break.strftime('%H:%M')
        break_time_end_str = break_item.end_break.strftime('%H:%M')
        break_times.append((break_time_start_str, break_time_end_str, break_item.id, break_item.active))

    builder.row(InlineKeyboardButton(
        text=date_data.get('month'),
        callback_data=BackToMonthTimetableCbData(year=date.year).pack()))

    second_row = [
        InlineKeyboardButton(text='<<<',
                             callback_data=SelectDayTimetableCbData.from_date(
                                 action=PRIOR_PAGE,
                                 date_day=date.date()).pack()),

        InlineKeyboardButton(text=f'{date_data.get('weekday')}',
                             callback_data=MonthTimetableCbData(
                                 year=date.year,
                                 month=date.month).pack()),

        InlineKeyboardButton(text='>>>',
                             callback_data=SelectDayTimetableCbData.from_date(
                                 action=NEXT_PAGE,
                                 date_day=date.date()).pack())
    ]

    builder.row(*second_row)

    if page < -len(work_time):
        page = -1
    elif page == len(work_time):
        page = 0

    third_row = [
        InlineKeyboardButton(text='<<',
                             callback_data=PageNumberSlotTimetableCbData.from_date(
                                 page=page - 1,
                                 date_day=date.date()).pack()),

        InlineKeyboardButton(text=page_label_template.format(work_time.index(work_time[page]) + 1, len(work_time)),
                             callback_data=MonthTimetableCbData(
                                 year=date.year,
                                 month=date.month).pack()),

        InlineKeyboardButton(text='>>',
                             callback_data=PageNumberSlotTimetableCbData.from_date(
                                 page=page + 1,
                                 date_day=date.date()).pack())
    ]

    builder.row(*third_row)

    for slot in work_time[page]:
        time_start_str = slot.time_start.strftime('%H:%M')
        time_end_str = slot.time_end.strftime('%H:%M')

        if slot.reserved is False:
            reserved_text = available_label
        else:
            reserved_text = slot.work_time_clients[0].get_full_name

        if slot.active is False:
            reserved_text = overlapped_label

        buttons = [
            InlineKeyboardButton(
                text=f'{time_start_str}-{time_end_str}',
                callback_data=WorkTimeSlotTimetableCbData(
                    id_work_time=slot.id,
                    reserved_slot=reserved_text not in [available_label, overlapped_label]
                ).pack()),

            InlineKeyboardButton(text=reserved_text,
                                 callback_data=WorkTimeSlotTimetableCbData(
                                     id_work_time=slot.id,
                                     reserved_slot=reserved_text not in [available_label, overlapped_label]
                                 ).pack())
        ]

        builder.row(*buttons)

        for break_start_str, break_end_str, break_id, break_active in break_times:
            if time_end_str == break_start_str:
                if break_active:
                    buttons = [
                        InlineKeyboardButton(
                            text=f'{break_start_str}-{break_end_str}',
                            callback_data=BreakTimeSlotTimetableCbData(id_break_time=break_id).pack()
                        ),
                        InlineKeyboardButton(text=break_label,
                                             callback_data=BreakTimeSlotTimetableCbData(id_break_time=break_id).pack())
                    ]

                    builder.row(*buttons)

    callback_data = AddMoreWorkTimeTimetableCbData.from_date(
        time_start_work_day=work_time[0][0].time_start,
        time_end_work_day=work_time[-1][-1].time_end
    ).pack()

    button = InlineKeyboardButton(
        text=add_work_time_label,
        callback_data=callback_data
    )

    builder.row(button)

    button = InlineKeyboardButton(
        text=RETURN,
        callback_data=MonthTimetableCbData(year=date.year, month=date.month).pack()
    )

    builder.row(
        button,
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
