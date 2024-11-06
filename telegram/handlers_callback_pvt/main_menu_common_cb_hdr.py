from aiogram import Router
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.handlers_private.main_menu_btn_pvt_hdr import return_main_menu_btn_handler

from telegram.keyboard_inline.common_buttons_inline import MainMenuInlineBtnCBData

from telegram.telegram_utils.handlers_stack_utils import get_handler_answer_flag_dict
from telegram.telegram_utils.messages_utils import inline_keyboard_is_actual


main_menu_common_cb_router = Router(name=__name__)
main_menu_common_cb_router.message.filter(ChatTypesFilter(["private"]))


@main_menu_common_cb_router.callback_query(MainMenuInlineBtnCBData.filter())
async def main_menu_common_callback_hdr(callback_query: CallbackQuery,
                                        state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    await callback_query.answer()

    message = callback_query.message

    # Call the same functionality handler of the reply keyboard button
    await return_main_menu_btn_handler(message=message, state=state)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True,
                                        upd_actual_msg_min_id=True)
