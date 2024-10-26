from time import sleep

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.db_queries.user_queries import get_services_list
from telegram.config.configs import PAUSE_CONFIGS
from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.keyboard_inline.enroll_services_inl_kbd import (
    get_enroll_service_inl_kbd)
from telegram.keyboard_reply.pvt_enroll_service_actions_kbd import (
    get_pvt_enroll_services_actions_reply_kbd)
from telegram.keyboard_reply.pvt_main_menu_kbd import (
    get_pvt_main_menu_kbd)
from telegram.params.buttons_main_menu import (
    MAIN_MENU_BUTTONS_PARAMS)
from telegram.params.messages import (
    NO_SERVICES,
    SELECT_OTHER_ACTIONS,
    SELECT_SERVICES_BELLOW)
from telegram.params.select_services_icons import (
    SELECT_SERVICES_ICONS)
from telegram.telegram_utils.fsm_states_utils import (
    get_valid_list_by_fsm_state_key)
from telegram.telegram_utils.messages_helpers import (
    get_service_brief_info)
from utilities.numeric_utils import number_or_str_to_float

enroll_services_pvt_router = Router(name=__name__)
enroll_services_pvt_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_pvt_router.message(
    F.text == MAIN_MENU_BUTTONS_PARAMS.ENROLL_SERVICES)
async def enroll_services_btn_handler(message: Message,
                                      state: FSMContext):
    state_data = await state.get_data()

    all_services_records = get_services_list()
    if not all_services_records:
        await message.answer(
            text=NO_SERVICES,
            reply_markup=get_pvt_main_menu_kbd())
        return

    await message.answer(text=SELECT_SERVICES_BELLOW)

    selected_services_ids = await get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from=state_data,
        fsm_state_literal_key="selected_services_ids_state")

    # For the future
    # max_service_name = ""
    # for service_record in all_services_records:
    #     if len(service_record.name) > len(max_service_name):
    #         max_service_name = service_record.name

    all_services_info_dict = {}

    for service_record in all_services_records:
        # For the future
        # fill_symbols_number = get_fill_symbols_number_via_pixels(
        #     text_long=max_service_name,
        #     text_short=service_record.name,
        #     fill_symbol=SPECIAL_CHARACTERS.FILL_IN_BLANK_SYMBOL)

        service_brief_text = get_service_brief_info(
            service_record=service_record)

        if service_record.id in selected_services_ids:
            same_id_count = selected_services_ids.count(service_record.id)
            inline_button_icon = f"{SELECT_SERVICES_ICONS.SELECTED} " * same_id_count
            button_selected = True
            one_more_service_btn = True
        else:
            inline_button_icon = SELECT_SERVICES_ICONS.NO_ICON
            button_selected = False
            one_more_service_btn = False

        await message.answer(
            text=f"{inline_button_icon} {service_brief_text}",
            reply_markup=get_enroll_service_inl_kbd(service_record.id,
                                                    button_selected,
                                                    one_more_service_btn))

        delay_seconds = number_or_str_to_float(PAUSE_CONFIGS.LIST_DELAY)
        sleep(delay_seconds)

        all_services_info_dict[service_record.id] = {
            "text": service_brief_text,
            "price": service_record.price,
            "duration": service_record.time_duration}

    await state.update_data(all_services_info_state=all_services_info_dict)

    await message.answer(
        text=SELECT_OTHER_ACTIONS,
        reply_markup=get_pvt_enroll_services_actions_reply_kbd())
