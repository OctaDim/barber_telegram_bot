from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.methods_enroll_src_inl_kbd import (
    get_methods_enroll_srcs_inl_kbd)
from telegram.params.buttons_main_menu import (
    MAIN_MENU_BUTTONS_PARAMS)
from telegram.params.messages import (
    HOW_SELECT_SERVICES)

enroll_services_pvt_router = Router(name=__name__)
enroll_services_pvt_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_pvt_router.message(F.text == MAIN_MENU_BUTTONS_PARAMS.ENROLL_SERVICES)
async def enroll_services_btn_reply_hdr_pvt(message: Message,
                                            state: FSMContext):
    selected_method_prefix = None

    await message.answer(
        text=HOW_SELECT_SERVICES,
        reply_markup=get_methods_enroll_srcs_inl_kbd(
            selected_method_prefix=selected_method_prefix))
