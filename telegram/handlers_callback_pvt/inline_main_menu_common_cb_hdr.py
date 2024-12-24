import inspect

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.handlers_private.main_menu_btn_reply_hdr_pvt import (
    main_menu_btn_reply_hdr_pvt)
from telegram.keyboard_inline.common_buttons_inline import (
    MainMenuInlineBtnCBData)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

inline_main_menu_common_cb_router = Router(name=__name__)
inline_main_menu_common_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_main_menu_common_cb_router.callback_query(MainMenuInlineBtnCBData.filter())
async def inline_main_menu_common_cb_hdr(callback_query: CallbackQuery,
                                         state: FSMContext):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    # await callback_query.answer()
    message = callback_query.message

    # Call the same functionality handler of the reply keyboard button
    await main_menu_btn_reply_hdr_pvt(message=message, state=state)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
