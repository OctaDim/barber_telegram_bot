from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from telegram.keyboard_inline.timetable_get_day_inl_kbd import NextStepDaysTimetableCbData
from telegram.keyboard_inline.timetable_get_month_inl_kbd import BackToAdminMenuTimetableCbData
from telegram.params.work_time_cb_data_message import RETURN, RETURN_ADMIN_PANEL


class BlockOutTimeCbData(CallbackData, prefix='block-out-time'):
    work_time_id: int


class ChangeTimeSlot(CallbackData, prefix='change-time-slot-timetable'):
    work_time_id: int


class AddClientToSlot(CallbackData, prefix='add-client-to-slot-timetable'):
    work_time_id: int


def get_actions_for_not_reserved_slot(
        work_time_id: int,
        work_time_active: bool,
):
    builder = InlineKeyboardBuilder()

    if work_time_active is True:
        buttons = [
            InlineKeyboardButton(
                text='Записать клиента.',
                callback_data=AddClientToSlot(work_time_id=work_time_id).pack()
            ),
            InlineKeyboardButton(
                text='Перекрыть время',
                callback_data=BlockOutTimeCbData(work_time_id=work_time_id).pack(),
            ),
            InlineKeyboardButton(
                text='Изменить',
                callback_data=ChangeTimeSlot(work_time_id=work_time_id).pack()
            )
        ]

    else:
        buttons = [
            InlineKeyboardButton(
                text='Вернуть время',
                callback_data=BlockOutTimeCbData(work_time_id=work_time_id).pack(),
            )
        ]

    builder.add(*buttons)
    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(
            text=RETURN,
            callback_data=NextStepDaysTimetableCbData(
                next_step=True).pack()
        ),
        InlineKeyboardButton(
            text=RETURN_ADMIN_PANEL,
            callback_data=BackToAdminMenuTimetableCbData(active=True).pack())
    )

    inline_keyboard_markup = builder.as_markup()

    return inline_keyboard_markup
