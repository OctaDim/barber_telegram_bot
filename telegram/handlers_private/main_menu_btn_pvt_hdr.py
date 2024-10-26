from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS
from telegram.params.messages import SELECT_ACTION
from telegram.telegram_utils.fsm_states_utils import get_valid_list_by_fsm_state_key

return_main_menu_pvt_router = Router(name=__name__)
return_main_menu_pvt_router.message.filter(ChatTypesFilter(["private"]))


@return_main_menu_pvt_router.message(F.text == COMMON_BUTTONS_PARAMS.MAIN_MENU)
async def return_main_menu_btn_handler(message: Message,
                                       state: FSMContext):
    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state,
        fsm_state_literal_key="handlers_stack")

    new_handlers_list = handlers_list[:1]  # List with the first item only
    await state.clear()
    await state.update_data(handlers_stack=new_handlers_list)

    print("\tTEST INFO: Main menu common handler. FSM state cleared. "
          "Only the first handler is left in the handler stack")
    print(f"\tTEST INFO: len(handlers_list): {len(new_handlers_list)}\n")

    await message.answer(text=SELECT_ACTION,
                         reply_markup=get_pvt_main_menu_kbd())
