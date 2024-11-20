from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.keyboard_inline.reservations_client_user_inl_kbd import (
    ReservationCancelledByClientCBData,
    ReservationCancelledByAdminCBData,
    ReservationCompletedCBData)
from telegram.params.messages import (
    RESERVATION_ADMIN_CANCELLED,
    RESERVATION_CLIENT_CANCELLED,
    RESERVATION_ALREADY_COMPLETED)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    inline_keyboard_is_actual)

clicked_reservation_cancelled_completed_cbr = Router(name=__name__)
clicked_reservation_cancelled_completed_cbr.message.filter(ChatTypesFilter(["private"]))


@clicked_reservation_cancelled_completed_cbr.callback_query(ReservationCancelledByClientCBData.filter())
@clicked_reservation_cancelled_completed_cbr.callback_query(ReservationCancelledByAdminCBData.filter())
@clicked_reservation_cancelled_completed_cbr.callback_query(ReservationCompletedCBData.filter())
async def reservation_cancelled_completed_cb_hdr(callback_query: CallbackQuery,
                                                 callback_data: CallbackData,
                                                 state: FSMContext):
    state_data = await state.get_data()

    if not await inline_keyboard_is_actual(state_data, callback_query):
        return get_handler_answer_flag_dict(skip_add_handler_stack=True)

    callback_prefix = callback_data.__prefix__

    match callback_prefix:
        case ReservationCancelledByClientCBData.__prefix__:
            text = RESERVATION_CLIENT_CANCELLED
        case ReservationCancelledByAdminCBData.__prefix__:
            text = RESERVATION_ADMIN_CANCELLED
        case ReservationCompletedCBData.__prefix__:
            text = RESERVATION_ALREADY_COMPLETED
        case _:
            text = ""

    # TG callback query alert message limit max 200 symbols
    text = text[0:197] + "..." if len(text) > 200 else text

    await callback_query.answer(text=text,
                                show_alert=True)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
