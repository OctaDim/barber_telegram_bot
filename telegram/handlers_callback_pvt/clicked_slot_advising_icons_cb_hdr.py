import inspect

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enrollment_intervals_inl_kbd import (
    SlotsAdvisingNoteCBData)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_slots_advising_explanation)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

clicked_slot_advising_icons_cb_router = Router(name=__name__)
clicked_slot_advising_icons_cb_router.message.filter(ChatTypesFilter(["private"]))


@clicked_slot_advising_icons_cb_router.callback_query(SlotsAdvisingNoteCBData.filter())
async def clicked_slot_advising_icons_hint_cb_hdr(callback_query: CallbackQuery,
                                                  state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    slots_advising_text = get_slots_advising_explanation()

    # TG callback query alert message limit max 200 symbols
    if len(slots_advising_text) <= 200:
        await callback_query.answer(text=slots_advising_text,
                                    show_alert=True)
    elif len(slots_advising_text) > 200:
        tg_len_validated_text = slots_advising_text[0:197] + "..."
        # slots_advising_text = get_slots_advising_brief_note()
        await callback_query.answer(text=tg_len_validated_text,
                                    show_alert=True)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
