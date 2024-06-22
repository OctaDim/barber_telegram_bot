from aiogram.utils.keyboard import (InlineKeyboardBuilder)
from aiogram.filters.callback_data import CallbackData


class HoursCallbackData(CallbackData, prefix='hours-services'):
    hours: int


class MinutesCallbackData(CallbackData, prefix='minutes-services'):
    minutes: int


def add_hours_time_duration_services_inl_kbd(selected_hours_value=None):
    builder = InlineKeyboardBuilder()

    for hours_step in range(0, 10):
        callback_data = HoursCallbackData(hours=hours_step)

        if hours_step != selected_hours_value:
            builder.button(text=f"{hours_step}h", callback_data=callback_data.pack())
        else:
            builder.button(text=f"✅ {hours_step}h", callback_data=callback_data.pack())

    builder.adjust(4)
    return builder.as_markup()


def add_minutes_time_duration_services_inl_kbd(selected_minutes_value=None):
    builder = InlineKeyboardBuilder()

    for minutes_step in range(0, 60, 5):
        callback_data = MinutesCallbackData(minutes=minutes_step)

        if minutes_step != selected_minutes_value:
            builder.button(text=f"{minutes_step}m", callback_data=callback_data.pack())

        else:
            builder.button(text=f"✅ {minutes_step}m", callback_data=callback_data.pack())

    builder.adjust(4)

    return builder.as_markup()
