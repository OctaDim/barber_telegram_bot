import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.addresses_queries import (
    get_company_addresses_for_maps)
from telegram.config.configs import (
    CONTACTS_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.submenu_contacts_inl_kbd import (
    OurMapInlineMenuCBData)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import (
    get_pvt_main_menu_reply_kbd)
from telegram.params.messages import (
    NO_MAPS_ADDRESSES, OR_SELECT_MAIN_MENU)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_helpers import (
    get_addresses_for_maps_text)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual, re_open_reply_keyboard_message)


inline_geo_map_router = Router(name=__name__)
inline_geo_map_router.message.filter(ChatTypesFilter(["private"]))


@inline_geo_map_router.callback_query(OurMapInlineMenuCBData.filter())
async def geo_map_link_cb_hdr(callback_query: CallbackQuery,
                              callback_data: CallbackData,
                              state: FSMContext):
    state_data = await state.get_data()

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    company_addresses = get_company_addresses_for_maps(
        company_id="all",
        address_order_by_fields=("sort_index", "name"))

    if not company_addresses:
        await callback_query.answer(text=NO_MAPS_ADDRESSES,
                                    show_alert=True)
        return

    addresses_text = get_addresses_for_maps_text(**company_addresses)

    try:
        await callback_query.message.edit_text(
            text=addresses_text,
            disable_web_page_preview=CONTACTS_CONFIGS.DISABLE_MAP_ADDRESSES_PREVIEW)
        print(f"\tPrior msg was edited to 'Addresses Maps' msg successfully\n")
    except (TelegramBadRequest, Exception) as exception_info:
        await callback_query.message.answer(
            text=addresses_text,
            disable_web_page_preview=CONTACTS_CONFIGS.DISABLE_MAP_ADDRESSES_PREVIEW,
            disable_notification=True)
        print(f"\tNew 'Addresses Maps' message was created, because "
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
