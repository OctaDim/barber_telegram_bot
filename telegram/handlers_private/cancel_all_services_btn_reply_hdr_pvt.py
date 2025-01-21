import inspect

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.config.configs import (
    PAUSE_CONFIGS)
from telegram.filters.chat_types_filter import (
    ChatTypesFilter)
from telegram.params.buttons_enroll_service import (
    ENROLL_SRCS_BUTTONS)
from telegram.params.messages import (
    ALL_SERVICES_CANCELLED,
    NONE_SERVICES_SELECTED)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    get_handler_answer_flag_dict)
from telegram.telegram_utils.messages_utils import (
    send_warning_message_with_delete_delay)


cancel_all_services_pvt_router = Router(name=__name__)
cancel_all_services_pvt_router.message.filter(ChatTypesFilter(["private"]))


@cancel_all_services_pvt_router.message(F.text == ENROLL_SRCS_BUTTONS.CANCEL_ALL_SERVICES)
async def cancel_all_services_btn_reply_hdr(message: Message,
                                            state: FSMContext):
    state_data = await state.get_data()
    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_state_dict=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    if selected_services_ids:
        info_message_text = ALL_SERVICES_CANCELLED
        await state.update_data(
            # Reset all total info of the selected services in a state
            selected_services_ids_state=None,
            selected_services_cost_state=None,
            selected_services_duration_state=None)
    else:
        info_message_text = NONE_SERVICES_SELECTED

    await send_warning_message_with_delete_delay(
        message_text=info_message_text,
        message=message,
        delete_delay_seconds=PAUSE_CONFIGS.INFO_MESSAGE_DELAY)

    return get_handler_answer_flag_dict(
        add_handler_to_return_stack=False,
        update_min_actual_msg_id=False,
        executed_handler_name=inspect.currentframe().f_code.co_name)
