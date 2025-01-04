import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_models.reservation_model import (
    Reservation)
from database.db_queries.all_reservations_ordered_query import (
    get_all_reservations_ordered)
from database.db_queries.user_obj_by_telegram_id import (
    get_user_obj_by_telegram_id)
from telegram.config.configs import (
    RESERVATIONS_CONFIGS,
    PAGINATION_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.reservations_client_inl_kbd import (
    get_reservation_client_user_inl_kbd)
from telegram.keyboard_inline.submenu_services_inl_kbd import (
    MyReservationsInlineMenuCBData)
from telegram.keyboard_reply.pvt_main_menu_reply_kbd import get_pvt_main_menu_reply_kbd
from telegram.params.messages import (
    NO_CLIENT_RESERVATIONS,
    ALL_RESERVATIONS_HERE,
    OR_SELECT_MAIN_MENU)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    re_open_reply_keyboard_message,
    inline_keyboard_is_actual)
from utilities.pagination_utility import (
    create_paginated_elems)

inline_client_reservations_cb_router = Router(name=__name__)
inline_client_reservations_cb_router.message.filter(ChatTypesFilter(["private"]))


@inline_client_reservations_cb_router.callback_query(MyReservationsInlineMenuCBData.filter())
async def inline_reservations_client_user_cb_hdr(callback_query: CallbackQuery,
                                                 callback_data: CallbackData,
                                                 state: FSMContext):
    state_data = await state.get_data()
    cur_handler_messages_ids = []

    # Checking if inline keyboard is actual and not obsolete by any reason
    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    cur_user_telegram_id = callback_query.from_user.id
    cur_user_obj = get_user_obj_by_telegram_id(
        telegram_id=cur_user_telegram_id)

    if RESERVATIONS_CONFIGS.SHOW_RESERVATIONS_ADMIN_CANCELLED:
        cancelled_by_admin_flag = "all"
    else:
        cancelled_by_admin_flag = False

    if RESERVATIONS_CONFIGS.SHOW_RESERVATIONS_CLIENT_CANCELLED:
        cancelled_by_client_flag = "all"
    else:
        cancelled_by_client_flag = False

    show_completed_flag = RESERVATIONS_CONFIGS.SHOW_COMPLETED_RESERVATIONS

    reservations_records = get_all_reservations_ordered(
        show_completed_reservations=show_completed_flag,
        client_user_id=cur_user_obj.id,
        cancelled_by_client=cancelled_by_client_flag,
        cancelled_by_admin=cancelled_by_admin_flag,
        active=True,
        order_by_fields=Reservation.reserved_interval_time_start.desc())

    if not reservations_records:
        await callback_query.answer(text=NO_CLIENT_RESERVATIONS,
                                    show_alert=True)
        return

    paginated_reservations = create_paginated_elems(
        all_elements=reservations_records,
        elements_per_page=PAGINATION_CONFIGS.RESERVATIONS_PER_PAGE)

    cur_page_number = 1
    # cur_page_number = await get_valid_int_by_fsm_state_key(
    #     fsm_state_or_dict_from=state_data,
    #     fsm_state_literal_key="current_page_number_of_reservations")
    # cur_page_number = 1 if not cur_page_number else cur_page_number

    current_page_reservations = paginated_reservations.get(cur_page_number)
    total_pages = len(paginated_reservations)

    try:
        cur_message = await callback_query.message.edit_text(
            text=ALL_RESERVATIONS_HERE,
            reply_markup=get_reservation_client_user_inl_kbd(
                current_page_reservations=current_page_reservations,
                total_pages_number=total_pages,
                current_page_number=cur_page_number))
        cur_message_id = cur_message.message_id
        cur_handler_messages_ids.append(cur_message_id)
        reservation_msg_id = cur_message_id
        print(f"\tPrior message was edited to Reservations msg successfully\n")

    except (TelegramBadRequest, Exception) as exception_info:
        cur_message = await callback_query.message.answer(
            text=ALL_RESERVATIONS_HERE,
            reply_markup=get_reservation_client_user_inl_kbd(
                current_page_reservations=current_page_reservations,
                total_pages_number=total_pages,
                current_page_number=cur_page_number))
        cur_message_id = cur_message.message_id
        cur_handler_messages_ids.append(cur_message_id)
        reservation_msg_id = cur_message_id
        print(f"\tNew Reservations message was created, because "
              f"\tprior message is not editable: {exception_info}\n")

    cur_message = await re_open_reply_keyboard_message(
        fsm_state=state,
        telegram_update_obj=callback_query,
        re_open_reply_msg_text=OR_SELECT_MAIN_MENU,
        re_open_reply_keyboard=get_pvt_main_menu_reply_kbd(),
        reply_kbd_opened_state_after_open=True)
    if cur_message:
        cur_handler_messages_ids.append(cur_message.message_id)

    await state.update_data(
        current_page_number_of_reservations=cur_page_number,
        paginated_reservations_records=paginated_reservations,
        # Additional update
        reservation_message_id_state=reservation_msg_id)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=True,
        handler_messages_ids=cur_handler_messages_ids,
        update_min_actual_msg_id=True,
        executed_handler_name=inspect.currentframe().f_code.co_name)
