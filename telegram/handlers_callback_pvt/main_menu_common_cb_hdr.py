from aiogram import Router

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import ChatTypesFilter

from telegram.handlers_private.main_menu_btn_pvt_hdr import return_main_menu_btn_handler

from telegram.keyboard_inline.common_cb_data_all_inl_kbds import MainMenuInlineBtnCBData


main_menu_common_cb_router = Router(name=__name__)
main_menu_common_cb_router.message.filter(ChatTypesFilter(["private"]))


@main_menu_common_cb_router.callback_query(MainMenuInlineBtnCBData.filter())
async def main_menu_common_callback_hdr(callback_query: CallbackQuery,
                                        state: FSMContext):
    await callback_query.answer()
    message = callback_query.message

    # Call the same functionality handler of the reply keyboard button
    await return_main_menu_btn_handler(message=message, state=state)
