from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.keyboard_inline.timetable_get_info_about_work_day_inl_kbd import AddMoreWorkTimeTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.work_time_cb_data_message import CONTINUED, RETURN, RETURN_ADMIN_PANEL, HOURS_LABEL, \
    HOURS_STEP_LABEL_TEMPLATE, MINUTES_LABEL, MINUTES_STEP_LABEL_TEMPLATE, CONTINUE_BUTTON_TXT


class AddIntervalWorkTimeCbData(CallbackData, prefix='add-work-time-interval'):
    time: str


class AddIntervalNextStepTimeWorkTimeCbData(CallbackData, prefix='add-service-end-time-interval'):
    next_step: bool



def add_work_time_interval_inl_kbd(work_time):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=HOURS_LABEL, callback_data="hour"))

    hours_buttons = []
    for hours_step in range(0, 12):
        time = HOURS_STEP_LABEL_TEMPLATE.format(hours_step)
        callback_data = AddIntervalWorkTimeCbData(time=time)
        hours_buttons.append(InlineKeyboardButton(text=time, callback_data=callback_data.pack()))

    for i in range(0, len(hours_buttons), 4):
        builder.row(*hours_buttons[i:i + 4])

    builder.row(InlineKeyboardButton(text=MINUTES_LABEL, callback_data="minutes"))

    minutes_buttons = []
    for minutes_step in range(0, 60, 5):
        time = MINUTES_STEP_LABEL_TEMPLATE.format(minutes_step)
        callback_data = AddIntervalWorkTimeCbData(time=time)
        minutes_buttons.append(InlineKeyboardButton(text=time, callback_data=callback_data.pack()))

    for i in range(0, len(minutes_buttons), 4):
        builder.row(*minutes_buttons[i:i + 4])

    builder.row(InlineKeyboardButton(
        text=CONTINUE_BUTTON_TXT,
        callback_data=AddIntervalNextStepTimeWorkTimeCbData(next_step=True).pack()
    ))

    buttons = [
        InlineKeyboardButton(
            text=RETURN,
            callback_data=AddMoreWorkTimeTimetableCbData.from_date(
                time_start_work_day=work_time[0].time_start,
                time_end_work_day=work_time[-1].time_end
            ).pack()
        ),
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack()
        )
    ]

    builder.row(*buttons)

    return builder.as_markup()
