import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
    MethodCategoryToMasterCBData,
    MethodCategoryToServiceCBData,
    MethodMasterToServiceCBData,
    get_methods_enroll_srcs_inl_kbd)
from telegram.params.messages import (
    HOW_SELECT_SERVICES)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

method_selected_enroll_srcs_cb_router = Router(name=__name__)
method_selected_enroll_srcs_cb_router.message.filter(ChatTypesFilter(["private"]))


@method_selected_enroll_srcs_cb_router.callback_query(MethodCategoryToMasterCBData.filter())
@method_selected_enroll_srcs_cb_router.callback_query(MethodCategoryToServiceCBData.filter())
@method_selected_enroll_srcs_cb_router.callback_query(MethodMasterToServiceCBData.filter())
async def method_selected_enroll_srcs_cb_hdr(callback_query: CallbackQuery,
                                             callback_data: CallbackData,
                                             state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    selected_method_prefix = callback_data.__prefix__

    # # Unselecting method if clicked the same method
    # new_selected_method_prefix = callback_data.__prefix__
    # old_selected_method_prefix = await get_valid_str_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="selected_method_prefix")
    # if new_selected_method_prefix == old_selected_method_prefix:
    #     selected_method_prefix = None

    try:
        await callback_query.message.edit_text(
            text=HOW_SELECT_SERVICES,
            reply_markup=get_methods_enroll_srcs_inl_kbd(
                selected_method_prefix=selected_method_prefix))
    except (TelegramBadRequest, Exception) as exception_info:
        print(f"\tMessage not modified, tg exception intercepted: {exception_info}\n")

    await state.update_data(
        selected_method_prefix=selected_method_prefix)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
