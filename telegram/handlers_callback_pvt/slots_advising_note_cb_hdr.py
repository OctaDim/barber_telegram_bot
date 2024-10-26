from aiogram import Router
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import SlotsAdvisingNoteCBData
from telegram.telegram_utils.handlers_stack_utils import get_handler_answer_flag_dict
from telegram.telegram_utils.messages_helpers import (
    get_slots_advising_explanation,
    get_slots_advising_brief_note)


slots_advising_note_cb_router = Router(name=__name__)
slots_advising_note_cb_router.message.filter(ChatTypesFilter(["private"]))


@slots_advising_note_cb_router.callback_query(SlotsAdvisingNoteCBData.filter())
async def slot_advising_note_cb_hdr(callback_query: CallbackQuery):
    slots_advising_text = get_slots_advising_explanation()

    if len(slots_advising_text) > 200:
        slots_advising_text = get_slots_advising_brief_note()

    if len(slots_advising_text) <= 200:
        await callback_query.answer(text=slots_advising_text,
                                    show_alert=True)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
