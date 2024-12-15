import inspect

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.submenu_contacts_inl_kbd import (
    OurMapInlineMenuCBData)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    OR_SELECT_MAIN_MENU_BUTTON,
    IN_DEVELOP_PROCESS)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    re_open_reply_keyboard_message)

inline_geo_map_router = Router(name=__name__)
inline_geo_map_router.message.filter(ChatTypesFilter(["private"]))


@inline_geo_map_router.callback_query(OurMapInlineMenuCBData.filter())
async def inline_frequent_questions_cb_hdr(callback_query: CallbackQuery,
                                           callback_data: CallbackData,
                                           state: FSMContext):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    await callback_query.answer(text=IN_DEVELOP_PROCESS,
                                show_alert=True)

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=callback_query,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU_BUTTON,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    # IMPORTANT: Set add_handler_to_return_stack=True, when realised (if logic necessary)
    # IMPORTANT: update_min_actual_msg_id=True, when realised (if logic necessary)
    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
