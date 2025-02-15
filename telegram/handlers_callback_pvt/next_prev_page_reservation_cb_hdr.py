import inspect

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.reservations_client_inl_kbd import (NextReservationPageCBData,
                                                                  PreviousReservationPageCBData,
                                                                  get_reservation_client_user_inl_kbd)
from telegram.params.messages import (
    ALL_RESERVATIONS_HERE)
from telegram.telegram_utils.fsm_states_utils import (get_valid_dict_by_fsm_state_key, get_valid_int_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)


next_prev_page_reservation_client_cb_router = Router(name=__name__)
next_prev_page_reservation_client_cb_router.message.filter(ChatTypesFilter(["private"]))


@next_prev_page_reservation_client_cb_router.callback_query(PreviousReservationPageCBData.filter())
@next_prev_page_reservation_client_cb_router.callback_query(NextReservationPageCBData.filter())
async def next_prev_page_reservation_client_cb_hdr(callback_query: CallbackQuery,
                                                   callback_data: CallbackData,
                                                   state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return

    print(f"{'-' * 115}\n\tHandler: {inspect.currentframe().f_code.co_name}\n")

    callback_prefix = callback_data.__prefix__

    cur_page_number = await get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="current_page_number_of_reservations")
    cur_page_number = 1 if not cur_page_number else cur_page_number

    paginated_reservations = await get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="paginated_reservations_records")

    total_pages = len(paginated_reservations)

    if callback_prefix == PreviousReservationPageCBData.__prefix__:
        if (cur_page_number - 1) < 1:
            cur_page_number = total_pages
        else:
            cur_page_number -= 1
    elif callback_prefix == NextReservationPageCBData.__prefix__:
        if (cur_page_number + 1) > total_pages:
            cur_page_number = 1
        else:
            cur_page_number += 1
    else:
        cur_page_number = 1

    # if callback_prefix == PreviousReservationPageCBData.__prefix__:
    #     if not paginated_reservations.get(cur_page_number - 1):
    #         cur_page_number = len(paginated_reservations)
    #     else:
    #         cur_page_number -= 1
    # elif callback_prefix == NextReservationPageCBData.__prefix__:
    #     if not paginated_reservations.get(cur_page_number + 1):
    #         cur_page_number = 1
    #     else:
    #         cur_page_number += 1
    # else:
    #     cur_page_number = 1

    current_page_reservations = paginated_reservations.get(cur_page_number)

    try:
        await callback_query.message.edit_text(
            text=ALL_RESERVATIONS_HERE,
            reply_markup=get_reservation_client_user_inl_kbd(
                current_page_reservations=current_page_reservations,
                total_pages_number=total_pages,
                current_page_number=cur_page_number))
    except (TelegramBadRequest, Exception) as exception_info:
        print(f"\tMessage not modified, exception intercepted: {exception_info}\n")

    await state.update_data(
        current_page_number_of_reservations=cur_page_number)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
