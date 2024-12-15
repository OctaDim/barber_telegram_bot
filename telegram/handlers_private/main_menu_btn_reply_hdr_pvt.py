import inspect

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.buttons_common import (
    COMMON_BUTTONS_PARAMS)
from telegram.params.messages import (
    SELECT_MAIN_MENU_BUTTON)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key,
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    re_open_reply_keyboard_message)

return_main_menu_pvt_router = Router(name=__name__)
return_main_menu_pvt_router.message.filter(ChatTypesFilter(["private"]))


@return_main_menu_pvt_router.message(F.text == COMMON_BUTTONS_PARAMS.MAIN_MENU)
async def main_menu_btn_reply_hdr_pvt(message: Message,
                                      state: FSMContext):
    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state,
        fsm_state_literal_key="handlers_stack")
    print(f"\tOrigin handler stack: len(handlers_list)={len(handlers_list)}\n")

    if len(handlers_list) > 0:
        prior_handler_dict = handlers_list[-1]
        prior_handler_msgs_ids = prior_handler_dict.get("handler_messages_ids")
        print(f"\tOrigin delete list: "
              f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n")

        if prior_handler_msgs_ids:
            prior_handler_msgs_ids = list(filter(
                lambda msg_id: msg_id is not None, prior_handler_msgs_ids))
            print(f"\tNone values removed from delete list: "
                  f"\tprior_handler_messages_ids = {prior_handler_msgs_ids}\n")

        if prior_handler_msgs_ids:
            bot = message.bot
            cur_chat_id = message.chat.id
            await bot.delete_messages(chat_id=cur_chat_id,
                                      message_ids=prior_handler_msgs_ids)
            print(f"\tPrior messages were deleted successfully\n"
                  f"\tprior_handler_msgs_ids (deleted ids) = {prior_handler_msgs_ids}\n")

            await state.update_data(main_menu_opened_state=False)
            print(f"\tMain Menu opened state updated to False\n")

        else:
            print(f"\tPrior messages were not deleted, because "
                  f"\tprior_handler_msgs_ids = {prior_handler_msgs_ids}\n")

    # Saving the first handler only (Main Menu) before clearing state
    new_handlers_list = handlers_list[:1]

    # Saving reply message id (Reply Menu) before clearing state
    prior_reply_message_id = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state,
        fsm_state_literal_key="prior_reply_message_id_state")

    await state.clear()

    await state.update_data(
        handlers_stack=new_handlers_list,
        prior_reply_message_id_state=prior_reply_message_id)
    print(f"\tFirst handler saved. Prior reply msg id saved\n"
          f"\tFSM state cleared. FSM state updated:\n"
          f"\tprior_reply_message_id_state = {prior_reply_message_id}"
          f"\tlen(handlers_list) = {len(new_handlers_list)}\n")

    await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=message,
        re_open_reply_msg_text=SELECT_MAIN_MENU_BUTTON,
        # re_open_reply_msg_text=MAIN_GREETING_RICH_TXT,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=False)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
