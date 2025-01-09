import inspect

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.submenu_balance_inl_kbd import (
    get_balance_inl_kbd_pvt)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.buttons_main_menu import (
    MAIN_MENU_BUTTONS)
from telegram.params.messages import (
    OR_SELECT_MAIN_MENU,
    SELECT_BALANCE_SECTION)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    re_open_reply_keyboard_message)

submenu_balance_pvt_router = Router(name=__name__)
submenu_balance_pvt_router.message.filter(ChatTypesFilter(["private"]))


@submenu_balance_pvt_router.message(F.text == MAIN_MENU_BUTTONS.BALANCE)
async def balance_btn_to_submenu_reply_hdr_pvt(message: Message,
                                               bot: Bot,
                                               state: FSMContext):
    cur_handler_messages_ids = []

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    try:
        cur_message = await message.edit_message_text(
            text=SELECT_BALANCE_SECTION,
            reply_markup=get_balance_inl_kbd_pvt())
        cur_handler_messages_ids.append(cur_message.message_id)
        print(f"\tPrior message (message.message_id) was edited "
              f"\tto Balance (sub menu) msg successfully :)\n")

    except (TelegramBadRequest, Exception) as exception_info:
        print(f"\tPrior message (message.message_id) is not editable: "
              f"\t{exception_info}\n")
        try:
            cur_message_id = message.message_id
            cur_chat_id = message.chat.id
            cur_message = await bot.edit_message_text(
                text=SELECT_BALANCE_SECTION,
                message_id=cur_message_id + 1,
                chat_id=cur_chat_id,
                reply_markup=get_balance_inl_kbd_pvt())
            cur_handler_messages_ids.append(cur_message.message_id)
            print(f"\tPrior msg (message.message_id + 1) "
                  f"\twas edited to Balance (sub menu) msg\n")

        except (TelegramBadRequest, Exception) as exception_info:
            cur_message = await message.answer(
                text=SELECT_BALANCE_SECTION,
                reply_markup=get_balance_inl_kbd_pvt())
            cur_handler_messages_ids.append(cur_message.message_id)
            print(f"\tNew Balance (sub menu) msg was created, because "
                  f"\tprior message (message.message_id + 1) is not editable:\n"
                  f"\t{exception_info}\n")

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=message,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=True,
        open_reply_kbd_msg_anyway=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    # await state.update_data()

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=True,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
