import re

from aiogram import types
from aiogram.filters import Filter


class ReservedSlotFilter(Filter):
    async def __call__(self, callback_query: types.CallbackQuery) -> bool:
        cb_query_data = callback_query.data

        pattern = r'work-time-slot-timetable\|(\d+\|\d+)'
        match = re.search(pattern, cb_query_data).group(1)

        if match[-1] == '1':
            return True

        return False
