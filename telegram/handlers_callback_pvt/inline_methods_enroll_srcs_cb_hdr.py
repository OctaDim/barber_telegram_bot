import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
    get_methods_enroll_srcs_inl_kbd)
from telegram.keyboard_inline.submenu_services_inl_kbd import (
    EnrollServicesInlineMenuCBData)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    HOW_SELECT_SERVICES,
    OR_SELECT_MAIN_MENU)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual, re_open_reply_keyboard_message)

inline_methods_enroll_srcs_cb_router = Router(name=__name__)
inline_methods_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_methods_enroll_srcs_cb_router.callback_query(EnrollServicesInlineMenuCBData.filter())
async def inline_methods_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                            callback_data: CallbackData,
                                            state: FSMContext):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    selected_method_prefix = None

    try:
        cur_message = await callback_query.message.edit_text(
            text=HOW_SELECT_SERVICES,
            reply_markup=get_methods_enroll_srcs_inl_kbd(
                selected_method_prefix=selected_method_prefix))
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tPrior message was edited to Methods msg successfully :)\n")

    except (TelegramBadRequest, Exception) as exception_info:
        cur_message = await callback_query.message.answer(
            text=HOW_SELECT_SERVICES,
            reply_markup=get_methods_enroll_srcs_inl_kbd(
                selected_method_prefix=selected_method_prefix),
            disable_notification=True)
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tNew Methods message was created, because "
              f"\tprior message is not editable: {exception_info}\n")

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=callback_query,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    # await state.update_data()

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=True,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
