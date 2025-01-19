from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from database.db_queries.all_services_by_work_time_id_query import get_all_services_by_work_time_id
from telegram.filters.chat_types_filter import IsAdmin
from telegram.keyboard_inline.timetable_get_all_services_inl_kbd import get_all_services
from telegram.keyboard_inline.timetable_get_month_inl_kbd import timetable_get_month_inl_kbd
from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS
from telegram.params.timetable_cb_data_message import SELECT_A_MONTH

from sqlalchemy_utils.types.phone_number import PhoneNumber

from utilities.service_time_format import get_time_duration_for_admin_preview

timetable_admin_btn_router = Router(name=__name__)
timetable_admin_btn_router.message.filter(IsAdmin())


class Timetable(StatesGroup):
    current_time_start_work_day = State()
    current_time_end_work_day = State()
    time_start_slot = State()
    time_end_slot = State()
    time_duration_slot = State()
    work_time_obj = State()
    work_time_id = State()
    name_new_client = State()
    phone_new_client = State()
    date_day = State()
    reserved_slot = State()


@timetable_admin_btn_router.message(F.text == MAIN_MANU_ADMIN_PARAMS.TIMETABLE)
async def get_inl_kbd_add_work_time(message: Message, state: FSMContext):
    await message.answer(
        text=SELECT_A_MONTH,
        reply_markup=timetable_get_month_inl_kbd(
            month=message.date.month,
            year=message.date.year,
            telegram_id=message.from_user.id),
        parse_mode=ParseMode.MARKDOWN
    )

    await state.clear()


async def add_name_new_client(
        message: Message,
        state: FSMContext,
        bot: Bot
):
    await bot.edit_message_text(
        message_id=message.message_id,
        chat_id=message.chat.id,
        text='Введите имя нового клиента'
    )

    await state.set_state(Timetable.name_new_client)


@timetable_admin_btn_router.message(StateFilter(Timetable.name_new_client))
async def add_phone_new_client(
        message: Message,
        state: FSMContext,
):
    await state.update_data(name_new_client=message.text)

    await message.answer(text='Введите номер телефона нового клиента')

    await state.set_state(Timetable.phone_new_client)


@timetable_admin_btn_router.message(StateFilter(Timetable.phone_new_client))
async def validate_phone_client(
        message: Message,
        state: FSMContext
):
    phone = message.text

    phone = PhoneNumber(raw_number=phone, region='BY')

    if not phone.is_valid_number():
        await message.answer(text='Введите корректный номер телефона')
        return

    await state.update_data(phone_new_client=phone.international)

    state_data = await state.get_data()

    services = get_all_services_by_work_time_id(work_time_id=state_data.get('work_time_id'))

    await message.answer(text='Выберите услугу на которую хотите записать клиента')

    messages_id = []

    for service in services:
        total_seconds = service.time_duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        time_duration = get_time_duration_for_admin_preview(
            hours=hours,
            minutes=minutes
        )

        message = await message.answer(text=f'Name: {service.name}\n'
                                            f'Description: {service.description}\n'
                                            f'Time duration: {time_duration}\n'
                                            f'Price: {service.price}\n',
                                       reply_markup=get_all_services(
                                           id_service=service.id,
                                           quantity=len(services)
                                       )
                                       )

        messages_id.append(message.message_id)

    return await state.update_data(messages_id=messages_id)
