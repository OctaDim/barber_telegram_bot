from aiogram import Router, F
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd

from telegram.params.messages import MAIN_MENU
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS


return_main_menu_pvt_router = Router(name=__name__)
return_main_menu_pvt_router.message.filter(ChatTypesFilter(["private"]))


@return_main_menu_pvt_router.message(F.text == COMMON_BUTTONS_PARAMS.MAIN_MENU)
async def return_main_menu_btn_handler(message: Message, state: FSMContext):

    await state.update_data(handlers_stack=None)

    await message.answer(text=MAIN_MENU,
                         reply_markup=get_pvt_main_menu_kbd())
