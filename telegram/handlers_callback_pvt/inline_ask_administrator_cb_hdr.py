import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.user_obj_by_telegram_id import (
    get_user_objs_with_masters_by_tg_id)
from telegram.config.settings import (
    BOT_CREDENTIALS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.submenu_ask_question_inl_kbd import (
    AskAdministratorInlineMenuCBData)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    NO_ADMINS_TO_CONNECT,
    OR_SELECT_MAIN_MENU)
from telegram.params.messages_inserts import MSG
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    re_open_reply_keyboard_message)
from utilities.list_utils import (
    convert_str_list_to_int_list,
    get_strs_list_from_env_string)


inline_ask_administrator_cb_router = Router(name=__name__)
inline_ask_administrator_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_ask_administrator_cb_router.callback_query(AskAdministratorInlineMenuCBData.filter())
async def inline_ask_administrator_cb_hdr(callback_query: CallbackQuery,
                                          callback_data: CallbackData,
                                          state: FSMContext):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    admins_ids_env_str = BOT_CREDENTIALS.TG_BOT_ASK_ADMINS_IDS
    admins_tg_ids_str = get_strs_list_from_env_string(admins_ids_env_str)
    admins_tg_ids_int = convert_str_list_to_int_list(admins_tg_ids_str)

    admins_users_objs = get_user_objs_with_masters_by_tg_id(
        telegram_ids=admins_tg_ids_int)

    if not admins_users_objs:
        print("if not admins_users_objs:", admins_users_objs)
        await callback_query.answer(text=NO_ADMINS_TO_CONNECT,
                                    show_alert=True)
        return

    first_contact_msg_sent_flag = False
    for admin_user_obj in admins_users_objs:
        admin_tg_username = admin_user_obj.username
        admin_user_fullname = admin_user_obj.get_full_name

        if admin_tg_username:
            admin_link = (f"<a href='https://t.me/{admin_tg_username}'>"
                          f"{MSG.ADMINISTRATOR}:  {admin_user_fullname}"
                          f"</a>")
        else:
            admin_link = f"{MSG.ADMINISTRATOR}:  {admin_user_fullname}"

        if not first_contact_msg_sent_flag:
            try:
                await callback_query.message.edit_text(text=admin_link)
                print(f"\tPrior msg was edited to 'Admin link' msg successfully\n"
                      f"\tadmin_link = {admin_link}\n")
            except (TelegramBadRequest, Exception) as exception_info:
                await callback_query.message.answer(
                    text=admin_link,
                    disable_notification=True)
                print(f"\tNew 'Admin link' message was created, because "
                      f"\tprior message is not editable: {exception_info}\n"
                      f"\tadmin_link = {admin_link}\n")
            first_contact_msg_sent_flag = True
        else:
            await callback_query.message.answer(
                text=admin_link,
                disable_notification=True)
            print(f"\tNew 'Admin link' message was created, because \n"
                  f"\tfirst_contact_msg_sent_flag = {first_contact_msg_sent_flag}\n"
                  f"\tadmin_link = {admin_link}\n")

    await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=callback_query,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        open_reply_kbd_msg_anyway=True,
        reply_kbd_opened_state_after_open=True)

    # await state.update_data()

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
