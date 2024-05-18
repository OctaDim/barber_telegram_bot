from aiogram import Router, F
from aiogram.types import Message

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.params.buttons_main_menu import MAIN_MENU_BUTTONS_PARAMS
from telegram.keyboard_reply.pvt_main_menu_kbd import get_pvt_main_menu_kbd
from telegram.keyboard_inline.select_services_inl_kbd import get_select_services_inl_kbd
from telegram.params.messages import NO_SERVICES, SELECT_SERVICES


from database.db_queries.user_queries import get_services_list
from telegram.params.select_services_icons import SELECT_SERVICES_ICONS


enroll_services_pvt_router = Router(name=__name__)
enroll_services_pvt_router.message.filter(ChatTypesFilter(["private"]))


@enroll_services_pvt_router.message(
    F.text == MAIN_MENU_BUTTONS_PARAMS.ENROLL_SERVICES)
async def enroll_services_btn_handler(message: Message):

    all_services_db_records = get_services_list()

    if not all_services_db_records:
        await message.answer(text=NO_SERVICES,
                             reply_markup=get_pvt_main_menu_kbd())
        return

    all_services_buttons_data = []

    for service in all_services_db_records:
        service_button_data = {}

        service_button_text= (f"{service.name} - "
                              f"{service.price} руб  "
                              f"({service.time_duration})")

        service_button_data["icon"] = SELECT_SERVICES_ICONS.UNSELECTED
        service_button_data["text"] = service_button_text
        service_button_data["callback_data"] = (f"{service_button_text}"
                                                f"_@callback@")
        all_services_buttons_data.append(service_button_data)

    await message.answer(
        text=SELECT_SERVICES,
        reply_markup=get_select_services_inl_kbd(all_services_buttons_data))
