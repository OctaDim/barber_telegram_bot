from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.enroll_methods_inl_kbd import (
    get_enroll_methods_inl_kbd)
from telegram.params.buttons_main_menu import (
    MAIN_MENU_BUTTONS_PARAMS)
from telegram.params.messages import (
    HOW_SELECT_SERVICES)

enroll_services_pvt_router = Router(name=__name__)
enroll_services_pvt_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_pvt_router.message(F.text == MAIN_MENU_BUTTONS_PARAMS.ENROLL_SERVICES)
async def enroll_services_btn_handler(message: Message,
                                      state: FSMContext):
    state_data = await state.get_data()

    selected_method_prefix = None
    # selected_method_prefix = await get_valid_str_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="selected_method_prefix")

    await message.answer(
        text=HOW_SELECT_SERVICES,
        reply_markup=get_enroll_methods_inl_kbd(
            selected_method_prefix=selected_method_prefix))
