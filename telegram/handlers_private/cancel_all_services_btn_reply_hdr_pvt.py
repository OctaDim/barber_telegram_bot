from time import sleep

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.config.configs import PAUSE_CONFIGS
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.params.buttons_enroll_service import ENROLL_SERVICE_BUTTONS
from telegram.params.messages import (ALL_SERVICES_CANCELLED,
                                      NONE_SERVICES_SELECTED)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key)
from telegram.telegram_utils.handlers_stack_utils import (
    execute_last_stack_handler,
    get_handler_answer_flag_dict)
from utilities.numeric_utils import number_or_str_to_float

cancel_all_services_pvt_router = Router(name=__name__)
cancel_all_services_pvt_router.message.filter(ChatTypesFilter(["private"]))


@cancel_all_services_pvt_router.message(
    F.text == ENROLL_SERVICE_BUTTONS.CANCEL_ALL_CERVICES)
async def cancel_all_services_btn_reply_hdr(message: Message,
                                            state: FSMContext):
    state_data = await state.get_data()
    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    if selected_services_ids:
        text = ALL_SERVICES_CANCELLED

        # Reset total info of the selected services in a state
        await state.update_data(
            selected_services_ids_state=None,
            selected_services_cost_state=None,
            selected_services_duration_state=None)
    else:
        text = NONE_SERVICES_SELECTED

    await message.answer(text=text)

    delay_seconds = number_or_str_to_float(PAUSE_CONFIGS.SHORT_MSG_DELAY)
    sleep(delay_seconds)

    handlers_list = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state,
        fsm_state_literal_key="handlers_stack")

    await execute_last_stack_handler(handlers_list=handlers_list)

    return get_handler_answer_flag_dict(skip_add_handler_stack=True)
