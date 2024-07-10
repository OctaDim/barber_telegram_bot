import asyncio

from aiogram import Router, F
from aiogram.types import Message

from telegram.filters.chat_types_filter import ChatTypesFilter

from aiogram.fsm.context import FSMContext

from telegram.keyboard_reply.pvt_enroll_service_actions_kbd import get_pvt_enroll_services_actions_reply_kbd
from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd
from telegram.keyboard_inline.enroll_services_inl_kbd import get_enroll_service_inl_kbd

from telegram.params.messages_helpers import get_service_brief_info_from_record
from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS_PARAMS
from telegram.params.messages_multiline import SELECT_SERVICES_TXT
from telegram.params.select_services_icons import SELECT_SERVICES_ICONS
from telegram.params.messages import (NO_SERVICES,
                                      SELECT_OTHER_ACTIONS)

from database.db_queries.user_queries import get_services_list
from telegram.telegram_utils.enroll_services_utils import get_selected_services_ids

enroll_services_pvt_router = Router(name=__name__)
enroll_services_pvt_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_pvt_router.message(
    F.text == MAIN_MENU_BUTTONS_PARAMS.ENROLL_SERVICES)
async def enroll_services_btn_handler(message: Message, state: FSMContext):
    all_services_records = get_services_list()

    if not all_services_records:
        await message.answer(text=NO_SERVICES,
                             reply_markup=get_pvt_main_menu_kbd())
        return

    await message.answer(text=SELECT_SERVICES_TXT)
    # await asyncio.sleep(0.2)

    selected_services_ids = await get_selected_services_ids(state=state)

    all_services_info_dict = {}

    for service in all_services_records:
        service_brief_text = get_service_brief_info_from_record(service)

        if service.id in selected_services_ids:
            same_id_count = selected_services_ids.count(service.id)
            inline_button_icon = f"{SELECT_SERVICES_ICONS.SELECTED} " *  same_id_count
            button_selected = True
            one_more_service_btn = True

        else:
            inline_button_icon = SELECT_SERVICES_ICONS.NO_ICON
            button_selected = False
            one_more_service_btn = False

        await message.answer(
            text=f"{inline_button_icon} {service_brief_text}",
            reply_markup=get_enroll_service_inl_kbd(service.id,
                                                    button_selected,
                                                    one_more_service_btn))
        # await asyncio.sleep(0.2)

        all_services_info_dict[service.id] = {
            "text": service_brief_text,
            "price": service.price,
            "duration": service.time_duration}

    await state.update_data(all_services_info_state=all_services_info_dict)

    await message.answer(
        text=SELECT_OTHER_ACTIONS,
        reply_markup=get_pvt_enroll_services_actions_reply_kbd())
