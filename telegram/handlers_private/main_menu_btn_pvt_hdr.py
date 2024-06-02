from aiogram import Router, F
from aiogram.types import Message

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.telegram_utils.delete_messages import delete_reply_msg_and_prev_msgs
from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd

from telegram.params.messages import MAIN_MENU
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS


return_main_menu_pvt_router = Router(name=__name__)
return_main_menu_pvt_router.message.filter(ChatTypesFilter(["private"]))


@return_main_menu_pvt_router.message(F.text == COMMON_BUTTONS_PARAMS.MAIN_MENU)
async def return_main_menu_btn_handler(message: Message):
    # await delete_reply_msg_and_prev_msgs(message=message,
    #                                      messages_number_to_delete=6)

    await message.answer(text=MAIN_MENU,
                         reply_markup=get_pvt_main_menu_kbd())
