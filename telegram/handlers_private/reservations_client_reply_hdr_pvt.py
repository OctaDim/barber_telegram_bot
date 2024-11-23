from time import sleep

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.db_models.reservation_model import (
    Reservation)
from database.db_queries.all_reservations_ordered_query import (
    get_all_reservations_ordered)
from database.db_queries.user_obj_by_telegram_id import (
    get_user_obj_by_telegram_id)
from telegram.config.configs import (
    PAUSE_CONFIGS,
    PAGINATION_CONFIGS, RESERVATIONS_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.handlers_private.main_menu_btn_reply_hdr_pvt import (
    main_menu_btn_reply_hdr_pvt)
from telegram.keyboard_inline.reservations_client_user_inl_kbd import (
    get_reservation_client_user_inl_kbd)
from telegram.params.buttons_main_menu import (
    MAIN_MENU_BUTTONS_PARAMS)
from telegram.params.messages import (
    NO_CLIENT_RESERVATIONS,
    ALL_RESERVATIONS_HERE)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from utilities.numeric_utils import (
    number_or_str_to_float)
from utilities.pagination_utility import (
    create_paginated_elems)

client_reservations_btn_router = Router(name=__name__)
client_reservations_btn_router.message.filter(ChatTypesFilter(["private"]))


@client_reservations_btn_router.message(F.text == MAIN_MENU_BUTTONS_PARAMS.RESERVATIONS)
async def client_reservations_btn_reply_hdr_pvt(message: Message,
                                                state: FSMContext):
    state_data = await state.get_data()

    cur_user_telegram_id = message.from_user.id
    cur_user_obj = get_user_obj_by_telegram_id(cur_user_telegram_id)

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
        await message.answer(text=NO_CLIENT_RESERVATIONS)
        sleep(number_or_str_to_float(PAUSE_CONFIGS.SHORT_MSG_DELAY))
        await main_menu_btn_reply_hdr_pvt(message=message, state=state)
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    paginated_reservations = create_paginated_elems(
        all_elements=reservations_records,
        elements_per_page=PAGINATION_CONFIGS.RESERVATIONS_PER_PAGE)

    cur_page_number = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="current_page_number_of_reservations")
    cur_page_number = 1 if not cur_page_number else cur_page_number

    current_page_reservations = paginated_reservations.get(cur_page_number)
    total_pages = len(paginated_reservations)

    await message.answer(
        text=ALL_RESERVATIONS_HERE,
        reply_markup=get_reservation_client_user_inl_kbd(
            current_page_reservations=current_page_reservations,
            total_pages_number=total_pages,
            current_page_number=cur_page_number))

    await state.update_data(
        current_page_number_of_reservations=cur_page_number,
        paginated_reservations_records=paginated_reservations)

    return get_handler_answer_flag_dict(upd_actual_msg_min_id=True)
