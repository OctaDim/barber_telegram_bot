import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.contacts_queries import (
    get_company_contacts)
from telegram.config.configs import (
    CONTACTS_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.submenu_contacts_inl_kbd import (
    OurContactsInlineMenuCBData)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    NO_CONTACTS,
    OR_SELECT_MAIN_MENU)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_contacts_text)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual,
    re_open_reply_keyboard_message)


inline_our_contacts_cb_router = Router(name=__name__)
inline_our_contacts_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_our_contacts_cb_router.callback_query(OurContactsInlineMenuCBData.filter())
async def inline_our_contacts_cb_hdr(callback_query: CallbackQuery,
                                     callback_data: CallbackData,
                                     state: FSMContext):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    contacts_data = get_company_contacts(
        company_id="all",
        socials_order_by_fields=("sort_index", "name"),
        phones_order_by_fields=("sort_index", "number"),
        address_order_by_fields=("sort_index", "street"))

    if not contacts_data:
        await callback_query.answer(text=NO_CONTACTS,
                                    show_alert=True)
        return

    contacts_text = get_contacts_text(
        **contacts_data,
        phones_international=CONTACTS_CONFIGS.PHONES_INTERNATIONAL)

    try:
        await callback_query.message.edit_text(
            text=contacts_text,
            disable_web_page_preview=CONTACTS_CONFIGS.DISABLE_CONTACTS_PREVIEW)
        print(f"\tPrior msg was edited to 'Contacts' msg successfully\n")
    except (TelegramBadRequest, Exception) as exception_info:
        await callback_query.message.answer(
            text=contacts_text,
            disable_web_page_preview=CONTACTS_CONFIGS.DISABLE_CONTACTS_PREVIEW,
            disable_notification=True)
        print(f"\tNew 'Contacts' message was created, because "
              f"\tprior message is not editable: {exception_info}\n")

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
